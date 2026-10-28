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
| `deploy/nginx/drvasileva-limits.conf` | The limits for the contact form and for editor sign-in (shared by the live and test sites). |
| `deploy/nginx/drvasileva-test.conf` | A test copy on your own domain (see *Test site* below). |
| `deploy/nginx/drvasileva-first-certs.conf` | A temporary config, used only to get the first certificates. |
| `deploy/nginx/mailcow-proxy.conf` | Only needed if mailcow is on the same VPS (step 2). |
| `deploy/systemd/drvasileva-contact.service` | Keeps the contact service running. |
| `deploy/contact.env.example` | Settings for the contact service: mailcow login and Turnstile key. |
| `server/admin_server.py` (+ `content_store.py`, `editor_pages.py`, `editor.js`) | The website editor at `admin.drvasileva.co.uk`: secure sign-in, then writing and publishing articles (steps 8 and 9). |
| `deploy/nginx/drvasileva-blog-en.conf`, `drvasileva-blog-bg.conf` | Serve the Articles pages that the editor publishes (step 9). |
| `deploy/systemd/drvasileva-backup.service`, `.timer` | A nightly backup of the posts (step 9). |
| `deploy/nginx/drvasileva-admin.conf`, `drvasileva-admin-common.conf` | nginx for the editor. |
| `deploy/systemd/drvasileva-admin.service` | Keeps the editor running, as its own restricted user. |
| `deploy/admin.env.example` | Settings for the editor: its address, where sign-in emails go, and mailcow. |
| everything else | The website's source, build scripts and previews. They are **not** served to visitors. See the main `README.md`. |

> `preview/site.html` and `preview/site-bg.html` are only previews you can open from your computer.
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
cp /var/www/dr-vasileva/deploy/nginx/drvasileva-limits.conf /etc/nginx/conf.d/
cp /var/www/dr-vasileva/deploy/nginx/drvasileva.conf /etc/nginx/conf.d/drvasileva.conf
nginx -t && systemctl reload nginx
```

Check it works:

- https://drvasileva.co.uk/about shows the English page.
- https://drvasileva.bg/za-men shows the Bulgarian page.
- https://drvasileva.bg/nyama shows the Bulgarian "page not found" page.
- The **EN / BG** switch moves between the two domains and keeps you on the same page.

If your server has no IPv6, delete the `listen [::]:…` lines. On nginx 1.25 or newer, `nginx -t` may warn that `listen … http2` is deprecated. That's harmless.

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

- The site already uses the real **site key** of the "Dr Vasileva" widget. Its hostnames are `drvasileva.co.uk`, `drvasileva.bg`, `drvasileva.vasilevdigital.com` and `drvasileva-bg.vasilevdigital.com`.
- Put the matching **secret key** in `contact.env` as `TURNSTILE_SECRET_KEY`, then run `systemctl restart drvasileva-contact`. Keep it only there, never in the repo.
- The form only works on the hostnames listed in the widget. On any other address, Turnstile refuses to load and the form can't be sent.

**Protection:**

- nginx allows 5 form posts per minute per visitor.
- The service allows 5 messages per 10 minutes per visitor.
- A hidden "honeypot" field catches simple bots.

## Test site (before the real domains point here)

You can try everything on your own domain first:

| Address | Site |
|---|---|
| `drvasileva.vasilevdigital.com` | English, `dist/en` |
| `drvasileva-bg.vasilevdigital.com` | Bulgarian, `dist/bg` |

The EN / BG switch moves between these two addresses, and search engines are told not to index them.

> **Don't point nginx at the repo folder or at `preview/`.** Those are the preview files, and their BG link goes to `site-bg.html`. The `root` must be `dist/en` or `dist/bg`.

1. Add a DNS **A** record for `drvasileva-bg.vasilevdigital.com` pointing to the VPS.
2. **Remove** the nginx config you made for `drvasileva.vasilevdigital.com` so far, then reload nginx.
3. Get one certificate covering both names. While you have no working config for them, use the temporary port-80 config:
   ```
   mkdir -p /var/www/letsencrypt
   sed 's/server_name .*/server_name drvasileva.vasilevdigital.com drvasileva-bg.vasilevdigital.com;/' \
       /var/www/dr-vasileva/deploy/nginx/drvasileva-first-certs.conf > /etc/nginx/conf.d/drvasileva-test.conf
   nginx -t && systemctl reload nginx
   certbot certonly --webroot -w /var/www/letsencrypt --cert-name drvasileva.vasilevdigital.com \
       -d drvasileva.vasilevdigital.com -d drvasileva-bg.vasilevdigital.com --deploy-hook "systemctl reload nginx"
   ```
   If certbot asks whether to update an existing certificate, answer yes.
4. Put the real test config in place:
   ```
   cp /var/www/dr-vasileva/deploy/nginx/drvasileva-common.conf /etc/nginx/snippets/
   cp /var/www/dr-vasileva/deploy/nginx/drvasileva-limits.conf /etc/nginx/conf.d/
   cp /var/www/dr-vasileva/deploy/nginx/drvasileva-test.conf /etc/nginx/conf.d/drvasileva-test.conf
   nginx -t && systemctl reload nginx
   ```

When the real domains go live, follow steps 4–5 above. You can keep the test site or delete `/etc/nginx/conf.d/drvasileva-test.conf`.

The contact form works on the test site too. Messages sent from the `-bg` address go to the Bulgarian inbox.

## 7. Updating the site later

```
cd /var/www/dr-vasileva && git pull
```

That's all: the pages are plain files, so changes show up straight away. Only these changes need more:

- If anything in `server/` changed, or the design changed, restart the services: `systemctl restart drvasileva-contact drvasileva-admin`. When the editor starts, it rebuilds the Articles pages with the current design.
- If the files in `deploy/nginx/` changed, copy them again and reload nginx.

## 8. The Admin Dashboard (admin.drvasileva.co.uk)

The Admin Dashboard ("the editor" below) is where she writes and publishes articles. Step 8 sets up the editor and its sign-in. Step 9 connects it to the live sites, so that what she publishes appears there.

**How sign-in is protected:**
- **Two-step sign-in:** a password plus a 6-digit code from an authenticator app on her phone. A stolen password alone is not enough.
- **Backup codes:** 10 one-time codes for when the phone isn't at hand.
- **Cloudflare Turnstile** on the sign-in form: a bot is turned away before its password is even looked at. So bots can neither guess nor cause the pauses below, which keeps her from being locked out by someone else's attack.
- **Lockout:**
  - 5 wrong tries from one address pause that address for 15 minutes (she can still sign in from her own);
  - 20 wrong tries within 15 minutes from all addresses together pause sign-in for everyone for 15 minutes;
  - nginx also limits how often sign-in can be tried.
- **Emails:** every sign-in and every lock is emailed. The editor also shows the previous sign-in, so a stranger's visit stands out.
- **No sign-up page and no "forgot password" email.** The account is created and changed only with a command on the server.
- **Sessions:**
  - she is signed out after 1 hour without activity, and always after 12 hours;
  - the session cookie can't be read by scripts, is only sent over HTTPS, and is never sent from other sites;
  - form posts from any other site are refused.
- **The editor page itself:** it runs only its own script (the sign-in page also Cloudflare's Turnstile), can't be put inside another site's frame, isn't stored by the browser, and isn't shown by search engines.
- **The editor service:** it runs as its own user, which can write only to `/var/lib/drvasileva-admin`.

### Set it up

1. **DNS:** add an A record for `admin.drvasileva.co.uk`. For testing, use `drvasileva-admin.vasilevdigital.com` instead.
2. **Certificate:**
   - Live site: add the name `admin.drvasileva.co.uk`. The temporary config in `drvasileva-first-certs.conf` already includes it:
     ```
     certbot certonly --webroot -w /var/www/letsencrypt -d admin.drvasileva.co.uk --deploy-hook "systemctl reload nginx"
     ```
   - Test site: add the name to the existing certificate:
     ```
     certbot certonly --webroot -w /var/www/letsencrypt --cert-name drvasileva.vasilevdigital.com --expand \
         -d drvasileva.vasilevdigital.com -d drvasileva-bg.vasilevdigital.com -d drvasileva-admin.vasilevdigital.com
     ```
3. **nginx:**
   ```
   cp /var/www/dr-vasileva/deploy/nginx/drvasileva-limits.conf /etc/nginx/conf.d/
   cp /var/www/dr-vasileva/deploy/nginx/drvasileva-admin-common.conf /etc/nginx/snippets/
   cp /var/www/dr-vasileva/deploy/nginx/drvasileva-admin.conf /etc/nginx/conf.d/     # live address
   cp /var/www/dr-vasileva/deploy/nginx/drvasileva-test.conf /etc/nginx/conf.d/      # test addresses (now includes the editor)
   nginx -t && systemctl reload nginx
   ```
4. **The editor's user and settings:**
   ```
   useradd --system --no-create-home --shell /usr/sbin/nologin drvasileva-admin
   install -d -o drvasileva-admin -g drvasileva-admin -m 700 /var/lib/drvasileva-admin
   cp /var/www/dr-vasileva/deploy/admin.env.example /etc/drvasileva/admin.env
   nano /etc/drvasileva/admin.env
   chmod 600 /etc/drvasileva/admin.env
   ```
   In the settings:
   - Set `ADMIN_ORIGIN` to the address you use: `https://admin.drvasileva.co.uk`, or `https://drvasileva-admin.vasilevdigital.com` while testing.
   - Set `ADMIN_ALERT_TO` to the inbox for sign-in emails.
   - Use the same mailcow details as the contact form.
   - **Turnstile:** set `TURNSTILE_SITE_KEY` and `TURNSTILE_SECRET_KEY`. You can use the contact form's widget: in Cloudflare → Turnstile → the widget → Hostnames, make sure `drvasileva.co.uk` (which covers `admin.`) and, while testing, `drvasileva-admin.vasilevdigital.com` are listed. Without the keys the check is simply off.
5. **Create her account,** with her phone next to you:
   ```
   apt install qrencode        # optional: shows a QR code to scan instead of typing the key
   sudo -u drvasileva-admin python3 /var/www/dr-vasileva/server/admin_server.py setup
   ```
   1. Type the password twice: at least 12 characters, and a few words together work well.
   2. Add the editor to an authenticator app on her phone, such as Google Authenticator, Microsoft Authenticator, 2FAS or Aegis. Scan the QR code, or type the setup key.
   3. Type the code the app shows.
   4. Write down or print the 10 backup codes, and keep them somewhere safe and away from the computer.
6. **Start it:**
   ```
   cp /var/www/dr-vasileva/deploy/systemd/drvasileva-admin.service /etc/systemd/system/
   systemctl daemon-reload && systemctl enable --now drvasileva-admin
   ```
   Then open the editor's address and sign in. The sign-in email should arrive within a minute.

**Later changes** (each signs everyone out after `systemctl restart drvasileva-admin`):

| What | Command (`sudo -u drvasileva-admin python3 /var/www/dr-vasileva/server/admin_server.py …`) |
|---|---|
| New password | `password` |
| Lost or new phone | `reset-2fa` |
| New backup codes (the old ones stop working) | `backup-codes` |
| Check the account | `status` |

> **If you use Cloudflare's proxy (orange cloud) for the editor:** nginx then sees Cloudflare's addresses, not the visitor's.
> - Turnstile and the 20-tries pause still protect the account.
> - The per-address pause becomes shared between visitors, so it can block her too.
>
> Keep the editor's DNS record "DNS only" (grey cloud), or set up nginx's real-IP module for Cloudflare.

## 9. Publishing from the editor

**What she can do in the editor:**
- **Write a post:** in Bulgarian | English tabs, with a toolbar for headings, bold, italic, lists, quotes and links.
- **Set the details:** the topic, the date, the BG BEN link for a column, and a cover photo.
- **Preview** it exactly as it will look on the site.
- **Publish and unpublish:** **Publish** puts it on both sites at once, and **Unpublish** takes it off. A post can only be published when both languages are filled in. Changes to a published post go live when she saves.
- **Undo mistakes:**
  - every save keeps a version she can restore (the last 30);
  - deleted posts stay in the bin for 30 days;
  - typing is also kept in her browser every 30 seconds, in case the browser closes before she saves.
- **Manage topics:** add and rename topics in both languages, and choose their colour and icon.

**Where things are kept:**
- **Her posts:** they live on the server in `/var/lib/drvasileva-admin/content`, not in the git folder, so `git pull` never touches them. On its first start the editor copies the 18 columns there from the repository.
- **The published pages:** the editor writes them to `/var/www/drvasileva-blog`, and nginx serves the Articles addresses from there.

**Photos:** each photo is redrawn on the server. This removes the location the phone saves in it and anything hidden in the file, turns it the right way up and resizes it. Anything that isn't a JPG, PNG or WebP photo is refused.

**Safety:** the preview opens as a sandbox, so it can't run scripts or touch her signed-in session.

### Set it up (after step 8)

1. **The photo library and the blog folder:**
   ```
   apt install python3-pil
   install -d -o drvasileva-admin -g drvasileva-admin -m 755 /var/www/drvasileva-blog
   ```
2. **The updated editor service**, which may now write to that folder and accepts photos up to 10 MB:
   ```
   cp /var/www/dr-vasileva/deploy/systemd/drvasileva-admin.service /etc/systemd/system/
   cp /var/www/dr-vasileva/deploy/nginx/drvasileva-admin-common.conf /etc/nginx/snippets/
   systemctl daemon-reload && systemctl restart drvasileva-admin
   ls /var/www/drvasileva-blog/en/articles      # the editor has written the Articles pages
   ```
3. **Serve the Articles pages from the editor:**
   1. Copy the snippets:
      ```
      cp /var/www/dr-vasileva/deploy/nginx/drvasileva-blog-en.conf /var/www/dr-vasileva/deploy/nginx/drvasileva-blog-bg.conf /etc/nginx/snippets/
      ```
   2. In `/etc/nginx/conf.d/drvasileva.conf`, remove the `#` in front of the two `include …drvasileva-blog-…` lines. On the test site, do the same in `drvasileva-test.conf`.
   3. Reload nginx:
      ```
      nginx -t && systemctl reload nginx
      ```

   Until this step, the Articles pages come from the git copy, which has the 18 columns but nothing published in the editor.
4. **Nightly backup** of the posts, kept for 30 days in `/var/backups/drvasileva`:
   ```
   cp /var/www/dr-vasileva/deploy/systemd/drvasileva-backup.* /etc/systemd/system/
   systemctl daemon-reload && systemctl enable --now drvasileva-backup.timer
   ```
   Now and then, copy `/var/backups/drvasileva` off the server too, for example to your computer.

**Test it:**
1. Write a short post in both languages.
2. Press **Publish**.
3. Open https://drvasileva.co.uk/articles and https://drvasileva.bg/statii.
4. Unpublish it again.

## Rebuilding `dist/` (only when the design or text changes)

The server never builds anything. Changes to the text or design are made in `src/`, rebuilt with `build/build.py` and committed together with `dist/`. The main `README.md` explains how.
