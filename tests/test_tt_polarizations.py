from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.tt_angular import (
    circular_tt_polarizations,
    frobenius_inner_product,
    rotated_tt_polarizations,
    tt_basis_reconstruct,
    tt_operator_matrix,
    tt_polarization_basis,
    tt_project_symmetric,
)


def test_axis_basis_is_normalized_transverse_traceless_and_oriented() -> None:
    basis = tt_polarization_basis([0, 0, 1], reference=[1, 0, 0])
    assert basis.first_transverse.cross(basis.second_transverse) == basis.direction
    for tensor in (basis.plus, basis.cross):
        assert tensor == tensor.T
        assert sp.trace(tensor) == 0
        assert tensor * basis.direction == sp.zeros(3, 1)
        assert frobenius_inner_product(tensor, tensor) == 1
    assert frobenius_inner_product(basis.plus, basis.cross) == 0


def test_basis_reconstruction_equals_tt_projection_for_arbitrary_direction() -> None:
    direction = sp.Matrix([1, 2, 2])
    basis = tt_polarization_basis(direction, reference=[1, -1, 0])
    tensor = sp.Matrix([[3, 2, 1], [2, -1, 4], [1, 4, 5]])
    assert sp.simplify(
        tt_basis_reconstruct(tensor, basis) - tt_project_symmetric(tensor, direction)
    ) == sp.zeros(3)


def test_tt_operator_has_exact_rank_two_projector_spectrum() -> None:
    operator = tt_operator_matrix([1, 2, 2])
    assert sp.simplify(operator - operator.T) == sp.zeros(6)
    assert sp.simplify(operator**2 - operator) == sp.zeros(6)
    assert sp.trace(operator) == 2
    assert operator.rank() == 2
    assert operator.eigenvals() == {sp.Integer(1): 2, sp.Integer(0): 4}


@pytest.mark.parametrize("direction", ([1, 0, 0], [0, 1, 0], [0, 0, 1]))
def test_piecewise_default_frame_covers_coordinate_axes(direction) -> None:
    basis = tt_polarization_basis(direction)
    assert basis.first_transverse.dot(basis.direction) == 0
    assert basis.second_transverse.dot(basis.direction) == 0
    assert basis.first_transverse.dot(basis.second_transverse) == 0


def test_transverse_frame_rotation_has_double_angle_law() -> None:
    angle = sp.symbols("psi", real=True)
    basis = tt_polarization_basis([0, 0, 1], reference=[1, 0, 0])
    plus, cross = rotated_tt_polarizations(basis, angle)
    first = sp.cos(angle) * basis.first_transverse + sp.sin(angle) * basis.second_transverse
    second = -sp.sin(angle) * basis.first_transverse + sp.cos(angle) * basis.second_transverse
    direct_plus = sp.simplify((first * first.T - second * second.T) / sp.sqrt(2))
    direct_cross = sp.simplify((first * second.T + second * first.T) / sp.sqrt(2))
    assert sp.simplify(plus - direct_plus) == sp.zeros(3)
    assert sp.simplify(cross - direct_cross) == sp.zeros(3)


def test_circular_basis_has_opposite_weight_two_frame_phases() -> None:
    angle = sp.symbols("psi", real=True)
    basis = tt_polarization_basis([0, 0, 1], reference=[1, 0, 0])
    right, left = circular_tt_polarizations(basis)
    rotated_plus, rotated_cross = rotated_tt_polarizations(basis, angle)
    rotated_right = sp.simplify((rotated_plus + sp.I * rotated_cross) / sp.sqrt(2))
    rotated_left = sp.simplify((rotated_plus - sp.I * rotated_cross) / sp.sqrt(2))
    right_phase = sp.cos(2 * angle) - sp.I * sp.sin(2 * angle)
    left_phase = sp.cos(2 * angle) + sp.I * sp.sin(2 * angle)
    assert sp.simplify(rotated_right - right_phase * right) == sp.zeros(3)
    assert sp.simplify(rotated_left - left_phase * left) == sp.zeros(3)


def test_gw3_unnormalized_tensors_have_norm_squared_two() -> None:
    source_plus = sp.diag(1, -1, 0)
    source_cross = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    assert frobenius_inner_product(source_plus, source_plus) == 2
    assert frobenius_inner_product(source_cross, source_cross) == 2
    basis = tt_polarization_basis([0, 0, 1], reference=[1, 0, 0])
    assert source_plus == sp.sqrt(2) * basis.plus
    assert source_cross == sp.sqrt(2) * basis.cross


def test_parallel_reference_and_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="parallel"):
        tt_polarization_basis([0, 0, 1], reference=[0, 0, 2])
    with pytest.raises(ValueError, match="nonzero"):
        tt_polarization_basis([0, 0, 0])
    with pytest.raises(ValueError, match="shapes"):
        frobenius_inner_product(sp.eye(2), sp.eye(3))
