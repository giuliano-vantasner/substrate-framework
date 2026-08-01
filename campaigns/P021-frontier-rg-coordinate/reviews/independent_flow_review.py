#!/usr/bin/env python3
"""Independent reciprocal-coupling derivation for P021."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P021-INDEPENDENT")
    time, initial_time, inverse_initial, coefficient = sp.symbols(
        "t t0 h0 b0", real=True
    )
    coefficient = sp.symbols("b0", positive=True)
    inverse = inverse_initial + coefficient * (time - initial_time) / (
        8 * sp.pi**2
    )
    checks.check(
        "direct reciprocal-coupling integration satisfies its constant derivative",
        sp.diff(inverse, time) == coefficient / (8 * sp.pi**2),
    )

    zero_time = sp.solve(sp.Eq(inverse, 0), time)[0]
    checks.check(
        "the zero occurs at the exact logarithmic scale separation",
        zero_time == initial_time - 8 * sp.pi**2 * inverse_initial / coefficient,
    )
    reference, coupling = sp.symbols("mu0 g0", positive=True)
    invariant = sp.simplify(
        reference
        * sp.exp((zero_time - initial_time).subs(inverse_initial, 1 / coupling**2))
    )
    checks.check(
        "exponentiating the independently derived zero gives the invariant scale",
        invariant
        == reference * sp.exp(-8 * sp.pi**2 / (coefficient * coupling**2)),
    )

    action, speed, length, ratio = sp.symbols("S c a q", positive=True)
    mass = sp.simplify(ratio * invariant.subs(reference, action * speed / length) / speed**2)
    coordinate = sp.simplify(mass * speed * length / action)
    checks.check(
        "independent substitution retains the mass-energy ratio in the coordinate",
        coordinate
        == ratio * sp.exp(-8 * sp.pi**2 / (coefficient * coupling**2)),
    )

    slope = sp.symbols("k", nonzero=True)
    left = sp.Matrix([[-1, slope], [-1, slope]])
    first_offset, second_offset = sp.symbols("r1 r2")
    checks.check(
        "identical left-hand rows can still make an inconsistent augmented system",
        left.rank() == 1
        and left.row_join(sp.Matrix([first_offset, second_offset])).rank() == 2,
    )

    total = checks.finish()
    print(f"P021 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
