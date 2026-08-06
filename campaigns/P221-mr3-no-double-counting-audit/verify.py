"""Primary exact and governance verifier for P221 MR3 and C-VAR-003."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.variational import finite_functional_interaction_ledger
from substrate_framework.verification import CheckLedger


CAMPAIGN = Path(__file__).resolve().parent
ROOT = CAMPAIGN.parents[1]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-44/"
    "bridge_MR3_no_double_counting.py"
)
SOURCE_SHA = "c5eaabaeede15909adb5d9ddb951353c376aaa381e669e35c6256d7015e7eddc"
FREEZE_SHA = "3161bee76001a24f0b9d8b41b892a32eb74597145c5a2d406975398f79f7363b"


def _quadratic_minimum(expression: sp.Expr, coordinate: sp.Symbol) -> sp.Expr:
    stationary = sp.solve(sp.diff(expression, coordinate), coordinate)
    if len(stationary) != 1:
        raise ValueError("expected one quadratic stationary point")
    return sp.simplify(expression.subs(coordinate, stationary[0]))


def _quadratic_interaction(second_center: sp.Expr) -> sp.Expr:
    coordinate = sp.symbols("x", real=True)
    base = coordinate**2
    first = (coordinate - 1) ** 2
    second = (coordinate - second_center) ** 2
    return finite_functional_interaction_ledger(
        _quadratic_minimum(base, coordinate),
        _quadratic_minimum(base + first, coordinate),
        _quadratic_minimum(base + second, coordinate),
        _quadratic_minimum(base + first + second, coordinate),
    ).interaction


def main() -> int:
    checks = CheckLedger("P221")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source and preregistered formula surface are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA
        and hashlib.sha256(
            (CAMPAIGN / "evidence/formula-freeze.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(source_tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source inventory separates six predicates and three assertions",
        len(calls) == 6 and len(assertions) == 3,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    current_scipy_import = any(
        isinstance(node, ast.ImportFrom)
        and node.module == "scipy.integrate"
        and any(alias.name == "trapezoid" for alias in node.names)
        for node in ast.walk(source_tree)
    )
    checks.check(
        "MR3 uses current SciPy trapezoid with no legacy NumPy version event",
        compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0
        and current_scipy_import,
    )
    reproduction = yaml.safe_load(
        (CAMPAIGN / "evidence/source-reproduction.yaml").read_text()
    )
    checks.check(
        "one native reproduction reached the six-check terminal tally",
        reproduction["native_run"]["exit_status"] == 0
        and reproduction["inventory"]["runtime_check_executions"] == 6
        and reproduction["native_run"]["terminal_tally"] == "ALL_6_CHECKS_PASS",
    )

    base_value, first_value, second_value = sp.symbols("A P Q", real=True)
    pointwise_mixed = sp.expand(
        (base_value + first_value + second_value)
        + base_value
        - (base_value + first_value)
        - (base_value + second_value)
    )
    checks.check(
        "the corresponding pointwise inclusion-exclusion expression vanishes",
        pointwise_mixed == 0,
    )
    m_a, m_ap, m_aq, m_apq = sp.symbols(
        "m_A m_AP m_AQ m_APQ",
        real=True,
    )
    ledger = finite_functional_interaction_ledger(m_a, m_ap, m_aq, m_apq)
    checks.check(
        "canonical ledger is the exact four-infimum mixed difference",
        ledger.interaction == m_apq + m_a - m_ap - m_aq
        and ledger.identity_residual == 0,
    )
    swapped = finite_functional_interaction_ledger(m_a, m_aq, m_ap, m_apq)
    checks.check(
        "the interaction is symmetric in the two additions",
        sp.simplify(swapped.interaction - ledger.interaction) == 0,
    )
    shift_a, shift_p, shift_q = sp.symbols("c_A c_P c_Q", real=True)
    shifted = finite_functional_interaction_ledger(
        m_a + shift_a,
        m_ap + shift_a + shift_p,
        m_aq + shift_a + shift_q,
        m_apq + shift_a + shift_p + shift_q,
    )
    checks.check(
        "consistent additive functional constants cancel exactly",
        sp.simplify(shifted.interaction - ledger.interaction) == 0,
    )

    positive = _quadratic_interaction(-1)
    negative = _quadratic_interaction(1)
    zero_center = 2 + sp.sqrt(3)
    zero = _quadratic_interaction(zero_center)
    checks.check(
        "nonnegative continuous coercive quadratics realize both signs and zero",
        positive == 1 and negative == -sp.Rational(1, 3) and zero == 0,
    )
    magnitude = sp.symbols("r", positive=True)
    positive_scaled = finite_functional_interaction_ledger(
        0,
        magnitude / 2,
        magnitude / 2,
        2 * magnitude,
    )
    negative_scaled = finite_functional_interaction_ledger(
        0,
        3 * magnitude / 2,
        3 * magnitude / 2,
        2 * magnitude,
    )
    checks.check(
        "positive scaling gives every positive and negative real magnitude",
        positive_scaled.interaction == magnitude
        and negative_scaled.interaction == -magnitude,
    )
    checks.mutation_sensitive(
        "zero interaction does not survive a generic optimizer-center mutation",
        lambda center: sp.simplify(_quadratic_interaction(center)) == 0,
        zero_center,
        (-1, 0, 1),
    )

    coordinate = sp.symbols("x", real=True)
    common_base = coordinate**2
    common_first = 2 * coordinate**2
    common_second = 3 * coordinate**2
    common = finite_functional_interaction_ledger(
        _quadratic_minimum(common_base, coordinate),
        _quadratic_minimum(common_base + common_first, coordinate),
        _quadratic_minimum(common_base + common_second, coordinate),
        _quadratic_minimum(common_base + common_first + common_second, coordinate),
    )
    checks.check(
        "a common minimizer of all three functionals is sufficient for zero",
        common.interaction == 0,
    )
    separate_minimizers = (
        set(sp.solve(sp.diff(coordinate**2, coordinate), coordinate)),
        set(sp.solve(sp.diff((coordinate - 1) ** 2, coordinate), coordinate)),
        set(
            sp.solve(
                sp.diff((coordinate - zero_center) ** 2, coordinate),
                coordinate,
            )
        ),
    )
    checks.check(
        "zero interaction does not imply a common minimizer",
        zero == 0 and set.intersection(*separate_minimizers) == set(),
    )

    numeric_scope = yaml.safe_load(
        (CAMPAIGN / "evidence/numeric-scope-audit.yaml").read_text()
    )
    reported = numeric_scope["reported_source_values"]
    reported_interaction = sp.Rational(str(reported["b_full"])) + sp.Rational(
        str(reported["b_classical"])
    ) - sp.Rational(str(reported["b_L0_only"])) - sp.Rational(
        str(reported["b_L6_only"])
    )
    checks.check(
        "MR3 reports one positive mixed interaction but not a sign theorem",
        reported_interaction > 0
        and numeric_scope["accepted_scope"] == "single_unrefined_stationary_branch_example",
    )
    solver = reproduction["solver_surface"]
    checks.check(
        "source numeric branch lacks every oracle needed for a minimizer claim",
        solver["routine"] == "scipy.integrate.solve_bvp"
        and set(solver["missing_oracles"])
        == {
            "mesh_refinement",
            "domain_refinement",
            "tolerance_refinement",
            "residual_norm",
            "Derrick_residual",
            "independent_method",
            "minimizer_proof",
        },
    )
    assigned_names = {
        target.id: node.value
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
    }
    loaded_names = {
        node.id
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    naive_sum = assigned_names.get("naive_sum")
    checks.check(
        "source itself forms the sum whose corpus-level absence it claims",
        isinstance(naive_sum, ast.BinOp)
        and isinstance(naive_sum.op, ast.Add)
        and {naive_sum.left.id, naive_sum.right.id}
        == {"M_classical_sector", "E_BPS_1"},
    )
    checks.check(
        "the alleged full recomputation snapshot is never consumed",
        "derived_snapshot" in assigned_names and "derived_snapshot" not in loaded_names,
    )
    guard_expression = assigned_names.get("indep")
    guard_text = ast.unparse(guard_expression) if guard_expression is not None else ""
    checks.check(
        "MR3.6 compares no solved branch despite saying all four are bit-identical",
        all(name not in guard_text for name in ("b_cl", "b_L0", "b_L6", "b_full"))
        and all(name in guard_text for name in ("E_DER", "C6", "C0", "E_BPS_1")),
    )

    lower_bound, slack = sp.symbols("L s", real=True, nonnegative=True)
    realized_value = lower_bound + slack
    checks.check(
        "a nonnegative slack separates a lower bound from a profile term value",
        sp.simplify(realized_value - lower_bound) == slack
        and realized_value.subs(slack, 1) != lower_bound,
    )
    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())
    claims = {entry["id"]: entry for entry in registry["claims"]}
    proposal = yaml.safe_load((CAMPAIGN / "proposal.yaml").read_text())
    interaction_claim_state_ok = (
        claims["C-VAR-003"]["review"] == "accepted"
        and claims["C-VAR-003"]["dependencies"] == []
        if proposal["status"] == "accepted"
        else "C-VAR-003" not in claims
    )
    checks.check(
        "C-VAR-002 owns joint order but not the four-infimum interaction",
        claims["C-VAR-002"]["review"] == "accepted"
        and "inf_{x in X} sum_i E_i(x)" in claims["C-VAR-002"]["statement"]
        and interaction_claim_state_ok,
    )
    checks.check(
        "the exact interaction API adds no physical field parameter or comparator",
        ledger.interaction.free_symbols == {m_a, m_ap, m_aq, m_apq}
        and ledger.interaction.free_symbols.isdisjoint(
            {sp.Symbol(name) for name in ("m_e", "m_pi", "m_rho", "m_N")}
        ),
    )
    delta = yaml.safe_load(
        (CAMPAIGN / "evidence/post-source-claim-delta.yaml").read_text()
    )
    checks.check(
        "the governed delta retains only the exact dependency-free theorem",
        delta["provisional_claim"] == "C-VAR-003"
        and delta["decision"] == "retain_for_exact_implementation_and_independent_review"
        and "physical_double_counting_refutation" in delta["excluded_source_surfaces"],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
