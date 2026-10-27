// The editor's only script (served as /editor.js; the editor allows no other scripts).
// Everything here is a convenience: without it the forms still work, with both languages shown one under the other.
(() => {
  const form = document.querySelector('form[data-editor]');
  if (!form) return;

  // BG | EN tabs
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

  // Formatting toolbar: wraps the selected text (or inserts a sample) in the simple formatting the site understands
  const wrap = (ta, kind) => {
    const { selectionStart: a, selectionEnd: b, value: v } = ta;
    const sel = v.slice(a, b);
    // Headings, lists and quotes start on a new line: put the mark in front of every selected line
    const prefixLines = (p, sample) => {
      const out = (sel || sample).split('\n')
        .map((l, i) => (typeof p === 'function' ? p(i) : p) + l.replace(/^(#{2,3} |[-*] |\d+[.)] |> ?)/, '')).join('\n');
      const gap = a > 0 && v[a - 1] !== '\n' ? '\n\n' : '';
      return [v.slice(0, a) + gap + out, v.slice(b)];
    };
    let parts;
    switch (kind) {
      case 'bold': parts = [v.slice(0, a) + `**${sel || 'bold text'}**`, v.slice(b)]; break;
      case 'italic': parts = [v.slice(0, a) + `*${sel || 'italic text'}*`, v.slice(b)]; break;
      case 'link': {
        const url = prompt('Web address for the link (https://…):', 'https://');
        if (!url || !/^(https?:\/\/|mailto:)\S+$/.test(url)) return;
        parts = [v.slice(0, a) + `[${sel || 'link text'}](${url})`, v.slice(b)]; break;
      }
      case 'h2': parts = prefixLines('## ', 'Heading'); break;
      case 'h3': parts = prefixLines('### ', 'Smaller heading'); break;
      case 'list': parts = prefixLines('- ', 'First point\nSecond point'); break;
      case 'olist': parts = prefixLines(i => `${i + 1}. `, 'First step\nSecond step'); break;
      case 'quote': parts = prefixLines('> ', 'A quote'); break;
      default: return;
    }
    ta.value = parts[0] + parts[1];
    ta.focus();
    ta.selectionStart = ta.selectionEnd = parts[0].length;
    ta.dispatchEvent(new Event('input', { bubbles: true }));
  };
  document.querySelectorAll('.toolbar').forEach(bar => {
    bar.hidden = false;
    const ta = document.getElementById(bar.dataset.for);
    bar.addEventListener('click', e => { const btn = e.target.closest('button[data-md]'); if (btn) wrap(ta, btn.dataset.md); });
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

  // Autosave in this browser every 30 seconds, so nothing is lost if the browser closes before saving
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
  form.addEventListener('submit', () => { form.dataset.submitting = '1'; store.clear(); });

  // Offer to bring back autosaved changes that are newer than the last save
  const kept = store.get(), banner = document.querySelector('[data-restore]');
  if (kept && kept.values && kept.time > (+form.dataset.saved || 0) * 1000 && JSON.stringify(kept.values) !== initial && banner) {
    banner.querySelector('[data-restore-time]').textContent = new Date(kept.time).toLocaleString();
    banner.hidden = false;
    banner.querySelector('[data-restore-yes]').addEventListener('click', () => {
      fields.forEach(f => { if (f.name in kept.values) f.value = kept.values[f.name]; });
      dirty = true; ticks(); banner.hidden = true;
    });
    banner.querySelector('[data-restore-no]').addEventListener('click', () => { store.clear(); banner.hidden = true; });
  } else if (kept) {
    store.clear();
  }
  ticks();
})();
