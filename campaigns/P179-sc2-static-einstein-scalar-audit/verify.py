#!/usr/bin/env python3
"""Primary source-aware exact and numeric verifier for SC2/C-STG-002."""

from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys

import numpy as np
from scipy.interpolate import CubicSpline
import sympy as sp

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.spherical_einstein_scalar import (
    regular_origin_sine_gordon_data,
    sine_gordon_gravity_scaling,
    static_spherical_sine_gordon_reduction,
)
from substrate_framework.spherical_einstein_scalar_bvp import (
    compare_static_spherical_scalar_solutions,
    finite_wall_boundary_residual,
    shoot_static_spherical_scalar_bvp,
    solve_static_spherical_scalar_bvp,
    static_spherical_scalar_rhs,
)
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P179-sc2-static-einstein-scalar-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-36/"
    "bridge_SC2_horndeski_selfconsistent_solve.py"
)
PINNED_HASHES = {
    SOURCE: "64dfc9c31edd8368cb0e2359ca646fc8f62fe306d6af7a326ff8934070b96425",
    ROOT / "governance/releases/v0.130.0.yaml": (
        "a13516d2a4de2d8d75b65ef5980c01e5feab408e123279954b4b12bf7dbf2ffb"
    ),
    CAMPAIGN / "evidence/proposal-revision-0001.yaml": (
        "27428b712bc4aa336774a0a624b7eb959e2a3b11209d43f11dc5676863a8b42b"
    ),
    CAMPAIGN / "evidence/numeric-thresholds.yaml": (
        "cdd74fe585b9624a88f8f2e1c3eb8b21952d2247fe320b22b0e6d95555b525e7"
    ),
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _native_source() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SOURCE)],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def _solve(**changes: float):
    parameters: dict[str, float | int] = {
        "central_amplitude": 3.0,
        "dimensionless_coupling": 0.03,
        "origin_epsilon": 0.001,
        "outer_radius": 40.0,
        "initial_mesh_points": 400,
        "tolerance": 1.0e-8,
        "max_nodes": 100_000,
        "frequency_guess": 0.89,
    }
    parameters.update(changes)
    return solve_static_spherical_scalar_bvp(**parameters)


def _solver_gate(solution) -> bool:
    tail_metric = 1.0 - 2.0 * solution.outer_mass / solution.outer_radius
    tail_squared = (1.0 - solution.frequency**2 / tail_metric) / tail_metric
    return (
        solution.completed
        and 0.0 < solution.frequency < 1.0
        and solution.max_collocation_rms_residual <= 1.05 * solution.tolerance
        and solution.boundary_residual_max_abs <= 1.0e-8
        and solution.off_grid_relative_ode_residual
        <= max(1.0e-8, 5.0 * solution.tolerance)
        and solution.minimum_radial_metric_function > 0.1
        and tail_squared > 0.0
    )


def _axis_gate(solutions: list) -> tuple[bool, list[tuple[float, float, float]]]:
    reference = solutions[-1]
    diagnostics = [
        (
            compare_static_spherical_scalar_solutions(reference, solution),
            abs(solution.frequency - reference.frequency),
            abs(solution.outer_mass - reference.outer_mass),
        )
        for solution in solutions
    ]
    passed = all(
        state <= 2.0e-6 and frequency <= 2.0e-7 and mass <= 2.0e-7
        for state, frequency, mass in diagnostics
    )
    return passed, diagnostics


def _wrong_coupling_residual(solution) -> float:
    midpoints = 0.5 * (solution.radius[:-1] + solution.radius[1:])
    spline = CubicSpline(solution.radius, solution.state, axis=1)
    state = np.asarray(spline(midpoints), dtype=np.float64)
    derivative = np.asarray(spline(midpoints, 1), dtype=np.float64)
    wrong_rhs = static_spherical_scalar_rhs(
        midpoints, state, solution.frequency, 0.0
    )
    scale = 1.0 + np.max(np.abs(wrong_rhs), axis=0)
    return float(np.max(np.abs(derivative - wrong_rhs) / scale[None, :]))


def main() -> int:
    checks = CheckLedger("P179/SC2/C-STG-002")
    for path, expected in PINNED_HASHES.items():
        checks.check(
            f"pinned artifact {path.name} retains its audited bytes",
            _digest(path) == expected,
        )

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "SC2 has seven lexical checks four assertions and two SciPy solver calls",
        len(source_checks) == 7
        and sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 4
        and source_text.count("solve_bvp(") == 1
        and source_text.count("solve_ivp(") == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "SC2 has no NumPy trapezoidal integration compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    native = _native_source()
    checks.check(
        "native hash-pinned SC2 exits zero and executes exactly seven predicates",
        native.returncode == 0
        and native.stderr == ""
        and len(re.findall(r"  PASS$", native.stdout, flags=re.MULTILINE)) == 7
        and native.stdout.count("ALL 7 CHECKS PASS") == 1,
        native.stderr[-500:],
    )

    kappa, field_scale, mu = sp.symbols("kappa F mu", positive=True)
    u, physical_radius, physical_time, geometric_mass = sp.symbols(
        "u r t M", real=True
    )
    scaling = sine_gordon_gravity_scaling(
        kappa,
        field_scale,
        mu,
        u,
        physical_radius,
        physical_time,
        geometric_mass,
    )
    checks.check(
        "physical scale ledger yields alpha=kappa F squared and dimensionless coordinates",
        scaling.dimensionless_coupling == kappa * field_scale**2
        and scaling.dimensionless_radius == mu * physical_radius
        and scaling.dimensionless_time == mu * physical_time
        and scaling.dimensionless_mass == mu * geometric_mass
        and scaling.physical_potential
        == mu**2 * field_scale**2 * (1 - sp.cos(u)),
    )

    x = sp.symbols("x", positive=True)
    omega, alpha = sp.symbols("Omega alpha", positive=True)
    amplitude = sp.Function("a", real=True)(x)
    mass = sp.Function("m", real=True)(x)
    phi = sp.Function("Phi", real=True)(x)
    reduction = static_spherical_sine_gordon_reduction(
        x, amplitude, mass, phi, omega, alpha
    )
    checks.check(
        "averaged conservation factorizes exactly through the projected scalar equation",
        reduction.conservation_identity_residual == 0
        and sp.simplify(
            reduction.conservation_residual - reduction.conservation_factor
        )
        == 0,
    )
    checks.check(
        "wrong Bessel sign and wrong radial divergence break conservation closure",
        sp.simplify(
            reduction.conservation_residual
            - reduction.radial_metric_function
            * sp.diff(amplitude, x)
            * (
                reduction.scalar_equation_residual
                + 4 * sp.besselj(1, amplitude)
                / reduction.radial_metric_function
            )
            / 2
        )
        != 0
        and sp.simplify(
            reduction.conservation_residual
            - reduction.radial_metric_function
            * sp.diff(amplitude, x)
            * (reduction.scalar_equation_residual - sp.diff(amplitude, x) / x)
            / 2
        )
        != 0,
    )
    origin = regular_origin_sine_gordon_data(
        sp.symbols("A", positive=True), 0, omega, alpha
    )
    checks.check(
        "regular-origin scalar mass and lapse coefficients cancel singular limits",
        origin.amplitude_second_derivative
        == (
            2 * sp.besselj(1, origin.central_amplitude)
            - omega**2 * origin.central_amplitude
        )
        / 3
        and sp.simplify(
            origin.mass_cubic_coefficient
            - alpha * origin.central_energy_density / 6
        )
        == 0,
    )
    checks.check(
        "discarded scalar and stress harmonics block pointwise full-PDE promotion",
        reduction.discarded_scalar_third_harmonic
        == 2 * sp.besselj(3, amplitude)
        and reduction.discarded_scalar_third_harmonic != 0
        and reduction.pointwise_energy_density_second_harmonic != 0,
    )

    phase = np.linspace(0.0, 2.0 * np.pi, 100_001)
    sample_amplitude = 1.7
    potential_average = np.trapezoid(
        1.0 - np.cos(sample_amplitude * np.cos(phase)), phase
    ) / (2.0 * np.pi)
    checks.check(
        "direct current-NumPy phase quadrature independently reproduces the Bessel average",
        abs(potential_average - (1.0 - float(sp.besselj(0, sample_amplitude))))
        < 2.0e-14,
    )

    axes = {
        "mesh": [_solve(initial_mesh_points=value) for value in (200, 400, 800)],
        "tolerance": [_solve(tolerance=value) for value in (1.0e-6, 1.0e-8, 1.0e-10)],
        "origin": [_solve(origin_epsilon=value) for value in (0.002, 0.001, 0.0005)],
        "wall": [_solve(outer_radius=value) for value in (30.0, 40.0, 60.0)],
    }
    for name, solutions in axes.items():
        for index, solution in enumerate(solutions):
            print(
                "NUMERIC",
                name,
                index,
                f"omega={solution.frequency:.15g}",
                f"mass={solution.outer_mass:.15g}",
                f"phi0={solution.central_lapse_exponent:.15g}",
                f"nodes={solution.adaptive_nodes}",
                f"colloc={solution.max_collocation_rms_residual:.6g}",
                f"bc={solution.boundary_residual_max_abs:.6g}",
                f"offgrid={solution.off_grid_relative_ode_residual:.6g}",
                f"minf={solution.minimum_radial_metric_function:.15g}",
            )
            checks.check(
                f"{name} level {index} satisfies solver residual horizon and tail gates",
                _solver_gate(solution),
            )
        stable, diagnostics = _axis_gate(solutions)
        print("STABILITY", name, diagnostics)
        checks.check(
            f"{name} refinement satisfies state frequency and mass stability gates",
            stable,
            str(diagnostics),
        )

    reference = axes["tolerance"][-1]
    shooting = shoot_static_spherical_scalar_bvp(reference)
    shooting_mass = float(shooting.ivp.state[2, -1])
    checks.check(
        "independent DOP853 root shooting satisfies wall and horizon gates",
        shooting.root_success
        and np.max(np.abs(shooting.boundary_residuals), initial=0.0) <= 1.0e-8
        and shooting.minimum_radial_metric_function > 0.1,
    )
    checks.check(
        "independent shooting agrees in frequency central lapse and mass",
        abs(shooting.frequency - reference.frequency) <= 1.0e-8
        and abs(
            shooting.central_lapse_exponent - reference.central_lapse_exponent
        )
        <= 1.0e-8
        and abs(shooting_mass - reference.outer_mass) <= 1.0e-8,
    )
    print(
        "SHOOTING",
        f"omega={shooting.frequency:.15g}",
        f"mass={shooting_mass:.15g}",
        f"phi0={shooting.central_lapse_exponent:.15g}",
        f"nfev={shooting.root_function_evaluations}",
        f"wall={shooting.boundary_residuals.tolist()}",
        f"minf={shooting.minimum_radial_metric_function:.15g}",
    )

    wrong_coupling = _wrong_coupling_residual(reference)
    wrong_amplitude = finite_wall_boundary_residual(
        reference.state[:, 0],
        reference.state[:, -1],
        reference.frequency,
        central_amplitude=2.5,
        dimensionless_coupling=reference.dimensionless_coupling,
        origin_epsilon=reference.origin_epsilon,
        outer_radius=reference.outer_radius,
    )
    checks.check(
        "zero-coupling mutation fails the finite-gravity ODE residual gate",
        wrong_coupling >= 1.0e-3,
        str(wrong_coupling),
    )
    checks.check(
        "wrong central-amplitude mutation fails the boundary gate",
        np.max(np.abs(wrong_amplitude), initial=0.0) >= 0.1,
        str(wrong_amplitude),
    )

    checks.check(
        "source wording exceeds the verified averaged canonical-scalar scope",
        "FULL coupled Einstein+scalar system" in source_text
        and "Horndeski" in source_text
        and "nonminimal" not in source_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
