#!/usr/bin/env python3
"""Independent coefficient-ratio review for MR1 without package mass APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P017-INDEPENDENT")
    shape, rest_energy, ratio = sp.symbols("b E_e X", positive=True)
    medium_coefficient = 48 * sp.pi**3
    skyrme_coefficient = 3 * sp.pi**2

    quotient = sp.cancel(medium_coefficient / skyrme_coefficient)
    checks.check(
        "direct coefficient division gives the unit ratio",
        quotient == 16 * sp.pi,
    )
    checks.check(
        "reverse substitution reconstructs exact mass equality",
        sp.simplify(
            medium_coefficient * shape * rest_energy
            - skyrme_coefficient * shape * quotient * rest_energy
        )
        == 0,
    )
    checks.check(
        "different shape powers retain model dependence",
        sp.solve(
            sp.Eq(
                medium_coefficient * shape**2 * rest_energy,
                skyrme_coefficient * shape * ratio,
            ),
            ratio,
        )
        == [16 * sp.pi * shape * rest_energy],
    )
    checks.check(
        "a changed medium coefficient breaks the accepted ratio",
        sp.cancel(47 * sp.pi**3 / skyrme_coefficient) != 16 * sp.pi,
    )
    allocation = sp.symbols("allocation", real=True)
    equality = sp.simplify(
        medium_coefficient * shape * rest_energy
        - skyrme_coefficient * shape * 16 * sp.pi * rest_energy
    )
    checks.check(
        "coefficient equality contains no sector-allocation proposition",
        equality == 0 and allocation not in equality.free_symbols,
    )

    total = checks.finish()
    print(f"P017 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
