"""The blog: turns the posts in content/ into the Articles pages of both sites.

Used by build/build.py when the site is built, and later by the editor on the server,
so it only needs Python's standard library.

content/topics.json                 the topics, with English and Bulgarian names
content/posts/<id>/post.json        what both languages share: topic, date, status, BG BEN link, cover photo
content/posts/<id>/en.md, bg.md     the text in each language (a few header lines, then the text)

Text formatting (the only formatting allowed; everything else shows as plain text).
The editor shows this as real formatting; it is only stored like this:
  ## Heading   ### Smaller heading   **bold**   *italic*   ++underline++   [link text](https://…)
  {lilac|coloured text} (colours: see TEXT_COLOURS)   - list item   1. numbered item   > quote
"""
import html
import json
import os
import re
import shutil
import urllib.parse

from routes import BLOG_KEY, DOMAINS, SLUGS

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ('en', 'bg')
COLOURS = ('sage', 'lilac', 'gold', 'forest', 'plum', 'sand')    # cover colours a topic can use (see extra.css)
ICONS = ('i-sun', 'i-heart', 'i-smile', 'i-leaf', 'i-puzzle', 'i-globe', 'i-feather')
TEXT_COLOURS = ('green', 'lilac', 'gold', 'rose')                    # text colours (see extra.css .tc-*)
PER_PAGE = 12                                                     # cards shown before "Show more"
# Reading speed, in words per minute, of an adult reading non-fiction silently (Brysbaert 2019, a review of
# 190 studies: 238 for English). The same text in Bulgarian takes about 5% fewer, slightly longer words
# (measured on her 18 columns in both languages), so the same reading time works out at about 225.
READING_WPM = {'en': 238, 'bg': 225}

UI = {
    'en': dict(home='Home', crumbs='Breadcrumb', articles='Articles', eyebrow='Articles', title='School of <em>Psychology</em>',
               lead='Practical psychology for everyday life: my articles and my column in BG BEN, the newspaper for Bulgarians in the UK.',
               all='All', filter='Filter by topic', more='Show more articles', min_read='{} min read', column='BG BEN column',
               search='Search the articles', search_ph='Search by title, topic or any word…', clear='Clear the search',
               year='Year', all_years='All years', kind='Type', all_kinds='All types', kind_article='Articles', kind_column='BG BEN columns',
               order='Order', newest='Newest first', oldest='Oldest first', count_one='1 article', count_many='{} articles',
               none='No articles match your search.', reset='Clear the search and filters',
               read_full='Read the full column on BG BEN (in Bulgarian)', read_pdf='Read the full column on BG BEN (PDF, in Bulgarian)',
               originally='Originally published in BG BEN, “School of Psychology”', share='Share', copy='Copy link', copied='Link copied',
               related='You might also <em>like</em>', author='Dr Mirena Vasileva',
               author_text='Psychologist and CBT psychotherapist. Since 2005 I have worked with adults, couples, children and families, online and in person, in Bulgarian and English.',
               author_btn='Get in touch', pubs='Looking for my research? See my <a href="{}">scientific publications</a>.',
               suffix=' – Dr Vasileva', site='Dr Vasileva', locale='en-GB',
               cta_title='Ready to <em>talk</em>?', cta_text='Call or message me in Bulgarian or English. We’ll find a time that suits you.', call='Call',
               months=('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')),
    'bg': dict(home='Начало', crumbs='Навигационна пътека', articles='Статии', eyebrow='Статии', title='Училище по <em>психология</em>',
               lead='Практична психология за всеки ден: моите статии и рубриката ми в БГ БЕН – вестникът на българите във Великобритания.',
               all='Всички', filter='Филтър по тема', more='Още статии', min_read='{} мин. четене', column='Рубрика в БГ БЕН',
               search='Търсене в статиите', search_ph='Търсете по заглавие, тема или дума…', clear='Изчисти търсенето',
               year='Година', all_years='Всички години', kind='Вид', all_kinds='Всички видове', kind_article='Статии', kind_column='Рубрики в БГ БЕН',
               order='Подредба', newest='Първо най-новите', oldest='Първо най-старите', count_one='1 статия', count_many='{} статии',
               none='Няма статии, които да отговарят на търсенето.', reset='Изчисти търсенето и филтрите',
               read_full='Прочетете цялата рубрика в БГ БЕН', read_pdf='Прочетете цялата рубрика в БГ БЕН (PDF)',
               originally='Публикувано за първи път в БГ БЕН, „Училище по психология“', share='Споделете', copy='Копирай връзката', copied='Връзката е копирана',
               related='Може да Ви <em>харесат</em>', author='д-р Мирена Василева',
               author_text='Психолог и когнитивно-поведенчески психотерапевт. От 2005 г. работя с възрастни, двойки, деца и семейства – онлайн и на живо, на български и английски.',
               author_btn='Свържете се с мен', pubs='Търсите научните ми трудове? Вижте <a href="{}">научните публикации</a>.',
               suffix=' – д-р Василева', site='д-р Василева', locale='bg',
               cta_title='Готови ли сте за <em>разговор</em>?', cta_text='Обадете се или ми пишете на български или английски. Ще намерим удобно за Вас време.', call='Обаждане',
               months=('януари', 'февруари', 'март', 'април', 'май', 'юни', 'юли', 'август', 'септември', 'октомври', 'ноември', 'декември')),
}


class PostError(ValueError):
    """A post or topic that can't be published; the message says what to fix."""


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------
esc = html.escape

BG_LATIN = dict(zip('абвгдежзийклмнопрстуфхцчшщъьюя',
                    ['a', 'b', 'v', 'g', 'd', 'e', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'h',
                     'ts', 'ch', 'sh', 'sht', 'a', 'y', 'yu', 'ya']))


def slugify(text):
    """Web address from a title, with Bulgarian letters written in Latin: 'Покана за щастие' -> 'pokana-za-shtastie'."""
    text = ''.join(BG_LATIN.get(c, c) for c in text.lower())
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')[:80].strip('-')


def _inline(text):
    t = esc(text, quote=True)
    t = re.sub(r'\[([^\]\n]+)\]\(((?:https?://|mailto:)[^\s)]+)\)',
               lambda m: f'<a href="{m.group(2)}"{"" if m.group(2).startswith("mailto:") else " target=\"_blank\" rel=\"noopener\""}>{m.group(1)}</a>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])', r'<em>\1</em>', t)
    t = re.sub(r'\+\+(?!\s)(.+?)(?<!\s)\+\+', r'<u>\1</u>', t)
    t = re.sub(r'\{(' + '|'.join(TEXT_COLOURS) + r')\|([^{}\n]+)\}', r'<span class="tc-\1">\2</span>', t)
    return t


def render_text(text):
    """The post text as HTML. Everything is escaped first, so only the formatting above becomes HTML."""
    out = []
    for block in re.split(r'\n\s*\n', text.replace('\r\n', '\n').strip()):
        lines = [l.rstrip() for l in block.split('\n') if l.strip()]
        if not lines:
            continue
        first = lines[0]
        if first.startswith('### '):
            out.append(f'<h3>{_inline(first[4:])}</h3>')
            lines = lines[1:]
        elif first.startswith('## '):
            out.append(f'<h2>{_inline(first[3:])}</h2>')
            lines = lines[1:]
        if not lines:
            continue
        if all(re.match(r'[-*] ', l) for l in lines):
            out.append('<ul>' + ''.join(f'<li>{_inline(l[2:])}</li>' for l in lines) + '</ul>')
        elif all(re.match(r'\d+[.)] ', l) for l in lines):
            first = int(re.match(r'\d+', lines[0]).group())          # a list after a paragraph can carry on: 2., 3. …
            start = f' start="{first}"' if 1 < first < 10000 else ''
            out.append(f'<ol{start}>' + ''.join(f'<li>{_inline(l.split(" ", 1)[1])}</li>' for l in lines) + '</ol>')
        elif all(l.startswith('>') for l in lines):
            out.append('<blockquote><p>' + '<br>'.join(_inline(l[1:].strip()) for l in lines) + '</p></blockquote>')
        else:
            out.append('<p>' + '<br>'.join(_inline(l) for l in lines) + '</p>')
    return '\n'.join(out)


def plain_text(text):
    """The words of a post's text, without the formatting marks: links keep their words, colours their text."""
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'\{(?:' + '|'.join(TEXT_COLOURS) + r')\|', '', text)
    return ' '.join(re.findall(r'\w+(?:[-’\']\w+)*', text))


def plain_words(text):
    return len(plain_text(text).split())


def reading_minutes(text, lang):
    """Minutes to read the text, to the nearest minute (at least 1)."""
    return max(1, int(plain_words(text) / READING_WPM[lang] + 0.5))


def format_date(date, lang):
    """'2026-09-19' -> '19 September 2026' / '19 септември 2026 г.'; '2025-12' -> 'December 2025'; '2025' -> '2025'."""
    parts = [int(p) for p in date.split('-')]
    m = UI[lang]['months']
    if len(parts) == 1:
        return str(parts[0])
    text = f'{m[parts[1] - 1]} {parts[0]}' if len(parts) == 2 else f'{parts[2]} {m[parts[1] - 1]} {parts[0]}'
    return text + (' г.' if lang == 'bg' else '')


# ---------------------------------------------------------------------------
# Reading the content folder
# ---------------------------------------------------------------------------
def read_text_file(path):
    """A language file: header lines ('title: …') between two '---' lines, then the text."""
    raw = open(path, encoding='utf-8').read().replace('\r\n', '\n')
    m = re.match(r'---\n(.*?)\n---\n?(.*)\Z', raw, re.S)
    if not m:
        raise PostError(f'{path}: must start with a header between two "---" lines')
    head = {}
    for line in m.group(1).split('\n'):
        if line.strip():
            key, sep, value = line.partition(':')
            if not sep:
                raise PostError(f'{path}: header line without ":": {line!r}')
            head[key.strip()] = value.strip()
    return head, m.group(2).strip()


def write_text_file(path, head, body):
    """The opposite of read_text_file. Header values are kept on one line, so they can't break the file."""
    lines = [f'{k}: {" ".join(str(v).split())}' for k, v in head.items() if v]
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write('---\n' + '\n'.join(lines) + '\n---\n' + body.replace('\r\n', '\n').strip() + '\n')
    os.replace(tmp, path)


def load_topics(content_dir):
    topics = json.load(open(os.path.join(content_dir, 'topics.json'), encoding='utf-8'))['topics']
    by_id = {}
    for t in topics:
        if not re.fullmatch(r'[a-z0-9-]+', t.get('id', '')) or t['id'] in by_id:
            raise PostError(f'topic id {t.get("id")!r} is missing, repeated or not in lowercase letters')
        if not t.get('en') or not t.get('bg'):
            raise PostError(f'topic {t["id"]}: needs an English and a Bulgarian name')
        if t.get('colour') not in COLOURS or t.get('icon') not in ICONS:
            raise PostError(f'topic {t["id"]}: unknown colour or icon')
        by_id[t['id']] = t
    return topics


def read_post(folder, topics, strict=True):
    """One post folder. strict=True checks everything a published page needs; strict=False (the editor's
    drafts) fills in what's missing, so an unfinished post can still be listed, edited and previewed."""
    pid = os.path.basename(folder)
    by_id = {t['id']: t for t in topics}
    if not re.fullmatch(r'[a-z0-9-]+', pid):
        raise PostError(f'post folder {pid!r}: use lowercase letters, numbers and "-" only')
    meta = json.load(open(os.path.join(folder, 'post.json'), encoding='utf-8'))
    problems = []
    if meta.get('status') not in ('draft', 'published'):
        problems.append('status must be "draft" or "published"')
    if meta.get('topic') not in by_id:
        problems.append('choose a topic')
    if not re.fullmatch(r'\d{4}(-\d{2}(-\d{2})?)?', meta.get('date') or ''):
        problems.append('the date must look like 2026-09-19 (or 2026-09, or 2026)')
    if meta.get('bgben') and not re.fullmatch(r'https://(www\.)?bgben\.co\.uk/\S+', meta['bgben']):
        problems.append('the BG BEN link must be an https://bgben.co.uk/… address')
    cover = meta.get('cover')
    if cover and (not re.fullmatch(r'[a-z0-9-]+\.(jpg|png|webp)', cover) or not os.path.isfile(os.path.join(folder, cover))):
        problems.append(f'cover photo {cover!r} not found')
        cover = None
    post = dict(id=pid, topic=meta.get('topic') if meta.get('topic') in by_id else topics[0]['id'],
                date=meta.get('date') or '', status=meta.get('status', 'draft'), bgben=meta.get('bgben') or None,
                cover=cover, folder=folder, text={})
    for lang in LANGS:
        path = os.path.join(folder, f'{lang}.md')
        head, body = read_text_file(path) if os.path.isfile(path) else ({}, '')
        name = 'English' if lang == 'en' else 'Bulgarian'
        for field, said in (('title', 'title'), ('summary', 'short description'), ('slug', 'web address')):
            if not head.get(field):
                problems.append(f'{name}: the {said} is missing')
        if head.get('slug') and not re.fullmatch(r'[a-z0-9-]+', head['slug']):
            problems.append(f'{name}: the web address may only use lowercase Latin letters, numbers and "-"')
        if not body and not post['bgben']:
            problems.append(f'{name}: the text is empty')
        post['text'][lang] = dict(title=head.get('title', ''), summary=head.get('summary', ''), slug=head.get('slug', ''),
                                  cover_alt=head.get('cover_alt', ''), body=body)
    if strict and problems:
        raise PostError(f'{pid}: ' + '; '.join(problems))
    post['problems'] = problems
    return post


def load(content_dir=os.path.join(REPO, 'content'), include_drafts=False):
    """Topics and published posts (newest first), checked so that every page can be built."""
    topics = load_topics(content_dir)
    posts, seen = [], {lang: {} for lang in LANGS}
    root = os.path.join(content_dir, 'posts')
    for pid in sorted(os.listdir(root)):
        folder = os.path.join(root, pid)
        if not os.path.isdir(folder):
            continue
        status = json.load(open(os.path.join(folder, 'post.json'), encoding='utf-8')).get('status')
        if status == 'draft' and not include_drafts:
            continue
        post = read_post(folder, topics)
        for lang in LANGS:
            slug = post['text'][lang]['slug']
            if slug in seen[lang]:
                raise PostError(f'{pid} ({lang.upper()}): web address {slug!r} is already used by {seen[lang][slug]}')
            seen[lang][slug] = pid
        posts.append(post)
    posts.sort(key=lambda p: (p['date'], p['id']), reverse=True)
    return topics, posts


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def contact_links():
    """Phone, WhatsApp and Viber links, read from the site's own source so they can't drift apart."""
    src = open(os.path.join(REPO, 'src', 'pages.js'), encoding='utf-8').read()
    return dict(re.findall(r"\b(TEL|WA|VIBER) = '([^']*)'", src))


class Blog:
    """The blog of one language. mode 'live' makes real addresses (/articles/…); 'preview' makes #/ links
    and ../ paths for the one-file previews."""

    def __init__(self, lang, topics, posts, mode='live'):
        self.lang, self.mode, self.ui = lang, mode, UI[lang]
        self.other = 'bg' if lang == 'en' else 'en'
        self.topics = {t['id']: t for t in topics}
        self.posts = posts
        self.contact = contact_links()

    # --- addresses
    def path(self, key, lang=None):
        """Address of a site page (route key) on this or the other site."""
        return SLUGS[lang or self.lang][key]

    def post_path(self, post, lang=None):
        lang = lang or self.lang
        return f"{SLUGS[lang][BLOG_KEY]}/{post['text'][lang]['slug']}"

    def href(self, key=None, post=None):
        """A link inside the site, as the current mode needs it."""
        if self.mode == 'preview':
            return '#' + (f"{BLOG_KEY}/{post['id']}" if post else key)
        return self.post_path(post) if post else self.path(key)

    def absolute(self, path, lang=None):
        return DOMAINS[lang or self.lang].rstrip('/') + path

    def asset(self, path):
        """path under public/, e.g. 'images/dr-vasileva.jpg'"""
        return ('../public/' if self.mode == 'preview' else '/') + path

    def cover_src(self, post):
        if self.mode == 'preview':
            return f"../content/posts/{post['id']}/{post['cover']}"
        return f"/images/posts/{post['id']}/{post['cover']}"

    # --- building blocks
    @staticmethod
    def ic(name, cls='icon'):
        return f'<svg class="{cls}"><use href="#{name}"/></svg>'

    def hero(self, crumbs, eyebrow, title, lead='', icon='', extra=''):
        c = ''.join(f'<span><a href="{h}">{t}</a></span>' if h else f'<span>{t}</span>' for t, h in crumbs)
        return f'''
    <section class="page-hero grain on-dark">
      <span class="blob b1"></span><span class="blob b2"></span>
      {f'<svg class="icon hero-icon"><use href="#{icon}"/></svg>' if icon else ''}
      <div class="wrap">
        <nav class="crumbs" aria-label="{self.ui['crumbs']}"><a href="{self.href('/')}">{self.ui['home']}</a>{c}</nav>
        <span class="eyebrow" data-reveal>{eyebrow}</span>
        <h1 data-reveal style="--d:.05s">{title}</h1>
        {f'<p class="lead" data-reveal style="--d:.12s">{lead}</p>' if lead else ''}{extra}
      </div>
    </section>'''

    def cta_band(self):
        c, ic = self.contact, self.ic
        return f'''
    <section class="cta-band"><div class="wrap"><div class="cta-box grain on-dark" data-reveal>
      <div><h2>{self.ui['cta_title']}</h2><p>{self.ui['cta_text']}</p></div>
      <div class="btn-row">
    <a class="btn btn-whatsapp" href="{c['WA']}">{ic('b-whatsapp', 'bi')}WhatsApp</a>
    <a class="btn btn-viber" href="{c['VIBER']}">{ic('b-viber', 'bi')}Viber</a>
    <a class="btn btn-cream" href="{c['TEL']}">{ic('i-phone')}{self.ui['call']}</a></div>
    </div></div></section>'''

    def topic_name(self, post):
        return esc(self.topics[post['topic']][self.lang])

    def cover(self, post, big=False):
        t = self.topics[post['topic']]
        if post['cover']:
            alt = esc(post['text'][self.lang]['cover_alt'])
            art = f'<img src="{self.cover_src(post)}" alt="{alt}" loading="{"eager" if big else "lazy"}">'
        else:
            art = f'<span class="bg"></span>{self.ic(t["icon"], "icon motif")}'
        return art + f'<span class="label">{esc(t[self.lang])}</span>'

    def meta_line(self, post, column=True):
        parts = [f'<time datetime="{post["date"]}">{format_date(post["date"], self.lang)}</time>']
        if post['bgben'] and column:
            parts.append(f'<span>{self.ui["column"]}</span>')
        parts.append(f'<span class="read-time">{self.ui["min_read"].format(reading_minutes(post["text"][self.lang]["body"], self.lang))}</span>')
        return '<span class="dot">·</span>'.join(parts)

    def card(self, post, featured=False, search=False):
        t, x = self.topics[post['topic']], post['text'][self.lang]
        extra = ''
        if search:            # what the Articles page's search and filters look at
            words = ' '.join((x['title'], x['summary'], t[self.lang], plain_text(x['body']))).lower()
            extra = (f' data-date="{esc(post["date"])}" data-year="{post["date"][:4]}" data-kind="{"column" if post["bgben"] else "article"}"'
                     f' data-text="{esc(words)}"')
        return f'''<a class="article c-{t['colour']}{' featured' if featured else ''}" data-tag="{t['id']}" href="{self.href(post=post)}"{extra} data-reveal>
        <div class="top">{self.cover(post)}</div>
        <div class="body"><h3>{esc(x['title'])}</h3><p class="sum">{esc(x['summary'])}</p><div class="meta"><span class="when">{self.meta_line(post, column=False)}</span>{self.ic('i-arrow')}</div></div>
      </a>'''

    # --- the two kinds of page (inner HTML of the page)
    def list_page(self):
        used = [t for t in self.topics.values() if any(p['topic'] == t['id'] for p in self.posts)]
        tabs = f'<button class="tab" aria-pressed="true" data-filter="all">{self.ui["all"]}</button>' + ''.join(
            f'<button class="tab" aria-pressed="false" data-filter="{t["id"]}">{esc(t[self.lang])}</button>' for t in used)
        cards = '\n      '.join(self.card(p, featured=(i == 0), search=True) for i, p in enumerate(self.posts))
        ui = self.ui
        opt = lambda v, label: f'<option value="{v}">{label}</option>'
        years = sorted({p['date'][:4] for p in self.posts}, reverse=True)
        kinds = {bool(p['bgben']) for p in self.posts}
        selects = [f'<label class="blog-select"><span>{ui["order"]}</span><select data-sort>{opt("new", ui["newest"])}{opt("old", ui["oldest"])}</select></label>']
        if len(years) > 1:
            selects.insert(0, f'<label class="blog-select"><span>{ui["year"]}</span><select data-year>{opt("", ui["all_years"])}{"".join(opt(y, y) for y in years)}</select></label>')
        if len(kinds) > 1:         # only when there are both her own articles and BG BEN columns
            selects.insert(1, f'<label class="blog-select"><span>{ui["kind"]}</span><select data-kind>{opt("", ui["all_kinds"])}'
                              f'{opt("article", ui["kind_article"])}{opt("column", ui["kind_column"])}</select></label>')
        count = ui['count_one'] if len(self.posts) == 1 else ui['count_many'].format(len(self.posts))
        return self.hero([(ui['articles'], None)], ui['eyebrow'], ui['title'], ui['lead'], 'i-feather') + f'''
    <section class="page-body"><div class="wrap">
      <form class="blog-tools" role="search" data-blog-tools data-count-one="{esc(ui['count_one'])}" data-count-many="{esc(ui['count_many'])}" data-reveal>
        <div class="blog-search">
          {self.ic('i-search', 'icon search-i')}
          <label class="sr-only" for="blog-q">{ui['search']}</label>
          <input id="blog-q" type="search" name="q" placeholder="{esc(ui['search_ph'])}" autocomplete="off" enterkeyhint="search" data-q>
          <button class="search-clear" type="button" aria-label="{ui['clear']}" data-clear hidden>×</button>
        </div>
        <div class="blog-selects">{''.join(selects)}</div>
      </form>
      <div class="tabs" role="group" aria-label="{ui['filter']}" data-reveal>{tabs}</div>
      <p class="blog-count" aria-live="polite" data-count>{count}</p>
      <div class="articles-grid blog-grid" data-per-page="{PER_PAGE}">
      {cards}
      </div>
      <div class="blog-empty" data-empty hidden><p>{ui['none']}</p><button class="btn btn-green" type="button" data-reset>{ui['reset']}</button></div>
      <div class="more-row"><button class="btn btn-green more-btn" type="button" hidden>{self.ui['more']}</button></div>
      <p class="pubs-link" data-reveal>{self.ui['pubs'].format(self.href('/publications'))}</p>
    </div></section>''' + self.cta_band()

    def share_links(self, post):
        url = self.absolute(self.post_path(post))
        q = urllib.parse.quote
        text = q(post['text'][self.lang]['title'] + ' ' + url)
        return f'''<div class="share" data-reveal><span>{self.ui['share']}</span>
          <a class="social facebook" href="https://www.facebook.com/sharer/sharer.php?u={q(url, safe='')}" target="_blank" rel="noopener" aria-label="Facebook">{self.ic('b-facebook', 'bi')}</a>
          <a class="social whatsapp" href="https://wa.me/?text={text}" target="_blank" rel="noopener" aria-label="WhatsApp">{self.ic('b-whatsapp', 'bi')}</a>
          <a class="social viber" href="viber://forward?text={text}" aria-label="Viber">{self.ic('b-viber', 'bi')}</a>
          <button class="social copy-link" type="button" data-copy="{esc(url)}" data-done="{self.ui['copied']}" aria-label="{self.ui['copy']}">{self.ic('i-link')}</button>
        </div>'''

    def post_page(self, post, preview=False):
        t, x, ui = self.topics[post['topic']], post['text'][self.lang], self.ui
        meta = f'<p class="post-meta" data-reveal style="--d:.18s">{self.meta_line(post)}</p>'
        body = render_text(x['body'])
        bgben = ''
        if post['bgben']:
            label = ui['read_pdf'] if post['bgben'].lower().endswith('.pdf') else ui['read_full']
            bgben = f'''
          <a class="read-more bgben" href="{esc(post['bgben'])}" target="_blank" rel="noopener" data-reveal>
            <span class="ri"><img src="{self.asset('images/logos/bg-ben.png')}" alt="BG BEN" width="400" height="400" loading="lazy"></span>
            <span><small>{ui['originally']}</small><b>{label}</b></span>{self.ic('i-arrow')}</a>'''
        related = [p for p in self.posts if p['topic'] == post['topic'] and p is not post]
        related += [p for p in self.posts if p['topic'] != post['topic'] and p is not post]
        related_cards = '\n      '.join(self.card(p) for p in related[:3])
        return self.hero([(ui['articles'], self.href(BLOG_KEY)), (esc(t[self.lang]), None)], esc(t[self.lang]),
                         esc(x['title']), esc(x['summary']), extra=meta) + f'''
    <section class="page-body"><div class="wrap post-wrap">
      <figure class="post-cover c-{t['colour']}" data-reveal>{self.cover(post, big=True)}</figure>
      <article class="prose post-text">
        {body}{bgben}
      </article>
      {self.share_links(post)}
      <aside class="author-box" data-reveal>
        <img src="{self.asset('images/dr-vasileva.jpg')}" alt="{ui['author']}" width="1242" height="1242" loading="lazy">
        <div><b>{ui['author']}</b><p>{ui['author_text']}</p>
          <a class="btn btn-green" href="{self.href('/contact')}">{ui['author_btn']} {self.ic('i-arrow', 'icon arrow-i')}</a></div>
      </aside>
    </div></section>''' + ('' if preview else (f'''
    <section class="page-body related"><div class="wrap">
      <h2 data-reveal>{ui['related']}</h2>
      <div class="articles-grid">
      {related_cards}
      </div>
    </div></section>''' if related_cards else '') + self.cta_band())

    def pages(self):
        """route key -> (inner HTML, page details) for the list page and every post"""
        out = {BLOG_KEY: (self.list_page(), dict(
            title=self.ui['articles'] + self.ui['suffix'], description=re.sub('<[^>]+>', '', self.ui['lead']),
            path=self.path(BLOG_KEY), other=self.absolute(self.path(BLOG_KEY, self.other), self.other),
            alternates={l: self.absolute(self.path(BLOG_KEY, l), l) for l in LANGS}, post=None))}
        for p in self.posts:
            x = p['text'][self.lang]
            out[f"{BLOG_KEY}/{p['id']}"] = (self.post_page(p), dict(
                title=x['title'] + self.ui['suffix'], description=x['summary'], path=self.post_path(p),
                other=self.absolute(self.post_path(p, self.other), self.other),
                alternates={l: self.absolute(self.post_path(p, l), l) for l in LANGS}, post=p))
        return out

    def feed(self):
        """Data for the home page's articles row: the topics in use and a ready-made card for each post."""
        used = [t for t in self.topics.values() if any(p['topic'] == t['id'] for p in self.posts)]
        return dict(all=self.ui['all'], topics=[dict(id=t['id'], name=t[self.lang]) for t in used],
                    posts=[dict(id=p['id'], topic=p['topic'], card=self.card(p)) for p in self.posts])


# ---------------------------------------------------------------------------
# Writing the live site
# ---------------------------------------------------------------------------
def _sub_once(pattern, repl, s):
    s2, n = re.subn(pattern, lambda m: repl, s, count=1)
    if n != 1:
        raise RuntimeError(f'page template: {pattern!r} not found')
    return s2


def static_page(shell, key, inner, info, lang):
    """A full HTML page: the site's shell with this page's content and details filled in."""
    ui = UI[lang]
    a = lambda v: esc(v, quote=True)
    post = info['post']
    image = DOMAINS[lang].rstrip('/') + (f"/images/posts/{post['id']}/{post['cover']}" if post and post['cover'] else f'/images/og-{lang}.png')
    page = shell
    page = _sub_once(r'<div class="page active" data-route="/">', '<div class="page" data-route="/">', page)
    page = _sub_once(r'<div id="pages"></div>', f'<div id="pages"><div class="page active" data-route="{key}">{inner}</div></div>', page)
    page = _sub_once(r'<title>[^<]*</title>', f'<title>{esc(info["title"])}</title>', page)
    page = _sub_once(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{a(info["alternates"][lang])}">', page)
    page = _sub_once(r'<link rel="alternate" hreflang="en-GB" href="[^"]*">', f'<link rel="alternate" hreflang="en-GB" href="{a(info["alternates"]["en"])}">', page)
    page = _sub_once(r'<link rel="alternate" hreflang="bg" href="[^"]*">', f'<link rel="alternate" hreflang="bg" href="{a(info["alternates"]["bg"])}">', page)
    page = _sub_once(r'<meta property="og:type" content="[^"]*">', f'<meta property="og:type" content="{"article" if post else "website"}">', page)
    page = _sub_once(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{a(info["title"])}">', page)
    page = _sub_once(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{a(info["description"])}">', page)
    page = _sub_once(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{a(info["alternates"][lang])}">', page)
    page = _sub_once(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{a(image)}">', page)
    page = _sub_once(r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{a(image)}">', page)
    page = _sub_once(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{a(info["description"])}">', page)
    if post and post['cover']:          # the shell's share image is 1200 × 630; a photo can be any size
        page = re.sub(r'<meta property="og:image:(width|height)" content="\d+">\n?', '', page)
    # Language switch: straight to this page in the other language (also without JavaScript)
    switch = f'href="{DOMAINS["bg" if lang == "en" else "en"]}" data-base='
    if switch not in page:
        raise RuntimeError('page template: language switch not found')
    page = page.replace(switch, f'href="{a(info["other"])}" data-base=')      # header and menu
    state = json.dumps(dict(key=key, url=info['path'], other=info['other'], title=info['title']), ensure_ascii=False).replace('</', '<\\/')
    page = _sub_once(r'<script>window\.SLUGS', f'<script>window.STATIC_PAGE = {state};</script>\n<script>window.SLUGS', page)
    if post:
        x = post['text'][lang]
        ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': x['title'], 'description': x['summary'],
              'inLanguage': ui['locale'], 'image': image, 'mainEntityOfPage': info['alternates'][lang],
              'author': {'@type': 'Person', 'name': UI[lang]['author'], 'url': DOMAINS[lang].rstrip('/') + SLUGS[lang]['/about']}}
        if len(post['date']) == 10:
            ld['datePublished'] = post['date']
        ld_json = json.dumps(ld, ensure_ascii=False).replace('</', '<\\/')
        page = _sub_once(r'</head>', f'<script type="application/ld+json">{ld_json}</script>\n</head>', page)
    return page


def write_site(lang, shell_path, out_dir, content_dir=os.path.join(REPO, 'content'), swap=False):
    """Write the blog pages, cover photos, posts.json and sitemap-articles.xml of one language into out_dir.
    swap=True (the editor's own folder, which holds only the blog): build next to it, then switch over
    in one step, so visitors never see a half-written blog."""
    if swap:
        tmp = out_dir.rstrip('/') + '.new'
        shutil.rmtree(tmp, ignore_errors=True)
        os.makedirs(tmp)
        pages = write_site(lang, shell_path, tmp, content_dir)
        old = out_dir.rstrip('/') + '.old'
        shutil.rmtree(old, ignore_errors=True)
        if os.path.isdir(out_dir):
            os.rename(out_dir, old)
        os.rename(tmp, out_dir)
        shutil.rmtree(old, ignore_errors=True)
        return pages
    topics, posts = load(content_dir)
    blog = Blog(lang, topics, posts)
    shell = open(shell_path, encoding='utf-8').read()
    blog_dir = os.path.join(out_dir, SLUGS[lang][BLOG_KEY].strip('/'))
    shutil.rmtree(blog_dir, ignore_errors=True)
    shutil.rmtree(os.path.join(out_dir, 'images', 'posts'), ignore_errors=True)
    pages = blog.pages()
    for key, (inner, info) in pages.items():
        target = os.path.join(out_dir, info['path'].strip('/'), 'index.html')
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, 'w', encoding='utf-8').write(static_page(shell, key, inner, info, lang))
    for p in posts:
        if p['cover']:
            dest = os.path.join(out_dir, 'images', 'posts', p['id'])
            os.makedirs(dest, exist_ok=True)
            shutil.copy(os.path.join(p['folder'], p['cover']), dest)
    json.dump(blog.feed(), open(os.path.join(out_dir, 'posts.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    urls = ''.join(
        f'  <url><loc>{esc(info["alternates"][lang])}</loc>'
        f'<xhtml:link rel="alternate" hreflang="en-GB" href="{esc(info["alternates"]["en"])}"/>'
        f'<xhtml:link rel="alternate" hreflang="bg" href="{esc(info["alternates"]["bg"])}"/></url>\n' for _, info in pages.values())
    open(os.path.join(out_dir, 'sitemap-articles.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + '</urlset>\n')
    return pages
