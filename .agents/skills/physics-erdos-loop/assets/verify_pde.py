#!/usr/bin/env python3
"""Pattern for a PDE verifier with SciPy and mesh-refinement evidence.

Replace the soluble heat-equation fixture with canonical claim APIs. Preserve
the pattern: explicit PDE data, importable solver machinery, a claim-defined
error norm, observed refinement order, and a sensitive physical assertion.
"""

from __future__ import annotations

import numpy as np
from scipy.sparse import diags

from substrate_framework.numerics import (
    SolverTolerances,
    refinement_study,
    solve_method_of_lines,
)
from substrate_framework.verification import CheckLedger


FINAL_TIME = 0.02
TOLERANCES = SolverTolerances(rtol=1.0e-10, atol=1.0e-12)


def solve_heat_equation(intervals: int) -> tuple[np.ndarray, np.ndarray]:
    """Solve u_t = u_xx on [0, 1] with zero boundaries and sine data."""

    spacing = 1.0 / intervals
    coordinate = np.linspace(0.0, 1.0, intervals + 1)[1:-1]
    count = coordinate.size
    laplacian = diags(
        [np.ones(count - 1), -2.0 * np.ones(count), np.ones(count - 1)],
        [-1, 0, 1],
        format="csr",
    ) / spacing**2
    result = solve_method_of_lines(
        lambda _time, state: laplacian @ state,
        (0.0, FINAL_TIME),
        np.sin(np.pi * coordinate),
        sample_times=[FINAL_TIME],
        tolerances=TOLERANCES,
    )
    return coordinate, result.state[:, -1]


def rms_error(solution: tuple[np.ndarray, np.ndarray]) -> float:
    coordinate, numeric = solution
    exact = np.exp(-(np.pi**2) * FINAL_TIME) * np.sin(np.pi * coordinate)
    return float(np.linalg.norm(numeric - exact) / np.sqrt(coordinate.size))


def amplitude_error(amplitude: float) -> float:
    coordinate, numeric = solve_heat_equation(64)
    return rms_error((coordinate, amplitude * numeric))


def run() -> int:
    checks = CheckLedger("PDE-VERIFIER-TEMPLATE")
    study = refinement_study((16, 32, 64), solve_heat_equation, rms_error)
    checks.check("mesh refinement reduces RMS error", study.errors_strictly_decrease)
    checks.check(
        "observed spatial order is second order",
        all(order is not None and order > 1.9 for order in study.observed_orders),
    )
    checks.mutation_sensitive(
        "diffusive evolution is amplitude-sensitive",
        predicate=lambda amplitude: amplitude_error(amplitude) < 3.0e-5,
        baseline=1.0,
        mutations=[0.9, 1.1],
    )
    return checks.finish()


if __name__ == "__main__":
    run()
