from __future__ import annotations

import numpy as np
import pytest

from substrate_framework.numerics import NumericalFailure
from substrate_framework.spherical_einstein_scalar_bvp import (
    finite_wall_boundary_residual,
    regular_origin_numeric_state,
    solve_static_spherical_scalar_bvp,
    static_spherical_scalar_rhs,
)


def test_regular_origin_numeric_state_has_declared_orders() -> None:
    epsilon = 1.0e-3
    state = regular_origin_numeric_state(3.0, -0.18, 0.89, 0.03, epsilon)
    assert state.shape == (4,)
    assert abs(state[0] - 3.0 - 0.5 * epsilon * state[1]) < 1.0e-12
    assert abs(state[1]) < 1.0e-3
    assert abs(state[2]) < 1.0e-9
    assert abs(state[3] + 0.18) < 1.0e-6


def test_reduced_rhs_refuses_to_clip_a_nonpositive_metric() -> None:
    with pytest.raises(NumericalFailure, match="nonpositive"):
        static_spherical_scalar_rhs(
            np.asarray([1.0]),
            np.asarray([[1.0], [0.0], [0.6], [0.0]]),
            0.9,
            0.03,
        )


def test_finite_gravity_bvp_retains_solver_boundary_and_horizon_evidence() -> None:
    solution = solve_static_spherical_scalar_bvp(
        central_amplitude=3.0,
        dimensionless_coupling=0.03,
        origin_epsilon=1.0e-3,
        outer_radius=30.0,
        initial_mesh_points=120,
        tolerance=2.0e-6,
        frequency_guess=0.89,
    )
    residual = finite_wall_boundary_residual(
        solution.state[:, 0],
        solution.state[:, -1],
        solution.frequency,
        central_amplitude=solution.central_amplitude,
        dimensionless_coupling=solution.dimensionless_coupling,
        origin_epsilon=solution.origin_epsilon,
        outer_radius=solution.outer_radius,
    )
    assert solution.completed
    assert solution.frequency == pytest.approx(0.890840, abs=4.0e-6)
    assert solution.outer_mass == pytest.approx(0.290961, abs=4.0e-6)
    assert solution.max_collocation_rms_residual < 2.1e-6
    assert solution.off_grid_relative_ode_residual < 2.0e-5
    assert solution.minimum_radial_metric_function > 0.85
    assert solution.outer_condition == "approximate_finite_wall_evanescent_Robin"
    assert np.max(np.abs(residual)) < 1.0e-9


def test_flat_limit_has_flat_metric_and_accepted_single_harmonic_frequency() -> None:
    solution = solve_static_spherical_scalar_bvp(
        central_amplitude=3.0,
        dimensionless_coupling=0.0,
        origin_epsilon=1.0e-3,
        outer_radius=30.0,
        initial_mesh_points=120,
        tolerance=2.0e-6,
        frequency_guess=0.96,
    )
    assert solution.frequency == pytest.approx(0.965311, abs=4.0e-6)
    assert np.max(np.abs(solution.mass)) < 1.0e-14
    assert np.max(np.abs(solution.lapse_exponent)) < 1.0e-14
    assert solution.minimum_radial_metric_function == pytest.approx(1.0)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"origin_epsilon": 0.0}, "origin_epsilon"),
        ({"dimensionless_coupling": -0.1}, "dimensionless_coupling"),
        ({"initial_mesh_points": 10}, "initial_mesh_points"),
        ({"frequency_guess": 1.0}, "frequency_guess"),
    ],
)
def test_bvp_input_guards(kwargs: dict[str, float], message: str) -> None:
    arguments = dict(
        central_amplitude=3.0,
        dimensionless_coupling=0.03,
        origin_epsilon=1.0e-3,
        outer_radius=20.0,
        initial_mesh_points=80,
        tolerance=1.0e-5,
        frequency_guess=0.9,
    )
    arguments.update(kwargs)
    with pytest.raises(ValueError, match=message):
        solve_static_spherical_scalar_bvp(**arguments)
