#!/usr/bin/env python3
"""Replay the accepted and pending source graph around TX2."""

from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
CAMPAIGN = ROOT / "campaigns/P181-tx2-rigid-axis-rotation-audit"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P181-TX2-SOURCE-GRAPH")
    inventory = yaml.safe_load(
        (CAMPAIGN / "evidence/source-graph-inventory.yaml").read_text(
            encoding="utf-8"
        )
    )
    queue_document = yaml.safe_load(
        (ROOT / "migration/source-claims.yaml").read_text(encoding="utf-8")
    )
    queue = queue_document["units"]
    queue_units = {item["source_unit"]: item for item in queue}
    nodes = inventory["nodes"]
    checks.check("source graph contains the nine frozen nodes", len(nodes) == 9)
    checks.check(
        "all graph source hashes remain pinned",
        all(
            _digest(SOURCE_ROOT / node["path"]) == node["sha256"]
            for node in nodes
        ),
    )
    checks.check(
        "inventory paths hashes and adjudicated dispositions match the generated queue",
        all(
            queue_units[node["source_unit"]]["path"] == node["path"]
            and queue_units[node["source_unit"]]["sha256"] == node["sha256"]
            and (
                node["source_unit"] == "TX3"
                or queue_units[node["source_unit"]]["disposition"]
                == node["disposition"]
            )
            for node in nodes
        ),
    )
    checks.check(
        "accepted dependency mappings remain qualified",
        queue_units["GW2"]["accepted_claims"] == ["C-MOM-001", "C-GW-001"]
        and "C-GW-002" in queue_units["GW3"]["accepted_claims"]
        and "C-GW-008" in queue_units["QB4"]["accepted_claims"]
        and "C-RMOM-001" in queue_units["TX1"]["accepted_claims"]
        and "C-RMOM-002" in queue_units["TX1"]["accepted_claims"],
    )
    checks.check(
        "TX2 is qualified through C-GW-009 without blanket TX3 authority",
        queue_units["TX2"]["disposition"] == "qualified"
        and "C-GW-009" in queue_units["TX2"]["accepted_claims"]
        and "TX3" in inventory["consumer_ceiling"],
    )
    tx2 = (SOURCE_ROOT / queue_units["TX2"]["path"]).read_text(encoding="utf-8")
    tx3 = (SOURCE_ROOT / queue_units["TX3"]["path"]).read_text(encoding="utf-8")
    checks.check(
        "TX2 explicitly consumes TX1 but misclassifies coordinate diagonals",
        "TX1 established" in tx2
        and "PAIRWISE DISTINCT" in tx2
        and "GENUINE TRIAXIALITY" in tx2,
    )
    checks.check(
        "TX3 is a direct narrative consumer requiring its own audit",
        "TX1 supplied" in tx3 and "TX2 made" in tx3,
    )
    compatibility_sources = [
        tx2,
        tx3,
        (ROOT / "src/substrate_framework/rigid_quadrupole_rotation.py").read_text(
            encoding="utf-8"
        ),
    ]
    audits = [
        audit_numpy_trapezoid_compatibility(source, filename=f"node-{index}")
        for index, source in enumerate(compatibility_sources)
    ]
    checks.check(
        "TX2 TX3 and the canonical rotation module have no legacy integration access",
        all(audit.legacy_references == 0 for audit in audits),
    )
    package = ROOT / "src/substrate_framework"
    checks.check(
        "all canonical dependency modules are materialized",
        all((package / module).is_file() for module in inventory["canonical_modules"]),
    )
    claims = yaml.safe_load(
        (ROOT / "governance/claims.yaml").read_text(encoding="utf-8")
    )["claims"]
    accepted_ids = {claim["id"] for claim in claims}
    checks.check(
        "accepted inputs and promoted C-GW-009 exist",
        set(inventory["canonical_claims"]) <= accepted_ids
        and "C-GW-009" in accepted_ids,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
