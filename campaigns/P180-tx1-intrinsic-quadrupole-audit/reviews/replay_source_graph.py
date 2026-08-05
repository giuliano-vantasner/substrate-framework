#!/usr/bin/env python3
"""Hash and authority replay for the TX1 dependency and consumer graph."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
CAMPAIGN = ROOT / "campaigns/P180-tx1-intrinsic-quadrupole-audit"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P180/TX1-SOURCE-GRAPH")
    inventory = yaml.safe_load((CAMPAIGN / "evidence/source-graph-inventory.yaml").read_text())
    migration = yaml.safe_load((ROOT / "migration/source-claims.yaml").read_text())
    units = {item["source_unit"]: item for item in migration["units"]}
    for node in inventory["nodes"]:
        unit = units[node["source_unit"]]
        source_path = SOURCE_ROOT / unit["path"]
        checks.check(
            f"{node['source_unit']} source bytes remain pinned",
            unit["sha256"] == node["sha256"] == _digest(source_path),
        )

    claims = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())["claims"]
    by_claim = {item["id"]: item for item in claims}
    release = yaml.safe_load((ROOT / "governance/releases/v0.132.0.yaml").read_text())
    checks.check(
        "pinned release contains the exact and numeric moment claims",
        {"C-RMOM-001", "C-RMOM-002"} <= set(release["accepted_claims"]),
    )
    checks.check(
        "exact claim dependency closure is accepted",
        by_claim["C-RMOM-001"]["dependencies"]
        == ["C-RMAP-001", "C-RPROF-001", "C-MOM-001"],
    )
    checks.check(
        "numeric claim depends on the exact factorization and accepted branch",
        by_claim["C-RMOM-002"]["dependencies"]
        == ["C-RMOM-001", "C-RPROF-002"],
    )

    tx1_path = SOURCE_ROOT / units["TX1"]["path"]
    tx1_text = tx1_path.read_text(encoding="utf-8")
    tree = ast.parse(tx1_text, filename=str(tx1_path))
    lexical_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("TX1 predicate and assertion inventory remains exact", len(lexical_checks) == 9 and len(assertions) == 2)
    compatibility = audit_numpy_trapezoid_compatibility(tx1_text, filename=str(tx1_path))
    checks.check(
        "TX1 legacy spelling remains a safe isolated compatibility branch",
        compatibility.direct_current_attributes == 1
        and compatibility.direct_legacy_attributes == 1
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    tx2 = (SOURCE_ROOT / units["TX2"]["path"]).read_text(encoding="utf-8")
    tx3 = (SOURCE_ROOT / units["TX3"]["path"]).read_text(encoding="utf-8")
    checks.check("TX2 is an explicit pending consumer of TX1's static tensor", "TX1 established" in tx2 and "RIGID ROTATION" in tx2)
    checks.check("TX3 composes pending TX1 and TX2 rather than validating them", "TX1 supplied" in tx3 and "TX2 made" in tx3)
    checks.check(
        "unchanged accepted and pending executions are hash-reused without ceremony",
        (ROOT / inventory["hash_reuse"]["TX1_native_execution"]).is_file()
        and (ROOT / inventory["hash_reuse"]["TX2_TX3_native_execution"]).is_file(),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
