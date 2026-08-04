from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.su2_doublets import (
    su2_chiral_factor_ledger,
    su2_common_charge_ledger,
    su2_fundamental_ledger,
    su2_same_carrier_projector_ledger,
)
from substrate_framework.symmetric_spin import symmetric_spin_rung


def _all_zero(matrices: tuple[sp.ImmutableMatrix, ...]) -> bool:
    return all(matrix == sp.zeros(*matrix.shape) for matrix in matrices)


def test_fundamental_ledger_closes_and_matches_accepted_n1_ladder() -> None:
    ledger = su2_fundamental_ledger()
    assert all(generator == generator.H for generator in ledger.generators)
    assert all(sp.trace(generator) == 0 for generator in ledger.generators)
    assert _all_zero(ledger.commutator_residuals)
    assert ledger.casimir == sp.Rational(3, 4) * sp.eye(2)
    assert ledger.commutant_basis == (sp.eye(2),)

    bottom = sp.ImmutableMatrix([0, 1])
    top = sp.ImmutableMatrix([1, 0])
    accepted = symmetric_spin_rung(1, 0)
    assert ledger.raising_operator * bottom == accepted.raising_coefficient * top
    assert ledger.lowering_operator * top == accepted.raising_coefficient * bottom


def test_independent_rank_one_factor_is_hermitian_and_closes() -> None:
    projector = sp.diag(1, 0)
    exchange = sp.ImmutableMatrix([[0, 1], [1, 0]])
    ledger = su2_chiral_factor_ledger(
        projector,
        parity_exchange=exchange,
    )
    assert ledger.complementary_projector == sp.diag(0, 1)
    assert _all_zero(ledger.left_hermiticity_residuals)
    assert _all_zero(ledger.right_hermiticity_residuals)
    assert _all_zero(ledger.left_commutator_residuals)
    assert _all_zero(ledger.right_commutator_residuals)
    assert _all_zero(ledger.parity_left_to_right_residuals or ())
    assert _all_zero(ledger.parity_vector_even_residuals or ())
    assert _all_zero(ledger.parity_axial_odd_residuals or ())

    right_subspace = sp.kronecker_product(sp.eye(2), sp.ImmutableMatrix([0, 1]))
    for generator in ledger.left_generators:
        assert generator * right_subspace == sp.zeros(4, 2)


def test_left_operator_is_exchanged_not_itself_parity_odd() -> None:
    ledger = su2_chiral_factor_ledger(
        sp.diag(1, 0),
        parity_exchange=sp.ImmutableMatrix([[0, 1], [1, 0]]),
    )
    assert all(
        left != right and left != -right
        for left, right in zip(
            ledger.left_generators,
            ledger.right_generators,
            strict=True,
        )
    )
    assert all(
        vector == left + right and axial == left - right
        for vector, axial, left, right in zip(
            ledger.vector_generators,
            ledger.axial_generators,
            ledger.left_generators,
            ledger.right_generators,
            strict=True,
        )
    )


def test_w2_same_carrier_projector_is_not_an_su2_representation() -> None:
    ledger = su2_same_carrier_projector_ledger(sp.diag(1, 0))
    assert ledger.projector_rank == 1
    assert ledger.projector_in_fundamental_commutant is False
    assert sum(residual != sp.zeros(2) for residual in ledger.hermiticity_residuals) == 2
    assert all(residual != sp.zeros(2) for residual in ledger.commutator_residuals)
    assert sum(
        residual != sp.zeros(2)
        for residual in ledger.projector_commutator_residuals
    ) == 2


def test_only_scalar_same_carrier_projectors_commute() -> None:
    fundamental = su2_fundamental_ledger()
    assert fundamental.commutant_basis == (sp.eye(2),)
    identity = su2_same_carrier_projector_ledger(sp.eye(2))
    zero = su2_same_carrier_projector_ledger(sp.zeros(2))
    assert identity.projector_in_fundamental_commutant
    assert zero.projector_in_fundamental_commutant
    assert identity.projector_rank == 2
    assert zero.projector_rank == 0


def test_common_abelian_charge_has_unit_separation() -> None:
    y, coefficient = sp.symbols("y c", real=True)
    ledger = su2_common_charge_ledger(y, coefficient=coefficient)
    assert _all_zero(ledger.commutator_residuals)
    assert ledger.upper_eigenvalue == coefficient * y + sp.Rational(1, 2)
    assert ledger.lower_eigenvalue == coefficient * y - sp.Rational(1, 2)
    assert ledger.eigenvalue_separation == 1


def test_w2_labels_require_a_declared_half_charge_rescaling() -> None:
    incompatible = su2_common_charge_ledger(0, assigned_labels=(1, -1))
    assert incompatible.assigned_label_residuals == (
        sp.Rational(1, 2),
        sp.Rational(-1, 2),
    )
    assert incompatible.labels_compatible is False

    compatible = su2_common_charge_ledger(
        0,
        assigned_labels=(sp.Rational(1, 2), sp.Rational(-1, 2)),
    )
    assert compatible.assigned_label_residuals == (0, 0)
    assert compatible.labels_compatible is True


def test_common_charge_shift_cannot_change_the_doublet_gap() -> None:
    for eigenvalue, coefficient in ((0, 1), (3, 2), (-5, sp.Rational(7, 3))):
        assert su2_common_charge_ledger(
            eigenvalue,
            coefficient=coefficient,
        ).eigenvalue_separation == 1


@pytest.mark.parametrize(
    "projector",
    [
        sp.Matrix([[1, 1], [0, 0]]),
        sp.diag(1, sp.Rational(1, 2)),
        sp.Matrix([[1.0, 0], [0, 0]]),
        sp.Matrix([[1, 0, 0], [0, 0, 0]]),
    ],
)
def test_invalid_projector_mutations_are_rejected(projector: sp.Matrix) -> None:
    with pytest.raises(ValueError):
        su2_chiral_factor_ledger(projector)


def test_wrong_parity_exchange_is_rejected() -> None:
    with pytest.raises(ValueError, match="exchange the projectors"):
        su2_chiral_factor_ledger(
            sp.diag(1, 0),
            parity_exchange=sp.eye(2),
        )


def test_same_carrier_dimension_and_charge_exactness_are_enforced() -> None:
    with pytest.raises(ValueError, match="two by two"):
        su2_same_carrier_projector_ledger(sp.eye(3))
    with pytest.raises(ValueError, match="must be exact"):
        su2_common_charge_ledger(0.5)
    with pytest.raises(ValueError, match="upper and lower"):
        su2_common_charge_ledger(0, assigned_labels=(1,))
