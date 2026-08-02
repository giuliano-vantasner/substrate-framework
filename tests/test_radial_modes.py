from __future__ import annotations

import numpy as np
import pytest
import sympy as sp

from substrate_framework.radial_modes import (
    apply_option_c_radial_hessian,
    classical_mode_scale_ledger,
    derrick_scale_tangent,
    derrick_scaling_evidence,
    is_below_continuum,
    option_c_continuum_threshold,
    option_c_euler_lagrange_residual,
    option_c_hedgehog_rhs,
    option_c_operator_coefficients,
    option_c_radial_energy_density,
    option_c_second_variation,
    radial_green_boundary_form,
    solve_option_c_hedgehog,
    solve_radial_finite_box_spectrum,
)


def test_option_c_euler_lagrange_residual_is_derived_from_energy() -> None:
    radius = sp.symbols("r", positive=True)
    field_symbol, derivative_symbol = sp.symbols("q p", real=True)
    profile = sp.Function("f")(radius)
    density = option_c_radial_energy_density(
        field_symbol,
        derivative_symbol,
        radius,
    )
    substitutions = {
        field_symbol: profile,
        derivative_symbol: sp.diff(profile, radius),
    }
    momentum = sp.diff(density, derivative_symbol).subs(substitutions)
    force = sp.diff(density, field_symbol).subs(substitutions)
    direct = sp.simplify((sp.diff(momentum, radius) - force) / 2)
    assert sp.simplify(direct - option_c_euler_lagrange_residual(profile, radius)) == 0


def test_second_variation_retains_the_mixed_derivative_correction() -> None:
    radius = sp.symbols("r", positive=True)
    profile = sp.Function("f")(radius)
    evidence = option_c_second_variation(profile, radius)
    expected = -sp.diff(evidence.mixed_coefficient, radius) / 2
    assert sp.simplify(evidence.mixed_boundary_correction - expected) == 0
    assert sp.simplify(
        evidence.potential_coefficient
        - evidence.local_half_hessian
        - evidence.mixed_boundary_correction
    ) == 0
    assert evidence.mixed_boundary_correction != 0

    mode = sp.Function("eta")(radius)
    epsilon = sp.symbols("epsilon", real=True)
    perturbed = profile + epsilon * mode
    density = option_c_radial_energy_density(
        perturbed,
        sp.diff(perturbed, radius),
        radius,
    )
    quadratic = sp.simplify(sp.diff(density, epsilon, 2).subs(epsilon, 0) / 2)
    self_adjoint = sp.simplify(
        evidence.gradient_coefficient * sp.diff(mode, radius) ** 2
        + evidence.potential_coefficient * mode**2
    )
    boundary_derivative = sp.diff(
        evidence.mixed_coefficient * mode**2 / 2,
        radius,
    )
    assert sp.simplify(quadratic - self_adjoint - boundary_derivative) == 0


def test_green_identity_and_hessian_are_self_adjoint_up_to_boundary_form() -> None:
    radius = sp.symbols("r", positive=True)
    profile = sp.Function("f")(radius)
    first = sp.Function("u")(radius)
    second = sp.Function("v")(radius)
    evidence = option_c_second_variation(profile, radius)
    difference = sp.simplify(
        first * apply_option_c_radial_hessian(second, profile, radius)
        - second * apply_option_c_radial_hessian(first, profile, radius)
    )
    boundary = radial_green_boundary_form(
        first,
        second,
        evidence.gradient_coefficient,
        radius,
    )
    assert sp.simplify(difference + sp.diff(boundary, radius)) == 0


def test_derrick_tangent_and_curvature_are_not_automatic_zero_modes() -> None:
    radius, scale = sp.symbols("r s", real=True)
    profile = sp.Function("f")(radius)
    family = profile.subs(radius, sp.exp(scale) * radius)
    assert sp.simplify(
        sp.diff(family, scale).subs(scale, 0)
        - derrick_scale_tangent(profile, radius)
    ) == 0
    e2, e4 = sp.symbols("E2 E4", positive=True)
    evidence = derrick_scaling_evidence(e2, e4, scale)
    assert evidence.slope_at_origin == -e2 + e4
    assert evidence.curvature_at_origin == e2 + e4
    assert evidence.curvature_at_origin.subs(e4, e2) == 2 * e2


def test_massless_continuum_rejects_positive_box_level_as_bound() -> None:
    threshold = option_c_continuum_threshold()
    assert threshold == 0
    assert not is_below_continuum(sp.Rational(1, 10), threshold)
    assert is_below_continuum(-sp.Rational(1, 10), threshold)


def test_generic_fem_reproduces_constant_dirichlet_spectrum() -> None:
    lower, upper = 0.1, 3.1
    radius = np.linspace(lower, upper, 801)
    ones = np.ones_like(radius)
    offset = 0.4
    evidence = solve_radial_finite_box_spectrum(
        radius,
        ones,
        np.full_like(radius, offset),
        ones,
        mode_count=3,
        continuum_threshold=offset,
    )
    exact = np.asarray(
        [offset + (index * np.pi / (upper - lower)) ** 2 for index in (1, 2, 3)]
    )
    assert np.allclose(evidence.eigenvalues, exact, rtol=2.0e-5)
    assert evidence.node_counts == (0, 1, 2)
    assert max(evidence.relative_residuals) < 1.0e-9
    assert not any(evidence.below_continuum)


def test_refined_hedgehog_profile_has_robin_tail_energy_and_virial_balance() -> None:
    profile = solve_option_c_hedgehog(outer_radius=24.0, sample_points=1201)
    assert 1.9 < profile.shooting_slope < 2.2
    assert abs(profile.outer_tail_residual) < 1.0e-7
    assert 1.22 < profile.energy_coefficient < 1.25
    total = profile.two_derivative_energy + profile.four_derivative_energy
    assert abs(profile.two_derivative_energy - profile.four_derivative_energy) / total < 2.0e-3

    fpp = np.asarray(
        [
            option_c_hedgehog_rhs(radius, state)[1]
            for radius, state in zip(
                profile.radius,
                np.column_stack((profile.field, profile.radial_derivative)),
                strict=True,
            )
        ]
    )
    gradient, potential, weight, correction = option_c_operator_coefficients(
        profile.radius,
        profile.field,
        profile.radial_derivative,
        fpp,
    )
    assert np.all(gradient > 0.0)
    assert np.all(weight > 0.0)
    assert np.max(np.abs(correction)) > 1.0
    assert np.all(np.isfinite(potential))


def test_classical_mode_scale_ledger_keeps_quantization_and_scale_free() -> None:
    eigenvalue = sp.Rational(1, 9)
    inverse_time, action, energy_scale, background = sp.symbols(
        "nu S E0 epsilon",
        positive=True,
    )
    ledger = classical_mode_scale_ledger(
        eigenvalue,
        inverse_time,
        action,
        energy_scale,
        background,
    )
    assert ledger.dimensionless_frequency == sp.Rational(1, 3)
    assert ledger.one_quantum_gap == action * inverse_time / 3
    assert ledger.gap_to_background_ratio == (
        action * inverse_time / (3 * energy_scale * background)
    )
    rho = sp.symbols("rho", positive=True)
    assert sp.simplify(
        ledger.gap_to_background_ratio.subs(inverse_time, rho * inverse_time)
        - rho * ledger.gap_to_background_ratio
    ) == 0


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: solve_option_c_hedgehog(slope_bracket=(0.5, 0.6)),
            "bracket",
        ),
        (
            lambda: solve_radial_finite_box_spectrum(
                [0.1, 0.2, 0.3, 0.4],
                [1.0, -1.0, 1.0, 1.0],
                [0.0, 0.0, 0.0, 0.0],
                [1.0, 1.0, 1.0, 1.0],
            ),
            "positive",
        ),
    ],
)
def test_invalid_radial_mode_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
