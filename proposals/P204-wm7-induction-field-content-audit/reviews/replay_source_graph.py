#!/usr/bin/env python3
"""Replay WM7's frozen dependency/SCC/consumer graph without cyclic authority."""

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
    "W1": ("merged-framework/bridges/phase-6/bridge_W1_parity_odd_chiral_coupling.py", "bfac7d7e4ccb0cdabc6bb2703dadb650c0e09ea883ec3ff70f039231d3e62388", 8, 2),
    "W2": ("merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9, 1),
    "W3": ("merged-framework/bridges/phase-6/bridge_W3_VA_charged_current.py", "b49a0bd1075b16b5906719b6ed51454ed04adab5168be7ec98178599313b3f17", 7, 1),
    "QCD1": ("merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py", "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed", 11, 1),
    "QCD3": ("merged-framework/bridges/phase-8/bridge_QCD3_asymptotic_freedom.py", "7d7c9a9bc2f04c933fc62484fec3329c0eb7769bb54ba8cd67701da5110af0ca", 9, 1),
    "SM2": ("merged-framework/bridges/phase-9/bridge_SM2_generation_hypercharge_charges.py", "cc5532e86128f010f6801dada96ae1ece5a6be845817127d69cf72810b9e33f1", 7, 1),
    "SM3": ("merged-framework/bridges/phase-9/bridge_SM3_anomaly_cancellation.py", "3ace90aa5377050e4dcab5778996079eea92c9cc56a53c276a60a5508f63b529", 8, 1),
    "SM4": ("merged-framework/bridges/phase-9/bridge_SM4_coupling_running_unification.py", "c0cc7ed32343afc65cf582d81b2455fdba96d2550e64e3e595e4c995ee53e3ac", 8, 1),
    "FG4": ("merged-framework/bridges/phase-11/bridge_FG4_cp_kobayashi_maskawa.py", "d9ebb32d440fb87540c7cb2d02a846b76dd4ee405288895308561762cd720ceb", 7, 1),
    "WM1": ("merged-framework/bridges/phase-23/bridge_WM1_sin2thetaw_trace_ratio.py", "75dc34e168c39cd0af0a21cd4c7d039088ac74baefb6615ece98f5069f5b8953", 9, 1),
    "WM2": ("merged-framework/bridges/phase-23/bridge_WM2_common_induction_normalization.py", "3c656894fc782dd40dcb495a91de5bbf5a46ec378bb3593eb30d7d4b387f34a3", 10, 1),
    "WM3": ("merged-framework/bridges/phase-23/bridge_WM3_sin2thetaw_rg_running.py", "2328ae4d6e66e1caa14a39042c362e57258406383f14ecaa5f5f6c468105e298", 10, 1),
    "WM5": ("merged-framework/bridges/phase-33/bridge_WM5_two_loop_coefficients.py", "8c3fbfeecb6f98d7d80c47e8f267fe1216dde724b81cc3f73f2a3bb17caf1bbc", 11, 1),
    "WM7": ("merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py", "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361", 10, 1),
    "WM8": ("merged-framework/bridges/phase-39/bridge_WM8_corrected_boundary_running.py", "741497f63cc39ee96c71e9a999c49ef9e821cf612d8b48b2959d05f9e6940518", 10, 1),
    "WM9": ("merged-framework/bridges/phase-39/bridge_WM9_scalar_multiplicity_from_condensate.py", "d0d94417f5abd572e2e306c1f33dc264d42cfef94e4281dbc258ea9fa83ffd4d", 8, 1),
    "WM10": ("merged-framework/bridges/phase-39/bridge_WM10_corrected_boundary_two_loop.py", "a813f32841a4809f0ca301d8f01cb432d07d43c6bc46433970c1dcf60afe8d29", 7, 1),
    "GC1": ("merged-framework/bridges/phase-42/bridge_GC1_overlap_binding_lock.py", "3c9610d349b7fa0e47a4f122ea5ab84da3a03f6cd83686c3aa6f161bfccf4ebe", 9, 2),
    "GC2": ("merged-framework/bridges/phase-42/bridge_GC2_corpus_already_multisoliton.py", "07611b1eb63450e7e82ab696eafe8566a6931a9acae9ccfbebe1823765ac4a65", 8, 2),
    "GC3": ("merged-framework/bridges/phase-42/bridge_GC3_cp_needs_relative_phases.py", "0e44cc80e118cd38366c033c508774bf9a7cab981e8ea3cf054998958426dad8", 9, 1),
    "GC4": ("merged-framework/bridges/phase-42/bridge_GC4_stability_forces_three.py", "3292400544911dca74009a019b24b44f105f8aeb5c68a6172220903950f465bb", 8, 1),
    "GC5": ("merged-framework/bridges/phase-42/bridge_GC5_two_role_structure_and_counts.py", "ffc638accff802c16804bd793b47e1cc5da018d5e0742ace57d9d3207e06b220", 8, 1),
    "GC6": ("merged-framework/bridges/phase-42/bridge_GC6_consequence_and_verdict.py", "e09822946b9b44ade21632c7db42d2061e493b112a13fab9a44e74a6a6d18b17", 6, 1),
}
DIRECT_DEPENDENCIES = {"FG4", "QCD1", "QCD3", "S1", "S2", "S3", "SM2", "SM3", "SM4", "W1", "W2", "W3", "WM1", "WM2", "WM3", "WM5", "WM8"}
DIRECT_CONSUMERS = {"GC1", "GC2", "GC3", "GC4", "GC5", "GC6", "WM10", "WM8", "WM9"}
TERMINAL_DEPENDENCIES = DIRECT_DEPENDENCIES - {"WM8"}
ROOT_MAPPING = ["C-MIX-002", "C-REP-001", "C-REP-003", "C-ANO-001", "C-RGE-005", "C-VAC-003"]
LEGACY_COUNTS = {"S2": 3, "W1": 2, "W3": 2}


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
    assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    return len(calls), len(assertions)


def main() -> int:
    checks = CheckLedger("P204-WM7-SOURCE-GRAPH")
    queue = load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}
    compatibility: dict[str, int] = {}
    totals = [0, 0]
    for unit, (relative, expected_hash, expected_calls, expected_asserts) in NODES.items():
        source = SOURCE_ROOT / relative
        checks.check(
            f"{unit} source remains path and hash pinned",
            units[unit]["path"] == relative and units[unit]["sha256"] == expected_hash and digest(source) == expected_hash,
        )
        actual_calls, actual_asserts = inventory(source)
        totals[0] += actual_calls
        totals[1] += actual_asserts
        checks.check(
            f"{unit} predicate inventory remains exact",
            (actual_calls, actual_asserts) == (expected_calls, expected_asserts),
        )
        audit = audit_numpy_trapezoid_compatibility(source.read_text(encoding="utf-8"), filename=relative)
        if audit.legacy_references:
            compatibility[unit] = audit.legacy_references
            checks.check(
                f"{unit} legacy name remains immutable alias-only evidence",
                audit.legacy_references == LEGACY_COUNTS[unit] and audit.eager_legacy_default_fallbacks == 0,
            )

    checks.check("twenty-six-node graph inventories 228 checks and 31 assertions once", len(NODES) == 26 and totals == [228, 31])
    checks.check("only three immutable ancestors expose the legacy NumPy name", compatibility == LEGACY_COUNTS)
    checks.check(
        "WM7's seventeen direct dependencies are exact",
        set(units["WM7"]["candidate_dependencies"]) == DIRECT_DEPENDENCIES,
    )
    checks.check(
        "sixteen noncyclic dependencies are terminally governed",
        all(units[unit]["disposition"] != "pending_adjudication" and units[unit]["accepted_claims"] for unit in TERMINAL_DEPENDENCIES),
    )
    checks.check(
        "WM8 is the sole excluded pending dependency and closes the source SCC",
        units["WM8"]["disposition"] == "pending_adjudication" and "WM7" in units["WM8"]["candidate_dependencies"],
    )
    reverse = {row["source_unit"] for row in queue["units"] if "WM7" in row.get("candidate_dependencies", [])}
    checks.check("nine direct reverse consumers are exact", reverse == DIRECT_CONSUMERS)
    checks.check(
        "every reverse consumer remains nonauthoritative or separately governed",
        all(unit == "WM8" or units[unit]["disposition"] == "pending_adjudication" for unit in DIRECT_CONSUMERS),
    )
    proposal = load(CAMPAIGN / "proposal.yaml")
    expected_status = "qualified" if proposal["status"] == "accepted" else "pending_adjudication"
    expected_mapping = ROOT_MAPPING if expected_status == "qualified" else []
    checks.check(
        "WM7 root authority matches the campaign stage",
        units["WM7"]["disposition"] == expected_status and units["WM7"]["accepted_claims"] == expected_mapping,
    )
    if expected_status == "qualified":
        decision = load(ROOT / "migration/dispositions.yaml")["units"]["WM7"]
        checks.check(
            "editable WM7 disposition and evidence are materialized",
            decision["disposition"] == "qualified" and decision["accepted_claims"] == ROOT_MAPPING and all((ROOT / path).is_file() for path in decision["evidence"]),
        )
    claims = {claim["id"]: claim for claim in load(ROOT / "governance/claims.yaml")["claims"]}
    checks.check(
        "accepted composition retains accepted four-axis authority",
        all(claim_id in claims and claims[claim_id]["review"] == "accepted" and claims[claim_id]["epistemic"] in {"active", "qualified"} for claim_id in ROOT_MAPPING),
    )
    checks.check("C-RGE-007 remains reserved and unpromoted", "C-RGE-007" not in claims)
    coverage = load(CAMPAIGN / "evidence/source-graph-inventory.yaml")["expected_coverage"]
    checks.check(
        "graph replay adds no duplicate native execution or scientific version failure",
        coverage["fresh_native_executions"] == 1 and coverage["graph_replay_native_executions"] == 0 and coverage["version_only_scientific_failures"] == 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
