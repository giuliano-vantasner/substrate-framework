#!/usr/bin/env python3
"""Replay GK3D6's dependency graph without granting backward authority."""

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
    "AS1": (
        "merged-framework/bridges/phase-21/bridge_AS1_two_length_transmutation.py",
        "baca25e9b2b999088c1dc2969f9979cd341c582b3bdcfd009432db0eae9ea6cf",
        10,
        1,
    ),
    "AS7": (
        "merged-framework/bridges/phase-22/bridge_AS7_gravity_confrontation_planck_granularity.py",
        "710635ddf323b8995dc4a1481aeb8232938d6db14c37bd95a537b26d17df3e0f",
        6,
        1,
    ),
    "GK3D2": (
        "merged-framework/bridges/phase-41/bridge_GK3D2_induced_kinetic_normalization.py",
        "856096aba38812dc17fb07ce5cf7c0fa13eb2623665ccf871810734ac3ca0886",
        17,
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
}
DEPENDENCY_MAPPINGS = {
    "AS1": ["C-DIM-001", "C-RGE-001", "C-RGE-002", "C-IDN-001", "C-RGE-003"],
    "AS7": ["C-IDN-002", "C-GRV-001", "C-RGE-003", "C-IDN-001", "C-DIM-008", "C-SYM-002"],
    "GK3D2": ["C-GAU-001", "C-DIM-009", "C-VAC-002", "C-MAX-001", "C-VAC-003"],
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
    "GK3D5": ["C-U1-001", "C-QBL-004"],
}
ROOT_MAPPING = [
    "C-RGE-003",
    "C-IDN-002",
    "C-VAC-003",
    "C-VAC-004",
    "C-REP-001",
    "C-QBL-004",
]


def _load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _inventory(path: Path) -> tuple[int, int]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
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
    checks = CheckLedger("P203-GK3D6-SOURCE-GRAPH")
    queue = _load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}
    compatibility_nodes: list[str] = []
    totals = [0, 0]
    for unit, (relative, expected_hash, expected_calls, expected_assertions) in NODES.items():
        source = SOURCE_ROOT / relative
        checks.check(
            f"{unit} source remains path and hash pinned",
            units[unit]["path"] == relative
            and units[unit]["sha256"] == expected_hash
            and _digest(source) == expected_hash,
        )
        actual_calls, actual_assertions = _inventory(source)
        totals[0] += actual_calls
        totals[1] += actual_assertions
        checks.check(
            f"{unit} predicate inventory remains exact",
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
                and compatibility.dynamic_current_getattrs == 1
                and compatibility.eager_legacy_default_fallbacks == 0,
            )

    checks.check(
        "seven-node inventory covers eighty-one checks and eight assertions once",
        totals == [81, 8],
    )
    checks.check(
        "GK3D5 is the sole immutable compatibility node",
        compatibility_nodes == ["GK3D5"],
    )
    checks.check(
        "GK3D6's six declared dependencies are exact and qualified",
        set(units["GK3D6"]["candidate_dependencies"]) == set(DEPENDENCY_MAPPINGS)
        and all(units[unit]["disposition"] == "qualified" for unit in DEPENDENCY_MAPPINGS),
    )
    checks.check(
        "dependency mappings remain individually governed",
        all(
            units[unit]["accepted_claims"] == mapping
            for unit, mapping in DEPENDENCY_MAPPINGS.items()
        ),
    )
    reverse = {
        row["source_unit"]
        for row in queue["units"]
        if "GK3D6" in row.get("candidate_dependencies", [])
    }
    checks.check("GK3D6 has no declared reverse consumers", reverse == set())

    proposal = _load(CAMPAIGN / "proposal.yaml")
    expected_status = (
        "qualified" if proposal["status"] == "accepted" else "pending_adjudication"
    )
    expected_mapping = ROOT_MAPPING if expected_status == "qualified" else []
    checks.check(
        "root source authority matches the campaign stage",
        units["GK3D6"]["disposition"] == expected_status
        and units["GK3D6"]["accepted_claims"] == expected_mapping,
    )
    if expected_status == "qualified":
        dispositions = _load(ROOT / "migration/dispositions.yaml")["units"]
        decision = dispositions["GK3D6"]
        checks.check(
            "editable root disposition and evidence are materialized",
            decision["disposition"] == "qualified"
            and decision["accepted_claims"] == ROOT_MAPPING
            and all((ROOT / path).is_file() for path in decision["evidence"]),
        )

    claims = {claim["id"]: claim for claim in _load(ROOT / "governance/claims.yaml")["claims"]}
    checks.check(
        "accepted composition has accepted four-axis authority",
        all(
            claim_id in claims
            and claims[claim_id]["review"] == "accepted"
            and claims[claim_id]["epistemic"] in {"active", "qualified"}
            for claim_id in ROOT_MAPPING
        ),
    )
    checks.check(
        "C-VAC-005 stays reserved and C-VAC-006 stays unpromoted",
        "C-VAC-005" not in claims and "C-VAC-006" not in claims,
    )
    inventory = _load(CAMPAIGN / "evidence/source-graph-inventory.yaml")
    checks.check(
        "graph replay counts no duplicate native execution",
        inventory["expected_coverage"]["fresh_native_executions"] == 1
        and inventory["expected_coverage"]["graph_replay_native_executions"] == 0
        and inventory["expected_coverage"]["version_only_scientific_failures"] == 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
