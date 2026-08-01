#!/usr/bin/env python3
"""Render canonical documentation from the accepted claim registry."""

from __future__ import annotations

import argparse
from pathlib import Path

from substrate_framework.governance import load_yaml, render_claim_index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated output is stale")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    registry = load_yaml(root / "governance" / "claims.yaml")
    target = root / "docs" / "generated" / "claim-index.md"
    rendered = render_claim_index(registry)
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != rendered:
            raise SystemExit("generated claim index is stale; run scripts/render_docs.py")
    else:
        target.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
