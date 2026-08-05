from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.gordon_scalar_compatibility import (
    nonzero_boost_scalar_ray_system,
    reciprocal_index_identity,
    rest_boost_scalar_conditions,
    transverse_gordon_scalar_residual,
)


def test_nonzero_symbolic_boost_has_full_rank_exact_ray_system() -> None:
    index = sp.symbols("N", positive=True)
    rapidity_coordinate = sp.symbols("r", real=True, nonzero=True)
    velocity = rapidity_coordinate / sp.sqrt(1 + rapidity_coordinate**2)
    result = nonzero_boost_scalar_ray_system(index, velocity)
    expected_minor = 8 * index**2 * rapidity_coordinate**2 * sp.sqrt(
        1 + rapidity_coordinate**2
    )
    assert sp.simplify(result.first_three_minor - expected_minor) == 0
    assert result.first_three_minor.is_zero is False
    assert result.diagnostics.coefficient_rank == 3
    assert result.diagnostics.unique
    solution = sp.solve(
        result.ray_conditions,
        [result.temporal_square, result.transverse_square, result.potential],
        dict=True,
    )
    assert solution == [
        {
            result.temporal_square: 0,
            result.transverse_square: 0,
            result.potential: 0,
        }
    ]


def test_rest_branch_closes_from_zero_tt_and_xx_components() -> None:
    index = sp.symbols("N", positive=True)
    result = rest_boost_scalar_conditions(index)
    a = result.temporal_square
    b = result.transverse_square
    potential = result.potential
    assert result.tt_zero_condition == index**2 * a + b + 2 * potential
    assert result.xx_zero_condition == index**2 * a + b - 2 * potential
    assert result.square_sum_condition == index**2 * a + b
    assert result.potential_condition == potential
    assert sp.solve(
        [result.square_sum_condition, result.potential_condition],
        [a, potential],
        dict=True,
    ) == [{a: -b / index**2, potential: 0}]
    assert result.square_sum_condition.subs({a: 0, b: 0}) == 0
    assert result.square_sum_condition.subs({a: 1, b: 0}) != 0
    assert result.square_sum_condition.subs({a: 0, b: 1}) != 0


def test_every_component_vanishes_on_reciprocal_affine_vacuum_locus() -> None:
    x = sp.symbols("x", positive=True)
    slope, intercept, coupling = sp.symbols("A B kappa", positive=True)
    index = 1 / (slope * x + intercept)
    result = transverse_gordon_scalar_residual(
        index,
        x,
        sp.Rational(1, 2),
        0,
        0,
        0,
        coupling,
    )
    assert result.geometry.curvature_kernel == 0
    assert result.stress.covariant == sp.zeros(4)
    assert result.residual_covariant == sp.zeros(4)


def test_zero_scalar_cannot_match_nonzero_gordon_curvature() -> None:
    x = sp.symbols("x", real=True)
    coupling = sp.symbols("kappa", positive=True)
    result = transverse_gordon_scalar_residual(
        sp.exp(x),
        x,
        sp.Rational(1, 2),
        0,
        0,
        0,
        coupling,
    )
    assert result.geometry.curvature_kernel == -1
    assert result.stress.covariant == sp.zeros(4)
    assert result.residual_covariant == result.geometry.einstein_covariant
    assert result.residual_covariant != sp.zeros(4)


def test_rest_geometry_requires_zero_kernel_after_scalar_vacuum() -> None:
    x = sp.symbols("x", real=True)
    coupling = sp.symbols("kappa", positive=True)
    result = transverse_gordon_scalar_residual(
        sp.exp(x),
        x,
        0,
        0,
        0,
        0,
        coupling,
    )
    geometry = result.geometry.einstein_covariant
    assert result.geometry.curvature_kernel == -1
    assert geometry[0, 0] == geometry[1, 1] == 0
    assert geometry[2, 2] == geometry[3, 3] == 1
    assert result.stress.covariant == sp.zeros(4)
    assert result.residual_covariant == geometry


def test_omitted_tx_component_is_a_load_bearing_equation() -> None:
    x = sp.symbols("x", real=True)
    temporal, transverse, coupling = sp.symbols("p q kappa", positive=True)
    result = transverse_gordon_scalar_residual(
        sp.exp(x),
        x,
        sp.Rational(1, 2),
        temporal,
        transverse,
        0,
        coupling,
    )
    assert result.geometry.einstein_covariant[0, 1] == 0
    assert result.stress.covariant[0, 1] == temporal * transverse
    assert result.residual_covariant[0, 1] == -coupling * temporal * transverse


def test_wrong_potential_sign_changes_the_source_stress() -> None:
    x = sp.symbols("x", real=True)
    potential, coupling = sp.symbols("V kappa", positive=True)
    result = transverse_gordon_scalar_residual(
        sp.exp(x),
        x,
        sp.Rational(1, 2),
        0,
        0,
        potential,
        coupling,
    )
    metric = result.geometry.metric.covariant
    wrong_sign_stress = metric * potential
    assert (result.stress.covariant + metric * potential).applyfunc(
        sp.simplify
    ) == sp.zeros(4)
    assert (wrong_sign_stress - result.stress.covariant - 2 * metric * potential).applyfunc(
        sp.simplify
    ) == sp.zeros(4)


def test_reciprocal_index_identity_and_non_affine_mutation() -> None:
    x = sp.symbols("x", positive=True)
    index = sp.Function("n", positive=True)(x)
    identity = reciprocal_index_identity(index, x)
    assert identity.identity_residual == 0
    affine = reciprocal_index_identity(1 / (x + sp.Integer(2)), x)
    nonaffine = reciprocal_index_identity(sp.exp(x), x)
    assert affine.curvature_kernel == 0
    assert affine.reciprocal_second_derivative == 0
    assert nonaffine.curvature_kernel == -1
    assert nonaffine.reciprocal_second_derivative == sp.exp(-x)


@pytest.mark.parametrize("velocity", [0, 1, -1, sp.Rational(3, 2), 0.5])
def test_nonzero_ray_system_rejects_invalid_velocity(velocity: object) -> None:
    index = sp.symbols("N", positive=True)
    with pytest.raises(ValueError, match="velocity"):
        nonzero_boost_scalar_ray_system(index, velocity)
