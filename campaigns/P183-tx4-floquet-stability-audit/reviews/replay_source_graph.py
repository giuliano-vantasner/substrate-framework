#!/usr/bin/env python3
"""Replay accepted dependencies and the pending consumer around TX4."""

from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
CAMPAIGN = ROOT / "campaigns/P183-tx4-floquet-stability-audit"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P183-TX4-SOURCE-GRAPH")
    inventory = yaml.safe_load(
        (CAMPAIGN / "evidence/source-graph-inventory.yaml").read_text(
            encoding="utf-8"
        )
    )
    queue = yaml.safe_load(
        (ROOT / "migration/source-claims.yaml").read_text(encoding="utf-8")
    )
    queue_units = {item["source_unit"]: item for item in queue["units"]}
    nodes = inventory["nodes"]
    checks.check("source graph contains the nine frozen nodes", len(nodes) == 9)
    checks.check(
        "all graph source hashes remain pinned",
        all(_digest(SOURCE_ROOT / node["path"]) == node["sha256"] for node in nodes),
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
        "accepted rational-map radial and Floquet requirement inputs remain closed",
        {"C-RMAP-001", "C-RMAP-002"}
        <= set(queue_units["E1"]["accepted_claims"])
        and {"C-RPROF-001", "C-RPROF-002"}
        <= set(queue_units["E2"]["accepted_claims"])
        and "C-PDE-009" in queue_units["QB3"]["accepted_claims"],
    )
    checks.check(
        "TX1 through TX3 retain only their qualified accepted mappings",
        {"C-RMOM-001", "C-RMOM-002"}
        <= set(queue_units["TX1"]["accepted_claims"])
        and "C-GW-009" in queue_units["TX2"]["accepted_claims"]
        and "C-GW-010" in queue_units["TX3"]["accepted_claims"],
    )
    checks.check(
        "TX4 is qualified through three narrow claims",
        queue_units["TX4"]["disposition"] == "qualified"
        and {"C-FLO-001", "C-ROT-001", "C-RMAP-003"}
        <= set(queue_units["TX4"]["accepted_claims"]),
    )
    checks.check(
        "TX5 remains separately pending with no inherited stability authority",
        queue_units["TX5"]["disposition"] == "pending_adjudication"
        and queue_units["TX5"]["accepted_claims"] == []
        and "TX5" in inventory["consumer_ceiling"],
    )
    tx4 = (SOURCE_ROOT / queue_units["TX4"]["path"]).read_text(encoding="utf-8")
    tx5 = (SOURCE_ROOT / queue_units["TX5"]["path"]).read_text(encoding="utf-8")
    checks.check(
        "M2 is a false token dependency rather than an imported source premise",
        "M2 =" in tx4
        and "bridge_M2" not in tx4
        and "M2" not in queue_units["TX4"].get("dependencies", []),
    )
    checks.check(
        "TX5 explicitly consumes TX4 prose but remains separately adjudicated",
        "TX4 established" in tx5
        and "TX4" in inventory["consumer_ceiling"],
    )
    module_texts = [
        (ROOT / "src/substrate_framework/rotating_stability.py").read_text(
            encoding="utf-8"
        ),
        (ROOT / "src/substrate_framework/rational_map_stability.py").read_text(
            encoding="utf-8"
        ),
    ]
    audits = [
        audit_numpy_trapezoid_compatibility(text, filename=name)
        for text, name in [(tx4, "TX4"), *zip(module_texts, ("rotating", "shape"), strict=True)]
    ]
    checks.check(
        "TX4 and canonical modules have no legacy integration access",
        all(
            audit.legacy_references == 0
            and audit.eager_legacy_default_fallbacks == 0
            for audit in audits
        ),
    )
    package = ROOT / "src/substrate_framework"
    checks.check(
        "all canonical graph modules are materialized",
        all((package / module).is_file() for module in inventory["canonical_modules"]),
    )
    claims = yaml.safe_load(
        (ROOT / "governance/claims.yaml").read_text(encoding="utf-8")
    )["claims"]
    accepted_ids = {claim["id"] for claim in claims if claim["review"] == "accepted"}
    checks.check(
        "accepted inputs and three promoted claims exist",
        set(inventory["canonical_claims"]) <= accepted_ids,
    )
    checks.check(
        "TX4 overclaims remain visible for historical audit",
        "DYNAMICALLY STABLE" in tx4
        and "SECULAR TERM IS A ZERO MODE" in tx4
        and "IT CANNOT FISSION" in tx4,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
