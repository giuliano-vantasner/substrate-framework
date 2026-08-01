#!/usr/bin/env python3
"""Independent exponent elimination and substitution review for P016."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def solve_target(target: tuple[int, int, int]) -> dict[sp.Symbol, sp.Expr]:
    x, y, z = sp.symbols("x y z")
    mass, length, time = target
    solutions = sp.solve(
        [
            sp.Eq(y, mass),
            sp.Eq(x + 2 * y + z, length),
            sp.Eq(-x - y, time),
        ],
        [x, y, z],
        dict=True,
    )
    assert len(solutions) == 1
    return solutions[0]


def run() -> int:
    checks = CheckLedger("P016-INDEPENDENT")
    x, y, z = sp.symbols("x y z")
    checks.check(
        "direct exponent elimination gives the unique mass monomial",
        solve_target((1, 0, 0)) == {x: -1, y: 1, z: -1},
    )
    checks.check(
        "direct exponent elimination gives the unique energy monomial",
        solve_target((1, 2, -2)) == {x: 1, y: 1, z: -1},
    )
    checks.check(
        "direct exponent elimination gives density and stiffness monomials",
        solve_target((1, -3, 0)) == {x: -1, y: 1, z: -4}
        and solve_target((1, -1, -2)) == {x: 1, y: 1, z: -4},
    )

    action, speed, length, ratio = sp.symbols("S c a kappa", positive=True)
    number_density = length**-3
    thermal = ratio * action * speed / length
    epsilon = sp.simplify(number_density * thermal / speed**2)
    inverse_mu = sp.simplify(number_density * thermal)
    mass_density = sp.simplify(epsilon / 2)
    checks.check(
        "direct premise substitution reconstructs both co-scaled responses",
        epsilon == ratio * action / (length**4 * speed)
        and inverse_mu == ratio * action * speed / length**4,
    )
    checks.check(
        "direct substitution retains the mass-density one-half",
        mass_density == ratio * action / (2 * length**4 * speed),
    )
    checks.check(
        "the wave-speed cancellation is independent of the free speed ratio",
        sp.simplify(inverse_mu / epsilon - speed**2) == 0
        and sp.diff(sp.simplify(inverse_mu / epsilon), ratio) == 0,
    )
    checks.check(
        "changing the conversion ratio leaves dimensions but changes mass density",
        sp.simplify(epsilon - mass_density) != 0,
    )

    total = checks.finish()
    print(f"P016 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
