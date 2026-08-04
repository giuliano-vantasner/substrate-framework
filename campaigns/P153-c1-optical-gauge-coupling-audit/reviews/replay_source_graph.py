#!/usr/bin/env python3
"""Replay C1 and classify the queue's reverse ``C1`` token hits."""

from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


NODES = {
    "C1": ("root", "merged-framework/bridges/phase-7/bridge_C1_Aeff_optical_metric_coupling.py", "6c0b625cbfd8396104f185e4e3785956f66989a10d9fddf9d553fe433c39f0f5", 9, 1),
    "P3D1": ("qualified_false_positive", "merged-framework/bridges/phase-14/bridge_P3D1_radial_pulson_exists.py", "f93b8dabfca0c49fb0bf1101c926e79c43dc2e9ebb35882083611a12ca9514fa", 6, 1),
    "LB4": ("qualified_false_positive", "merged-framework/bridges/phase-26/bridge_LB4_thermal_decoherence_gwindow.py", "e33361e6985002e76342203716fd00ca72c22f905590825a6c064fe472b0d103", 40, 0),
    "GK3D2": ("pending_false_positive", "merged-framework/bridges/phase-41/bridge_GK3D2_induced_kinetic_normalization.py", "856096aba38812dc17fb07ce5cf7c0fa13eb2623665ccf871810734ac3ca0886", 17, 1),
    "EL4": ("qualified_false_positive", "merged-framework/bridges/phase-46/bridge_EL4_me_in_the_frontier_form.py", "4ae8185505b11d3cf2beffcbb6ec786e4bfbdd57e00cd42b8fc223a28a17cf2f", 10, 1),
    "G2": ("qualified_false_positive", "merged-framework/bridges/phase-5/bridge_G2_gordon_metric_3plus1.py", "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88", 6, 1),
    "M2": ("pending_false_positive", "merged-framework/bridges/phase-7/bridge_M2_meissner_proca_W_mass.py", "4ae3e5cb06e7c0bce6387ac7b84f555de65f12cce4be42d620405bb2b5c5b59f", 7, 1),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    checks = CheckLedger("P153-C1-SOURCE-GRAPH")
    root = Path(source_root)
    checks.check("seven frozen C1 graph nodes", len(NODES) == 7)
    total_predicates = 0
    total_assertions = 0
    legacy_shapes: dict[str, int] = {}
    current_shapes: dict[str, int] = {}
    texts: dict[str, str] = {}
    for name, (_, relative, digest, expected_checks, expected_assertions) in NODES.items():
        path = root / relative
        source = path.read_text(encoding="utf-8")
        texts[name] = source
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
        if compatibility.current_references:
            current_shapes[name] = compatibility.current_references
        total_predicates += predicate_count
        total_assertions += assertion_count

    checks.check("semantic graph inventories 95 source predicates", total_predicates == 95)
    checks.check("semantic graph inventories six assertions", total_assertions == 6)
    checks.check(
        "only immutable P3D1 has a legacy integration reference",
        legacy_shapes == {"P3D1": 1},
    )
    checks.check(
        "P3D1 also contains the current integration API",
        current_shapes == {"P3D1": 1},
    )
    checks.check(
        "qualified reverse hits retain their existing accepted closures",
        {
            name
            for name, entry in NODES.items()
            if entry[0] == "qualified_false_positive"
        }
        == {"P3D1", "LB4", "EL4", "G2"},
    )
    checks.check(
        "pending reverse hits gain no authority",
        {name for name, entry in NODES.items() if entry[0] == "pending_false_positive"}
        == {"GK3D2", "M2"},
    )
    checks.check(
        "P3D1 C1 token is a coarse-resolution result variable",
        'C1 = evolve(A=3.0' in texts["P3D1"]
        and 'tc = C1["t"]' in texts["P3D1"],
    )
    checks.check(
        "LB4 C1 token is a rung-local check label",
        "equipartition, rung096 C1" in texts["LB4"],
    )
    checks.check(
        "GK3D2 C1 token is a SymPy integration constant",
        'C1 = sp.Symbol("C1")' in texts["GK3D2"]
        and "const_val = sp.solve" in texts["GK3D2"],
    )
    checks.check(
        "EL4 C1 token is a solved RGE integration constant",
        "C1 = sp.solve" in texts["EL4"]
        and 'sp.Symbol("C1")' in texts["EL4"],
    )
    checks.check(
        "G2 C1 token is a polynomial coefficient variable",
        "B1 = rem1.coeff(NTT, 1); C1 = rem1.coeff(NTT, 0)" in texts["G2"],
    )
    checks.check(
        "M2 C1 token is the conventional dsolve integration constant",
        "general solution C1 e^{-M_W x} + C2 e^{+M_W x}" in texts["M2"],
    )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
