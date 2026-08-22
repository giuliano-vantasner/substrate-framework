"""Shared helpers for the P241 SymPy audit modules."""

from __future__ import annotations


def _check(name: str, claim: str, ok: bool, detail: str) -> dict[str, object]:
    return {"name": name, "claim": claim, "passed": bool(ok), "detail": detail}
