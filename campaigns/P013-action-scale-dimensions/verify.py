#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for proposed C-ACT-001/C-DIM-001."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.action_scales import (
    rigid_rotor_energy,
    rigid_rotor_normalized_action,
    secant_action_scale,
)
from substrate_framework.dimensional_analysis import (
    dimensionless_group_count,
    dimensionless_monomial_basis,
)
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class RotorCandidate:
    energy_numerator: int
    energy_denominator: int
    action_coefficient: int


def rotor_candidate_is_exact(candidate: RotorCandidate) -> bool:
    inertia, frequency = sp.symbols("I omega", positive=True)
    energy = (
        sp.Rational(candidate.energy_numerator, candidate.energy_denominator)
        * inertia
        * frequency**2
    )
    action = candidate.action_coefficient * inertia * frequency
    return sp.simplify(energy / frequency - action / 2) == 0


@dataclass(frozen=True)
class DimensionCandidate:
    frequency_time_exponent: int
    action_time_exponent: int


def dimension_candidate_is_exact(candidate: DimensionCandidate) -> bool:
    two = sp.Matrix([[1, 0], [0, candidate.frequency_time_exponent]])
    three = sp.Matrix(
        [
            [1, 0, 1],
            [0, candidate.frequency_time_exponent, candidate.action_time_exponent],
        ]
    )
    basis = dimensionless_monomial_basis(three)
    return (
        dimensionless_group_count(two) == 0
        and dimensionless_monomial_basis(two) == ()
        and dimensionless_group_count(three) == 1
        and len(basis) == 1
        and basis[0] == sp.Matrix([-1, 1, 1])
    )


def run() -> int:
    action_checks = CheckLedger("C-ACT-001")
    dimension_checks = CheckLedger("C-DIM-001")
    action = sp.symbols("J", positive=True)
    energy = sp.Function("E")(action)
    frequency = sp.diff(energy, action)

    quotient_derivative = sp.diff(energy / action, action)
    action_checks.check(
        "the derivative of E/J is exactly the secant-equality residual",
        sp.simplify(
            quotient_derivative
            - (action * frequency - energy) / action**2
        )
        == 0,
    )
    action_checks.check(
        "E/frequency=J is equivalent to the zero derivative of E/J",
        sp.simplify(
            (energy - action * frequency) + action**2 * quotient_derivative
        )
        == 0,
    )

    coefficient = sp.symbols("C", positive=True)
    linear_energy = coefficient * action
    action_checks.check(
        "every positive linear energy law satisfies the action-secant identity",
        sp.simplify(
            linear_energy / sp.diff(linear_energy, action) - action
        )
        == 0,
    )
    nonlinear_energy = coefficient * action**2
    action_checks.check(
        "a quadratic energy law gives half the action rather than the action",
        sp.simplify(
            nonlinear_energy / sp.diff(nonlinear_energy, action) - action / 2
        )
        == 0,
    )

    inertia, angular_frequency = sp.symbols("I omega", positive=True)
    rotor_energy = rigid_rotor_energy(inertia, angular_frequency)
    rotor_action = rigid_rotor_normalized_action(inertia, angular_frequency)
    action_checks.check(
        "the rigid-rotor contour action is normalized as I*omega",
        rotor_action == inertia * angular_frequency,
    )
    action_checks.check(
        "the rigid-rotor secant is exactly half its normalized action",
        sp.simplify(
            secant_action_scale(rotor_energy, angular_frequency)
            - rotor_action / 2
        )
        == 0,
    )
    rotor_energy_from_action = rotor_action**2 / (2 * inertia)
    action_checks.check(
        "the canonical derivative of rotor energy recovers angular frequency",
        sp.simplify(
            sp.diff(action**2 / (2 * inertia), action).subs(action, rotor_action)
            - angular_frequency
        )
        == 0
        and sp.simplify(rotor_energy_from_action - rotor_energy) == 0,
    )
    action_checks.mutation_sensitive(
        "rotor energy half-factor and normalized-action coefficient",
        rotor_candidate_is_exact,
        RotorCandidate(1, 2, 1),
        [
            RotorCandidate(1, 1, 1),
            RotorCandidate(1, 3, 1),
            RotorCandidate(1, 2, 2),
        ],
    )

    two_scale = sp.Matrix([[1, 0], [0, -1]])
    dimension_checks.check(
        "the E and omega primitive set has full rank and no dimensionless monomial",
        two_scale.rank() == 2
        and dimensionless_group_count(two_scale) == 0
        and dimensionless_monomial_basis(two_scale) == (),
    )
    three_scale = sp.Matrix([[1, 0, 1], [0, -1, 1]])
    basis = dimensionless_monomial_basis(three_scale)
    dimension_checks.check(
        "adding one action scale creates exactly one dimensionless group",
        three_scale.rank() == 2
        and dimensionless_group_count(three_scale) == 1
        and len(basis) == 1,
    )
    dimension_checks.check(
        "the unique normalized exponent vector is (-1,1,1)",
        basis[0] == sp.Matrix([-1, 1, 1])
        and three_scale * basis[0] == sp.zeros(2, 1),
    )
    dimension_checks.check(
        "the exponent vector represents S*omega/E",
        sp.simplify(
            sp.Symbol("E", positive=True) ** basis[0][0]
            * sp.Symbol("omega", positive=True) ** basis[0][1]
            * sp.Symbol("S", positive=True) ** basis[0][2]
            - sp.Symbol("S", positive=True)
            * sp.Symbol("omega", positive=True)
            / sp.Symbol("E", positive=True)
        )
        == 0,
    )
    dimension_checks.mutation_sensitive(
        "frequency and action time dimensions",
        dimension_candidate_is_exact,
        DimensionCandidate(-1, 1),
        [
            DimensionCandidate(0, 1),
            DimensionCandidate(1, 1),
            DimensionCandidate(-1, 0),
        ],
    )

    action_total = action_checks.finish()
    dimension_total = dimension_checks.finish()
    print(f"P013 ALL {action_total + dimension_total} CHECKS PASS")
    return action_total + dimension_total


if __name__ == "__main__":
    run()
