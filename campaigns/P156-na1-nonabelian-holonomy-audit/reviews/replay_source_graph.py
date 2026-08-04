#!/usr/bin/env python3
"""Replay the frozen NA1 source, dependency, and consumer graph."""

from __future__ import annotations

import ast
import hashlib
import re
import sys
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


NODES = {
    "T1Z2": (
        "merged-framework/bridges/phase-1/bridge_T1Z2_same_minus_one.py",
        "d9c08f9440fb79b9ef445ad77aff113db6c7c7f8943c5838180fb5704fd71bed",
        10,
        1,
    ),
    "W2": (
        "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py",
        "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16",
        9,
        1,
    ),
    "W7": (
        "merged-framework/bridges/phase-6/bridge_W7_su2L_gauging_charged_current.py",
        "1a1fa278f6b8a0cab74d020fc01db1fa3576f57084d0cd80959867c591bf66c3",
        11,
        1,
    ),
    "B1": (
        "merged-framework/bridges/phase-7/bridge_B1_disclination_berry_connection.py",
        "2de4faa60ecc1f87ca356afd55c2a531a89327c3c46e4296176052113de7b0b6",
        8,
        1,
    ),
    "NA1": (
        "merged-framework/bridges/phase-7/bridge_NA1_su2L_wilson_loop.py",
        "c36b2eeace179a95b44400ea42b74f6263671fd4b4a8441fc682c480bc9372c8",
        5,
        1,
    ),
    "O1": (
        "merged-framework/bridges/phase-7/bridge_O1_spin1_bec_rp2.py",
        "270877b5ae3507ba5000643333a06269dce2c6a2ec7dbd9ae86f8e2b6e77ef64",
        7,
        1,
    ),
    "CF3": (
        "merged-framework/bridges/phase-10/bridge_CF3_wilson_area_law.py",
        "8655579ef3173730c315d60aa821f7085cc131920ae49cb93c60b075d884889d",
        6,
        1,
    ),
    "OM1": (
        "merged-framework/bridges/phase-19/bridge_OM1_single_minus_one_identity.py",
        "c5af6786d4873675ddb552c4a0ae222e4ee3ab7472b74844b28dc4d257358007",
        5,
        1,
    ),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _shape(text: str, filename: str) -> tuple[int, int]:
    tree = ast.parse(text, filename=filename)
    checks = sum(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
        for node in ast.walk(tree)
    )
    assertions = sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
    return checks, assertions


def run(source_root: Path) -> int:
    checks = CheckLedger("P156-NA1-SOURCE-GRAPH")
    texts: dict[str, str] = {}
    compatibility = {}

    checks.check("eight frozen NA1 graph nodes", len(NODES) == 8)
    for name, (relative, expected_hash, expected_checks, expected_assertions) in NODES.items():
        path = source_root / relative
        text = path.read_text(encoding="utf-8")
        texts[name] = text
        compatibility[name] = audit_numpy_trapezoid_compatibility(
            text,
            filename=str(path),
        )
        checks.check(f"{name} pinned source hash", _sha256(path) == expected_hash)
        checks.check(
            f"{name} frozen predicate and assertion inventory",
            _shape(text, str(path)) == (expected_checks, expected_assertions),
        )

    checks.check(
        "graph inventories 61 source predicates",
        sum(node[2] for node in NODES.values()) == 61,
    )
    checks.check(
        "graph inventories eight assertions",
        sum(node[3] for node in NODES.values()) == 8,
    )
    checks.check(
        "only immutable B1 has executable legacy integration access",
        compatibility["B1"].legacy_references == 1
        and compatibility["B1"].current_references == 1
        and all(
            report.legacy_references == 0
            for name, report in compatibility.items()
            if name != "B1"
        ),
    )
    checks.check(
        "NA1 actually imports W7 and transitively names W2",
        "IMPORTED from W7" in texts["NA1"]
        and "IMPORTED there from W2" in texts["NA1"],
    )
    checks.check(
        "T1Z2 is a scalar-value reference rather than matrix transport authority",
        "T1-Z2" in texts["NA1"]
        and "wilson_eig = sp.Integer(-1)" in texts["NA1"],
    )
    checks.check(
        "B1 and O1 are only named as sibling threads by NA1",
        "Sibling thread: B1" in texts["NA1"]
        and "O1 (RP^2 from the spin-1 BEC)" in texts["NA1"],
    )
    checks.check(
        "W4 queue edge is a variable-token false positive",
        re.search(r"\bW4\b", texts["NA1"]) is None
        and "W_4pi" in texts["NA1"],
    )
    checks.check(
        "pending O1 uses NA1 only in a same-value sibling sentence",
        "NA1" in texts["O1"]
        and "same Z_2 read by the SU(2)_L Wilson loop" in texts["O1"],
    )
    checks.check(
        "qualified CF3 is a later center and expectation-law analogy",
        "Extend NA1" in texts["CF3"]
        and "area-law" in texts["CF3"].lower(),
    )
    checks.check(
        "qualified OM1 explicitly says NA1 set equality is insufficient",
        "assertion (NA1.5) does NOT capture this" in texts["OM1"]
        and "bare 'all == -1' assertion" in texts["OM1"],
    )
    checks.check(
        "source graph supplies no physical weak action or AB observable",
        "the Wilson-loop formalism" in texts["NA1"]
        and "NA1 EVALUATES it" in texts["NA1"]
        and "DECLARED" in texts["NA1"],
    )
    return checks.finish()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: replay_source_graph.py source_root")
    tally = run(Path(sys.argv[1]))
    print(f"P156 SOURCE GRAPH ALL {tally} CHECKS PASS")
