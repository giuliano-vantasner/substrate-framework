"""Hash-sensitive P217 source graph replay with governed execution reuse."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
import subprocess

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")


@dataclass(frozen=True)
class SourceNode:
    label: str
    path: str
    sha256: str
    checks: int
    assertions: int
    relation: str


NODES = (
    SourceNode("E2", "merged-framework/bridges/phase-29/bridge_E2_multi_skyrmion_solutions.py", "fdde30878eaf1f8dff7fce9c2d9d4234d1d6e14566be6d2ee56dd1926481c46f", 6, 1, "qualified_predecessor"),
    SourceNode("E4", "merged-framework/bridges/phase-29/bridge_E4_bps_zero_binding_resolution.py", "f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7", 5, 1, "qualified_predecessor"),
    SourceNode("KI3", "merged-framework/bridges/phase-34/bridge_KI3_bracket_is_sharp.py", "10e92457cbd213782e5778f5b739660a6d07ea229c44746e24fe0132844fcbd3", 5, 1, "qualified_predecessor"),
    SourceNode("MK1", "merged-framework/bridges/phase-43/bridge_MK1_mu_from_medium_cosine.py", "98ff5459ae3c6cb64a9a7632fbaa8613f1f5b1adb68419de25ffa06b1c3a3222", 7, 1, "qualified_predecessor"),
    SourceNode("MK2", "merged-framework/bridges/phase-43/bridge_MK2_lambda_from_medium_omega.py", "351136bca28e413ddd54f1b15bf7084dffe32af565fc87e7220d1437a525eb07", 7, 1, "qualified_predecessor"),
    SourceNode("MK3", "merged-framework/bridges/phase-43/bridge_MK3_epsilon_pinned.py", "64254d0f6b9d6ff57f5a8b0a4b86a510e2bef230b4f3bec062533fac59516404", 6, 1, "qualified_predecessor"),
    SourceNode("MK4", "merged-framework/bridges/phase-43/bridge_MK4_bps_compacton_and_pt_failure.py", "9f2e299032aace53c3ac2c2d1d5626372e4bdf1aa3b7b0650f574a9f7b8f7295", 6, 1, "audited_root"),
    SourceNode("MK5", "merged-framework/bridges/phase-43/bridge_MK5_generalized_solve_kappa.py", "a5ecb5d0d2ba96cf8083a9cfb32ddb44c2a4f4841bf776ebbccb91bc12b246f8", 8, 1, "pending_reverse_consumer"),
    SourceNode("MK6", "merged-framework/bridges/phase-43/bridge_MK6_confrontation_and_tension.py", "ef900954d9782bbf2589ff3e33045577ebdce3860d1a3ed7a6a6827e0ae81788", 6, 1, "pending_reverse_consumer"),
    SourceNode("MR2", "merged-framework/bridges/phase-44/bridge_MR2_bps_normalization_pi_squared.py", "2e62ce2d6cbee805a988046a27a742e622931291e8e013a9aede6ce16e48e990", 8, 1, "pending_reverse_consumer"),
    SourceNode("MR6", "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py", "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d", 6, 3, "pending_reverse_consumer"),
)

PREDECESSORS = {"E2", "E4", "KI3", "MK1", "MK2", "MK3"}
REUSED_CONSUMERS = {"MK5", "MK6", "MR2", "MR6"}
TALLY = re.compile(r"ALL\s+(\d+)\s+CHECKS\s+PASS(?:ED)?", re.IGNORECASE)


def main() -> int:
    checks = CheckLedger("P217-GRAPH")
    rows: list[dict[str, object]] = []
    expected = {node.label: node for node in NODES}
    for node in NODES:
        path = SOURCE_ROOT / node.path
        payload = path.read_bytes()
        text = payload.decode("utf-8")
        tree = ast.parse(text, filename=node.path)
        compatibility = audit_numpy_trapezoid_compatibility(text, filename=node.path)
        rows.append(
            {
                "label": node.label,
                "hash_ok": hashlib.sha256(payload).hexdigest() == node.sha256,
                "checks": sum(
                    isinstance(item, ast.Call)
                    and isinstance(item.func, ast.Name)
                    and item.func.id == "check"
                    for item in ast.walk(tree)
                ),
                "assertions": sum(isinstance(item, ast.Assert) for item in ast.walk(tree)),
                "legacy": compatibility.legacy_references,
                "current": compatibility.current_references,
                "eager": compatibility.eager_legacy_default_fallbacks,
                "text": text,
            }
        )
    by_label = {str(row["label"]): row for row in rows}
    checks.check(
        "all eleven graph nodes retain their pinned hashes",
        len(rows) == 11 and all(bool(row["hash_ok"]) for row in rows),
    )
    checks.check(
        "graph inventory pins 70 predicates and 13 assertions",
        sum(int(row["checks"]) for row in rows) == 70
        and sum(int(row["assertions"]) for row in rows) == 13
        and all(
            row["checks"] == expected[str(row["label"])].checks
            and row["assertions"] == expected[str(row["label"])].assertions
            for row in rows
        ),
    )

    root = SOURCE_ROOT / expected["MK4"].path
    result = subprocess.run(
        [str(ROOT / ".venv/bin/python"), str(root)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    terminal = TALLY.findall(result.stdout)
    checks.check(
        "MK4 root freshly reaches its six-check terminal tally",
        result.returncode == 0 and terminal and int(terminal[-1]) == 6,
    )

    dispositions = yaml.safe_load(
        (ROOT / "migration/dispositions.yaml").read_text()
    )["units"]
    checks.check(
        "every predecessor is consumed only at its qualified disposition",
        all(
            label in dispositions and dispositions[label]["disposition"] == "qualified"
            for label in PREDECESSORS
        ),
    )
    checks.check(
        "later consumers remain nonauthoritative and explicitly depend on MK4",
        all(label not in dispositions for label in REUSED_CONSUMERS)
        and all("MK4" in str(by_label[label]["text"]) for label in REUSED_CONSUMERS),
    )

    prior_inventory = yaml.safe_load(
        (
            ROOT
            / "campaigns/P215-mk2-vector-sextic-matching-audit/evidence/source-graph-inventory.yaml"
        ).read_text()
    )
    prior_rows = {row["label"]: row for row in prior_inventory["replay"]}
    prior_script = (
        ROOT
        / "campaigns/P215-mk2-vector-sextic-matching-audit/reviews/replay_source_graph.py"
    ).read_text()
    checks.check(
        "unchanged expensive later executions are hash-reused from P215",
        all(
            prior_rows[label]["verdict"] == "clean_noncanonical"
            and expected[label].sha256 in prior_script
            and bool(by_label[label]["hash_ok"])
            for label in REUSED_CONSUMERS
        ),
    )
    checks.check(
        "MK4 uses current SciPy trapezoid with no legacy NumPy surface",
        by_label["MK4"]["legacy"] == 0
        and by_label["MK4"]["current"] == 0
        and by_label["MK4"]["eager"] == 0
        and "from scipy.integrate import trapezoid" in str(by_label["MK4"]["text"]),
    )
    checks.check(
        "E2 current-first fallback is compatibility provenance only",
        by_label["E2"]["legacy"] == 1
        and by_label["E2"]["current"] == 1
        and by_label["E2"]["eager"] == 0
        and all(
            int(row["legacy"]) == 0
            and int(row["current"]) == 0
            and int(row["eager"]) == 0
            for row in rows
            if row["label"] != "E2"
        ),
    )
    checks.check(
        "dirty untracked later source work is excluded from the pinned graph",
        all(not node.label.startswith(("BM", "CE")) for node in NODES),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
