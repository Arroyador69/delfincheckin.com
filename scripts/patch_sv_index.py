#!/usr/bin/env python3
"""One-off patches for sv/index.html (copied from Spanish root index)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SV = ROOT / "sv" / "index.html"


def main() -> None:
    t = SV.read_text(encoding="utf-8")

    t = t.replace('<html lang="es">', '<html lang="sv">', 1)
    t = t.replace(
        '<link rel="canonical" href="https://delfincheckin.com/">',
        '<link rel="canonical" href="https://delfincheckin.com/sv/">',
        1,
    )
    if 'hreflang="sv"' not in t:
        t = t.replace(
            '<link rel="alternate" hreflang="fi" href="https://delfincheckin.com/fi/">',
            '<link rel="alternate" hreflang="fi" href="https://delfincheckin.com/fi/">'
            '\n  <link rel="alternate" hreflang="sv" href="https://delfincheckin.com/sv/">',
            1,
        )

    t = t.replace('<meta name="language" content="Spanish">', '<meta name="language" content="Swedish">', 1)
    t = t.replace(
        '<meta name="msapplication-starturl" content="/">',
        '<meta name="msapplication-starturl" content="/sv/">',
        1,
    )
    t = t.replace(
        '<meta name="msapplication-tooltip" content="Software de gestión hotelera">',
        '<meta name="msapplication-tooltip" content="Hotell-PMS och incheckning">',
        1,
    )

    t = t.replace(
        "<title>Delfín Check‑in · Software de gestión hotelera y auto check‑in</title>",
        "<title>Delfín Check‑in · Hotell-PMS och digital gästincheckning</title>",
        1,
    )
    t = t.replace(
        '<meta name="description" content="Delfín Check‑in: PMS con registro de viajeros que crea reservas casi solas (revisas y confirmas), facturas y exportación. Plan Pro: reseñas Google y microsite para más reservas directas fuera de Airbnb/Booking. Plan Básico gratuito para primeros usuarios.">',
        '<meta name="description" content="Delfín Check-in: hotell-PMS där resenärsregistrering skapar bokningar åt dig – granska, bekräfta, fakturera och exportera. Pro: Google-recensioner och mikrosajt för fler direktbokningar utanför Airbnb/Booking. Gratis grundplan för tidiga användare.">',
        1,
    )

    t = re.sub(
        r'<meta http-equiv="content-language" content="[^"]*">',
        '<meta http-equiv="content-language" content="sv-SE">',
        t,
        count=1,
    )
    t = re.sub(
        r'<meta property="og:locale" content="[^"]*">',
        '<meta property="og:locale" content="sv_SE">',
        t,
        count=1,
    )
    t = t.replace('property="og:url" content="https://delfincheckin.com/"', 'property="og:url" content="https://delfincheckin.com/sv/"', 1)

    # Language switcher trigger (initial state on /sv/)
    t = t.replace('aria-label="Cambiar idioma"', 'aria-label="Byt språk"', 1)
    t = t.replace(
        '<span id="home-lang-trigger-full" class="hl-desktop">🇪🇸 Español</span>',
        '<span id="home-lang-trigger-full" class="hl-desktop">🇸🇪 Svenska</span>',
        1,
    )
    t = t.replace(
        '<span id="home-lang-trigger-mobile" class="hl-mobile" aria-hidden="true">🇪🇸</span>',
        '<span id="home-lang-trigger-mobile" class="hl-mobile" aria-hidden="true">🇸🇪</span>',
        1,
    )

    # Nav
    t = t.replace(
        '<a class="btn primary" href="#registro">Registro Gratis</a>',
        '<a class="btn primary" href="#registro">Gratis registrering</a>',
        1,
    )
    t = t.replace(
        '<a class="btn" href="#calendario-limpieza" data-es="Calendario limpieza" data-en="Cleaning calendar">Calendario limpieza</a>',
        '<a class="btn" href="#calendario-limpieza" data-es="Calendario limpieza" data-en="Cleaning calendar">Städschema</a>',
        1,
    )
    t = t.replace('<a class="btn" href="#caracteristicas">Funciones</a>', '<a class="btn" href="#caracteristicas">Funktioner</a>', 1)

    old_hero = """      <div class="badges">
        <span class="badge" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); color: #92400e; font-weight: 800;">🚀 Próximamente</span>
        <span class="badge" style="background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); color: #166534; font-weight: 800;">💯 Plan Básico Gratis</span>
        <span class="badge" style="background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); color: #3730a3; font-weight: 800;">👥 De Propietarios para Propietarios</span>
      </div>
      <h1>El software de gestión hotelera (PMS) que siempre quisiste tener. <strong style="color: var(--brand);">Acceso gratuito al plan básico si te apuntas ya.</strong></h1>
      <div style="margin: 18px 0 20px; max-width: 720px; padding: 18px 20px; border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.22); background: linear-gradient(135deg, rgba(238, 242, 255, 0.95) 0%, rgba(240, 253, 250, 0.92) 100%); box-shadow: 0 4px 24px rgba(37, 99, 235, 0.07);" role="note" aria-label="Idea central">
        <p style="margin: 0; font-size: clamp(15px, 2.5vw, 17px); font-weight: 650; color: #1e1b4b; line-height: 1.5;">
          Cada check-in que registras con Delfín Check-in es una oportunidad de fidelizar al huésped y trabajar tu próxima reserva directa.
        </p>
      </div>
      <p style="font-size: 20px; line-height: 1.6;">Estamos construyendo el sistema de gestión para hoteles, hostales y alojamientos vacacionales hecho <strong>por propietarios, para propietarios</strong>. Sin complicaciones, sin costes ocultos. <strong style="color: var(--accent);">⚠️ Importante: Los primeros en apuntarse tendrán acceso permanente al Plan Básico sin coste mensual. Regístrate ahora antes de que se agoten las plazas.</strong></p>
      <div style="margin: 16px 0; padding: 14px 18px; background: #f8fafc; border: 1px solid var(--border); border-radius: 12px;">
        <p style="margin: 0; color: var(--muted); font-size: 13px; line-height: 1.55;">
          <strong style="color: var(--text);">Prueba sin riesgo:</strong> el plan gratuito no pide tarjeta. Úsalo todo el tiempo que quieras; si te encaja el producto, podrás pasar a un plan de pago cuando lo necesites.
        </p>
      </div>
      <div style="margin: 20px 0; padding: 16px; background: rgba(68,192,255,0.1); border-left: 4px solid var(--brand); border-radius: 8px;">
        <p style="margin: 0; color: var(--muted); font-size: 14px; line-height: 1.6;">
          <strong style="color: var(--brand);">ℹ️ Nota:</strong> El producto está en constante evolución. Las funcionalidades incluidas en cada plan pueden evolucionar con el tiempo, manteniendo siempre la existencia de un plan gratuito sin coste.
        </p>
      </div>
      <div class="hero-card" style="background: linear-gradient(135deg, rgba(68,192,255,0.1) 0%, rgba(124,240,124,0.1) 100%); border: 2px solid rgba(68,192,255,0.3);">
        <div style="text-align: center; margin-bottom: 20px;">
          <h2 style="margin: 0 0 10px; font-size: 24px; color: var(--brand);">🎯 Todo lo que necesitas, en un solo lugar</h2>
          <p style="color: var(--muted); margin: 0;">Desarrollado por propietarios que conocen tus necesidades reales</p>
        </div>
        <div class="checklist">
          <div class="check"><i>✔</i> <strong>Motor de reservas</strong> - Gestiona tus reservas desde un panel intuitivo</div>
          <div class="check"><i>✔</i> <strong>6 idiomas</strong> - Español, francés, inglés, italiano, portugués y finés en el panel</div>
          <div class="check"><i>✔</i> <strong>Check-in digital</strong> - Envío al Ministerio del Interior (desde 2€/mes + 2€/propiedad)</div>
          <div class="check"><i>✔</i> <strong>App móvil</strong> - iOS y Android en desarrollo (próximamente)</div>
          <div class="check"><i>✔</i> <strong>Exportación de datos</strong> - CSV/Excel para contabilidad</div>
          <div class="check"><i>✔</i> <strong>Plan Básico Gratis</strong> - Acceso sin coste mensual, financiado con anuncios discretos</div>
        </div>
      </div>
      
      <!-- Badges de confianza -->
      <div style="display: flex; justify-content: center; align-items: center; gap: 24px; margin-top: 20px; flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 20px; font-size: 14px; font-weight: 600; color: #2563eb;">
          <span>🔒</span>
          <span>SSL Seguro</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 20px; font-size: 14px; font-weight: 600; color: #16a34a;">
          <span>🛡️</span>
          <span>RGPD Compliant</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: #fef3c7; border: 1px solid #fde68a; border-radius: 20px; font-size: 14px; font-weight: 600; color: #d97706;">
          <span>⭐</span>
          <span>4.8/5 Valoración</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: #f3e8ff; border: 1px solid #c4b5fd; border-radius: 20px; font-size: 14px; font-weight: 600; color: #7c3aed;">
          <span>🚀</span>
          <span>99.9% Uptime</span>
        </div>
      </div>"""

    new_hero = """      <div class="badges">
        <span class="badge" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); color: #92400e; font-weight: 800;">🚀 Kommer snart</span>
        <span class="badge" style="background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); color: #166534; font-weight: 800;">💯 Gratis grundplan</span>
        <span class="badge" style="background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); color: #3730a3; font-weight: 800;">👥 Av värdar, för värdar</span>
      </div>
      <h1>Hotell-PMS du alltid velat ha. <strong style="color: var(--brand);">Gratis grundplan om du registrerar dig nu.</strong></h1>
      <div style="margin: 18px 0 20px; max-width: 720px; padding: 18px 20px; border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.22); background: linear-gradient(135deg, rgba(238, 242, 255, 0.95) 0%, rgba(240, 253, 250, 0.92) 100%); box-shadow: 0 4px 24px rgba(37, 99, 235, 0.07);" role="note" aria-label="Kärnbudskap">
        <p style="margin: 0; font-size: clamp(15px, 2.5vw, 17px); font-weight: 650; color: #1e1b4b; line-height: 1.5;">
          Varje incheckning du loggar i Delfín Check-in är en chans att stärka relationen med gästen och jobba mot nästa direktbokning.
        </p>
      </div>
      <p style="font-size: 20px; line-height: 1.6;">Vi bygger ett system för hotell, vandrarhem och semesterboenden <strong>av ägare, för ägare</strong>. Utan krångel, utan dolda avgifter. <strong style="color: var(--accent);">⚠️ Viktigt: De första som registrerar sig får permanent tillgång till grundplanen utan månadskostnad. Registrera dig nu innan platserna tar slut.</strong></p>
      <div style="margin: 16px 0; padding: 14px 18px; background: #f8fafc; border: 1px solid var(--border); border-radius: 12px;">
        <p style="margin: 0; color: var(--muted); font-size: 13px; line-height: 1.55;">
          <strong style="color: var(--text);">Prova riskfritt:</strong> den gratis planen kräver inget kort. Använd den så länge du vill; när du vill ha mer kan du gå vidare till en betalplan.
        </p>
      </div>
      <div style="margin: 20px 0; padding: 16px; background: rgba(68,192,255,0.1); border-left: 4px solid var(--brand); border-radius: 8px;">
        <p style="margin: 0; color: var(--muted); font-size: 14px; line-height: 1.6;">
          <strong style="color: var(--brand);">ℹ️ Obs:</strong> Produkten utvecklas hela tiden. Funktionerna i varje plan kan förändras över tid, men en gratisplan kommer alltid att finnas.
        </p>
      </div>
      <div class="hero-card" style="background: linear-gradient(135deg, rgba(68,192,255,0.1) 0%, rgba(124,240,124,0.1) 100%); border: 2px solid rgba(68,192,255,0.3);">
        <div style="text-align: center; margin-bottom: 20px;">
          <h2 style="margin: 0 0 10px; font-size: 24px; color: var(--brand);">🎯 Allt du behöver på ett ställe</h2>
          <p style="color: var(--muted); margin: 0;">Byggt av värdar som förstår vad du verkligen behöver</p>
        </div>
        <div class="checklist">
          <div class="check"><i>✔</i> <strong>Bokningsmotor</strong> – Hantera bokningar från en tydlig översikt</div>
          <div class="check"><i>✔</i> <strong>7 språk</strong> – Spanska, franska, engelska, italienska, portugisiska, finska och svenska i panelen</div>
          <div class="check"><i>✔</i> <strong>Digital incheckning</strong> – Inlämning till inrikesministeriet (från 2 €/mån + 2 €/fastighet)</div>
          <div class="check"><i>✔</i> <strong>Mobilapp</strong> – iOS och Android under utveckling (kommer snart)</div>
          <div class="check"><i>✔</i> <strong>Dataexport</strong> – CSV/Excel för bokföring</div>
          <div class="check"><i>✔</i> <strong>Gratis grundplan</strong> – Ingen månadskostnad, finansieras med diskreta annonser</div>
        </div>
      </div>
      
      <!-- Badges de confianza -->
      <div style="display: flex; justify-content: center; align-items: center; gap: 24px; margin-top: 20px; flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 20px; font-size: 14px; font-weight: 600; color: #2563eb;">
          <span>🔒</span>
          <span>Säker SSL</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 20px; font-size: 14px; font-weight: 600; color: #16a34a;">
          <span>🛡️</span>
          <span>GDPR-redo</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: #fef3c7; border: 1px solid #fde68a; border-radius: 20px; font-size: 14px; font-weight: 600; color: #d97706;">
          <span>⭐</span>
          <span>4,8/5 i betyg</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: #f3e8ff; border: 1px solid #c4b5fd; border-radius: 20px; font-size: 14px; font-weight: 600; color: #7c3aed;">
          <span>🚀</span>
          <span>99,9 % drifttid</span>
        </div>
      </div>"""

    if old_hero not in t:
        raise SystemExit("hero block not found — index.html layout changed")
    t = t.replace(old_hero, new_hero, 1)

    SV.write_text(t, encoding="utf-8")
    print("Patched", SV)


if __name__ == "__main__":
    main()
