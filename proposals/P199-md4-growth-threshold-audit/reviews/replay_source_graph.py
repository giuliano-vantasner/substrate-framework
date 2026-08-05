#!/usr/bin/env python3
"""Verify P199's eleven-node MD4 dependency and consumer graph."""

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
    "AS7": ("merged-framework/bridges/phase-22/bridge_AS7_gravity_confrontation_planck_granularity.py", "710635ddf323b8995dc4a1481aeb8232938d6db14c37bd95a537b26d17df3e0f", 6),
    "MC1": ("merged-framework/bridges/phase-27/bridge_MC1_constitutive_reduction.py", "32ed770bb753a9d1f0e67620a66fa29355e84c430c150694ffdfdb3003a8d3f3", 24),
    "MC3": ("merged-framework/bridges/phase-27/bridge_MC3_per_medium_omega0.py", "74fbddc086781a0d61d5dd22effabf48d7ff37f47c6d97ebde0b2fb6186464a5", 29),
    "MD1": ("merged-framework/bridges/phase-38/bridge_MD1_mode_count_is_a_counting_theorem.py", "e7408667dbb6644e4c88a0a1523b6eb5f9058c628b5650ff0bf72cfa3238e5ba", 27),
    "MD2": ("merged-framework/bridges/phase-38/bridge_MD2_phase_variance_and_the_overparametrization.py", "7dee2e731cc957c97ee151d3fd3349080460f2dc5781be8d4fd7869a589d2df0", 26),
    "MD3": ("merged-framework/bridges/phase-38/bridge_MD3_vertex_operator_removes_the_single_vacuum_bound.py", "2c50b4cacb8746a35f99c26d9f0edd0227314ab9410677aebc54c29812daf128", 41),
    "PN2": ("merged-framework/bridges/phase-30/bridge_PN2_subdivision_count.py", "66eaa13faaba5bc3ff22d3515e04136b48a1f5a885f7ebfdc980931063c07b3a", 25),
    "WN6": ("merged-framework/bridges/phase-37/bridge_WN6_scale_verdict_and_missing_bridge.py", "07f049bac9eb99cb29ef6c3cd333aaecddc17492a73a8fc2aac7eb140ebcab10", 32),
    "MD4": ("merged-framework/bridges/phase-38/bridge_MD4_growth_threshold_and_the_rescue.py", "269b275b2eabddc0f2539ecd22b672692de8790316b91c0f264d98e3582bc144", 34),
    "MD5": ("merged-framework/bridges/phase-38/bridge_MD5_phase32_preserved_and_isotope_handshake.py", "bcc45611ce87312a11cdc35d2bdc4c1a92b2e9fdb44c427f7676701f69326ecb", 63),
    "MD6": ("merged-framework/bridges/phase-38/bridge_MD6_honesty_firewall_and_debt_ledger.py", "08b6d263323e3a09da39152c7409795d97477521f2fcf8d57b295922fefa1cbf", 40),
}
RECORDS = {
    "AS7": ("campaigns/P078-as7-gravity-scale-confrontation/evidence/source-reproduction.yaml", "41c70ee7fd7ee511dbbc30aff6151e29837135b42a1fc6e71bb96227676d209d"),
    "MC1": ("campaigns/P095-mc1-dimensional-sine-gordon/evidence/source-reproduction.yaml", "877314f97c79d4aafbb5b78c0fcce2b5323af3f554189cb7ab649efd3bc5c0a0"),
    "MC3": ("campaigns/P097-mc3-medium-gap-maps/evidence/source-reproduction.yaml", "898e4140b99ac37718a0689eb5d1685dcece5723065b0ca7c382f0057aacea9a"),
    "MD1": ("campaigns/P196-md1-mode-counting-audit/evidence/source-reproduction.yaml", "cf0b41000bbfebb983b3b27ee4b13070944d6631d50d02e3a8e766ffa2d32236"),
    "MD2": ("campaigns/P197-md2-phase-variance-audit/evidence/source-reproduction.yaml", "310ab82e29a206b6be00c666382de9f11d7eb0c27928a734f06124c2cb5b4929"),
    "MD3": ("campaigns/P198-md3-vertex-operator-audit/evidence/source-reproduction.yaml", "3e2539b7c07f94af1e234da4fb219dcf0183c8ec2904e21dff714de88deb3dbb"),
    "PN2": ("campaigns/P110-pn2-energy-subdivision-count-audit/evidence/source-reproduction.yaml", "fe04495709fa0a68591fd0526dba4042631799148621efad520b2eaf9aa91af9"),
    "WN6": ("campaigns/P194-wn6-scale-verdict-audit/evidence/source-reproduction.yaml", "42f0a42b57da16032317b9b43c16cc5564f127eae37119499c3def1007ccd5e6"),
    "MD4": ("evidence/source-reproduction.yaml", "1bb3925573cd0b1054c076bf5e521d8cafe36a99962e63490e2c1f941d09be51"),
}
P196_CONSUMERS = ROOT / "campaigns/P196-md1-mode-counting-audit/evidence/consumer-reproduction.yaml"
P196_CONSUMERS_SHA256 = "6d6373ef1513c6f2891450bbef96311b7566ae35cc02e5837064f9366de41335"
P191_GRAPH_RESULT = ROOT / "campaigns/P191-wn3-bosonic-multiplicity-audit/attempts/0010/result.yaml"
P191_GRAPH_RESULT_SHA256 = "781a7add133853217694abb416c99a961391855f5cc2f3f2d278871e2712dbda"
P191_GRAPH_SCRIPT = ROOT / "campaigns/P191-wn3-bosonic-multiplicity-audit/reviews/replay_source_graph.py"
P191_GRAPH_SCRIPT_SHA256 = "d781fd010cab8cf356bc66ee4eddbd8c6bcb2d4bafd41aa72fe2120b12483fcb"
DIRECT_DEPENDENCIES = {"AS7", "MC1", "MC3", "MD1", "MD2", "MD3", "PN2", "WN6"}
DIRECT_CONSUMERS = {"MD5", "MD6"}
EXPECTED_MAPPINGS = {
    "AS7": ["C-IDN-002", "C-GRV-001", "C-RGE-003", "C-IDN-001", "C-DIM-008", "C-SYM-002"],
    "MC1": ["C-MED-003", "C-SG-001", "C-SG-002", "C-SG-003", "C-SG-017"],
    "MC3": ["C-LAT-001", "C-LAT-002", "C-MED-003", "C-SG-017", "C-SG-018", "C-MED-004"],
    "MD1": ["C-MED-003", "C-SG-018", "C-DOS-001"],
    "MD2": ["C-DOS-001", "C-QFL-001"],
    "MD3": ["C-OSC-001", "C-CMB-003", "C-VOP-001"],
    "PN2": [],
    "WN6": ["C-SG-019", "C-OSC-001", "C-CMB-003", "C-OSC-002"],
}


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P199-MD4-SOURCE-GRAPH")
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
        path = CAMPAIGN / relative if unit == "MD4" else ROOT / relative
        records_valid = records_valid and digest(path) == expected_hash
    checks.check("nine dependency and root execution records remain pinned", records_valid)

    p196 = load(P196_CONSUMERS)
    checks.check(
        "MD6 recent native record remains exact",
        digest(P196_CONSUMERS) == P196_CONSUMERS_SHA256
        and p196["native_replay"]["MD6"]["terminal_tally"] == "ALL_40_CHECKS_PASS"
        and p196["native_replay"]["MD6"]["exit_status"] == 0,
    )
    p191 = load(P191_GRAPH_RESULT)
    checks.check(
        "MD5 byte-pinned graph replay record remains exact",
        digest(P191_GRAPH_RESULT) == P191_GRAPH_RESULT_SHA256
        and digest(P191_GRAPH_SCRIPT) == P191_GRAPH_SCRIPT_SHA256
        and p191["source_graph"]["native_checks"] == 637
        and p191["source_graph"]["replay_result"] == "ALL_56_CHECKS_PASS"
        and '"MD5": ("merged-framework/bridges/phase-38/bridge_MD5' in P191_GRAPH_SCRIPT.read_text(encoding="utf-8"),
    )
    checks.check(
        "eleven unique nodes cover 347 native checks without duplicate execution",
        len(NODES) == 11 and sum(row[2] for row in NODES.values()) == 347,
    )
    checks.check("no graph node requires a legacy quadrature alias", compatibility_events == [])
    checks.check(
        "MD4 direct dependencies are exact and qualified",
        set(units["MD4"]["candidate_dependencies"]) == DIRECT_DEPENDENCIES
        and all(units[unit]["disposition"] == "qualified" for unit in DIRECT_DEPENDENCIES),
    )
    checks.check(
        "all qualified dependencies retain exact accepted mappings",
        all(units[unit]["accepted_claims"] == mapping for unit, mapping in EXPECTED_MAPPINGS.items()),
    )
    reverse = {
        row["source_unit"]
        for row in queue["units"]
        if "MD4" in row.get("candidate_dependencies", [])
    }
    checks.check(
        "MD4 direct reverse consumers are exact and remain pending",
        reverse == DIRECT_CONSUMERS
        and all(units[unit]["disposition"] == "pending_adjudication" for unit in DIRECT_CONSUMERS),
    )
    proposal = load(CAMPAIGN / "proposal.yaml")
    expected_status = "qualified" if proposal["status"] == "accepted" else "pending_adjudication"
    expected_mapping = ["C-CMB-003", "C-MKV-001"] if expected_status == "qualified" else []
    checks.check(
        "MD4 root authority matches the campaign stage",
        units["MD4"]["disposition"] == expected_status
        and units["MD4"]["accepted_claims"] == expected_mapping,
    )
    checks.check(
        "reused consumer records are not counted as fresh executions",
        load(CAMPAIGN / "evidence/consumer-reproduction.yaml")["total"]
        == {
            "scripts": 2,
            "native_checks_covered": 103,
            "fresh_native_executions": 0,
            "exit_statuses_all_zero": True,
        },
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
