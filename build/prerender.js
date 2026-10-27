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
const types = { '.html': 'text/html; charset=utf-8', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.webmanifest': 'application/manifest+json', '.css': 'text/css', '.woff2': 'font/woff2' };

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
    const got = await page.evaluate(() => ({
      pages: document.getElementById('pages').innerHTML,
      title: document.title,
      head: [...document.querySelectorAll('link[rel="canonical"], link[rel="alternate"][hreflang], meta[property="og:url"]')].map(m => m.outerHTML),
    }));
    let html = index
      .replace('<div id="pages"></div>', `<div id="pages">${got.pages}</div>`)
      .replace('<div class="page active" data-route="/">', '<div class="page" data-route="/">')
      .replace(/<title>[^<]*<\/title>/, `<title>${got.title.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</title>`);
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
