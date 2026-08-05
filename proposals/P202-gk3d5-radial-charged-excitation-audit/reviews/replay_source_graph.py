#!/usr/bin/env python3
"""Replay P202's GK3D5 dependency and direct-consumer authority graph."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
CAMPAIGN = Path(__file__).resolve().parents[1]
NODES = {
    "EM1": (
        "merged-framework/bridges/phase-3/bridge_EM1_u1_noether_charge.py",
        "2f5c6e0236748bc6f3a8ce4a77bd18dc26b3cef235038d57bc71310361ea4850",
        16,
        1,
    ),
    "EM2": (
        "merged-framework/bridges/phase-3/bridge_EM2_gauge_u1_minimal_coupling.py",
        "9787ae25521e19d926de0f9addafd16353bebc149cea83f3d9dd4c491fef91d6",
        11,
        1,
    ),
    "EM6": (
        "merged-framework/bridges/phase-3/bridge_EM6_derived_profile_stability.py",
        "926df2dc5014042472b3d47576af06676eb654d9da4634f147c7044d4e91f897",
        11,
        2,
    ),
    "GK3D1": (
        "merged-framework/bridges/phase-41/bridge_GK3D1_master_polarization_general_D.py",
        "9a25110ba53adfb439d0cfd0570bd311b0a43a20f13d1351f45c3fa4075aeacb",
        19,
        1,
    ),
    "GK3D3": (
        "merged-framework/bridges/phase-41/bridge_GK3D3_transmutation_closes_the_log.py",
        "1c3f81d15ace3ec2c6326c89659596f5b9ff84ac23ef7f0143a53ad92b23b211",
        14,
        1,
    ),
    "GK3D4": (
        "merged-framework/bridges/phase-41/bridge_GK3D4_three_sectors_one_construction.py",
        "046273d9a06f92ddbe9cd666d3b6de0f321b9709c371aeee8103394dd2a2ad35",
        11,
        1,
    ),
    "GK3D5": (
        "merged-framework/bridges/phase-41/bridge_GK3D5_charged_excitation_exists_in_3D.py",
        "201d4fd2594a73c7b59dbe81e0e66f1d3d43a52605a26174c70bd072626992e2",
        13,
        2,
    ),
    "GK3D6": (
        "merged-framework/bridges/phase-41/bridge_GK3D6_oneloop_accuracy_and_exact_ratios.py",
        "e0ab2a2db57affe023e6838ed835656412cf01188225f31084e6a6a1baf8e036",
        10,
        1,
    ),
    "EL2": (
        "merged-framework/bridges/phase-46/bridge_EL2_lepton_is_baryonless_fermion.py",
        "db90b921e0b3d6966597a39817ad48219cd94fa27ff8aa2a1de4a64c3ccf6965",
        11,
        3,
    ),
}
DIRECT_DEPENDENCIES = {"EM1", "EM2", "EM6", "GK3D1", "GK3D3", "GK3D4"}
DIRECT_CONSUMERS = {"GK3D6", "EL2"}
DEPENDENCY_MAPPINGS = {
    "EM1": ["C-U1-001", "C-U1-002"],
    "EM2": ["C-GAU-001"],
    "EM6": ["C-QBL-001"],
    "GK3D1": ["C-GAU-001", "C-DIM-009", "C-VAC-002"],
    "GK3D3": ["C-RGE-003", "C-IDN-002", "C-DIM-009", "C-VAC-003", "C-VAC-004"],
    "GK3D4": [
        "C-LIE-001",
        "C-REP-002",
        "C-PGA-001",
        "C-DIM-009",
        "C-VAC-002",
        "C-VAC-003",
        "C-VAC-004",
        "C-REP-001",
        "C-RGE-005",
        "C-ANO-001",
    ],
}


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_inventory(path: Path) -> tuple[int, int]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    return len(calls), len(assertions)


def main() -> int:
    checks = CheckLedger("P202-GK3D5-SOURCE-GRAPH")
    queue = load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}
    compatibility_nodes: list[str] = []
    inventory_totals = [0, 0]
    for unit, (relative, expected_hash, expected_calls, expected_assertions) in NODES.items():
        source = SOURCE_ROOT / relative
        checks.check(
            f"{unit} source remains path and hash pinned",
            units[unit]["path"] == relative
            and units[unit]["sha256"] == expected_hash
            and digest(source) == expected_hash,
        )
        actual_calls, actual_assertions = source_inventory(source)
        inventory_totals[0] += actual_calls
        inventory_totals[1] += actual_assertions
        checks.check(
            f"{unit} static predicate inventory remains exact",
            actual_calls == expected_calls and actual_assertions == expected_assertions,
        )
        compatibility = audit_numpy_trapezoid_compatibility(
            source.read_text(encoding="utf-8"), filename=relative
        )
        if compatibility.legacy_references:
            compatibility_nodes.append(unit)
            checks.check(
                f"{unit} legacy name is a safe lazy compatibility fallback",
                compatibility.current_references == 1
                and compatibility.legacy_references == 1
                and compatibility.eager_legacy_default_fallbacks == 0,
            )

    checks.check(
        "nine-node graph inventory covers 116 checks and 13 assertions once",
        len(NODES) == 9 and inventory_totals == [116, 13],
    )
    checks.check(
        "GK3D5 is the sole immutable compatibility node",
        compatibility_nodes == ["GK3D5"],
    )
    checks.check(
        "six direct dependencies are exact and qualified",
        set(units["GK3D5"]["candidate_dependencies"]) == DIRECT_DEPENDENCIES
        and all(units[unit]["disposition"] == "qualified" for unit in DIRECT_DEPENDENCIES),
    )
    checks.check(
        "qualified dependencies retain individual accepted mappings",
        all(
            units[unit]["accepted_claims"] == mapping
            for unit, mapping in DEPENDENCY_MAPPINGS.items()
        ),
    )
    reverse = {
        row["source_unit"]
        for row in queue["units"]
        if "GK3D5" in row.get("candidate_dependencies", [])
    }
    checks.check("two direct reverse consumers are exact", reverse == DIRECT_CONSUMERS)
    checks.check(
        "GK3D6 remains pending for its own campaign",
        units["GK3D6"]["disposition"] == "pending_adjudication"
        and units["GK3D6"]["accepted_claims"] == [],
    )
    checks.check(
        "qualified EL2 grants no backward or new radial authority",
        units["EL2"]["disposition"] == "qualified"
        and units["EL2"]["accepted_claims"] == ["C-TOP-001", "C-U1-001"],
    )
    proposal = load(CAMPAIGN / "proposal.yaml")
    expected_status = (
        "qualified" if proposal["status"] == "accepted" else "pending_adjudication"
    )
    expected_mapping = (
        ["C-U1-001", "C-QBL-004"] if expected_status == "qualified" else []
    )
    checks.check(
        "GK3D5 root authority matches the campaign stage",
        units["GK3D5"]["disposition"] == expected_status
        and units["GK3D5"]["accepted_claims"] == expected_mapping,
    )
    inventory = load(CAMPAIGN / "evidence/source-graph-inventory.yaml")
    checks.check(
        "graph replay counts no duplicate native execution",
        inventory["expected_coverage"]["fresh_native_executions"] == 0
        and inventory["expected_coverage"][
            "duplicate_native_execution_records_counted"
        ]
        == 0
        and inventory["expected_coverage"]["version_only_scientific_failures"]
        == 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
