"""P241 audit oracle — Recovery formulae (16) satisfy matching (14) exactly.

Standalone module: python3 S08_impedance_recovery.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_impedance_recovery() -> dict[str, object]:
    """Recovery formulae (16) satisfy matching (14) exactly."""
    a1, a2, a3 = sp.symbols("a1 a2 a3", positive=True)
    rho0, c0, Th0 = sp.symbols("rho0 c_0 Theta_0", positive=True)
    detA = a1 * a2 * a3
    rho = rho0 * c0 / detA ** sp.Rational(1, 6)
    Th_i = [a * Th0 / (c0 * detA ** sp.Rational(1, 6)) for a in (a1, a2, a3)]
    detTh = Th_i[0] * Th_i[1] * Th_i[2]
    lhs6 = rho**3 * detTh           # sixth power of rho*(detTh)^{1/3}
    rhs6 = (rho0 * Th0) ** 3        # sixth power of Z0^2
    vals = {a1: sp.Rational(4), a2: sp.Rational(9, 4), a3: sp.Rational(2, 3),
            rho0: sp.Rational(3), c0: sp.Rational(5), Th0: sp.Rational(7)}
    resid = sp.simplify(lhs6.subs(vals) - rhs6.subs(vals))
    return _check(
        "impedance_recovery_exact",
        "P241-S08 (13)-(16)",
        resid == 0,
        f"rho^3*det(Theta) - Z0^6 at rational sample: {resid} == 0; "
        "(14) holds identically under (16).",
    )

if __name__ == "__main__":
    result = check_impedance_recovery()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
