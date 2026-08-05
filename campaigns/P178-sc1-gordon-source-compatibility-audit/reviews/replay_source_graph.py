#!/usr/bin/env python3
"""Hash-pinned dependency and SC1 reverse-consumer replay for P178."""

from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCES = {
    "G2": (
        SOURCE_ROOT / "merged-framework/bridges/phase-5/bridge_G2_gordon_metric_3plus1.py",
        "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88",
        6,
        1,
    ),
    "G3": (
        SOURCE_ROOT / "merged-framework/bridges/phase-5/bridge_G3_horndeski_scalar_tensor.py",
        "8d462ce2bfd57bfced9fdedd511e9d2711e0c2454bc0d0441c681288495719ba",
        11,
        1,
    ),
    "SC1": (
        SOURCE_ROOT / "merged-framework/bridges/phase-36/bridge_SC1_gordon_coupled_overdetermined.py",
        "70799bff934f1f6986545a0bde0cb94fe016dd4b468b36614ac3e5d9bb74aec0",
        5,
        1,
    ),
    "SC2": (
        SOURCE_ROOT / "merged-framework/bridges/phase-36/bridge_SC2_horndeski_selfconsistent_solve.py",
        "64dfc9c31edd8368cb0e2359ca646fc8f62fe306d6af7a326ff8934070b96425",
        7,
        4,
    ),
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _inventory(path: Path) -> tuple[int, int, object]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    checks = sum(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
        for node in ast.walk(tree)
    )
    assertions = sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
    compatibility = audit_numpy_trapezoid_compatibility(source, filename=str(path))
    return checks, assertions, compatibility


def _run(path: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(path)],
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def main() -> int:
    checks = CheckLedger("P178-SC1-SOURCE-GRAPH")
    observed_predicates = 0
    observed_assertions = 0
    for unit, (path, digest, expected_checks, expected_assertions) in SOURCES.items():
        checks.check(f"{unit} retains its pinned source hash", _digest(path) == digest)
        count, assertions, compatibility = _inventory(path)
        observed_predicates += count
        observed_assertions += assertions
        checks.check(
            f"{unit} retains its lexical predicate and assertion inventory",
            count == expected_checks and assertions == expected_assertions,
        )
        checks.check(
            f"{unit} has no trapezoid-name compatibility event",
            compatibility.legacy_references == 0
            and compatibility.current_references == 0
            and compatibility.eager_legacy_default_fallbacks == 0,
        )
    checks.check(
        "the four-node graph inventories predicates and assertions separately",
        observed_predicates == 29 and observed_assertions == 7,
    )

    queue = yaml.safe_load((ROOT / "migration/source-claims.yaml").read_text())
    entries = {entry["source_unit"]: entry for entry in queue["units"]}
    checks.check(
        "accepted dependency mappings remain individually qualified",
        entries["G2"]["disposition"] == "qualified"
        and entries["G2"]["accepted_claims"] == ["C-GOR-001"]
        and entries["G3"]["disposition"] == "qualified"
        and entries["G3"]["accepted_claims"] == ["C-STG-001"],
    )
    checks.check(
        "SC1 is frozen pending or exactly qualified while SC2 remains pending",
        (
            (
                entries["SC1"]["disposition"] == "pending_adjudication"
                and entries["SC1"]["accepted_claims"] == []
            )
            or (
                entries["SC1"]["disposition"] == "qualified"
                and entries["SC1"]["accepted_claims"]
                == ["C-GOR-001", "C-STG-001", "C-GOR-002"]
            )
        )
        and entries["SC2"]["disposition"] == "pending_adjudication"
        and entries["SC2"]["accepted_claims"] == [],
    )
    checks.check(
        "SC2 explicitly consumes SC1's Gordon-closure prose",
        "SC1" in entries["SC2"]["candidate_dependencies"]
        and "READ TOGETHER WITH SC1" in SOURCES["SC2"][0].read_text(encoding="utf-8"),
    )

    sc1 = _run(SOURCES["SC1"][0], 60)
    checks.check(
        "SC1 native replay executes five predicates with clean status",
        sc1.returncode == 0
        and len(re.findall(r"  PASS$", sc1.stdout, flags=re.MULTILINE)) == 5
        and sc1.stdout.count("ALL 5 CHECKS PASS") == 1,
        sc1.stderr[-500:],
    )
    sc2 = _run(SOURCES["SC2"][0], 600)
    checks.check(
        "SC2 native reverse-consumer replay executes seven predicates",
        sc2.returncode == 0
        and len(re.findall(r"  PASS$", sc2.stdout, flags=re.MULTILINE)) == 7
        and sc2.stdout.count("ALL 7 CHECKS PASS") == 1,
        sc2.stderr[-1000:],
    )
    checks.check(
        "SC2 runtime depends narratively on SC1 but earns no authority here",
        re.search(r"READ TOGETHER WITH SC1", sc2.stdout) is not None
        and re.search(r"Gordon route CANNOT be closed", sc2.stdout) is not None
        and entries["SC2"]["accepted_claims"] == [],
    )

    p142 = yaml.safe_load(
        (ROOT / "campaigns/P142-g2-gordon-metric-audit/adjudication.yaml").read_text()
    )
    p143 = yaml.safe_load(
        (ROOT / "campaigns/P143-g3-scalar-tensor-audit/adjudication.yaml").read_text()
    )
    checks.check(
        "hash-reused G2 and G3 adjudications retain empty debt",
        p142["status"] == "accepted"
        and p142["debt"] == []
        and p142["accepted_mappings"] == ["C-GOR-001"]
        and p143["status"] == "accepted"
        and p143["debt"] == []
        and p143["accepted_mappings"] == ["C-STG-001"],
    )
    checks.check(
        "successful predecessor execution is evidence rather than blanket authority",
        "source evidence only" in (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        or (
            entries["SC1"]["accepted_claims"]
            in ([], ["C-GOR-001", "C-STG-001", "C-GOR-002"])
            and entries["SC2"]["accepted_claims"] == []
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
