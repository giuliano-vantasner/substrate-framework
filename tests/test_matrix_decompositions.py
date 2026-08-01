from __future__ import annotations

import numpy as np
import pytest

from substrate_framework.matrix_decompositions import (
    biunitary_decomposition,
    gram_eigenvalues,
    real_symmetric_rotation,
    relative_left_basis,
    unitarity_residual,
)


def assert_decomposition(matrix: np.ndarray, tolerance: float = 2e-12) -> None:
    result = biunitary_decomposition(matrix)
    assert result.diagonal.shape == matrix.shape
    assert np.all(result.singular_values >= 0.0)
    assert unitarity_residual(result.left) < tolerance
    assert unitarity_residual(result.right) < tolerance
    assert np.max(np.abs(result.reconstruct() - matrix)) < tolerance
    assert np.max(np.abs(result.diagonalize(matrix) - result.diagonal)) < tolerance


def test_complex_square_decomposition_uses_one_explicit_convention() -> None:
    matrix = np.array([[1 + 1j, -1], [0, 1 - 1j]], dtype=complex)
    assert_decomposition(matrix)


def test_rectangular_and_rank_deficient_cases_are_supported() -> None:
    rectangular = np.array(
        [[1 + 1j, 2], [2 + 2j, 4], [-1j, 3]],
        dtype=complex,
    )
    rank_deficient = np.array([[1, 2, 3], [2, 4, 6]], dtype=complex)
    assert_decomposition(rectangular)
    assert_decomposition(rank_deficient)
    assert biunitary_decomposition(rank_deficient).singular_values[-1] < 1e-12


def test_gram_spectra_have_the_squared_nonzero_singular_values() -> None:
    matrix = np.array([[1 + 1j, 2, 0], [0, -1j, 3]], dtype=complex)
    result = biunitary_decomposition(matrix)
    left, right = gram_eigenvalues(matrix)
    expected = result.singular_values**2
    assert np.allclose(left[: len(expected)], expected, atol=2e-12)
    assert np.allclose(right[: len(expected)], expected, atol=2e-12)
    assert abs(right[-1]) < 2e-12


def test_repeated_singular_subspace_has_nonunique_paired_bases() -> None:
    matrix = 3.0 * np.eye(2, dtype=complex)
    result = biunitary_decomposition(matrix)
    phase_rotation = np.array(
        [[1, 1j], [1j, 1]], dtype=complex
    ) / np.sqrt(2.0)
    left = result.left @ phase_rotation
    right = result.right @ phase_rotation
    reconstructed = left @ result.diagonal @ right.conj().T
    assert unitarity_residual(phase_rotation) < 2e-15
    assert np.max(np.abs(reconstructed - matrix)) < 2e-12
    assert not np.allclose(left, result.left)


def test_relative_left_basis_is_unitary_and_aligned_bases_give_identity() -> None:
    first = biunitary_decomposition(
        np.array([[1 + 1j, -1], [0, 1 - 1j]], dtype=complex)
    ).left
    second = biunitary_decomposition(
        np.array([[0, -1 + 1j], [-1 - 1j, 1j]], dtype=complex)
    ).left
    relative = relative_left_basis(first, second)
    assert unitarity_residual(relative) < 2e-12
    assert np.allclose(relative_left_basis(first, first), np.eye(2), atol=2e-12)


def test_nonunitary_basis_and_wrong_conjugation_are_rejected() -> None:
    unitary = np.array([[1, 1j], [1j, 1]], dtype=complex) / np.sqrt(2.0)
    with pytest.raises(ValueError, match="first basis"):
        relative_left_basis(1.1 * unitary, unitary)

    matrix = np.array([[1 + 2j, -3j], [2, 1 - 1j]], dtype=complex)
    result = biunitary_decomposition(matrix)
    correct = result.left @ result.diagonal @ result.right.conj().T
    wrong = result.left @ result.diagonal @ result.right.T
    assert np.max(np.abs(correct - matrix)) < 2e-12
    assert np.max(np.abs(wrong - matrix)) > 1e-2


def test_real_symmetric_rotation_diagonalizes_and_handles_degeneracy() -> None:
    result = real_symmetric_rotation([[1.0, 0.5], [0.5, 2.0]])
    assert result.angle == pytest.approx(np.pi / 8)
    assert np.max(np.abs(result.rotation.T @ result.rotation - np.eye(2))) < 2e-15
    assert np.max(np.abs(result.diagonalized - np.diag(np.diag(result.diagonalized)))) < 2e-15

    degenerate = real_symmetric_rotation(4.0 * np.eye(2))
    assert degenerate.angle == 0.0
    assert np.array_equal(degenerate.rotation, np.eye(2))


@pytest.mark.parametrize(
    ("matrix", "message"),
    [
        ([[1, 0, 0], [0, 1, 0]], "2 by 2"),
        ([[1, 2], [0, 1]], "symmetric"),
        ([[1, 1j], [-1j, 2]], "real"),
    ],
)
def test_real_symmetric_rotation_rejects_out_of_scope_matrices(matrix, message) -> None:
    with pytest.raises(ValueError, match=message):
        real_symmetric_rotation(matrix)


@pytest.mark.parametrize("matrix", [[], [1, 2], [[np.inf]]])
def test_decomposition_rejects_invalid_matrices(matrix) -> None:
    with pytest.raises(ValueError, match="matrix"):
        biunitary_decomposition(matrix)
