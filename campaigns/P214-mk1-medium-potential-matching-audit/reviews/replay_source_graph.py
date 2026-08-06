"""Pinned predecessor and reverse-consumer replay for the P214 MK1 audit."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
import subprocess
import time

import numpy as np
import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
CAMPAIGN = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class SourceNode:
    label: str
    path: str
    sha256: str
    lexical_checks: int
    assertions: int
    relation: str


NODES = (
    SourceNode("E1", "merged-framework/bridges/phase-29/bridge_E1_rational_map_integrals.py", "1afa9ba8ade88912e7361bbbd6f59a9fce5cc114c75ddf604a6439bc066ae2d1", 6, 1, "qualified_predecessor"),
    SourceNode("E2", "merged-framework/bridges/phase-29/bridge_E2_multi_skyrmion_solutions.py", "fdde30878eaf1f8dff7fce9c2d9d4234d1d6e14566be6d2ee56dd1926481c46f", 6, 1, "qualified_predecessor"),
    SourceNode("E3", "merged-framework/bridges/phase-29/bridge_E3_yield_coefficient_overbinding.py", "aa76b9e675d4fbb45594e9d3df5107af175e927a24840260ca71ffda1bad3315", 5, 1, "qualified_predecessor"),
    SourceNode("E4", "merged-framework/bridges/phase-29/bridge_E4_bps_zero_binding_resolution.py", "f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7", 5, 1, "qualified_predecessor"),
    SourceNode("KI2", "merged-framework/bridges/phase-34/bridge_KI2_epsilon_underdetermination.py", "9e16fc6fafa940f43d559ea0f6a9c2730940d1247f36f655375c2f75f6fd1e81", 6, 1, "qualified_predecessor"),
    SourceNode("MC1", "merged-framework/bridges/phase-27/bridge_MC1_constitutive_reduction.py", "32ed770bb753a9d1f0e67620a66fa29355e84c430c150694ffdfdb3003a8d3f3", 24, 0, "qualified_predecessor"),
    SourceNode("MK1", "merged-framework/bridges/phase-43/bridge_MK1_mu_from_medium_cosine.py", "98ff5459ae3c6cb64a9a7632fbaa8613f1f5b1adb68419de25ffa06b1c3a3222", 7, 1, "audited_root"),
    SourceNode("MK2", "merged-framework/bridges/phase-43/bridge_MK2_lambda_from_medium_omega.py", "351136bca28e413ddd54f1b15bf7084dffe32af565fc87e7220d1437a525eb07", 7, 1, "pending_predecessor_and_reverse_consumer"),
    SourceNode("MK3", "merged-framework/bridges/phase-43/bridge_MK3_epsilon_pinned.py", "64254d0f6b9d6ff57f5a8b0a4b86a510e2bef230b4f3bec062533fac59516404", 6, 1, "pending_reverse_consumer"),
    SourceNode("MK4", "merged-framework/bridges/phase-43/bridge_MK4_bps_compacton_and_pt_failure.py", "9f2e299032aace53c3ac2c2d1d5626372e4bdf1aa3b7b0650f574a9f7b8f7295", 6, 1, "pending_reverse_consumer"),
    SourceNode("MK5", "merged-framework/bridges/phase-43/bridge_MK5_generalized_solve_kappa.py", "a5ecb5d0d2ba96cf8083a9cfb32ddb44c2a4f4841bf776ebbccb91bc12b246f8", 8, 1, "pending_reverse_consumer"),
    SourceNode("MK6", "merged-framework/bridges/phase-43/bridge_MK6_confrontation_and_tension.py", "ef900954d9782bbf2589ff3e33045577ebdce3860d1a3ed7a6a6827e0ae81788", 6, 1, "pending_reverse_consumer"),
    SourceNode("MR2", "merged-framework/bridges/phase-44/bridge_MR2_bps_normalization_pi_squared.py", "2e62ce2d6cbee805a988046a27a742e622931291e8e013a9aede6ce16e48e990", 8, 1, "pending_reverse_consumer"),
    SourceNode("MR6", "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py", "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d", 6, 3, "pending_reverse_consumer"),
    SourceNode("NY1", "merged-framework/bridges/phase-24/bridge_NY1_skyrme_energy_unit.py", "b3531d7f906fe396a1326d44d68f34d09ae34988e86a8f721c360040c4aa0921", 9, 0, "duplicate_predecessor"),
    SourceNode("PG2", "merged-framework/bridges/phase-18/bridge_PG2_gmor_pion_mass.py", "0502a53f65d3bd11a3f17d26d55ed7d67a1e0f61d194b38cd41728873c4a06ad", 4, 1, "qualified_predecessor"),
    SourceNode("S3", "merged-framework/bridges/phase-4/bridge_S3_su3_wzw_baryon_reps.py", "44d8cd1f3a3b3d0a316d0984db92d5e47e13cac9dcf3d476e2d996bf09f13b9a", 10, 2, "qualified_predecessor"),
)

DIRECT_PREDECESSORS = {"E1", "E2", "E3", "E4", "KI2", "MC1", "MK2", "NY1", "PG2", "S3"}
REVERSE_CONSUMERS = {"MK2", "MK3", "MK4", "MK5", "MK6", "MR2", "MR6"}
SAFE_LAZY_LEGACY = {"E1", "E2", "E3"}
TALLY = re.compile(r"ALL\s+(\d+)\s+CHECKS\s+PASS(?:ED)?", re.IGNORECASE)


def main() -> int:
    checks = CheckLedger("P214-GRAPH")
    rows: list[dict[str, object]] = []

    for node in NODES:
        path = SOURCE_ROOT / node.path
        payload = path.read_bytes()
        text = payload.decode("utf-8")
        tree = ast.parse(text, filename=node.path)
        lexical = sum(
            isinstance(item, ast.Call)
            and isinstance(item.func, ast.Name)
            and item.func.id == "check"
            for item in ast.walk(tree)
        )
        assertions = sum(isinstance(item, ast.Assert) for item in ast.walk(tree))
        compatibility = audit_numpy_trapezoid_compatibility(text, filename=node.path)
        started = time.monotonic()
        result = subprocess.run(
            [str(ROOT / ".venv/bin/python"), str(path)],
            cwd=SOURCE_ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        elapsed = time.monotonic() - started
        terminal = TALLY.findall(result.stdout)
        rows.append(
            {
                "label": node.label,
                "hash_ok": hashlib.sha256(payload).hexdigest() == node.sha256,
                "lexical_checks": lexical,
                "assertions": assertions,
                "legacy": compatibility.legacy_references,
                "current": compatibility.current_references,
                "eager": compatibility.eager_legacy_default_fallbacks,
                "returncode": result.returncode,
                "terminal": int(terminal[-1]) if terminal else None,
                "elapsed": elapsed,
                "mentions_MK1": "MK1" in text,
            }
        )

    checks.check(
        "all seventeen source nodes retain their pinned hashes",
        len(rows) == 17 and all(bool(row["hash_ok"]) for row in rows),
    )
    expected_by_label = {node.label: node for node in NODES}
    checks.check(
        "graph inventory pins 129 lexical predicates and 18 assertions",
        sum(int(row["lexical_checks"]) for row in rows) == 129
        and sum(int(row["assertions"]) for row in rows) == 18
        and all(
            row["lexical_checks"] == expected_by_label[str(row["label"])].lexical_checks
            and row["assertions"] == expected_by_label[str(row["label"])].assertions
            for row in rows
        ),
    )
    checks.check(
        "every node exits cleanly and reports its full runtime tally",
        all(
            row["returncode"] == 0
            and row["terminal"] == row["lexical_checks"]
            for row in rows
        ),
    )
    checks.check(
        "only E1 through E3 expose safe current-first lazy legacy branches",
        hasattr(np, "trapezoid")
        and not hasattr(np, "trapz")
        and {
            str(row["label"])
            for row in rows
            if int(row["legacy"]) > 0 or int(row["current"]) > 0
        }
        == SAFE_LAZY_LEGACY
        and all(
            int(row["legacy"]) == 1
            and int(row["current"]) == 1
            and int(row["eager"]) == 0
            for row in rows
            if row["label"] in SAFE_LAZY_LEGACY
        )
        and all(int(row["eager"]) == 0 for row in rows),
    )
    checks.check(
        "all seven declared reverse consumers name MK1 explicitly",
        {str(row["label"]) for row in rows if row["label"] in REVERSE_CONSUMERS}
        == REVERSE_CONSUMERS
        and all(bool(row["mentions_MK1"]) for row in rows if row["label"] in REVERSE_CONSUMERS),
    )
    proposal = yaml.safe_load((CAMPAIGN / "proposal.yaml").read_text())
    allowed = " ".join(proposal["allowed_imports"])
    checks.check(
        "pending reverse consumers are replayed as evidence and never imported as authority",
        all(label not in allowed for label in REVERSE_CONSUMERS)
        and set(proposal["source_units"]) == {"MK1"},
    )
    provenance = yaml.safe_load((CAMPAIGN / "evidence/input-provenance.yaml").read_text())
    checks.check(
        "the frozen dependency set is complete and types MK2 as nonauthority",
        set(provenance["candidate_dependencies"]) == DIRECT_PREDECESSORS
        and provenance["candidate_dependencies"]["MK2"]["authority"] == "none",
    )

    for row in rows:
        print(
            "GRAPH",
            row["label"],
            f"checks={row['terminal']}",
            f"assertions={row['assertions']}",
            f"legacy={row['legacy']}",
            f"current={row['current']}",
            f"eager={row['eager']}",
            f"seconds={float(row['elapsed']):.3f}",
        )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
