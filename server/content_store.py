"""The editor's posts on the server: saving, versions, the bin, topics, cover photos and publishing.

The posts live outside the git folder (ADMIN_CONTENT_DIR), so `git pull` never touches her work.
On the first start they are copied from the repository's content/ folder.

Publishing writes the blog's pages for both sites into BLOG_OUT_DIR/en and BLOG_OUT_DIR/bg, using the
site's own page shell from SITE_DIST_DIR; nginx serves the Articles addresses from there.
"""
import io
import json
import os
import re
import shutil
import threading
import time

import blog

ENV = os.environ
REPO = blog.REPO
DATA_DIR = ENV.get('ADMIN_DATA_DIR', '/var/lib/drvasileva-admin')
CONTENT = ENV.get('ADMIN_CONTENT_DIR', os.path.join(DATA_DIR, 'content'))
SEED = os.path.join(REPO, 'content')
BLOG_OUT = ENV.get('BLOG_OUT_DIR', '/var/www/drvasileva-blog')
DIST = ENV.get('SITE_DIST_DIR', os.path.join(REPO, 'dist'))
POSTS = os.path.join(CONTENT, 'posts')
BIN = os.path.join(CONTENT, 'bin')
KEEP_VERSIONS, BIN_DAYS = 30, 30
MAX_PHOTO = 10 * 1024 * 1024
MAX_PIXELS = 40_000_000
LIMITS = dict(title=200, summary=400, slug=80, cover_alt=200, body=100_000)
ID_RE = re.compile(r'[a-z0-9-]{1,80}')
STAMP_RE = re.compile(r'\d{8}-\d{6}-\d{6}')
lock = threading.RLock()           # one change at a time


class EditError(ValueError):
    """Something she can fix; the message is shown in the editor."""


def stamp():
    t = time.time()
    return time.strftime('%Y%m%d-%H%M%S', time.localtime(t)) + f'-{int(t % 1 * 1e6):06d}'


def stamp_time(s):
    return time.mktime(time.strptime(s[:15], '%Y%m%d-%H%M%S'))


# ---------------------------------------------------------------------------
# Start-up
# ---------------------------------------------------------------------------
def init():
    with lock:
        if not os.path.isdir(POSTS):
            os.makedirs(CONTENT, exist_ok=True)
            shutil.copytree(SEED, CONTENT, dirs_exist_ok=True)
        os.makedirs(BIN, exist_ok=True)
        purge_bin()
        publish_site()


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------
def topics():
    return blog.load_topics(CONTENT)


def folder_of(pid):
    if not ID_RE.fullmatch(pid or ''):
        raise EditError('No such post.')
    f = os.path.join(POSTS, pid)
    if not os.path.isfile(os.path.join(f, 'post.json')):
        raise EditError('No such post.')
    return f


def get(pid):
    return blog.read_post(folder_of(pid), topics(), strict=False)


def list_posts():
    t = topics()
    out = []
    for pid in sorted(os.listdir(POSTS)):
        f = os.path.join(POSTS, pid)
        if ID_RE.fullmatch(pid) and os.path.isfile(os.path.join(f, 'post.json')):
            p = blog.read_post(f, t, strict=False)
            p['saved'] = os.path.getmtime(os.path.join(f, 'post.json'))
            out.append(p)
    # drafts without a date first, then newest first
    return sorted(out, key=lambda p: (p['date'] or '9999', p['saved']), reverse=True)


# ---------------------------------------------------------------------------
# Saving
# ---------------------------------------------------------------------------
def one_line(v, n):
    return ' '.join(str(v or '').split())[:n]


def clean(fields):
    """What came from the form, trimmed to safe sizes. Header fields are kept on one line."""
    t = {x['id'] for x in topics()}
    out = dict(topic=fields.get('topic') if fields.get('topic') in t else None,
               date=one_line(fields.get('date'), 10), bgben=one_line(fields.get('bgben'), 300), text={})
    for lang in blog.LANGS:
        x = {k: one_line(fields.get(f'{lang}_{k}'), LIMITS[k]) for k in ('title', 'summary', 'slug', 'cover_alt')}
        x['slug'] = blog.slugify(x['slug'])          # empty: filled in by save()
        body = str(fields.get(f'{lang}_body') or '').replace('\r\n', '\n')
        x['body'] = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', body)[:LIMITS['body']].strip()
        out['text'][lang] = x
    return out


def new_id(data):
    base = blog.slugify(data['text']['en']['slug'] or data['text']['en']['title']) or blog.slugify(data['text']['bg']['slug'] or data['text']['bg']['title']) or 'post'
    pid, n = base[:70], 2
    while os.path.exists(os.path.join(POSTS, pid)) or any(x.startswith(pid + '--') for x in os.listdir(BIN)):
        pid, n = f'{base[:66]}-{n}', n + 1
    return pid


def snapshot(folder):
    """Keep a copy of the post as it is now (unchanged photos are linked, not copied)."""
    if not os.path.isfile(os.path.join(folder, 'post.json')):
        return
    vdir = os.path.join(folder, 'versions', stamp())
    os.makedirs(vdir)
    for name in os.listdir(folder):
        src = os.path.join(folder, name)
        if os.path.isfile(src):
            try:
                os.link(src, os.path.join(vdir, name))
            except OSError:
                shutil.copy2(src, vdir)
    versions = sorted(os.listdir(os.path.join(folder, 'versions')))
    for old in versions[:-KEEP_VERSIONS]:
        shutil.rmtree(os.path.join(folder, 'versions', old), ignore_errors=True)


def write_files(folder, meta, data):
    tmp = os.path.join(folder, 'post.json.tmp')
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    os.replace(tmp, os.path.join(folder, 'post.json'))
    for lang in blog.LANGS:
        x = data['text'][lang]
        blog.write_text_file(os.path.join(folder, f'{lang}.md'),
                             {k: x[k] for k in ('title', 'slug', 'summary', 'cover_alt')}, x['body'])


def restore_files(folder, vdir):
    for name in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, name)):
            os.remove(os.path.join(folder, name))
    for name in os.listdir(vdir):
        shutil.copy2(os.path.join(vdir, name), folder)


def save(pid, fields, action='save', photo=None, remove_photo=False):
    """Save a post (pid None = new). action: save | publish | unpublish. Returns the post id.
    A published post only changes on the site if the change can be published; otherwise nothing changes."""
    data = clean(fields)
    if not data['topic']:
        raise EditError('Please choose a topic.')
    if data['date'] and not re.fullmatch(r'\d{4}(-\d{2}(-\d{2})?)?', data['date']):
        raise EditError('The date must look like 2026-09-19 (or 2026-09, or 2026).')
    if data['bgben'] and not re.fullmatch(r'https://(www\.)?bgben\.co\.uk/\S+', data['bgben']):
        raise EditError('The BG BEN link must start with https://bgben.co.uk/')
    if not any(data['text'][l]['title'] for l in blog.LANGS):
        raise EditError('Please give the post a title first.')
    image = process_photo(photo) if photo else None
    with lock:
        if pid is None:
            pid = new_id(data)
            os.makedirs(os.path.join(POSTS, pid))
            meta = {'status': 'draft'}
        else:
            meta = json.load(open(os.path.join(folder_of(pid), 'post.json'), encoding='utf-8'))
        folder = os.path.join(POSTS, pid)
        was_published = meta.get('status') == 'published'
        # Web addresses: an empty field keeps the post's current address (so links never break);
        # a post without one gets it from its title
        for lang in blog.LANGS:
            x = data['text'][lang]
            if not x['slug']:
                path = os.path.join(folder, f'{lang}.md')
                current = blog.read_text_file(path)[0].get('slug') if os.path.isfile(path) else ''
                x['slug'] = current or blog.slugify(x['title'])
        snapshot(folder)
        vdir = None
        if os.path.isdir(os.path.join(folder, 'versions')):
            vdir = os.path.join(folder, 'versions', sorted(os.listdir(os.path.join(folder, 'versions')))[-1])
        old_cover = meta.get('cover')
        meta.update(topic=data['topic'], date=data['date'] or meta.get('date') or '', bgben=data['bgben'] or None)   # empty date: keep it
        if image:
            meta['cover'] = f'cover-{os.urandom(4).hex()}.jpg'
            open(os.path.join(folder, meta['cover']), 'wb').write(image)
        elif remove_photo:
            meta['cover'] = None
        if meta.get('cover') != old_cover and old_cover and os.path.isfile(os.path.join(folder, old_cover)):
            os.remove(os.path.join(folder, old_cover))          # still kept in the version just made
        if action == 'publish':
            meta['status'] = 'published'
            meta['date'] = meta['date'] or time.strftime('%Y-%m-%d')
        elif action == 'unpublish':
            meta['status'] = 'draft'
        write_files(folder, meta, data)
        if meta['status'] == 'published' or was_published:
            try:
                blog.load(CONTENT)                                  # every published post must still be buildable
            except blog.PostError as e:
                reason = str(e).split(': ', 1)[-1]
                if was_published and vdir:
                    restore_files(folder, vdir)                     # the live post stays as it was
                    raise EditError(f'Not saved, because the published post would be incomplete: {reason}. '
                                    'Fix this and save again, or unpublish the post first.')
                meta['status'] = 'draft'
                write_files(folder, meta, data)
                err = EditError(f'Saved as a draft, but it can’t be published yet: {reason}.')
                err.pid = pid                                       # the text is saved: show the post
                raise err
            publish_site()
    return pid


# ---------------------------------------------------------------------------
# Versions and the bin
# ---------------------------------------------------------------------------
def versions(pid):
    vroot = os.path.join(folder_of(pid), 'versions')
    if not os.path.isdir(vroot):
        return []
    out = []
    for v in sorted(os.listdir(vroot), reverse=True):
        if STAMP_RE.fullmatch(v):
            head, _ = blog.read_text_file(os.path.join(vroot, v, 'bg.md')) if os.path.isfile(os.path.join(vroot, v, 'bg.md')) else ({}, '')
            head_en, _ = blog.read_text_file(os.path.join(vroot, v, 'en.md')) if os.path.isfile(os.path.join(vroot, v, 'en.md')) else ({}, '')
            meta = json.load(open(os.path.join(vroot, v, 'post.json'), encoding='utf-8'))
            out.append(dict(id=v, time=stamp_time(v), title=head.get('title') or head_en.get('title', ''), status=meta.get('status')))
    return out


def restore_version(pid, v):
    folder = folder_of(pid)
    if not STAMP_RE.fullmatch(v or '') or not os.path.isdir(os.path.join(folder, 'versions', v)):
        raise EditError('No such version.')
    with lock:
        current = json.load(open(os.path.join(folder, 'post.json'), encoding='utf-8')).get('status')
        snapshot(folder)
        vdir = os.path.join(folder, 'versions', v)
        restore_files(folder, vdir)
        meta = json.load(open(os.path.join(folder, 'post.json'), encoding='utf-8'))
        if meta.get('status') != current:      # restoring the text never publishes or unpublishes by itself
            meta['status'] = current
            with open(os.path.join(folder, 'post.json'), 'w', encoding='utf-8') as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
        if current == 'published':
            try:
                blog.load(CONTENT)
            except blog.PostError as e:
                restore_files(folder, os.path.join(folder, 'versions', sorted(os.listdir(os.path.join(folder, 'versions')))[-1]))
                raise EditError(f'That version can’t be published as it is: {str(e).split(": ", 1)[-1]}. Unpublish the post first to restore it.')
            publish_site()


def delete(pid):
    folder = folder_of(pid)
    with lock:
        was_published = json.load(open(os.path.join(folder, 'post.json'), encoding='utf-8')).get('status') == 'published'
        os.rename(folder, os.path.join(BIN, f'{pid}--{stamp()}'))
        if was_published:
            publish_site()


def list_bin():
    out = []
    for name in sorted(os.listdir(BIN), reverse=True):
        m = re.fullmatch(r'([a-z0-9-]{1,80})--(\d{8}-\d{6}-\d{6})', name)
        if m:
            head, _ = blog.read_text_file(os.path.join(BIN, name, 'bg.md')) if os.path.isfile(os.path.join(BIN, name, 'bg.md')) else ({}, '')
            out.append(dict(name=name, id=m.group(1), deleted=stamp_time(m.group(2)), title=head.get('title') or m.group(1),
                            purge=stamp_time(m.group(2)) + BIN_DAYS * 86400))
    return out


def restore_bin(name):
    m = re.fullmatch(r'([a-z0-9-]{1,80})--(\d{8}-\d{6}-\d{6})', name or '')
    if not m or not os.path.isdir(os.path.join(BIN, name)):
        raise EditError('No such post in the bin.')
    with lock:
        target = os.path.join(POSTS, m.group(1))
        if os.path.exists(target):
            raise EditError('A post with the same name exists again. Rename or delete that one first.')
        os.rename(os.path.join(BIN, name), target)
        meta = json.load(open(os.path.join(target, 'post.json'), encoding='utf-8'))
        if meta.get('status') == 'published':                # comes back as a draft, to be checked before publishing
            meta['status'] = 'draft'
            with open(os.path.join(target, 'post.json'), 'w', encoding='utf-8') as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
    return m.group(1)


def purge_bin():
    now = time.time()
    for b in list_bin():
        if b['purge'] < now:
            shutil.rmtree(os.path.join(BIN, b['name']), ignore_errors=True)


# ---------------------------------------------------------------------------
# Topics
# ---------------------------------------------------------------------------
def save_topics(rows, new=None, remove=None):
    """rows: {id: {en, bg, colour, icon}} for the existing topics; new: the same for a new one; remove: an id."""
    with lock:
        current = topics()
        used = {p['topic'] for p in list_posts()}
        out = []
        for t in current:
            if t['id'] == remove:
                if t['id'] in used:
                    raise EditError('This topic still has posts. Move them to another topic first.')
                continue
            r = rows.get(t['id'], {})
            t = dict(t, en=one_line(r.get('en'), 60) or t['en'], bg=one_line(r.get('bg'), 60) or t['bg'],
                     colour=r.get('colour') if r.get('colour') in blog.COLOURS else t['colour'],
                     icon=r.get('icon') if r.get('icon') in blog.ICONS else t['icon'])
            out.append(t)
        if new and (new.get('en') or new.get('bg')):
            en, bg = one_line(new.get('en'), 60), one_line(new.get('bg'), 60)
            if not en or not bg:
                raise EditError('A new topic needs both an English and a Bulgarian name.')
            tid = blog.slugify(en) or blog.slugify(bg)
            if any(t['id'] == tid for t in out):
                raise EditError('There is already a topic with this name.')
            out.append(dict(id=tid, en=en, bg=bg, colour=new.get('colour') if new.get('colour') in blog.COLOURS else blog.COLOURS[len(out) % len(blog.COLOURS)],
                            icon=new.get('icon') if new.get('icon') in blog.ICONS else 'i-leaf'))
        tmp = os.path.join(CONTENT, 'topics.json.tmp')
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump({'topics': out}, f, ensure_ascii=False, indent=2)
        os.replace(tmp, os.path.join(CONTENT, 'topics.json'))
        publish_site()


# ---------------------------------------------------------------------------
# Cover photos
# ---------------------------------------------------------------------------
def process_photo(raw):
    """Redraw the photo: removes everything hidden in the file (including the phone's GPS location),
    turns it the right way up and makes it a web-sized JPEG. Anything that isn't a photo is refused."""
    if len(raw) > MAX_PHOTO:
        raise EditError('The photo is too large (more than 10 MB).')
    try:
        from PIL import Image, ImageOps
    except ImportError:
        raise EditError('Photos need the Pillow library on the server: apt install python3-pil') from None
    Image.MAX_IMAGE_PIXELS = MAX_PIXELS
    try:
        with Image.open(io.BytesIO(raw)) as probe:             # reads only the header, not the picture
            if probe.format not in ('JPEG', 'PNG', 'WEBP'):
                raise EditError('Please upload a JPG, PNG or WebP photo.')
            if probe.size[0] * probe.size[1] > MAX_PIXELS:     # a small file that would unpack to a huge picture
                raise EditError('The photo has too many pixels. Please use a photo of at most 40 megapixels.')
            probe.verify()
        with Image.open(io.BytesIO(raw)) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode not in ('RGB', 'L'):
                bg = Image.new('RGB', im.size, (250, 247, 242))
                im = im.convert('RGBA')
                bg.paste(im, mask=im.split()[-1])
                im = bg
            im = im.convert('RGB')
            im.thumbnail((2000, 2000))
            out = io.BytesIO()
            im.save(out, 'JPEG', quality=85, optimize=True, progressive=True)     # no EXIF, no GPS, no comments
            return out.getvalue()
    except EditError:
        raise
    except Exception:          # noqa: BLE001  (a broken or disguised file)
        raise EditError('That file could not be read as a photo.') from None


# ---------------------------------------------------------------------------
# Publishing and previews
# ---------------------------------------------------------------------------
def publish_site():
    """Rebuild the blog pages of both sites from the posts here."""
    with lock:
        for lang in blog.LANGS:
            blog.write_site(lang, os.path.join(DIST, lang, 'index.html'), os.path.join(BLOG_OUT, lang), CONTENT, swap=True)


def preview(pid, lang):
    """The post's page exactly as it would look on the site, with the site's scripts removed."""
    t = topics()
    post = get(pid)
    for l in blog.LANGS:
        x = post['text'][l]
        x['title'] = x['title'] or '(no title yet)'
        x['slug'] = x['slug'] or 'preview'
    post['date'] = post['date'] or time.strftime('%Y-%m-%d')
    try:
        _, published = blog.load(CONTENT)
    except blog.PostError:
        published = []
    posts = [post] + [p for p in published if p['id'] != pid]
    b = blog.Blog(lang, t, posts)
    key = f'{blog.BLOG_KEY}/{pid}'
    inner, info = b.pages()[key]
    shell = open(os.path.join(DIST, lang, 'index.html'), encoding='utf-8').read()
    page = blog.static_page(shell, key, inner, info, lang)
    page = re.sub(r'<script\b[^>]*>.*?</script>', '', page, flags=re.S | re.I)
    if post['cover']:          # the preview can't send the sign-in cookie, so the photo travels inside the page
        import base64
        data = base64.b64encode(open(os.path.join(post['folder'], post['cover']), 'rb').read()).decode()
        page = page.replace(b.cover_src(post), 'data:image/jpeg;base64,' + data)
    banner = ('<div style="position:fixed;z-index:9999;left:50%;top:12px;transform:translateX(-50%);background:#8E79A6;color:#fff;'
              'font:600 14px/1.2 Manrope,system-ui,sans-serif;padding:10px 18px;border-radius:999px;box-shadow:0 8px 24px rgba(0,0,0,.25)">'
              + ('Preview – this is how the post will look' if post['status'] == 'draft' else 'Preview of your latest saved changes') + '</div>')
    i = page.index('>', page.index('<body')) + 1
    return page[:i] + banner + page[i:]
