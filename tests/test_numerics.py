from __future__ import annotations

import numpy as np
from scipy.sparse import diags

from substrate_framework.numerics import (
    SolverTolerances,
    refinement_study,
    solve_bvp_evidence,
    solve_ivp_evidence,
    solve_method_of_lines,
)


TIGHT = SolverTolerances(rtol=1.0e-11, atol=1.0e-13)


def test_ivp_records_conserved_quantity_drift() -> None:
    result = solve_ivp_evidence(
        lambda _time, state: np.array([state[1], -state[0]]),
        (0.0, 2.0 * np.pi),
        [1.0, 0.0],
        sample_times=np.linspace(0.0, 2.0 * np.pi, 101),
        tolerances=TIGHT,
        invariant=lambda state: float(state @ state),
    )

    np.testing.assert_allclose(result.state[:, -1], [1.0, 0.0], atol=2.0e-10)
    assert result.max_abs_invariant_drift is not None
    assert result.max_abs_invariant_drift < 2.0e-10
    assert result.function_evaluations > 0


def test_bvp_records_collocation_residuals() -> None:
    coordinate = np.linspace(0.0, np.pi / 2.0, 21)
    guess = np.vstack((coordinate / coordinate[-1], np.ones_like(coordinate)))
    result = solve_bvp_evidence(
        lambda _x, state: np.vstack((state[1], -state[0])),
        lambda left, right: np.array([left[0], right[0] - 1.0]),
        coordinate,
        guess,
        tolerance=1.0e-8,
    )

    np.testing.assert_allclose(result.state[0], np.sin(result.coordinate), atol=2.0e-8)
    assert result.max_rms_residual < 1.0e-8
    assert result.iterations > 0


def test_method_of_lines_heat_equation_has_second_order_spatial_convergence() -> None:
    final_time = 0.02

    def solve(intervals: int) -> tuple[np.ndarray, np.ndarray]:
        spacing = 1.0 / intervals
        coordinate = np.linspace(0.0, 1.0, intervals + 1)[1:-1]
        count = coordinate.size
        laplacian = diags(
            [np.ones(count - 1), -2.0 * np.ones(count), np.ones(count - 1)],
            offsets=[-1, 0, 1],
            format="csr",
        ) / spacing**2
        result = solve_method_of_lines(
            lambda _time, state: laplacian @ state,
            (0.0, final_time),
            np.sin(np.pi * coordinate),
            sample_times=[final_time],
            tolerances=TIGHT,
        )
        return coordinate, result.state[:, -1]

    def rms_error(solution: tuple[np.ndarray, np.ndarray]) -> float:
        coordinate, numeric = solution
        exact = np.exp(-(np.pi**2) * final_time) * np.sin(np.pi * coordinate)
        return float(np.linalg.norm(numeric - exact) / np.sqrt(coordinate.size))

    study = refinement_study((16, 32, 64), solve, rms_error)

    assert study.errors_strictly_decrease
    assert study.final_error < 3.0e-5
    assert all(order is not None and order > 1.9 for order in study.observed_orders)
