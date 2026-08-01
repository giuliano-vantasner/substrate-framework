#!/usr/bin/env python3
"""Independent symbolic information audit for P029."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P029-INDEPENDENT")
    flux, tension, area = sp.symbols("Phi sigma A", positive=True)
    solved_area = sp.solve(sp.Eq(tension, flux**2 / (2 * area)), area)
    checks.check(
        "solving the ideal-tube equation gives one reconstructed area",
        solved_area == [flux**2 / (2 * tension)],
    )
    checks.check(
        "back-substitution is an identity for every positive tension",
        sp.simplify(flux**2 / (2 * solved_area[0]) - tension) == 0,
    )

    winding, gauge, vacuum = sp.symbols("n g v", positive=True)
    quantized_flux = 2 * sp.pi * winding / gauge
    penetration_length = 1 / (gauge * vacuum)
    ratio = sp.simplify(
        solved_area[0].subs(flux, quantized_flux) / penetration_length**2
    )
    checks.check(
        "independent elimination cancels the gauge coupling",
        ratio == 2 * sp.pi**2 * winding**2 * vacuum**2 / tension,
    )

    lower_ratio, upper_ratio = sp.Rational(1, 10), sp.Integer(100)
    tension_interval = (
        sp.simplify(2 * sp.pi**2 / upper_ratio),
        sp.simplify(2 * sp.pi**2 / lower_ratio),
    )
    checks.check(
        "the source window maps to a factor-one-thousand tension interval",
        sp.simplify(tension_interval[1] / tension_interval[0]) == 1000,
    )

    profile_radius = sp.symbols("r", positive=True)
    profile_density = sp.Function("epsilon")(profile_radius)
    profile_area = sp.integrate(
        2 * sp.pi * profile_radius,
        (profile_radius, 0, sp.oo),
    )
    checks.check(
        "the inverted area contains no profile-defined support criterion",
        not solved_area[0].has(profile_density)
        and profile_area is sp.oo,
    )
    area_factor = sp.symbols("c", positive=True)
    checks.check(
        "a free geometric area factor changes the alleged scale match",
        sp.diff(ratio / area_factor, area_factor) != 0,
    )

    total = checks.finish()
    print(f"P029 INDEPENDENT INFORMATION REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
