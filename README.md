# Dr Vasileva – website

The bilingual website of **Dr Mirena Vasileva**, Psychologist & CBT Psychotherapist.

- **drvasileva.co.uk** is the English site.
- **drvasileva.bg** is the Bulgarian site.

Both sites have the same content in different languages, and the EN / BG switch moves between them on the same page.

## Folders

| Folder | What's in it |
|---|---|
| `dist/` | **The finished websites:** `dist/en` and `dist/bg`. This is what the server shows to visitors. Built automatically; don't edit by hand. |
| `src/` | **The website's source.** Edit text and design here (see below). |
| `src/bg/` | The Bulgarian content and translations. |
| `public/` | Images, icons, fonts (`public/fonts/`) and `site.webmanifest`, copied as they are into both sites. The fonts are served from the site itself, so visitors' details never go to Google. |
| `build/` | The scripts that turn `src/` + `public/` into `dist/` and `preview/`. |
| `preview/` | One-file previews (`site.html`, `site-bg.html`) you can open from your computer. Built automatically. |
| `brand/` | Logo files for use outside the website, and the sources of the share images and app icons. |
| `server/` | The contact-form service that runs on the VPS and sends messages through mailcow. |
| `deploy/` | nginx and systemd settings, plus **`deploy/README.md`**, the step-by-step server guide. |
| `docs/` | `project-notes.md`: everything decided about the site, the content, and what's still to do. |

## Making a change

1. **Edit the source.** Edit the files in `src/`:

   | File | What it holds |
   |---|---|
   | `home.html` | The home page, header, footer and styles |
   | `pages.js` | All the other pages and their content |
   | `extra.css` | Styles for the other pages |
   | `bg/` | The same in Bulgarian: `bg/pages.js`, `bg/data1.js`, `bg/data2.js`, `bg/blocks.js`, and `bg/pairs.py` for the smaller interface texts |

2. **Rebuild.** You need Python 3, Node and Playwright with Chromium:
   ```
   npm install -g playwright && npx playwright install chromium   # once
   NODE_PATH=$(npm root -g) python3 build/build.py
   ```
   The build stops with an error if an English text was changed and its Bulgarian translation in `src/bg/pairs.py` no longer matches. That keeps English from slipping onto the Bulgarian site.

3. **Check the previews:** open `preview/site.html` or `preview/site-bg.html` in a browser.

4. **Publish.** Commit and push, then run `git pull` on the server. The new pages show straight away.

**Changing the photo, share images or icons:**

- Share images: edit `brand/share-image-en.html` and `brand/share-image-bg.html`.
- App and phone icons: edit `brand/icon-square.svg`.
- Browser-tab icon: edit `public/images/favicon.svg`.

Then recreate the images and rebuild:

```
NODE_PATH=$(npm root -g) node build/make-images.js
NODE_PATH=$(npm root -g) python3 build/build.py
```

`build/txt2svg.py` turned the "DR VASILEVA" lettering into the logo shape in `src/logo-symbol.txt`. You only need it if the logo text changes.

## Running it on the server

See **`deploy/README.md`**.
