#!/usr/bin/env python3
"""Primary exact and numeric verifier for TX1/C-RMOM-001/002."""

from __future__ import annotations

import ast
import hashlib
import math
from pathlib import Path

import numpy as np
from scipy.integrate import simpson
import sympy as sp

from substrate_framework.numerics import (
    SolverTolerances,
    solve_bvp_evidence,
)
from substrate_framework.rational_map_moments import (
    degree_one_rational_map_angular_stf_moments,
    degree_two_axial_rational_map_angular_stf_moments,
    degree_two_profile_intrinsic_moments,
    factorized_rational_map_energy_moments,
    rational_map_local_energy_density,
)
from substrate_framework.rational_map_radial import (
    rational_map_radial_energy_density,
    solve_rational_map_radial_profile,
)
from substrate_framework.rational_maps import axial_rational_map_angular_integral
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P180-tx1-intrinsic-quadrupole-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-40/"
    "bridge_TX1_b2_intrinsic_quadrupole.py"
)
SOURCE_SHA256 = "30161731af4e3ffda219adbdc7af9db66f6829fbbd3736a3198ed19a644ac8ff"
RELEASE_SHA256 = "f3b8587555ca99523213519a2296849978437491566b587bafa554b24d23acf1"
ANGULAR_TWO = float(axial_rational_map_angular_integral(2))


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _solve(
    *,
    inner_radius: float = 1e-4,
    outer_radius: float = 24.0,
    sample_points: int = 2401,
    rtol: float = 3e-10,
    max_step: float = 0.05,
):
    return solve_rational_map_radial_profile(
        2,
        ANGULAR_TWO,
        inner_radius=inner_radius,
        outer_radius=outer_radius,
        sample_points=sample_points,
        tolerances=SolverTolerances(
            rtol=rtol,
            atol=max(1e-13, rtol * 0.01),
            max_step=max_step,
        ),
    )


def _profile_gate(profile: object, moment: object) -> bool:
    return bool(
        np.all(np.isfinite(profile.field))
        and np.all(np.isfinite(profile.radial_derivative))
        and abs(profile.inner_boundary_residual) < 2e-11
        and abs(profile.outer_boundary_residual) < 2e-7
        and np.max(np.diff(profile.field)) < 2e-7
        and moment.profile_energy_closure_relative_error < 2e-11
        and moment.normalized_axial_ratio < -0.1
    )


def _axis_values(profiles: list[object]) -> list[float]:
    return [degree_two_profile_intrinsic_moments(item).normalized_axial_ratio for item in profiles]


def _finest_pair_relative(values: list[float]) -> float:
    return abs(values[-1] - values[-2]) / max(abs(values[-1]), 1e-30)


def _independent_collocation_moment() -> dict[str, float]:
    degree = 2
    inner = 1e-4
    outer = 24.0
    tolerance = 3e-7
    sigma = (math.sqrt(1 + 8 * degree) - 1) / 2
    tail_power = sigma + 1
    inner_points = 200
    mesh = np.concatenate(
        (
            np.geomspace(inner, 0.25, inner_points, endpoint=False),
            np.linspace(0.25, outer, 401),
        )
    )
    width = 1 + math.sqrt(degree)
    scaled = (mesh / width) ** sigma
    field_guess = np.pi * (1 + scaled) ** (-tail_power / sigma)
    derivative_guess = -tail_power * field_guess * scaled / (mesh * (1 + scaled))

    def equations(radius: np.ndarray, state: np.ndarray) -> np.ndarray:
        field, derivative = state
        sine = np.sin(field)
        sine_twice = np.sin(2 * field)
        second = (
            -2 * radius * derivative
            - degree * sine_twice * (derivative**2 - 1)
            + ANGULAR_TWO * sine_twice * sine**2 / radius**2
        ) / (radius**2 + 2 * degree * sine**2)
        return np.vstack((derivative, second))

    def boundary(left: np.ndarray, right: np.ndarray) -> np.ndarray:
        return np.asarray(
            (
                inner * left[1] + sigma * (np.pi - left[0]),
                outer * right[1] + tail_power * right[0],
            )
        )

    solution = solve_bvp_evidence(
        equations,
        boundary,
        mesh,
        np.vstack((field_guess, derivative_guess)),
        tolerance=tolerance,
        bc_tol=3e-8,
        max_nodes=50_000,
    )
    radius = solution.coordinate
    field, derivative = solution.state
    sine_squared = np.sin(field) ** 2
    m0 = float(simpson(radius**2 * derivative**2, x=radius))
    m1 = float(simpson(2 * sine_squared * (1 + derivative**2), x=radius))
    m2 = float(simpson(sine_squared**2 / radius**2, x=radius))
    h1 = float(simpson(2 * radius**2 * sine_squared * (1 + derivative**2), x=radius))
    h2 = float(simpson(sine_squared**2, x=radius))

    amplitude = float((np.pi - field[0]) / inner**sigma)
    tail_amplitude = float(field[-1] * outer**tail_power)
    m0 += amplitude**2 * sigma**2 * inner ** (2 * sigma + 1) / (2 * sigma + 1)
    m1 += (
        2 * amplitude**2 * inner ** (2 * sigma + 1) / (2 * sigma + 1)
        + 2 * amplitude**4 * sigma**2 * inner ** (4 * sigma - 1) / (4 * sigma - 1)
    )
    m2 += amplitude**4 * inner ** (4 * sigma - 1) / (4 * sigma - 1)
    h1 += (
        2 * amplitude**2 * inner ** (2 * sigma + 3) / (2 * sigma + 3)
        + 2 * amplitude**4 * sigma**2 * inner ** (4 * sigma + 1) / (4 * sigma + 1)
    )
    h2 += amplitude**4 * inner ** (4 * sigma + 1) / (4 * sigma + 1)
    m0 += tail_power**2 * tail_amplitude**2 * outer ** (1 - 2 * tail_power) / (2 * tail_power - 1)
    m1 += (
        2 * tail_amplitude**2 * outer ** (1 - 2 * tail_power) / (2 * tail_power - 1)
        + 2
        * tail_power**2
        * tail_amplitude**4
        * outer ** (-4 * tail_power - 1)
        / (4 * tail_power + 1)
    )
    m2 += tail_amplitude**4 * outer ** (-4 * tail_power - 1) / (4 * tail_power + 1)
    h1 += (
        2 * tail_amplitude**2 * outer ** (3 - 2 * tail_power) / (2 * tail_power - 3)
        + 2
        * tail_power**2
        * tail_amplitude**4
        * outer ** (1 - 4 * tail_power)
        / (4 * tail_power - 1)
    )
    h2 += tail_amplitude**4 * outer ** (1 - 4 * tail_power) / (4 * tail_power - 1)

    a1zz = 8 * np.pi * (3 * np.pi - 10) / 3
    a2zz = 8 * np.pi * (3 * np.pi - 16) / 9
    monopole = 4 * np.pi * (m0 + 2 * m1 + ANGULAR_TWO * m2)
    axial = a1zz * h1 + a2zz * h2
    boundary_residual = float(
        np.max(np.abs(boundary(solution.state[:, 0], solution.state[:, -1])))
    )
    return {
        "ratio": axial / monopole,
        "boundary_residual": boundary_residual,
        "max_rms_residual": solution.max_rms_residual,
        "monopole": monopole,
        "axial": axial,
    }


def main() -> int:
    checks = CheckLedger("P180/TX1/C-RMOM-001/002")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.131.0.yaml") == RELEASE_SHA256,
    )
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    lexical_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("source lexical and assertion inventory is exact", len(lexical_checks) == 9 and len(assertions) == 2)
    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check(
        "immutable NumPy dispatch is isolated compatibility evidence",
        compatibility.direct_current_attributes == 1
        and compatibility.direct_legacy_attributes == 1
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    field, derivative = sp.symbols("f fp", real=True)
    radius, jacobian, degree, angular_integral = sp.symbols("r J B I", positive=True)
    local = rational_map_local_energy_density(field, derivative, radius, jacobian)
    polynomial = sp.Poly(sp.expand(radius**2 * local), jacobian)
    averaged = (
        polynomial.coeff_monomial(1)
        + degree * polynomial.coeff_monomial(jacobian)
        + angular_integral * polynomial.coeff_monomial(jacobian**2)
    )
    accepted = rational_map_radial_energy_density(
        field,
        derivative,
        radius,
        degree,
        angular_integral,
    )
    checks.check("local density reduces exactly to C-RPROF-001", sp.simplify(averaged - accepted) == 0)

    one = degree_one_rational_map_angular_stf_moments()
    checks.check("degree-one angular density has an exact STF null", one.linear_stf == sp.zeros(3) and one.quadratic_stf == sp.zeros(3))
    two = degree_two_axial_rational_map_angular_stf_moments()
    u = next(iter(two.conformal_jacobian.free_symbols))
    direct_mean = sp.integrate(two.conformal_jacobian, (u, -1, 1)) / 2
    direct_square = sp.integrate(two.conformal_jacobian**2, (u, -1, 1)) / 2
    checks.check("degree-two sphere means are exact", sp.simplify(direct_mean - 2) == 0 and sp.simplify(direct_square - sp.pi - sp.Rational(8, 3)) == 0)
    checks.check(
        "degree-two angular STF tensors are exact and negative on axis",
        sp.simplify(sp.trace(two.linear_stf)) == 0
        and sp.simplify(sp.trace(two.quadratic_stf)) == 0
        and two.linear_stf[2, 2].is_negative is True
        and two.quadratic_stf[2, 2].is_negative is True,
    )
    h1, h2 = sp.symbols("H1 H2", positive=True)
    symbolic = factorized_rational_map_energy_moments(
        two,
        isotropic_monopole_radial=1,
        linear_monopole_radial=1,
        quadratic_monopole_radial=1,
        linear_second_radial=h1,
        quadratic_second_radial=h2,
    )
    checks.check(
        "factorization fixes oblate axial form and convention",
        symbolic.normalized_stf[2, 2].is_negative is True
        and symbolic.normalized_stf[0, 0].is_positive is True
        and sp.simplify(symbolic.normalized_stf[0, 0] + symbolic.normalized_stf[2, 2] / 2) == 0
        and sp.simplify(symbolic.triple_normalized_quadrupole - 3 * symbolic.normalized_stf) == sp.zeros(3),
    )
    without_squared = sp.simplify(h1 * two.linear_stf)
    checks.check(
        "load-bearing Nc-squared term mutation changes the tensor",
        sp.simplify(symbolic.normalized_stf - without_squared) != sp.zeros(3),
    )
    outer, field_at_outer, tail_exponent = sp.symbols("R f_R p", positive=True)
    source_tail = field_at_outer**4 * outer / (4 * tail_exponent + 1)
    correct_tail = field_at_outer**4 / (outer * (4 * tail_exponent + 1))
    checks.check("source monopole tail mutation differs by R squared", sp.simplify(source_tail / correct_tail - outer**2) == 0)

    baseline_profile = _solve()
    baseline = degree_two_profile_intrinsic_moments(baseline_profile)
    checks.check("canonical corrected branch passes solver and moment gates", _profile_gate(baseline_profile, baseline))
    checks.check(
        "canonical tensor is diagonal traceless and convention complete",
        abs(float(np.trace(baseline.normalized_stf))) < 2e-12
        and np.max(np.abs(baseline.normalized_stf - np.diag(np.diag(baseline.normalized_stf)))) < 2e-12
        and np.allclose(baseline.triple_normalized_quadrupole, 3 * baseline.normalized_stf, rtol=2e-15, atol=2e-13),
    )

    axes = {
        "outer": [_solve(outer_radius=value) for value in (16.0, 24.0, 32.0, 48.0)],
        "inner": [_solve(inner_radius=value) for value in (2e-4, 1e-4, 5e-5)],
        "samples": [_solve(sample_points=value) for value in (1201, 2401, 4801)],
        "tolerance": [_solve(rtol=value) for value in (1e-8, 3e-10, 1e-11)],
        "max_step": [_solve(max_step=value) for value in (0.1, 0.05, 0.025)],
    }
    axis_results: dict[str, list[float]] = {}
    for name, profiles in axes.items():
        moments = [degree_two_profile_intrinsic_moments(profile) for profile in profiles]
        values = [item.normalized_axial_ratio for item in moments]
        axis_results[name] = values
        checks.check(
            f"{name} refinement passes its frozen gate",
            all(_profile_gate(profile, moment) for profile, moment in zip(profiles, moments))
            and _finest_pair_relative(values) < 3e-6,
            repr(values),
        )

    independent = _independent_collocation_moment()
    relative_method_difference = abs(independent["ratio"] - baseline.normalized_axial_ratio) / abs(baseline.normalized_axial_ratio)
    checks.check(
        "fresh collocation and Simpson route passes independently",
        independent["boundary_residual"] < 3e-8
        and independent["max_rms_residual"] <= 3.05e-7
        and independent["ratio"] < -0.1,
        repr(independent),
    )
    checks.check(
        "canonical and independent moments agree within frozen tolerance",
        relative_method_difference < 2e-6,
        f"relative difference={relative_method_difference:.3e}",
    )
    checks.check(
        "static moment is not a radiation verdict",
        sp.diff(symbolic.normalized_stf, sp.Symbol("t"), 3) == sp.zeros(3),
    )

    print(
        "NUMERIC BASELINE "
        f"M={baseline.monopole:.12f} "
        f"I_STF_zz={baseline.normalized_stf[2,2]:.12f} "
        f"I_STF_zz/M={baseline.normalized_axial_ratio:.12f} "
        f"Q_zz/M={baseline.triple_axial_ratio:.12f}"
    )
    print(
        "INDEPENDENT "
        f"M={independent['monopole']:.12f} "
        f"I_STF_zz={independent['axial']:.12f} "
        f"I_STF_zz/M={independent['ratio']:.12f}"
    )
    for name, values in axis_results.items():
        print(f"AXIS {name} {values}")
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
