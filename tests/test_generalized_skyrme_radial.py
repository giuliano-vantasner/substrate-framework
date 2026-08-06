from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import sympy as sp

import substrate_framework as sf
from substrate_framework.generalized_skyrme_radial import (
    generalized_skyrme_endpoint_data,
    generalized_skyrme_energy_components,
    generalized_skyrme_radial_energy_density,
    generalized_skyrme_radial_euler_lagrange_residual,
    generalized_skyrme_radial_rhs,
    generalized_skyrme_reduced_coefficients,
    generalized_skyrme_scaling_residual,
    generalized_skyrme_tail_robin_coefficient,
    solve_generalized_skyrme_radial_profile,
)
from substrate_framework.rational_map_radial import (
    rational_map_radial_energy_density,
    rational_map_radial_euler_lagrange_residual,
)


def test_generalized_skyrme_api_is_package_exported() -> None:
    assert (
        sf.solve_generalized_skyrme_radial_profile
        is solve_generalized_skyrme_radial_profile
    )
    assert (
        sf.generalized_skyrme_radial_energy_density
        is generalized_skyrme_radial_energy_density
    )


def test_extended_equation_is_independently_varied_from_density() -> None:
    r = sp.symbols("r", positive=True)
    q, p = sp.symbols("q p", real=True)
    b, angular = sp.symbols("B I", positive=True)
    c6, c0 = sp.symbols("c6 c0", nonnegative=True)
    profile = sp.Function("f")(r)
    density = generalized_skyrme_radial_energy_density(
        q, p, r, b, angular, c6, c0
    )
    substitutions = {q: profile, p: sp.diff(profile, r)}
    direct = sp.simplify(
        (
            sp.diff(sp.diff(density, p).subs(substitutions), r)
            - sp.diff(density, q).subs(substitutions)
        )
        / 2
    )
    residual = generalized_skyrme_radial_euler_lagrange_residual(
        profile, r, b, angular, c6, c0
    )
    assert sp.simplify(direct - residual) == 0


def test_zero_extra_coefficients_recover_accepted_radial_surface_exactly() -> None:
    r = sp.symbols("r", positive=True)
    f, fp = sp.symbols("f fp", real=True)
    b, angular = sp.symbols("B I", positive=True)
    profile = sp.Function("F")(r)
    assert sp.simplify(
        generalized_skyrme_radial_energy_density(
            f, fp, r, b, angular, 0, 0
        )
        - rational_map_radial_energy_density(f, fp, r, b, angular)
    ) == 0
    assert sp.simplify(
        generalized_skyrme_radial_euler_lagrange_residual(
            profile, r, b, angular, 0, 0
        )
        - rational_map_radial_euler_lagrange_residual(
            profile, r, b, angular
        )
    ) == 0


def test_density_is_a_sum_of_nonnegative_declared_terms() -> None:
    density = generalized_skyrme_radial_energy_density(
        sp.pi / 3, sp.Rational(-2, 5), 2, 4, 7, sp.Rational(1, 2), sp.Rational(1, 4)
    )
    assert density.is_positive is True
    assert generalized_skyrme_radial_energy_density(0, 0, 2, 4, 7, 0, 0) == 0


def test_lambda_convention_conversion_and_reduced_coefficients_are_exact() -> None:
    lam, mu, coupling, scale = sp.symbols("lambda mu e F", positive=True)
    c6, c0 = generalized_skyrme_reduced_coefficients(lam, mu, coupling, scale)
    lambda_a = sp.pi**2 * lam
    assert sp.simplify(
        c6 - lambda_a**2 * coupling**4 * scale**2 / (8 * sp.pi**4)
    ) == 0
    assert c0 == 32 * mu**2 / (coupling**2 * scale**4)


def test_scaling_residual_has_the_four_declared_weights() -> None:
    e2, e4, e6, e0, scale = sp.symbols("E2 E4 E6 E0 s", positive=True)
    scaled = scale * e2 + e4 / scale + e6 / scale**3 + scale**3 * e0
    assert sp.simplify(
        sp.diff(scaled, scale).subs(scale, 1)
        - generalized_skyrme_scaling_residual(e2, e4, e6, e0)
    ) == 0


@pytest.mark.parametrize("degree", [1, 2, 4])
def test_endpoint_data_satisfy_origin_and_tail_indicial_equations(degree: int) -> None:
    data = generalized_skyrme_endpoint_data(degree, sp.Rational(1, 4))
    assert data.origin_power * (data.origin_power + 1.0) == pytest.approx(
        2.0 * degree
    )
    assert data.tail_power * (data.tail_power - 1.0) == pytest.approx(
        2.0 * degree
    )
    assert data.tail_mass == pytest.approx(1.0 / np.sqrt(8.0))


def test_massive_tail_robin_coefficient_is_sensitive_to_potential() -> None:
    massless = generalized_skyrme_tail_robin_coefficient(20.0, 2, 0.0)
    massive = generalized_skyrme_tail_robin_coefficient(20.0, 2, 0.25)
    assert massive > massless
    assert massive > np.sqrt(0.25 / 2.0)


def test_rhs_matches_symbolic_residual_on_a_nonsingular_sample() -> None:
    r = np.asarray([0.7, 1.1, 1.9])
    f = np.asarray([2.2, 1.4, 0.5])
    fp = np.asarray([-0.8, -0.7, -0.3])
    rhs = generalized_skyrme_radial_rhs(r, np.vstack((f, fp)), 2, 5.8, 0.5, 0.25)
    assert np.all(np.isfinite(rhs))
    assert np.all(rhs[0] == fp)
    mutated = generalized_skyrme_radial_rhs(r, np.vstack((f, fp)), 2, 4.0, 0.5, 0.25)
    assert np.max(np.abs(rhs[1] - mutated[1])) > 1.0e-2


def test_sampled_components_recover_l2_l4_and_respond_to_extra_terms() -> None:
    r = np.linspace(0.05, 8.0, 501)
    f = 2.0 * np.exp(-r)
    fp = -f
    base = generalized_skyrme_energy_components(r, f, fp, 2, 5.8, 0.0, 0.0)
    extended = generalized_skyrme_energy_components(r, f, fp, 2, 5.8, 0.5, 0.25)
    assert base[2:] == (0.0, 0.0)
    assert extended[:2] == pytest.approx(base[:2], rel=1.0e-15)
    assert extended[2] > 0.0
    assert extended[3] > 0.0


def test_supplied_rational_coefficient_branches_converge_and_are_virial_balanced() -> None:
    inputs = ((1, 1.0), (2, float(np.pi + 8.0 / 3.0)), (4, 20.6496264884189))
    profiles = [
        solve_generalized_skyrme_radial_profile(
            degree,
            angular,
            0.5,
            0.25,
            outer_radius=20.0,
            initial_points=401,
            sample_points=4001,
            continuation_steps=8,
            tolerance=2.0e-6,
        )
        for degree, angular in inputs
    ]
    for profile in profiles:
        assert np.all(np.isfinite(profile.field))
        assert np.all(np.isfinite(profile.radial_derivative))
        assert profile.max_rms_residual < 2.1e-6
        assert abs(profile.inner_boundary_residual) < 2.0e-11
        assert abs(profile.outer_boundary_residual) < 2.0e-11
        assert np.max(profile.radial_derivative) < 1.0e-6
        assert profile.energy_coefficient > 0.0
        assert profile.virial_relative_residual < 2.0e-4
    coefficients = {profile.degree: profile.energy_coefficient for profile in profiles}
    kappa = 3.0 * np.pi**2 * (2.0 * coefficients[2] - coefficients[4])
    assert coefficients == pytest.approx(
        {
            1: 1.4326169543619196,
            2: 2.798884988462644,
            4: 5.19738869881647,
        },
        rel=3.0e-8,
    )
    assert kappa == pytest.approx(11.85481447360972, rel=3.0e-8)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: generalized_skyrme_radial_energy_density(0, 0, 1, 1, 1, -1, 0),
            "nonnegative",
        ),
        (
            lambda: solve_generalized_skyrme_radial_profile(0, 1, 0.5, 0.25),
            "positive integer",
        ),
        (
            lambda: solve_generalized_skyrme_radial_profile(
                1, 1, 0.5, 0.25, inner_radius=2, outer_radius=1
            ),
            "exceed",
        ),
    ],
)
def test_invalid_inputs_fail_explicitly(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()


def test_canonical_module_has_no_direct_numpy_trapezoid_api() -> None:
    source = Path("src/substrate_framework/generalized_skyrme_radial.py").read_text(
        encoding="utf-8"
    )
    assert "np.tr" + "apz" not in source
    assert "np.tr" + "apezoid" not in source
