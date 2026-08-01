#!/usr/bin/env python3
"""Independent exponent and information review for P018 without package APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P018-INDEPENDENT")
    p, q, r = sp.symbols("p q r")
    solutions = sp.solve(
        [
            sp.Eq(q, 1),
            sp.Eq(p + 2 * q + r, 0),
            sp.Eq(-p - q, 0),
        ],
        [p, q, r],
        dict=True,
    )
    checks.check(
        "direct elimination gives the unique speed-action-length mass exponents",
        solutions == [{p: -1, q: 1, r: -1}],
    )

    mass, speed, action, length, coordinate = sp.symbols(
        "m c S a N", positive=True
    )
    forward = mass * speed * length / action
    backward = coordinate * action / (speed * length)
    checks.check(
        "direct substitution proves inverse after forward",
        sp.simplify(backward.subs(coordinate, forward) - mass) == 0,
    )
    checks.check(
        "direct substitution proves forward after inverse",
        sp.simplify(forward.subs(mass, backward) - coordinate) == 0,
    )
    checks.check(
        "the coordinate remains a load-bearing free input",
        sp.diff(backward, coordinate) == action / (speed * length),
    )

    other_coordinate = sp.symbols("N_h", positive=True)
    ratio = sp.simplify(
        backward
        / (other_coordinate * action / (speed * length))
    )
    checks.check(
        "shared scales cancel from a ratio but two coordinates remain",
        ratio == coordinate / other_coordinate
        and ratio.free_symbols == {coordinate, other_coordinate},
    )
    checks.check(
        "changing the coordinate changes mass without changing dimensions",
        sp.simplify(backward.subs(coordinate, 2) - 2 * backward.subs(coordinate, 1))
        == 0,
    )

    total = checks.finish()
    print(f"P018 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
