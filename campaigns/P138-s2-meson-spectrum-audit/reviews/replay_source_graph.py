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
    SourceNode("S2", "merged-framework/bridges/phase-4/bridge_S2_meson_hedgehog_spectrum.py", "48a9eadf6fbc1e3ebe7fcd6b98c2d60cc10a3f5282404c84e4626910f296eaf7", 10, "primary"),
    SourceNode("B1", "merged-framework/bridges/phase-7/bridge_B1_disclination_berry_connection.py", "2de4faa60ecc1f87ca356afd55c2a531a89327c3c46e4296176052113de7b0b6", 8, "pending"),
    SourceNode("T1Z2", "merged-framework/bridges/phase-1/bridge_T1Z2_same_minus_one.py", "d9c08f9440fb79b9ef445ad77aff113db6c7c7f8943c5838180fb5704fd71bed", 10, "qualified"),
    SourceNode("S3", "merged-framework/bridges/phase-4/bridge_S3_su3_wzw_baryon_reps.py", "44d8cd1f3a3b3d0a316d0984db92d5e47e13cac9dcf3d476e2d996bf09f13b9a", 10, "pending"),
    SourceNode("O1", "merged-framework/bridges/phase-7/bridge_O1_spin1_bec_rp2.py", "270877b5ae3507ba5000643333a06269dce2c6a2ec7dbd9ae86f8e2b6e77ef64", 7, "pending"),
    SourceNode("FG2", "merged-framework/bridges/phase-11/bridge_FG2_family_tower.py", "aef0ed225fca1f12fcccb284015d97ce3faa25291f07addda24e82ebbc5ae166", 7, "qualified"),
    SourceNode("FG4", "merged-framework/bridges/phase-11/bridge_FG4_cp_kobayashi_maskawa.py", "d9ebb32d440fb87540c7cb2d02a846b76dd4ee405288895308561762cd720ceb", 7, "qualified"),
    SourceNode("P3D2", "merged-framework/bridges/phase-14/bridge_P3D2_spherical_quadrupole_null.py", "72802a3bb3ed46be3bf7b96e035028b0ded352ae02e587cb14b9db902b2125cb", 4, "qualified"),
    SourceNode("WZ3", "merged-framework/bridges/phase-17/bridge_WZ3_goldstone_wilczek_baryon_current.py", "30da2ac41a0d46c48bd4e1b9733c3712d0b6c1c9b4838f1a1df3c4db22cc3569", 7, "qualified"),
    SourceNode("PG1", "merged-framework/bridges/phase-18/bridge_PG1_pion_goldstone_massless.py", "a51ecc1833cd166bbef5aa799d2ab9eacc453b088660dbb98426591a7157aa74", 4, "qualified"),
    SourceNode("PG2", "merged-framework/bridges/phase-18/bridge_PG2_gmor_pion_mass.py", "0502a53f65d3bd11a3f17d26d55ed7d67a1e0f61d194b38cd41728873c4a06ad", 4, "qualified"),
    SourceNode("PG3", "merged-framework/bridges/phase-18/bridge_PG3_roper_radial_excitation.py", "4e3b56ab04977d254a291dd56d28e3285d72e86b3d640e0cfc322d5818cf007f", 8, "qualified"),
    SourceNode("PG4", "merged-framework/bridges/phase-18/bridge_PG4_goldberger_treiman.py", "e13e68536d14bedb1c8fa7ec10110172d0a1b73e08ce365863013dc7db66f1e9", 4, "qualified"),
    SourceNode("WM2", "merged-framework/bridges/phase-23/bridge_WM2_common_induction_normalization.py", "3c656894fc782dd40dcb495a91de5bbf5a46ec378bb3593eb30d7d4b387f34a3", 10, "duplicate"),
    SourceNode("NY1", "merged-framework/bridges/phase-24/bridge_NY1_skyrme_energy_unit.py", "b3531d7f906fe396a1326d44d68f34d09ae34988e86a8f721c360040c4aa0921", 9, "duplicate"),
    SourceNode("E1", "merged-framework/bridges/phase-29/bridge_E1_rational_map_integrals.py", "1afa9ba8ade88912e7361bbbd6f59a9fce5cc114c75ddf604a6439bc066ae2d1", 6, "qualified"),
    SourceNode("E2", "merged-framework/bridges/phase-29/bridge_E2_multi_skyrmion_solutions.py", "fdde30878eaf1f8dff7fce9c2d9d4234d1d6e14566be6d2ee56dd1926481c46f", 6, "qualified"),
    SourceNode("PN6", "merged-framework/bridges/phase-30/bridge_PN6_general_L_lossless_null.py", "50ebbf97568fef13e69fc926db3e57457aba4685f3140ac8786bed525e71289f", 30, "qualified"),
    SourceNode("WM7", "merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py", "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361", 10, "pending"),
    SourceNode("WM8", "merged-framework/bridges/phase-39/bridge_WM8_corrected_boundary_running.py", "741497f63cc39ee96c71e9a999c49ef9e821cf612d8b48b2959d05f9e6940518", 10, "pending"),
)

EXPECTED_COMPATIBILITY = {
    "S2": (3, 0, 0, 0, 0),
    "B1": (0, 1, 0, 1, 1),
    "P3D2": (1, 0, 0, 1, 0),
    "WZ3": (1, 0, 0, 0, 0),
    "PG3": (1, 0, 0, 1, 0),
    "E1": (1, 0, 0, 1, 0),
    "E2": (1, 0, 0, 1, 0),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    root = Path(source_root)
    checks = CheckLedger("P138-S2-SOURCE-GRAPH")
    observed_predicates = 0
    observed_compatibility: dict[str, tuple[int, int, int, int, int]] = {}

    checks.check("twenty frozen dependency and reverse-consumer nodes", len(NODES) == 20)
    checks.check(
        "frozen authority classes are complete",
        {role: sum(node.role == role for node in NODES) for role in {node.role for node in NODES}}
        == {"primary": 1, "pending": 5, "qualified": 12, "duplicate": 2},
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

    checks.check("frozen graph inventories 171 source predicates", observed_predicates == 171)
    checks.check(
        "immutable compatibility shapes are exhaustively classified",
        observed_compatibility == EXPECTED_COMPATIBILITY,
    )
    checks.check(
        "S2 requires alias-only replay backed by the current implementation",
        observed_compatibility["S2"] == (3, 0, 0, 0, 0),
    )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
