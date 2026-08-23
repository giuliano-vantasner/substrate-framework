"""Aligned-vacuum fluctuation census tests (P243, advances #163).

Expectations are taken from the independently captured attempt record
``proposals/P243-clock-sourced-induced-coupling/attempts/0001/stdout.txt``
(exact rational census values), not regenerated from the module under test.
"""

from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.m5_covariant_action import (
    MINKOWSKI_MOSTLY_PLUS,
    spectral_trace_potential,
)
from substrate_framework.m5_fluctuation_spectrum import (
    _symmetric_basis,
    aligned_vacuum,
    certify_projector_variation,
    classify_census,
    potential_stiffness_matrix,
)

CERTIFIED_TARGETS = (4, 1, sp.Rational(3, 10), 0)
RECORDED_GAPS = {sp.Integer(67905), sp.Integer(30),
                 sp.Rational(361141, 250000), sp.Integer(1)}
RECORDED_KINETIC = {sp.Rational(1, 9), sp.Rational(100, 1369),
                    sp.Rational(1, 16)}
_ETA = sp.Matrix(MINKOWSKI_MOSTLY_PLUS[:4, :4])
_EPSILON = sp.Symbol("_epsilon", positive=True)


def _potential_second(shifted: sp.Matrix) -> sp.Expr:
    """Independent recomputation of the V quadratic coefficient."""
    weights = (sp.Integer(1),) * len(CERTIFIED_TARGETS)
    series = sp.expand(
        spectral_trace_potential(shifted, CERTIFIED_TARGETS, _ETA,
                                 weights)
    )
    return sp.cancel(series.coeff(_EPSILON, 2))


def test_symmetric_basis_dimension_is_d_times_d_plus_1_over_2() -> None:
    for dimension, expected in ((2, 3), (3, 6), (4, 10)):
        basis = _symmetric_basis(dimension)
        assert len(basis) == expected
        assert all(matrix.is_symmetric for matrix in basis)


def test_aligned_vacuum_is_exact_and_diagonal_in_targets() -> None:
    covariant, mixed = aligned_vacuum(CERTIFIED_TARGETS)
    assert covariant == _ETA * mixed
    assert mixed == sp.diag(*CERTIFIED_TARGETS)


def test_census_reproduces_the_recorded_classification() -> None:
    ledger = classify_census(targets=CERTIFIED_TARGETS)
    assert ledger.basis_dimension == 10
    assert ledger.massless_count == 3
    assert ledger.inert_count == 3
    assert ledger.stiffness_rank == 4
    assert ledger.kinetic_rank == 3
    assert set(ledger.massive_stiff_gaps) == RECORDED_GAPS
    assert set(ledger.kinetic_coefficients) == RECORDED_KINETIC


def test_census_values_are_exact_rationals() -> None:
    ledger = classify_census(targets=CERTIFIED_TARGETS)
    assert all(gap.is_Rational for gap in ledger.massive_stiff_gaps)
    assert all(coef.is_Rational for coef in ledger.kinetic_coefficients)
    assert all(weight.is_Rational for weight in ledger.weights)
    assert ledger.projector_stiffness.is_Rational


def test_projector_variation_certification_passes_every_direction() -> None:
    dims = certify_projector_variation(targets=CERTIFIED_TARGETS)
    assert dims == [0] * 10


def test_kappa_rescale_doubles_the_massless_kinetic_terms() -> None:
    doubled = classify_census(
        targets=CERTIFIED_TARGETS, projector_stiffness=2
    )
    scaled = {sp.cancel(2 * coef) for coef in
              classify_census(targets=CERTIFIED_TARGETS).kinetic_coefficients}
    assert set(doubled.kinetic_coefficients) == scaled
    assert set(doubled.massive_stiff_gaps) == RECORDED_GAPS


def test_weight_mutation_moves_the_stiff_gaps() -> None:
    light = classify_census(targets=CERTIFIED_TARGETS,
                            weights=(1, 1, 1, 2))
    assert light.massless_count == 3
    assert set(light.massive_stiff_gaps) != RECORDED_GAPS
    # The mutated gaps stay exact rationals, not perturbed floats.
    assert all(gap.is_Rational for gap in light.massive_stiff_gaps)


def test_degenerate_timelike_target_is_rejected() -> None:
    """The recorded attempt-0001 mutation: a duplicated timelike target
    breaks the census premise and must be rejected by a named ValueError
    raised out of classification."""
    with pytest.raises(ValueError):
        classify_census(targets=(1, 1, sp.Rational(3, 10), 0))


def test_stiffness_diagonals_equal_direct_second_coefficients() -> None:
    basis, stiffness = potential_stiffness_matrix(
        targets=CERTIFIED_TARGETS
    )
    covariant, _ = aligned_vacuum(CERTIFIED_TARGETS)
    for index, element in enumerate(basis):
        shifted = covariant + _EPSILON * element
        direct = _potential_second(shifted)
        assert sp.simplify(stiffness[index, index] - direct) == 0
