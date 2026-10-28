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
| `content/` | **The articles (blog):** `topics.json` and one folder per post in `content/posts/`. See *Articles* below. |
| `src/bg/` | The Bulgarian content and translations. |
| `public/` | Images, icons, fonts (`public/fonts/`) and `site.webmanifest`, copied as they are into both sites. The fonts are served from the site itself, so visitors' details never go to Google. |
| `build/` | The scripts that turn `src/` + `public/` into `dist/` and `preview/`. |
| `preview/` | One-file previews (`site.html`, `site-bg.html`) you can open from your computer. Built automatically. |
| `brand/` | Logo files for use outside the website, and the sources of the share images and app icons. |
| `server/` | The services that run on the VPS: the contact form (sends through mailcow) and the Admin Dashboard (the editor) at `admin.drvasileva.co.uk`. |
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

## Articles (blog)

The Articles pages are made by `build/blog.py` from `content/`. The editor at `admin.drvasileva.co.uk` uses the same code on the server.

> **Once the editor is running, her posts live on the server, not here.** `content/` in the repository is only the starting copy the editor makes on its first start; publishing in the editor never changes the repository. See `deploy/README.md` step 9.

| File | What it holds |
|---|---|
| `content/topics.json` | The topics, each with an English and a Bulgarian name, a cover colour (`sage`, `lilac`, `gold`, `forest`, `plum`, `sand`) and an icon |
| `content/posts/<id>/post.json` | What both languages share: `topic`, `date` (`2026-09-19`, `2026-09` or `2026`), `status` (`draft` or `published`), the `bgben` link (optional) and the `cover` photo (optional) |
| `content/posts/<id>/en.md`, `bg.md` | The text in each language. Every post needs both. |

A language file looks like this:

```
---
title: Expired gratitude
slug: expired-gratitude
summary: One or two sentences for the cards and for Google.
cover_alt: (only with a cover photo) what the photo shows
---
The text. A blank line starts a new paragraph.

## A heading
**bold**, *italic*, ++underline++, {lilac|coloured words} (green, lilac, gold or rose), [a link](https://example.com),
lists with "- ", numbered lists with "1. ", quotes with "> ".
```

In the editor she never sees these marks: the text box shows real formatting, with buttons for each style.

The text can't contain HTML: anything else is shown as plain text, which keeps the pages safe.

**Each post gets:**
- its own page in both languages, such as `/articles/<slug>` and `/statii/<slug>`;
- a card on the Articles page and in the home page's row;
- an entry in `sitemap-articles.xml`.

**Topics** appear in the filters only once they have a post.

**The Articles page** has a search box (title, summary, topic and the whole text; capitals, accents and word endings don't matter), the topic buttons, Year, Order and, once there are both her own articles and BG BEN columns, Type. The choice stays in the page's address, so a search can be shared.

**Reading time** (`reading_minutes` in `build/blog.py`): the words of the text in that language, divided by 238 words a minute for English (Brysbaert 2019, silent reading of non-fiction) or 225 for Bulgarian (her texts have about 5% fewer words in Bulgarian, so the same text takes the same time), rounded to the nearest minute, at least 1.

To add a post by hand, copy a post folder, edit it, and rebuild.

## Running it on the server

See **`deploy/README.md`**.
