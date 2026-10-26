// Cloudflare Pages Function: POST /api/contact
//
// Receives the contact form, checks the Cloudflare Turnstile token, and emails
// the message to Dr Vasileva through Resend (https://resend.com).
//
// Environment variables (Cloudflare Pages → Settings → Environment variables):
//   TURNSTILE_SECRET_KEY  Turnstile secret key (Cloudflare dashboard → Turnstile)
//   RESEND_API_KEY        Resend API key
//   CONTACT_TO            Inbox that receives the messages, e.g. contact@drvasileva.co.uk
//   CONTACT_FROM          Verified sender, e.g. "Website <website@drvasileva.co.uk>"

const LIMITS = { name: 100, email: 150, phone: 30, topic: 80, reply: 20, language: 20, message: 3000 };
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

export async function onRequestPost({ request, env }) {
  let form;
  try {
    form = await request.formData();
  } catch {
    return json({ ok: false, error: 'bad_request' }, 400);
  }

  // Honeypot: real visitors never fill this hidden field. Pretend it worked.
  if (form.get('website')) return json({ ok: true });

  // 1. Turnstile check
  const verify = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    body: new URLSearchParams({
      secret: env.TURNSTILE_SECRET_KEY,
      response: form.get('cf-turnstile-response') || '',
      remoteip: request.headers.get('CF-Connecting-IP') || '',
    }),
  });
  const outcome = await verify.json().catch(() => ({}));
  if (!outcome.success) return json({ ok: false, error: 'verification' }, 400);

  // 2. Validate fields
  const field = key => String(form.get(key) || '').trim().slice(0, LIMITS[key]);
  const data = Object.fromEntries(Object.keys(LIMITS).map(k => [k, field(k)]));
  if (!data.name || !EMAIL_RE.test(data.email) || !data.message || form.get('consent') !== 'on') {
    return json({ ok: false, error: 'invalid' }, 400);
  }

  // 3. Send the email
  const site = new URL(request.url).hostname;
  const text = [
    `New message from ${site}`,
    '',
    `Name:      ${data.name}`,
    `Email:     ${data.email}`,
    `Phone:     ${data.phone || '-'}`,
    `Topic:     ${data.topic || '-'}`,
    `Reply by:  ${data.reply || '-'}`,
    `Language:  ${data.language || '-'}`,
    '',
    data.message,
  ].join('\n');

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: env.CONTACT_FROM,
      to: [env.CONTACT_TO],
      reply_to: data.email,
      subject: `Website message from ${data.name}`,
      text,
    }),
  });
  if (!res.ok) return json({ ok: false, error: 'send' }, 502);

  return json({ ok: true });
}
