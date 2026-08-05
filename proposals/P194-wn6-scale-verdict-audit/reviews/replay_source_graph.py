#!/usr/bin/env python3
"""Verify P194's byte-reused nineteen-node WN6 source graph."""

from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
PROPOSAL = Path(__file__).resolve().parents[1]
P192_INVENTORY = ROOT / "campaigns/P192-wn4-derived-weight-crossover-audit/evidence/source-graph-inventory.yaml"
P193_INVENTORY = ROOT / "campaigns/P193-wn5-branching-prediction-audit/evidence/source-graph-inventory.yaml"
P193_REPLAY = ROOT / "campaigns/P193-wn5-branching-prediction-audit/reviews/replay_source_graph.py"
P193_ATTEMPT = ROOT / "campaigns/P193-wn5-branching-prediction-audit/attempts/0006/result.yaml"
P137_REPRODUCTION = ROOT / "campaigns/P137-s1-two-skyrmion-force-audit/evidence/source-reproduction.yaml"
P194_REPRODUCTION = PROPOSAL / "evidence/source-reproduction.yaml"
PINNED_EVIDENCE = {
    P193_INVENTORY: "6932265e39311a2f2284aca6e5d8a40a7369860a452e91d8b6b88633d62f734e",
    P193_REPLAY: "be0ee3d29c9891d22ac00635625e85b8856842ed6634db9d959c9bd05e6356b0",
    P193_ATTEMPT: "730b857bb05b77b5b977f9b6a164d81eda4746d47a41f39f007d663f0e762efe",
    P137_REPRODUCTION: "1fc5e40a7dace5bed98856980e0bc11d10de978407e52339dcba5b9c2ab4a622",
    P194_REPRODUCTION: "42f0a42b57da16032317b9b43c16cc5564f127eae37119499c3def1007ccd5e6",
}
GB1 = {
    "path": "merged-framework/bridges/phase-32/bridge_GB1_channel_definitions.py",
    "sha256": "ace0515d7ea362ef45a55db22308aecffdad9a003d03f2b1209c0a11874b489b",
    "native_tally": 18,
}
S1 = {
    "path": "merged-framework/bridges/phase-4/bridge_S1_nn_force_two_skyrmion.py",
    "sha256": "ebe1ba930be26f17671d8e82779d14fc00e7a8b988a4aada722a32d0d9328ddd",
    "native_tally": 11,
}
EXPECTED_DIRECT_DEPENDENCIES = {"PN1", "PN2", "S1", "WN1", "WN2", "WN3", "WN4"}
EXPECTED_DIRECT_REVERSE = {"WN7", "MD1", "MD2", "MD3", "MD4", "MD5", "MD6"}


def _load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P194-WN6-SOURCE-GRAPH")
    queue = _load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}
    p192 = _load(P192_INVENTORY)
    expected_nodes = {row["source_unit"]: row for row in p192["nodes"]}
    expected_nodes["GB1"] = {"source_unit": "GB1", **GB1}
    expected_nodes["S1"] = {"source_unit": "S1", **S1}

    for unit, row in sorted(expected_nodes.items()):
        relative = row["path"]
        expected_hash = row["sha256"]
        path = SOURCE_ROOT / relative
        checks.check(
            f"{unit} source path and hash remain pinned",
            units[unit]["path"] == relative
            and units[unit]["sha256"] == expected_hash
            and _digest(path) == expected_hash,
        )
        compatibility = audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"),
            filename=relative,
        )
        checks.check(
            f"{unit} has no legacy quadrature compatibility surface",
            compatibility.legacy_references == 0
            and compatibility.eager_legacy_default_fallbacks == 0,
        )

    checks.check(
        "P193 P137 and P194 execution records remain byte-pinned",
        all(_digest(path) == expected for path, expected in PINNED_EVIDENCE.items()),
    )
    p193 = _load(P193_INVENTORY)
    checks.check(
        "P193 supplies eighteen unchanged nodes and 680 native checks",
        p193["expected_coverage"]["unique_nodes"] == 18
        and p193["expected_coverage"]["total_native_checks_covered"] == 680
        and p193["actual_replay"]["terminal_tally"] == "ALL_46_CHECKS_PASS",
    )
    s1_reproduction = _load(P137_REPRODUCTION)
    root_reproduction = _load(P194_REPRODUCTION)
    checks.check(
        "S1 and WN6 reuse their exact terminal native records",
        s1_reproduction["terminal_tally"] == "ALL 11 CHECKS PASS"
        and s1_reproduction["exit_status"] == 0
        and root_reproduction["terminal_tally"] == "ALL_32_CHECKS_PASS"
        and root_reproduction["exit_status"] == 0,
    )
    checks.check(
        "nineteen unique nodes cover 691 native checks without counted duplicate execution",
        len(expected_nodes) == 19
        and sum(row["native_tally"] for row in expected_nodes.values()) == 691,
    )
    checks.check(
        "WN6 direct source dependencies are exact",
        set(units["WN6"]["candidate_dependencies"])
        == EXPECTED_DIRECT_DEPENDENCIES,
    )
    reverse: dict[str, set[str]] = {}
    for row in queue["units"]:
        for dependency in row.get("candidate_dependencies", []):
            reverse.setdefault(dependency, set()).add(row["source_unit"])
    checks.check(
        "WN6 direct reverse consumers are exact",
        reverse.get("WN6", set()) == EXPECTED_DIRECT_REVERSE,
    )
    checks.check(
        "all seven source dependencies retain qualified status without S1 phase authority",
        all(units[unit]["disposition"] == "qualified" for unit in EXPECTED_DIRECT_DEPENDENCIES)
        and units["S1"]["accepted_claims"]
        == ["C-CC-001", "C-VIR-001", "C-RPROF-001", "C-SKY-001"],
    )
    consumer_audit = _load(PROPOSAL / "evidence/consumer-audit.yaml")
    checks.check(
        "all seven reverse consumers remain pending without promotion",
        set(consumer_audit["direct_source_consumers"]) == EXPECTED_DIRECT_REVERSE
        and consumer_audit["consumer_dispositions_changed"] == []
        and consumer_audit["downstream_claims_promoted"] == [],
    )
    checks.check(
        "claim dependency consumer impact nonduplication and disposition reviews are materialized",
        all(
            (PROPOSAL / relative).is_file()
            for relative in (
                "evidence/dependency-audit.yaml",
                "evidence/consumer-audit.yaml",
                "evidence/gitnexus-impact.yaml",
                "evidence/nonduplication-audit.yaml",
                "evidence/source-graph-inventory.yaml",
                "reviews/C-OSC-002-claim-review.md",
                "reviews/WN6-disposition-review.md",
                "reviews/source_adjudication.md",
                "reviews/impact_analysis.md",
            )
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())

