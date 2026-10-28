"""The editor's screens (HTML). Everything shown is escaped; the only script is /editor.js."""
import hashlib
import html
import os
import time

import blog

esc = html.escape
APP = 'Dr Vasileva editor'
LANG_NAMES = {'bg': 'Български', 'en': 'English'}
COLOUR_NAMES = dict(sage='Sage green', lilac='Lilac', gold='Gold', forest='Forest green', plum='Plum', sand='Sand')
ICON_NAMES = {'i-sun': 'Sun', 'i-heart': 'Heart', 'i-smile': 'Smile', 'i-leaf': 'Leaf', 'i-puzzle': 'Puzzle', 'i-globe': 'Globe', 'i-feather': 'Feather'}


def when(t):
    return time.strftime('%d %b %Y, %H:%M', time.localtime(t))


CSS = """
:root { --green: #4F6F52; --green-dark: #344E38; --green-deep: #2C4430; --cream: #FAF7F2; --sand: #EDE6DA; --line: #D9D2C5; --lilac: #B9A3C9; --lilac-deep: #8E79A6; --muted: #5E625D; --red: #A4423A; --white: #fff; }
* { box-sizing: border-box; }
body { margin: 0; font-family: Manrope, system-ui, sans-serif; color: #232823; background: var(--cream); line-height: 1.6; -webkit-font-smoothing: antialiased; }
h1, h2, h3 { font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 600; line-height: 1.1; color: var(--green-deep); margin: 0 0 .4em; }
h2 { font-size: 1.7rem; } h3 { font-size: 1.35rem; }
a { color: var(--green-dark); }
[hidden] { display: none !important; }
.word { font-weight: 600; letter-spacing: .32em; font-size: .9rem; color: inherit; text-decoration: none; white-space: nowrap; }
.login { min-height: 100vh; display: grid; place-items: center; padding: 24px; background: radial-gradient(circle at 20% 10%, #4F6F52, #2C4430 60%); }
.card { width: 100%; max-width: 420px; background: var(--white); border-radius: 22px; padding: 36px 32px; box-shadow: 0 30px 60px -30px rgba(0,0,0,.5); }
.card .word { display: block; color: var(--green-deep); margin-bottom: 26px; }
.card h1 { font-size: 2.2rem; }
.card p.sub { color: var(--muted); margin: 0 0 22px; font-size: .95rem; }
label { display: block; font-weight: 600; font-size: .88rem; margin: 18px 0 6px; color: var(--green-deep); }
label small, .hint { font-weight: 500; color: var(--muted); font-size: .82rem; }
.hint { display: block; margin-top: 4px; }
input[type=password], input[type=text], input[type=url], select, textarea { width: 100%; font: inherit; font-size: 1rem; padding: 12px 14px; border: 1px solid var(--line); border-radius: 12px; background: var(--white); color: inherit; }
.login input { background: var(--cream); }
textarea { min-height: 380px; line-height: 1.7; resize: vertical; }
textarea.short { min-height: 0; }
input:focus, select:focus, textarea:focus { outline: 2px solid var(--lilac); outline-offset: 1px; border-color: var(--lilac-deep); }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; font: inherit; font-weight: 700; font-size: .95rem; padding: 12px 22px; border-radius: 999px; border: 0; cursor: pointer; background: var(--green-dark); color: var(--white); text-decoration: none; white-space: nowrap; }
.btn:hover { filter: brightness(1.1); }
.btn.wide { width: 100%; margin-top: 24px; }
.btn.light { background: rgba(250,247,242,.12); color: var(--cream); border: 1px solid rgba(250,247,242,.25); padding: 9px 18px; }
.btn.outline { background: var(--white); color: var(--green-deep); border: 1px solid var(--line); }
.btn.lilac { background: var(--lilac-deep); }
.btn.danger { background: var(--white); color: var(--red); border: 1px solid #E7C9C5; }
.btn.small { padding: 7px 14px; font-size: .84rem; }
.error, .ok { border-radius: 12px; padding: 12px 14px; font-size: .92rem; font-weight: 600; margin: 0 0 18px; }
.error { background: #F8E9E7; color: var(--red); }
.ok { background: #E4ECE3; color: var(--green-dark); }
.note { margin: 22px 0 0; font-size: .82rem; color: var(--muted); text-align: center; }
header.top { background: var(--green-deep); color: var(--cream); position: sticky; top: 0; z-index: 10; }
header.top .wrap { display: flex; align-items: center; gap: 22px; padding-top: 14px; padding-bottom: 14px; }
header.top .word span { opacity: .6; letter-spacing: .1em; font-weight: 500; margin-left: 10px; }
header.top nav { display: flex; gap: 4px; margin-right: auto; flex-wrap: wrap; }
header.top nav a { color: rgba(250,247,242,.8); text-decoration: none; font-weight: 600; font-size: .9rem; padding: 7px 12px; border-radius: 999px; }
header.top nav a:hover, header.top nav a[aria-current] { background: rgba(250,247,242,.1); color: var(--cream); }
header.top form { margin: 0; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 0 24px; }
main.wrap { padding-top: 36px; padding-bottom: 80px; }
.head { display: flex; align-items: flex-end; justify-content: space-between; gap: 16px; flex-wrap: wrap; margin-bottom: 20px; }
.head h1 { margin: 0; }
.info { display: flex; flex-wrap: wrap; gap: 6px 26px; font-size: .86rem; color: var(--muted); margin: 0 0 24px; }
.info b { color: var(--green-deep); }
table { width: 100%; border-collapse: collapse; background: var(--white); border-radius: 16px; overflow: hidden; box-shadow: 0 16px 40px -32px rgba(44,68,48,.6); }
th, td { text-align: left; padding: 12px 16px; border-bottom: 1px solid var(--sand); font-size: .92rem; vertical-align: middle; }
th { font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); background: #F6F2EA; }
td small { display: block; color: var(--muted); }
td a.title { color: inherit; text-decoration: none; font-weight: 700; }
td a.title:hover { text-decoration: underline; }
td.actions { white-space: nowrap; text-align: right; }
td.actions a { margin-left: 10px; font-size: .86rem; font-weight: 600; }
.tag { display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: .74rem; font-weight: 700; white-space: nowrap; }
.tag.published { background: #E4ECE3; color: var(--green-dark); }
.tag.draft { background: #EEE7F3; color: #5E4A78; }
.tag.warn { background: #F8E9E7; color: var(--red); }
.panel { background: var(--white); border-radius: 18px; padding: 22px 24px; box-shadow: 0 16px 40px -34px rgba(44,68,48,.6); margin-bottom: 20px; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 0 20px; }
.grid3 { display: grid; grid-template-columns: 1.2fr 1fr 1.4fr; gap: 0 20px; }
.tabs { display: flex; gap: 6px; margin: 4px 0 18px; }
.tab { font: inherit; font-weight: 700; font-size: .92rem; padding: 9px 18px; border-radius: 999px; border: 1px solid var(--line); background: var(--white); color: var(--green-deep); cursor: pointer; }
.tab[aria-selected=true] { background: var(--green-dark); color: var(--white); border-color: var(--green-dark); }
.tab .done { margin-left: 6px; opacity: .8; }
.lang-panel > h2 { margin-top: 6px; }
.toolbar { position: sticky; top: 66px; z-index: 4; display: flex; flex-wrap: wrap; gap: 8px 14px; padding: 8px; margin: 4px 0 0; background: #F6F2EA; border: 1px solid var(--line); border-bottom: 0; border-radius: 12px 12px 0 0; }
.toolbar .group { display: flex; flex-wrap: wrap; gap: 4px; }
.toolbar button { display: inline-flex; align-items: center; gap: 6px; font: inherit; font-weight: 600; font-size: .84rem; padding: 6px 10px 6px 6px; border-radius: 8px; border: 1px solid transparent; background: transparent; color: var(--green-deep); cursor: pointer; white-space: nowrap; }
.toolbar button:hover { background: var(--white); border-color: var(--line); }
.toolbar button[aria-pressed=true] { background: var(--green-dark); color: var(--white); }
.toolbar .ic { display: inline-grid; place-items: center; width: 24px; height: 24px; border-radius: 6px; background: var(--white); border: 1px solid var(--line); font-size: .9rem; color: var(--green-deep); }
.toolbar button[aria-pressed=true] .ic { border-color: transparent; }
.toolbar .ic.serif { font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 700; font-size: 1.15rem; }
.toolbar .ic.small { font-size: .9rem; }
.toolbar .swatches { display: flex; gap: 2px; } .toolbar .swatches i { width: 7px; height: 14px; border-radius: 3px; }
.colour-menu { position: relative; }
.colour-list { position: absolute; top: calc(100% + 4px); left: 0; z-index: 6; display: grid; gap: 2px; padding: 6px; min-width: 160px; background: var(--white); border: 1px solid var(--line); border-radius: 12px; box-shadow: 0 16px 40px -18px rgba(44,68,48,.45); }
.colour-list button { padding: 7px 10px; }
.dot { width: 14px; height: 14px; border-radius: 50%; display: inline-block; } .dot.none { border: 1px dashed var(--muted); }
.tc-green-bg { background: #344E38; } .tc-lilac-bg { background: #6E5A8A; } .tc-gold-bg { background: #8A6A2B; } .tc-rose-bg { background: #A4423A; }
.rich { position: relative; min-height: 380px; padding: 18px 20px; border: 1px solid var(--line); border-radius: 0 0 12px 12px; background: var(--white); font-size: 1.05rem; line-height: 1.75; color: #2E332E; outline: none; overflow-wrap: anywhere; }
.rich:focus { border-color: var(--lilac-deep); box-shadow: 0 0 0 2px var(--lilac); }
.rich > :first-child { margin-top: 0; }
.rich p { margin: 0 0 1em; }
.rich h2 { font-size: 1.9rem; margin: 1.2em 0 .4em; } .rich h3 { font-size: 1.45rem; margin: 1.1em 0 .35em; }
.rich ul, .rich ol { margin: 0 0 1em; padding-left: 1.4em; }
.rich blockquote { margin: 1em 0; padding: 2px 0 2px 20px; border-left: 3px solid var(--lilac); font-family: 'Cormorant Garamond', Georgia, serif; font-size: 1.4rem; line-height: 1.4; color: var(--green-deep); }
.rich blockquote p { margin: 0; }
.rich a { color: var(--green-dark); font-weight: 600; }
.rich u { text-underline-offset: .18em; }
.rich .tc-green { color: #344E38; } .rich .tc-lilac { color: #6E5A8A; } .rich .tc-gold { color: #8A6A2B; } .rich .tc-rose { color: #A4423A; }
.rich.empty::before { content: attr(data-placeholder); color: #9A9C97; pointer-events: none; position: absolute; }
details.more { margin-top: 18px; }
details.more summary { cursor: pointer; font-weight: 600; font-size: .88rem; color: var(--muted); }
.cover { display: grid; grid-template-columns: 220px 1fr; gap: 20px; align-items: start; }
.cover .thumb { aspect-ratio: 16 / 10; border-radius: 14px; overflow: hidden; background: var(--sand); display: grid; place-items: center; color: var(--muted); font-size: .85rem; text-align: center; padding: 8px; }
.cover .thumb img { width: 100%; height: 100%; object-fit: cover; }
.check { display: flex; gap: 8px; align-items: center; font-weight: 500; margin-top: 10px; }
.actionbar { position: sticky; bottom: 0; z-index: 5; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; padding: 14px 18px; margin: 24px 0 0; background: rgba(250,247,242,.94); backdrop-filter: blur(6px); border: 1px solid var(--line); border-radius: 18px; }
.actionbar .grow { flex: 1; }
.actionbar .status { font-size: .86rem; color: var(--muted); }
.links { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; }
.restore { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; padding: 12px 16px; border-radius: 14px; background: #EEE7F3; margin-bottom: 18px; font-weight: 600; font-size: .92rem; }
.danger-zone { margin-top: 40px; padding: 20px 24px; border: 1px solid #E7C9C5; border-radius: 18px; background: var(--white); }
.danger-zone form { display: flex; flex-wrap: wrap; gap: 14px; align-items: center; }
.swatch { display: inline-block; width: 14px; height: 14px; border-radius: 50%; vertical-align: -2px; margin-right: 6px; }
.empty { padding: 30px; text-align: center; color: var(--muted); background: var(--white); border-radius: 16px; }
@media (max-width: 760px) {
  .grid2, .grid3, .cover { grid-template-columns: 1fr; }
  th:nth-child(2), td:nth-child(2), th:nth-child(4), td:nth-child(4) { display: none; }
  header.top .wrap { flex-wrap: wrap; gap: 10px; }
  .card { padding: 28px 22px; }
  .actionbar { padding: 10px 12px; gap: 8px; border-radius: 14px; }
  .actionbar .status { display: none; }
  .actionbar .btn { flex: 1; padding: 11px 12px; }
}
"""


# The editor's script, read once at start-up, so the page, the styles and the script always belong together.
# Their addresses carry a version, so browsers load the new ones after every update instead of a cached copy.
EDITOR_JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'editor.js'), 'rb').read()
VERSION = hashlib.sha256(CSS.encode() + EDITOR_JS).hexdigest()[:10]


def page(title, body, cls='', script=False):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(title)} – {APP}</title>
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="stylesheet" href="/admin.css?v={VERSION}">
{f'<script src="/editor.js?v={VERSION}" defer></script>' if script else ''}
</head>
<body class="{cls}">
{body}
</body>
</html>'''


def login_page(error='', notice=''):
    err = f'<p class="error" role="alert">{esc(error)}</p>' if error else ''
    if notice:
        form = f'<p class="sub">{esc(notice)}</p>'
    else:
        form = '''<form method="post" action="/login" autocomplete="on">
      <label for="password">Password</label>
      <input id="password" name="password" type="password" autocomplete="current-password" required autofocus>
      <label for="code">Code <small>from your authenticator app, or a backup code</small></label>
      <input id="code" name="code" type="text" inputmode="numeric" autocomplete="one-time-code" maxlength="14" required>
      <button class="btn wide" type="submit">Sign in</button>
    </form>'''
    return page('Sign in', f'''<main class="login"><div class="card">
    <span class="word">DR VASILEVA</span>
    <h1>Website editor</h1>
    <p class="sub">Sign in to write and publish articles.</p>
    {err}
    {form}
    <p class="note">Every sign-in is emailed to the owner.</p>
  </div></main>''', 'login-page')


def frame(title, csrf, current, body, script=False):
    nav = ''.join(f'<a href="{h}"{" aria-current=page" if h == current else ""}>{t}</a>'
                  for h, t in (('/', 'Posts'), ('/topics', 'Topics'), ('/bin', 'Bin')))
    return page(title, f'''<header class="top"><div class="wrap">
    <a class="word" href="/">DR VASILEVA<span>Editor</span></a>
    <nav aria-label="Editor">{nav}</nav>
    <form method="post" action="/logout"><input type="hidden" name="csrf" value="{esc(csrf)}"><button class="btn light" type="submit">Sign out</button></form>
  </div></header>
  <main class="wrap">{body}</main>''', script=script)


def message(ok='', error=''):
    return (f'<p class="ok" role="status">{esc(ok)}</p>' if ok else '') + (f'<p class="error" role="alert">{esc(error)}</p>' if error else '')


def posts_list(csrf, posts, topics, previous, ok='', error=''):
    names = {t['id']: t['en'] for t in topics}
    rows = []
    for p in posts:
        bg, en = p['text']['bg'], p['text']['en']
        missing = [LANG_NAMES[l] for l in blog.LANGS if not (p['text'][l]['title'] and (p['text'][l]['body'] or p['bgben']))]
        state = f'<span class="tag {p["status"]}">{"Published" if p["status"] == "published" else "Draft"}</span>'
        if missing:
            state += f' <span class="tag warn">{" + ".join(missing)} missing</span>'
        rows.append(f'''<tr>
        <td><a class="title" href="/posts/{p['id']}">{esc(bg['title'] or en['title'] or '(no title)')}</a><small>{esc(en['title'] if bg['title'] else '')}</small></td>
        <td>{esc(names.get(p['topic'], ''))}</td>
        <td>{state}</td>
        <td>{esc(blog.format_date(p['date'], 'en')) if p['date'] else '–'}</td>
        <td class="actions"><a href="/posts/{p['id']}">Edit</a><a href="/preview/{p['id']}/bg" target="_blank" rel="noopener">Preview</a></td>
      </tr>''')
    table = (f'<table><thead><tr><th>Title</th><th>Topic</th><th>Status</th><th>Date</th><th></th></tr></thead><tbody>{"".join(rows)}</tbody></table>'
             if rows else '<p class="empty">No posts yet.</p>')
    prev = f'{when(previous["time"])} from {esc(previous["ip"])}' if previous else 'this is the first sign-in'
    return frame('Posts', csrf, '/', f'''
    <div class="head"><h1>Posts</h1><a class="btn" href="/posts/new">+ New post</a></div>
    <div class="info"><span>Previous sign-in: <b>{prev}</b></span><span>You are signed out after 1 hour without activity.</span></div>
    {message(ok, error)}
    {table}''')


def edit_form(csrf, post, topics, ok='', error='', is_new=False):
    """post: the editor's view of a post (blog.read_post, strict=False), or the values just submitted."""
    pid = post.get('id') or ''
    action = '/posts/new' if is_new else f'/posts/{pid}'
    published = post.get('status') == 'published'
    options = ''.join(f'<option value="{esc(t["id"])}"{" selected" if t["id"] == post.get("topic") else ""}>{esc(t["en"])} / {esc(t["bg"])}</option>' for t in topics)
    cover = post.get('cover')
    thumb = f'<img src="/media/{esc(pid)}/{esc(cover)}" alt="">' if cover and pid else 'No photo: the post shows its topic’s coloured cover.'
    tabs, panels = [], []
    for lang in ('bg', 'en'):
        x = post['text'][lang]
        tabs.append(f'<button class="tab" type="button" role="tab" data-tab="{lang}" aria-selected="{"true" if lang == "bg" else "false"}">{LANG_NAMES[lang]}<span class="done" data-done="{lang}"></span></button>')
        panels.append(f'''<section class="panel lang-panel" data-panel="{lang}" lang="{lang}">
      <h2>{LANG_NAMES[lang]}</h2>
      <label for="{lang}_title">Title</label>
      <input id="{lang}_title" name="{lang}_title" type="text" maxlength="200" value="{esc(x['title'])}">
      <label for="{lang}_summary">Summary <small>one or two sentences, shown on the cards and in Google</small></label>
      <textarea class="short" id="{lang}_summary" name="{lang}_summary" rows="2" maxlength="400">{esc(x['summary'])}</textarea>
      <label for="{lang}_body">Text</label>
      <div class="toolbar" data-for="{lang}_body" role="toolbar" aria-label="Formatting" hidden>
        <div class="group">
          <button type="button" data-cmd="h2" title="A big heading for a new section"><span class="ic serif">H</span>Heading</button>
          <button type="button" data-cmd="h3" title="A smaller heading"><span class="ic serif small">H</span>Subheading</button>
          <button type="button" data-cmd="p" title="Back to normal text"><span class="ic">¶</span>Normal text</button>
        </div>
        <div class="group">
          <button type="button" data-cmd="bold" title="Bold (Ctrl+B)"><span class="ic"><b>B</b></span>Bold</button>
          <button type="button" data-cmd="italic" title="Italic (Ctrl+I)"><span class="ic"><i>I</i></span>Italic</button>
          <button type="button" data-cmd="underline" title="Underline (Ctrl+U)"><span class="ic"><u>U</u></span>Underline</button>
          <div class="colour-menu">
            <button type="button" data-cmd="colours" aria-expanded="false" title="Colour the selected words"><span class="ic"><span class="swatches"><i class="tc-lilac-bg"></i><i class="tc-gold-bg"></i></span></span>Colour ▾</button>
            <div class="colour-list" hidden>
              <button type="button" data-colour="green"><span class="dot tc-green-bg"></span>Green</button>
              <button type="button" data-colour="lilac"><span class="dot tc-lilac-bg"></span>Lilac</button>
              <button type="button" data-colour="gold"><span class="dot tc-gold-bg"></span>Gold</button>
              <button type="button" data-colour="rose"><span class="dot tc-rose-bg"></span>Rose</button>
              <button type="button" data-colour=""><span class="dot none"></span>No colour</button>
            </div>
          </div>
        </div>
        <div class="group">
          <button type="button" data-cmd="ul" title="A list with dots"><span class="ic">•</span>Bullet list</button>
          <button type="button" data-cmd="ol" title="A numbered list"><span class="ic">1.</span>Numbered list</button>
          <button type="button" data-cmd="renum" title="Numbered lists carry on after a paragraph. Use this to start this list again at 1, or to carry on again." hidden><span class="ic">↺</span>Restart numbering</button>
          <button type="button" data-cmd="quote" title="A quote, shown larger"><span class="ic serif">“</span>Quote</button>
        </div>
        <div class="group">
          <button type="button" data-cmd="link" title="Turn the selected words into a link"><span class="ic">↗</span>Link</button>
          <button type="button" data-cmd="clear" title="Remove bold, italic, underline, colour and links from the selected words"><span class="ic"><s>T</s></span>Clear formatting</button>
        </div>
      </div>
      <textarea id="{lang}_body" name="{lang}_body" rows="18" maxlength="100000">{esc(x['body'])}</textarea>
      <span class="hint" data-hint>A blank line starts a new paragraph. **bold**, *italic*, ++underline++, {{lilac|coloured words}}, ## heading, - list, &gt; quote, [link text](https://…)</span>
      <details class="more">
        <summary>Web address and photo description</summary>
        <label for="{lang}_slug">Web address <small>made from the title if left empty; avoid changing it once published</small></label>
        <input id="{lang}_slug" name="{lang}_slug" type="text" maxlength="80" value="{esc(x['slug'])}">
        <label for="{lang}_cover_alt">Photo description <small>for blind visitors and Google, e.g. “A mother and daughter talking”</small></label>
        <input id="{lang}_cover_alt" name="{lang}_cover_alt" type="text" maxlength="200" value="{esc(x['cover_alt'])}">
      </details>
    </section>''')
    problems = post.get('problems') or []
    todo = f'<p class="hint">Before it can be published: {esc("; ".join(problems))}.</p>' if problems and not is_new else ''
    buttons = (f'''<button class="btn" type="submit" name="action" value="save">Save changes</button>
        <button class="btn outline" type="submit" name="action" value="unpublish">Unpublish</button>''' if published else
               f'''<button class="btn outline" type="submit" name="action" value="save">Save draft</button>
        <button class="btn" type="submit" name="action" value="publish">Publish</button>''')
    links = '' if is_new else f'''<a class="btn outline small" href="/preview/{esc(pid)}/bg" target="_blank" rel="noopener">Preview BG</a>
        <a class="btn outline small" href="/preview/{esc(pid)}/en" target="_blank" rel="noopener">Preview EN</a>
        <a class="btn outline small" href="/posts/{esc(pid)}/versions">Versions</a>'''
    danger = '' if is_new else f'''<div class="danger-zone"><form method="post" action="/posts/{esc(pid)}/delete">
      <input type="hidden" name="csrf" value="{esc(csrf)}">
      <label class="check"><input type="checkbox" name="confirm" value="yes" required> Move this post to the bin{" (it disappears from the site)" if published else ""}</label>
      <button class="btn danger small" type="submit">Delete</button>
      <span class="hint">The bin keeps it for 30 days.</span></form></div>'''
    state = 'Published – changes go live when you save' if published else ('New post' if is_new else 'Draft – not on the site')
    return frame('New post' if is_new else (post['text']['bg']['title'] or post['text']['en']['title'] or 'Post'), csrf, '/', f'''
    <div class="head"><h1>{'New post' if is_new else 'Edit post'}</h1><a href="/">← All posts</a></div>
    {message(ok, error)}
    <div class="restore" data-restore hidden><span>Unsaved changes from this browser were found (<span data-restore-time></span>).</span>
      <button class="btn small" type="button" data-restore-yes>Restore them</button><button class="btn outline small" type="button" data-restore-no>Discard</button></div>
    <form method="post" action="{action}" enctype="multipart/form-data" data-editor data-key="{esc(pid or 'new')}" data-saved="{int(post.get('saved') or 0)}">
      <input type="hidden" name="csrf" value="{esc(csrf)}">
      <section class="panel">
        <div class="grid3">
          <div><label for="topic">Topic</label><select id="topic" name="topic" required>{options}</select><span class="hint"><a href="/topics">Add or change topics</a></span></div>
          <div><label for="date">Date</label><input id="date" name="date" type="text" inputmode="numeric" maxlength="10" placeholder="2026-09-19" value="{esc(post.get('date') or '')}">
            <span class="hint">Year-month-day. Empty = the day it is published.</span></div>
          <div><label for="bgben">BG BEN link <small>only for columns</small></label><input id="bgben" name="bgben" type="url" maxlength="300" placeholder="https://bgben.co.uk/…" value="{esc(post.get('bgben') or '')}"></div>
        </div>
        <div class="cover">
          <div><label>Cover photo</label><div class="thumb" data-thumb>{thumb}</div></div>
          <div><label for="photo">Choose a photo <small>JPG, PNG or WebP, up to 10 MB</small></label>
            <input id="photo" name="photo" type="file" accept="image/jpeg,image/png,image/webp">
            <span class="hint">The photo is resized for the web, and the location your phone saves in photos is removed.</span>
            {'<label class="check"><input type="checkbox" name="remove_photo" value="yes"> Remove the photo</label>' if cover else ''}</div>
        </div>
      </section>
      <div class="tabs" role="tablist" hidden>{''.join(tabs)}</div>
      {''.join(panels)}
      {todo}
      {f'<div class="links">{links}</div>' if links else ''}
      <div class="actionbar">
        <span class="status grow">{state}<span data-autosaved></span></span>
        {buttons}
      </div>
    </form>
    {danger}''', script=True)


def versions_page(csrf, pid, title, versions, ok='', error=''):
    rows = ''.join(f'''<tr><td>{when(v['time'])}</td><td>{esc(v['title'])}</td><td><span class="tag {esc(v['status'] or 'draft')}">{'Published' if v['status'] == 'published' else 'Draft'}</span></td>
      <td class="actions"><form method="post" action="/posts/{esc(pid)}/versions/{esc(v['id'])}/restore"><input type="hidden" name="csrf" value="{esc(csrf)}"><button class="btn outline small" type="submit">Restore</button></form></td></tr>''' for v in versions)
    table = f'<table><thead><tr><th>Saved</th><th>Title</th><th>Status then</th><th></th></tr></thead><tbody>{rows}</tbody></table>' if rows else '<p class="empty">No earlier versions yet. One is kept each time you save.</p>'
    return frame('Versions', csrf, '/', f'''
    <div class="head"><h1>Versions</h1><a href="/posts/{esc(pid)}">← Back to “{esc(title)}”</a></div>
    <p class="info">The last 30 saved versions are kept. Restoring brings back the text and photo of that version; whether the post is published stays as it is now.</p>
    {message(ok, error)}{table}''')


def topics_page(csrf, topics, counts, ok='', error=''):
    def selects(prefix, t):
        cs = ''.join(f'<option value="{c}"{" selected" if t.get("colour") == c else ""}>{COLOUR_NAMES[c]}</option>' for c in blog.COLOURS)
        ic = ''.join(f'<option value="{i}"{" selected" if t.get("icon") == i else ""}>{ICON_NAMES[i]}</option>' for i in blog.ICONS)
        return f'<td><select name="{prefix}_colour" aria-label="Colour">{cs}</select></td><td><select name="{prefix}_icon" aria-label="Icon">{ic}</select></td>'
    rows = ''.join(f'''<tr><td><input type="text" name="{esc(t['id'])}_en" value="{esc(t['en'])}" maxlength="60" aria-label="English name" required></td>
      <td><input type="text" name="{esc(t['id'])}_bg" value="{esc(t['bg'])}" maxlength="60" aria-label="Bulgarian name" required></td>
      {selects(esc(t['id']), t)}<td>{counts.get(t['id'], 0)}</td>
      <td class="actions">{'' if counts.get(t['id']) else f'<button class="btn danger small" type="submit" name="remove" value="{esc(t["id"])}" formnovalidate>Delete</button>'}</td></tr>''' for t in topics)
    return frame('Topics', csrf, '/topics', f'''
    <div class="head"><h1>Topics</h1></div>
    <p class="info">Topics appear as filters on the Articles page once they have a published post. A topic with posts can’t be deleted.</p>
    {message(ok, error)}
    <form method="post" action="/topics"><input type="hidden" name="csrf" value="{esc(csrf)}">
      <table><thead><tr><th>English</th><th>Български</th><th>Colour</th><th>Icon</th><th>Posts</th><th></th></tr></thead><tbody>{rows}
      <tr><td><input type="text" name="new_en" maxlength="60" placeholder="New topic (English)" aria-label="New topic, English"></td>
      <td><input type="text" name="new_bg" maxlength="60" placeholder="Нова тема" aria-label="New topic, Bulgarian"></td>{selects('new', {})}<td></td><td></td></tr>
      </tbody></table>
      <div class="actionbar"><span class="grow status">Changes to names go live on the site when you save.</span><button class="btn" type="submit">Save topics</button></div>
    </form>''')


def bin_page(csrf, items, ok='', error=''):
    rows = ''.join(f'''<tr><td><b>{esc(b['title'])}</b></td><td>{when(b['deleted'])}</td><td>{when(b['purge'])}</td>
      <td class="actions"><form method="post" action="/bin/{esc(b['name'])}/restore"><input type="hidden" name="csrf" value="{esc(csrf)}"><button class="btn outline small" type="submit">Restore</button></form></td></tr>''' for b in items)
    table = f'<table><thead><tr><th>Post</th><th>Deleted</th><th>Removed for good</th><th></th></tr></thead><tbody>{rows}</tbody></table>' if rows else '<p class="empty">The bin is empty.</p>'
    return frame('Bin', csrf, '/bin', f'''
    <div class="head"><h1>Bin</h1></div>
    <p class="info">Deleted posts stay here for 30 days. A restored post comes back as a draft, so you can check it before publishing.</p>
    {message(ok, error)}{table}''')
