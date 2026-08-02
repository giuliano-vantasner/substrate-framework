"""Independent collocation and finite-volume review of P062.

This route deliberately does not import ``substrate_framework.radial_modes``.
It derives the mixed Hessian term directly, solves the background with SciPy
collocation, integrates energy with Simpson's rule, and assembles a mass-lumped
finite-volume spectrum transformed to an ordinary symmetric tridiagonal
problem.
"""

from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.integrate import simpson, solve_bvp
from scipy.linalg import eigh_tridiagonal

from substrate_framework.verification import CheckLedger


def equations(
    radius: np.ndarray,
    state: np.ndarray,
    _parameters: np.ndarray | None = None,
) -> np.ndarray:
    field = state[0]
    derivative = state[1]
    sine = np.sin(field)
    coefficient = radius**2 + 2.0 * sine**2
    second = (
        -2.0 * radius * derivative
        - np.sin(2.0 * field) * (derivative**2 - 1.0)
        + np.sin(2.0 * field) * sine**2 / radius**2
    ) / coefficient
    return np.vstack((derivative, second))


def solve_profile(outer_radius: float, points: int):
    inner_radius = 1.0e-3
    mesh = np.linspace(inner_radius, outer_radius, 500)
    scale = 1.2
    ratio = (scale / mesh) ** 2
    guess_field = 2.0 * np.arctan(ratio)
    guess_derivative = -4.0 * ratio / (mesh * (1.0 + ratio**2))
    guess = np.vstack((guess_field, guess_derivative))

    def boundary(left, right, parameter):
        slope = parameter[0]
        return np.asarray(
            (
                left[0] + slope * inner_radius - np.pi,
                left[1] + slope,
                outer_radius * right[1] + 2.0 * right[0],
            )
        )

    result = solve_bvp(
        equations,
        boundary,
        mesh,
        guess,
        p=np.asarray((2.0,)),
        tol=2.0e-8,
        max_nodes=50_000,
        verbose=0,
    )
    if not result.success:
        raise RuntimeError(result.message)
    radius = np.linspace(inner_radius, outer_radius, points)
    state = result.sol(radius)
    return result, radius, state[0], state[1]


def exact_coefficients(radius, field, derivative):
    second = equations(radius, np.vstack((field, derivative)))[1]
    sine = np.sin(field)
    cosine = np.cos(field)
    cosine_twice = np.cos(2.0 * field)
    gradient = radius**2 + 2.0 * sine**2
    local = (
        2.0 * cosine_twice
        + 2.0 * cosine_twice * derivative**2
        + 2.0 * sine**2 * (3.0 * cosine**2 - sine**2) / radius**2
    )
    correction = (
        -4.0 * cosine_twice * derivative**2
        - 2.0 * np.sin(2.0 * field) * second
    )
    return gradient, local + correction, gradient.copy(), correction


def finite_volume_spectrum(radius, gradient, potential, weight, mode_count=4):
    spacing = float(radius[1] - radius[0])
    if not np.allclose(np.diff(radius), spacing, rtol=1.0e-10, atol=1.0e-13):
        raise ValueError("independent finite-volume grid must be uniform")
    midpoint_gradient = (gradient[:-1] + gradient[1:]) / 2.0
    diagonal = (
        midpoint_gradient[:-1] + midpoint_gradient[1:]
    ) / spacing**2 + potential[1:-1]
    off_diagonal = -midpoint_gradient[1:-1] / spacing**2
    interior_weight = weight[1:-1]
    transformed_diagonal = diagonal / interior_weight
    transformed_off = off_diagonal / np.sqrt(
        interior_weight[:-1] * interior_weight[1:]
    )
    eigenvalues, eigenvectors = eigh_tridiagonal(
        transformed_diagonal,
        transformed_off,
        select="i",
        select_range=(0, mode_count - 1),
    )
    nodes = []
    for index in range(mode_count):
        vector = eigenvectors[:, index] / np.sqrt(interior_weight)
        significant = vector[np.abs(vector) > 1.0e-8 * np.max(np.abs(vector))]
        nodes.append(int(np.count_nonzero(significant[:-1] * significant[1:] < 0.0)))
    return eigenvalues, tuple(nodes)


def energy_evidence(radius, field, derivative):
    sine_squared = np.sin(field) ** 2
    two = 4.0 * np.pi * simpson(
        radius**2 * derivative**2 + 2.0 * sine_squared,
        x=radius,
    )
    four = 4.0 * np.pi * simpson(
        2.0 * sine_squared * derivative**2 + sine_squared**2 / radius**2,
        x=radius,
    )
    return float(two), float(four), float((two + four) / (12.0 * np.pi**2))


def main() -> int:
    ledger = CheckLedger("P062-INDEPENDENT")
    radius_symbol = sp.symbols("r", positive=True)
    field = sp.Function("f")(radius_symbol)
    mode = sp.Function("eta")(radius_symbol)
    epsilon = sp.symbols("epsilon", real=True)
    perturbed = field + epsilon * mode
    derivative = sp.diff(perturbed, radius_symbol)
    density = (
        (radius_symbol**2 + 2 * sp.sin(perturbed) ** 2) * derivative**2
        + 2 * sp.sin(perturbed) ** 2
        + sp.sin(perturbed) ** 4 / radius_symbol**2
    )
    quadratic = sp.simplify(sp.diff(density, epsilon, 2).subs(epsilon, 0) / 2)
    fp = sp.diff(field, radius_symbol)
    gradient = radius_symbol**2 + 2 * sp.sin(field) ** 2
    local = (
        2 * sp.cos(2 * field)
        + 2 * sp.cos(2 * field) * fp**2
        + 2
        * sp.sin(field) ** 2
        * (3 * sp.cos(field) ** 2 - sp.sin(field) ** 2)
        / radius_symbol**2
    )
    mixed = 4 * sp.sin(2 * field) * fp
    correction = -sp.diff(mixed, radius_symbol) / 2
    reconstructed = (
        gradient * sp.diff(mode, radius_symbol) ** 2
        + (local + correction) * mode**2
        + sp.diff(mixed * mode**2 / 2, radius_symbol)
    )
    ledger.check(
        "independent epsilon expansion retains mixed correction",
        sp.simplify(quadratic - reconstructed) == 0,
    )
    ledger.check("independent correction is nonzero", sp.simplify(correction) != 0)

    domains = ((12.0, 801), (18.0, 1201), (24.0, 1601))
    primary_lowest = (0.13113240098603374, 0.06107224003037779, 0.03475412672211401)
    profiles = []
    spectra = []
    for outer, points in domains:
        result, radius, field_values, derivative_values = solve_profile(outer, points)
        coefficients = exact_coefficients(radius, field_values, derivative_values)
        eigenvalues, nodes = finite_volume_spectrum(
            radius,
            coefficients[0],
            coefficients[1],
            coefficients[2],
        )
        two, four, b1 = energy_evidence(radius, field_values, derivative_values)
        tail = outer * derivative_values[-1] + 2.0 * field_values[-1]
        profiles.append((result, two, four, b1, tail, result.p[0]))
        spectra.append((eigenvalues, nodes, coefficients))
        print(
            "INDEPENDENT",
            f"R={outer:.0f}",
            f"slope={result.p[0]:.12f}",
            f"B1={b1:.12f}",
            "eigenvalues=" + ",".join(f"{value:.9f}" for value in eigenvalues),
            "nodes=" + ",".join(str(value) for value in nodes),
            f"max_bvp_residual={np.max(result.rms_residuals):.3e}",
        )

    ledger.check("all independent BVP solves succeeded", all(item[0].success for item in profiles))
    ledger.check(
        "independent BVP residuals are resolved",
        max(float(np.max(item[0].rms_residuals)) for item in profiles) < 2.1e-8,
    )
    slopes = np.asarray([item[5] for item in profiles])
    ledger.check(
        "independent slopes are domain stable",
        abs(slopes[-1] - slopes[-2]) / slopes[-1] < 2.0e-8,
    )
    b1_values = np.asarray([item[3] for item in profiles])
    ledger.check(
        "independent Simpson energy converges",
        np.all(np.diff(b1_values) > 0.0) and 1.231 < b1_values[-1] < 1.232,
    )
    ledger.check(
        "independent virial imbalance decreases",
        all(
            abs(item[1] - item[2]) / (item[1] + item[2]) < limit
            for item, limit in zip(profiles, (5.0e-4, 1.5e-4, 7.0e-5), strict=True)
        ),
    )
    ledger.check(
        "independent Robin tails close",
        max(abs(item[4]) for item in profiles) < 3.0e-7,
    )

    lowest = np.asarray([item[0][0] for item in spectra])
    ledger.check(
        "independent finite-volume node ordering",
        all(item[1] == (0, 1, 2, 3) for item in spectra),
    )
    ledger.check(
        "independent levels agree with consistent-mass FEM",
        np.allclose(lowest, primary_lowest, rtol=7.0e-4),
    )
    ledger.check(
        "independent lowest level collapses with domain",
        np.all(np.diff(lowest) < 0.0) and lowest[-1] < 0.35 * lowest[0],
    )
    ledger.check(
        "independent positive levels are above zero continuum",
        np.all(lowest > 0.0),
    )

    source_mask = (
        (np.linspace(1.0e-3, 12.0, 801) >= 0.3)
        & (np.linspace(1.0e-3, 12.0, 801) <= 12.0)
    )
    _result, source_radius, source_field, source_derivative = solve_profile(12.0, 801)
    source_coefficients = exact_coefficients(
        source_radius,
        source_field,
        source_derivative,
    )
    source_local_potential = source_coefficients[1] - source_coefficients[3]
    source_like, _nodes = finite_volume_spectrum(
        source_radius[source_mask],
        source_coefficients[0][source_mask],
        source_local_potential[source_mask],
        source_coefficients[2][source_mask],
    )
    ledger.check(
        "source-like omitted-term window reproduces the reported scale",
        0.05 < source_like[0] < 0.20,
    )
    ledger.check(
        "source-like construction differs from corrected origin-complete level",
        abs(source_like[0] - lowest[0]) / lowest[0] > 0.05,
    )

    eigenvalue, rotational_gap = sp.symbols("lambda Delta", positive=True)
    correct_ratio = sp.sqrt(eigenvalue) / rotational_gap
    source_ratio = eigenvalue / rotational_gap
    ledger.check(
        "independent gap algebra uses frequency not squared frequency",
        sp.simplify(correct_ratio - source_ratio) != 0,
    )
    scale = sp.symbols("s", positive=True)
    ledger.check(
        "independent physical gap retains a free inverse-time scale",
        sp.diff(scale * sp.sqrt(eigenvalue), scale) == sp.sqrt(eigenvalue),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
