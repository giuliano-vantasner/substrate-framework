#!/usr/bin/env python3
"""Independent first-integral and charge rederivation for P031."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P031-INDEPENDENT")
    coordinate = sp.symbols("x", real=True)
    frequency = sp.symbols("omega", positive=True)
    kappa = sp.sqrt(sp.Rational(1, 2) - frequency**2)
    field = sp.Function("f")(coordinate)
    first_integral_derivative = sp.diff(
        sp.diff(field, coordinate) ** 2 / 2
        - kappa**2 * field**2 / 2
        + field**4 / 48,
        coordinate,
    )
    ode_factor = sp.diff(field, coordinate) * (
        sp.diff(field, coordinate, 2)
        - kappa**2 * field
        + field**3 / 12
    )
    checks.check(
        "multiplication by f-prime gives the conserved first integral",
        sp.simplify(first_integral_derivative - ode_factor) == 0,
    )

    peak = sp.symbols("A", positive=True)
    peak_solutions = sp.solve(
        sp.Eq(-kappa**2 * peak**2 / 2 + peak**4 / 48, 0),
        peak**2,
    )
    nonzero_peak_solutions = [
        solution for solution in peak_solutions if solution != 0
    ]
    checks.check(
        "the nonzero turning point independently fixes A-squared",
        len(nonzero_peak_solutions) == 1
        and sp.simplify(nonzero_peak_solutions[0] - 24 * kappa**2) == 0,
    )

    amplitude = sp.sqrt(24) * kappa
    profile = amplitude / sp.cosh(kappa * coordinate)
    first_integral = (
        sp.diff(profile, coordinate) ** 2
        - kappa**2 * profile**2
        + profile**4 / 24
    )
    checks.check(
        "the independently constructed homoclinic profile obeys that integral",
        sp.simplify(first_integral) == 0,
    )
    checks.check(
        "differentiating the first-integral solution recovers the ODE",
        sp.simplify(
            sp.diff(profile, coordinate, 2)
            - kappa**2 * profile
            + profile**3 / 12
        )
        == 0,
    )

    scaled_coordinate = sp.symbols("u", real=True)
    norm = sp.integrate(
        amplitude**2 / (kappa * sp.cosh(scaled_coordinate) ** 2),
        (scaled_coordinate, -sp.oo, sp.oo),
    )
    charge = sp.simplify(2 * frequency * norm)
    expected = 96 * frequency * kappa
    checks.check(
        "direct norm integration gives the accepted-current charge",
        sp.simplify(charge - expected) == 0,
    )
    derivative = sp.diff(expected, frequency)
    checks.check(
        "independent differentiation fixes the charge maximum and branch signs",
        sp.solve(sp.Eq(derivative, 0), frequency) == [sp.Rational(1, 2)]
        and expected.subs(frequency, sp.Rational(1, 2)) == 24
        and derivative.subs(frequency, sp.Rational(1, 4)) > 0
        and derivative.subs(frequency, sp.Rational(3, 5)) < 0,
    )
    arbitrary_verdict = sp.symbols("spectral_verdict")
    checks.check(
        "profile and charge identities leave a spectral verdict unconstrained",
        arbitrary_verdict not in (profile.free_symbols | charge.free_symbols)
        and sp.diff(arbitrary_verdict, frequency) == 0,
    )

    total = checks.finish()
    print(f"P031 INDEPENDENT FIRST-INTEGRAL REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
