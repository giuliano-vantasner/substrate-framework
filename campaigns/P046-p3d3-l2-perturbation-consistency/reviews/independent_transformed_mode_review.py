#!/usr/bin/env python3
"""Independent transformed-field DOP853 review of P046's l=2 evolution."""

from __future__ import annotations

import numpy as np
import sympy as sp

from substrate_framework.numerics import (
    SolverTolerances,
    solve_method_of_lines,
    trapezoid_integral,
)
from substrate_framework.radial_sine_gordon import gaussian_radial_seed
from substrate_framework.sine_gordon_l_modes import (
    evolve_radial_background_with_linearized_mode,
    linearized_p2_energy_triple_stf,
    regular_l_mode_gaussian_seed,
)
from substrate_framework.verification import CheckLedger


def relative_radial_error(
    first: np.ndarray, second: np.ndarray, radius: np.ndarray
) -> float:
    """Relative spherical L2 difference between radial scalar fields."""

    return float(
        np.sqrt(
            trapezoid_integral(np.square(first - second) * radius**2, radius)
            / trapezoid_integral(np.square(second) * radius**2, radius)
        )
    )


def relative_transformed_error(
    first: np.ndarray, second: np.ndarray, radius: np.ndarray
) -> float:
    """Relative L2 difference of the transformed modes r*psi."""

    return float(
        np.sqrt(
            trapezoid_integral(np.square(radius * (first - second)), radius)
            / trapezoid_integral(np.square(radius * second), radius)
        )
    )


def main() -> int:
    ledger = CheckLedger("P046-INDEPENDENT")

    radius_symbol = sp.symbols("r", positive=True, real=True)
    background = sp.Function("P")(radius_symbol)
    mode = sp.Function("psi")(radius_symbol)
    symbolic_transformed_background = radius_symbol * background
    symbolic_transformed_mode = radius_symbol * mode
    ledger.check(
        "the independent v=r*P transform removes the radial background first derivative",
        sp.simplify(
            sp.diff(symbolic_transformed_background, radius_symbol, 2)
            - radius_symbol
            * (
                sp.diff(background, radius_symbol, 2)
                + 2 * sp.diff(background, radius_symbol) / radius_symbol
            )
        )
        == 0,
    )
    ledger.check(
        "the independent z=r*psi transform retains exactly the l=2 barrier six",
        sp.simplify(
            sp.diff(symbolic_transformed_mode, radius_symbol, 2)
            - 6 * symbolic_transformed_mode / radius_symbol**2
            - radius_symbol
            * (
                sp.diff(mode, radius_symbol, 2)
                + 2 * sp.diff(mode, radius_symbol) / radius_symbol
                - 6 * mode / radius_symbol**2
            )
        )
        == 0,
    )

    spacing = 0.2
    outer_radius = 60.0
    final_time = 20.0
    radius = spacing * np.arange(int(round(outer_radius / spacing)) + 1)
    interior_radius = radius[1:-1]
    interior_size = interior_radius.size
    background_initial = gaussian_radial_seed(radius, 3.0, 4.0)
    mode_initial = regular_l_mode_gaussian_seed(
        radius, ell=2, amplitude=0.2, width=4.0
    )
    transformed_background_initial = radius * background_initial
    transformed_mode_initial = radius * mode_initial
    initial_state = np.concatenate(
        (
            transformed_background_initial[1:-1],
            transformed_mode_initial[1:-1],
            np.zeros(interior_size),
            np.zeros(interior_size),
        )
    )

    def rhs(_time: float, state: np.ndarray) -> np.ndarray:
        transformed_background = np.zeros_like(radius)
        transformed_mode = np.zeros_like(radius)
        transformed_background[1:-1] = state[:interior_size]
        transformed_mode[1:-1] = state[interior_size : 2 * interior_size]
        background_acceleration = (
            transformed_background[2:]
            - 2.0 * transformed_background[1:-1]
            + transformed_background[:-2]
        ) / spacing**2 - interior_radius * np.sin(
            transformed_background[1:-1] / interior_radius
        )
        mode_acceleration = (
            (
                transformed_mode[2:]
                - 2.0 * transformed_mode[1:-1]
                + transformed_mode[:-2]
            )
            / spacing**2
            - 6.0 * transformed_mode[1:-1] / interior_radius**2
            - np.cos(transformed_background[1:-1] / interior_radius)
            * transformed_mode[1:-1]
        )
        return np.concatenate(
            (
                state[2 * interior_size : 3 * interior_size],
                state[3 * interior_size :],
                background_acceleration,
                mode_acceleration,
            )
        )

    independent = solve_method_of_lines(
        rhs,
        (0.0, final_time),
        initial_state,
        sample_times=np.array([0.0, final_time]),
        method="DOP853",
        tolerances=SolverTolerances(rtol=2.0e-8, atol=2.0e-10, max_step=0.1),
    )
    ledger.check(
        "the independent transformed-field DOP853 integration exits cleanly",
        independent.method == "DOP853"
        and independent.function_evaluations > 0
        and np.all(np.isfinite(independent.state)),
    )

    final_state = independent.state[:, -1]
    numeric_transformed_background = np.zeros_like(radius)
    numeric_transformed_mode = np.zeros_like(radius)
    transformed_background_velocity = np.zeros_like(radius)
    transformed_mode_velocity = np.zeros_like(radius)
    numeric_transformed_background[1:-1] = final_state[:interior_size]
    numeric_transformed_mode[1:-1] = final_state[interior_size : 2 * interior_size]
    transformed_background_velocity[1:-1] = final_state[
        2 * interior_size : 3 * interior_size
    ]
    transformed_mode_velocity[1:-1] = final_state[3 * interior_size :]

    reviewed_background = np.zeros_like(radius)
    reviewed_mode = np.zeros_like(radius)
    reviewed_background_velocity = np.zeros_like(radius)
    reviewed_mode_velocity = np.zeros_like(radius)
    reviewed_background[1:] = numeric_transformed_background[1:] / radius[1:]
    reviewed_mode[1:] = numeric_transformed_mode[1:] / radius[1:]
    reviewed_background_velocity[1:] = transformed_background_velocity[1:] / radius[1:]
    reviewed_mode_velocity[1:] = transformed_mode_velocity[1:] / radius[1:]
    reviewed_background[0] = (4.0 * reviewed_background[1] - reviewed_background[2]) / 3.0
    reviewed_background_velocity[0] = (
        4.0 * reviewed_background_velocity[1] - reviewed_background_velocity[2]
    ) / 3.0
    ledger.check(
        "the independent transformed solution preserves regular l=2 origin behavior",
        reviewed_mode[0] == 0.0
        and reviewed_mode_velocity[0] == 0.0
        and np.all(np.isfinite(reviewed_mode[1:4] / radius[1:4] ** 2)),
    )

    canonical = evolve_radial_background_with_linearized_mode(
        background_initial,
        mode_initial,
        spacing=spacing,
        final_time=final_time,
        ell=2,
        courant=0.4,
        sample_interval=0.4,
    )
    background_error = relative_radial_error(
        canonical.final_background, reviewed_background, radius
    )
    mode_error = relative_transformed_error(
        canonical.final_mode, reviewed_mode, radius
    )
    ledger.check(
        "DOP853 and velocity-Verlet background fields agree at the declared coarse mesh",
        background_error < 0.03,
        f"relative radial L2={background_error:.9g}",
    )
    ledger.check(
        "DOP853 and velocity-Verlet regular l=2 profiles agree",
        mode_error < 0.015,
        f"relative transformed L2={mode_error:.9g}",
    )
    reviewed_tensor = linearized_p2_energy_triple_stf(
        reviewed_background,
        reviewed_background_velocity,
        reviewed_mode,
        reviewed_mode_velocity,
        radius,
    )
    canonical_qzz = canonical.p2_triple_stf_zz_coefficient[-1]
    qzz_error = abs(canonical_qzz - reviewed_tensor[2, 2]) / abs(reviewed_tensor[2, 2])
    ledger.check(
        "the independent evolution reproduces the nonzero first-order STF moment",
        abs(reviewed_tensor[2, 2]) > 300.0 and qzz_error < 0.003,
        f"Qzz={reviewed_tensor[2, 2]:.9g}, relative difference={qzz_error:.9g}",
    )

    def barrier_predicate(candidate: object) -> bool:
        coefficient = sp.sympify(candidate)
        expression = (
            sp.diff(symbolic_transformed_mode, radius_symbol, 2)
            - coefficient * symbolic_transformed_mode / radius_symbol**2
            - radius_symbol
            * (
                sp.diff(mode, radius_symbol, 2)
                + 2 * sp.diff(mode, radius_symbol) / radius_symbol
                - 6 * mode / radius_symbol**2
            )
        )
        return sp.simplify(expression) == 0

    ledger.mutation_sensitive(
        "independently rederived l=2 barrier",
        barrier_predicate,
        6,
        [0, 2, 12],
    )
    print(
        "P046 independent metrics: "
        f"nfev={independent.function_evaluations}, "
        f"background_relative_l2={background_error:.9e}, "
        f"mode_relative_l2={mode_error:.9e}, "
        f"Qzz={reviewed_tensor[2, 2]:.9e}, Qzz_relative_error={qzz_error:.9e}"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
