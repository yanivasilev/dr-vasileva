// The editor's only script (served as /editor.js; the editor allows no other scripts).
// Everything here is a convenience: without it the forms still work, with plain text boxes and
// both languages shown one under the other.
(() => {
  const form = document.querySelector('form[data-editor]');
  if (!form) return;

  /* ---------------------------------------------------------------------
     The text format. Posts are stored as simple text (see build/blog.py):
       ## Heading   ### Subheading   **bold**   *italic*   ++underline++
       {lilac|coloured}   [link](https://…)   - list   1. list   > quote
     The editor shows it as real formatting and turns it back into text on every change.
     --------------------------------------------------------------------- */
  const COLOURS = ['green', 'lilac', 'gold', 'rose'];
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const okLink = h => /^(https?:\/\/|mailto:)\S+$/.test(h || '');

  // text -> HTML (the same rules as render_text() in build/blog.py; everything is escaped first)
  const inline = text => esc(text)
    .replace(/\[([^\]\n]+)\]\(((?:https?:\/\/|mailto:)[^\s)]+)\)/g, '<a href="$2">$1</a>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])/g, '<em>$1</em>')
    .replace(/\+\+(?!\s)(.+?)(?<!\s)\+\+/g, '<u>$1</u>')
    .replace(new RegExp(`\\{(${COLOURS.join('|')})\\|([^{}\\n]+)\\}`, 'g'), '<span class="tc-$1">$2</span>');
  const toHTML = text => {
    const out = [];
    for (const block of text.replace(/\r\n/g, '\n').trim().split(/\n\s*\n/)) {
      let lines = block.split('\n').map(l => l.trimEnd()).filter(l => l.trim());
      if (!lines.length) continue;
      const h = lines[0].match(/^(#{2,3}) (.*)$/);
      if (h) { out.push(`<h${h[1].length}>${inline(h[2])}</h${h[1].length}>`); lines = lines.slice(1); if (!lines.length) continue; }
      if (lines.every(l => /^[-*] /.test(l))) out.push('<ul>' + lines.map(l => `<li>${inline(l.slice(2))}</li>`).join('') + '</ul>');
      else if (lines.every(l => /^\d+[.)] /.test(l))) {
        const first = parseInt(lines[0], 10);
        out.push(`<ol${first > 1 && first < 10000 ? ` start="${first}"` : ''}>` + lines.map(l => `<li>${inline(l.replace(/^\d+[.)] /, ''))}</li>`).join('') + '</ol>');
      }
      else if (lines.every(l => l.startsWith('>'))) out.push('<blockquote><p>' + lines.map(l => inline(l.slice(1).trim())).join('<br>') + '</p></blockquote>');
      else out.push('<p>' + lines.map(inline).join('<br>') + '</p>');
    }
    return out.join('') || '<p><br></p>';
  };

  // HTML -> text
  const colourOf = el => COLOURS.find(c => el.classList?.contains(`tc-${c}`));
  const mark = (m, s) => s.split('\n').map(line => {          // marks can't span lines, and keep spaces outside
    const [, a, mid, b] = line.match(/^(\s*)([\s\S]*?)(\s*)$/);
    return mid ? `${a}${m[0]}${mid}${m[1]}${b}` : line;
  }).join('\n');
  const BLOCKS = new Set(['P', 'DIV', 'H1', 'H2', 'H3', 'H4', 'LI', 'BLOCKQUOTE', 'UL', 'OL']);
  const inl = node => [...node.childNodes].map(one).join('');
  const one = n => {
    if (n.nodeType === 3) return n.nodeValue.replace(/ /g, ' ').replace(/\n/g, ' ');
    if (n.nodeType !== 1) return '';
    const t = n.tagName, inner = inl(n);
    if (t === 'BR') return '\n';
    if (t === 'B' || t === 'STRONG') return mark(['**', '**'], inner);
    if (t === 'I' || t === 'EM') return mark(['*', '*'], inner);
    if (t === 'U') return mark(['++', '++'], inner);
    if (t === 'A') return okLink(n.getAttribute('href')) && inner.trim() ? `[${inner.replace(/[[\]\n]/g, ' ').trim()}](${n.getAttribute('href')})` : inner;
    if (t === 'SPAN' && colourOf(n)) return mark([`{${colourOf(n)}|`, '}'], inner.replace(/[{}]/g, ''));
    if (BLOCKS.has(t)) return '\n' + inner + '\n';
    return inner;
  };
  const tidy = s => s.replace(/[ \t]+\n/g, '\n').replace(/\n{2,}/g, '\n').trim();
  const flat = s => tidy(s).replace(/\n/g, ' ');
  const tag = n => n.nodeType === 1 ? n.tagName : '';
  const hasBlock = n => [...n.children].some(c => BLOCKS.has(c.tagName));
  // Walks the blocks, whatever nesting the browser made (a list inside a paragraph, a quote inside a list …)
  const walk = (node, out) => {
    let loose = '';
    const flush = () => { if (loose.trim()) out.push(tidy(loose)); loose = ''; };
    for (const n of node.childNodes) {
      const t = tag(n);
      if ((t === 'P' || t === 'DIV' || t === 'LI') && hasBlock(n)) { flush(); walk(n, out); }
      else if (t === 'P' || t === 'DIV') { flush(); out.push(tidy(inl(n))); }
      else if (t === 'H1' || t === 'H2') { flush(); out.push('## ' + flat(inl(n))); }
      else if (t === 'H3' || t === 'H4') { flush(); out.push('### ' + flat(inl(n))); }
      else if (t === 'UL' || t === 'OL') {
        flush();
        const items = [...n.querySelectorAll('li')].filter(li => !li.querySelector('li')).map(li => flat(inl(li))).filter(Boolean);
        const start = t === 'OL' && n.start > 0 ? n.start : 1;
        if (items.length) out.push(items.map((x, i) => (t === 'UL' ? '- ' : `${start + i}. `) + x).join('\n'));
      } else if (t === 'BLOCKQUOTE') {
        flush();
        const inner = [];
        walk(n, inner);
        const lines = inner.join('\n').split('\n').map(l => l.replace(/^(#{2,3} |> |- |\d+\. )/, '').trim()).filter(Boolean);
        if (lines.length) out.push(lines.map(l => '> ' + l).join('\n'));
      } else if (t === 'BR') loose += '\n';
      else loose += one(n);
    }
    flush();
  };
  const fromHTML = root => {
    const blocks = [];
    walk(root, blocks);
    return blocks.filter(b => b.replace(/^(#{2,3} |> |- |\d+\. )/gm, '').trim()).join('\n\n');
  };

  /* ---------------------------------------------------------------------
     The formatted text boxes
     --------------------------------------------------------------------- */
  document.execCommand('defaultParagraphSeparator', false, 'p');
  document.execCommand('styleWithCSS', false, false);
  const editors = [];
  document.querySelectorAll('.toolbar[data-for]').forEach(bar => {
    if (!bar.querySelector('[data-cmd]')) return;          // a page from an older version: keep the plain text box
    const ta = document.getElementById(bar.dataset.for);
    const rich = document.createElement('div');
    rich.className = 'rich';
    rich.contentEditable = 'true';
    rich.setAttribute('role', 'textbox');
    rich.setAttribute('aria-multiline', 'true');
    rich.setAttribute('aria-label', document.querySelector(`label[for="${ta.id}"]`)?.textContent || 'Text');
    rich.dataset.placeholder = 'Start writing here…';
    rich.lang = ta.closest('[lang]')?.lang || '';
    // Numbered lists carry on after a paragraph (1 … 2 … 3); a heading, or "Restart numbering", starts again at 1
    const continuing = () => {
      const starts = new Map();
      let next = 1;
      for (const el of rich.children) {
        if (/^H[1-4]$/.test(el.tagName)) next = 1;
        else if (el.tagName === 'OL') {
          starts.set(el, next);
          next = (el.dataset.restart ? 1 : next) + el.querySelectorAll('li').length;
        }
      }
      return starts;
    };
    const renumber = () => {
      for (const [el, auto] of continuing()) {
        const start = el.dataset.restart ? 1 : auto;
        if (start > 1) el.setAttribute('start', start); else el.removeAttribute('start');
      }
    };
    const load = text => {
      rich.innerHTML = toHTML(text);
      rich.classList.toggle('empty', !text.trim());
      // a list saved as starting at 1 where it would otherwise carry on was restarted on purpose
      for (const [el, auto] of continuing()) if (auto > 1 && !el.hasAttribute('start')) el.dataset.restart = '1';
      renumber();
    };
    load(ta.value);
    ta.hidden = true;
    ta.after(rich);
    bar.hidden = false;
    const hint = ta.parentElement.querySelector('[data-hint]');
    if (hint) hint.textContent = 'Select words, then click a button above. Press Enter for a new paragraph.';
    const sync = () => {
      renumber();
      const text = fromHTML(rich);
      rich.classList.toggle('empty', !text);
      if (ta.value !== text) { ta.value = text; ta.dispatchEvent(new Event('input', { bubbles: true })); }
    };
    rich.addEventListener('input', sync);
    // Pasted or dropped text comes in as plain text, so no hidden formatting or code gets in
    rich.addEventListener('paste', e => {
      e.preventDefault();
      document.execCommand('insertText', false, (e.clipboardData || window.clipboardData).getData('text/plain'));
    });
    rich.addEventListener('drop', e => e.preventDefault());
    // Enter on an empty line inside a quote ends the quote (lists already work like this)
    rich.addEventListener('keydown', e => {
      if (e.key !== 'Enter' || e.shiftKey) return;
      const sel = getSelection();
      let line = sel.anchorNode;
      while (line && line.parentNode && line.parentNode.tagName !== 'BLOCKQUOTE' && line !== rich) line = line.parentNode;
      const quote = line?.parentNode;
      if (!quote || quote.tagName !== 'BLOCKQUOTE' || quote.parentNode !== rich || line.textContent.trim()) return;
      e.preventDefault();
      const p = document.createElement('p');
      p.append(document.createElement('br'));
      line.remove();
      quote.after(p);
      const r = document.createRange();
      r.setStart(p, 0);
      sel.removeAllRanges();
      sel.addRange(r);
      sync();
    });
    editors.push({ bar, ta, rich, load, sync });

    const inRich = () => { const s = getSelection(); return s.rangeCount && rich.contains(s.getRangeAt(0).commonAncestorContainer); };
    const currentList = () => {
      let n = getSelection().anchorNode;
      while (n && n.parentNode !== rich) n = n.parentNode;
      return n && n.tagName === 'OL' ? n : null;
    };
    const block = () => {                        // the kind of top-level block the cursor is in
      let n = getSelection().anchorNode;
      while (n && n.parentNode !== rich) n = n.parentNode;
      return n && n.nodeType === 1 ? n.tagName : 'P';
    };
    const unwrapColours = range => {
      rich.querySelectorAll('span').forEach(sp => {
        if (colourOf(sp) && range.intersectsNode(sp)) sp.replaceWith(...sp.childNodes);
      });
    };
    const colour = c => {
      const sel = getSelection();
      if (!inRich() || sel.isCollapsed) return alert('First select the words you want to colour.');
      const range = sel.getRangeAt(0);
      unwrapColours(range);
      if (c) {
        const span = document.createElement('span');
        span.className = `tc-${c}`;
        span.append(range.extractContents());
        span.querySelectorAll('span').forEach(sp => colourOf(sp) && sp.replaceWith(...sp.childNodes));
        range.insertNode(span);
        sel.selectAllChildren(span);
      }
      sync();
    };
    // Headings, normal text, quotes and lists change whole paragraphs. They are done here rather than by the
    // browser, which nests lists inside paragraphs and quotes in ways that are hard to undo.
    const topBlocks = () => {
      const sel = getSelection();
      if (!inRich()) return [];
      const r = sel.getRangeAt(0);
      let blocks = [...rich.childNodes].filter(c => r.intersectsNode(c));
      if (!blocks.length) { rich.append(document.createElement('p')); blocks = [rich.lastChild]; }
      return blocks;
    };
    const linesOf = b => {                       // the lines of a block, as lists of nodes (moved, not copied)
      const lines = [[]];
      const go = node => {
        for (const c of [...node.childNodes]) {
          const t = tag(c);
          if (t === 'BR') lines.push([]);
          else if (BLOCKS.has(t)) { lines.push([]); go(c); lines.push([]); }
          else lines[lines.length - 1].push(c);
        }
      };
      if (b.nodeType === 3) lines[0].push(b); else go(b);
      return lines.filter(l => l.some(n => (n.textContent || '').trim() || tag(n) === 'IMG'));
    };
    const caretAtEnd = el => {
      const r = document.createRange();
      r.selectNodeContents(el);
      r.collapse(false);
      const sel = getSelection();
      sel.removeAllRanges();
      sel.addRange(r);
    };
    const make = (name, nodes) => {
      const el = document.createElement(name);
      nodes.forEach(n => el.append(n));
      if (!el.childNodes.length) el.append(document.createElement('br'));
      return el;
    };
    const setBlocks = kind => {                  // kind: p | h2 | h3 | blockquote | ul | ol
      const blocks = topBlocks();
      if (!blocks.length) return;
      const same = blocks.every(b => tag(b) === kind.toUpperCase());
      const target = same && kind !== 'p' ? 'p' : kind;           // pressing it again turns it back to normal text
      let lines = blocks.flatMap(linesOf);
      if (!lines.length) lines = [[]];
      let made;
      if (target === 'ul' || target === 'ol') made = [make(target, lines.map(l => make('li', l)))];
      else if (target === 'blockquote') {
        const p = make('p', []);
        p.replaceChildren();
        lines.forEach((l, i) => { if (i) p.append(document.createElement('br')); l.forEach(n => p.append(n)); });
        if (!p.childNodes.length) p.append(document.createElement('br'));
        made = [make('blockquote', [p])];
      } else if (target === 'h2' || target === 'h3') made = lines.map(l => make(target, l));
      else made = lines.map(l => make('p', l));
      blocks[0].replaceWith(...made);
      blocks.slice(1).forEach(b => b.remove());
      caretAtEnd(made[made.length - 1]);
    };
    const commands = {
      bold: () => document.execCommand('bold'),
      italic: () => document.execCommand('italic'),
      underline: () => document.execCommand('underline'),
      h2: () => setBlocks('h2'),
      h3: () => setBlocks('h3'),
      p: () => setBlocks('p'),
      quote: () => setBlocks('blockquote'),
      ul: () => setBlocks('ul'),
      ol: () => setBlocks('ol'),
      renum: () => {
        const ol = currentList();
        if (!ol) return;
        if (ol.dataset.restart) delete ol.dataset.restart; else ol.dataset.restart = '1';
      },
      link: () => {
        const sel = getSelection();
        if (sel.isCollapsed) return alert('First select the words that should become a link.');
        const url = prompt('Web address for the link (starting with https://):', 'https://');
        if (url === null) return;
        if (!okLink(url.trim()) || url.trim() === 'https://') return alert('Please enter a full address, starting with https://');
        document.execCommand('createLink', false, url.trim());
      },
      clear: () => {
        const sel = getSelection();
        if (!sel.rangeCount) return;
        document.execCommand('removeFormat');
        document.execCommand('unlink');
        unwrapColours(sel.getRangeAt(0));
      },
    };
    const menu = bar.querySelector('.colour-list'), menuBtn = bar.querySelector('[data-cmd=colours]');
    const closeMenu = () => { if (menu) { menu.hidden = true; menuBtn.setAttribute('aria-expanded', 'false'); } };
    bar.addEventListener('mousedown', e => { if (e.target.closest('button')) e.preventDefault(); });   // keep the selection in the text
    bar.addEventListener('click', e => {
      const btn = e.target.closest('button');
      if (!btn) return;
      if (btn.dataset.cmd === 'colours') { menu.hidden = !menu.hidden; menuBtn.setAttribute('aria-expanded', String(!menu.hidden)); return; }
      if ('colour' in btn.dataset) { closeMenu(); return colour(btn.dataset.colour); }
      if (!inRich()) rich.focus();
      commands[btn.dataset.cmd]?.();
      closeMenu();
      sync();
      state();
    });
    document.addEventListener('click', e => { if (!e.target.closest('.colour-menu')) closeMenu(); });
    // Buttons show what the selected text already has
    const renumBtn = bar.querySelector('[data-cmd=renum]');
    const state = () => {
      if (!inRich()) return;
      const b = block();
      const ol = currentList();
      const continues = ol && (ol.dataset.restart || continuing().get(ol) > 1);
      if (renumBtn) {
        renumBtn.hidden = !continues;
        renumBtn.lastChild.textContent = ol && ol.dataset.restart ? 'Continue numbering' : 'Restart numbering';
      }
      for (const [cmd, on] of Object.entries({ bold: !/^H[1-4]$/.test(b) && document.queryCommandState('bold'),   // headings are bold anyway
        italic: document.queryCommandState('italic'),
        underline: document.queryCommandState('underline'), h2: b === 'H2', h3: b === 'H3', quote: b === 'BLOCKQUOTE',
        ul: b === 'UL', ol: b === 'OL' })) {
        bar.querySelector(`[data-cmd=${cmd}]`)?.setAttribute('aria-pressed', String(!!on));
      }
    };
    document.addEventListener('selectionchange', state);
  });

  /* ---------------------------------------------------------------------
     BG | EN tabs
     --------------------------------------------------------------------- */
  const tabs = [...document.querySelectorAll('.tab[data-tab]')];
  const panels = [...document.querySelectorAll('[data-panel]')];
  const show = lang => {
    tabs.forEach(t => t.setAttribute('aria-selected', t.dataset.tab === lang));
    panels.forEach(p => p.hidden = p.dataset.panel !== lang);
  };
  tabs.forEach(t => t.addEventListener('click', () => show(t.dataset.tab)));
  if (tabs.length) { document.querySelector('.tabs').hidden = false; show('bg'); }
  const ticks = () => tabs.forEach(t => {
    const l = t.dataset.tab, done = form.elements[`${l}_title`].value.trim() && form.elements[`${l}_body`].value.trim();
    t.querySelector('[data-done]').textContent = done ? '✓' : '';
  });

  // Cover photo: show the chosen photo straight away
  const photo = form.elements.photo, thumb = document.querySelector('[data-thumb]');
  photo?.addEventListener('change', () => {
    const f = photo.files[0];
    if (!f) return;
    const img = document.createElement('img');
    img.src = URL.createObjectURL(f);
    img.alt = '';
    thumb.replaceChildren(img);
  });

  /* ---------------------------------------------------------------------
     Autosave in this browser every 30 seconds, so nothing is lost if the browser closes before saving
     --------------------------------------------------------------------- */
  const key = `drv-editor:${form.dataset.key}`;
  const fields = [...form.querySelectorAll('input[type=text], input[type=url], textarea, select')];
  const values = () => Object.fromEntries(fields.map(f => [f.name, f.value]));
  const initial = JSON.stringify(values());
  let dirty = false;
  const store = {
    get() { try { return JSON.parse(localStorage.getItem(key)); } catch { return null; } },
    set(v) { try { localStorage.setItem(key, JSON.stringify(v)); } catch { /* private mode: no autosave */ } },
    clear() { try { localStorage.removeItem(key); } catch { /* nothing */ } },
  };
  const note = document.querySelector('[data-autosaved]');
  const autosave = () => {
    if (!dirty) return;
    store.set({ time: Date.now(), values: values() });
    if (note) note.textContent = ` · unsaved changes kept in this browser at ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
  };
  form.addEventListener('input', () => { dirty = JSON.stringify(values()) !== initial; ticks(); });
  setInterval(autosave, 30000);
  addEventListener('pagehide', autosave);
  addEventListener('beforeunload', e => { if (dirty && !form.dataset.submitting) { autosave(); e.preventDefault(); } });
  form.addEventListener('submit', () => { editors.forEach(ed => ed.sync()); form.dataset.submitting = '1'; store.clear(); });

  // Offer to bring back autosaved changes that are newer than the last save
  const kept = store.get(), banner = document.querySelector('[data-restore]');
  if (kept && kept.values && kept.time > (+form.dataset.saved || 0) * 1000 && JSON.stringify(kept.values) !== initial && banner) {
    banner.querySelector('[data-restore-time]').textContent = new Date(kept.time).toLocaleString();
    banner.hidden = false;
    banner.querySelector('[data-restore-yes]').addEventListener('click', () => {
      fields.forEach(f => { if (f.name in kept.values) f.value = kept.values[f.name]; });
      editors.forEach(ed => ed.load(ed.ta.value));
      dirty = true; ticks(); banner.hidden = true;
    });
    banner.querySelector('[data-restore-no]').addEventListener('click', () => { store.clear(); banner.hidden = true; });
  } else if (kept) {
    store.clear();
  }
  ticks();
})();
