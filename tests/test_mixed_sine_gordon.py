from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

import substrate_framework as framework
from substrate_framework.mixed_sine_gordon import (
    MixedSineGordonLinearSpectrum,
    MixedSineGordonScaleChoice,
    mixed_coefficient_from_absorption_rate,
    mixed_sine_gordon_dimension_matrix,
    mixed_sine_gordon_dimensionless_coupling,
    mixed_sine_gordon_hyperbolic_coordinates,
    mixed_sine_gordon_linear_spectrum,
    mixed_sine_gordon_linearized_residual,
    mixed_sine_gordon_log_scale_jacobian,
    mixed_sine_gordon_physical_coordinates,
    mixed_sine_gordon_residual,
    mixed_sine_gordon_scale_choice,
    normalized_hyperbolic_sine_gordon_residual,
)


def test_public_package_exports_mixed_coordinate_api() -> None:
    assert framework.MixedSineGordonLinearSpectrum is MixedSineGordonLinearSpectrum
    assert framework.MixedSineGordonScaleChoice is MixedSineGordonScaleChoice
    assert framework.mixed_sine_gordon_residual is mixed_sine_gordon_residual


def test_direct_vacuum_linearization_keeps_the_mixed_derivative() -> None:
    z, tau, epsilon, g = sp.symbols("z tau epsilon g", positive=True)
    psi = sp.Function("psi")(z, tau)
    nonlinear = mixed_sine_gordon_residual(epsilon * psi, z, tau, g)
    direct = sp.diff(nonlinear, epsilon).subs(epsilon, 0)
    assert sp.simplify(
        direct - mixed_sine_gordon_linearized_residual(psi, z, tau, g)
    ) == 0


def test_plane_wave_characteristic_is_k_omega_equals_g() -> None:
    z, tau = sp.symbols("z tau", real=True)
    k, angular, g = sp.symbols("k Omega g", positive=True)
    wave = sp.exp(sp.I * (k * z - angular * tau))
    characteristic = sp.simplify(
        mixed_sine_gordon_linearized_residual(wave, z, tau, g) / wave
    )
    assert characteristic == k * angular - g
    assert sp.simplify(characteristic.subs(angular, g / k)) == 0


def test_mixed_spectrum_has_no_finite_frequency_floor() -> None:
    k, g = sp.symbols("k g", positive=True)
    spectrum = mixed_sine_gordon_linear_spectrum(k, g)
    assert spectrum.angular_frequency == g / k
    assert spectrum.phase_velocity == g / k**2
    assert spectrum.group_velocity == -g / k**2
    assert sp.limit(spectrum.angular_frequency, k, sp.oo) == 0
    assert sp.limit(spectrum.angular_frequency, k, 0, dir="+") == sp.oo


def test_normalizing_scale_family_retains_one_free_aspect_scale() -> None:
    g, length = sp.symbols("g L", positive=True)
    choice = mixed_sine_gordon_scale_choice(g, length)
    assert choice.time_scale == 1 / (g * length)
    assert choice.inverse_length_scale == 1 / length
    assert choice.inverse_time_scale == g * length
    assert mixed_sine_gordon_dimensionless_coupling(
        g, choice.length_scale, choice.time_scale
    ) == 1
    first = mixed_sine_gordon_scale_choice(6, 2)
    second = mixed_sine_gordon_scale_choice(6, 3)
    assert first.inverse_time_scale == 12
    assert second.inverse_time_scale == 18
    jacobian = mixed_sine_gordon_log_scale_jacobian()
    assert jacobian.rank() == 1
    assert jacobian.nullspace() == [sp.Matrix([-1, 1])]


def test_hyperbolic_coordinate_map_is_exactly_invertible() -> None:
    z, tau, length, time = sp.symbols("z tau L T", positive=True)
    space, clock = mixed_sine_gordon_hyperbolic_coordinates(
        z, tau, length, time
    )
    assert mixed_sine_gordon_physical_coordinates(
        space, clock, length, time
    ) == (z, tau)


def test_coordinate_pullback_has_the_derived_sign_and_factor() -> None:
    z, tau, length, time = sp.symbols("z tau L T", positive=True)
    x, clock = sp.symbols("X S", real=True)
    trial = x**2 + 3 * clock**2 + x * clock
    mapped_x, mapped_clock = mixed_sine_gordon_hyperbolic_coordinates(
        z, tau, length, time
    )
    pulled = trial.subs({x: mapped_x, clock: mapped_clock})
    mixed = mixed_sine_gordon_residual(
        pulled, z, tau, 1 / (length * time)
    )
    hyperbolic = normalized_hyperbolic_sine_gordon_residual(
        trial, x, clock
    ).subs({x: mapped_x, clock: mapped_clock})
    assert sp.trigsimp(mixed + hyperbolic / (length * time)) == 0


def test_normalized_kink_cross_check_survives_the_coordinate_map() -> None:
    x, clock = sp.symbols("X S", real=True)
    kink = 4 * sp.atan(sp.exp(x))
    residual = normalized_hyperbolic_sine_gordon_residual(kink, x, clock)
    assert sp.simplify(sp.expand_trig(residual)) == 0


def test_dimension_ledger_separates_absorption_mixed_coefficient_and_gap() -> None:
    assert mixed_sine_gordon_dimension_matrix() == sp.ImmutableMatrix(
        [[-1, -1, 0, 0], [-1, 0, -1, -2]]
    )
    alpha, rate = sp.symbols("alpha gamma", positive=True)
    assert mixed_coefficient_from_absorption_rate(
        alpha, rate, sp.Rational(1, 2)
    ) == alpha * rate / 2


def test_exact_mixed_module_uses_no_numpy_quadrature_alias() -> None:
    source = Path("src/substrate_framework/mixed_sine_gordon.py").read_text(
        encoding="utf-8"
    )
    assert "np." + "trapz" not in source
    assert "np." + "trapezoid" not in source


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: mixed_sine_gordon_scale_choice(1.0, 1), "exact"),
        (lambda: mixed_sine_gordon_scale_choice(1, 0), "positive"),
        (lambda: mixed_sine_gordon_linear_spectrum(-1, 1), "positive"),
        (
            lambda: mixed_coefficient_from_absorption_rate(1, 1, -1),
            "positive",
        ),
    ],
)
def test_mixed_coordinate_api_rejects_invalid_inputs(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
