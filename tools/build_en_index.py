#!/usr/bin/env python3
"""
Genera en/index.html a partir de index.html (ES): metadatos EN, selector EN activo,
sustituciones de copy y bloque FAQ en inglés.

Ejecutar desde la raíz del repo:
  python3 tools/build_en_index.py
"""
from __future__ import annotations

import html as html_module
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
SRC = ROOT / "index.html"
DST_DIR = ROOT / "en"
DST = DST_DIR / "index.html"
FAQ_EN = TOOLS / "faq_section_en.html"
FAQ_MAINENTITY_EN = TOOLS / "faq_mainentity_en.json"


def head_and_switch(text: str) -> str:
    """Metadatos y selector de idioma para la versión EN."""
    pairs = [
        ('<html lang="es">', '<html lang="en">'),
        (
            '<link rel="canonical" href="https://delfincheckin.com/">',
            '<link rel="canonical" href="https://delfincheckin.com/en/">',
        ),
        (
            "<title>Delfín Check‑in · Software de gestión hotelera y auto check‑in</title>",
            "<title>Delfín Check-in · Hotel PMS &amp; guest check-in software</title>",
        ),
        (
            'content="Delfín Check‑in: software de gestión hotelera (PMS) con Plan Básico gratuito. Reservas, gestión de habitaciones y panel de administración. Acceso permanente al plan básico sin coste mensual para primeros usuarios."',
            'content="Delfín Check-in: hotel PMS with a free Basic plan. Reservations, rooms, admin panel and guest check-in. Permanent free basic access for early users. Built for Spain; UI in 5 languages."',
        ),
        (
            'content="Software de gestión hotelera (PMS) con Plan Básico gratuito. Planes Check-in (2€+2€/prop), Standard (9,99€/mes) y Pro (29,99€/mes). Envío automático al Ministerio del Interior. Regístrate ahora."',
            'content="Hotel PMS with a free Basic plan. Check-in (€2/mo + €2/property), Standard (€9.99/mo) and Pro (€29.99/mo). Automatic submission to the Spanish Ministry of the Interior. Sign up now."',
        ),
        ('<meta property="og:url" content="https://delfincheckin.com/">', '<meta property="og:url" content="https://delfincheckin.com/en/">'),
        ('<meta property="og:locale" content="es_ES">', '<meta property="og:locale" content="en_GB">'),
        (
            'content="Software de gestión hotelera (PMS) con Plan Básico gratuito. Planes Check-in (2€+2€/prop), Standard (9,99€/mes), Pro (29,99€/mes). Envío automático MIR. Regístrate ahora."',
            'content="Hotel PMS with free Basic plan. Check-in, Standard and Pro. MIR submission. Sign up now."',
        ),
        (
            'content="Software de gestión hotelera (PMS) con Plan Básico gratuito. Planes Check-in (2€+2€/prop), Standard (9,99€/mes), Pro (29,99€/mes). Envío automático al Ministerio del Interior."',
            'content="Hotel PMS with free Basic plan. Paid plans with Ministry of the Interior submission for Spain."',
        ),
        (
            'content="Delfín Check-in es un software de gestión hotelera (PMS) con Plan Básico gratuito. Los primeros usuarios tienen acceso permanente sin coste mensual. Incluye gestión de reservas, habitaciones, exportación de datos y panel de administración. El módulo de check-in digital con envío al Ministerio del Interior cuesta 2€/mes."',
            'content="Delfín Check-in is a hotel PMS with a free Basic plan. Early users keep permanent free basic access. Includes reservations, rooms, exports and admin panel. Digital check-in with Ministry submission is €2/month."',
        ),
        ('<meta http-equiv="content-language" content="es-ES">', '<meta http-equiv="content-language" content="en">'),
        ('<meta name="language" content="Spanish">', '<meta name="language" content="English">', 2),
        (
            '<meta name="keywords" content="software hotel, PMS gratis, reservas, gestión de hoteles, motor de reservas, sistema hotelero, gestión de alojamientos, reservas online, panel administración hotel, software gestión hotelera España, sistema reservas hoteles, gestión habitaciones hotel, software hotelero profesional, sistema gestión alojamientos turísticos, plataforma hotelera, software para hostales, gestión reservas hoteles, software hotelero completo, gestión hotelera digital, sistema reservas alojamientos, software gestión turística, plataforma gestión hotelera, sistema hotelero integrado, software para hoteles pequeños, gestión digital hoteles">',
            '<meta name="keywords" content="hotel PMS, free PMS, hotel software, booking engine, property management Spain, guest check-in, MIR, Ministry Interior, hostel software, vacation rental, hotel reservations, small hotel PMS">',
        ),
        (
            '<meta property="og:title" content="Delfín Check‑in · Software de gestión hotelera y auto check‑in">',
            '<meta property="og:title" content="Delfín Check-in · Hotel PMS &amp; guest check-in software">',
        ),
        (
            '<meta name="twitter:title" content="Delfín Check‑in · Software de gestión hotelera y auto check‑in">',
            '<meta name="twitter:title" content="Delfín Check-in · Hotel PMS &amp; guest check-in software">',
        ),
        (
            '<meta name="twitter:description" content="Software de gestión hotelera (PMS) con Plan Básico gratuito. Planes Check-in (2€+2€/prop), Standard (9,99€/mes) y Pro (29,99€/mes). Envío automático MIR. Regístrate ahora.">',
            '<meta name="twitter:description" content="Hotel PMS with a free Basic plan. Check-in, Standard and Pro. Automatic MIR (Ministry) submission for Spain. Sign up now.">',
        ),
        (
            '<meta property="og:image:alt" content="Delfín Check-in - Software de gestión hotelera">',
            '<meta property="og:image:alt" content="Delfín Check-in — hotel PMS and guest check-in">',
        ),
        (
            '<meta name="twitter:image:alt" content="Delfín Check-in - Software de gestión hotelera">',
            '<meta name="twitter:image:alt" content="Delfín Check-in — hotel PMS and guest check-in">',
        ),
        (
            '<meta name="msapplication-tooltip" content="Software de gestión hotelera">',
            '<meta name="msapplication-tooltip" content="Hotel PMS &amp; check-in">',
        ),
        ('<meta name="msapplication-starturl" content="/">', '<meta name="msapplication-starturl" content="/en/">'),
        (
            '<meta name="abstract" content="Software de gestión hotelera (PMS) con Plan Básico gratuito. Planes Check-in (2€+2€/prop), Standard (9,99€/mes), Pro (29,99€/mes). Envío automático al Ministerio del Interior.">',
            '<meta name="abstract" content="Hotel PMS with a free Basic plan. Check-in, Standard and Pro. Automatic submission to the Spanish Ministry of the Interior.">',
        ),
        (
            '<meta name="topic" content="Software de gestión hotelera, PMS, sistema de reservas, check-in digital">',
            '<meta name="topic" content="Hotel PMS, reservations, digital check-in, Spain MIR">',
        ),
        (
            '<meta name="classification" content="Software, Gestión Hotelera, PMS, Sistema de Reservas">',
            '<meta name="classification" content="Software, Hotel Management, PMS, Reservations">',
        ),
        (
            '<meta name="DC.title" content="Delfín Check-in - Software de gestión hotelera gratuito">',
            '<meta name="DC.title" content="Delfín Check-in — free hotel PMS">',
        ),
        (
            '<meta name="news_keywords" content="software hotel, PMS gratis, gestión hotelera, check-in digital, reservas online">',
            '<meta name="news_keywords" content="hotel software, free PMS, hotel management, digital check-in, online bookings">',
        ),
        ('<meta name="article:tag" content="PMS gratis">', '<meta name="article:tag" content="free PMS">'),
        ('<meta name="article:tag" content="gestión hotelera">', '<meta name="article:tag" content="hotel management">'),
        ('<meta name="article:tag" content="check-in digital">', '<meta name="article:tag" content="digital check-in">'),
        ('<meta name="article:tag" content="reservas online">', '<meta name="article:tag" content="online bookings">'),
    ]
    for item in pairs:
        if len(item) == 3:
            old, new, n = item
            text = text.replace(old, new, n)
        else:
            old, new = item
            text = text.replace(old, new, 1)

    # Selector: EN activo
    text = text.replace(
        '<a href="/" class="lang-switch__btn lang-switch__btn--active"',
        '<a href="/" class="lang-switch__btn"',
        1,
    )
    text = text.replace(
        '<a href="/en/" class="lang-switch__btn"',
        '<a href="/en/" class="lang-switch__btn lang-switch__btn--active"',
        1,
    )
    return text


def _find_matching_close_tag(html: str, tag: str, start: int) -> tuple[int, int] | None:
    tag_l = tag.lower()
    open_re = re.compile(rf"<{re.escape(tag_l)}(\s[^>]*)?>", re.IGNORECASE)
    close_re = re.compile(rf"</{re.escape(tag_l)}\s*>", re.IGNORECASE)
    pos = start
    depth = 1
    while depth > 0 and pos < len(html):
        m_close = close_re.search(html, pos)
        m_open = open_re.search(html, pos)
        if not m_close:
            return None
        if m_open and m_open.start() < m_close.start():
            depth += 1
            pos = m_open.end()
        else:
            depth -= 1
            if depth == 0:
                return (m_close.start(), m_close.end())
            pos = m_close.end()
    return None


def _gt_after_attributes(html: str, pos: int) -> int:
    """Después del cierre de un valor entre comillas, encuentra el '>' que cierra el tag (no uno dentro de otra comilla)."""
    i = pos
    n = len(html)
    while i < n:
        while i < n and html[i] in " \t\n\r":
            i += 1
        if i < n and html[i] == ">":
            return i
        if i >= n:
            break
        eq = html.find("=", i)
        if eq < 0:
            return html.find(">", pos)
        if eq + 1 < n and html[eq + 1] == '"':
            q2 = html.find('"', eq + 2)
            if q2 < 0:
                return html.find(">", pos)
            i = q2 + 1
        else:
            i = eq + 2
    return html.find(">", pos)


def swap_data_en_attributes(html: str) -> str:
    """Sustituye el texto visible por data-en y elimina data-es/data-en del tag de apertura."""
    pos = 0
    out: list[str] = []
    while True:
        j = html.find('data-en="', pos)
        if j == -1:
            out.append(html[pos:])
            return "".join(out)
        lt = html.rfind("<", 0, j)
        if lt < 0:
            pos = j + 1
            continue
        out.append(html[pos:lt])
        q = j + len('data-en="')
        en_chars: list[str] = []
        while q < len(html) and html[q] != '"':
            en_chars.append(html[q])
            q += 1
        if q >= len(html):
            out.append(html[j:])
            return "".join(out)
        en_html = html_module.unescape("".join(en_chars))
        q += 1
        gt = _gt_after_attributes(html, q)
        if gt < 0:
            out.append(html[j:])
            return "".join(out)
        open_snip = html[lt : gt + 1]
        mm = re.match(r"<([a-zA-Z][\w-]*)", open_snip)
        if not mm:
            pos = j + 1
            continue
        tag = mm.group(1).lower()
        void_tags = frozenset(
            {"meta", "link", "img", "br", "input", "hr", "source", "area", "base", "col", "embed", "wbr"}
        )
        if tag in void_tags:
            pos = j + 1
            continue
        inner_start = gt + 1
        bounds = _find_matching_close_tag(html, tag, inner_start)
        if bounds is None:
            pos = j + 1
            continue
        close_start, close_end = bounds
        cleaned_open = re.sub(r'\s+data-es="[^"]*"', "", open_snip)
        cleaned_open = re.sub(r'\s+data-en="[^"]*"', "", cleaned_open)
        out.append(cleaned_open)
        out.append(en_html)
        out.append(html[close_start:close_end])
        pos = close_end


def swap_data_en_placeholders(html: str) -> str:
    return re.sub(
        r'placeholder="[^"]*"\s+data-es-placeholder="[^"]*"\s+data-en-placeholder="([^"]*)"',
        r'placeholder="\1"',
        html,
    )


def _patch_ld_graph_en(data: dict, faq_main: list) -> None:
    for node in data["@graph"]:
        t = node.get("@type")
        if t == "Organization":
            node["description"] = (
                "Hotel PMS and guest check-in software for hotels and holiday accommodations in Spain."
            )
        elif t == "SoftwareApplication":
            node["@id"] = "https://delfincheckin.com/en/#software"
            node["url"] = "https://delfincheckin.com/en/"
            node["description"] = (
                "Hotel PMS with a free Basic plan. Check-in (€2/mo + €2/property), Standard (€9.99/mo) "
                "and Pro (€29.99/mo). Automatic submission to the Spanish Ministry of the Interior."
            )
            node["offers"][0]["name"] = "Free (Basic) plan"
            node["offers"][0]["description"] = "Basic plan with no monthly fee for early users"
            node["offers"][0]["priceSpecification"]["unitText"] = "no monthly fee"
            node["featureList"] = [
                "Reservation management",
                "Interface in 5 languages (Spanish, French, English, Italian, Portuguese)",
                "Administration panel",
                "Invoices and receipts as PDF",
                "Mobile app iOS and Android",
                "Calendar integration",
                "Technical support",
            ]
        elif t == "WebPage":
            node["@id"] = "https://delfincheckin.com/en/#webpage"
            node["url"] = "https://delfincheckin.com/en/"
            node["name"] = "Delfín Check-in · Hotel PMS & guest check-in software"
            node["description"] = (
                "Hotel PMS with a free Basic plan. Check-in, Standard and Pro. "
                "Automatic MIR (Ministry) submission for Spain."
            )
            node["breadcrumb"]["itemListElement"][0]["name"] = "Home"
            node["breadcrumb"]["itemListElement"][0]["item"] = "https://delfincheckin.com/en/"
        elif t == "FAQPage":
            node["@id"] = "https://delfincheckin.com/en/#faq"
            node["mainEntity"] = faq_main


def replace_ld_json_script(html: str, source_html: str) -> str:
    marker = '<script type="application/ld+json">'
    si = source_html.find(marker)
    if si < 0:
        return html
    brace_start = source_html.find("{", si)
    depth = 0
    i = brace_start
    while i < len(source_html):
        if source_html[i] == "{":
            depth += 1
        elif source_html[i] == "}":
            depth -= 1
            if depth == 0:
                brace_end = i + 1
                break
        i += 1
    else:
        return html
    data = json.loads(source_html[brace_start:brace_end])
    faq_main = json.loads(FAQ_MAINENTITY_EN.read_text(encoding="utf-8"))
    _patch_ld_graph_en(data, faq_main)
    dumped = json.dumps(data, ensure_ascii=False, indent=2)
    indented = "\n".join(("  " + line) if line else "" for line in dumped.split("\n"))

    si2 = html.find(marker)
    if si2 < 0:
        return html
    bs = html.find("{", si2)
    depth = 0
    i = bs
    while i < len(html):
        if html[i] == "{":
            depth += 1
        elif html[i] == "}":
            depth -= 1
            if depth == 0:
                be = i + 1
                return html[:bs] + indented + html[be:]
        i += 1
    return html


# Sustituciones de cuerpo (orden: se re-ordenan por longitud descendente al aplicar)
REPLACEMENTS: list[tuple[str, str]] = [
    (
        "El software de gestión hotelera (PMS) que siempre quisiste tener. <strong style=\"color: var(--brand);\">Acceso gratuito al plan básico si te apuntas ya.</strong>",
        "The hotel PMS you always wished you had. <strong style=\"color: var(--brand);\">Free basic plan if you sign up now.</strong>",
    ),
    (
        "Estamos construyendo el sistema de gestión para hoteles, hostales y alojamientos vacacionales hecho <strong>por propietarios, para propietarios</strong>. Sin complicaciones, sin costes ocultos. <strong style=\"color: var(--accent);\">⚠️ Importante: Los primeros en apuntarse tendrán acceso permanente al Plan Básico sin coste mensual. Regístrate ahora antes de que se agoten las plazas.</strong>",
        "We are building property management for hotels, hostels and holiday rentals <strong>by owners, for owners</strong>. No fuss, no hidden fees. <strong style=\"color: var(--accent);\">⚠️ Important: the first to sign up get permanent Basic plan access with no monthly fee. Register now before spots run out.</strong>",
    ),
    (
        "<strong style=\"color: var(--brand);\">ℹ️ Nota:</strong> El producto está en constante evolución. Las funcionalidades incluidas en cada plan pueden evolucionar con el tiempo, manteniendo siempre la existencia de un plan gratuito sin coste.",
        "<strong style=\"color: var(--brand);\">ℹ️ Note:</strong> The product keeps evolving. Features in each plan may change over time, but a free plan will always exist.",
    ),
    (
        "<h2 style=\"margin: 0 0 10px; font-size: 24px; color: var(--brand);\">🎯 Todo lo que necesitas, en un solo lugar</h2>",
        "<h2 style=\"margin: 0 0 10px; font-size: 24px; color: var(--brand);\">🎯 Everything you need in one place</h2>",
    ),
    (
        "<p style=\"color: var(--muted); margin: 0;\">Desarrollado por propietarios que conocen tus necesidades reales</p>",
        "<p style=\"color: var(--muted); margin: 0;\">Built by owners who understand what you really need</p>",
    ),
    (
        "<div class=\"check\"><i>✔</i> <strong>Motor de reservas</strong> - Gestiona tus reservas desde un panel intuitivo</div>",
        "<div class=\"check\"><i>✔</i> <strong>Booking engine</strong> — Manage reservations from an intuitive panel</div>",
    ),
    (
        "<div class=\"check\"><i>✔</i> <strong>5 idiomas</strong> - Español, francés, inglés, italiano y portugués en el panel</div>",
        "<div class=\"check\"><i>✔</i> <strong>5 languages</strong> — Spanish, French, English, Italian and Portuguese in the panel</div>",
    ),
    (
        "<div class=\"check\"><i>✔</i> <strong>Check-in digital</strong> - Envío al Ministerio del Interior (desde 2€/mes + 2€/propiedad)</div>",
        "<div class=\"check\"><i>✔</i> <strong>Digital check-in</strong> — Ministry of the Interior submission (from €2/mo + €2/property)</div>",
    ),
    (
        "<div class=\"check\"><i>✔</i> <strong>App móvil</strong> - iOS y Android en desarrollo (próximamente)</div>",
        "<div class=\"check\"><i>✔</i> <strong>Mobile app</strong> — iOS and Android in development (coming soon)</div>",
    ),
    (
        "<div class=\"check\"><i>✔</i> <strong>Exportación de datos</strong> - CSV/Excel para contabilidad</div>",
        "<div class=\"check\"><i>✔</i> <strong>Data export</strong> — CSV/Excel for accounting</div>",
    ),
    (
        "<div class=\"check\"><i>✔</i> <strong>Plan Básico Gratis</strong> - Acceso sin coste mensual, financiado con anuncios discretos</div>",
        "<div class=\"check\"><i>✔</i> <strong>Free Basic plan</strong> — No monthly fee, funded by discreet ads</div>",
    ),
    ("<span>SSL Seguro</span>", "<span>Secure SSL</span>"),
    ("<span>RGPD Compliant</span>", "<span>GDPR ready</span>"),
    ("<span>4.8/5 Valoración</span>", "<span>4.8/5 rating</span>"),
    ("<a class=\"btn primary\" href=\"#registro\">Registro Gratis</a>", "<a class=\"btn primary\" href=\"#registro\">Free sign-up</a>"),
    ("<a class=\"btn\" href=\"#caracteristicas\">Funciones</a>", "<a class=\"btn\" href=\"#caracteristicas\">Features</a>"),
    (
        "<h2 id=\"microsite-title\" style=\"margin: 0 0 16px; font-size: clamp(28px, 4vw, 40px); color: #1d4ed8;\">Microsite propio para reservas directas</h2>",
        "<h2 id=\"microsite-title\" style=\"margin: 0 0 16px; font-size: clamp(28px, 4vw, 40px); color: #1d4ed8;\">Your own microsite for direct bookings</h2>",
    ),
    (
        "Crea en minutos una página pública para tu alojamiento, comparte el enlace en redes o con tus huéspedes y recibe reservas directas.",
        "Create a public page for your property in minutes, share the link on social or with guests, and take direct bookings.",
    ),
    (
        "Con nuestro sistema de <strong style=\"color:#0f172a;\">pago directo</strong> las comisiones se reducen a la mitad y el dinero entra en tu cuenta bancaria sin esperas.",
        "With our <strong style=\"color:#0f172a;\">direct payment</strong> flow, fees are cut and money reaches your bank account without delays.",
    ),
    ("<strong style=\"color:#0f172a;\">Microsite con tu marca</strong>", "<strong style=\"color:#0f172a;\">Branded microsite</strong>"),
    (
        "<p style=\"margin:4px 0 0; color:#64748b;\">Personaliza portada, fotos, descripción y condiciones para compartir tu alojamiento con un enlace único.</p>",
        "<p style=\"margin:4px 0 0; color:#64748b;\">Customise cover, photos, description and terms—share your property with one link.</p>",
    ),
    ("<strong style=\"color:#0f172a;\">Pagos directos con comisiones mínimas</strong>", "<strong style=\"color:#0f172a;\">Direct payments, low fees</strong>"),
    (
        "<p style=\"margin:4px 0 0; color:#64748b;\">Integra el cobro seguro con Stripe y recibe pagos directos de tus huéspedes.</p>",
        "<p style=\"margin:4px 0 0; color:#64748b;\">Secure Stripe checkout; guests pay you directly.</p>",
    ),
    ("<strong style=\"color:#0f172a;\">Enlaces de cobro a medida</strong>", "<strong style=\"color:#0f172a;\">Custom payment links</strong>"),
    (
        "<p style=\"margin:4px 0 0; color:#64748b;\">Define fechas, importe acordado y envía el enlace al huésped para que complete el pago desde cualquier dispositivo.</p>",
        "<p style=\"margin:4px 0 0; color:#64748b;\">Set dates, amount and send the link so guests can pay from any device.</p>",
    ),
    ("<a href=\"#registro\" class=\"btn primary\" style=\"text-decoration:none;\">Quiero mi microsite</a>", "<a href=\"#registro\" class=\"btn primary\" style=\"text-decoration:none;\">I want my microsite</a>"),
    ("<a href=\"#caracteristicas\" class=\"btn\" style=\"text-decoration:none;\">Ver más funciones</a>", "<a href=\"#caracteristicas\" class=\"btn\" style=\"text-decoration:none;\">More features</a>"),
    ("<p style=\"margin:0; font-size:14px; color:#64748b;\">Microsite · Vista previa</p>", "<p style=\"margin:0; font-size:14px; color:#64748b;\">Microsite · Preview</p>"),
    ("<h4 style=\"margin:0 0 6px; font-size:18px;\">Apartamento Centro Málaga</h4>", "<h4 style=\"margin:0 0 6px; font-size:18px;\">Downtown Málaga apartment</h4>"),
    ("<p style=\"margin:0; font-size:14px; opacity:0.9;\">3 huéspedes · 2 noches · 280 €</p>", "<p style=\"margin:0; font-size:14px; opacity:0.9;\">3 guests · 2 nights · €280</p>"),
    ("<span style=\"font-size:14px; color:#475569;\">Check‑in 12 mayo · Check‑out 14 mayo</span>", "<span style=\"font-size:14px; color:#475569;\">Check-in 12 May · Check-out 14 May</span>"),
    ("<span style=\"font-size:14px; color:#475569;\">Pago seguro con tarjeta · Confirmación instantánea</span>", "<span style=\"font-size:14px; color:#475569;\">Secure card payment · Instant confirmation</span>"),
    (">Reservar y pagar ahora</button>", ">Book and pay now</button>"),
    (
        "Envía este microsite a tu huésped, recibe la reserva y el pago directo sin dependencias externas.",
        "Send this microsite to your guest, take the booking and payment directly—no middlemen.",
    ),
    ("💎 Programa de Recomendaciones", "💎 Referral &amp; affiliate programmes"),
    (
        "<h2 id=\"gana-dinero-title\" style=\"margin: 0 0 16px; font-size: clamp(32px, 5vw, 42px); color: #0f172a; font-weight: 800;\">Gana dinero con Delfín Check-in o ahorrátelo</h2>",
        "<h2 id=\"gana-dinero-title\" style=\"margin: 0 0 16px; font-size: clamp(32px, 5vw, 42px); color: #0f172a; font-weight: 800;\">Earn with Delfín Check-in—or save on your bill</h2>",
    ),
    (
        "Si eres propietario y usas Delfín Check-in (Plan Pro o Check-in), recomiéndanos y consigue <strong style=\"color:#0f172a;\">meses gratis</strong>.",
        "If you are an owner on Pro or Check-in, refer us and earn <strong style=\"color:#0f172a;\">free months</strong>.",
    ),
    (
        "Si no eres propietario pero conoces a alguien que podría usar nuestro software de gestión hotelera (PMS), gana <strong style=\"color:#0f172a;\">comisiones recurrentes</strong> recomendándonos.",
        "If you are not an owner but know someone who needs a PMS, earn <strong style=\"color:#0f172a;\">recurring commission</strong> by referring us.",
    ),
    ("<h3 style=\"margin: 0 0 12px; font-size: 24px; color: #1d4ed8; font-weight: 700;\">Soy Propietario</h3>", "<h3 style=\"margin: 0 0 12px; font-size: 24px; color: #1d4ed8; font-weight: 700;\">I’m a property owner</h3>"),
    (
        "Recomienda Delfín Check-in a otros propietarios y consigue <strong style=\"color:#0f172a;\">meses gratis</strong> en nuestros planes.",
        "Refer other owners to Delfín Check-in and get <strong style=\"color:#0f172a;\">free months</strong> on our plans.",
    ),
    ("Ver Programa de Referidos", "Referral programme"),
    ("<h3 style=\"margin: 0 0 12px; font-size: 24px; color: #7c3aed; font-weight: 700;\">No soy Propietario</h3>", "<h3 style=\"margin: 0 0 12px; font-size: 24px; color: #7c3aed; font-weight: 700;\">I’m not an owner</h3>"),
    ("Ver Programa de Afiliados", "Affiliate programme"),
    ("<span style=\"background: rgba(37,99,235,0.1); color: #1d4ed8; font-weight: 700; font-size: 14px; padding: 6px 14px; border-radius: 999px;\">Pagos directos</span>", "<span style=\"background: rgba(37,99,235,0.1); color: #1d4ed8; font-weight: 700; font-size: 14px; padding: 6px 14px; border-radius: 999px;\">Direct payments</span>"),
    (
        "<h2 id=\"links-title\" style=\"margin: 0; font-size: clamp(26px, 4vw, 36px); color: #0f172a;\">Crea enlaces de cobro personalizados en segundos</h2>",
        "<h2 id=\"links-title\" style=\"margin: 0; font-size: clamp(26px, 4vw, 36px); color: #0f172a;\">Create custom payment links in seconds</h2>",
    ),
    (
        "Define las fechas de estancia, introduce el importe que has acordado con tu huésped y genera un enlace único de pago. Lo compartes por WhatsApp o email y el huésped paga de forma segura. El dinero aterriza directamente en tu cuenta bancaria.",
        "Set stay dates, enter the amount you agreed with the guest and generate a unique payment link. Share it by WhatsApp or email; they pay securely and funds go to your bank.",
    ),
    ("<h3 style=\"margin: 0 0 8px; color: #1d4ed8; font-size: 18px;\">Configura la reserva</h3>", "<h3 style=\"margin: 0 0 8px; color: #1d4ed8; font-size: 18px;\">Set up the booking</h3>"),
    (
        "<p style=\"margin: 0; color: #475569; line-height: 1.6;\">Selecciona fechas de check‑in y check‑out, número de noches y cualquier comentario para el huésped.</p>",
        "<p style=\"margin: 0; color: #475569; line-height: 1.6;\">Pick check-in and check-out dates, number of nights and any note for the guest.</p>",
    ),
    ("<h3 style=\"margin: 0 0 8px; color: #047857; font-size: 18px;\">Elige el importe</h3>", "<h3 style=\"margin: 0 0 8px; color: #047857; font-size: 18px;\">Enter the amount</h3>"),
    (
        "<p style=\"margin: 0; color: #475569; line-height: 1.6;\">Introduce la cantidad exacta que habéis acordado (reserva completa o señal) y genera el enlace en un clic.</p>",
        "<p style=\"margin: 0; color: #475569; line-height: 1.6;\">Enter the exact amount (full stay or deposit) and create the link in one click.</p>",
    ),
    ("<h3 style=\"margin: 0 0 8px; color: #6d28d9; font-size: 18px;\">Comparte y cobra</h3>", "<h3 style=\"margin: 0 0 8px; color: #6d28d9; font-size: 18px;\">Share and get paid</h3>"),
    (
        "<p style=\"margin: 0; color: #475569; line-height: 1.6;\">Envía el enlace por WhatsApp, SMS o email. El huésped paga con tarjeta y recibes el dinero directamente en tu cuenta bancaria.</p>",
        "<p style=\"margin: 0; color: #475569; line-height: 1.6;\">Send the link by WhatsApp, SMS or email. The guest pays by card; you receive funds in your bank.</p>",
    ),
    ("<p style=\"margin: 0; font-size: 16px; color: #0f172a; font-weight: 600;\">Ejemplo de enlace generado</p>", "<p style=\"margin: 0; font-size: 16px; color: #0f172a; font-weight: 600;\">Sample generated link</p>"),
    (">Copiar</button>", ">Copy</button>"),
    ("<span style=\"background: rgba(124,58,237,0.1); color: #5b21b6; font-weight: 700; font-size: 14px; padding: 6px 14px; border-radius: 999px; width: fit-content;\">Aplicación móvil incluida</span>", "<span style=\"background: rgba(124,58,237,0.1); color: #5b21b6; font-weight: 700; font-size: 14px; padding: 6px 14px; border-radius: 999px; width: fit-content;\">Mobile app included</span>"),
    (
        "<h2 id=\"app-title\" style=\"margin:0; font-size: clamp(28px, 4vw, 38px); color:#312e81;\">Controla tu alojamiento desde el bolsillo</h2>",
        "<h2 id=\"app-title\" style=\"margin:0; font-size: clamp(28px, 4vw, 38px); color:#312e81;\">Run your property from your pocket</h2>",
    ),
    (
        "Delfín Check-in incluye acceso a la app para propietarios en <strong>App Store</strong> y <strong>Google Play</strong>. Recibe alertas de check-in, consulta reservas, marca habitaciones como listas y atiende incidencias sin abrir el portátil.",
        "Delfín Check-in includes owner apps on <strong>App Store</strong> and <strong>Google Play</strong>. Get check-in alerts, browse reservations, mark rooms ready and handle issues without a laptop.",
    ),
    (
        "<span>Notificaciones push inmediatas cuando se crea o modifica una reserva.</span>",
        "<span>Instant push notifications when a reservation is created or changed.</span>",
    ),
    (
        "<span>Listado completo de huéspedes, check-ins y documentos desde el móvil.</span>",
        "<span>Full guest list, check-ins and documents on mobile.</span>",
    ),
    (
        "<span>Acceso seguro con el mismo usuario y contraseña de tu panel web.</span>",
        "<span>Secure sign-in with the same credentials as the web panel.</span>",
    ),
    ("<span>Disponible en iOS y Android</span>", "<span>Available on iOS and Android</span>"),
    ("<a href=\"#instrucciones\" class=\"btn\" style=\"text-decoration:none;\">Ver cómo funciona</a>", "<a href=\"#instrucciones\" class=\"btn\" style=\"text-decoration:none;\">How it works</a>"),
    ("<h3 style=\"margin:4px 0 0; font-size:20px; color:#312e81;\">Panel del propietario</h3>", "<h3 style=\"margin:4px 0 0; font-size:20px; color:#312e81;\">Owner dashboard</h3>"),
    ("<span>Check-in hoy</span>", "<span>Check-in today</span>"),
    ("<span>🧳 Huespedes</span>", "<span>🧳 Guests</span>"),
    ("<span>Estado</span>", "<span>Status</span>"),
    ("<span>✔ Documentación completada</span>", "<span>✔ Documents complete</span>"),
    (">Ver calendario</button>", ">View calendar</button>"),
    (">Enviar mensaje al huésped</button>", ">Message guest</button>"),
    (
        "<h2 style=\"margin: 0 0 16px; font-size: clamp(32px, 5vw, 48px); font-weight: 800; color: #0f172a;\">Así se ve nuestra app móvil</h2>",
        "<h2 style=\"margin: 0 0 16px; font-size: clamp(32px, 5vw, 48px); font-weight: 800; color: #0f172a;\">This is what our mobile app looks like</h2>",
    ),
    (
        "Gestiona tu alojamiento desde cualquier lugar. Reservas, calendario, huéspedes y pagos, todo en la palma de tu mano.",
        "Manage your property anywhere—bookings, calendar, guests and payments in your hand.",
    ),
    ("📱 Vista Previa", "📱 Preview"),
    (
        "<h3 style=\"margin: 0 0 12px; font-size: 24px; font-weight: 700; color: #0f172a;\">¿Quieres probarla cuando esté lista?</h3>",
        "<h3 style=\"margin: 0 0 12px; font-size: 24px; font-weight: 700; color: #0f172a;\">Want early access?</h3>",
    ),
    (
        "Regístrate ahora y sé de los primeros en recibir acceso a la app móvil cuando lancemos.",
        "Sign up now to be among the first to try the mobile app at launch.",
    ),
    ("🚀 Quiero probar la app", "🚀 I want early app access"),
    ("<h2 style=\"margin: 0 0 16px; font-size: clamp(32px, 5vw, 48px); font-weight: 800; color: #0f172a;\">Aprende a usar Delfín Check-in</h2>", "<h2 style=\"margin: 0 0 16px; font-size: clamp(32px, 5vw, 48px); font-weight: 800; color: #0f172a;\">Learn how to use Delfín Check-in</h2>"),
    (
        "Descubre todas las funcionalidades del panel de usuario en este video tutorial completo.",
        "See the main panel features in this full video walkthrough.",
    ),
    ('title="Video Tutorial - Panel de Usuario Delfín Check-in"', 'title="Video tutorial - Delfín Check-in panel"'),
    ("Ver en YouTube", "Watch on YouTube"),
    ("<h2 id=\"datos-title\">Todos los datos centralizados</h2>", "<h2 id=\"datos-title\">All your data in one place</h2>"),
    (
        "<p class=\"lead\">Exporta un único archivo con todos los ingresos y reservas para tu declaración de la renta anual. Ahorra tiempo y errores.</p>",
        "<p class=\"lead\">Export one file with revenue and bookings for your annual tax return. Save time and mistakes.</p>",
    ),
    ("<i>✔</i> Descarga CSV/Excel unificado</div>", "<i>✔</i> Unified CSV/Excel download</div>"),
    ("<i>✔</i> Rangos de fechas (mes/año fiscal)</div>", "<i>✔</i> Date ranges (month/tax year)</div>"),
    ("<i>✔</i> Datos listos para asesoría</div>", "<i>✔</i> Accountant-ready data</div>"),
    ("<a class=\"btn primary\" href=\"#\" id=\"downloadCsvBtn\">Descargar ejemplo (CSV)</a>", "<a class=\"btn primary\" href=\"#\" id=\"downloadCsvBtn\">Download sample (CSV)</a>"),
    (
        "<h2 style=\"text-align: center; margin-bottom: 16px; font-size: 36px; font-weight: 800;\">Planes claros y transparentes</h2>",
        "<h2 style=\"text-align: center; margin-bottom: 16px; font-size: 36px; font-weight: 800;\">Clear, transparent pricing</h2>",
    ),
    (
        "Sin sorpresas, sin letra pequeña. Sabes exactamente qué obtienes y qué cuesta.",
        "No surprises, no fine print. You know exactly what you get and what it costs.",
    ),
    (
        "⚠️ <strong>IMPORTANTE:</strong> El acceso permanente al Plan Gratuito (Básico) sin coste mensual solo está disponible si te apuntas ahora. Las plazas son limitadas. <strong>Regístrate ya antes de que se agoten.</strong>",
        "⚠️ <strong>IMPORTANT:</strong> Permanent free Basic plan access is only for those who sign up now. Spots are limited. <strong>Register before they run out.</strong>",
    ),
    ("<h3 style=\"margin-top: 20px; font-size: 22px; font-weight: 800;\">Plan Básico</h3>", "<h3 style=\"margin-top: 20px; font-size: 22px; font-weight: 800;\">Basic plan</h3>"),
    ("<p style=\"color: #64748b; font-size: 14px; margin-bottom: 12px;\">Hasta 1 propiedad. Con anuncios.</p>", "<p style=\"color: #64748b; font-size: 14px; margin-bottom: 12px;\">Up to 1 property. Includes ads.</p>"),
    ("<li>✅ Formulario y listado de viajeros</li>", "<li>✅ Traveller form and list</li>"),
    ("<li>✅ Descarga XML (subida manual al Ministerio)</li>", "<li>✅ XML download (manual Ministry upload)</li>"),
    ("<li>✅ Reservas directas (9% comisión)</li>", "<li>✅ Direct bookings (9% fee)</li>"),
    ("<li>⚠️ Anuncios discretos</li>", "<li>⚠️ Discreet ads</li>"),
    ("<li>❌ Envío automático MIR (no incluido)</li>", "<li>❌ Automatic MIR submission (not included)</li>"),
    ("<a href=\"#registro\" class=\"btn primary\" style=\"width: 100%; text-align: center; padding: 16px; font-size: 18px; font-weight: 700;\">Empezar Gratis</a>", "<a href=\"#registro\" class=\"btn primary\" style=\"width: 100%; text-align: center; padding: 16px; font-size: 18px; font-weight: 700;\">Start free</a>"),
    (
        "<h3 style=\"margin-top: 20px; font-size: 22px; font-weight: 800; color: #1e40af;\">Plan Check-in</h3>",
        "<h3 style=\"margin-top: 20px; font-size: 22px; font-weight: 800; color: #1e40af;\">Check-in plan</h3>",
    ),
    ("<p style=\"color: #64748b; font-size: 14px; margin-bottom: 12px;\">Propiedades ilimitadas. Con anuncios.</p>", "<p style=\"color: #64748b; font-size: 14px; margin-bottom: 12px;\">Unlimited properties. Includes ads.</p>"),
    ("<li>✅ Envío automático al Ministerio (MIR)</li>", "<li>✅ Automatic Ministry (MIR) submission</li>"),
    ("<li>✅ Check-in digital y registro de viajeros</li>", "<li>✅ Digital check-in &amp; traveller registration</li>"),
    ("<li>✅ Cumplimiento RD 933/2021</li>", "<li>✅ RD 933/2021 compliance focus</li>"),
    ("Contratar Check-in", "Get Check-in"),
    ("<h3 style=\"margin-top: 20px; font-size: 22px; font-weight: 800; color: #b45309;\">Plan Standard</h3>", "<h3 style=\"margin-top: 20px; font-size: 22px; font-weight: 800; color: #b45309;\">Standard plan</h3>"),
    (
        "<p style=\"color: #64748b; font-size: 14px; margin-bottom: 12px;\">1 propiedad incluida. +2€/propiedad o habitación extra. Sin anuncios.</p>",
        "<p style=\"color: #64748b; font-size: 14px; margin-bottom: 12px;\">1 property included. +€2/extra property or room. No ads.</p>",
    ),
    ("<li>✅ Todo lo del Check-in</li>", "<li>✅ Everything in Check-in</li>"),
    ("<li>✅ Sin anuncios</li>", "<li>✅ No ads</li>"),
    ("Contratar Standard", "Get Standard"),
    ("Contratar Pro", "Get Pro"),
    (
        "<h4 style=\"margin: 0 0 12px 0; color: #1e40af; font-weight: 700; font-size: 18px;\">ℹ️ Transparencia total</h4>",
        "<h4 style=\"margin: 0 0 12px 0; color: #1e40af; font-weight: 700; font-size: 18px;\">ℹ️ Full transparency</h4>",
    ),
    (
        "<li><strong>Plan Básico:</strong> 0€/mes, hasta 1 propiedad. Financiado con anuncios. Solo descarga XML (sin envío automático MIR).</li>",
        "<li><strong>Basic:</strong> €0/mo, up to 1 property. Ad-funded. XML download only (no automatic MIR).</li>",
    ),
    (
        "<li><strong>Plan Check-in:</strong> 2€/mes + 2€ por cada propiedad. Incluye envío automático al Ministerio del Interior.</li>",
        "<li><strong>Check-in:</strong> €2/mo + €2 per property. Includes automatic Ministry submission.</li>",
    ),
    (
        "<li><strong>Plan Standard:</strong> 9,99€/mes, 1 propiedad incluida, +2€/mes por cada propiedad o habitación adicional. Sin anuncios.</li>",
        "<li><strong>Standard:</strong> €9.99/mo, 1 property included, +€2/mo per extra property or room. No ads.</li>",
    ),
    (
        "<li><strong>Plan Pro:</strong> 29,99€/mes, 1 propiedad incluida, +2€/mes por cada adicional. Sin anuncios y comisión reducida (5%) en reservas directas.</li>",
        "<li><strong>Pro:</strong> €29.99/mo, 1 property included, +€2/mo per extra. No ads and 5% fee on direct bookings.</li>",
    ),
    (
        "<li><strong>Sin sorpresas:</strong> Sabes exactamente qué obtienes y qué cuesta desde el primer día.</li>",
        "<li><strong>No surprises:</strong> You know what you get and what you pay from day one.</li>",
    ),
    (
        "<h2 style=\"color: white; margin-bottom: 16px; font-size: 42px; font-weight: 900; text-shadow: 0 4px 12px rgba(0,0,0,0.2);\">El software de gestión hotelera (PMS) que estabas esperando</h2>",
        "<h2 style=\"color: white; margin-bottom: 16px; font-size: 42px; font-weight: 900; text-shadow: 0 4px 12px rgba(0,0,0,0.2);\">The hotel PMS you were waiting for</h2>",
    ),
    (
        "<strong>Acceso gratuito al plan básico si te apuntas ya.</strong> De propietarios, para propietarios.",
        "<strong>Free basic access if you sign up now.</strong> By owners, for owners.",
    ),
    (
        "Estamos en la fase final de desarrollo. <strong>Regístrate ahora</strong> y sé de los primeros en probarlo cuando lancemos.",
        "We are in the final development phase. <strong>Sign up now</strong> to be among the first to try it at launch.",
    ),
    (
        "<br><strong style=\"font-size: 20px;\">Los primeros usuarios tendrán acceso permanente al Plan Gratuito (Básico) sin coste mensual.</strong>",
        "<br><strong style=\"font-size: 20px;\">Early users get permanent free Basic plan access with no monthly fee.</strong>",
    ),
    (
        "<br><span style=\"font-size: 16px; opacity: 0.9;\">Planes de pago: Check-in desde 2€/mes + 2€/propiedad, Standard 9,99€/mes, Pro 29,99€/mes.</span>",
        "<br><span style=\"font-size: 16px; opacity: 0.9;\">Paid plans: Check-in from €2/mo + €2/property, Standard €9.99/mo, Pro €29.99/mo.</span>",
    ),
    (
        "<p style=\"margin: 0; font-size: 16px; font-weight: 600;\">📱 Apps móviles en desarrollo | 💯 Plan Básico Gratis | 💰 Check-in desde 2€/mes</p>",
        "<p style=\"margin: 0; font-size: 16px; font-weight: 600;\">📱 Mobile apps in development | 💯 Free Basic | 💰 Check-in from €2/mo</p>",
    ),
    (
        "<h3 style=\"color: #0f172a; font-size: 28px; font-weight: 800; margin-bottom: 8px;\">🎁 Consigue acceso permanente al plan básico</h3>",
        "<h3 style=\"color: #0f172a; font-size: 28px; font-weight: 800; margin-bottom: 8px;\">🎁 Get permanent free basic access</h3>",
    ),
    (
        "Únete a la lista de espera y recibe acceso prioritario cuando lancemos.",
        "Join the waitlist for priority access at launch.",
    ),
    (
        "<strong style=\"color: #2563eb;\">Los primeros usuarios tendrán acceso permanente al Plan Gratuito (Básico) sin coste mensual.</strong>",
        "<strong style=\"color: #2563eb;\">Early users keep permanent free Basic plan access.</strong>",
    ),
    ("<span style=\"display: block; margin-bottom: 8px; font-weight: 600; color: #0f172a;\">Email *</span>", "<span style=\"display: block; margin-bottom: 8px; font-weight: 600; color: #0f172a;\">Email *</span>"),
    ("<span style=\"display: block; margin-bottom: 8px; font-weight: 600; color: #0f172a;\">Nombre (opcional)</span>", "<span style=\"display: block; margin-bottom: 8px; font-weight: 600; color: #0f172a;\">Name (optional)</span>"),
    ("placeholder=\"Tu nombre\"", 'placeholder="Your name"'),
    ("<span id=\"waitlistSubmitText\">🎁 Quiero acceso permanente al plan básico</span>", "<span id=\"waitlistSubmitText\">🎁 I want permanent free basic access</span>"),
    ("<span id=\"waitlistLoading\" style=\"display: none;\">Enviando...</span>", "<span id=\"waitlistLoading\" style=\"display: none;\">Sending...</span>"),
    (
        "<h4 style=\"margin: 0 0 8px 0; color: #1e40af; font-weight: 700; font-size: 18px;\">✨ Plan Gratuito (Básico) - Incluye esto</h4>",
        "<h4 style=\"margin: 0 0 8px 0; color: #1e40af; font-weight: 700; font-size: 18px;\">✨ Free (Basic) plan — included</h4>",
    ),
    (
        "<li><strong>✅ Gestión de reservas</strong> - Gestiona todas tus reservas desde un panel intuitivo</li>",
        "<li><strong>✅ Reservations</strong> — Manage everything from an intuitive panel</li>",
    ),
    (
        "<li><strong>✅ Interfaz en 5 idiomas</strong> - Español, francés, inglés, italiano y portugués</li>",
        "<li><strong>✅ 5-language UI</strong> — Spanish, French, English, Italian and Portuguese</li>",
    ),
    (
        "<li><strong>✅ Gestión de habitaciones o propiedades</strong> - Controla tu inventario</li>",
        "<li><strong>✅ Rooms or properties</strong> — Control your inventory</li>",
    ),
    ("<li><strong>✅ Exportación de datos</strong> - CSV/Excel</li>", "<li><strong>✅ Data export</strong> — CSV/Excel</li>"),
    (
        "<li><strong>✅ Panel de administración</strong> - Intuitivo y potente</li>",
        "<li><strong>✅ Admin panel</strong> — Intuitive and powerful</li>",
    ),
    ("<li><strong>✅ Soporte por email</strong> - Siempre disponible</li>", "<li><strong>✅ Email support</strong></li>"),
    ("<li><strong>✅ App móvil</strong> - iOS y Android (próximamente)</li>", "<li><strong>✅ Mobile app</strong> — iOS and Android (soon)</li>"),
    (
        "❌ <strong>No incluye:</strong> Envío automático al Ministerio (disponible en Plan Check-in desde 2€/mes)",
        "❌ <strong>Not included:</strong> Automatic Ministry submission (Check-in plan from €2/mo)",
    ),
    ("<h3 style=\"text-align: center; margin-bottom: 20px;\">Información de contacto</h3>", "<h3 style=\"text-align: center; margin-bottom: 20px;\">Contact details</h3>"),
    ("<div style=\"font-weight: 600; color: var(--text); margin-bottom: 4px;\">Horario</div>", "<div style=\"font-weight: 600; color: var(--text); margin-bottom: 4px;\">Hours</div>"),
    ("<div style=\"color: var(--muted); font-size: 14px;\">Lun-Dom: 9:00-22:00</div>", "<div style=\"color: var(--muted); font-size: 14px;\">Mon–Sun: 9:00–22:00</div>"),
    (">Email directo</a>", ">Email us</a>"),
    ("<h2>Lo que dicen nuestros clientes</h2>", "<h2>What our users say</h2>"),
    (
        "<p class=\"lead\">Hostales y apartamentos que ya confían en Delfín Check-in para su gestión diaria.</p>",
        "<p class=\"lead\">Hostels and apartments trusting Delfín Check-in for day-to-day operations.</p>",
    ),
    (
        "\"Estamos cansados de pagar cientos de euros al mes por sistemas complicados. Por eso estamos construyendo Delfín Check-in:",
        "\"We were tired of paying hundreds a month for clunky systems. That is why we are building Delfín Check-in:",
    ),
    (
        "<strong style=\"color: var(--brand);\">gratis, simple y hecho por propietarios que entienden lo que realmente necesitas</strong>.\"",
        "<strong style=\"color: var(--brand);\">free, simple and built by owners who get what you need</strong>.\"",
    ),
    ("<div class=\"testimonial-author\" style=\"margin-top: 16px; font-weight: 700;\">El equipo de Delfín Check-in</div>", "<div class=\"testimonial-author\" style=\"margin-top: 16px; font-weight: 700;\">The Delfín Check-in team</div>"),
    ("<div class=\"testimonial-role\">Propietarios de alojamientos turísticos</div>", "<div class=\"testimonial-role\">Holiday rental owners</div>"),
    ("<div class=\"testimonial-author\">Nuestra promesa</div>", "<div class=\"testimonial-author\">Our promise</div>"),
    ("<div class=\"testimonial-role\">Para todos los propietarios</div>", "<div class=\"testimonial-role\">For every owner</div>"),
    ("<div class=\"testimonial-author\" style=\"margin-top: 16px; font-weight: 700;\">Nuestro enfoque</div>", "<div class=\"testimonial-author\" style=\"margin-top: 16px; font-weight: 700;\">Our focus</div>"),
    ("<div class=\"testimonial-role\">Lo esencial primero, el resto viene después</div>", "<div class=\"testimonial-role\">Core product first—the rest follows</div>"),
    (
        "<h3 style=\"margin: 0; font-size: 20px; font-weight: 700;\">Previsualización de Ficha de Registro</h3>",
        "<h3 style=\"margin: 0; font-size: 20px; font-weight: 700;\">Registration preview</h3>",
    ),
    (
        "<p style=\"margin: 4px 0 0; font-size: 14px; opacity: 0.9;\">Datos del huésped generados automáticamente</p>",
        "<p style=\"margin: 4px 0 0; font-size: 14px; opacity: 0.9;\">Sample guest data</p>",
    ),
    ("👤 Información Personal", "👤 Personal details"),
    ("Nombre completo", "Full name"),
    ("Documento de identidad", "ID document"),
    ("Fecha de nacimiento", "Date of birth"),
    ("Nacionalidad", "Nationality"),
    ("📧 Información de Contacto", "📧 Contact"),
    ("Correo electrónico", "Email"),
    ("🏨 Información de Estancia", "🏨 Stay details"),
    ("Fecha de entrada", "Arrival date"),
    ("Fecha de salida", "Departure date"),
    ("Idioma del formulario", "Form language"),
    (
        "<strong>ℹ️ Nota:</strong> Esta es una previsualización con datos de ejemplo. En producción se generará el documento oficial conforme a la normativa del Ministerio del Interior.",
        "<strong>ℹ️ Note:</strong> This is a sample preview. In production the official document is generated per Ministry rules.",
    ),
    (
        "<p style=\"margin: 0; color: var(--muted); font-size: 14px;\">Software de gestión hotelera y auto check‑in para hostales y apartamentos.</p>",
        "<p style=\"margin: 0; color: var(--muted); font-size: 14px;\">Hotel PMS and guest check-in for hostels and apartments.</p>",
    ),
    ("<h4 style=\"margin: 0 0 10px; color: var(--text);\">Contacto</h4>", "<h4 style=\"margin: 0 0 10px; color: var(--text);\">Contact</h4>"),
    ("<h4 style=\"margin: 0 0 10px; color: var(--text);\">Programas</h4>", "<h4 style=\"margin: 0 0 10px; color: var(--text);\">Programmes</h4>"),
    (">Programa de Referidos</a>", ">Referral programme</a>"),
    (">Programa de Afiliados</a>", ">Affiliate programme</a>"),
    ("<h4 style=\"margin: 0 0 10px; color: var(--text);\">Legal</h4>", "<h4 style=\"margin: 0 0 10px; color: var(--text);\">Legal</h4>"),
    ("Política de Privacidad", "Privacy policy"),
    ("Política de Cookies", "Cookie policy"),
    ("Términos de Servicio", "Terms of service"),
    ("Aviso Legal", "Legal notice"),
    (">Gestionar Cookies</button>", ">Cookie settings</button>"),
    ("<a href=\"#registro\" style=\"color: var(--brand);\">Registro Gratis</a>", "<a href=\"#registro\" style=\"color: var(--brand);\">Free sign-up</a>"),
    (
        "El Plan Gratuito (Básico) se financia con anuncios elegantes y discretos. El Plan Check-in tiene un coste de 2€/mes. Sin costes ocultos.",
        "The free Basic plan is ad-funded. The Check-in plan is €2/mo. No hidden fees.",
    ),
    (
        "<strong style=\"color: var(--brand);\">ℹ️ Aviso Legal:</strong> Delfín Check-in se reserva el derecho de modificar las funcionalidades incluidas en cada plan. El servicio mantendrá la disponibilidad de un plan gratuito sin coste mensual, con funcionalidades básicas, conforme a los Términos de Servicio vigentes en cada momento.",
        "<strong style=\"color: var(--brand);\">ℹ️ Legal:</strong> Delfín Check-in may change features included in each plan. A free plan with basic features and no monthly fee will remain available, per the Terms of Service in force.",
    ),
    (
        "🍪 <strong>Utilizamos cookies</strong> para mejorar tu experiencia, analizar el tráfico y personalizar contenido.",
        "🍪 <strong>We use cookies</strong> to improve your experience, analyse traffic and personalise content.",
    ),
    (">Solo necesarias</button>", ">Necessary only</button>"),
    (">Personalizar</button>", ">Customise</button>"),
    (">Aceptar todas</button>", ">Accept all</button>"),
    # Feature cards (sin data-en previo)
    ("<h3 style=\"margin: 0; color: #1e40af; font-size: 18px;\">Gestión de reservas</h3>", "<h3 style=\"margin: 0; color: #1e40af; font-size: 18px;\">Reservation management</h3>"),
    (
        "<p style=\"margin: 0; color: #64748b; line-height: 1.5;\">Gestiona todas tus reservas desde un panel web intuitivo. Crea reservas manualmente, organiza tu calendario y controla tu inventario de forma sencilla.</p>",
        "<p style=\"margin: 0; color: #64748b; line-height: 1.5;\">Manage all reservations from an intuitive web panel. Create bookings manually, organise your calendar and keep inventory under control.</p>",
    ),
    ("<h3 style=\"margin: 0; color: #d97706; font-size: 18px;\">Pre‑check‑in online</h3>", "<h3 style=\"margin: 0; color: #d97706; font-size: 18px;\">Online pre-check-in</h3>"),
    (
        "<p style=\"margin: 0; color: #64748b; line-height: 1.5;\">Módulo de check-in digital: Permite a tus huéspedes completar su información y envía automáticamente al Ministerio del Interior de España. <strong>Plan Check-in: desde 2€/mes + 2€/propiedad. Standard 9,99€/mes. Pro 29,99€/mes.</strong></p>",
        "<p style=\"margin: 0; color: #64748b; line-height: 1.5;\">Digital check-in: guests complete their details and we submit to the Spanish Ministry of the Interior. <strong>Check-in plan: from €2/mo + €2/property. Standard €9.99/mo. Pro €29.99/mo.</strong></p>",
    ),
    ("<h3 style=\"margin: 0; color: #7c3aed; font-size: 18px;\">App móvil Android &amp; iPhone</h3>", "<h3 style=\"margin: 0; color: #7c3aed; font-size: 18px;\">Mobile app — Android &amp; iPhone</h3>"),
    (
        "<p style=\"margin: 0; color: #64748b; line-height: 1.5;\">Aplicaciones móviles nativas para iOS y Android <strong>en desarrollo</strong>. Próximamente podrás gestionar todo desde tu móvil con notificaciones en tiempo real.</p>",
        "<p style=\"margin: 0; color: #64748b; line-height: 1.5;\">Native iOS and Android apps are <strong>in development</strong>. Soon you will manage everything on your phone with real-time notifications.</p>",
    ),
    ("<h3 style=\"margin: 0; color: #0891b2; font-size: 18px;\">Exportación de datos</h3>", "<h3 style=\"margin: 0; color: #0891b2; font-size: 18px;\">Data export</h3>"),
    ("<p style=\"margin: 0; color: #64748b; line-height: 1.5;\">CSV/Excel para contabilidad y declaración de renta</p>", "<p style=\"margin: 0; color: #64748b; line-height: 1.5;\">CSV/Excel for accounting and tax filing</p>"),
    (
        "<strong>🚀 En desarrollo:</strong> Las aplicaciones móviles están en desarrollo. <strong>Regístrate para ser de los primeros en probarlo cuando esté listo.</strong>",
        "<strong>🚀 In development:</strong> Mobile apps are in development. <strong>Sign up to try them early.</strong>",
    ),
    ("🚀 Próximamente", "🚀 Coming soon"),
    ("💯 Plan Básico Gratis", "💯 Free Basic plan"),
    ("👥 De Propietarios para Propietarios", "👥 By owners, for owners"),
    (
        "Cuantos más refieras, más meses gratis acumulas.",
        "The more you refer, the more free months you earn.",
    ),
    (
        '<li><strong>🔗 Crea enlaces de pago personalizados</strong> - Define fechas, importe acordado y genera un enlace único de pago. Compártelo por WhatsApp o email y el huésped paga de forma segura. El dinero entra directamente en tu cuenta bancaria.</li>',
        '<li><strong>🔗 Custom payment links</strong> — Set dates, amount and generate a unique payment link. Share by WhatsApp or email; the guest pays securely and funds reach your bank.</li>',
    ),
    (
        '<li><strong>🌐 Microsite para reservas directas</strong> - Crea en minutos una página pública para tu alojamiento, comparte el enlace en redes o con tus huéspedes y recibe reservas directas. Con pagos directos las comisiones se reducen y el dinero entra en tu cuenta sin esperas.</li>',
        '<li><strong>🌐 Direct-booking microsite</strong> — Create a public page in minutes, share the link and take direct bookings. Direct payments mean lower fees and faster payouts.</li>',
    ),
    (
        '<strong style="font-size: 16px; color: #059669;">🎁 Los primeros usuarios: tendrás acceso permanente al plan básico sin coste mensual</strong>',
        '<strong style="font-size: 16px; color: #059669;">🎁 Early users: permanent free basic plan access with no monthly fee</strong>',
    ),
    (
        '<span style="background: rgba(37,99,235,0.10); color: #1d4ed8; font-weight: 700; font-size: 14px; padding: 6px 14px; border-radius: 999px; width: fit-content;">Nuevo · Asistente dentro del panel</span>',
        '<span style="background: rgba(37,99,235,0.10); color: #1d4ed8; font-weight: 700; font-size: 14px; padding: 6px 14px; border-radius: 999px; width: fit-content;">New · In-panel assistant</span>',
    ),
    (
        '<h2 id="asistente-title" style="margin:0; font-size: clamp(28px, 4vw, 38px); color:#0f172a; font-weight: 800;">Asistente de soporte para usar el software paso a paso</h2>',
        '<h2 id="asistente-title" style="margin:0; font-size: clamp(28px, 4vw, 38px); color:#0f172a; font-weight: 800;">Step-by-step support assistant inside the software</h2>',
    ),
    (
        'Dentro del panel de administración cuentas con un <strong>asistente de soporte integrado</strong> que te ayuda a usar el PMS en lenguaje humano.\n            Le puedes preguntar cómo hacer algo (por ejemplo “crear una reserva”, “enviar el parte de viajeros” o “configurar un microsite”) y te responde con instrucciones claras dentro del propio panel.',
        'In the admin panel you have a <strong>built-in support assistant</strong> that helps you use the PMS in plain language.\n            Ask how to do something (for example “create a booking”, “send the traveller report” or “set up a microsite”) and get clear instructions right in the panel.',
    ),
    (
        "<span>Respuestas en texto sencillo, sin tecnicismos, pensadas para propietarios y pequeños alojamientos.</span>",
        "<span>Plain-language answers for owners and small properties—no jargon.</span>",
    ),
    (
        "<span>Te guía para configurar el sistema: propiedades, tarifas, microsite, enlaces de pago y más.</span>",
        "<span>Guides you through setup: properties, rates, microsite, payment links and more.</span>",
    ),
    (
        "<span>Te recuerda los pasos para cumplir con el RD 933/2021 y enviar correctamente los partes de viajeros.</span>",
        "<span>Reminds you of steps for RD 933/2021 and sending traveller reports correctly.</span>",
    ),
    (
        '<p style="margin:14px 0 0; font-size:14px; color:#64748b; max-width:640px;">\n            El asistente está pensado para que <strong>no tengas miedo a tocar nada</strong>: le preguntas, sigues sus pasos y configuras tu alojamiento con tranquilidad.\n          </p>',
        '<p style="margin:14px 0 0; font-size:14px; color:#64748b; max-width:640px;">\n            The assistant is there so you <strong>never fear clicking around</strong>: ask, follow the steps and set up your property with confidence.\n          </p>',
    ),
    (
        '<p style="margin:0; font-size:12px; color:#cbd5f5; opacity:0.9;">Asistente de soporte</p>',
        '<p style="margin:0; font-size:12px; color:#cbd5f5; opacity:0.9;">Support assistant</p>',
    ),
    (
        '<p style="margin:0 0 6px; font-size:11px; color:#9ca3af;">Tú · 10:21</p>',
        '<p style="margin:0 0 6px; font-size:11px; color:#9ca3af;">You · 10:21</p>',
    ),
    (
        '<p style="margin:0; font-size:13px; color:#e5e7eb;">“Es mi primer día usando el sistema, ¿qué pasos tengo que seguir para tenerlo todo listo?”</p>',
        '<p style="margin:0; font-size:13px; color:#e5e7eb;">“It’s my first day—what steps should I follow to get everything ready?”</p>',
    ),
    (
        '<p style="margin:0 0 6px; font-size:11px; color:#9ca3af;">Asistente · 10:21</p>',
        '<p style="margin:0 0 6px; font-size:11px; color:#9ca3af;">Assistant · 10:21</p>',
    ),
    (
        "<li>Da de alta tu alojamiento y habitaciones.</li>",
        "<li>Add your property and rooms.</li>",
    ),
    (
        "<li>Configura tus planes (Básico, Check‑in, Pro) y precios.</li>",
        "<li>Set your plans (Basic, Check-in, Pro) and rates.</li>",
    ),
    (
        "<li>Activa el módulo de check‑in digital para enviar los partes.</li>",
        "<li>Enable digital check-in to submit traveller reports.</li>",
    ),
    (
        "<li>Crea tu microsite o enlaces de cobro si quieres reservas directas.</li>",
        "<li>Create your microsite or payment links for direct bookings.</li>",
    ),
    (
        "<li>Invita a tu equipo y revisa el calendario de reservas.</li>",
        "<li>Invite your team and review the booking calendar.</li>",
    ),
    (
        '<p style="margin:8px 0 0; font-size:12px; color:#9ca3af;">Si quieres, te voy guiando por cada paso desde aquí.</p>',
        '<p style="margin:8px 0 0; font-size:12px; color:#9ca3af;">I can walk you through each step from here if you like.</p>',
    ),
    (
        '<span style="font-size:14px; color:#9ca3af;">Escribe tu duda sobre el panel...</span>',
        '<span style="font-size:14px; color:#9ca3af;">Type your question about the panel...</span>',
    ),
    (
        '"La idea es simple: un PMS que funcione, que sea fácil de usar y que no cueste un ojo de la cara. \n            <strong>Eso es lo que estamos construyendo.</strong>"',
        '"The idea is simple: a PMS that works, is easy to use and does not cost a fortune.\n            <strong>That is what we are building.</strong>"',
    ),
    (
        '"Las apps móviles están en desarrollo. \n            Pero el core del PMS: <strong style="color: var(--brand);">gestionar reservas y habitaciones de forma simple y gratis</strong>, eso es lo primero."',
        '"Mobile apps are in development.\n            But the core of the PMS—<strong style="color: var(--brand);">managing bookings and rooms simply and for free</strong>—comes first."',
    ),
    (
        '<label style="display: block; font-size: 12px; color: #64748b; margin-bottom: 8px;">Nombre del huésped *</label>',
        '<label style="display: block; font-size: 12px; color: #64748b; margin-bottom: 8px;">Guest name *</label>',
    ),
    (
        '<p style="margin: 4px 0 0; font-size: 11px; color: #64748b;">Ben Gibson • 2 huéspedes</p>',
        '<p style="margin: 4px 0 0; font-size: 11px; color: #64748b;">Ben Gibson • 2 guests</p>',
    ),
    (
        '<span>Disponible en varios idiomas (español, inglés, francés, italiano y portugués) para adaptarse a tu equipo.</span>',
        '<span>Available in several languages (Spanish, English, French, Italian and Portuguese) for your team.</span>',
    ),
    (
        '<h4 style="margin: 0; color: #1e40af; font-size: 16px; font-weight: 600;">¿Qué pasa después?</h4>',
        '<h4 style="margin: 0; color: #1e40af; font-size: 16px; font-weight: 600;">What happens next?</h4>',
    ),
    (
        'Recibirás un <strong>email de onboarding</strong> con una <strong>contraseña temporal</strong> para acceder a tu panel de administración en <strong>admin.delfincheckin.com</strong>.',
        'You will receive an <strong>onboarding email</strong> with a <strong>temporary password</strong> to access your admin panel at <strong>admin.delfincheckin.com</strong>.',
    ),
    (
        '<strong>⚠️ Importante:</strong> Deberás cambiar la contraseña temporal nada más entrar por primera vez por seguridad.',
        '<strong>⚠️ Important:</strong> You must change the temporary password on first login for security.',
    ),
    (
        '<span id="buttonText">💳 Contratar</span>',
        '<span id="buttonText">💳 Subscribe</span>',
    ),
    (
        '<span id="spinner" style="display: none;">⏳ Procesando...</span>',
        '<span id="spinner" style="display: none;">⏳ Processing...</span>',
    ),
    ("🔒 Pago 100% seguro procesado por Stripe", "🔒 100% secure payment processed by Stripe"),
    (
        '<a href="politica-privacidad.html" style="color: var(--brand); text-decoration: underline;">Privacidad</a>',
        '<a href="politica-privacidad.html" style="color: var(--brand); text-decoration: underline;">Privacy</a>',
    ),
    (
        "planText = plan === 'monthly' ? 'mensual' : plan === 'yearly' ? 'anual' : 'volumen';\n      subject = `Consulta plan ${planText} - Delfín Check-in`;\n      body = `Hola,%0D%0A%0D%0AMe interesa el plan ${planText} de Delfín Check-in para ${properties} ${properties == 1 ? 'propiedad' : 'propiedades'}.%0D%0A%0D%0A¿Podrían darme más información sobre:%0D%0A- Precios y planes disponibles%0D%0A- Funcionalidades incluidas%0D%0A- Proceso de implementación%0D%0A%0D%0AGracias.`;",
        "planText = plan === 'monthly' ? 'monthly' : plan === 'yearly' ? 'yearly' : 'volume';\n      subject = `Plan enquiry (${planText}) - Delfín Check-in`;\n      body = `Hello,%0D%0A%0D%0AI am interested in the ${planText} plan for Delfín Check-in for ${properties} ${properties == 1 ? 'property' : 'properties'}.%0D%0A%0D%0ACould you share more about:%0D%0A- Pricing and available plans%0D%0A- Included features%0D%0A- Onboarding process%0D%0A%0D%0AThank you.`;",
    ),
    (
        'const body = `Hola,%0D%0A%0D%0AMe interesa conocer más sobre Delfín Check-in${planText}.%0D%0A%0D%0A¿Podrían enviarme información sobre:%0D%0A- Precios y planes disponibles%0D%0A- Funcionalidades incluidas%0D%0A- Proceso de implementación%0D%0A%0D%0AGracias.`;',
        'const body = `Hello,%0D%0A%0D%0AI would like to know more about Delfín Check-in${planText}.%0D%0A%0D%0ACould you send information on:%0D%0A- Pricing and plans%0D%0A- Included features%0D%0A- Implementation process%0D%0A%0D%0AThank you.`;',
    ),
    (
        '<h4 style="margin: 0 0 12px; color: #1e40af; font-size: 16px;">Contacta con nosotros</h4>',
        '<h4 style="margin: 0 0 12px; color: #1e40af; font-size: 16px;">Contact us</h4>',
    ),
    (
        '<p style="margin: 0; color: #64748b; font-size: 14px;">Te responderemos por email en menos de 24 horas.</p>',
        '<p style="margin: 0; color: #64748b; font-size: 14px;">We will reply by email within 24 hours.</p>',
    ),
    (
        '<div style="font-weight: 600;">Contactar por Email</div>',
        '<div style="font-weight: 600;">Email us</div>',
    ),
    (
        '<div style="font-size: 12px; opacity: 0.9;">Respuesta en 24h</div>',
        '<div style="font-size: 12px; opacity: 0.9;">Reply within 24h</div>',
    ),
    (
        '<strong>💡 Consejo:</strong> Te responderemos por email en menos de 24 horas',
        '<strong>💡 Tip:</strong> We reply by email within 24 hours',
    ),
    (
        "              ☐ Declaro haber leído y aceptado los Términos y Condiciones, la Política de Privacidad y los Supuestos de Uso del servicio Delfín Check-in, y consiento el tratamiento de mis datos conforme a lo dispuesto en la normativa vigente de protección de datos.",
        "              ☐ I declare that I have read and accept the Terms and Conditions, the Privacy Policy and the Acceptable Use terms for Delfín Check-in, and I consent to the processing of my data in accordance with applicable data-protection law.",
    ),
    ("Ver términos detallados", "View full terms"),
    (
        '<p style="font-weight: 600; margin: 0 0 10px 0;">Al aceptar, confirmo que:</p>',
        '<p style="font-weight: 600; margin: 0 0 10px 0;">By accepting, I confirm that:</p>',
    ),
    (
        '<p style="margin: 0 0 8px 0;">• Comprendo que Delfín Check-in es una herramienta de gestión que facilita la creación, almacenamiento y exportación de ficheros de registro de viajeros conforme al Real Decreto 933/2021, pero que no realiza el envío automático al MIR ni sustituye las obligaciones legales del titular del alojamiento.</p>',
        '<p style="margin: 0 0 8px 0;">• I understand that Delfín Check-in is a management tool that helps create, store and export traveller registration files under Royal Decree 933/2021, but it does not perform automatic MIR submission or replace the legal duties of the accommodation owner.</p>',
    ),
    (
        '<p style="margin: 0 0 8px 0;">• Soy responsable de la veracidad, exactitud y conservación de los datos introducidos en los formularios de registro.</p>',
        '<p style="margin: 0 0 8px 0;">• I am responsible for the accuracy and retention of data entered in registration forms.</p>',
    ),
    (
        '<p style="margin: 0 0 8px 0;">• Entiendo que la IA y las funciones disponibles (por ejemplo, chatbot en Telegram o WhatsApp) actúan como asistencia complementaria y no como servicio oficial de verificación, firma o presentación telemática ante las autoridades.</p>',
        '<p style="margin: 0 0 8px 0;">• I understand that AI and related features (e.g. chatbots on Telegram or WhatsApp) are complementary assistance only, not an official verification, signature or telematic filing service with authorities.</p>',
    ),
    (
        '<p style="margin: 0 0 8px 0;">• Acepto que los datos procesados se almacenarán de forma segura durante el tiempo necesario para cumplir con las finalidades del servicio y la normativa aplicable.</p>',
        '<p style="margin: 0 0 8px 0;">• I accept that processed data will be stored securely for as long as needed to fulfil the service purposes and applicable law.</p>',
    ),
    (
        '<p style="margin: 0 0 8px 0;">• Reconozco que el servicio requiere una suscripción activa (mensual o anual), cuyo pago otorga acceso al software y sus funcionalidades, sin implicar custodia ni certificación oficial de registros.</p>',
        '<p style="margin: 0 0 8px 0;">• I acknowledge that the service requires an active subscription (monthly or yearly); payment grants access to the software and features, without implying custody or official certification of records.</p>',
    ),
    (
        '<p style="margin: 0 0 8px 0;">• Comprendo que pueden producirse interrupciones temporales por mantenimiento, actualizaciones o causas técnicas ajenas a la plataforma, y que estas no darán lugar a compensaciones salvo en casos de incidencia prolongada.</p>',
        '<p style="margin: 0 0 8px 0;">• I understand there may be temporary interruptions for maintenance, updates or technical causes beyond the platform, and these do not entitle compensation except in case of prolonged incidents.</p>',
    ),
    (
        '<p style="margin: 0 0 8px 0;">• Acepto que los precios, condiciones y funcionalidades del servicio podrán actualizarse, comunicándose siempre por medios electrónicos con antelación razonable.</p>',
        '<p style="margin: 0 0 8px 0;">• I accept that prices, terms and features may be updated, with reasonable notice by electronic means.</p>',
    ),
    (
        '<p style="margin: 0 0 8px 0;">• He revisado las políticas aplicables en <a href="terminos-servicio.html" target="_blank" style="color: #2563eb; text-decoration: underline;">Términos de Servicio</a> y <a href="politica-privacidad.html" target="_blank" style="color: #2563eb; text-decoration: underline;">Política de Privacidad</a> y las acepto expresamente antes de realizar el pago.</p>',
        '<p style="margin: 0 0 8px 0;">• I have reviewed the applicable policies in <a href="terminos-servicio.html" target="_blank" style="color: #2563eb; text-decoration: underline;">Terms of service</a> and <a href="politica-privacidad.html" target="_blank" style="color: #2563eb; text-decoration: underline;">Privacy policy</a> and expressly accept them before paying.</p>',
    ),
    (
        '<p style="font-weight: 600; margin: 0; border-top: 1px solid #e5e7eb; padding-top: 10px;">Al continuar, confirmo mi conformidad y doy consentimiento informado para la prestación del servicio.</p>',
        '<p style="font-weight: 600; margin: 0; border-top: 1px solid #e5e7eb; padding-top: 10px;">By continuing, I confirm my agreement and give informed consent to receive the service.</p>',
    ),
    ("console.warn('Elementos de calculadora no encontrados')", "console.warn('Calculator elements not found')"),
    (
        "const subject = `Nueva consulta desde la web - ${name}`;",
        "const subject = `Website enquiry - ${name}`;",
    ),
    (
        "const subject = `Consulta Delfín Check-in${planText}`;",
        "const subject = `Delfín Check-in enquiry${planText}`;",
    ),
]


def apply_body_replacements(text: str) -> str:
    ordered = sorted(REPLACEMENTS, key=lambda x: len(x[0]), reverse=True)
    for old, new in ordered:
        if old not in text:
            continue
        n = text.count(old)
        if n > 1:
            print(f"  [warn] {n}× match, replacing all: {old[:50]}…")
        text = text.replace(old, new)
    return text


def replace_faq(text: str) -> str:
    faq = FAQ_EN.read_text(encoding="utf-8").strip()
    return re.sub(
        r"<section id=\"faq\" class=\"section container\">[\s\S]*?</section>",
        faq,
        text,
        count=1,
    )


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Missing {SRC}")
    if not FAQ_EN.is_file():
        raise SystemExit(f"Missing {FAQ_EN}")
    if not FAQ_MAINENTITY_EN.is_file():
        raise SystemExit(f"Missing {FAQ_MAINENTITY_EN}")

    source_es = SRC.read_text(encoding="utf-8")
    DST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)
    text = DST.read_text(encoding="utf-8")
    text = head_and_switch(text)
    text = replace_ld_json_script(text, source_es)
    text = replace_faq(text)
    # Antes de sustituciones masivas: evita que matches rompan atributos data-es/data-en
    text = swap_data_en_attributes(text)
    text = swap_data_en_placeholders(text)
    text = apply_body_replacements(text)
    DST.write_text(text, encoding="utf-8")
    print(f"Wrote {DST} ({len(text):,} chars)")


if __name__ == "__main__":
    main()
