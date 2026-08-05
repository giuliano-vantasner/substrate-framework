#!/usr/bin/env python3
"""Verify P196's nine-node MD1 dependency and consumer graph."""

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
    "D3S": ("merged-framework/bridges/phase-19/bridge_D3S_coulomb_from_sg.py", "a5ff9c760cf8776115881d7a2e5e86c562cdf461f61f36784ff95c6381d24d71", 13),
    "MC1": ("merged-framework/bridges/phase-27/bridge_MC1_constitutive_reduction.py", "32ed770bb753a9d1f0e67620a66fa29355e84c430c150694ffdfdb3003a8d3f3", 24),
    "MC2": ("merged-framework/bridges/phase-27/bridge_MC2_dispersion_gap_rejection.py", "b73b5a623ae645b1232b09a3f144eb6429f89fbb0cb130a3d223f42129bacef0", 21),
    "QCD5": ("merged-framework/bridges/phase-8/bridge_QCD5_d3_overdetermination.py", "60a2f5b8dbd76f3b4d6b0a48e4fcd5ed9edbc6a4e1d3869cb4a40bf30c87084c", 7),
    "WN6": ("merged-framework/bridges/phase-37/bridge_WN6_scale_verdict_and_missing_bridge.py", "07f049bac9eb99cb29ef6c3cd333aaecddc17492a73a8fc2aac7eb140ebcab10", 32),
    "MD1": ("merged-framework/bridges/phase-38/bridge_MD1_mode_count_is_a_counting_theorem.py", "e7408667dbb6644e4c88a0a1523b6eb5f9058c628b5650ff0bf72cfa3238e5ba", 27),
    "MD2": ("merged-framework/bridges/phase-38/bridge_MD2_phase_variance_and_the_overparametrization.py", "7dee2e731cc957c97ee151d3fd3349080460f2dc5781be8d4fd7869a589d2df0", 26),
    "MD4": ("merged-framework/bridges/phase-38/bridge_MD4_growth_threshold_and_the_rescue.py", "269b275b2eabddc0f2539ecd22b672692de8790316b91c0f264d98e3582bc144", 34),
    "MD6": ("merged-framework/bridges/phase-38/bridge_MD6_honesty_firewall_and_debt_ledger.py", "08b6d263323e3a09da39152c7409795d97477521f2fcf8d57b295922fefa1cbf", 40),
}
RECORDS = {
    "D3S": ("campaigns/P064-d3s-gap-locality-coulomb/evidence/source-reproduction.yaml", "8fdf4c0c01bb5dc8b25313ef768fc5d14ea88c3336eb9da52ef0f9a8aa2128cd"),
    "MC1": ("campaigns/P095-mc1-dimensional-sine-gordon/evidence/source-reproduction.yaml", "877314f97c79d4aafbb5b78c0fcce2b5323af3f554189cb7ab649efd3bc5c0a0"),
    "MC2": ("campaigns/P096-mc2-dispersion-tail-classification/evidence/source-reproduction.yaml", "7b8b5147c13c3e2aafae2bffa5a682c766800bb556deb60ca815e8f713c2fee9"),
    "QCD5": ("campaigns/P162-qcd5-dimensional-overdetermination-audit/evidence/source-reproduction.yaml", "25e8b6e6d6656dcd92dd5f2f4c20faa319c01855ae0f87708f0abcd02d393064"),
    "WN6": ("campaigns/P194-wn6-scale-verdict-audit/evidence/source-reproduction.yaml", "42f0a42b57da16032317b9b43c16cc5564f127eae37119499c3def1007ccd5e6"),
    "MD1": ("proposals/P196-md1-mode-counting-audit/evidence/source-reproduction.yaml", "cf0b41000bbfebb983b3b27ee4b13070944d6631d50d02e3a8e766ffa2d32236"),
}
CONSUMER_RECORD = PROPOSAL / "evidence/consumer-reproduction.yaml"
CONSUMER_RECORD_SHA256 = "6d6373ef1513c6f2891450bbef96311b7566ae35cc02e5837064f9366de41335"
DIRECT_DEPENDENCIES = {"D3S", "MC1", "MC2", "QCD5", "WN6"}
DIRECT_CONSUMERS = {"MD2", "MD4", "MD6"}


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P196-MD1-SOURCE-GRAPH")
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
            source.read_text(encoding="utf-8"), filename=relative
        )
        if compatibility.legacy_references or compatibility.eager_legacy_default_fallbacks:
            compatibility_events.append(unit)

    checks.check(
        "six dependency and root execution records remain pinned",
        all(digest(ROOT / path) == expected for path, expected in RECORDS.values()),
    )
    consumer_record = load(CONSUMER_RECORD)
    checks.check(
        "three consumer executions remain pinned at one hundred checks",
        digest(CONSUMER_RECORD) == CONSUMER_RECORD_SHA256
        and consumer_record["total"]
        == {"scripts": 3, "checks": 100, "exit_statuses_all_zero": True},
    )
    checks.check(
        "nine unique nodes cover 224 native checks",
        len(NODES) == 9 and sum(row[2] for row in NODES.values()) == 224,
    )
    checks.check(
        "no graph node requires a legacy quadrature alias",
        compatibility_events == [],
    )
    checks.check(
        "MD1 direct dependencies are exact and qualified",
        set(units["MD1"]["candidate_dependencies"]) == DIRECT_DEPENDENCIES
        and all(units[unit]["disposition"] == "qualified" for unit in DIRECT_DEPENDENCIES),
    )
    reverse = {
        row["source_unit"]
        for row in queue["units"]
        if "MD1" in row.get("candidate_dependencies", [])
    }
    checks.check(
        "MD1 direct reverse consumers are exact and remain pending",
        reverse == DIRECT_CONSUMERS
        and all(units[unit]["disposition"] == "pending_adjudication" for unit in DIRECT_CONSUMERS),
    )
    checks.check(
        "MD1 remains pending before claim promotion",
        units["MD1"]["disposition"] == "pending_adjudication"
        and units["MD1"]["accepted_claims"] == [],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())

