"""Primary exact and numerical verifier for the P098 MC4 audit."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.dimensional_sine_gordon import (
    dimensional_sine_gordon_coefficients_from_speed_gap,
    dimensional_sine_gordon_scales,
    linear_wave_energy_density,
    linear_wave_residual,
    linear_wave_traveling_field,
)
from substrate_framework.numerics import SolverTolerances, trapezoid_integral
from substrate_framework.sine_gordon_1d import (
    PeriodicSineGordonEvolution,
    evolve_periodic_sine_gordon_leapfrog,
    evolve_periodic_sine_gordon_mol,
    moving_breather_samples,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-27/"
    "bridge_MC4_physical_units_pde.py"
)
SOURCE_SHA256 = "db001de1fde9684282bb5353ec0a5ef4ddcf168809e0c02ca99878fb3f5ff698"
CONTRACT_SHA256 = "8b0cf8610796d75eced40caaf78bb248b62e5f237952982490ecf082d9f96ece"


@dataclass(frozen=True)
class RegressionResult:
    """Final-state exact-solution error and relative energy drift."""

    evolution: PeriodicSineGordonEvolution
    phase_space_error: float
    relative_energy_drift: float


def _campaign_dir() -> Path:
    candidates = (
        Path("campaigns/P098-mc4-physical-pde-regression"),
        Path("proposals/P098-mc4-physical-pde-regression"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _coordinate(half_width: float, spatial_step: float) -> np.ndarray:
    return np.arange(-half_width, half_width, spatial_step, dtype=np.float64)


def _relative_phase_space_error(
    coordinate: np.ndarray,
    field: np.ndarray,
    velocity: np.ndarray,
    exact_field: np.ndarray,
    exact_velocity: np.ndarray,
) -> float:
    numerator = trapezoid_integral(
        np.square(field - exact_field) + np.square(velocity - exact_velocity),
        coordinate,
    )
    denominator = trapezoid_integral(
        np.square(exact_field) + np.square(exact_velocity),
        coordinate,
    )
    return float(np.sqrt(numerator / denominator))


def _evaluate(
    evolution: PeriodicSineGordonEvolution,
    frequency: float,
) -> RegressionResult:
    final_time = float(evolution.time[-1])
    exact_field, exact_velocity, _ = moving_breather_samples(
        evolution.coordinate,
        final_time,
        frequency,
    )
    error = _relative_phase_space_error(
        evolution.coordinate,
        evolution.field[-1],
        evolution.velocity[-1],
        exact_field,
        exact_velocity,
    )
    energy_scale = abs(float(evolution.energy[0]))
    drift = float(np.max(np.abs(evolution.energy - evolution.energy[0]))) / energy_scale
    return RegressionResult(evolution, error, drift)


def _leapfrog_regression(
    *,
    half_width: float,
    spatial_step: float,
    courant: float,
    frequency: float,
    final_time: float,
) -> RegressionResult:
    coordinate = _coordinate(half_width, spatial_step)
    field, velocity, _ = moving_breather_samples(coordinate, 0.0, frequency)
    evolution = evolve_periodic_sine_gordon_leapfrog(
        coordinate,
        field,
        velocity,
        final_time,
        courant * spatial_step,
        sample_stride=10**9,
    )
    return _evaluate(evolution, frequency)


def _mol_regression(
    *,
    half_width: float,
    spatial_step: float,
    frequency: float,
    final_time: float,
    tolerances: SolverTolerances,
) -> RegressionResult:
    coordinate = _coordinate(half_width, spatial_step)
    field, velocity, _ = moving_breather_samples(coordinate, 0.0, frequency)
    evolution = evolve_periodic_sine_gordon_mol(
        coordinate,
        field,
        velocity,
        np.asarray([0.0, final_time]),
        tolerances=tolerances,
        method="DOP853",
    )
    return _evaluate(evolution, frequency)


def _observed_order(coarse_error: float, fine_error: float) -> float:
    return float(np.log(coarse_error / fine_error) / np.log(2.0))


def main() -> int:
    checks = CheckLedger("P098")
    campaign_dir = _campaign_dir()
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("MC4 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
    normalized_contract = (campaign_dir / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n", b"status: draft\n"
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )

    check_calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    imports = {
        alias.name
        for node in source_tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    function_names = {
        node.name for node in source_tree.body if isinstance(node, ast.FunctionDef)
    }
    checks.check(
        "source has five runtime predicates and its literal terminal tally",
        len(check_calls) == 5 and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source copies its numerical machinery rather than importing framework APIs",
        imports == {"sys", "numpy"}
        and not any(isinstance(node, ast.ImportFrom) for node in source_tree.body)
        and {
            "check",
            "lap1d",
            "grad1d",
            "breather_ic",
            "evolve",
            "dominant_omega",
            "retained_core",
            "core_width_rms",
        }.issubset(function_names),
    )
    checks.check(
        "source quadrature dispatch is historical rather than canonical",
        'trapz = np.trapezoid if hasattr(np, "trapezoid") else np.trapz'
        in source_text
        and "trapezoid_integral" not in source_text,
    )
    checks.check(
        "source spatial and temporal refinement are coupled and only two-level",
        'G1 = run_good(ell=1.0, dx=0.05)' in source_text
        and 'G1b = run_good(ell=1.0, dx=0.025)' in source_text
        and "dt = 0.4 * dx / c" in source_text,
    )

    c, ell = sp.symbols("c ell", positive=True)
    coefficients = dimensional_sine_gordon_coefficients_from_speed_gap(
        1 / c**2,
        c,
        c / ell,
    )
    scales = dimensional_sine_gordon_scales(coefficients)
    checks.check(
        "source coefficient normalization gives the declared physical scales",
        sp.simplify(coefficients.gradient - 1) == 0
        and sp.simplify(coefficients.onsite - 1 / ell**2) == 0
        and sp.simplify(scales.signal_speed - c) == 0
        and sp.simplify(scales.gap_frequency - c / ell) == 0
        and sp.simplify(scales.length - ell) == 0,
    )

    x, t = sp.symbols("x t", real=True)
    normalized_x, normalized_t = sp.symbols("X tau", real=True)
    profile = sp.Function("U")
    physical_field = profile(x / ell, c * t / ell)
    physical_residual = sp.diff(physical_field, t, 2) - c**2 * sp.diff(
        physical_field, x, 2
    ) + (c / ell) ** 2 * sp.sin(physical_field)
    expected_residual = (c / ell) ** 2 * (
        sp.Subs(
            sp.diff(profile(normalized_x, normalized_t), normalized_t, 2),
            (normalized_x, normalized_t),
            (x / ell, c * t / ell),
        )
        - sp.Subs(
            sp.diff(profile(normalized_x, normalized_t), normalized_x, 2),
            (normalized_x, normalized_t),
            (x / ell, c * t / ell),
        )
        + sp.sin(physical_field)
    )
    checks.check(
        "chain rule reduces the physical equation exactly to normalized sine-Gordon",
        sp.simplify(physical_residual - expected_residual) == 0,
    )

    kinetic_shape, onsite_shape = sp.symbols("A B", positive=True)
    source_width_weight = kinetic_shape / ell**2 + onsite_shape
    covariant_width_weight = (kinetic_shape + onsite_shape) / ell**2
    checks.check(
        "the source width proxy breaks exact ell similarity",
        sp.simplify(sp.diff(ell**2 * source_width_weight, ell))
        == 2 * ell * onsite_shape
        and sp.simplify(sp.diff(ell**2 * covariant_width_weight, ell)) == 0
        and 'g = ux**2 + (1.0 - np.cos(u))' in source_text,
    )
    checks.mutation_sensitive(
        "the inverse-ell-squared onsite weight is load bearing",
        lambda weight: sp.simplify(sp.diff(ell**2 * weight, ell)) == 0,
        covariant_width_weight,
        [source_width_weight, kinetic_shape + onsite_shape / ell**2],
    )

    packet = linear_wave_traveling_field(
        sp.sech,
        x,
        t,
        sp.Rational(3, 2),
    )
    packet_residual = linear_wave_residual(
        packet,
        x,
        t,
        sp.Rational(3, 2),
    )
    packet_energy = linear_wave_energy_density(
        packet,
        x,
        t,
        sp.Rational(4, 9),
        sp.Integer(1),
    )
    packet_energy_at_zero = sp.simplify(packet_energy.subs(t, 0))
    packet_energy_primitive = sp.tanh(x) ** 3 / 3
    checks.check(
        "gapless wave equation retains an exact localized traveling packet",
        sp.simplify(packet_residual) == 0
        and sp.simplify(
            sp.diff(packet_energy_primitive, x) - packet_energy_at_zero
        )
        == 0
        and sp.limit(packet_energy_primitive, x, sp.oo)
        - sp.limit(packet_energy_primitive, x, -sp.oo)
        == sp.Rational(2, 3),
    )
    checks.check(
        "source gapless control measures fixed-core drainage rather than universal delocalization",
        "gapless=True" in source_text
        and "N_bad/N_good" in source_text
        and "linear_wave_traveling_field" not in source_text,
    )

    frequency = 3.0 / 5.0
    final_time = 4.0 * 2.0 * np.pi / frequency
    spatial_steps = (1.0 / 5.0, 1.0 / 10.0, 1.0 / 20.0, 1.0 / 40.0)
    spatial_results = tuple(
        _leapfrog_regression(
            half_width=30.0,
            spatial_step=step,
            courant=2.0 / 5.0,
            frequency=frequency,
            final_time=final_time,
        )
        for step in spatial_steps
    )
    spatial_errors = tuple(result.phase_space_error for result in spatial_results)
    spatial_orders = tuple(
        _observed_order(coarse, fine)
        for coarse, fine in zip(spatial_errors, spatial_errors[1:])
    )
    print("P098 spatial errors:", spatial_errors)
    print("P098 spatial orders:", spatial_orders)
    print(
        "P098 spatial energy drifts:",
        tuple(result.relative_energy_drift for result in spatial_results),
    )
    checks.check(
        "three-level leapfrog phase-space errors strictly decrease",
        all(fine < coarse for coarse, fine in zip(spatial_errors, spatial_errors[1:])),
    )
    checks.check(
        "leapfrog spatial refinement retains second-order convergence",
        min(spatial_orders) > 1.5,
    )
    checks.check(
        "finest leapfrog exact-family error is below one-half percent",
        spatial_results[-1].phase_space_error < 5.0e-3,
    )
    checks.check(
        "finest leapfrog relative energy drift is below one-half percent",
        spatial_results[-1].relative_energy_drift < 5.0e-3,
    )

    time_coarse = _leapfrog_regression(
        half_width=30.0,
        spatial_step=1.0 / 10.0,
        courant=2.0 / 5.0,
        frequency=frequency,
        final_time=final_time,
    )
    time_fine = _leapfrog_regression(
        half_width=30.0,
        spatial_step=1.0 / 10.0,
        courant=1.0 / 5.0,
        frequency=frequency,
        final_time=final_time,
    )
    time_finer = _leapfrog_regression(
        half_width=30.0,
        spatial_step=1.0 / 10.0,
        courant=1.0 / 10.0,
        frequency=frequency,
        final_time=final_time,
    )
    print(
        "P098 time-step errors:",
        time_coarse.phase_space_error,
        time_fine.phase_space_error,
        time_finer.phase_space_error,
    )
    checks.check(
        "one-at-a-time timestep halvings reduce exact-family error",
        time_finer.phase_space_error
        < time_fine.phase_space_error
        < time_coarse.phase_space_error,
    )

    domain_results = tuple(
        _leapfrog_regression(
            half_width=half_width,
            spatial_step=1.0 / 20.0,
            courant=2.0 / 5.0,
            frequency=frequency,
            final_time=final_time,
        )
        for half_width in (20.0, 30.0, 40.0)
    )
    domain_errors = tuple(result.phase_space_error for result in domain_results)
    print("P098 domain errors:", domain_errors)
    checks.check(
        "domain refinement leaves the finest-grid error stable",
        max(domain_errors) / min(domain_errors) < 1.2,
    )

    tolerance_levels = (
        SolverTolerances(rtol=1.0e-8, atol=1.0e-11, max_step=1.0 / 50.0),
        SolverTolerances(rtol=1.0e-9, atol=1.0e-12, max_step=1.0 / 50.0),
        SolverTolerances(rtol=1.0e-10, atol=1.0e-13, max_step=1.0 / 50.0),
    )
    mol_results = tuple(
        _mol_regression(
            half_width=30.0,
            spatial_step=1.0 / 10.0,
            frequency=frequency,
            final_time=final_time,
            tolerances=tolerances,
        )
        for tolerances in tolerance_levels
    )
    mol_errors = tuple(result.phase_space_error for result in mol_results)
    print("P098 DOP853 errors:", mol_errors)
    print(
        "P098 DOP853 function evaluations:",
        tuple(result.evolution.function_evaluations for result in mol_results),
    )
    checks.check(
        "DOP853 solver status and finite-state gates are inherited from canonical API",
        all(
            result.evolution.method == "periodic-centered-DOP853"
            and result.evolution.function_evaluations is not None
            and result.evolution.function_evaluations > 0
            and np.all(np.isfinite(result.evolution.field))
            and np.all(np.isfinite(result.evolution.velocity))
            for result in mol_results
        ),
    )
    checks.check(
        "DOP853 tolerance refinement does not worsen the spatially limited error",
        mol_errors[-1] <= 1.02 * mol_errors[0]
        and mol_errors[-1] <= 1.02 * mol_errors[1],
    )

    tight_mol = mol_results[-1]
    cross_method_error = _relative_phase_space_error(
        tight_mol.evolution.coordinate,
        tight_mol.evolution.field[-1],
        tight_mol.evolution.velocity[-1],
        time_finer.evolution.field[-1],
        time_finer.evolution.velocity[-1],
    )
    print("P098 cross-time-method error:", cross_method_error)
    checks.check(
        "time-refined leapfrog and tight DOP853 agree below one-half percent",
        cross_method_error < 5.0e-3,
    )

    verifier_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    direct_numpy_integration_calls = [
        node
        for node in ast.walk(verifier_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "np"
        and node.func.attr in {"trapz", "trapezoid"}
    ]
    checks.check(
        "new numerical work contains no direct NumPy quadrature call",
        not direct_numpy_integration_calls,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
