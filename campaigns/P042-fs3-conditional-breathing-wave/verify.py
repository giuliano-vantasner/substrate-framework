#!/usr/bin/env python3
"""Verify P042's conditional breathing-mode theorem and audit FS3."""

from __future__ import annotations

import argparse
import hashlib
import math
import subprocess
import sys
from pathlib import Path

import sympy as sp
from scipy.integrate import quad

from substrate_framework.governance import load_yaml
from substrate_framework.separable_moments import (
    axisymmetric_separable_stf_derivative,
    axisymmetric_stf_tt_readout,
)
from substrate_framework.sine_gordon import (
    breather_energy_second_moment,
    breather_energy_second_moment_derivative,
)
from substrate_framework.tt_angular import (
    conditional_tt_power,
    frobenius_norm_squared,
)
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "572e4e156897bf335784cc606123e9a482fdf13a16434a239e15583050a0ac90"
)


def refined_cycle_mean(function, period: float, subdivisions: int) -> tuple[float, float]:
    """Integrate a smooth periodic square over explicitly split subintervals."""

    total = 0.0
    error = 0.0
    for index in range(subdivisions):
        left = period * index / subdivisions
        right = period * (index + 1) / subdivisions
        value, estimate = quad(
            lambda time: function(time) ** 2,
            left,
            right,
            epsabs=1.0e-11,
            epsrel=1.0e-11,
            limit=200,
        )
        total += value
        error += estimate
    return total / period, error / period


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument(
        "--source-reproduction",
        type=Path,
        help="reuse a hash-matched durable reproduction record",
    )
    args = parser.parse_args()
    ledger = CheckLedger("P042-FS3")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    source_words = " ".join(source_text.split())
    ledger.check(
        "the audited FS3 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    if args.source_reproduction is None:
        reproduction = subprocess.run(
            [sys.executable, str(args.source_file)],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        reproduction_exit = reproduction.returncode
        reproduction_tally = reproduction.stdout
        reproduction_values: dict[str, object] = {}
    else:
        reproduction_record = load_yaml(args.source_reproduction)
        if reproduction_record.get("sha256") != EXPECTED_SOURCE_SHA256:
            raise ValueError("source reproduction record does not match FS3 hash")
        reproduction_exit = reproduction_record.get("exit_code")
        reproduction_tally = str(reproduction_record.get("terminal_tally", ""))
        reproduction_values = dict(reproduction_record.get("reported_values", {}))
    ledger.check("FS3 exits cleanly", reproduction_exit == 0)
    ledger.check(
        "FS3's declared five-check tally reproduces",
        "ALL 5 CHECKS PASS" in reproduction_tally,
    )
    ledger.check(
        "FS3 uses the current trapezoid API with an older-version fallback",
        'np.trapezoid if hasattr(np, "trapezoid") else np.trapz' in source_text,
    )

    time = sp.symbols("t", real=True)
    omega = sp.symbols("omega", positive=True, real=True)
    moment = breather_energy_second_moment(omega, time)
    second = breather_energy_second_moment_derivative(omega, time, 2)
    third = breather_energy_second_moment_derivative(omega, time, 3)
    ledger.check(
        "the canonical API differentiates the accepted exact moment rather than sampled data",
        sp.simplify(second - sp.diff(moment, time, 2)) == 0
        and sp.simplify(third - sp.diff(moment, time, 3)) == 0,
    )
    ledger.check(
        "the third derivative is odd and inherits the exact scalar-moment period",
        sp.simplify(third.subs(time, -time) + third) == 0
        and sp.simplify(
            third.subs(time, time + sp.pi / omega) - third
        )
        == 0,
    )

    special_frequency = sp.sqrt(2) / 2
    special_period = sp.pi / special_frequency
    special_second = breather_energy_second_moment_derivative(
        special_frequency,
        time,
        2,
    )
    special_third = breather_energy_second_moment_derivative(
        special_frequency,
        time,
        3,
    )
    ledger.check(
        "symmetry phases make instantaneous third-derivative power exactly zero",
        special_third.subs(time, 0) == 0
        and sp.simplify(special_third.subs(time, special_period / 2)) == 0,
    )
    ledger.check(
        "a quarter-half-period phase makes the exact third derivative nonzero",
        sp.simplify(
            special_third.subs(time, special_period / 4) + sp.Rational(64, 3)
        )
        == 0,
    )

    derivative, coupling = sp.symbols("d G", positive=True, real=True)
    normalized_third = axisymmetric_separable_stf_derivative(derivative)
    triple_third = axisymmetric_separable_stf_derivative(derivative, 3)
    ledger.check(
        "normalized and triple third-derivative contractions retain the factor nine",
        sp.simplify(
            frobenius_norm_squared(normalized_third) - 2 * derivative**2 / 3
        )
        == 0
        and sp.simplify(
            frobenius_norm_squared(triple_third) - 6 * derivative**2
        )
        == 0,
    )
    flux_prefactor = 1 / (32 * sp.pi * coupling)
    normalized_power = conditional_tt_power(
        normalized_third,
        2 * coupling,
        flux_prefactor,
    )
    triple_power = conditional_tt_power(
        triple_third,
        2 * coupling / 3,
        flux_prefactor,
    )
    wrong_triple_power = conditional_tt_power(
        triple_third,
        2 * coupling,
        flux_prefactor,
    )
    ledger.check(
        "consistent normalized and triple conventions give the same conditional power",
        sp.simplify(normalized_power - 2 * coupling * derivative**2 / 15) == 0
        and sp.simplify(triple_power - normalized_power) == 0,
    )
    ledger.check(
        "using the normalized waveform coefficient with the triple tensor multiplies power by nine",
        sp.simplify(wrong_triple_power - 9 * normalized_power) == 0,
    )
    ledger.check(
        "the exact conditional power is nonnegative but not strictly positive at every time",
        sp.simplify(
            normalized_power.subs(derivative, special_third).subs(time, 0)
        )
        == 0
        and sp.simplify(
            normalized_power.subs(derivative, special_third).subs(
                time,
                special_period / 4,
            )
            - sp.Rational(8192, 135) * coupling
        )
        == 0,
    )

    inclination = sp.symbols("i", real=True)
    readout = axisymmetric_stf_tt_readout(derivative, inclination)
    ledger.check(
        "the arbitrary-inclination normalized plus coordinate has the sine-squared pattern",
        sp.trigsimp(
            readout.normalized_plus_coordinate
            - derivative * sp.sin(inclination) ** 2 / sp.sqrt(2)
        )
        == 0
        and readout.normalized_cross_coordinate == 0,
    )
    ledger.check(
        "the conventional matrix plus readout carries the separate one-half normalization",
        sp.trigsimp(
            readout.conventional_plus_readout
            - derivative * sp.sin(inclination) ** 2 / 2
        )
        == 0
        and readout.conventional_cross_readout == 0,
    )
    ledger.check(
        "the exact viewing limits are an axial null and perpendicular linear plus tensor",
        axisymmetric_stf_tt_readout(derivative, 0).projected_tensor == sp.zeros(3)
        and axisymmetric_stf_tt_readout(
            derivative,
            sp.pi / 2,
        ).projected_tensor
        == sp.diag(derivative / 2, -derivative / 2, 0),
    )
    ledger.check(
        "normalized and triple waveform coefficients give the same perpendicular waveform",
        sp.simplify(2 * coupling * special_second / 2)
        == sp.simplify((2 * coupling / 3) * (3 * special_second) / 2),
    )

    special_third_float = sp.lambdify(time, special_third, "math")
    period_float = math.pi / (1.0 / math.sqrt(2.0))
    cycle_evidence = [
        refined_cycle_mean(special_third_float, period_float, subdivisions)
        for subdivisions in (4, 8, 16, 32)
    ]
    cycle_values = [value for value, _ in cycle_evidence]
    cycle_errors = [error for _, error in cycle_evidence]
    cycle_mean = cycle_values[-1]
    ledger.check(
        "direct exact-expression quadrature is stable under interval refinement",
        max(cycle_values) - min(cycle_values) < 2.0e-11
        and cycle_errors[-1] < 2.0e-10,
    )
    ledger.check(
        "the special-frequency third-derivative mean square is resolution bounded",
        379.4646380687 < cycle_mean < 379.4646380688,
    )

    omega_float = 1.0 / math.sqrt(2.0)

    def dynamic_moment_theta(theta: float) -> float:
        return 16.0 * math.sqrt(2.0) * math.asinh(math.sin(theta)) ** 2

    harmonic_terms: list[float] = []
    coefficient_errors: list[float] = []
    for harmonic in range(1, 17):
        coefficient, coefficient_error = quad(
            lambda theta, k=harmonic: dynamic_moment_theta(theta)
            * math.cos(2 * k * theta),
            0.0,
            math.pi,
            epsabs=1.0e-12,
            epsrel=1.0e-12,
            limit=300,
        )
        coefficient_errors.append(coefficient_error)
        coefficient *= 2.0 / math.pi
        harmonic_terms.append(
            0.5 * (2 * harmonic * omega_float) ** 6 * coefficient**2
        )
    ledger.check(
        "all sixteen Fourier quadratures report finite controlled error",
        all(math.isfinite(value) for value in harmonic_terms)
        and all(math.isfinite(value) for value in coefficient_errors)
        and max(coefficient_errors) < 2.0e-10,
    )
    partial_sums = [sum(harmonic_terms[:count]) for count in (4, 8, 12, 16)]
    partial_errors = [abs(value - cycle_mean) for value in partial_sums]
    ledger.check(
        "independent Fourier-Parseval truncation converges to the time-domain mean",
        partial_errors[1] < partial_errors[0]
        and partial_errors[2] < partial_errors[1]
        and partial_errors[-1] < 2.0e-10,
    )
    first_fraction = harmonic_terms[0] / cycle_mean
    ledger.check(
        "the two-omega harmonic supplies just over eighty percent of derivative power",
        0.8053698716 < first_fraction < 0.8053698718
        and harmonic_terms[0] > sum(harmonic_terms[1:]),
    )
    corrected_average_power = 2.0 * cycle_mean / 15.0
    ledger.check(
        "the corrected unit-coupling conditional average is one ninth of FS3's spectral value",
        50.5952850758 < corrected_average_power < 50.5952850759
        and (
            not reproduction_values
            or abs(
                float(reproduction_values["source_spectral_power"])
                / corrected_average_power
                - 9.0
            )
            < 2.0e-7
        ),
    )

    def power_scale_predicate(candidate: object) -> bool:
        scale = sp.sympify(candidate)
        candidate_power = scale * coupling * derivative**2
        return sp.simplify(candidate_power - normalized_power) == 0

    ledger.mutation_sensitive(
        "conditional normalized power coefficient",
        power_scale_predicate,
        sp.Rational(2, 15),
        [sp.Rational(6, 5), sp.Rational(2, 5), sp.Rational(1, 15)],
    )

    def waveform_scale_predicate(candidate: object) -> bool:
        scale = sp.sympify(candidate)
        normalized_readout = 2 * coupling * derivative / 2
        triple_readout = scale * coupling * (3 * derivative) / 2
        return sp.simplify(triple_readout - normalized_readout) == 0

    ledger.mutation_sensitive(
        "triple-tensor waveform coefficient",
        waveform_scale_predicate,
        sp.Rational(2, 3),
        [2, 1, sp.Rational(1, 3)],
    )

    ledger.check(
        "FS3's purported closed spectral sum is an FFT of the same sampled source moment",
        "mu_spec = np.array([mu_of_t(tt) for tt in ts_spec])" in source_text
        and "Fmu = np.fft.rfft(mu_spec)" in source_text
        and "M_SPEC = 256" in source_text,
    )
    ledger.check(
        "FS3 pairs triple Q with the unrescaled normalized power and waveform coefficients",
        "Q = 3.0 * I.copy()" in source_text
        and "P_num = (Geff / 5.0)" in source_text
        and "(2 G_eff/r) Lambda[Qddot]" in source_words,
    )
    ledger.check(
        "FS3's strict positivity verdict samples around exact zero-power phases",
        "P_positive = np.min(P_num) > 0.0" in source_text
        and "t = np.linspace(0.0, T_total, N)" in source_text
        and "EDGE = 60" in source_text,
    )
    ledger.check(
        "FS3 repeats the factor-two static-kink derivative defect without affecting constancy",
        "uk_x = 4.0 / np.cosh(xk)" in source_text
        and sp.simplify(
            (sp.diff(4 * sp.atan(sp.exp(time)), time) - 2 / sp.cosh(time)).rewrite(
                sp.exp
            )
        )
        == 0,
    )
    ledger.check(
        "FS3 imports rather than derives the retarded waveform and supplies no source or gravity closure",
        "standard linearized GR" in source_text
        and "axisymmetric rigid transverse embedding (FS2)" in source_text
        and "partial_mu T" not in source_text
        and "field equation" not in source_words.lower(),
    )

    count = ledger.finish()
    print(f"P042 FS3 CONDITIONAL BREATHING-WAVE AUDIT ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
