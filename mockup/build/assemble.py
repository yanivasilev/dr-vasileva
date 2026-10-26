import os, re

B = os.path.dirname(os.path.abspath(__file__))
REPO = '/home/user/dr-vasileva'
s = open(f'{REPO}/mockup/home.html').read()
extra = open(f'{B}/extra.css').read()
pages = open(f'{B}/pages.js').read()
logo_sym = open(f'{B}/logo-symbol.txt').read()


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
rep('<link rel="icon" href="../images/favicon.svg" type="image/svg+xml">', '''<link rel="icon" href="../images/favicon.ico" sizes="any">
<link rel="icon" href="../images/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../images/apple-touch-icon.png">
<link rel="manifest" href="../site.webmanifest">\n<script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" async defer></script>''')

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
    '<ul><li><a href="#/about">About me</a></li><li><a href="#/who-i-help">Who I help</a></li><li><a href="#/issues">What I help with</a></li><li><a href="#/articles">Articles</a></li><li><a href="#/fees">Fees</a></li></ul>')
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
s = s[:a] + open(f'{B}/why.html').read() + '\n' + s[b:]

# ---- home becomes the "/" page
rep('<main id="top">', '<main id="top">\n<div class="page active" data-route="/">')
rep('</main>', '</div>\n<div id="pages"></div>\n</main>')
rep('<div class="tiles">', '<div class="tiles" id="home-tiles">')

# ---- JS
rep('  const years = new Date().getFullYear() - 2005;', '  const years = new Date().getFullYear() - 2005;\n  const YEARS = years;')
rep("  document.querySelectorAll('[data-reveal], .quote, .about-photo').forEach(el => io.observe(el));", open(f'{B}/home-extra.js').read())
s = s.replace('</script>\n</body>', '</script>\n<script>' + pages + '</script>\n</body>', 1)
assert 'const PAGES = {}' in s

# ---- language switch: link to the other language's page, keeping the current page
bg = {}
exec(open(f'{B}/bg/pairs.py').read(), bg)
rep('<div class="lang" aria-label="Language"><a href="https://drvasileva.bg/" hreflang="bg" lang="bg">BG</a><a href="#" class="on" aria-current="true">EN</a></div>', bg['LANG_EN'], 2)
s = s.replace('</script>\n</body>', """  // Keep the same page when switching language (preview: the two files; live site: the two domains)
  const syncLang = () => document.querySelectorAll('.lang a[data-base]').forEach(a => a.href = a.dataset.base + location.hash);
  addEventListener('hashchange', syncLang);
  syncLang();
</script>\n</body>""", 1)

open(f'{REPO}/mockup/site.html', 'w').write(s)
print('site.html', len(s))

# =====================================================================
# Bulgarian version
# =====================================================================
b = s
def swap(start, end, file):
    global b
    i = b.index(start); j = b.index(end, i)
    assert b.count(start) == 1, start
    b = b[:i] + open(f'{B}/bg/{file}').read() + b[j:]
swap('  const WHO = [', '  /* =====================================================================\n     Building blocks', 'data1.js')
swap('  const ctaButtons = `', '  const faqList =', 'blocks.js')
swap('  /* Extra content for the "Who I help" pages */', '  /* =====================================================================\n     Pages\n', 'data2.js')
swap("  PAGES['/about'] = () => `", '  function articleCards()', 'pages.js')
for en, tr in bg['HEAD']:
    assert b.count(en) == 1, ('HEAD', en[:70])
    b = b.replace(en, tr)
assert b.count(bg['LANG_EN']) == 2
b = b.replace(bg['LANG_EN'], bg['LANG_BG'])
missing = [en for en, tr in bg['PAIRS'] if en not in b]
assert not missing, ('not found', missing)
for en, tr in bg['PAIRS']:
    b = b.replace(en, tr)
open(f'{REPO}/mockup/site-bg.html', 'w').write(b)
print('site-bg.html', len(b))
