#!/usr/bin/env python3
"""Independent angle-coordinate review for proposed C-SG-006/007.

This route does not import the new secant or lattice APIs.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    secant_checks = CheckLedger("C-SG-006-INDEPENDENT")
    lattice_checks = CheckLedger("C-SG-007-INDEPENDENT")
    theta = sp.symbols("theta", positive=True)
    energy = 16 * sp.sin(theta)
    frequency = sp.cos(theta)
    action = 16 * theta
    secant = sp.simplify(energy / frequency)
    ratio = sp.simplify(action / secant)

    secant_checks.check(
        "the action-angle coordinate gives H=16*tan(theta) and J/H=theta*cot(theta)",
        sp.trigsimp(secant - 16 * sp.tan(theta)) == 0
        and sp.trigsimp(ratio - theta / sp.tan(theta)) == 0,
    )
    secant_checks.check(
        "the independent derivative ratio gives dE/dH=cos(theta)^3",
        sp.trigsimp(
            sp.diff(energy, theta) / sp.diff(secant, theta)
            - sp.cos(theta) ** 3
        )
        == 0,
    )
    monotonic_numerator = theta - sp.sin(theta) * sp.cos(theta)
    secant_checks.check(
        "theta-sin(theta)cos(theta) grows from zero on the physical angle interval",
        sp.simplify(sp.limit(monotonic_numerator, theta, 0, dir="+")) == 0
        and sp.trigsimp(sp.diff(monotonic_numerator, theta) - 2 * sp.sin(theta) ** 2)
        == 0,
    )
    secant_checks.check(
        "theta*cot(theta) decreases with theta and therefore increases with omega",
        sp.trigsimp(
            sp.diff(ratio, theta)
            + monotonic_numerator / sp.sin(theta) ** 2
        )
        == 0,
    )

    level = sp.symbols("n", positive=True, integer=True)
    quantum = sp.symbols("h", positive=True)
    level_angle = level * quantum / 16
    level_energy = 16 * sp.sin(level_angle)
    next_energy = 16 * sp.sin((level + 1) * quantum / 16)
    direct_gap = sp.expand_trig(next_energy) - sp.expand_trig(level_energy)
    target_gap = 32 * sp.sin(quantum / 32) * sp.cos(
        (2 * level + 1) * quantum / 32
    )
    lattice_checks.check(
        "direct sine subtraction gives the adjacent finite difference",
        sp.trigsimp(direct_gap - target_gap) == 0,
    )
    lattice_checks.check(
        "the finite difference rejects an off-by-one next level",
        sp.trigsimp(
            16 * sp.sin((level + 2) * quantum / 16)
            - level_energy
            - target_gap
        )
        != 0,
    )
    lattice_checks.check(
        "the continuous interpolation derivative is distinct at an exact anchor",
        sp.simplify(
            (next_energy - level_energy).subs({level: 1, quantum: 4})
            - (
                quantum * sp.cos(level * quantum / 16)
            ).subs({level: 1, quantum: 4})
        )
        != 0,
    )

    secant_total = secant_checks.finish()
    lattice_total = lattice_checks.finish()
    print(
        "P011 INDEPENDENT REVIEW ALL "
        f"{secant_total + lattice_total} CHECKS PASS"
    )
    return secant_total + lattice_total


if __name__ == "__main__":
    run()
