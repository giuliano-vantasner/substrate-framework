#!/usr/bin/env python3
"""Replay WM8's terminal dependency and reverse-consumer authority graph."""

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
    "S1": ("merged-framework/bridges/phase-4/bridge_S1_nn_force_two_skyrmion.py", "ebe1ba930be26f17671d8e82779d14fc00e7a8b988a4aada722a32d0d9328ddd", 11, 2),
    "S2": ("merged-framework/bridges/phase-4/bridge_S2_meson_hedgehog_spectrum.py", "48a9eadf6fbc1e3ebe7fcd6b98c2d60cc10a3f5282404c84e4626910f296eaf7", 10, 1),
    "S3": ("merged-framework/bridges/phase-4/bridge_S3_su3_wzw_baryon_reps.py", "44d8cd1f3a3b3d0a316d0984db92d5e47e13cac9dcf3d476e2d996bf09f13b9a", 10, 2),
    "SM2": ("merged-framework/bridges/phase-9/bridge_SM2_generation_hypercharge_charges.py", "cc5532e86128f010f6801dada96ae1ece5a6be845817127d69cf72810b9e33f1", 7, 1),
    "SM4": ("merged-framework/bridges/phase-9/bridge_SM4_coupling_running_unification.py", "c0cc7ed32343afc65cf582d81b2455fdba96d2550e64e3e595e4c995ee53e3ac", 8, 1),
    "WM2": ("merged-framework/bridges/phase-23/bridge_WM2_common_induction_normalization.py", "3c656894fc782dd40dcb495a91de5bbf5a46ec378bb3593eb30d7d4b387f34a3", 10, 1),
    "WM3": ("merged-framework/bridges/phase-23/bridge_WM3_sin2thetaw_rg_running.py", "2328ae4d6e66e1caa14a39042c362e57258406383f14ecaa5f5f6c468105e298", 10, 1),
    "WM6": ("merged-framework/bridges/phase-33/bridge_WM6_two_loop_running.py", "6d1ea4245adcf490466974d4a40b24843cd92e883c6e885936fb030cd1b31d57", 11, 1),
    "WM7": ("merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py", "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361", 10, 1),
    "WM8": ("merged-framework/bridges/phase-39/bridge_WM8_corrected_boundary_running.py", "741497f63cc39ee96c71e9a999c49ef9e821cf612d8b48b2959d05f9e6940518", 10, 1),
    "WM9": ("merged-framework/bridges/phase-39/bridge_WM9_scalar_multiplicity_from_condensate.py", "d0d94417f5abd572e2e306c1f33dc264d42cfef94e4281dbc258ea9fa83ffd4d", 8, 1),
    "WM10": ("merged-framework/bridges/phase-39/bridge_WM10_corrected_boundary_two_loop.py", "a813f32841a4809f0ca301d8f01cb432d07d43c6bc46433970c1dcf60afe8d29", 7, 1),
    "GC6": ("merged-framework/bridges/phase-42/bridge_GC6_consequence_and_verdict.py", "e09822946b9b44ade21632c7db42d2061e493b112a13fab9a44e74a6a6d18b17", 6, 1),
}
DIRECT_DEPENDENCIES = {"S1", "S2", "S3", "SM2", "SM4", "WM2", "WM3", "WM6", "WM7"}
DIRECT_CONSUMERS = {"GC6", "WM10", "WM7", "WM9"}
PENDING_CONSUMERS = {"GC6", "WM10", "WM9"}
ROOT_MAPPING = ["C-MIX-002", "C-REP-001", "C-REP-003", "C-RGE-004", "C-RGE-005", "C-RGE-006", "C-VAC-003"]


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(path: Path) -> tuple[int, int]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "check"]
    return len(calls), sum(isinstance(node, ast.Assert) for node in ast.walk(tree))


def main() -> int:
    checks = CheckLedger("P205-WM8-SOURCE-GRAPH")
    queue = load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}
    compatibility: dict[str, int] = {}
    totals = [0, 0]
    for unit, (relative, expected_hash, expected_calls, expected_asserts) in NODES.items():
        source = SOURCE_ROOT / relative
        checks.check(f"{unit} source remains path and hash pinned", units[unit]["path"] == relative and units[unit]["sha256"] == expected_hash and digest(source) == expected_hash)
        actual = inventory(source)
        totals[0] += actual[0]
        totals[1] += actual[1]
        checks.check(f"{unit} predicate inventory remains exact", actual == (expected_calls, expected_asserts))
        audit = audit_numpy_trapezoid_compatibility(source.read_text(encoding="utf-8"), filename=relative)
        if audit.legacy_references:
            compatibility[unit] = audit.legacy_references
            checks.check(f"{unit} legacy name is immutable alias-only evidence", unit == "S2" and audit.legacy_references == 3 and audit.eager_legacy_default_fallbacks == 0)

    checks.check("thirteen-node graph inventories 118 checks and 15 assertions once", len(NODES) == 13 and totals == [118, 15])
    checks.check("S2 is the sole immutable compatibility node", compatibility == {"S2": 3})
    checks.check("WM8's nine dependencies are exact and terminal", set(units["WM8"]["candidate_dependencies"]) == DIRECT_DEPENDENCIES and all(units[unit]["disposition"] != "pending_adjudication" for unit in DIRECT_DEPENDENCIES))
    checks.check("every dependency retains an individual accepted mapping", all(units[unit]["accepted_claims"] for unit in DIRECT_DEPENDENCIES))
    reverse = {row["source_unit"] for row in queue["units"] if "WM8" in row.get("candidate_dependencies", [])}
    checks.check("four direct reverse consumers are exact", reverse == DIRECT_CONSUMERS)
    checks.check("three forward consumers remain pending and nonauthoritative", all(units[unit]["disposition"] == "pending_adjudication" for unit in PENDING_CONSUMERS))
    checks.check("qualified WM7 grants no backward WM8 authority", units["WM7"]["disposition"] == "qualified" and "C-RGE-006" not in units["WM7"]["accepted_claims"])

    proposal = load(CAMPAIGN / "proposal.yaml")
    expected_status = "qualified" if proposal["status"] == "accepted" else "pending_adjudication"
    expected_mapping = ROOT_MAPPING if expected_status == "qualified" else []
    checks.check("WM8 root authority matches the campaign stage", units["WM8"]["disposition"] == expected_status and units["WM8"]["accepted_claims"] == expected_mapping)
    if expected_status == "qualified":
        decision = load(ROOT / "migration/dispositions.yaml")["units"]["WM8"]
        checks.check("editable WM8 disposition and evidence are materialized", decision["disposition"] == "qualified" and decision["accepted_claims"] == ROOT_MAPPING and all((ROOT / path).is_file() for path in decision["evidence"]))
    claims = {claim["id"]: claim for claim in load(ROOT / "governance/claims.yaml")["claims"]}
    checks.check("accepted composition retains accepted four-axis authority", all(claim_id in claims and claims[claim_id]["review"] == "accepted" and claims[claim_id]["epistemic"] in {"active", "qualified"} for claim_id in ROOT_MAPPING))
    checks.check("C-RGE-008 remains reserved and unpromoted", "C-RGE-008" not in claims)
    coverage = load(CAMPAIGN / "evidence/source-graph-inventory.yaml")["expected_coverage"]
    checks.check("graph replay adds no duplicate execution or scientific version failure", coverage["fresh_native_executions"] == 1 and coverage["graph_replay_native_executions"] == 0 and coverage["version_only_scientific_failures"] == 0)
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
