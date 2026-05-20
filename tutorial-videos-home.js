/**
 * Tutoriales YouTube en la portada (index.html y /en/, /it/, …).
 * UI según idioma de la URL; audio de los vídeos siempre en español.
 */
(function () {
  var STR = {
    es: {
      videoIntroEyebrow: 'Vídeo · 2 minutos',
      videoIntroTitle: '¿Qué es Delfín Check-in?',
      videoIntroBody:
        'Software para alojamientos: registro de viajeros (MIR), reservas en tu panel y envío al Ministerio del Interior. Míralo primero y luego explora planes y registro gratis.',
      videoHeroCtaPrimary: 'Empezar gratis',
      videoHeroCtaPlans: 'Ver planes',
      videoOnboardingTitle: 'Empieza gratis en 6 pasos',
      videoOnboardingBody:
        'Regístrate sin tarjeta, recibe el email de onboarding y en minutos tienes el panel listo. El sistema trabaja por ti.',
      videoReputationBadge: 'Plan Pro',
      videoReputationTitle: 'Reseñas en Google y más reservas directas',
      videoReputationBody:
        'Tras cada checkout, tus huéspedes reciben un recordatorio para valorarte en Google. Te encuentran en Maps antes de entrar en Airbnb o Booking.',
      videoReputationCta: 'Contratar Plan Pro',
      videoSpanishNote: 'El audio del vídeo está en español.',
    },
    en: {
      videoIntroEyebrow: 'Video · 2 minutes',
      videoIntroTitle: 'What is Delfín Check-in?',
      videoIntroBody:
        'Software for lodging: guest registration (MIR), bookings in your dashboard, and submission to the Spanish Ministry. Watch this first, then explore plans and free signup.',
      videoHeroCtaPrimary: 'Start free',
      videoHeroCtaPlans: 'View plans',
      videoOnboardingTitle: 'Start free in 6 steps',
      videoOnboardingBody:
        'Sign up with no card, open the onboarding email, and have your panel ready in minutes. The system works for you.',
      videoReputationBadge: 'Pro plan',
      videoReputationTitle: 'Google reviews and more direct bookings',
      videoReputationBody:
        'After each checkout, guests get a reminder to review you on Google. They find you on Maps before opening Airbnb or Booking.',
      videoReputationCta: 'Get Pro plan',
      videoSpanishNote: 'Video audio is in Spanish.',
    },
    it: {
      videoIntroEyebrow: 'Video · 2 minuti',
      videoIntroTitle: "Cos'è Delfín Check-in?",
      videoIntroBody:
        "Software per strutture ricettive: registrazione ospiti (MIR), prenotazioni nel pannello e invio al Ministero dell'Interno spagnolo. Guardalo per primo, poi scopri piani e registrazione gratuita.",
      videoHeroCtaPrimary: 'Inizia gratis',
      videoHeroCtaPlans: 'Vedi i piani',
      videoOnboardingTitle: 'Inizia gratis in 6 passi',
      videoOnboardingBody:
        "Registrati senza carta, apri l'email di onboarding e in pochi minuti il pannello è pronto. Il sistema lavora per te.",
      videoReputationBadge: 'Piano Pro',
      videoReputationTitle: 'Recensioni Google e più prenotazioni dirette',
      videoReputationBody:
        'Dopo ogni checkout, gli ospiti ricevono un promemoria per recensirti su Google. Ti trovano su Maps prima di aprire Airbnb o Booking.',
      videoReputationCta: 'Attiva il Piano Pro',
      videoSpanishNote: "L'audio del video è in spagnolo.",
    },
    pt: {
      videoIntroEyebrow: 'Vídeo · 2 minutos',
      videoIntroTitle: 'O que é o Delfín Check-in?',
      videoIntroBody:
        'Software para alojamentos: registo de hóspedes (MIR), reservas no painel e envio ao Ministério do Interior espanhol. Veja primeiro e depois explore planos e registo grátis.',
      videoHeroCtaPrimary: 'Começar grátis',
      videoHeroCtaPlans: 'Ver planos',
      videoOnboardingTitle: 'Comece grátis em 6 passos',
      videoOnboardingBody:
        'Registe-se sem cartão, abra o email de onboarding e em minutos o painel está pronto. O sistema trabalha por si.',
      videoReputationBadge: 'Plano Pro',
      videoReputationTitle: 'Avaliações no Google e mais reservas diretas',
      videoReputationBody:
        'Após cada checkout, os hóspedes recebem um lembrete para avaliar no Google. Encontram-no no Maps antes de abrir Airbnb ou Booking.',
      videoReputationCta: 'Contratar Plano Pro',
      videoSpanishNote: 'O áudio do vídeo está em espanhol.',
    },
    fr: {
      videoIntroEyebrow: 'Vidéo · 2 minutes',
      videoIntroTitle: "Qu'est-ce que Delfín Check-in ?",
      videoIntroBody:
        "Logiciel pour hébergements : fiches voyageurs (MIR), réservations dans votre tableau de bord et envoi au ministère de l'Intérieur espagnol. Regardez d'abord, puis découvrez les offres et l'inscription gratuite.",
      videoHeroCtaPrimary: 'Commencer gratuitement',
      videoHeroCtaPlans: 'Voir les offres',
      videoOnboardingTitle: 'Commencez gratuitement en 6 étapes',
      videoOnboardingBody:
        "Inscrivez-vous sans carte, ouvrez l'email d'onboarding et votre panneau est prêt en quelques minutes. Le système travaille pour vous.",
      videoReputationBadge: 'Offre Pro',
      videoReputationTitle: 'Avis Google et plus de réservations directes',
      videoReputationBody:
        'Après chaque départ, vos clients reçoivent un rappel pour vous noter sur Google. Vous trouvent sur Maps avant Airbnb ou Booking.',
      videoReputationCta: "Choisir l'offre Pro",
      videoSpanishNote: "L'audio de la vidéo est en espagnol.",
    },
    fi: {
      videoIntroEyebrow: 'Video · 2 minuuttia',
      videoIntroTitle: 'Mikä on Delfín Check-in?',
      videoIntroBody:
        'Majoitusohjelmisto: vierasrekisteröinti (MIR), varaukset paneelissa ja lähetys Espanjan sisäministeriölle. Katso ensin, sitten tutustu suunnitelmiin ja ilmaiseen rekisteröitymiseen.',
      videoHeroCtaPrimary: 'Aloita ilmaiseksi',
      videoHeroCtaPlans: 'Katso suunnitelmat',
      videoOnboardingTitle: 'Aloita ilmaiseksi 6 vaiheessa',
      videoOnboardingBody:
        'Rekisteröidy ilman korttia, avaa onboarding-sähköposti ja paneeli on valmis minuuteissa. Järjestelmä tekee työn puolestasi.',
      videoReputationBadge: 'Pro-sopimus',
      videoReputationTitle: 'Google-arvostelut ja enemmän suoria varauksia',
      videoReputationBody:
        'Jokaisen uloskirjautumisen jälkeen vieraat saavat muistutuksen arvioida sinut Googlessa. Löytävät sinut Mapsista ennen Airbnbta tai Bookingia.',
      videoReputationCta: 'Tilaa Pro-sopimus',
      videoSpanishNote: 'Videon ääni on espanjaksi.',
    },
    sv: {
      videoIntroEyebrow: 'Video · 2 minuter',
      videoIntroTitle: 'Vad är Delfín Check-in?',
      videoIntroBody:
        'Programvara för boenden: gästregistrering (MIR), bokningar i panelen och inlämning till Spaniens inrikesministerium. Titta först, utforska sedan planer och gratis registrering.',
      videoHeroCtaPrimary: 'Börja gratis',
      videoHeroCtaPlans: 'Se planer',
      videoOnboardingTitle: 'Börja gratis i 6 steg',
      videoOnboardingBody:
        'Registrera dig utan kort, öppna onboarding-mailet och panelen är klar på minuter. Systemet jobbar för dig.',
      videoReputationBadge: 'Pro-plan',
      videoReputationTitle: 'Google-omdömen och fler direktbokningar',
      videoReputationBody:
        'Efter varje utcheckning får gäster en påminnelse att recensera dig på Google. De hittar dig på Maps innan Airbnb eller Booking.',
      videoReputationCta: 'Välj Pro-plan',
      videoSpanishNote: 'Videons ljud är på spanska.',
    },
  };

  function detectLang() {
    var p = (location.pathname || '/').replace(/\/$/, '') || '/';
    if (p === '/en' || p.indexOf('/en/') === 0) return 'en';
    if (p === '/it' || p.indexOf('/it/') === 0) return 'it';
    if (p === '/pt' || p.indexOf('/pt/') === 0) return 'pt';
    if (p === '/fr' || p.indexOf('/fr/') === 0) return 'fr';
    if (p === '/fi' || p.indexOf('/fi/') === 0) return 'fi';
    if (p === '/sv' || p.indexOf('/sv/') === 0) return 'sv';
    return 'es';
  }

  function plansProHref(lang) {
    var q = '?lang=' + encodeURIComponent(lang) + '&source=home-reputation#plan-pro';
    if (lang === 'es') return '/planes/' + q;
    return '/' + lang + '/planes/' + q;
  }

  function plansHref(lang) {
    if (lang === 'es') return '/planes/';
    return '/' + lang + '/planes/';
  }

  function apply() {
    var lang = detectLang();
    var t = STR[lang] || STR.es;
    document.querySelectorAll('[data-home-video-key]').forEach(function (el) {
      var key = el.getAttribute('data-home-video-key');
      if (t[key]) el.textContent = t[key];
    });
    var cta = document.getElementById('home-video-reputation-cta');
    if (cta) cta.setAttribute('href', plansProHref(lang));
    var plansBtn = document.getElementById('home-video-hero-plans');
    if (plansBtn) plansBtn.setAttribute('href', plansHref(lang));
    var iframe = document.querySelector('#home-video-intro iframe');
    if (iframe) iframe.setAttribute('title', t.videoIntroTitle);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', apply);
  } else {
    apply();
  }
})();
