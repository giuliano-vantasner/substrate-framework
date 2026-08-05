#!/usr/bin/env python3
"""Verify P198's ten-node MD3 dependency and consumer graph."""

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
    "PN1": ("merged-framework/bridges/phase-30/bridge_PN1_multiphonon_vertex.py", "f2fcd58c97b9e9aa0b92e0ece9d92ff6c7ddaddec1b385b10a68a156ac3df985", 32),
    "PN2": ("merged-framework/bridges/phase-30/bridge_PN2_subdivision_count.py", "66eaa13faaba5bc3ff22d3515e04136b48a1f5a885f7ebfdc980931063c07b3a", 25),
    "PN3": ("merged-framework/bridges/phase-30/bridge_PN3_dicke_collective_scaling.py", "da472079f418368926e27d22567cdf3ad8f32c836146ed8107ae2874f377b58b", 14),
    "WN3": ("merged-framework/bridges/phase-37/bridge_WN3_amplitude_scale_and_multiplicity.py", "8a13c8b2af4d89297a11b3ef7460cc1f35fe274dc4affb2b9a7d3649bc237e88", 48),
    "WN4": ("merged-framework/bridges/phase-37/bridge_WN4_derived_weight_and_crossover.py", "2377bb4ba817cd20c188d4adeeeb9169253e9b1231477ac2069b36cc923fc7e2", 43),
    "WN6": ("merged-framework/bridges/phase-37/bridge_WN6_scale_verdict_and_missing_bridge.py", "07f049bac9eb99cb29ef6c3cd333aaecddc17492a73a8fc2aac7eb140ebcab10", 32),
    "MD3": ("merged-framework/bridges/phase-38/bridge_MD3_vertex_operator_removes_the_single_vacuum_bound.py", "2c50b4cacb8746a35f99c26d9f0edd0227314ab9410677aebc54c29812daf128", 41),
    "MD4": ("merged-framework/bridges/phase-38/bridge_MD4_growth_threshold_and_the_rescue.py", "269b275b2eabddc0f2539ecd22b672692de8790316b91c0f264d98e3582bc144", 34),
    "MD5": ("merged-framework/bridges/phase-38/bridge_MD5_phase32_preserved_and_isotope_handshake.py", "bcc45611ce87312a11cdc35d2bdc4c1a92b2e9fdb44c427f7676701f69326ecb", 63),
    "MD6": ("merged-framework/bridges/phase-38/bridge_MD6_honesty_firewall_and_debt_ledger.py", "08b6d263323e3a09da39152c7409795d97477521f2fcf8d57b295922fefa1cbf", 40),
}
RECORDS = {
    "PN1": ("campaigns/P109-pn1-cosine-mixed-vertex-audit/evidence/source-reproduction.yaml", "61eb61d8a32b53b7f571792f2648ee96a37e1b761a50fef51dc8748d43d18eeb", 32),
    "PN2": ("campaigns/P110-pn2-energy-subdivision-count-audit/evidence/source-reproduction.yaml", "fe04495709fa0a68591fd0526dba4042631799148621efad520b2eaf9aa91af9", 25),
    "PN3": ("campaigns/P111-pn3-symmetric-spin-ladder-audit/evidence/source-reproduction.yaml", "31f1314253a48c20e7dd3ec107687e291f61c4480aee15549145ba07ce997c8f", 14),
    "WN3": ("campaigns/P191-wn3-bosonic-multiplicity-audit/evidence/source-reproduction.yaml", "5860c970728e1605f6217f855e7290b38720cd6a855e9abf9b1d4f891ad50727", 48),
    "WN4": ("campaigns/P192-wn4-derived-weight-crossover-audit/evidence/source-reproduction.yaml", "23e83b021eebd2c72fee0d6432d6d0aa7ecd8a9d38b47257df0a3b6af0067a0b", 43),
    "WN6": ("campaigns/P194-wn6-scale-verdict-audit/evidence/source-reproduction.yaml", "42f0a42b57da16032317b9b43c16cc5564f127eae37119499c3def1007ccd5e6", 32),
    "MD3": ("evidence/source-reproduction.yaml", "3e2539b7c07f94af1e234da4fb219dcf0183c8ec2904e21dff714de88deb3dbb", 41),
}
P196_CONSUMERS = ROOT / "campaigns/P196-md1-mode-counting-audit/evidence/consumer-reproduction.yaml"
P196_CONSUMERS_SHA256 = "6d6373ef1513c6f2891450bbef96311b7566ae35cc02e5837064f9366de41335"
P191_GRAPH_RESULT = ROOT / "campaigns/P191-wn3-bosonic-multiplicity-audit/attempts/0010/result.yaml"
P191_GRAPH_RESULT_SHA256 = "781a7add133853217694abb416c99a961391855f5cc2f3f2d278871e2712dbda"
P191_GRAPH_SCRIPT = ROOT / "campaigns/P191-wn3-bosonic-multiplicity-audit/reviews/replay_source_graph.py"
P191_GRAPH_SCRIPT_SHA256 = "d781fd010cab8cf356bc66ee4eddbd8c6bcb2d4bafd41aa72fe2120b12483fcb"
DIRECT_DEPENDENCIES = {"PN1", "PN2", "PN3", "WN3", "WN4", "WN6"}
DIRECT_CONSUMERS = {"MD4", "MD5", "MD6"}
EXPECTED_MAPPINGS = {
    "PN1": ["C-SG-019"],
    "PN2": [],
    "PN3": ["C-SPN-002"],
    "WN3": ["C-SG-019", "C-CMB-001", "C-OSC-001"],
    "WN4": ["C-OSC-001", "C-CMB-003"],
    "WN6": ["C-SG-019", "C-OSC-001", "C-CMB-003", "C-OSC-002"],
}


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runtime_tally(record: dict) -> int:
    for key in ("runtime_checks", "runtime_check_executions", "executed_checks"):
        if key in record:
            return int(record[key])
    raise KeyError("native record has no runtime tally")


def main() -> int:
    checks = CheckLedger("P198-MD3-SOURCE-GRAPH")
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
    for unit, (relative, expected_hash, expected_tally) in RECORDS.items():
        record_path = CAMPAIGN / relative if unit == "MD3" else ROOT / relative
        record = load(record_path)
        records_valid = records_valid and digest(record_path) == expected_hash
        records_valid = records_valid and runtime_tally(record) == expected_tally
        records_valid = records_valid and record["exit_status"] == 0
    checks.check("seven dependency and root execution records remain pinned", records_valid)

    p196 = load(P196_CONSUMERS)
    checks.check(
        "MD4 and MD6 recent native records remain exact",
        digest(P196_CONSUMERS) == P196_CONSUMERS_SHA256
        and p196["native_replay"]["MD4"]["terminal_tally"] == "ALL_34_CHECKS_PASS"
        and p196["native_replay"]["MD4"]["exit_status"] == 0
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
        "ten unique nodes cover 372 native checks without duplicate execution",
        len(NODES) == 10 and sum(row[2] for row in NODES.values()) == 372,
    )
    checks.check("no graph node requires a legacy quadrature alias", compatibility_events == [])
    checks.check(
        "MD3 direct dependencies are exact and qualified",
        set(units["MD3"]["candidate_dependencies"]) == DIRECT_DEPENDENCIES
        and all(units[unit]["disposition"] == "qualified" for unit in DIRECT_DEPENDENCIES),
    )
    checks.check(
        "all qualified dependencies retain exact accepted mappings",
        all(units[unit]["accepted_claims"] == mapping for unit, mapping in EXPECTED_MAPPINGS.items()),
    )
    reverse = {
        row["source_unit"]
        for row in queue["units"]
        if "MD3" in row.get("candidate_dependencies", [])
    }
    checks.check(
        "MD3 direct reverse consumers are exact and remain pending",
        reverse == DIRECT_CONSUMERS
        and all(
            units[unit]["disposition"] == "pending_adjudication"
            for unit in DIRECT_CONSUMERS
        ),
    )
    proposal = load(CAMPAIGN / "proposal.yaml")
    expected_status = "qualified" if proposal["status"] == "accepted" else "pending_adjudication"
    expected_mapping = ["C-OSC-001", "C-CMB-003", "C-VOP-001"] if expected_status == "qualified" else []
    checks.check(
        "MD3 root authority matches the campaign stage",
        units["MD3"]["disposition"] == expected_status
        and units["MD3"]["accepted_claims"] == expected_mapping,
    )
    checks.check(
        "reused consumer records are not counted as fresh executions",
        load(CAMPAIGN / "evidence/consumer-reproduction.yaml")["total"]
        == {
            "scripts": 3,
            "native_checks_covered": 137,
            "fresh_native_executions": 0,
            "exit_statuses_all_zero": True,
        },
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
