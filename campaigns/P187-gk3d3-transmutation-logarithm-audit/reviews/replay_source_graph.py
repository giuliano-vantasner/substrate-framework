#!/usr/bin/env python3
"""Replay C-VAC-004, GK3D3, and immutable reverse-consumer closure."""

from __future__ import annotations

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
    if not isinstance(data, dict):
        raise TypeError(f"expected mapping in {path}")
    return data


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P187-GK3D3-SOURCE-GRAPH")
    queue = _load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}

    for unit, expected_hash in EXPECTED_HASHES.items():
        path = SOURCE_ROOT / EXPECTED_PATHS[unit]
        checks.check(
            f"{unit} source hash and queue path remain pinned",
            _digest(path) == expected_hash
            and units[unit]["sha256"] == expected_hash
            and units[unit]["path"] == EXPECTED_PATHS[unit],
        )

    reverse: dict[str, list[str]] = {}
    for row in queue["units"]:
        for dependency in row.get("candidate_dependencies", []):
            reverse.setdefault(dependency, []).append(row["source_unit"])
    direct = set(reverse.get("GK3D3", []))
    checks.check(
        "direct source consumers including the narrative cycle are exact",
        direct == {"GK3D1", "GK3D2", "GK3D4", "GK3D5", "GK3D6"},
    )
    seen = {"GK3D3"}
    frontier = ["GK3D3"]
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
        "transitive source consumer depths are exact",
        depths
        == {
            "GK3D1": 1,
            "GK3D2": 1,
            "GK3D4": 1,
            "GK3D5": 1,
            "GK3D6": 1,
            "EL2": 2,
            "HE5": 3,
        },
    )

    expected_mapping = [
        "C-RGE-003",
        "C-IDN-002",
        "C-DIM-009",
        "C-VAC-003",
        "C-VAC-004",
    ]
    checks.check(
        "GK3D3 generated qualification and mappings are exact",
        units["GK3D3"]["disposition"] == "qualified"
        and units["GK3D3"]["accepted_claims"] == expected_mapping,
    )

    registry = _load(ROOT / "governance/claims.yaml")
    claims = {claim["id"]: claim for claim in registry["claims"]}
    claim = claims["C-VAC-004"]
    checks.check(
        "C-VAC-004 four-axis status and direct dependencies are exact",
        claim["verification"] == "symbolic_verified"
        and claim["review"] == "accepted"
        and claim["compatibility"] == "compatible_extension"
        and claim["epistemic"] == "active"
        and claim["dependencies"] == ["C-RGE-003", "C-VAC-003"],
    )
    checks.check(
        "C-VAC-004 statement retains conversions boundary and scope ceiling",
        "without requiring K0=K1" in claim["statement"]
        and "Z_ref+b/(b0*g^2)" in claim["statement"]
        and "separately declared zero-matching" in claim["statement"]
        and "does not identify either length" in claim["statement"],
    )

    release = _load(ROOT / "governance/releases/v0.139.0.yaml")
    checks.check(
        "v0.139.0 pins the unique 179-claim set and C-VAC-004",
        release["release"] == "v0.139.0"
        and len(release["accepted_claims"]) == 179
        and len(set(release["accepted_claims"])) == 179
        and "C-VAC-004" in release["accepted_claims"],
    )
    checks.check(
        "release contains the complete accepted dependency closure",
        set(claim["dependencies"]).issubset(release["accepted_claims"])
        and all(dependency in claims for dependency in claim["dependencies"]),
    )

    dispositions = _load(ROOT / "migration/dispositions.yaml")["units"]
    decision = dispositions["GK3D3"]
    checks.check(
        "editable disposition evidence is materialized",
        decision["disposition"] == "qualified"
        and decision["accepted_claims"] == expected_mapping
        and all((ROOT / path).is_file() for path in decision["evidence"]),
    )

    no_surface: list[str] = []
    for unit in EXPECTED_PATHS:
        source_text = (SOURCE_ROOT / EXPECTED_PATHS[unit]).read_text(encoding="utf-8")
        compatibility = audit_numpy_trapezoid_compatibility(
            source_text,
            filename=EXPECTED_PATHS[unit],
        )
        if compatibility.legacy_references == 0:
            no_surface.append(unit)
    checks.check(
        "seven inventoried nodes have no legacy trapezoidal reference",
        set(no_surface) == {"GK3D1", "GK3D2", "GK3D3", "GK3D4", "GK3D6", "EL2", "HE5"},
    )
    gk3d5_text = (SOURCE_ROOT / EXPECTED_PATHS["GK3D5"]).read_text(
        encoding="utf-8"
    )
    gk3d5_compatibility = audit_numpy_trapezoid_compatibility(
        gk3d5_text,
        filename=EXPECTED_PATHS["GK3D5"],
    )
    checks.check(
        "GK3D5 uses a current-first lazy compatibility fallback",
        gk3d5_compatibility.dynamic_current_getattrs == 1
        and gk3d5_compatibility.direct_legacy_attributes == 1
        and gk3d5_compatibility.eager_legacy_default_fallbacks == 0
        and 'getattr(np, "trapezoid", None) or np.trapz' in gk3d5_text,
    )

    canonical_path = ROOT / "src/substrate_framework/kinetic_scale_matching.py"
    canonical_compatibility = audit_numpy_trapezoid_compatibility(
        canonical_path.read_text(encoding="utf-8"),
        filename=str(canonical_path),
    )
    checks.check(
        "canonical composition has no NumPy compatibility surface",
        canonical_compatibility.legacy_references == 0
        and canonical_compatibility.current_references == 0
        and canonical_compatibility.eager_legacy_default_fallbacks == 0,
    )

    gk3d4_text = (SOURCE_ROOT / EXPECTED_PATHS["GK3D4"]).read_text(
        encoding="utf-8"
    )
    gk3d6_text = (SOURCE_ROOT / EXPECTED_PATHS["GK3D6"]).read_text(
        encoding="utf-8"
    )
    checks.check(
        "forward narratives expose the exact ceilings requiring later review",
        "Z_i = {k: sp.simplify(v / (b0 * beta2))" in gk3d4_text
        and "Writing m = hbar c0/xi outright, as GK3D3 did" in gk3d6_text
        and "GK3D3's logarithm" in gk3d5_text,
    )
    checks.check(
        "accepted generated records exist",
        (ROOT / "memory/framework/claims/C-VAC-004.md").is_file()
        and (ROOT / "memory/framework/releases/v0.139.0.md").is_file()
        and (ROOT / "memory/vantasner/decisions/C-VAC-004-review.md").is_file()
        and (ROOT / "memory/vantasner/decisions/GK3D3-qualified-review.md").is_file(),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
