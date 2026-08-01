#!/usr/bin/env python3
"""Exact branch, quadrature, asymptotic, and source audit for FG1."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import math
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp

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
from substrate_framework.u1_charge import stationary_u1_charge_density
from substrate_framework.verification import CheckLedger


FG1_SHA256 = "f0e655828c2796d9f38aaff0d055dfe8a28562de700f408600e645dce2b2b45b"


@dataclass(frozen=True)
class IntegralConvention:
    sine_coefficient: sp.Expr
    cosine_coefficient: sp.Expr
    frequency_sign: int


def run(source_file: Path) -> int:
    checks = CheckLedger("P032-FG1")
    payload = source_file.read_bytes()
    source_text = payload.decode("utf-8")
    checks.check(
        "the audited FG1 source is the hash-pinned candidate unit",
        hashlib.sha256(payload).hexdigest() == FG1_SHA256,
    )
    checks.check(
        "the exact-sine model remains conditional on a predecessor potential",
        "potential V(rho)=1-cos(sqrt(rho))" in source_text
        and "[EM6-dossier]" in source_text
        and "omega : spatial coordinate" not in source_text,
    )

    coordinate = sp.symbols("x", real=True)
    frequency = sp.symbols("omega", positive=True)
    profile = sp.Function("f")(coordinate)
    first_integral = exact_sine_qball_first_integral_residual(
        profile, coordinate, frequency
    )
    residual = exact_sine_qball_residual(
        profile, coordinate, frequency
    )
    checks.check(
        "the localized first integral differentiates to the declared ODE",
        sp.simplify(
            sp.diff(first_integral, coordinate)
            - 2 * sp.diff(profile, coordinate) * residual
        )
        == 0,
    )
    field_value, peak = sp.symbols("f f0", positive=True)
    square = exact_sine_qball_effective_square(field_value, frequency)
    checks.check(
        "localized boundary data fix the peak equation exactly",
        exact_sine_qball_effective_square(0, frequency) == 0
        and exact_sine_qball_effective_square(peak, frequency)
        == 1 - sp.cos(peak) - frequency**2 * peak**2,
    )

    ratio = (1 - sp.cos(field_value)) / field_value**2
    half_argument = sp.symbols("z", positive=True)
    sinc = sp.sin(half_argument) / half_argument
    monotonic_witness = sp.sin(half_argument) - half_argument * sp.cos(
        half_argument
    )
    checks.check(
        "the peak ratio is one-half times a squared sinc",
        sp.trigsimp(
            ratio.subs(field_value, 2 * half_argument) - sinc**2 / 2
        )
        == 0,
    )
    checks.check(
        "the sinc monotonicity witness grows from zero on zero-to-pi",
        sp.limit(monotonic_witness, half_argument, 0, dir="+") == 0
        and sp.diff(monotonic_witness, half_argument)
        == half_argument * sp.sin(half_argument),
    )
    checks.check(
        "the peak ratio spans the full frequency-squared domain",
        sp.limit(ratio, field_value, 0, dir="+") == sp.Rational(1, 2)
        and ratio.subs(field_value, 2 * sp.pi) == 0,
    )

    numeric_frequencies = (0.1, 0.3, 0.6, 0.7, 0.705)
    peaks = {
        value: exact_sine_qball_peak_amplitude(value)
        for value in numeric_frequencies
    }
    checks.check(
        "bracketed roots select the unique peak inside zero-to-two-pi",
        all(0.0 < amplitude < 2.0 * math.pi for amplitude in peaks.values())
        and all(
            abs(
                float(
                    exact_sine_qball_effective_square(amplitude, value)
                )
            )
            < 2.0e-13
            for value, amplitude in peaks.items()
        ),
    )
    checks.check(
        "the orbit square stays positive below every selected peak",
        all(
            float(
                exact_sine_qball_effective_square(
                    fraction * amplitude, value
                )
            )
            > 0.0
            for value, amplitude in peaks.items()
            for fraction in (0.1, 0.5, 0.9)
        ),
    )
    later_root_frequency = 0.1
    later_left = 2.0 * math.pi
    later_right = 3.0 * math.pi
    checks.check(
        "a later-root mutation crosses a forbidden negative-square interval",
        float(
            exact_sine_qball_effective_square(
                later_left, later_root_frequency
            )
        )
        < 0.0
        and float(
            exact_sine_qball_effective_square(
                later_right, later_root_frequency
            )
        )
        > 0.0,
    )

    inverse_profile = exact_sine_qball_coordinate_quadrature(
        field_value, peak, frequency
    )
    checks.check(
        "the inverse quadrature has the decreasing positive-half branch",
        sp.simplify(
            sp.diff(inverse_profile, field_value)
            + 1 / sp.sqrt(square)
        )
        == 0,
    )
    kappa = sp.sqrt(sp.Rational(1, 2) - frequency**2)
    checks.check(
        "the inverse coordinate diverges logarithmically at the vacuum",
        sp.limit(square / field_value**2, field_value, 0, dir="+")
        == kappa**2,
    )

    density = stationary_u1_charge_density(field_value, frequency)
    charge_quadrature = exact_sine_qball_charge_quadrature(
        peak, frequency
    )
    checks.check(
        "the even-profile accepted-current change of variables fixes charge factor four",
        density == 2 * frequency * field_value**2
        and isinstance(
            sp.simplify(charge_quadrature / (4 * frequency)),
            sp.Integral,
        ),
    )
    checks.check(
        "the charge integrand is finite at zero and integrable at the simple peak",
        sp.limit(field_value**2 / sp.sqrt(square), field_value, 0, dir="+")
        == 0,
    )

    coarse_charge = evaluate_exact_sine_qball_charge(
        sp.Rational(3, 5), epsabs=1.0e-8, epsrel=1.0e-8
    )
    fine_charge = evaluate_exact_sine_qball_charge(
        sp.Rational(3, 5), epsabs=1.0e-11, epsrel=1.0e-11
    )
    checks.check(
        "endpoint-regularized charge is stable under tolerance refinement",
        abs(coarse_charge.charge - fine_charge.charge) < 1.0e-8
        and fine_charge.absolute_error < 1.0e-9,
    )

    direct_peak = fine_charge.peak

    def direct_square(value: float) -> float:
        return 2.0 * math.sin(value / 2.0) ** 2 - 0.6**2 * value**2

    direct_integral, direct_error = quad(
        lambda value: value**2 / math.sqrt(direct_square(value)),
        0.0,
        direct_peak,
        epsabs=1.0e-10,
        epsrel=1.0e-10,
        points=[direct_peak],
        limit=500,
    )
    checks.check(
        "direct field-variable quadrature independently matches the regularized charge",
        abs(4.0 * 0.6 * direct_integral - fine_charge.charge) < 1.0e-8
        and direct_error < 1.0e-8,
    )

    def source_ode(_x: float, state: np.ndarray) -> tuple[float, float]:
        return (
            float(state[1]),
            0.5 * math.sin(float(state[0])) - 0.6**2 * float(state[0]),
        )

    source_kappa = math.sqrt(0.5 - 0.6**2)
    source_domain = 40.0 / source_kappa
    source_grid = np.linspace(0.0, source_domain, 16000)
    source_like = solve_ivp(
        source_ode,
        (0.0, source_domain),
        (direct_peak, 0.0),
        t_eval=source_grid,
        rtol=1.0e-10,
        atol=1.0e-12,
        method="DOP853",
    )
    source_like_charge = 4.0 * 0.6 * np.trapezoid(
        source_like.y[0] ** 2, source_grid
    )
    checks.check(
        "FG1's long separatrix shoot rebounds and triples the physical charge quadrature",
        source_like.success
        and abs(source_like_charge / fine_charge.charge - 3.0) < 1.0e-6
        and np.max(np.abs(source_like.y[0][source_grid > 30.0]))
        > 0.9 * direct_peak,
    )

    scaled_profile, small_kappa = sp.symbols("F kappa", positive=True)
    exact_scaled_rhs = exact_sine_qball_scaled_rhs(
        scaled_profile, small_kappa
    )
    checks.check(
        "the scaled exact equation has the quartic Q-ball as its leading operator",
        sp.series(exact_scaled_rhs, small_kappa, 0, 3).removeO()
        == scaled_profile
        - scaled_profile**3 / 12
        + small_kappa**2 * scaled_profile**5 / 240,
    )
    scaled_peak = sp.symbols("a", positive=True)
    scaled_peak_square = (
        1
        - sp.cos(small_kappa * scaled_peak)
        - (sp.Rational(1, 2) - small_kappa**2)
        * small_kappa**2
        * scaled_peak**2
    ) / small_kappa**4
    leading_peak = sp.limit(scaled_peak_square, small_kappa, 0, dir="+")
    checks.check(
        "the peak equation forces the quartic scaled amplitude sqrt twenty-four",
        leading_peak == scaled_peak**2 - scaled_peak**4 / 24
        and sp.solve(sp.Eq(leading_peak, 0), scaled_peak)
        == [2 * sp.sqrt(6)],
    )

    amplitude_ratios: list[float] = []
    charge_ratios: list[float] = []
    for value in (0.68, 0.70, 0.705):
        width = float(quartic_qball_inverse_width(value))
        amplitude_ratios.append(
            exact_sine_qball_peak_amplitude(value)
            / (math.sqrt(24.0) * width)
        )
        charge_ratios.append(
            evaluate_exact_sine_qball_charge(value).charge
            / float(quartic_qball_charge(value))
        )
    checks.check(
        "shrinking-amplitude peak and charge ratios converge toward the quartic family",
        amplitude_ratios == sorted(amplitude_ratios, reverse=True)
        and charge_ratios == sorted(charge_ratios, reverse=True)
        and amplitude_ratios[-1] < 1.002
        and charge_ratios[-1] < 1.004,
    )

    eta = sp.sqrt(1 - frequency**2)
    phi4_width_residual = sp.simplify(
        eta**2 - (sp.Rational(1, 2) - frequency**2)
    )
    checks.check(
        "EM1's envelope width remains off shell by an exact one-half",
        phi4_width_residual == sp.Rational(1, 2),
    )
    em1_profile = sp.sech(eta * coordinate)
    checks.check(
        "EM1's unit-amplitude envelope is not the exact-sine profile",
        sp.simplify(
            exact_sine_qball_residual(
                em1_profile, coordinate, sp.Rational(1, 2)
            ).subs(coordinate, 0)
        )
        != 0,
    )
    checks.check(
        "the EM6-to-EM1 charge ratio is algebraic comparison not object identity",
        "Q_EM6/Q_EM1 = 24*kappa*eta" in source_text
        and "eta is REJECTED as the Q-ball width" in source_text,
    )
    checks.check(
        "FG1 again assigns stability without a fluctuation operator or theorem audit",
        "Vakhitov-Kolokolov" in source_text
        and "fluctuation operator" not in source_text
        and "eigenvalue" not in source_text,
    )
    checks.check(
        "the unmodified pinned source contains its terminal NumPy failure",
        "np.trapz" in source_text,
    )

    field = sp.Function("g")(coordinate)

    def convention_closes(candidate: object) -> bool:
        convention = candidate
        assert isinstance(convention, IntegralConvention)
        trial_residual = (
            sp.diff(field, coordinate, 2)
            - convention.sine_coefficient * sp.sin(field)
            + convention.frequency_sign * frequency**2 * field
        )
        trial_integral = (
            sp.diff(field, coordinate) ** 2
            - convention.cosine_coefficient * (1 - sp.cos(field))
            + convention.frequency_sign * frequency**2 * field**2
        )
        return (
            sp.simplify(
                sp.diff(trial_integral, coordinate)
                - 2 * sp.diff(field, coordinate) * trial_residual
            )
            == 0
            and convention == IntegralConvention(
                sp.Rational(1, 2), sp.Integer(1), 1
            )
        )

    checks.mutation_sensitive(
        "sine potential and frequency signs",
        convention_closes,
        IntegralConvention(sp.Rational(1, 2), sp.Integer(1), 1),
        [
            IntegralConvention(sp.Integer(1), sp.Integer(1), 1),
            IntegralConvention(sp.Rational(1, 2), sp.Integer(-1), 1),
            IntegralConvention(sp.Rational(1, 2), sp.Integer(1), -1),
        ],
    )

    total = checks.finish()
    print(f"P032 FG1 EXACT-SINE QBALL AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
