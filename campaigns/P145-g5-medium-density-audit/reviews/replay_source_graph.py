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
    SourceNode("G5", "merged-framework/bridges/phase-5/bridge_G5_Geff_medium_density.py", "38a28bb452b055e7aa7894e1c31e3fcc98bfc5c6a8cbee2040aa003c62a4071a", 15, "primary"),
    SourceNode("G1", "merged-framework/bridges/phase-5/bridge_G1_radiating_dilaton_source.py", "580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876", 10, "qualified_dependency"),
    SourceNode("G2", "merged-framework/bridges/phase-5/bridge_G2_gordon_metric_3plus1.py", "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88", 6, "qualified_dependency"),
    SourceNode("G3", "merged-framework/bridges/phase-5/bridge_G3_horndeski_scalar_tensor.py", "8d462ce2bfd57bfced9fdedd511e9d2711e0c2454bc0d0441c681288495719ba", 11, "qualified_dependency"),
    SourceNode("G4", "merged-framework/bridges/phase-5/bridge_G4_radiation_reaction_self_force.py", "308c8d82aff062fb0f0254498fb2bdb19fe6bdc207036cb0fa73643d3608c799", 10, "qualified_dependency"),
    SourceNode("W5", "merged-framework/bridges/phase-6/bridge_W5_chiral_asymmetry_magnitude.py", "5afea85e0e70236ddd076e2da585d6ab5861d52211239642eac1c951f1c6a71a", 27, "pending_consumer"),
    SourceNode("QCD1", "merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py", "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed", 11, "pending_consumer"),
    SourceNode("SM1", "merged-framework/bridges/phase-9/bridge_SM1_combined_gauge_group.py", "bb7b70bc2ac0dd703f95ccbbaf843d40e78279f357795b9be74d6eee484749f2", 6, "pending_consumer"),
    SourceNode("OD", "merged-framework/bridges/phase-19/bridge_OD_over_determination_test.py", "300259218ca36063625d42487dc1d8f00def4b5d58ef6ffc0b4dc174852fdeb6", 8, "qualified_consumer"),
    SourceNode("AS1", "merged-framework/bridges/phase-21/bridge_AS1_two_length_transmutation.py", "baca25e9b2b999088c1dc2969f9979cd341c582b3bdcfd009432db0eae9ea6cf", 10, "qualified_consumer"),
    SourceNode("AS2", "merged-framework/bridges/phase-21/bridge_AS2_medium_constants_reduce.py", "48ad6312d70248f2fda1cc935a09a567267a78a9494a62cb18312cf79412a631", 8, "qualified_consumer"),
    SourceNode("AS3", "merged-framework/bridges/phase-21/bridge_AS3_sakharov_kappa_reduce.py", "f88cc85a3fb64d1b8aabdf53ced29168d78fce9470e586dc19564288a120903b", 8, "qualified_consumer"),
    SourceNode("AS4", "merged-framework/bridges/phase-21/bridge_AS4_over_determination_v2.py", "cdcfea3ac26c932a3db792c864baa026c761555d3c0e34c7b1bc025ea962745f", 7, "duplicate_consumer"),
    SourceNode("OD3", "merged-framework/bridges/phase-22/bridge_OD3_beta_pinned.py", "af96fa76a30c9ebb863e0a50b605ade5003a7595f28188ce7ca4d0884d67910c", 8, "duplicate_consumer"),
)

EXPECTED_COMPATIBILITY = {
    "G1": (2, 0, 0, 0, 0),
    "G4": (1, 0, 0, 0, 0),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    root = Path(source_root)
    checks = CheckLedger("P145-G5-SOURCE-GRAPH")
    observed_predicates = 0
    observed_compatibility: dict[str, tuple[int, int, int, int, int]] = {}

    checks.check("fourteen frozen dependency and consumer nodes", len(NODES) == 14)
    checks.check(
        "frozen authority classes are complete",
        {
            role: sum(node.role == role for node in NODES)
            for role in {node.role for node in NODES}
        }
        == {
            "primary": 1,
            "qualified_dependency": 4,
            "pending_consumer": 3,
            "qualified_consumer": 4,
            "duplicate_consumer": 2,
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

    checks.check(
        "frozen graph inventories 145 source predicates",
        observed_predicates == 145,
    )
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
