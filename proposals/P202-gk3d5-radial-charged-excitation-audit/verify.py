#!/usr/bin/env python3
"""Primary exact and numerical verifier for provisional C-QBL-004."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline
import sympy as sp

from substrate_framework.exact_sine_qball import exact_sine_qball_residual
from substrate_framework.numerics import NumericalFailure
from substrate_framework.radial_qball import (
    fit_radial_tail_rate,
    radial_qball_observables,
    radial_tail_rate,
    shoot_radial_qball,
    shooting_observables,
    smooth_complex_potential,
    smooth_complex_potential_derivative,
    solve_radial_qball_bvp,
    symbolic_radial_charge_density,
    symbolic_radial_energy_density,
    symbolic_radial_profile_residual,
    symbolic_radial_reduced_lagrangian,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-41/"
    "bridge_GK3D5_charged_excitation_exists_in_3D.py"
)
PINS = {
    "source": "201d4fd2594a73c7b59dbe81e0e66f1d3d43a52605a26174c70bd072626992e2",
    "release": "fbb97885d564d6dc57c8b5bdf37cd619484a4f361545ea4ae198917de6b2ed05",
    "freeze": "c4312c463d5e84f5059d0221798dc496c993aa747e156a8a86606b8b6bf2a574",
    "module": "ba41ec4f5ba26e1db7607c59438520c0def109dffaad3b3b60a4404b63fc80c9",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_change(left: float, right: float) -> float:
    return abs(left - right) / abs(right)


def main() -> int:
    checks = CheckLedger("P202-GK3D5-PRIMARY")
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)
    checks.check("source is hash pinned", digest(SOURCE) == PINS["source"])
    checks.check(
        "base release is hash pinned",
        digest(ROOT / "governance/releases/v0.149.0.yaml") == PINS["release"],
    )
    checks.check(
        "formula freeze is hash pinned",
        digest(CAMPAIGN / "evidence/formula-freeze.yaml") == PINS["freeze"],
    )
    checks.check(
        "canonical radial API is hash pinned",
        digest(ROOT / "src/substrate_framework/radial_qball.py") == PINS["module"],
    )

    source_calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check("source inventory has thirteen static check sites", len(source_calls) == 13)
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "immutable integration fallback is classified without scientific failure",
        compatibility.dynamic_current_getattrs == 1
        and compatibility.direct_legacy_attributes == 1
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    rho = sp.symbols("rho", nonnegative=True)
    potential_series = sp.series(smooth_complex_potential(rho), rho, 0, 4)
    checks.check(
        "smooth complex potential has the frozen analytic series",
        potential_series
        == rho / 2 - rho**2 / 24 + rho**3 / 720 + sp.Order(rho**4),
    )
    checks.check(
        "potential derivative has removable one-half origin limit",
        smooth_complex_potential_derivative(sp.Integer(0)) == sp.Rational(1, 2)
        and sp.limit(sp.sin(sp.sqrt(rho)) / (2 * sp.sqrt(rho)), rho, 0, dir="+")
        == sp.Rational(1, 2),
    )

    radius = sp.symbols("r", positive=True)
    omega = sp.symbols("omega", positive=True)
    profile = sp.Function("f")(radius)
    reduced = symbolic_radial_reduced_lagrangian(radius, profile, omega)
    variation = sp.diff(sp.diff(reduced, sp.diff(profile, radius)), radius) - sp.diff(
        reduced, profile
    )
    residual = symbolic_radial_profile_residual(radius, profile, omega)
    checks.check(
        "radial equation follows from the declared action normalization",
        sp.simplify(variation / (-2 * radius**2) - residual) == 0,
    )
    checks.check(
        "charge and energy densities use one consistent current convention",
        symbolic_radial_charge_density(radius, profile, omega)
        == 2 * omega * radius**2 * profile**2
        and symbolic_radial_energy_density(radius, profile, omega)
        == radius**2
        * (
            omega**2 * profile**2
            + sp.diff(profile, radius) ** 2
            + 1
            - sp.cos(profile)
        ),
    )

    center, coefficient = sp.symbols("a b", real=True)
    trial = center + coefficient * radius**2
    origin_limit = sp.limit(
        symbolic_radial_profile_residual(radius, trial, omega), radius, 0, dir="+"
    )
    checks.check(
        "regular-origin series coefficient is force divided by six",
        sp.solve(sp.Eq(origin_limit, 0), coefficient)
        == [sp.sin(center) / 12 - center * omega**2 / 6],
    )
    epsilon, amplitude = sp.symbols("epsilon amplitude", positive=True)
    linear_force = sp.expand(
        sp.series(
            sp.sin(epsilon * amplitude) / 2 - omega**2 * epsilon * amplitude,
            epsilon,
            0,
            3,
        ).removeO()
    ).coeff(epsilon)
    checks.check(
        "small-amplitude tail has the frozen localization gap",
        sp.simplify(linear_force - (sp.Rational(1, 2) - omega**2) * amplitude)
        == 0,
    )
    kappa, constant, wall = sp.symbols("kappa constant wall", positive=True)
    tail = constant * sp.exp(-kappa * radius) / radius
    checks.check(
        "exponential radial tail has finite norm beyond any positive wall",
        sp.integrate(radius**2 * tail**2, (radius, wall, sp.oo))
        == constant**2 * sp.exp(-2 * kappa * wall) / (2 * kappa),
    )
    gradient, effective, scale = sp.symbols(
        "gradient effective scale", positive=True
    )
    scaled_stationary = scale * gradient + scale**3 * effective
    checks.check(
        "three-dimensional scaling gives the Pohozaev identity",
        sp.diff(scaled_stationary, scale).subs(scale, 1)
        == gradient + 3 * effective,
    )
    one_dimensional = exact_sine_qball_residual(profile, radius, omega)
    checks.check(
        "accepted one-dimensional profile is not a three-dimensional lift",
        sp.simplify(residual - one_dimensional)
        == 2 * sp.diff(profile, radius) / radius,
    )

    configs = (
        (20.0, 1001, 1.0e-6),
        (30.0, 2001, 1.0e-8),
        (40.0, 4001, 1.0e-8),
    )
    solutions = [
        solve_radial_qball_bvp(
            frequency=0.5,
            outer_radius=outer_radius,
            initial_mesh_points=points,
            tolerance=tolerance,
        )
        for outer_radius, points, tolerance in configs
    ]
    observables = [radial_qball_observables(solution) for solution in solutions]
    checks.check(
        "every collocation level closes solver residual and boundary gates",
        all(
            solution.evidence.max_rms_residual <= 1.0e-6
            and solution.maximum_boundary_residual < 1.0e-8
            and solution.off_grid_ode_residual_max_abs < 1.0e-7
            for solution in solutions
        ),
    )
    checks.check(
        "collocation levels remain nontrivial nodeless and monotone",
        all(
            np.all(
                solution.state_at(
                    np.linspace(
                        solution.origin_epsilon,
                        min(18.0, solution.outer_radius - 1.0),
                        4001,
                    )
                )[0]
                > 0.0
            )
            and np.all(
                solution.state_at(
                    np.linspace(
                        solution.origin_epsilon,
                        min(18.0, solution.outer_radius - 1.0),
                        4001,
                    )
                )[1]
                < 0.0
            )
            for solution in solutions
        ),
    )
    core = np.linspace(1.0e-6, 10.0, 4001)
    core_errors = [
        float(
            np.max(
                np.abs(left.state_at(core)[0] - right.state_at(core)[0])
            )
            / np.max(np.abs(right.state_at(core)[0]))
        )
        for left, right in zip(solutions, solutions[1:])
    ]
    checks.check(
        "domain refinement decreases core profile error below the frozen gate",
        core_errors[1] < core_errors[0] and core_errors[1] < 1.0e-3,
    )
    checks.check(
        "radius thirty to forty closes charge and energy refinement",
        relative_change(observables[1].energy, observables[2].energy) < 1.0e-3
        and relative_change(
            observables[1].noether_charge, observables[2].noether_charge
        )
        < 1.0e-3,
    )
    checks.check(
        "fine branch closes the Pohozaev and analytic tail gates",
        observables[2].normalized_pohozaev_residual < 1.0e-4
        and relative_change(
            fit_radial_tail_rate(
                solutions[2], fit_start=8.0, fit_stop=16.0
            ),
            radial_tail_rate(0.5),
        )
        < 0.05,
    )

    shooting = shoot_radial_qball(
        frequency=0.5,
        central_bracket=(6.1, 6.125),
        outer_radius=20.0,
        sample_points=12_001,
    )
    shooting_values = shooting_observables(shooting)
    checks.check(
        "independent shooting closes root positivity and monotonicity gates",
        shooting.root_converged
        and abs(shooting.robin_residual) < 1.0e-8
        and np.all(shooting.ivp.state[0] > 0.0)
        and np.all(shooting.ivp.state[1] < 0.0),
    )
    checks.check(
        "collocation and shooting agree in center charge and energy",
        relative_change(shooting.central_amplitude, solutions[0].central_amplitude)
        < 2.0e-3
        and relative_change(shooting_values.energy, observables[0].energy) < 2.0e-3
        and relative_change(
            shooting_values.noether_charge, observables[0].noether_charge
        )
        < 2.0e-3,
    )

    fine = solutions[1]
    probe_radius = np.linspace(0.1, 10.0, 3001)
    spline = CubicSpline(fine.evidence.coordinate, fine.evidence.state, axis=1)
    probe_state = np.asarray(spline(probe_radius), dtype=np.float64)
    probe_derivative = np.asarray(spline(probe_radius, 1), dtype=np.float64)

    def coefficient_verdict(candidate: object) -> bool:
        geometry, sine_coefficient, frequency_coefficient = candidate  # type: ignore[misc]
        f, fp = probe_state
        residual_values = (
            probe_derivative[1]
            + float(geometry) * fp / probe_radius
            - float(sine_coefficient) * np.sin(f)
            + float(frequency_coefficient) * 0.25 * f
        )
        return float(np.max(np.abs(residual_values))) < 1.0e-6

    checks.mutation_sensitive(
        "profile oracle depends on geometry force and frequency",
        coefficient_verdict,
        (2.0, 0.5, 1.0),
        [(0.0, 0.5, 1.0), (2.0, 1.0, 1.0), (2.0, 0.5, 0.0)],
    )

    zero_rejected = False
    try:
        solve_radial_qball_bvp(
            frequency=0.5,
            outer_radius=10.0,
            initial_mesh_points=101,
            tolerance=1.0e-5,
            central_guess=1.0e-10,
        )
    except NumericalFailure as error:
        zero_rejected = "trivial branch" in str(error)
    checks.check("trivial collocation branch is rejected explicitly", zero_rejected)

    truncated = solve_radial_qball_bvp(
        frequency=0.5,
        outer_radius=8.0,
        initial_mesh_points=801,
        tolerance=1.0e-7,
    )
    truncated_values = radial_qball_observables(truncated, quadrature_points=10_001)
    checks.check(
        "premature domain truncation fails physical convergence gates",
        truncated_values.normalized_pohozaev_residual > 1.0e-2
        and relative_change(truncated_values.energy, observables[2].energy) > 1.0e-2,
    )
    checks.check(
        "claim ceiling excludes quantum loop and particle identifications",
        "does not quantize the branch"
        in (ROOT / "src/substrate_framework/radial_qball.py").read_text(
            encoding="utf-8"
        )
        and "no_quantization_or_asymptotic_particle_state"
        in (CAMPAIGN / "evidence/numerical-construction.yaml").read_text(
            encoding="utf-8"
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
