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
    SourceNode("G3", "merged-framework/bridges/phase-5/bridge_G3_horndeski_scalar_tensor.py", "8d462ce2bfd57bfced9fdedd511e9d2711e0c2454bc0d0441c681288495719ba", 11, "primary"),
    SourceNode("G2", "merged-framework/bridges/phase-5/bridge_G2_gordon_metric_3plus1.py", "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88", 6, "qualified_dependency"),
    SourceNode("G4", "merged-framework/bridges/phase-5/bridge_G4_radiation_reaction_self_force.py", "308c8d82aff062fb0f0254498fb2bdb19fe6bdc207036cb0fa73643d3608c799", 10, "pending_dependency_consumer"),
    SourceNode("T1E", "merged-framework/bridges/phase-1/bridge_T1E_E0_triple_oracle.py", "bdd57d929b7bed2436ad5803f0a614d4887a35a7eab5ecd78b23041888e48a97", 11, "qualified_consumer"),
    SourceNode("NC4", "merged-framework/bridges/phase-15/bridge_NC4_pde_robustness.py", "9efa788da093213f354cbd9e26b7bd0be81129d6f966128b5c0fd10fe0081570", 15, "qualified_consumer"),
    SourceNode("WZ4", "merged-framework/bridges/phase-17/bridge_WZ4_hls_vector_meson_anomalous.py", "fca6b9c1d95bdf49e99b863470c7e800880e493b3f716159aa2341f8cf963d2b", 9, "qualified_consumer"),
    SourceNode("OD", "merged-framework/bridges/phase-19/bridge_OD_over_determination_test.py", "300259218ca36063625d42487dc1d8f00def4b5d58ef6ffc0b4dc174852fdeb6", 8, "qualified_consumer"),
    SourceNode("EM3", "merged-framework/bridges/phase-3/bridge_EM3_maxwell_coulomb_tail.py", "1c674bae211322b24a4504ff5aafc04424eb6a4bfe7813f63e5ec4337f783fc9", 11, "qualified_consumer"),
    SourceNode("G1", "merged-framework/bridges/phase-5/bridge_G1_radiating_dilaton_source.py", "580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876", 10, "qualified_consumer"),
    SourceNode("SC1", "merged-framework/bridges/phase-36/bridge_SC1_gordon_coupled_overdetermined.py", "70799bff934f1f6986545a0bde0cb94fe016dd4b468b36614ac3e5d9bb74aec0", 5, "pending_consumer"),
    SourceNode("SC2", "merged-framework/bridges/phase-36/bridge_SC2_horndeski_selfconsistent_solve.py", "64dfc9c31edd8368cb0e2359ca646fc8f62fe306d6af7a326ff8934070b96425", 7, "pending_consumer"),
    SourceNode("G5", "merged-framework/bridges/phase-5/bridge_G5_Geff_medium_density.py", "38a28bb452b055e7aa7894e1c31e3fcc98bfc5c6a8cbee2040aa003c62a4071a", 15, "pending_consumer"),
    SourceNode("QCD1", "merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py", "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed", 11, "pending_consumer"),
    SourceNode("SM1", "merged-framework/bridges/phase-9/bridge_SM1_combined_gauge_group.py", "bb7b70bc2ac0dd703f95ccbbaf843d40e78279f357795b9be74d6eee484749f2", 6, "pending_consumer"),
)


EXPECTED_COMPATIBILITY = {
    "G4": (1, 0, 0, 0, 0),
    "NC4": (1, 0, 0, 0, 0),
    "G1": (2, 0, 0, 0, 0),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    root = Path(source_root)
    checks = CheckLedger("P143-G3-SOURCE-GRAPH")
    observed_predicates = 0
    observed_compatibility: dict[str, tuple[int, int, int, int, int]] = {}

    checks.check("fourteen frozen dependency and reverse-consumer nodes", len(NODES) == 14)
    checks.check(
        "frozen authority classes are complete",
        {
            role: sum(node.role == role for node in NODES)
            for role in {node.role for node in NODES}
        }
        == {
            "primary": 1,
            "qualified_dependency": 1,
            "pending_dependency_consumer": 1,
            "qualified_consumer": 6,
            "pending_consumer": 5,
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
        checks.check(f"{node.unit} frozen predicate inventory", static_checks == node.static_checks)
        compatibility = audit_numpy_trapezoid_compatibility(text, filename=str(path))
        shape = (
            compatibility.direct_legacy_attributes,
            compatibility.dynamic_legacy_getattrs,
            compatibility.imported_legacy_names,
            compatibility.current_references,
            compatibility.eager_legacy_default_fallbacks,
        )
        if any(shape[index] for index in (0, 1, 2, 4)):
            observed_compatibility[node.unit] = shape

    checks.check("frozen graph inventories 135 source predicates", observed_predicates == 135)
    checks.check(
        "immutable compatibility shapes are exhaustively classified",
        observed_compatibility == EXPECTED_COMPATIBILITY,
    )
    for unit, expected in EXPECTED_COMPATIBILITY.items():
        checks.check(
            f"{unit} retains exact alias-only compatibility shape",
            observed_compatibility[unit] == expected,
        )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
