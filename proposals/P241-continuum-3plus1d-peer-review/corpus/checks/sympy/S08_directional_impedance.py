"""P241 audit oracle — Scalar matching does not make an anisotropic interface reflectionless.

Standalone module: python3 S08_directional_impedance.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_directional_impedance_counterexample() -> dict[str, object]:
    """Scalar matching does NOT make an anisotropic interface reflectionless.

    Media A,B both satisfy rho*(det Theta)^{1/3}=Z0^2 yet have unequal normal
    impedances sqrt(rho*Theta_nn); the interface reflection coefficient
    r=(Z_A-Z_B)/(Z_A+Z_B) derived from continuity of u and of Theta*u_x is
    nonzero. Reflectionlessness requires directional matching.
    """
    # Medium A: Theta = diag(4s, s, s/4), medium B: Theta = diag(s, s, s);
    # matching fixes rho_pm = Z0^2/s each. Normal (x-direction) impedances:
    s = sp.Symbol("s", positive=True)
    Z0 = sp.Symbol("Z_0", positive=True)
    rhoA, rhoB = Z0**2 / s, Z0**2 / s
    ZA, ZB = sp.sqrt(rhoA * 4 * s), sp.sqrt(rhoB * s)
    r_coeff = sp.simplify((ZA - ZB) / (ZA + ZB))
    # derive r by solving continuity conditions symbolically:
    ui, ur, ut_, k1, k2, om = sp.symbols("u_i u_r u_t k_1 k_2 omega", positive=True)
    x = sp.Symbol("x", real=True)
    # wave eqn: rho*u_tt = Theta*u_xx; dispersion k = omega*sqrt(rho/Theta).
    # continuity at x=0: ui+ur=ut_; flux: Theta1*(k1*(ui-ur)) = Theta2*k2*ut_
    sol = sp.solve(
        [
            sp.Eq(ui + ur, ut_),
            sp.Eq(4 * s * k1 * (ui - ur), s * k2 * ut_),
        ],
        [ur, ut_], dict=True,
    )[0]
    r_derived = sp.simplify(sol[ur].subs({k1: om * sp.sqrt(rhoA / (4 * s)),
                                          k2: om * sp.sqrt(rhoB / s)}) / ui)
    r_derived_simplified = sp.cancel(r_derived.subs(s, sp.Rational(1)))
    nonzero = sp.simplify(r_derived_simplified - 0) != 0
    return _check(
        "directional_impedance_counterexample",
        "P241-S08 reflectionless interpretation",
        bool(nonzero),
        f"Both media satisfy (14); normal-incidence reflection coefficient "
        f"r=(ZA-ZB)/(ZA+ZB)={sp.nsimplify(r_coeff)} != 0 (derived {r_derived_simplified}). "
        "The Principle-of-Inertia interpretation of (13)-(14) requires directional "
        "(normal) impedance matching, not only the scalar determinant condition.",
    )

if __name__ == "__main__":
    result = check_directional_impedance_counterexample()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
