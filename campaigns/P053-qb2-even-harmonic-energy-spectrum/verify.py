"""Primary verifier for P053 energy observables and the QB2 disposition."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
import yaml
from scipy.special import jv

import substrate_framework.numerics as numerics_module
import substrate_framework.radial_harmonic_observables as observable_module
from substrate_framework.radial_harmonic_balance import (
    nonlinear_projection_remainder,
    solve_radial_harmonic_balance,
)
from substrate_framework.radial_harmonic_observables import (
    integrate_spherical_radial_density,
    periodic_fourier_coefficients,
    radial_harmonic_energy_density,
    spherical_radial_second_moment_tensor,
    time_averaged_per_axis_energy_variance,
)
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "f7ff064a708d4b3072b247088bee532eda6b14ef4a9d9f5480ea80743a22bbff"


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
    for maximum in (1, 3, 5, 7, 9):
        current = solve_radial_harmonic_balance(
            tuple(range(1, maximum + 1, 2)),
            central_fundamental=2.5,
            outer_radius=outer_radius,
            frequency_guess=0.9769 if previous is None else previous.frequency,
            radial_points=radial_points,
            temporal_samples=temporal_samples,
            tolerance=tolerance,
            initial_solution=previous,
        )
        solutions.append(current)
        previous = current
    return solutions


def _sample(solution, *, radial_samples: int = 2401, phase_samples: int = 512):
    radius = np.linspace(solution.origin_epsilon, 12.0, radial_samples)
    amplitudes = np.vstack(
        [np.interp(radius, solution.radius, row) for row in solution.amplitudes]
    )
    derivatives = np.vstack(
        [
            np.interp(radius, solution.radius, row)
            for row in solution.radial_derivatives
        ]
    )
    phase = 2.0 * np.pi * np.arange(phase_samples) / phase_samples
    density = radial_harmonic_energy_density(
        amplitudes,
        derivatives,
        solution.harmonics,
        solution.frequency,
        phase,
    )
    moment = np.asarray(
        integrate_spherical_radial_density(radius, density, radial_power=2)
    )
    spectrum = periodic_fourier_coefficients(moment, max_harmonic=20)
    remainder = nonlinear_projection_remainder(
        amplitudes, solution.harmonics, temporal_samples=1024
    )
    return {
        "radius": radius,
        "density": density,
        "spectrum": spectrum,
        "remainder": float(np.sqrt(np.mean(np.square(remainder)))),
        "variance": time_averaged_per_axis_energy_variance(radius, density),
    }


def _full_box_density(solution):
    radius = np.linspace(solution.origin_epsilon, solution.outer_radius, 2401)
    amplitudes = np.vstack(
        [np.interp(radius, solution.radius, row) for row in solution.amplitudes]
    )
    derivatives = np.vstack(
        [
            np.interp(radius, solution.radius, row)
            for row in solution.radial_derivatives
        ]
    )
    phase = 2.0 * np.pi * np.arange(512) / 512
    density = radial_harmonic_energy_density(
        amplitudes,
        derivatives,
        solution.harmonics,
        solution.frequency,
        phase,
    )
    return radius, density


def _full_box_variance(solution) -> float:
    radius, density = _full_box_density(solution)
    return time_averaged_per_axis_energy_variance(radius, density)


def _full_box_energy_range(solution) -> float:
    radius, density = _full_box_density(solution)
    energy = np.asarray(integrate_spherical_radial_density(radius, density))
    return float(np.ptp(energy) / np.mean(energy))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    parser.add_argument("--numerical-audit", type=Path, required=True)
    parser.add_argument("--independent-result", type=Path, required=True)
    parser.add_argument("--migration-queue", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    arguments = parser.parse_args()

    source = arguments.source_file.read_text()
    reproduction = _load(arguments.source_reproduction)
    recorded = _load(arguments.numerical_audit)
    independent = _load(arguments.independent_result)
    queue = _load(arguments.migration_queue)
    claims = _load(arguments.claims)
    entry = next(item for item in queue["units"] if item["source_unit"] == "QB2")
    claim_ids = {claim["id"] for claim in claims["claims"]}
    ledger = CheckLedger("P053-QB2")

    ledger.check(
        "QB2 is the hash-pinned primary source unit",
        _hash(arguments.source_file) == SOURCE_SHA256
        and entry["sha256"] == SOURCE_SHA256
        and entry["disposition"] in {"pending_adjudication", "qualified"},
    )
    ledger.check(
        "the literal source exits cleanly with its complete tally",
        reproduction["process_exit_code"] == 0
        and reproduction["terminal_tally"] == "ALL 5 CHECKS PASS",
    )
    ledger.check(
        "the source dependencies remain candidate navigation rather than hidden authority",
        entry["candidate_dependencies"] == ["FS2", "P3D1", "P3D3", "QB1"],
    )
    ledger.check(
        "the exact and numerical claim delta is atomic before or after promotion",
        {"C-PDE-007", "C-PDE-008"}.isdisjoint(claim_ids)
        or {"C-PDE-007", "C-PDE-008"}.issubset(claim_ids),
    )
    ledger.check(
        "QB2 selects the current NumPy trapezoid spelling before its legacy fallback",
        'np.trapezoid if hasattr(np, "trapezoid") else np.trapz' in source,
    )
    ledger.check(
        "QB2 computes a radial second energy moment rather than total energy or an STF tensor",
        "T00 * r**2 * 4.0 * np.pi * r**2" in source
        and reproduction["static_audit"]["scalar_observable"].startswith(
            "S(t)=4*pi*integral r^4"
        ),
    )
    ledger.check(
        "QB2 substitutes a standalone N=1 shooting branch for the accepted N=9 dependency",
        "A_CORE = 3.0" in source
        and "u(r,t) = a_1(r) cos" in source
        and reproduction["static_audit"]["branch"].startswith("A standalone"),
    )
    ledger.check(
        "QB2 consumes its IVP shooting results without solver-status guards",
        "solve_ivp" in source and ".success" not in source and ".message" not in source,
    )
    ledger.check(
        "QB2's nonzero twice-frequency argument omits the radial-gradient coefficient",
        "coeff_2w_kin" in source
        and "2 J_2" in source
        and "coeff_2w_grad" not in source,
    )
    ledger.check(
        "QB2 supplies no harmonic, radial, wall, tolerance, or transform refinement",
        reproduction["static_audit"]["refinements"] == "absent",
    )

    tau = sp.symbols("tau", real=True)
    ledger.check(
        "every retained odd cosine harmonic has exact half-period antisymmetry",
        all(
            sp.trigsimp(sp.cos(mode * (tau + sp.pi)) + sp.cos(mode * tau)) == 0
            for mode in (1, 3, 5, 7, 9)
        ),
    )
    ledger.check(
        "an even temporal harmonic breaks the field antisymmetry",
        sp.trigsimp(sp.cos(2 * (tau + sp.pi)) + sp.cos(2 * tau)) != 0,
    )
    field, field_t, field_r = sp.symbols("u u_t u_r", real=True)
    energy = (field_t**2 + field_r**2) / 2 + 1 - sp.cos(field)
    ledger.check(
        "canonical energy density is exactly invariant under the half-period sign reversal",
        sp.simplify(
            energy.subs({field: -field, field_t: -field_t, field_r: -field_r})
            - energy
        )
        == 0,
    )
    odd_mode = sp.symbols("odd_mode", integer=True, odd=True)
    ledger.check(
        "half-period invariance cancels every odd Fourier coefficient",
        sp.simplify(1 + (-1) ** odd_mode) == 0,
    )

    phase = 2.0 * np.pi * np.arange(4096) / 4096
    amplitude, derivative, frequency = 0.8, 0.3, 0.9
    local_density = radial_harmonic_energy_density(
        [[amplitude]], [[derivative]], (1,), frequency, phase
    )[:, 0]
    local_spectrum = periodic_fourier_coefficients(local_density, max_harmonic=8)
    expected_cos2 = (
        derivative**2 / 4
        - frequency**2 * amplitude**2 / 4
        + 2 * jv(2, amplitude)
    )
    ledger.check(
        "the full local twice-frequency coefficient includes kinetic, gradient, and potential terms",
        abs(local_spectrum.cosine[2] - expected_cos2) < 2.0e-15,
    )
    ledger.mutation_sensitive(
        "the physical time-derivative frequency factor",
        lambda factor: abs(
            periodic_fourier_coefficients(
                0.5
                * (factor * frequency * amplitude * np.sin(phase)) ** 2
                + 0.5 * derivative**2 * np.cos(phase) ** 2
                + 1
                - np.cos(amplitude * np.cos(phase)),
                max_harmonic=8,
            ).cosine[2]
            - expected_cos2
        )
        < 2.0e-15,
        1.0,
        (0.0, 2.0),
    )
    cancelling_derivative = np.sqrt(0.97**2 - 8.0 * jv(2, 1.0))
    cancelling = radial_harmonic_energy_density(
        [[1.0]], [[cancelling_derivative]], (1,), 0.97, phase
    )[:, 0]
    cancelling_spectrum = periodic_fourier_coefficients(
        cancelling, max_harmonic=8
    )
    ledger.check(
        "even selection does not force a nonzero or lowest twice-frequency line",
        cancelling_spectrum.amplitude[2] < 2.0e-15
        and cancelling_spectrum.amplitude[4] > 1.0e-3,
    )

    radius = np.linspace(0.0, 2.0, 1001)
    radial_density = np.ones((8, radius.size))
    tensor = spherical_radial_second_moment_tensor(radius, radial_density)
    trace = np.trace(tensor, axis1=-2, axis2=-1)
    stf = tensor - trace[:, None, None] * np.eye(3) / 3.0
    ledger.check(
        "a spherical radial second moment has an exact zero STF projection",
        np.max(np.abs(stf)) == 0.0,
    )
    anisotropic = np.diag([1.0, 0.0, 0.0])
    anisotropic_stf = anisotropic - np.eye(3) * np.trace(anisotropic) / 3.0
    ledger.check(
        "an anisotropic source mutation produces a nonzero STF tensor",
        np.max(np.abs(anisotropic_stf)) > 0.6,
    )
    signal = 1.4 + 0.7 * np.cos(4 * phase) - 0.2 * np.sin(6 * phase)
    normalized = periodic_fourier_coefficients(signal, max_harmonic=8)
    ledger.check(
        "the direct real transform preserves DC, cosine, sine, and phase normalization",
        abs(normalized.cosine[0] - 1.4) < 2.0e-14
        and abs(normalized.cosine[4] - 0.7) < 2.0e-14
        and abs(normalized.sine[6] + 0.2) < 2.0e-14,
    )

    baseline = _solve_ladder(40.0)
    sampled = [_sample(solution) for solution in baseline]
    cos2 = [float(item["spectrum"].cosine[2]) for item in sampled]
    remainders = [item["remainder"] for item in sampled]
    energy_ranges = [_full_box_energy_range(solution) for solution in baseline]
    ledger.check(
        "every canonical dependency solve completes with resolved collocation residuals",
        all(
            solution.completed and solution.max_collocation_rms_residual < 1.1e-8
            for solution in baseline
        ),
    )
    ledger.check(
        "the core twice-frequency coefficient stabilizes through N=9",
        all(
            fine < 0.02 * coarse
            for coarse, fine in zip(
                np.abs(np.diff(cos2))[:-1], np.abs(np.diff(cos2))[1:]
            )
        ),
    )
    ledger.check(
        "the full nonlinear core remainder decreases with every added odd harmonic",
        all(fine < 0.2 * coarse for coarse, fine in zip(remainders, remainders[1:]))
        and remainders[-1] < 2.0e-5,
    )
    ledger.check(
        "the full-box energy defect tracks the truncation hierarchy",
        all(fine < 0.2 * coarse for coarse, fine in zip(energy_ranges, energy_ranges[1:]))
        and energy_ranges[-1] < 1.1e-6,
    )
    baseline_spectrum = sampled[-1]["spectrum"]
    even_power = float(np.sum(np.square(baseline_spectrum.amplitude[2::2])))
    odd_power = float(np.sum(np.square(baseline_spectrum.amplitude[1::2])))
    ledger.check(
        "the N=9 declared scalar moment has a dominant resolved twice-frequency line",
        baseline_spectrum.amplitude[2] ** 2 / even_power > 0.9998
        and odd_power / even_power < 1.0e-24,
    )
    ledger.check(
        "fresh canonical coefficients reproduce the recorded primary evidence",
        abs(cos2[-1] - recorded["baseline"]["second_cos2"]) < 2.0e-8
        and abs(
            sampled[-1]["variance"] - recorded["baseline"]["per_axis_variance"]
        )
        < 2.0e-8,
    )

    temporal_cos2 = [
        float(_sample(baseline[-1], phase_samples=count)["spectrum"].cosine[2])
        for count in (256, 512, 1024)
    ]
    radial_cos2 = [
        float(_sample(baseline[-1], radial_samples=count)["spectrum"].cosine[2])
        for count in (1201, 2401, 4801)
    ]
    ledger.check(
        "endpoint-excluded temporal refinement preserves the direct coefficient",
        np.ptp(temporal_cos2) < 2.0e-9,
    )
    ledger.check(
        "radial quadrature refinement converges the direct coefficient",
        abs(radial_cos2[2] - radial_cos2[1])
        < 0.3 * abs(radial_cos2[1] - radial_cos2[0]),
    )
    mesh_200 = _solve_ladder(40.0, radial_points=200)[-1]
    mesh_400 = _solve_ladder(40.0, radial_points=400)[-1]
    mesh_cos2 = [
        float(_sample(solution)["spectrum"].cosine[2])
        for solution in (mesh_200, baseline[-1], mesh_400)
    ]
    ledger.check(
        "initial BVP mesh refinement preserves the core coefficient",
        np.ptp(mesh_cos2) < 0.006,
    )
    tight = solve_radial_harmonic_balance(
        baseline[-1].harmonics,
        central_fundamental=2.5,
        outer_radius=40.0,
        frequency_guess=baseline[-1].frequency,
        temporal_samples=512,
        tolerance=1.0e-9,
        initial_solution=baseline[-1],
    )
    tight_cos2 = float(_sample(tight)["spectrum"].cosine[2])
    ledger.check(
        "tolerance and projection refinement preserve the coefficient and reduce residual",
        tight.completed
        and abs(tight_cos2 - cos2[-1]) < 0.008
        and tight.max_collocation_rms_residual
        < 0.11 * baseline[-1].max_collocation_rms_residual,
    )

    domain = {40.0: baseline[-1]}
    for outer in (30.0, 50.0, 60.0):
        domain[outer] = _solve_ladder(outer)[-1]
    domain_core_cos2 = [
        float(_sample(domain[outer])["spectrum"].cosine[2])
        for outer in (30.0, 40.0, 50.0, 60.0)
    ]
    domain_full_variance = [
        _full_box_variance(domain[outer]) for outer in (30.0, 40.0, 50.0, 60.0)
    ]
    ledger.check(
        "the finite-box core line remains bounded but not wall independent",
        np.ptp(domain_core_cos2) < 8.0
        and np.ptp(domain_core_cos2) > 5.0,
    )
    ledger.check(
        "the full-box scalar variance exposes the accepted radiative wall resonance",
        max(domain_full_variance) > 1.03 * np.median(domain_full_variance),
    )
    ledger.check(
        "the independent quadrature review reproduces the line and rejects false oracles",
        independent["verdict"] == "passed"
        and independent["terminal_tally"] == "ALL 22 CHECKS PASS [P053-INDEPENDENT]"
        and abs(independent["independent_coefficients"]["second_cos2"] - cos2[-1])
        < 0.03
        and independent["counterexamples"]["arbitrary_non_solution_pde_residual_rms"]
        > 0.1,
    )
    observable_source = Path(observable_module.__file__).read_text()
    numerics_source = Path(numerics_module.__file__).read_text()
    ledger.check(
        "canonical observables centralize NumPy-version-independent trapezoid dispatch",
        "np.trapz" not in observable_source
        and "np.trapezoid" not in observable_source
        and 'getattr(np, "trapezoid", None)' in numerics_source
        and 'getattr(np, "trapz", None)' in numerics_source,
    )
    ledger.check(
        "the strongest result remains a finite-box scalar line with zero spherical STF",
        recorded["interpretation"]["supported"].startswith(
            "A dominant twice-frequency line"
        )
        and "spherical STF tensor is zero" in recorded["interpretation"]["excluded"],
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
