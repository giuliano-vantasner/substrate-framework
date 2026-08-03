from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import sympy as sp

import substrate_framework as sf
from substrate_framework.numerics import SolverTolerances
from substrate_framework.radial_modes import (
    derrick_scaling_evidence,
    option_c_energy_components,
    option_c_euler_lagrange_residual,
    option_c_radial_energy_density,
    solve_option_c_hedgehog,
)
from substrate_framework.rational_map_radial import (
    massless_tail_boundary_residual,
    rational_map_radial_endpoint_exponents,
    rational_map_radial_energy_components,
    rational_map_radial_energy_density,
    rational_map_radial_euler_lagrange_residual,
    rational_map_radial_rhs,
    regular_origin_boundary_residual,
    solve_rational_map_radial_profile,
)
from substrate_framework.rational_maps import axial_rational_map_angular_integral


def test_rational_radial_public_api_is_package_exported() -> None:
    assert sf.solve_rational_map_radial_profile is solve_rational_map_radial_profile
    assert sf.rational_map_radial_energy_density is rational_map_radial_energy_density


def test_generalized_radial_equation_is_derived_from_declared_density() -> None:
    radius = sp.symbols("r", positive=True)
    field_symbol, derivative_symbol = sp.symbols("q p", real=True)
    degree, angular = sp.symbols("B I", positive=True)
    profile = sp.Function("f")(radius)
    density = rational_map_radial_energy_density(
        field_symbol,
        derivative_symbol,
        radius,
        degree,
        angular,
    )
    substitutions = {
        field_symbol: profile,
        derivative_symbol: sp.diff(profile, radius),
    }
    momentum = sp.diff(density, derivative_symbol).subs(substitutions)
    force = sp.diff(density, field_symbol).subs(substitutions)
    direct = sp.simplify((sp.diff(momentum, radius) - force) / 2)
    residual = rational_map_radial_euler_lagrange_residual(
        profile,
        radius,
        degree,
        angular,
    )
    assert sp.simplify(direct - residual) == 0


def test_degree_one_reduces_exactly_to_accepted_option_c_surface() -> None:
    radius = sp.symbols("r", positive=True)
    field, derivative = sp.symbols("f fp", real=True)
    profile = sp.Function("F")(radius)
    generalized_density = rational_map_radial_energy_density(
        field,
        derivative,
        radius,
        1,
        1,
    )
    assert sp.simplify(
        generalized_density
        - option_c_radial_energy_density(field, derivative, radius)
    ) == 0
    assert sp.simplify(
        rational_map_radial_euler_lagrange_residual(profile, radius, 1, 1)
        - option_c_euler_lagrange_residual(profile, radius)
    ) == 0


@pytest.mark.parametrize("degree", [1, 2, 4, 7])
def test_endpoint_powers_satisfy_both_indicial_equations(degree: int) -> None:
    evidence = rational_map_radial_endpoint_exponents(degree)
    sigma = evidence.origin_power
    tail = evidence.tail_power
    assert sp.simplify(sigma * (sigma + 1) - 2 * degree) == 0
    assert sp.simplify(tail * (tail - 1) - 2 * degree) == 0
    assert sp.simplify(tail - sigma - 1) == 0
    if degree == 1:
        assert sigma == 1
        assert tail == 2


def test_asymptotic_boundary_residuals_are_sensitive_to_power_mutations() -> None:
    radius = 0.03
    sigma = 1.7
    amplitude = 0.8
    field = np.pi - amplitude * radius**sigma
    derivative = -amplitude * sigma * radius ** (sigma - 1.0)
    assert regular_origin_boundary_residual(
        radius,
        field,
        derivative,
        sigma,
    ) == pytest.approx(0.0, abs=2.0e-15)
    assert abs(
        regular_origin_boundary_residual(
            radius,
            field,
            derivative,
            sigma + 0.2,
        )
    ) > 1.0e-4

    radius = 20.0
    tail = 2.6
    amplitude = 1.4
    field = amplitude * radius**-tail
    derivative = -tail * amplitude * radius ** (-tail - 1.0)
    assert massless_tail_boundary_residual(
        radius,
        field,
        derivative,
        tail,
    ) == pytest.approx(0.0, abs=2.0e-18)
    assert abs(
        massless_tail_boundary_residual(
            radius,
            field,
            derivative,
            tail + 0.2,
        )
    ) > 1.0e-5


def test_generalized_energy_split_has_declared_scale_identity() -> None:
    e2, e4, scale = sp.symbols("E2 E4 s", positive=True)
    evidence = derrick_scaling_evidence(e2, e4, scale)
    assert evidence.scaled_energy == sp.exp(-scale) * e2 + sp.exp(scale) * e4
    assert evidence.slope_at_origin == e4 - e2
    assert evidence.curvature_at_origin == e2 + e4
    assert evidence.stationary_condition == e4 - e2


def test_generalized_sampled_energy_reuses_option_c_normalization() -> None:
    radius = np.linspace(0.05, 8.0, 501)
    field = 2.0 * np.exp(-radius)
    derivative = -field
    generalized = rational_map_radial_energy_components(
        radius,
        field,
        derivative,
        1,
        1,
    )
    accepted = option_c_energy_components(radius, field, derivative)
    assert generalized == pytest.approx(accepted, rel=2.0e-15)


def test_corrected_stationary_branches_are_finite_ordered_and_virial_balanced() -> None:
    tolerances = SolverTolerances(rtol=3.0e-10, atol=3.0e-12, max_step=0.05)
    inputs = (
        (1, 1.0),
        (2, float(axial_rational_map_angular_integral(2))),
        (4, 20.6496264884189),
    )
    profiles = [
        solve_rational_map_radial_profile(
            degree,
            angular,
            outer_radius=24.0,
            sample_points=1201,
            tolerances=tolerances,
        )
        for degree, angular in inputs
    ]
    for profile in profiles:
        assert np.all(np.isfinite(profile.field))
        assert np.all(np.isfinite(profile.radial_derivative))
        assert abs(profile.inner_boundary_residual) < 2.0e-12
        assert abs(profile.outer_boundary_residual) < 2.0e-7
        assert profile.energy_coefficient > 0.0
        assert profile.virial_relative_imbalance < 3.0e-3
        assert profile.origin_two_derivative_estimate >= 0.0
        assert profile.origin_four_derivative_estimate >= 0.0
        assert profile.tail_two_derivative_estimate >= 0.0
        assert profile.tail_four_derivative_estimate >= 0.0
    per_degree = [profile.per_degree_energy_coefficient for profile in profiles]
    assert per_degree[0] > per_degree[1] > per_degree[2]

    option_c = solve_option_c_hedgehog(
        outer_radius=24.0,
        sample_points=1201,
        tolerances=tolerances,
    )
    assert profiles[0].origin_amplitude == pytest.approx(
        option_c.shooting_slope,
        rel=2.0e-9,
    )
    degree_one_domain_coefficient = (
        profiles[0].domain_two_derivative_energy
        + profiles[0].domain_four_derivative_energy
    ) / (12.0 * np.pi**2)
    assert degree_one_domain_coefficient == pytest.approx(
        option_c.energy_coefficient,
        rel=2.0e-5,
    )
    assert profiles[0].energy_coefficient > degree_one_domain_coefficient


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: rational_map_radial_rhs(1.0, [0.0, 0.0], 0, 1.0),
            "positive integer",
        ),
        (
            lambda: solve_rational_map_radial_profile(
                2,
                5.8,
                amplitude_bracket=(0.1, 0.2),
            ),
            "bracket",
        ),
        (
            lambda: rational_map_radial_energy_components(
                [0.1, 0.2, 0.3, 0.4],
                [1.0, 0.9, 0.8, 0.7],
                [0.0, 0.0, 0.0, 0.0],
                1,
                -1.0,
            ),
            "positive",
        ),
    ],
)
def test_invalid_generalized_radial_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()


def test_canonical_radial_module_has_no_direct_numpy_trapezoid_api() -> None:
    source = Path("src/substrate_framework/rational_map_radial.py").read_text(
        encoding="utf-8"
    )
    assert "np.tr" + "apz" not in source
    assert "np.tr" + "apezoid" not in source
