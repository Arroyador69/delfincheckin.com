/**
 * Tutoriales YouTube en la portada (index.html y /en/, /it/, …).
 * UI según idioma de la URL; audio de los vídeos siempre en español.
 */
(function () {
  var STR = {
    es: {
      videoIntroTitle: '¿Qué es Delfín Check-in?',
      videoIntroBody:
        'Registro de viajeros, reserva en el panel y envío al Ministerio del Interior (MIR). Mira cómo encaja todo en un solo flujo.',
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
      videoIntroTitle: 'What is Delfín Check-in?',
      videoIntroBody:
        'Guest registration, booking in your dashboard, and submission to the Spanish Ministry (MIR). See how it fits together.',
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
      videoIntroTitle: "Cos'è Delfín Check-in?",
      videoIntroBody:
        "Registrazione ospiti, prenotazione nel pannello e invio al Ministero dell'Interno spagnolo (MIR). Guarda come funziona in un unico flusso.",
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
      videoIntroTitle: 'O que é o Delfín Check-in?',
      videoIntroBody:
        'Registo de hóspedes, reserva no painel e envio ao Ministério do Interior espanhol (MIR). Veja como encaixa num único fluxo.',
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
      videoIntroTitle: "Qu'est-ce que Delfín Check-in ?",
      videoIntroBody:
        "Enregistrement des voyageurs, réservation dans votre tableau de bord et envoi au ministère de l'Intérieur espagnol (MIR). Voyez comment tout s'articule.",
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
      videoIntroTitle: 'Mikä on Delfín Check-in?',
      videoIntroBody:
        'Vieraiden rekisteröinti, varaus paneelissa ja lähetys Espanjan sisäministeriölle (MIR). Katso miten kaikki linkittyy yhteen.',
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
      videoIntroTitle: 'Vad är Delfín Check-in?',
      videoIntroBody:
        'Gästregistrering, bokning i panelen och inlämning till Spaniens inrikesministerium (MIR). Se hur allt hänger ihop.',
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

  function apply() {
    var lang = detectLang();
    var t = STR[lang] || STR.es;
    document.querySelectorAll('[data-home-video-key]').forEach(function (el) {
      var key = el.getAttribute('data-home-video-key');
      if (t[key]) el.textContent = t[key];
    });
    var cta = document.getElementById('home-video-reputation-cta');
    if (cta) cta.setAttribute('href', plansProHref(lang));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', apply);
  } else {
    apply();
  }
})();
