// Recreates the share images and app icons in public/images/ from the sources in brand/.
// Only needed when the photo, headline or icon design changes.
// Usage: NODE_PATH=$(npm root -g) node build/make-images.js   (then run build/build.py)
// favicon.ico is made from the PNGs with Python's Pillow, if it is installed.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const repo = path.dirname(__dirname);
const brand = path.join(repo, 'brand');
const out = path.join(repo, 'public', 'images');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'drv-images-'));

(async () => {
  const browser = await chromium.launch();

  // Link previews (Facebook, WhatsApp, Viber …): 1200 × 630
  for (const lang of ['en', 'bg']) {
    const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
    await page.goto('file://' + path.join(brand, `share-image-${lang}.html`), { waitUntil: 'networkidle' });
    await page.waitForTimeout(400);
    await page.screenshot({ path: path.join(out, `og-${lang}.png`) });
    await page.close();
  }

  // Icons: square artwork for phones (they round the corners themselves), rounded favicon for browser tabs
  const icons = [
    ['apple-touch-icon.png', 180, 'icon-square.svg'], ['icon-192.png', 192, 'icon-square.svg'], ['icon-512.png', 512, 'icon-square.svg'],
    ['favicon-16.png', 16, null], ['favicon-32.png', 32, null], ['favicon-48.png', 48, null],
  ];
  for (const [name, size, src] of icons) {
    const file = src ? path.join(brand, src) : path.join(out, 'favicon.svg');
    const page = await browser.newPage({ viewport: { width: size, height: size } });
    await page.setContent(`<style>html,body{margin:0;background:transparent}</style>${fs.readFileSync(file, 'utf8').replace('<svg ', `<svg width="${size}" height="${size}" `)}`);
    await page.screenshot({ path: path.join(name.startsWith('favicon-') ? tmp : out, name), omitBackground: true });
    await page.close();
  }
  await browser.close();

  try {
    execFileSync('python3', ['-c', `
from PIL import Image
import sys
t, out = sys.argv[1], sys.argv[2]
ims = [Image.open(f'{t}/favicon-{s}.png').convert('RGBA') for s in (48, 32, 16)]
ims[0].save(out, sizes=[(48, 48), (32, 32), (16, 16)], append_images=ims[1:])
`, tmp, path.join(out, 'favicon.ico')], { stdio: 'inherit' });
  } catch { console.log('favicon.ico not updated (needs: pip install pillow)'); }
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log('Updated public/images: og-en.png, og-bg.png, apple-touch-icon.png, icon-192.png, icon-512.png, favicon.ico');
})();
