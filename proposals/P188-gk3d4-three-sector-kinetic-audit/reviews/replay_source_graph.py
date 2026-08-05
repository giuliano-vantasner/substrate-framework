#!/usr/bin/env python3
"""Replay GK3D4's accepted composition and immutable consumer closure."""

from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
EXPECTED_PATHS = {
    "GK3D4": "merged-framework/bridges/phase-41/bridge_GK3D4_three_sectors_one_construction.py",
    "GK3D5": "merged-framework/bridges/phase-41/bridge_GK3D5_charged_excitation_exists_in_3D.py",
    "GK3D6": "merged-framework/bridges/phase-41/bridge_GK3D6_oneloop_accuracy_and_exact_ratios.py",
    "EL2": "merged-framework/bridges/phase-46/bridge_EL2_lepton_is_baryonless_fermion.py",
    "HE5": "merged-framework/bridges/phase-45/bridge_HE5_consumer_dependency_parse.py",
}
EXPECTED_HASHES = {
    "GK3D4": "046273d9a06f92ddbe9cd666d3b6de0f321b9709c371aeee8103394dd2a2ad35",
    "GK3D5": "201d4fd2594a73c7b59dbe81e0e66f1d3d43a52605a26174c70bd072626992e2",
    "GK3D6": "e0ab2a2db57affe023e6838ed835656412cf01188225f31084e6a6a1baf8e036",
    "EL2": "db90b921e0b3d6966597a39817ad48219cd94fa27ff8aa2a1de4a64c3ccf6965",
    "HE5": "70a8402413e3bdde15a9d9b93fb4fc282f277b28a5943da9fad4a8cc6c561b81",
}
EXPECTED_MAPPING = [
    "C-LIE-001",
    "C-REP-002",
    "C-PGA-001",
    "C-DIM-009",
    "C-VAC-002",
    "C-VAC-003",
    "C-VAC-004",
    "C-REP-001",
    "C-RGE-005",
    "C-ANO-001",
]


def _load(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"expected mapping in {path}")
    return data


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P188-GK3D4-SOURCE-GRAPH")
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
    checks.check(
        "direct reverse consumers are exact",
        set(reverse.get("GK3D4", [])) == {"GK3D5", "GK3D6"},
    )

    seen = {"GK3D4"}
    frontier = ["GK3D4"]
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
        "transitive reverse consumer depths are exact",
        depths == {"GK3D5": 1, "GK3D6": 1, "EL2": 2, "HE5": 3},
    )

    checks.check(
        "GK3D4 generated qualification and mappings are exact",
        units["GK3D4"]["disposition"] == "qualified"
        and units["GK3D4"]["accepted_claims"] == EXPECTED_MAPPING,
    )

    dispositions = _load(ROOT / "migration/dispositions.yaml")["units"]
    decision = dispositions["GK3D4"]
    checks.check(
        "editable GK3D4 disposition evidence is materialized",
        decision["disposition"] == "qualified"
        and decision["accepted_claims"] == EXPECTED_MAPPING
        and all((ROOT / path).is_file() for path in decision["evidence"]),
    )

    registry = _load(ROOT / "governance/claims.yaml")
    claims = {claim["id"]: claim for claim in registry["claims"]}
    checks.check(
        "accepted composition exists with accepted four-axis status",
        all(
            claim_id in claims
            and claims[claim_id]["review"] == "accepted"
            and claims[claim_id]["epistemic"] in {"active", "qualified"}
            for claim_id in EXPECTED_MAPPING
        ),
    )
    closure = {
        dependency
        for claim_id in EXPECTED_MAPPING
        for dependency in claims[claim_id].get("dependencies", [])
    }
    checks.check(
        "accepted composition dependency closure remains in the registry",
        closure.issubset(claims),
    )
    checks.check(
        "reserved C-VAC-005 remains unpromoted",
        "C-VAC-005" not in claims and len(claims) == 179,
    )

    current = _load(ROOT / "governance/releases/current.yaml")
    release = _load(ROOT / "governance/releases/v0.139.0.yaml")
    checks.check(
        "no-new-claim disposition leaves v0.139.0 current",
        current["release"] == "v0.139.0"
        and release["release"] == "v0.139.0"
        and len(release["accepted_claims"]) == 179,
    )

    no_surface: list[str] = []
    for unit in EXPECTED_PATHS:
        text = (SOURCE_ROOT / EXPECTED_PATHS[unit]).read_text(encoding="utf-8")
        compatibility = audit_numpy_trapezoid_compatibility(
            text,
            filename=EXPECTED_PATHS[unit],
        )
        if compatibility.legacy_references == 0:
            no_surface.append(unit)
    checks.check(
        "four closure nodes have no legacy trapezoidal surface",
        set(no_surface) == {"GK3D4", "GK3D6", "EL2", "HE5"},
    )
    gk3d5_text = (SOURCE_ROOT / EXPECTED_PATHS["GK3D5"]).read_text(
        encoding="utf-8"
    )
    gk3d5_compatibility = audit_numpy_trapezoid_compatibility(
        gk3d5_text,
        filename=EXPECTED_PATHS["GK3D5"],
    )
    checks.check(
        "GK3D5 immutable fallback is current-first and lazy",
        gk3d5_compatibility.dynamic_current_getattrs == 1
        and gk3d5_compatibility.direct_legacy_attributes == 1
        and gk3d5_compatibility.eager_legacy_default_fallbacks == 0,
    )

    gk3d6_text = (SOURCE_ROOT / EXPECTED_PATHS["GK3D6"]).read_text(
        encoding="utf-8"
    )
    checks.check(
        "GK3D6 exposes the direct ratio and three-eighths propagation ceiling",
        "GK3D4's ratios" in gk3d6_text
        and "GK3D4.4a found" in gk3d6_text
        and "GK3D4.5b is exact" in gk3d6_text,
    )
    checks.check(
        "terminal campaign and durable decision records exist",
        (ROOT / "campaigns/P188-gk3d4-three-sector-kinetic-audit/adjudication.yaml").is_file()
        and (ROOT / "memory/vantasner/decisions/GK3D4-qualified-review.md").is_file()
        and not (ROOT / "proposals/P188-gk3d4-three-sector-kinetic-audit").exists(),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
