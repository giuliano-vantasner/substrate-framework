from __future__ import annotations

import pytest
import sympy as sp
import substrate_framework as framework

from substrate_framework.dimensional_sine_gordon import (
    DimensionalBreatherObservables,
    DimensionalSineGordonCoefficients,
    DimensionalSineGordonScales,
    dimensional_breather_field,
    dimensional_breather_observables,
    dimensional_sine_gordon_coefficient_dimension_matrix,
    dimensional_sine_gordon_coefficients,
    dimensional_sine_gordon_coefficients_from_speed_gap,
    dimensional_sine_gordon_hamiltonian_density,
    dimensional_sine_gordon_lagrangian_density,
    dimensional_sine_gordon_log_ratio_jacobian,
    dimensional_sine_gordon_normalized_coordinates,
    dimensional_sine_gordon_physical_coordinates,
    dimensional_sine_gordon_residual,
    dimensional_sine_gordon_scales,
    rescale_dimensional_sine_gordon_coefficients,
)


def test_public_package_exports_dimensional_sine_gordon_api() -> None:
    assert framework.DimensionalSineGordonCoefficients is DimensionalSineGordonCoefficients
    assert framework.DimensionalSineGordonScales is DimensionalSineGordonScales
    assert framework.DimensionalBreatherObservables is DimensionalBreatherObservables
    assert framework.dimensional_breather_field is dimensional_breather_field
    assert framework.dimensional_breather_observables is dimensional_breather_observables


def test_coefficient_ratios_and_inverse_family_retain_the_common_scale() -> None:
    coefficients = dimensional_sine_gordon_coefficients(2, 8, 18)
    scales = dimensional_sine_gordon_scales(coefficients)
    assert scales.signal_speed == 2
    assert scales.gap_frequency == 3
    assert scales.length == sp.Rational(2, 3)
    assert scales.energy == 12
    assert scales.action == 4
    assert scales.length == scales.signal_speed / scales.gap_frequency
    assert scales.energy == scales.gap_frequency * scales.action

    inverse = dimensional_sine_gordon_coefficients_from_speed_gap(2, 2, 3)
    assert inverse == coefficients


def test_common_multiplier_preserves_dynamics_but_rescales_energy_and_action() -> None:
    coefficients = dimensional_sine_gordon_coefficients(2, 8, 18)
    scaled = rescale_dimensional_sine_gordon_coefficients(coefficients, 5)
    original_scales = dimensional_sine_gordon_scales(coefficients)
    scaled_scales = dimensional_sine_gordon_scales(scaled)
    assert scaled_scales.signal_speed == original_scales.signal_speed
    assert scaled_scales.gap_frequency == original_scales.gap_frequency
    assert scaled_scales.length == original_scales.length
    assert scaled_scales.energy == 5 * original_scales.energy
    assert scaled_scales.action == 5 * original_scales.action


def test_ratio_jacobian_exposes_one_common_coefficient_direction() -> None:
    jacobian = dimensional_sine_gordon_log_ratio_jacobian()
    assert jacobian.rank() == 2
    assert jacobian * sp.ones(3, 1) == sp.zeros(3, 1)
    assert jacobian.T.nullspace() == [sp.Matrix([-1, 1, 1])]


def test_coefficient_dimension_matrix_matches_energy_density_convention() -> None:
    matrix = dimensional_sine_gordon_coefficient_dimension_matrix()
    assert matrix == sp.Matrix([[1, 1, 1], [-1, 1, -1], [2, 0, 0]])
    assert matrix.det() == -4
    assert matrix.rank() == 3
    assert matrix.nullspace() == []


def test_coordinate_maps_are_exact_inverses() -> None:
    x, t, X, tau = sp.symbols("x t X tau", real=True)
    coefficients = dimensional_sine_gordon_coefficients(2, 8, 18)
    normalized = dimensional_sine_gordon_normalized_coordinates(x, t, coefficients)
    assert normalized == (sp.Rational(3, 2) * x, 3 * t)
    physical = dimensional_sine_gordon_physical_coordinates(*normalized, coefficients)
    assert physical == (x, t)
    inverse_physical = dimensional_sine_gordon_physical_coordinates(X, tau, coefficients)
    assert dimensional_sine_gordon_normalized_coordinates(
        *inverse_physical,
        coefficients,
    ) == (X, tau)


def test_declared_lagrangian_and_hamiltonian_densities_keep_all_coefficients() -> None:
    x, t = sp.symbols("x t", real=True)
    field = sp.Function("u")(x, t)
    coefficients = dimensional_sine_gordon_coefficients(2, 8, 18)
    kinetic = sp.diff(field, t) ** 2
    gradient = sp.diff(field, x) ** 2
    potential = 1 - sp.cos(field)
    assert dimensional_sine_gordon_lagrangian_density(
        field,
        x,
        t,
        coefficients,
    ) == kinetic - 4 * gradient - 18 * potential
    assert dimensional_sine_gordon_hamiltonian_density(
        field,
        x,
        t,
        coefficients,
    ) == kinetic + 4 * gradient + 18 * potential


def test_pulled_back_breather_solves_the_dimensional_equation() -> None:
    x, t = sp.symbols("x t", real=True)
    coefficients = dimensional_sine_gordon_coefficients(2, 8, 18)
    field = dimensional_breather_field(x, t, sp.Rational(1, 2), coefficients)
    assert sp.simplify(
        dimensional_sine_gordon_residual(field, x, t, coefficients)
    ) == 0


def test_dimensional_breather_observables_include_physical_scales() -> None:
    coefficients = dimensional_sine_gordon_coefficients(2, 8, 18)
    observables = dimensional_breather_observables(sp.Rational(1, 2), coefficients)
    assert observables.angular_frequency == sp.Rational(3, 2)
    assert observables.period == 4 * sp.pi / 3
    assert observables.inverse_width == 3 * sp.sqrt(3) / 4
    assert sp.simplify(observables.profile_length - 4 / (3 * sp.sqrt(3))) == 0
    assert observables.energy == 96 * sp.sqrt(3)
    assert observables.action == 64 * sp.pi / 3


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: dimensional_sine_gordon_coefficients(0, 1, 1), "inertia"),
        (lambda: dimensional_sine_gordon_coefficients(1, -1, 1), "gradient"),
        (lambda: dimensional_sine_gordon_coefficients(1, 1, 1.0), "exact"),
        (
            lambda: dimensional_sine_gordon_coefficients_from_speed_gap(1, 0, 1),
            "signal_speed",
        ),
        (
            lambda: dimensional_breather_observables(
                1,
                dimensional_sine_gordon_coefficients(1, 1, 1),
            ),
            "frequency",
        ),
        (
            lambda: rescale_dimensional_sine_gordon_coefficients(
                dimensional_sine_gordon_coefficients(1, 1, 1),
                0,
            ),
            "multiplier",
        ),
        (
            lambda: dimensional_sine_gordon_residual(
                sp.Function("u")(sp.Symbol("x"), sp.Symbol("t")),
                sp.Symbol("x"),
                sp.Symbol("t"),
                DimensionalSineGordonCoefficients(1, -1, 1),
            ),
            "gradient",
        ),
    ],
)
def test_exact_positive_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
