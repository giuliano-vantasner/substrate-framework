from __future__ import annotations

import math

import pytest
import sympy as sp

from substrate_framework.exact_sine_qball import (
    evaluate_exact_sine_qball_charge,
    exact_sine_qball_charge_quadrature,
    exact_sine_qball_coordinate_quadrature,
    exact_sine_qball_effective_square,
    exact_sine_qball_first_integral_residual,
    exact_sine_qball_peak_amplitude,
    exact_sine_qball_residual,
    exact_sine_qball_scaled_rhs,
)
from substrate_framework.quartic_qball import (
    quartic_qball_charge,
    quartic_qball_inverse_width,
)


def test_first_integral_differentiates_to_declared_ode() -> None:
    coordinate = sp.symbols("x", real=True)
    frequency = sp.symbols("omega", positive=True)
    profile = sp.Function("f")(coordinate)
    first_integral = exact_sine_qball_first_integral_residual(
        profile, coordinate, frequency
    )
    assert sp.simplify(
        sp.diff(first_integral, coordinate)
        - 2
        * sp.diff(profile, coordinate)
        * exact_sine_qball_residual(profile, coordinate, frequency)
    ) == 0


def test_peak_root_is_first_positive_turning_point() -> None:
    for frequency in (0.1, 0.3, 0.6, 0.7, 0.705):
        peak = exact_sine_qball_peak_amplitude(frequency)
        assert 0.0 < peak < 2.0 * math.pi
        assert abs(
            float(exact_sine_qball_effective_square(peak, frequency))
        ) < 2.0e-13
        for fraction in (0.1, 0.5, 0.9):
            assert float(
                exact_sine_qball_effective_square(
                    fraction * peak, frequency
                )
            ) > 0.0


def test_exact_quadratures_encode_profile_and_accepted_charge() -> None:
    frequency, peak, field = sp.symbols(
        "omega f0 f", positive=True
    )
    coordinate = exact_sine_qball_coordinate_quadrature(
        field, peak, frequency
    )
    charge = exact_sine_qball_charge_quadrature(peak, frequency)
    assert isinstance(coordinate, sp.Integral)
    assert coordinate.limits[0][1:] == (field, peak)
    assert isinstance(charge / (4 * frequency), sp.Integral)


def test_charge_quadrature_is_tolerance_stable() -> None:
    coarse = evaluate_exact_sine_qball_charge(
        sp.Rational(3, 5), epsabs=1.0e-8, epsrel=1.0e-8
    )
    fine = evaluate_exact_sine_qball_charge(
        sp.Rational(3, 5), epsabs=1.0e-11, epsrel=1.0e-11
    )
    assert abs(coarse.charge - fine.charge) < 1.0e-8
    assert fine.absolute_error < 1.0e-9
    assert fine.peak == pytest.approx(coarse.peak, abs=1.0e-13)


def test_small_amplitude_limit_recovers_quartic_family() -> None:
    scaled_profile, inverse_width = sp.symbols("F kappa", positive=True)
    scaled_rhs = exact_sine_qball_scaled_rhs(
        scaled_profile, inverse_width
    )
    assert sp.series(scaled_rhs, inverse_width, 0, 3).removeO() == (
        scaled_profile
        - scaled_profile**3 / 12
        + inverse_width**2 * scaled_profile**5 / 240
    )

    amplitude_ratios = []
    charge_ratios = []
    for frequency in (0.68, 0.70, 0.705):
        kappa = float(quartic_qball_inverse_width(frequency))
        amplitude_ratios.append(
            exact_sine_qball_peak_amplitude(frequency)
            / (math.sqrt(24.0) * kappa)
        )
        charge_ratios.append(
            evaluate_exact_sine_qball_charge(frequency).charge
            / float(quartic_qball_charge(frequency))
        )
    assert all(ratio > 1.0 for ratio in amplitude_ratios)
    assert all(ratio > 1.0 for ratio in charge_ratios)
    assert amplitude_ratios == sorted(amplitude_ratios, reverse=True)
    assert charge_ratios == sorted(charge_ratios, reverse=True)
    assert amplitude_ratios[-1] < 1.002
    assert charge_ratios[-1] < 1.004


@pytest.mark.parametrize(
    "frequency", [0, -sp.Rational(1, 3), sp.sqrt(sp.Rational(1, 2)), 1, sp.I]
)
def test_frequency_domain_is_open_and_real(frequency) -> None:
    with pytest.raises(ValueError, match="omega"):
        exact_sine_qball_effective_square(1, frequency)


def test_numeric_helpers_reject_symbolic_frequency_and_bad_tolerances() -> None:
    frequency = sp.symbols("omega", positive=True)
    with pytest.raises(ValueError, match="numeric"):
        exact_sine_qball_peak_amplitude(frequency)
    with pytest.raises(ValueError, match="tolerances"):
        evaluate_exact_sine_qball_charge(sp.Rational(3, 5), epsabs=0)
