"""Sending email through your own mail server (mailcow) over SMTP. Used by the contact form and the editor.

Settings come from environment variables:
  SMTP_HOST, SMTP_PORT (465 or 587), SMTP_SECURITY (ssl | starttls | none, none is for local testing only),
  SMTP_USER, SMTP_PASSWORD, MAIL_FROM
"""
import email.utils
import os
import smtplib
import ssl
from email.message import EmailMessage


def send(to, subject, body, reply_to=None, msgid_domain=None):
    env = os.environ
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = env['MAIL_FROM']
    msg['To'] = to
    if reply_to:
        msg['Reply-To'] = reply_to
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = email.utils.make_msgid(domain=msgid_domain)
    msg.set_content(body)
    host, port, security = env['SMTP_HOST'], int(env.get('SMTP_PORT', '465')), env.get('SMTP_SECURITY', 'ssl')
    ctx = ssl.create_default_context()
    if security == 'ssl':
        server = smtplib.SMTP_SSL(host, port, context=ctx, timeout=20)
    else:
        server = smtplib.SMTP(host, port, timeout=20)
        if security == 'starttls':
            server.starttls(context=ctx)
    with server:
        if env.get('SMTP_USER'):
            server.login(env['SMTP_USER'], env['SMTP_PASSWORD'])
        server.send_message(msg)
