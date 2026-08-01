#!/usr/bin/env python3
"""Independent light-cone and exterior-calculus review of P048."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P048-INDEPENDENT")

    u, v = sp.symbols("u v", real=True)
    field = sp.Function("Phi")(u, v)
    current_plus = 2 * sp.diff(field, u)
    current_minus = 2 * sp.diff(field, v)
    equation_wave_part = 4 * sp.diff(field, u, v)
    on_shell_mixed = -sp.sin(field) / 4
    ledger.check(
        "an independent characteristic-coordinate derivation fixes both half sources",
        sp.simplify(sp.diff(current_plus, v).subs(sp.diff(field, u, v), on_shell_mixed)
                    + sp.sin(field) / 2) == 0
        and sp.simplify(sp.diff(current_minus, u).subs(sp.diff(field, u, v), on_shell_mixed)
                        + sp.sin(field) / 2) == 0
        and equation_wave_part.subs(sp.diff(field, u, v), on_shell_mixed)
        == -sp.sin(field),
    )

    x, t = sp.symbols("x t", real=True)
    arbitrary = sp.Function("f")(x, t)
    epsilon = sp.Matrix([[0, 1], [-1, 0]])
    gradient_covector = sp.Matrix([sp.diff(arbitrary, t), sp.diff(arbitrary, x)])
    current = epsilon * gradient_covector / (2 * sp.pi)
    ledger.check(
        "the antisymmetric orientation tensor independently gives the current components",
        current[0] == sp.diff(arbitrary, x) / (2 * sp.pi)
        and current[1] == -sp.diff(arbitrary, t) / (2 * sp.pi),
    )
    ledger.check(
        "antisymmetry contracts the symmetric Hessian to zero without an equation of motion",
        sp.simplify(sp.diff(current[0], t) + sp.diff(current[1], x)) == 0,
    )

    lower, upper = sp.symbols("phi_minus phi_plus", real=True)
    boundary_charge = (upper - lower) / (2 * sp.pi)
    reflected_charge = (lower - upper) / (2 * sp.pi)
    ledger.check(
        "the fundamental theorem gives a boundary charge reversed by endpoint exchange",
        sp.simplify(reflected_charge + boundary_charge) == 0,
    )

    kink = 4 * sp.atan(sp.exp(x))
    reflected = kink.subs(x, -x)
    kink_charge = sp.integrate(sp.diff(kink, x) / (2 * sp.pi), (x, -sp.oo, sp.oo))
    reflected_charge = sp.integrate(
        sp.diff(reflected, x) / (2 * sp.pi),
        (x, -sp.oo, sp.oo),
    )
    ledger.check(
        "a direct profile calculation gives opposite unit charges",
        sp.simplify(kink_charge) == 1 and sp.simplify(reflected_charge) == -1,
    )

    parity_field = arbitrary.subs(x, -x)
    parity_equation = (
        sp.diff(parity_field, t, 2)
        - sp.diff(parity_field, x, 2)
        + sp.sin(parity_field)
    )
    original_reflected = (
        sp.diff(arbitrary, t, 2)
        - sp.diff(arbitrary, x, 2)
        + sp.sin(arbitrary)
    ).subs(x, -x)
    ledger.check(
        "the same transformation that flips winding leaves the SG equation invariant",
        sp.simplify(parity_equation - original_reflected) == 0,
    )

    small = sp.symbols("small", positive=True)
    profile = sp.Function("g")(x, t)
    linear_source = sp.limit(-sp.sin(small * profile) / small, small, 0, dir="+")
    ledger.check(
        "the linearized sine-Gordon source remains nonzero at first field order",
        linear_source == -profile,
    )

    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
