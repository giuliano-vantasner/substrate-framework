#!/usr/bin/env python3
"""Verify P045's spherical STF theorem and audit P3D2."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.conserved_moments import (
    axisymmetric_p2_density_second_moments,
    spherical_density_second_moments,
    symmetric_trace_free,
)
from substrate_framework.governance import load_yaml
from substrate_framework.numerics import NumericalFailure
from substrate_framework.radial_sine_gordon import (
    RadialEvolution,
    estimate_angular_frequency,
    estimate_peak_angular_frequency,
    evolve_radial_sine_gordon_leapfrog,
)
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "72802a3bb3ed46be3bf7b96e035028b0ded352ae02e587cb14b9db902b2125cb"
)


def window_relative_half_range(
    result: RadialEvolution,
    values: np.ndarray,
    start: float,
) -> float:
    selected = result.time >= start
    return float(np.ptp(values[selected]) / (2.0 * np.mean(values[selected])))


def core_retention(result: RadialEvolution) -> float:
    early = (result.time >= 120.0) & (result.time <= 180.0)
    late = (result.time >= 360.0) & (result.time <= 430.0)
    return float(np.mean(result.core_energy[late]) / np.mean(result.core_energy[early]))


def moment_metrics(result: RadialEvolution) -> dict[str, float] | None:
    try:
        output: dict[str, float] = {
            "retention": core_retention(result),
            "core_radius": result.core_radius,
        }
        for start in (220.0, 300.0):
            center = estimate_angular_frequency(
                result.time, result.center, window_start=start
            )
            moment_fft = estimate_angular_frequency(
                result.time,
                result.core_energy_radius_moment,
                window_start=start,
                detrend_linear=True,
            )
            moment_peaks = estimate_peak_angular_frequency(
                result.time,
                result.core_energy_radius_moment,
                window_start=start,
                minimum_period=2.5,
                prominence_fraction=0.1,
            )
            label = int(start)
            output[f"center_fft_{label}"] = center.spectral_omega
            output[f"center_cross_{label}"] = center.crossing_omega
            output[f"moment_fft_{label}"] = moment_fft.spectral_omega
            output[f"moment_peak_{label}"] = moment_peaks.angular_frequency
            output[f"ratio_fft_{label}"] = (
                moment_fft.spectral_omega / center.spectral_omega
            )
            output[f"ratio_time_{label}"] = (
                moment_peaks.angular_frequency / center.crossing_omega
            )
            output[f"period_scatter_{label}"] = (
                moment_peaks.relative_period_standard_deviation
            )
            output[f"relative_half_range_{label}"] = window_relative_half_range(
                result, result.core_energy_radius_moment, start
            )
        return output
    except (ValueError, ArithmeticError, NumericalFailure):
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P045-P3D2")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    reproduction = load_yaml(args.source_reproduction)
    ledger.check(
        "the audited P3D2 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    ledger.check(
        "the hash-matched source reproduction exits with its four-check tally",
        reproduction.get("sha256") == EXPECTED_SOURCE_SHA256
        and reproduction.get("exit_code") == 0
        and "ALL 4 CHECKS PASS" in str(reproduction.get("terminal_tally", "")),
    )
    ledger.check(
        "P3D2 uses the current trapezoid API with an older-version fallback",
        'np.trapezoid if hasattr(np, "trapezoid") else np.trapz' in source_text,
    )

    theta, phi = sp.symbols("theta phi", real=True)
    unit = sp.Matrix(
        [
            sp.sin(theta) * sp.cos(phi),
            sp.sin(theta) * sp.sin(phi),
            sp.cos(theta),
        ]
    )

    def sphere_integral(expression: sp.Expr) -> sp.Expr:
        return sp.integrate(
            sp.integrate(expression * sp.sin(theta), (theta, 0, sp.pi)),
            (phi, 0, 2 * sp.pi),
        )

    angular_second = sp.Matrix(
        3,
        3,
        lambda row, column: sp.simplify(
            sphere_integral(unit[row] * unit[column])
        ),
    )
    ledger.check(
        "direct sphere integration gives four-pi-over-three times identity",
        angular_second == 4 * sp.pi * sp.eye(3) / 3,
    )

    scalar, amplitude = sp.symbols("J a", real=True)
    spherical = spherical_density_second_moments(scalar)
    ledger.check(
        "an arbitrary radial density has isotropic second moment and exact STF null",
        spherical.second_moment == scalar * sp.eye(3) / 3
        and sp.trace(spherical.second_moment) == scalar
        and spherical.trace_free_second_moment == sp.zeros(3)
        and spherical.triple_normalized_quadrupole == sp.zeros(3),
    )

    p2 = axisymmetric_p2_density_second_moments(scalar, amplitude)
    expected_normalized = sp.diag(
        -amplitude * scalar / 15,
        -amplitude * scalar / 15,
        2 * amplitude * scalar / 15,
    )
    ledger.check(
        "the exact P2 deformation has a nonzero axisymmetric STF tensor",
        p2.trace_free_second_moment == expected_normalized
        and p2.triple_normalized_quadrupole == 3 * expected_normalized
        and sp.simplify(sp.trace(p2.second_moment) - scalar) == 0,
    )

    mu = sp.symbols("mu", real=True)
    polynomial = (3 * mu**2 - 1) / 2
    ledger.check(
        "independent polynomial moments reproduce the P2 diagonal coefficients",
        sp.integrate(polynomial, (mu, -1, 1)) == 0
        and sp.integrate(mu**2 * polynomial, (mu, -1, 1)) == sp.Rational(4, 15)
        and sp.integrate((1 - mu**2) * polynomial, (mu, -1, 1))
        == -sp.Rational(4, 15),
    )

    nodes, weights = np.polynomial.legendre.leggauss(24)
    azimuth = 2.0 * np.pi * np.arange(48) / 48.0
    numeric_tensor = np.zeros((3, 3))
    numeric_amplitude = 0.37
    for node, weight in zip(nodes, weights):
        polar_radius = np.sqrt(1.0 - node**2)
        angular_weight = 1.0 + numeric_amplitude * (3.0 * node**2 - 1.0) / 2.0
        for angle in azimuth:
            direction = np.array(
                [polar_radius * np.cos(angle), polar_radius * np.sin(angle), node]
            )
            numeric_tensor += (
                weight
                * (2.0 * np.pi / azimuth.size)
                * angular_weight
                * np.outer(direction, direction)
            )
    numeric_tensor /= 4.0 * np.pi
    numeric_stf = numeric_tensor - np.eye(3) * np.trace(numeric_tensor) / 3.0
    exact_numeric = np.array(
        axisymmetric_p2_density_second_moments(1.0, numeric_amplitude)
        .trace_free_second_moment,
        dtype=float,
    )
    ledger.check(
        "independent direct angular quadrature agrees with the exact P2 API",
        np.max(np.abs(numeric_stf - exact_numeric)) < 2.0e-14,
    )

    def isotropic_coefficient_predicate(candidate: object) -> bool:
        coefficient = sp.sympify(candidate)
        moment = coefficient * scalar * sp.eye(3)
        return bool(
            moment == scalar * sp.eye(3) / 3
            and sp.trace(moment) == scalar
            and symmetric_trace_free(moment) == sp.zeros(3)
        )

    ledger.mutation_sensitive(
        "isotropic second-moment normalization",
        isotropic_coefficient_predicate,
        sp.Rational(1, 3),
        [1, sp.Rational(1, 2), sp.Rational(1, 4)],
    )

    long_common = dict(
        amplitude=3.0,
        width=4.0,
        outer_radius=200.0,
        final_time=450.0,
        core_radius=30.0,
        sample_interval=0.2,
        damping_width=50.0,
    )
    coarse = evolve_radial_sine_gordon_leapfrog(
        **long_common, spacing=0.1, courant=0.4
    )
    baseline = evolve_radial_sine_gordon_leapfrog(
        **long_common, spacing=0.05, courant=0.4
    )
    fine = evolve_radial_sine_gordon_leapfrog(
        **long_common, spacing=0.025, courant=0.4
    )
    timestep_fine = evolve_radial_sine_gordon_leapfrog(
        **long_common, spacing=0.05, courant=0.2
    )
    domain_small = evolve_radial_sine_gordon_leapfrog(
        **{**long_common, "outer_radius": 160.0}, spacing=0.1, courant=0.4
    )
    domain_large = evolve_radial_sine_gordon_leapfrog(
        **{**long_common, "outer_radius": 240.0}, spacing=0.1, courant=0.4
    )
    core_20 = evolve_radial_sine_gordon_leapfrog(
        **{**long_common, "core_radius": 20.0}, spacing=0.1, courant=0.4
    )
    core_25 = evolve_radial_sine_gordon_leapfrog(
        **{**long_common, "core_radius": 25.0}, spacing=0.1, courant=0.4
    )
    core_40 = evolve_radial_sine_gordon_leapfrog(
        **{**long_common, "core_radius": 40.0}, spacing=0.1, courant=0.4
    )
    weak = evolve_radial_sine_gordon_leapfrog(
        **{**long_common, "amplitude": 4.0, "width": 3.0},
        spacing=0.1,
        courant=0.4,
    )
    results = {
        "coarse": coarse,
        "baseline": baseline,
        "fine": fine,
        "timestep_fine": timestep_fine,
        "domain_small": domain_small,
        "domain_large": domain_large,
        "core_20": core_20,
        "core_25": core_25,
        "core_40": core_40,
        "weak": weak,
    }
    metrics = {name: moment_metrics(result) for name, result in results.items()}
    for name, values in metrics.items():
        if values is None:
            print(f"  {name}: no resolved combined moment-frequency verdict")
        else:
            print(
                f"  {name}: retention={values['retention']:.9f}, "
                f"Rcore={values['core_radius']:.1f}, "
                f"window220=(fft={values['moment_fft_220']:.9f}, "
                f"peaks={values['moment_peak_220']:.9f}, "
                f"ratios={values['ratio_fft_220']:.9f}/"
                f"{values['ratio_time_220']:.9f}), "
                f"window300=(fft={values['moment_fft_300']:.9f}, "
                f"peaks={values['moment_peak_300']:.9f}, "
                f"ratios={values['ratio_fft_300']:.9f}/"
                f"{values['ratio_time_300']:.9f})"
            )

    ledger.check(
        "all radial evolutions complete and record finite derived moment traces",
        all(
            result.completed
            and np.all(np.isfinite(result.core_energy_radius_moment))
            and np.all(np.isfinite(result.total_energy_radius_moment))
            for result in results.values()
        ),
    )
    baseline_metrics = metrics["baseline"]
    assert baseline_metrics is not None
    ledger.check(
        "the declared core energy-radius moment has resolved nontrivial breathing",
        baseline_metrics["relative_half_range_220"] > 0.25
        and baseline_metrics["relative_half_range_300"] > 0.25,
    )
    ledger.check(
        "FFT and prominent-peak routes place the core moment near twice the field frequency",
        max(
            abs(baseline_metrics[key] - 2.0)
            for key in (
                "ratio_fft_220",
                "ratio_time_220",
                "ratio_fft_300",
                "ratio_time_300",
            )
        )
        < 0.003
        and max(
            baseline_metrics["period_scatter_220"],
            baseline_metrics["period_scatter_300"],
        )
        < 0.03,
    )
    ledger.check(
        "the two moment-frequency estimators agree on both settled windows",
        max(
            abs(
                baseline_metrics[f"moment_fft_{start}"]
                - baseline_metrics[f"moment_peak_{start}"]
            )
            for start in (220, 300)
        )
        < 0.007,
    )

    comparable = [
        metrics[name]
        for name in (
            "coarse",
            "fine",
            "timestep_fine",
            "domain_small",
            "domain_large",
        )
    ]
    assert all(item is not None for item in comparable)
    ledger.check(
        "mesh, timestep, and domain changes preserve moment-frequency ratios",
        max(
            abs(item[f"ratio_fft_{start}"] - 2.0)  # type: ignore[index]
            for item in comparable
            for start in (220, 300)
        )
        < 0.001
        and max(
            abs(item[f"ratio_time_{start}"] - 2.0)  # type: ignore[index]
            for item in comparable
            for start in (220, 300)
        )
        < 0.002,
    )
    core_metrics = [metrics[name] for name in ("core_20", "core_25", "coarse")]
    assert all(item is not None for item in core_metrics)
    ledger.check(
        "core cutoffs from twenty through thirty preserve the resolved frequency",
        max(
            max(
                item[f"moment_fft_{start}"]  # type: ignore[index]
                for item in core_metrics
            )
            - min(
                item[f"moment_fft_{start}"]  # type: ignore[index]
                for item in core_metrics
            )
            for start in (220, 300)
        )
        < 5.0e-4
        and max(
            abs(item[f"ratio_time_{start}"] - 2.0)  # type: ignore[index]
            for item in core_metrics
            for start in (220, 300)
        )
        < 0.002,
    )

    def numeric_verdict(candidate: object) -> bool:
        values = moment_metrics(candidate)  # type: ignore[arg-type]
        if values is None:
            return False
        return bool(
            values["retention"] > 0.9
            and values["relative_half_range_220"] > 0.25
            and abs(values["ratio_fft_220"] - 2.0) < 0.01
            and abs(values["ratio_time_220"] - 2.0) < 0.01
            and abs(values["ratio_fft_300"] - 2.0) < 0.01
            and abs(values["ratio_time_300"] - 2.0) < 0.01
        )

    ledger.mutation_sensitive(
        "persistent-core twice-frequency moment verdict",
        numeric_verdict,
        baseline,
        [core_40, weak],
    )
    ledger.check(
        "P3D2's numerical STF zero is exact-theorem regression rather than an independent oracle",
        "I = (S / 3.0) * delta" in source_text
        and "Q = stf_Q(I)" in source_text,
    )
    ledger.check(
        "P3D2's exact FFT-bin ratio is resolution bounded rather than exact frequency equality",
        abs(
            float(reproduction["reported_values"]["core_fft_omega"]) - 0.8901
        )
        < 1.0e-12
        and baseline_metrics["moment_fft_220"]
        != 2.0 * baseline_metrics["center_fft_220"],
    )

    return ledger.finish()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"P045 verifier failed: {error}", file=sys.stderr)
        raise
