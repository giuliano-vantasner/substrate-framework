import numpy as np
import pytest
import sympy as sp

from substrate_framework.gauge_beta import (
    GaugeFactor,
    ProductMultiplet,
    product_gauge_coefficients,
)
from substrate_framework.gauge_running import (
    ThreeFactorBoundaryProblem,
    direct_coupling_downward_rhs,
    exact_one_loop_boundary_solution,
    inverse_coupling_downward_rhs,
    solve_three_factor_boundary_running,
)
from substrate_framework.numerics import NumericalFailure, SolverTolerances


def _ledger():
    factors = (
        GaugeFactor("U1", 0, is_abelian=True),
        GaugeFactor("SU2", 2),
        GaugeFactor("SU3", 3),
    )
    fields = (
        ProductMultiplet("Q", "weyl_fermion", 3, (sp.Rational(1, 10), sp.Rational(3, 2), 1), (sp.Rational(1, 60), sp.Rational(3, 4), sp.Rational(4, 3))),
        ProductMultiplet("u", "weyl_fermion", 3, (sp.Rational(4, 5), 0, sp.Rational(1, 2)), (sp.Rational(4, 15), 0, sp.Rational(4, 3))),
        ProductMultiplet("d", "weyl_fermion", 3, (sp.Rational(1, 5), 0, sp.Rational(1, 2)), (sp.Rational(1, 15), 0, sp.Rational(4, 3))),
        ProductMultiplet("L", "weyl_fermion", 3, (sp.Rational(3, 10), sp.Rational(1, 2), 0), (sp.Rational(3, 20), sp.Rational(3, 4), 0)),
        ProductMultiplet("e", "weyl_fermion", 3, (sp.Rational(3, 5), 0, 0), (sp.Rational(3, 5), 0, 0)),
        ProductMultiplet("H", "complex_scalar", 1, (sp.Rational(3, 10), sp.Rational(1, 2), 0), (sp.Rational(3, 20), sp.Rational(3, 4), 0)),
    )
    return product_gauge_coefficients(factors, fields)


def _problem(reference_scale=sp.Rational(227969, 2500), boundary=(1, 1, 1)):
    return ThreeFactorBoundaryProblem(
        coefficients=_ledger(),
        reference_scale=reference_scale,
        boundary_ratios=boundary,
        low_constraint_matrix=((0, 0, 1), (sp.Rational(5, 3), 1, 0)),
        low_constraint_targets=(sp.Rational(500, 59), sp.Rational(1279, 10)),
        readout_weights=(0, 1, 0),
        readout_normalization=sp.Rational(1279, 10),
    )


def test_exact_one_loop_solution_matches_the_accepted_affine_reconstruction() -> None:
    solution = exact_one_loop_boundary_solution(_problem())
    assert solution.boundary_amplitude == sp.Rational(1639681, 39530)
    assert solution.scaled_log_span == sp.Rational(186383, 39530)
    assert solution.log_scale_span == 2 * sp.pi * sp.Rational(186383, 39530)
    assert solution.readout == sp.Rational(6296809, 30335322)
    assert solution.constraint_residuals == (0, 0)


def test_numeric_zero_matrix_route_recovers_the_exact_one_loop_solution() -> None:
    problem = _problem()
    exact = exact_one_loop_boundary_solution(problem)
    numeric = solve_three_factor_boundary_running(
        problem,
        initial_boundary_amplitude=40,
        initial_log_scale_span=30,
        matrix_scale=0,
    )
    assert numeric.boundary_amplitude == pytest.approx(float(exact.boundary_amplitude), rel=2e-11)
    assert numeric.log_scale_span == pytest.approx(float(exact.log_scale_span), rel=2e-11)
    assert numeric.readout == pytest.approx(float(exact.readout), abs=2e-12)
    assert numeric.max_abs_constraint_residual < 1e-9
    assert numeric.minimum_inverse_coupling > 0


def test_two_loop_solution_is_stable_under_method_and_tolerance_changes() -> None:
    problem = _problem()
    baseline = solve_three_factor_boundary_running(
        problem,
        initial_boundary_amplitude=41,
        initial_log_scale_span=29,
        tolerances=SolverTolerances(rtol=1e-10, atol=1e-12),
        integration_method="DOP853",
    )
    tight = solve_three_factor_boundary_running(
        problem,
        initial_boundary_amplitude=43,
        initial_log_scale_span=31,
        tolerances=SolverTolerances(rtol=1e-12, atol=1e-14),
        integration_method="DOP853",
    )
    radau = solve_three_factor_boundary_running(
        problem,
        initial_boundary_amplitude=40,
        initial_log_scale_span=28,
        tolerances=SolverTolerances(rtol=1e-10, atol=1e-12),
        integration_method="Radau",
    )
    assert baseline.readout == pytest.approx(0.210641, abs=1e-6)
    assert abs(tight.readout - baseline.readout) < 2e-10
    assert abs(radau.readout - baseline.readout) < 2e-9
    assert baseline.max_abs_constraint_residual < 1e-9
    assert tight.max_abs_constraint_residual < 1e-9
    assert radau.max_abs_constraint_residual < 1e-9


def test_reference_scale_changes_only_the_reported_high_scale() -> None:
    baseline = solve_three_factor_boundary_running(
        _problem(reference_scale=10),
        initial_boundary_amplitude=41,
        initial_log_scale_span=29,
    )
    rescaled = solve_three_factor_boundary_running(
        _problem(reference_scale=70),
        initial_boundary_amplitude=41,
        initial_log_scale_span=29,
    )
    assert rescaled.readout == pytest.approx(baseline.readout, abs=1e-13)
    assert rescaled.boundary_amplitude == pytest.approx(baseline.boundary_amplitude)
    assert rescaled.log_scale_span == pytest.approx(baseline.log_scale_span)
    assert rescaled.high_scale == pytest.approx(7 * baseline.high_scale)


def test_sign_transpose_and_boundary_mutations_change_the_conditional_output() -> None:
    problem = _problem()
    baseline = solve_three_factor_boundary_running(
        problem,
        initial_boundary_amplitude=41,
        initial_log_scale_span=29,
    )
    sign_flip = solve_three_factor_boundary_running(
        problem,
        initial_boundary_amplitude=41,
        initial_log_scale_span=29,
        matrix_scale=-1,
    )
    matrix = problem.coefficients.two_loop_gauge_matrix
    transposed_ledger = problem.coefficients.__class__(
        **{
            **problem.coefficients.__dict__,
            "two_loop_gauge_matrix": tuple(zip(*matrix, strict=True)),
        }
    )
    transposed_problem = ThreeFactorBoundaryProblem(
        **{**problem.__dict__, "coefficients": transposed_ledger}
    )
    transpose = solve_three_factor_boundary_running(
        transposed_problem,
        initial_boundary_amplitude=41,
        initial_log_scale_span=29,
    )
    shifted_boundary = solve_three_factor_boundary_running(
        _problem(boundary=(1, sp.Rational(21, 20), 1)),
        initial_boundary_amplitude=41,
        initial_log_scale_span=29,
    )
    assert abs(sign_flip.readout - baseline.readout) > 1e-3
    assert abs(transpose.readout - baseline.readout) > 1e-4
    assert abs(shifted_boundary.readout - baseline.readout) > 1e-3


def test_direct_and_inverse_rhs_are_the_same_coordinate_flow() -> None:
    ledger = _ledger()
    inverse = np.array([52.0, 37.0, 11.0])
    coupling = np.sqrt(4.0 * np.pi / inverse)
    direct_rhs = direct_coupling_downward_rhs(ledger, coupling)
    implied_inverse_rhs = -8.0 * np.pi * direct_rhs / coupling**3
    np.testing.assert_allclose(
        implied_inverse_rhs,
        inverse_coupling_downward_rhs(ledger, inverse),
        rtol=2e-15,
        atol=2e-15,
    )


@pytest.mark.parametrize(
    "problem",
    [
        ThreeFactorBoundaryProblem(_ledger(), 0, (1, 1, 1), ((0, 0, 1), (1, 1, 0)), (1, 2), (0, 1, 0), 2),
        ThreeFactorBoundaryProblem(_ledger(), 1, (1, 0, 1), ((0, 0, 1), (1, 1, 0)), (1, 2), (0, 1, 0), 2),
        ThreeFactorBoundaryProblem(_ledger(), 1, (1, 1, 1), ((0, 0, 1), (0, 0, 2)), (1, 2), (0, 1, 0), 2),
        ThreeFactorBoundaryProblem(_ledger(), 1, (1, 1, 1), ((0, 0, 1), (1, 1, 0)), (0, 2), (0, 1, 0), 2),
        ThreeFactorBoundaryProblem(_ledger(), 1, (1, 1, 1), ((0, 0, 1), (1, 1, 0)), (1, 2), (0, 0, 0), 2),
    ],
)
def test_invalid_boundary_problems_are_rejected(problem) -> None:
    with pytest.raises(ValueError):
        solve_three_factor_boundary_running(
            problem,
            initial_boundary_amplitude=1,
            initial_log_scale_span=1,
        )


def test_nonpositive_state_and_impossible_residual_gate_are_rejected() -> None:
    with pytest.raises(NumericalFailure):
        inverse_coupling_downward_rhs(_ledger(), [1, 0, 2])
    with pytest.raises(NumericalFailure):
        solve_three_factor_boundary_running(
            _problem(),
            initial_boundary_amplitude=41,
            initial_log_scale_span=29,
            residual_tolerance=1e-18,
        )
