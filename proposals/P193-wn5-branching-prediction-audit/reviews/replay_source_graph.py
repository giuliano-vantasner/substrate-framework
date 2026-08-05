#!/usr/bin/env python3
"""Verify P193's byte-reused eighteen-node WN5 source graph."""

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
P192_REPLAY = ROOT / "campaigns/P192-wn4-derived-weight-crossover-audit/reviews/replay_source_graph.py"
P192_ATTEMPT = ROOT / "campaigns/P192-wn4-derived-weight-crossover-audit/attempts/0011/result.yaml"
P122_REPRODUCTION = ROOT / "campaigns/P122-gb1-channel-branching-audit/evidence/source-reproduction.yaml"
P193_REPRODUCTION = PROPOSAL / "evidence/source-reproduction.yaml"
PINNED_EVIDENCE = {
    P192_INVENTORY: "08711e413630374492d59eec8a71093d4eb3d84a052bcff731db6ab976a55255",
    P192_REPLAY: "f78ab11835d9754dbcc0f752198291bf4f528578d9273d26b359b359502452e9",
    P192_ATTEMPT: "af40f2a7f13e395a9cb360df475e5eef3e283ed111b5403011660a0990c207d1",
    P122_REPRODUCTION: "d9fff939489f21fb54a4bdfd2013becd20bc8295b45cc8a06acc6f48ed959e32",
    P193_REPRODUCTION: "0a9cf3bd10974ef0aecea97040608d602294a3e064947a2076e947fea2f00dae",
}
GB1 = {
    "path": "merged-framework/bridges/phase-32/bridge_GB1_channel_definitions.py",
    "sha256": "ace0515d7ea362ef45a55db22308aecffdad9a003d03f2b1209c0a11874b489b",
    "native_tally": 18,
}
EXPECTED_DIRECT_DEPENDENCIES = {"GB1", "GB4", "WN3", "WN4"}
EXPECTED_DIRECT_REVERSE = {"WN7", "MD5"}
EXPECTED_DEPTH_TWO = {"MD6"}


def _load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P193-WN5-SOURCE-GRAPH")
    queue = _load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}
    prior = _load(P192_INVENTORY)
    prior_rows = {row["source_unit"]: row for row in prior["nodes"]}
    expected_nodes = dict(prior_rows)
    expected_nodes["GB1"] = {"source_unit": "GB1", **GB1}

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
        "P192 P122 and P193 execution records remain byte-pinned",
        all(_digest(path) == expected for path, expected in PINNED_EVIDENCE.items()),
    )
    checks.check(
        "P192 supplies exactly seventeen unchanged rows and 662 native checks",
        len(prior_rows) == 17
        and sum(row["native_tally"] for row in prior_rows.values()) == 662
        and prior["actual_replay"]["terminal_tally"] == "ALL_43_CHECKS_PASS",
    )
    gb1_reproduction = _load(P122_REPRODUCTION)
    root_reproduction = _load(P193_REPRODUCTION)
    checks.check(
        "GB1 and WN5 reuse their exact terminal native records",
        gb1_reproduction["terminal_tally"] == "ALL 18 CHECKS PASS"
        and gb1_reproduction["exit_status"] == 0
        and root_reproduction["terminal_tally"] == "ALL_41_CHECKS_PASS"
        and root_reproduction["exit_status"] == 0,
    )
    checks.check(
        "eighteen unique nodes cover 680 native checks without counted duplicate execution",
        len(expected_nodes) == 18
        and sum(row["native_tally"] for unit, row in prior_rows.items() if unit != "WN5")
        == 621
        and 621 + GB1["native_tally"] + root_reproduction["runtime_checks"] == 680,
    )
    checks.check(
        "WN5 direct source dependencies are exact",
        set(units["WN5"]["candidate_dependencies"])
        == EXPECTED_DIRECT_DEPENDENCIES,
    )
    reverse: dict[str, set[str]] = {}
    for row in queue["units"]:
        for dependency in row.get("candidate_dependencies", []):
            reverse.setdefault(dependency, set()).add(row["source_unit"])
    checks.check(
        "WN5 direct reverse consumers are exact",
        reverse.get("WN5", set()) == EXPECTED_DIRECT_REVERSE,
    )
    depth_two = {
        consumer
        for direct in EXPECTED_DIRECT_REVERSE
        for consumer in reverse.get(direct, set())
        if consumer not in EXPECTED_DIRECT_REVERSE and consumer != "WN5"
    }
    checks.check(
        "WN5 depth-two pending consumer set is exact",
        depth_two == EXPECTED_DEPTH_TWO,
    )
    checks.check(
        "source dependencies retain their reviewed authority boundaries",
        units["GB1"]["accepted_claims"] == ["C-BRN-001"]
        and units["GB4"]["accepted_claims"] == ["C-BRN-001"]
        and units["WN3"]["accepted_claims"]
        == ["C-SG-019", "C-CMB-001", "C-OSC-001"]
        and units["WN4"]["accepted_claims"] == ["C-OSC-001", "C-CMB-003"],
    )
    consumer_audit = _load(PROPOSAL / "evidence/consumer-audit.yaml")
    checks.check(
        "all three reverse consumers remain pending without promotion",
        set(consumer_audit["direct_source_consumers"]) == EXPECTED_DIRECT_REVERSE
        and set(consumer_audit["depth_two_consumers"]) == EXPECTED_DEPTH_TWO
        and consumer_audit["consumer_dispositions_changed"] == []
        and consumer_audit["downstream_claims_promoted"] == [],
    )
    checks.check(
        "dependency consumer impact nonduplication and disposition reviews are materialized",
        all(
            (PROPOSAL / relative).is_file()
            for relative in (
                "evidence/dependency-audit.yaml",
                "evidence/consumer-audit.yaml",
                "evidence/gitnexus-impact.yaml",
                "evidence/nonduplication-audit.yaml",
                "evidence/source-graph-inventory.yaml",
                "reviews/WN5-disposition-review.md",
                "reviews/source_adjudication.md",
                "reviews/impact_analysis.md",
            )
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
