#!/usr/bin/env node
/**
 * Limpieza segura de waitlist en artículos ya publicados.
 *
 * Enfoque:
 * - NO regex global que pueda “comerse” HTML.
 * - Eliminación por bloques con balanceo básico de tags.
 * - Dry-run por defecto. Solo escribe con --write.
 * - Validaciones: preserva el contenido del artículo y evita reducciones excesivas.
 *
 * Quita:
 * - <section id="registro" ...>...</section> (waitlist legacy)
 * - Bloques popupWaitlist / popup-overlay legacy
 * - <script>...</script> que contenga /blog/waitlist o waitlistForm/popupWaitlist (solo ese script)
 */
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const articlesDir = path.join(root, 'articulos');

const WRITE = process.argv.includes('--write');
const TARGET = process.argv.find((a) => a.startsWith('--file='))?.slice('--file='.length);

function findAllScriptBlocks(html) {
  const blocks = [];
  let i = 0;
  while (true) {
    const start = html.indexOf('<script', i);
    if (start === -1) break;
    const startEnd = html.indexOf('>', start);
    if (startEnd === -1) break;
    const end = html.indexOf('</script>', startEnd + 1);
    if (end === -1) break;
    blocks.push({ start, end: end + '</script>'.length });
    i = end + '</script>'.length;
  }
  return blocks;
}

function removeScriptsByPredicate(html, predicate) {
  const blocks = findAllScriptBlocks(html);
  if (blocks.length === 0) return { html, removed: 0 };

  let removed = 0;
  let out = '';
  let last = 0;
  for (const b of blocks) {
    const chunk = html.slice(b.start, b.end);
    if (predicate(chunk)) {
      out += html.slice(last, b.start);
      last = b.end;
      removed++;
    }
  }
  out += html.slice(last);
  return { html: out, removed };
}

function removeSectionByIdRegistro(html) {
  const needle = 'id="registro"';
  let idx = html.indexOf(needle);
  if (idx === -1) idx = html.indexOf("id='registro'");
  if (idx === -1) return { html, removed: 0 };

  // Buscar el inicio del <section ...> que contiene id="registro"
  const start = html.lastIndexOf('<section', idx);
  if (start === -1) return { html, removed: 0 };
  const openEnd = html.indexOf('>', start);
  if (openEnd === -1) return { html, removed: 0 };

  // Balanceo simple de <section ...> ... </section>
  // Ya estamos en un <section ...> (depth=1). Buscamos su cierre correspondiente.
  let depth = 1;
  let pos = openEnd + 1;
  while (pos < html.length) {
    const nextOpen = html.indexOf('<section', pos);
    const nextClose = html.indexOf('</section>', pos);
    if (nextClose === -1) break;
    if (nextOpen !== -1 && nextOpen < nextClose) {
      depth++;
      pos = nextOpen + 8;
      continue;
    }
    // close
    depth--;
    const end = nextClose + '</section>'.length;
    if (depth === 0) {
      // Guardarraíl: solo borramos si el bloque contiene señales claras de la waitlist legacy.
      const block = html.slice(start, end).toLowerCase();
      const isWaitlist =
        block.includes('lista de espera') ||
        block.includes('waitlistform') ||
        block.includes('quiero acceso anticipado') ||
        block.includes('acceso permanente');
      if (!isWaitlist) return { html, removed: 0 };

      const before = html.slice(0, start);
      const after = html.slice(end);
      return { html: before + after, removed: 1 };
    }
    pos = end;
  }
  return { html, removed: 0 };
}

function removePopupOverlay(html) {
  // Quitar el overlay legacy por id popupWaitlist (si existe). Está dentro de un div grande.
  let idx = html.indexOf('id="popupWaitlist"');
  if (idx === -1) idx = html.indexOf("id='popupWaitlist'");
  if (idx === -1) return { html, removed: 0 };

  // Buscar el inicio del div contenedor del overlay.
  const start = html.lastIndexOf('<div', idx);
  if (start === -1) return { html, removed: 0 };
  const openEnd = html.indexOf('>', start);
  if (openEnd === -1) return { html, removed: 0 };

  // Balanceo simple de <div ...> ... </div>
  let depth = 0;
  let pos = start;
  while (pos < html.length) {
    const nextOpen = html.indexOf('<div', pos);
    const nextClose = html.indexOf('</div>', pos);
    if (nextClose === -1) break;
    if (nextOpen !== -1 && nextOpen < nextClose) {
      depth++;
      pos = nextOpen + 4;
      continue;
    }
    if (depth === 0) {
      const end = nextClose + '</div>'.length;
      const before = html.slice(0, start);
      const after = html.slice(end);
      return { html: before + after, removed: 1 };
    }
    depth--;
    pos = nextClose + 6;
  }
  return { html, removed: 0 };
}

function validateNotDestroyed(before, after) {
  // Debe seguir existiendo el wrapper del contenido del artículo
  const mustHave = [
    '<div class="article-content">',
    '<header>',
    '<footer',
  ];
  for (const s of mustHave) {
    if (!after.includes(s)) return `Falta bloque obligatorio: ${s}`;
  }

  // El texto del artículo no debe desaparecer: la article-content debería seguir conteniendo al menos un <p> o <h2>
  const beforeIdx = before.indexOf('<div class="article-content">');
  const afterIdx = after.indexOf('<div class="article-content">');
  if (beforeIdx === -1 || afterIdx === -1) return 'No se pudo localizar article-content.';

  const afterSlice = after.slice(afterIdx, afterIdx + 5000);
  if (!/<p\b|<h2\b|<h3\b/i.test(afterSlice)) return 'El contenido del artículo parece vacío tras la limpieza.';

  // Evitar reducciones demasiado grandes (señal de borrado accidental)
  const ratio = after.length / Math.max(1, before.length);
  if (ratio < 0.6) return `Reducción excesiva de HTML (${Math.round(ratio * 100)}%). Aborto.`;

  return null;
}

function stripWaitlistSafe(html) {
  let out = String(html);
  let removed = { section: 0, popup: 0, scripts: 0 };

  // 1) Sección legacy #registro
  {
    const r = removeSectionByIdRegistro(out);
    out = r.html;
    removed.section += r.removed;
  }

  // 2) Popup overlay legacy
  {
    const r = removePopupOverlay(out);
    out = r.html;
    removed.popup += r.removed;
  }

  // 3) Scripts waitlist (solo script blocks que contienen esas cadenas)
  {
    const r = removeScriptsByPredicate(out, (chunk) => {
      const c = chunk.toLowerCase();
      return c.includes('/blog/waitlist') || c.includes('waitlistform') || c.includes('popupwaitlist');
    });
    out = r.html;
    removed.scripts += r.removed;
  }

  // Limpieza ligera de huecos
  out = out.replace(/\n{5,}/g, '\n\n\n');
  return { html: out, removed };
}

function main() {
  if (!fs.existsSync(articlesDir)) {
    console.error('No existe:', articlesDir);
    process.exit(1);
  }

  const files = TARGET
    ? [path.isAbsolute(TARGET) ? TARGET : path.join(root, TARGET)]
    : fs
        .readdirSync(articlesDir)
        .filter((f) => f.endsWith('.html') && f !== '_template.html')
        .map((f) => path.join(articlesDir, f));

  let modified = 0;
  let skipped = 0;
  for (const file of files) {
    const before = fs.readFileSync(file, 'utf8');
    const { html: after, removed } = stripWaitlistSafe(before);
    const changed = after !== before;

    if (!changed) continue;

    const err = validateNotDestroyed(before, after);
    if (err) {
      skipped++;
      console.error(`[SKIP] ${path.basename(file)}: ${err}`);
      continue;
    }

    modified++;
    const msg = `[OK] ${path.basename(file)} removed: section=${removed.section} popup=${removed.popup} scripts=${removed.scripts}`;
    console.log(msg);

    if (WRITE) {
      fs.writeFileSync(file, after, 'utf8');
    }
  }

  console.log(`\nResumen: candidatos=${files.length} modificados=${modified} skipped=${skipped} modo=${WRITE ? 'WRITE' : 'DRY-RUN'}`);
  if (!WRITE) {
    console.log('Para escribir cambios: node scripts/remove-waitlist-from-articles.js --write');
  }
}

main();

