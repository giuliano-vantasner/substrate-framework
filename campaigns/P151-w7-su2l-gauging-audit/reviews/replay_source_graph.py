#!/usr/bin/env python3
"""Hash and predicate replay for W7's dependency and consumer graph."""

from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


NODES = {
    "W7": ("root", "merged-framework/bridges/phase-6/bridge_W7_su2L_gauging_charged_current.py", "1a1fa278f6b8a0cab74d020fc01db1fa3576f57084d0cd80959867c591bf66c3", 11, 1),
    "EM2": ("qualified_dependency", "merged-framework/bridges/phase-3/bridge_EM2_gauge_u1_minimal_coupling.py", "9787ae25521e19d926de0f9addafd16353bebc149cea83f3d9dd4c491fef91d6", 11, 1),
    "EM3": ("qualified_dependency", "merged-framework/bridges/phase-3/bridge_EM3_maxwell_coulomb_tail.py", "1c674bae211322b24a4504ff5aafc04424eb6a4bfe7813f63e5ec4337f783fc9", 11, 1),
    "EM5": ("qualified_dependency", "merged-framework/bridges/phase-3/bridge_EM5_induced_gauge_sector.py", "bcf2c49e1e98eefea98be0076afd29341ce80fd71a7b141618978139982e4ec0", 11, 1),
    "G1": ("qualified_dependency", "merged-framework/bridges/phase-5/bridge_G1_radiating_dilaton_source.py", "580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876", 10, 1),
    "W1": ("qualified_dependency", "merged-framework/bridges/phase-6/bridge_W1_parity_odd_chiral_coupling.py", "bfac7d7e4ccb0cdabc6bb2703dadb650c0e09ea883ec3ff70f039231d3e62388", 8, 2),
    "W2": ("qualified_dependency_and_consumer", "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9, 1),
    "W3": ("qualified_dependency", "merged-framework/bridges/phase-6/bridge_W3_VA_charged_current.py", "b49a0bd1075b16b5906719b6ed51454ed04adab5168be7ec98178599313b3f17", 7, 1),
    "W5": ("qualified_dependency_and_consumer", "merged-framework/bridges/phase-6/bridge_W5_chiral_asymmetry_magnitude.py", "5afea85e0e70236ddd076e2da585d6ab5861d52211239642eac1c951f1c6a71a", 27, 1),
    "M1": ("pending_dependency_and_consumer", "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9, 1),
    "M2": ("pending_dependency_and_consumer", "merged-framework/bridges/phase-7/bridge_M2_meissner_proca_W_mass.py", "4ae3e5cb06e7c0bce6387ac7b84f555de65f12cce4be42d620405bb2b5c5b59f", 7, 1),
    "NA1": ("pending_consumer", "merged-framework/bridges/phase-7/bridge_NA1_su2L_wilson_loop.py", "c36b2eeace179a95b44400ea42b74f6263671fd4b4a8441fc682c480bc9372c8", 5, 1),
    "YM1": ("pending_dependency_and_consumer", "merged-framework/bridges/phase-7/bridge_YM1_yang_mills_induction.py", "bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6", 9, 1),
    "FG3": ("qualified_consumer", "merged-framework/bridges/phase-11/bridge_FG3_flavor_mixing_matrix.py", "5030cf63716914a0effe2d89de2510c14a1c081784ffa2abfd73d24d982ea7cb", 6, 1),
    "FG4": ("qualified_consumer", "merged-framework/bridges/phase-11/bridge_FG4_cp_kobayashi_maskawa.py", "d9ebb32d440fb87540c7cb2d02a846b76dd4ee405288895308561762cd720ceb", 7, 1),
    "NC1": ("qualified_consumer", "merged-framework/bridges/phase-15/bridge_NC1_nonlinear_chiral_current.py", "b7206df001095b2706818ea5f3ffde13d24887816d867f7252da460588b010f5", 8, 1),
    "NC2": ("qualified_consumer", "merged-framework/bridges/phase-15/bridge_NC2_chiral_stress_tensor.py", "6854fafe62ef7c8bfcf558573e3c89fec0d2144cb9a39df2e2ecb6d66d960136", 7, 1),
    "OM1": ("qualified_consumer", "merged-framework/bridges/phase-19/bridge_OM1_single_minus_one_identity.py", "c5af6786d4873675ddb552c4a0ae222e4ee3ab7472b74844b28dc4d257358007", 5, 1),
}

DECLARED_DEPENDENCIES = ("EM2", "EM3", "EM5", "G1", "M1", "M2", "W1", "W2", "W3", "W5", "YM1")
REVERSE_CONSUMERS = ("W2", "W5", "M1", "M2", "NA1", "YM1", "FG3", "FG4", "NC1", "NC2", "OM1")
COMPATIBILITY_SHAPES = {"G1": 2, "W1": 2, "W3": 2}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    checks = CheckLedger("P151-W7-SOURCE-GRAPH")
    root = Path(source_root)
    checks.check("eighteen frozen dependency and consumer nodes", len(NODES) == 18)
    total_checks = 0
    total_assertions = 0
    actual_shapes: dict[str, int] = {}
    for name, (_, relative, digest, expected_checks, expected_assertions) in NODES.items():
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
        total_checks += predicate_count
        total_assertions += assertion_count
        compatibility = audit_numpy_trapezoid_compatibility(source, filename=str(path))
        if compatibility.legacy_references:
            actual_shapes[name] = compatibility.legacy_references
        checks.check(
            f"{name} has no eager legacy fallback",
            compatibility.eager_legacy_default_fallbacks == 0,
        )

    checks.check("frozen graph inventories 168 source checks", total_checks == 168)
    checks.check("frozen graph inventories nineteen assertions", total_assertions == 19)
    checks.check(
        "immutable compatibility shapes are exhaustively classified",
        actual_shapes == COMPATIBILITY_SHAPES,
    )
    checks.check(
        "W7 declared dependency set is frozen",
        DECLARED_DEPENDENCIES
        == ("EM2", "EM3", "EM5", "G1", "M1", "M2", "W1", "W2", "W3", "W5", "YM1"),
    )
    checks.check(
        "W7 reverse consumers are frozen",
        REVERSE_CONSUMERS
        == ("W2", "W5", "M1", "M2", "NA1", "YM1", "FG3", "FG4", "NC1", "NC2", "OM1"),
    )
    checks.check(
        "pending nodes gain no authority",
        {name for name, entry in NODES.items() if entry[0].startswith("pending")}
        == {"M1", "M2", "NA1", "YM1"},
    )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
