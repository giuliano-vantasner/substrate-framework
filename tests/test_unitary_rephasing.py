from __future__ import annotations

import numpy as np
import pytest

from substrate_framework.matrix_decompositions import unitarity_residual
from substrate_framework.unitary_rephasing import (
    generic_rephasing_counts,
    invariant_quartet,
    rephase_unitary,
    rephasing_orbit_dimension,
    standard_three_angle_unitary,
    support_stabilizer_dimension,
)


@pytest.mark.parametrize(
    ("size", "angles", "orbit", "quotient", "phases"),
    [(1, 0, 1, 0, 0), (2, 1, 3, 1, 0), (3, 3, 5, 4, 1), (4, 6, 7, 9, 3)],
)
def test_generic_counts_close(size, angles, orbit, quotient, phases) -> None:
    counts = generic_rephasing_counts(size)
    assert counts.unitary_parameters == size**2
    assert counts.orthogonal_angles == angles
    assert counts.generic_orbit == orbit
    assert counts.generic_quotient == quotient
    assert counts.irreducible_phases == phases
    assert counts.orthogonal_angles + counts.generic_orbit + counts.irreducible_phases == size**2


@pytest.mark.parametrize("size", [True, 0, -1, 2.5])
def test_generic_counts_require_a_positive_integer(size) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        generic_rephasing_counts(size)


def test_support_graph_exposes_nongeneric_stabilizers() -> None:
    dense = standard_three_angle_unitary(0.31, 0.27, 0.44, 0.73)
    permutation = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    block = np.array(
        [[3 / 5, 4 / 5, 0], [-4 / 5, 3 / 5, 0], [0, 0, 1]], dtype=complex
    )
    assert support_stabilizer_dimension(dense) == 1
    assert support_stabilizer_dimension(block) == 2
    assert support_stabilizer_dimension(permutation) == 3
    assert rephasing_orbit_dimension(dense) == 5
    assert rephasing_orbit_dimension(block) == 4
    assert rephasing_orbit_dimension(permutation) == 3


def test_rephasing_preserves_unitarity_moduli_and_quartet() -> None:
    matrix = standard_three_angle_unitary(0.21, 0.17, 0.38, 0.61)
    before = invariant_quartet(matrix, 0, 1, 1, 2)
    transformed = rephase_unitary(matrix, [0.2, -0.7, 1.1], [0.4, 0.9, -0.3])
    after = invariant_quartet(transformed, 0, 1, 1, 2)
    assert unitarity_residual(transformed) < 2e-15
    assert np.allclose(np.abs(transformed), np.abs(matrix), atol=2e-15)
    assert after == pytest.approx(before, abs=2e-15)


def test_three_angle_quartet_matches_closed_form_and_conjugation_sign() -> None:
    t12, t13, t23, delta = 0.23, 0.19, 0.41, 0.67
    matrix = standard_three_angle_unitary(t12, t13, t23, delta)
    quartet = invariant_quartet(matrix, 0, 1, 1, 2)
    expected = (
        np.cos(t12)
        * np.cos(t23)
        * np.cos(t13) ** 2
        * np.sin(t12)
        * np.sin(t23)
        * np.sin(t13)
        * np.sin(delta)
    )
    assert unitarity_residual(matrix) < 2e-15
    assert quartet.imag == pytest.approx(expected, abs=2e-15)
    conjugated = invariant_quartet(matrix.conj(), 0, 1, 1, 2)
    assert conjugated.imag == pytest.approx(-quartet.imag, abs=2e-15)


def test_two_by_two_unitary_quartet_is_real() -> None:
    phase = np.exp(0.37j)
    rotation = np.array([[3 / 5, 4 / 5], [-4 / 5, 3 / 5]], dtype=complex)
    matrix = np.diag([phase, 1 / phase]) @ rotation @ np.diag([1j, -1j])
    assert unitarity_residual(matrix) < 2e-15
    assert abs(invariant_quartet(matrix, 0, 1, 0, 1).imag) < 2e-15


def test_wrong_quartet_conjugation_is_not_rephasing_invariant() -> None:
    matrix = standard_three_angle_unitary(0.21, 0.17, 0.38, 0.61)
    transformed = rephase_unitary(matrix, [0.2, -0.7, 1.1], [0.4, 0.9, -0.3])
    wrong_before = matrix[0, 1] * matrix[1, 2] * np.conj(matrix[0, 2]) * matrix[1, 1]
    wrong_after = transformed[0, 1] * transformed[1, 2] * np.conj(transformed[0, 2]) * transformed[1, 1]
    assert abs(wrong_after - wrong_before) > 1e-2


def test_invalid_unitary_and_phase_shapes_are_rejected() -> None:
    with pytest.raises(ValueError, match="unitary"):
        support_stabilizer_dimension([[1, 1], [0, 1]])
    with pytest.raises(ValueError, match="phase vectors"):
        rephase_unitary(np.eye(2), [0], [0, 1])
