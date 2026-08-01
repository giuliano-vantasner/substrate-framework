#!/usr/bin/env python3
"""Independent determinant-form reconstruction for proposed C-OG-003.

This review does not import ``substrate_framework.optical_geometry``. It starts
from the metric and the coordinate formula for the scalar wave operator.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("C-OG-003-INDEPENDENT")
    x = sp.symbols("x", real=True)
    c0 = sp.symbols("c0", positive=True)
    potential = sp.Function("Phi")(x)
    density = sp.Function("rho")(x)
    kappa = sp.symbols("kappa", real=True)

    index = 1 / (1 + 2 * potential / c0**2)
    metric = sp.diag(-1 / index, index / c0**2)
    inverse = sp.simplify(metric.inv())
    volume_density = sp.sqrt(-sp.simplify(metric.det()))
    dilaton = sp.log(index)

    checks.check(
        "the declared metric volume density is constant",
        sp.simplify(volume_density - 1 / c0) == 0,
    )
    checks.check(
        "the independently inverted spatial metric component is c0^2/n",
        sp.simplify(inverse[1, 1] - c0**2 / index) == 0,
    )

    box_from_density = sp.simplify(
        sp.diff(
            volume_density * inverse[1, 1] * sp.diff(dilaton, x),
            x,
        )
        / volume_density
    )
    source_side = sp.simplify(-box_from_density)
    checks.check(
        "the determinant-form scalar operator gives the exact source-side pullback",
        sp.simplify(source_side - 2 * sp.diff(potential, x, 2)) == 0,
    )
    checks.check(
        "the matter-source residual factorizes without assigning a coupling",
        sp.simplify(
            source_side
            - kappa * density
            - 2
            * (sp.diff(potential, x, 2) - kappa * density / 2)
        )
        == 0,
    )

    wrong_index = 1 / (1 + potential / c0**2)
    wrong_dilaton = sp.log(wrong_index)
    wrong_source = sp.simplify(
        -sp.diff(
            volume_density
            * (c0**2 / wrong_index)
            * sp.diff(wrong_dilaton, x),
            x,
        )
        / volume_density
    )
    checks.check(
        "halving the TF coefficient breaks the factor of two",
        sp.simplify(wrong_source - 2 * sp.diff(potential, x, 2)) != 0,
    )

    total = checks.finish()
    print(f"P010 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
