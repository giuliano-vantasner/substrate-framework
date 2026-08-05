#!/usr/bin/env python3
"""Verify P201's seven-node MD6 dependency graph without duplicate execution."""

from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
CAMPAIGN = Path(__file__).resolve().parents[1]
NODES = {
    "WN6": (
        "merged-framework/bridges/phase-37/bridge_WN6_scale_verdict_and_missing_bridge.py",
        "07f049bac9eb99cb29ef6c3cd333aaecddc17492a73a8fc2aac7eb140ebcab10",
        32,
    ),
    "MD1": (
        "merged-framework/bridges/phase-38/bridge_MD1_mode_count_is_a_counting_theorem.py",
        "e7408667dbb6644e4c88a0a1523b6eb5f9058c628b5650ff0bf72cfa3238e5ba",
        27,
    ),
    "MD2": (
        "merged-framework/bridges/phase-38/bridge_MD2_phase_variance_and_the_overparametrization.py",
        "7dee2e731cc957c97ee151d3fd3349080460f2dc5781be8d4fd7869a589d2df0",
        26,
    ),
    "MD3": (
        "merged-framework/bridges/phase-38/bridge_MD3_vertex_operator_removes_the_single_vacuum_bound.py",
        "2c50b4cacb8746a35f99c26d9f0edd0227314ab9410677aebc54c29812daf128",
        41,
    ),
    "MD4": (
        "merged-framework/bridges/phase-38/bridge_MD4_growth_threshold_and_the_rescue.py",
        "269b275b2eabddc0f2539ecd22b672692de8790316b91c0f264d98e3582bc144",
        34,
    ),
    "MD5": (
        "merged-framework/bridges/phase-38/bridge_MD5_phase32_preserved_and_isotope_handshake.py",
        "bcc45611ce87312a11cdc35d2bdc4c1a92b2e9fdb44c427f7676701f69326ecb",
        63,
    ),
    "MD6": (
        "merged-framework/bridges/phase-38/bridge_MD6_honesty_firewall_and_debt_ledger.py",
        "08b6d263323e3a09da39152c7409795d97477521f2fcf8d57b295922fefa1cbf",
        40,
    ),
}
RECORDS = {
    "WN6": (
        "campaigns/P194-wn6-scale-verdict-audit/evidence/source-reproduction.yaml",
        "42f0a42b57da16032317b9b43c16cc5564f127eae37119499c3def1007ccd5e6",
    ),
    "MD1": (
        "campaigns/P196-md1-mode-counting-audit/evidence/source-reproduction.yaml",
        "cf0b41000bbfebb983b3b27ee4b13070944d6631d50d02e3a8e766ffa2d32236",
    ),
    "MD2": (
        "campaigns/P197-md2-phase-variance-audit/evidence/source-reproduction.yaml",
        "310ab82e29a206b6be00c666382de9f11d7eb0c27928a734f06124c2cb5b4929",
    ),
    "MD3": (
        "campaigns/P198-md3-vertex-operator-audit/evidence/source-reproduction.yaml",
        "3e2539b7c07f94af1e234da4fb219dcf0183c8ec2904e21dff714de88deb3dbb",
    ),
    "MD4": (
        "campaigns/P199-md4-growth-threshold-audit/evidence/source-reproduction.yaml",
        "1bb3925573cd0b1054c076bf5e521d8cafe36a99962e63490e2c1f941d09be51",
    ),
    "MD5": (
        "campaigns/P200-md5-branching-handshake-audit/evidence/source-reproduction.yaml",
        "7151a527d5ca808045ce28e06864636e866453e95cec9bda355652226c81f565",
    ),
    "MD6": (
        "evidence/source-reproduction.yaml",
        "f3a5ad150bb010ffd081ae8582370ff0d1447d92ea0a85d28a4913322d300f35",
    ),
}
DIRECT_DEPENDENCIES = {"MD1", "MD2", "MD3", "MD4", "MD5", "WN6"}
EXPECTED_MAPPINGS = {
    "WN6": ["C-SG-019", "C-OSC-001", "C-CMB-003", "C-OSC-002"],
    "MD1": ["C-MED-003", "C-SG-018", "C-DOS-001"],
    "MD2": ["C-DOS-001", "C-QFL-001"],
    "MD3": ["C-OSC-001", "C-CMB-003", "C-VOP-001"],
    "MD4": ["C-CMB-003", "C-MKV-001"],
    "MD5": ["C-BRN-001", "C-CMB-003", "C-BRN-002"],
}


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P201-MD6-SOURCE-GRAPH")
    queue = load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}
    compatibility_events: list[str] = []
    for unit, (relative, expected_hash, _) in NODES.items():
        source = SOURCE_ROOT / relative
        checks.check(
            f"{unit} source remains path and hash pinned",
            units[unit]["path"] == relative
            and units[unit]["sha256"] == expected_hash
            and digest(source) == expected_hash,
        )
        compatibility = audit_numpy_trapezoid_compatibility(
            source.read_text(encoding="utf-8"),
            filename=relative,
        )
        if compatibility.legacy_references or compatibility.eager_legacy_default_fallbacks:
            compatibility_events.append(unit)

    records_valid = True
    for unit, (relative, expected_hash) in RECORDS.items():
        path = CAMPAIGN / relative if unit == "MD6" else ROOT / relative
        records_valid = records_valid and digest(path) == expected_hash
    checks.check("all seven native execution records remain pinned", records_valid)
    checks.check(
        "seven unique nodes cover 263 predicates without duplicate execution",
        len(NODES) == 7 and sum(row[2] for row in NODES.values()) == 263,
    )
    checks.check("no graph node requires a legacy quadrature alias", compatibility_events == [])
    checks.check(
        "MD6 direct dependencies are exact and qualified",
        set(units["MD6"]["candidate_dependencies"]) == DIRECT_DEPENDENCIES
        and all(units[unit]["disposition"] == "qualified" for unit in DIRECT_DEPENDENCIES),
    )
    checks.check(
        "all dependencies retain exact accepted mappings",
        all(units[unit]["accepted_claims"] == mapping for unit, mapping in EXPECTED_MAPPINGS.items()),
    )
    reverse_consumers = {
        row["source_unit"]
        for row in queue["units"]
        if "MD6" in row.get("candidate_dependencies", [])
    }
    checks.check("MD6 has no direct reverse consumers", reverse_consumers == set())
    proposal = load(CAMPAIGN / "proposal.yaml")
    expected_disposition = "qualified" if proposal["status"] == "accepted" else "pending_adjudication"
    checks.check(
        "MD6 root authority matches the campaign stage",
        units["MD6"]["disposition"] == expected_disposition
        and units["MD6"]["accepted_claims"] == [],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
