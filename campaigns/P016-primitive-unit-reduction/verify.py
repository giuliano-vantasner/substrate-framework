#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for proposed C-DIM-002/C-MED-002."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.constitutive import (
    lattice_debye_energy,
    lattice_reduced_responses,
    local_wave_speed,
)
from substrate_framework.dimensional_analysis import monomial_exponents
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class PrimitiveCandidate:
    speed_time_exponent: int
    action_mass_exponent: int
    action_time_exponent: int
    length_length_exponent: int


def primitive_candidate_is_exact(candidate: PrimitiveCandidate) -> bool:
    matrix = sp.Matrix(
        [
            [0, candidate.action_mass_exponent, 0],
            [1, 2, candidate.length_length_exponent],
            [candidate.speed_time_exponent, candidate.action_time_exponent, 0],
        ]
    )
    if matrix.rank() != 3:
        return False
    try:
        mass = monomial_exponents(matrix, sp.Matrix([1, 0, 0]))
        energy = monomial_exponents(matrix, sp.Matrix([1, 2, -2]))
        time = monomial_exponents(matrix, sp.Matrix([0, 0, 1]))
    except ValueError:
        return False
    return (
        mass == sp.Matrix([-1, 1, -1])
        and energy == sp.Matrix([1, 1, -1])
        and time == sp.Matrix([-1, 0, 1])
    )


@dataclass(frozen=True)
class MediumCandidate:
    debye_length_power: int
    number_density_length_power: int
    mass_density_numerator: int
    mass_density_denominator: int


def medium_candidate_is_exact(candidate: MediumCandidate) -> bool:
    action, speed, length, ratio = sp.symbols("S c a kappa", positive=True)
    thermal = ratio * action * speed * length**candidate.debye_length_power
    number_density = length**candidate.number_density_length_power
    epsilon = sp.simplify(number_density * thermal / speed**2)
    inverse_mu = sp.simplify(number_density * thermal)
    mass_density = sp.simplify(
        sp.Rational(
            candidate.mass_density_numerator,
            candidate.mass_density_denominator,
        )
        * epsilon
    )
    expected = lattice_reduced_responses(action, speed, length, ratio)
    return (
        thermal == expected[0]
        and epsilon == expected[1]
        and inverse_mu == expected[2]
        and mass_density == expected[3]
    )


def run() -> int:
    dimension_checks = CheckLedger("C-DIM-002")
    medium_checks = CheckLedger("C-MED-002")

    primitives = sp.Matrix(
        [
            [0, 1, 0],
            [1, 2, 1],
            [-1, -1, 0],
        ]
    )
    dimension_checks.check(
        "the declared speed-action-length matrix has determinant -1 and full rank",
        primitives.det() == -1 and primitives.rank() == 3,
    )
    dimension_checks.check(
        "the full-rank primitive set has no dimensionless monomial kernel",
        primitives.nullspace() == [],
    )

    targets = {
        "mass": (sp.Matrix([1, 0, 0]), sp.Matrix([-1, 1, -1])),
        "energy": (sp.Matrix([1, 2, -2]), sp.Matrix([1, 1, -1])),
        "time": (sp.Matrix([0, 0, 1]), sp.Matrix([-1, 0, 1])),
        "density": (sp.Matrix([1, -3, 0]), sp.Matrix([-1, 1, -4])),
        "stiffness": (sp.Matrix([1, -1, -2]), sp.Matrix([1, 1, -4])),
    }
    for name, (target, expected) in targets.items():
        exponents = monomial_exponents(primitives, target)
        dimension_checks.check(
            f"the {name} target has its exact unique monomial exponents",
            exponents == expected and primitives * exponents == target,
        )

    speed_length_only = primitives[:, [0, 2]]
    mass_target = targets["mass"][0]
    dimension_checks.check(
        "speed and length alone cannot span a mass dimension",
        speed_length_only.rank() == 2
        and speed_length_only.row_join(mass_target).rank() == 3,
    )
    coefficient = sp.symbols("alpha", positive=True)
    action, speed, length = sp.symbols("S c a", positive=True)
    energy_monomial = action * speed / length
    dimension_checks.check(
        "dimensional uniqueness leaves every dimensionless coefficient free",
        sp.diff(coefficient * energy_monomial, coefficient) == energy_monomial
        and coefficient.is_number is not True,
    )
    dimension_checks.mutation_sensitive(
        "speed, action, and length dimensions",
        primitive_candidate_is_exact,
        PrimitiveCandidate(-1, 1, -1, 1),
        [
            PrimitiveCandidate(1, 1, -1, 1),
            PrimitiveCandidate(-1, 0, -1, 1),
            PrimitiveCandidate(-1, 1, 1, 1),
            PrimitiveCandidate(-1, 1, -1, 2),
        ],
    )

    ratio = sp.symbols("kappa", positive=True)
    thermal = lattice_debye_energy(action, speed, length, ratio)
    medium_checks.check(
        "the declared Debye scale retains its free dimensionless speed ratio",
        thermal == ratio * action * speed / length
        and sp.diff(thermal, ratio) == action * speed / length,
    )
    free_thermal = sp.symbols("Theta_free", positive=True)
    medium_checks.check(
        "an independent thermal scale is not eliminated without the Debye premise",
        sp.diff(free_thermal, length) == 0
        and sp.diff(thermal, length) == -ratio * action * speed / length**2
        and sp.simplify(free_thermal - thermal) != 0,
    )

    thermal, epsilon, inverse_mu, mass_density = lattice_reduced_responses(
        action, speed, length, ratio
    )
    medium_checks.check(
        "conditional substitution gives the exact reduced response formulas",
        thermal == ratio * action * speed / length
        and epsilon == ratio * action / (length**4 * speed)
        and inverse_mu == ratio * action * speed / length**4,
    )
    medium_checks.check(
        "the declared mass-density ratio supplies the load-bearing one-half",
        mass_density == ratio * action / (2 * length**4 * speed)
        and sp.simplify(mass_density - epsilon / 2) == 0,
    )
    source_expression_without_half = ratio * action / (length**4 * speed)
    medium_checks.check(
        "AS2's implemented rho expression without one-half is explicitly rejected",
        sp.simplify(source_expression_without_half - mass_density) != 0
        and sp.simplify(source_expression_without_half - epsilon) == 0,
    )
    medium_checks.check(
        "the co-scaled responses preserve the reference wave speed",
        sp.simplify(epsilon / inverse_mu - 1 / speed**2) == 0
        and local_wave_speed(epsilon, inverse_mu) == speed,
    )
    medium_checks.check(
        "density and stiffness dimensions agree with the primitive-basis theorem",
        monomial_exponents(primitives, targets["density"][0])
        == sp.Matrix([-1, 1, -4])
        and monomial_exponents(primitives, targets["stiffness"][0])
        == sp.Matrix([1, 1, -4]),
    )
    alternative_density_ratio = sp.symbols("r", positive=True)
    alternative = lattice_reduced_responses(
        action,
        speed,
        length,
        ratio,
        alternative_density_ratio,
    )
    medium_checks.check(
        "dimensional analysis cannot select the mass-density conversion ratio",
        sp.simplify(alternative[3] - alternative_density_ratio * epsilon) == 0
        and sp.diff(alternative[3], alternative_density_ratio) == epsilon,
    )
    medium_checks.mutation_sensitive(
        "Debye, number-density, and mass-density premises",
        medium_candidate_is_exact,
        MediumCandidate(-1, -3, 1, 2),
        [
            MediumCandidate(-2, -3, 1, 2),
            MediumCandidate(-1, -2, 1, 2),
            MediumCandidate(-1, -3, 1, 1),
            MediumCandidate(-1, -3, 2, 3),
        ],
    )

    dimension_total = dimension_checks.finish()
    medium_total = medium_checks.finish()
    print(f"P016 ALL {dimension_total + medium_total} CHECKS PASS")
    return dimension_total + medium_total


if __name__ == "__main__":
    run()
