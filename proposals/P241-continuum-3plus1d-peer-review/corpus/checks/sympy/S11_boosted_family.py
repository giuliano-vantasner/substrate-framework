"""P241 audit oracle — Boost-closed-family Legendre derivation of the square-root form.

Standalone module: python3 S11_boosted_family.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_boosted_family_squareroot() -> dict[str, object]:
    """Boost-closed-family derivation of the square-root form.

    Given a boost-closed lump family with E = gamma*E0, p = gamma*E0*v/c0^2,
    the Legendre transform L = p.v - E = -E0/gamma = -(E0/c0)*sqrt(c0^2-v^2):
    the canonical square-root form follows exactly (any spatial dimension).
    """
    v, E0v, c0 = sp.symbols("v E_0 c_0", positive=True)
    gamma = 1 / sp.sqrt(1 - v**2 / c0**2)
    E_expr = gamma * E0v
    p_expr = gamma * E0v * v / c0**2
    L_legendre = sp.simplify(p_expr * v - E_expr)
    ok = sp.simplify(L_legendre + E0v / gamma) == 0
    ok2 = sp.simplify(L_legendre + (E0v / c0) * sp.sqrt(c0**2 - v**2)) == 0
    return _check(
        "boosted_family_squareroot",
        "P241-S11 conditional reduction support",
        bool(ok and ok2),
        "L = p*v - E = -E0/gamma exactly for any boost-closed family with "
        "E=gamma*E0, p=gamma*E0*v/c0^2: supplies the conditional square-root "
        "derivation the manuscript asserts; inhomogeneous corrections are "
        "O(ell/L) (quantified by scipy corpus N05/RP2).",
    )

if __name__ == "__main__":
    result = check_boosted_family_squareroot()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
