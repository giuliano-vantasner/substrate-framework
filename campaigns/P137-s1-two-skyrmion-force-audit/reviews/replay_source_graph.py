from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
import subprocess
import sys

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class SourceNode:
    label: str
    relative_path: str
    sha256: str
    expected_checks: int
    disposition: str
    accepted_claims: tuple[str, ...]
    legacy_references: int = 0
    current_references: int = 0
    eager_fallbacks: int = 0


NODES = (
    SourceNode(
        "T2B",
        "merged-framework/bridges/phase-2/bridge_T2B_dynamic_optionC_EP.py",
        "c6826db8b4199977d602fc5bf92b6e432f60eea1d9805f9e42c1309ccff3c7af",
        8,
        "qualified_dependency",
        ("C-VAR-001", "C-CC-001", "C-VIR-001"),
    ),
    SourceNode(
        "S1",
        "merged-framework/bridges/phase-4/bridge_S1_nn_force_two_skyrmion.py",
        "ebe1ba930be26f17671d8e82779d14fc00e7a8b988a4aada722a32d0d9328ddd",
        11,
        "active_source",
        (),
    ),
    SourceNode(
        "S5",
        "merged-framework/bridges/phase-4/bridge_S5_realizability_magnitude.py",
        "b92a9db67940169fcd9919f83fda6ae8c56b9b9e40b0d2cbebef5539a5dccde6",
        28,
        "qualified_dependency",
        ("C-VIR-001", "C-MED-001", "C-SK-001"),
    ),
    SourceNode(
        "G1",
        "merged-framework/bridges/phase-5/bridge_G1_radiating_dilaton_source.py",
        "580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876",
        10,
        "pending_dependency",
        (),
        legacy_references=2,
    ),
    SourceNode(
        "G2",
        "merged-framework/bridges/phase-5/bridge_G2_gordon_metric_3plus1.py",
        "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88",
        6,
        "pending_dependency",
        (),
    ),
    SourceNode(
        "B1",
        "merged-framework/bridges/phase-7/bridge_B1_disclination_berry_connection.py",
        "2de4faa60ecc1f87ca356afd55c2a531a89327c3c46e4296176052113de7b0b6",
        8,
        "pending_dependency",
        (),
        legacy_references=1,
        current_references=1,
        eager_fallbacks=1,
    ),
    SourceNode(
        "PG4",
        "merged-framework/bridges/phase-18/bridge_PG4_goldberger_treiman.py",
        "e13e68536d14bedb1c8fa7ec10110172d0a1b73e08ce365863013dc7db66f1e9",
        4,
        "qualified_consumer",
        ("C-WID-001", "C-GTR-001"),
    ),
    SourceNode(
        "PN6",
        "merged-framework/bridges/phase-30/bridge_PN6_general_L_lossless_null.py",
        "50ebbf97568fef13e69fc926db3e57457aba4685f3140ac8786bed525e71289f",
        30,
        "qualified_consumer",
        ("C-RES-001",),
    ),
    SourceNode(
        "WN6",
        "merged-framework/bridges/phase-37/bridge_WN6_scale_verdict_and_missing_bridge.py",
        "07f049bac9eb99cb29ef6c3cd333aaecddc17492a73a8fc2aac7eb140ebcab10",
        32,
        "pending_consumer",
        (),
    ),
    SourceNode(
        "WM7",
        "merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py",
        "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361",
        10,
        "pending_consumer",
        (),
    ),
    SourceNode(
        "WM8",
        "merged-framework/bridges/phase-39/bridge_WM8_corrected_boundary_running.py",
        "741497f63cc39ee96c71e9a999c49ef9e821cf612d8b48b2959d05f9e6940518",
        10,
        "pending_consumer",
        (),
    ),
)


ALIAS_WRAPPER = (
    "import numpy as numpy,runpy,sys;"
    "setattr(numpy,'trapz',numpy.trapezoid);"
    "runpy.run_path(sys.argv[1],run_name='__main__')"
)


def main(source_root: str) -> int:
    checks = CheckLedger("P137-S1-SOURCE-GRAPH")
    root = Path(source_root).resolve()
    total_predicates = 0
    alias_nodes = 0

    for node in NODES:
        path = root / node.relative_path
        payload = path.read_bytes()
        checks.check(
            f"{node.label} hash matches pinned source graph",
            hashlib.sha256(payload).hexdigest() == node.sha256,
        )
        compatibility = audit_numpy_trapezoid_compatibility(
            payload.decode("utf-8"), filename=str(path)
        )
        checks.check(
            f"{node.label} compatibility inventory is exact",
            compatibility.legacy_references == node.legacy_references
            and compatibility.current_references == node.current_references
            and compatibility.eager_legacy_default_fallbacks
            == node.eager_fallbacks,
        )
        if compatibility.requires_legacy_alias:
            command = [sys.executable, "-c", ALIAS_WRAPPER, str(path)]
            alias_nodes += 1
        else:
            command = [sys.executable, str(path)]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=240,
        )
        match = re.search(r"ALL\s+(\d+)\s+CHECKS\s+PASS", completed.stdout)
        checks.check(
            f"{node.label} source replay exits cleanly",
            completed.returncode == 0 and "CHECK FAILED" not in completed.stdout,
            detail=completed.stderr[-500:] if completed.stderr else None,
        )
        checks.check(
            f"{node.label} terminal tally is exact",
            match is not None and int(match.group(1)) == node.expected_checks,
            detail=completed.stdout[-500:],
        )
        total_predicates += node.expected_checks
        print(
            f"SOURCE {node.label}: {node.expected_checks} predicates; "
            f"{node.disposition}; alias={compatibility.requires_legacy_alias}"
        )

    checks.check("source graph contains eleven declared nodes", len(NODES) == 11)
    checks.check("source graph replays 157 predicates", total_predicates == 157)
    checks.check("only G1 and B1 need alias-only replay", alias_nodes == 2)
    checks.check(
        "pending dependencies grant no accepted claims",
        all(
            not node.accepted_claims
            for node in NODES
            if node.disposition == "pending_dependency"
        ),
    )
    checks.check(
        "pending consumers grant no accepted claims",
        all(
            not node.accepted_claims
            for node in NODES
            if node.disposition == "pending_consumer"
        ),
    )
    checks.check(
        "qualified consumers remain on claim closures independent of S1",
        next(node for node in NODES if node.label == "PG4").accepted_claims
        == ("C-WID-001", "C-GTR-001")
        and next(node for node in NODES if node.label == "PN6").accepted_claims
        == ("C-RES-001",),
    )
    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
