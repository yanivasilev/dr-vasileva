#!/usr/bin/env python3
"""Contact form service for drvasileva.co.uk and drvasileva.bg.

Runs behind nginx (POST /api/contact is proxied here). It checks the Cloudflare
Turnstile token, validates the form and sends the message through your own mail
server (e.g. mailcow) over SMTP. Python standard library only.

Settings come from environment variables (see deploy/contact.env.example):
  TURNSTILE_SECRET_KEY   Turnstile secret key
  SMTP_HOST              e.g. mail.example.com
  SMTP_PORT              465 (SSL) or 587 (STARTTLS)
  SMTP_SECURITY          ssl | starttls | none (none is for local testing only)
  SMTP_USER, SMTP_PASSWORD   mailbox used to send, e.g. website@drvasileva.co.uk
  MAIL_FROM              e.g. "Website <website@drvasileva.co.uk>"
  MAIL_TO_EN, MAIL_TO_BG     inbox for each domain (MAIL_TO_BG falls back to MAIL_TO_EN)
  LISTEN_HOST, LISTEN_PORT   default 127.0.0.1:8787
"""
import email.utils
import json
import os
import re
import smtplib
import ssl
import sys
import threading
import time
import urllib.parse
import urllib.request
from email.message import EmailMessage
from email.parser import BytesParser
from email.policy import HTTP
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ENV = os.environ
TURNSTILE_URL = ENV.get('TURNSTILE_VERIFY_URL', 'https://challenges.cloudflare.com/turnstile/v0/siteverify')
LIMITS = {'name': 100, 'email': 150, 'phone': 30, 'topic': 80, 'reply': 20, 'language': 20, 'message': 3000}
EMAIL_RE = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
MAX_BODY = 64 * 1024
RATE = {'window': 600, 'max': 5}          # at most 5 messages per IP every 10 minutes
_hits, _lock = {}, threading.Lock()


def rate_limited(ip):
    now = time.time()
    with _lock:
        hits = [t for t in _hits.get(ip, []) if now - t < RATE['window']]
        limited = len(hits) >= RATE['max']
        if not limited:
            hits.append(now)
        _hits[ip] = hits
        return limited


def parse_form(content_type, body):
    """Return the form fields as a dict (multipart/form-data or urlencoded)."""
    if content_type.startswith('multipart/form-data'):
        msg = BytesParser(policy=HTTP).parsebytes(b'Content-Type: ' + content_type.encode() + b'\r\n\r\n' + body)
        fields = {}
        for part in msg.iter_parts():
            name = part.get_param('name', header='content-disposition')
            if name:
                # browsers send form fields as UTF-8 without declaring a charset
                fields[name] = '' if part.get_filename() else (part.get_payload(decode=True) or b'').decode('utf-8', 'replace')
        return fields
    return {k: v[0] for k, v in urllib.parse.parse_qs(body.decode('utf-8', 'replace')).items()}


def turnstile_ok(token, ip):
    data = urllib.parse.urlencode({'secret': ENV.get('TURNSTILE_SECRET_KEY', ''), 'response': token, 'remoteip': ip}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(TURNSTILE_URL, data=data), timeout=10) as r:
            return bool(json.load(r).get('success'))
    except Exception as e:
        print('turnstile error:', e, file=sys.stderr)
        return False


def send_mail(site, to, data):
    msg = EmailMessage()
    msg['Subject'] = f"Website message from {data['name']}"
    msg['From'] = ENV['MAIL_FROM']
    msg['To'] = to
    msg['Reply-To'] = data['email']
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = email.utils.make_msgid(domain=site)
    msg.set_content('\n'.join([
        f'New message from {site}', '',
        f"Name:      {data['name']}",
        f"Email:     {data['email']}",
        f"Phone:     {data['phone'] or '-'}",
        f"Topic:     {data['topic'] or '-'}",
        f"Reply by:  {data['reply'] or '-'}",
        f"Language:  {data['language'] or '-'}",
        '', data['message'],
    ]))
    host, port, security = ENV['SMTP_HOST'], int(ENV.get('SMTP_PORT', '465')), ENV.get('SMTP_SECURITY', 'ssl')
    ctx = ssl.create_default_context()
    if security == 'ssl':
        server = smtplib.SMTP_SSL(host, port, context=ctx, timeout=20)
    else:
        server = smtplib.SMTP(host, port, timeout=20)
        if security == 'starttls':
            server.starttls(context=ctx)
    with server:
        if ENV.get('SMTP_USER'):
            server.login(ENV['SMTP_USER'], ENV['SMTP_PASSWORD'])
        server.send_message(msg)


class Handler(BaseHTTPRequestHandler):
    server_version = 'contact'

    def reply(self, status, body):
        raw = json.dumps(body).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        if self.path.split('?')[0] != '/api/contact':
            return self.reply(404, {'ok': False, 'error': 'not_found'})
        length = int(self.headers.get('Content-Length') or 0)
        if not 0 < length <= MAX_BODY:
            return self.reply(413, {'ok': False, 'error': 'too_large'})
        ip = self.headers.get('X-Real-IP') or self.client_address[0]
        if rate_limited(ip):
            return self.reply(429, {'ok': False, 'error': 'rate_limited'})
        try:
            form = parse_form(self.headers.get('Content-Type', ''), self.rfile.read(length))
        except Exception:
            return self.reply(400, {'ok': False, 'error': 'bad_request'})

        if form.get('website'):                      # honeypot: only bots fill it in
            return self.reply(200, {'ok': True})
        if not turnstile_ok(form.get('cf-turnstile-response', ''), ip):
            return self.reply(400, {'ok': False, 'error': 'verification'})

        data = {k: str(form.get(k, '')).strip()[:n] for k, n in LIMITS.items()}
        if not data['name'] or not EMAIL_RE.match(data['email']) or not data['message'] or form.get('consent') != 'on':
            return self.reply(400, {'ok': False, 'error': 'invalid'})
        data = {k: v.replace('\r', ' ').replace('\n', ' ') if k != 'message' else v for k, v in data.items()}

        site = (self.headers.get('Host') or 'drvasileva.co.uk').split(':')[0]
        is_bg = site.endswith('.bg') or site.startswith('bg.')          # bg.<test domain> is the Bulgarian test site
        to = ENV.get('MAIL_TO_BG') if is_bg and ENV.get('MAIL_TO_BG') else ENV['MAIL_TO_EN']
        try:
            send_mail(site, to, data)
        except Exception as e:
            print('send error:', e, file=sys.stderr)
            return self.reply(502, {'ok': False, 'error': 'send'})
        return self.reply(200, {'ok': True})

    def log_message(self, fmt, *args):            # keep personal data out of the logs
        sys.stderr.write('%s %s\n' % (self.command, args[1] if len(args) > 1 else ''))


if __name__ == '__main__':
    addr = (ENV.get('LISTEN_HOST', '127.0.0.1'), int(ENV.get('LISTEN_PORT', '8787')))
    print('contact service listening on %s:%d' % addr, file=sys.stderr)
    ThreadingHTTPServer(addr, Handler).serve_forever()
