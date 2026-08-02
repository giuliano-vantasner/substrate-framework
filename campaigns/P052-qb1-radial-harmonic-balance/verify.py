"""Primary verifier for P052 radial harmonic balance and QB1."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
import yaml
from scipy.special import jv

import substrate_framework.radial_harmonic_balance as harmonic_module
from substrate_framework.radial_harmonic_balance import (
    classify_harmonic_tail_channels,
    nonlinear_projection_remainder,
    odd_harmonics,
    project_sine_harmonics,
    reconstruct_radial_harmonics,
    solve_radial_harmonic_balance,
)
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "1f387c140ca80be0e457efd17146267bdecab1cbdbcdd10dd34287bc5de2dc7a"


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path):
    return yaml.safe_load(path.read_text())


def _solve_ladder(
    outer_radius: float,
    *,
    radial_points: int = 300,
    temporal_samples: int = 256,
    tolerance: float = 1.0e-8,
):
    previous = None
    solutions = []
    frequency_guess = 0.95
    for maximum in (1, 3, 5, 7, 9):
        current = solve_radial_harmonic_balance(
            odd_harmonics(maximum),
            central_fundamental=2.5,
            outer_radius=outer_radius,
            frequency_guess=frequency_guess,
            radial_points=radial_points,
            temporal_samples=temporal_samples,
            tolerance=tolerance,
            initial_solution=previous,
        )
        solutions.append(current)
        previous = current
        frequency_guess = current.frequency
    return solutions


def _uniform_amplitudes(solution, samples: int = 2401):
    radius = np.linspace(solution.origin_epsilon, solution.outer_radius, samples)
    amplitudes = np.vstack(
        [np.interp(radius, solution.radius, row) for row in solution.amplitudes]
    )
    return radius, amplitudes


def _core_remainder(solution) -> float:
    radius, amplitudes = _uniform_amplitudes(solution)
    remainder = nonlinear_projection_remainder(
        amplitudes, solution.harmonics, temporal_samples=1024
    )
    return float(np.sqrt(np.mean(remainder[:, radius <= 12.0] ** 2)))


def _tail_norm(solution, harmonic: int) -> float:
    radius, amplitudes = _uniform_amplitudes(solution)
    index = solution.harmonics.index(harmonic)
    selected = radius >= 0.75 * solution.outer_radius
    return float(
        np.sqrt(np.mean((radius[selected] * amplitudes[index, selected]) ** 2))
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    parser.add_argument("--numerical-audit", type=Path, required=True)
    parser.add_argument("--migration-queue", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    arguments = parser.parse_args()

    source = arguments.source_file.read_text()
    reproduction = _load(arguments.source_reproduction)
    recorded_numeric = _load(arguments.numerical_audit)
    queue = _load(arguments.migration_queue)
    claims = _load(arguments.claims)
    queue_entry = next(
        item for item in queue["units"] if item["source_unit"] == "QB1"
    )
    claim_map = {claim["id"]: claim for claim in claims["claims"]}
    ledger = CheckLedger("P052-QB1")

    ledger.check(
        "QB1 is the hash-pinned primary source unit",
        _hash(arguments.source_file) == SOURCE_SHA256
        and queue_entry["sha256"] == SOURCE_SHA256
        and queue_entry["disposition"] in {"pending_adjudication", "qualified"},
    )
    ledger.check(
        "the literal source exits cleanly with its complete tally",
        reproduction["process_exit_code"] == 0
        and reproduction["terminal_tally"] == "ALL 6 CHECKS PASS",
    )
    ledger.check(
        "the predecessor dependency is evidence rather than an accepted claim ID",
        queue_entry["candidate_dependencies"] == ["P3D1"],
    )
    ledger.check(
        "the split claim delta is atomic before or after promotion",
        ({"C-PDE-005", "C-PDE-006"}.isdisjoint(claim_map))
        or {"C-PDE-005", "C-PDE-006"}.issubset(claim_map),
    )

    ledger.check(
        "QB1 projects the radial equation with the correct sign convention",
        "a_n'' + (2/r) a_n' + (n omega)^2 a_n - S_n(r) = 0" in source,
    )
    ledger.check(
        "QB1 places every retained mode on one finite Dirichlet wall",
        "res.append(Yb[2 * idx])" in source and "R=40.0" in source,
    )
    ledger.check(
        "QB1's truncation verdict observes only successive frequency shifts",
        "converges = d35 < d13" in source and "omitted" not in source,
    )
    ledger.check(
        "QB1 calibrates its free amplitude to the accepted IVP comparator",
        "target = 0.921" in source
        and "A_star" in source
        and "eigen_omega(A_star" in source,
    )
    ledger.check(
        "QB1 omits domain and projection refinement",
        reproduction["static_audit"]["domain_refinement"] == "absent"
        and reproduction["static_audit"]["temporal_projection_refinement"]
        == "absent",
    )

    tau = sp.symbols("tau", real=True)
    odd_antisymmetry = all(
        sp.trigsimp(sp.cos(mode * (tau + sp.pi)) + sp.cos(mode * tau)) == 0
        for mode in (1, 3, 5, 7, 9)
    )
    ledger.check(
        "odd cosine harmonics have exact half-period antisymmetry",
        odd_antisymmetry,
    )
    ledger.check(
        "an even-harmonic mutation breaks half-period antisymmetry",
        sp.trigsimp(sp.cos(2 * (tau + sp.pi)) + sp.cos(2 * tau)) != 0,
    )
    phases = np.linspace(0.0, np.pi, 101)
    sample_coefficients = np.array([[1.1], [-0.2], [0.03]])
    reconstructed = reconstruct_radial_harmonics(
        sample_coefficients, (1, 3, 5), phases
    )
    shifted = reconstruct_radial_harmonics(
        sample_coefficients, (1, 3, 5), phases + np.pi
    )
    ledger.check(
        "the importable reconstruction preserves the exact antisymmetry",
        np.max(np.abs(reconstructed + shifted)) < 3.0e-15,
    )

    amplitudes = np.array([[0.2, 1.0, 2.5, 4.0]])
    targets = (1, 3, 5, 7)
    projected = project_sine_harmonics(
        amplitudes,
        (1,),
        target_harmonics=targets,
        temporal_samples=512,
    )
    expected = np.vstack(
        [
            2.0
            * (-1.0) ** ((mode - 1) // 2)
            * jv(mode, amplitudes[0])
            for mode in targets
        ]
    )
    ledger.check(
        "periodic projection independently matches Jacobi-Anger coefficients",
        np.max(np.abs(projected - expected)) < 8.0e-15,
    )
    ledger.mutation_sensitive(
        "the Fourier factor two is load-bearing",
        lambda factor: np.max(np.abs(factor * projected / 2.0 - expected)) < 8.0e-15,
        2.0,
        (1.0, -2.0),
    )

    radius, a0, a2, geometry = sp.symbols(
        "r a0 a2 geometry", positive=True, real=True
    )
    regular_series = a0 + a2 * radius**2 / 2
    regular_limit = sp.limit(
        sp.diff(regular_series, radius, 2)
        + geometry * sp.diff(regular_series, radius) / radius,
        radius,
        0,
    )
    ledger.mutation_sensitive(
        "the three-dimensional radial-origin factor is load-bearing",
        lambda coefficient: sp.simplify(
            regular_limit.subs(geometry, coefficient) - 3 * a2
        )
        == 0,
        2,
        (0, 1, 3),
    )

    kappa, wave_number, phase = sp.symbols(
        "kappa wave_number phase", positive=True, real=True
    )
    evanescent = sp.exp(-kappa * radius) / radius
    radiative = sp.sin(wave_number * radius + phase) / radius
    radial_laplacian = lambda expression: sp.diff(expression, radius, 2) + 2 * sp.diff(
        expression, radius
    ) / radius
    ledger.check(
        "the evanescent one-over-r tail has positive radial Laplacian eigenvalue",
        sp.simplify(radial_laplacian(evanescent) - kappa**2 * evanescent)
        == 0,
    )
    ledger.check(
        "the radiative one-over-r tail has negative radial Laplacian eigenvalue",
        sp.simplify(radial_laplacian(radiative) + wave_number**2 * radiative)
        == 0,
    )
    theta, angular = sp.symbols("theta angular", positive=True, real=True)
    averaged_radial_density = sp.integrate(
        ((angular**2 + 1) * sp.sin(theta) ** 2 + wave_number**2 * sp.cos(theta) ** 2)
        / 4,
        (theta, 0, 2 * sp.pi),
    ) / (2 * sp.pi)
    ledger.check(
        "a radiative one-over-r tail has positive asymptotic energy per radial length",
        sp.simplify(
            averaged_radial_density.subs(wave_number**2, angular**2 - 1)
            - angular**2 / 4
        )
        == 0,
    )

    reference_frequency = 0.9768739
    channels = classify_harmonic_tail_channels(
        (1, 3, 5, 7, 9), reference_frequency
    )
    ledger.check(
        "the source-like fundamental is evanescent but every retained higher mode radiates",
        [channel.behavior for channel in channels]
        == ["evanescent", "radiative", "radiative", "radiative", "radiative"],
    )
    ledger.check(
        "a sub-gap fundamental does not remove its nonlinear radiation channels",
        reference_frequency < 1.0 and 3.0 * reference_frequency > 1.0,
    )

    baseline = _solve_ladder(40.0)
    frequencies = [solution.frequency for solution in baseline]
    remainders = [_core_remainder(solution) for solution in baseline]
    ledger.check(
        "every canonical BVP completes with resolved collocation residuals",
        all(
            solution.completed and solution.max_collocation_rms_residual < 1.1e-8
            for solution in baseline
        ),
    )
    ledger.check(
        "frequency increments shrink through the N=9 ladder",
        all(
            fine < coarse
            for coarse, fine in zip(
                np.abs(np.diff(frequencies))[:-1],
                np.abs(np.diff(frequencies))[1:],
            )
        ),
    )
    ledger.check(
        "the full nonlinear core remainder decreases at every harmonic level",
        all(fine < 0.2 * coarse for coarse, fine in zip(remainders, remainders[1:])),
    )
    ledger.check(
        "the N=9 full core remainder is below two times ten to the minus five",
        remainders[-1] < 2.0e-5,
    )
    ledger.check(
        "the recorded primary evidence matches the fresh N=9 solve",
        abs(
            frequencies[-1]
            - recorded_numeric["baseline"]["levels"][-1]["omega"]
        )
        < 5.0e-9,
    )
    ledger.check(
        "the canonical outer conditions expose every finite-wall radiative mode",
        baseline[-1].outer_conditions
        == (
            "decaying_robin",
            "dirichlet_box",
            "dirichlet_box",
            "dirichlet_box",
            "dirichlet_box",
        ),
    )

    mesh_200 = _solve_ladder(40.0, radial_points=200)[-1]
    mesh_400 = _solve_ladder(40.0, radial_points=400)[-1]
    ledger.check(
        "adaptive collocation is insensitive to the initial radial mesh",
        abs(mesh_200.frequency - mesh_400.frequency) < 5.0e-9,
    )
    time_512 = solve_radial_harmonic_balance(
        baseline[-1].harmonics,
        central_fundamental=2.5,
        outer_radius=40.0,
        frequency_guess=baseline[-1].frequency,
        temporal_samples=512,
        tolerance=1.0e-8,
        initial_solution=baseline[-1],
    )
    tight = solve_radial_harmonic_balance(
        time_512.harmonics,
        central_fundamental=2.5,
        outer_radius=40.0,
        frequency_guess=time_512.frequency,
        temporal_samples=512,
        tolerance=1.0e-9,
        initial_solution=time_512,
    )
    ledger.check(
        "temporal projection refinement preserves the branch",
        abs(time_512.frequency - baseline[-1].frequency) < 5.0e-9,
    )
    ledger.check(
        "nonlinear tolerance refinement preserves the branch and reduces the solver residual",
        abs(tight.frequency - time_512.frequency) < 5.0e-9
        and tight.max_collocation_rms_residual
        < 0.11 * time_512.max_collocation_rms_residual,
    )

    domain_solutions = {
        outer: _solve_ladder(outer)[-1] for outer in (30.0, 50.0, 60.0)
    }
    domain_solutions[40.0] = baseline[-1]
    domain_frequencies = [
        domain_solutions[outer].frequency for outer in (30.0, 40.0, 50.0, 60.0)
    ]
    domain_tail_norms = [
        _tail_norm(domain_solutions[outer], 3)
        for outer in (30.0, 40.0, 50.0, 60.0)
    ]
    ledger.check(
        "the finite-box core frequency remains numerically bounded across four walls",
        np.ptp(domain_frequencies) < 1.0e-4,
    )
    ledger.check(
        "the radiative third-harmonic tail exposes a wall-standing-wave resonance",
        max(domain_tail_norms) > 10.0 * np.median(domain_tail_norms),
    )

    amplitude_two = solve_radial_harmonic_balance(
        (1,),
        central_fundamental=2.0,
        outer_radius=40.0,
        frequency_guess=0.95,
        radial_points=240,
        temporal_samples=128,
        tolerance=2.0e-6,
    )
    amplitude_three = solve_radial_harmonic_balance(
        (1,),
        central_fundamental=3.0,
        outer_radius=40.0,
        frequency_guess=0.95,
        radial_points=240,
        temporal_samples=128,
        tolerance=2.0e-6,
    )
    ledger.check(
        "the central amplitude is a load-bearing free branch coordinate",
        amplitude_two.frequency > baseline[0].frequency > amplitude_three.frequency
        and amplitude_two.frequency - amplitude_three.frequency > 0.01,
    )
    ledger.check(
        "no version-specific NumPy trapezoid call enters the canonical harmonic solver",
        "np.trapz" not in Path(harmonic_module.__file__).read_text()
        and "np.trapezoid" not in Path(harmonic_module.__file__).read_text(),
    )
    ledger.check(
        "the strongest result is a finite-box branch rather than a unique localized eigenstate",
        recorded_numeric["interpretation"]["supported"].startswith(
            "A nontrivial finite-radius"
        )
        and "not an infinite-domain" in recorded_numeric["interpretation"]["excluded"],
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
