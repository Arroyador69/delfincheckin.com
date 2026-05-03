#!/usr/bin/env python3
"""Actualiza index.html por idioma: Polar/subscribe, landing-tracking local, bloque #registro sin waitlist."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES: list[tuple[str, str]] = [
    ("index.html", "es"),
    ("en/index.html", "en"),
    ("sv/index.html", "sv"),
    ("fi/index.html", "fi"),
    ("fr/index.html", "fr"),
    ("pt/index.html", "pt"),
    ("it/index.html", "it"),
]


def polar_url(locale: str, plan: str) -> str:
    return (
        "https://admin.delfincheckin.com/api/polar/subscribe-redirect"
        f"?plan={plan}&locale={locale}&seats=1&interval=month"
    )


def subscribe_url(locale: str, source: str = "delfincheckin") -> str:
    return f"https://admin.delfincheckin.com/{locale}/subscribe?source={source}"


def admin_login() -> str:
    return "https://admin.delfincheckin.com/admin-login"


def new_registro_section(locale: str) -> str:
    """HTML reemplazo de <!-- Registro Pre-lanzamiento --> … hasta antes de Formulario de Contacto."""
    sub_block = subscribe_url(locale, "delfincheckin_registro")
    login = admin_login()
    if locale == "es":
        h2 = "Listo para usar: elige plan y contrata en la web"
        p = (
            "El pago recurrente del software se gestiona con <strong>Polar</strong> (checkout seguro). "
            "Tras el pago recibirás un email para completar el onboarding.<br>"
            "¿Quieres el plan <strong>gratis</strong>? Entra en el panel."
        )
        b1 = "Ver planes y pagar (Polar)"
        b2 = "Acceder al panel"
    elif locale == "en":
        h2 = "Ready to use: pick a plan and subscribe on the web"
        p = (
            "Recurring billing runs through <strong>Polar</strong> (secure checkout). "
            "After payment you will get an email to finish onboarding.<br>"
            "Want the <strong>free</strong> plan? Open the dashboard."
        )
        b1 = "View plans & pay (Polar)"
        b2 = "Log in to dashboard"
    elif locale == "sv":
        h2 = "Redo att använda: välj plan och teckna på webben"
        p = (
            "Återkommande betalning sker via <strong>Polar</strong> (säker checkout). "
            "Efter betalning får du e-post för att slutföra onboarding.<br>"
            "Vill du börja med <strong>gratisplanen</strong>? Öppna panelen."
        )
        b1 = "Se planer och betala (Polar)"
        b2 = "Logga in i panelen"
    elif locale == "fi":
        h2 = "Valmis käyttöön: valitse suunnitelma ja tilaa verkossa"
        p = (
            "Toistuva veloitus tapahtuu <strong>Polarilla</strong> (turvallinen kassa). "
            "Maksun jälkeen saat sähköpostin onboardingia varten.<br>"
            "<strong>Ilmainen</strong> suunnitelma: kirjaudu paneeliin."
        )
        b1 = "Katso suunnitelmat ja maksa (Polar)"
        b2 = "Kirjaudu paneeliin"
    elif locale == "fr":
        h2 = "Prêt à l’emploi : choisissez une offre et souscrivez sur le web"
        p = (
            "La facturation récurrente passe par <strong>Polar</strong> (paiement sécurisé). "
            "Après paiement vous recevrez un e-mail pour terminer l’onboarding.<br>"
            "Offre <strong>gratuite</strong> ? Connectez-vous au tableau de bord."
        )
        b1 = "Voir les offres et payer (Polar)"
        b2 = "Connexion au tableau de bord"
    elif locale == "pt":
        h2 = "Pronto a usar: escolha o plano e subscreva na web"
        p = (
            "A faturação recorrente faz-se com <strong>Polar</strong> (checkout seguro). "
            "Após o pagamento recebe email para concluir o onboarding.<br>"
            "Plano <strong>grátis</strong>? Entre no painel."
        )
        b1 = "Ver planos e pagar (Polar)"
        b2 = "Entrar no painel"
    else:  # it
        h2 = "Pronto all’uso: scegli il piano e abbonati sul web"
        p = (
            "La fatturazione ricorrente avviene con <strong>Polar</strong> (checkout sicuro). "
            "Dopo il pagamento riceverai un’email per completare l’onboarding.<br>"
            "Piano <strong>gratuito</strong>? Accedi al pannello."
        )
        b1 = "Vedi piani e paga (Polar)"
        b2 = "Accedi al pannello"

    return f"""    <!-- Contratar / Polar (sin waitlist) -->
    <section id="registro" class="section container" style="background: linear-gradient(135deg, #0d9488 0%, #2563eb 100%); border-radius: 24px; padding: 48px 24px; margin: 64px auto; max-width: 900px; box-shadow: 0 20px 60px rgba(37, 99, 235, 0.25);">
      <div style="text-align: center; color: white; margin-bottom: 24px;">
        <div style="font-size: 56px; margin-bottom: 12px;">🐬</div>
        <h2 style="color: white; margin-bottom: 12px; font-size: 34px; font-weight: 900;">{h2}</h2>
        <p style="color: rgba(255,255,255,0.95); font-size: 18px; line-height: 1.65; max-width: 640px; margin: 0 auto;">{p}</p>
      </div>
      <div class="card" style="background: white; max-width: 560px; margin: 0 auto; padding: 28px; text-align: center;">
        <div style="display: flex; flex-direction: column; gap: 12px;">
          <a class="btn primary" href="{sub_block}" style="display: inline-block; padding: 16px 24px; font-size: 17px; font-weight: 800; background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%); color: white; border-radius: 12px; text-decoration: none;">{b1}</a>
          <a class="btn primary" href="{login}" style="display: inline-block; padding: 14px 24px; font-size: 16px; font-weight: 700; background: #1e293b; color: white; border-radius: 12px; text-decoration: none;">{b2}</a>
        </div>
      </div>
    </section>

"""


def patch_file(rel: str, loc: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")

    text = text.replace(
        "https://admin.delfincheckin.com/landing-tracking.js",
        "/landing-tracking.js",
    )

    # Planes de pago → Polar (mismos gradientes en todos los index)
    text = re.sub(
        r'(<a href=")#registro(" class="btn primary"[^>]*background: linear-gradient\(135deg, #2563eb 0%, #1d4ed8 100%\))',
        rf"\g<1>{polar_url(loc, 'checkin')}\g<2>",
        text,
        count=1,
    )
    text = re.sub(
        r'(<a href=")#registro(" class="btn primary"[^>]*background: linear-gradient\(135deg, #d97706 0%, #b45309 100%\))',
        rf"\g<1>{polar_url(loc, 'standard')}\g<2>",
        text,
        count=1,
    )
    text = re.sub(
        r'(<a href=")#registro(" class="btn primary"[^>]*background: linear-gradient\(135deg, #7c3aed 0%, #5b21b6 100%\))',
        rf"\g<1>{polar_url(loc, 'pro')}\g<2>",
        text,
        count=1,
    )

    sub = subscribe_url(loc, "delfincheckin")
    text = text.replace('href="#registro"', f'href="{sub}"')

    # Sustituir bloque antiguo de pre-lanzamiento / waitlist
    marker_start = "<!-- Registro Pre-lanzamiento -->"
    marker_end = "<!-- Formulario de Contacto -->"
    i0 = text.find(marker_start)
    i1 = text.find(marker_end)
    if i0 == -1 or i1 == -1 or i1 <= i0:
        raise SystemExit(f"No se encontró bloque registro en {rel}")
    text = text[:i0] + new_registro_section(loc) + text[i1:]

    path.write_text(text, encoding="utf-8")
    print("OK", rel)


def main() -> None:
    for rel, loc in FILES:
        patch_file(rel, loc)
    print("Hecho:", len(FILES), "archivos")


if __name__ == "__main__":
    main()
