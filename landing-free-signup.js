(function () {
  'use strict';

  var API = 'https://admin.delfincheckin.com/api/public/signup-free';
  var SUPPORT = 'contacto@delfincheckin.com';

  function lang() {
    var l = (document.documentElement.getAttribute('lang') || 'es').toLowerCase().split('-')[0];
    var ok = ['es', 'en', 'fr', 'it', 'pt', 'fi', 'sv'];
    return ok.indexOf(l) >= 0 ? l : 'es';
  }

  var COPY = {
    es: {
      sending: 'Enviando…',
      invalid: 'Introduce un email válido.',
      error: 'No se pudo completar el registro. Inténtalo más tarde.',
      success:
        '<strong>¡Revisa tu correo!</strong> Te hemos enviado el enlace para <strong>entrar al sistema</strong> y completar el onboarding. En unos <strong>2 minutos</strong> puedes estar usándolo.<br><br>Si no lo ves, busca en <strong>spam, correo no deseado o promociones</strong>. ¿Nada? Escríbenos a <a href="mailto:' +
        SUPPORT +
        '">' +
        SUPPORT +
        '</a>.',
      cta: 'Empezar ahora — es gratis',
      popupCta: 'Probar ahora con mi email',
    },
    en: {
      sending: 'Sending…',
      invalid: 'Please enter a valid email.',
      error: 'Could not complete signup. Please try again later.',
      success:
        '<strong>Check your inbox!</strong> We sent you the link to <strong>access the system</strong> and finish onboarding. In about <strong>2 minutes</strong> you can be up and running.<br><br>If you do not see it, check <strong>spam or junk</strong>. Still nothing? Email us at <a href="mailto:' +
        SUPPORT +
        '">' +
        SUPPORT +
        '</a>.',
      cta: 'Start now — it\'s free',
      popupCta: 'Try now with my email',
    },
    fr: {
      sending: 'Envoi en cours…',
      invalid: 'Entrez une adresse e-mail valide.',
      error: 'Inscription impossible. Réessayez plus tard.',
      success:
        '<strong>Vérifiez votre boîte mail !</strong> Nous vous avons envoyé le lien pour <strong>accéder au système</strong>. Environ <strong>2 minutes</strong> pour être opérationnel.<br><br>Sinon, regardez les <strong>courriers indésirables</strong>. Rien ? Écrivez à <a href="mailto:' +
        SUPPORT +
        '">' +
        SUPPORT +
        '</a>.',
      cta: 'Commencer maintenant — gratuit',
      popupCta: 'Essayer avec mon e-mail',
    },
    it: {
      sending: 'Invio in corso…',
      invalid: 'Inserisci un\'email valida.',
      error: 'Registrazione non riuscita. Riprova più tardi.',
      success:
        '<strong>Controlla la posta!</strong> Ti abbiamo inviato il link per <strong>entrare nel sistema</strong>. In circa <strong>2 minuti</strong> puoi iniziare.<br><br>Controlla anche <strong>spam</strong>. Niente? Scrivi a <a href="mailto:' +
        SUPPORT +
        '">' +
        SUPPORT +
        '</a>.',
      cta: 'Inizia ora — è gratis',
      popupCta: 'Prova ora con la mia email',
    },
    pt: {
      sending: 'A enviar…',
      invalid: 'Introduza um email válido.',
      error: 'Não foi possível concluir o registo. Tente mais tarde.',
      success:
        '<strong>Verifique o email!</strong> Enviámos o link para <strong>entrar no sistema</strong>. Em cerca de <strong>2 minutos</strong> pode estar a usar.<br><br>Veja também <strong>spam ou lixo</strong>. Nada? <a href="mailto:' +
        SUPPORT +
        '">' +
        SUPPORT +
        '</a>.',
      cta: 'Começar agora — grátis',
      popupCta: 'Experimentar com o meu email',
    },
    fi: {
      sending: 'Lähetetään…',
      invalid: 'Anna kelvollinen sähköposti.',
      error: 'Rekisteröinti epäonnistui. Yritä myöhemmin.',
      success:
        '<strong>Tarkista sähköposti!</strong> Lähetimme linkin <strong>järjestelmään</strong>. Noin <strong>2 minuutissa</strong> voit aloittaa.<br><br>Tarkista myös <strong>roskaposti</strong>. Ei mitään? <a href="mailto:' +
        SUPPORT +
        '">' +
        SUPPORT +
        '</a>.',
      cta: 'Aloita nyt — ilmainen',
      popupCta: 'Kokeile sähköpostillani',
    },
    sv: {
      sending: 'Skickar…',
      invalid: 'Ange en giltig e-postadress.',
      error: 'Registreringen misslyckades. Försök igen senare.',
      success:
        '<strong>Kolla din e-post!</strong> Vi skickade länken för att <strong>logga in i systemet</strong>. På cirka <strong>2 minuter</strong> kan du vara igång.<br><br>Kolla även <strong>skräppost</strong>. Inget? <a href="mailto:' +
        SUPPORT +
        '">' +
        SUPPORT +
        '</a>.',
      cta: 'Börja nu — gratis',
      popupCta: 'Prova med min e-post',
    },
  };

  function t(key) {
    var L = COPY[lang()] || COPY.es;
    return L[key] || COPY.es[key];
  }

  function validEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
  }

  function showMsg(el, html, ok) {
    if (!el) return;
    el.innerHTML = html;
    el.classList.remove('is-success', 'is-error');
    el.classList.add(ok ? 'is-success' : 'is-error');
    el.style.display = 'block';
  }

  async function submitSignup(email, locale, name) {
    var body = { email: email, locale: locale || lang() };
    if (name) body.name = name;
    var res = await fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    var data = {};
    try {
      data = await res.json();
    } catch (e) {}
    if (!res.ok || data.success === false) {
      throw new Error((data && data.error) || t('error'));
    }
    return data;
  }

  function wireMainForm() {
    var form = document.getElementById('landingFreeSignupForm');
    if (!form || form.dataset.delfinWired === '1') return;
    form.dataset.delfinWired = '1';

    var emailEl = document.getElementById('landingFreeSignupEmail');
    var nameEl = document.getElementById('landingFreeSignupName');
    var btn = document.getElementById('landingFreeSignupSubmit');
    var btnText = document.getElementById('landingFreeSignupSubmitText');
    var btnLoad = document.getElementById('landingFreeSignupLoading');
    var msg = document.getElementById('landingFreeSignupMessage');
    var locale = form.getAttribute('data-signup-locale') || lang();

    if (btnText) btnText.textContent = t('cta');

    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      var v = String((emailEl && emailEl.value) || '').trim();
      if (!validEmail(v)) {
        showMsg(msg, t('invalid'), false);
        return;
      }
      if (btn) btn.disabled = true;
      if (btnText) btnText.style.display = 'none';
      if (btnLoad) btnLoad.style.display = 'inline';
      showMsg(msg, t('sending'), true);
      try {
        await submitSignup(v, locale, nameEl ? String(nameEl.value || '').trim() : '');
        showMsg(msg, t('success'), true);
        trackLanding('form_submit', { form_id: 'landing_free_signup' });
        form.reset();
      } catch (err) {
        showMsg(msg, String(err.message || t('error')), false);
      } finally {
        if (btn) btn.disabled = false;
        if (btnText) btnText.style.display = 'inline';
        if (btnLoad) btnLoad.style.display = 'none';
      }
    });
  }

  function wirePopupForm() {
    var btn = document.getElementById('delfin-popup-submit');
    var emailEl = document.getElementById('delfin-popup-email');
    var msg = document.getElementById('delfin-popup-msg');
    if (!btn || !emailEl || btn.dataset.delfinWired === '1') return;
    btn.dataset.delfinWired = '1';
    btn.textContent = t('popupCta');

    btn.addEventListener('click', async function () {
      var v = String(emailEl.value || '').trim();
      if (!validEmail(v)) {
        msg.innerHTML = t('invalid');
        msg.className = 'is-error';
        msg.style.display = 'block';
        return;
      }
      btn.disabled = true;
      msg.innerHTML = t('sending');
      msg.className = '';
      msg.style.display = 'block';
      try {
        await submitSignup(v, lang(), '');
        msg.innerHTML = t('success');
        msg.className = 'is-success';
        trackLanding('popup_click', { source: 'email_capture', action: 'signup_success' });
        emailEl.value = '';
      } catch (err) {
        msg.innerHTML = String(err.message || t('error'));
        msg.className = 'is-error';
      } finally {
        btn.disabled = false;
      }
    });
  }

  function trackLanding(eventType, data) {
    try {
      if (typeof window.delfinLandingTrack === 'function') {
        window.delfinLandingTrack(eventType, data || {});
      }
    } catch (e) {}
  }

  function wirePopupToggle() {
    var overlay = document.getElementById('delfin-soft-popup-overlay');
    if (!overlay || overlay.dataset.delfinWired === '1') return;
    overlay.dataset.delfinWired = '1';

    var closeBtn = document.getElementById('delfin-soft-popup-close');
    var laterBtn = document.getElementById('delfin-soft-popup-later');
    var scrollBtn = document.getElementById('delfin-soft-popup-scroll');

    function safeGet(k) {
      try {
        return localStorage.getItem(k);
      } catch (e) {
        return null;
      }
    }
    function safeSet(k, v) {
      try {
        localStorage.setItem(k, v);
      } catch (e) {}
    }

    var KEY = 'delfin_landing_soft_popup_last';
    var last = Number(safeGet(KEY) || '0');
    if (last && Date.now() - last < 604800000) return;

    function close() {
      overlay.style.display = 'none';
      safeSet(KEY, String(Date.now()));
      trackLanding('popup_close', { source: 'email_capture' });
    }
    function open() {
      overlay.style.display = 'flex';
      window.popupShown = true;
      trackLanding('popup_view', { source: 'email_capture' });
      var inp = document.getElementById('delfin-popup-email');
      if (inp) setTimeout(function () {
        inp.focus();
      }, 200);
    }

    if (closeBtn) closeBtn.addEventListener('click', close);
    if (laterBtn) laterBtn.addEventListener('click', close);
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) close();
    });
    if (scrollBtn) {
      scrollBtn.addEventListener('click', function (e) {
        e.preventDefault();
        close();
        var reg = document.getElementById('registro');
        if (reg) reg.scrollIntoView({ behavior: 'smooth', block: 'start' });
        var mainEmail = document.getElementById('landingFreeSignupEmail');
        if (mainEmail) setTimeout(function () {
          mainEmail.focus();
        }, 400);
      });
    }

    setTimeout(open, 8000);
  }

  function init() {
    wireMainForm();
    wirePopupForm();
    wirePopupToggle();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
