#!/usr/bin/env python3
"""Replay accepted dependencies and pending consumers around TX3."""

from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
CAMPAIGN = ROOT / "campaigns/P182-tx3-polarization-ellipse-audit"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P182-TX3-SOURCE-GRAPH")
    inventory = yaml.safe_load(
        (CAMPAIGN / "evidence/source-graph-inventory.yaml").read_text(
            encoding="utf-8"
        )
    )
    queue_document = yaml.safe_load(
        (ROOT / "migration/source-claims.yaml").read_text(encoding="utf-8")
    )
    queue_units = {
        item["source_unit"]: item for item in queue_document["units"]
    }
    nodes = inventory["nodes"]
    checks.check("source graph contains the ten frozen nodes", len(nodes) == 10)
    checks.check(
        "all graph source hashes remain pinned",
        all(
            _digest(SOURCE_ROOT / node["path"]) == node["sha256"]
            for node in nodes
        ),
    )
    checks.check(
        "inventory paths and hashes match the generated queue",
        all(
            queue_units[node["source_unit"]]["path"] == node["path"]
            and queue_units[node["source_unit"]]["sha256"] == node["sha256"]
            for node in nodes
        ),
    )
    checks.check(
        "accepted dependency mappings remain closed",
        queue_units["GW2"]["accepted_claims"] == ["C-MOM-001", "C-GW-001"]
        and "C-GW-002" in queue_units["GW3"]["accepted_claims"]
        and "C-GW-003" in queue_units["GW4"]["accepted_claims"]
        and "C-GW-007" in queue_units["QB3"]["accepted_claims"]
        and "C-GW-008" in queue_units["QB4"]["accepted_claims"]
        and "C-GW-009" in queue_units["TX2"]["accepted_claims"],
    )
    checks.check(
        "TX3 is qualified through C-GW-010 without blanket future authority",
        queue_units["TX3"]["disposition"] == "qualified"
        and "C-GW-010" in queue_units["TX3"]["accepted_claims"]
        and "TX4" in inventory["consumer_ceiling"]
        and "TX5" in inventory["consumer_ceiling"],
    )
    tx3 = (SOURCE_ROOT / queue_units["TX3"]["path"]).read_text(
        encoding="utf-8"
    )
    tx4 = (SOURCE_ROOT / queue_units["TX4"]["path"]).read_text(
        encoding="utf-8"
    )
    tx5 = (SOURCE_ROOT / queue_units["TX5"]["path"]).read_text(
        encoding="utf-8"
    )
    checks.check(
        "future consumers explicitly build on TX3 but remain separately adjudicated",
        "TX1-TX3 built" in tx4
        and "TX4 established" in tx5
        and queue_units["TX4"]["disposition"] in {"pending_adjudication", "qualified", "refuted", "duplicate_evidence", "out_of_scope", "migrated"}
        and queue_units["TX5"]["disposition"] in {"pending_adjudication", "qualified", "refuted", "duplicate_evidence", "out_of_scope", "migrated"},
    )
    module_text = (
        ROOT / "src/substrate_framework/rotating_quadrupole_polarization.py"
    ).read_text(encoding="utf-8")
    audits = [
        audit_numpy_trapezoid_compatibility(source, filename=name)
        for source, name in ((tx3, "TX3"), (module_text, "canonical"))
    ]
    checks.check(
        "TX3 and its canonical module have no legacy integration access",
        all(
            audit.legacy_references == 0
            and audit.eager_legacy_default_fallbacks == 0
            for audit in audits
        ),
    )
    package = ROOT / "src/substrate_framework"
    checks.check(
        "all canonical dependency modules are materialized",
        all((package / module).is_file() for module in inventory["canonical_modules"]),
    )
    claims = yaml.safe_load(
        (ROOT / "governance/claims.yaml").read_text(encoding="utf-8")
    )["claims"]
    accepted_ids = {
        claim["id"] for claim in claims if claim["review"] == "accepted"
    }
    checks.check(
        "accepted inputs and promoted C-GW-010 exist",
        set(inventory["canonical_claims"]) <= accepted_ids,
    )
    checks.check(
        "TX3 source overclaims remain visible for historical audit",
        "incommensurate phases" in tx3
        and "INDEPENDENT of the rotation" in tx3
        and "self-consistent soliton" in tx3,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
