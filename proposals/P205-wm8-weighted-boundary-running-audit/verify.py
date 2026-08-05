#!/usr/bin/env python3
"""Primary exact verifier for WM8 weighted-boundary one-loop running."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml
from substrate_framework.gauge_beta import GaugeFactor, ProductMultiplet, product_gauge_coefficients
from substrate_framework.gauge_running import ThreeFactorBoundaryProblem, exact_one_loop_boundary_solution
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path("/home/dan/substrate/merged-framework/bridges/phase-39/bridge_WM8_corrected_boundary_running.py")
SOURCE_SHA256 = "741497f63cc39ee96c71e9a999c49ef9e821cf612d8b48b2959d05f9e6940518"
RELEASE_SHA256 = "18dffeef5efd516018c918f65b45173c81ac0e1ba99fdd8a96274cc1df5c72db"
FORMULA_FREEZE_SHA256 = "341f2d5e21f08d0f8efaf20e423fc8e62368fbc3430ea7fc5abfc5fe807d7baa"
R = sp.Rational
E = R(1279, 10)
STRONG = R(500, 59)
REFERENCE = R(227969, 2500)
MEASURED = R(11561, 50000)
CONSTRAINTS = ((0, 0, 1), (R(5, 3), 1, 0))


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
    return ProductMultiplet(
        label,
        kind,
        multiplicity,
        (y2 * color * isospin, R(1, 2) * color if isospin == 2 else 0, R(1, 2) * isospin if color == 3 else 0),
        (y2, R(3, 4) if isospin == 2 else 0, R(4, 3) if color == 3 else 0),
    )


def ledger(higgs_count: int = 1):
    factors = (GaugeFactor("U1", 0, True), GaugeFactor("SU2", 2), GaugeFactor("SU3", 3))
    fields = [
        multiplet("Q_L", "weyl_fermion", 3, (3, 2), R(1, 6)),
        multiplet("u_R_conj", "weyl_fermion", 3, (3, 1), -R(2, 3)),
        multiplet("d_R_conj", "weyl_fermion", 3, (3, 1), R(1, 3)),
        multiplet("L_L", "weyl_fermion", 3, (1, 2), -R(1, 2)),
        multiplet("e_R_conj", "weyl_fermion", 3, (1, 1), 1),
    ]
    if higgs_count:
        fields.append(multiplet("H", "complex_scalar", higgs_count, (1, 2), R(1, 2)))
    return product_gauge_coefficients(factors, fields)


def boundary(higgs_count: int | sp.Expr) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    return (4 + sp.sympify(higgs_count) / 10, 4 + sp.sympify(higgs_count) / 6, sp.Integer(4))


def problem(boundary_count: int, running_count: int = 1, *, boundary_override=None, constraints=CONSTRAINTS, targets=(STRONG, E)) -> ThreeFactorBoundaryProblem:
    return ThreeFactorBoundaryProblem(
        coefficients=ledger(running_count),
        reference_scale=REFERENCE,
        boundary_ratios=boundary_override or boundary(boundary_count),
        low_constraint_matrix=constraints,
        low_constraint_targets=targets,
        readout_weights=(0, 1, 0),
        readout_normalization=E,
    )


def main() -> int:
    checks = CheckLedger("P205-WM8-WEIGHTED-BOUNDARY")
    checks.check("source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check("base release remains pinned", digest(ROOT / "governance/releases/v0.150.0.yaml") == RELEASE_SHA256)
    checks.check("late formula freeze remains pinned", digest(CAMPAIGN / "evidence/formula-freeze.yaml") == FORMULA_FREEZE_SHA256)

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    source_checks = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "check"]
    checks.check("source predicate inventory remains exact", len(source_checks) == 10 and sum(isinstance(n, ast.Assert) for n in ast.walk(tree)) == 1)
    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check("source has no quadrature compatibility surface", compatibility.legacy_references == compatibility.current_references == compatibility.eager_legacy_default_fallbacks == 0)
    solve_function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "solve_boundary")
    checks.check("measured comparator is absent from the solve function dataflow", all(not (isinstance(n, ast.Name) and n.id == "SIN2_MEASURED") for n in ast.walk(solve_function)))
    checks.check("source comparator guard replays an identical solve rather than an actual perturbation", "perturbed = solve_boundary(*S_corr)" in source_text and source_text.count("SIN2_MEASURED =") == 1)
    checks.check("source varies boundary scalar count while holding running coefficients fixed", "b1, b2, b3 = R(_wm7.b1), R(_wm7.b2), R(_wm7.b3)" in source_text and "S_cf = _wm7.induced_S(_wm7.N_GEN, _wm7.N_GEN)" in source_text)

    standard = ledger(1)
    checks.check("accepted supplied ledger reproduces WM8 one-loop coefficients", standard.one_loop == (R(41, 10), -R(19, 6), -7))
    solutions = [exact_one_loop_boundary_solution(problem(n)) for n in range(4)]
    checks.check("canonical exact API reproduces the fermion-boundary WM3 readout", solutions[0].readout == R(6296809, 30335322) and solutions[0].constraint_residuals == (0, 0))
    checks.check("canonical exact API reproduces WM8's corrected rational solve", abs(float(solutions[1].boundary_amplitude) - 10.1058921418) < 1e-10 and abs(float(solutions[1].scaled_log_span) - 4.56414175655) < 1e-10)
    checks.check("canonical exact API reproduces WM8's corrected readout", abs(float(solutions[1].readout) - 0.216221801107) < 1e-12 and solutions[1].constraint_residuals == (0, 0))
    checks.check("all four boundary-only solutions retain positive affine coordinates", all(s.boundary_amplitude > 0 and s.scaled_log_span > 0 and all(v > 0 for v in s.low_inverse_couplings) for s in solutions))

    n = sp.Symbol("N_H", real=True)
    C = sp.Matrix(CONSTRAINTS)
    S = sp.Matrix(boundary(n))
    fixed_b = sp.Matrix(standard.one_loop)
    d = sp.Matrix([STRONG, E])
    fixed_design = sp.Matrix.hstack(C * S, C * fixed_b)
    fixed_parameters = sp.simplify(fixed_design.inv() * d)
    fixed_low = sp.simplify(fixed_parameters[0] * S + fixed_parameters[1] * fixed_b)
    fixed_readout = sp.factor(fixed_low[1] / E)
    checks.check("boundary-only design determinant stays nonsingular for nonnegative scalar count", sp.simplify(fixed_design.det() - (7 * n + 268) / 3) == 0)
    checks.check("boundary-only amplitude and span are exact rational functions", sp.simplify(fixed_parameters[0] - R(1639681, 590) / (7 * n + 268)) == 0 and sp.simplify(fixed_parameters[1] + R(2, 295) * (1250 * n - 186383) / (7 * n + 268)) == 0)
    checks.check("boundary-only readout is the exact WM8 scalar-count family", sp.simplify(fixed_readout - 19 * (91299 * n + 1325644) / (452766 * (7 * n + 268))) == 0)
    checks.check("boundary-only readout is increasing on the nonnegative domain", sp.simplify(sp.diff(fixed_readout, n) - R(144291928, 226383) / (7 * n + 268) ** 2) == 0)
    checks.check("source's N_H three near-hit is exact only on the fixed-running path", abs(float(fixed_readout.subs(n, 3)) - 0.232261554419) < 1e-12)

    coherent_b = sp.Matrix([4 + n / 10, -R(10, 3) + n / 6, -7])
    coherent_design = sp.Matrix.hstack(C * S, C * coherent_b)
    coherent_parameters = sp.simplify(coherent_design.inv() * d)
    coherent_low = sp.simplify(coherent_parameters[0] * S + coherent_parameters[1] * coherent_b)
    coherent_readout = sp.factor(coherent_low[1] / E)
    checks.check("coherent scalar-count running changes both boundary and beta ledger", coherent_b.subs(n, 1) == fixed_b and coherent_b.subs(n, 3) != fixed_b)
    checks.check("coherent design remains exact and nonsingular for nonnegative count", sp.simplify(coherent_design.det() - 11 * (n + 24) / 3) == 0)
    checks.check("coherent readout family differs except at the selected one-scalar point", sp.factor(coherent_readout - fixed_readout).subs(n, 1) == 0 and sp.factor(coherent_readout - fixed_readout).subs(n, 3) != 0)
    checks.check("coherent N_H three counterfactual is not the advertised near-hit", abs(float(coherent_readout.subs(n, 3)) - 0.238878442809) < 1e-12 and abs(float(coherent_readout.subs(n, 3) - MEASURED)) > abs(float(fixed_readout.subs(n, 3) - MEASURED)))
    checks.check("coherent N_H two is closer but still cannot select multiplicity", abs(float(coherent_readout.subs(n, 2) - MEASURED)) < abs(float(coherent_readout.subs(n, 1) - MEASURED)))

    changed_target = exact_one_loop_boundary_solution(problem(1, targets=(STRONG + 1, E)))
    changed_boundary = exact_one_loop_boundary_solution(problem(1, boundary_override=(R(21, 5), R(25, 6), 4)))
    checks.mutation_sensitive("conditional WM8 readout", lambda candidate: candidate == solutions[1].readout, solutions[1].readout, [changed_target.readout, changed_boundary.readout, solutions[0].readout, solutions[2].readout])

    v = fixed_b + R(7, 4) * sp.Matrix(boundary(1))
    singular_constraints = ((0, 0, 1), (v[1], -v[0], 0))
    singular_design = sp.Matrix(singular_constraints)
    checks.check("rank-two constraint mutation makes the two-column design singular", singular_design.rank() == 2 and sp.Matrix.hstack(singular_design * sp.Matrix(boundary(1)), singular_design * fixed_b).det() == 0)
    singular_rejected = False
    try:
        exact_one_loop_boundary_solution(problem(1, constraints=singular_constraints))
    except ValueError:
        singular_rejected = True
    checks.check("canonical exact solver rejects the singular design", singular_rejected)

    offset = sp.Matrix([0, 1, 0])
    offset_parameters = sp.Matrix.hstack(C * sp.Matrix(boundary(1)), C * fixed_b).inv() * (d - C * offset)
    offset_readout = sp.simplify((offset_parameters[0] * sp.Matrix(boundary(1)) + offset_parameters[1] * fixed_b + offset)[1] / E)
    checks.check("independent matching offsets change the exact readout", offset_readout != solutions[1].readout)
    checks.check("comparator mutation changes miss only and never the exact solve", solutions[1].readout == exact_one_loop_boundary_solution(problem(1)).readout and abs(solutions[1].readout - MEASURED) != abs(solutions[1].readout - (MEASURED + R(1, 100))))

    claims = {claim["id"]: claim for claim in load(ROOT / "governance/claims.yaml")["claims"]}
    checks.check("C-RGE-006 already owns the general weighted-boundary design", "columns C*S and C*b" in claims["C-RGE-006"]["statement"] and "unique exact solution" in claims["C-RGE-006"]["statement"])
    checks.check("accepted running claims type the source as conditional inverse inference", "conditional inverse inference" in claims["C-RGE-004"]["statement"] and "conditional inverse solution" in claims["C-RGE-006"]["statement"])
    checks.check("accepted beta claim retains same-order and matching omissions", "Yukawa" in claims["C-RGE-005"]["statement"] and "thresholds" in claims["C-RGE-005"]["statement"] and "matching" in claims["C-RGE-005"]["statement"])
    checks.check("C-RGE-008 remains absent because the general object is already accepted", "C-RGE-008" not in claims)
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
