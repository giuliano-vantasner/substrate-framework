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
    SourceNode("S4", "merged-framework/bridges/phase-4/bridge_S4_c4_vector_meson_closure.py", "49c7b2392bbe23d2824f4f73030ccd30f245e1750e0c7736dc420d3f64d7a780", 11, "primary"),
    SourceNode("B1", "merged-framework/bridges/phase-7/bridge_B1_disclination_berry_connection.py", "2de4faa60ecc1f87ca356afd55c2a531a89327c3c46e4296176052113de7b0b6", 8, "pending_dependency"),
    SourceNode("S3", "merged-framework/bridges/phase-4/bridge_S3_su3_wzw_baryon_reps.py", "44d8cd1f3a3b3d0a316d0984db92d5e47e13cac9dcf3d476e2d996bf09f13b9a", 10, "qualified_consumer"),
    SourceNode("WZ1", "merged-framework/bridges/phase-17/bridge_WZ1_wzw_5d_chern_simons.py", "87bab354a83a6edd05ed77ed0778e1cdf11cf402f92414664f7a3196df0551b9", 12, "qualified_consumer"),
    SourceNode("WZ4", "merged-framework/bridges/phase-17/bridge_WZ4_hls_vector_meson_anomalous.py", "fca6b9c1d95bdf49e99b863470c7e800880e493b3f716159aa2341f8cf963d2b", 9, "qualified_consumer"),
    SourceNode("PN6", "merged-framework/bridges/phase-30/bridge_PN6_general_L_lossless_null.py", "50ebbf97568fef13e69fc926db3e57457aba4685f3140ac8786bed525e71289f", 30, "qualified_consumer"),
    SourceNode("KI1", "merged-framework/bridges/phase-34/bridge_KI1_exhaustive_coupling_search.py", "a1ec5f8e64e56165d2c51ad2389ecb455870572ba4ef9eca292151bde4ddb42b", 5, "pending_consumer"),
    SourceNode("KI2", "merged-framework/bridges/phase-34/bridge_KI2_epsilon_underdetermination.py", "9e16fc6fafa940f43d559ea0f6a9c2730940d1247f36f655375c2f75f6fd1e81", 6, "pending_consumer"),
    SourceNode("MK2", "merged-framework/bridges/phase-43/bridge_MK2_lambda_from_medium_omega.py", "351136bca28e413ddd54f1b15bf7084dffe32af565fc87e7220d1437a525eb07", 7, "pending_consumer"),
    SourceNode("MR3", "merged-framework/bridges/phase-44/bridge_MR3_no_double_counting.py", "c5eaabaeede15909adb5d9ddb951353c376aaa381e669e35c6256d7015e7eddc", 6, "pending_consumer"),
    SourceNode("MR4", "merged-framework/bridges/phase-44/bridge_MR4_e_from_rho_saturation.py", "cefe7192b935ec18992e9cd76fd348ef81934ed9d20843ced3627973cec9d3d7", 7, "pending_consumer"),
    SourceNode("MR5", "merged-framework/bridges/phase-44/bridge_MR5_solve_at_derived_e.py", "0da10adafe3badb7f3eab225543bc601996df45b142f2d59b5d0ddd6dd9117d7", 6, "pending_consumer"),
    SourceNode("MR6", "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py", "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d", 6, "pending_consumer"),
)


EXPECTED_COMPATIBILITY = {
    "B1": (0, 1, 0, 1, 1),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_root: str) -> int:
    root = Path(source_root)
    checks = CheckLedger("P140-S4-SOURCE-GRAPH")
    observed_predicates = 0
    observed_compatibility: dict[str, tuple[int, int, int, int, int]] = {}

    checks.check("thirteen frozen dependency and reverse-consumer nodes", len(NODES) == 13)
    checks.check(
        "frozen authority classes are complete",
        {
            role: sum(node.role == role for node in NODES)
            for role in {node.role for node in NODES}
        }
        == {
            "primary": 1,
            "pending_dependency": 1,
            "qualified_consumer": 4,
            "pending_consumer": 7,
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

    checks.check("frozen graph inventories 123 source predicates", observed_predicates == 123)
    checks.check(
        "immutable compatibility shapes are exhaustively classified",
        observed_compatibility == EXPECTED_COMPATIBILITY,
    )
    checks.check(
        "B1 retains an alias-only replay path backed by np.trapezoid",
        observed_compatibility["B1"] == (0, 1, 0, 1, 1),
    )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
