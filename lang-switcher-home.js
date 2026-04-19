/**
 * Selector de idioma en la portada (index.html / en/index.html).
 * ES + EN = esta web; IT, PT, FR, FI = /landing.html?lang= (misma cobertura que producto).
 */
(function () {
  var LANGS = [
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'it', name: 'Italiano', flag: '🇮🇹' },
    { code: 'pt', name: 'Português', flag: '🇵🇹' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' },
    { code: 'fi', name: 'Suomi', flag: '🇫🇮' },
  ];

  function detectLang() {
    var p = (location.pathname || '/').replace(/\/$/, '') || '/';
    if (p === '/en' || p.indexOf('/en/') === 0) return 'en';
    return 'es';
  }

  function hrefFor(code) {
    if (code === 'es') return '/';
    if (code === 'en') return '/en/';
    return '/landing.html?lang=' + encodeURIComponent(code);
  }

  function entryFor(code) {
    for (var i = 0; i < LANGS.length; i++) {
      if (LANGS[i].code === code) return LANGS[i];
    }
    return LANGS[0];
  }

  function setOpen(open) {
    var dd = document.getElementById('home-lang-dd');
    var tr = document.getElementById('home-lang-trigger');
    if (!dd || !tr) return;
    if (open) {
      dd.classList.add('hl-open');
      tr.classList.add('hl-open');
      tr.setAttribute('aria-expanded', 'true');
    } else {
      dd.classList.remove('hl-open');
      tr.classList.remove('hl-open');
      tr.setAttribute('aria-expanded', 'false');
    }
  }

  function syncTrigger(lang) {
    var L = entryFor(lang);
    var full = document.getElementById('home-lang-trigger-full');
    var mob = document.getElementById('home-lang-trigger-mobile');
    if (full) full.textContent = (L.flag ? L.flag + ' ' : '') + L.name;
    if (mob) mob.textContent = L.flag || '';
    document.querySelectorAll('.home-lang-opt').forEach(function (btn) {
      var c = btn.getAttribute('data-lang-code');
      var on = c === lang;
      btn.classList.toggle('hl-active', on);
      btn.setAttribute('aria-current', on ? 'true' : 'false');
      var ch = btn.querySelector('.home-lang-check');
      if (ch) ch.style.visibility = on ? 'visible' : 'hidden';
    });
  }

  function init() {
    var root = document.getElementById('home-lang-root');
    var dd = document.getElementById('home-lang-dd');
    var tr = document.getElementById('home-lang-trigger');
    if (!root || !dd || !tr) return;

    var current = detectLang();
    LANGS.forEach(function (L) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'home-lang-opt' + (L.code === current ? ' hl-active' : '');
      btn.setAttribute('data-lang-code', L.code);
      btn.setAttribute('role', 'option');
      btn.setAttribute('aria-selected', L.code === current ? 'true' : 'false');
      var sf = document.createElement('span');
      sf.className = 'home-lang-flag';
      sf.setAttribute('aria-hidden', 'true');
      sf.textContent = L.flag;
      var sn = document.createElement('span');
      sn.textContent = L.name;
      var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('class', 'home-lang-check');
      svg.setAttribute('viewBox', '0 0 20 20');
      svg.setAttribute('fill', 'currentColor');
      svg.style.visibility = L.code === current ? 'visible' : 'hidden';
      var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute(
        'd',
        'M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z'
      );
      svg.appendChild(path);
      btn.appendChild(sf);
      btn.appendChild(sn);
      btn.appendChild(svg);
      btn.addEventListener('click', function () {
        if (L.code === 'es' && detectLang() === 'es') {
          setOpen(false);
          return;
        }
        if (L.code === 'en' && detectLang() === 'en') {
          setOpen(false);
          return;
        }
        location.href = hrefFor(L.code);
      });
      dd.appendChild(btn);
    });

    syncTrigger(current);

    tr.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !dd.classList.contains('hl-open');
      setOpen(open);
    });

    document.addEventListener('mousedown', function (e) {
      if (root.contains(e.target)) return;
      setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
