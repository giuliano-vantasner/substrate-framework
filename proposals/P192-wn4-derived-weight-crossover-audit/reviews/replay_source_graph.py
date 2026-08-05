#!/usr/bin/env python3
"""Replay new WN4 graph evidence and verify hash-identical P191 reuse."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import subprocess

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
PROPOSAL = Path(__file__).resolve().parents[1]
PRIOR_INVENTORY = (
    ROOT
    / "campaigns/P191-wn3-bosonic-multiplicity-audit/evidence/source-graph-inventory.yaml"
)
PRIOR_REPLAY = (
    ROOT
    / "campaigns/P191-wn3-bosonic-multiplicity-audit/reviews/replay_source_graph.py"
)
PRIOR_ATTEMPT = (
    ROOT / "campaigns/P191-wn3-bosonic-multiplicity-audit/attempts/0010/result.yaml"
)
PRIOR_HASHES = {
    PRIOR_INVENTORY: "878596e0e445e93af4cea7e5d12df8dbf5dcfc77e88dc8b73df6be6cb0d020a4",
    PRIOR_REPLAY: "d781fd010cab8cf356bc66ee4eddbd8c6bcb2d4bafd41aa72fe2120b12483fcb",
    PRIOR_ATTEMPT: "781a7add133853217694abb416c99a961391855f5cc2f3f2d278871e2712dbda",
}
EXPECTED = {
    "GB4": ("merged-framework/bridges/phase-32/bridge_GB4_branching_ratio.py", "497ed6deda4a0f11562baeaef0ec7bc21cc20b38d3d11c69ed07728ed33faeb0", 23),
    "PN1": ("merged-framework/bridges/phase-30/bridge_PN1_multiphonon_vertex.py", "f2fcd58c97b9e9aa0b92e0ece9d92ff6c7ddaddec1b385b10a68a156ac3df985", 32),
    "PN2": ("merged-framework/bridges/phase-30/bridge_PN2_subdivision_count.py", "66eaa13faaba5bc3ff22d3515e04136b48a1f5a885f7ebfdc980931063c07b3a", 25),
    "PN3": ("merged-framework/bridges/phase-30/bridge_PN3_dicke_collective_scaling.py", "da472079f418368926e27d22567cdf3ad8f32c836146ed8107ae2874f377b58b", 14),
    "WN1": ("merged-framework/bridges/phase-37/bridge_WN1_vertex_coefficient_magnitude.py", "3764b29955c3bd51c10278159e08a52ff616a7041510e56917b091f1a802cdde", 44),
    "WN2": ("merged-framework/bridges/phase-37/bridge_WN2_coefficient_cannot_be_the_weight.py", "dc9a7dbd79c908d1ec206392cdd81a34b5a39c08dcba31f2c164c3d92073504c", 70),
    "WN3": ("merged-framework/bridges/phase-37/bridge_WN3_amplitude_scale_and_multiplicity.py", "8a13c8b2af4d89297a11b3ef7460cc1f35fe274dc4affb2b9a7d3649bc237e88", 48),
    "WN4": ("merged-framework/bridges/phase-37/bridge_WN4_derived_weight_and_crossover.py", "2377bb4ba817cd20c188d4adeeeb9169253e9b1231477ac2069b36cc923fc7e2", 43),
    "WN5": ("merged-framework/bridges/phase-37/bridge_WN5_gb4_preserved_and_new_prediction.py", "5618ba007e041512a7d207026dc6369c8277312acba4c250219a1629585a7fbc", 41),
    "WN6": ("merged-framework/bridges/phase-37/bridge_WN6_scale_verdict_and_missing_bridge.py", "07f049bac9eb99cb29ef6c3cd333aaecddc17492a73a8fc2aac7eb140ebcab10", 32),
    "WN7": ("merged-framework/bridges/phase-37/bridge_WN7_honesty_firewall_guard.py", "88844689bf682ca5ff524378f4e5e46a25bcab54b1a3a6e59afe69b990694d50", 59),
    "MD1": ("merged-framework/bridges/phase-38/bridge_MD1_mode_count_is_a_counting_theorem.py", "e7408667dbb6644e4c88a0a1523b6eb5f9058c628b5650ff0bf72cfa3238e5ba", 27),
    "MD2": ("merged-framework/bridges/phase-38/bridge_MD2_phase_variance_and_the_overparametrization.py", "7dee2e731cc957c97ee151d3fd3349080460f2dc5781be8d4fd7869a589d2df0", 26),
    "MD3": ("merged-framework/bridges/phase-38/bridge_MD3_vertex_operator_removes_the_single_vacuum_bound.py", "2c50b4cacb8746a35f99c26d9f0edd0227314ab9410677aebc54c29812daf128", 41),
    "MD4": ("merged-framework/bridges/phase-38/bridge_MD4_growth_threshold_and_the_rescue.py", "269b275b2eabddc0f2539ecd22b672692de8790316b91c0f264d98e3582bc144", 34),
    "MD5": ("merged-framework/bridges/phase-38/bridge_MD5_phase32_preserved_and_isotope_handshake.py", "bcc45611ce87312a11cdc35d2bdc4c1a92b2e9fdb44c427f7676701f69326ecb", 63),
    "MD6": ("merged-framework/bridges/phase-38/bridge_MD6_honesty_firewall_and_debt_ledger.py", "08b6d263323e3a09da39152c7409795d97477521f2fcf8d57b295922fefa1cbf", 40),
}
PRIOR_NODES = set(EXPECTED) - {"PN2"}
EXPECTED_DIRECT_DEPENDENCIES = {"GB4", "PN2", "WN3"}
EXPECTED_DIRECT_REVERSE = {"WN2", "WN5", "WN6", "WN7", "MD3"}
EXPECTED_DOWNSTREAM = {"WN5", "WN6", "WN7", "MD1", "MD2", "MD3", "MD4", "MD5", "MD6"}


def _load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P192-WN4-SOURCE-GRAPH")
    queue = _load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}

    for unit, (relative, expected_hash, _) in EXPECTED.items():
        path = SOURCE_ROOT / relative
        checks.check(
            f"{unit} source path and hash remain pinned",
            units[unit]["path"] == relative
            and units[unit]["sha256"] == expected_hash
            and _digest(path) == expected_hash,
        )
        compatibility = audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"),
            filename=relative,
        )
        checks.check(
            f"{unit} has no legacy quadrature compatibility surface",
            compatibility.legacy_references == 0
            and compatibility.eager_legacy_default_fallbacks == 0,
        )

    prior = _load(PRIOR_INVENTORY)
    checks.check(
        "P191 execution evidence remains byte-pinned and reusable",
        all(_digest(path) == expected for path, expected in PRIOR_HASHES.items())
        and prior["actual_native_replay"]["nodes_passed"] == 16
        and prior["actual_native_replay"]["runtime_checks_passed"] == 637
        and prior["actual_native_replay"]["exit_failures"] == 0
        and prior["actual_native_replay"]["compatibility_aliases"] == 0,
    )
    prior_rows = {row["source_unit"]: row for row in prior["nodes"]}
    checks.check(
        "the reused P191 record covers exactly the sixteen unchanged nodes",
        set(prior_rows) == PRIOR_NODES
        and all(
            prior_rows[unit]["sha256"] == EXPECTED[unit][1]
            and prior_rows[unit]["native_tally"] == EXPECTED[unit][2]
            for unit in PRIOR_NODES
        ),
    )

    pn2_path = SOURCE_ROOT / EXPECTED["PN2"][0]
    completed = subprocess.run(
        [str(ROOT / ".venv/bin/python"), str(pn2_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    tallies = re.findall(r"ALL (\d+) CHECKS PASS", completed.stdout)
    checks.check(
        "newly relevant PN2 executes freshly with its exact tally",
        completed.returncode == 0
        and tallies == ["25"]
        and "FAIL:" not in completed.stdout,
        completed.stderr[-500:],
    )
    checks.check(
        "seventeen nodes cover 662 native checks without duplicate execution",
        len(EXPECTED) == 17
        and sum(value[2] for value in EXPECTED.values()) == 662
        and sum(value[2] for key, value in EXPECTED.items() if key != "PN2")
        == 637,
    )
    checks.check(
        "WN4 direct source dependencies are exact",
        set(units["WN4"]["candidate_dependencies"])
        == EXPECTED_DIRECT_DEPENDENCIES,
    )
    reverse: dict[str, set[str]] = {}
    for row in queue["units"]:
        for dependency in row.get("candidate_dependencies", []):
            reverse.setdefault(dependency, set()).add(row["source_unit"])
    checks.check(
        "WN4 direct reverse consumers including the accepted forward cycle are exact",
        reverse.get("WN4", set()) == EXPECTED_DIRECT_REVERSE,
    )
    consumer_audit = _load(PROPOSAL / "evidence/consumer-audit.yaml")
    checks.check(
        "all nine unadjudicated downstream consumers are frozen without promotion",
        set(consumer_audit["direct_source_consumers"]) - {"WN2"}
        | set(consumer_audit["depth_two_consumers"])
        == EXPECTED_DOWNSTREAM
        and consumer_audit["consumer_dispositions_changed"] == []
        and consumer_audit["downstream_claims_promoted"] == [],
    )
    checks.check(
        "source dependencies retain their reviewed authority boundaries",
        units["GB4"]["disposition"] == "qualified"
        and units["GB4"]["accepted_claims"] == ["C-BRN-001"]
        and units["PN2"]["disposition"] == "qualified"
        and units["PN2"]["accepted_claims"] == []
        and units["WN3"]["disposition"] == "qualified"
        and units["WN3"]["accepted_claims"]
        == ["C-SG-019", "C-CMB-001", "C-OSC-001"],
    )
    checks.check(
        "claim source consumer nonduplication and impact reviews are materialized",
        all(
            (PROPOSAL / relative).is_file()
            for relative in (
                "evidence/dependency-audit.yaml",
                "evidence/consumer-audit.yaml",
                "evidence/nonduplication-audit.yaml",
                "evidence/source-graph-inventory.yaml",
                "reviews/C-CMB-003-claim-review.md",
                "reviews/source_adjudication.md",
                "reviews/impact_analysis.md",
            )
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
