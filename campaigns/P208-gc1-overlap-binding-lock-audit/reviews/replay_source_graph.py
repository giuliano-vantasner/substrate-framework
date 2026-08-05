#!/usr/bin/env python3
"""Replay GC1's hash, predicate, authority, and compatibility graph."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import (
    audit_numpy_trapezoid_compatibility,
)
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
CAMPAIGN = Path(__file__).resolve().parents[1]
NODES = {
    "EM6": ("merged-framework/bridges/phase-3/bridge_EM6_derived_profile_stability.py", "926df2dc5014042472b3d47576af06676eb654d9da4634f147c7044d4e91f897", 11, 2),
    "FG2": ("merged-framework/bridges/phase-11/bridge_FG2_family_tower.py", "aef0ed225fca1f12fcccb284015d97ce3faa25291f07addda24e82ebbc5ae166", 7, 3),
    "GC1": ("merged-framework/bridges/phase-42/bridge_GC1_overlap_binding_lock.py", "3c9610d349b7fa0e47a4f122ea5ab84da3a03f6cd83686c3aa6f161bfccf4ebe", 9, 2),
    "GC2": ("merged-framework/bridges/phase-42/bridge_GC2_corpus_already_multisoliton.py", "07611b1eb63450e7e82ab696eafe8566a6931a9acae9ccfbebe1823765ac4a65", 8, 2),
    "GC3": ("merged-framework/bridges/phase-42/bridge_GC3_cp_needs_relative_phases.py", "0e44cc80e118cd38366c033c508774bf9a7cab981e8ea3cf054998958426dad8", 9, 1),
    "GC4": ("merged-framework/bridges/phase-42/bridge_GC4_stability_forces_three.py", "3292400544911dca74009a019b24b44f105f8aeb5c68a6172220903950f465bb", 8, 1),
    "GC5": ("merged-framework/bridges/phase-42/bridge_GC5_two_role_structure_and_counts.py", "ffc638accff802c16804bd793b47e1cc5da018d5e0742ace57d9d3207e06b220", 8, 1),
    "GC6": ("merged-framework/bridges/phase-42/bridge_GC6_consequence_and_verdict.py", "e09822946b9b44ade21632c7db42d2061e493b112a13fab9a44e74a6a6d18b17", 6, 1),
    "MH1": ("merged-framework/bridges/phase-20/bridge_MH1_yukawa_overlap_mass_formula.py", "6e32edbd129c40ed587408fa70128951f65c04f379a633414fd8202e80ca1854", 4, 1),
    "MH2": ("merged-framework/bridges/phase-20/bridge_MH2_overlap_hierarchy.py", "0596c06fb98205f5deca9cfcd99e1442216c95925d6182788c6cb01686a161d9", 5, 2),
    "O1": ("merged-framework/bridges/phase-7/bridge_O1_spin1_bec_rp2.py", "270877b5ae3507ba5000643333a06269dce2c6a2ec7dbd9ae86f8e2b6e77ef64", 7, 1),
    "WM7": ("merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py", "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361", 10, 1),
    "WM9": ("merged-framework/bridges/phase-39/bridge_WM9_scalar_multiplicity_from_condensate.py", "d0d94417f5abd572e2e306c1f33dc264d42cfef94e4281dbc258ea9fa83ffd4d", 8, 1),
    "WM10": ("merged-framework/bridges/phase-39/bridge_WM10_corrected_boundary_two_loop.py", "a813f32841a4809f0ca301d8f01cb432d07d43c6bc46433970c1dcf60afe8d29", 7, 1),
}
TERMINAL_DEPENDENCIES = {"EM6", "FG2", "MH1", "MH2", "O1", "WM7", "WM9", "WM10"}
CYCLE_DEPENDENCIES = {"GC3", "GC4", "GC5"}
DIRECT_CONSUMERS = {"GC2", "GC3", "GC4", "GC5", "GC6"}
ROOT_MAPPING = [
    "C-QBL-001",
    "C-QBL-002",
    "C-QBL-003",
    "C-OVL-001",
    "C-OVL-002",
    "C-QBL-005",
]


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(path: Path) -> tuple[int, int]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    return len(calls), sum(isinstance(node, ast.Assert) for node in ast.walk(tree))


def main() -> int:
    checks = CheckLedger("P208-GC1-SOURCE-GRAPH")
    queue = load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}
    totals = [0, 0]
    compatibility: dict[str, int] = {}
    for unit, (relative, expected_hash, expected_calls, expected_asserts) in NODES.items():
        source = SOURCE_ROOT / relative
        checks.check(
            f"{unit} source remains path and hash pinned",
            units[unit]["path"] == relative
            and units[unit]["sha256"] == expected_hash
            and digest(source) == expected_hash,
        )
        actual = inventory(source)
        totals[0] += actual[0]
        totals[1] += actual[1]
        checks.check(
            f"{unit} predicate inventory remains exact",
            actual == (expected_calls, expected_asserts),
        )
        audit = audit_numpy_trapezoid_compatibility(
            source.read_text(encoding="utf-8"), filename=relative
        )
        if audit.legacy_references:
            compatibility[unit] = audit.legacy_references

    checks.check(
        "fourteen-node graph inventories 107 checks and 20 assertions once",
        len(NODES) == 14 and totals == [107, 20],
    )
    checks.check("GC1 graph has no quadrature compatibility surface", compatibility == {})
    checks.check(
        "GC1 source dependency partition is exact",
        set(units["GC1"]["candidate_dependencies"])
        == TERMINAL_DEPENDENCIES | CYCLE_DEPENDENCIES,
    )
    reverse = {
        row["source_unit"]
        for row in queue["units"]
        if "GC1" in row.get("candidate_dependencies", [])
    }
    checks.check("five direct reverse consumers are exact", reverse == DIRECT_CONSUMERS)

    dependency = load(CAMPAIGN / "evidence/dependency-audit.yaml")
    checks.check(
        "pending cycle edges are recorded as nonauthoritative",
        set(dependency["nonauthoritative_cycle_dependencies"])
        == CYCLE_DEPENDENCIES
        and dependency["backward_authority"] == "none",
    )
    checks.check(
        "terminal dependency mappings are frozen individually",
        set(dependency["terminal_dependencies"]) == TERMINAL_DEPENDENCIES
        and all(dependency["terminal_dependencies"][unit] for unit in TERMINAL_DEPENDENCIES),
    )

    proposal = load(CAMPAIGN / "proposal.yaml")
    expected_status = "qualified" if proposal["status"] == "accepted" else "pending_adjudication"
    expected_mapping = ROOT_MAPPING if expected_status == "qualified" else []
    checks.check(
        "GC1 root authority matches the campaign stage",
        units["GC1"]["disposition"] == expected_status
        and units["GC1"]["accepted_claims"] == expected_mapping,
    )
    if expected_status == "qualified":
        decision = load(ROOT / "migration/dispositions.yaml")["units"]["GC1"]
        checks.check(
            "editable GC1 disposition and evidence are materialized",
            decision["disposition"] == "qualified"
            and decision["accepted_claims"] == ROOT_MAPPING
            and all((ROOT / path).is_file() for path in decision["evidence"]),
        )
    claims = {
        claim["id"]: claim
        for claim in load(ROOT / "governance/claims.yaml")["claims"]
    }
    if proposal["status"] == "accepted":
        checks.check(
            "accepted GC1 mapping is claim-level closed",
            all(
                claim_id in claims
                and claims[claim_id]["review"] == "accepted"
                and claims[claim_id]["epistemic"] in {"active", "qualified"}
                for claim_id in ROOT_MAPPING
            ),
        )
    coverage = load(CAMPAIGN / "evidence/source-graph-inventory.yaml")[
        "expected_coverage"
    ]
    checks.check(
        "graph replay adds no duplicate execution or scientific version failure",
        coverage["fresh_native_executions"] == 1
        and coverage["graph_replay_native_executions"] == 0
        and coverage["version_only_scientific_failures"] == 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
