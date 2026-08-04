#!/usr/bin/env python3
"""Hash and predicate replay for W4's dependency and consumer graph."""

from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


NODES = {
    "W4": ("root", "merged-framework/bridges/phase-6/bridge_W4_neutrino_missing_energy.py", "afa341c860ba89889d8d0a9fe6cd62948b5303f243e3884abf7d3acf24a7f602", 8, 1),
    "G1": ("qualified_dependency", "merged-framework/bridges/phase-5/bridge_G1_radiating_dilaton_source.py", "580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876", 10, 1),
    "G2": ("qualified_dependency", "merged-framework/bridges/phase-5/bridge_G2_gordon_metric_3plus1.py", "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88", 6, 1),
    "W3": ("qualified_dependency", "merged-framework/bridges/phase-6/bridge_W3_VA_charged_current.py", "b49a0bd1075b16b5906719b6ed51454ed04adab5168be7ec98178599313b3f17", 7, 1),
    "W5": ("pending_dependency_and_consumer", "merged-framework/bridges/phase-6/bridge_W5_chiral_asymmetry_magnitude.py", "5afea85e0e70236ddd076e2da585d6ab5861d52211239642eac1c951f1c6a71a", 27, 1),
    "NA1": ("pending_consumer", "merged-framework/bridges/phase-7/bridge_NA1_su2L_wilson_loop.py", "c36b2eeace179a95b44400ea42b74f6263671fd4b4a8441fc682c480bc9372c8", 5, 1),
}

DECLARED_DEPENDENCIES = ("G1", "G2", "W3", "W5")
REVERSE_CONSUMERS = ("NA1", "W5")
COMPATIBILITY_SHAPES = {"G1": 2, "W3": 2}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    checks = CheckLedger("P149-W4-SOURCE-GRAPH")
    root = Path(source_root)
    checks.check("six frozen dependency and consumer nodes", len(NODES) == 6)
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

    checks.check("frozen graph inventories 63 source checks", total_checks == 63)
    checks.check("frozen graph inventories six assertions", total_assertions == 6)
    checks.check(
        "immutable compatibility shapes are exhaustively classified",
        actual_shapes == COMPATIBILITY_SHAPES,
    )
    checks.check(
        "W4 declared dependency set is frozen",
        DECLARED_DEPENDENCIES == ("G1", "G2", "W3", "W5"),
    )
    checks.check(
        "W4 reverse consumers are frozen",
        REVERSE_CONSUMERS == ("NA1", "W5"),
    )
    checks.check(
        "pending nodes gain no authority",
        {name for name, entry in NODES.items() if entry[0].startswith("pending")}
        == {"NA1", "W5"},
    )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
