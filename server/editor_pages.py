"""The editor's screens (HTML). Everything shown is escaped; the only script is /editor.js."""
import hashlib
import html
import json
import os
import urllib.parse

import blog
from editor_i18n import _, lang, msg, path as current_path, when, JS_KEYS, BG

esc = html.escape
APP = 'Dr Vasileva editor'
LANG_NAMES = {'bg': 'Български', 'en': 'English'}
COLOUR_NAMES = dict(sage='Sage green', lilac='Lilac', gold='Gold', forest='Forest green', plum='Plum', sand='Sand')
ICON_NAMES = {'i-sun': 'Sun', 'i-heart': 'Heart', 'i-smile': 'Smile', 'i-leaf': 'Leaf', 'i-puzzle': 'Puzzle', 'i-globe': 'Globe', 'i-feather': 'Feather'}


def _topic_icons():
    """The site's own icons for topics, so the editor's previews match the Articles page."""
    import re
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'home.html'), encoding='utf-8').read()
    found = [m.group(0) for i in blog.ICONS for m in [re.search(rf'<symbol id="{i}"[^>]*>.*?</symbol>', src, re.S)] if m]
    return '<svg xmlns="http://www.w3.org/2000/svg" hidden>' + ''.join(found) + '</svg>'


ICON_SPRITE = _topic_icons()


_ICON_PATHS = {
    'edit': '<path d="M21.17 6.81a1 1 0 0 0-3.99-3.99L3.84 16.17a2 2 0 0 0-.5.83l-1.32 4.35a.5.5 0 0 0 .62.62l4.35-1.32a2 2 0 0 0 .83-.5z"/><path d="m15 5 4 4"/>',
    'preview': '<path d="M2.06 12.35a1 1 0 0 1 0-.7 10.75 10.75 0 0 1 19.88 0 1 1 0 0 1 0 .7 10.75 10.75 0 0 1-19.88 0"/><circle cx="12" cy="12" r="3"/>',
    'delete': '<path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M10 11v6M14 11v6"/>',
    'versions': '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>',
    'photo': '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.09-3.09a2 2 0 0 0-2.82 0L6 21"/>',
}


def icon(name):
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{_ICON_PATHS[name]}</svg>'


def confirm_name(name):
    """What she types to confirm a delete: the name with dashes for spaces (like GitHub)."""
    return '-'.join(str(name).split())


def delete_heading(what):
    return _('Delete this topic?') if what == 'topic' else _('Delete this post?')


def delete_link(href, name, what, note):
    """A bin icon. With the script it opens the delete box; without, it opens a page with the same question."""
    return (f'<a class="icon-btn danger" href="{href}" data-delete data-name="{esc(confirm_name(name))}" data-heading="{esc(delete_heading(what))}" '
            f'data-note="{esc(_(note))}" title="{_("Delete")}" aria-label="{_("Delete")}: {esc(name)}">{icon("delete")}</a>')


def ui_lang_switch():
    """БГ | EN: the editor's own language, remembered in this browser."""
    nxt = urllib.parse.quote(current_path(), safe='/?=&')
    return (f'<nav class="ui-lang" aria-label="{_("Language of the editor")}">' +
            ''.join(f'<a href="/lang/{l}?next={nxt}" lang="{l}"{" aria-current=true" if l == lang() else ""}>{t}</a>'
                    for l, t in (('bg', 'БГ'), ('en', 'EN'))) + '</nav>')


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
input[type=password], input[type=text], input[type=url], input[type=search], select, textarea { width: 100%; font: inherit; font-size: 1rem; padding: 12px 14px; border: 1px solid var(--line); border-radius: 12px; background: var(--white); color: inherit; }
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
.btn.red, .btn.signout { background: var(--red); color: var(--white); }
.btn.signout { padding: 9px 18px; }
dialog.confirm { border: 0; border-radius: 20px; padding: 28px 28px 24px; max-width: 380px; width: calc(100% - 40px); box-shadow: 0 30px 70px -20px rgba(0,0,0,.45); }
dialog.confirm::backdrop { background: rgba(28,40,30,.55); }
dialog.confirm h2 { margin: 0 0 8px; }
dialog.confirm p { margin: 0 0 22px; color: var(--muted); }
.btn-row { display: flex; gap: 10px; justify-content: flex-end; flex-wrap: wrap; }
.icons { display: inline-flex; gap: 4px; }
.icon-btn { display: inline-grid; place-items: center; width: 36px; height: 36px; border-radius: 10px; color: var(--green-deep); border: 1px solid transparent; }
.icon-btn:hover { background: var(--sand); border-color: var(--line); }
.icon-btn.danger { color: var(--red); } .icon-btn.danger:hover { background: #F8E9E7; border-color: #E7C9C5; }
.icon-btn.disabled { color: #B9B6AE; cursor: not-allowed; background: transparent; font: inherit; padding: 0; }
.ico { fill: none; stroke: currentColor; stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; }
.icon-btn .ico { width: 19px; height: 19px; fill: none; stroke: currentColor; stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; }
td.actions a.icon-btn { margin-left: 0; }
dialog.confirm label { margin-top: 0; font-weight: 500; color: var(--muted); }
dialog.confirm code, .delete-page code { font: 600 .9rem/1.4 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; color: var(--red); background: #F8E9E7; padding: 2px 6px; border-radius: 6px; word-break: break-all; }
dialog.confirm input { margin: 8px 0 20px; }
.delete-page { max-width: 560px; } .delete-page input { margin: 8px 0 20px; }
.btn:disabled { opacity: .45; cursor: not-allowed; filter: none; }
.search { margin: 0 0 16px; }
.search-row { display: flex; gap: 10px; }
.search-row input { flex: 1; }
.search-row .btn { padding: 12px 26px; }
.filter-row { display: flex; align-items: center; gap: 12px 18px; margin-top: 12px; }
.filter-row label { flex: 1; min-width: 0; display: flex; align-items: center; gap: 10px; margin: 0; font-size: .86rem; color: var(--muted); white-space: nowrap; }
.filter-row select { flex: 1; min-width: 0; width: auto; padding: 9px 12px; font-size: .9rem; }
.filter-row .reset { flex-shrink: 0; font-size: .86rem; font-weight: 600; }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.topic-preview { position: relative; display: block; width: 150px; height: 82px; border-radius: 12px; overflow: hidden; }
.topic-preview .bg { position: absolute; inset: 0; }
.topic-preview .motif { position: absolute; right: -14px; bottom: -14px; width: 74px; height: 74px; fill: none; stroke: rgba(255,255,255,.3); stroke-width: 1.2; stroke-linecap: round; stroke-linejoin: round; }
.topic-preview .label { position: absolute; left: 10px; bottom: 9px; max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: .62rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: rgba(255,255,255,.95); background: rgba(0,0,0,.16); padding: 3px 8px; border-radius: 999px; }
.c-sage .bg { background: linear-gradient(135deg, #7E9C80, #3E5A41); } .c-lilac .bg { background: linear-gradient(135deg, #C9B6D6, #7C6797); }
.c-gold .bg { background: linear-gradient(135deg, #DEC189, #A9823D); } .c-forest .bg { background: linear-gradient(135deg, #5F7F62, #24392A); }
.c-plum .bg { background: linear-gradient(135deg, #A58BBE, #4E3D66); } .c-sand .bg { background: linear-gradient(135deg, #D8C6A4, #8F7650); }
.new-topic { display: grid; grid-template-columns: 1.3fr 1fr; gap: 30px; align-items: start; }
.new-topic .topic-preview { width: 100%; max-width: 340px; height: 180px; border-radius: 18px; }
.new-topic .topic-preview .motif { width: 160px; height: 160px; right: -30px; bottom: -30px; }
.new-topic .topic-preview .label { font-size: .74rem; left: 16px; bottom: 14px; max-width: 280px; }
table.topics td { vertical-align: middle; padding: 10px 8px; }
table.topics th { padding: 12px 8px; }
table.topics td:first-child, table.topics th:first-child { padding-left: 16px; }
table.topics input { min-width: 150px; }
table.topics select { min-width: 132px; padding-right: 8px; }
table.topics .topic-preview { width: 124px; height: 72px; }
.btn.small { padding: 7px 14px; font-size: .84rem; }
.error, .ok { border-radius: 12px; padding: 12px 14px; font-size: .92rem; font-weight: 600; margin: 0 0 18px; }
.error { background: #F8E9E7; color: var(--red); }
.ok { background: #E4ECE3; color: var(--green-dark); }
.msg { display: flex; align-items: center; gap: 12px; border-radius: 12px; padding: 12px 10px 12px 16px; margin: 0 0 18px; font-size: .92rem; font-weight: 600; border: 1px solid transparent; }
.msg > span { flex: 1; }
.msg.ok { background: #E4ECE3; color: var(--green-dark); border-color: #CFDDCD; }
.msg.removed, .msg.error { background: #F8E9E7; color: var(--red); border-color: #EBCFCB; }
.msg.warn { background: #FBF0DC; color: #7A5418; border-color: #EFD9AE; }
.msg-x { flex-shrink: 0; width: 30px; height: 30px; border-radius: 8px; border: 0; background: transparent; color: inherit; font-size: 1.3rem; line-height: 1; cursor: pointer; opacity: .7; }
.msg-x:hover { opacity: 1; background: rgba(0,0,0,.06); }
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
.info.above { margin: -12px 0 14px; }
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
.lang-switch { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; padding: 5px; margin: 0 0 14px; background: var(--white); border: 1px solid var(--line); border-radius: 16px; box-shadow: 0 16px 40px -34px rgba(44,68,48,.6); }
.lang-switch .tab { display: flex; align-items: center; justify-content: center; gap: 12px; font: inherit; font-weight: 700; font-size: 1rem; padding: 12px 16px; border: 0; border-radius: 12px; background: transparent; color: var(--green-deep); cursor: pointer; }
.lang-switch .tab:hover { background: #F6F2EA; }
.lang-switch .tab[aria-selected=true] { background: var(--green-dark); color: var(--white); }
.lang-switch .state { font-size: .74rem; font-weight: 700; letter-spacing: .02em; padding: 3px 10px 3px 8px; border-radius: 999px; background: #FBF0DC; color: #7A5418; display: inline-flex; align-items: center; gap: 6px; }
.lang-switch .state::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: #C08A2D; }
.lang-switch .state.ready { background: #E4ECE3; color: var(--green-dark); }
.lang-switch .state.ready::before { background: var(--green); }
.lang-switch .tab[aria-selected=true] .state { background: rgba(255,255,255,.16); color: var(--white); }
.lang-switch .tab[aria-selected=true] .state::before { background: #F0C77A; }
.lang-switch .tab[aria-selected=true] .state.ready::before { background: #A9D3AE; }
.lang-panel > h2 { margin-top: 6px; }
.toolbar { position: sticky; top: 65px; z-index: 4; display: flex; flex-wrap: wrap; gap: 8px 14px; padding: 8px; margin: 4px 0 0; background: #F6F2EA; border: 1px solid var(--line); border-bottom: 0; border-radius: 12px 12px 0 0; }
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
.rich:focus { outline: none; }
.editor-box { margin-top: 4px; border-radius: 12px; transition: box-shadow .15s; }
.editor-box .toolbar { margin: 0; }
.editor-box:focus-within { box-shadow: 0 0 0 2px var(--lilac); }
.editor-box:focus-within .toolbar, .editor-box:focus-within .rich { border-color: var(--lilac-deep); }
.rich > :first-child { margin-top: 0; }
.rich p { margin: 0 0 1em; }
.rich h2 { font-size: 1.9rem; margin: 1.2em 0 .4em; } .rich h3 { font-size: 1.45rem; margin: 1.1em 0 .35em; }
.rich ul, .rich ol { margin: 0 0 1em; padding-left: 1.4em; }
.rich blockquote { margin: 1em 0; padding: 2px 0 2px 20px; border-left: 3px solid var(--lilac); font-family: 'Cormorant Garamond', Georgia, serif; font-size: 1.4rem; line-height: 1.4; color: var(--green-deep); }
.rich blockquote p { margin: 0; }
.rich a { color: var(--green-dark); font-weight: 600; }
.rich u { text-underline-offset: .18em; }
.rich .tc-green { color: #344E38; } .rich .tc-lilac { color: #6E5A8A; } .rich .tc-gold { color: #8A6A2B; } .rich .tc-rose { color: #A4423A; }
.rich.empty::before { content: attr(data-placeholder); color: #9A9C97; pointer-events: none; position: absolute; left: 20px; top: 18px; }
details.more { margin-top: 18px; }
details.more summary { cursor: pointer; font-weight: 600; font-size: .88rem; color: var(--muted); }
.cover { display: grid; grid-template-columns: 1fr; gap: 26px; align-items: start; margin-top: 6px; }
.cover.has-photo { grid-template-columns: 300px 1fr; }
.cover:not(.has-photo) .thumb-art { aspect-ratio: auto; height: 170px; }
.thumb-box { position: relative; }
.photo-x { position: absolute; top: 10px; right: 10px; display: grid; place-items: center; width: 34px; height: 34px; padding: 0; border: 0; border-radius: 50%; background: rgba(28,40,30,.72); color: var(--white); font-size: 1.35rem; line-height: 1; cursor: pointer; box-shadow: 0 6px 16px -6px rgba(0,0,0,.5); }
.photo-x:hover, .photo-x:focus-visible { background: var(--red); }
.warn-text { color: #7A5418; font-weight: 600; }
.cover .label { display: block; font-weight: 600; font-size: .88rem; margin: 18px 0 6px; color: var(--green-deep); }
.cover .thumb { display: block; margin: 0; cursor: pointer; border-radius: 14px; outline-offset: 3px; }
.cover .thumb:focus-within { outline: 2px solid var(--lilac-deep); }
.cover .thumb-art { display: grid; place-items: center; aspect-ratio: 16 / 10; border-radius: 14px; overflow: hidden; background: #F6F2EA; border: 2px dashed var(--line); color: var(--muted); text-align: center; transition: border-color .2s, background .2s; }
.cover .thumb:hover .thumb-art { border-color: var(--lilac-deep); background: #F3EEF6; }
.cover .thumb-art img { width: 100%; height: 100%; object-fit: cover; }
.cover .thumb-art:has(img) { border-style: solid; border-color: transparent; }
.empty-photo { display: grid; justify-items: center; gap: 4px; padding: 12px; } .empty-photo .ico { width: 30px; height: 30px; color: var(--lilac-deep); margin-bottom: 4px; } .empty-photo b { color: var(--green-deep); font-size: 1rem; } .empty-photo span { font-size: .85rem; }
.alt-fields { padding-top: 6px; }
.hint.above { margin: -2px 0 8px; }
textarea.grow { field-sizing: content; min-height: 3.4em; resize: none; overflow: hidden; }
.check { display: flex; gap: 8px; align-items: center; font-weight: 500; margin-top: 10px; }
.actionbar { position: sticky; bottom: -1px; z-index: 5; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; padding: 14px 18px; margin: 24px 0 0; background: rgba(250,247,242,.94); backdrop-filter: blur(6px); border: 1px solid var(--line); border-radius: 18px; }
.actionbar .grow { flex: 1; }
.actionbar.stuck { border-bottom-left-radius: 0; border-bottom-right-radius: 0; border-bottom-color: transparent; box-shadow: 0 -10px 30px -24px rgba(44,68,48,.5); }
.toolbar.stuck { border-top-left-radius: 0; border-top-right-radius: 0; box-shadow: 0 10px 24px -22px rgba(44,68,48,.6); }
.actionbar .status { font-size: .86rem; color: var(--muted); }
.page-links { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; padding: 5px; margin: 18px 0 0; background: var(--white); border: 1px solid var(--line); border-radius: 16px; box-shadow: 0 16px 40px -34px rgba(44,68,48,.6); }
.page-links a { display: flex; align-items: center; justify-content: center; gap: 12px; padding: 12px 14px; border-radius: 12px; color: var(--green-deep); text-decoration: none; }
.page-links a:hover, .page-links a:focus-visible { background: #F6F2EA; }
.page-links .pl-ic { flex-shrink: 0; display: grid; place-items: center; width: 38px; height: 38px; border-radius: 10px; background: #F3EEF6; color: var(--lilac-deep); }
.page-links .pl-ic .ico { width: 19px; height: 19px; }
.page-links b { display: block; font-size: .95rem; }
.page-links small { display: block; font-size: .78rem; color: var(--muted); }
.ui-lang { display: inline-flex; gap: 2px; padding: 3px; border-radius: 999px; background: rgba(250,247,242,.1); }
.ui-lang a { padding: 5px 11px; border-radius: 999px; font-size: .78rem; font-weight: 700; letter-spacing: .04em; color: rgba(250,247,242,.78); text-decoration: none; }
.ui-lang a:hover { color: var(--cream); }
.ui-lang a[aria-current] { background: var(--cream); color: var(--green-deep); }
header.top .ui-lang { margin: 0; flex-wrap: nowrap; }
header.top .ui-lang a { padding: 5px 11px; font-size: .78rem; }
header.top .ui-lang a[aria-current] { background: var(--cream); color: var(--green-deep); }
.card { position: relative; }
.card .ui-lang { position: absolute; top: 18px; right: 18px; background: #F3EEE5; }
.card .ui-lang a { color: var(--green-deep); }
.card .ui-lang a[aria-current] { background: var(--green-dark); color: var(--white); }
.restore { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; padding: 12px 16px; border-radius: 14px; background: #EEE7F3; margin-bottom: 18px; font-weight: 600; font-size: .92rem; }
.danger-zone { margin-top: 40px; padding: 20px 24px; border: 1px solid #E7C9C5; border-radius: 18px; background: var(--white); }
.danger-zone form { display: flex; flex-wrap: wrap; gap: 14px; align-items: center; }
.swatch { display: inline-block; width: 14px; height: 14px; border-radius: 50%; vertical-align: -2px; margin-right: 6px; }
.empty { padding: 30px; text-align: center; color: var(--muted); background: var(--white); border-radius: 16px; }
@media (max-width: 760px) {
  .grid2, .grid3, .cover { grid-template-columns: 1fr; }
  table.posts th:nth-child(2), table.posts td:nth-child(2), table.posts th:nth-child(4), table.posts td:nth-child(4) { display: none; }
  header.top .wrap { flex-wrap: wrap; gap: 10px; }
  .card { padding: 28px 22px; }
  .actionbar { padding: 10px 12px; gap: 8px; border-radius: 14px; }
  .actionbar .status { display: none; }
  .actionbar .btn { flex: 1; padding: 11px 12px; }
  .new-topic { grid-template-columns: 1fr; }
  .lang-switch .tab { flex-direction: column; gap: 6px; padding: 10px 8px; }
  .search-row .btn { padding: 12px 16px; }
  .filter-row { flex-wrap: wrap; } .filter-row label { flex: 1 1 100%; } .filter-row label span { width: 58px; }
  .cover.has-photo { grid-template-columns: 1fr; }
  .page-links { grid-template-columns: 1fr; }
  table.topics th:nth-child(6), table.topics td:nth-child(6) { display: none; }
}
"""


# The editor's script, read once at start-up, so the page, the styles and the script always belong together.
# Their addresses carry a version, so browsers load the new ones after every update instead of a cached copy.
EDITOR_JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'editor.js'), 'rb').read()
VERSION = hashlib.sha256(CSS.encode() + EDITOR_JS).hexdigest()[:10]


def page(title, body, cls='', script=False):
    words = ''
    if lang() == 'bg' and script:           # the texts editor.js shows, as data (not a script, so the CSP allows it)
        words = ('<script type="application/json" id="i18n">' +
                 json.dumps({k: BG[k] for k in JS_KEYS if k in BG}, ensure_ascii=False).replace('<', '\\u003c') + '</script>')
    return f'''<!doctype html>
<html lang="{lang()}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(title)} – {_(APP)}</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
<link rel="stylesheet" href="/fonts/fonts.css">
{words}
<link rel="stylesheet" href="/admin.css?v={VERSION}">
{f'<script src="/editor.js?v={VERSION}" defer></script>' if script else ''}
</head>
<body class="{cls}">
{body}
</body>
</html>'''


def login_page(error='', notice=''):
    err = f'<p class="error" role="alert">{esc(msg(error))}</p>' if error else ''
    if notice:
        form = f'<p class="sub">{esc(msg(notice))}</p>'
    else:
        form = f'''<form method="post" action="/login" autocomplete="on">
      <label for="password">{_('Password')}</label>
      <input id="password" name="password" type="password" autocomplete="current-password" required autofocus>
      <label for="code">{_('Code')} <small>{_('from your authenticator app, or a backup code')}</small></label>
      <input id="code" name="code" type="text" inputmode="numeric" autocomplete="one-time-code" maxlength="14" required>
      <button class="btn wide" type="submit">{_('Sign in')}</button>
    </form>'''
    return page(_('Sign in'), f'''<main class="login"><div class="card">
    {ui_lang_switch()}
    <span class="word">DR VASILEVA</span>
    <h1>{_('Website editor')}</h1>
    <p class="sub">{_('Sign in to write and publish articles.')}</p>
    {err}
    {form}
    <p class="note">{_('Every sign-in is emailed to the owner.')}</p>
  </div></main>''', 'login-page')


def not_found_page():
    return page(_('Not found'), f'<main class="login"><div class="card"><h1>{_("Not found")}</h1><p class="sub"><a href="/">{_("Back to the editor")}</a></p></div></main>')


def frame(title, csrf, current, body, script=False):
    nav = ''.join(f'<a href="{h}"{" aria-current=page" if h == current else ""}>{t}</a>'
                  for h, t in (('/', _('Posts')), ('/topics', _('Topics')), ('/bin', _('Bin'))))
    return page(title, f'''<header class="top"><div class="wrap">
    <a class="word" href="/">DR VASILEVA<span>{_('Editor')}</span></a>
    <nav aria-label="{_('Editor')}">{nav}</nav>
    {ui_lang_switch()}
    <form method="post" action="/logout" data-signout><input type="hidden" name="csrf" value="{esc(csrf)}"><button class="btn signout" type="submit">{_('Sign out')}</button></form>
  </div></header>
  <main class="wrap">{body}</main>
  <dialog class="confirm" id="signout-dialog" aria-labelledby="signout-title">
    <form method="dialog">
      <h2 id="signout-title">{_('Sign out?')}</h2>
      <p>{_('Anything not saved on this page will be lost.')}</p>
      <div class="btn-row"><button class="btn outline" value="no" autofocus>{_('No, stay')}</button><button class="btn red" value="yes">{_('Yes, sign out')}</button></div>
    </form>
  </dialog>
  <dialog class="confirm" id="delete-dialog" aria-labelledby="delete-title">
    <form method="post" data-delete-form>
      <input type="hidden" name="csrf" value="{esc(csrf)}">
      <h2 id="delete-title" data-heading>{_('Delete this post?')}</h2>
      <p data-note></p>
      <label for="confirm_name">{_('To confirm, type')} <code data-expected></code></label>
      <input id="confirm_name" name="confirm_name" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" required>
      <div class="btn-row"><button class="btn outline" type="button" data-cancel>{_('Cancel')}</button><button class="btn red" type="submit" disabled>{_('Delete')}</button></div>
    </form>
  </dialog>''', script=True)


def note(kind, text):
    """A message at the top of a screen. kind: ok (green), removed (red), error (red), warn (amber)."""
    role = 'alert' if kind in ('error', 'warn') else 'status'
    return (f'<div class="msg {kind}" role="{role}"><span>{esc(msg(text))}</span>'
            f'<button class="msg-x" type="button" aria-label="{_("Close this message")}" hidden>×</button></div>')


def message(ok='', error=''):
    """ok: text, or (kind, text) for a red 'removed' message."""
    kind, text = ok if isinstance(ok, tuple) else ('ok', ok)
    return (note(kind, text) if text else '') + (note('error', error) if error else '') + '<div data-messages></div>'


def post_title(p):
    """A post's title in the editor's language, or else in the other one."""
    other = 'en' if lang() == 'bg' else 'bg'
    return p['text'][lang()]['title'] or p['text'][other]['title']


def topic_name(t):
    """A topic's name in the editor's language."""
    return t.get(lang()) or t.get('en', '')


def posts_list(csrf, posts, topics, previous, ok='', error='', query='', sort='new', topic='', status=''):
    names = {t['id']: topic_name(t) for t in topics}
    rows = []
    for p in posts:
        bg, en = p['text']['bg'], p['text']['en']
        first, second = (bg, en) if lang() == 'bg' else (en, bg)
        if not first['title']:
            first, second = second, first
        title = post_title(p)
        missing = [LANG_NAMES[l] for l in blog.LANGS if not (p['text'][l]['title'] and (p['text'][l]['body'] or p['bgben']))]
        state = f'<span class="tag {p["status"]}">{_("Published") if p["status"] == "published" else _("Draft")}</span>'
        if missing:
            state += f' <span class="tag warn">{esc(msg(" + ".join(missing) + " missing"))}</span>'
        words = f"{bg['title']} {en['title']}".lower()
        hide = (query and query.lower() not in words) or (topic and p['topic'] != topic) or (status and p['status'] != status)
        note = 'It disappears from the site and stays in the bin for 30 days.' if p['status'] == 'published' else 'It stays in the bin for 30 days.'
        rows.append(f"""<tr data-title="{esc(words)}" data-topic="{esc(p['topic'])}" data-status="{p['status']}" data-date="{esc(p['date'] or '9999')}"{' hidden' if hide else ''}>
        <td><a class="title" href="/posts/{p['id']}">{esc(title or _('(no title)'))}</a><small>{esc(second['title'] if first['title'] else '')}</small></td>
        <td>{esc(names.get(p['topic'], ''))}</td>
        <td>{state}</td>
        <td>{esc(blog.format_date(p['date'], lang())) if p['date'] else '–'}</td>
        <td class="actions"><span class="icons">
          <a class="icon-btn" href="/posts/{p['id']}" title="{_('Edit')}" aria-label="{_('Edit')}: {esc(title)}">{icon('edit')}</a>
          <a class="icon-btn" href="/preview/{p['id']}/{lang()}" target="_blank" rel="noopener" title="{_('Preview')}" aria-label="{_('Preview')}: {esc(title)}">{icon('preview')}</a>
          {delete_link(f"/posts/{p['id']}/delete", title or p['id'], 'post', note)}
        </span></td>
      </tr>""")
    table = (f'<table class="posts"><thead><tr><th>{_("Title")}</th><th>{_("Topic")}</th><th>{_("Status")}</th><th>{_("Date")}</th><th></th></tr></thead><tbody>{"".join(rows)}</tbody></table>'
             if rows else f'<p class="empty">{_("No posts yet.")}</p>')
    prev = when(previous['time']) if previous else _('this is the first sign-in')
    shown = sum(1 for p in posts if (not query or query.lower() in f"{p['text']['bg']['title']} {p['text']['en']['title']}".lower())
                and (not topic or p['topic'] == topic) and (not status or p['status'] == status))
    opt = lambda value, label, current: f'<option value="{esc(value)}"{" selected" if value == current else ""}>{esc(label)}</option>'
    return frame(_('Posts'), csrf, '/', f"""
    <div class="info above"><span>{_('Previous sign-in:')} <b>{prev}</b></span><span>{_('You are signed out after 1 hour without activity.')}</span></div>
    <div class="head"><h1>{_('Posts')}</h1><a class="btn" href="/posts/new">{_('+ New post')}</a></div>
    {message(ok, error)}
    <form class="search" method="get" action="/" role="search" data-filters>
      <div class="search-row">
        <label class="sr" for="q">{_('Search posts by title')}</label>
        <input id="q" name="q" type="search" value="{esc(query)}" placeholder="{_('Search by title, in Bulgarian or English…')}" autocomplete="off" data-search>
        <button class="btn" type="submit">{_('Search')}</button>
      </div>
      <div class="filter-row">
        <label><span>{_('Order')}</span> <select name="sort" data-sort>{opt('new', _('Newest first'), sort)}{opt('old', _('Oldest first'), sort)}</select></label>
        <label><span>{_('Topic')}</span> <select name="topic" data-topic>{opt('', _('All topics'), topic)}{''.join(opt(t['id'], topic_name(t), topic) for t in topics)}</select></label>
        <label><span>{_('Status')}</span> <select name="status" data-status>{opt('', _('All'), status)}{opt('published', _('Published'), status)}{opt('draft', _('Drafts'), status)}</select></label>
        <a class="reset" href="/" data-reset{'' if (query or topic or status or sort != 'new') else ' hidden'}>{_('Clear filters')}</a>
      </div>
    </form>
    {table}
    <p class="empty" data-none{' hidden' if shown or not posts else ''}>{_('No posts match.')}</p>""")


def toolbar(lang_code):
    b = lambda cmd, ic, label, title, extra='': (f'<button type="button" data-cmd="{cmd}" title="{_(title)}"{extra}>'
                                                 f'<span class="ic{ic[0]}">{ic[1]}</span>{_(label)}</button>')
    colours = ''.join(f'<button type="button" data-colour="{c}"><span class="dot tc-{c}-bg"></span>{_(n)}</button>'
                      for c, n in (('green', 'Green'), ('lilac', 'Lilac'), ('gold', 'Gold'), ('rose', 'Rose')))
    return f"""<div class="toolbar" data-for="{lang_code}_body" role="toolbar" aria-label="{_('Formatting')}" hidden>
        <div class="group">
          {b('h2', (' serif', 'H'), 'Heading', 'A big heading for a new section')}
          {b('h3', (' serif small', 'H'), 'Subheading', 'A smaller heading')}
          {b('p', ('', '¶'), 'Normal text', 'Back to normal text')}
        </div>
        <div class="group">
          {b('bold', ('', '<b>B</b>'), 'Bold', 'Bold (Ctrl+B)')}
          {b('italic', ('', '<i>I</i>'), 'Italic', 'Italic (Ctrl+I)')}
          {b('underline', ('', '<u>U</u>'), 'Underline', 'Underline (Ctrl+U)')}
          <div class="colour-menu">
            <button type="button" data-cmd="colours" aria-expanded="false" title="{_('Colour the selected words')}"><span class="ic"><span class="swatches"><i class="tc-lilac-bg"></i><i class="tc-gold-bg"></i></span></span>{_('Colour')} ▾</button>
            <div class="colour-list" hidden>
              {colours}
              <button type="button" data-colour=""><span class="dot none"></span>{_('No colour')}</button>
            </div>
          </div>
        </div>
        <div class="group">
          {b('ul', ('', '•'), 'Bullet list', 'A list with dots')}
          {b('ol', ('', '1.'), 'Numbered list', 'A numbered list')}
          {b('renum', ('', '↺'), 'Restart numbering', 'Numbered lists carry on after a paragraph. Use this to start this list again at 1, or to carry on again.', ' hidden')}
          {b('quote', (' serif', '“'), 'Quote', 'A quote, shown larger')}
        </div>
        <div class="group">
          {b('link', ('', '↗'), 'Link', 'Turn the selected words into a link')}
          {b('clear', ('', '<s>T</s>'), 'Clear formatting', 'Remove bold, italic, underline, colour and links from the selected words')}
        </div>
      </div>"""


EMPTY_PHOTO = lambda: f'<span class="empty-photo">{icon("photo")}<b>{_("No photo yet")}</b><span>{_("Click here to add one")}</span></span>'


def edit_form(csrf, post, topics, ok='', error='', is_new=False):
    """post: the editor's view of a post (blog.read_post, strict=False), or the values just submitted."""
    pid = post.get('id') or ''
    action = '/posts/new' if is_new else f'/posts/{pid}'
    published = post.get('status') == 'published'
    order = ('bg', 'en') if lang() == 'bg' else ('en', 'bg')
    options = ''.join(f'<option value="{esc(t["id"])}"{" selected" if t["id"] == post.get("topic") else ""}>{esc(t[order[0]])} / {esc(t[order[1]])}</option>' for t in topics)
    cover = post.get('cover')
    thumb = f'<img src="/media/{esc(pid)}/{esc(cover)}" alt="">' if cover and pid else EMPTY_PHOTO()
    tabs, panels = [], []
    for code in ('bg', 'en'):
        x = post['text'][code]
        ready = bool(x['title'] and x['summary'] and (x['body'] or post.get('bgben')))
        tabs.append(f'<button class="tab" type="button" role="tab" data-tab="{code}" aria-selected="{"true" if code == "bg" else "false"}">'
                    f'<span class="name">{LANG_NAMES[code]}</span><span class="state{" ready" if ready else ""}" data-done="{code}">{_("Complete") if ready else _("Not finished")}</span></button>')
        panels.append(f"""<section class="panel lang-panel" data-panel="{code}" lang="{code}">
      <h2>{LANG_NAMES[code]}</h2>
      <label for="{code}_title">{_('Title')}</label>
      <input id="{code}_title" name="{code}_title" type="text" maxlength="200" value="{esc(x['title'])}">
      <label for="{code}_summary">{_('Short description')}</label>
      <span class="hint above">{_('One or two sentences that tell readers what the article is about. They appear under the title on the Articles page, and in Google’s search results.')}</span>
      <textarea class="short grow" id="{code}_summary" name="{code}_summary" rows="2" maxlength="400">{esc(x['summary'])}</textarea>
      <label for="{code}_body">{_('Text')}</label>
      {toolbar(code)}
      <textarea id="{code}_body" name="{code}_body" rows="18" maxlength="100000">{esc(x['body'])}</textarea>
      <span class="hint" data-hint>{_('A blank line starts a new paragraph.')} **bold**, *italic*, ++underline++, {{lilac|coloured words}}, ## heading, - list, &gt; quote, [link text](https://…)</span>
    </section>""")
    problems = post.get('problems') or []
    todo = f'<p class="hint">{esc(msg("Before it can be published: " + "; ".join(problems) + "."))}</p>' if problems and not is_new else ''
    buttons = (f"""<button class="btn" type="submit" name="action" value="save" data-save>{_('Save changes')}</button>
        <button class="btn outline" type="submit" name="action" value="unpublish">{_('Unpublish')}</button>""" if published else
               f"""<button class="btn outline" type="submit" name="action" value="save" data-save>{_('Save draft')}</button>
        <button class="btn" type="submit" name="action" value="publish">{_('Publish')}</button>""")
    link = lambda href, ic, label, sub, new_tab=True: (
        f'<a href="{href}"{" target=_blank rel=noopener" if new_tab else ""}><span class="pl-ic">{icon(ic)}</span>'
        f'<span><b>{_(label)}</b><small>{_(sub)}</small></span></a>')
    links = '' if is_new else (f'<nav class="page-links" aria-label="{_("Preview and versions")}">'
                               + link(f'/preview/{esc(pid)}/bg', 'preview', 'Preview in Bulgarian', 'Opens in a new tab')
                               + link(f'/preview/{esc(pid)}/en', 'preview', 'Preview in English', 'Opens in a new tab')
                               + link(f'/posts/{esc(pid)}/versions', 'versions', 'Versions', 'Earlier saved copies', False) + '</nav>')
    state = _('Published – changes go live when you save') if published else (_('New post') if is_new else _('Draft – not on the site'))
    alt = lambda code: post['text'][code]['cover_alt']
    return frame(_('New post') if is_new else (post_title(post) or _('Post')), csrf, '/', f"""
    <div class="head"><h1>{_('New post') if is_new else _('Edit post')}</h1><a href="/">{_('← All posts')}</a></div>
    {message(ok, error)}
    <div class="restore" data-restore hidden><span>{_('Unsaved changes from this browser were found')} (<span data-restore-time></span>).</span>
      <button class="btn small" type="button" data-restore-yes>{_('Restore them')}</button><button class="btn outline small" type="button" data-restore-no>{_('Discard')}</button></div>
    <form method="post" action="{action}" enctype="multipart/form-data" data-editor data-key="{esc(pid or 'new')}" data-saved="{int(post.get('saved') or 0)}">
      <input type="hidden" name="csrf" value="{esc(csrf)}">
      <section class="panel">
        <div class="grid3">
          <div><label for="topic">{_('Topic')}</label><select id="topic" name="topic" required>{options}</select><span class="hint"><a href="/topics">{_('Add or change topics')}</a></span></div>
          <div><label for="date">{_('Date')}</label><input id="date" name="date" type="text" inputmode="numeric" maxlength="10" placeholder="2026-09-19" value="{esc(post.get('date') or '')}">
            <span class="hint">{_('Year-month-day. Empty = the day it is published.')}</span></div>
          <div><label for="bgben">{_('BG BEN link')} <small>{_('only for columns')}</small></label><input id="bgben" name="bgben" type="url" maxlength="300" placeholder="https://bgben.co.uk/…" value="{esc(post.get('bgben') or '')}"></div>
        </div>
        <div class="cover{' has-photo' if cover else ''}" data-cover>
          <div><span class="label">{_('Cover photo')}</span>
            <div class="thumb-box">
              <label class="thumb" title="{_('Click to choose a photo')}">
                <input class="sr" id="photo" name="photo" type="file" accept="image/jpeg,image/png,image/webp">
                <span class="thumb-art" data-thumb>{thumb}</span>
              </label>
              <button class="photo-x" type="button" data-photo-x title="{_('Remove the photo')}" aria-label="{_('Remove the photo')}" hidden>×</button>
            </div>
            <template data-empty-photo>{EMPTY_PHOTO()}</template>
            <span class="hint" data-photo-hint data-with="{_('JPG, PNG or WebP, up to 10 MB. Click the photo to change it, or × to remove it. The location phones save in photos is removed.')}"
              data-without="{_('JPG, PNG or WebP, up to 10 MB. The location phones save in photos is removed.')}">{_('JPG, PNG or WebP, up to 10 MB. The location phones save in photos is removed.')}</span>
            <span class="hint warn-text" data-removed-note hidden>{_('The photo will be removed when you save.')}</span>
            {f'<label class="check" data-remove-check><input type="checkbox" name="remove_photo" value="yes"> {_("Remove the photo")}</label>' if cover else ''}
          </div>
          <div class="alt-fields" data-alt{'' if cover else ' hidden'}>
            <label for="bg_cover_alt">{_('Photo description in Bulgarian')}</label>
            <input id="bg_cover_alt" name="bg_cover_alt" type="text" maxlength="200" value="{esc(alt('bg'))}" lang="bg">
            <label for="en_cover_alt">{_('Photo description in English')}</label>
            <input id="en_cover_alt" name="en_cover_alt" type="text" maxlength="200" value="{esc(alt('en'))}" lang="en">
            <span class="hint">{_('Say in a few words what the photo shows, for example “A mother and daughter talking”. It is read out to blind visitors and helps Google.')}</span>
          </div>
        </div>
      </section>
      <div class="tabs lang-switch" role="tablist" aria-label="{_('Language')}" hidden>{''.join(tabs)}</div>
      {''.join(panels)}
      {todo}
      {links}
      <div class="actionbar">
        <span class="status grow">{state}<span data-autosaved></span></span>
        {buttons}
      </div>
    </form>
""", script=True)


def versions_page(csrf, pid, title, versions, ok='', error=''):
    rows = ''.join(f"""<tr><td>{when(v['time'])}</td><td>{esc(v['title'])}</td><td><span class="tag {esc(v['status'] or 'draft')}">{_('Published') if v['status'] == 'published' else _('Draft')}</span></td>
      <td class="actions"><form method="post" action="/posts/{esc(pid)}/versions/{esc(v['id'])}/restore"><input type="hidden" name="csrf" value="{esc(csrf)}"><button class="btn outline small" type="submit">{_('Restore')}</button></form></td></tr>""" for v in versions)
    table = (f'<table><thead><tr><th>{_("Saved")}</th><th>{_("Title")}</th><th>{_("Status then")}</th><th></th></tr></thead><tbody>{rows}</tbody></table>' if rows
             else f'<p class="empty">{_("No earlier versions yet. One is kept each time you save.")}</p>')
    return frame(_('Versions'), csrf, '/', f"""
    <div class="head"><h1>{_('Versions')}</h1><a href="/posts/{esc(pid)}">{esc(msg('← Back to ' + quoted(title)))}</a></div>
    <p class="info">{_('The last 30 saved versions are kept. Restoring brings back the text and photo of that version; whether the post is published stays as it is now.')}</p>
    {message(ok, error)}{table}""")


def topic_preview(t, label=None):
    """A small version of the topic's cover on the Articles page: its colour and icon."""
    return (f'<span class="topic-preview c-{esc(t.get("colour") or blog.COLOURS[0])}" data-preview><span class="bg"></span>'
            f'<svg class="motif" aria-hidden="true"><use href="#{esc(t.get("icon") or "i-leaf")}"/></svg>'
            f'<span class="label">{esc(label if label is not None else topic_name(t))}</span></span>')


def topic_selects(prefix, t):
    cs = ''.join(f'<option value="{c}"{" selected" if t.get("colour") == c else ""}>{_(COLOUR_NAMES[c])}</option>' for c in blog.COLOURS)
    ic = ''.join(f'<option value="{i}"{" selected" if t.get("icon") == i else ""}>{_(ICON_NAMES[i])}</option>' for i in blog.ICONS)
    return (f'<select name="{prefix}_colour" aria-label="{_("Colour")}" data-colour-select>{cs}</select>',
            f'<select name="{prefix}_icon" aria-label="{_("Icon")}" data-icon-select>{ic}</select>')


def quoted(text):
    return f'„{text}“' if lang() == 'bg' else f'“{text}”'


def blocked_text(t, n):
    name = quoted(topic_name(t))
    return msg(f'{name} can’t be deleted because 1 post uses it. Move it to another topic first.' if n == 1 else
               f'{name} can’t be deleted because {n} posts use it. Move them to another topic first.')


def topics_page(csrf, topics, counts, ok='', error=''):
    first, second = ('bg', 'en') if lang() == 'bg' else ('en', 'bg')
    rows = ''.join(f"""<tr>
      <td>{topic_preview(t)}</td>
      <td><a class="title" href="/topics/{esc(t['id'])}">{esc(t[first])}</a></td>
      <td>{esc(t[second])}</td>
      <td>{counts.get(t['id'], 0)}</td>
      <td class="actions"><span class="icons">
        <a class="icon-btn" href="/topics/{esc(t['id'])}" title="{_('Edit')}" aria-label="{_('Edit')}: {esc(topic_name(t))}">{icon('edit')}</a>
        {delete_link(f"/topics/{esc(t['id'])}/delete", topic_name(t), 'topic', 'It disappears from the editor. This can’t be undone.') if not counts.get(t['id']) else
         f'<button class="icon-btn disabled" type="button" aria-disabled="true" title="{_("Can’t be deleted")}" data-blocked="{esc(blocked_text(t, counts[t["id"]]))}">{icon("delete")}</button>'}
      </span></td></tr>""" for t in topics)
    head = lambda code: 'Български' if code == 'bg' else _('English')
    return frame(_('Topics'), csrf, '/topics', f"""{ICON_SPRITE}
    <div class="head"><h1>{_('Topics')}</h1><a class="btn" href="/topics/new">{_('+ New topic')}</a></div>
    <p class="info">{_('Topics appear as filters on the Articles page once they have a published post.')}</p>
    {message(ok, error)}
    <table class="topics"><thead><tr><th>{_('Looks like')}</th><th>{head(first)}</th><th>{head(second)}</th><th>{_('Posts')}</th><th></th></tr></thead>
    <tbody>{rows}</tbody></table>""")


def topic_form(csrf, t=None, error=''):
    """New topic (t None) or edit an existing one; the preview follows the choices."""
    is_new = not (t and t.get('id'))
    t = {'en': '', 'bg': '', 'colour': blog.COLOURS[1], 'icon': 'i-leaf', **{k: v for k, v in (t or {}).items() if v}}
    colour, icon_select = topic_selects('new', t)
    action = '/topics/new' if is_new else f'/topics/{esc(t["id"])}'
    fields = {'en': f"""<label for="new_en">{_('English name')}</label><input id="new_en" name="new_en" type="text" maxlength="60" value="{esc(t['en'])}" placeholder="e.g. Grief &amp; loss" required{' data-name' if lang() == 'en' else ''}>""",
              'bg': f"""<label for="new_bg">{_('Bulgarian name')}</label><input id="new_bg" name="new_bg" type="text" maxlength="60" value="{esc(t['bg'])}" placeholder="напр. Загуба и скръб" required{' data-name' if lang() == 'bg' else ''}>"""}
    order = ('bg', 'en') if lang() == 'bg' else ('en', 'bg')
    return frame(_('New topic') if is_new else topic_name(t), csrf, '/topics', f"""{ICON_SPRITE}
    <div class="head"><h1>{_('New topic') if is_new else _('Edit topic')}</h1><a href="/topics">{_('← All topics')}</a></div>
    {message(error=error)}
    <form method="post" action="{action}" data-topic-row><input type="hidden" name="csrf" value="{esc(csrf)}">
      <section class="panel new-topic">
        <div>
          {fields[order[0]]}
          {fields[order[1]]}
          <div class="grid2"><div><label for="new_colour">{_('Colour')}</label>{colour.replace('<select ', '<select id="new_colour" ', 1)}</div>
            <div><label for="new_icon">{_('Icon')}</label>{icon_select.replace('<select ', '<select id="new_icon" ', 1)}</div></div>
        </div>
        <div><label>{_('How it looks on the Articles page')}</label>{topic_preview(t, topic_name(t) or _('New topic'))}</div>
      </section>
      <div class="actionbar"><span class="grow status">{_('The topic appears on the site once it has a published post.') if is_new else _('Changes go live on the site when you save.')}</span>
        <a class="btn outline" href="/topics">{_('Cancel')}</a><button class="btn" type="submit" data-save>{_('Add topic') if is_new else _('Save changes')}</button></div>
    </form>""")


def delete_page(csrf, action, name, what, note, error=''):
    """The delete question as a page: used when the script is off, or after a wrong name."""
    back = '/topics' if what == 'topic' else '/'
    return frame(_('Delete topic') if what == 'topic' else _('Delete post'), csrf, back, f"""
    <div class="head"><h1>{delete_heading(what)}</h1><a href="{back}">{_('← Back')}</a></div>
    {message(error=error)}
    <form class="panel delete-page" method="post" action="{esc(action)}">
      <input type="hidden" name="csrf" value="{esc(csrf)}">
      <p><b>{esc(name)}</b></p><p class="hint">{esc(_(note))}</p>
      <label for="confirm_page_name">{_('To confirm, type')} <code>{esc(confirm_name(name))}</code></label>
      <input id="confirm_page_name" name="confirm_name" type="text" autocomplete="off" spellcheck="false" required>
      <div class="btn-row"><a class="btn outline" href="{back}">{_('Cancel')}</a><button class="btn red" type="submit">{_('Delete')}</button></div>
    </form>""")


def bin_page(csrf, items, ok='', error=''):
    rows = ''.join(f"""<tr><td><b>{esc(b['title'])}</b></td><td>{when(b['deleted'])}</td><td>{when(b['purge'])}</td>
      <td class="actions"><form method="post" action="/bin/{esc(b['name'])}/restore"><input type="hidden" name="csrf" value="{esc(csrf)}"><button class="btn outline small" type="submit">{_('Restore')}</button></form></td></tr>""" for b in items)
    table = (f'<table><thead><tr><th>{_("Post")}</th><th>{_("Deleted")}</th><th>{_("Removed for good")}</th><th></th></tr></thead><tbody>{rows}</tbody></table>' if rows
             else f'<p class="empty">{_("The bin is empty.")}</p>')
    return frame(_('Bin'), csrf, '/bin', f"""
    <div class="head"><h1>{_('Bin')}</h1></div>
    <p class="info">{_('Deleted posts stay here for 30 days. A restored post comes back as a draft, so you can check it before publishing.')}</p>
    {message(ok, error)}{table}""")
