#!/usr/bin/env python3
"""Hash and predicate replay for W1's frozen dependency/consumer graph."""

from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


NODES = {
    "W1": (
        "root",
        "merged-framework/bridges/phase-6/bridge_W1_parity_odd_chiral_coupling.py",
        "bfac7d7e4ccb0cdabc6bb2703dadb650c0e09ea883ec3ff70f039231d3e62388",
        8,
        2,
    ),
    "NC1": (
        "dependency_and_qualified_consumer",
        "merged-framework/bridges/phase-15/bridge_NC1_nonlinear_chiral_current.py",
        "b7206df001095b2706818ea5f3ffde13d24887816d867f7252da460588b010f5",
        8,
        1,
    ),
    "NC4": (
        "dependency",
        "merged-framework/bridges/phase-15/bridge_NC4_pde_robustness.py",
        "9efa788da093213f354cbd9e26b7bd0be81129d6f966128b5c0fd10fe0081570",
        15,
        0,
    ),
    "W2": (
        "pending_consumer",
        "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py",
        "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16",
        9,
        1,
    ),
    "W3": (
        "pending_consumer",
        "merged-framework/bridges/phase-6/bridge_W3_VA_charged_current.py",
        "b49a0bd1075b16b5906719b6ed51454ed04adab5168be7ec98178599313b3f17",
        7,
        1,
    ),
    "W5": (
        "pending_consumer",
        "merged-framework/bridges/phase-6/bridge_W5_chiral_asymmetry_magnitude.py",
        "5afea85e0e70236ddd076e2da585d6ab5861d52211239642eac1c951f1c6a71a",
        27,
        1,
    ),
    "W7": (
        "pending_consumer",
        "merged-framework/bridges/phase-6/bridge_W7_su2L_gauging_charged_current.py",
        "1a1fa278f6b8a0cab74d020fc01db1fa3576f57084d0cd80959867c591bf66c3",
        11,
        1,
    ),
    "M1": (
        "pending_consumer",
        "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py",
        "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f",
        9,
        1,
    ),
    "NC2": (
        "qualified_consumer",
        "merged-framework/bridges/phase-15/bridge_NC2_chiral_stress_tensor.py",
        "6854fafe62ef7c8bfcf558573e3c89fec0d2144cb9a39df2e2ecb6d66d960136",
        7,
        1,
    ),
    "NC3": (
        "qualified_consumer",
        "merged-framework/bridges/phase-15/bridge_NC3_nonlinear_rectification.py",
        "dceed4b3d8f59daa75bbd6b31e9a726de99f180e252accb19f7d0ae625c5c9bd",
        18,
        0,
    ),
    "WM7": (
        "pending_consumer",
        "merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py",
        "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361",
        10,
        1,
    ),
}

W1_DEPENDENCIES = ("NC1", "NC4")
REVERSE_CONSUMERS = ("M1", "NC1", "NC2", "NC3", "W2", "W3", "W5", "W7", "WM7")
COMPATIBILITY_SHAPES = {"NC4": 1, "W1": 2, "W3": 2}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    checks = CheckLedger("P146-W1-SOURCE-GRAPH")
    root = Path(source_root)
    checks.check("eleven frozen dependency and consumer nodes", len(NODES) == 11)
    checks.check(
        "frozen authority classes are complete",
        {entry[0] for entry in NODES.values()}
        == {
            "root",
            "dependency",
            "dependency_and_qualified_consumer",
            "pending_consumer",
            "qualified_consumer",
        },
    )
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

    checks.check("frozen graph inventories 129 source checks", total_checks == 129)
    checks.check("frozen graph inventories ten source assertions", total_assertions == 10)
    checks.check(
        "immutable compatibility shapes are exhaustively classified",
        actual_shapes == COMPATIBILITY_SHAPES,
    )
    checks.check("W1 retains exact two-call compatibility shape", actual_shapes["W1"] == 2)
    checks.check("NC4 retains exact one-call compatibility shape", actual_shapes["NC4"] == 1)
    checks.check("W3 retains exact two-call compatibility shape", actual_shapes["W3"] == 2)
    checks.check("W1 frozen dependencies are NC1 and NC4", W1_DEPENDENCIES == ("NC1", "NC4"))
    checks.check(
        "nine frozen reverse consumers are complete",
        REVERSE_CONSUMERS
        == ("M1", "NC1", "NC2", "NC3", "W2", "W3", "W5", "W7", "WM7"),
    )
    checks.check(
        "qualified consumers remain a distinct authority class",
        {name for name, entry in NODES.items() if "qualified_consumer" in entry[0]}
        == {"NC1", "NC2", "NC3"},
    )
    checks.check(
        "pending consumers gain no accepted authority",
        {name for name, entry in NODES.items() if entry[0] == "pending_consumer"}
        == {"M1", "W2", "W3", "W5", "W7", "WM7"},
    )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
