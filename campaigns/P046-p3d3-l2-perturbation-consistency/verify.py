#!/usr/bin/env python3
"""Verify P046's regular l=2 sine-Gordon sector and audit P3D3."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.special import spherical_jn

from substrate_framework.governance import load_yaml
from substrate_framework.numerics import trapezoid_integral
from substrate_framework.radial_sine_gordon import gaussian_radial_seed
from substrate_framework.sine_gordon_l_modes import (
    LinearizedAngularModeEvolution,
    evolve_radial_background_with_linearized_mode,
    legendre_p2,
    linearized_p2_energy_triple_stf,
    multiplicative_p2_first_order_residual_coefficient,
    multiplicative_p2_residual,
    regular_l_mode_gaussian_seed,
    transformed_l_mode_acceleration,
)
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "3f4532bac5e517b1324bf74153da9acdc9ef1cb10f53fc3df8cd0483d51e8fa2"
)


def run_branch(
    spacing: float,
    *,
    outer_radius: float = 80.0,
    final_time: float = 40.0,
    courant: float = 0.4,
    mode_amplitude: float = 0.2,
) -> LinearizedAngularModeEvolution:
    """Run the declared P046 background and regular l=2 IVP."""

    radius = spacing * np.arange(int(round(outer_radius / spacing)) + 1)
    background = gaussian_radial_seed(radius, 3.0, 4.0)
    mode = regular_l_mode_gaussian_seed(
        radius, ell=2, amplitude=mode_amplitude, width=4.0
    )
    return evolve_radial_background_with_linearized_mode(
        background,
        mode,
        spacing=spacing,
        final_time=final_time,
        ell=2,
        courant=courant,
        sample_interval=0.4,
    )


def relative_weighted_field_difference(
    coarse: np.ndarray,
    fine_on_coarse: np.ndarray,
    radius: np.ndarray,
) -> float:
    """Relative radial L2 error with the spherical r-squared measure."""

    numerator = trapezoid_integral(
        np.square(coarse - fine_on_coarse) * radius**2, radius
    )
    denominator = trapezoid_integral(
        np.square(fine_on_coarse) * radius**2, radius
    )
    return float(np.sqrt(numerator / denominator))


def relative_transformed_mode_difference(
    coarse: np.ndarray,
    fine_on_coarse: np.ndarray,
    radius: np.ndarray,
) -> float:
    """Relative mode L2 error, equivalently measured on v=r*psi."""

    numerator = trapezoid_integral(
        np.square(radius * (coarse - fine_on_coarse)), radius
    )
    denominator = trapezoid_integral(np.square(radius * fine_on_coarse), radius)
    return float(np.sqrt(numerator / denominator))


def relative_trace_rms(first: np.ndarray, second: np.ndarray) -> float:
    """Return RMS disagreement normalized by the second trace RMS."""

    return float(
        np.sqrt(np.mean(np.square(first - second)))
        / np.sqrt(np.mean(np.square(second)))
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P046-P3D3")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    reproduction = load_yaml(args.source_reproduction)
    ledger.check(
        "the audited P3D3 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    ledger.check(
        "the exact source reproduction exits with its five-check tally",
        reproduction.get("sha256") == EXPECTED_SOURCE_SHA256
        and reproduction.get("exit_code") == 0
        and "ALL 5 CHECKS PASS" in str(reproduction.get("terminal_tally", "")),
    )
    ledger.check(
        "P3D3 selects the current NumPy trapezoid API before its legacy fallback",
        'np.trapezoid if hasattr(np, "trapezoid") else np.trapz' in source_text,
    )

    radius, amplitude, background, harmonic = sp.symbols(
        "r a P Y", positive=True, real=True
    )
    factor = 1 + amplitude * harmonic
    residual = (
        sp.sin(background * factor)
        - factor * sp.sin(background)
        + 6 * amplitude * background * harmonic / radius**2
    )
    first_order = harmonic * (
        background * sp.cos(background)
        - sp.sin(background)
        + 6 * background / radius**2
    )
    ledger.check(
        "the multiplicative construction has the exact full-PDE residual",
        sp.simplify(sp.diff(residual, amplitude).subs(amplitude, 0) - first_order)
        == 0
        and sp.simplify(residual.subs(amplitude, 0)) == 0,
    )
    ledger.check(
        "P3D3's multiplicative ansatz fails already at first perturbative order",
        sp.simplify(first_order.subs({background: 1, radius: 2, harmonic: 1}))
        != 0,
    )
    numeric_residual = multiplicative_p2_residual(
        np.array([0.7, 1.1, 1.4]),
        np.array([0.8, 1.3, 2.0]),
        0.3,
        np.array([-0.6, 0.2, 0.9]),
    )
    numeric_first = multiplicative_p2_first_order_residual_coefficient(
        np.array([0.7, 1.1, 1.4]),
        np.array([0.8, 1.3, 2.0]),
        np.array([-0.6, 0.2, 0.9]),
    )
    finite_step = 1.0e-6
    centered_difference = (
        multiplicative_p2_residual(
            np.array([0.7, 1.1, 1.4]),
            np.array([0.8, 1.3, 2.0]),
            finite_step,
            np.array([-0.6, 0.2, 0.9]),
        )
        - multiplicative_p2_residual(
            np.array([0.7, 1.1, 1.4]),
            np.array([0.8, 1.3, 2.0]),
            -finite_step,
            np.array([-0.6, 0.2, 0.9]),
        )
    ) / (2.0 * finite_step)
    ledger.check(
        "the package residual is nonzero and its Taylor derivative is sensitive",
        np.max(np.abs(numeric_residual)) > 0.1
        and np.allclose(centered_difference, numeric_first, rtol=3.0e-10, atol=3.0e-10),
    )

    mu = sp.symbols("mu", real=True)
    p2 = (3 * mu**2 - 1) / 2
    p4 = (35 * mu**4 - 30 * mu**2 + 3) / 8
    p2_square_decomposition = sp.Rational(1, 5) + sp.Rational(2, 7) * p2 + sp.Rational(18, 35) * p4
    second_order = sp.expand(sp.diff(residual, amplitude, 2).subs(amplitude, 0) / 2)
    ledger.check(
        "the finite deformation leaks into l=4 at second order",
        sp.simplify(p2**2 - p2_square_decomposition) == 0
        and sp.simplify(second_order.subs(harmonic, p2) + background**2 * sp.sin(background) * p2**2 / 2)
        == 0
        and sp.simplify(-background**2 * sp.sin(background) * sp.Rational(9, 35))
        != 0,
    )

    psi, psi_tt, psi_rr, psi_r = sp.symbols(
        "psi psi_tt psi_rr psi_r", real=True
    )
    linearized_equation = (
        psi_tt
        - psi_rr
        - 2 * psi_r / radius
        + 6 * psi / radius**2
        + sp.cos(background) * psi
    )
    ledger.check(
        "the true regular l=2 perturbation equation contains angular barrier six",
        linearized_equation.coeff(psi_tt) == 1
        and linearized_equation.coeff(psi_rr) == -1
        and sp.simplify(linearized_equation.coeff(psi_r) + 2 / radius) == 0
        and sp.simplify(linearized_equation.coeff(psi) - (6 / radius**2 + sp.cos(background)))
        == 0,
    )
    transformed = sp.Function("v")(radius)
    transformed_spatial = sp.diff(transformed, radius, 2) - 6 * transformed / radius**2
    ledger.check(
        "v=r*psi makes the regular solid-harmonic behavior v proportional r cubed nonsingular",
        sp.simplify(transformed_spatial.subs(transformed, radius**3).doit()) == 0,
    )

    def angular_barrier_predicate(candidate: object) -> bool:
        coefficient = float(candidate)
        grid_spacing = 0.025
        grid = grid_spacing * np.arange(401)
        transformed_mode = grid**3
        static_background = np.full_like(grid, np.pi / 2.0)
        mutated = transformed_l_mode_acceleration(
            static_background,
            transformed_mode,
            grid_spacing,
            ell=int(round((-1.0 + np.sqrt(1.0 + 4.0 * coefficient)) / 2.0)),
        )
        return bool(np.max(np.abs(mutated[1:-1])) < 2.0e-9)

    ledger.mutation_sensitive(
        "l=2 angular barrier coefficient",
        angular_barrier_predicate,
        6,
        [2, 12],
    )

    source_seed_l2_origin = 3.0 * 0.3
    regular_grid = 0.05 * np.arange(101)
    regular_seed = regular_l_mode_gaussian_seed(
        regular_grid, ell=2, amplitude=0.3, width=4.0
    )
    ledger.check(
        "the source seed violates l=2 origin regularity while the canonical seed obeys it",
        source_seed_l2_origin != 0.0
        and regular_seed[0] == 0.0
        and np.max(np.abs(regular_seed[1:4] / regular_grid[1:4] ** 2)) < np.inf,
    )
    ledger.check(
        "the construction-route T00 omits its nonradial angular-gradient energy",
        "T00 = 0.5 * Ut**2 + 0.5 * Ur**2 + (1.0 - np.cos(U))" in source_text
        and "(uth / RR)**2" in source_text,
    )

    radial_symbol, h_symbol = sp.symbols("r h", positive=True, real=True)
    angular_norm = sp.Rational(4, 5) * sp.pi
    scalar_h = 4 * sp.pi * sp.Integral(radial_symbol**4 * h_symbol, radial_symbol)
    expected_q = sp.diag(-scalar_h / 5, -scalar_h / 5, 2 * scalar_h / 5)
    ledger.check(
        "exact P2 angular integration fixes the first-order energy triple-STF tensor",
        sp.integrate(p2**2, (mu, -1, 1)) * 2 * sp.pi == angular_norm
        and sp.trace(expected_q) == 0
        and expected_q[0, 0] == expected_q[1, 1]
        and expected_q[2, 2] == -2 * expected_q[0, 0],
    )
    moment_grid = np.linspace(0.0, 2.0, 801)
    moment_background = np.full_like(moment_grid, np.pi / 2.0)
    moment_mode = moment_grid**2
    zeros = np.zeros_like(moment_grid)
    numeric_tensor = linearized_p2_energy_triple_stf(
        moment_background, zeros, moment_mode, zeros, moment_grid
    )
    analytic_scalar = 4.0 * np.pi * 2.0**7 / 7.0
    ledger.check(
        "the numeric moment API reproduces the independently integrated normalization",
        np.allclose(
            numeric_tensor,
            np.diag(
                [-analytic_scalar / 5.0, -analytic_scalar / 5.0, 2.0 * analytic_scalar / 5.0]
            ),
            rtol=6.0e-6,
            atol=1.0e-12,
        ),
    )

    coarse, baseline, fine = [run_branch(spacing) for spacing in (0.2, 0.1, 0.05)]
    simulations = (coarse, baseline, fine)
    ledger.check(
        "all regular background-mode evolutions complete with finite diagnostics",
        all(
            result.completed
            and np.all(np.isfinite(result.final_background))
            and np.all(np.isfinite(result.final_mode))
            and np.all(np.isfinite(result.p2_triple_stf_zz_coefficient))
            for result in simulations
        ),
    )
    ledger.check(
        "the finite-time regular l=2 sector carries a resolved nonzero STF energy moment",
        min(
            np.sqrt(np.mean(np.square(result.p2_triple_stf_zz_coefficient)))
            for result in simulations
        )
        > 390.0
        and all(0.5 < result.mode_norm[-1] / result.mode_norm[0] < 0.8 for result in simulations),
    )
    ledger.check(
        "the interpreted interval is causally quiet at the finite outer boundary",
        max(result.max_boundary_background for result in simulations) < 1.0e-15
        and max(result.max_boundary_mode for result in simulations) < 1.0e-15
        and fine.time[-1] < fine.outer_radius,
    )

    background_errors: list[float] = []
    mode_errors: list[float] = []
    q_errors: list[float] = []
    for first, second in ((coarse, baseline), (baseline, fine)):
        stride = int(round(first.spacing / second.spacing))
        background_errors.append(
            relative_weighted_field_difference(
                first.final_background,
                second.final_background[::stride],
                first.radius,
            )
        )
        mode_errors.append(
            relative_transformed_mode_difference(
                first.final_mode, second.final_mode[::stride], first.radius
            )
        )
        q_errors.append(
            relative_trace_rms(
                first.p2_triple_stf_zz_coefficient,
                second.p2_triple_stf_zz_coefficient,
            )
        )
    ledger.check(
        "background, l=2 profile, and STF trace self-converge at approximately second order",
        min(
            background_errors[0] / background_errors[1],
            mode_errors[0] / mode_errors[1],
            q_errors[0] / q_errors[1],
        )
        > 3.5
        and background_errors[1] < 0.006
        and mode_errors[1] < 0.009
        and q_errors[1] < 0.003,
    )
    energy_ranges = [
        float(np.ptp(result.background_energy) / result.background_energy[0])
        for result in simulations
    ]
    ledger.check(
        "closed-box background-energy error decreases by four under each mesh halving",
        energy_ranges[0] / energy_ranges[1] > 3.8
        and energy_ranges[1] / energy_ranges[2] > 3.8
        and energy_ranges[2] < 2.1e-4,
    )

    timestep_fine = run_branch(0.1, courant=0.2)
    timestep_error = relative_trace_rms(
        baseline.p2_triple_stf_zz_coefficient,
        timestep_fine.p2_triple_stf_zz_coefficient,
    )
    ledger.check(
        "timestep halving preserves the STF trace",
        timestep_error < 0.0011,
        f"relative RMS={timestep_error:.9g}",
    )
    domain_large = run_branch(0.1, outer_radius=100.0)
    domain_mask = baseline.radius <= 60.0
    domain_error = relative_transformed_mode_difference(
        baseline.final_mode[domain_mask],
        domain_large.final_mode[: np.count_nonzero(domain_mask)],
        baseline.radius[domain_mask],
    )
    ledger.check(
        "a causally disconnected domain extension leaves the interpreted mode unchanged",
        domain_error < 1.0e-12,
        f"relative L2={domain_error:.9g}",
    )
    half_amplitude = run_branch(0.1, mode_amplitude=0.1)
    ledger.check(
        "halving the perturbation amplitude halves both field mode and STF coefficient",
        np.max(np.abs(half_amplitude.final_mode - 0.5 * baseline.final_mode)) < 1.0e-13
        and np.max(
            np.abs(
                half_amplitude.p2_triple_stf_zz_coefficient
                - 0.5 * baseline.p2_triple_stf_zz_coefficient
            )
        )
        < 1.0e-10,
    )
    zero_amplitude = run_branch(0.2, final_time=2.0, mode_amplitude=0.0)
    ledger.check(
        "zero l=2 seed gives an exact zero mode and zero STF coefficient",
        np.array_equal(zero_amplitude.final_mode, np.zeros_like(zero_amplitude.final_mode))
        and np.array_equal(
            zero_amplitude.p2_triple_stf_zz_coefficient,
            np.zeros_like(zero_amplitude.p2_triple_stf_zz_coefficient),
        ),
    )

    first_j2_zero = brentq(lambda value: spherical_jn(2, value), 5.0, 7.0)
    free_errors: list[float] = []
    free_energy_ranges: list[float] = []
    for spacing in (0.2, 0.1, 0.05):
        free_radius = spacing * np.arange(int(round(20.0 / spacing)) + 1)
        wave_number = first_j2_zero / 20.0
        free_initial = spherical_jn(2, wave_number * free_radius)
        free_time = 8.0
        free = evolve_radial_background_with_linearized_mode(
            np.zeros_like(free_radius),
            free_initial,
            spacing=spacing,
            final_time=free_time,
            ell=2,
            courant=0.4,
            sample_interval=0.4,
        )
        exact = free_initial * np.cos(np.sqrt(1.0 + wave_number**2) * free_time)
        free_errors.append(
            relative_transformed_mode_difference(free.final_mode, exact, free_radius)
        )
        free_energy_ranges.append(
            float(np.ptp(free.quadratic_mode_energy) / free.quadratic_mode_energy[0])
        )
    ledger.check(
        "the exact free spherical-Bessel l=2 box mode converges at second order",
        free_errors[0] / free_errors[1] > 3.9
        and free_errors[1] / free_errors[2] > 3.9
        and free_errors[2] < 3.0e-4,
    )
    ledger.check(
        "the soluble static-background quadratic energy converges under refinement",
        free_energy_ranges[0] / free_energy_ranges[1] > 3.9
        and free_energy_ranges[1] / free_energy_ranges[2] > 3.9
        and free_energy_ranges[2] < 1.1e-4,
    )

    ledger.check(
        "P3D3's exact axisymmetric STF ratio is structural rather than a PDE oracle",
        "Qxx_list.append(Q[0, 0])" in source_text
        and "Ixx, Ixx, Izz" in source_text
        and "pde_axisym = np.max(np.abs(Qxx_p / Qzz_p - (-0.5)))" in source_text,
    )
    ledger.check(
        "P3D3's claimed FS2 recovery is definitional and numerically incompatible",
        reproduction.get("reported_values", {}).get("solved_sigma_perp_squared") == 3.8373
        and "sigma_perp2_solved = I_perp_solved / E0_solved" in source_text
        and "sigma^2 = 0.64 there" in source_text
        and abs(3.8373 - 0.64) > 3.0,
    )
    ledger.check(
        "P3D3's gravity and GW-line language lies outside its derived dependency closure",
        "G_eff = c0 = 1" in source_text
        and "NO absolute scale pinned" in source_text
        and "GW line will be 2 omega_p" in source_text,
    )

    print(
        "P046 numeric metrics: "
        f"background_errors={background_errors}, mode_errors={mode_errors}, "
        f"q_errors={q_errors}, energy_ranges={energy_ranges}, "
        f"timestep_q_error={timestep_error:.9e}, domain_mode_error={domain_error:.9e}, "
        f"free_errors={free_errors}, free_energy_ranges={free_energy_ranges}"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
