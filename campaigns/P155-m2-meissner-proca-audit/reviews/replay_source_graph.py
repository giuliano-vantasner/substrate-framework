#!/usr/bin/env python3
"""Freeze M2's declared graph and semantic consumers without rerunning it."""

from __future__ import annotations

import argparse
import ast
import hashlib
import re
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


NODES = {
    "M2": ("root", "merged-framework/bridges/phase-7/bridge_M2_meissner_proca_W_mass.py", "4ae3e5cb06e7c0bce6387ac7b84f555de65f12cce4be42d620405bb2b5c5b59f", 7, 1),
    "C1": ("qualified_inventory_false_dependency", "merged-framework/bridges/phase-7/bridge_C1_Aeff_optical_metric_coupling.py", "6c0b625cbfd8396104f185e4e3785956f66989a10d9fddf9d553fe433c39f0f5", 9, 1),
    "EM5": ("qualified_rejected_template_dependency", "merged-framework/bridges/phase-3/bridge_EM5_induced_gauge_sector.py", "bcf2c49e1e98eefea98be0076afd29341ce80fd71a7b141618978139982e4ec0", 11, 1),
    "EM6": ("qualified_rejected_ontology_dependency", "merged-framework/bridges/phase-3/bridge_EM6_derived_profile_stability.py", "926df2dc5014042472b3d47576af06676eb654d9da4634f147c7044d4e91f897", 11, 2),
    "M1": ("qualified_coefficient_dependency", "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9, 1),
    "W2": ("qualified_inventory_false_dependency_and_narrative_consumer", "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9, 1),
    "W5": ("qualified_narrative_consumer", "merged-framework/bridges/phase-6/bridge_W5_chiral_asymmetry_magnitude.py", "5afea85e0e70236ddd076e2da585d6ab5861d52211239642eac1c951f1c6a71a", 27, 1),
    "W7": ("qualified_residual_dependency_and_narrative_consumer", "merged-framework/bridges/phase-6/bridge_W7_su2L_gauging_charged_current.py", "1a1fa278f6b8a0cab74d020fc01db1fa3576f57084d0cd80959867c591bf66c3", 11, 1),
    "YM1": ("pending_kinetic_consumer", "merged-framework/bridges/phase-7/bridge_YM1_yang_mills_induction.py", "bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6", 9, 1),
    "CF1": ("qualified_Abelian_Higgs_analogy_consumer", "merged-framework/bridges/phase-10/bridge_CF1_dual_superconductor_flux_tube.py", "a4ec97923804f1b7c624b7619bc6b6a1cbb62f42d659897799545b257ca33f5d", 8, 2),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    checks = CheckLedger("P155-M2-SOURCE-GRAPH")
    root = Path(source_root)
    checks.check("ten frozen M2 graph nodes", len(NODES) == 10)
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
            predicate_count == expected_checks
            and assertion_count == expected_assertions,
        )
        compatibility = audit_numpy_trapezoid_compatibility(
            source,
            filename=str(path),
        )
        if compatibility.legacy_references:
            legacy_shapes[name] = compatibility.legacy_references
        if compatibility.current_references:
            current_shapes[name] = compatibility.current_references
        total_predicates += predicate_count
        total_assertions += assertion_count

    checks.check("graph inventories 111 source predicates", total_predicates == 111)
    checks.check("graph inventories twelve assertions", total_assertions == 12)
    checks.check(
        "only immutable CF1 has legacy NumPy integration access",
        legacy_shapes == {"CF1": 3} and current_shapes == {},
    )
    checks.check(
        "YM1 is the only pending nonroot node",
        {
            name
            for name, entry in NODES.items()
            if entry[0].startswith("pending_")
        }
        == {"YM1"},
    )
    checks.check(
        "C1 queue edge is an integration-constant token false positive",
        "C1 e^{-M_W x}" in texts["M2"]
        and "bridge_C1" not in texts["M2"]
        and "optical" not in texts["M2"].lower(),
    )
    checks.check(
        "W2 queue edge is absent from M2's actual source body",
        re.search(r"\bW2\b", texts["M2"]) is None
        and "M_W2" in texts["M2"]
        and "M1 (Anderson-Higgs mass matrix) and M2 (Meissner-Proca)"
        in texts["W2"],
    )
    checks.check(
        "M2 directly imports only M1's conditional charged coefficient",
        "M_W2 = g**2 * v**2 / 4" in texts["M2"]
        and "IMPORTED from M1" in texts["M2"],
    )
    checks.check(
        "EM5 and EM6 are physical overread dependencies rather than authority",
        "M2 is EM5 with e^2/pi -> g^2 v^2/4" in texts["M2"]
        and "EM6: the order parameter's complex/U(1)" in texts["M2"],
    )
    checks.check(
        "W7 residual reference cannot supply the missing action",
        "Phase-6 residual W7" in texts["M2"]
        and "The W/Z masses follow from phase-7's M1 and M2" in texts["W7"],
    )
    checks.check(
        "W5's forward supersession narrative is scientifically independent",
        "reason is SUPERSEDED by W7 in this same phase + phase-7 M1/M2"
        in texts["W5"],
    )
    checks.check(
        "pending YM1 claims an unauthorized kinetic completion",
        "After YM1, M1/M2" in texts["YM1"]
        and "imported kinetic term -- the kinetic term they mass-gap"
        in texts["YM1"],
    )
    checks.check(
        "CF1's accepted model declares its own functional",
        "FUNCTIONAL (DECLARED" in texts["CF1"]
        and "dualizes M2's London" in texts["CF1"],
    )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
