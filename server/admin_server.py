#!/usr/bin/env python3
"""The website editor at admin.drvasileva.co.uk. This part: secure sign-in.

Runs behind nginx on 127.0.0.1:8788. Python standard library only.

Security:
  - One account, created only with a command on the server (no sign-up page, no "forgot password" email).
  - Password (stored as a scrypt hash) plus a 6-digit code from an authenticator app (TOTP), or a one-time backup code.
  - 5 wrong tries lock sign-in for 15 minutes; one address may fail 10 times in 15 minutes. Both are emailed.
  - Every successful sign-in is emailed, and the dashboard shows the previous one.
  - Session cookie: __Host- prefix, Secure, HttpOnly, SameSite=Strict; ends after 1 hour idle and always after 12 hours.
  - Every form post needs this site's Origin and, when signed in, the session's CSRF token.
  - Strict Content Security Policy, no framing, no caching, not indexed.

Commands (run on the server as the service user, see deploy/README.md):
  admin_server.py setup          create the account: password, authenticator app, backup codes
  admin_server.py password       change the password
  admin_server.py reset-2fa      new authenticator key (for example after losing the phone)
  admin_server.py backup-codes   new backup codes (the old ones stop working)
  admin_server.py status         show whether the account exists and when it was last used

Settings (environment, see deploy/admin.env.example):
  ADMIN_ORIGIN       https://admin.drvasileva.co.uk (form posts from anywhere else are refused)
  ADMIN_DATA_DIR     where the account is kept, default /var/lib/drvasileva-admin
  ADMIN_ALERT_TO     where sign-in emails go
  CONTENT_DIR        the blog's content folder, default <repository>/content
  SMTP_* and MAIL_FROM as for the contact form (server/mailer.py)
  LISTEN_HOST, LISTEN_PORT   default 127.0.0.1:8788
  COOKIE_SECURE=0, SESSION_IDLE, SESSION_MAX, LOCK_SECONDS: for local testing only
"""
import base64
import getpass
import hashlib
import hmac
import html
import json
import os
import re
import secrets
import shutil
import struct
import subprocess
import sys
import threading
import time
import urllib.parse
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, 'build'))
import mailer  # noqa: E402  (server/mailer.py)
import blog    # noqa: E402  (build/blog.py)

ENV = os.environ
DATA_DIR = ENV.get('ADMIN_DATA_DIR', '/var/lib/drvasileva-admin')
ACCOUNT = os.path.join(DATA_DIR, 'account.json')
ORIGIN = ENV.get('ADMIN_ORIGIN', 'https://admin.drvasileva.co.uk').rstrip('/')
CONTENT_DIR = ENV.get('CONTENT_DIR', os.path.join(REPO, 'content'))
FONTS = os.path.join(REPO, 'public', 'fonts')
SECURE = ENV.get('COOKIE_SECURE', '1') != '0'
COOKIE = '__Host-drv_session' if SECURE else 'drv_session'
IDLE = int(ENV.get('SESSION_IDLE', 3600))
MAX_AGE = int(ENV.get('SESSION_MAX', 12 * 3600))
LOCK_AFTER, LOCK_SECONDS = 5, int(ENV.get('LOCK_SECONDS', 15 * 60))
IP_FAILS, IP_WINDOW = 10, 15 * 60
MAX_FORM = 8 * 1024
SCRYPT = dict(n=2 ** 15, r=8, p=1)
APP = 'Dr Vasileva editor'

_lock = threading.Lock()
_sessions = {}                 # sha256(token) -> {created, seen, csrf}
_ip_fails = {}                 # address -> [times]
_state = {'fails': 0, 'locked_until': 0}
_login_lock = threading.Lock()   # one sign-in at a time, so a code can never be used twice


# ---------------------------------------------------------------------------
# Account: password, authenticator key, backup codes
# ---------------------------------------------------------------------------
def b64(b):
    return base64.b64encode(b).decode()


def hash_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, dklen=32, maxmem=64 * 2 ** 20, **SCRYPT)
    return f"scrypt${SCRYPT['n']}${SCRYPT['r']}${SCRYPT['p']}${b64(salt)}${b64(digest)}"


def check_password(password, stored):
    try:
        _, n, r, p, salt, digest = stored.split('$')
        test = hashlib.scrypt(password.encode(), salt=base64.b64decode(salt), n=int(n), r=int(r), p=int(p),
                              dklen=32, maxmem=64 * 2 ** 20)
        return hmac.compare_digest(test, base64.b64decode(digest))
    except (ValueError, TypeError):
        return False


def totp(secret, counter):
    """RFC 6238: the 6-digit code for one 30-second step"""
    key = base64.b32decode(secret + '=' * (-len(secret) % 8))
    mac = hmac.new(key, struct.pack('>Q', counter), 'sha1').digest()
    offset = mac[-1] & 15
    return f"{(struct.unpack('>I', mac[offset:offset + 4])[0] & 0x7fffffff) % 1000000:06d}"


def new_backup_codes():
    codes = [f'{secrets.token_hex(2)}-{secrets.token_hex(2)}-{secrets.token_hex(2)}' for _ in range(10)]
    return codes, [hashlib.sha256(c.encode()).hexdigest() for c in codes]


def load_account():
    try:
        with open(ACCOUNT, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def save_account(acc):
    os.makedirs(DATA_DIR, mode=0o700, exist_ok=True)
    tmp = ACCOUNT + '.tmp'
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(acc, f)
    os.replace(tmp, ACCOUNT)


def check_second_factor(acc, code):
    """A current authenticator code (each code works once) or an unused backup code. Returns what to save, or None."""
    code = code.strip().lower().replace(' ', '')
    if re.fullmatch(r'\d{6}', code):
        now = int(time.time() // 30)
        for step in (now - 1, now, now + 1):
            if step > acc.get('totp_last', 0) and hmac.compare_digest(totp(acc['totp'], step), code):
                return {'totp_last': step}
        return None
    if re.fullmatch(r'[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}', code):
        h = hashlib.sha256(code.encode()).hexdigest()
        left = [x for x in acc.get('backup', []) if not hmac.compare_digest(x, h)]
        if len(left) < len(acc.get('backup', [])):
            return {'backup': left}
    return None


# ---------------------------------------------------------------------------
# Sessions and sign-in limits
# ---------------------------------------------------------------------------
def new_session():
    token = secrets.token_urlsafe(32)
    now = time.time()
    with _lock:
        _sessions[hashlib.sha256(token.encode()).hexdigest()] = {'created': now, 'seen': now, 'csrf': secrets.token_urlsafe(24)}
    return token


def get_session(token):
    if not token:
        return None
    key = hashlib.sha256(token.encode()).hexdigest()
    now = time.time()
    with _lock:
        for k in [k for k, s in _sessions.items() if now - s['seen'] > IDLE or now - s['created'] > MAX_AGE]:
            del _sessions[k]
        s = _sessions.get(key)
        if s:
            s['seen'] = now
            s['key'] = key
        return s


def end_session(s):
    with _lock:
        _sessions.pop(s.get('key'), None)


def ip_blocked(ip):
    now = time.time()
    with _lock:
        recent = [t for t in _ip_fails.get(ip, []) if now - t < IP_WINDOW]
        _ip_fails[ip] = recent
        return len(recent) >= IP_FAILS


def record_failure(ip):
    """Returns True when this failure locks sign-in."""
    now = time.time()
    with _lock:
        _ip_fails.setdefault(ip, []).append(now)
        _state['fails'] += 1
        if _state['fails'] >= LOCK_AFTER:
            _state['fails'] = 0
            _state['locked_until'] = now + LOCK_SECONDS
            return True
    return False


def alert(subject, lines):
    """Email the owner in the background; a mail problem never blocks sign-in."""
    to = ENV.get('ADMIN_ALERT_TO')
    if not to:
        return

    def run():
        try:
            mailer.send(to, subject, '\n'.join(lines), msgid_domain=urllib.parse.urlparse(ORIGIN).hostname)
        except Exception as e:      # noqa: BLE001
            print('alert email failed:', type(e).__name__, file=sys.stderr)
    threading.Thread(target=run, daemon=True).start()


def when(t):
    return time.strftime('%d %b %Y, %H:%M', time.localtime(t))


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
esc = html.escape
CSS = """
:root { --green: #4F6F52; --green-dark: #344E38; --green-deep: #2C4430; --cream: #FAF7F2; --sand: #EDE6DA; --lilac: #B9A3C9; --lilac-deep: #8E79A6; --muted: #5E625D; --red: #A4423A; --white: #fff; }
* { box-sizing: border-box; }
body { margin: 0; font-family: Manrope, system-ui, sans-serif; color: #232823; background: var(--cream); line-height: 1.6; -webkit-font-smoothing: antialiased; }
h1, h2 { font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 600; line-height: 1.1; color: var(--green-deep); margin: 0 0 .4em; }
a { color: var(--green-dark); }
.word { font-weight: 600; letter-spacing: .32em; font-size: .9rem; color: inherit; text-decoration: none; }
.login { min-height: 100vh; display: grid; place-items: center; padding: 24px; background: radial-gradient(circle at 20% 10%, #4F6F52, #2C4430 60%); }
.card { width: 100%; max-width: 420px; background: var(--white); border-radius: 22px; padding: 36px 32px; box-shadow: 0 30px 60px -30px rgba(0,0,0,.5); }
.card .word { display: block; color: var(--green-deep); margin-bottom: 26px; }
.card h1 { font-size: 2.2rem; }
.card p.sub { color: var(--muted); margin: 0 0 22px; font-size: .95rem; }
label { display: block; font-weight: 600; font-size: .88rem; margin: 16px 0 6px; color: var(--green-deep); }
label small { font-weight: 500; color: var(--muted); }
input[type=password], input[type=text] { width: 100%; font: inherit; font-size: 1rem; padding: 13px 15px; border: 1px solid #D9D2C5; border-radius: 12px; background: var(--cream); color: inherit; }
input:focus { outline: 2px solid var(--lilac); outline-offset: 1px; border-color: var(--lilac-deep); }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; font: inherit; font-weight: 700; font-size: .95rem; padding: 13px 22px; border-radius: 999px; border: 0; cursor: pointer; background: var(--green-dark); color: var(--white); text-decoration: none; }
.btn.wide { width: 100%; margin-top: 24px; }
.btn.light { background: rgba(250,247,242,.12); color: var(--cream); border: 1px solid rgba(250,247,242,.25); padding: 9px 18px; }
.error { background: #F8E9E7; color: var(--red); border-radius: 12px; padding: 12px 14px; font-size: .92rem; font-weight: 600; margin: 0 0 6px; }
.note { margin: 22px 0 0; font-size: .82rem; color: var(--muted); text-align: center; }
header.top { background: var(--green-deep); color: var(--cream); }
header.top .wrap { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding-top: 16px; padding-bottom: 16px; }
header.top .word span { opacity: .6; letter-spacing: .1em; font-weight: 500; margin-left: 10px; }
header.top form { margin: 0; }
.wrap { max-width: 1040px; margin: 0 auto; padding: 0 24px; }
main.wrap { padding-top: 40px; padding-bottom: 60px; }
.info { display: flex; flex-wrap: wrap; gap: 10px 26px; font-size: .88rem; color: var(--muted); margin-bottom: 30px; }
.info b { color: var(--green-deep); }
table { width: 100%; border-collapse: collapse; background: var(--white); border-radius: 16px; overflow: hidden; box-shadow: 0 16px 40px -32px rgba(44,68,48,.6); }
th, td { text-align: left; padding: 12px 16px; border-bottom: 1px solid var(--sand); font-size: .92rem; vertical-align: top; }
th { font-size: .74rem; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); background: #F6F2EA; }
td small { display: block; color: var(--muted); }
.tag { display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: .76rem; font-weight: 700; }
.tag.published { background: #E4ECE3; color: var(--green-dark); }
.tag.draft { background: #EEE7F3; color: #5E4A78; }
.soon { margin-top: 26px; padding: 16px 18px; border-radius: 14px; background: var(--sand); font-size: .92rem; }
@media (max-width: 640px) { th:nth-child(3), td:nth-child(3) { display: none; } .card { padding: 28px 22px; } }
"""


def page(title, body, cls=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(title)} – {APP}</title>
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="stylesheet" href="/admin.css">
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


def dashboard(s, acc):
    try:
        _, posts = blog.load(CONTENT_DIR, include_drafts=True)
        rows = ''.join(
            f'<tr><td><b>{esc(p["text"]["bg"]["title"])}</b><small>{esc(p["text"]["en"]["title"])}</small></td>'
            f'<td><span class="tag {p["status"]}">{"Published" if p["status"] == "published" else "Draft"}</span></td>'
            f'<td>{esc(blog.format_date(p["date"], "en"))}</td></tr>' for p in posts)
        table = f'<table><thead><tr><th>Title (BG / EN)</th><th>Status</th><th>Date</th></tr></thead><tbody>{rows}</tbody></table>'
    except Exception as e:      # noqa: BLE001  (a broken post must not lock her out of the editor)
        table = f'<p class="error">The posts could not be read: {esc(str(e))}</p>'
    prev = acc.get('previous_login')
    prev_text = f'{when(prev["time"])} from {esc(prev["ip"])}' if prev else 'this is the first sign-in'
    return page('Posts', f'''<header class="top"><div class="wrap">
    <a class="word" href="/">DR VASILEVA<span>Editor</span></a>
    <form method="post" action="/logout"><input type="hidden" name="csrf" value="{esc(s['csrf'])}"><button class="btn light" type="submit">Sign out</button></form>
  </div></header>
  <main class="wrap">
    <h1>Posts</h1>
    <div class="info"><span>Previous sign-in: <b>{prev_text}</b></span><span>Signed out automatically after 1 hour without activity.</span></div>
    {table}
    <p class="soon">Writing, editing and publishing posts will be added here in the next update.</p>
  </main>''')


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
HEADERS = {
    'Content-Security-Policy': "default-src 'none'; style-src 'self'; font-src 'self'; img-src 'self' data:; form-action 'self'; frame-ancestors 'none'; base-uri 'none'",
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'same-origin',     # with no-referrer, browsers label their own form posts "Origin: null"
    'Cache-Control': 'no-store',
    'X-Robots-Tag': 'noindex, nofollow',
    'Cross-Origin-Opener-Policy': 'same-origin',
    'Cross-Origin-Resource-Policy': 'same-origin',
    'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=()',
}
GENERIC = 'That didn’t work. Check your password and the code, then try again.'
LOCKED = 'Too many attempts. Sign-in is paused for 15 minutes.'


class Handler(BaseHTTPRequestHandler):
    def version_string(self):                     # no software versions in the Server header
        return 'editor'

    # --- helpers
    def send(self, status, body=b'', ctype='text/html; charset=utf-8', headers=None, cache=False):
        if isinstance(body, str):
            body = body.encode()
        self.send_response(status)
        for k, v in HEADERS.items():
            if not (cache and k == 'Cache-Control'):
                self.send_header(k, v)
        if cache:
            self.send_header('Cache-Control', 'public, max-age=86400')
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        for k, v in (headers or []):
            self.send_header(k, v)
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)

    def redirect(self, to, headers=None):
        self.send(303, '', headers=[('Location', to)] + (headers or []))

    def ip(self):
        return self.headers.get('X-Real-IP') or self.client_address[0]

    def session(self):
        c = SimpleCookie()
        try:
            c.load(self.headers.get('Cookie', ''))
        except Exception:           # noqa: BLE001
            return None
        return get_session(c[COOKIE].value if COOKIE in c else None)

    def cookie(self, token, max_age):
        flags = '; Secure' if SECURE else ''
        return ('Set-Cookie', f'{COOKIE}={token}; Path=/; HttpOnly; SameSite=Strict; Max-Age={max_age}{flags}')

    def same_origin(self):
        # A browser always sends one of these with a form post; pages on other sites can't fake either
        origin = self.headers.get('Origin')
        if origin and origin != 'null':
            return origin.rstrip('/') == ORIGIN
        return self.headers.get('Sec-Fetch-Site') == 'same-origin'

    def form(self):
        length = int(self.headers.get('Content-Length') or 0)
        if not 0 <= length <= MAX_FORM or not self.headers.get('Content-Type', '').startswith('application/x-www-form-urlencoded'):
            return None
        return {k: v[0] for k, v in urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8', 'replace')).items()}

    # --- routes
    def do_GET(self):
        path = self.path.split('?')[0]
        if path == '/admin.css':
            return self.send(200, CSS, 'text/css; charset=utf-8', cache=True)
        m = re.fullmatch(r'/fonts/([a-z0-9-]+\.(woff2|css))', path)
        if m:
            f = os.path.join(FONTS, m.group(1))
            if os.path.isfile(f):
                return self.send(200, open(f, 'rb').read(), 'font/woff2' if m.group(2) == 'woff2' else 'text/css; charset=utf-8', cache=True)
            return self.send(404, 'Not found', 'text/plain')
        s = self.session()
        if path == '/login':
            if s:
                return self.redirect('/')
            acc = load_account()
            return self.send(200, login_page(notice='' if acc else 'The editor has not been set up yet. Run the setup command on the server (see deploy/README.md).'))
        if path == '/':
            acc = load_account()
            if not s or not acc:
                return self.redirect('/login')
            return self.send(200, dashboard(s, acc))
        return self.send(404, page('Not found', '<main class="login"><div class="card"><h1>Not found</h1><p class="sub"><a href="/">Back to the editor</a></p></div></main>'))

    do_HEAD = do_GET

    def do_POST(self):
        path = self.path.split('?')[0]
        if not self.same_origin():
            return self.send(403, 'Forbidden', 'text/plain')
        form = self.form()
        if form is None:
            return self.send(400, 'Bad request', 'text/plain')
        if path == '/login':
            with _login_lock:
                return self.login(form)
        s = self.session()
        if not s or not hmac.compare_digest(form.get('csrf', ''), s['csrf']):
            return self.send(403, 'Forbidden', 'text/plain')
        if path == '/logout':
            end_session(s)
            return self.redirect('/login', [self.cookie('', 0)])
        return self.send(404, 'Not found', 'text/plain')

    def login(self, form):
        acc, ip, now = load_account(), self.ip(), time.time()
        if not acc:
            return self.redirect('/login')
        if ip_blocked(ip) or _state['locked_until'] > now:
            return self.send(429, login_page(LOCKED))
        password, code = form.get('password', '')[:200], form.get('code', '')[:20]
        ok = check_password(password, acc['password'])          # always checked, so timing says nothing
        changes = check_second_factor(acc, code) if ok else None
        if not changes:
            print(f'sign-in failed from {ip}', file=sys.stderr)
            if record_failure(ip):
                alert('Website editor: sign-in locked', [
                    f'There were {LOCK_AFTER} wrong sign-in attempts, so sign-in to the editor is paused for 15 minutes.',
                    '', f'Last attempt: {when(now)} from {ip}', f'Browser: {self.headers.get("User-Agent", "-")[:200]}',
                    '', 'If this wasn’t you, nothing needs doing: the password and code were not accepted.',
                    'If it keeps happening, change the password on the server (see deploy/README.md).'])
            return self.send(400, login_page(GENERIC))
        with _lock:
            _state['fails'] = 0
        acc.update(changes)
        if acc.get('last_login'):
            acc['previous_login'] = acc['last_login']
        acc['last_login'] = {'time': now, 'ip': ip}
        save_account(acc)
        token = new_session()
        backup_left = f' {len(acc["backup"])} backup codes are left.' if 'backup' in changes else ''
        alert('Website editor: new sign-in', [
            'Someone signed in to the website editor.', '', f'Time: {when(now)}', f'Address: {ip}',
            f'Browser: {self.headers.get("User-Agent", "-")[:200]}',
            *(['', f'A backup code was used.{backup_left}'] if backup_left else []),
            '', 'If this wasn’t you, change the password and reset the authenticator on the server straight away (see deploy/README.md).'])
        print(f'sign-in from {ip}', file=sys.stderr)
        return self.redirect('/', [self.cookie(token, MAX_AGE)])

    def do_PUT(self):
        self.send(405, 'Method not allowed', 'text/plain')

    do_DELETE = do_PATCH = do_PUT

    def log_message(self, fmt, *args):            # method, path and status only: no form data
        sys.stderr.write('%s %s %s\n' % (self.command, self.path.split('?')[0][:80], args[1] if len(args) > 1 else ''))


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
def ask_password():
    while True:
        p1 = getpass.getpass('New password (at least 12 characters): ')
        if len(p1) < 12:
            print('Too short, please use at least 12 characters (a few words together work well).')
            continue
        if getpass.getpass('Type it again: ') != p1:
            print('The two passwords are different, please try again.')
            continue
        return p1


def new_authenticator(acc):
    secret = base64.b32encode(secrets.token_bytes(20)).decode().rstrip('=')
    label = urllib.parse.quote(f'{APP}:admin')
    uri = f'otpauth://totp/{label}?secret={secret}&issuer={urllib.parse.quote(APP)}&digits=6&period=30'
    print('\nAdd the editor to an authenticator app (Google Authenticator, Microsoft Authenticator, 2FAS, Aegis …):')
    if shutil.which('qrencode'):
        print('Scan this code with the app:\n')
        subprocess.run(['qrencode', '-t', 'ANSIUTF8', uri], check=False)
    print('Or choose "enter a setup key" and type:', ' '.join(secret[i:i + 4] for i in range(0, len(secret), 4)))
    print('  (account name: Dr Vasileva editor, time-based)\n')
    for _ in range(5):
        code = input('Type the 6-digit code the app now shows: ').strip().replace(' ', '')
        now = int(time.time() // 30)
        if any(totp(secret, step) == code for step in (now - 1, now, now + 1)):
            acc['totp'], acc['totp_last'] = secret, 0
            print('The authenticator app works.')
            return
        print('That code does not match. Check the phone\'s time is set automatically, then try again.')
    sys.exit('Stopped: the authenticator was not confirmed, nothing was changed.')


def new_codes(acc):
    codes, hashes = new_backup_codes()
    acc['backup'] = hashes
    print('\nBackup codes. Each works once, instead of the app code. Print or write them down and keep them somewhere safe:\n')
    for i in range(0, 10, 2):
        print(f'   {codes[i]}      {codes[i + 1]}')
    print()


def command(name):
    acc = load_account()
    if name == 'status':
        if not acc:
            return print(f'No account yet ({ACCOUNT}). Run: admin_server.py setup')
        last = acc.get('last_login')
        return print(f'Account set up. Last sign-in: {when(last["time"]) + " from " + last["ip"] if last else "never"}. '
                     f'Backup codes left: {len(acc.get("backup", []))}.')
    if name == 'setup':
        if acc:
            sys.exit('The account already exists. Use "password", "reset-2fa" or "backup-codes" to change it.')
        acc = {'created': time.time()}
        acc['password'] = hash_password(ask_password())
        new_authenticator(acc)
        new_codes(acc)
    elif not acc:
        sys.exit('No account yet. Run: admin_server.py setup')
    elif name == 'password':
        acc['password'] = hash_password(ask_password())
    elif name == 'reset-2fa':
        new_authenticator(acc)
    elif name == 'backup-codes':
        new_codes(acc)
    else:
        sys.exit(__doc__)
    save_account(acc)
    print('Saved. Restart the editor so everyone is signed out: systemctl restart drvasileva-admin')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        command(sys.argv[1])
    else:
        addr = (ENV.get('LISTEN_HOST', '127.0.0.1'), int(ENV.get('LISTEN_PORT', '8788')))
        print('editor listening on %s:%d' % addr, file=sys.stderr)
        ThreadingHTTPServer(addr, Handler).serve_forever()
