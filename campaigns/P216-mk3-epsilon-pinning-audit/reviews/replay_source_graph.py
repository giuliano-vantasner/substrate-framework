"""Hash-sensitive P216 source graph replay with governed execution reuse."""

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
    SourceNode("B1", "merged-framework/bridges/phase-7/bridge_B1_disclination_berry_connection.py", "2de4faa60ecc1f87ca356afd55c2a531a89327c3c46e4296176052113de7b0b6", 8, 1, "candidate_predecessor"),
    SourceNode("E3", "merged-framework/bridges/phase-29/bridge_E3_yield_coefficient_overbinding.py", "aa76b9e675d4fbb45594e9d3df5107af175e927a24840260ca71ffda1bad3315", 5, 1, "candidate_predecessor"),
    SourceNode("E4", "merged-framework/bridges/phase-29/bridge_E4_bps_zero_binding_resolution.py", "f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7", 5, 1, "candidate_predecessor"),
    SourceNode("HE4", "merged-framework/bridges/phase-45/bridge_HE4_dhn_action_variable.py", "0fae1f54748a5206214afaeb1fb7293f46c04c6146e1779c41837fddaf245f29", 16, 1, "candidate_predecessor"),
    SourceNode("KI2", "merged-framework/bridges/phase-34/bridge_KI2_epsilon_underdetermination.py", "9e16fc6fafa940f43d559ea0f6a9c2730940d1247f36f655375c2f75f6fd1e81", 6, 1, "qualified_predecessor"),
    SourceNode("KI4", "merged-framework/bridges/phase-34/bridge_KI4_backsolve_circularity.py", "138f204c2bf7e7278a1a4aadad4bed1680e11b6b6de7189a02640a81652f00cd", 5, 1, "qualified_predecessor"),
    SourceNode("MK1", "merged-framework/bridges/phase-43/bridge_MK1_mu_from_medium_cosine.py", "98ff5459ae3c6cb64a9a7632fbaa8613f1f5b1adb68419de25ffa06b1c3a3222", 7, 1, "qualified_predecessor"),
    SourceNode("MK2", "merged-framework/bridges/phase-43/bridge_MK2_lambda_from_medium_omega.py", "351136bca28e413ddd54f1b15bf7084dffe32af565fc87e7220d1437a525eb07", 7, 1, "qualified_predecessor"),
    SourceNode("MK3", "merged-framework/bridges/phase-43/bridge_MK3_epsilon_pinned.py", "64254d0f6b9d6ff57f5a8b0a4b86a510e2bef230b4f3bec062533fac59516404", 6, 1, "audited_root"),
    SourceNode("MK4", "merged-framework/bridges/phase-43/bridge_MK4_bps_compacton_and_pt_failure.py", "9f2e299032aace53c3ac2c2d1d5626372e4bdf1aa3b7b0650f574a9f7b8f7295", 6, 1, "pending_reverse_consumer"),
    SourceNode("MK5", "merged-framework/bridges/phase-43/bridge_MK5_generalized_solve_kappa.py", "a5ecb5d0d2ba96cf8083a9cfb32ddb44c2a4f4841bf776ebbccb91bc12b246f8", 8, 1, "pending_reverse_consumer"),
    SourceNode("MK6", "merged-framework/bridges/phase-43/bridge_MK6_confrontation_and_tension.py", "ef900954d9782bbf2589ff3e33045577ebdce3860d1a3ed7a6a6827e0ae81788", 6, 1, "pending_reverse_consumer"),
    SourceNode("NY1", "merged-framework/bridges/phase-24/bridge_NY1_skyrme_energy_unit.py", "b3531d7f906fe396a1326d44d68f34d09ae34988e86a8f721c360040c4aa0921", 9, 0, "duplicate_predecessor"),
    SourceNode("MR2", "merged-framework/bridges/phase-44/bridge_MR2_bps_normalization_pi_squared.py", "2e62ce2d6cbee805a988046a27a742e622931291e8e013a9aede6ce16e48e990", 8, 1, "pending_reverse_consumer"),
    SourceNode("MR6", "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py", "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d", 6, 3, "pending_reverse_consumer"),
)

REUSED_CONSUMERS = {"MK4", "MK5", "MK6", "MR2", "MR6"}
TALLY = re.compile(r"ALL\s+(\d+)\s+CHECKS\s+PASS(?:ED)?", re.IGNORECASE)


def main() -> int:
    checks = CheckLedger("P216-GRAPH")
    rows: list[dict[str, object]] = []
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
    expected = {node.label: node for node in NODES}
    checks.check(
        "all fifteen graph nodes retain their pinned hashes",
        len(rows) == 15 and all(bool(row["hash_ok"]) for row in rows),
    )
    checks.check(
        "graph inventory pins 108 predicates and 16 assertions",
        sum(int(row["checks"]) for row in rows) == 108
        and sum(int(row["assertions"]) for row in rows) == 16
        and all(
            row["checks"] == expected[str(row["label"])].checks
            and row["assertions"] == expected[str(row["label"])].assertions
            for row in rows
        ),
    )

    root_path = SOURCE_ROOT / expected["MK3"].path
    root_result = subprocess.run(
        [str(ROOT / ".venv/bin/python"), str(root_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    terminal = TALLY.findall(root_result.stdout)
    checks.check(
        "MK3 root freshly reaches its six-check terminal tally",
        root_result.returncode == 0 and terminal and int(terminal[-1]) == 6,
    )

    dispositions = yaml.safe_load(
        (ROOT / "migration/dispositions.yaml").read_text()
    )["units"]
    checks.check(
        "every authoritative predecessor is consumed only at its governed disposition",
        all(
            label in dispositions
            and dispositions[label]["disposition"]
            in {"qualified", "duplicate_evidence"}
            for label in ["B1", "E3", "E4", "HE4", "KI2", "KI4", "MK1", "MK2", "NY1"]
        ),
    )
    checks.check(
        "reverse consumers remain nonauthoritative and name the MK3 value or source",
        all(label not in dispositions for label in REUSED_CONSUMERS)
        and "MK3" in str(by_label["MK4"]["text"])
        and "MK3" in str(by_label["MK5"]["text"])
        and "0.496" in str(by_label["MK6"]["text"])
        and "MK3" in str(by_label["MR2"]["text"])
        and "MK3" in str(by_label["MR6"]["text"]),
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
        "unchanged expensive reverse-consumer executions are hash-reused from P215",
        all(
            prior_rows[label]["verdict"] == "clean_noncanonical"
            and expected[label].sha256 in prior_script
            and bool(by_label[label]["hash_ok"])
            for label in REUSED_CONSUMERS
        ),
    )
    checks.check(
        "MK3 itself has no integration-name compatibility surface",
        by_label["MK3"]["legacy"] == 0
        and by_label["MK3"]["current"] == 0
        and by_label["MK3"]["eager"] == 0,
    )
    checks.check(
        "inherited B1 and E3 version surfaces remain compatibility provenance only",
        by_label["B1"]["legacy"] == 1
        and by_label["B1"]["current"] == 1
        and by_label["B1"]["eager"] == 1
        and by_label["E3"]["legacy"] == 1
        and by_label["E3"]["current"] == 1
        and by_label["E3"]["eager"] == 0
        and all(
            int(row["legacy"]) == 0
            and int(row["current"]) == 0
            and int(row["eager"]) == 0
            for row in rows
            if row["label"] not in {"B1", "E3"}
        ),
    )
    checks.check(
        "dirty untracked later source work is excluded from the pinned graph",
        all(not node.label.startswith(("BM", "CE")) for node in NODES),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())

