#!/usr/bin/env python3
"""Hash and predicate replay for W3's frozen dependency/consumer graph."""

from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


NODES = {
    "W3": ("root", "merged-framework/bridges/phase-6/bridge_W3_VA_charged_current.py", "b49a0bd1075b16b5906719b6ed51454ed04adab5168be7ec98178599313b3f17", 7, 1, 2, 0),
    "EM1": ("dependency", "merged-framework/bridges/phase-3/bridge_EM1_u1_noether_charge.py", "2f5c6e0236748bc6f3a8ce4a77bd18dc26b3cef235038d57bc71310361ea4850", 16, 1, 0, 0),
    "G1": ("dependency", "merged-framework/bridges/phase-5/bridge_G1_radiating_dilaton_source.py", "580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876", 10, 1, 2, 0),
    "G2": ("dependency", "merged-framework/bridges/phase-5/bridge_G2_gordon_metric_3plus1.py", "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88", 6, 1, 0, 0),
    "NC4": ("dependency", "merged-framework/bridges/phase-15/bridge_NC4_pde_robustness.py", "9efa788da093213f354cbd9e26b7bd0be81129d6f966128b5c0fd10fe0081570", 15, 0, 1, 0),
    "W1": ("dependency", "merged-framework/bridges/phase-6/bridge_W1_parity_odd_chiral_coupling.py", "bfac7d7e4ccb0cdabc6bb2703dadb650c0e09ea883ec3ff70f039231d3e62388", 8, 2, 2, 0),
    "W2": ("dependency_consumer", "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9, 1, 0, 0),
    "W5": ("dependency_consumer", "merged-framework/bridges/phase-6/bridge_W5_chiral_asymmetry_magnitude.py", "5afea85e0e70236ddd076e2da585d6ab5861d52211239642eac1c951f1c6a71a", 27, 1, 0, 0),
    "NC1": ("dependency_consumer", "merged-framework/bridges/phase-15/bridge_NC1_nonlinear_chiral_current.py", "b7206df001095b2706818ea5f3ffde13d24887816d867f7252da460588b010f5", 8, 1, 0, 0),
    "W4": ("consumer", "merged-framework/bridges/phase-6/bridge_W4_neutrino_missing_energy.py", "afa341c860ba89889d8d0a9fe6cd62948b5303f243e3884abf7d3acf24a7f602", 8, 1, 0, 0),
    "W7": ("consumer", "merged-framework/bridges/phase-6/bridge_W7_su2L_gauging_charged_current.py", "1a1fa278f6b8a0cab74d020fc01db1fa3576f57084d0cd80959867c591bf66c3", 11, 1, 0, 0),
    "M1": ("consumer", "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9, 1, 0, 0),
    "FG3": ("consumer", "merged-framework/bridges/phase-11/bridge_FG3_flavor_mixing_matrix.py", "5030cf63716914a0effe2d89de2510c14a1c081784ffa2abfd73d24d982ea7cb", 6, 1, 0, 0),
    "FG4": ("consumer", "merged-framework/bridges/phase-11/bridge_FG4_cp_kobayashi_maskawa.py", "d9ebb32d440fb87540c7cb2d02a846b76dd4ee405288895308561762cd720ceb", 7, 1, 0, 0),
    "NC3": ("consumer", "merged-framework/bridges/phase-15/bridge_NC3_nonlinear_rectification.py", "dceed4b3d8f59daa75bbd6b31e9a726de99f180e252accb19f7d0ae625c5c9bd", 18, 0, 0, 0),
    "AS6": ("consumer", "merged-framework/bridges/phase-22/bridge_AS6_beta_self_dual_pin.py", "2f6c76d8aedde25b343f85cb54b2618cd03c816a29553fa70a523909265dd7f0", 9, 1, 0, 0),
    "WM7": ("consumer", "merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py", "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361", 10, 1, 0, 0),
}

DEPENDENCIES = ("EM1", "G1", "G2", "NC1", "NC4", "W1", "W2", "W5")
REVERSE_CONSUMERS = ("W2", "W4", "W5", "W7", "M1", "FG3", "FG4", "NC1", "NC3", "AS6", "WM7")
QUALIFIED = {"EM1", "G1", "G2", "NC1", "NC4", "W1", "W2", "FG3", "FG4", "NC3", "AS6"}
PENDING = {"W3", "W4", "W5", "W7", "M1", "WM7"}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    checks = CheckLedger("P148-W3-SOURCE-GRAPH")
    root = Path(source_root)
    checks.check("seventeen frozen graph nodes", len(NODES) == 17)
    checks.check(
        "frozen authority classes partition the graph",
        QUALIFIED | PENDING == set(NODES) and not (QUALIFIED & PENDING),
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

    checks.check("frozen graph inventories 184 source predicates", total_checks == 184)
    checks.check("frozen graph inventories 16 assertions", total_assertions == 16)
    checks.check(
        "immutable compatibility shapes are exhaustive",
        compatibility_shapes == {
            "G1": (2, 0),
            "W1": (2, 0),
            "W3": (2, 0),
            "NC4": (1, 0),
        },
    )
    checks.check("eight declared dependencies are frozen", len(DEPENDENCIES) == 8)
    checks.check("eleven reverse consumers are frozen", len(REVERSE_CONSUMERS) == 11)
    checks.check(
        "dependency-consumer overlap is exact",
        set(DEPENDENCIES) & set(REVERSE_CONSUMERS) == {"W2", "W5", "NC1"},
    )
    checks.check(
        "qualified nodes remain separate accepted surfaces",
        len(QUALIFIED) == 11 and "W3" not in QUALIFIED,
    )
    checks.check(
        "pending nodes gain no authority",
        PENDING == {"W3", "W4", "W5", "W7", "M1", "WM7"},
    )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
