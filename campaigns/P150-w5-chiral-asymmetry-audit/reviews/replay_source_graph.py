#!/usr/bin/env python3
"""Hash and predicate replay for W5's dependency and consumer graph."""

from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


NODES = {
    "W5": ("root", "merged-framework/bridges/phase-6/bridge_W5_chiral_asymmetry_magnitude.py", "5afea85e0e70236ddd076e2da585d6ab5861d52211239642eac1c951f1c6a71a", 27, 1),
    "G1": ("qualified_dependency", "merged-framework/bridges/phase-5/bridge_G1_radiating_dilaton_source.py", "580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876", 10, 1),
    "G2": ("qualified_dependency", "merged-framework/bridges/phase-5/bridge_G2_gordon_metric_3plus1.py", "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88", 6, 1),
    "G5": ("qualified_dependency", "merged-framework/bridges/phase-5/bridge_G5_Geff_medium_density.py", "38a28bb452b055e7aa7894e1c31e3fcc98bfc5c6a8cbee2040aa003c62a4071a", 15, 1),
    "S5": ("qualified_dependency", "merged-framework/bridges/phase-4/bridge_S5_realizability_magnitude.py", "b92a9db67940169fcd9919f83fda6ae8c56b9b9e40b0d2cbebef5539a5dccde6", 28, 1),
    "W1": ("qualified_dependency", "merged-framework/bridges/phase-6/bridge_W1_parity_odd_chiral_coupling.py", "bfac7d7e4ccb0cdabc6bb2703dadb650c0e09ea883ec3ff70f039231d3e62388", 8, 2),
    "W2": ("qualified_dependency", "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9, 1),
    "W3": ("qualified_dependency_and_consumer", "merged-framework/bridges/phase-6/bridge_W3_VA_charged_current.py", "b49a0bd1075b16b5906719b6ed51454ed04adab5168be7ec98178599313b3f17", 7, 1),
    "W4": ("qualified_dependency_and_consumer", "merged-framework/bridges/phase-6/bridge_W4_neutrino_missing_energy.py", "afa341c860ba89889d8d0a9fe6cd62948b5303f243e3884abf7d3acf24a7f602", 8, 1),
    "W7": ("pending_dependency_and_consumer", "merged-framework/bridges/phase-6/bridge_W7_su2L_gauging_charged_current.py", "1a1fa278f6b8a0cab74d020fc01db1fa3576f57084d0cd80959867c591bf66c3", 11, 1),
    "M1": ("pending_dependency", "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9, 1),
    "M2": ("pending_dependency", "merged-framework/bridges/phase-7/bridge_M2_meissner_proca_W_mass.py", "4ae3e5cb06e7c0bce6387ac7b84f555de65f12cce4be42d620405bb2b5c5b59f", 7, 1),
    "YM1": ("pending_consumer", "merged-framework/bridges/phase-7/bridge_YM1_yang_mills_induction.py", "bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6", 9, 1),
}

DECLARED_DEPENDENCIES = ("G1", "G2", "G5", "M1", "M2", "S5", "W1", "W2", "W3", "W4", "W7")
REVERSE_CONSUMERS = ("W3", "W4", "W7", "YM1")
COMPATIBILITY_SHAPES = {"G1": 2, "W1": 2, "W3": 2}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    checks = CheckLedger("P150-W5-SOURCE-GRAPH")
    root = Path(source_root)
    checks.check("thirteen frozen dependency and consumer nodes", len(NODES) == 13)
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

    checks.check("frozen graph inventories 154 source checks", total_checks == 154)
    checks.check("frozen graph inventories fourteen assertions", total_assertions == 14)
    checks.check(
        "immutable compatibility shapes are exhaustively classified",
        actual_shapes == COMPATIBILITY_SHAPES,
    )
    checks.check(
        "W5 declared dependency set is frozen",
        DECLARED_DEPENDENCIES
        == ("G1", "G2", "G5", "M1", "M2", "S5", "W1", "W2", "W3", "W4", "W7"),
    )
    checks.check(
        "W5 reverse consumers are frozen",
        REVERSE_CONSUMERS == ("W3", "W4", "W7", "YM1"),
    )
    checks.check(
        "pending nodes gain no authority",
        {name for name, entry in NODES.items() if entry[0].startswith("pending")}
        == {"M1", "M2", "W7", "YM1"},
    )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
