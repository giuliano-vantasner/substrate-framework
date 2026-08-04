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
    SourceNode("S3", "merged-framework/bridges/phase-4/bridge_S3_su3_wzw_baryon_reps.py", "44d8cd1f3a3b3d0a316d0984db92d5e47e13cac9dcf3d476e2d996bf09f13b9a", 10, "primary"),
    SourceNode("S2", "merged-framework/bridges/phase-4/bridge_S2_meson_hedgehog_spectrum.py", "48a9eadf6fbc1e3ebe7fcd6b98c2d60cc10a3f5282404c84e4626910f296eaf7", 10, "qualified"),
    SourceNode("S4", "merged-framework/bridges/phase-4/bridge_S4_c4_vector_meson_closure.py", "49c7b2392bbe23d2824f4f73030ccd30f245e1750e0c7736dc420d3f64d7a780", 11, "pending"),
    SourceNode("S5", "merged-framework/bridges/phase-4/bridge_S5_realizability_magnitude.py", "b92a9db67940169fcd9919f83fda6ae8c56b9b9e40b0d2cbebef5539a5dccde6", 28, "qualified"),
    SourceNode("WZ1", "merged-framework/bridges/phase-17/bridge_WZ1_wzw_5d_chern_simons.py", "87bab354a83a6edd05ed77ed0778e1cdf11cf402f92414664f7a3196df0551b9", 12, "qualified"),
    SourceNode("WZ4", "merged-framework/bridges/phase-17/bridge_WZ4_hls_vector_meson_anomalous.py", "fca6b9c1d95bdf49e99b863470c7e800880e493b3f716159aa2341f8cf963d2b", 9, "qualified"),
    SourceNode("W2", "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9, "pending"),
    SourceNode("QCD1", "merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py", "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed", 11, "pending"),
    SourceNode("WZ2", "merged-framework/bridges/phase-17/bridge_WZ2_level_quantization_pi5.py", "f991e222f038268077d3f50e759beeec95ac65f06a8369011ecc0e0ad79ce3ff", 8, "qualified"),
    SourceNode("WZ3", "merged-framework/bridges/phase-17/bridge_WZ3_goldstone_wilczek_baryon_current.py", "30da2ac41a0d46c48bd4e1b9733c3712d0b6c1c9b4838f1a1df3c4db22cc3569", 7, "qualified"),
    SourceNode("AS8", "merged-framework/bridges/phase-22/bridge_AS8_superborn_quantum_face_of_granularity.py", "47fda3732d8901b6949b2859952123be675eef2bb28bad0ac0d241948fe3ea73", 5, "qualified"),
    SourceNode("WM2", "merged-framework/bridges/phase-23/bridge_WM2_common_induction_normalization.py", "3c656894fc782dd40dcb495a91de5bbf5a46ec378bb3593eb30d7d4b387f34a3", 10, "duplicate"),
    SourceNode("PN6", "merged-framework/bridges/phase-30/bridge_PN6_general_L_lossless_null.py", "50ebbf97568fef13e69fc926db3e57457aba4685f3140ac8786bed525e71289f", 30, "qualified"),
    SourceNode("WM7", "merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py", "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361", 10, "pending"),
    SourceNode("WM8", "merged-framework/bridges/phase-39/bridge_WM8_corrected_boundary_running.py", "741497f63cc39ee96c71e9a999c49ef9e821cf612d8b48b2959d05f9e6940518", 10, "pending"),
    SourceNode("MK1", "merged-framework/bridges/phase-43/bridge_MK1_mu_from_medium_cosine.py", "98ff5459ae3c6cb64a9a7632fbaa8613f1f5b1adb68419de25ffa06b1c3a3222", 7, "pending"),
    SourceNode("MR2", "merged-framework/bridges/phase-44/bridge_MR2_bps_normalization_pi_squared.py", "2e62ce2d6cbee805a988046a27a742e622931291e8e013a9aede6ce16e48e990", 8, "pending"),
)


EXPECTED_COMPATIBILITY = {
    "S2": (3, 0, 0, 0, 0),
    "WZ3": (1, 0, 0, 0, 0),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    root = Path(source_root)
    checks = CheckLedger("P139-S3-SOURCE-GRAPH")
    observed_predicates = 0
    observed_compatibility: dict[str, tuple[int, int, int, int, int]] = {}

    checks.check("seventeen frozen dependency and reverse-consumer nodes", len(NODES) == 17)
    checks.check(
        "frozen authority classes are complete",
        {role: sum(node.role == role for node in NODES) for role in {node.role for node in NODES}}
        == {"primary": 1, "qualified": 8, "pending": 7, "duplicate": 1},
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

    checks.check("frozen graph inventories 195 source predicates", observed_predicates == 195)
    checks.check(
        "immutable compatibility shapes are exhaustively classified",
        observed_compatibility == EXPECTED_COMPATIBILITY,
    )
    checks.check(
        "S2 and WZ3 retain their classified alias-only replay paths",
        observed_compatibility["S2"] == (3, 0, 0, 0, 0)
        and observed_compatibility["WZ3"] == (1, 0, 0, 0, 0),
    )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
