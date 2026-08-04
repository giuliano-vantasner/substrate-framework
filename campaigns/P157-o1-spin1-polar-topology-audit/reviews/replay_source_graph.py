#!/usr/bin/env python3
"""Replay the frozen O1 source, dependency, and consumer graph."""

from __future__ import annotations

import ast
import hashlib
import re
import sys
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


NODES = {
    "T1E": (
        "merged-framework/bridges/phase-1/bridge_T1E_E0_triple_oracle.py",
        "bdd57d929b7bed2436ad5803f0a614d4887a35a7eab5ecd78b23041888e48a97",
        11,
        1,
    ),
    "S2": (
        "merged-framework/bridges/phase-4/bridge_S2_meson_hedgehog_spectrum.py",
        "48a9eadf6fbc1e3ebe7fcd6b98c2d60cc10a3f5282404c84e4626910f296eaf7",
        10,
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
    "CF5": (
        "merged-framework/bridges/phase-10/bridge_CF5_flux_tube_tension_consistency.py",
        "0a449f8b95bc0a83fb0316992fb0d1776a6157e1445029623b4608246dc256f7",
        6,
        2,
    ),
    "ME1": (
        "merged-framework/bridges/phase-20/bridge_ME1_polar_phase_selection.py",
        "54d34a026b45d7ae01b53dae022cbcab61f380f4cda289d6a5862d2cc72adc71",
        4,
        1,
    ),
    "ME2": (
        "merged-framework/bridges/phase-20/bridge_ME2_half_quantum_vortex.py",
        "40eec343312cc85d442471a224c0501071ea556308b517e5c8b1efe067a789e4",
        4,
        1,
    ),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _shape(text: str, filename: str) -> tuple[int, int]:
    tree = ast.parse(text, filename=filename)
    predicates = sum(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
        for node in ast.walk(tree)
    )
    assertions = sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
    return predicates, assertions


def run(source_root: Path) -> int:
    checks = CheckLedger("P157-O1-SOURCE-GRAPH")
    texts: dict[str, str] = {}
    compatibility = {}

    checks.check("eight frozen O1 graph nodes", len(NODES) == 8)
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
        "graph inventories 55 source predicates",
        sum(node[2] for node in NODES.values()) == 55,
    )
    checks.check(
        "graph inventories nine assertions",
        sum(node[3] for node in NODES.values()) == 9,
    )
    checks.check(
        "immutable legacy integration surfaces remain provenance only",
        compatibility["B1"].legacy_references == 1
        and compatibility["B1"].current_references == 1
        and compatibility["S2"].legacy_references == 3
        and compatibility["S2"].current_references == 0
        and compatibility["CF5"].legacy_references == 1
        and compatibility["CF5"].current_references == 0
        and all(
            report.legacy_references == 0
            for name, report in compatibility.items()
            if name not in {"B1", "S2", "CF5"}
        ),
    )
    checks.check(
        "O1 names B1 and NA1 only as same-value siblings",
        "Sibling thread: B1" in texts["O1"]
        and "NA1" in texts["O1"]
        and "same Z_2" in texts["O1"],
    )
    checks.check(
        "ME1 is a later source consumer of O1 spin-one representatives",
        "O1" in texts["ME1"]
        and "psi_polar = sp.Matrix([0, 1, 0])" in texts["ME1"]
        and "Fmats = [Fx, Fy, Fz]" in texts["ME1"]
        and "c2" in texts["ME1"],
    )
    checks.check(
        "ME2 is a later narrative consumer of O1 topology and Berry claims",
        "O1.2" in texts["ME2"]
        and "O1.3" in texts["ME2"]
        and "half-quantum" in texts["ME2"].lower(),
    )
    checks.check(
        "T1E queue edge is unrelated oracle-one language",
        re.search(r"\bO1\b", texts["T1E"]) is not None
        and "oracle" in texts["T1E"].lower()
        and "spin1" not in texts["T1E"].lower(),
    )
    checks.check(
        "CF5 queue edge is only asymptotic order-one notation",
        "O(1)" in texts["CF5"]
        and "spin-1" not in texts["CF5"].lower(),
    )
    checks.check(
        "S2 queue edge has no O1 source dependency",
        re.search(r"\bO1\b", texts["S2"]) is None
        and "Bridge S2" in texts["S2"]
        and "S^2" in texts["O1"],
    )
    checks.check(
        "source graph supplies no physical spinor-BEC closure",
        "H-BEC condensate microscopically SELECTS" in texts["O1"]
        and "F=1 HYPERFINE MANIFOLD genuinely does remain" in texts["O1"]
        and "NOT claimed" in texts["O1"],
    )
    return checks.finish()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: replay_source_graph.py source_root")
    tally = run(Path(sys.argv[1]))
    print(f"P157 SOURCE GRAPH ALL {tally} CHECKS PASS")
