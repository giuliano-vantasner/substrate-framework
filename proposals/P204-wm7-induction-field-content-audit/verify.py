#!/usr/bin/env python3
"""Primary exact verifier for the WM7 induction field-content audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.charge_traces import (
    charge_coupling_angle_ledger,
    common_trace_normalized_coupling_angle,
)
from substrate_framework.gauge_beta import (
    GaugeFactor,
    ProductMultiplet,
    abelian_gauge_rescaling_ledger,
    product_gauge_coefficients,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-39/"
    "bridge_WM7_induction_trace_field_content.py"
)
SOURCE_SHA256 = "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361"
RELEASE_SHA256 = "18dffeef5efd516018c918f65b45173c81ac0e1ba99fdd8a96274cc1df5c72db"
FORMULA_FREEZE_SHA256 = (
    "f6c489112f37c5aff696a2ea4b8a0a9720f79eccbd426ca598078bbec6f8a9e0"
)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def _factors() -> tuple[GaugeFactor, ...]:
    return (
        GaugeFactor("U1", 0, is_abelian=True),
        GaugeFactor("SU2", 2),
        GaugeFactor("SU3", 3),
    )


def _multiplet(
    label: str,
    kind: str,
    multiplicity: int,
    dimensions: tuple[int, int],
    hypercharge: sp.Expr,
) -> ProductMultiplet:
    color, isospin = dimensions
    normalized_charge_squared = sp.Rational(3, 5) * hypercharge**2
    dynkin = (
        normalized_charge_squared * color * isospin,
        sp.Rational(1, 2) * color if isospin == 2 else 0,
        sp.Rational(1, 2) * isospin if color == 3 else 0,
    )
    casimir = (
        normalized_charge_squared,
        sp.Rational(3, 4) if isospin == 2 else 0,
        sp.Rational(4, 3) if color == 3 else 0,
    )
    return ProductMultiplet(label, kind, multiplicity, dynkin, casimir)


def _supplied_table(higgs_count: int = 1) -> tuple[ProductMultiplet, ...]:
    rows = (
        _multiplet("Q_L", "weyl_fermion", 3, (3, 2), sp.Rational(1, 6)),
        _multiplet("u_R_conj", "weyl_fermion", 3, (3, 1), -sp.Rational(2, 3)),
        _multiplet("d_R_conj", "weyl_fermion", 3, (3, 1), sp.Rational(1, 3)),
        _multiplet("L_L", "weyl_fermion", 3, (1, 2), -sp.Rational(1, 2)),
        _multiplet("e_R_conj", "weyl_fermion", 3, (1, 1), 1),
    )
    if higgs_count == 0:
        return rows
    return rows + (
        _multiplet(
            "H", "complex_scalar", higgs_count, (1, 2), sp.Rational(1, 2)
        ),
    )


def main() -> int:
    checks = CheckLedger("P204-WM7-INDUCTION-CONTENT")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.150.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned",
        _digest(CAMPAIGN / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    check_calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(source_tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source predicate inventory remains exact",
        len(check_calls) == 10 and len(assertions) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "source has no trapezoidal compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "source dynamically imports three tables but hardcodes decisive counts and conventions",
        source_text.count("_load(os.path.join") == 3
        and all(
            token in source_text
            for token in (
                "N_GEN = 3",
                "N_H = 1",
                "GUT = R(3, 5)",
                "SCALARS = [(\"H\", 1, 2, Y_H)]",
                "T_FUND = R(1, 2)",
            )
        ),
    )
    checks.check(
        "source constructs no determinant regulator matching or common kinetic action",
        not any(
            token in source_text
            for token in (
                "Tr log(",
                "functional_determinant",
                "counterterm",
                "Z_ref",
                "matching_offset",
                "threshold_mass",
            )
        ),
    )

    ledger = product_gauge_coefficients(_factors(), _supplied_table())
    checks.check(
        "accepted supplied table has exact separated one-loop contributions",
        ledger.one_loop_gauge == (0, -sp.Rational(22, 3), -11)
        and ledger.one_loop_weyl_fermions == (4, 4, 4)
        and ledger.one_loop_complex_scalars
        == (sp.Rational(1, 10), sp.Rational(1, 6), 0),
    )
    matter = tuple(
        sp.simplify(
            ledger.one_loop_weyl_fermions[index]
            + ledger.one_loop_complex_scalars[index]
        )
        for index in range(3)
    )
    checks.check(
        "completed matter vector is exact supplied-table arithmetic",
        matter == (sp.Rational(41, 10), sp.Rational(25, 6), 4)
        and tuple(
            sp.simplify(ledger.one_loop[index] - ledger.one_loop_gauge[index])
            for index in range(3)
        )
        == matter,
    )
    checks.check(
        "integer ratio and spread reproduce conditionally",
        tuple(value * 30 for value in matter) == (123, 125, 120)
        and max(matter) / min(matter) == sp.Rational(25, 24),
    )
    no_scalar = product_gauge_coefficients(_factors(), _supplied_table(0))
    two_scalars = product_gauge_coefficients(_factors(), _supplied_table(2))
    checks.check(
        "scalar-count mutations change only the supplied scalar contribution",
        no_scalar.one_loop_weyl_fermions == (4, 4, 4)
        and no_scalar.one_loop_complex_scalars == (0, 0, 0)
        and two_scalars.one_loop_complex_scalars
        == (sp.Rational(1, 5), sp.Rational(1, 3), 0),
    )
    checks.mutation_sensitive(
        "matter contribution vector",
        lambda candidate: candidate == matter,
        matter,
        [
            no_scalar.one_loop_weyl_fermions,
            tuple(
                no_scalar.one_loop_weyl_fermions[index]
                + two_scalars.one_loop_complex_scalars[index]
                for index in range(3)
            ),
            (matter[0], matter[1], matter[2] + 1),
        ],
    )

    weyl_sums = sp.Matrix(
        [value / sp.Rational(2, 3) for value in ledger.one_loop_weyl_fermions]
    )
    scalar_sums = sp.Matrix(
        [
            value / sp.Rational(1, 3)
            for value in ledger.one_loop_complex_scalars
        ]
    )
    design = sp.Matrix.hstack(weyl_sums, scalar_sums)
    target = sp.Matrix(matter)
    solution = sp.linsolve((design, target))
    checks.check(
        "weight solve is exact rank-two inverse reconstruction",
        design.rank() == 2
        and design.row_join(target).rank() == 2
        and solution == {(sp.Rational(2, 3), sp.Rational(1, 3))},
    )
    checks.check(
        "target is built from the same imported weights being reconstructed",
        target
        == design * sp.Matrix([sp.Rational(2, 3), sp.Rational(1, 3)]),
    )
    left_null = design.T.nullspace()
    checks.check(
        "third equation supplies consistency but not independent provenance",
        len(left_null) == 1 and sp.simplify((left_null[0].T * target)[0]) == 0,
    )
    mutated_target = target + sp.Matrix([1, 0, 0])
    checks.check(
        "independent coefficient mutation breaks the reconstructed consistency",
        design.row_join(mutated_target).rank() == 3,
    )
    checks.check(
        "removing the scalar destroys scalar-weight identifiability",
        sp.Matrix.hstack(weyl_sums, sp.zeros(3, 1)).rank() == 1,
    )

    n_h = sp.Symbol("N_H", real=True)
    scalar_family = (
        4 + n_h / 10,
        4 + n_h / 6,
        sp.Integer(4),
    )
    concurrence_solutions = sp.solve(
        [scalar_family[0] - scalar_family[2], scalar_family[1] - scalar_family[2]],
        [n_h],
        dict=True,
    )
    checks.check(
        "supplied scalar-count family is concurrent exactly at zero",
        concurrence_solutions == [{n_h: 0}],
    )
    checks.check(
        "one supplied scalar recovers the source vector",
        tuple(sp.simplify(value.subs(n_h, 1)) for value in scalar_family) == matter,
    )

    common = sp.Symbol("C", positive=True)
    boundaries = sp.symbols("z_1 z_2 z_3", real=True)
    coefficients = sp.symbols("C_1 C_2 C_3", positive=True)
    general_inverse = tuple(
        boundaries[index] + coefficients[index] * matter[index]
        for index in range(3)
    )
    zero_common = tuple(common * value for value in matter)
    checks.check(
        "common inverse-weight ratio is an explicit zero-boundary specialization",
        sp.simplify((1 / zero_common[0]) / (1 / zero_common[1]))
        == sp.Rational(125, 123),
    )
    checks.check(
        "independent affine boundaries and coefficients remain load bearing",
        general_inverse[0].has(boundaries[0], coefficients[0])
        and general_inverse[1].has(boundaries[1], coefficients[1])
        and sp.simplify(
            (1 / general_inverse[0]) / (1 / general_inverse[1])
            - sp.Rational(125, 123)
        )
        != 0,
    )
    checks.mutation_sensitive(
        "common zero-boundary coupling ratio",
        lambda candidate: sp.simplify(candidate - sp.Rational(125, 123)) == 0,
        (1 / zero_common[0]) / (1 / zero_common[1]),
        [
            (1 / (zero_common[0] + 1)) / (1 / zero_common[1]),
            (1 / (2 * zero_common[0])) / (1 / zero_common[1]),
            (1 / zero_common[0]) / (1 / (zero_common[1] + 1)),
        ],
    )

    canonical_abelian = sp.Rational(5, 3) * matter[0]
    conditional_angle = common_trace_normalized_coupling_angle(
        matter[1], canonical_abelian, common
    )
    independent_angle = charge_coupling_angle_ledger(
        matter[1], canonical_abelian, 1, 1
    )
    checks.check(
        "twenty-five over sixty-six is exact under the common law",
        conditional_angle.coupling_angle == sp.Rational(25, 66)
        and conditional_angle.common_coefficient_residual == 0,
    )
    checks.check(
        "independent couplings refute an automatic weak-angle boundary",
        independent_angle.trace_angle == sp.Rational(25, 66)
        and independent_angle.coupling_angle == sp.Rational(1, 2),
    )
    rho = sp.Symbol("rho", positive=True)
    rescaled = abelian_gauge_rescaling_ledger(ledger, (rho, 1, 1))
    rescaled_matter = tuple(
        sp.simplify(
            rescaled.rescaled.one_loop_weyl_fermions[index]
            + rescaled.rescaled.one_loop_complex_scalars[index]
        )
        for index in range(3)
    )
    checks.check(
        "Abelian coordinate rescaling moves the raw ratio covariantly",
        rescaled_matter[0] == rho**2 * matter[0]
        and rescaled_matter[1:] == matter[1:]
        and rescaled.one_loop_residuals == (0, 0, 0),
    )

    checks.check(
        "negative gauge beta contribution does not force a negative total kinetic coordinate",
        tuple(
            boundary + coefficient
            for boundary, coefficient in zip((1, 4, 8), ledger.one_loop, strict=True)
        )
        == (sp.Rational(51, 10), sp.Rational(5, 6), 1),
    )
    claims = {
        claim["id"]: claim for claim in _load(ROOT / "governance/claims.yaml")["claims"]
    }
    checks.check(
        "accepted claims classify the source tables and counts as supplied",
        "separately supplied" in claims["C-RGE-005"]["statement"]
        and "does not derive physical representations" in claims["C-RGE-005"]["assumptions"][-2]
        and "finite table is supplied" in claims["C-REP-003"]["assumptions"][0],
    )
    checks.check(
        "generic three-by-three phase count does not derive three physical generations",
        "no quark or generation map" in claims["C-MIX-002"]["statement"],
    )
    checks.check(
        "accepted affine theorem retains matching boundaries and physical ceiling",
        "Z_ref" in claims["C-VAC-003"]["statement"]
        and "physical charged spectrum" in claims["C-VAC-003"]["statement"],
    )
    checks.check(
        "C-RGE-007 remains absent because accepted composition owns the object",
        "C-RGE-007" not in claims,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
