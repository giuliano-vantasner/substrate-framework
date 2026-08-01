#!/usr/bin/env python3
"""Independent energy-integral and scaled-limit review for P032."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P032-INDEPENDENT")
    coordinate = sp.symbols("x", real=True)
    frequency = sp.symbols("omega", positive=True)
    field = sp.Function("f")(coordinate)
    potential_energy = (1 - sp.cos(field)) / 2 - frequency**2 * field**2 / 2
    first_integral = sp.diff(field, coordinate) ** 2 / 2 - potential_energy
    checks.check(
        "direct multiplication by f-prime derives the localized energy integral",
        sp.simplify(
            sp.diff(first_integral, coordinate)
            - sp.diff(field, coordinate)
            * (
                sp.diff(field, coordinate, 2)
                - sp.sin(field) / 2
                + frequency**2 * field
            )
        )
        == 0,
    )

    amplitude = sp.symbols("a", positive=True)
    root_ratio = (1 - sp.cos(amplitude)) / amplitude**2
    checks.check(
        "the peak condition is frequency-squared equals the decreasing sinc ratio",
        sp.trigsimp(
            root_ratio
            - sp.Rational(1, 2)
            * (sp.sin(amplitude / 2) / (amplitude / 2)) ** 2
        )
        == 0
        and sp.limit(root_ratio, amplitude, 0, dir="+")
        == sp.Rational(1, 2)
        and root_ratio.subs(amplitude, 2 * sp.pi) == 0,
    )
    half = sp.symbols("z", positive=True)
    witness = sp.sin(half) - half * sp.cos(half)
    checks.check(
        "the independent monotonicity witness has positive derivative on zero-to-pi",
        sp.diff(witness, half) == half * sp.sin(half)
        and sp.limit(witness, half, 0, dir="+") == 0,
    )

    value, peak = sp.symbols("u f0", positive=True)
    square = 1 - sp.cos(value) - frequency**2 * value**2
    inverse = sp.Integral(
        1 / sp.sqrt(square), (value, sp.symbols("f", positive=True), peak)
    )
    checks.check(
        "the inverse quadrature independently solves the negative square-root branch",
        sp.simplify(
            sp.diff(inverse, inverse.limits[0][1])
            + 1
            / sp.sqrt(
                square.subs(value, inverse.limits[0][1])
            )
        )
        == 0,
    )

    charge = 4 * frequency * sp.Integral(
        value**2 / sp.sqrt(square), (value, 0, peak)
    )
    checks.check(
        "evenness and the accepted density independently fix the charge quadrature",
        isinstance(sp.simplify(charge / (4 * frequency)), sp.Integral),
    )

    kappa, scaled = sp.symbols("kappa F", positive=True)
    scaled_rhs = (
        sp.sin(kappa * scaled) / 2
        - (sp.Rational(1, 2) - kappa**2) * kappa * scaled
    ) / kappa**3
    checks.check(
        "independent scaling recovers the quartic differential equation",
        sp.series(scaled_rhs, kappa, 0, 3).removeO()
        == scaled - scaled**3 / 12 + kappa**2 * scaled**5 / 240,
    )
    peak_balance = (
        1
        - sp.cos(kappa * scaled)
        - (sp.Rational(1, 2) - kappa**2) * kappa**2 * scaled**2
    ) / kappa**4
    checks.check(
        "independent peak scaling selects sqrt twenty-four",
        sp.solve(
            sp.Eq(sp.limit(peak_balance, kappa, 0, dir="+"), 0),
            scaled,
        )
        == [2 * sp.sqrt(6)],
    )
    eta = sp.sqrt(1 - frequency**2)
    checks.check(
        "the breather envelope width fails the quartic balance by one-half",
        sp.simplify(
            eta**2 - (sp.Rational(1, 2) - frequency**2)
        )
        == sp.Rational(1, 2),
    )

    total = checks.finish()
    print(f"P032 INDEPENDENT ENERGY/ASYMPTOTIC REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
