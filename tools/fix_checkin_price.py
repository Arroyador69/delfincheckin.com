#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path


REPLACEMENTS: list[tuple[str, str]] = [
    # ES
    ("2€/mes", "2€/mes"),
    ("2 € al mes", "2 € al mes"),
    ("2€ al mes", "2€ al mes"),
    ("2 €/mes", "2 €/mes"),
    # EN
    ("€2/month", "€2/month"),
    ("€2/mo", "€2/mo"),
    ("2 €/month", "2 €/month"),
    # FR
    ("2 €/mois", "2 €/mois"),
    ("2 € par mois", "2 € par mois"),
    ("2 €/mois", "2 €/mois"),  # NBSP variant
    # IT
    ("2€/mese", "2€/mese"),
    ("€2/mese", "€2/mese"),
    ("2€ al mese", "2€ al mese"),
    # PT
    ("2€/mês", "2€/mês"),
    ("2€ por mês", "2€ por mês"),
    # FI
    ("2 €/kk", "2 €/kk"),
    ("2 € kuukaudessa", "2 € kuukaudessa"),
]


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if ".git" in parts:
        return True
    if "node_modules" in parts:
        return True
    return False


def is_text_candidate(path: Path) -> bool:
    # Keep this conservative—only files likely to contain copy.
    return path.suffix.lower() in {
        ".html",
        ".htm",
        ".json",
        ".md",
        ".txt",
        ".py",
        ".js",
        ".css",
        ".xml",
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    changed_files = 0
    total_replacements = 0

    for root, dirs, files in os.walk(repo_root):
        root_path = Path(root)
        # prune dirs
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules"}]

        for name in files:
            p = root_path / name
            if should_skip(p) or not is_text_candidate(p):
                continue

            try:
                data = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            except OSError:
                continue

            new_data = data
            file_repl = 0
            for a, b in REPLACEMENTS:
                if a in new_data:
                    count = new_data.count(a)
                    new_data = new_data.replace(a, b)
                    file_repl += count

            if new_data != data:
                p.write_text(new_data, encoding="utf-8")
                changed_files += 1
                total_replacements += file_repl

    print(f"Updated {changed_files} files with {total_replacements} replacements.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

