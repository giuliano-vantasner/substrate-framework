"""Hash-sensitive MR5 consumer replay with durable execution reuse."""

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
    path: str
    sha256: str
    checks: int
    assertions: int


NODES = (
    SourceNode(
        "MR5",
        "merged-framework/bridges/phase-44/bridge_MR5_solve_at_derived_e.py",
        "0da10adafe3badb7f3eab225543bc601996df45b142f2d59b5d0ddd6dd9117d7",
        6,
        1,
    ),
    SourceNode(
        "MR6",
        "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py",
        "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d",
        6,
        3,
    ),
)


def main() -> int:
    checks = CheckLedger("P223-GRAPH")
    paths = [node.path for node in NODES]
    status = subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "status", "--porcelain", "--", *paths],
        capture_output=True,
        text=True,
        check=True,
    )
    checks.check("both pinned source paths are clean", status.stdout == "")
    rows: dict[str, dict[str, object]] = {}
    for node in NODES:
        payload = (SOURCE_ROOT / node.path).read_bytes()
        source = payload.decode("utf-8")
        tree = ast.parse(source)
        compatibility = audit_numpy_trapezoid_compatibility(
            source, filename=node.path
        )
        rows[node.label] = {
            "hash": hashlib.sha256(payload).hexdigest(),
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
        "nodes retain pinned hashes and exact lexical inventories",
        all(rows[node.label]["hash"] == node.sha256 for node in NODES)
        and sum(int(row["checks"]) for row in rows.values()) == 12
        and sum(int(row["assertions"]) for row in rows.values()) == 4
        and all(
            rows[node.label]["checks"] == node.checks
            and rows[node.label]["assertions"] == node.assertions
            for node in NODES
        ),
    )
    inventory = yaml.safe_load((ROOT / "migration/source-claims.yaml").read_text())
    units = {entry["source_unit"]: entry for entry in inventory["units"]}
    proposal = yaml.safe_load((CAMPAIGN / "proposal.yaml").read_text())
    if proposal["status"] == "accepted":
        adjudication = yaml.safe_load((CAMPAIGN / "adjudication.yaml").read_text())
        expected_disposition = adjudication["source_disposition"]["MR5"]
        expected_claims = set(adjudication["accepted_mappings"])
    else:
        expected_disposition = "pending_adjudication"
        expected_claims = set()
    checks.check(
        "MR5 state agrees exactly with its governed campaign transaction",
        units["MR5"]["disposition"] == expected_disposition
        and set(units["MR5"]["accepted_claims"]) == expected_claims,
    )
    checks.check(
        "MR6 remains pending and grants no backward authority",
        units["MR6"]["disposition"] == "pending_adjudication"
        and units["MR6"]["accepted_claims"] == [],
    )
    checks.check(
        "the direct reverse consumer explicitly names MR5",
        "MR5" in str(rows["MR6"]["source"]),
    )
    p174 = (
        ROOT
        / "campaigns/P174-ki4-backsolve-circularity-audit/evidence/source-graph-inventory.yaml"
    ).read_text()
    p215 = yaml.safe_load(
        (
            ROOT
            / "campaigns/P215-mk2-vector-sextic-matching-audit/evidence/source-graph-inventory.yaml"
        ).read_text()
    )
    p215_rows = {row["label"]: row for row in p215["replay"]}
    checks.check(
        "hash-identical expensive native executions are reused without reruns",
        "MR5: {relation: pending_reverse_consumer, checks: 6, assertions: 1, execution: fresh_clean}"
        in p174
        and p215_rows["MR6"]["verdict"] == "clean_noncanonical"
        and p215_rows["MR6"]["runtime_checks"] == 6,
    )
    checks.check(
        "MR5 and MR6 use current trapezoid with no legacy access",
        all(
            "trapezoid" in str(rows[label]["source"])
            and "trapz" not in str(rows[label]["source"])
            and rows[label]["legacy"] == 0
            and rows[label]["eager"] == 0
            for label in rows
        ),
    )
    checks.check(
        "no consumer imports a new MR5 API or closes physical dependencies",
        "solve_generalized_skyrme_radial_profile" not in str(rows["MR6"]["source"])
        and proposal["claims_proposed"] == [],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
