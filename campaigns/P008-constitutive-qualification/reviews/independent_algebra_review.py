#!/usr/bin/env python3
"""Independent exponent and coefficient elimination review for P008.

This file intentionally imports neither new claim module.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    medium_checks = CheckLedger("C-MED-001-INDEPENDENT")
    skyrme_checks = CheckLedger("C-SK-001-INDEPENDENT")

    density, thermal, speed = sp.symbols("rho Theta c", positive=True)
    p, q, r, s = sp.symbols("p q r s", real=True)
    general_speed = sp.simplify(
        sp.sqrt(
            density**q
            * thermal**s
            / (density**p * thermal**r / speed**2)
        )
    )
    density_sensitivity = sp.simplify(
        density * sp.diff(sp.log(general_speed), density)
    )
    thermal_sensitivity = sp.simplify(
        thermal * sp.diff(sp.log(general_speed), thermal)
    )
    medium_checks.check(
        "direct exponent algebra gives half-difference sensitivities",
        sp.simplify(density_sensitivity - (q - p) / 2) == 0
        and sp.simplify(thermal_sensitivity - (s - r) / 2) == 0,
    )
    medium_checks.check(
        "both sensitivities vanish exactly when corresponding exponents match",
        sp.solve(
            [sp.Eq(density_sensitivity, 0), sp.Eq(thermal_sensitivity, 0)],
            [q, s],
            dict=True,
        )
        == [{q: p, s: r}],
    )
    medium_checks.check(
        "a density exponent mismatch produces a nonzero index response",
        density_sensitivity.subs({p: 1, q: 2}) == sp.Rational(1, 2),
    )

    coefficient, rest_energy, ratio = sp.symbols(
        "B1 E_e ratio", positive=True
    )
    topological_coefficient = 48 * sp.pi**3 * coefficient * rest_energy
    anw_coefficient = 3 * sp.pi**2 * coefficient * ratio
    skyrme_checks.check(
        "direct coefficient division independently gives 16*pi*E_e",
        sp.simplify(topological_coefficient / (3 * sp.pi**2 * coefficient))
        == 16 * sp.pi * rest_energy,
    )
    skyrme_checks.check(
        "the independently obtained ratio makes both premises equal",
        sp.simplify(
            topological_coefficient
            - anw_coefficient.subs(ratio, 16 * sp.pi * rest_energy)
        )
        == 0,
    )
    wrong_ratio = sp.solve(
        sp.Eq(
            3 * sp.pi**2 * coefficient * ratio,
            48 * sp.pi**3 * coefficient**2 * rest_energy,
        ),
        ratio,
    )[0]
    skyrme_checks.check(
        "a squared B1 premise independently prevents coefficient cancellation",
        sp.simplify(wrong_ratio - 16 * sp.pi * coefficient * rest_energy)
        == 0
        and coefficient in wrong_ratio.free_symbols,
    )

    medium_total = medium_checks.finish()
    skyrme_total = skyrme_checks.finish()
    total = medium_total + skyrme_total
    print(f"P008 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
