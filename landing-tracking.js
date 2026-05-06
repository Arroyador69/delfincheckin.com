/**
 * ========================================
 * Landing Page Analytics Tracking
 * ========================================
 * Sistema completo de tracking para la landing page
 */

(function() {
  'use strict';

  // Configuración
  const API_URL = 'https://admin.delfincheckin.com/api/landing/track';
  const SCROLL_THRESHOLDS = [25, 50, 75, 100]; // Porcentajes de scroll a trackear
  const POPUP_DELAY = 10000; // 10 segundos
  const POPUP_SCROLL_THRESHOLD = 50; // Mostrar popup al 50% de scroll

  /** Textos del popup según idioma de la landing (html lang). */
  function popupLangCode() {
    let l = (document.documentElement.getAttribute('lang') || 'es').toLowerCase().split('-')[0];
    const ok = ['es', 'en', 'it', 'pt', 'fr', 'fi', 'sv'];
    if (!ok.includes(l)) l = 'es';
    return l;
  }

  function subscribePageUrl() {
    return '#planes';
  }

  const POPUP_COPY = {
    es: {
      title: 'Prueba Delfín Check‑in gratis (1 propiedad)',
      body: 'Empieza hoy con <strong>1 propiedad gratis</strong>. Si necesitas automatizar el <strong>envío de partes de viajeros al Gobierno de España (MIR)</strong>, está disponible desde <strong>2€/mes</strong>.',
      cta: 'Ver planes',
      close: 'Cerrar',
    },
    en: {
      title: 'Try Delfín Check‑in free (1 property)',
      body: 'Start today with <strong>1 property free</strong>. If you need automatic <strong>traveller reports submission to Spain (MIR)</strong>, it’s available from <strong>€2/month</strong>.',
      cta: 'See plans',
      close: 'Close',
    },
    it: {
      title: 'Prova Delfín Check‑in gratis (1 proprietà)',
      body: 'Inizia oggi con <strong>1 proprietà gratis</strong>. Se ti serve l’invio automatico dei <strong>dati viaggiatori al Governo spagnolo (MIR)</strong>, è disponibile da <strong>2€/mese</strong>.',
      cta: 'Vedi piani',
      close: 'Chiudi',
    },
    pt: {
      title: 'Experimente o Delfín Check‑in grátis (1 propriedade)',
      body: 'Comece hoje com <strong>1 propriedade grátis</strong>. Se precisar do <strong>envio automático de dados de viajantes ao Governo de Espanha (MIR)</strong>, está disponível a partir de <strong>2€/mês</strong>.',
      cta: 'Ver planos',
      close: 'Fechar',
    },
    fr: {
      title: 'Essayez Delfín Check‑in gratuitement (1 propriété)',
      body: 'Commencez aujourd’hui avec <strong>1 propriété gratuite</strong>. Si vous avez besoin de l’<strong>envoi automatique des données voyageurs au Gouvernement espagnol (MIR)</strong>, c’est disponible dès <strong>2€/mois</strong>.',
      cta: 'Voir les offres',
      close: 'Fermer',
    },
    fi: {
      title: 'Kokeile Delfín Check‑in ilmaiseksi (1 kohde)',
      body: 'Aloita tänään: <strong>1 kohde ilmaiseksi</strong>. Jos tarvitset automaattisen <strong>matkustajatietojen lähetyksen Espanjan viranomaisille (MIR)</strong>, se on saatavilla alkaen <strong>2€/kk</strong>.',
      cta: 'Katso suunnitelmat',
      close: 'Sulje',
    },
    sv: {
      title: 'Testa Delfín Check‑in gratis (1 boende)',
      body: 'Börja idag med <strong>1 boende gratis</strong>. Om du behöver automatisk <strong>rapportering av resenärsdata till Spanien (MIR)</strong> finns det från <strong>2€/månad</strong>.',
      cta: 'Se planer',
      close: 'Stäng',
    },
  };

  // Generar o recuperar session_id
  function getSessionId() {
    let sessionId = localStorage.getItem('landing_session_id');
    if (!sessionId) {
      sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('landing_session_id', sessionId);
    }
    return sessionId;
  }

  // Obtener información del navegador
  function getBrowserInfo() {
    return {
      user_agent: navigator.userAgent,
      referrer: document.referrer || 'direct',
      language: navigator.language,
      screen_width: window.screen.width,
      screen_height: window.screen.height,
      viewport_width: window.innerWidth,
      viewport_height: window.innerHeight,
    };
  }

  // Enviar evento al servidor
  function trackEvent(eventType, eventData = {}) {
    const sessionId = getSessionId();
    const browserInfo = getBrowserInfo();

    const payload = {
      session_id: sessionId,
      event_type: eventType,
      event_data: {
        ...eventData,
        ...browserInfo,
        url: window.location.href,
        timestamp: new Date().toISOString(),
      },
      user_agent: browserInfo.user_agent,
      referrer: browserInfo.referrer,
    };

    // Enviar de forma asíncrona (no bloquear)
    fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    }).catch(error => {
      // Silenciar errores para no afectar UX
      console.debug('Tracking error (ignored):', error);
    });
  }

  // Trackear tiempo en página
  let timeOnPageStart = Date.now();
  let maxScrollDepth = 0;
  let scrollTracked = new Set();

  // Trackear page_view al cargar
  trackEvent('page_view', {
    page_title: document.title,
    page_path: window.location.pathname,
  });

  // Trackear scroll depth
  let lastScrollTime = Date.now();
  window.addEventListener('scroll', function() {
    const scrollPercent = Math.round(
      (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100
    );
    
    maxScrollDepth = Math.max(maxScrollDepth, scrollPercent);

    // Trackear cada threshold solo una vez
    SCROLL_THRESHOLDS.forEach(threshold => {
      if (scrollPercent >= threshold && !scrollTracked.has(threshold)) {
        scrollTracked.add(threshold);
        trackEvent('scroll', {
          scroll_percent: scrollPercent,
          scroll_position: window.scrollY,
        });
      }
    });

    // Mostrar popup al 50% de scroll (si no se ha mostrado)
    if (scrollPercent >= POPUP_SCROLL_THRESHOLD && !window.popupShown) {
      showPopup();
    }
  }, { passive: true });

  // Trackear clics en elementos importantes
  document.addEventListener('click', function(e) {
    const target = e.target;
    const tagName = target.tagName.toLowerCase();
    
    // Trackear clics en botones, links y elementos con data-track
    if (tagName === 'button' || tagName === 'a' || target.hasAttribute('data-track')) {
      trackEvent('click', {
        element: tagName,
        text: target.textContent?.trim().substring(0, 50),
        href: target.href || null,
        id: target.id || null,
        class: target.className || null,
      });
    }
  });

  const FREE_SIGNUP_MSG = {
    es: {
      invalid: 'Introduce un email válido.',
      ok: '<strong>Revisa tu correo.</strong> Te hemos enviado un enlace para continuar con el onboarding.',
      err: 'No se pudo completar. Inténtalo de nuevo.',
      net: 'Error de conexión. Inténtalo más tarde.',
    },
    en: {
      invalid: 'Please enter a valid email.',
      ok: '<strong>Check your inbox.</strong> We sent you a link to finish onboarding.',
      err: 'Something went wrong. Try again later.',
      net: 'Connection error. Try again later.',
    },
    it: {
      invalid: 'Inserisci un’email valida.',
      ok: '<strong>Controlla la posta.</strong> Ti abbiamo inviato un link per continuare l’onboarding.',
      err: 'Operazione non riuscita. Riprova.',
      net: 'Errore di connessione. Riprova più tardi.',
    },
    pt: {
      invalid: 'Introduza um email válido.',
      ok: '<strong>Verifique o seu email.</strong> Enviámos a ligação para continuar o onboarding.',
      err: 'Não foi possível concluir. Tente novamente.',
      net: 'Erro de ligação. Tente mais tarde.',
    },
    fr: {
      invalid: 'Veuillez saisir une adresse e-mail valide.',
      ok: '<strong>Vérifiez votre boîte mail.</strong> Nous vous avons envoyé un lien pour poursuivre l’onboarding.',
      err: 'Impossible de terminer. Réessayez.',
      net: 'Erreur de connexion. Réessayez plus tard.',
    },
    fi: {
      invalid: 'Anna kelvollinen sähköpostiosoite.',
      ok: '<strong>Tarkista postisi.</strong> Lähetimme linkin onboardingin jatkamiseen.',
      err: 'Toiminto epäonnistui. Yritä uudelleen.',
      net: 'Yhteysvirhe. Yritä myöhemmin uudelleen.',
    },
    sv: {
      invalid: 'Ange en giltig e-postadress.',
      ok: '<strong>Kolla din inkorg.</strong> Vi har skickat en länk för att fortsätta onboarding.',
      err: 'Det gick inte att slutföra. Försök igen.',
      net: 'Anslutningsfel. Försök igen senare.',
    },
  };

  function setupLandingFreeSignup() {
    const form = document.getElementById('landingFreeSignupForm');
    if (!form) return;

    const lang = popupLangCode();
    const copy = FREE_SIGNUP_MSG[lang] || FREE_SIGNUP_MSG.es;

    form.addEventListener('submit', async function(ev) {
      ev.preventDefault();
      const locale = form.getAttribute('data-signup-locale') || 'es';
      const emailEl = document.getElementById('landingFreeSignupEmail');
      const nameEl = document.getElementById('landingFreeSignupName');
      const msg = document.getElementById('landingFreeSignupMessage');
      const submitBtn = document.getElementById('landingFreeSignupSubmit');
      const tSubmit = document.getElementById('landingFreeSignupSubmitText');
      const tLoad = document.getElementById('landingFreeSignupLoading');
      if (!emailEl || !msg || !submitBtn || !tSubmit || !tLoad) return;

      const email = String(emailEl.value || '').trim();
      const name = nameEl ? String(nameEl.value || '').trim() : '';
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        msg.style.display = 'block';
        msg.style.background = '#fee2e2';
        msg.style.color = '#991b1b';
        msg.textContent = copy.invalid;
        return;
      }

      submitBtn.disabled = true;
      tSubmit.style.display = 'none';
      tLoad.style.display = 'inline';

      try {
        const res = await fetch('https://admin.delfincheckin.com/api/public/signup-free', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, name: name || undefined, locale }),
        });
        const data = await res.json().catch(function() {
          return {};
        });
        msg.style.display = 'block';
        if (data.success) {
          msg.style.background = '#d1fae5';
          msg.style.color = '#065f46';
          msg.innerHTML = copy.ok;
          emailEl.value = '';
          if (nameEl) nameEl.value = '';
          trackEvent('form_submit', { form_id: 'landing_free_signup' });
        } else {
          msg.style.background = '#fee2e2';
          msg.style.color = '#991b1b';
          msg.textContent = data.error || copy.err;
        }
      } catch (err) {
        msg.style.display = 'block';
        msg.style.background = '#fee2e2';
        msg.style.color = '#991b1b';
        msg.textContent = copy.net;
      } finally {
        submitBtn.disabled = false;
        tSubmit.style.display = 'inline';
        tLoad.style.display = 'none';
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupLandingFreeSignup);
  } else {
    setupLandingFreeSignup();
  }

  // Trackear inicio de formulario waitlist
  const waitlistForm = document.getElementById('waitlistForm');
  if (waitlistForm) {
    const waitlistEmail = document.getElementById('waitlistEmail');
    if (waitlistEmail) {
      waitlistEmail.addEventListener('focus', function() {
        trackEvent('form_start', {
          form_id: 'waitlist',
        });
      }, { once: true });
    }

    // Trackear envío de formulario (interceptar submit)
    const originalSubmit = window.submitWaitlist;
    if (originalSubmit) {
      window.submitWaitlist = function(event) {
        trackEvent('form_submit', {
          form_id: 'waitlist',
        });
        return originalSubmit.call(this, event);
      };
    }
  }

  // Trackear salida de página
  let exitTracked = false;
  window.addEventListener('beforeunload', function() {
    if (!exitTracked) {
      exitTracked = true;
      const timeOnPage = Math.round((Date.now() - timeOnPageStart) / 1000);
      
      // Enviar evento de salida (puede no llegar siempre, pero intentamos)
      navigator.sendBeacon(API_URL, JSON.stringify({
        session_id: getSessionId(),
        event_type: 'exit',
        time_on_page: timeOnPage,
        max_scroll_depth: maxScrollDepth,
      }));
    }
  });

  // ========================================
  // POPUP MODAL
  // ========================================

  let popupShown = false;
  let popupTimer = null;

  function createPopup() {
    const lang = popupLangCode();
    const copy = POPUP_COPY[lang] || POPUP_COPY.es;
    const subUrl = subscribePageUrl();

    // Crear overlay
    const overlay = document.createElement('div');
    overlay.id = 'pms-popup-overlay';
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      z-index: 10000;
      display: none;
      align-items: center;
      justify-content: center;
      animation: fadeIn 0.3s ease;
    `;

    // Crear popup
    const popup = document.createElement('div');
    popup.id = 'pms-popup';
    popup.style.cssText = `
      background: white;
      border-radius: 16px;
      padding: 32px;
      max-width: 500px;
      width: 90%;
      position: relative;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
      animation: slideUp 0.3s ease;
      text-align: center;
    `;

    const esc = (s) =>
      String(s || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/"/g, '&quot;');

    // Contenido del popup (planes; sin waitlist)
    popup.innerHTML = `
      <button id="pms-popup-close" type="button" style="
        position: absolute;
        top: 12px;
        right: 12px;
        background: none;
        border: none;
        font-size: 24px;
        cursor: pointer;
        color: #64748b;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: all 0.2s;
      ">×</button>
      
      <div style="font-size: 64px; margin-bottom: 16px;">🐬</div>
      <h2 style="
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
        margin: 0 0 12px 0;
        line-height: 1.2;
      ">${esc(copy.title)}</h2>
      <p style="
        font-size: 18px;
        color: #64748b;
        margin: 0 0 24px 0;
        line-height: 1.6;
      ">${String(copy.body || '')}</p>
      <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
        <a href="${esc(subUrl)}" id="pms-popup-cta" style="
          background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
          color: white;
          padding: 14px 28px;
          border-radius: 12px;
          text-decoration: none;
          font-weight: 700;
          font-size: 16px;
          transition: all 0.2s;
          display: inline-block;
          box-shadow: 0 4px 12px rgba(13, 148, 136, 0.35);
        ">${esc(copy.cta)}</a>
        <button type="button" id="pms-popup-close-btn" style="
          background: #f1f5f9;
          color: #64748b;
          padding: 14px 28px;
          border-radius: 12px;
          border: none;
          font-weight: 600;
          font-size: 16px;
          cursor: pointer;
          transition: all 0.2s;
        ">${esc(copy.close)}</button>
      </div>
    `;

    // Añadir estilos de animación
    const style = document.createElement('style');
    style.textContent = `
      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }
      @keyframes slideUp {
        from { 
          opacity: 0;
          transform: translateY(20px);
        }
        to { 
          opacity: 1;
          transform: translateY(0);
        }
      }
      #pms-popup-close:hover {
        background: #f1f5f9;
        color: #0f172a;
      }
      #pms-popup-cta:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(13, 148, 136, 0.45);
      }
      #pms-popup-close-btn:hover {
        background: #e2e8f0;
      }
    `;
    document.head.appendChild(style);

    overlay.appendChild(popup);
    document.body.appendChild(overlay);

    // Event listeners
    const closePopup = function() {
      overlay.style.display = 'none';
      trackEvent('popup_close');
      // Guardar en localStorage que se cerró
      localStorage.setItem('pms_popup_closed', 'true');
    };

    const closeBtn = document.getElementById('pms-popup-close');
    const closeBtn2 = document.getElementById('pms-popup-close-btn');
    const ctaBtn = document.getElementById('pms-popup-cta');
    
    if (closeBtn) closeBtn.addEventListener('click', closePopup);
    if (closeBtn2) closeBtn2.addEventListener('click', closePopup);
    
    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) {
        closePopup();
      }
    });

    if (ctaBtn) {
      ctaBtn.addEventListener('click', function () {
        trackEvent('popup_click', { action: 'subscribe_plans', href: ctaBtn.getAttribute('href') });
      });
    }

    return overlay;
  }

  function showPopup() {
    if (popupShown) return;
    
    // Verificar si ya se cerró antes (localStorage)
    if (localStorage.getItem('pms_popup_closed')) {
      return;
    }

    popupShown = true;
    window.popupShown = true;
    
    let overlay = document.getElementById('pms-popup-overlay');
    if (!overlay) {
      overlay = createPopup();
    }

    overlay.style.display = 'flex';
    trackEvent('popup_view');
  }

  // Mostrar popup después de X segundos
  popupTimer = setTimeout(function() {
    showPopup();
  }, POPUP_DELAY);

  // Limpiar timer si la página se cierra antes
  window.addEventListener('beforeunload', function() {
    if (popupTimer) {
      clearTimeout(popupTimer);
    }
  });

})();
