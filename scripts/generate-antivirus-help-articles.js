#!/usr/bin/env node
/**
 * Genera artículos de ayuda antivirus (6 idiomas) a partir del shell de un artículo existente.
 * Mantiene planes, FAQs, footer y scripts del artículo MIR.
 */
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const shellPath = path.join(
  root,
  'articulos/configurar-mir-delfin-check-in-2026.html'
);
const shell = fs.readFileSync(shellPath, 'utf8');

const LOCALES = {
  es: {
    lang: 'es',
    dir: 'articulos',
    slug: 'antivirus-bloquea-enlace-activacion',
    home: 'https://delfincheckin.com',
    onboarding: 'https://admin.delfincheckin.com/es/onboarding',
    title: 'Si tu antivirus bloquea el enlace de activación de Delfín Check-in',
    description:
      'Guía paso a paso cuando Avast u otro antivirus marca «phishing» el email de bienvenida. El panel oficial es admin.delfincheckin.com.',
    keywords:
      'Avast phishing, enlace activación, Delfín Check-in, falso positivo antivirus, admin delfincheckin',
    readTime: '4',
    headerCta: 'Registro Gratis',
    headerFeatures: 'Funciones',
    content: `
<p>Algunos antivirus (Avast, AVG, Defender, etc.) marcan por error el email de bienvenida de <strong>Delfín Check-in</strong>. No es una estafa: es el acceso legítimo a tu panel de gestión.</p>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:16px 20px;margin:1.5rem 0;">
  <p style="margin:0 0 8px;font-weight:800;color:#1e3a8a;">Dominio oficial del panel</p>
  <p style="margin:0;font-family:ui-monospace,monospace;font-weight:700;">admin.delfincheckin.com</p>
</div>

<h2>Avast / AVG</h2>
<ol>
  <li>En la alerta, abre <strong>Más opciones</strong> o <strong>Detalles</strong>.</li>
  <li>Elige <strong>Informar de un falso positivo</strong> o añade una excepción para <code>admin.delfincheckin.com</code>.</li>
  <li>Copia el enlace del último email y pégalo en Chrome tras permitir la excepción.</li>
</ol>

<h2>Otras soluciones rápidas</h2>
<ul>
  <li>Abre el enlace completo del email (o el nuevo que te reenviamos) en el navegador.</li>
  <li>Prueba desde el móvil con datos móviles o otro navegador.</li>
  <li>Si el enlace caducó (72 h), pide uno nuevo desde la <a href="ONBOARDING_URL">pantalla de onboarding</a> con tu email.</li>
</ul>

<h2>Reporte a fabricantes</h2>
<p>Podemos reportar la URL a Avast y a Google Safe Browsing como falso positivo; las listas globales pueden tardar días en actualizarse.</p>

<p>¿Sigues bloqueado? Escríbenos a <a href="mailto:contacto@delfincheckin.com">contacto@delfincheckin.com</a> con el email con el que te registraste.</p>
`,
  },
  en: {
    lang: 'en',
    dir: 'en/articulos',
    slug: 'antivirus-blocks-activation-link',
    home: 'https://delfincheckin.com/en/',
    onboarding: 'https://admin.delfincheckin.com/en/onboarding',
    title: 'If your antivirus blocks the Delfín Check-in activation link',
    description:
      'Step-by-step guide when Avast or another antivirus flags the welcome email as phishing. The official panel is admin.delfincheckin.com.',
    keywords:
      'Avast phishing, activation link, Delfín Check-in, antivirus false positive',
    readTime: '4',
    headerCta: 'Free sign-up',
    headerFeatures: 'Features',
    content: `
<p>Some antivirus apps (Avast, AVG, Defender, etc.) wrongly flag the <strong>Delfín Check-in</strong> welcome email. It is not a scam — it is your legitimate management panel.</p>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:16px 20px;margin:1.5rem 0;">
  <p style="margin:0 0 8px;font-weight:800;color:#1e3a8a;">Official panel domain</p>
  <p style="margin:0;font-family:ui-monospace,monospace;font-weight:700;">admin.delfincheckin.com</p>
</div>

<h2>Avast / AVG</h2>
<ol>
  <li>In the alert, open <strong>More options</strong> or <strong>Details</strong>.</li>
  <li>Choose <strong>Report a false positive</strong> or add an exception for <code>admin.delfincheckin.com</code>.</li>
  <li>Copy the link from your latest email and paste it in Chrome after allowing the exception.</li>
</ol>

<h2>Other quick fixes</h2>
<ul>
  <li>Open the full link from the email (or the new one we resend) in your browser.</li>
  <li>Try from your phone on mobile data or another browser.</li>
  <li>If the link expired (72h), request a new one from <a href="ONBOARDING_URL">onboarding</a> with your email.</li>
</ul>

<h2>Vendor reports</h2>
<p>We can report the URL to Avast and Google Safe Browsing; global lists may take days to update.</p>

<p>Still blocked? Email <a href="mailto:contacto@delfincheckin.com">contacto@delfincheckin.com</a> with your registration address.</p>
`,
  },
  fr: {
    lang: 'fr',
    dir: 'fr/articulos',
    slug: 'antivirus-bloque-lien-activation',
    home: 'https://delfincheckin.com/fr/',
    onboarding: 'https://admin.delfincheckin.com/fr/onboarding',
    title: 'Si votre antivirus bloque le lien d’activation Delfín Check-in',
    description:
      'Guide lorsqu’Avast ou un autre antivirus signale le courriel de bienvenue comme phishing. Panneau officiel : admin.delfincheckin.com.',
    keywords: 'Avast phishing, lien activation, Delfín Check-in, faux positif antivirus',
    readTime: '4',
    headerCta: 'Inscription gratuite',
    headerFeatures: 'Fonctionnalités',
    content: `
<p>Certains antivirus (Avast, AVG, Defender…) signalent par erreur l’e-mail de bienvenue de <strong>Delfín Check-in</strong>. Ce n’est pas une arnaque : c’est l’accès légitime à votre panneau.</p>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:16px 20px;margin:1.5rem 0;">
  <p style="margin:0 0 8px;font-weight:800;color:#1e3a8a;">Domaine officiel du panneau</p>
  <p style="margin:0;font-family:ui-monospace,monospace;font-weight:700;">admin.delfincheckin.com</p>
</div>

<h2>Avast / AVG</h2>
<ol>
  <li>Dans l’alerte, ouvrez <strong>Plus d’options</strong> ou <strong>Détails</strong>.</li>
  <li>Choisissez <strong>Signaler un faux positif</strong> ou une exception pour <code>admin.delfincheckin.com</code>.</li>
  <li>Copiez le lien du dernier e-mail et ouvrez-le dans Chrome après l’exception.</li>
</ol>

<h2>Autres solutions</h2>
<ul>
  <li>Ouvrez le lien complet de l’e-mail (ou le nouveau renvoyé) dans le navigateur.</li>
  <li>Essayez depuis le mobile en données ou un autre navigateur.</li>
  <li>Si le lien a expiré (72 h), demandez-en un nouveau via <a href="ONBOARDING_URL">l’onboarding</a>.</li>
</ul>

<p>Toujours bloqué ? <a href="mailto:contacto@delfincheckin.com">contacto@delfincheckin.com</a></p>
`,
  },
  it: {
    lang: 'it',
    dir: 'it/articulos',
    slug: 'antivirus-blocca-link-attivazione',
    home: 'https://delfincheckin.com/it/',
    onboarding: 'https://admin.delfincheckin.com/it/onboarding',
    title: 'Se l’antivirus blocca il link di attivazione Delfín Check-in',
    description:
      'Guida quando Avast o altro antivirus segnala l’email di benvenuto come phishing. Pannello ufficiale: admin.delfincheckin.com.',
    keywords: 'Avast phishing, link attivazione, Delfín Check-in, falso positivo',
    readTime: '4',
    headerCta: 'Registrazione gratuita',
    headerFeatures: 'Funzioni',
    content: `
<p>Alcuni antivirus (Avast, AVG, Defender…) segnalano per errore l’email di benvenuto di <strong>Delfín Check-in</strong>. Non è una truffa: è l’accesso legittimo al pannello.</p>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:16px 20px;margin:1.5rem 0;">
  <p style="margin:0 0 8px;font-weight:800;color:#1e3a8a;">Dominio ufficiale del pannello</p>
  <p style="margin:0;font-family:ui-monospace,monospace;font-weight:700;">admin.delfincheckin.com</p>
</div>

<h2>Avast / AVG</h2>
<ol>
  <li>Nell’avviso, apri <strong>Altre opzioni</strong> o <strong>Dettagli</strong>.</li>
  <li>Scegli <strong>Segnala falso positivo</strong> o un’eccezione per <code>admin.delfincheckin.com</code>.</li>
  <li>Copia il link dall’ultima email e incollalo in Chrome.</li>
</ol>

<ul>
  <li>Apri il link completo dall’email o quello nuovo che ti inviamo.</li>
  <li>Prova da telefono con dati mobili o altro browser.</li>
  <li>Link scaduto (72 h)? Richiedine uno da <a href="ONBOARDING_URL">onboarding</a>.</li>
</ul>

<p>Bloccato ancora? <a href="mailto:contacto@delfincheckin.com">contacto@delfincheckin.com</a></p>
`,
  },
  pt: {
    lang: 'pt',
    dir: 'pt/articulos',
    slug: 'antivirus-bloqueia-link-ativacao',
    home: 'https://delfincheckin.com/pt/',
    onboarding: 'https://admin.delfincheckin.com/pt/onboarding',
    title: 'Se o antivírus bloquear o link de ativação do Delfín Check-in',
    description:
      'Guia quando o Avast ou outro antivírus marca o email de boas-vindas como phishing. Painel oficial: admin.delfincheckin.com.',
    keywords: 'Avast phishing, link ativação, Delfín Check-in, falso positivo',
    readTime: '4',
    headerCta: 'Registo grátis',
    headerFeatures: 'Funcionalidades',
    content: `
<p>Alguns antivírus (Avast, AVG, Defender…) marcam por engano o email de boas-vindas do <strong>Delfín Check-in</strong>. Não é fraude: é o acesso legítimo ao painel.</p>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:16px 20px;margin:1.5rem 0;">
  <p style="margin:0 0 8px;font-weight:800;color:#1e3a8a;">Domínio oficial do painel</p>
  <p style="margin:0;font-family:ui-monospace,monospace;font-weight:700;">admin.delfincheckin.com</p>
</div>

<h2>Avast / AVG</h2>
<ol>
  <li>No alerta, abra <strong>Mais opções</strong> ou <strong>Detalhes</strong>.</li>
  <li>Escolha <strong>Reportar falso positivo</strong> ou exceção para <code>admin.delfincheckin.com</code>.</li>
  <li>Copie o link do último email e abra no Chrome.</li>
</ol>

<ul>
  <li>Abra o link completo do email (ou o novo que reenviamos).</li>
  <li>Tente no telemóvel com dados móveis ou outro browser.</li>
  <li>Link expirado (72 h)? Peça um novo em <a href="ONBOARDING_URL">onboarding</a>.</li>
</ul>

<p>Ainda bloqueado? <a href="mailto:contacto@delfincheckin.com">contacto@delfincheckin.com</a></p>
`,
  },
  fi: {
    lang: 'fi',
    dir: 'fi/articulos',
    slug: 'antivirus-estaa-aktivointilinkki',
    home: 'https://delfincheckin.com/fi/',
    onboarding: 'https://admin.delfincheckin.com/fi/onboarding',
    title: 'Jos virustentorjunta estää Delfín Check-in -aktivointilinkin',
    description:
      'Ohje kun Avast tai muu ohjelma merkitsee tervetulosähköpostin phishingiksi. Virallinen paneeli: admin.delfincheckin.com.',
    keywords: 'Avast phishing, aktivointilinkki, Delfín Check-in, väärä positiivinen',
    readTime: '4',
    headerCta: 'Ilmainen rekisteröityminen',
    headerFeatures: 'Ominaisuudet',
    content: `
<p>Jotkin virustentorjuntaohjelmat (Avast, AVG, Defender…) merkitsevät virheellisesti <strong>Delfín Check-in</strong> -tervetulosähköpostin. Kyseessä ei ole huijaus vaan laillinen hallintapaneeli.</p>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:16px 20px;margin:1.5rem 0;">
  <p style="margin:0 0 8px;font-weight:800;color:#1e3a8a;">Virallinen paneelin domain</p>
  <p style="margin:0;font-family:ui-monospace,monospace;font-weight:700;">admin.delfincheckin.com</p>
</div>

<h2>Avast / AVG</h2>
<ol>
  <li>Avaa hälytyksessä <strong>Lisäasetukset</strong> tai <strong>Tiedot</strong>.</li>
  <li>Valitse <strong>Ilmoita väärästä positiivisesta</strong> tai poikkeus <code>admin.delfincheckin.com</code>.</li>
  <li>Kopioi linkki viimeisestä sähköpostista ja avaa Chromessa.</li>
</ol>

<ul>
  <li>Avaa sähköpostin koko linkki (tai uusi lähetetty linkki).</li>
  <li>Kokeile puhelimella mobiilidatalla tai toisella selaimella.</li>
  <li>Linkki vanhentunut (72 h)? Pyydä uusi <a href="ONBOARDING_URL">onboardingissa</a>.</li>
</ul>

<p>Yhä estetty? <a href="mailto:contacto@delfincheckin.com">contacto@delfincheckin.com</a></p>
`,
  },
};

const HREFLANG = [
  ['es', 'https://delfincheckin.com/articulos/antivirus-bloquea-enlace-activacion'],
  ['en', 'https://delfincheckin.com/en/articulos/antivirus-blocks-activation-link'],
  ['fr', 'https://delfincheckin.com/fr/articulos/antivirus-bloque-lien-activation'],
  ['it', 'https://delfincheckin.com/it/articulos/antivirus-blocca-link-attivazione'],
  ['pt', 'https://delfincheckin.com/pt/articulos/antivirus-bloqueia-link-ativacao'],
  ['fi', 'https://delfincheckin.com/fi/articulos/antivirus-estaa-aktivointilinkki'],
];

function langSwitcher(active) {
  const items = [
    ['es', 'https://delfincheckin.com/articulos/antivirus-bloquea-enlace-activacion', 'ES', '🇪🇸'],
    ['en', 'https://delfincheckin.com/en/articulos/antivirus-blocks-activation-link', 'EN', '🇬🇧'],
    ['fr', 'https://delfincheckin.com/fr/articulos/antivirus-bloque-lien-activation', 'FR', '🇫🇷'],
    ['it', 'https://delfincheckin.com/it/articulos/antivirus-blocca-link-attivazione', 'IT', '🇮🇹'],
    ['pt', 'https://delfincheckin.com/pt/articulos/antivirus-bloqueia-link-ativacao', 'PT', '🇵🇹'],
    ['fi', 'https://delfincheckin.com/fi/articulos/antivirus-estaa-aktivointilinkki', 'FI', '🇫🇮'],
  ];
  const links = items
    .map(([code, href, label, flag]) => {
      const cls =
        code === active
          ? 'lang-switch__btn lang-switch__btn--active'
          : 'lang-switch__btn';
      return `<a href="${href}" class="${cls}" hreflang="${code}" lang="${code}" title="${label}"><span aria-hidden="true">${flag}</span><span class="lang-switch__code">${label}</span></a>`;
    })
    .join('\n          ');
  return `<nav class="lang-switch" role="navigation" aria-label="Idioma" style="display:inline-flex;gap:4px;margin-right:8px;flex-wrap:wrap;">\n          ${links}\n        </nav>`;
}

function extractTail(html) {
  const marker = '<section style="margin: 2.5rem 0;">';
  const idx = html.indexOf(marker);
  if (idx === -1) throw new Error('No se encontró bloque de planes en el shell');
  return html.slice(idx);
}

const tail = extractTail(shell);

function buildLocale(loc, cfg) {
  const canonical = `https://delfincheckin.com/${cfg.dir}/${cfg.slug}`;
  const content = cfg.content.trim().replace(/ONBOARDING_URL/g, cfg.onboarding);
  const hreflangBlock = HREFLANG.map(
    ([lang, url]) =>
      `  <link rel="alternate" hreflang="${lang}" href="${url}">`
  ).join('\n');

  let head = shell.slice(shell.indexOf('<!DOCTYPE'), shell.indexOf('</head>') + 7);
  head = head.replace(/<html lang="[^"]*">/, `<html lang="${cfg.lang}">`);
  head = head.replace(/<title>[\s\S]*?<\/title>/, `<title>${cfg.title} | Delfín Check-in</title>`);
  head = head.replace(
    /<meta name="description" content="[^"]*">/,
    `<meta name="description" content="${cfg.description.replace(/"/g, '&quot;')}">`
  );
  head = head.replace(
    /<meta name="keywords" content="[^"]*">/,
    `<meta name="keywords" content="${cfg.keywords}">`
  );
  head = head.replace(
    /<link rel="canonical" href="[^"]*">/,
    `<link rel="canonical" href="${canonical}">`
  );
  head = head.replace(
    /<meta property="og:url" content="[^"]*">/,
    `<meta property="og:url" content="${canonical}">`
  );
  head = head.replace(
    /<meta property="og:title" content="[^"]*">/,
    `<meta property="og:title" content="${cfg.title.replace(/"/g, '&quot;')}">`
  );
  head = head.replace(
    /<meta property="og:description" content="[^"]*">/,
    `<meta property="og:description" content="${cfg.description.replace(/"/g, '&quot;')}">`
  );
  head = head.replace(
    /<meta name="twitter:url" content="[^"]*">/,
    `<meta name="twitter:url" content="${canonical}">`
  );
  head = head.replace(
    /<meta name="twitter:title" content="[^"]*">/,
    `<meta name="twitter:title" content="${cfg.title.replace(/"/g, '&quot;')}">`
  );
  head = head.replace(
    /<meta name="twitter:description" content="[^"]*">/,
    `<meta name="twitter:description" content="${cfg.description.replace(/"/g, '&quot;')}">`
  );
  head = head.replace(
    /<meta name="language" content="[^"]*">/,
    `<meta name="language" content="${cfg.lang}">`
  );
  if (!head.includes('hreflang="es"')) {
    head = head.replace('</head>', `${hreflangBlock}\n  <link rel="alternate" hreflang="x-default" href="https://delfincheckin.com/articulos/antivirus-bloquea-enlace-activacion">\n</head>`);
  }
  if (!head.includes('lang-switcher-home.css')) {
    head = head.replace(
      '</head>',
      '  <link rel="stylesheet" href="/lang-switcher-home.css" />\n</head>'
    );
  }

  const header = `  <header>
    <div class="nav">
      <a href="${cfg.home}" class="brand">
        <div class="logo" aria-hidden="true">🐬</div>
        <b>Delfín Check‑in</b>
      </a>
      <div class="nav-actions" style="flex-wrap:wrap;align-items:center;">
        ${langSwitcher(loc)}
        <a class="btn primary" href="${cfg.home}#registro">${cfg.headerCta}</a>
        <a class="btn" href="${cfg.home}#caracteristicas">${cfg.headerFeatures}</a>
      </div>
    </div>
  </header>`;

  const main = `  <main class="container">
    <article>
      <h1>${cfg.title}</h1>
      <div class="article-meta">
        <span>📅 2026-05-20</span>
        <span>✍️ Delfín Check-in</span>
        <span>⏱️ ${cfg.readTime} min lectura</span>
      </div>
      <div class="article-content">
        ${content}
      </div>
    </article>
    ${tail}`;

  const bodyStart = shell.indexOf('<body>');
  const styles = shell.slice(shell.indexOf('<style>'), bodyStart);

  return `<!DOCTYPE html>
<html lang="${cfg.lang}">
<head>
${head.slice(head.indexOf('<!-- Google tag'))}
${styles}
</head>
<body>
${header}

${main}
`;
}

for (const [loc, cfg] of Object.entries(LOCALES)) {
  const outDir = path.join(root, cfg.dir);
  fs.mkdirSync(outDir, { recursive: true });
  const outPath = path.join(outDir, `${cfg.slug}.html`);
  fs.writeFileSync(outPath, buildLocale(loc, cfg), 'utf8');
  console.log('✓', path.relative(root, outPath));
}

console.log('\nListo. URLs públicas en delfincheckin.com/articulos/...');
