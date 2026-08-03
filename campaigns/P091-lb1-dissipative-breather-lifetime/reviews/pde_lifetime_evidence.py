"""Damped-PDE refinement evidence for the P091 adiabatic lifetime audit."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from substrate_framework.numerics import SolverTolerances
from substrate_framework.sine_gordon_1d import (
    BulkDrivenSineGordonEvolution,
    evolve_bulk_driven_sine_gordon_leapfrog,
    evolve_bulk_driven_sine_gordon_mol,
)
from substrate_framework.verification import CheckLedger


OMEGA_INITIAL = 1.0 / np.sqrt(2.0)
GAMMA = 0.02
FINAL_TIME = 50.0
SAMPLE_INTERVAL = 0.25
CORE_RADIUS = 40.0


@dataclass(frozen=True)
class Metrics:
    method: str
    half_domain: float
    spatial_step: float
    damping_rate: float
    final_time: float
    initial_energy: float
    final_energy: float
    predicted_final_energy: float
    normalized_energy_rms: float
    normalized_action_rms: float
    frozen_form_factor_energy_rms: float
    relative_balance_residual: float


def initial_data(
    half_domain: float,
    spatial_step: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the exact phase-zero breather data on an inclusive grid."""

    point_count = int(round(2.0 * half_domain / spatial_step)) + 1
    coordinate = np.linspace(-half_domain, half_domain, point_count)
    inverse_width = np.sqrt(1.0 - OMEGA_INITIAL**2)
    field = np.zeros_like(coordinate)
    velocity = 4.0 * inverse_width / np.cosh(inverse_width * coordinate)
    velocity[[0, -1]] = 0.0
    return coordinate, field, velocity


def reduced_energy(time: np.ndarray, gamma: float = GAMMA) -> np.ndarray:
    """Return the conditional phase-averaged family energy."""

    theta_initial = np.arccos(OMEGA_INITIAL)
    return 16.0 * np.sin(theta_initial * np.exp(-gamma * time))


def action_from_energy(energy: np.ndarray) -> np.ndarray:
    """Invert the accepted family energy map on its open branch."""

    return 16.0 * np.arcsin(np.clip(energy / 16.0, 0.0, 1.0))


def metrics(
    result: BulkDrivenSineGordonEvolution,
    half_domain: float,
    damping_rate: float,
) -> Metrics:
    """Compare a PDE trajectory with the preregistered reduced observables."""

    expected_energy = reduced_energy(result.time, damping_rate)
    measured_action = action_from_energy(result.total_energy)
    expected_action = 16.0 * np.arccos(OMEGA_INITIAL) * np.exp(
        -damping_rate * result.time
    )
    initial_energy = float(result.initial_energy)
    initial_form_factor = np.pi / 4.0
    frozen_form_factor_energy = initial_energy * np.exp(
        -damping_rate * initial_form_factor * result.time
    )
    return Metrics(
        method=result.method,
        half_domain=half_domain,
        spatial_step=result.spatial_step,
        damping_rate=damping_rate,
        final_time=float(result.time[-1]),
        initial_energy=initial_energy,
        final_energy=float(result.total_energy[-1]),
        predicted_final_energy=float(expected_energy[-1]),
        normalized_energy_rms=float(
            np.sqrt(np.mean(np.square(result.total_energy - expected_energy)))
            / initial_energy
        ),
        normalized_action_rms=float(
            np.sqrt(np.mean(np.square(measured_action - expected_action)))
            / expected_action[0]
        ),
        frozen_form_factor_energy_rms=float(
            np.sqrt(
                np.mean(
                    np.square(result.total_energy - frozen_form_factor_energy)
                )
            )
            / initial_energy
        ),
        relative_balance_residual=abs(result.energy_balance_residual) / initial_energy,
    )


def leapfrog_run(
    half_domain: float,
    spatial_step: float,
    damping_rate: float = GAMMA,
    final_time: float = FINAL_TIME,
) -> Metrics:
    coordinate, field, velocity = initial_data(half_domain, spatial_step)
    result = evolve_bulk_driven_sine_gordon_leapfrog(
        coordinate,
        field,
        velocity,
        lambda _time: np.zeros_like(coordinate),
        np.full_like(coordinate, damping_rate),
        final_time,
        spatial_step / 2.0,
        core_radius=CORE_RADIUS,
        sample_interval=SAMPLE_INTERVAL,
    )
    return metrics(result, half_domain, damping_rate)


def mol_run(
    half_domain: float,
    spatial_step: float,
    damping_rate: float = GAMMA,
    final_time: float = FINAL_TIME,
) -> Metrics:
    coordinate, field, velocity = initial_data(half_domain, spatial_step)
    sample_times = np.linspace(
        0.0,
        final_time,
        int(round(final_time / SAMPLE_INTERVAL)) + 1,
    )
    result = evolve_bulk_driven_sine_gordon_mol(
        coordinate,
        field,
        velocity,
        lambda _time: np.zeros_like(coordinate),
        np.full_like(coordinate, damping_rate),
        sample_times,
        core_radius=CORE_RADIUS,
        tolerances=SolverTolerances(rtol=1e-9, atol=1e-11),
        method="DOP853",
    )
    return metrics(result, half_domain, damping_rate)


def main() -> int:
    configurations = (
        ("leapfrog", 60.0, 0.2, 0.02, 50.0),
        ("leapfrog", 60.0, 0.1, 0.02, 50.0),
        ("leapfrog", 60.0, 0.05, 0.02, 50.0),
        ("leapfrog", 80.0, 0.1, 0.02, 50.0),
        ("DOP853", 60.0, 0.2, 0.02, 50.0),
        ("leapfrog", 60.0, 0.1, 0.01, 100.0),
        ("leapfrog", 60.0, 0.1, 0.0, 50.0),
    )
    results: list[Metrics] = []
    for method, half_domain, spatial_step, damping_rate, final_time in configurations:
        result = (
            leapfrog_run(half_domain, spatial_step, damping_rate, final_time)
            if method == "leapfrog"
            else mol_run(half_domain, spatial_step, damping_rate, final_time)
        )
        print(result)
        results.append(result)

    coarse, medium, fine, large_domain, dop853, slower, lossless = results
    checks = CheckLedger("P091-PDE")
    exact_initial_energy = 8.0 * np.sqrt(2.0)
    checks.check(
        "phase-zero grids reproduce the exact initial breather energy",
        all(abs(item.initial_energy - exact_initial_energy) < 1e-12 for item in results),
    )
    checks.check(
        "all damped trajectories meet the preregistered five-percent energy ceiling",
        all(item.normalized_energy_rms < 0.05 for item in results if item.damping_rate > 0.0),
    )
    checks.check(
        "all damped trajectories meet the preregistered five-percent action ceiling",
        all(item.normalized_action_rms < 0.05 for item in results if item.damping_rate > 0.0),
    )
    checks.check(
        "leapfrog energy-ledger residual refines at second order",
        medium.relative_balance_residual < coarse.relative_balance_residual / 3.0
        and fine.relative_balance_residual < medium.relative_balance_residual / 3.0,
    )
    checks.check(
        "physical reduction discrepancy stabilizes under spatial refinement",
        fine.normalized_energy_rms < medium.normalized_energy_rms
        < coarse.normalized_energy_rms,
    )
    checks.check(
        "larger domain leaves the measured trajectory unchanged",
        abs(large_domain.final_energy - medium.final_energy) / exact_initial_energy
        < 1e-10
        and abs(
            large_domain.normalized_energy_rms - medium.normalized_energy_rms
        )
        < 1e-12,
    )
    checks.check(
        "independent DOP853 and refined leapfrog endpoints agree",
        abs(dop853.final_energy - fine.final_energy) / exact_initial_energy < 2e-4,
    )
    checks.check(
        "adiabatic error improves when damping is halved at equal slow time",
        slower.normalized_energy_rms < fine.normalized_energy_rms / 1.9
        and slower.normalized_action_rms < fine.normalized_action_rms / 1.9,
    )
    checks.check(
        "lossless soluble control conserves energy within numerical resolution",
        lossless.normalized_energy_rms < 1e-3
        and lossless.relative_balance_residual < 1e-3,
    )
    checks.mutation_sensitive(
        "evolving nonlinear action law beats the frozen-initial-D source law",
        lambda item: item.normalized_energy_rms
        < item.frozen_form_factor_energy_rms / 4.0,
        fine,
        (
            Metrics(
                method=fine.method,
                half_domain=fine.half_domain,
                spatial_step=fine.spatial_step,
                damping_rate=fine.damping_rate,
                final_time=fine.final_time,
                initial_energy=fine.initial_energy,
                final_energy=fine.final_energy,
                predicted_final_energy=fine.predicted_final_energy,
                normalized_energy_rms=fine.frozen_form_factor_energy_rms,
                normalized_action_rms=fine.normalized_action_rms,
                frozen_form_factor_energy_rms=fine.normalized_energy_rms,
                relative_balance_residual=fine.relative_balance_residual,
            ),
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
