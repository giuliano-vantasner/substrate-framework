#!/usr/bin/env python3
"""Verify P044's finite-time radial sine-Gordon oscillon evidence."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.governance import load_yaml
from substrate_framework.numerics import SolverTolerances
from substrate_framework.radial_sine_gordon import (
    RadialEvolution,
    estimate_angular_frequency,
    evolve_radial_sine_gordon_leapfrog,
    evolve_radial_sine_gordon_mol,
    radial_laplacian,
    radial_sine_gordon_energy,
)
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "f93b8dabfca0c49fb0bf1101c926e79c43dc2e9ebb35882083611a12ca9514fa"
)


def relative_range(values: np.ndarray) -> float:
    """Return peak-to-peak variation relative to the first value."""

    return float(np.ptp(values) / values[0])


def window_mean(result: RadialEvolution, values: np.ndarray, start: float, end: float) -> float:
    selected = (result.time >= start) & (result.time <= end)
    if np.count_nonzero(selected) < 2:
        raise ValueError("diagnostic window contains fewer than two samples")
    return float(np.mean(values[selected]))


def window_amplitude(result: RadialEvolution, start: float, end: float) -> float:
    selected = (result.time >= start) & (result.time <= end)
    return float(np.ptp(result.center[selected]) / 2.0)


def settled_metrics(result: RadialEvolution) -> dict[str, float]:
    early_core = window_mean(result, result.core_energy, 120.0, 180.0)
    late_core = window_mean(result, result.core_energy, 360.0, 430.0)
    frequency_220 = estimate_angular_frequency(
        result.time, result.center, window_start=220.0
    )
    frequency_300 = estimate_angular_frequency(
        result.time, result.center, window_start=300.0
    )
    late = result.time >= 320.0
    relative_slope = float(
        np.polyfit(result.time[late], result.core_energy[late], 1)[0]
        / np.mean(result.core_energy[late])
    )
    return {
        "retention": late_core / early_core,
        "late_amplitude": window_amplitude(result, 360.0, 430.0),
        "omega_fft_220": frequency_220.spectral_omega,
        "omega_cross_220": frequency_220.crossing_omega,
        "omega_fft_300": frequency_300.spectral_omega,
        "omega_cross_300": frequency_300.crossing_omega,
        "fft_bin_300": frequency_300.fft_bin_width,
        "cycles_300": float(frequency_300.crossing_cycles),
        "relative_core_slope": relative_slope,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P044-P3D1")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    reproduction = load_yaml(args.source_reproduction)
    ledger.check(
        "the audited P3D1 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    ledger.check(
        "the durable reproduction record is hash matched and exited cleanly",
        reproduction.get("sha256") == EXPECTED_SOURCE_SHA256
        and reproduction.get("exit_code") == 0,
    )
    ledger.check(
        "the source's declared six-check terminal tally reproduced",
        "ALL 6 CHECKS PASS" in str(reproduction.get("terminal_tally", "")),
    )
    ledger.check(
        "the source selects the current NumPy trapezoid API before its legacy fallback",
        'np.trapezoid if hasattr(np, "trapezoid") else np.trapz' in source_text
        and callable(getattr(np, "trapezoid", None) or getattr(np, "trapz", None)),
    )

    radius = sp.symbols("r", positive=True, real=True)
    field, field_t, field_r = sp.symbols("u u_t u_r", real=True)
    field_tt, field_rr, field_tr = sp.symbols("u_tt u_rr u_tr", real=True)
    radial_lagrangian = radius**2 * (
        field_t**2 / 2 - field_r**2 / 2 - (1 - sp.cos(field))
    )
    time_term = radius**2 * field_tt
    radial_term = -2 * radius * field_r - radius**2 * field_rr
    field_term = sp.diff(radial_lagrangian, field)
    euler_lagrange = sp.expand(time_term + radial_term - field_term)
    radial_equation = field_tt - field_rr - 2 * field_r / radius + sp.sin(field)
    ledger.check(
        "radial action variation gives the declared 3+1 sine-Gordon equation",
        sp.simplify(euler_lagrange - radius**2 * radial_equation) == 0,
    )
    energy_time_derivative = (
        field_t * field_tt + field_r * field_tr + sp.sin(field) * field_t
    )
    outward_divergence = (
        2 * field_t * field_r / radius
        + field_tr * field_r
        + field_t * field_rr
    )
    ledger.check(
        "the radial PDE implies the exact local energy continuity equation",
        sp.simplify(
            (energy_time_derivative - outward_divergence).subs(
                field_tt, field_rr + 2 * field_r / radius - sp.sin(field)
            )
        )
        == 0,
    )
    ledger.check(
        "linearization fixes the dimensionless continuum threshold at omega one",
        sp.limit(sp.sin(field) / field, field, 0) == 1,
    )

    wave_number = 0.7
    operator_errors: list[float] = []
    origin_residuals: list[float] = []
    for spacing in (0.2, 0.1, 0.05):
        grid = spacing * np.arange(int(round(20.0 / spacing)) + 1)
        regular_mode = wave_number * np.sinc(wave_number * grid / np.pi)
        residual = (
            radial_laplacian(regular_mode, spacing)[:-2]
            + wave_number**2 * regular_mode[:-2]
        )
        operator_errors.append(float(np.max(np.abs(residual))))
        origin_residuals.append(abs(float(residual[0])))
    operator_ratios = [
        operator_errors[index] / operator_errors[index + 1]
        for index in range(2)
    ]
    ledger.check(
        "the regular spherical Klein-Gordon mode validates the origin and radial operator",
        max(origin_residuals) < 4.0e-4
        and operator_errors[-1] < 4.0e-5
        and min(operator_ratios) > 3.9,
    )

    quadratic_grid = 0.05 * np.arange(201)
    quadratic = quadratic_grid**2

    def geometry_predicate(candidate: object) -> bool:
        coefficient = float(candidate)
        values = radial_laplacian(
            quadratic, 0.05, geometric_coefficient=coefficient
        )[:-1]
        return bool(np.allclose(values, 6.0, rtol=0.0, atol=2.0e-10))

    ledger.mutation_sensitive(
        "three-dimensional geometric coefficient and regular-origin stencil",
        geometry_predicate,
        2.0,
        [0.0, 1.0, 3.0],
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
    weak_packet = evolve_radial_sine_gordon_leapfrog(
        **{**long_common, "amplitude": 4.0, "width": 3.0},
        spacing=0.1,
        courant=0.4,
    )
    metrics = {name: settled_metrics(result) for name, result in (
        ("coarse", coarse),
        ("baseline", baseline),
        ("fine", fine),
        ("timestep_fine", timestep_fine),
        ("domain_small", domain_small),
        ("domain_large", domain_large),
        ("weak_packet", weak_packet),
    )}

    print("P044 finite-time metrics")
    for name, values in metrics.items():
        print(
            f"  {name}: retention={values['retention']:.9f}, "
            f"late_amp={values['late_amplitude']:.9f}, "
            f"omega220=({values['omega_fft_220']:.9f},"
            f"{values['omega_cross_220']:.9f}), "
            f"omega300=({values['omega_fft_300']:.9f},"
            f"{values['omega_cross_300']:.9f}), "
            f"slope={values['relative_core_slope']:.9e}"
        )

    ledger.check(
        "all fixed-step evolutions complete with finite diagnostics",
        all(
            result.completed
            and np.all(np.isfinite(result.center))
            and np.all(np.isfinite(result.core_energy))
            and np.all(np.isfinite(result.total_energy))
            for result in (
                coarse,
                baseline,
                fine,
                timestep_fine,
                domain_small,
                domain_large,
                weak_packet,
            )
        ),
    )
    baseline_metrics = metrics["baseline"]
    frequency_values = [
        baseline_metrics[key]
        for key in (
            "omega_fft_220",
            "omega_cross_220",
            "omega_fft_300",
            "omega_cross_300",
        )
    ]
    ledger.check(
        "the late core remains localized and oscillatory through t=430",
        baseline_metrics["retention"] > 0.92
        and baseline_metrics["late_amplitude"] > 4.0
        and baseline_metrics["cycles_300"] >= 20,
    )
    ledger.check(
        "two estimators and two settled windows resolve a sub-threshold frequency",
        min(frequency_values) > 0.90
        and max(frequency_values) < 0.94
        and baseline_metrics["fft_bin_300"] < 0.05,
    )
    ledger.check(
        "the finite-time leakage observation is bounded without fitting an exponential law",
        -1.5e-4 < baseline_metrics["relative_core_slope"] < -1.0e-4,
    )

    common_time = baseline.time[baseline.time <= 60.0]
    coarse_center = np.interp(common_time, coarse.time, coarse.center)
    fine_center = np.interp(common_time, fine.time, fine.center)
    coarse_difference = float(np.sqrt(np.mean(np.square(coarse_center - baseline.center[: common_time.size]))))
    fine_difference = float(np.sqrt(np.mean(np.square(baseline.center[: common_time.size] - fine_center))))
    ledger.check(
        "the center trajectory has second-order spatial self-convergence",
        fine_difference < coarse_difference
        and coarse_difference / fine_difference > 3.7
        and fine_difference < 2.0e-3,
    )
    ledger.check(
        "halving the timestep leaves load-bearing long-time metrics stable",
        abs(metrics["timestep_fine"]["retention"] - baseline_metrics["retention"])
        < 5.0e-5
        and max(
            abs(metrics["timestep_fine"][key] - baseline_metrics[key])
            for key in ("omega_fft_220", "omega_cross_220")
        )
        < 5.0e-4,
    )
    ledger.check(
        "moving the sponge and outer boundary leaves core observables unchanged",
        max(
            abs(metrics[name]["retention"] - metrics["coarse"]["retention"])
            for name in ("domain_small", "domain_large")
        )
        < 1.0e-6
        and max(
            abs(metrics[name]["omega_cross_220"] - metrics["coarse"]["omega_cross_220"])
            for name in ("domain_small", "domain_large")
        )
        < 1.0e-6
        and max(
            domain_small.max_monitor_amplitude,
            coarse.max_monitor_amplitude,
            domain_large.max_monitor_amplitude,
        )
        < 4.0e-3,
    )

    final_total = radial_sine_gordon_energy(
        baseline.final_field, baseline.final_velocity, baseline.radius
    )
    core_fractions: dict[float, float] = {}
    for core_radius in (10.0, 20.0, 30.0, 40.0):
        selected = baseline.radius <= core_radius
        core_fractions[core_radius] = radial_sine_gordon_energy(
            baseline.final_field[selected],
            baseline.final_velocity[selected],
            baseline.radius[selected],
        ) / final_total
    ledger.check(
        "late localization is stable under the declared core-radius diagnostic",
        core_fractions[10.0] > 0.93
        and core_fractions[40.0] < 0.97
        and all(
            core_fractions[right] > core_fractions[left]
            for left, right in zip((10.0, 20.0, 30.0), (20.0, 30.0, 40.0))
        ),
    )

    closed_results = [
        evolve_radial_sine_gordon_leapfrog(
            amplitude=3.0,
            width=4.0,
            spacing=spacing,
            outer_radius=140.0,
            final_time=120.0,
            core_radius=30.0,
            sample_interval=0.2,
            courant=0.4,
        )
        for spacing in (0.1, 0.05, 0.025)
    ]
    energy_variations = [relative_range(result.total_energy) for result in closed_results]
    ledger.check(
        "closed-box energy variation decreases at second order on three grids",
        energy_variations[2] < energy_variations[1] < energy_variations[0]
        and energy_variations[2] < 8.0e-5
        and energy_variations[0] / energy_variations[1] > 3.8
        and energy_variations[1] / energy_variations[2] > 3.8,
    )
    ledger.check(
        "the closed-box boundary remains causally quiet during the energy audit",
        max(result.max_monitor_amplitude for result in closed_results) < 1.0e-20,
    )

    independent_common = dict(
        amplitude=3.0,
        width=4.0,
        spacing=0.2,
        outer_radius=80.0,
        final_time=60.0,
        core_radius=20.0,
        sample_interval=0.2,
    )
    independent_leapfrog = evolve_radial_sine_gordon_leapfrog(
        **independent_common, courant=0.4
    )
    independent_mol = evolve_radial_sine_gordon_mol(
        **independent_common,
        tolerances=SolverTolerances(rtol=2.0e-7, atol=2.0e-9, max_step=0.1),
    )
    overlap = (
        (independent_mol.time >= independent_leapfrog.time[0])
        & (independent_mol.time <= independent_leapfrog.time[-1])
    )
    comparison_time = independent_mol.time[overlap]
    leapfrog_center = np.interp(
        comparison_time, independent_leapfrog.time, independent_leapfrog.center
    )
    leapfrog_core = np.interp(
        comparison_time, independent_leapfrog.time, independent_leapfrog.core_energy
    )
    center_relative_rms = float(
        np.sqrt(np.mean(np.square(leapfrog_center - independent_mol.center[overlap])))
        / np.std(independent_mol.center[overlap])
    )
    core_relative_max = float(
        np.max(np.abs(leapfrog_core - independent_mol.core_energy[overlap]))
        / np.mean(independent_mol.core_energy[overlap])
    )
    ledger.check(
        "independent DOP853 method-of-lines evolution agrees with leapfrog",
        independent_mol.completed
        and independent_mol.function_evaluations is not None
        and independent_mol.function_evaluations > 0
        and center_relative_rms < 0.011
        and core_relative_max < 0.003,
    )

    def oscillon_predicate(candidate: object) -> bool:
        values = settled_metrics(candidate)  # type: ignore[arg-type]
        frequencies = [
            values["omega_fft_220"],
            values["omega_cross_220"],
            values["omega_fft_300"],
            values["omega_cross_300"],
        ]
        return bool(
            values["retention"] > 0.9
            and values["late_amplitude"] > 3.0
            and max(frequencies) < 0.95
        )

    ledger.mutation_sensitive(
        "finite-time localized sub-gap trajectory verdict",
        oscillon_predicate,
        baseline,
        [weak_packet],
    )
    ledger.check(
        "invalid explicit Courant factors are rejected before evolution",
        rejects_invalid_courant(),
    )

    print(
        "P044 error controls: "
        f"operator={operator_errors}, spatial_rms=({coarse_difference:.9e},"
        f" {fine_difference:.9e}), energy_variations={energy_variations}, "
        f"independent=(center_rms={center_relative_rms:.9e}, "
        f"core_max={core_relative_max:.9e}), core_fractions={core_fractions}"
    )
    return ledger.finish()


def rejects_invalid_courant() -> bool:
    try:
        evolve_radial_sine_gordon_leapfrog(
            amplitude=3.0,
            width=4.0,
            spacing=0.1,
            outer_radius=20.0,
            final_time=1.0,
            core_radius=5.0,
            courant=1.0,
        )
    except ValueError:
        return True
    return False


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"P044 verifier failed: {error}", file=sys.stderr)
        raise
