#!/usr/bin/env python3
"""Replay GK3D1 source, claim, release, and reverse-consumer closure."""

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
    checks = CheckLedger("P185-GK3D1-SOURCE-GRAPH")
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
        "generated queue counts close after GK3D1 qualification",
        queue["primary_unit_count"] == 218
        and queue["disposition_counts"]
        == {
            "duplicate_evidence": 8,
            "migrated": 3,
            "out_of_scope": 1,
            "pending_adjudication": 39,
            "qualified": 166,
            "refuted": 1,
        },
    )
    checks.check(
        "GK3D1 generated disposition and accepted mappings are exact",
        units["GK3D1"]["disposition"] == "qualified"
        and units["GK3D1"]["accepted_claims"]
        == ["C-GAU-001", "C-DIM-009", "C-VAC-002"],
    )

    reverse: dict[str, list[str]] = {}
    for row in queue["units"]:
        for dependency in row.get("candidate_dependencies", []):
            reverse.setdefault(dependency, []).append(row["source_unit"])
    direct = set(reverse.get("GK3D1", []))
    checks.check(
        "direct source reverse consumers are complete",
        direct == {"GK3D2", "GK3D3", "GK3D4", "GK3D5"},
    )
    seen = {"GK3D1"}
    frontier = ["GK3D1"]
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
            "GK3D2": 1,
            "GK3D3": 1,
            "GK3D4": 1,
            "GK3D5": 1,
            "GK3D6": 2,
            "EL2": 2,
            "HE5": 3,
        },
    )
    checks.check(
        "downstream source dispositions remain individually governed",
        all(
            units[unit]["disposition"] == "pending_adjudication"
            for unit in ("GK3D2", "GK3D3", "GK3D4", "GK3D5", "GK3D6")
        )
        and units["EL2"]["disposition"] == "qualified"
        and units["HE5"]["disposition"] == "out_of_scope",
    )

    registry = _load(ROOT / "governance/claims.yaml")
    claims = {claim["id"]: claim for claim in registry["claims"]}
    claim = claims["C-VAC-002"]
    checks.check(
        "C-VAC-002 four-axis status and dependency closure are exact",
        claim["verification"] == "symbolic_verified"
        and claim["review"] == "accepted"
        and claim["compatibility"] == "compatible_extension"
        and claim["epistemic"] == "active"
        and claim["dependencies"] == ["C-GAU-001", "C-DIM-009"]
        and all(dependency in claims for dependency in claim["dependencies"]),
    )
    checks.check(
        "claim statement retains the counterterm and physical-scope ceiling",
        "arbitrary finite local constant c_fin" in claim["statement"]
        and "derive no physical charged excitation" in claim["statement"]
        and "total Maxwell coefficient" in claim["statement"]
        and "above threshold requires" in claim["statement"],
    )

    release = _load(ROOT / "governance/releases/v0.137.0.yaml")
    current = _load(ROOT / "governance/releases/current.yaml")
    checks.check(
        "v0.137.0 and current pin the same 177-claim set",
        release == current
        and release["release"] == "v0.137.0"
        and len(release["accepted_claims"]) == 177
        and len(set(release["accepted_claims"])) == 177
        and "C-VAC-002" in release["accepted_claims"],
    )
    checks.check(
        "release contains the complete C-VAC-002 dependency closure",
        set(claim["dependencies"]).issubset(release["accepted_claims"]),
    )

    source_text = (SOURCE_ROOT / EXPECTED_PATHS["GK3D1"]).read_text(
        encoding="utf-8"
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=EXPECTED_PATHS["GK3D1"],
    )
    canonical_text = (
        ROOT / "src/substrate_framework/dirac_vacuum_polarization.py"
    ).read_text(encoding="utf-8")
    canonical_tree = ast.parse(canonical_text)
    checks.check(
        "source and canonical implementation have no NumPy compatibility surface",
        compatibility.current_references == 0
        and compatibility.legacy_references == 0
        and "import numpy" not in canonical_text
        and "np.trapz" not in canonical_text,
    )
    checks.check(
        "canonical implementation contains no floor-based trace continuation",
        not any(isinstance(node, ast.FloorDiv) for node in ast.walk(canonical_tree))
        and not any(
            isinstance(node, ast.Call)
            and (
                (isinstance(node.func, ast.Name) and node.func.id == "floor")
                or (isinstance(node.func, ast.Attribute) and node.func.attr == "floor")
            )
            for node in ast.walk(canonical_tree)
        )
        and "spinor_trace" in canonical_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
