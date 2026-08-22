"""P241 audit oracle — Einbein constraint (27) and recovery of the square root (26).

Standalone module: python3 S12_einbein_constraint.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_einbein_constraint() -> dict[str, object]:
    """Einbein constraint (27) and recovery of the square root (26)."""
    e, sig, M0, c0 = sp.symbols("e sigma M_0 c_0", positive=True, real=True)
    sig_real = sp.Symbol("sigma", real=True)
    L = sig_real / (2 * e) - e * (M0 * c0) ** 2 / 2
    constraint = sp.simplify(sp.diff(L, e) * (-2 * e**2))
    # constraint == sigma + e^2 (M0 c0)^2:
    ok_constraint = sp.simplify(constraint - (sig_real + e**2 * (M0 * c0) ** 2)) == 0
    e_root = sp.sqrt(-sig_real) / (M0 * c0)
    L_sub = sp.simplify(L.subs(e, e_root))
    ok_recover = sp.simplify(L_sub + M0 * c0 * sp.sqrt(-sig_real)) == 0
    return _check(
        "einbein_constraint_exact",
        "P241-S12 (26)-(27)",
        ok_constraint and ok_recover,
        "dL/de=0 <=> sigma + e^2(M0 c0)^2 = 0; substituting e=sqrt(-sigma)/(M0 c0) "
        "returns L = -M0*c0*sqrt(-sigma): square-root form recovered exactly.",
    )

if __name__ == "__main__":
    result = check_einbein_constraint()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
