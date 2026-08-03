from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.lattice_scalar import (
    PhysicalPhaseChainCoefficients,
    centered_second_difference,
    centered_taylor_laplacian,
    centered_taylor_remainder_bound,
    forward_difference,
    lattice_laplacian_symbol,
    lattice_mode_relative_deficit,
    lattice_spatial_frequency_squared,
    linearized_lattice_dispersion_squared,
    mass_scale_phase_gap_ratio,
    periodic_action_error_bound,
    periodic_lattice_eom_residual,
    periodic_lattice_lagrangian,
    periodic_physical_phase_chain_eom_residual,
    periodic_physical_phase_chain_lagrangian,
    phase_coupling_from_stiffness_scale,
    phase_inertia_from_mass_scale,
    physical_phase_chain_coefficients,
    physical_phase_chain_dimension_matrix,
    physical_phase_chain_dispersion_squared,
    physical_phase_chain_from_displacement,
    physical_phase_chain_gap_ratio,
    physical_phase_chain_scales,
)


def test_finite_differences_keep_spacing_powers_and_orientation() -> None:
    assert forward_difference(2, 5, 3) == 1
    assert centered_second_difference(1, 4, 9, 2) == sp.Rational(1, 2)


def test_centered_taylor_coefficients_are_derived_from_both_neighbours() -> None:
    a = sp.symbols("a", positive=True)
    jet = sp.symbols("d0:7")
    expansion = centered_taylor_laplacian(jet, a)
    assert expansion == jet[2] + a**2 * jet[4] / 12 + a**4 * jet[6] / 360
    assert all(not expansion.has(jet[index]) for index in (0, 1, 3, 5))


def test_centered_taylor_remainder_bound_has_the_next_even_order() -> None:
    a, bound = sp.symbols("a M8", positive=True)
    assert centered_taylor_remainder_bound(a, bound) == bound * a**6 / 20160
    assert (
        centered_taylor_remainder_bound(
            a, bound, retained_derivative_order=4
        )
        == bound * a**4 / 360
    )


def test_exact_laplacian_symbol_matches_shift_eigenvalue() -> None:
    k, a = sp.symbols("k a", real=True, positive=True)
    direct = sp.simplify((sp.exp(sp.I * k * a) - 2 + sp.exp(-sp.I * k * a)) / a**2)
    real_direct = sp.simplify(sp.expand_complex(direct))
    assert sp.trigsimp(real_direct - lattice_laplacian_symbol(k, a)) == 0


def test_symbol_is_even_periodic_and_retains_brillouin_edge() -> None:
    k, a = sp.symbols("k a", real=True, positive=True)
    symbol = lattice_laplacian_symbol(k, a)
    assert sp.simplify(symbol - lattice_laplacian_symbol(-k, a)) == 0
    assert sp.trigsimp(symbol - lattice_laplacian_symbol(k + 2 * sp.pi / a, a)) == 0
    assert lattice_spatial_frequency_squared(sp.pi / a, a) == 4 / a**2


def test_linearized_dispersion_has_exact_long_wave_coefficients() -> None:
    k, a, mass = sp.symbols("k a m", positive=True)
    dispersion = linearized_lattice_dispersion_squared(k, a, mass)
    series = sp.series(dispersion, a, 0, 6).removeO().expand()
    assert series == mass**2 + k**2 - a**2 * k**4 / 12 + a**4 * k**6 / 360
    assert sp.limit(dispersion, a, 0) == mass**2 + k**2


def test_relative_mode_deficit_exposes_long_wave_and_edge_regimes() -> None:
    k, a = sp.symbols("k a", positive=True)
    deficit = lattice_mode_relative_deficit(k, a)
    assert sp.series(deficit, a, 0, 6).removeO().expand() == (
        a**2 * k**2 / 12 - a**4 * k**4 / 360
    )
    edge = lattice_mode_relative_deficit(sp.pi / a, a)
    assert sp.simplify(edge - (1 - 4 / sp.pi**2)) == 0


def test_periodic_lagrangian_has_riemann_weight_and_wraparound_bond() -> None:
    q0, q1, v0, v1, a, mass = sp.symbols("q0 q1 v0 v1 a m", positive=True)
    result = periodic_lattice_lagrangian((q0, q1), (v0, v1), a, mass)
    expected = a * (
        (v0**2 + v1**2) / 2
        - ((q1 - q0) / a) ** 2
        - mass**2 * (2 - sp.cos(q0) - sp.cos(q1))
    )
    assert sp.simplify(result - expected) == 0


def test_sitewise_variation_of_action_gives_canonical_eom_residual() -> None:
    q = sp.symbols("q0:3", real=True)
    velocity = sp.symbols("v0:3", real=True)
    acceleration = sp.symbols("b0:3", real=True)
    a, mass = sp.symbols("a m", positive=True)
    lagrangian = periodic_lattice_lagrangian(q, velocity, a, mass)
    residuals = periodic_lattice_eom_residual(q, acceleration, a, mass)
    for index in range(3):
        euler_lagrange = a * acceleration[index] - sp.diff(lagrangian, q[index])
        assert sp.simplify(euler_lagrange - a * residuals[index]) == 0


def test_constant_sampled_field_has_no_spatial_energy() -> None:
    value, speed, a, mass = sp.symbols("q v a m", positive=True)
    result = periodic_lattice_lagrangian(
        (value, value, value, value),
        (speed, speed, speed, speed),
        a,
        mass,
    )
    expected = 4 * a * (speed**2 / 2 - mass**2 * (1 - sp.cos(value)))
    assert sp.simplify(result - expected) == 0


def test_action_error_bound_is_explicit_and_vanishes_with_spacing() -> None:
    length, duration, a = sp.symbols("L T a", positive=True)
    mx, mxx, mt, mtx, mass = sp.symbols("Mx Mxx Mt Mtx m", positive=True)
    bound = periodic_action_error_bound(
        length, duration, a, mx, mxx, mt, mtx, mass
    )
    expected = duration * length * (
        a * mt * mtx / 2
        + a * mass**2 * mx / 2
        + a * mx * mxx
        + a**2 * mxx**2 / 8
    )
    assert sp.simplify(bound - expected) == 0
    assert sp.limit(bound, a, 0) == 0


def test_physical_phase_chain_variation_keeps_inertia_and_energy_coefficients() -> None:
    q = sp.symbols("q0:3", real=True)
    velocity = sp.symbols("v0:3", real=True)
    acceleration = sp.symbols("b0:3", real=True)
    inertia, coupling, onsite, spacing = sp.symbols(
        "I K V0 a", positive=True
    )
    coefficients = physical_phase_chain_coefficients(
        inertia, coupling, onsite, spacing
    )
    lagrangian = periodic_physical_phase_chain_lagrangian(
        q, velocity, coefficients
    )
    residuals = periodic_physical_phase_chain_eom_residual(
        q, acceleration, coefficients
    )
    for index in range(3):
        euler_lagrange = inertia * acceleration[index] - sp.diff(
            lagrangian, q[index]
        )
        assert sp.simplify(euler_lagrange - residuals[index]) == 0


def test_physical_phase_chain_dispersion_and_scales_are_exact() -> None:
    inertia, coupling, onsite, spacing, k = sp.symbols(
        "I K V0 a k", positive=True
    )
    coefficients = physical_phase_chain_coefficients(
        inertia, coupling, onsite, spacing
    )
    dispersion = physical_phase_chain_dispersion_squared(k, coefficients)
    assert dispersion == (
        onsite + 4 * coupling * sp.sin(k * spacing / 2) ** 2
    ) / inertia
    series = sp.series(dispersion, k, 0, 6).removeO().expand()
    assert series == (
        onsite / inertia
        + coupling * spacing**2 * k**2 / inertia
        - coupling * spacing**4 * k**4 / (12 * inertia)
    )
    scales = physical_phase_chain_scales(coefficients)
    assert scales.gap_frequency == sp.sqrt(onsite / inertia)
    assert scales.band_edge_frequency == sp.sqrt(
        (onsite + 4 * coupling) / inertia
    )
    assert scales.long_wave_speed == spacing * sp.sqrt(coupling / inertia)
    assert physical_phase_chain_dispersion_squared(0, coefficients) == (
        scales.gap_frequency**2
    )
    assert physical_phase_chain_dispersion_squared(
        sp.pi / spacing, coefficients
    ) == scales.band_edge_frequency**2


def test_displacement_lift_exposes_the_missing_coordinate_scale() -> None:
    mass, scale, stiffness, onsite, spacing = sp.symbols(
        "m b kappa V0 a", positive=True
    )
    coefficients = physical_phase_chain_from_displacement(
        mass, scale, stiffness, onsite, spacing
    )
    assert coefficients.inertia == mass * scale**2
    assert coefficients.coupling == stiffness * scale**2
    assert phase_inertia_from_mass_scale(mass, scale) == mass * scale**2
    assert phase_coupling_from_stiffness_scale(stiffness, scale) == (
        stiffness * scale**2
    )
    assert physical_phase_chain_scales(coefficients).gap_frequency == sp.sqrt(
        onsite / (mass * scale**2)
    )
    assert physical_phase_chain_dimension_matrix() == sp.ImmutableMatrix(
        [[1, 1, 1, 0, 1, 0], [2, 2, 2, 1, 0, 1], [0, -2, -2, 0, 0, 0]]
    )


def test_isotope_ratio_requires_curvature_inertia_and_scale_assumptions() -> None:
    mass_h, scale_h, onsite_h = sp.symbols("m_H b_H V_H", positive=True)
    mass_d, scale_d, onsite_d = sp.symbols("m_D b_D V_D", positive=True)
    ratio = mass_scale_phase_gap_ratio(
        mass_h, scale_h, onsite_h, mass_d, scale_d, onsite_d
    )
    expected = sp.sqrt(
        onsite_h * mass_d * scale_d**2
        / (onsite_d * mass_h * scale_h**2)
    )
    assert ratio == expected
    assert sp.simplify(
        ratio.subs(
            {
                onsite_d: onsite_h,
                scale_d: scale_h,
                mass_d: 2 * mass_h,
            }
        )
        - sp.sqrt(2)
    ) == 0
    assert sp.simplify(
        ratio.subs(
            {
                onsite_d: 2 * onsite_h,
                scale_d: scale_h,
                mass_d: 2 * mass_h,
            }
        )
        - 1
    ) == 0


def test_general_coefficient_gap_ratio_matches_direct_scales() -> None:
    first = physical_phase_chain_coefficients(2, 3, 5, 7)
    second = physical_phase_chain_coefficients(11, 13, 17, 19)
    direct = (
        physical_phase_chain_scales(first).gap_frequency
        / physical_phase_chain_scales(second).gap_frequency
    )
    assert sp.simplify(physical_phase_chain_gap_ratio(first, second) - direct) == 0


def test_canonical_lattice_module_uses_no_numpy_quadrature_alias() -> None:
    source = Path("src/substrate_framework/lattice_scalar.py").read_text(encoding="utf-8")
    assert "np." + "trapz" not in source
    assert "np." + "trapezoid" not in source


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: forward_difference(0, 1, 0), "positive"),
        (lambda: centered_taylor_laplacian((1, 2), 1), "even order"),
        (
            lambda: centered_taylor_remainder_bound(
                1, 1, retained_derivative_order=3
            ),
            "even integer",
        ),
        (lambda: lattice_mode_relative_deficit(0, 1), "nonzero"),
        (lambda: periodic_lattice_lagrangian((1,), (1,), 1), "two periodic"),
        (
            lambda: periodic_lattice_lagrangian((1, 2), (1, 2, 3), 1),
            "same number",
        ),
        (
            lambda: periodic_lattice_eom_residual((1, 2), (1, 2, 3), 1),
            "same number",
        ),
        (
            lambda: periodic_action_error_bound(1, 1, 1, -1, 1, 1, 1),
            "nonnegative",
        ),
        (
            lambda: physical_phase_chain_coefficients(1.0, 1, 1, 1),
            "exact",
        ),
        (
            lambda: physical_phase_chain_dispersion_squared(
                sp.I, physical_phase_chain_coefficients(1, 1, 1, 1)
            ),
            "real",
        ),
        (
            lambda: periodic_physical_phase_chain_lagrangian(
                (1, 2),
                (1, 2, 3),
                physical_phase_chain_coefficients(1, 1, 1, 1),
            ),
            "same number",
        ),
        (
            lambda: physical_phase_chain_scales(
                PhysicalPhaseChainCoefficients(1, -1, 1, 1)
            ),
            "coupling",
        ),
    ],
)
def test_lattice_scalar_api_rejects_invalid_inputs(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
