"""The blog: turns the posts in content/ into the Articles pages of both sites.

Used by build/build.py when the site is built, and later by the editor on the server,
so it only needs Python's standard library.

content/topics.json                 the topics, with English and Bulgarian names
content/posts/<id>/post.json        what both languages share: topic, date, status, BG BEN link, cover photo
content/posts/<id>/en.md, bg.md     the text in each language (a few header lines, then the text)

Text formatting (the only formatting allowed; everything else shows as plain text):
  ## Heading   ### Smaller heading   **bold**   *italic*   [link text](https://…)
  - list item   1. numbered item   > quote
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
PER_PAGE = 12                                                     # cards shown before "Show more"

UI = {
    'en': dict(home='Home', crumbs='Breadcrumb', articles='Articles', eyebrow='Articles', title='School of <em>Psychology</em>',
               lead='Practical psychology for everyday life: my articles and my column in BG BEN, the newspaper for Bulgarians in the UK.',
               all='All', filter='Filter by topic', more='Show more articles', min_read='{} min read', column='BG BEN column',
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
            out.append('<ol>' + ''.join(f'<li>{_inline(l.split(" ", 1)[1])}</li>' for l in lines) + '</ol>')
        elif all(l.startswith('>') for l in lines):
            out.append('<blockquote><p>' + '<br>'.join(_inline(l[1:].strip()) for l in lines) + '</p></blockquote>')
        else:
            out.append('<p>' + '<br>'.join(_inline(l) for l in lines) + '</p>')
    return '\n'.join(out)


def plain_words(text):
    return len(re.findall(r'\w+', re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)))


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


def load(content_dir=os.path.join(REPO, 'content'), include_drafts=False):
    """Topics and published posts (newest first), checked so that every page can be built."""
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

    posts, seen = [], {lang: {} for lang in LANGS}
    root = os.path.join(content_dir, 'posts')
    for pid in sorted(os.listdir(root)):
        folder = os.path.join(root, pid)
        if not os.path.isdir(folder):
            continue
        if not re.fullmatch(r'[a-z0-9-]+', pid):
            raise PostError(f'post folder {pid!r}: use lowercase letters, numbers and "-" only')
        meta = json.load(open(os.path.join(folder, 'post.json'), encoding='utf-8'))
        if meta.get('status') not in ('draft', 'published'):
            raise PostError(f'{pid}: status must be "draft" or "published"')
        if meta['status'] == 'draft' and not include_drafts:
            continue
        if meta.get('topic') not in by_id:
            raise PostError(f'{pid}: unknown topic {meta.get("topic")!r}')
        if not re.fullmatch(r'\d{4}(-\d{2}(-\d{2})?)?', meta.get('date', '')):
            raise PostError(f'{pid}: date must look like 2026-09-19 (or 2026-09, or 2026)')
        if meta.get('bgben') and not re.fullmatch(r'https://(www\.)?bgben\.co\.uk/\S+', meta['bgben']):
            raise PostError(f'{pid}: the BG BEN link must be an https://bgben.co.uk/… address')
        cover = meta.get('cover')
        if cover and (not re.fullmatch(r'[a-z0-9-]+\.(jpg|png|webp)', cover) or not os.path.isfile(os.path.join(folder, cover))):
            raise PostError(f'{pid}: cover photo {cover!r} not found')
        post = dict(id=pid, topic=meta['topic'], date=meta['date'], status=meta['status'], bgben=meta.get('bgben'),
                    cover=cover, folder=folder, text={})
        for lang in LANGS:
            path = os.path.join(folder, f'{lang}.md')
            if not os.path.isfile(path):
                raise PostError(f'{pid}: the {lang.upper()} version is missing (every post needs both languages)')
            head, body = read_text_file(path)
            for field in ('title', 'summary', 'slug'):
                if not head.get(field):
                    raise PostError(f'{pid} ({lang.upper()}): "{field}" is missing')
            if not re.fullmatch(r'[a-z0-9-]+', head['slug']):
                raise PostError(f'{pid} ({lang.upper()}): the slug may only use lowercase Latin letters, numbers and "-"')
            if head['slug'] in seen[lang]:
                raise PostError(f'{pid} ({lang.upper()}): slug {head["slug"]!r} is already used by {seen[lang][head["slug"]]}')
            seen[lang][head['slug']] = pid
            if not body and not post['bgben']:
                raise PostError(f'{pid} ({lang.upper()}): the text is empty')
            post['text'][lang] = dict(title=head['title'], summary=head['summary'], slug=head['slug'],
                                      cover_alt=head.get('cover_alt', ''), body=body)
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

    def meta_line(self, post):
        words = plain_words(post['text'][self.lang]['body'])
        extra = self.ui['column'] if post['bgben'] else self.ui['min_read'].format(max(1, round(words / 200)))
        return f'<time datetime="{post["date"]}">{format_date(post["date"], self.lang)}</time><span class="dot">·</span><span>{extra}</span>'

    def card(self, post, featured=False):
        t, x = self.topics[post['topic']], post['text'][self.lang]
        return f'''<a class="article c-{t['colour']}{' featured' if featured else ''}" data-tag="{t['id']}" href="{self.href(post=post)}" data-reveal>
        <div class="top">{self.cover(post)}</div>
        <div class="body"><h3>{esc(x['title'])}</h3><p class="sum">{esc(x['summary'])}</p><div class="meta"><span class="when">{self.meta_line(post)}</span>{self.ic('i-arrow')}</div></div>
      </a>'''

    # --- the two kinds of page (inner HTML of the page)
    def list_page(self):
        used = [t for t in self.topics.values() if any(p['topic'] == t['id'] for p in self.posts)]
        tabs = f'<button class="tab" aria-pressed="true" data-filter="all">{self.ui["all"]}</button>' + ''.join(
            f'<button class="tab" aria-pressed="false" data-filter="{t["id"]}">{esc(t[self.lang])}</button>' for t in used)
        cards = '\n      '.join(self.card(p, featured=(i == 0)) for i, p in enumerate(self.posts))
        return self.hero([(self.ui['articles'], None)], self.ui['eyebrow'], self.ui['title'], self.ui['lead'], 'i-feather') + f'''
    <section class="page-body"><div class="wrap">
      <div class="tabs" role="group" aria-label="{self.ui['filter']}" data-reveal>{tabs}</div>
      <div class="articles-grid blog-grid" data-per-page="{PER_PAGE}">
      {cards}
      </div>
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

    def post_page(self, post):
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
    </div></section>''' + (f'''
    <section class="page-body related"><div class="wrap">
      <h2 data-reveal>{ui['related']}</h2>
      <div class="articles-grid">
      {related_cards}
      </div>
    </div></section>''' if related_cards else '') + self.cta_band()

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


def write_site(lang, shell_path, out_dir, content_dir=os.path.join(REPO, 'content')):
    """Write the blog pages, cover photos, posts.json and sitemap-articles.xml of one language into out_dir."""
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
