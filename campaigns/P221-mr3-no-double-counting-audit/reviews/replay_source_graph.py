"""Static hash-sensitive MR3 consumer replay with durable execution reuse."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from pathlib import Path
import subprocess

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


CAMPAIGN = Path(__file__).resolve().parents[1]
ROOT = CAMPAIGN.parents[1]
SOURCE_ROOT = Path("/home/dan/substrate")


@dataclass(frozen=True)
class SourceNode:
    label: str
    relation: str
    path: str
    sha256: str
    checks: int
    assertions: int


NODES = (
    SourceNode("MR3", "audited_root", "merged-framework/bridges/phase-44/bridge_MR3_no_double_counting.py", "c5eaabaeede15909adb5d9ddb951353c376aaa381e669e35c6256d7015e7eddc", 6, 3),
    SourceNode("MR4", "pending_sibling", "merged-framework/bridges/phase-44/bridge_MR4_e_from_rho_saturation.py", "cefe7192b935ec18992e9cd76fd348ef81934ed9d20843ced3627973cec9d3d7", 7, 1),
    SourceNode("MR5", "pending_reverse_consumer", "merged-framework/bridges/phase-44/bridge_MR5_solve_at_derived_e.py", "0da10adafe3badb7f3eab225543bc601996df45b142f2d59b5d0ddd6dd9117d7", 6, 1),
    SourceNode("MR6", "pending_reverse_consumer", "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py", "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d", 6, 3),
)


def main() -> int:
    checks = CheckLedger("P221-GRAPH")
    paths = [node.path for node in NODES]
    source_status = subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "status", "--porcelain", "--", *paths],
        capture_output=True,
        text=True,
        check=True,
    )
    checks.check("all four pinned MR paths are clean", source_status.stdout == "")

    rows: dict[str, dict[str, object]] = {}
    for node in NODES:
        path = SOURCE_ROOT / node.path
        payload = path.read_bytes()
        source = payload.decode("utf-8")
        tree = ast.parse(source, filename=node.path)
        compatibility = audit_numpy_trapezoid_compatibility(source, filename=node.path)
        rows[node.label] = {
            "hash_ok": hashlib.sha256(payload).hexdigest() == node.sha256,
            "checks": sum(
                isinstance(item, ast.Call)
                and isinstance(item.func, ast.Name)
                and item.func.id == "check"
                for item in ast.walk(tree)
            ),
            "assertions": sum(isinstance(item, ast.Assert) for item in ast.walk(tree)),
            "legacy": compatibility.legacy_references,
            "eager": compatibility.eager_legacy_default_fallbacks,
            "source": source,
        }
    checks.check(
        "all nodes retain pinned hashes and exact lexical inventories",
        all(bool(row["hash_ok"]) for row in rows.values())
        and sum(int(row["checks"]) for row in rows.values()) == 25
        and sum(int(row["assertions"]) for row in rows.values()) == 8
        and all(
            rows[node.label]["checks"] == node.checks
            and rows[node.label]["assertions"] == node.assertions
            for node in NODES
        ),
    )

    inventory = yaml.safe_load((ROOT / "migration/source-claims.yaml").read_text())
    units = {entry["source_unit"]: entry for entry in inventory["units"]}
    proposal = yaml.safe_load((CAMPAIGN / "proposal.yaml").read_text())
    expected_root = "qualified" if proposal["status"] == "accepted" else "pending_adjudication"
    checks.check(
        "MR3 terminalizes only with accepted review",
        units["MR3"]["disposition"] == expected_root
        and (
            set(units["MR3"]["accepted_claims"])
            == {
                "C-VAR-003",
                "C-VAR-002",
                "C-BPS-001",
                "C-BPS-002",
                "C-GSK-001",
                "C-SK-001",
            }
            if expected_root == "qualified"
            else units["MR3"]["accepted_claims"] == []
        ),
    )
    checks.check(
        "MR4 through MR6 remain nonauthoritative during MR3 review",
        all(
            units[label]["disposition"] == "pending_adjudication"
            and units[label]["accepted_claims"] == []
            for label in ("MR4", "MR5", "MR6")
        ),
    )
    checks.check(
        "both reverse consumers explicitly name MR3",
        all("MR3" in str(rows[label]["source"]) for label in ("MR5", "MR6")),
    )
    checks.check(
        "MR4 is a sibling input proposal rather than an MR3 consumer",
        "MR3" not in str(rows["MR4"]["source"])
        and "MR4" in str(rows["MR3"]["source"]),
    )
    checks.check(
        "MR5 and MR6 consume only the source diagnosis not the exact new API",
        all(
            "finite_functional_interaction_ledger" not in str(rows[label]["source"])
            and "C-VAR-003" not in str(rows[label]["source"])
            for label in ("MR5", "MR6")
        ),
    )

    reproduction = yaml.safe_load(
        (CAMPAIGN / "evidence/source-reproduction.yaml").read_text()
    )
    p215 = yaml.safe_load(
        (ROOT / "campaigns/P215-mk2-vector-sextic-matching-audit/evidence/source-graph-inventory.yaml").read_text()
    )
    p215_rows = {entry["label"]: entry for entry in p215["replay"]}
    p174 = (
        ROOT / "campaigns/P174-ki4-backsolve-circularity-audit/evidence/source-graph-inventory.yaml"
    ).read_text()
    checks.check(
        "hash-identical native executions are reused without ceremonial reruns",
        reproduction["native_run"]["exit_status"] == 0
        and reproduction["inventory"]["runtime_check_executions"] == 6
        and p215_rows["MR4"]["verdict"] == "clean_noncanonical"
        and p215_rows["MR6"]["verdict"] == "clean_noncanonical"
        and "MR5: {relation: pending_reverse_consumer, checks: 6, assertions: 1, execution: fresh_clean}"
        in p174,
    )
    checks.check(
        "all mutable pending sampled integrations use current SciPy trapezoid",
        all(
            "from scipy.integrate import" in str(rows[label]["source"])
            and "trapezoid" in str(rows[label]["source"])
            and "trapz" not in str(rows[label]["source"])
            for label in ("MR3", "MR5", "MR6")
        )
        and all(
            rows[label]["legacy"] == 0 and rows[label]["eager"] == 0
            for label in rows
        ),
    )
    checks.check(
        "C-VAR-003 grants no backward physical authority",
        proposal["claims_proposed"] == ["C-VAR-003"]
        and proposal["allowed_imports"]
        and all(units[label]["accepted_claims"] == [] for label in ("MR4", "MR5", "MR6")),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
