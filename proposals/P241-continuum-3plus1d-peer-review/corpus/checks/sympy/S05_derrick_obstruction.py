"""P241 audit oracle — Derrick scaling obstruction for static real lumps in d=3 (Section 3 scope).

Standalone module: python3 S05_derrick_obstruction.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_derrick_static_obstruction() -> dict[str, object]:
    """Derrick scaling obstruction for static real lumps in d=3.

    For u_lam(x)=u(lam*x): E_grad(lam)=E_grad/lam, E_pot(lam)=E_pot/lam^3, so
    E'(lam) = -E_grad/lam^2 - 3*E_pot/lam^4 < 0 for all lam>0: no stationary
    point, hence no finite-energy static lump of a real scalar with positive
    gradient and potential energies. Existence must be time-dependent or
    charged (Benci-Fortunato class).
    """
    lam = sp.Symbol("lambda", positive=True)
    Eg, Ep = sp.symbols("E_g E_p", positive=True)
    E = Eg / lam + Ep / lam**3
    dE = sp.simplify(sp.diff(E, lam))
    ok = sp.simplify(-dE * lam**4 - Eg * lam**2 - 3 * Ep) == 0 and dE != 0
    sign_neg = sp.simplify(dE.subs(lam, 1)) < 0
    return _check(
        "derrick_static_obstruction",
        "P241-S05/S06 (Section 3)",
        ok and sign_neg,
        "E(lambda)=E_g/lambda+E_p/lambda^3 gives E'(lambda)<0 identically for "
        "positive gradient/potential energies: static real lumps obstructed in d=3; "
        "the Benci-Fortunato hylomorphic existence class is charged/time-dependent, "
        "so Section 3's real-field appeal needs scoping to oscillon-type "
        "finite-time objects (see scipy corpus).",
    )

if __name__ == "__main__":
    result = check_derrick_static_obstruction()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
