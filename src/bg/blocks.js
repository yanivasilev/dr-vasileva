  const ctaButtons = `
    <a class="btn btn-whatsapp" href="${WA}">${ic('b-whatsapp', 'bi')}WhatsApp</a>
    <a class="btn btn-viber" href="${VIBER}">${ic('b-viber', 'bi')}Viber</a>
    <a class="btn btn-cream" href="${TEL}">${ic('i-phone')}Обаждане</a>`;
  const hero = ({ crumbs = [], eyebrow, title, lead, icon }) => `
    <section class="page-hero grain on-dark">
      <span class="blob b1"></span><span class="blob b2"></span>
      ${icon ? `<svg class="icon hero-icon"><use href="#${icon}"/></svg>` : ''}
      <div class="wrap">
        <nav class="crumbs" aria-label="Навигационна пътека"><a href="#/">Начало</a>${crumbs.map(([t, h]) => h ? `<span><a href="${h}">${t}</a></span>` : `<span>${t}</span>`).join('')}</nav>
        ${eyebrow ? `<span class="eyebrow" data-reveal>${eyebrow}</span>` : ''}
        <h1 data-reveal style="--d:.05s">${title}</h1>
        ${lead ? `<p class="lead" data-reveal style="--d:.12s">${lead}</p>` : ''}
      </div>
    </section>`;
  const ctaBand = (title = 'Готови ли сте за <em>разговор</em>?', text = 'Обадете се или ми пишете на български или английски. Ще намерим удобно за Вас време.') => `
    <section class="cta-band"><div class="wrap"><div class="cta-box grain on-dark" data-reveal>
      <div><h2>${title}</h2><p>${text}</p></div>
      <div class="btn-row">${ctaButtons}</div>
    </div></div></section>`;
  const contactBox = `
    <div class="box dark grain on-dark"><h3>Свържете се с мен</h3><p>Онлайн или на живо, на български или английски.</p>
      <div class="btn-row">
        <a class="btn btn-whatsapp" href="${WA}">${ic('b-whatsapp', 'bi')}WhatsApp</a>
        <a class="btn btn-viber" href="${VIBER}">${ic('b-viber', 'bi')}Viber</a>
        <a class="btn btn-cream" href="${TEL}">${ic('i-phone')}${PHONE}</a>
      </div></div>`;
