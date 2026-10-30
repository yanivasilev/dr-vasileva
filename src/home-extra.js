  const observeReveals = () => document.querySelectorAll('.page.active [data-reveal]:not(.in), .page.active .quote:not(.in), .page.active .about-photo:not(.in)').forEach(el => io.observe(el));
  observeReveals();

  // Live clocks for London and Sofia
  const clock = tz => new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: tz }).format(new Date());
  const tickClocks = () => {
    document.getElementById('t-lon').textContent = clock('Europe/London');
    document.getElementById('t-sof').textContent = clock('Europe/Sofia');
  };
  if (document.getElementById('t-lon')) { tickClocks(); setInterval(tickClocks, 15000); }

  // Greeting switches between Bulgarian and English
  const greetWords = [...document.querySelectorAll('#greet span')];
  let gi = 0;
  if (!reduce && greetWords.length) setInterval(() => {
    const cur = greetWords[gi]; gi = (gi + 1) % greetWords.length; const next = greetWords[gi];
    cur.classList.remove('on'); cur.classList.add('out');
    next.classList.remove('out'); next.classList.add('on');
    setTimeout(() => cur.classList.remove('out'), 900);
  }, 2600);
