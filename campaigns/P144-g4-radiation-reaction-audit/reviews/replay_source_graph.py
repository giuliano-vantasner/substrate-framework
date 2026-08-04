from __future__ import annotations

import argparse
import ast
import hashlib
from dataclasses import dataclass
from pathlib import Path

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class SourceNode:
    unit: str
    path: str
    sha256: str
    static_checks: int
    role: str


NODES = (
    SourceNode("G4", "merged-framework/bridges/phase-5/bridge_G4_radiation_reaction_self_force.py", "308c8d82aff062fb0f0254498fb2bdb19fe6bdc207036cb0fa73643d3608c799", 10, "primary"),
    SourceNode("G1", "merged-framework/bridges/phase-5/bridge_G1_radiating_dilaton_source.py", "580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876", 10, "qualified_dependency"),
    SourceNode("G2", "merged-framework/bridges/phase-5/bridge_G2_gordon_metric_3plus1.py", "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88", 6, "qualified_dependency"),
    SourceNode("G3", "merged-framework/bridges/phase-5/bridge_G3_horndeski_scalar_tensor.py", "8d462ce2bfd57bfced9fdedd511e9d2711e0c2454bc0d0441c681288495719ba", 11, "qualified_dependency_and_consumer"),
    SourceNode("T2A", "merged-framework/bridges/phase-2/bridge_T2A_moving_source.py", "669803de1403c8ca66e399aa4b7c0e762447e40df7c241fe530a6b4e06dde70a", 12, "qualified_dependency"),
    SourceNode("T2C", "merged-framework/bridges/phase-2/bridge_T2C_tidal_MP.py", "651fd75287dd25b5c34208ea5789df89be50f5050ec139ae2d99f4962440c369", 13, "qualified_dependency"),
    SourceNode("FS4", "merged-framework/bridges/phase-13/bridge_FS4_formfactor_into_radiation.py", "2f3c1b02bbad06bded6a38d0e1c203b2ba9c71c63adea34645d041b820feb129", 5, "duplicate_consumer"),
    SourceNode("G5", "merged-framework/bridges/phase-5/bridge_G5_Geff_medium_density.py", "38a28bb452b055e7aa7894e1c31e3fcc98bfc5c6a8cbee2040aa003c62a4071a", 15, "pending_consumer"),
    SourceNode("QCD1", "merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py", "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed", 11, "pending_consumer"),
    SourceNode("SM1", "merged-framework/bridges/phase-9/bridge_SM1_combined_gauge_group.py", "bb7b70bc2ac0dd703f95ccbbaf843d40e78279f357795b9be74d6eee484749f2", 6, "pending_consumer"),
)


EXPECTED_COMPATIBILITY = {
    "G1": (2, 0, 0, 0, 0),
    "G4": (1, 0, 0, 0, 0),
    "FS4": (1, 0, 0, 1, 0),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    root = Path(source_root)
    checks = CheckLedger("P144-G4-SOURCE-GRAPH")
    observed_predicates = 0
    observed_compatibility: dict[str, tuple[int, int, int, int, int]] = {}

    checks.check("ten frozen dependency and reverse-consumer nodes", len(NODES) == 10)
    checks.check(
        "frozen authority classes are complete",
        {
            role: sum(node.role == role for node in NODES)
            for role in {node.role for node in NODES}
        }
        == {
            "primary": 1,
            "qualified_dependency": 4,
            "qualified_dependency_and_consumer": 1,
            "duplicate_consumer": 1,
            "pending_consumer": 3,
        },
    )

    for node in NODES:
        path = root / node.path
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
        static_checks = sum(
            isinstance(item, ast.Call)
            and isinstance(item.func, ast.Name)
            and item.func.id == "check"
            for item in ast.walk(tree)
        )
        observed_predicates += static_checks
        checks.check(f"{node.unit} pinned source hash", _sha256(path) == node.sha256)
        checks.check(
            f"{node.unit} frozen predicate inventory",
            static_checks == node.static_checks,
        )
        compatibility = audit_numpy_trapezoid_compatibility(
            text,
            filename=str(path),
        )
        shape = (
            compatibility.direct_legacy_attributes,
            compatibility.dynamic_legacy_getattrs,
            compatibility.imported_legacy_names,
            compatibility.current_references,
            compatibility.eager_legacy_default_fallbacks,
        )
        if any(shape):
            observed_compatibility[node.unit] = shape

    checks.check("frozen graph inventories 99 source predicates", observed_predicates == 99)
    checks.check(
        "immutable compatibility shapes are exhaustively classified",
        observed_compatibility == EXPECTED_COMPATIBILITY,
    )
    for unit, expected in EXPECTED_COMPATIBILITY.items():
        checks.check(
            f"{unit} retains exact compatibility shape",
            observed_compatibility[unit] == expected,
        )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
