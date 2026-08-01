#!/usr/bin/env python3
"""Independent transformed-field review of P044's radial IVP solver."""

from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.integrate import simpson, solve_ivp

from substrate_framework.radial_sine_gordon import evolve_radial_sine_gordon_leapfrog
from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P044-INDEPENDENT")
    radius_symbol = sp.symbols("r", positive=True, real=True)
    u, u_r, u_rr, u_tt = sp.symbols("u u_r u_rr u_tt", real=True)
    v_rr = 2 * u_r + radius_symbol * u_rr
    v_tt = radius_symbol * u_tt
    ledger.check(
        "v=r*u removes the radial first-derivative singularity exactly",
        sp.simplify(
            v_tt
            - v_rr
            + radius_symbol * sp.sin(u)
            - radius_symbol
            * (u_tt - u_rr - 2 * u_r / radius_symbol + sp.sin(u))
        )
        == 0,
    )

    spacing = 0.2
    outer_radius = 80.0
    final_time = 60.0
    radius = np.arange(int(round(outer_radius / spacing)) + 1) * spacing
    interior_radius = radius[1:-1]
    interior_size = interior_radius.size
    field0 = 3.0 * np.exp(-np.square(radius / 4.0))
    transformed0 = interior_radius * field0[1:-1]
    state0 = np.concatenate((transformed0, np.zeros(interior_size)))
    sample_time = np.linspace(0.0, final_time, 301)

    def transformed_rhs(_time: float, state: np.ndarray) -> np.ndarray:
        transformed = np.zeros_like(radius)
        transformed[1:-1] = state[:interior_size]
        velocity = state[interior_size:]
        second = (
            transformed[2:] - 2.0 * transformed[1:-1] + transformed[:-2]
        ) / spacing**2
        acceleration = second - interior_radius * np.sin(
            transformed[1:-1] / interior_radius
        )
        return np.concatenate((velocity, acceleration))

    solution = solve_ivp(
        transformed_rhs,
        (0.0, final_time),
        state0,
        t_eval=sample_time,
        method="DOP853",
        rtol=2.0e-7,
        atol=2.0e-9,
        max_step=0.1,
    )
    ledger.check(
        "the independent transformed-field integration exits successfully",
        solution.success
        and solution.nfev > 0
        and np.all(np.isfinite(solution.y)),
        solution.message,
    )

    independent_center: list[float] = []
    independent_core: list[float] = []
    independent_total: list[float] = []
    core = radius <= 20.0
    for index in range(solution.t.size):
        transformed = np.zeros_like(radius)
        transformed_velocity = np.zeros_like(radius)
        transformed[1:-1] = solution.y[:interior_size, index]
        transformed_velocity[1:-1] = solution.y[interior_size:, index]
        field = np.zeros_like(radius)
        velocity = np.zeros_like(radius)
        field[1:] = transformed[1:] / radius[1:]
        velocity[1:] = transformed_velocity[1:] / radius[1:]
        field[0] = (4.0 * field[1] - field[2]) / 3.0
        velocity[0] = (4.0 * velocity[1] - velocity[2]) / 3.0
        gradient = np.empty_like(field)
        gradient[0] = 0.0
        gradient[1:-1] = (field[2:] - field[:-2]) / (2.0 * spacing)
        gradient[-1] = (3.0 * field[-1] - 4.0 * field[-2] + field[-3]) / (
            2.0 * spacing
        )
        density = (
            np.square(velocity) / 2.0
            + np.square(gradient) / 2.0
            + 1.0
            - np.cos(field)
        )
        shell = 4.0 * np.pi * np.square(radius) * density
        independent_center.append(float(field[0]))
        independent_core.append(float(simpson(shell[core], x=radius[core])))
        independent_total.append(float(simpson(shell, x=radius)))

    primary = evolve_radial_sine_gordon_leapfrog(
        amplitude=3.0,
        width=4.0,
        spacing=spacing,
        outer_radius=outer_radius,
        final_time=final_time,
        core_radius=20.0,
        sample_interval=0.2,
        courant=0.4,
    )
    selected = (solution.t >= primary.time[0]) & (solution.t <= primary.time[-1])
    comparison_time = solution.t[selected]
    primary_center = np.interp(comparison_time, primary.time, primary.center)
    primary_core = np.interp(comparison_time, primary.time, primary.core_energy)
    reviewed_center = np.asarray(independent_center)[selected]
    reviewed_core = np.asarray(independent_core)[selected]
    relative_center_rms = float(
        np.sqrt(np.mean(np.square(primary_center - reviewed_center)))
        / np.std(reviewed_center)
    )
    relative_core_max = float(
        np.max(np.abs(primary_core - reviewed_core)) / np.mean(reviewed_core)
    )
    ledger.check(
        "transformed-field and direct-radial center trajectories agree",
        relative_center_rms < 0.02,
        f"relative RMS={relative_center_rms:.6g}",
    )
    ledger.check(
        "independent Simpson core energy agrees with canonical diagnostics",
        relative_core_max < 0.005,
        f"relative maximum={relative_core_max:.6g}",
    )
    energy_variation = float(
        np.ptp(independent_total) / np.asarray(independent_total)[0]
    )
    ledger.check(
        "the transformed-field route independently controls closed-box energy",
        energy_variation < 0.003,
        f"relative range={energy_variation:.6g}",
    )

    def transform_coefficient_predicate(candidate: object) -> bool:
        coefficient = sp.sympify(candidate)
        mutated = (
            v_tt
            - v_rr
            + radius_symbol * sp.sin(u)
            - radius_symbol
            * (u_tt - u_rr - coefficient * u_r / radius_symbol + sp.sin(u))
        )
        return sp.simplify(mutated) == 0

    ledger.mutation_sensitive(
        "transformed-field geometric coefficient",
        transform_coefficient_predicate,
        2,
        [0, 1, 3],
    )
    print(
        "P044 independent metrics: "
        f"nfev={solution.nfev}, center_relative_rms={relative_center_rms:.9e}, "
        f"core_relative_max={relative_core_max:.9e}, "
        f"energy_relative_range={energy_variation:.9e}"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
