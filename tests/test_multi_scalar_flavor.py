from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.multi_scalar_flavor import (
    multi_scalar_mass_basis_ledger,
    off_diagonal_part,
    takagi_multi_scalar_mass_basis_ledger,
)


def test_diagonal_mass_sum_does_not_force_diagonal_scalar_couplings() -> None:
    a = sp.symbols("a", nonzero=True)
    first = sp.Matrix([[1, a], [a, 2]])
    second = sp.Matrix([[0, -a], [-a, 1]])
    ledger = multi_scalar_mass_basis_ledger(
        (first, second),
        (1, 1),
        sp.eye(2),
        sp.eye(2),
    )
    assert ledger.diagonal_mass_matrix == sp.diag(1, 3)
    assert ledger.reconstructed_diagonal_mass_matrix == sp.diag(1, 3)
    assert ledger.reconstruction_residual == sp.zeros(2)
    assert ledger.off_diagonal_couplings[0] == sp.Matrix([[0, a], [a, 0]])
    assert ledger.off_diagonal_couplings[1] == -ledger.off_diagonal_couplings[0]
    assert ledger.all_couplings_diagonal is False


def test_common_matrix_alignment_is_sufficient_in_a_diagonalizing_basis() -> None:
    reference = sp.diag(2, 5, 11)
    ledger = multi_scalar_mass_basis_ledger(
        (reference, -3 * reference, 7 * reference),
        (2, 1, -1),
        sp.eye(3),
        sp.eye(3),
    )
    assert ledger.mass_matrix == -8 * reference
    assert ledger.all_couplings_diagonal
    assert all(matrix == sp.zeros(3) for matrix in ledger.off_diagonal_couplings)


def test_zero_combined_alignment_coefficient_does_not_force_diagonality() -> None:
    reference = sp.Matrix([[0, 1], [1, 0]])
    ledger = multi_scalar_mass_basis_ledger(
        (reference, -reference),
        (1, 1),
        sp.eye(2),
        sp.eye(2),
    )
    assert ledger.mass_matrix == sp.zeros(2)
    assert ledger.diagonal_mass_matrix == sp.zeros(2)
    assert not ledger.all_couplings_diagonal


def test_takagi_wrapper_uses_conjugate_right_basis() -> None:
    unitary = sp.Matrix([[1, sp.I], [sp.I, 1]]) / sp.sqrt(2)
    first = sp.diag(-sp.Rational(1, 2), sp.Rational(1, 2))
    second = sp.Matrix([[0, sp.Rational(3, 2)], [sp.Rational(3, 2), 0]])
    ledger = takagi_multi_scalar_mass_basis_ledger(
        (first, second),
        (1, sp.I),
        unitary,
    )
    assert ledger.mass_matrix == sp.Matrix(
        [[-sp.Rational(1, 2), 3 * sp.I / 2], [3 * sp.I / 2, sp.Rational(1, 2)]]
    )
    assert ledger.diagonal_mass_matrix == sp.diag(1, 2)
    assert ledger.all_couplings_diagonal

    wrong = tuple(
        sp.simplify(unitary.adjoint() * matrix * unitary)
        for matrix in (first, second)
    )
    assert any(off_diagonal_part(matrix) != sp.zeros(2) for matrix in wrong)


def test_degenerate_mass_basis_can_change_individual_diagonality() -> None:
    first = sp.diag(1, 0)
    second = sp.diag(0, 1)
    identity_ledger = multi_scalar_mass_basis_ledger(
        (first, second), (1, 1), sp.eye(2), sp.eye(2)
    )
    rotation = sp.Matrix([[1, 1], [-1, 1]]) / sp.sqrt(2)
    rotated_ledger = multi_scalar_mass_basis_ledger(
        (first, second), (1, 1), rotation, rotation
    )
    assert identity_ledger.diagonal_mass_matrix == sp.eye(2)
    assert rotated_ledger.diagonal_mass_matrix == sp.eye(2)
    assert identity_ledger.all_couplings_diagonal
    assert not rotated_ledger.all_couplings_diagonal


def test_nontrivial_real_rotation_reconstructs_every_transformed_coupling() -> None:
    rotation = sp.Matrix([[1, 1], [-1, 1]]) / sp.sqrt(2)
    first = rotation * sp.diag(1, 4) * rotation.T
    second = rotation * sp.diag(3, -2) * rotation.T
    ledger = multi_scalar_mass_basis_ledger(
        (first, second), (2, -1), rotation, rotation
    )
    assert ledger.diagonal_mass_matrix == sp.diag(-1, 10)
    assert ledger.mass_basis_couplings == (sp.diag(1, 4), sp.diag(3, -2))
    assert ledger.all_couplings_diagonal


@pytest.mark.parametrize(
    ("operation", "message"),
    [
        (
            lambda: multi_scalar_mass_basis_ledger((), (), sp.eye(1), sp.eye(1)),
            "at least one",
        ),
        (
            lambda: multi_scalar_mass_basis_ledger(
                (sp.eye(2),), (), sp.eye(2), sp.eye(2)
            ),
            "one scalar weight",
        ),
        (
            lambda: multi_scalar_mass_basis_ledger(
                (sp.eye(2), sp.eye(3)), (1, 1), sp.eye(2), sp.eye(2)
            ),
            "common square shape",
        ),
        (
            lambda: multi_scalar_mass_basis_ledger(
                (sp.eye(2),), (1,), [[1, 1], [0, 1]], sp.eye(2)
            ),
            "exactly unitary",
        ),
        (
            lambda: multi_scalar_mass_basis_ledger(
                (sp.Matrix([[1, 1], [1, 2]]),), (1,), sp.eye(2), sp.eye(2)
            ),
            "do not diagonalize",
        ),
        (
            lambda: multi_scalar_mass_basis_ledger(
                ([[1.0]],), (1,), sp.eye(1), sp.eye(1)
            ),
            "exact rather than floating",
        ),
        (
            lambda: takagi_multi_scalar_mass_basis_ledger(
                (sp.Matrix([[0, 1], [0, 0]]),), (1,), sp.eye(2)
            ),
            "must be symmetric",
        ),
    ],
)
def test_multi_scalar_api_rejects_invalid_inputs(operation, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        operation()


def test_canonical_module_has_no_numpy_or_quadrature_surface() -> None:
    source = Path("src/substrate_framework/multi_scalar_flavor.py").read_text(
        encoding="utf-8"
    )
    assert "numpy" not in source
    assert "np." + "trapz" not in source
    assert "np." + "trapezoid" not in source
