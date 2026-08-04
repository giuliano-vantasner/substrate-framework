from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.boundary_correlations import (
    boundary_sign_correlation_density,
    oriented_half_line_parity_ledger,
    right_half_line_topological_charge_change,
    scalar_boundary_parity_ledger,
    scalar_boundary_trace_family,
    sinusoidal_boundary_sign_correlation,
)
from substrate_framework.sine_gordon import breather_field


def test_scalar_boundary_residual_has_exact_even_odd_decomposition() -> None:
    u, v, a, beta, source = sp.symbols("u v a beta J", real=True)
    ledger = scalar_boundary_parity_ledger(u, v, a, beta, source)
    assert ledger.residual == a * u + beta * v - source
    assert ledger.parity_even_component == a * u - source
    assert ledger.parity_odd_component == beta * v
    assert ledger.residual == (
        ledger.parity_even_component + ledger.parity_odd_component
    )
    assert ledger.parity_image_residual == a * u - beta * v - source
    assert ledger.parity_image_residual == ledger.reflected_coefficient_residual
    assert ledger.fixed_parameter_parity_defect == -2 * beta * v


def test_mixed_boundary_residual_is_not_a_parity_eigenobject() -> None:
    u, v = sp.symbols("u v", real=True)
    mixed = scalar_boundary_parity_ledger(u, v, 1, 1, 0)
    assert sp.simplify(mixed.parity_image_residual - mixed.residual) != 0
    assert sp.simplify(mixed.parity_image_residual + mixed.residual) != 0

    temporal_only = scalar_boundary_parity_ledger(u, v, 1, 0, 0)
    assert temporal_only.parity_image_residual == temporal_only.residual

    spatial_only = scalar_boundary_parity_ledger(u, v, 0, 1, 0)
    assert spatial_only.parity_image_residual == -spatial_only.residual


def test_boundary_coefficient_pair_is_covariant_not_one_fixed_invariant() -> None:
    u, v, source = sp.symbols("u v J", real=True)
    plus = scalar_boundary_parity_ledger(u, v, 1, 1, source)
    minus = scalar_boundary_parity_ledger(u, v, 1, -1, source)
    assert plus.parity_image_residual == minus.residual
    assert plus.parity_image_residual != plus.residual


def test_oriented_half_line_parity_preserves_normal_coefficient() -> None:
    u, v, a, eta, source = sp.symbols("u v a eta J", real=True)
    ledger = oriented_half_line_parity_ledger(u, v, a, eta, source)
    assert ledger.right_outward_trace == -v
    assert ledger.left_parity_coordinate_trace == -v
    assert ledger.left_outward_trace == -v
    assert ledger.right_residual == a * u - eta * v - source
    assert ledger.left_parity_residual == ledger.right_residual


def test_one_boundary_equation_retains_a_trace_family() -> None:
    u, a, beta, source = sp.symbols(
        "u a beta J",
        real=True,
        nonzero=True,
    )
    family = scalar_boundary_trace_family(u, a, beta, source)
    assert family.coordinate_trace_solution == (source - a * u) / beta
    assert family.temporal_only_constraint is None
    assert family.coordinate_trace_free is False
    assert sp.simplify(
        a * u + beta * family.coordinate_trace_solution - source
    ) == 0


def test_temporal_only_boundary_leaves_coordinate_trace_arbitrary() -> None:
    family = scalar_boundary_trace_family(3, 2, 0, 6)
    assert family.coordinate_trace_solution is None
    assert family.temporal_only_constraint == 0
    assert family.coordinate_trace_free is True
    for coordinate_trace in (-7, 0, 11):
        assert 2 * 3 + 0 * coordinate_trace - 6 == 0


def test_boundary_trace_family_requires_declared_coefficient_branch() -> None:
    beta = sp.Symbol("beta", real=True)
    with pytest.raises(ValueError, match="declared zero or nonzero"):
        scalar_boundary_trace_family(1, 1, beta, 0)


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        ((1.0, 1, 1, 1, 0), "temporal_trace"),
        ((1, sp.I, 1, 1, 0), "coordinate_trace"),
        ((1, 1, 1, 1, sp.Rational(1, 2) + sp.I), "source"),
    ],
)
def test_exact_boundary_parity_api_rejects_inexact_or_nonreal_inputs(
    arguments: tuple[object, ...],
    message: str,
) -> None:
    error = TypeError if message == "temporal_trace" else ValueError
    with pytest.raises(error, match=message):
        scalar_boundary_parity_ledger(*arguments)


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
