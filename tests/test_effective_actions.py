from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.effective_actions import (
    eliminate_even_odd_sources,
    eliminate_quadratic_field,
    low_momentum_inverse_expansion,
    quadratic_source_action,
    stationary_reduced_variation,
)


def test_scalar_quadratic_elimination_derives_field_and_effective_term() -> None:
    mass, coupling, current, field = sp.symbols(
        "m g j V", nonzero=True, real=True
    )
    kernel = sp.Matrix([[mass**2]])
    source = sp.Matrix([coupling * current])
    result = eliminate_quadratic_field(kernel, source)
    action = quadratic_source_action(sp.Matrix([field]), kernel, source)
    assert sp.diff(action, field) == mass**2 * field + coupling * current
    assert result.stationary_field == sp.Matrix([-coupling * current / mass**2])
    assert result.stationarity_residual == sp.zeros(1, 1)
    assert result.effective_term == -coupling**2 * current**2 / (2 * mass**2)
    assert sp.simplify(
        action.subs(field, result.stationary_field[0]) - result.effective_term
    ) == 0


def test_matrix_elimination_matches_completion_of_the_square() -> None:
    v1, v2, j1, j2 = sp.symbols("v1 v2 j1 j2", real=True)
    kernel = sp.Matrix([[3, 1], [1, 2]])
    source = sp.Matrix([j1, j2])
    field = sp.Matrix([v1, v2])
    result = eliminate_quadratic_field(kernel, source)
    shifted = field - result.stationary_field
    action = quadratic_source_action(field, kernel, source)
    completed = sp.simplify(
        (shifted.T * kernel * shifted)[0] / 2 + result.effective_term
    )
    assert sp.simplify(action - completed) == 0
    assert result.stationarity_residual == sp.zeros(2, 1)
    assert result.inverse_kernel == sp.Matrix(
        [
            [sp.Rational(2, 5), -sp.Rational(1, 5)],
            [-sp.Rational(1, 5), sp.Rational(3, 5)],
        ]
    )


def test_even_odd_source_split_has_a_sensitive_odd_cross_term() -> None:
    even_amplitude, odd_amplitude = sp.symbols("a b", real=True)
    kernel = sp.Matrix([[2, 1], [1, 3]])
    even = sp.Matrix([even_amplitude, 0])
    odd = sp.Matrix([0, odd_amplitude])
    result = eliminate_even_odd_sources(kernel, even, odd)
    assert result.even_square == -3 * even_amplitude**2 / 10
    assert result.odd_square == -odd_amplitude**2 / 5
    assert result.odd_cross == even_amplitude * odd_amplitude / 5
    assert sp.simplify(
        result.elimination.effective_term
        - (result.even_square + result.odd_square + result.odd_cross)
    ) == 0
    assert sp.simplify(
        result.parity_transformed_effective_term
        - result.elimination.effective_term.subs(odd_amplitude, -odd_amplitude)
    ) == 0
    assert result.odd_cross.subs(odd_amplitude, 0) == 0
    assert result.odd_cross.subs(even_amplitude, 0) == 0


def test_low_momentum_series_retains_exact_truncation_residual() -> None:
    mass, momentum_squared = sp.symbols("m q2", nonzero=True, real=True)
    expansion = low_momentum_inverse_expansion(
        sp.Matrix([[mass**2]]),
        sp.Matrix([[-momentum_squared]]),
        max_order=2,
    )
    expected = sp.Matrix(
        [[mass**-2 + momentum_squared / mass**4 + momentum_squared**2 / mass**6]]
    )
    assert (expansion.approximation - expected).applyfunc(sp.simplify) == sp.zeros(1)
    expected_residual = sp.Matrix([[-momentum_squared**3 / mass**6]])
    assert (expansion.left_residual - expected_residual).applyfunc(
        sp.simplify
    ) == sp.zeros(1)
    assert expansion.right_residual == expansion.left_residual
    assert expansion.left_residual != sp.zeros(1)


def test_noncommuting_inverse_series_is_correct_through_declared_order() -> None:
    scale = sp.symbols("lambda", real=True)
    mass = sp.diag(2, 3)
    derivative_base = sp.Matrix([[1, 2], [2, -1]])
    expansion = low_momentum_inverse_expansion(
        mass,
        scale * derivative_base,
        max_order=2,
    )
    for residual in (expansion.left_residual, expansion.right_residual):
        truncated = residual.applyfunc(
            lambda entry: sp.series(entry, scale, 0, 3).removeO()
        )
        assert truncated == sp.zeros(2)
        assert residual != sp.zeros(2)


def test_stationarity_removes_only_the_induced_variation() -> None:
    anomaly, induced, residual = sp.symbols("A dV R", real=True)
    assert stationary_reduced_variation(anomaly, [0], [induced]) == anomaly
    assert (
        stationary_reduced_variation(anomaly, [residual], [induced])
        == anomaly + induced * residual
    )
    assert stationary_reduced_variation(0, [0], [induced]) == 0


def test_invalid_kernels_sources_and_orders_are_rejected() -> None:
    with pytest.raises(ValueError, match="square"):
        eliminate_quadratic_field(sp.zeros(2, 3), [1, 2])
    with pytest.raises(ValueError, match="symmetric"):
        eliminate_quadratic_field(sp.Matrix([[1, 1], [0, 1]]), [1, 2])
    with pytest.raises(ValueError, match="invertible"):
        eliminate_quadratic_field(sp.ones(2), [1, 2])
    with pytest.raises(ValueError, match="column"):
        eliminate_quadratic_field(sp.eye(2), sp.Matrix([[1, 2]]))
    with pytest.raises(TypeError, match="integer"):
        low_momentum_inverse_expansion(sp.eye(1), sp.zeros(1), 1.5)
    with pytest.raises(ValueError, match="nonnegative"):
        low_momentum_inverse_expansion(sp.eye(1), sp.zeros(1), -1)
    with pytest.raises(ValueError, match="equal-size"):
        stationary_reduced_variation(0, [0, 0], [0])
