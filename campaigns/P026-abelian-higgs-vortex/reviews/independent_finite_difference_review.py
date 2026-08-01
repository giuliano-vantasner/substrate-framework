#!/usr/bin/env python3
"""Independent finite-difference and exact-convention review for P026."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import least_squares
from scipy.sparse import lil_matrix
import sympy as sp

from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class FiniteDifferenceVortex:
    radius: np.ndarray
    scalar: np.ndarray
    gauge: np.ndarray
    residual_norm: float
    tension: float


def solve_finite_difference(points: int) -> FiniteDifferenceVortex:
    """Solve the gauge-coupling-one equations without the package BVP code."""

    inner, outer = 1.0e-3, 12.0
    vacuum, winding, lam = 1.0, 1.0, 2.0
    radius = np.linspace(inner, outer, points)
    step = radius[1] - radius[0]
    interior = points - 2

    def unpack(unknown: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        scalar = np.empty(points)
        gauge = np.empty(points)
        scalar[0], scalar[-1] = 0.0, vacuum
        gauge[0], gauge[-1] = 0.0, winding
        scalar[1:-1] = unknown[:interior]
        gauge[1:-1] = unknown[interior:]
        return scalar, gauge

    def residual(unknown: np.ndarray) -> np.ndarray:
        scalar, gauge = unpack(unknown)
        r = radius[1:-1]
        scalar_prime = (scalar[2:] - scalar[:-2]) / (2.0 * step)
        scalar_second = (scalar[2:] - 2.0 * scalar[1:-1] + scalar[:-2]) / step**2
        gauge_prime = (gauge[2:] - gauge[:-2]) / (2.0 * step)
        gauge_second = (gauge[2:] - 2.0 * gauge[1:-1] + gauge[:-2]) / step**2
        scalar_residual = (
            scalar_second
            + scalar_prime / r
            - scalar[1:-1] * (winding - gauge[1:-1]) ** 2 / r**2
            - lam * scalar[1:-1] * (scalar[1:-1] ** 2 - vacuum**2)
        )
        gauge_residual = (
            gauge_second
            - gauge_prime / r
            + (winding - gauge[1:-1]) * scalar[1:-1] ** 2
        )
        return np.concatenate((scalar_residual, gauge_residual))

    sparsity = lil_matrix((2 * interior, 2 * interior), dtype=int)
    for index in range(interior):
        for neighbor in (index - 1, index, index + 1):
            if 0 <= neighbor < interior:
                sparsity[index, neighbor] = 1
                sparsity[interior + index, interior + neighbor] = 1
        sparsity[index, interior + index] = 1
        sparsity[interior + index, index] = 1

    scalar_guess = np.tanh(radius[1:-1])
    gauge_guess = 1.0 - np.exp(-radius[1:-1] ** 2)
    result = least_squares(
        residual,
        np.concatenate((scalar_guess, gauge_guess)),
        jac_sparsity=sparsity.tocsr(),
        xtol=1.0e-11,
        ftol=1.0e-11,
        gtol=1.0e-11,
        max_nfev=2000,
    )
    if not result.success:
        raise RuntimeError(f"finite-difference solve failed: {result.message}")
    scalar, gauge = unpack(result.x)
    scalar_prime = np.gradient(scalar, radius, edge_order=2)
    gauge_prime = np.gradient(gauge, radius, edge_order=2)
    density = (
        scalar_prime**2 / 2
        + scalar**2 * (winding - gauge) ** 2 / (2 * radius**2)
        + (gauge_prime / radius) ** 2 / 2
        + lam * (scalar**2 - vacuum**2) ** 2 / 4
    )
    tension = float(2.0 * np.pi * np.trapezoid(radius * density, radius))
    return FiniteDifferenceVortex(
        radius,
        scalar,
        gauge,
        float(np.max(np.abs(residual(result.x)))),
        tension,
    )


def run() -> int:
    checks = CheckLedger("P026-INDEPENDENT")

    radius = sp.symbols("r", positive=True)
    winding = sp.symbols("n", integer=True, positive=True)
    gauge_coupling, vacuum = sp.symbols("g v", positive=True)
    asymptotic = sp.symbols("a_infinity", real=True)
    log_coefficient = vacuum**2 * (winding - asymptotic) ** 2
    checks.check(
        "independent large-radius energy analysis uniquely fixes a infinity",
        sp.solve(sp.Eq(log_coefficient, 0), asymptotic) == [winding],
    )
    physical_connection = winding / (gauge_coupling * radius)
    flux = sp.integrate(
        physical_connection * radius,
        (sp.symbols("theta"), 0, 2 * sp.pi),
    )
    checks.check(
        "independent line integration gives two pi winding over coupling",
        sp.simplify(flux - 2 * sp.pi * winding / gauge_coupling) == 0,
    )

    solutions = [solve_finite_difference(points) for points in (101, 201, 401)]
    for points, solution in zip((101, 201, 401), solutions):
        print(
            f"FD N={points}: max_residual={solution.residual_norm:.3e} "
            f"tension={solution.tension:.9f}"
        )
    checks.check(
        "all three finite-difference nonlinear solves close their discrete residuals",
        all(solution.residual_norm < 1.0e-7 for solution in solutions),
    )
    checks.check(
        "independent profiles obey boundaries positivity and monotonicity",
        all(
            abs(solution.scalar[0]) < 1.0e-12
            and abs(solution.scalar[-1] - 1.0) < 1.0e-12
            and abs(solution.gauge[0]) < 1.0e-12
            and abs(solution.gauge[-1] - 1.0) < 1.0e-12
            and np.min(solution.scalar) >= -1.0e-9
            and np.max(solution.scalar) <= 1.0 + 1.0e-9
            and np.min(solution.gauge) >= -1.0e-9
            and np.max(solution.gauge) <= 1.0 + 1.0e-9
            and np.min(np.diff(solution.scalar)) >= -1.0e-8
            and np.min(np.diff(solution.gauge)) >= -1.0e-8
            for solution in solutions
        ),
    )
    errors = [abs(solution.tension - 4.2116046) for solution in solutions]
    checks.check(
        "finite-difference tension converges toward the collocation value",
        errors[2] < errors[1] < errors[0] and errors[2] < 3.0e-3,
    )

    fine = solutions[-1]
    scalar_mass = -np.polyfit(
        fine.radius[(fine.radius >= 4.0) & (fine.radius <= 8.0)],
        np.log(
            (1.0 - fine.scalar[(fine.radius >= 4.0) & (fine.radius <= 8.0)])
            * np.sqrt(fine.radius[(fine.radius >= 4.0) & (fine.radius <= 8.0)])
        ),
        1,
    )[0]
    checks.check(
        "independent scalar tail is consistent with the exact inverse length two",
        abs(scalar_mass - 2.0) < 0.15,
    )

    total = checks.finish()
    print(f"P026 INDEPENDENT FINITE-DIFFERENCE REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
