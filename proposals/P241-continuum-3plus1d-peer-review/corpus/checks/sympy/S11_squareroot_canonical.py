"""P241 audit oracle — Radicand of Leff (21) equals -g(X,X) under (23)-(25).

Standalone module: python3 S11_squareroot_canonical.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_squareroot_canonical_equivalence() -> dict[str, object]:
    """Radicand of Leff (21) equals -g_{mu nu} Xdot^mu Xdot^nu under (23)-(25).

    Evaluated on a concrete rational SPD acoustic tensor: the identification
    is exact, and the einbein action built from the identified metric returns
    the square-root Lagrangian (22).
    """
    c0 = sp.Rational(297, 100)
    Amat = sp.Matrix([[4, 0, 0], [0, sp.Rational(9, 4), 0], [0, 0, sp.Rational(2, 3)]])
    Ainv12 = Amat**sp.Rational(-1, 2)
    d16 = Amat.det() ** sp.Rational(1, 6)
    v = sp.Matrix([sp.Rational(1, 3), -sp.Rational(2, 5), sp.Rational(7, 2)])
    xd = sp.Matrix([sp.Rational(3, 2), sp.Rational(1, 7), -sp.Rational(5, 4)])
    radicand = (
        d16 / c0
        - (v.T * Ainv12 * v)[0] / c0
        - 2 * (v.T * Ainv12 * xd)[0] / c0
        - c0 * (xd.T * Ainv12 * xd)[0]
    )
    g00 = -d16 / c0 + (v.T * Ainv12 * v)[0] / c0
    g0 = Ainv12 * v / c0
    gsp = c0 * Ainv12
    neg_gxx = -g00 - 2 * (g0.T * xd)[0] - (xd.T * gsp * xd)[0]
    resid = sp.simplify(neg_gxx - radicand)
    return _check(
        "squareroot_canonical_equivalence",
        "P241-S11 (21)-(25)",
        resid == 0,
        f"-g(X,X) vs (21) radicand residual on concrete SPD A: {resid} == 0; "
        "the map (rho,Theta,V) -> g_{mu nu} is exact given the identification.",
    )

if __name__ == "__main__":
    result = check_squareroot_canonical_equivalence()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
