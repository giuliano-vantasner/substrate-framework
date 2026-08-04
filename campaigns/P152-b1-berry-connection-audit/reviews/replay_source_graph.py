#!/usr/bin/env python3
"""Hash, predicate, and compatibility replay for B1's semantic consumers."""

from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


NODES = {
    "B1": ("root", "merged-framework/bridges/phase-7/bridge_B1_disclination_berry_connection.py", "2de4faa60ecc1f87ca356afd55c2a531a89327c3c46e4296176052113de7b0b6", 8, 1),
    "C1": ("pending_consumer", "merged-framework/bridges/phase-7/bridge_C1_Aeff_optical_metric_coupling.py", "6c0b625cbfd8396104f185e4e3785956f66989a10d9fddf9d553fe433c39f0f5", 9, 1),
    "NA1": ("pending_consumer", "merged-framework/bridges/phase-7/bridge_NA1_su2L_wilson_loop.py", "c36b2eeace179a95b44400ea42b74f6263671fd4b4a8441fc682c480bc9372c8", 5, 1),
    "O1": ("pending_consumer", "merged-framework/bridges/phase-7/bridge_O1_spin1_bec_rp2.py", "270877b5ae3507ba5000643333a06269dce2c6a2ec7dbd9ae86f8e2b6e77ef64", 7, 1),
    "OM1": ("qualified_consumer", "merged-framework/bridges/phase-19/bridge_OM1_single_minus_one_identity.py", "c5af6786d4873675ddb552c4a0ae222e4ee3ab7472b74844b28dc4d257358007", 5, 1),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    checks = CheckLedger("P152-B1-SOURCE-GRAPH")
    root = Path(source_root)
    checks.check("five frozen semantic graph nodes", len(NODES) == 5)
    total_predicates = 0
    total_assertions = 0
    legacy_shapes: dict[str, int] = {}
    eager_shapes: dict[str, int] = {}
    source_texts: dict[str, str] = {}
    for name, (_, relative, digest, expected_checks, expected_assertions) in NODES.items():
        path = root / relative
        source = path.read_text(encoding="utf-8")
        source_texts[name] = source
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
            legacy_shapes[name] = compatibility.legacy_references
        if compatibility.eager_legacy_default_fallbacks:
            eager_shapes[name] = compatibility.eager_legacy_default_fallbacks
        total_predicates += predicate_count
        total_assertions += assertion_count

    checks.check("semantic graph inventories 34 source predicates", total_predicates == 34)
    checks.check("semantic graph inventories five assertions", total_assertions == 5)
    checks.check(
        "only immutable B1 has a legacy integration reference",
        legacy_shapes == {"B1": 1},
    )
    checks.check(
        "only immutable B1 has the eager legacy fallback",
        eager_shapes == {"B1": 1},
    )
    checks.check(
        "pending consumers gain no authority",
        {name for name, entry in NODES.items() if entry[0] == "pending_consumer"}
        == {"C1", "NA1", "O1"},
    )
    checks.check(
        "C1 imports B1 as a declared local symbol",
        'A_eff = sp.symbols("A_eff", real=True)' in source_texts["C1"]
        and "from B1 (= 1/2)" in source_texts["C1"],
    )
    checks.check(
        "NA1 cites B1 only as a sibling thread",
        source_texts["NA1"].count("B1") == 1
        and "Sibling thread: B1" in source_texts["NA1"],
    )
    checks.check(
        "O1 cites B1 as a sibling and repeats a fixed-ray phase construction",
        source_texts["O1"].count("B1") == 1
        and "Sibling thread: B1" in source_texts["O1"]
        and "psi_chi = sp.exp(I * chi / 2) * (R_spin1(2, chi) * psi_polar_ref)"
        in source_texts["O1"],
    )
    checks.check(
        "OM1 reconstructs B1's bare integral rather than an endpoint-corrected invariant",
        "B1 exp(i*oint A_eff)" in source_texts["OM1"]
        and "def berry_holonomy" in source_texts["OM1"],
    )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
