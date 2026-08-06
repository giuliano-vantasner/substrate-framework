"""Hash-sensitive MR4 consumer replay with durable execution reuse."""

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
    SourceNode("MR4", "merged-framework/bridges/phase-44/bridge_MR4_e_from_rho_saturation.py", "cefe7192b935ec18992e9cd76fd348ef81934ed9d20843ced3627973cec9d3d7", 7, 1),
    SourceNode("MR5", "merged-framework/bridges/phase-44/bridge_MR5_solve_at_derived_e.py", "0da10adafe3badb7f3eab225543bc601996df45b142f2d59b5d0ddd6dd9117d7", 6, 1),
    SourceNode("MR6", "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py", "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d", 6, 3),
)


def main() -> int:
    checks = CheckLedger("P222-GRAPH")
    paths = [node.path for node in NODES]
    status = subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "status", "--porcelain", "--", *paths],
        capture_output=True,
        text=True,
        check=True,
    )
    checks.check("all three pinned MR paths are clean", status.stdout == "")
    rows: dict[str, dict[str, object]] = {}
    for node in NODES:
        payload = (SOURCE_ROOT / node.path).read_bytes()
        source = payload.decode("utf-8")
        tree = ast.parse(source)
        compatibility = audit_numpy_trapezoid_compatibility(source, filename=node.path)
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
        "all nodes retain pinned hashes and exact lexical inventories",
        all(rows[node.label]["hash"] == node.sha256 for node in NODES)
        and sum(int(row["checks"]) for row in rows.values()) == 19
        and sum(int(row["assertions"]) for row in rows.values()) == 5
        and all(
            rows[node.label]["checks"] == node.checks
            and rows[node.label]["assertions"] == node.assertions
            for node in NODES
        ),
    )
    inventory = yaml.safe_load((ROOT / "migration/source-claims.yaml").read_text())
    units = {entry["source_unit"]: entry for entry in inventory["units"]}
    proposal = yaml.safe_load((CAMPAIGN / "proposal.yaml").read_text())
    expected = "duplicate_evidence" if proposal["status"] == "accepted" else "pending_adjudication"
    checks.check(
        "MR4 terminalizes only through accepted existing owners",
        units["MR4"]["disposition"] == expected
        and (
            set(units["MR4"]["accepted_claims"]) == {"C-VEC-001", "C-SK-001"}
            if expected == "duplicate_evidence"
            else units["MR4"]["accepted_claims"] == []
        ),
    )
    checks.check(
        "MR5 and MR6 remain pending and grant no backward authority",
        all(
            units[label]["disposition"] == "pending_adjudication"
            and units[label]["accepted_claims"] == []
            for label in ("MR5", "MR6")
        ),
    )
    checks.check(
        "both reverse consumers explicitly name MR4",
        all("MR4" in str(rows[label]["source"]) for label in ("MR5", "MR6")),
    )
    p215 = yaml.safe_load(
        (ROOT / "campaigns/P215-mk2-vector-sextic-matching-audit/evidence/source-graph-inventory.yaml").read_text()
    )
    p215_rows = {row["label"]: row for row in p215["replay"]}
    p174 = (
        ROOT / "campaigns/P174-ki4-backsolve-circularity-audit/evidence/source-graph-inventory.yaml"
    ).read_text()
    checks.check(
        "hash-identical native executions are reused without reruns",
        p215_rows["MR4"]["verdict"] == "clean_noncanonical"
        and p215_rows["MR4"]["runtime_checks"] == 7
        and p215_rows["MR6"]["verdict"] == "clean_noncanonical"
        and "MR5: {relation: pending_reverse_consumer, checks: 6, assertions: 1, execution: fresh_clean}"
        in p174,
    )
    checks.check(
        "MR4 has no integration surface and pending consumers use current trapezoid",
        "numpy" not in str(rows["MR4"]["source"])
        and "scipy" not in str(rows["MR4"]["source"])
        and all(
            "trapezoid" in str(rows[label]["source"])
            and "trapz" not in str(rows[label]["source"])
            for label in ("MR5", "MR6")
        )
        and all(rows[label]["legacy"] == 0 and rows[label]["eager"] == 0 for label in rows),
    )
    checks.check(
        "no consumer imports a new MR4 API or grants physical closure",
        all("conditional_hls_ksrf_matching" not in str(rows[label]["source"]) for label in ("MR5", "MR6"))
        and proposal["claims_proposed"] == [],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
