#!/usr/bin/env python3
"""
Translate en/index.html clones (it/pt/fr/fi) using Google Translate (deep-translator).
Run from repo root: . .venv-translate/bin/activate && python3 scripts/translate_home.py it
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString
from deep_translator import GoogleTranslator

SKIP_TAGS = frozenset({"script", "style", "noscript"})

META_NAMES_TRANSLATE = {
    "description",
    "keywords",
    "abstract",
    "summary",
    "topic",
    "news_keywords",
    "language",
    "twitter:title",
    "twitter:description",
    "twitter:image:alt",
    "msapplication-tooltip",
    "DC.title",
}

META_PROP_TRANSLATE = {
    "og:title",
    "og:description",
    "og:image:alt",
    "og:site_name",
    "article:author",
}


def should_translate_meta(meta) -> bool:
    name = (meta.get("name") or "").lower()
    prop = meta.get("property") or ""
    if name in META_NAMES_TRANSLATE:
        return True
    if prop in META_PROP_TRANSLATE:
        return True
    if prop.startswith("article:") and "tag" in prop:
        return True
    return False


def should_translate_json_str(s: str) -> bool:
    if not isinstance(s, str) or len(s) < 4:
        return False
    if "http://" in s or "https://" in s or s.startswith("/") or s.startswith("@"):
        return False
    if re.fullmatch(r"[\d\s€$.,:%\-–]+", s):
        return False
    return True


def translate_json(obj, translator, cache: dict):
    if isinstance(obj, dict):
        return {k: translate_json(v, translator, cache) for k, v in obj.items()}
    if isinstance(obj, list):
        return [translate_json(v, translator, cache) for v in obj]
    if isinstance(obj, str):
        if not should_translate_json_str(obj):
            return obj
        if obj in cache:
            return cache[obj]
        try:
            out = translator.translate(obj)
            cache[obj] = out
            time.sleep(0.08)
        except Exception:
            cache[obj] = obj
            return obj
        return out
    return obj


def batch_translate(strings: list[str], translator, batch_size: int = 45) -> dict[str, str]:
    mapping: dict[str, str] = {}
    total_batches = (len(strings) + batch_size - 1) // batch_size
    for i in range(0, len(strings), batch_size):
        chunk = strings[i : i + batch_size]
        bn = i // batch_size + 1
        print(f"  Lote {bn}/{total_batches} ({len(chunk)} cadenas)...", flush=True)
        try:
            out = translator.translate_batch(chunk)
            if not out or len(out) != len(chunk):
                raise ValueError("batch length mismatch")
            for a, b in zip(chunk, out):
                mapping[a] = b if b is not None and str(b).strip() != "" else a
        except Exception:
            for s in chunk:
                try:
                    t = translator.translate(s)
                    mapping[s] = t if t is not None and str(t).strip() != "" else s
                    time.sleep(0.12)
                except Exception:
                    mapping[s] = s
        time.sleep(0.35)
    return mapping


def collect_unique_strings(soup: BeautifulSoup) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []

    def add(s: str) -> None:
        t = s
        if len(t.strip()) < 2:
            return
        if t in seen:
            return
        seen.add(t)
        out.append(t)

    for el in soup.descendants:
        if not isinstance(el, NavigableString) or isinstance(el, Comment):
            continue
        if el.parent and el.parent.name in SKIP_TAGS:
            continue
        add(str(el))

    for meta in soup.find_all("meta"):
        if not should_translate_meta(meta):
            continue
        c = meta.get("content")
        if c and len(c.strip()) > 1:
            add(c)

    for tag in soup.find_all(True):
        for attr in ("alt", "aria-label", "title", "placeholder"):
            v = tag.get(attr)
            if v and len(v.strip()) > 2:
                add(v)

    out.sort(key=len, reverse=True)
    return out


def apply_text_mapping(soup: BeautifulSoup, mapping: dict[str, str]) -> None:
    def safe(m: dict[str, str], key: str) -> str:
        v = m.get(key, key)
        return key if v is None or str(v).strip() == "" else v

    for el in soup.descendants:
        if not isinstance(el, NavigableString) or isinstance(el, Comment):
            continue
        if el.parent and el.parent.name in SKIP_TAGS:
            continue
        s = str(el)
        if s in mapping:
            el.replace_with(safe(mapping, s))

    for meta in soup.find_all("meta"):
        if not should_translate_meta(meta):
            continue
        c = meta.get("content")
        if c and c in mapping:
            meta["content"] = safe(mapping, c)

    for tag in soup.find_all(True):
        for attr in ("alt", "aria-label", "title", "placeholder"):
            v = tag.get(attr)
            if v and v in mapping:
                tag[attr] = safe(mapping, v)


def process_ld_json(soup: BeautifulSoup, translator, lang: str) -> None:
    cache: dict[str, str] = {}
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string
        if not raw or not raw.strip():
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        data = translate_json(data, translator, cache)
        script.string = json.dumps(data, ensure_ascii=False, indent=2)


def fix_locale_urls(html: str, from_prefix: str, to_prefix: str) -> str:
    """from_prefix e.g. https://delfincheckin.com/en/ -> https://delfincheckin.com/it/"""
    return html.replace(from_prefix, to_prefix).replace(
        "https://delfincheckin.com/en#", "https://delfincheckin.com" + to_prefix.rstrip("/") + "#"
    )


LOCALE_META = {
    "it": ("it-IT", "it_IT"),
    "pt": ("pt-PT", "pt_PT"),
    "fr": ("fr-FR", "fr_FR"),
    "fi": ("fi-FI", "fi_FI"),
}


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: translate_home.py <it|pt|fr|fi>")
        sys.exit(1)
    lang = sys.argv[1].lower()
    targets = {"it": "it", "pt": "pt", "fr": "fr", "fi": "fi"}
    if lang not in targets:
        print("Unsupported lang")
        sys.exit(1)
    cl, og_loc = LOCALE_META[lang]

    root = Path(__file__).resolve().parent.parent
    src = root / "en" / "index.html"
    dest = root / lang / "index.html"
    if not src.is_file():
        print("Missing", src)
        sys.exit(1)

    html = src.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    translator = GoogleTranslator(source="en", target=targets[lang])

    strings = collect_unique_strings(soup)
    print(f"Unique strings: {len(strings)}")
    mapping = batch_translate(strings, translator)
    apply_text_mapping(soup, mapping)
    print("  JSON-LD (schema.org)...", flush=True)
    process_ld_json(soup, translator, lang)

    html_el = soup.find("html")
    if html_el:
        html_el["lang"] = lang

    out = str(soup)
    if not out.lstrip().startswith("<!DOCTYPE"):
        out = "<!DOCTYPE html>\n" + out
    out = fix_locale_urls(out, "https://delfincheckin.com/en/", f"https://delfincheckin.com/{lang}/")
    out = out.replace('content="/en/"', f'content="/{lang}/"')
    out = out.replace("content='/en/'", f"content='/{lang}/'")
    out = re.sub(
        r'<meta http-equiv="content-language" content="[^"]*">',
        f'<meta http-equiv="content-language" content="{cl}">',
        out,
        count=1,
    )
    out = re.sub(
        r'<meta property="og:locale" content="[^"]*">',
        f'<meta property="og:locale" content="{og_loc}">',
        out,
        count=1,
    )

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
    print("Wrote", dest)


if __name__ == "__main__":
    main()
