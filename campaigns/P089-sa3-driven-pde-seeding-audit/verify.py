#!/usr/bin/env python3
"""Primary verifier for the P089 SA3 driven-PDE audit."""

from __future__ import annotations

import ast
import hashlib
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework import (
    BulkDrivenSineGordonEvolution,
    BreatherSnapshotFit,
    BreatherTraceFit,
    evolve_bulk_driven_sine_gordon_leapfrog,
    fit_rest_breather_center_trace,
    fit_rest_breather_snapshot,
    gaussian_sine_full_line_l2,
    gaussian_sine_trace,
    localized_sech_bulk_source,
    moving_breather_samples,
)
from substrate_framework.numerics import trapezoid_integral
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-25/"
    "bridge_SA3_driven_sg_pde_seeding.py"
)
SOURCE_SHA256 = "3aec2a8bca448f28bceb175e44ff2a6c3dcba3b57c22a0dcbd93f8d405a17e8f"
CONTRACT_SHA256 = "5e983910488a13104d250e3cb8e3d35c7f308126926ed282909a7e32a911e464"
FREEZE_SHA256 = "8e7f165f0f377116d44fa285f31826a5f4782b4ef5778f0c81aa7580b861f918"

OMEGA_DRIVE = 1.0 / np.sqrt(2.0)
INVERSE_SOURCE_WIDTH = np.sqrt(1.0 - OMEGA_DRIVE**2)
FAST_WIDTH = 4.0 / OMEGA_DRIVE
SOURCE_CENTER_TIME = 30.0
PROXY_TARGET = 400.0
FINAL_TIME = 410.0
LATE_TIME = 320.0
CORE_RADIUS = 12.0
SAMPLE_INTERVAL = 0.16


@dataclass(frozen=True)
class ClassifiedRun:
    result: BulkDrivenSineGordonEvolution
    trace_fit: BreatherTraceFit
    snapshot_fit: BreatherSnapshotFit
    late_core_mean: float


def _campaign_dir() -> Path:
    candidates = (
        Path("campaigns/P089-sa3-driven-pde-seeding-audit"),
        Path("proposals/P089-sa3-driven-pde-seeding-audit"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _damping(coordinate: np.ndarray, outer_radius: float, width: float) -> np.ndarray:
    damping = np.zeros_like(coordinate)
    start = outer_radius - width
    selected = np.abs(coordinate) > start
    damping[selected] = np.square(
        (np.abs(coordinate[selected]) - start) / width
    )
    return damping


def _amplitude(target: float, frequency: float, width: float) -> float:
    return float(
        np.sqrt(target / gaussian_sine_full_line_l2(1.0, frequency, width))
    )


def _run(
    *,
    spacing: float,
    outer_radius: float = 80.0,
    sponge_width: float = 40.0,
    proxy_target: float = PROXY_TARGET,
    frequency: float = OMEGA_DRIVE,
    temporal_width: float = FAST_WIDTH,
    courant: float = 0.4,
) -> ClassifiedRun:
    point_count = int(round(2.0 * outer_radius / spacing)) + 1
    coordinate = np.linspace(-outer_radius, outer_radius, point_count)
    zero = np.zeros_like(coordinate)
    amplitude = _amplitude(proxy_target, frequency, temporal_width)
    source = localized_sech_bulk_source(
        coordinate,
        INVERSE_SOURCE_WIDTH,
        gaussian_sine_trace(
            amplitude,
            frequency,
            SOURCE_CENTER_TIME,
            temporal_width,
        ),
    )
    result = evolve_bulk_driven_sine_gordon_leapfrog(
        coordinate,
        zero,
        zero,
        source,
        _damping(coordinate, outer_radius, sponge_width),
        FINAL_TIME,
        courant * spacing,
        core_radius=CORE_RADIUS,
        sample_interval=SAMPLE_INTERVAL,
    )
    late = result.time > LATE_TIME
    trace_fit = fit_rest_breather_center_trace(
        result.time[late],
        result.center_field[late],
    )
    snapshot_fit = fit_rest_breather_snapshot(
        result.coordinate,
        result.final_field,
        result.final_velocity,
        fit_radius=CORE_RADIUS,
    )
    return ClassifiedRun(
        result=result,
        trace_fit=trace_fit,
        snapshot_fit=snapshot_fit,
        late_core_mean=float(np.mean(result.core_energy[late])),
    )


def _passes_narrow_breather_classifier(run: ClassifiedRun) -> bool:
    energy_error = abs(
        run.late_core_mean - run.trace_fit.fitted_energy
    ) / run.trace_fit.fitted_energy
    return bool(
        run.trace_fit.relative_rms_error < 0.05
        and run.snapshot_fit.joint_relative_l2_error < 0.12
        and energy_error < 0.03
        and 0.15 < run.trace_fit.angular_frequency < 0.4
    )


def _source_fft_bin(spacing: float, bin_index: int) -> float:
    time_step = 0.4 * spacing
    steps = int(FINAL_TIME / time_step)
    labels = np.asarray(
        [
            step * time_step
            for step in range(2, steps + 1)
            if step % 8 == 0 and step * time_step > LATE_TIME
        ]
    )
    frequencies = 2.0 * np.pi * np.fft.rfftfreq(
        labels.size,
        labels[1] - labels[0],
    )
    return float(frequencies[bin_index])


def main() -> int:
    checks = CheckLedger("P089")
    campaign_dir = _campaign_dir()
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("SA3 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
    normalized_contract = (campaign_dir / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n",
        b"status: draft\n",
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    checks.check(
        "pre-source freeze record remains immutable",
        _sha256(campaign_dir / "evidence/frozen-proposal.yaml") == FREEZE_SHA256,
    )
    literal_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source has five literal checks and a clean terminal tally",
        len(literal_checks) == 5
        and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source selects current trapezoid before its legacy fallback",
        'np.trapezoid if hasattr(np, "trapezoid") else np.trapz' in source_text,
    )
    checks.check(
        "source labels the previous-time field with the new-time timestamp",
        "t = n * dt" in source_text
        and "rec_t.append(t)" in source_text
        and "rec_core.append(phi_cur[icore])" in source_text,
    )
    deposited_function = next(
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.FunctionDef) and node.name == "deposited_energy"
    )
    deposited_names = {
        node.id for node in ast.walk(deposited_function) if isinstance(node, ast.Name)
    }
    checks.check(
        "source proxy is a waveform norm rather than deposited PDE energy",
        {"phi", "ut", "Jfield", "sp"}.isdisjoint(deposited_names)
        and "f(tt) ** 2" in ast.get_source_segment(source_text, deposited_function),
    )

    phi_t, phi_x, phi_tt, phi_xx, phi_xt, source, gamma = sp.symbols(
        "phi_t phi_x phi_tt phi_xx phi_xt J gamma",
        real=True,
    )
    energy_rate = phi_t * phi_tt + phi_x * phi_xt + sp.Symbol("sin_phi") * phi_t
    equation = phi_xx - sp.Symbol("sin_phi") + source - gamma * phi_t
    flux_divergence = phi_xt * phi_x + phi_t * phi_xx
    checks.check(
        "forced damped energy balance retains work dissipation and flux",
        sp.simplify(
            energy_rate.subs(phi_tt, equation)
            - flux_divergence
            - source * phi_t
            + gamma * phi_t**2
        )
        == 0,
    )

    amplitude = 1.7
    frequency = 0.8
    width = 2.1
    phase = 0.37
    trace = gaussian_sine_trace(amplitude, frequency, -0.4, width, phase)
    integration_time = np.linspace(-18.0, 18.0, 20001)
    integrated_norm = trapezoid_integral(
        np.square([trace(float(value)) for value in integration_time]),
        integration_time,
    )
    exact_norm = gaussian_sine_full_line_l2(amplitude, frequency, width, phase)
    checks.check(
        "exact Gaussian-sine norm matches independent sampled quadrature",
        abs(integrated_norm - exact_norm) / exact_norm < 2.0e-12,
    )
    slow_frequency = 0.28 * OMEGA_DRIVE
    slow_width = 40.0
    slow_amplitude = _amplitude(PROXY_TARGET, slow_frequency, slow_width)
    slow_trace = gaussian_sine_trace(
        slow_amplitude,
        slow_frequency,
        SOURCE_CENTER_TIME,
        slow_width,
    )
    applied_time = np.linspace(0.0, FINAL_TIME, 100001)
    applied_slow_norm = trapezoid_integral(
        np.square([slow_trace(float(value)) for value in applied_time]),
        applied_time,
    )
    checks.check(
        "simulation truncates the alleged equal-norm slow waveform",
        applied_slow_norm < 0.9 * PROXY_TARGET,
        f"applied slow norm={applied_slow_norm:.9f}",
    )
    checks.check(
        "source frequency outputs are raw finite-window FFT bins",
        abs(_source_fft_bin(0.05, 4) - 0.2790) < 5.0e-4
        and abs(_source_fft_bin(0.025, 4) - 0.2793) < 5.0e-4
        and abs(_source_fft_bin(0.05, 3) - 0.2093) < 5.0e-4,
    )

    classifier_coordinate = np.linspace(-12.0, 12.0, 481)
    exact_field, exact_velocity, _ = moving_breather_samples(
        classifier_coordinate,
        1.1 / 0.53,
        0.53,
    )
    exact_fit = fit_rest_breather_snapshot(
        classifier_coordinate,
        exact_field,
        exact_velocity,
        fit_radius=8.0,
    )
    scaled_fit = fit_rest_breather_snapshot(
        classifier_coordinate,
        0.7 * exact_field,
        0.7 * exact_velocity,
        fit_radius=8.0,
    )
    standing_fit = fit_rest_breather_snapshot(
        classifier_coordinate,
        0.3 * np.cos(np.pi * classifier_coordinate / 24.0),
        np.zeros_like(classifier_coordinate),
        fit_radius=8.0,
    )
    kink_fit = fit_rest_breather_snapshot(
        classifier_coordinate,
        4.0 * np.arctan(np.exp(classifier_coordinate)),
        np.zeros_like(classifier_coordinate),
        fit_radius=8.0,
    )
    checks.check(
        "snapshot classifier recovers an exact planted breather",
        exact_fit.joint_relative_l2_error < 1.0e-11
        and abs(exact_fit.angular_frequency - 0.53) < 1.0e-10,
    )
    checks.check(
        "snapshot classifier rejects amplitude rescaling standing radiation and a kink",
        scaled_fit.joint_relative_l2_error > 0.1
        and standing_fit.joint_relative_l2_error > 0.5
        and kink_fit.joint_relative_l2_error > 0.5,
    )

    spatial_runs = {
        spacing: _run(spacing=spacing)
        for spacing in (0.05, 0.025, 0.0125)
    }
    checks.check(
        "all three fast-drive grids pass the frozen composite breather classifier",
        all(_passes_narrow_breather_classifier(run) for run in spatial_runs.values()),
    )
    frequencies = [
        spatial_runs[spacing].trace_fit.angular_frequency
        for spacing in (0.05, 0.025, 0.0125)
    ]
    frequency_differences = np.abs(np.diff(frequencies))
    checks.check(
        "late fitted frequency has second-order spatial self-convergence",
        frequency_differences[1] < frequency_differences[0] / 3.5,
        f"frequencies={frequencies}",
    )
    core_means = [
        spatial_runs[spacing].late_core_mean
        for spacing in (0.05, 0.025, 0.0125)
    ]
    core_differences = np.abs(np.diff(core_means))
    checks.check(
        "late core energy has convergent spatial refinement",
        core_differences[1] < core_differences[0] / 3.5,
        f"core means={core_means}",
    )
    balance_residuals = [
        abs(spatial_runs[spacing].result.energy_balance_residual)
        / spatial_runs[spacing].result.cumulative_source_work
        for spacing in (0.05, 0.025, 0.0125)
    ]
    checks.check(
        "source-work damping and final-energy ledger converges under refinement",
        balance_residuals[1] < balance_residuals[0] / 3.5
        and balance_residuals[2] < balance_residuals[1] / 3.5
        and balance_residuals[-1] < 5.0e-5,
        f"relative residuals={balance_residuals}",
    )

    domain_large = _run(spacing=0.05, outer_radius=120.0)
    baseline = spatial_runs[0.05]
    checks.check(
        "fast branch is stable under outer-domain extension",
        _passes_narrow_breather_classifier(domain_large)
        and abs(
            domain_large.trace_fit.angular_frequency
            - baseline.trace_fit.angular_frequency
        )
        < 2.0e-4,
    )
    sponge_runs = [
        _run(spacing=0.05, sponge_width=width_value)
        for width_value in (30.0, 50.0)
    ]
    checks.check(
        "fast branch survives independent sponge-width mutations",
        all(_passes_narrow_breather_classifier(run) for run in sponge_runs)
        and all(
            abs(run.trace_fit.angular_frequency - baseline.trace_fit.angular_frequency)
            < 2.0e-4
            for run in sponge_runs
        ),
    )

    target_mutations = [
        _run(spacing=0.05, proxy_target=target)
        for target in (380.0, 420.0)
    ]
    checks.check(
        "load-bearing proxy-target mutations destroy the narrow fast branch",
        _passes_narrow_breather_classifier(baseline)
        and not any(_passes_narrow_breather_classifier(run) for run in target_mutations),
    )

    slow_run = _run(
        spacing=0.05,
        outer_radius=160.0,
        frequency=slow_frequency,
        temporal_width=slow_width,
    )
    transition_count = int(
        np.count_nonzero(
            np.diff(np.floor((slow_run.result.final_field + np.pi) / (2.0 * np.pi)))
        )
    )
    checks.check(
        "slow control receives more than three times the fast source work",
        slow_run.result.cumulative_source_work
        > 3.0 * baseline.result.cumulative_source_work,
        (
            f"fast work={baseline.result.cumulative_source_work:.9f}, "
            f"slow work={slow_run.result.cumulative_source_work:.9f}"
        ),
    )
    checks.check(
        "slow control forms a nonvacuum multi-transition state outside the core tally",
        slow_run.result.total_energy[-1] > 64.0
        and np.max(slow_run.result.final_field) > 7.0 * np.pi
        and transition_count >= 8
        and slow_run.snapshot_fit.joint_relative_l2_error > 0.5,
        (
            f"energy={slow_run.result.total_energy[-1]:.9f}, "
            f"field_max={np.max(slow_run.result.final_field):.9f}, "
            f"transitions={transition_count}"
        ),
    )

    print("P089 spatial metrics")
    for spacing, run in spatial_runs.items():
        print(
            f"  dx={spacing:.4f} omega={run.trace_fit.angular_frequency:.9f} "
            f"trace_rel={run.trace_fit.relative_rms_error:.9e} "
            f"snapshot_joint={run.snapshot_fit.joint_relative_l2_error:.9e} "
            f"core_mean={run.late_core_mean:.9f} "
            f"work={run.result.cumulative_source_work:.9f} "
            f"loss={run.result.cumulative_damping_loss:.9f} "
            f"balance={run.result.energy_balance_residual:.9e}"
        )
    print(
        "P089 slow metrics: "
        f"work={slow_run.result.cumulative_source_work:.9f}, "
        f"total_energy={slow_run.result.total_energy[-1]:.9f}, "
        f"field_max={np.max(slow_run.result.final_field):.9f}, "
        f"transitions={transition_count}, "
        f"snapshot_joint={slow_run.snapshot_fit.joint_relative_l2_error:.9f}"
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
