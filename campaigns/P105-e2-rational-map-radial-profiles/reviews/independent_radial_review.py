"""Independent P105 derivation and collocation without the canonical radial API."""

from __future__ import annotations

import ast
import math
from pathlib import Path

import numpy as np
from scipy.integrate import simpson
import sympy as sp

from substrate_framework.numerics import solve_bvp_evidence
from substrate_framework.verification import CheckLedger


def _endpoint_powers(degree: int) -> tuple[float, float]:
    root = math.sqrt(1.0 + 8.0 * degree)
    return (root - 1.0) / 2.0, (root + 1.0) / 2.0


def _fresh_collocation(
    degree: int,
    angular_integral: float,
    *,
    inner: float = 1.0e-4,
    outer: float = 24.0,
    tolerance: float = 3.0e-7,
    mesh_points: int = 601,
) -> dict[str, object]:
    """Solve the declared equation from a two-power analytic initial guess."""

    sigma, tail_power = _endpoint_powers(degree)
    inner_points = max(80, mesh_points // 3)
    outer_points = mesh_points - inner_points
    mesh = np.concatenate(
        (
            np.geomspace(inner, 0.25, inner_points, endpoint=False),
            np.linspace(0.25, outer, outer_points),
        )
    )
    width = 1.0 + math.sqrt(float(degree))
    scaled = (mesh / width) ** sigma
    field_guess = np.pi * (1.0 + scaled) ** (-tail_power / sigma)
    derivative_guess = (
        -tail_power * field_guess * scaled / (mesh * (1.0 + scaled))
    )

    def equations(radius: np.ndarray, state: np.ndarray) -> np.ndarray:
        field, derivative = state
        sine = np.sin(field)
        sine_twice = np.sin(2.0 * field)
        coefficient = radius**2 + 2.0 * degree * sine**2
        second = (
            -2.0 * radius * derivative
            - degree * sine_twice * (derivative**2 - 1.0)
            + angular_integral * sine_twice * sine**2 / radius**2
        ) / coefficient
        return np.vstack((derivative, second))

    def boundary(left: np.ndarray, right: np.ndarray) -> np.ndarray:
        return np.asarray(
            (
                inner * left[1] + sigma * (np.pi - left[0]),
                outer * right[1] + tail_power * right[0],
            )
        )

    evidence = solve_bvp_evidence(
        equations,
        boundary,
        mesh,
        np.vstack((field_guess, derivative_guess)),
        tolerance=tolerance,
        max_nodes=50_000,
        bc_tol=tolerance / 10.0,
    )
    radius = evidence.coordinate
    field, derivative = evidence.state
    sine_squared = np.sin(field) ** 2
    two_density = radius**2 * derivative**2 + 2.0 * degree * sine_squared
    four_density = (
        2.0 * degree * sine_squared * derivative**2
        + angular_integral * sine_squared**2 / radius**2
    )
    domain_two = 4.0 * np.pi * float(simpson(two_density, x=radius))
    domain_four = 4.0 * np.pi * float(simpson(four_density, x=radius))

    amplitude = float((np.pi - field[0]) / inner**sigma)
    tail_amplitude = float(field[-1] * outer**tail_power)
    origin_two = (
        4.0
        * np.pi
        * amplitude**2
        * (sigma**2 + 2.0 * degree)
        * inner ** (2.0 * sigma + 1.0)
        / (2.0 * sigma + 1.0)
    )
    origin_four = (
        4.0
        * np.pi
        * amplitude**4
        * (2.0 * degree * sigma**2 + angular_integral)
        * inner ** (4.0 * sigma - 1.0)
        / (4.0 * sigma - 1.0)
    )
    tail_two = (
        4.0
        * np.pi
        * tail_amplitude**2
        * (tail_power**2 + 2.0 * degree)
        * outer ** (1.0 - 2.0 * tail_power)
        / (2.0 * tail_power - 1.0)
    )
    tail_four = (
        4.0
        * np.pi
        * tail_amplitude**4
        * (2.0 * degree * tail_power**2 + angular_integral)
        * outer ** (-4.0 * tail_power - 1.0)
        / (4.0 * tail_power + 1.0)
    )
    two = domain_two + origin_two + tail_two
    four = domain_four + origin_four + tail_four
    return {
        "degree": degree,
        "angular_integral": angular_integral,
        "radius": radius,
        "field": field,
        "derivative": derivative,
        "inner_residual": float(boundary(evidence.state[:, 0], evidence.state[:, -1])[0]),
        "outer_residual": float(boundary(evidence.state[:, 0], evidence.state[:, -1])[1]),
        "max_rms_residual": evidence.max_rms_residual,
        "iterations": evidence.iterations,
        "energy_coefficient": (two + four) / (12.0 * np.pi**2),
        "per_degree": (two + four) / (12.0 * np.pi**2 * degree),
        "virial": abs(two - four) / (two + four),
    }


def main() -> int:
    checks = CheckLedger("C-RPROF-001/002-INDEPENDENT")
    radius = sp.symbols("r", positive=True)
    value, slope = sp.symbols("q p", real=True)
    degree, angular = sp.symbols("B I", positive=True)
    profile = sp.Function("f")(radius)
    density = (
        radius**2 * slope**2
        + 2 * degree * sp.sin(value) ** 2 * (1 + slope**2)
        + angular * sp.sin(value) ** 4 / radius**2
    )
    substitutions = {
        value: profile,
        slope: sp.diff(profile, radius),
    }
    direct_residual = sp.simplify(
        (
            sp.diff(sp.diff(density, slope).subs(substitutions), radius)
            - sp.diff(density, value).subs(substitutions)
        )
        / 2
    )
    displayed_residual = sp.simplify(
        (radius**2 + 2 * degree * sp.sin(profile) ** 2)
        * sp.diff(profile, radius, 2)
        + 2 * radius * sp.diff(profile, radius)
        + degree
        * sp.sin(2 * profile)
        * (sp.diff(profile, radius) ** 2 - 1)
        - angular * sp.sin(2 * profile) * sp.sin(profile) ** 2 / radius**2
    )
    checks.check(
        "fresh variation derives the generalized radial equation",
        sp.simplify(direct_residual - displayed_residual) == 0,
    )
    sigma = (sp.sqrt(1 + 8 * degree) - 1) / 2
    tail_power = (sp.sqrt(1 + 8 * degree) + 1) / 2
    checks.check(
        "fresh dominant-balance route satisfies both endpoint equations",
        sp.simplify(sigma * (sigma + 1) - 2 * degree) == 0
        and sp.simplify(tail_power * (tail_power - 1) - 2 * degree) == 0,
    )
    scale = sp.symbols("s", real=True)
    two, four = sp.symbols("E2 E4", positive=True)
    scaled = sp.exp(-scale) * two + sp.exp(scale) * four
    checks.check(
        "fresh scale differentiation gives the stationary virial identity",
        sp.diff(scaled, scale).subs(scale, 0) == four - two
        and sp.diff(scaled, scale, 2).subs(scale, 0) == two + four,
    )

    inputs = (
        (1, 1.0),
        (2, float(sp.pi + sp.Rational(8, 3))),
        (4, 20.6496264884189),
    )
    profiles = [_fresh_collocation(*item) for item in inputs]
    checks.check(
        "fresh collocation succeeds with finite monotone profiles",
        all(
            np.all(np.isfinite(result["field"]))
            and np.all(np.isfinite(result["derivative"]))
            and np.max(result["field"]) <= np.pi + 2.0e-7
            and np.min(result["field"]) >= -2.0e-7
            and np.max(result["derivative"]) < 2.0e-7
            for result in profiles
        ),
    )
    checks.check(
        "fresh collocation reports small equation and boundary residuals",
        all(
            result["max_rms_residual"] < 5.0e-7
            and abs(result["inner_residual"]) < 2.0e-8
            and abs(result["outer_residual"]) < 2.0e-8
            for result in profiles
        ),
    )
    checks.check(
        "fresh corrected-input branches satisfy the Derrick balance",
        max(float(result["virial"]) for result in profiles) < 5.0e-4,
    )
    per_degree = [float(result["per_degree"]) for result in profiles]
    checks.check(
        "fresh conditional per-degree energies decrease for the three declared branches",
        per_degree[0] > per_degree[1] > per_degree[2],
        f"per_degree={per_degree}",
    )

    degree_four_coarse = _fresh_collocation(
        4,
        20.6496264884189,
        tolerance=2.0e-6,
        mesh_points=401,
    )
    checks.check(
        "fresh degree-four collocation is tolerance and mesh stable",
        abs(
            float(degree_four_coarse["energy_coefficient"])
            - float(profiles[-1]["energy_coefficient"])
        )
        / float(profiles[-1]["energy_coefficient"])
        < 8.0e-5,
    )
    review_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    checks.check(
        "independent review imports no canonical rational radial implementation",
        all(
            not isinstance(node, ast.ImportFrom)
            or node.module != "substrate_framework.rational_map_radial"
            for node in ast.walk(review_tree)
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
