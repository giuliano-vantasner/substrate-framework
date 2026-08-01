from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.boundary_correlations import (
    boundary_sign_correlation_density,
    right_half_line_topological_charge_change,
    sinusoidal_boundary_sign_correlation,
)
from substrate_framework.sine_gordon import breather_field


def test_boundary_sign_correlation_uses_coordinate_derivative() -> None:
    time_derivative, coordinate_derivative = sp.symbols(
        "u v",
        real=True,
    )
    density = boundary_sign_correlation_density(
        time_derivative,
        coordinate_derivative,
    )
    assert density == sp.sign(time_derivative) * coordinate_derivative
    assert sp.simplify(
        boundary_sign_correlation_density(
            time_derivative,
            -coordinate_derivative,
        )
        + density
    ) == 0
    assert sp.simplify(
        boundary_sign_correlation_density(
            -time_derivative,
            -coordinate_derivative,
        )
        - density
    ) == 0


def test_sinusoidal_boundary_sign_correlation_has_explicit_phase_convention() -> None:
    amplitude, frequency, phase = sp.symbols(
        "B omega delta",
        positive=True,
    )
    result = sinusoidal_boundary_sign_correlation(
        3,
        amplitude,
        frequency,
        phase,
    )
    assert result == 4 * amplitude * sp.cos(phase) / frequency
    assert sinusoidal_boundary_sign_correlation(3, amplitude, frequency, 0) == (
        4 * amplitude / frequency
    )
    assert sinusoidal_boundary_sign_correlation(3, amplitude, frequency, sp.pi) == (
        -4 * amplitude / frequency
    )
    assert sinusoidal_boundary_sign_correlation(
        3,
        amplitude,
        frequency,
        sp.pi / 2,
    ) == 0
    assert sinusoidal_boundary_sign_correlation(
        -3,
        amplitude,
        frequency,
        phase,
    ) == -result


def test_winding_change_is_independent_of_nonzero_sign_correlation() -> None:
    frequency = sp.Rational(3, 5)
    rectification = sinusoidal_boundary_sign_correlation(2, 7, frequency, 0)
    period_field_change = sp.integrate(
        2 * sp.sin(frequency * sp.Symbol("t")),
        (sp.Symbol("t"), 0, 2 * sp.pi / frequency),
    )
    assert rectification == sp.Rational(140, 3)
    assert period_field_change == 0
    assert right_half_line_topological_charge_change(period_field_change) == 0


def test_exact_rest_breather_sign_correlation_is_period_antisymmetric() -> None:
    x, t = sp.symbols("x t", real=True)
    omega = sp.Rational(3, 5)
    period = 2 * sp.pi / omega
    field = breather_field(x - sp.Rational(1, 3), t, omega)
    boundary_time = sp.diff(field, t).subs(x, sp.Rational(2, 5))
    boundary_space = sp.diff(field, x).subs(x, sp.Rational(2, 5))
    assert sp.simplify(boundary_time.subs(t, period - t) - boundary_time) == 0
    assert sp.simplify(boundary_space.subs(t, period - t) + boundary_space) == 0


def test_oriented_normal_and_fixed_coordinate_parity_are_distinct() -> None:
    time_derivative, coordinate_derivative = sp.symbols(
        "u v",
        real=True,
    )
    fixed_coordinate = boundary_sign_correlation_density(
        time_derivative,
        coordinate_derivative,
    )
    parity_fixed_coordinate = boundary_sign_correlation_density(
        time_derivative,
        -coordinate_derivative,
    )
    right_outward_normal = -coordinate_derivative
    parity_mapped_left_outward_normal = -coordinate_derivative
    normal_density = boundary_sign_correlation_density(
        time_derivative,
        right_outward_normal,
    )
    parity_normal_density = boundary_sign_correlation_density(
        time_derivative,
        parity_mapped_left_outward_normal,
    )
    assert sp.simplify(parity_fixed_coordinate + fixed_coordinate) == 0
    assert parity_normal_density == normal_density


@pytest.mark.parametrize("angular_frequency", [0, -1, sp.I])
def test_sinusoidal_correlation_rejects_invalid_frequency(
    angular_frequency: sp.Expr,
) -> None:
    with pytest.raises(ValueError, match="angular_frequency"):
        sinusoidal_boundary_sign_correlation(1, 1, angular_frequency, 0)


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        ((sp.I, 1, 1, 0), "time_amplitude"),
        ((1, sp.I, 1, 0), "coordinate_amplitude"),
        ((1, 1, 1, sp.I), "relative_phase"),
    ],
)
def test_sinusoidal_correlation_rejects_nonreal_inputs(
    arguments: tuple[sp.Expr, ...],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        sinusoidal_boundary_sign_correlation(*arguments)
