# Running the website on your VPS

This guide puts both sites on one server:

- **drvasileva.co.uk** serves the English site from `dist/en`.
- **drvasileva.bg** serves the Bulgarian site from `dist/bg`.

One nginx serves both, and nginx picks the language from the domain name.
The contact form sends its email through your own mailcow server.

```
visitor ──► nginx ──► dist/en  or  dist/bg      (ready-made pages, nothing to build)
               └──► /api/contact ──► contact service (Python, 127.0.0.1:8787) ──► mailcow (SMTP) ──► inbox
```

The pages are already built and committed in `dist/`. The server only needs:

- nginx
- python3 (already on Ubuntu)
- certbot

You don't need Node, a build step or a database.

## What's in the repo

| Path | What it is |
|---|---|
| `dist/en`, `dist/bg` | The finished websites. Every page is a real file, for example `dist/bg/za-men/index.html` is drvasileva.bg/za-men. |
| `dist/*/404.html` | The "page not found" page. nginx sends it with a real 404 status. |
| `server/contact_server.py` | The contact-form service: it checks Turnstile, validates the form and sends the email via SMTP. |
| `deploy/nginx/drvasileva.conf` | The nginx sites: www→bare redirects, http→https, both domains. |
| `deploy/nginx/drvasileva-common.conf` | Settings shared by both domains: 404 page, `/api/contact`, caching, security headers. |
| `deploy/nginx/drvasileva-first-certs.conf` | A temporary config, used only to get the first certificates. |
| `deploy/nginx/mailcow-proxy.conf` | Only needed if mailcow is on the same VPS (step 2). |
| `deploy/systemd/drvasileva-contact.service` | Keeps the contact service running. |
| `deploy/contact.env.example` | Settings for the contact service: mailcow login and Turnstile key. |
| `mockup/` | The design sources and build script. They are **not** served to visitors. |

> `mockup/site.html` and `mockup/site-bg.html` are only previews you can open from your computer.
> They use addresses like `site.html#/about` because a single file can't have real pages.
> The live sites in `dist/` use real addresses like `/about` and `/za-men`.

---

## 1. DNS

Both domains and their `www` versions need to point at the VPS.

| Name | Type | Value |
|---|---|---|
| `drvasileva.co.uk` | A | your VPS IPv4 |
| `www.drvasileva.co.uk` | A | your VPS IPv4 |
| `drvasileva.bg` | A | your VPS IPv4 |
| `www.drvasileva.bg` | A | your VPS IPv4 |

Add AAAA records too if the VPS has IPv6.

If the email addresses `contact@drvasileva.*` should arrive in mailcow:

- add both domains in mailcow (*Email → Configuration → Domains*);
- create the DNS records mailcow lists for them: MX, SPF, DKIM, DMARC and autodiscover.

## 2. If mailcow runs on the same VPS

mailcow comes with its own nginx, and that nginx takes ports 80 and 443. There can only be one owner of those ports. The fix is to move mailcow's web server to local ports and let the main nginx pass the mail hostname through to it. Email itself is not affected, because SMTP and IMAP don't use these ports.

1. Edit `mailcow.conf`, which is usually in `/opt/mailcow-dockerized`:
   ```
   HTTP_PORT=8080
   HTTP_BIND=127.0.0.1
   HTTPS_PORT=8443
   HTTPS_BIND=127.0.0.1
   ```
   Keep `SKIP_LETS_ENCRYPT=n`, so mailcow keeps renewing its own certificate.
2. Restart mailcow:
   ```
   cd /opt/mailcow-dockerized && docker compose down && docker compose up -d
   ```
3. Install nginx on the host:
   ```
   apt install nginx certbot
   ```
4. Set up the mail hostname proxy:
   1. Copy `deploy/nginx/mailcow-proxy.conf` to `/etc/nginx/conf.d/`.
   2. Replace `mail.example.com` with your mailcow hostname.
   3. Check and reload: `nginx -t && systemctl reload nginx`.
   4. Make sure the mailcow web interface still opens.

If mailcow is on a **different** server, skip this step and run `apt install nginx certbot`.

## 3. Get the code

```
cd /var/www
git clone -b claude/nifty-hopper-d24hdq https://github.com/yanivasilev/dr-vasileva.git dr-vasileva
```

Once this branch is merged, use `main` instead of `claude/nifty-hopper-d24hdq`.

**An earlier `git pull` didn't fix the Bulgarian site.** That's because the old setup:

- had no folder for the .bg domain;
- had a language link that pointed at a preview file.

`dist/bg` and the nginx config in this folder fix both. Check which branch you're on with `git branch`.

## 4. Certificates (first time only)

The full nginx config refers to certificate files that don't exist yet, so get the certificates first.

1. Serve the certificate checks with the temporary config:
   ```
   mkdir -p /var/www/letsencrypt
   cp deploy/nginx/drvasileva-first-certs.conf /etc/nginx/conf.d/drvasileva.conf
   nginx -t && systemctl reload nginx
   ```
2. Get the two certificates:
   ```
   certbot certonly --webroot -w /var/www/letsencrypt -d drvasileva.co.uk -d www.drvasileva.co.uk --deploy-hook "systemctl reload nginx"
   certbot certonly --webroot -w /var/www/letsencrypt -d drvasileva.bg -d www.drvasileva.bg --deploy-hook "systemctl reload nginx"
   ```

certbot renews them automatically from now on.

## 5. nginx

```
cp /var/www/dr-vasileva/deploy/nginx/drvasileva-common.conf /etc/nginx/snippets/
cp /var/www/dr-vasileva/deploy/nginx/drvasileva.conf /etc/nginx/conf.d/drvasileva.conf
nginx -t && systemctl reload nginx
```

Check it works:

- https://drvasileva.co.uk/about shows the English page.
- https://drvasileva.bg/za-men shows the Bulgarian page.
- https://drvasileva.bg/nyama shows the Bulgarian "page not found" page.
- The **EN / BG** switch moves between the two domains and keeps you on the same page.

If your server has no IPv6, delete the `listen [::]:…` lines.

## 6. Contact form → mailcow

1. **Create a mailbox for the website in mailcow.** For example, `website@drvasileva.co.uk` with a long random password. The website uses it only to send. Messages go to `contact@drvasileva.co.uk` from the .co.uk site and to `contact@drvasileva.bg` from the .bg site. The visitor's address is set as *Reply-To*, so she can press Reply.
2. **Fill in the settings and protect the file:**
   ```
   mkdir -p /etc/drvasileva
   cp /var/www/dr-vasileva/deploy/contact.env.example /etc/drvasileva/contact.env
   nano /etc/drvasileva/contact.env
   chmod 600 /etc/drvasileva/contact.env
   ```
   Set these values:
   - `SMTP_HOST`: your mailcow hostname, such as `mail.example.com`. This works even when mailcow is on the same server.
   - `SMTP_USER` and `SMTP_PASSWORD`: the mailbox from point 1.
   - Keep port `465` with `ssl`, or use `587` with `starttls`.
3. **Start the service:**
   ```
   cp /var/www/dr-vasileva/deploy/systemd/drvasileva-contact.service /etc/systemd/system/
   systemctl daemon-reload && systemctl enable --now drvasileva-contact
   systemctl status drvasileva-contact
   ```
4. **Test it.** Send a message from https://drvasileva.co.uk/contact. If nothing arrives:
   - check the service log: `journalctl -u drvasileva-contact -n 50`;
   - check mailcow's *Postfix* log.

The log records only errors, never names or messages.

**Turnstile:**

- Until real keys are set, the site uses Cloudflare's *test* keys. The form works, but nothing is actually checked.
- To protect the form for real:
  1. Create a Turnstile widget at dash.cloudflare.com → Turnstile and add both domains.
  2. Put the **secret key** in `contact.env`.
  3. Run `systemctl restart drvasileva-contact`.
  4. Send the **site key** for the website. The site needs to be rebuilt with it, and Claude can do that.

**Protection:**

- nginx allows 5 form posts per minute per visitor.
- The service allows 5 messages per 10 minutes per visitor.
- A hidden "honeypot" field catches simple bots.

## 7. Updating the site later

```
cd /var/www/dr-vasileva && git pull
```

That's all: the pages are plain files, so changes show up straight away. Only these changes need more:

- If `server/contact_server.py` changed, restart the service: `systemctl restart drvasileva-contact`.
- If the files in `deploy/nginx/` changed, copy them again and reload nginx.

## Rebuilding `dist/` (only when the design or text changes)

Edit the files in `mockup/` and `mockup/build/`, then rebuild. You need Python 3, Node and Playwright with Chromium. It's easiest to do this on a computer, not the VPS, then commit `dist/`.

```
npm install -g playwright && npx playwright install chromium
NODE_PATH=$(npm root -g) python3 mockup/build/assemble.py
```

The build:

- creates the previews `mockup/site.html` and `mockup/site-bg.html`;
- creates `dist/en` and `dist/bg`, and saves every page as its own file;
- stops with an error if any Bulgarian translation no longer matches the English text.

## Alternative: Cloudflare Pages

`functions/api/contact.js` is the same contact form for Cloudflare Pages, sending through Resend instead of mailcow. You need it only if the site moves off the VPS; see PROJECT-NOTES.md §11.
