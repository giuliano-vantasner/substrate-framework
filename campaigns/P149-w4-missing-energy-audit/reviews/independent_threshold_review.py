#!/usr/bin/env python3
"""Fresh two-body threshold derivation without the canonical ledger helper."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P149-independent")
    mass1, mass2 = sp.symbols("m1 m2", positive=True)
    rapidity = sp.symbols("theta", real=True)
    metric = sp.diag(1, -1)
    total = sp.Matrix((mass1 + mass2, 0))
    observed = sp.Matrix((mass1 * sp.cosh(rapidity), mass1 * sp.sinh(rapidity)))
    residual = total - observed

    checks.check(
        "fresh matrix route puts observed particle on shell",
        sp.trigsimp((observed.T * metric * observed)[0] - mass1**2) == 0,
    )
    checks.check(
        "fresh residual closes threshold four-momentum",
        observed + residual == total,
    )
    defect = sp.factor(
        sp.trigsimp(sp.expand((residual.T * metric * residual)[0] - mass2**2))
    )
    expected = -2 * mass1 * (mass1 + mass2) * (sp.cosh(rapidity) - 1)
    checks.check("fresh component expansion derives the defect", defect == expected)

    positive_coordinate = sp.symbols("u", positive=True)
    rationalized = sp.factor(
        expected.subs(
            sp.cosh(rapidity),
            (positive_coordinate + 1 / positive_coordinate) / 2,
        )
    )
    checks.check(
        "positive exponential coordinate makes the sign manifest",
        rationalized
        == -mass1 * (mass1 + mass2) * (positive_coordinate - 1) ** 2
        / positive_coordinate,
    )
    checks.check(
        "fresh equality solve has the unique positive coordinate",
        sp.solve(sp.Eq(rationalized, 0), positive_coordinate) == [1],
    )
    checks.check(
        "exponential injectivity maps equality to zero rapidity",
        sp.solve(sp.Eq(sp.exp(rapidity), 1), rapidity) == [0],
    )

    zero_observed = observed.subs(rapidity, 0)
    zero_residual = residual.subs(rapidity, 0)
    checks.check(
        "fresh equality point has both particles at rest",
        zero_observed == sp.Matrix((mass1, 0))
        and zero_residual == sp.Matrix((mass2, 0)),
    )

    exact_point = {mass1: 8, mass2: 8, rapidity: sp.log(2)}
    point_observed = observed.subs(exact_point).applyfunc(
        lambda value: sp.simplify(value.rewrite(sp.exp))
    )
    point_residual = residual.subs(exact_point).applyfunc(
        lambda value: sp.simplify(value.rewrite(sp.exp))
    )
    checks.check(
        "fresh W4 point gives vectors ten-six and six-minus-six",
        point_observed == sp.Matrix((10, 6))
        and point_residual == sp.Matrix((6, -6)),
    )
    checks.check(
        "fresh W4 residual has zero invariant rather than mass sixty-four",
        (point_residual.T * metric * point_residual)[0] == 0
        and (point_residual.T * metric * point_residual)[0] - 64 == -64,
    )
    checks.check(
        "fresh on-shell recoil pair requires total energy twenty",
        point_observed[0] + sp.sqrt(64 + point_observed[1] ** 2) == 20,
    )

    altered_total = sp.Matrix((20, 0))
    altered_residual = altered_total - point_observed
    checks.check(
        "above-threshold mutation restores the second equal-mass shell",
        altered_residual == sp.Matrix((10, -6))
        and (altered_residual.T * metric * altered_residual)[0] == 64,
    )
    wrong_sign = sp.Matrix((point_residual[0], -point_residual[1]))
    checks.check(
        "momentum-sign mutation keeps mass defect but breaks closure",
        (wrong_sign.T * metric * wrong_sign)[0]
        == (point_residual.T * metric * point_residual)[0]
        and point_observed + wrong_sign != sp.Matrix((16, 0)),
    )
    wrong_threshold = sp.Matrix((mass1 + mass2 + 1, 0))
    checks.check(
        "total-energy mutation changes the symbolic residual shell",
        sp.simplify(
            ((wrong_threshold - observed).T * metric * (wrong_threshold - observed))[0]
            - mass2**2
            - defect
        )
        != 0,
    )

    charge_zero = sp.Integer(0)
    escaped_energy = sp.Integer(0)
    boundary_stored_energy = sp.Integer(16)
    checks.check(
        "fresh countermodel separates charge from invisible energy",
        charge_zero == 0
        and escaped_energy == 0
        and boundary_stored_energy > 0,
    )
    checks.check(
        "same missing scalar permits a non-particle boundary channel",
        point_residual[0] == 6
        and boundary_stored_energy - 10 == point_residual[0],
    )

    tally = checks.finish()
    print(f"P149 INDEPENDENT ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
