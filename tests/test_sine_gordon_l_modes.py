from __future__ import annotations

import numpy as np
import pytest

from substrate_framework.radial_sine_gordon import gaussian_radial_seed
from substrate_framework.sine_gordon_l_modes import (
    evolve_radial_background_with_linearized_mode,
    legendre_p2,
    linearized_p2_energy_triple_stf,
    multiplicative_p2_first_order_residual_coefficient,
    multiplicative_p2_residual,
    regular_l_mode_gaussian_seed,
    transformed_l_mode_acceleration,
)


def test_p2_values_and_multiplicative_residual_derivative() -> None:
    mu = np.array([-1.0, 0.0, 1.0])
    assert np.array_equal(legendre_p2(mu), np.array([1.0, -0.5, 1.0]))
    field = np.array([0.7, 1.1, 1.4])
    radius = np.array([0.8, 1.3, 2.0])
    step = 1.0e-6
    numerical = (
        multiplicative_p2_residual(field, radius, step, mu)
        - multiplicative_p2_residual(field, radius, -step, mu)
    ) / (2.0 * step)
    exact = multiplicative_p2_first_order_residual_coefficient(field, radius, mu)
    assert np.allclose(numerical, exact, rtol=2.0e-10, atol=2.0e-10)
    assert np.max(np.abs(exact)) > 1.0


def test_regular_seed_and_transformed_solid_harmonic_limit() -> None:
    spacing = 0.025
    radius = spacing * np.arange(401)
    seed = regular_l_mode_gaussian_seed(
        radius, ell=2, amplitude=0.4, width=3.0
    )
    assert seed[0] == 0.0
    coefficients = seed[1:4] / np.square(radius[1:4])
    assert np.ptp(coefficients) / np.mean(coefficients) < 2.0e-3

    transformed_solid_harmonic = radius**3
    background = np.full_like(radius, np.pi / 2.0)
    acceleration = transformed_l_mode_acceleration(
        background, transformed_solid_harmonic, spacing, ell=2
    )
    assert np.max(np.abs(acceleration[1:-1])) < 2.0e-9


def test_first_order_energy_moment_has_exact_axisymmetric_stf_structure() -> None:
    radius = np.linspace(0.0, 2.0, 401)
    background = np.full_like(radius, np.pi / 2.0)
    mode = np.square(radius)
    zeros = np.zeros_like(radius)
    tensor = linearized_p2_energy_triple_stf(
        background, zeros, mode, zeros, radius
    )
    scalar = 4.0 * np.pi * 2.0**7 / 7.0
    assert tensor == pytest.approx(
        np.diag([-scalar / 5.0, -scalar / 5.0, 2.0 * scalar / 5.0]),
        rel=3.0e-5,
    )
    assert np.trace(tensor) == pytest.approx(0.0, abs=1.0e-12)


def test_short_regular_l2_evolution_is_finite_and_linear_in_seed() -> None:
    spacing = 0.2
    radius = spacing * np.arange(101)
    background = gaussian_radial_seed(radius, 0.7, 3.0)
    mode = regular_l_mode_gaussian_seed(
        radius, ell=2, amplitude=0.1, width=3.0
    )
    baseline = evolve_radial_background_with_linearized_mode(
        background,
        mode,
        spacing=spacing,
        final_time=2.0,
        ell=2,
        sample_interval=0.2,
    )
    half = evolve_radial_background_with_linearized_mode(
        background,
        0.5 * mode,
        spacing=spacing,
        final_time=2.0,
        ell=2,
        sample_interval=0.2,
    )
    assert baseline.completed
    assert baseline.method == "velocity-verlet-transformed-mode"
    assert np.all(np.isfinite(baseline.p2_triple_stf_zz_coefficient))
    assert np.max(np.abs(baseline.final_mode)) > 0.0
    assert half.final_mode == pytest.approx(0.5 * baseline.final_mode)
    assert half.p2_triple_stf_zz_coefficient == pytest.approx(
        0.5 * baseline.p2_triple_stf_zz_coefficient
    )


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: legendre_p2([1.1]), r"\[-1, 1\]"),
        (
            lambda: multiplicative_p2_residual([1.0], [0.0], 0.1, [0.2]),
            "strictly above zero",
        ),
        (
            lambda: regular_l_mode_gaussian_seed(
                [0.0, 1.0, 2.0], ell=0, amplitude=1.0, width=1.0
            ),
            "positive integer",
        ),
        (
            lambda: evolve_radial_background_with_linearized_mode(
                np.zeros(11),
                np.ones(11),
                spacing=0.1,
                final_time=1.0,
                ell=2,
            ),
            "vanish at the origin",
        ),
    ],
)
def test_invalid_l_mode_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
