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
    dimensionless_monomial_basis,
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


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: secant_action_scale(0, 1), "energy"),
        (lambda: secant_action_scale(1, 0), "frequency"),
        (lambda: rigid_rotor_energy(-1, 1), "inertia"),
        (lambda: rigid_rotor_normalized_action(1, -1), "angular_frequency"),
    ],
)
def test_numeric_positive_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
