"""P241 audit oracle — Counterexample to unhypothesized M0 constancy (20)-(21).

Standalone module: python3 S10_rest_mass_variation.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_rest_mass_variation_counterexample() -> dict[str, object]:
    """Counterexample to unhypothesized 'M0 = E0/c0^2 is a true constant'.

    Fixed potential U(u) = m^2 u^2/2 + lambda u^4/4 with a frozen eikonal
    profile gives E0(X) = Theta(X)*G_grad + U-terms independent of position;
    under matching Theta(X) varies, hence E0 and M0 = E0/c0^2 vary along the
    path and the Euler-Lagrange equations are not pure geodesics.
    """
    x, Th0_, kappa, m2, lam4, c0 = sp.symbols("x Theta_0 kappa m^2 lambda c_0", positive=True)
    G_grad, G_pot = sp.symbols("G_grad G_pot", positive=True)
    Th = Th0_ * (1 + kappa * x)
    E0 = Th * G_grad + m2 * G_pot
    M0_of_x = sp.simplify(E0 / c0**2)
    dM0 = sp.diff(M0_of_x, x)
    nonzero = sp.simplify(dM0.subs({Th0_: 1, kappa: sp.Rational(1, 5), G_grad: sp.Rational(3, 2),
                                    G_pot: 1, m2: 1, c0: 1})) != 0
    return _check(
        "rest_mass_variation_counterexample",
        "P241-S10 (20)-(21) M0 constancy",
        bool(nonzero),
        "For fixed potential and frozen eikonal profile, dM0/dX = "
        "kappa*Theta0*G_grad/c0^2 != 0: the proper mass varies along the path "
        "unless an additional adiabatic-invariance hypothesis holds. Repair: "
        "state E0(X)=const explicitly (or derive it from an action-invariance "
        "assumption); otherwise the trajectory equations acquire non-geodesic "
        "force terms and Section 5's geodesic conclusion is conditional.",
    )

if __name__ == "__main__":
    result = check_rest_mass_variation_counterexample()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
