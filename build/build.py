# Builds the website from src/:
#   preview/site.html, preview/site-bg.html   one-file previews to open from your computer (#/ links)
#   dist/en, dist/bg                          the live sites for drvasileva.co.uk and drvasileva.bg
# Run from anywhere:  NODE_PATH=$(npm root -g) python3 build/build.py
import json, os, re, shutil, subprocess, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = f'{REPO}/build'        # build scripts
SRC = f'{REPO}/src'        # website source
sys.path.insert(0, B)
import blog
from routes import BG_SLUGS, BLOG_KEY, DOMAINS, EN_SLUGS
s = open(f'{SRC}/home.html').read()
extra = open(f'{SRC}/extra.css').read()
pages = open(f'{SRC}/pages.js').read()
logo_sym = open(f'{SRC}/logo-symbol.txt').read()


def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (n, a[:90])
    s = s.replace(a, b)


# ---- head
rep('<title>Dr Vasileva – Psychologist & CBT Psychotherapist</title>', '''<title>Dr Vasileva – Psychologist & CBT Psychotherapist</title>
<link rel="canonical" href="https://drvasileva.co.uk/">
<link rel="alternate" hreflang="en-GB" href="https://drvasileva.co.uk/">
<link rel="alternate" hreflang="bg" href="https://drvasileva.bg/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Dr Vasileva">
<meta property="og:title" content="Dr Vasileva – Psychologist & CBT Psychotherapist">
<meta property="og:description" content="Online and in-person sessions in Bulgarian and English for adults, couples, families, children and teenagers.">
<meta property="og:url" content="https://drvasileva.co.uk/">
<meta property="og:image" content="https://drvasileva.co.uk/images/og-en.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_GB">
<meta property="og:locale:alternate" content="bg_BG">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://drvasileva.co.uk/images/og-en.png">''')
rep('<link rel="icon" href="../public/images/favicon.svg" type="image/svg+xml">', '''<link rel="icon" href="../public/images/favicon.ico" sizes="any">
<link rel="icon" href="../public/images/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../public/images/apple-touch-icon.png">
<link rel="manifest" href="../public/site.webmanifest">\n<script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" async defer></script>''')

# ---- CSS
s = s.replace('</style>', extra + '''
  .nav-links a[aria-current]::after { content: ""; position: absolute; left: 50%; bottom: 3px; width: 4px; height: 4px; border-radius: 50%; background: currentColor; transform: translateX(-50%); }
</style>''', 1)

# ---- icons
rep('  <symbol id="b-whatsapp"', logo_sym + '''
  <symbol id="i-cloud" viewBox="0 0 24 24"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></symbol>
  <symbol id="i-flame" viewBox="0 0 24 24"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></symbol>
  <symbol id="i-zap" viewBox="0 0 24 24"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/></symbol>
  <symbol id="i-pen" viewBox="0 0 24 24"><path d="M12 20h9M16.38 3.62a1 1 0 0 1 3 3L7.37 18.64a2 2 0 0 1-.86.5l-2.87.84a.5.5 0 0 1-.62-.62l.84-2.87a2 2 0 0 1 .5-.86z"/></symbol>
  <symbol id="i-card" viewBox="0 0 24 24"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></symbol>
  <symbol id="i-pin" viewBox="0 0 24 24"><path d="M20 10c0 4.99-5.54 10.19-7.4 11.8a1 1 0 0 1-1.2 0C9.54 20.19 4 14.99 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></symbol>
  <symbol id="i-phone-off" viewBox="0 0 24 24"><path d="M10.68 13.31a16 16 0 0 0 3.41 2.6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7 2 2 0 0 1 1.72 2v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.42 19.42 0 0 1-3.33-2.67m-2.67-3.34a19.79 19.79 0 0 1-3.07-8.63A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91M22 2 2 22"/></symbol>
  <symbol id="i-send" viewBox="0 0 24 24"><path d="M14.54 21.69a.5.5 0 0 0 .94-.03l6.5-19a.5.5 0 0 0-.64-.63l-19 6.5a.5.5 0 0 0-.02.93l7.93 3.18a2 2 0 0 1 1.11 1.11zM21.85 2.15 10.91 13.09"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></symbol>
  <symbol id="i-down" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></symbol>
  <symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7.5"/><path d="m20.5 20.5-4.2-4.2"/></symbol>
  <symbol id="i-link" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></symbol>
  <symbol id="b-whatsapp"''')

# ---- logo
rep('<span class="name">Dr Vasileva</span>', '<svg class="wordmark" role="img" aria-label="Dr Vasileva"><use href="#logo"/></svg>', 2)
rep('<div class="bigname" aria-hidden="true">Dr Vasileva</div>', '<div class="bigname" aria-hidden="true"><svg><use href="#logo"/></svg></div>')

# ---- links
rep('<a class="logo" href="#top" aria-label="Dr Vasileva – home">', '<a class="logo" href="#/" aria-label="Dr Vasileva – home">')
rep('<a class="logo" href="#top">', '<a class="logo" href="#/">')
rep('''      <li><a href="#about">About me</a></li>
      <li><a href="#who">Who I help</a></li>
      <li><a href="#">What I help with</a></li>
      <li><a href="#articles">Articles</a></li>
      <li><a href="#">FAQ</a></li>''', '''      <li><a href="#/about">About me</a></li>
      <li><a href="#/who-i-help">Who I help</a></li>
      <li><a href="#/issues">What I help with</a></li>
      <li><a href="#/articles">Articles</a></li>
      <li><a href="#/faq">FAQ</a></li>''')
rep('<a class="btn btn-cream roll" href="#contact">', '<a class="btn btn-cream roll" href="#/contact">')
for t, h, i in [('Home', '#/', 0), ('About me', '#/about', 1), ('Who I help', '#/who-i-help', 2), ('What I help with', '#/issues', 3),
                ('Articles', '#/articles', 4), ('FAQ', '#/faq', 5), ('Contact', '#/contact', 6)]:
    s, n = re.subn(r'<li><a href="[^"]*" data-close style="--i:%d">%s</a></li>' % (i, re.escape(t)), f'<li><a href="{h}" data-close style="--i:{i}">{t}</a></li>', s)
    assert n == 1, t
slugs = ['adults', 'couples-families', 'children-teens', 'special-educational-needs', 'group-sessions', 'organisations']
it = iter(slugs)
s, n = re.subn(r'<a class="card" href="#"', lambda m: f'<a class="card" href="#/who-i-help/{next(it)}"', s)
assert n == 6
rep('<a class="btn btn-green" href="#" data-reveal style="--d:.35s">More about me', '<a class="btn btn-green" href="#/about" data-reveal style="--d:.35s">More about me')
rep('<ul><li><a href="#about">About me</a></li><li><a href="#who">Who I help</a></li><li><a href="#">What I help with</a></li><li><a href="#articles">Articles</a></li><li><a href="#">Fees</a></li></ul>',
    '<ul><li><a href="#/about">About me</a></li><li><a href="#/who-i-help">Who I help</a></li><li><a href="#/issues">What I help with</a></li><li><a href="#/articles">Articles</a></li><li><a href="#/publications">Scientific publications</a></li><li><a href="#/fees">Fees</a></li></ul>')
rep('<ul><li><a href="#">FAQ</a></li><li><a href="#">Press</a></li><li><a href="#">Crisis help</a></li><li><a href="#contact">Contact</a></li></ul>',
    '<ul><li><a href="#/faq">FAQ</a></li><li><a href="#/press">Press</a></li><li><a href="#/crisis">Crisis help</a></li><li><a href="#/contact">Contact</a></li></ul>')
rep('<ul><li><a href="#">Privacy</a></li><li><a href="#">Cookies</a></li><li><a href="#">Terms</a></li></ul>',
    '<ul><li><a href="#/privacy">Privacy</a></li><li><a href="#/cookies">Cookies</a></li><li><a href="#/terms">Terms</a></li></ul>')
rep('''      <div class="track-ui">''', '''      <div class="track-ui">
        <a class="btn btn-green" href="#/articles" style="padding:12px 20px;font-size:.9rem">All articles <svg class="icon arrow-i"><use href="#i-arrow"/></svg></a>''')
s, n = re.subn(r'<span class="press-item">(<span class="p-(?:ico|logo)">.*?</small></span>)</span>', r'<a class="press-item" href="#/press" style="text-decoration:none">\1</a>', s)
assert n == 3

# ---- Why work with me: bento
a = s.index('  <!-- Why work with me -->'); b = s.index('  <!-- Quote -->')
s = s[:a] + open(f'{SRC}/why.html').read() + '\n' + s[b:]

# ---- home becomes the "/" page
rep('<main id="top">', '<main id="top">\n<div class="page active" data-route="/">')
rep('</main>', '</div>\n<div id="pages"></div>\n</main>')
rep('<div class="tiles">', '<div class="tiles" id="home-tiles">')

# ---- JS
rep('  const years = new Date().getFullYear() - 2005;', '  const years = new Date().getFullYear() - 2005;\n  const YEARS = years;')
rep("  document.querySelectorAll('[data-reveal], .quote, .about-photo').forEach(el => io.observe(el));", open(f'{SRC}/home-extra.js').read())
s = s.replace('</script>\n</body>', '</script>\n<script>' + pages + '</script>\n</body>', 1)
assert 'const PAGES = {}' in s

# ---- language switch: link to the other language's page, keeping the current page
bg = {}
exec(open(f'{SRC}/bg/pairs.py').read(), bg)
rep('<div class="lang" aria-label="Language"><a href="https://drvasileva.bg/" hreflang="bg" lang="bg">BG</a><a href="#" class="on" aria-current="true">EN</a></div>', bg['LANG_EN'], 2)


# =====================================================================
# Bulgarian version
# =====================================================================
b = s
def swap(start, end, file):
    global b
    i = b.index(start); j = b.index(end, i)
    assert b.count(start) == 1, start
    b = b[:i] + open(f'{SRC}/bg/{file}').read() + b[j:]
swap('  const WHO = [', '  /* =====================================================================\n     Building blocks', 'data1.js')
swap('  const ctaButtons = `', '  const faqList =', 'blocks.js')
swap('  /* Extra content for the "Who I help" pages */', '  /* =====================================================================\n     Pages\n', 'data2.js')
swap("  PAGES['/about'] = () => `", '  /* =====================================================================\n     Dropdown menus', 'pages.js')
for en, tr in bg['HEAD']:
    assert b.count(en) == 1, ('HEAD', en[:70])
    b = b.replace(en, tr)
assert b.count(bg['LANG_EN']) == 2
b = b.replace(bg['LANG_EN'], bg['LANG_BG'])
missing = [en for en, tr in bg['PAIRS'] if en not in b]
assert not missing, ('not found', missing)
for en, tr in bg['PAIRS']:
    b = b.replace(en, tr)

# =====================================================================
# Articles (blog): pages and cards made by build/blog.py from content/
# =====================================================================
topics, posts = blog.load()


def with_blog(html, lang, mode):
    # The home page's articles row (window.POSTS) and, in the previews, the blog's pages (window.BLOG_PAGES)
    b_ = blog.Blog(lang, topics, posts, mode)
    data = {'POSTS': b_.feed()}
    if mode == 'preview':
        data['BLOG_PAGES'] = {k: inner for k, (inner, _) in b_.pages().items()}
    js = ''.join(f'window.{k} = {json.dumps(v, ensure_ascii=False)};' for k, v in data.items()).replace('</', '<\\/')
    marker = '<script>document.documentElement.classList.add'
    assert html.count(marker) == 1
    return html.replace(marker, f'<script>{js}</script>\n{marker}')


open(f'{REPO}/preview/site.html', 'w').write(with_blog(s, 'en', 'preview'))
open(f'{REPO}/preview/site-bg.html', 'w').write(with_blog(b, 'bg', 'preview'))
print('previews: site.html, site-bg.html')

# =====================================================================
# Deployable sites: dist/en (drvasileva.co.uk) and dist/bg (drvasileva.bg)
# =====================================================================
def for_server(html):
    # Paths become absolute (served from the domain root) and the language switch links to the other domain
    html = html.replace('../public/', '/')
    html = html.replace('href="site-bg.html" data-base="site-bg.html"', f'href="{DOMAINS["bg"]}" data-base="{DOMAINS["bg"]}"')
    html = html.replace('href="site.html" data-base="site.html"', f'href="{DOMAINS["en"]}" data-base="{DOMAINS["en"]}"')
    assert '../' not in html and 'site-bg.html' not in html and '"site.html"' not in html
    return html


def not_found(html):
    # Same app, but it opens on the 404 view; <base> makes every link go back to the domain root
    return html.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<base href="/">\n<meta name="robots" content="noindex">\n<script>window.NOT_FOUND = true</script>', 1)


SLUGS = {'en': (EN_SLUGS, BG_SLUGS), 'bg': (BG_SLUGS, EN_SLUGS)}
# The blog's posts get addresses too, so links like #/articles/<id> become /articles/<slug> or /statii/<slug>
POST_SLUGS = {lang: {f"{BLOG_KEY}/{p['id']}": blog.Blog(lang, topics, posts).post_path(p) for p in posts} for lang in ('en', 'bg')}


def check_cta(out, lang):
    # The blog writes its own "Ready to talk?" band; make sure it still matches the one in src/
    page = open(f"{out}{SLUGS[lang][0]['/fees']}/index.html").read()
    site = re.search(r'<div class="cta-box[^>]*>(.*?)</div></div></section>', page, re.S).group(1)
    mine = re.search(r'<div class="cta-box[^>]*>(.*?)</div></div></section>', blog.Blog(lang, topics, posts).cta_band(), re.S).group(1)
    norm = lambda h: (re.findall(r'href="([^"]*)"', h), re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', h)).strip())
    assert norm(site) == norm(mine), ('blog.py cta_band() no longer matches src/ – update UI in blog.py', norm(site), norm(mine))


for lang, html in (('en', s), ('bg', b)):
    out = f'{REPO}/dist/{lang}'
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(f'{REPO}/public', out)          # images, icons, site.webmanifest
    own, other = SLUGS[lang]
    own = {**own, **POST_SLUGS[lang]}
    other = {**other, **POST_SLUGS['bg' if lang == 'en' else 'en']}
    page = for_server(with_blog(html, lang, 'live')).replace('<script>document.documentElement.classList.add', '<script>window.SLUGS = ' + json.dumps(own) + '; window.OTHER_SLUGS = ' + json.dumps(other) + ';</script>\n<script>document.documentElement.classList.add', 1)
    assert 'window.SLUGS' in page
    open(f'{out}/index.html', 'w').write(page)
    open(f'{out}/404.html', 'w').write(not_found(page))
    open(f'{out}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAINS[lang]}sitemap.xml\nSitemap: {DOMAINS[lang]}sitemap-articles.xml\n')
    app_pages = [k for k in SLUGS[lang][0] if k != BLOG_KEY]      # the blog writes its own pages and sitemap
    urls = ''.join(f'  <url><loc>{DOMAINS[lang].rstrip("/")}{own[k]}</loc>'
                   f'<xhtml:link rel="alternate" hreflang="en-GB" href="{DOMAINS["en"].rstrip("/")}{EN_SLUGS[k]}"/>'
                   f'<xhtml:link rel="alternate" hreflang="bg" href="{DOMAINS["bg"].rstrip("/")}{BG_SLUGS[k]}"/></url>\n' for k in app_pages)
    open(f'{out}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + '</urlset>\n')
    # Save every page as its own HTML file (needs Node + Playwright on the machine that builds)
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as routes_file:
        json.dump([[k, own[k]] for k in app_pages], routes_file)
    subprocess.run(['node', f'{B}/prerender.js', out, routes_file.name], check=True)
    os.unlink(routes_file.name)
    check_cta(out, lang)
    blog_pages = blog.write_site(lang, f'{out}/index.html', out)
    print(f'dist/{lang}: index.html, 404.html, {len(blog_pages)} article pages, posts.json, robots.txt, sitemaps')
