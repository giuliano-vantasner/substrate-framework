"""Fresh exact authority and strictness review for P224 without MR6 imports."""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN = Path(__file__).resolve().parents[1]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-44/"
    "bridge_MR6_ledger_and_confrontation.py"
)


def main() -> int:
    checks = CheckLedger("P224-independent")
    lambda_a, mu, average = sp.symbols("lambda_A mu W", positive=True)
    lambda_bps = lambda_a / sp.pi**2
    checks.check(
        "fresh same-current conversion removes pi squared exactly",
        sp.simplify(2 * lambda_bps * mu * sp.pi**2 * average - 2 * lambda_a * mu * average)
        == 0,
    )
    pion, color = sp.symbols("m_pi N_c", positive=True)
    corrected = 8 * sp.sqrt(2) * color * pion / (15 * sp.pi)
    wrong = 8 * sp.sqrt(2) * sp.pi * color * pion / 15
    checks.check(
        "fresh conditional formulas differ by exactly pi squared",
        sp.simplify(wrong - sp.pi**2 * corrected) == 0,
    )
    checks.check(
        "fresh numeric evaluation retains supplied color and pion inputs",
        abs(float(corrected.subs({color: 3, pion: sp.Rational(13803, 100)})) - 99.41652889533228)
        < 1.0e-12
        and corrected.free_symbols == {color, pion},
    )

    base = (0, 1)
    nonnegative_addition = (0, 1)
    joint = tuple(x + y for x, y in zip(base, nonnegative_addition))
    checks.check(
        "fresh finite counterexample refutes positivity-somewhere strictness",
        min(base) == min(joint) == 0
        and nonnegative_addition[1] > 0
        and all(value >= 0 for value in nonnegative_addition),
    )
    base2 = (0, 3)
    addition2 = (2, 0)
    joint2 = tuple(x + y for x, y in zip(base2, addition2))
    checks.check(
        "strictness is possible but needs minimizer incompatibility data",
        min(joint2) > min(base2) + min(addition2),
    )
    scale, first, second = sp.symbols("s c6 c0", nonnegative=True)
    tangent = sp.Matrix(
        [sp.diff(scale**2 * first, scale), sp.diff(scale**2 * second, scale)]
    )
    checks.check(
        "one common scale path has rank one in two coefficient coordinates",
        tangent.rank() == 1,
    )

    ledger = yaml.safe_load(
        (CAMPAIGN / "evidence/authority-ledger.yaml").read_text()
    )
    checks.check(
        "fresh authority review finds no accepted claim overturned by MR6",
        ledger["counts"]["accepted_claims_changed_by_MR6"] == 0
        and ledger["rows"]["MK6_3"]["governed_result"]
        == "physical_double_counting_diagnosis_rejected_not_later_overturned",
    )
    dispositions = yaml.safe_load((ROOT / "migration/dispositions.yaml").read_text())[
        "units"
    ]
    checks.check(
        "all predecessor MK and MR units have individual terminal dispositions",
        all(
            dispositions[label]["disposition"]
            in {"qualified", "duplicate_evidence", "refuted", "out_of_scope", "migrated"}
            for label in (
                "MK1", "MK2", "MK3", "MK4", "MK5", "MK6",
                "MR1", "MR2", "MR3", "MR4", "MR5",
            )
        ),
    )
    p223 = yaml.safe_load(
        (
            ROOT
            / "campaigns/P223-mr5-derived-coupling-solve-audit/evidence/primary-numerical-evidence.yaml"
        ).read_text()
    )
    checks.check(
        "fresh ledger uses governed MR5 regression rather than stale prose",
        abs(p223["domains"]["R20"]["kappa"] - 11.536444259568) < 1.0e-12
        and ledger["rows"]["MR6_2"]["governed_result"]
        == "no_accepted_physical_confrontation_and_source_kappa_stale_after_P223",
    )

    source_text = SOURCE.read_text()
    source_tree = ast.parse(source_text)
    literals = {
        float(node.value)
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
    }
    checks.check(
        "fresh AST review finds comparator data outside guard needles",
        {938.92, 1836.15}.issubset(literals)
        and "FORBIDDEN = [929 / 1000.0, 28296 / 1000.0]" in source_text,
    )
    independent_assignment = next(
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "indep" for target in node.targets)
    )
    independent_names = {
        node.id for node in ast.walk(independent_assignment.value) if isinstance(node, ast.Name)
    }
    checks.check(
        "fresh guard review confirms solved branches are not recomputed",
        independent_names.isdisjoint({"B_CL", "B_FULL", "B_L0", "bs"}),
    )
    delta = yaml.safe_load(
        (CAMPAIGN / "evidence/post-source-claim-delta.yaml").read_text()
    )
    checks.check(
        "fresh review finds only existing exact owners and no package delta",
        set(delta["unchanged_exact_owners"])
        == {"C-BPS-001", "C-VEC-002", "C-VAR-002"}
        and delta["reserved_identifiers"] == []
        and delta["package_change"] == "none",
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
