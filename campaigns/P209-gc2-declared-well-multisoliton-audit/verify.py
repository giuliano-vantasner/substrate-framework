#!/usr/bin/env python3
"""Primary exact verifier for GC2's declared-well and count interpretation."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.qball_fluctuations import (
    quartic_fluctuation_bound_eigenvalues,
    quartic_fluctuation_bound_modes,
    quartic_fluctuation_operator,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.translated_localization import poschl_teller_ground_ledger
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCE = SOURCE_ROOT / (
    "merged-framework/bridges/phase-42/"
    "bridge_GC2_corpus_already_multisoliton.py"
)
MH2 = SOURCE_ROOT / "merged-framework/bridges/phase-20/bridge_MH2_overlap_hierarchy.py"
FG2 = SOURCE_ROOT / "merged-framework/bridges/phase-11/bridge_FG2_family_tower.py"
FG4 = SOURCE_ROOT / (
    "merged-framework/bridges/phase-11/bridge_FG4_cp_kobayashi_maskawa.py"
)
WM9 = SOURCE_ROOT / (
    "merged-framework/bridges/phase-39/"
    "bridge_WM9_scalar_multiplicity_from_condensate.py"
)
SOURCE_SHA256 = "07611b1eb63450e7e82ab696eafe8566a6931a9acae9ccfbebe1823765ac4a65"
RELEASE_SHA256 = "d4a34703c842ced4804bf3ad87378529f753cd75a532c7ef559dcef46627d6a5"
FORMULA_FREEZE_SHA256 = "fa1bdb71ad94a98ee3938d502d8292143c9a421856a0f93a54321c5564a6f5b2"
ROOT_MAPPING = [
    "C-QBL-001",
    "C-QBL-003",
    "C-OVL-001",
    "C-OVL-002",
    "C-MIX-002",
    "C-QBL-005",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def module_assignments(path: Path) -> dict[str, ast.AST]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    assignments: dict[str, ast.AST] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                assignments[target.id] = node.value
    return assignments


def numeric_literal(node: ast.AST) -> float:
    value = ast.literal_eval(node)
    if not isinstance(value, (int, float)):
        raise TypeError(f"expected numeric literal, got {value!r}")
    return float(value)


def main() -> int:
    checks = CheckLedger("P209-GC2-DECLARED-WELL-AUDIT")
    checks.check("source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        digest(ROOT / "governance/releases/v0.151.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned",
        digest(CAMPAIGN / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    source_calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source predicate inventory remains exact",
        len(source_calls) == 8
        and sum(isinstance(node, ast.Assert) for node in ast.walk(source_tree)) == 2,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "source has no NumPy quadrature compatibility surface",
        compatibility.legacy_references
        == compatibility.current_references
        == compatibility.eager_legacy_default_fallbacks
        == 0,
    )

    mh2_assignments = module_assignments(MH2)
    source_assignments = module_assignments(SOURCE)
    wm9_assignments = module_assignments(WM9)
    depth = sp.Rational(str(numeric_literal(mh2_assignments["WELL_DEPTH"])))
    width = sp.Rational(str(numeric_literal(mh2_assignments["WELL_W"])))
    spacing = sp.Rational(str(numeric_literal(mh2_assignments["D_SPACING"])))
    rung_count = int(numeric_literal(mh2_assignments["N_GEN"]))
    checks.check(
        "MH2 external-well inputs are bare source literals",
        (depth, width, spacing, rung_count)
        == (sp.Integer(12), sp.Rational(7, 10), sp.Integer(4), 6),
    )
    checks.check(
        "GC2 executes six supplied centers rather than a three-member construction",
        rung_count == 6
        and "range(MH2_N_GEN)" in source_text
        and "three-soliton" in source_text,
    )
    checks.check(
        "WM9 generation count is a literal tuple cardinality",
        ast.literal_eval(wm9_assignments["MODES"]) == (1, 2, 3)
        and "n_modes = len(MODES)" in WM9.read_text(encoding="utf-8"),
    )
    checks.check(
        "changing a supplied center list changes its count",
        len(tuple(range(2))) == 2
        and len(tuple(range(4))) == 4
        and len(tuple(range(rung_count))) == 6,
    )

    centers = tuple(sp.Integer(n) * spacing for n in range(rung_count))
    grounds = [poschl_teller_ground_ledger(depth, width, center) for center in centers]
    checks.check(
        "canonical translated wells are exactly isospectral",
        len({sp.simplify(ground.eigenvalue) for ground in grounds}) == 1
        and all(ground.index == grounds[0].index for ground in grounds),
    )
    checks.check(
        "canonical translated family retains supplied centers",
        tuple(ground.center for ground in grounds) == centers,
    )
    index = grounds[0].index
    variance = sp.simplify(width**2 * sp.polygamma(1, index) / 2)
    centered_width = sp.sqrt(variance)
    t = sp.symbols("t", real=True)
    log_characteristic = (
        sp.loggamma(index + sp.I * width * t / 2)
        + sp.loggamma(index - sp.I * width * t / 2)
        - 2 * sp.loggamma(index)
    )
    centered_mean = sp.simplify(
        sp.diff(log_characteristic, t).subs(t, 0) / sp.I
    )
    derived_variance = sp.simplify(
        -sp.diff(log_characteristic, t, 2).subs(t, 0)
    )
    checks.check(
        "characteristic function derives translated means and centered variance",
        centered_mean == 0
        and derived_variance == variance
        and variance.is_positive is True
        and all(sp.simplify(center + centered_mean) == center for center in centers),
    )
    checks.check(
        "origin RMS and centered width are distinct under nonzero translation",
        all(sp.simplify(center**2 + variance - variance) == center**2 for center in centers)
        and all(center**2 + variance != variance for center in centers[1:]),
    )
    checks.check(
        "exact centered width matches source regression but needs no finite box",
        abs(float(sp.N(centered_width, 16)) - 0.4005) < 2.0e-3,
    )
    checks.check(
        "translation alone drives centered-width over displacement to zero",
        sp.limit(centered_width / sp.Symbol("R", positive=True), sp.Symbol("R", positive=True), sp.oo)
        == 0,
    )
    checks.check(
        "source quantity named centroid is actually mean absolute coordinate",
        "cent = float(np.sum(d * np.abs(xi)) * h)" in source_text
        and "np.sum(d * xi) * h" in source_text,
    )
    checks.check(
        "source refinement omits width ratio and domain convergence",
        "conv = max(abs(a[0] - b[0])" in source_text
        and "Lbox = MH2_N_GEN * MH2_D_SPACING + 8.0" in source_text
        and "abs(a[1] - b[1])" not in source_text,
    )
    function_names = {
        node.name for node in source_tree.body if isinstance(node, ast.FunctionDef)
    }
    checks.check(
        "GC2 builds no common nonlinear multisoliton field solution",
        function_names == {"check", "read_source", "literal", "mh2_mode_stats"}
        and "solve_ivp" not in source_text
        and "eigh_tridiagonal" in source_text,
    )

    omega = sp.Rational(9, 20)
    kappa_squared = sp.Rational(1, 2) - omega**2
    core_depths = tuple(
        sp.simplify(6 * kappa_squared * sp.sech(sp.sqrt(kappa_squared) * center) ** 2)
        for center in centers
    )
    ratios = tuple(sp.N(depth / value, 30) for value in core_depths)
    checks.check(
        "quartic core depth differs from every planted fixed well",
        all(sp.N(value - depth, 30) != 0 for value in core_depths),
    )
    checks.check(
        "fixed-well to quartic-core ratio grows on the supplied positive ladder",
        all(ratios[index_] < ratios[index_ + 1] for index_ in range(len(ratios) - 1))
        and ratios[-1] > sp.Integer(10) ** 9,
    )
    checks.check(
        "core-derived depth mutation destroys external-family isospectrality",
        len(
            {
                sp.N(poschl_teller_ground_ledger(value, width).eigenvalue, 20)
                for value in core_depths
            }
        )
        == rung_count,
    )

    x = sp.symbols("x", real=True)
    kappa = sp.symbols("kappa", positive=True)
    p = sp.symbols("p", positive=True)
    sech_p = sp.sech(kappa * x) ** p
    potential = kappa**2 - 6 * kappa**2 * sp.sech(kappa * x) ** 2
    applied = sp.simplify(-sp.diff(sech_p, x, 2) + potential * sech_p)
    residual = sp.trigsimp(
        applied - kappa**2 * (1 - p**2) * sech_p,
        method="fu",
    )
    expected = (
        kappa**2
        * (p * (p + 1) - 6)
        * sp.sech(kappa * x) ** (p + 2)
    )
    checks.check(
        "sech-power residual is derived rather than copied",
        sp.simplify(sp.expand_trig(residual - expected)) == 0,
    )
    checks.check(
        "only p two in WM9's supplied tuple is a pure sech eigenfunction",
        sp.simplify(expected.subs(p, 2)) == 0
        and all(sp.simplify(expected.subs(p, value)) != 0 for value in (1, 3)),
    )

    bound_values = quartic_fluctuation_bound_eigenvalues(omega)
    bound_modes = quartic_fluctuation_bound_modes(x, omega)
    checks.check(
        "canonical quartic spectrum contains one negative and one zero Hessian level",
        bound_values[0] < 0 and bound_values[1] == 0,
    )
    checks.check(
        "canonical odd level is exactly the translation tangent",
        sp.simplify(
            quartic_fluctuation_operator(bound_modes[1], x, omega)
            - bound_values[1] * bound_modes[1]
        )
        == 0,
    )
    checks.check(
        "removing the collective zero leaves a negative Hessian level not a particle tower",
        tuple(value for value in bound_values if value != 0) == (bound_values[0],)
        and bound_values[0] < 0,
    )
    checks.check(
        "GC2 hard-codes the noncanonical exact-sine count",
        numeric_literal(source_assignments["fg2_sg_count"]) == 3.0,
    )
    dispositions = load(ROOT / "migration/dispositions.yaml")["units"]
    checks.check(
        "accepted FG2 disposition rejects the exact-sine third level",
        "exact-sine third level violates" in dispositions["FG2"]["qualification"]
        and dispositions["FG2"]["accepted_claims"] == ["C-QBL-001", "C-QBL-003"],
    )

    fg2_text = FG2.read_text(encoding="utf-8")
    fg4_text = FG4.read_text(encoding="utf-8")
    wm9_text = WM9.read_text(encoding="utf-8")
    checks.check(
        "FG2 and FG4 independently disclaim derivation of count three",
        "NOT forced to 3" in fg2_text
        and "number of families N stays an INPUT" in fg4_text,
    )
    checks.check(
        "WM9 nevertheless attributes its literal three to FG4",
        "which FG4 fixes at" in wm9_text and "MODES = (1, 2, 3)" in wm9_text,
    )
    checks.check(
        "GC2 anti-fit globals test does not scan reachable source strings",
        "in_scope = measured_names & set(globals().keys())" in source_text
        and "SRC_WM9 = read_source" in source_text
        and "SIN2_MEASURED" in wm9_text,
    )

    claims = {
        claim["id"]: claim
        for claim in load(ROOT / "governance/claims.yaml")["claims"]
    }
    checks.check(
        "translated-well claim retains external supplied-family ceiling",
        all(
            phrase in claims["C-OVL-002"]["statement"]
            for phrase in (
                "Translation changes R but not its spectrum",
                "common multi-rung spectrum",
                "generation count",
            )
        ),
    )
    checks.check(
        "quartic spectrum claim rejects particle and generation interpretation",
        "not positive particle masses or generations"
        in claims["C-QBL-003"]["statement"],
    )
    checks.check(
        "phase-count claim rejects observed family-count interpretation",
        "observed family count" in claims["C-MIX-002"]["statement"],
    )
    checks.check(
        "quartic core claim rejects a multisoliton conclusion",
        "multisoliton solution" in claims["C-QBL-005"]["statement"],
    )
    checks.check(
        "no reserved duplicate claim has entered the registry",
        "C-OVL-004" not in claims,
    )

    proposal = load(CAMPAIGN / "proposal.yaml")
    queue = load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}
    expected_status = (
        "qualified" if proposal["status"] == "accepted" else "pending_adjudication"
    )
    expected_mapping = ROOT_MAPPING if expected_status == "qualified" else []
    checks.check(
        "GC2 governed mapping matches campaign stage",
        units["GC2"]["disposition"] == expected_status
        and units["GC2"]["accepted_claims"] == expected_mapping,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
