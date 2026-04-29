# 📝 INSTRUCCIONES PARA CREAR NUEVOS ARTÍCULOS

## 🎉 ACTUALIZACIÓN - Popup Mejorado (Enero 2026)

**El popup ahora tiene mejor UX:**
- ✅ **Sin formulario duplicado**: Solo muestra un botón CTA
- ✅ **Scroll suave a waitlist**: Al hacer clic, cierra y baja a la sección de waitlist completa
- ✅ **Usuarios ven todo**: Todas las características de la waitlist están visibles
- ✅ **Ya integrado**: El template `_template.html` ya incluye este comportamiento

## ⚠️ IMPORTANTE: MANTENER CONSISTENCIA TOTAL CON LA LANDING

Cada artículo DEBE tener EXACTAMENTE los mismos elementos visuales y funcionales que la landing page (`index.html`).

---

## 🎨 ELEMENTOS QUE DEBEN SER IDÉNTICOS A LA LANDING

### 1. SECCIÓN DE WAITLIST (Registro)

**Diseño exacto de la landing:**
- Fondo: `linear-gradient(135deg, #44c0ff 0%, #2563eb 100%)`
- Texto principal: Blanco, 42px, peso 900
- Emoji del delfín: 🐬 (64px)
- Card interna: fondo blanco con padding 32px
- Emoji objetivo: 🎯 (48px)
- Inputs: altura 52px, border 2px, border-radius 12px
- Botón: fondo `linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)`
- Box informativo: fondo `#f0f9ff`, border-left 4px `#2563eb`

**Lista de características:**
- ✅ Gestión de reservas
- ✅ Gestión de habitaciones o propiedades
- ✅ Exportación de datos (CSV/Excel)
- ✅ Panel de administración
- ✅ Soporte por email
- ✅ App móvil (iOS y Android próximamente)
- 🔗 Crea enlaces de pago personalizados
- 🌐 Microsite para reservas directas
- 💡 Financiado con anuncios
- 🎁 Los primeros usuarios: acceso permanente sin coste mensual
- ❌ **No incluye:** Check-in digital (2€/mes) ni envío al Ministerio del Interior

### 2. POPUP DE WAITLIST

**IMPORTANTE:** Hay DOS variantes de popup. Usa esta:

**Popup Simple "¿Te interesa Delfín Check-in?"**
- Fondo overlay: `rgba(15,23,42,.6)` con `backdrop-filter: blur(4px)`
- Card popup: blanco, border-radius 20px, padding 40px
- Emoji delfín: 🐬 en azul claro
- Título: "¿Te interesa Delfín Check-in?" en azul (`#2563eb`), 28px
- Descripción breve
- Formulario con mismo diseño que el inline
- Botón de cierre (×) en top-right
- Animación `fadeIn` para overlay y `slideUp` para contenido

**Condiciones para mostrar:**
- Después de 20 segundos en la página
- O al alcanzar 50% de scroll (lo que ocurra primero)
- Solo si no se cerró anteriormente (check localStorage)

### 3. FAQs (TODAS LAS 26 PREGUNTAS)

**Lista completa de preguntas (en orden):**

1. ¿Es realmente gratis?
2. ¿Es gratis para siempre?
3. ¿Necesito tarjeta?
4. ¿Pueden cambiar las funciones del plan gratuito?
5. ¿Qué pasa si más adelante hay nuevos planes?
6. ¿Cómo funciona el módulo de check-in digital?
7. ¿Cómo se hace el check-in online?
8. ¿Puedo exportar datos para la asesoría y la renta?
9. ¿Cómo funciona el registro de viajeros?
10. ¿Qué idiomas soporta el sistema?
11. ¿Qué incluye el módulo de check-in digital?
12. ¿Qué incluye el Plan Gratuito (Básico) y qué no?
13. ¿Qué seguridad tienen los datos de mis huéspedes?
14. ¿Puedo personalizar el formulario de check-in?
15. ¿Puedo exportar mis datos?
16. ¿Qué pasa si no tengo internet? 📶
17. ¿Hay límite en el número de huéspedes o reservas?
18. ¿Cuándo estará disponible el módulo de check-in?
19. ¿Puedo probar el sistema?
20. ¿Qué soporte técnico incluye?
21. ¿Tienen programa de referidos?
22. ¿Tienen programa de afiliados?
23. ¿Cuál es la diferencia entre el programa de referidos y el de afiliados?
24. ¿Puedo participar en ambos programas a la vez?
25. ¿Cuándo empiezo a recibir recompensas o comisiones?
26. ¿Cómo consigo mi link de referido o afiliado?

**Diseño:**
- `<details>` con fondo blanco
- Border 1px solid `var(--border)`
- Border-radius 12px
- Padding 16px 20px
- Margin-bottom 12px
- Summary: font-weight 600, font-size 17px
- Icono + para cerrado, − para abierto (color azul)

---

## 📊 SEO Y OPTIMIZACIÓN PARA IAs

### Meta Tags Obligatorios

```html
<!-- Básicos -->
<title>{{ARTICLE_TITLE}} | Delfín Check-in</title>
<meta name="description" content="{{META_DESCRIPTION - MAX 160 CARACTERES}}">
<meta name="keywords" content="{{KEYWORDS_SEPARADAS_POR_COMAS}}">
<link rel="canonical" href="https://delfincheckin.com/articulos/{{ARTICLE_SLUG}}">

<!-- Open Graph (Facebook) -->
<meta property="og:type" content="article">
<meta property="og:url" content="https://delfincheckin.com/articulos/{{ARTICLE_SLUG}}">
<meta property="og:title" content="{{ARTICLE_TITLE}}">
<meta property="og:description" content="{{META_DESCRIPTION}}">
<meta property="og:image" content="https://delfincheckin.com/og-image.svg">
<meta property="article:published_time" content="{{PUBLISHED_DATE}}">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ARTICLE_TITLE}}">
<meta name="twitter:description" content="{{META_DESCRIPTION}}">

<!-- SEO Avanzado -->
<meta name="author" content="Delfín Check-in">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="language" content="Spanish">
<meta name="geo.region" content="ES">
```

### Schema.org JSON-LD (Obligatorio)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{ARTICLE_TITLE}}",
  "description": "{{META_DESCRIPTION}}",
  "image": "https://delfincheckin.com/og-image.svg",
  "author": {
    "@type": "Organization",
    "name": "Delfín Check-in",
    "url": "https://delfincheckin.com"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Delfín Check-in",
    "logo": {
      "@type": "ImageObject",
      "url": "https://delfincheckin.com/og-image.svg"
    }
  },
  "datePublished": "{{PUBLISHED_DATE}}",
  "dateModified": "{{MODIFIED_DATE}}",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://delfincheckin.com/articulos/{{ARTICLE_SLUG}}"
  }
}
```

---

## 🎯 ESTRUCTURA DE CONTENIDO

### Plantilla de Estructura Obligatoria

```html
<h1>{{TÍTULO_PRINCIPAL}}</h1>

<p>Introducción: Por qué este tema es importante para propietarios de alquiler vacacional.</p>

<h2>Marco legal aplicable en España</h2>
<p>Explicación clara de la normativa (RD 933/2021, Ley Orgánica, etc.)</p>

<h3>Subsección específica</h3>
<p>Desarrollo del marco legal</p>

<h2>Errores/Situaciones más comunes</h2>
<h3>Error 1: Título descriptivo</h3>
<p>Explicación del error</p>
<p><strong>Consecuencia:</strong> Qué pasa si cometes este error</p>

<h3>Error 2: Título descriptivo</h3>
<p>Explicación del error</p>

<!-- Repetir para cada error/situación -->

<h2>Consecuencias reales</h2>
<p>Multas, tiempos, riesgos (SIN ALARMISMOS, con datos oficiales)</p>

<h2>Buenas prácticas actuales</h2>
<ul>
  <li>Práctica 1</li>
  <li>Práctica 2</li>
</ul>

<h2>Conclusión</h2>
<p>Cierre preventivo y educativo (NO VENDER DIRECTAMENTE)</p>
```

### Elementos Visuales Recomendados

**Highlight Box (Información Importante):**
```html
<div class="highlight-box">
  <h3>⚖️ Título</h3>
  <p>Contenido importante</p>
</div>
```

**Warning Box (Advertencias):**
```html
<div class="warning-box">
  <h3>⚠️ Título de advertencia</h3>
  <ul>
    <li>Punto 1</li>
    <li>Punto 2</li>
  </ul>
</div>
```

---

## 🔧 TRACKING Y ANALYTICS

### Eventos que se trackean automáticamente:
- `page_view`: Al cargar la página
- `scroll`: Cada vez que el usuario hace scroll
- `click`: Todos los clics en la página
- `popup_view`: Cuando se muestra el popup
- `popup_close`: Cuando se cierra el popup
- `popup_click`: Cuando se hace clic en el CTA del popup
- `form_start`: Cuando se empieza a rellenar el formulario
- `form_submit`: Cuando se envía el formulario
- `exit`: Al salir de la página

### Source del Lead

Todos los leads se guardan con:
```
source: "article:{{ARTICLE_SLUG}}"
```

Ejemplo: `source: "article:multas-por-no-registrar-viajeros-espana"`

---

## ✍️ GUÍA DE REDACCIÓN

### Tono y Estilo

1. **Lenguaje claro y accesible** (no jurídico complejo)
2. **Tono informativo y preventivo** (sin alarmismos)
3. **100% legal** (basado en normativa real)
4. **Educativo** (no vender directamente)
5. **Profesional pero cercano**

### Palabras y Frases Prohibidas

❌ NO usar:
- "¡Cuidado! Podrías enfrentarte a..."
- "Evita sanciones millonarias..."
- "Urgente: necesitas..."
- "La solución definitiva es..."
- "Contrata nuestro servicio para..."

✅ SÍ usar:
- "Según el RD 933/2021..."
- "Los importes oficiales son..."
- "La mejor práctica actual es..."
- "Para cumplir con la normativa..."
- "Recomendaciones preventivas..."

### Ejemplos de Buena Redacción

**Malo:**
> "¡Cuidado! Si no registras a tus huéspedes podrías enfrentarte a multas de hasta 600.000€. No te arriesgues, contrata nuestro software ahora."

**Bueno:**
> "El RD 933/2021 establece sanciones que oscilan entre 100€ y 600.000€, dependiendo de la gravedad del incumplimiento. La mayoría de infracciones por parte de pequeños propietarios se consideran leves (100-600€) o graves (601-30.000€). Para evitar problemas, la mejor práctica es implementar un sistema de registro desde el primer momento."

---

## 📝 CHECKLIST ANTES DE PUBLICAR

Antes de crear un nuevo artículo, verifica:

- [ ] Título optimizado para SEO (máx 60 caracteres)
- [ ] Meta descripción atractiva (máx 160 caracteres)
- [ ] 3-5 keywords relevantes identificadas
- [ ] Contenido 100% legal (citas a normativa oficial)
- [ ] Estructura H1 > H2 > H3 correcta
- [ ] Sección de waitlist IDÉNTICA a la landing
- [ ] Popup con mismo diseño que la landing
- [ ] 26 FAQs completas incluidas
- [ ] Schema.org JSON-LD configurado
- [ ] Slug amigable y descriptivo
- [ ] Tracking JavaScript implementado
- [ ] Responsive design verificado
- [ ] Links internos a otros artículos (si aplica)
- [ ] Revisión ortográfica y gramatical
- [ ] Tiempo de lectura estimado (5-7 min ideal)

---

## 🚀 PROCESO DE PUBLICACIÓN

1. **Crear archivo HTML** en `delfincheckin.com/articulos/{{slug}}.html`
2. **Registrar en el CMS** (`/superadmin/blog-manager`)
3. **Probar en local** (verificar popup, formularios, tracking)
4. **Push a GitHub** del repo `delfincheckin.com`
5. **Verificar en producción** (https://delfincheckin.com/articulos/{{slug}})
6. **Indexar en Google Search Console**
7. **Monitorear métricas** en `/superadmin/blog-analytics`

---

## 📞 CONTACTO

Si tienes dudas sobre cómo crear un artículo:
- Email: contacto@delfincheckin.com
- Revisa el artículo ejemplo: `multas-por-no-registrar-viajeros-espana.html`

---

**Última actualización:** 18 de enero de 2026  
**Versión:** 1.0
