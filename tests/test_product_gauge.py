from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.product_gauge import (
    product_gauge_connection_component,
    standard_product_gauge_algebra,
)


def test_standard_product_algebra_closes_every_factor_and_cross_bracket() -> None:
    ledger = standard_product_gauge_algebra(sp.Integer(1))

    assert len(ledger.color_commutator_residuals) == 64
    assert len(ledger.isospin_commutator_residuals) == 9
    assert len(ledger.cross_commutator_residuals) == 35
    assert all(residual == sp.zeros(6) for residual in ledger.color_commutator_residuals)
    assert all(residual == sp.zeros(6) for residual in ledger.isospin_commutator_residuals)
    assert all(residual == sp.zeros(6) for residual in ledger.cross_commutator_residuals)


def test_nonzero_weight_gives_twelve_independent_generators() -> None:
    ledger = standard_product_gauge_algebra(sp.Rational(7, 3))

    assert len(ledger.generators) == 12
    assert ledger.flattened_generator_matrix.shape == (36, 12)
    assert ledger.generator_rank == 12
    assert ledger.abelian_generator == sp.Rational(7, 3) * sp.eye(6)


@pytest.mark.parametrize("weight", [0, sp.Symbol("y", real=True), sp.Rational(1, 2) + sp.I, 1.0])
def test_invalid_or_unresolved_abelian_weight_is_rejected(weight: sp.Expr) -> None:
    with pytest.raises(ValueError):
        standard_product_gauge_algebra(weight)


def test_joint_commutant_is_exactly_the_scalar_span() -> None:
    ledger = standard_product_gauge_algebra(sp.Integer(1))

    assert ledger.joint_commutant_basis == (sp.ImmutableMatrix(sp.eye(6)),)
    assert all(
        residual == sp.zeros(6)
        for residual in ledger.factor_commutator_residuals(sp.diag(3, 3, 3, 3, 3, 3))
    )


def test_mixed_tensor_is_not_in_the_joint_commutant() -> None:
    ledger = standard_product_gauge_algebra(sp.Integer(1))
    mixed = sp.kronecker_product(
        ledger.color_generators[0], ledger.isospin_generators[0]
    )

    residuals = ledger.factor_commutator_residuals(mixed)
    assert any(residual != sp.zeros(6) for residual in residuals)


def test_compact_u1_full_turn_is_a_separate_global_gate() -> None:
    integer_weight = standard_product_gauge_algebra(sp.Integer(1))
    half_weight = standard_product_gauge_algebra(sp.Rational(1, 2))

    assert integer_weight.compact_u1_single_valued
    assert integer_weight.compact_u1_full_turn_residual == sp.zeros(6)
    assert not half_weight.compact_u1_single_valued
    assert half_weight.compact_u1_full_turn == -sp.eye(6)
    assert half_weight.generator_rank == integer_weight.generator_rank == 12


def test_connection_component_is_an_exact_three_term_sum() -> None:
    ledger = standard_product_gauge_algebra(sp.Integer(2))
    color = sp.symbols("G0:8", real=True)
    isospin = sp.symbols("W0:3", real=True)
    hypercharge_field = sp.symbols("B", real=True)
    strengths = sp.symbols("g_s g g_Y", positive=True)

    connection = product_gauge_connection_component(
        ledger, color, isospin, hypercharge_field, strengths
    )

    assert sp.simplify(
        connection.total
        - connection.color_term
        - connection.isospin_term
        - connection.abelian_term
    ) == sp.zeros(6)
    assert sp.simplify(connection.abelian_term[0, 0] - 2 * strengths[2] * hypercharge_field) == 0
    assert connection.couplings == strengths


def test_connection_input_shapes_and_exactness_are_enforced() -> None:
    ledger = standard_product_gauge_algebra(sp.Integer(1))

    with pytest.raises(ValueError):
        product_gauge_connection_component(ledger, [0] * 7, [0] * 3, 0, [1, 1, 1])
    with pytest.raises(ValueError):
        product_gauge_connection_component(ledger, [0] * 8, [0] * 2, 0, [1, 1, 1])
    with pytest.raises(ValueError):
        product_gauge_connection_component(ledger, [0] * 8, [0] * 3, 0, [1, 1])
    with pytest.raises(ValueError):
        product_gauge_connection_component(ledger, [0] * 8, [0] * 3, 0.5, [1, 1, 1])
