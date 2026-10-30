// Saves every page of a built site as its own HTML file, so each address
// (/about, /za-men, …) is a real page with its own content, title and links.
// Usage: node prerender.js <dist folder> <routes.json>
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const [dir, routesFile] = process.argv.slice(2);
const routes = JSON.parse(fs.readFileSync(routesFile, 'utf8'));   // [[key, url], ...]
const index = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.webmanifest': 'application/manifest+json', '.css': 'text/css', '.woff2': 'font/woff2' };

// Small static server: real files, otherwise the app's index.html
const server = http.createServer((req, res) => {
  const file = path.join(dir, decodeURIComponent(req.url.split('?')[0]));
  if (file.startsWith(dir) && fs.existsSync(file) && fs.statSync(file).isFile()) {
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream' });
    return fs.createReadStream(file).pipe(res);
  }
  res.writeHead(200, { 'Content-Type': types['.html'] }); res.end(index);
});

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });   // counters show their final value
  await page.route(/challenges\.cloudflare\.com/, r => r.abort());
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  for (const [key, url] of routes) {
    if (key === '/') continue;
    await page.goto(origin + encodeURI(url), { waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => document.querySelector('#pages .page.active'));
    const got = await page.evaluate(() => {
      const el = document.querySelector('#pages .page.active');
      const text = n => n.textContent.replace(/\s+/g, ' ').trim();
      // This page's own description for Google and link previews: its introduction, then its first paragraphs
      let desc = '';
      for (const n of el.querySelectorAll('.page-hero .lead, .page-body p')) {
        if (desc.length >= 120) break;
        if (n.closest('details, form, .faq')) continue;               // not an answer from a list of questions
        if (n.matches('.updated')) continue;                            // nor a page's “last updated” line
        const t = text(n).replace(/\s*·\s*/g, ', ');
        if (t.length > 30) desc += (desc ? (/[.!?…]$/.test(desc) ? ' ' : '. ') : '') + t;
      }
      // a short introduction on a page of questions: add the first questions
      for (const q of desc.length < 80 ? el.querySelectorAll('.faq summary') : []) {
        if (desc.length >= 130) break;
        desc += ' ' + text(q);
      }
      if (desc.length > 158) desc = desc.slice(0, 157).replace(/[\s,;:–-]+\S*$/, '') + '…';
      const site = new URL(document.querySelector('link[rel="canonical"]').href).origin;    // the real domain
      const real = u => site + new URL(u).pathname;
      return {
        pages: document.getElementById('pages').innerHTML,
        title: document.title,
        head: [...document.querySelectorAll('link[rel="canonical"], link[rel="alternate"][hreflang], meta[property="og:url"]')].map(m => m.outerHTML),
        desc,
        url: document.querySelector('link[rel="canonical"]').href,
        home: site + '/',
        homeName: document.documentElement.lang === 'bg' ? 'Начало' : 'Home',
        crumbs: [...el.querySelectorAll('.crumbs a, .crumbs span:not(:has(a))')].slice(1).map(n => ({ name: text(n), url: n.href ? real(n.href) : null })),
        faq: [...el.querySelectorAll('.faq details')].map(d => ({ q: text(d.querySelector('summary')), a: text(d.querySelector('.answer')) })),
      };
    });
    // Structured data: where the page sits in the site, and on the FAQ page its questions and answers
    const ld = [];
    if (got.crumbs.length) ld.push({ '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement:
      [{ name: got.homeName, url: got.home }, ...got.crumbs].map((c, i) => ({ '@type': 'ListItem', position: i + 1, name: c.name, item: c.url || got.url })) });
    if (got.faq.length) ld.push({ '@context': 'https://schema.org', '@type': 'FAQPage', mainEntity: got.faq.map(f => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: f.a } })) });
    const attr = v => v.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
    // Each page carries only its own content: the home page's is left out (an empty marker stays, and the
    // menu's Home link then opens the home page itself)
    const home = /<div class="page active" data-route="\/">[\s\S]*?<\/div>\n<div id="pages"><\/div>/;
    if (!home.test(index)) throw new Error('prerender: home page block not found');
    let html = index
      .replace(home, () => `<div class="page" data-route="/" data-elsewhere></div>\n<div id="pages">${got.pages}</div>`)
      .replace(/<script>window\.POSTS = .*?<\/script>\n/s, '')          // the home row's cards: home page only
      .replace(/<title>[^<]*<\/title>/, `<title>${got.title.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</title>`);
    if (got.desc) html = html
      .replace(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${attr(got.desc)}">`)
      .replace(/<meta property="og:description" content="[^"]*">/, `<meta property="og:description" content="${attr(got.desc)}">`)
      .replace(/<meta property="og:title" content="[^"]*">/, `<meta property="og:title" content="${attr(got.title)}">`);
    if (ld.length) html = html.replace('</head>', ld.map(x => `<script type="application/ld+json">${JSON.stringify(x).replace(/</g, '\\u003c')}</script>\n`).join('') + '</head>');
    const heads = html.match(/<link rel="canonical"[^>]*>|<link rel="alternate" hreflang="[^"]*"[^>]*>|<meta property="og:url"[^>]*>/g);
    heads.forEach((tag, i) => { html = html.replace(tag, got.head[i]); });
    const out = path.join(dir, url, 'index.html');
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, html);
  }
  console.log(`${dir}: ${routes.length - 1} pages saved`, errors.length ? errors : '');
  await browser.close();
  server.close();
})();
