#!/usr/bin/env python3
"""Replay GC6's frozen source graph without executing predecessor scripts."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
EXPECTED = {
    "EM6": ("merged-framework/bridges/phase-3/bridge_EM6_derived_profile_stability.py", "926df2dc5014042472b3d47576af06676eb654d9da4634f147c7044d4e91f897", 11, 2),
    "FG2": ("merged-framework/bridges/phase-11/bridge_FG2_family_tower.py", "aef0ed225fca1f12fcccb284015d97ce3faa25291f07addda24e82ebbc5ae166", 7, 3),
    "FG4": ("merged-framework/bridges/phase-11/bridge_FG4_cp_kobayashi_maskawa.py", "d9ebb32d440fb87540c7cb2d02a846b76dd4ee405288895308561762cd720ceb", 7, 1),
    "GC1": ("merged-framework/bridges/phase-42/bridge_GC1_overlap_binding_lock.py", "3c9610d349b7fa0e47a4f122ea5ab84da3a03f6cd83686c3aa6f161bfccf4ebe", 9, 2),
    "GC2": ("merged-framework/bridges/phase-42/bridge_GC2_corpus_already_multisoliton.py", "07611b1eb63450e7e82ab696eafe8566a6931a9acae9ccfbebe1823765ac4a65", 8, 2),
    "GC3": ("merged-framework/bridges/phase-42/bridge_GC3_cp_needs_relative_phases.py", "0e44cc80e118cd38366c033c508774bf9a7cab981e8ea3cf054998958426dad8", 9, 1),
    "GC4": ("merged-framework/bridges/phase-42/bridge_GC4_stability_forces_three.py", "3292400544911dca74009a019b24b44f105f8aeb5c68a6172220903950f465bb", 8, 1),
    "GC5": ("merged-framework/bridges/phase-42/bridge_GC5_two_role_structure_and_counts.py", "ffc638accff802c16804bd793b47e1cc5da018d5e0742ace57d9d3207e06b220", 8, 1),
    "GC6": ("merged-framework/bridges/phase-42/bridge_GC6_consequence_and_verdict.py", "e09822946b9b44ade21632c7db42d2061e493b112a13fab9a44e74a6a6d18b17", 6, 1),
    "MH2": ("merged-framework/bridges/phase-20/bridge_MH2_overlap_hierarchy.py", "0596c06fb98205f5deca9cfcd99e1442216c95925d6182788c6cb01686a161d9", 5, 2),
    "WM10": ("merged-framework/bridges/phase-39/bridge_WM10_corrected_boundary_two_loop.py", "a813f32841a4809f0ca301d8f01cb432d07d43c6bc46433970c1dcf60afe8d29", 7, 1),
    "WM2": ("merged-framework/bridges/phase-23/bridge_WM2_common_induction_normalization.py", "3c656894fc782dd40dcb495a91de5bbf5a46ec378bb3593eb30d7d4b387f34a3", 10, 1),
    "WM3": ("merged-framework/bridges/phase-23/bridge_WM3_sin2thetaw_rg_running.py", "2328ae4d6e66e1caa14a39042c362e57258406383f14ecaa5f5f6c468105e298", 10, 1),
    "WM7": ("merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py", "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361", 10, 1),
    "WM8": ("merged-framework/bridges/phase-39/bridge_WM8_corrected_boundary_running.py", "741497f63cc39ee96c71e9a999c49ef9e821cf612d8b48b2959d05f9e6940518", 10, 1),
    "WM9": ("merged-framework/bridges/phase-39/bridge_WM9_scalar_multiplicity_from_condensate.py", "d0d94417f5abd572e2e306c1f33dc264d42cfef94e4281dbc258ea9fa83ffd4d", 8, 1),
}
DIRECT = set(EXPECTED) - {"GC6"}
REVERSE = {"GC5"}
ROOT_MAPPING = [
    "C-QBL-001",
    "C-OVL-001",
    "C-OVL-002",
    "C-OVL-003",
    "C-OVL-005",
    "C-MIX-001",
    "C-MIX-002",
    "C-MIX-003",
    "C-MIX-004",
    "C-QBL-006",
    "C-PHS-001",
    "C-PHS-002",
    "C-REP-001",
    "C-REP-003",
    "C-ANO-001",
    "C-RGE-004",
    "C-RGE-005",
    "C-RGE-006",
    "C-VAC-003",
]


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def main() -> int:
    checks = CheckLedger("P213-GC6-SOURCE-GRAPH")
    checks.check(
        "frozen graph node set remains exact",
        set(EXPECTED) == {"GC6"} | DIRECT | REVERSE,
    )
    checks.check(
        "frozen graph totals remain exact",
        len(EXPECTED) == 16
        and sum(item[2] for item in EXPECTED.values()) == 133
        and sum(item[3] for item in EXPECTED.values()) == 22,
    )
    compatibility = {}
    for label, (relative, expected_hash, expected_checks, expected_asserts) in EXPECTED.items():
        path = SOURCE_ROOT / relative
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        checks.check(
            f"{label} source hash remains pinned",
            hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash,
        )
        checks.check(
            f"{label} predicate and assertion inventory remains exact",
            sum(
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "check"
                for node in ast.walk(tree)
            )
            == expected_checks
            and sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
            == expected_asserts,
        )
        compatibility[label] = audit_numpy_trapezoid_compatibility(
            source, filename=str(path)
        )
    checks.check(
        "all graph nodes have zero quadrature compatibility surface",
        all(
            audit.legacy_references
            == audit.current_references
            == audit.eager_legacy_default_fallbacks
            == 0
            for audit in compatibility.values()
        ),
    )

    dispositions = load(ROOT / "migration/dispositions.yaml")["units"]
    checks.check(
        "all direct authority dependencies remain terminal",
        all(
            dispositions[label]["disposition"]
            in {"qualified", "migrated", "duplicate_evidence", "refuted", "out_of_scope"}
            for label in DIRECT
        ),
    )
    checks.check(
        "GC5 reverse edge remains nonauthoritative for its earlier disposition",
        REVERSE == {"GC5"}
        and "GC6" not in dispositions["GC5"]["accepted_claims"],
    )

    proposal_path = ROOT / "proposals/P213-gc6-fcnc-consequence-audit/proposal.yaml"
    if not proposal_path.exists():
        proposal_path = ROOT / "campaigns/P213-gc6-fcnc-consequence-audit/proposal.yaml"
    proposal = load(proposal_path)
    root = dispositions.get("GC6")
    if root is None:
        checks.check(
            "active root remains governed by the pinned proposal",
            proposal["claims_proposed"] == ["C-MIX-004"]
            and proposal["revision"] == 3,
        )
    else:
        checks.check(
            "terminal root remains qualified with the exact mapping",
            root["disposition"] == "qualified"
            and root["accepted_claims"] == ROOT_MAPPING,
        )

    release = load(ROOT / "governance/releases/current.yaml")
    if root is None:
        checks.check(
            "base release excludes the provisional claim before promotion",
            "C-MIX-004" not in release["accepted_claims"],
        )
    else:
        checks.check(
            "accepted release contains the new claim and dependency closure",
            {"C-MIX-001", "C-MIX-004"} <= set(release["accepted_claims"]),
        )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
