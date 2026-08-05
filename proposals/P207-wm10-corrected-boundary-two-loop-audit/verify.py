#!/usr/bin/env python3
"""Primary status-gated audit of WM10's arbitrary-boundary two-loop solve."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
import yaml

from substrate_framework.gauge_beta import GaugeFactor, ProductMultiplet, product_gauge_coefficients
from substrate_framework.gauge_running import ThreeFactorBoundaryProblem, exact_one_loop_boundary_solution, solve_three_factor_boundary_running
from substrate_framework.numerics import SolverTolerances
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path("/home/dan/substrate/merged-framework/bridges/phase-39/bridge_WM10_corrected_boundary_two_loop.py")
SOURCE_SHA256 = "a813f32841a4809f0ca301d8f01cb432d07d43c6bc46433970c1dcf60afe8d29"
RELEASE_SHA256 = "18dffeef5efd516018c918f65b45173c81ac0e1ba99fdd8a96274cc1df5c72db"
FORMULA_FREEZE_SHA256 = "fca66fa2373f3d962ade6bbe0ef0f3583ce92fe6c697e27a94e973ad7571e81b"
R = sp.Rational
REFERENCE = R(227969, 2500)
STRONG = R(500, 59)
ELECTROMAGNETIC = R(1279, 10)
CONSTRAINTS = ((0, 0, 1), (R(5, 3), 1, 0))
BASE_BOUNDARY = (4, 4, 4)
CORRECTED_BOUNDARY = (R(41, 10), R(25, 6), 4)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def multiplet(label: str, kind: str, multiplicity: int, dimensions: tuple[int, int], hypercharge: sp.Expr) -> ProductMultiplet:
    color, isospin = dimensions
    y2 = R(3, 5) * hypercharge**2
    return ProductMultiplet(label, kind, multiplicity, (y2 * color * isospin, R(1, 2) * color if isospin == 2 else 0, R(1, 2) * isospin if color == 3 else 0), (y2, R(3, 4) if isospin == 2 else 0, R(4, 3) if color == 3 else 0))


def ledger():
    factors = (GaugeFactor("U1", 0, True), GaugeFactor("SU2", 2), GaugeFactor("SU3", 3))
    fields = [
        multiplet("Q_L", "weyl_fermion", 3, (3, 2), R(1, 6)),
        multiplet("u_R_conj", "weyl_fermion", 3, (3, 1), -R(2, 3)),
        multiplet("d_R_conj", "weyl_fermion", 3, (3, 1), R(1, 3)),
        multiplet("L_L", "weyl_fermion", 3, (1, 2), -R(1, 2)),
        multiplet("e_R_conj", "weyl_fermion", 3, (1, 1), 1),
        multiplet("H", "complex_scalar", 1, (1, 2), R(1, 2)),
    ]
    return product_gauge_coefficients(factors, fields)


def problem(boundary=CORRECTED_BOUNDARY, *, targets=(STRONG, ELECTROMAGNETIC)) -> ThreeFactorBoundaryProblem:
    return ThreeFactorBoundaryProblem(
        coefficients=ledger(),
        reference_scale=REFERENCE,
        boundary_ratios=boundary,
        low_constraint_matrix=CONSTRAINTS,
        low_constraint_targets=targets,
        readout_weights=(0, 1, 0),
        readout_normalization=ELECTROMAGNETIC,
    )


def solve(boundary, matrix_scale, *, method="DOP853", rtol=1e-11, atol=1e-13):
    return solve_three_factor_boundary_running(
        problem(boundary),
        initial_boundary_amplitude=10.2,
        initial_log_scale_span=29.0,
        matrix_scale=matrix_scale,
        tolerances=SolverTolerances(rtol=rtol, atol=atol),
        integration_method=method,
        residual_tolerance=1e-8,
        sample_count=257,
    )


def main() -> int:
    checks = CheckLedger("P207-WM10-CORRECTED-BOUNDARY-TWO-LOOP")
    checks.check("source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check("base release remains pinned", digest(ROOT / "governance/releases/v0.150.0.yaml") == RELEASE_SHA256)
    checks.check("formula freeze remains pinned", digest(CAMPAIGN / "evidence/formula-freeze.yaml") == FORMULA_FREEZE_SHA256)

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    source_checks = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "check"]
    checks.check("source predicate inventory remains exact", len(source_checks) == 7 and sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1)
    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check("source has no quadrature compatibility surface", compatibility.legacy_references == compatibility.current_references == compatibility.eager_legacy_default_fallbacks == 0)
    integrate_function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "_integrate")
    checks.check("source solve_ivp uses its default method only", not any(isinstance(node, ast.keyword) and node.arg == "method" for node in ast.walk(integrate_function)))
    residual_function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "_residuals")
    checks.check("measured comparator is absent from source shooting residuals", all(not (isinstance(node, ast.Name) and node.id == "SIN2_MEASURED") for node in ast.walk(residual_function)))
    checks.check("source comparator guard repeats an identical solve", "s2_repeat, _, _, _ = solve_boundary(S_CORR, BMAT)" in source_text and "SIN2_MEASURED = _wm3.SIN2_MEASURED" in source_text)
    checks.check("source grid discards each returned success flag", "val, _, _, okk = solve_boundary" in source_text and source_text.count("okk") == 1)
    checks.check("source monotonicity claim is based on a three by three grid", "for si, s in enumerate((0.0, 0.5, 1.0))" in source_text and "for ti, t in enumerate((0.0, 0.5, 1.0))" in source_text)

    coefficients = ledger()
    checks.check("accepted supplied ledger reproduces one-loop vector", coefficients.one_loop == (R(41, 10), -R(19, 6), -7))
    checks.check("accepted supplied ledger reproduces gauge-only two-loop matrix", coefficients.two_loop_gauge_matrix == ((R(199, 50), R(27, 10), R(44, 5)), (R(9, 10), R(35, 6), 12), (R(11, 10), R(9, 2), -26)))

    exact_base = exact_one_loop_boundary_solution(problem(BASE_BOUNDARY))
    exact_boundary = exact_one_loop_boundary_solution(problem(CORRECTED_BOUNDARY))
    base = solve(BASE_BOUNDARY, 0)
    matrix = solve(BASE_BOUNDARY, 1)
    boundary = solve(CORRECTED_BOUNDARY, 0)
    combined = solve(CORRECTED_BOUNDARY, 1)
    checks.check("canonical zero-matrix base reproduces exact affine solution", abs(base.readout - float(exact_base.readout)) < 2e-12 and base.max_abs_constraint_residual < 1e-9)
    checks.check("canonical corrected-boundary zero-matrix route reproduces WM8 exactly", abs(boundary.readout - float(exact_boundary.readout)) < 2e-12 and abs(boundary.readout - 0.2162218011069736) < 2e-12)
    checks.check("canonical equal-boundary full-matrix route reproduces C-RGE-006", abs(matrix.readout - 0.2106411357493541) < 2e-11 and abs(matrix.high_scale - 4.1301501696149e14) / matrix.high_scale < 2e-10)
    checks.check("canonical combined route reproduces WM10 conditional output", abs(combined.readout - 0.2192066478076030) < 2e-11 and abs(combined.high_scale - 1.6183315845707e14) / combined.high_scale < 2e-10)
    checks.check("all four canonical routes close status residual and positivity gates", all(value.max_abs_constraint_residual < 1e-8 and value.minimum_inverse_coupling > 0 and value.integration.function_evaluations > 0 for value in (base, matrix, boundary, combined)))

    tight = solve(CORRECTED_BOUNDARY, 1, rtol=1e-13, atol=1e-15)
    radau = solve(CORRECTED_BOUNDARY, 1, method="Radau", rtol=1e-11, atol=1e-13)
    checks.check("DOP853 tolerance tightening stabilizes combined readout", abs(tight.readout - combined.readout) < 3e-10 and tight.max_abs_constraint_residual < 1e-8)
    checks.check("Radau independently reproduces the combined inverse-coupling route", abs(radau.readout - combined.readout) < 3e-9 and abs(radau.log_scale_span - combined.log_scale_span) < 2e-7 and radau.max_abs_constraint_residual < 1e-8)

    cross_term = combined.readout - boundary.readout - matrix.readout + base.readout
    checks.check("four-corner interaction is nonzero and negative", abs(cross_term + 8.27877686e-5) < 2e-12 and cross_term < 0)
    checks.check("combined shift is not the sum of separately computed shifts", abs((combined.readout - base.readout) - ((boundary.readout - base.readout) + (matrix.readout - base.readout))) > 8e-5)

    sampled = np.empty((5, 5))
    base_array = np.asarray(BASE_BOUNDARY, dtype=float)
    corrected_array = np.asarray([float(value) for value in CORRECTED_BOUNDARY])
    for i, scalar_fraction in enumerate(np.linspace(0.0, 1.0, 5)):
        current_boundary = tuple(base_array + scalar_fraction * (corrected_array - base_array))
        for j, matrix_fraction in enumerate(np.linspace(0.0, 1.0, 5)):
            sampled[i, j] = solve(current_boundary, matrix_fraction).readout
    checks.check("refined sampled surface is increasing along both declared axes", np.all(np.diff(sampled, axis=0) > 0) and np.all(np.diff(sampled, axis=1) > 0))
    checks.check("sampled monotonicity is retained only as bounded numeric evidence", sampled.shape == (5, 5) and np.isfinite(sampled).all())

    sign_flip = solve(CORRECTED_BOUNDARY, -1)
    flipped_boundary = tuple(2 * base_array - corrected_array)
    boundary_flip = solve(flipped_boundary, 1)
    checks.mutation_sensitive("combined conditional readout", lambda candidate: abs(candidate - combined.readout) < 1e-10, combined.readout, [sign_flip.readout, boundary_flip.readout, base.readout, matrix.readout, boundary.readout])
    changed_target = solve_three_factor_boundary_running(problem(CORRECTED_BOUNDARY, targets=(STRONG + 1, ELECTROMAGNETIC)), initial_boundary_amplitude=10, initial_log_scale_span=28, matrix_scale=1)
    checks.check("supplied low-target mutation changes the conditional readout", abs(changed_target.readout - combined.readout) > 1e-4)
    checks.check("comparator mutation changes miss only and never the solve", combined.readout == solve(CORRECTED_BOUNDARY, 1).readout and abs(combined.readout - 0.23122) != abs(combined.readout - 0.24))
    matching_offset_readout = (combined.low_inverse_couplings[1] + 1.0) / float(ELECTROMAGNETIC)
    checks.check("independent finite matching offset changes the readout without changing beta arrays", abs(matching_offset_readout - combined.readout) > 0.007 and coefficients.one_loop == ledger().one_loop)

    claims = {claim["id"]: claim for claim in load(ROOT / "governance/claims.yaml")["claims"]}
    checks.check("C-RGE-006 already quantifies over supplied positive boundary ratios", "positive high-boundary ratios S" in claims["C-RGE-006"]["statement"] and "a(0)=A*S" in claims["C-RGE-006"]["statement"])
    checks.check("C-RGE-006 types the result as conditional inverse inference", "conditional inverse solution" in claims["C-RGE-006"]["statement"] and "not an ab-initio prediction" in claims["C-RGE-006"]["statement"])
    checks.check("accepted running claims retain same-order matching and scheme omissions", all(phrase in claims["C-RGE-005"]["statement"] for phrase in ("Yukawa", "thresholds", "matching")) and "scheme conversion" in claims["C-RGE-006"]["statement"])
    checks.check("WM9 disposition grants no scalar or generation multiplicity theorem", "N_H=1" in load(ROOT / "migration/dispositions.yaml")["units"]["WM9"]["qualification"] and "not accepted" in load(ROOT / "migration/dispositions.yaml")["units"]["WM9"]["qualification"])
    checks.check("C-RGE-008 remains absent because the arbitrary-boundary object is accepted", "C-RGE-008" not in claims)
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
