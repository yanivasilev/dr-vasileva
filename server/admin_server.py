#!/usr/bin/env python3
"""The website editor at admin.drvasileva.co.uk: secure sign-in, then writing and publishing the articles.

Runs behind nginx on 127.0.0.1:8788. Python standard library, plus Pillow for cover photos.
The posts are kept by server/content_store.py, the screens are in server/editor_pages.py.

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
  ADMIN_CONTENT_DIR  where the posts are kept, default /var/lib/drvasileva-admin/content
  BLOG_OUT_DIR       where the published blog pages go (served by nginx), default /var/www/drvasileva-blog
  SITE_DIST_DIR      the built site, whose page shell the blog uses, default <repository>/dist
  SMTP_* and MAIL_FROM as for the contact form (server/mailer.py)
  LISTEN_HOST, LISTEN_PORT   default 127.0.0.1:8788
  COOKIE_SECURE=0, SESSION_IDLE, SESSION_MAX, LOCK_SECONDS: for local testing only
"""
import base64
import getpass
import hashlib
import hmac
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
from email.parser import BytesParser
from email.policy import HTTP
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, 'build'))
import mailer         # noqa: E402  (server/mailer.py)
import blog           # noqa: E402  (build/blog.py)
import content_store as store   # noqa: E402
import editor_pages as ui       # noqa: E402
from editor_pages import login_page, page   # noqa: E402

ENV = os.environ
DATA_DIR = ENV.get('ADMIN_DATA_DIR', '/var/lib/drvasileva-admin')
ACCOUNT = os.path.join(DATA_DIR, 'account.json')
ORIGIN = ENV.get('ADMIN_ORIGIN', 'https://admin.drvasileva.co.uk').rstrip('/')
FONTS = os.path.join(REPO, 'public', 'fonts')
IMAGES = os.path.join(store.DIST, 'en', 'images')       # the site's own images, for previews
SECURE = ENV.get('COOKIE_SECURE', '1') != '0'
COOKIE = '__Host-drv_session' if SECURE else 'drv_session'
IDLE = int(ENV.get('SESSION_IDLE', 3600))
MAX_AGE = int(ENV.get('SESSION_MAX', 12 * 3600))
LOCK_AFTER, LOCK_SECONDS = 5, int(ENV.get('LOCK_SECONDS', 15 * 60))
IP_FAILS, IP_WINDOW = 10, 15 * 60
MAX_FORM = 64 * 1024
MAX_UPLOAD = 12 * 1024 * 1024            # a post's text plus a cover photo
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
# HTTP
# ---------------------------------------------------------------------------
HEADERS = {
    'Content-Security-Policy': "default-src 'none'; script-src 'self'; style-src 'self'; font-src 'self'; img-src 'self' data: blob:; form-action 'self'; frame-ancestors 'none'; base-uri 'none'",
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'same-origin',     # with no-referrer, browsers label their own form posts "Origin: null"
    'Cache-Control': 'no-store',
    'X-Robots-Tag': 'noindex, nofollow',
    'Cross-Origin-Opener-Policy': 'same-origin',
    'Cross-Origin-Resource-Policy': 'same-origin',
    'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=()',
}
# A preview is shown as a sandbox: it can't run scripts, can't reach her session and can't post forms
PREVIEW_CSP = "sandbox; default-src 'none'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'none'"
OK = {'saved': 'Saved.', 'published': 'Published. The post is now on both sites.', 'unpublished': 'Unpublished. The post is no longer on the site.',
      'created': 'Saved as a draft.', 'restored': 'Restored.', 'deleted': 'The post was moved to the bin.', 'topics': 'Topics saved.', 'topic_added': 'New topic added.', 'topic_deleted': 'The topic was deleted.'}
GENERIC = 'That didn’t work. Check your password and the code, then try again.'
LOCKED = 'Too many attempts. Sign-in is paused for 15 minutes.'


class Handler(BaseHTTPRequestHandler):
    def version_string(self):                     # no software versions in the Server header
        return 'editor'

    # --- helpers
    def send(self, status, body=b'', ctype='text/html; charset=utf-8', headers=None, cache=False, csp=None):
        if isinstance(body, str):
            body = body.encode()
        self.send_response(status)
        for k, v in HEADERS.items():
            if cache and k in ('Cache-Control', 'Cross-Origin-Resource-Policy'):
                continue
            self.send_header(k, csp if csp and k == 'Content-Security-Policy' else v)
        if cache:                  # public files (fonts, images, styles): previews may load them too
            self.send_header('Cache-Control', 'public, max-age=86400')
            self.send_header('Cross-Origin-Resource-Policy', 'cross-origin')
            self.send_header('Access-Control-Allow-Origin', '*')
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
        """Form fields (urlencoded, or multipart with at most one file 'photo'). None if too large or not a form."""
        ctype = self.headers.get('Content-Type', '')
        try:
            length = int(self.headers.get('Content-Length') or 0)
        except ValueError:
            return None
        if ctype.startswith('application/x-www-form-urlencoded') and 0 <= length <= MAX_FORM:
            return {k: v[0] for k, v in urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8', 'replace')).items()}
        if ctype.startswith('multipart/form-data') and 0 < length <= MAX_UPLOAD:
            msg = BytesParser(policy=HTTP).parsebytes(b'Content-Type: ' + ctype.encode() + b'\r\n\r\n' + self.rfile.read(length))
            fields = {}
            for part in msg.iter_parts():
                name = part.get_param('name', header='content-disposition')
                data = part.get_payload(decode=True) or b''
                if name == 'photo':
                    fields['photo'] = data if part.get_filename() and data else None
                elif name:
                    fields[name] = data.decode('utf-8', 'replace')
            return fields
        return None

    # --- routes
    def static(self, path):
        """Public files: styles, the editor's script, fonts and the site's images (for previews)."""
        if path == '/admin.css':
            return self.send(200, ui.CSS, 'text/css; charset=utf-8', cache=True)
        if path == '/editor.js':
            return self.send(200, ui.EDITOR_JS, 'text/javascript; charset=utf-8', cache=True)
        m = re.fullmatch(r'/fonts/([a-z0-9-]+\.(woff2|css))', path)
        if m:
            f = os.path.join(FONTS, m.group(1))
            ctype = 'font/woff2' if m.group(2) == 'woff2' else 'text/css; charset=utf-8'
        else:
            m = re.fullmatch(r'/images/((?:logos/)?[a-z0-9_-]+\.(png|jpg|svg|ico))', path)
            if not m:
                return False
            f = os.path.join(IMAGES, m.group(1))
            ctype = {'png': 'image/png', 'jpg': 'image/jpeg', 'svg': 'image/svg+xml', 'ico': 'image/x-icon'}[m.group(2)]
        if os.path.isfile(f):
            self.send(200, open(f, 'rb').read(), ctype, cache=True)
        else:
            self.send(404, 'Not found', 'text/plain')
        return True

    def not_found(self):
        return self.send(404, page('Not found', '<main class="login"><div class="card"><h1>Not found</h1><p class="sub"><a href="/">Back to the editor</a></p></div></main>'))

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path, query = url.path, urllib.parse.parse_qs(url.query)
        if self.static(path) is not False:
            return
        s = self.session()
        if path == '/login':
            if s:
                return self.redirect('/')
            return self.send(200, login_page(notice='' if load_account() else 'The editor has not been set up yet. Run the setup command on the server (see deploy/README.md).'))
        acc = load_account()
        if not s or not acc:
            return self.redirect('/login')
        ok = OK.get((query.get('ok') or [''])[0], '')
        try:
            if path == '/':
                q = (query.get('q') or [''])[0].strip()[:100]
                return self.send(200, ui.posts_list(s['csrf'], store.list_posts(), store.topics(), acc.get('previous_login'), ok, query=q))
            if path == '/posts/new':
                empty = dict(id='', topic=None, date='', bgben='', status='draft', cover=None,
                             text={l: dict(title='', summary='', slug='', cover_alt='', body='') for l in blog.LANGS})
                return self.send(200, ui.edit_form(s['csrf'], empty, store.topics(), is_new=True))
            m = re.fullmatch(r'/posts/([a-z0-9-]{1,80})', path)
            if m:
                post = store.get(m.group(1))
                post['saved'] = os.path.getmtime(os.path.join(post['folder'], 'post.json'))
                return self.send(200, ui.edit_form(s['csrf'], post, store.topics(), ok, error=s.pop('flash', '')))
            m = re.fullmatch(r'/posts/([a-z0-9-]{1,80})/versions', path)
            if m:
                post = store.get(m.group(1))
                return self.send(200, ui.versions_page(s['csrf'], post['id'], post['text']['bg']['title'] or post['text']['en']['title'], store.versions(post['id']), ok))
            m = re.fullmatch(r'/preview/([a-z0-9-]{1,80})/(bg|en)', path)
            if m:
                return self.send(200, store.preview(m.group(1), m.group(2)), csp=PREVIEW_CSP)
            m = re.fullmatch(r'/media/([a-z0-9-]{1,80})/(cover-[0-9a-f]{8}\.jpg|[a-z0-9-]+\.(?:jpg|png|webp))', path)
            if m:
                f = os.path.join(store.folder_of(m.group(1)), m.group(2))
                if os.path.isfile(f):
                    return self.send(200, open(f, 'rb').read(), {'png': 'image/png', 'webp': 'image/webp'}.get(f.rsplit('.', 1)[1], 'image/jpeg'))
                return self.not_found()
            if path == '/topics':
                counts = {}
                for p in store.list_posts():
                    counts[p['topic']] = counts.get(p['topic'], 0) + 1
                return self.send(200, ui.topics_page(s['csrf'], store.topics(), counts, ok))
            if path == '/topics/new':
                return self.send(200, ui.topic_form(s['csrf']))
            m = re.fullmatch(r'/topics/([a-z0-9-]{1,80})', path)
            if m:
                t = next((x for x in store.topics() if x['id'] == m.group(1)), None)
                if not t:
                    return self.not_found()
                used = sum(1 for p in store.list_posts() if p['topic'] == t['id'])
                return self.send(200, ui.topic_form(s['csrf'], t, posts=used))
            if path == '/bin':
                return self.send(200, ui.bin_page(s['csrf'], store.list_bin(), ok))
        except store.EditError:
            return self.not_found()
        return self.not_found()

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
        try:
            return self.change(path, form, s)
        except store.EditError as e:
            if getattr(e, 'pid', None):                        # saved, but not publishable yet
                s['flash'] = str(e)
                return self.redirect(f'/posts/{e.pid}')
            return self.change_failed(path, form, s, str(e))
        except blog.PostError as e:
            return self.change_failed(path, form, s, f'Something in the posts needs fixing: {e}')

    def change(self, path, form, s):
        m = re.fullmatch(r'/posts/(new|[a-z0-9-]{1,80})', path)
        if m:
            action = form.get('action') if form.get('action') in ('save', 'publish', 'unpublish') else 'save'
            is_new = m.group(1) == 'new'
            pid = store.save(None if is_new else m.group(1), form, action, form.get('photo'), form.get('remove_photo') == 'yes')
            code = {'publish': 'published', 'unpublish': 'unpublished'}.get(action, 'created' if is_new else 'saved')
            return self.redirect(f'/posts/{pid}?ok={code}')
        m = re.fullmatch(r'/posts/([a-z0-9-]{1,80})/delete', path)
        if m:
            if form.get('confirm') != 'yes':
                raise store.EditError('Tick the box to confirm.')
            store.delete(m.group(1))
            return self.redirect('/?ok=deleted')
        m = re.fullmatch(r'/posts/([a-z0-9-]{1,80})/versions/(\d{8}-\d{6}-\d{6})/restore', path)
        if m:
            store.restore_version(m.group(1), m.group(2))
            return self.redirect(f'/posts/{m.group(1)}?ok=restored')
        m = re.fullmatch(r'/bin/([a-z0-9-]{1,80}--\d{8}-\d{6}-\d{6})/restore', path)
        if m:
            pid = store.restore_bin(m.group(1))
            return self.redirect(f'/posts/{pid}?ok=restored')
        if path == '/topics/new':
            if not (form.get('new_en', '').strip() and form.get('new_bg', '').strip()):
                raise store.EditError('Please give the topic a name in both English and Bulgarian.')
            store.save_topics({}, {k: form.get(f'new_{k}') or '' for k in ('en', 'bg', 'colour', 'icon')})
            return self.redirect('/topics?ok=topic_added')
        m = re.fullmatch(r'/topics/([a-z0-9-]{1,80})/delete', path)
        if m:
            if form.get('confirm') != 'yes':
                raise store.EditError('Tick the box to confirm.')
            if not any(t['id'] == m.group(1) for t in store.topics()):
                raise store.EditError('No such topic.')
            store.save_topics({}, None, m.group(1))
            return self.redirect('/topics?ok=topic_deleted')
        m = re.fullmatch(r'/topics/([a-z0-9-]{1,80})', path)
        if m:
            if not any(t['id'] == m.group(1) for t in store.topics()):
                raise store.EditError('No such topic.')
            if not (form.get('new_en', '').strip() and form.get('new_bg', '').strip()):
                raise store.EditError('Please give the topic a name in both English and Bulgarian.')
            store.save_topics({m.group(1): {k: form.get(f'new_{k}') for k in ('en', 'bg', 'colour', 'icon')}})
            return self.redirect('/topics?ok=topics')
        return self.send(404, 'Not found', 'text/plain')

    def change_failed(self, path, form, s, error):
        """Show the problem on the same screen; a post form keeps everything she typed."""
        m = re.fullmatch(r'/posts/(new|[a-z0-9-]{1,80})', path)
        if m:
            is_new = m.group(1) == 'new'
            try:
                current = None if is_new else store.get(m.group(1))
            except store.EditError:
                return self.not_found()
            typed = dict(id='' if is_new else m.group(1), topic=form.get('topic'), date=form.get('date', ''), bgben=form.get('bgben', ''),
                         status=current['status'] if current else 'draft', cover=current['cover'] if current else None,
                         text={l: {k: form.get(f'{l}_{k}', '') for k in ('title', 'summary', 'slug', 'cover_alt', 'body')} for l in blog.LANGS})
            return self.send(400, ui.edit_form(s['csrf'], typed, store.topics(), error=error, is_new=is_new))
        if path.startswith('/posts/') and path.endswith('/delete'):
            return self.redirect(path[:-len('/delete')])
        if '/versions/' in path:
            pid = path.split('/')[2]
            post = store.get(pid)
            return self.send(400, ui.versions_page(s['csrf'], pid, post['text']['bg']['title'], store.versions(pid), error=error))
        if path.startswith('/bin/'):
            return self.send(400, ui.bin_page(s['csrf'], store.list_bin(), error=error))
        m = re.fullmatch(r'/topics/(new|[a-z0-9-]{1,80})(/delete)?', path)
        if m:
            values = {k: form.get(f'new_{k}', '') for k in ('en', 'bg', 'colour', 'icon')}
            current = next((x for x in store.topics() if x['id'] == m.group(1)), None)
            if m.group(1) != 'new' and not current:
                return self.not_found()
            if m.group(2):                                   # delete refused: show the topic as it is
                values = current
            elif current:
                values['id'] = current['id']
            used = sum(1 for p in store.list_posts() if current and p['topic'] == current['id'])
            return self.send(400, ui.topic_form(s['csrf'], values, error, posts=used))
        return self.send(400, 'Bad request', 'text/plain')

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
        store.init()                     # first start: copy the posts; every start: rebuild the blog pages
        addr = (ENV.get('LISTEN_HOST', '127.0.0.1'), int(ENV.get('LISTEN_PORT', '8788')))
        print('editor listening on %s:%d' % addr, file=sys.stderr)
        ThreadingHTTPServer(addr, Handler).serve_forever()
