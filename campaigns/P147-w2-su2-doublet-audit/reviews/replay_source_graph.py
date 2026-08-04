#!/usr/bin/env python3
"""Hash and predicate replay for W2's frozen dependency/consumer graph."""

from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


NODES = {
    "W2": ("root", "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9, 1, 0, 0),
    "EM1": ("dependency", "merged-framework/bridges/phase-3/bridge_EM1_u1_noether_charge.py", "2f5c6e0236748bc6f3a8ce4a77bd18dc26b3cef235038d57bc71310361ea4850", 16, 1, 0, 0),
    "EM2": ("dependency", "merged-framework/bridges/phase-3/bridge_EM2_gauge_u1_minimal_coupling.py", "9787ae25521e19d926de0f9addafd16353bebc149cea83f3d9dd4c491fef91d6", 11, 1, 0, 0),
    "EM3": ("dependency", "merged-framework/bridges/phase-3/bridge_EM3_maxwell_coulomb_tail.py", "1c674bae211322b24a4504ff5aafc04424eb6a4bfe7813f63e5ec4337f783fc9", 11, 1, 0, 0),
    "M1": ("dependency_consumer", "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9, 1, 0, 0),
    "M2": ("dependency_consumer", "merged-framework/bridges/phase-7/bridge_M2_meissner_proca_W_mass.py", "4ae3e5cb06e7c0bce6387ac7b84f555de65f12cce4be42d620405bb2b5c5b59f", 7, 1, 0, 0),
    "S3": ("dependency", "merged-framework/bridges/phase-4/bridge_S3_su3_wzw_baryon_reps.py", "44d8cd1f3a3b3d0a316d0984db92d5e47e13cac9dcf3d476e2d996bf09f13b9a", 10, 2, 0, 0),
    "SM2": ("dependency_consumer", "merged-framework/bridges/phase-9/bridge_SM2_generation_hypercharge_charges.py", "cc5532e86128f010f6801dada96ae1ece5a6be845817127d69cf72810b9e33f1", 7, 1, 0, 0),
    "W1": ("dependency", "merged-framework/bridges/phase-6/bridge_W1_parity_odd_chiral_coupling.py", "bfac7d7e4ccb0cdabc6bb2703dadb650c0e09ea883ec3ff70f039231d3e62388", 8, 2, 2, 0),
    "W3": ("dependency_consumer", "merged-framework/bridges/phase-6/bridge_W3_VA_charged_current.py", "b49a0bd1075b16b5906719b6ed51454ed04adab5168be7ec98178599313b3f17", 7, 1, 2, 0),
    "W7": ("dependency_consumer", "merged-framework/bridges/phase-6/bridge_W7_su2L_gauging_charged_current.py", "1a1fa278f6b8a0cab74d020fc01db1fa3576f57084d0cd80959867c591bf66c3", 11, 1, 0, 0),
    "WM1": ("dependency_consumer", "merged-framework/bridges/phase-23/bridge_WM1_sin2thetaw_trace_ratio.py", "75dc34e168c39cd0af0a21cd4c7d039088ac74baefb6615ece98f5069f5b8953", 9, 1, 0, 0),
    "WM3": ("dependency", "merged-framework/bridges/phase-23/bridge_WM3_sin2thetaw_rg_running.py", "2328ae4d6e66e1caa14a39042c362e57258406383f14ecaa5f5f6c468105e298", 10, 1, 0, 0),
    "YM1": ("dependency_consumer", "merged-framework/bridges/phase-7/bridge_YM1_yang_mills_induction.py", "bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6", 9, 1, 0, 0),
    "W5": ("consumer", "merged-framework/bridges/phase-6/bridge_W5_chiral_asymmetry_magnitude.py", "5afea85e0e70236ddd076e2da585d6ab5861d52211239642eac1c951f1c6a71a", 27, 1, 0, 0),
    "NA1": ("consumer", "merged-framework/bridges/phase-7/bridge_NA1_su2L_wilson_loop.py", "c36b2eeace179a95b44400ea42b74f6263671fd4b4a8441fc682c480bc9372c8", 5, 1, 0, 0),
    "YM2": ("consumer", "merged-framework/bridges/phase-7/bridge_YM2_yang_mills_3plus1_lift.py", "19c8708ea9b81eff719362ee713dd3d933b5422788759ae6e8933c705863b11c", 10, 1, 1, 1),
    "SM1": ("consumer", "merged-framework/bridges/phase-9/bridge_SM1_combined_gauge_group.py", "bb7b70bc2ac0dd703f95ccbbaf843d40e78279f357795b9be74d6eee484749f2", 6, 1, 0, 0),
    "SM3": ("consumer", "merged-framework/bridges/phase-9/bridge_SM3_anomaly_cancellation.py", "3ace90aa5377050e4dcab5778996079eea92c9cc56a53c276a60a5508f63b529", 8, 1, 0, 0),
    "FG3": ("consumer", "merged-framework/bridges/phase-11/bridge_FG3_flavor_mixing_matrix.py", "5030cf63716914a0effe2d89de2510c14a1c081784ffa2abfd73d24d982ea7cb", 6, 1, 0, 0),
    "FG4": ("consumer", "merged-framework/bridges/phase-11/bridge_FG4_cp_kobayashi_maskawa.py", "d9ebb32d440fb87540c7cb2d02a846b76dd4ee405288895308561762cd720ceb", 7, 1, 0, 0),
    "WM2": ("consumer", "merged-framework/bridges/phase-23/bridge_WM2_common_induction_normalization.py", "3c656894fc782dd40dcb495a91de5bbf5a46ec378bb3593eb30d7d4b387f34a3", 10, 1, 0, 0),
    "GK1": ("consumer", "merged-framework/bridges/phase-35/bridge_GK1_gauge_kinetic_dimensionality_boundary.py", "c142538897e9168769483aeb978ea86587fa9a073e606aa204316238dfa24d74", 11, 1, 0, 0),
    "WM7": ("consumer", "merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py", "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361", 10, 1, 0, 0),
}

DEPENDENCIES = ("EM1", "EM2", "EM3", "M1", "M2", "S3", "SM2", "W1", "W3", "W7", "WM1", "WM3", "YM1")
REVERSE_CONSUMERS = ("W3", "W5", "W7", "M1", "M2", "NA1", "YM1", "YM2", "SM1", "SM2", "SM3", "FG3", "FG4", "WM1", "WM2", "GK1", "WM7")
QUALIFIED = {"EM1", "EM2", "EM3", "S3", "W1", "WM1", "WM3", "FG3", "FG4"}
PENDING = {"M1", "M2", "SM2", "W2", "W3", "W5", "W7", "NA1", "YM1", "YM2", "SM1", "SM3", "GK1", "WM7"}
DUPLICATE = {"WM2"}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    checks = CheckLedger("P147-W2-SOURCE-GRAPH")
    root = Path(source_root)
    checks.check("twenty-four frozen graph nodes", len(NODES) == 24)
    checks.check(
        "frozen authority classes partition the graph",
        QUALIFIED | PENDING | DUPLICATE == set(NODES)
        and not (QUALIFIED & PENDING)
        and not (QUALIFIED & DUPLICATE)
        and not (PENDING & DUPLICATE),
    )
    total_checks = 0
    total_assertions = 0
    compatibility_shapes: dict[str, tuple[int, int]] = {}
    for name, (_, relative, digest, expected_checks, expected_assertions, expected_legacy, expected_eager) in NODES.items():
        path = root / relative
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        predicate_count = sum(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            for node in ast.walk(tree)
        )
        assertion_count = sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
        checks.check(f"{name} pinned source hash", _sha256(path) == digest)
        checks.check(
            f"{name} frozen predicate and assertion inventory",
            predicate_count == expected_checks and assertion_count == expected_assertions,
        )
        compatibility = audit_numpy_trapezoid_compatibility(source, filename=str(path))
        if compatibility.legacy_references:
            compatibility_shapes[name] = (
                compatibility.legacy_references,
                compatibility.eager_legacy_default_fallbacks,
            )
        checks.check(
            f"{name} frozen compatibility shape",
            compatibility.legacy_references == expected_legacy
            and compatibility.eager_legacy_default_fallbacks == expected_eager,
        )
        total_checks += predicate_count
        total_assertions += assertion_count

    checks.check("frozen graph inventories 234 source predicates", total_checks == 234)
    checks.check("frozen graph inventories 26 assertions", total_assertions == 26)
    checks.check(
        "immutable compatibility shapes are exhaustive",
        compatibility_shapes == {"W1": (2, 0), "W3": (2, 0), "YM2": (1, 1)},
    )
    checks.check("thirteen declared dependencies are frozen", len(DEPENDENCIES) == 13)
    checks.check("seventeen reverse consumers are frozen", len(REVERSE_CONSUMERS) == 17)
    checks.check(
        "dependency-consumer overlap is exact",
        set(DEPENDENCIES) & set(REVERSE_CONSUMERS)
        == {"M1", "M2", "SM2", "W3", "W7", "WM1", "YM1"},
    )
    checks.check(
        "qualified nodes remain separate accepted surfaces",
        QUALIFIED == {"EM1", "EM2", "EM3", "S3", "W1", "WM1", "WM3", "FG3", "FG4"},
    )
    checks.check(
        "pending nodes gain no authority",
        len(PENDING) == 14 and "W2" in PENDING,
    )
    checks.check("WM2 remains duplicate evidence", DUPLICATE == {"WM2"})
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
