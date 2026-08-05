#!/usr/bin/env python3
"""Replay WN1's exact theorem and immutable reverse-consumer closure."""

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
EXPECTED = {
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
EXPECTED_MAPPING = ["C-SG-019", "C-CMB-001"]


def _load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P189-WN1-SOURCE-GRAPH")
    queue = _load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}

    for unit, (relative, expected_hash, expected_tally) in EXPECTED.items():
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
        completed = subprocess.run(
            [str(ROOT / ".venv/bin/python"), str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        tallies = re.findall(r"ALL (\d+) CHECKS PASS", completed.stdout)
        checks.check(
            f"{unit} native replay exits cleanly with its exact tally",
            completed.returncode == 0
            and tallies
            and int(tallies[-1]) == expected_tally,
            completed.stderr[-500:],
        )

    reverse: dict[str, list[str]] = {}
    for row in queue["units"]:
        for dependency in row.get("candidate_dependencies", []):
            reverse.setdefault(dependency, []).append(row["source_unit"])
    checks.check(
        "direct reverse consumers are exact",
        set(reverse.get("WN1", [])) == {"WN2", "WN3", "WN6", "WN7"},
    )
    seen = {"WN1"}
    frontier = ["WN1"]
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
        "reverse closure has four direct and eight depth-two consumers",
        {unit for unit, value in depths.items() if value == 1}
        == {"WN2", "WN3", "WN6", "WN7"}
        and {unit for unit, value in depths.items() if value == 2}
        == {"WN4", "WN5", "MD1", "MD2", "MD3", "MD4", "MD5", "MD6"},
    )

    checks.check(
        "WN1 generated qualification and mappings are exact",
        units["WN1"]["disposition"] == "qualified"
        and units["WN1"]["accepted_claims"] == EXPECTED_MAPPING,
    )
    checks.check(
        "all twelve consumers remain individually pending and unpromoted",
        all(
            units[unit]["disposition"] == "pending_adjudication"
            and units[unit]["accepted_claims"] == []
            for unit in EXPECTED
            if unit != "WN1"
        ),
    )
    dispositions = _load(ROOT / "migration/dispositions.yaml")["units"]
    decision = dispositions["WN1"]
    checks.check(
        "editable WN1 disposition evidence is materialized",
        decision["disposition"] == "qualified"
        and decision["accepted_claims"] == EXPECTED_MAPPING
        and all((ROOT / path).is_file() for path in decision["evidence"]),
    )

    registry = _load(ROOT / "governance/claims.yaml")
    claims = {claim["id"]: claim for claim in registry["claims"]}
    claim = claims["C-CMB-001"]
    checks.check(
        "factorial claim is individually accepted with closed dependency",
        claim["verification"] == "symbolic_verified"
        and claim["review"] == "accepted"
        and claim["compatibility"] == "compatible_extension"
        and claim["epistemic"] == "active"
        and claim["dependencies"] == ["C-SG-019"],
    )
    checks.check(
        "accepted claim keeps coefficient square separate from transition rate",
        "not by itself" in claim["statement"]
        and "transition rate" in claim["statement"]
        and any("Golden-rule" in premise for premise in claim["assumptions"]),
    )
    checks.check(
        "terminal campaign and durable decision records exist",
        (ROOT / "campaigns/P189-wn1-factorial-suppression-audit/adjudication.yaml").is_file()
        and (ROOT / "memory/vantasner/decisions/C-CMB-001-review.md").is_file()
        and (ROOT / "memory/vantasner/decisions/WN1-qualified-review.md").is_file()
        and not (ROOT / "proposals/P189-wn1-factorial-suppression-audit").exists(),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
