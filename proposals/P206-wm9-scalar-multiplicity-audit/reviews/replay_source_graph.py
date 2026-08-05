#!/usr/bin/env python3
"""Replay WM9's terminal dependency and reverse-consumer authority graph."""

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
    "EM6": ("merged-framework/bridges/phase-3/bridge_EM6_derived_profile_stability.py", "926df2dc5014042472b3d47576af06676eb654d9da4634f147c7044d4e91f897", 11, 2),
    "FG2": ("merged-framework/bridges/phase-11/bridge_FG2_family_tower.py", "aef0ed225fca1f12fcccb284015d97ce3faa25291f07addda24e82ebbc5ae166", 7, 3),
    "FG4": ("merged-framework/bridges/phase-11/bridge_FG4_cp_kobayashi_maskawa.py", "d9ebb32d440fb87540c7cb2d02a846b76dd4ee405288895308561762cd720ceb", 7, 1),
    "M1": ("merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9, 1),
    "MH1": ("merged-framework/bridges/phase-20/bridge_MH1_yukawa_overlap_mass_formula.py", "6e32edbd129c40ed587408fa70128951f65c04f379a633414fd8202e80ca1854", 4, 1),
    "SM2": ("merged-framework/bridges/phase-9/bridge_SM2_generation_hypercharge_charges.py", "cc5532e86128f010f6801dada96ae1ece5a6be845817127d69cf72810b9e33f1", 7, 1),
    "SM4": ("merged-framework/bridges/phase-9/bridge_SM4_coupling_running_unification.py", "c0cc7ed32343afc65cf582d81b2455fdba96d2550e64e3e595e4c995ee53e3ac", 8, 1),
    "WM3": ("merged-framework/bridges/phase-23/bridge_WM3_sin2thetaw_rg_running.py", "2328ae4d6e66e1caa14a39042c362e57258406383f14ecaa5f5f6c468105e298", 10, 1),
    "WM7": ("merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py", "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361", 10, 1),
    "WM8": ("merged-framework/bridges/phase-39/bridge_WM8_corrected_boundary_running.py", "741497f63cc39ee96c71e9a999c49ef9e821cf612d8b48b2959d05f9e6940518", 10, 1),
    "WM9": ("merged-framework/bridges/phase-39/bridge_WM9_scalar_multiplicity_from_condensate.py", "d0d94417f5abd572e2e306c1f33dc264d42cfef94e4281dbc258ea9fa83ffd4d", 8, 1),
    "WM10": ("merged-framework/bridges/phase-39/bridge_WM10_corrected_boundary_two_loop.py", "a813f32841a4809f0ca301d8f01cb432d07d43c6bc46433970c1dcf60afe8d29", 7, 1),
    "GC1": ("merged-framework/bridges/phase-42/bridge_GC1_overlap_binding_lock.py", "3c9610d349b7fa0e47a4f122ea5ab84da3a03f6cd83686c3aa6f161bfccf4ebe", 9, 2),
    "GC2": ("merged-framework/bridges/phase-42/bridge_GC2_corpus_already_multisoliton.py", "07611b1eb63450e7e82ab696eafe8566a6931a9acae9ccfbebe1823765ac4a65", 8, 2),
    "GC5": ("merged-framework/bridges/phase-42/bridge_GC5_two_role_structure_and_counts.py", "ffc638accff802c16804bd793b47e1cc5da018d5e0742ace57d9d3207e06b220", 8, 1),
    "GC6": ("merged-framework/bridges/phase-42/bridge_GC6_consequence_and_verdict.py", "e09822946b9b44ade21632c7db42d2061e493b112a13fab9a44e74a6a6d18b17", 6, 1),
}
DIRECT_DEPENDENCIES = {"EM6", "FG2", "FG4", "M1", "MH1", "SM2", "SM4", "WM3", "WM7", "WM8"}
DIRECT_CONSUMERS = {"WM10", "GC1", "GC2", "GC5", "GC6"}
ROOT_MAPPING = [
    "C-QBL-001",
    "C-QBL-003",
    "C-OVL-001",
    "C-MIX-002",
    "C-GSM-001",
    "C-REP-001",
    "C-REP-003",
    "C-RGE-005",
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
    checks = CheckLedger("P206-WM9-SOURCE-GRAPH")
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
        "sixteen-node graph inventories 129 checks and 21 assertions once",
        len(NODES) == 16 and totals == [129, 21],
    )
    checks.check(
        "WM9 graph has no quadrature compatibility surface",
        compatibility == {},
    )
    checks.check(
        "WM9's ten declared dependencies are exact and terminal",
        set(units["WM9"]["candidate_dependencies"]) == DIRECT_DEPENDENCIES
        and all(
            units[unit]["disposition"] != "pending_adjudication"
            for unit in DIRECT_DEPENDENCIES
        ),
    )
    checks.check(
        "every dependency retains an individual accepted mapping",
        all(units[unit]["accepted_claims"] for unit in DIRECT_DEPENDENCIES),
    )
    reverse = {
        row["source_unit"]
        for row in queue["units"]
        if "WM9" in row.get("candidate_dependencies", [])
    }
    checks.check("five direct reverse consumers are exact", reverse == DIRECT_CONSUMERS)
    checks.check(
        "all five forward consumers remain pending and nonauthoritative",
        all(
            units[unit]["disposition"] == "pending_adjudication"
            for unit in DIRECT_CONSUMERS
        ),
    )

    proposal = load(CAMPAIGN / "proposal.yaml")
    expected_status = "qualified" if proposal["status"] == "accepted" else "pending_adjudication"
    expected_mapping = ROOT_MAPPING if expected_status == "qualified" else []
    checks.check(
        "WM9 root authority matches the campaign stage",
        units["WM9"]["disposition"] == expected_status
        and units["WM9"]["accepted_claims"] == expected_mapping,
    )
    if expected_status == "qualified":
        decision = load(ROOT / "migration/dispositions.yaml")["units"]["WM9"]
        checks.check(
            "editable WM9 disposition and evidence are materialized",
            decision["disposition"] == "qualified"
            and decision["accepted_claims"] == ROOT_MAPPING
            and all((ROOT / path).is_file() for path in decision["evidence"]),
        )
    claims = {
        claim["id"]: claim
        for claim in load(ROOT / "governance/claims.yaml")["claims"]
    }
    checks.check(
        "accepted composition retains accepted four-axis authority",
        all(
            claim_id in claims
            and claims[claim_id]["review"] == "accepted"
            and claims[claim_id]["epistemic"] in {"active", "qualified"}
            for claim_id in ROOT_MAPPING
        ),
    )
    checks.check(
        "multiplicity theorem identifiers remain reserved and unpromoted",
        "C-OVL-004" not in claims and "C-RGE-008" not in claims,
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
