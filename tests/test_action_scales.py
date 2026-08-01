from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.action_scales import (
    rigid_rotor_energy,
    rigid_rotor_normalized_action,
    secant_action_scale,
)
from substrate_framework.dimensional_analysis import (
    dimensionless_group_count,
    dimensionless_mass_coordinate,
    dimensionless_monomial_basis,
    mass_from_dimensionless_coordinate,
    monomial_exponents,
)


def test_rotor_secant_is_half_the_normalized_action() -> None:
    inertia, frequency = sp.symbols("I omega", positive=True)
    energy = rigid_rotor_energy(inertia, frequency)
    action = rigid_rotor_normalized_action(inertia, frequency)
    assert sp.simplify(secant_action_scale(energy, frequency) - action / 2) == 0


def test_dimensionless_group_bases_are_exact() -> None:
    two_scale = sp.Matrix([[1, 0], [0, -1]])
    three_scale = sp.Matrix([[1, 0, 1], [0, -1, 1]])
    assert dimensionless_group_count(two_scale) == 0
    assert dimensionless_monomial_basis(two_scale) == ()
    basis = dimensionless_monomial_basis(three_scale)
    assert dimensionless_group_count(three_scale) == 1
    assert len(basis) == 1
    assert basis[0] == sp.Matrix([-1, 1, 1])


def test_speed_action_length_basis_has_unique_target_exponents() -> None:
    primitives = sp.Matrix(
        [
            [0, 1, 0],
            [1, 2, 1],
            [-1, -1, 0],
        ]
    )
    assert monomial_exponents(primitives, sp.Matrix([1, 0, 0])) == sp.Matrix(
        [-1, 1, -1]
    )
    assert monomial_exponents(primitives, sp.Matrix([1, 2, -2])) == sp.Matrix(
        [1, 1, -1]
    )


def test_monomial_exponent_solver_rejects_nonunique_or_unspanned_targets() -> None:
    with pytest.raises(ValueError, match="not unique"):
        monomial_exponents(sp.Matrix([[1, 1], [0, 0]]), sp.Matrix([1, 0]))
    with pytest.raises(ValueError, match="outside"):
        monomial_exponents(sp.Matrix([[1], [0]]), sp.Matrix([0, 1]))


def test_dimensionless_mass_coordinate_is_an_exact_bijection() -> None:
    mass, speed, action, length = sp.symbols("m c S a", positive=True)
    coordinate = dimensionless_mass_coordinate(mass, speed, action, length)
    assert coordinate == mass * speed * length / action
    assert (
        mass_from_dimensionless_coordinate(coordinate, speed, action, length)
        == mass
    )


def test_mass_coordinate_retains_an_arbitrary_dimensionless_input() -> None:
    coordinate, speed, action, length = sp.symbols("N c S a", positive=True)
    mass = mass_from_dimensionless_coordinate(coordinate, speed, action, length)
    assert mass == coordinate * action / (speed * length)
    assert sp.diff(mass, coordinate) == action / (speed * length)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: secant_action_scale(0, 1), "energy"),
        (lambda: secant_action_scale(1, 0), "frequency"),
        (lambda: rigid_rotor_energy(-1, 1), "inertia"),
        (lambda: rigid_rotor_normalized_action(1, -1), "angular_frequency"),
        (lambda: dimensionless_mass_coordinate(0, 1, 1, 1), "mass"),
        (lambda: dimensionless_mass_coordinate(1, 0, 1, 1), "speed"),
        (lambda: dimensionless_mass_coordinate(1, 1, 0, 1), "action"),
        (lambda: dimensionless_mass_coordinate(1, 1, 1, 0), "length"),
        (lambda: mass_from_dimensionless_coordinate(0, 1, 1, 1), "coordinate"),
    ],
)
def test_numeric_positive_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
