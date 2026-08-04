"""Primary status, refinement, mutation, and source-semantics verifier for P130."""

from __future__ import annotations

import ast
import hashlib
from dataclasses import fields
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import brentq

from substrate_framework.gauge_beta import (
    GaugeFactor,
    ProductMultiplet,
    product_gauge_coefficients,
)
from substrate_framework.gauge_running import (
    ThreeFactorBoundaryProblem,
    exact_one_loop_boundary_solution,
    solve_three_factor_boundary_running,
)
from substrate_framework.numerics import SolverTolerances
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-33/"
    "bridge_WM6_two_loop_running.py"
)
CAMPAIGN = Path("campaigns/P130-wm6-two-loop-running-audit")
SOURCE_SHA = "6d1ea4245adcf490466974d4a40b24843cd92e883c6e885936fb030cd1b31d57"
FREEZE_SHA = "7800f2aed53ad54f436b4d77a1f43fd5b735b0d4a18cab90b6e883ebedfeed97"


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


def _problem(*, boundary=(1, 1, 1), electromagnetic_inverse=sp.Rational(1279, 10)):
    return ThreeFactorBoundaryProblem(
        coefficients=_ledger(),
        reference_scale=sp.Rational(227969, 2500),
        boundary_ratios=boundary,
        low_constraint_matrix=((0, 0, 1), (sp.Rational(5, 3), 1, 0)),
        low_constraint_targets=(sp.Rational(500, 59), electromagnetic_inverse),
        readout_weights=(0, 1, 0),
        readout_normalization=electromagnetic_inverse,
    )


def _solve(problem=None, **options):
    return solve_three_factor_boundary_running(
        _problem() if problem is None else problem,
        initial_boundary_amplitude=options.pop("initial_boundary_amplitude", 41),
        initial_log_scale_span=options.pop("initial_log_scale_span", 29),
        **options,
    )


def main() -> int:
    checks = CheckLedger("WM6-TWO-LOOP-RUNNING-AUDIT")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    tree = ast.parse(source_text)
    checks.check(
        "WM6 source bytes are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA,
    )
    normalized_contract = (CAMPAIGN / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n", b"status: draft\n"
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == FREEZE_SHA,
    )
    checks.check(
        "pre-source contract remains byte immutable",
        hashlib.sha256(
            (CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "eleven source call sites match the terminal tally",
        len(source_checks) == 11 and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "WM6 has no quadrature compatibility path",
        all(
            token not in source_text
            for token in ("np.trapz", "np.trapezoid", "trapezoid_integral")
        ),
    )

    solve_ivp_call = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "solve_ivp"
    )
    checks.check(
        "source leaves its solve_ivp method at the undeclared SciPy default",
        not any(keyword.arg == "method" for keyword in solve_ivp_call.keywords),
    )
    residual_function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "_residuals"
    )
    residual_names = {
        node.id for node in ast.walk(residual_function) if isinstance(node, ast.Name)
    }
    comparator_loads = sum(
        isinstance(node, ast.Name)
        and isinstance(node.ctx, ast.Load)
        and node.id == "SIN2_MEASURED"
        for node in ast.walk(tree)
    )
    checks.check(
        "weak comparator is absent from shooting but enters more than two later expressions",
        "SIN2_MEASURED" not in residual_names and comparator_loads > 2,
    )
    checks.check(
        "source exact-language oracle is only a rounded-literal regression",
        "math.isclose(s2_1L, 0.20757" in source_text
        and "math.isclose(log10_1L, 14.826" in source_text,
    )
    checks.check(
        "canonical problem record has no comparator or measured-coordinate field",
        all(
            token not in field.name
            for field in fields(ThreeFactorBoundaryProblem)
            for token in ("comparator", "measured", "sin2")
        ),
    )

    exact = exact_one_loop_boundary_solution(_problem())
    checks.check(
        "exact zero-matrix route recovers the accepted affine reconstruction",
        exact.boundary_amplitude == sp.Rational(1639681, 39530)
        and exact.scaled_log_span == sp.Rational(186383, 39530)
        and exact.readout == sp.Rational(6296809, 30335322)
        and exact.constraint_residuals == (0, 0),
    )
    numeric_zero = _solve(matrix_scale=0)
    checks.check(
        "status-gated numeric zero-matrix solve reproduces the exact route",
        abs(numeric_zero.readout - float(exact.readout)) < 2e-11
        and abs(numeric_zero.boundary_amplitude - float(exact.boundary_amplitude)) < 2e-8
        and numeric_zero.max_abs_constraint_residual < 1e-9,
    )

    loose = _solve(tolerances=SolverTolerances(rtol=1e-8, atol=1e-10))
    baseline = _solve(tolerances=SolverTolerances(rtol=1e-10, atol=1e-12))
    tight = _solve(
        initial_boundary_amplitude=44,
        initial_log_scale_span=32,
        tolerances=SolverTolerances(rtol=1e-12, atol=1e-14),
    )
    radau = _solve(
        initial_boundary_amplitude=39,
        initial_log_scale_span=27,
        integration_method="Radau",
        tolerances=SolverTolerances(rtol=1e-10, atol=1e-12),
    )
    checks.check(
        "every shooting and IVP route closes status residual and positivity gates",
        all(
            result.max_abs_constraint_residual < 1e-8
            and result.minimum_inverse_coupling > 0
            and result.root_function_evaluations > 0
            and result.integration.function_evaluations > 0
            for result in (loose, baseline, tight, radau)
        ),
    )
    checks.check(
        "tolerance tightening and Radau agree beyond the claimed numeric digits",
        abs(loose.readout - baseline.readout) < 2e-8
        and abs(tight.readout - baseline.readout) < 2e-10
        and abs(radau.readout - baseline.readout) < 2e-9,
    )
    checks.check(
        "canonical conditional specialization reproduces source numeric outputs",
        abs(baseline.readout - 0.210641) < 1e-6
        and abs(np.log10(baseline.high_scale) - 14.616) < 2e-3,
    )

    scale_seven = _solve(
        problem=ThreeFactorBoundaryProblem(
            **{**_problem().__dict__, "reference_scale": 7 * _problem().reference_scale}
        )
    )
    checks.check(
        "reference-scale covariance leaves dimensionless inference unchanged",
        abs(scale_seven.readout - baseline.readout) < 1e-13
        and abs(scale_seven.log_scale_span - baseline.log_scale_span) < 1e-11
        and abs(scale_seven.high_scale / baseline.high_scale - 7) < 1e-11,
    )

    sign_flip = _solve(matrix_scale=-1)
    transpose_matrix = tuple(zip(*_ledger().two_loop_gauge_matrix, strict=True))
    transposed_ledger = _ledger().__class__(
        **{**_ledger().__dict__, "two_loop_gauge_matrix": transpose_matrix}
    )
    transposed = _solve(
        problem=ThreeFactorBoundaryProblem(
            **{**_problem().__dict__, "coefficients": transposed_ledger}
        )
    )
    boundary_mutant = _solve(problem=_problem(boundary=(1, sp.Rational(21, 20), 1)))
    input_mutant = _solve(problem=_problem(electromagnetic_inverse=128))
    checks.mutation_sensitive(
        "conditional running readout",
        lambda value: abs(float(value) - baseline.readout) < 1e-10,
        baseline.readout,
        (sign_flip.readout, transposed.readout, boundary_mutant.readout, input_mutant.readout),
    )

    target = 0.23122
    fitted_scale = brentq(lambda scale: _solve(matrix_scale=scale).readout - target, 1, 12)
    alternate_target_scale = brentq(
        lambda scale: _solve(matrix_scale=scale).readout - 0.22,
        1,
        12,
    )
    checks.check(
        "uniform matrix scaling is a target-dependent inverse family",
        8 < fitted_scale < 10
        and 2 < alternate_target_scale < 6
        and abs(fitted_scale - alternate_target_scale) > 3,
    )
    checks.check(
        "uniform scaling cannot encode the independent tensor structure of an unknown order",
        np.linalg.matrix_rank(
            np.column_stack(
                (
                    np.asarray(_ledger().two_loop_gauge_matrix, dtype=float).reshape(-1),
                    np.eye(3, dtype=float).reshape(-1),
                )
            )
        )
        == 2,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
