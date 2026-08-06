from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from substrate_framework.common_phase_matrices import (
    common_phase_grams,
    odd_antisymmetric_trace,
    real_gram_relative_basis,
)
from substrate_framework.matrix_decompositions import unitarity_residual
from substrate_framework.unitary_rephasing import invariant_quartet


def test_common_phase_cancels_from_both_rectangular_grams() -> None:
    real = np.array([[1.0, -2.0, 3.0], [4.0, 0.5, -1.0]])
    expected_left = real @ real.T
    expected_right = real.T @ real
    for phase in (-2.1, 0.0, 0.73, 9.4):
        result = common_phase_grams(real, phase)
        assert np.allclose(result.left_gram, expected_left, atol=2e-14)
        assert np.allclose(result.right_gram, expected_right, atol=2e-14)


def test_two_separate_global_phases_still_give_a_real_relative_basis() -> None:
    first = np.array([[1.0, 2.0, 0.0], [0.0, 1.0, -1.0], [2.0, 0.0, 1.0]])
    second = np.array([[2.0, -1.0], [1.0, 3.0], [0.5, 2.0]])
    result = real_gram_relative_basis(
        first,
        second,
        first_phase=0.37,
        second_phase=-1.29,
    )
    assert unitarity_residual(result.relative_basis) < 2e-15
    assert np.max(np.abs(result.relative_basis.imag)) == 0.0
    for rows in ((0, 1), (0, 2), (1, 2)):
        for columns in ((0, 1), (0, 2), (1, 2)):
            quartet = invariant_quartet(
                result.relative_basis,
                rows[0],
                rows[1],
                columns[0],
                columns[1],
            )
            assert quartet.imag == 0.0


@pytest.mark.parametrize("dimension", [2, 3, 4, 5])
def test_real_gram_commutator_is_antisymmetric_with_zero_odd_traces(
    dimension: int,
) -> None:
    first = np.arange(1, dimension * (dimension + 1) + 1, dtype=float).reshape(
        dimension, dimension + 1
    )
    second = np.flip(first, axis=1) + np.eye(dimension, dimension + 1)
    result = real_gram_relative_basis(first, second)
    assert np.allclose(result.commutator.T, -result.commutator, atol=2e-12)
    for power in (1, 3, 5):
        scale = max(1.0, np.linalg.norm(result.commutator, ord=np.inf) ** power)
        relative_trace = abs(
            odd_antisymmetric_trace(result.commutator, power)
        ) / scale
        assert relative_trace < 2e-14
    if dimension % 2 == 1:
        determinant_scale = max(
            1.0,
            np.linalg.norm(result.commutator, ord=np.inf) ** dimension,
        )
        assert abs(np.linalg.det(result.commutator)) / determinant_scale < 2e-14


def test_degenerate_gram_allows_complex_coordinate_basis_but_real_choice_exists() -> None:
    identity = np.eye(3)
    result = real_gram_relative_basis(identity, identity)
    omega = np.exp(2j * np.pi / 3)
    fourier = np.array(
        [[1, 1, 1], [1, omega, omega**2], [1, omega**2, omega]],
        dtype=complex,
    ) / np.sqrt(3.0)
    assert np.allclose(fourier.conj().T @ identity @ fourier, identity, atol=2e-15)
    assert abs(invariant_quartet(fourier, 0, 1, 1, 2).imag) > 1e-2
    assert np.array_equal(result.relative_basis, identity)
    assert np.array_equal(result.commutator, np.zeros((3, 3)))


def test_entrywise_complex_structure_breaks_the_common_phase_premise() -> None:
    real_part = np.diag([1.0, 2.0, 4.0])
    imaginary_part = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0]])
    matrix = real_part + 1j * imaginary_part
    gram = matrix @ matrix.conj().T
    assert np.max(np.abs(gram.imag)) > 1.0
    with pytest.raises(ValueError, match="exactly real"):
        common_phase_grams(matrix, 0.3)


@pytest.mark.parametrize(
    ("operation", "message"),
    [
        (lambda: common_phase_grams([], 0.0), "non-empty"),
        (lambda: common_phase_grams([[1.0 + 1j]], 0.0), "exactly real"),
        (lambda: common_phase_grams([[1.0]], np.inf), "finite real"),
        (lambda: common_phase_grams([[1.0]], True), "finite real"),
        (lambda: real_gram_relative_basis(np.ones((2, 2)), np.ones((3, 2))), "row dimension"),
        (lambda: odd_antisymmetric_trace(np.eye(2), 3), "antisymmetric"),
        (lambda: odd_antisymmetric_trace([[0.0, 1.0], [-1.0, 0.0]], 2), "odd positive"),
    ],
)
def test_invalid_inputs_are_rejected(operation, message: str) -> None:
    with pytest.raises((TypeError, ValueError), match=message):
        operation()


def test_canonical_module_uses_no_numpy_quadrature_name() -> None:
    source = Path("src/substrate_framework/common_phase_matrices.py").read_text()
    assert "np." + "trapz" not in source
    assert "np." + "trapezoid" not in source
