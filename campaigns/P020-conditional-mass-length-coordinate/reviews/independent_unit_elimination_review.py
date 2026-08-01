#!/usr/bin/env python3
"""Independent declared-unit elimination review for P020."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P020-INDEPENDENT")
    unit, mass, coupling, length, action, speed = sp.symbols(
        "U m e L S c", positive=True
    )
    product_coefficient, energy_coefficient = sp.symbols("r k", positive=True)

    general = sp.solve(
        [
            sp.Eq(unit * length, product_coefficient * action * speed / coupling**2),
            sp.Eq(unit, energy_coefficient * mass * speed**2),
        ],
        [unit, mass],
        dict=True,
    )[0][mass]
    checks.check(
        "direct elimination retains both declared coefficients",
        general
        == product_coefficient
        * action
        / (energy_coefficient * coupling**2 * length * speed),
    )
    specialized = sp.simplify(
        general.subs(
            {
                product_coefficient: sp.Rational(1, 2),
                energy_coefficient: 4 * sp.pi,
            }
        )
    )
    checks.check(
        "declared EL3 coefficients give the exact conditional mass",
        specialized == action / (8 * sp.pi * coupling**2 * length * speed),
    )
    coordinate = sp.simplify(specialized * speed * length / action)
    checks.check(
        "direct normalization gives the exact dimensionless coordinate",
        coordinate == 1 / (8 * sp.pi * coupling**2),
    )
    checks.check(
        "varying the coupling varies the reconstructed mass",
        sp.diff(specialized, coupling) != 0,
    )
    free_function = sp.Function("g")(coupling)
    checks.check(
        "dimensions allow an arbitrary function of the dimensionless coupling",
        sp.diff(free_function * action / (speed * length), free_function)
        == action / (speed * length),
    )

    total = checks.finish()
    print(f"P020 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
