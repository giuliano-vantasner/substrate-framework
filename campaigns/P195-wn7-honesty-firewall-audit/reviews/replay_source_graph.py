#!/usr/bin/env python3
"""Verify P195's byte-reused eleven-node direct WN7 source graph."""

from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
PROPOSAL = Path(__file__).resolve().parents[1]
NODES = {
    "CM1": {
        "path": "merged-framework/bridges/phase-31/bridge_CM1_separation_boundary.py",
        "sha256": "0f6881d96469274664ed1b762ff56a88b94ecdca599c22f8bb181052bd7f3ccc",
        "tally": 13,
        "record": "campaigns/P115-cm1-screened-barrier-ceiling-audit/evidence/source-reproduction.yaml",
        "record_sha256": "dc29a6d4604385869172e14261581c1d184afffd1129d36ada38d691185aa814",
    },
    "GB4": {
        "path": "merged-framework/bridges/phase-32/bridge_GB4_branching_ratio.py",
        "sha256": "497ed6deda4a0f11562baeaef0ec7bc21cc20b38d3d11c69ed07728ed33faeb0",
        "tally": 23,
        "record": "campaigns/P125-gb4-weighted-branching-audit/evidence/source-reproduction.yaml",
        "record_sha256": "f81760ba788e16b334f8546273a2e5ad5af8ee089a446109de20e2ac7278025a",
    },
    "GB6": {
        "path": "merged-framework/bridges/phase-32/bridge_GB6_honesty_firewall_guard.py",
        "sha256": "edcfc0fafad48dbfc88ebf97613d45c1b6cf7e85b95548ae4006b373a2cfc49a",
        "tally": 29,
        "record": "campaigns/P127-gb6-honesty-firewall-audit/evidence/source-reproduction.yaml",
        "record_sha256": "06f1fdcd4f2dfdacc58ff0c72c45b8d18da8daa9c3d33e8ff0a54813b8fcb497",
    },
    "PN4": {
        "path": "merged-framework/bridges/phase-30/bridge_PN4_lossy_exchange_and_guard.py",
        "sha256": "45ac6c039805964efa41ae8167f6257af18c5ef2b066d376efa19ec79dfd0c67",
        "tally": 27,
        "record": "campaigns/P112-pn4-lossy-paired-resolvent-audit/evidence/source-reproduction.yaml",
        "record_sha256": "0b0a2d9cbe49d77876b43715561a51ed0b4ca8864a1b3db17fc537f5bba9a8c9",
    },
    "WN1": {
        "path": "merged-framework/bridges/phase-37/bridge_WN1_vertex_coefficient_magnitude.py",
        "sha256": "3764b29955c3bd51c10278159e08a52ff616a7041510e56917b091f1a802cdde",
        "tally": 44,
        "record": "campaigns/P189-wn1-factorial-suppression-audit/evidence/source-reproduction.yaml",
        "record_sha256": "9e3aacd22af50cb8bcfb6491dd38ac096e9911be57a1f01618cef71300c233a4",
    },
    "WN2": {
        "path": "merged-framework/bridges/phase-37/bridge_WN2_coefficient_cannot_be_the_weight.py",
        "sha256": "dc9a7dbd79c908d1ec206392cdd81a34b5a39c08dcba31f2c164c3d92073504c",
        "tally": 70,
        "record": "campaigns/P190-wn2-coefficient-weight-audit/evidence/source-reproduction.yaml",
        "record_sha256": "663cf752311ab2728a0e1fcb8b3c992278db3dbf0e64f52d5a488b7dd928bfb4",
    },
    "WN3": {
        "path": "merged-framework/bridges/phase-37/bridge_WN3_amplitude_scale_and_multiplicity.py",
        "sha256": "8a13c8b2af4d89297a11b3ef7460cc1f35fe274dc4affb2b9a7d3649bc237e88",
        "tally": 48,
        "record": "campaigns/P191-wn3-bosonic-multiplicity-audit/evidence/source-reproduction.yaml",
        "record_sha256": "5860c970728e1605f6217f855e7290b38720cd6a855e9abf9b1d4f891ad50727",
    },
    "WN4": {
        "path": "merged-framework/bridges/phase-37/bridge_WN4_derived_weight_and_crossover.py",
        "sha256": "2377bb4ba817cd20c188d4adeeeb9169253e9b1231477ac2069b36cc923fc7e2",
        "tally": 43,
        "record": "campaigns/P192-wn4-derived-weight-crossover-audit/evidence/source-reproduction.yaml",
        "record_sha256": "23e83b021eebd2c72fee0d6432d6d0aa7ecd8a9d38b47257df0a3b6af0067a0b",
    },
    "WN5": {
        "path": "merged-framework/bridges/phase-37/bridge_WN5_gb4_preserved_and_new_prediction.py",
        "sha256": "5618ba007e041512a7d207026dc6369c8277312acba4c250219a1629585a7fbc",
        "tally": 41,
        "record": "campaigns/P193-wn5-branching-prediction-audit/evidence/source-reproduction.yaml",
        "record_sha256": "0a9cf3bd10974ef0aecea97040608d602294a3e064947a2076e947fea2f00dae",
    },
    "WN6": {
        "path": "merged-framework/bridges/phase-37/bridge_WN6_scale_verdict_and_missing_bridge.py",
        "sha256": "07f049bac9eb99cb29ef6c3cd333aaecddc17492a73a8fc2aac7eb140ebcab10",
        "tally": 32,
        "record": "campaigns/P194-wn6-scale-verdict-audit/evidence/source-reproduction.yaml",
        "record_sha256": "42f0a42b57da16032317b9b43c16cc5564f127eae37119499c3def1007ccd5e6",
    },
    "WN7": {
        "path": "merged-framework/bridges/phase-37/bridge_WN7_honesty_firewall_guard.py",
        "sha256": "88844689bf682ca5ff524378f4e5e46a25bcab54b1a3a6e59afe69b990694d50",
        "tally": 59,
        "record": "campaigns/P195-wn7-honesty-firewall-audit/evidence/source-reproduction.yaml",
        "record_sha256": "79b075e0708346e6d8372c2da367efbd73cf36e0582be44d896a575ff3265428",
    },
}
DIRECT_DEPENDENCIES = {"CM1", "GB4", "GB6", "PN4", "WN1", "WN2", "WN3", "WN4", "WN5", "WN6"}
ACCEPTED_MAPPINGS = {
    "CM1": ["C-SCR-001"],
    "GB4": ["C-BRN-001"],
    "GB6": [],
    "PN4": ["C-RES-001"],
    "WN1": ["C-SG-019", "C-CMB-001"],
    "WN2": ["C-SG-019", "C-CMB-001", "C-CMB-002", "C-BRN-001"],
    "WN3": ["C-SG-019", "C-CMB-001", "C-OSC-001"],
    "WN4": ["C-OSC-001", "C-CMB-003"],
    "WN5": ["C-BRN-001", "C-OSC-001"],
    "WN6": ["C-SG-019", "C-OSC-001", "C-CMB-003", "C-OSC-002"],
}


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record_tally(record: dict) -> int | None:
    for field in ("runtime_checks", "runtime_predicates", "runtime_check_executions"):
        if field in record:
            return int(record[field])
    return None


def main() -> int:
    checks = CheckLedger("P195-WN7-SOURCE-GRAPH")
    queue = load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}

    compatibility_events: list[str] = []
    for unit, expected in NODES.items():
        source_path = SOURCE_ROOT / expected["path"]
        record_path = ROOT / expected["record"]
        record = load(record_path)
        exit_status = record.get("exit_status", record.get("exit_code"))
        checks.check(
            f"{unit} source and native record remain pinned",
            units[unit]["path"] == expected["path"]
            and units[unit]["sha256"] == expected["sha256"]
            and digest(source_path) == expected["sha256"]
            and digest(record_path) == expected["record_sha256"]
            and record_tally(record) == expected["tally"]
            and exit_status == 0,
        )
        compatibility = audit_numpy_trapezoid_compatibility(
            source_path.read_text(encoding="utf-8"),
            filename=expected["path"],
        )
        if compatibility.legacy_references or compatibility.eager_legacy_default_fallbacks:
            compatibility_events.append(unit)

    checks.check(
        "eleven unique records cover 429 native checks without re-execution",
        len(NODES) == 11 and sum(row["tally"] for row in NODES.values()) == 429,
    )
    checks.check(
        "no direct graph node needs a legacy NumPy compatibility alias",
        compatibility_events == [],
    )
    checks.check(
        "WN7 direct source dependencies are exact",
        set(units["WN7"]["candidate_dependencies"]) == DIRECT_DEPENDENCIES,
    )
    reverse = {
        row["source_unit"]
        for row in queue["units"]
        if "WN7" in row.get("candidate_dependencies", [])
    }
    checks.check("WN7 has no reverse source consumer", reverse == set())
    checks.check(
        "all ten direct dependencies are qualified",
        all(units[unit]["disposition"] == "qualified" for unit in DIRECT_DEPENDENCIES),
    )
    checks.check(
        "accepted mappings stay individually pinned and grant no firewall claim",
        all(units[unit]["accepted_claims"] == claims for unit, claims in ACCEPTED_MAPPINGS.items())
        and units["WN7"]["accepted_claims"] == [],
    )
    checks.check(
        "WN7 is terminally qualified without an accepted claim mapping",
        units["WN7"]["disposition"] == "qualified"
        and units["WN7"]["accepted_claims"] == [],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
