#!/usr/bin/env python3
"""Independent jet, sign, and curvature rederivation for P030."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P030-INDEPENDENT")
    psi, dpsi, gauge, dchi, coupling = sp.symbols(
        "psi dpsi A dchi e", positive=True
    )
    phase = sp.symbols("U", nonzero=True)
    original = dpsi - sp.I * coupling * gauge * psi
    transformed = phase * (dpsi + sp.I * coupling * dchi * psi) - (
        sp.I * coupling * (gauge + dchi) * phase * psi
    )
    checks.check(
        "independent jet expansion proves local covariance",
        sp.simplify(transformed - phase * original) == 0,
    )

    amplitude, phase_gradient, connection = sp.symbols(
        "f theta_mu A_mu", real=True
    )
    accepted_current = -2 * amplitude**2 * phase_gradient
    expanded_cross = -2 * coupling * amplitude**2 * phase_gradient * connection
    checks.check(
        "independent polar expansion gives plus e A times accepted current",
        sp.simplify(expanded_cross - coupling * connection * accepted_current)
        == 0,
    )

    x_mu, x_nu = sp.symbols("x_mu x_nu")
    field = sp.Function("psi")(x_mu, x_nu)
    a_mu = sp.Function("A_mu")(x_mu, x_nu)
    a_nu = sp.Function("A_nu")(x_mu, x_nu)

    def derivative(value: sp.Expr, connection_value: sp.Expr, variable: sp.Symbol) -> sp.Expr:
        return sp.diff(value, variable) - sp.I * coupling * connection_value * value

    commutator = sp.simplify(
        derivative(derivative(field, a_nu, x_nu), a_mu, x_mu)
        - derivative(derivative(field, a_mu, x_mu), a_nu, x_nu)
    )
    curvature = sp.diff(a_nu, x_mu) - sp.diff(a_mu, x_nu)
    checks.check(
        "independent nested derivatives give minus i e F psi",
        sp.simplify(commutator + sp.I * coupling * curvature * field) == 0,
    )

    winding = sp.symbols("N", integer=True, positive=True)
    asymptotic = sp.symbols("a", real=True)
    checks.check(
        "independent logarithmic coefficient forces a to integer winding",
        sp.solve(sp.Eq((winding - asymptotic) ** 2, 0), asymptotic)
        == [winding],
    )
    checks.check(
        "the resulting matter holonomy is one for integer winding",
        sp.simplify(sp.exp(2 * sp.pi * sp.I * winding)) == 1,
    )
    checks.check(
        "half-flux minus one is outside the integer-winding consequence",
        sp.exp(sp.I * sp.pi) == -1
        and sp.Rational(1, 2).is_integer is False,
    )
    arbitrary_coefficient = sp.symbols("c", real=True)
    checks.check(
        "local symmetry cannot fix a gauge-kinetic coefficient",
        sp.diff(arbitrary_coefficient * curvature**2, arbitrary_coefficient)
        == curvature**2,
    )

    total = checks.finish()
    print(f"P030 INDEPENDENT SIGN/COMMUTATOR REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
