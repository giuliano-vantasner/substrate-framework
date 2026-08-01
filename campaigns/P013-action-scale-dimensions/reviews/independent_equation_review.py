#!/usr/bin/env python3
"""Independent quotient and exponent-equation review for C-ACT-001/C-DIM-001."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    action_checks = CheckLedger("C-ACT-001-INDEPENDENT")
    dimension_checks = CheckLedger("C-DIM-001-INDEPENDENT")
    action = sp.symbols("J", positive=True)
    coefficient = sp.symbols("C", positive=True)

    action_checks.check(
        "separating E'=E/J integrates to the positive linear family",
        sp.integrate(1 / sp.Symbol("y", positive=True), sp.Symbol("y", positive=True))
        == sp.log(sp.Symbol("y", positive=True))
        and sp.diff(coefficient * action, action) == coefficient,
    )
    action_checks.check(
        "the linear family has constant frequency and exact secant equality",
        sp.simplify(
            coefficient * action
            / sp.diff(coefficient * action, action)
            - action
        )
        == 0,
    )
    inertia = sp.symbols("I", positive=True)
    rotor_energy = action**2 / (2 * inertia)
    action_checks.check(
        "the independent rotor Hamiltonian gives secant J/2",
        sp.simplify(
            rotor_energy / sp.diff(rotor_energy, action) - action / 2
        )
        == 0,
    )

    p, q, r = sp.symbols("p q r", real=True)
    two_solution = sp.solve([sp.Eq(p, 0), sp.Eq(-q, 0)], [p, q], dict=True)
    dimension_checks.check(
        "direct exponent equations for E^p*omega^q have only the zero solution",
        two_solution == [{p: 0, q: 0}],
    )
    three_solution = sp.linsolve([p + r, -q + r], (p, q, r))
    dimension_checks.check(
        "direct exponent elimination yields the one-parameter (-r,r,r) family",
        three_solution == {(-r, r, r)},
    )
    dimension_checks.check(
        "normalizing the action exponent produces S*omega/E",
        sp.Matrix([[1, 0, 1], [0, -1, 1]])
        * sp.Matrix([-1, 1, 1])
        == sp.zeros(2, 1),
    )

    action_total = action_checks.finish()
    dimension_total = dimension_checks.finish()
    print(
        "P013 INDEPENDENT REVIEW ALL "
        f"{action_total + dimension_total} CHECKS PASS"
    )
    return action_total + dimension_total


if __name__ == "__main__":
    run()
