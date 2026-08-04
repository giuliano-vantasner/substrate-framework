#!/usr/bin/env python3
"""Freeze M1's semantic source consumers without ceremonial execution."""

from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


NODES = {
    "M1": ("root", "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9, 1),
    "M2": ("pending_direct_consumer", "merged-framework/bridges/phase-7/bridge_M2_meissner_proca_W_mass.py", "4ae3e5cb06e7c0bce6387ac7b84f555de65f12cce4be42d620405bb2b5c5b59f", 7, 1),
    "SM2": ("pending_semantic_consumer", "merged-framework/bridges/phase-9/bridge_SM2_generation_hypercharge_charges.py", "cc5532e86128f010f6801dada96ae1ece5a6be845817127d69cf72810b9e33f1", 7, 1),
    "CF1": ("qualified_declared_scale_reference", "merged-framework/bridges/phase-10/bridge_CF1_dual_superconductor_flux_tube.py", "a4ec97923804f1b7c624b7619bc6b6a1cbb62f42d659897799545b257ca33f5d", 8, 2),
    "FG3": ("qualified_unauthorized_template_reference", "merged-framework/bridges/phase-11/bridge_FG3_flavor_mixing_matrix.py", "5030cf63716914a0effe2d89de2510c14a1c081784ffa2abfd73d24d982ea7cb", 6, 1),
    "WM1": ("qualified_narrative_context", "merged-framework/bridges/phase-23/bridge_WM1_sin2thetaw_trace_ratio.py", "75dc34e168c39cd0af0a21cd4c7d039088ac74baefb6615ece98f5069f5b8953", 9, 1),
    "WM9": ("pending_unauthorized_condensate_consumer", "merged-framework/bridges/phase-39/bridge_WM9_scalar_multiplicity_from_condensate.py", "d0d94417f5abd572e2e306c1f33dc264d42cfef94e4281dbc258ea9fa83ffd4d", 8, 1),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    checks = CheckLedger("P154-M1-SOURCE-GRAPH")
    root = Path(source_root)
    checks.check("seven frozen M1 semantic graph nodes", len(NODES) == 7)
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

    checks.check("semantic graph inventories 54 source predicates", total_predicates == 54)
    checks.check("semantic graph inventories eight assertions", total_assertions == 8)
    checks.check(
        "only immutable CF1 has legacy NumPy integration access",
        legacy_shapes == {"CF1": 3} and current_shapes == {},
    )
    checks.check(
        "pending semantic consumers gain no authority",
        {
            name
            for name, entry in NODES.items()
            if entry[0].startswith("pending_")
        }
        == {"M2", "SM2", "WM9"},
    )
    checks.check(
        "qualified references retain independent accepted closures",
        {
            name
            for name, entry in NODES.items()
            if entry[0].startswith("qualified_")
        }
        == {"CF1", "FG3", "WM1"},
    )
    checks.check(
        "M2 directly imports only the conditional charged coefficient",
        "M_W2 = g**2 * v**2 / 4" in texts["M2"]
        and "IMPORTED from M1" in texts["M2"],
    )
    checks.check(
        "SM2 uses M1 only for a declared hypercharge convention",
        "Y_PS = Y_M1 / 2" in texts["SM2"]
        and "Q = T3 + Y/2" in texts["SM2"],
    )
    checks.check(
        "CF1 treats v as declared model input in its accepted closure",
        "v = condensate VEV [M1]" in texts["CF1"]
        and "DECLARED -- the cylindrical ansatz" in texts["CF1"],
    )
    checks.check(
        "FG3 imports an unauthorized fermion condensate template",
        "family mass = y v/sqrt(2)" in texts["FG3"]
        and "M1 is the GAUGE-boson matrix" in texts["FG3"],
    )
    checks.check(
        "WM1 exact trace computation is independent of M1 mass algebra",
        "M1 DECLARED sin^2 theta_W" in texts["WM1"]
        and "Tr(T_3^2)/Tr(Q^2)" in texts["WM1"],
    )
    checks.check(
        "WM9 imports the rejected condensate-promotion premise",
        "M1 forms the electroweak Higgs by PROMOTING" in texts["WM9"]
        and "N_H = 1 from EM6/M1" in texts["WM9"],
    )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
