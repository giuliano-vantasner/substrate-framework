#!/usr/bin/env python3
"""Primary verifier for P051's NC4 numerical and interpretation audit."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

from substrate_framework import (
    CheckLedger,
    SolverTolerances,
    breather_field,
    evolve_driven_sine_gordon_leapfrog,
    evolve_driven_sine_gordon_mol,
    evolve_periodic_sine_gordon_leapfrog,
    evolve_periodic_sine_gordon_mol,
    gaussian_sine_neumann_drive,
    load_yaml,
    moving_breather_samples,
    sampled_boundary_sign_correlation,
    sine_gordon_residual,
)

SOURCE_SHA256 = "9efa788da093213f354cbd9e26b7bd0be81129d6f966128b5c0fd10fe0081570"
STUDY_SHA256 = "15891957668461dd8c50a4fdb44e716838d439c6b9b76472425131a3f9d08c9f"
FREQUENCIES = (0.2, 0.4, 0.6, 0.8)
SOURCE_PHASES = {0.2: 5.50, 0.4: 0.79, 0.6: 5.50, 0.8: 4.71}


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_parameters(omega: float) -> dict[str, float]:
    inverse_width = float(np.sqrt(1.0 - omega**2))
    breather_speed = 0.3
    initial_center = 35.0
    impact_time = initial_center / breather_speed
    interaction_width = 1.0 / (breather_speed * inverse_width)
    final_time = impact_time + 3.0 * interaction_width + 20.0
    binding_gap = 16.0 * (1.0 - inverse_width)
    _, impact_velocity, _ = moving_breather_samples(
        [0.0],
        impact_time,
        omega,
        velocity=-breather_speed,
        center=initial_center,
    )
    force_amplitude = (
        binding_gap
        * np.pi
        / (2.0 * abs(float(impact_velocity[0])) * interaction_width)
    )
    return {
        "inverse_width": inverse_width,
        "breather_speed": breather_speed,
        "initial_center": initial_center,
        "impact_time": impact_time,
        "interaction_width": interaction_width,
        "final_time": final_time,
        "force_amplitude": float(force_amplitude),
    }


def _corrected_case(
    omega: float,
    orientation: int,
    intervals: int,
    scale: float,
    phase: float,
    *,
    courant: float = 0.4,
    domain_length: float = 60.0,
) -> tuple[Any, float]:
    parameters = _source_parameters(omega)
    coordinate = np.linspace(0.0, domain_length, intervals + 1)
    field0, velocity0, _ = moving_breather_samples(
        coordinate,
        0.0,
        omega,
        velocity=-parameters["breather_speed"],
        center=parameters["initial_center"],
    )
    drive = gaussian_sine_neumann_drive(
        orientation * scale * parameters["force_amplitude"],
        omega,
        parameters["impact_time"],
        parameters["interaction_width"],
        phase,
    )
    result = evolve_driven_sine_gordon_leapfrog(
        coordinate,
        field0,
        velocity0,
        drive,
        parameters["final_time"],
        courant * domain_length / intervals,
        bulk_start=10.0,
    )
    window = (
        (result.boundary_time > parameters["impact_time"] - 2.0 * parameters["interaction_width"])
        & (result.boundary_time < parameters["impact_time"] + 2.0 * parameters["interaction_width"])
    )
    selected = np.where(window)[0][1:-1]
    correlation = sampled_boundary_sign_correlation(
        result.boundary_time[selected],
        result.boundary_velocity[selected],
        result.boundary_coordinate_derivative[selected],
    )
    return result, correlation


def _adaptive_case(
    orientation: int,
    intervals: int,
    scale: float,
) -> tuple[Any, float]:
    omega = 0.6
    parameters = _source_parameters(omega)
    coordinate = np.linspace(0.0, 60.0, intervals + 1)
    field0, velocity0, _ = moving_breather_samples(
        coordinate,
        0.0,
        omega,
        velocity=-parameters["breather_speed"],
        center=parameters["initial_center"],
    )
    drive = gaussian_sine_neumann_drive(
        orientation * scale * parameters["force_amplitude"],
        omega,
        parameters["impact_time"],
        parameters["interaction_width"],
        SOURCE_PHASES[omega],
    )
    sample_times = np.linspace(
        0.0,
        parameters["final_time"],
        int(np.ceil(parameters["final_time"] / 0.1)) + 1,
    )
    result = evolve_driven_sine_gordon_mol(
        coordinate,
        field0,
        velocity0,
        drive,
        sample_times,
        bulk_start=10.0,
        tolerances=SolverTolerances(rtol=1.0e-8, atol=1.0e-10, max_step=0.1),
    )
    window = (
        (result.boundary_time > parameters["impact_time"] - 2.0 * parameters["interaction_width"])
        & (result.boundary_time < parameters["impact_time"] + 2.0 * parameters["interaction_width"])
    )
    selected = np.where(window)[0][1:-1]
    correlation = sampled_boundary_sign_correlation(
        result.boundary_time[selected],
        result.boundary_velocity[selected],
        result.boundary_coordinate_derivative[selected],
    )
    return result, correlation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--study-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    parser.add_argument("--migration-queue", type=Path, required=True)
    arguments = parser.parse_args()
    ledger = CheckLedger("P051-NC4")
    campaign = Path(__file__).resolve().parent

    source_text = arguments.source_file.read_text(encoding="utf-8")
    study_text = arguments.study_file.read_text(encoding="utf-8")
    reproduction = load_yaml(arguments.source_reproduction)
    adapter_result = load_yaml(campaign / "attempts/0002/result.yaml")
    queue = load_yaml(arguments.migration_queue)
    queue_entry = next(
        unit for unit in queue["units"] if unit["source_unit"] == "NC4"
    )
    ledger.check(
        "the NC4 source is the hash-pinned primary unit",
        _hash(arguments.source_file) == SOURCE_SHA256
        and queue_entry["sha256"] == SOURCE_SHA256
        and queue_entry["disposition"] in {"pending_adjudication", "qualified"},
    )
    ledger.check("the imported study solver is pinned at the audited baseline", _hash(arguments.study_file) == STUDY_SHA256)
    ledger.check("literal current-environment reproduction fails before a tally", reproduction["process_exit_code"] == 1 and reproduction["terminal_tally"] is None and reproduction["verdict"] == "reproduction_failed_on_removed_numpy_api")
    ledger.check("the compatibility-only adapter recovers the source's thirty checks", adapter_result["process_exit_code"] == 0 and adapter_result["terminal_tally"] == "ALL 30 CHECKS PASS")
    ledger.check("the removed quadrature name is source evidence rather than canonical code", "np.trapz(" in source_text and "np.trapz(" not in (campaign.parent.parent / "src/substrate_framework/sine_gordon_1d.py").read_text(encoding="utf-8"))

    source_spacing = 60.0 / 2400.0
    coordinate_spacing = 60.0 / (2400.0 - 1.0)
    ledger.check("NC4's source coordinate and stencil spacings are inconsistent", coordinate_spacing != source_spacing and "np.linspace(0, L, Nx)" in source_text and "dx = L / Nx" in source_text)
    ledger.check("the imported right boundary overwrites five evolved cells", "phi_new[-5:] = phi_new[-6]" in source_text and "phi_new[-5:] = phi_new[-6]" in study_text)
    ledger.check("q_bulk is an endpoint coordinate on a finite subinterval", "q_bulk = (phi_final[bulk_mask][-1] - phi_final[bulk_mask][0])" in study_text)
    ledger.check("the source explicitly calibrates a phase separately at every frequency", "calibrated as the phase that maximises" in source_text and all(f"{frequency}: {phase:.2f}" in source_text for frequency, phase in SOURCE_PHASES.items()))
    ledger.check("the charge and correlation headlines use different drive strengths", "DIAG_SCALE = 0.15" in source_text and "FULL_SCALE = 1.0" in source_text)
    ledger.check("source refinement couples space and time at one selected frequency", "WC = 0.6" in source_text and "Nx1 = 2 * Nx0" in source_text and "dt = 0.4 * dx" in source_text)
    ledger.check("the zero-drive guard compares identical eps-independent inputs", "scale=0.0" in source_text and "F0 = scale" in source_text and "return eps * F0" in source_text)

    x, t, omega = sp.symbols("x t omega", real=True)
    field = breather_field(x, t, sp.Rational(3, 5))
    residual = sine_gordon_residual(field, x, t)
    spatial_second = sp.diff(field, x, 2)
    sine_term = sp.sin(field)
    ledger.check("the accepted nonlinear breather solves the exact PDE", sp.trigsimp(residual) == 0)
    ledger.mutation_sensitive(
        "the spatial operator sign is load-bearing",
        lambda coefficient: sp.simplify(residual + (1 - coefficient) * spatial_second) == 0,
        1,
        (0, -1),
    )
    ledger.mutation_sensitive(
        "the nonlinear sine coefficient is load-bearing",
        lambda coefficient: sp.trigsimp(residual + (coefficient - 1) * sine_term) == 0,
        1,
        (0, 2),
    )

    periodic_errors: list[float] = []
    periodic_drifts: list[float] = []
    for point_count in (128, 256, 512):
        coordinate = np.linspace(-20.0, 20.0, point_count, endpoint=False)
        field0, velocity0, _ = moving_breather_samples(coordinate, 0.0, 0.6)
        spacing = coordinate[1] - coordinate[0]
        evolution = evolve_periodic_sine_gordon_leapfrog(
            coordinate,
            field0,
            velocity0,
            2.0,
            0.2 * spacing,
            sample_stride=8,
        )
        exact, _, _ = moving_breather_samples(coordinate, 2.0, 0.6)
        periodic_errors.append(float(np.sqrt(np.mean(np.square(evolution.field[-1] - exact)))))
        periodic_drifts.append(float(np.ptp(evolution.energy) / evolution.energy[0]))
    ledger.check("the exact nonlinear breather has second-order spatial-temporal convergence", periodic_errors[1] < periodic_errors[0] / 3.8 and periodic_errors[2] < periodic_errors[1] / 3.8 and periodic_errors[-1] < 2.0e-4)
    ledger.check("the periodic discrete-energy drift converges at second order", periodic_drifts[1] < periodic_drifts[0] / 3.8 and periodic_drifts[2] < periodic_drifts[1] / 3.8)

    coordinate = np.linspace(-20.0, 20.0, 256, endpoint=False)
    field0, velocity0, _ = moving_breather_samples(coordinate, 0.0, 0.6)
    leapfrog = evolve_periodic_sine_gordon_leapfrog(coordinate, field0, velocity0, 2.0, 0.03, sample_stride=7)
    adaptive_loose = evolve_periodic_sine_gordon_mol(
        coordinate,
        field0,
        velocity0,
        np.linspace(0.0, 2.0, 11),
        tolerances=SolverTolerances(rtol=1.0e-7, atol=1.0e-9, max_step=0.1),
    )
    adaptive_tight = evolve_periodic_sine_gordon_mol(
        coordinate,
        field0,
        velocity0,
        np.linspace(0.0, 2.0, 11),
        tolerances=SolverTolerances(rtol=1.0e-10, atol=1.0e-12, max_step=0.05),
    )
    ledger.check("DOP853 independently agrees with leapfrog on the nonlinear reference", np.sqrt(np.mean(np.square(leapfrog.field[-1] - adaptive_tight.field[-1]))) < 2.0e-4)
    ledger.check("adaptive-tolerance refinement leaves a resolved common trajectory", np.sqrt(np.mean(np.square(adaptive_loose.field[-1] - adaptive_tight.field[-1]))) < 2.0e-8 and np.ptp(adaptive_tight.energy) / adaptive_tight.energy[0] < 1.0e-9)

    grid_results: dict[int, dict[str, Any]] = {}
    for intervals in (600, 1200, 2400):
        full_plus, _ = _corrected_case(0.6, 1, intervals, 1.0, SOURCE_PHASES[0.6])
        full_minus, _ = _corrected_case(0.6, -1, intervals, 1.0, SOURCE_PHASES[0.6])
        _diag_plus_result, diagnostic_plus = _corrected_case(0.6, 1, intervals, 0.15, SOURCE_PHASES[0.6])
        _diag_minus_result, diagnostic_minus = _corrected_case(0.6, -1, intervals, 0.15, SOURCE_PHASES[0.6])
        grid_results[intervals] = {
            "dQ": full_plus.bulk_endpoint_charge_coordinate - full_minus.bulk_endpoint_charge_coordinate,
            "wq_plus": diagnostic_plus,
            "wq_minus": diagnostic_minus,
            "energy_residuals": (abs(full_plus.energy_balance_residual), abs(full_minus.energy_balance_residual)),
        }
    ledger.check("the corrected w=0.6 endpoint response converges on three fine grids", all(grid_results[level]["dQ"] < -1.0 for level in grid_results) and abs(grid_results[2400]["dQ"] - grid_results[1200]["dQ"]) < abs(grid_results[1200]["dQ"] - grid_results[600]["dQ"]))
    ledger.check("the corrected diagnostic correlations converge with opposite fine-grid signs", all(grid_results[level]["wq_plus"] > 0 and grid_results[level]["wq_minus"] < 0 for level in grid_results) and abs(grid_results[2400]["wq_plus"] - grid_results[1200]["wq_plus"]) < abs(grid_results[1200]["wq_plus"] - grid_results[600]["wq_plus"]) and abs(grid_results[2400]["wq_minus"] - grid_results[1200]["wq_minus"]) < abs(grid_results[1200]["wq_minus"] - grid_results[600]["wq_minus"]))
    ledger.check("driven energy-flux residuals decrease on fine-grid refinement", max(grid_results[1200]["energy_residuals"]) < max(grid_results[600]["energy_residuals"]) and max(grid_results[2400]["energy_residuals"]) < max(grid_results[1200]["energy_residuals"]))

    time_plus, time_wq_plus = _corrected_case(0.6, 1, 600, 1.0, SOURCE_PHASES[0.6], courant=0.2)
    time_minus, _ = _corrected_case(0.6, -1, 600, 1.0, SOURCE_PHASES[0.6], courant=0.2)
    _time_diag, time_diagnostic = _corrected_case(0.6, 1, 600, 0.15, SOURCE_PHASES[0.6], courant=0.2)
    time_dq = time_plus.bulk_endpoint_charge_coordinate - time_minus.bulk_endpoint_charge_coordinate
    ledger.check("independent timestep halving approaches the fine-grid response", abs(time_dq - grid_results[2400]["dQ"]) < abs(grid_results[600]["dQ"] - grid_results[2400]["dQ"]) and abs(time_diagnostic - grid_results[2400]["wq_plus"]) < abs(grid_results[600]["wq_plus"] - grid_results[2400]["wq_plus"]))

    domain_plus, _ = _corrected_case(0.6, 1, 700, 1.0, SOURCE_PHASES[0.6], domain_length=70.0)
    domain_minus, _ = _corrected_case(0.6, -1, 700, 1.0, SOURCE_PHASES[0.6], domain_length=70.0)
    domain_dq = domain_plus.bulk_endpoint_charge_coordinate - domain_minus.bulk_endpoint_charge_coordinate
    ledger.check("a same-spacing domain extension preserves the finite-time endpoint response", abs(domain_dq - grid_results[600]["dQ"]) < 1.0e-4)

    adaptive_results: dict[int, dict[str, Any]] = {}
    for intervals in (300, 600):
        full_plus, _ = _adaptive_case(1, intervals, 1.0)
        full_minus, _ = _adaptive_case(-1, intervals, 1.0)
        diagnostic_plus_result, diagnostic_plus = _adaptive_case(1, intervals, 0.15)
        diagnostic_minus_result, diagnostic_minus = _adaptive_case(-1, intervals, 0.15)
        adaptive_results[intervals] = {
            "dQ": full_plus.bulk_endpoint_charge_coordinate - full_minus.bulk_endpoint_charge_coordinate,
            "wq_plus": diagnostic_plus,
            "wq_minus": diagnostic_minus,
            "energy_residuals": (
                abs(diagnostic_plus_result.energy_balance_residual),
                abs(diagnostic_minus_result.energy_balance_residual),
            ),
        }
    ledger.check("adaptive method-of-lines independently preserves the calibrated response signs", all(adaptive_results[level]["dQ"] < -1.0 and adaptive_results[level]["wq_plus"] > 0 and adaptive_results[level]["wq_minus"] < 0 for level in adaptive_results))
    ledger.check("adaptive driven energy-flux residual decreases with spatial refinement", max(adaptive_results[600]["energy_residuals"]) < max(adaptive_results[300]["energy_residuals"]))

    common_phase = SOURCE_PHASES[0.6]
    w08_plus, _ = _corrected_case(0.8, 1, 600, 1.0, common_phase)
    w08_minus, _ = _corrected_case(0.8, -1, 600, 1.0, common_phase)
    common_phase_dq_w08 = w08_plus.bulk_endpoint_charge_coordinate - w08_minus.bulk_endpoint_charge_coordinate
    ledger.check("a common-drive phase counterexample reverses the alleged amplitude-sweep sign", grid_results[600]["dQ"] < 0 and common_phase_dq_w08 > 0)

    parameters = _source_parameters(0.6)
    drive_plus = gaussian_sine_neumann_drive(parameters["force_amplitude"], 0.6, parameters["impact_time"], parameters["interaction_width"], common_phase)
    phase_shifted_plus = gaussian_sine_neumann_drive(parameters["force_amplitude"], 0.6, parameters["impact_time"], parameters["interaction_width"], common_phase + np.pi)
    drive_minus = gaussian_sine_neumann_drive(-parameters["force_amplitude"], 0.6, parameters["impact_time"], parameters["interaction_width"], common_phase)
    sample = np.linspace(parameters["impact_time"] - 2.0, parameters["impact_time"] + 2.0, 101)
    ledger.check("a pi phase shift exactly relabels the two declared eps drives", np.allclose([phase_shifted_plus(value) for value in sample], [drive_minus(value) for value in sample], rtol=0.0, atol=2.0e-15) and not np.allclose([drive_plus(value) for value in sample], [drive_minus(value) for value in sample]))
    ledger.check("fractional endpoint coordinates do not satisfy the integer-vacuum conclusion", abs(adapter_result["observations"]["dQ"]["0.2"] - round(adapter_result["observations"]["dQ"]["0.2"])) > 0.1)
    ledger.check("the surviving numerical result is only a tuned IBVP response", queue_entry["candidate_dependencies"] == ["G1", "G2", "G3", "NC1", "NC3"] and all(item not in {"C-SG-001", "C-SG-011", "C-SG-013"} for item in queue_entry["candidate_dependencies"]))

    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
