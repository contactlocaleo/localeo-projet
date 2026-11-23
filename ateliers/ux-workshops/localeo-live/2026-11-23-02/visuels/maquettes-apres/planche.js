(() => {
  const icons = {
    bell: '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M10 21h4"/>',
    menu: '<path d="M4 6h16M4 12h16M4 18h16"/>',
    book: '<path d="M12 6v15M3 4h5a4 4 0 0 1 4 2 4 4 0 0 1 4-2h5v14h-5a5 5 0 0 0-4 3 5 5 0 0 0-4-3H3z"/>',
    gift: '<path d="M3 8h18v4H3zM5 12v9h14v-9M12 8v13M12 8c-6 0-7-5-3-5 2 0 3 3 3 5 0-2 1-5 3-5 4 0 3 5-3 5z"/>',
    compass: '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-1.7 5.3-5.3 1.7 1.7-5.3z"/>',
    calendar: '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 9h16M8 3v4M16 3v4M8 13h3M8 16h6"/>',
    pin: '<path d="M19 10c0 4-7 10-7 10S5 14 5 10a7 7 0 1 1 14 0z"/><circle cx="12" cy="10" r="2"/>',
    search: '<circle cx="10.5" cy="10.5" r="5.5"/><path d="m15 15 5 5"/>',
    refresh: '<path d="M20 10a8 8 0 1 0-2 8M20 4v6h-6"/>',
    share: '<path d="M12 16V3m-4 4 4-4 4 4M5 12v8h14v-8"/>'
  };
  const screens = window.LiveMockScreens || {};
  const params = new URLSearchParams(location.search);
  const key = params.get('etat') || 'C1-consignes';
  const screen = Object.hasOwn(screens, key) ? screens[key] : null;
  const main = document.querySelector('#screen');
  if (screen) {
    document.title = key.split('-')[0] + ' · ' + screen.title + ' — Maquette Localeo Live';
    main.innerHTML = screen.body;
    if (key.startsWith('F1-') && params.get('origine') === 'tirages') {
      main.querySelector('.backlink').outerHTML = '<a class="backlink" href="?etat=D1-tirages#tirage-passeport">← Retour à mes lots</a>';
      main.querySelectorAll('a[href^="?etat=F1-"]').forEach((link) => {
        const destination = new URL(link.href);
        destination.searchParams.set('origine', 'tirages');
        link.href = destination.href;
      });
    }
    document.querySelectorAll('[data-tab]').forEach((tab) => {
      if (tab.dataset.tab === screen.tab) tab.setAttribute('aria-current', 'page');
    });
  } else {
    main.innerHTML = '<h1>Planche indisponible</h1><a class="action" href="../comparatif-avant-apres.html">Ouvrir le comparatif</a>';
  }

  document.querySelectorAll('[data-icon]').forEach((element) => {
    const path = icons[element.dataset.icon];
    if (path) {
      element.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + path + '</svg>';
      element.setAttribute('aria-hidden', 'true');
    }
  });

  document.addEventListener('submit', (event) => event.preventDefault());
  document.addEventListener('click', (event) => {
    if (event.target.closest('[aria-disabled="true"]')) event.preventDefault();
    const link = event.target.closest('a[data-focus-target]');
    const destination = link && document.getElementById(link.hash.slice(1));
    if (destination) {
      event.preventDefault();
      destination.focus({ preventScroll: true });
      destination.scrollIntoView({ block: 'start' });
    }
  });
  if (screen && window.parent !== window) {
    window.parent.postMessage({ type: 'localeo-planche', key }, '*');
  }
  if (location.hash) {
    const destination = document.getElementById(location.hash.slice(1));
    if (destination) requestAnimationFrame(() => {
      destination.focus({ preventScroll: true });
      destination.scrollIntoView({ block: 'nearest' });
    });
  } else if (screen?.startAt) {
    document.fonts.ready.then(() => document.getElementById(screen.startAt)?.scrollIntoView({ block: 'start' }));
  }
})();
