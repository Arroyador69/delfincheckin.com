#!/usr/bin/env python3
"""
Obsoleto: antes insertaba el bloque «Polar / Ver planes» y reescribía #registro.

El flujo actual está en `apply-landing-free-and-polar-cleanup.py` (mismo directorio tools/):
formulario plan gratuito → API `signup-free`, enlaces de pago → `subscribe-redirect`, CTAs gratis → `#registro`.
"""

from __future__ import annotations

import sys


def main() -> None:
    print(
        "sync-landing-polar.py ya no se ejecuta (evita reintroducir el bloque Polar).\n"
        "Usa en su lugar: python3 tools/apply-landing-free-and-polar-cleanup.py",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
