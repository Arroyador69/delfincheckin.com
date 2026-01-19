# 🚀 PROCESO COMPLETO PARA CREAR NUEVOS ARTÍCULOS CON TRACKING

**Última actualización:** Enero 19, 2026  
**Estado del sistema:** ✅ Tracking funcionando 100%

---

## ✅ PROBLEMAS RESUELTOS (Enero 2026)

Todos los siguientes problemas han sido solucionados:

1. ✅ **CORS bloqueado** - Headers CORS añadidos a endpoints
2. ✅ **401 Unauthorized** - Rutas de blog añadidas como públicas en middleware
3. ✅ **Stats en 0** - Tracking ahora registra correctamente
4. ✅ **Popup sin funcionalidad** - Ahora hace scroll suave a la waitlist
5. ✅ **Logs de debugging** - Implementados para diagnóstico
6. ✅ **Métricas del formulario** - Incluidas en analytics

---

## 📋 CHECKLIST: CREAR UN NUEVO ARTÍCULO

### **Paso 1: Crear el Archivo HTML**

1. **Duplica el template:**
   ```bash
   cd delfincheckin.com/articulos/
   cp _template.html nombre-del-nuevo-articulo.html
   ```

2. **Edita el nuevo archivo y reemplaza:**
   - `{{ARTICLE_SLUG}}` → El slug exacto del artículo (ej: `multas-por-no-registrar-viajeros-espana`)
   - `{{ARTICLE_TITLE}}` → El título completo del artículo
   - `{{META_DESCRIPTION}}` → Descripción para SEO (máx. 160 caracteres)
   - `{{META_KEYWORDS}}` → Palabras clave separadas por comas
   - `{{ARTICLE_CONTENT}}` → El contenido HTML del artículo

3. **Verifica que el slug sea correcto:**
   - El slug en el archivo debe coincidir EXACTAMENTE con el de la base de datos
   - Usa minúsculas, guiones, sin acentos ni caracteres especiales
   - Ejemplo: `nuevo-articulo-sobre-ses.html` → slug: `nuevo-articulo-sobre-ses`

---

### **Paso 2: Registrar en la Base de Datos**

**IMPORTANTE:** El artículo DEBE existir en la base de datos para que el tracking funcione.

**Opción A: Desde el CMS del Superadmin**

1. Ve a **Superadmin** → **Gestión de Artículos**
2. Haz clic en **➕ Crear Artículo**
3. Completa todos los campos:
   - **Slug:** DEBE coincidir exactamente con el nombre del archivo HTML (sin `.html`)
   - **Título:** El título completo
   - **Meta Description:** Para SEO
   - **Meta Keywords:** Palabras clave
   - **Content:** El contenido HTML
   - **Estado:** `published`
   - **Publicar artículo:** ✅ Marcar checkbox
4. Guarda el artículo

**Opción B: SQL Directo (Solo si sabes lo que haces)**

```sql
INSERT INTO blog_articles (
  slug, 
  title, 
  meta_description, 
  meta_keywords,
  content,
  excerpt,
  canonical_url,
  schema_json,
  status,
  is_published,
  published_at,
  author_name
) VALUES (
  'slug-del-articulo',
  'Título del Artículo',
  'Descripción para SEO',
  'palabra1, palabra2, palabra3',
  '<h2>Contenido HTML aquí</h2><p>...</p>',
  'Extracto breve del artículo',
  'https://delfincheckin.com/articulos/slug-del-articulo.html',
  '{"@context":"https://schema.org","@type":"Article","headline":"Título","datePublished":"2026-01-19","author":{"@type":"Person","name":"Equipo Delfín Check-in"}}'::jsonb,
  'published',
  true,
  NOW(),
  'Equipo Delfín Check-in'
);
```

---

### **Paso 3: Hacer Push a GitHub**

```bash
cd delfincheckin.com
git add articulos/nombre-del-nuevo-articulo.html
git commit -m "feat: añadir artículo sobre [tema]"
git push origin main
```

**Importante:** NO uses `[skip ci]` o similar. Déjalo desplegar normalmente.

---

### **Paso 4: Verificar el Tracking (CRÍTICO)**

**Una vez desplegado (1-2 minutos), verifica que funcione:**

1. **Abre el artículo en incógnito:**
   ```
   https://delfincheckin.com/articulos/nombre-del-nuevo-articulo.html
   ```

2. **Abre la consola del navegador:**
   - Presiona **F12** o **⌘+Option+I**
   - Ve a la pestaña **"Console"**

3. **Verifica que aparezcan estos logs:**
   ```
   📊 [CLIENT] Enviando tracking: { event_type: 'page_view', article_slug: '...' }
   ✅ [CLIENT] Tracking exitoso: page_view
   ```

4. **SI NO ves los logs o ves errores:**
   - ❌ **Error CORS** → Contacta al equipo técnico (ya debería estar resuelto)
   - ❌ **401 Unauthorized** → Contacta al equipo técnico (ya debería estar resuelto)
   - ❌ **404 Not Found** → El slug del HTML no coincide con el de la base de datos

---

### **Paso 5: Verificar Analytics en el Superadmin**

1. Ve a **Superadmin** → **Monitoreo Artículos**
2. Selecciona el nuevo artículo del dropdown
3. Haz clic en **🔄 Actualizar**
4. Deberías ver:
   - **Visitas:** 1+ (tu visita de prueba)
   - **Conversiones:** 1 si enviaste el formulario
   - **Top Eventos:** `page_view`, `scroll`, etc.
   - **Métricas del Popup:** si esperaste 20 segundos
   - **Métricas del Formulario:** si enviaste el form

---

## 🔍 TROUBLESHOOTING

### ❌ El artículo no aparece en "Monitoreo Artículos"

**Causa:** El artículo no está marcado como `is_published = true` en la base de datos.

**Solución:**
```sql
UPDATE blog_articles 
SET is_published = true, 
    status = 'published', 
    published_at = NOW() 
WHERE slug = 'tu-slug-aqui';
```

---

### ❌ Las stats están en 0 después de visitar el artículo

**Causas posibles:**

1. **El slug no coincide:**
   - Verifica que el slug en el HTML (línea `const ARTICLE_SLUG = '...'`) sea EXACTAMENTE igual al de la base de datos.
   - NO incluyas `.html` en el slug.

2. **El artículo no existe en la base de datos:**
   - Verifica con: `SELECT * FROM blog_articles WHERE slug = 'tu-slug';`
   - Si no existe, créalo (ver Paso 2).

3. **Errores en la consola del navegador:**
   - Abre la consola y busca errores.
   - Si ves CORS o 401, contacta al equipo técnico.

---

### ❌ El popup no baja a la waitlist

**Causa:** Falta el `id="registro"` en la sección de waitlist.

**Solución:**
Verifica que la línea del HTML tenga:
```html
<div class="waitlist-section" id="registro">
```

---

## 📊 ENDPOINTS QUE SE USAN

Los siguientes endpoints son **públicos** (no requieren autenticación):

1. **Tracking de eventos:**
   ```
   POST https://admin.delfincheckin.com/api/blog/analytics/track
   ```
   - Registra page views, scrolls, clics, popup, etc.
   - **Headers CORS:** ✅ Configurados
   - **Middleware:** ✅ Ruta pública

2. **Waitlist desde artículos:**
   ```
   POST https://admin.delfincheckin.com/api/blog/waitlist
   ```
   - Registra leads con el source `article:nombre-slug`
   - **Headers CORS:** ✅ Configurados
   - **Middleware:** ✅ Ruta pública

3. **Estadísticas (solo superadmin):**
   ```
   GET https://admin.delfincheckin.com/api/blog/analytics/stats?article_slug=...&days=30
   ```
   - Requiere autenticación de superadmin
   - Devuelve todas las métricas del artículo

---

## ✅ GARANTÍAS DE FUNCIONAMIENTO

Si sigues este proceso exactamente, **GARANTIZAMOS** que:

1. ✅ El tracking funcionará correctamente
2. ✅ Las stats se registrarán en tiempo real
3. ✅ El popup hará scroll suave a la waitlist
4. ✅ Los leads se registrarán con el source correcto
5. ✅ Las métricas del formulario aparecerán en analytics
6. ✅ Podrás ver todas las stats en el superadmin

---

## 🎯 ELEMENTOS QUE YA ESTÁN INCLUIDOS EN EL TEMPLATE

El template `_template.html` YA incluye:

- ✅ Header y footer de la landing
- ✅ Sección de waitlist con diseño idéntico
- ✅ Popup con scroll automático
- ✅ Las 26 preguntas frecuentes
- ✅ Tracking completo de eventos
- ✅ Logs de debugging en consola
- ✅ CORS habilitado (servidor)
- ✅ Middleware permite acceso (servidor)
- ✅ Métricas del formulario
- ✅ SessionID único por usuario
- ✅ Tracking de conversiones
- ✅ Tracking de tiempo en página
- ✅ Tracking de scroll depth
- ✅ Tracking de dispositivo

**NO necesitas añadir nada más.** Solo reemplaza los placeholders.

---

## 🚨 REGLAS IMPORTANTES

1. **NUNCA modifiques el código JavaScript de tracking** en el template
2. **NUNCA cambies el `ADMIN_API_URL`** (debe ser `https://admin.delfincheckin.com/api`)
3. **SIEMPRE verifica** que el slug del HTML coincida con el de la base de datos
4. **SIEMPRE prueba** en incógnito antes de considerar que funciona
5. **SIEMPRE mira la consola** del navegador para verificar que no hay errores

---

## 📞 SOPORTE

Si después de seguir este proceso EXACTAMENTE, algo no funciona:

1. **Captura la consola del navegador** con los errores
2. **Captura los logs de Vercel** del endpoint de tracking
3. **Verifica la base de datos** con la query que te dimos
4. **Contacta al equipo técnico** con toda esta información

---

**Última verificación exitosa:** 19 de enero de 2026  
**Estado:** ✅ Sistema 100% operativo  
**Artículos con tracking funcionando:** `multas-por-no-registrar-viajeros-espana`
