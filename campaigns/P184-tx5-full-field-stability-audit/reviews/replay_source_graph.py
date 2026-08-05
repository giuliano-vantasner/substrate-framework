#!/usr/bin/env python3
"""Replay accepted dependencies and governed source boundaries around TX5."""

from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
CAMPAIGN = ROOT / "campaigns/P184-tx5-full-field-stability-audit"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P184-TX5-SOURCE-GRAPH")
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
    checks.check("source graph contains the seven frozen nodes", len(nodes) == 7)
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
        "rational-map and reduced-profile source inputs remain closed",
        {"C-RMAP-001", "C-RMAP-002"}
        <= set(queue_units["E1"]["accepted_claims"])
        and {"C-RPROF-001", "C-RPROF-002"}
        <= set(queue_units["E2"]["accepted_claims"]),
    )
    checks.check(
        "qualified TX1 and TX2 retain only their scoped accepted mappings",
        {"C-RMOM-001", "C-RMOM-002"}
        <= set(queue_units["TX1"]["accepted_claims"])
        and "C-GW-009" in queue_units["TX2"]["accepted_claims"],
    )
    checks.check(
        "qualified TX4 retains its narrow corrected stability mappings",
        queue_units["TX4"]["disposition"] == "qualified"
        and {"C-FLO-001", "C-ROT-001", "C-RMAP-003"}
        <= set(queue_units["TX4"]["accepted_claims"]),
    )
    checks.check(
        "TX5 is qualified only through the new pointwise theorem plus accepted inputs",
        queue_units["TX5"]["disposition"] == "qualified"
        and "C-SKY-002" in queue_units["TX5"]["accepted_claims"]
        and "C-PDE-014" not in queue_units["TX5"]["accepted_claims"],
    )

    tx5_path = SOURCE_ROOT / queue_units["TX5"]["path"]
    tx5 = tx5_path.read_text(encoding="utf-8")
    checks.check(
        "E4 is a false source token dependency rather than an imported unit",
        "def E_parts" in tx5
        and "e2, e4" in tx5
        and "bridge_E4" not in tx5
        and "E4" in queue_units["TX5"].get("candidate_dependencies", []),
    )
    checks.check(
        "TX5 consumes TX4 prose but receives only adjudicated TX4 authority",
        "TX4 established" in tx5 and queue_units["TX4"]["disposition"] == "qualified",
    )
    tx5_index = next(
        index
        for index, item in enumerate(queue["units"])
        if item["source_unit"] == "TX5"
    )
    checks.check(
        "no later source unit declares TX5 as a candidate dependency",
        all(
            "TX5" not in item.get("candidate_dependencies", [])
            for item in queue["units"][tx5_index + 1 :]
        ),
    )

    module_text = (ROOT / "src/substrate_framework/skyrme_o4.py").read_text(
        encoding="utf-8"
    )
    audits = [
        audit_numpy_trapezoid_compatibility(text, filename=name)
        for text, name in ((tx5, "TX5"), (module_text, "skyrme_o4"))
    ]
    checks.check(
        "TX5 and its canonical module have no legacy integration access",
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
        "accepted inputs and C-SKY-002 exist",
        set(inventory["canonical_claims"]) <= accepted_ids,
    )
    checks.check(
        "TX5 overclaims remain visible for historical audit",
        "STRICT LOCAL MINIMUM" in tx5
        and "every direction tested is uphill" in tx5
        and "this IS linear dynamical stability" in tx5,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
