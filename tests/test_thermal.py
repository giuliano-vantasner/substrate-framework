from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.thermal import (
    activated_barrier_log_elasticity,
    conditional_coth_gated_capillary_rate,
    coth_gated_log_stationarity_residual,
    coth_gated_reduced_shape,
    coth_gated_response_shape,
    coth_gated_stationary_coordinate_upper_bound,
    declared_coth_effective_scale,
    inverse_power_input_log_elasticity,
    symmetric_two_level_gate,
    two_level_occupation_variance,
    two_level_upper_occupation,
)


def test_exact_two_level_values() -> None:
    splitting = sp.log(3)
    assert two_level_upper_occupation(splitting) == sp.Rational(1, 4)
    assert two_level_occupation_variance(splitting) == sp.Rational(3, 16)
    assert symmetric_two_level_gate(splitting) == sp.Rational(3, 8)


def test_gate_has_exact_hyperbolic_form() -> None:
    x = sp.symbols("x", real=True)
    assert sp.simplify(
        (
            symmetric_two_level_gate(x)
            - sp.sech(x / 2) ** 2 / 2
        ).rewrite(sp.exp)
    ) == 0


def test_complex_splitting_is_rejected() -> None:
    with pytest.raises(ValueError, match="real and dimensionless"):
        symmetric_two_level_gate(sp.I)


def test_declared_coth_scale_has_exact_limits() -> None:
    quantum, thermal = sp.symbols("q vartheta", positive=True)
    scale = declared_coth_effective_scale(quantum, thermal)
    assert scale == quantum * sp.coth(quantum / (2 * thermal)) / 2
    assert sp.limit(scale, thermal, 0, dir="+") == quantum / 2
    assert sp.limit(scale / thermal, thermal, sp.oo) == 1


def test_capillary_rate_is_exact_source_prefactor_elimination() -> None:
    tension, drive, quantum, thermal, frequency = sp.symbols(
        "tau p q vartheta nu",
        positive=True,
    )
    barrier = sp.pi * tension**2 / drive
    scale = declared_coth_effective_scale(quantum, thermal)
    expected = (
        frequency
        * tension
        / sp.sqrt(drive * scale)
        * sp.exp(-barrier / scale)
        * symmetric_two_level_gate(quantum / thermal)
    )
    actual = conditional_coth_gated_capillary_rate(
        frequency,
        barrier,
        quantum,
        thermal,
    )
    assert sp.simplify(actual - expected) == 0


def test_reduced_shape_and_stationary_residual_are_derived() -> None:
    coordinate, ratio = sp.symbols("u b", positive=True)
    shape = coth_gated_reduced_shape(coordinate, ratio)
    residual = coth_gated_log_stationarity_residual(coordinate, ratio)
    assert shape == sp.sqrt(coordinate) * (1 - coordinate**2) * sp.exp(
        -2 * ratio * coordinate
    )
    assert sp.simplify(sp.diff(sp.log(shape), coordinate) - residual) == 0
    expected_numerator = 1 - 5 * coordinate**2 - 4 * ratio * coordinate * (
        1 - coordinate**2
    )
    assert sp.factor(2 * coordinate * (1 - coordinate**2) * residual) == sp.factor(
        expected_numerator
    )


def test_source_prefactor_has_unique_root_below_one_over_sqrt_five() -> None:
    coordinate, ratio = sp.symbols("u b", positive=True)
    residual = coth_gated_log_stationarity_residual(coordinate, ratio)
    derivative = sp.diff(residual, coordinate)
    assert sp.simplify(
        derivative
        - (
            -sp.Rational(1, 2) / coordinate**2
            - 2 * (1 + coordinate**2) / (1 - coordinate**2) ** 2
        )
    ) == 0
    assert coth_gated_stationary_coordinate_upper_bound() == 1 / sp.sqrt(5)
    assert sp.simplify(residual.subs(coordinate, 1 / sp.sqrt(5)) + 2 * ratio) == 0
    assert sp.limit(residual, coordinate, 0, dir="+") == sp.oo


def test_constant_prefactor_removes_finite_optimum() -> None:
    coordinate, ratio = sp.symbols("u b", positive=True)
    exponent = sp.Integer(0)
    residual = coth_gated_log_stationarity_residual(
        coordinate,
        ratio,
        prefactor_exponent=exponent,
    )
    assert residual == -2 * coordinate / (1 - coordinate**2) - 2 * ratio
    assert sp.limit(
        coth_gated_reduced_shape(
            coordinate,
            ratio,
            prefactor_exponent=exponent,
        ),
        coordinate,
        0,
        dir="+",
    ) == 1


def test_barrier_and_inverse_power_elasticities_change_sign() -> None:
    barrier, scale = sp.symbols("E Theta", positive=True)
    assert activated_barrier_log_elasticity(barrier, scale) == sp.Rational(
        1,
        2,
    ) - barrier / scale
    assert inverse_power_input_log_elasticity(barrier, scale, 2) == (
        2 * barrier / scale - 1
    )
    assert inverse_power_input_log_elasticity(
        barrier,
        scale,
        2,
        prefactor_exponent=0,
    ) == 2 * barrier / scale


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: declared_coth_effective_scale(0, 1), "quantum_energy"),
        (lambda: coth_gated_response_shape(1, 1, 1, prefactor_exponent=-1), "nonnegative"),
        (lambda: coth_gated_reduced_shape(1, 1), "open unit interval"),
        (lambda: conditional_coth_gated_capillary_rate(0, 1, 1, 1), "attempt_frequency"),
    ],
)
def test_coth_rate_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
