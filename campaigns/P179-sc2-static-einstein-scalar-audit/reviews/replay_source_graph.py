#!/usr/bin/env python3
"""Hash, inventory, disposition, compatibility, and attempt replay for P179."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
CAMPAIGN = ROOT / "campaigns/P179-sc2-static-einstein-scalar-audit"
SOURCES = {
    "G3": ("merged-framework/bridges/phase-5/bridge_G3_horndeski_scalar_tensor.py", "8d462ce2bfd57bfced9fdedd511e9d2711e0c2454bc0d0441c681288495719ba", 11, 1, 0, 0),
    "QB1": ("merged-framework/bridges/phase-16/bridge_QB1_radial_eigenvalue_quasibreather.py", "1f387c140ca80be0e457efd17146267bdecab1cbdbcdd10dd34287bc5de2dc7a", 6, 1, 0, 0),
    "QB3": ("merged-framework/bridges/phase-16/bridge_QB3_triaxial_nonaxisymmetric.py", "e9626f2e4829084635386eea271d0abdd39c81dfcd6899765d2f4bffac83e0c8", 4, 1, 1, 1),
    "BX1": ("merged-framework/bridges/phase-36/bridge_BX1_l2_mode_box_artifact.py", "a80364df834f23b5ad006b54e7097e0a38d846405ba40408e558a8773aa74fb3", 8, 1, 0, 0),
    "SC1": ("merged-framework/bridges/phase-36/bridge_SC1_gordon_coupled_overdetermined.py", "70799bff934f1f6986545a0bde0cb94fe016dd4b468b36614ac3e5d9bb74aec0", 5, 1, 0, 0),
    "SC2": ("merged-framework/bridges/phase-36/bridge_SC2_horndeski_selfconsistent_solve.py", "64dfc9c31edd8368cb0e2359ca646fc8f62fe306d6af7a326ff8934070b96425", 7, 4, 0, 0),
    "TX1": ("merged-framework/bridges/phase-40/bridge_TX1_b2_intrinsic_quadrupole.py", "30161731af4e3ffda219adbdc7af9db66f6829fbbd3736a3198ed19a644ac8ff", 9, 2, 1, 1),
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P179-SC2-SOURCE-GRAPH")
    predicates = 0
    assertions = 0
    for unit, (relative, digest, expected_checks, expected_asserts, legacy, current) in SOURCES.items():
        path = SOURCE_ROOT / relative
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        lexical = sum(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            for node in ast.walk(tree)
        )
        assertion_count = sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
        predicates += lexical
        assertions += assertion_count
        checks.check(f"{unit} retains its pinned bytes", _digest(path) == digest)
        checks.check(
            f"{unit} retains its lexical predicate and assertion inventory",
            lexical == expected_checks and assertion_count == expected_asserts,
        )
        compatibility = audit_numpy_trapezoid_compatibility(source, filename=str(path))
        checks.check(
            f"{unit} compatibility syntax retains its classified surface",
            compatibility.legacy_references == legacy
            and compatibility.current_references == current
            and compatibility.eager_legacy_default_fallbacks == 0,
        )
    checks.check(
        "the seven-node graph inventories checks and assertions separately",
        predicates == 50 and assertions == 11,
    )

    queue = yaml.safe_load((ROOT / "migration/source-claims.yaml").read_text())
    entries = {entry["source_unit"]: entry for entry in queue["units"]}
    checks.check(
        "accepted dependency source mappings remain individually closed",
        entries["G3"]["accepted_claims"] == ["C-STG-001"]
        and entries["QB1"]["accepted_claims"] == ["C-PDE-005", "C-PDE-006"]
        and "C-PDE-009" in entries["QB3"]["accepted_claims"]
        and "C-PDE-012" in entries["BX1"]["accepted_claims"]
        and entries["SC1"]["accepted_claims"]
        == ["C-GOR-001", "C-STG-001", "C-GOR-002"],
    )
    promoted = {
        "C-STG-001",
        "C-PDE-005",
        "C-PDE-009",
        "C-PDE-012",
        "C-STG-002",
        "C-PDE-013",
    }
    sc2 = entries["SC2"]
    checks.check(
        "SC2 is transition-safe from pending to its exact qualified mapping",
        (
            sc2["disposition"] == "pending_adjudication"
            and sc2["accepted_claims"] == []
        )
        or (
            sc2["disposition"] == "qualified"
            and set(sc2["accepted_claims"]) == promoted
        ),
    )
    checks.check(
        "TX1 remains a pending reverse consumer without accepted claims",
        entries["TX1"]["disposition"] == "pending_adjudication"
        and entries["TX1"]["accepted_claims"] == [],
    )
    checks.check(
        "inventory E1 E2 and E3 tokens are local equation-label collisions",
        all(token in entries["SC2"]["candidate_dependencies"] for token in ("E1", "E2", "E3"))
        and all(f"({token})" in (SOURCE_ROOT / SOURCES["SC2"][0]).read_text() for token in ("E1", "E2", "E3")),
    )

    native_sc2 = yaml.safe_load((CAMPAIGN / "attempts/0002/result.yaml").read_text())
    native_tx1 = yaml.safe_load((CAMPAIGN / "attempts/0009/result.yaml").read_text())
    checks.check(
        "SC2 native execution is reused from its recorded clean seven-check attempt",
        native_sc2["process"]["exit_code"] == 0
        and native_sc2["process"]["runtime_checks"] == 7
        and native_sc2["compatibility"]["scientific_candidate_failures_from_version_events"] == 0,
    )
    checks.check(
        "TX1 native execution is reused without turning its legacy spelling into science",
        native_tx1["process"]["exit_code"] == 0
        and native_tx1["process"]["runtime_checks"] == 9
        and native_tx1["compatibility"]["scientific_candidate_failures_from_version_events"] == 0,
    )
    checks.check(
        "successful reverse-consumer execution creates no blanket authority",
        entries["TX1"]["accepted_claims"] == []
        and native_tx1["authority"].startswith("TX1 remains pending"),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
