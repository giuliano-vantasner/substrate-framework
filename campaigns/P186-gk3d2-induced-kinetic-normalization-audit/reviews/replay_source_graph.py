#!/usr/bin/env python3
"""Replay GK3D2 claim, release, queue, and reverse-consumer closure."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
EXPECTED_HASHES = {
    "GK3D1": "9a25110ba53adfb439d0cfd0570bd311b0a43a20f13d1351f45c3fa4075aeacb",
    "GK3D2": "856096aba38812dc17fb07ce5cf7c0fa13eb2623665ccf871810734ac3ca0886",
    "GK3D3": "1c3f81d15ace3ec2c6326c89659596f5b9ff84ac23ef7f0143a53ad92b23b211",
    "GK3D4": "046273d9a06f92ddbe9cd666d3b6de0f321b9709c371aeee8103394dd2a2ad35",
    "GK3D5": "201d4fd2594a73c7b59dbe81e0e66f1d3d43a52605a26174c70bd072626992e2",
    "GK3D6": "e0ab2a2db57affe023e6838ed835656412cf01188225f31084e6a6a1baf8e036",
    "EL2": "db90b921e0b3d6966597a39817ad48219cd94fa27ff8aa2a1de4a64c3ccf6965",
    "HE5": "70a8402413e3bdde15a9d9b93fb4fc282f277b28a5943da9fad4a8cc6c561b81",
}
EXPECTED_PATHS = {
    "GK3D1": "merged-framework/bridges/phase-41/bridge_GK3D1_master_polarization_general_D.py",
    "GK3D2": "merged-framework/bridges/phase-41/bridge_GK3D2_induced_kinetic_normalization.py",
    "GK3D3": "merged-framework/bridges/phase-41/bridge_GK3D3_transmutation_closes_the_log.py",
    "GK3D4": "merged-framework/bridges/phase-41/bridge_GK3D4_three_sectors_one_construction.py",
    "GK3D5": "merged-framework/bridges/phase-41/bridge_GK3D5_charged_excitation_exists_in_3D.py",
    "GK3D6": "merged-framework/bridges/phase-41/bridge_GK3D6_oneloop_accuracy_and_exact_ratios.py",
    "EL2": "merged-framework/bridges/phase-46/bridge_EL2_lepton_is_baryonless_fermion.py",
    "HE5": "merged-framework/bridges/phase-45/bridge_HE5_consumer_dependency_parse.py",
}


def _load(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P186-GK3D2-SOURCE-GRAPH")
    queue = _load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}

    for unit, expected_hash in EXPECTED_HASHES.items():
        path = SOURCE_ROOT / EXPECTED_PATHS[unit]
        checks.check(
            f"{unit} source hash remains pinned",
            _digest(path) == expected_hash
            and units[unit]["sha256"] == expected_hash
            and units[unit]["path"] == EXPECTED_PATHS[unit],
        )

    checks.check(
        "generated queue counts close after GK3D2 qualification",
        queue["primary_unit_count"] == 218
        and queue["disposition_counts"]
        == {
            "duplicate_evidence": 8,
            "migrated": 3,
            "out_of_scope": 1,
            "pending_adjudication": 38,
            "qualified": 167,
            "refuted": 1,
        },
    )
    expected_mapping = [
        "C-GAU-001",
        "C-DIM-009",
        "C-VAC-002",
        "C-MAX-001",
        "C-VAC-003",
    ]
    checks.check(
        "GK3D2 generated disposition and accepted mappings are exact",
        units["GK3D2"]["disposition"] == "qualified"
        and units["GK3D2"]["accepted_claims"] == expected_mapping,
    )

    reverse: dict[str, list[str]] = {}
    for row in queue["units"]:
        for dependency in row.get("candidate_dependencies", []):
            reverse.setdefault(dependency, []).append(row["source_unit"])
    direct = set(reverse.get("GK3D2", []))
    checks.check(
        "direct source reverse consumers including the source cycle are exact",
        direct == {"GK3D1", "GK3D3", "GK3D4", "GK3D6"},
    )
    seen = {"GK3D2"}
    frontier = ["GK3D2"]
    depths: dict[str, int] = {}
    depth = 0
    while frontier:
        depth += 1
        next_frontier: list[str] = []
        for parent in frontier:
            for child in reverse.get(parent, []):
                if child not in seen:
                    seen.add(child)
                    depths[child] = depth
                    next_frontier.append(child)
        frontier = next_frontier
    checks.check(
        "transitive source reverse-consumer depths are exact",
        depths
        == {
            "GK3D1": 1,
            "GK3D3": 1,
            "GK3D4": 1,
            "GK3D6": 1,
            "GK3D5": 2,
            "EL2": 3,
            "HE5": 4,
        },
    )
    checks.check(
        "downstream source dispositions remain individually governed",
        units["GK3D1"]["disposition"] == "qualified"
        and all(
            units[unit]["disposition"] == "pending_adjudication"
            for unit in ("GK3D3", "GK3D4", "GK3D5", "GK3D6")
        )
        and units["EL2"]["disposition"] == "qualified"
        and units["HE5"]["disposition"] == "out_of_scope",
    )

    registry = _load(ROOT / "governance/claims.yaml")
    claims = {claim["id"]: claim for claim in registry["claims"]}
    claim = claims["C-VAC-003"]
    checks.check(
        "C-VAC-003 four-axis status and dependency closure are exact",
        claim["verification"] == "symbolic_verified"
        and claim["review"] == "accepted"
        and claim["compatibility"] == "compatible_extension"
        and claim["epistemic"] == "active"
        and claim["dependencies"]
        == ["C-GAU-001", "C-DIM-009", "C-VAC-002", "C-MAX-001"]
        and all(dependency in claims for dependency in claim["dependencies"]),
    )
    checks.check(
        "claim statement retains the affine boundary and physical-scope ceiling",
        "independent real reference value Z_ref" in claim["statement"]
        and "separately declared zero-matching" in claim["statement"]
        and "does not fix Z_ref" in claim["statement"]
        and "physical charged spectrum" in claim["statement"],
    )

    release = _load(ROOT / "governance/releases/v0.138.0.yaml")
    current = _load(ROOT / "governance/releases/current.yaml")
    checks.check(
        "v0.138.0 and current pin the same 178-claim set",
        release == current
        and release["release"] == "v0.138.0"
        and len(release["accepted_claims"]) == 178
        and len(set(release["accepted_claims"])) == 178
        and "C-VAC-003" in release["accepted_claims"],
    )
    checks.check(
        "release contains the complete C-VAC-003 dependency closure",
        set(claim["dependencies"]).issubset(release["accepted_claims"]),
    )

    source_text = (SOURCE_ROOT / EXPECTED_PATHS["GK3D2"]).read_text(
        encoding="utf-8"
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=EXPECTED_PATHS["GK3D2"],
    )
    canonical_text = (
        ROOT / "src/substrate_framework/vacuum_polarization.py"
    ).read_text(encoding="utf-8")
    canonical_tree = ast.parse(canonical_text)
    checks.check(
        "GK3D2 and canonical implementation have no NumPy compatibility surface",
        compatibility.current_references == 0
        and compatibility.legacy_references == 0
        and not any(
            isinstance(node, (ast.Import, ast.ImportFrom))
            and (
                (isinstance(node, ast.Import) and any(alias.name == "numpy" for alias in node.names))
                or (isinstance(node, ast.ImportFrom) and node.module == "numpy")
            )
            for node in ast.walk(canonical_tree)
        ),
    )
    gk3d5_text = (SOURCE_ROOT / EXPECTED_PATHS["GK3D5"]).read_text(
        encoding="utf-8"
    )
    gk3d5_compatibility = audit_numpy_trapezoid_compatibility(
        gk3d5_text,
        filename=EXPECTED_PATHS["GK3D5"],
    )
    checks.check(
        "pending GK3D5 uses a current-first lazy legacy compatibility path",
        gk3d5_compatibility.dynamic_current_getattrs == 1
        and gk3d5_compatibility.direct_legacy_attributes == 1
        and gk3d5_compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "consumer ceiling is explicit in every direct pending narrative",
        "additive constant removed by rung25"
        in (SOURCE_ROOT / EXPECTED_PATHS["GK3D3"]).read_text(encoding="utf-8")
        and "Z_i = 1/g_i^2"
        in (SOURCE_ROOT / EXPECTED_PATHS["GK3D4"]).read_text(encoding="utf-8")
        and "exactly independent of c"
        in (SOURCE_ROOT / EXPECTED_PATHS["GK3D6"]).read_text(encoding="utf-8").lower(),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
