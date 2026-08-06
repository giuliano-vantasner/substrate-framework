#!/usr/bin/env python3
"""Replay GC3's immutable dependency and reverse-consumer governance graph."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")
EXPECTED = {
    "EM6": (11, 2),
    "FG2": (7, 3),
    "FG3": (6, 1),
    "FG4": (7, 1),
    "GC1": (9, 2),
    "GC3": (9, 1),
    "GC4": (8, 1),
    "GC5": (8, 1),
    "GC6": (6, 1),
    "MH1": (4, 1),
    "MH2": (5, 2),
    "WM10": (7, 1),
    "WM7": (10, 1),
}
ROOT_MAPPING = [
    "C-QBL-001",
    "C-QBL-003",
    "C-OVL-001",
    "C-MIX-001",
    "C-MIX-002",
    "C-MIX-003",
]
TERMINAL_DEPENDENCIES = {
    "EM6",
    "FG2",
    "FG3",
    "FG4",
    "GC1",
    "MH1",
    "MH2",
    "WM10",
    "WM7",
}
CYCLE_DEPENDENCIES = {"GC4", "GC5"}
REVERSE_CONSUMERS = {"GC4", "GC5", "GC6"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P210-GC3-SOURCE-GRAPH")
    queue = yaml.safe_load((ROOT / "migration/source-claims.yaml").read_text())
    units = {entry["source_unit"]: entry for entry in queue["units"]}
    checks.check(
        "terminal graph node set remains exact",
        set(EXPECTED)
        == TERMINAL_DEPENDENCIES
        | CYCLE_DEPENDENCIES
        | REVERSE_CONSUMERS
        | {"GC3"},
    )
    checks.check(
        "terminal graph totals remain exact",
        len(EXPECTED) == 13
        and sum(value[0] for value in EXPECTED.values()) == 97
        and sum(value[1] for value in EXPECTED.values()) == 18,
    )

    compatibility_results = []
    for name, (expected_checks, expected_assertions) in EXPECTED.items():
        entry = units[name]
        path = SOURCE_ROOT / entry["path"]
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        checks.check(
            f"{name} source hash remains pinned",
            digest(path) == entry["sha256"],
        )
        checks.check(
            f"{name} predicate and assertion inventory remains exact",
            sum(
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "check"
                for node in ast.walk(tree)
            )
            == expected_checks
            and sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
            == expected_assertions,
        )
        compatibility_results.append(
            audit_numpy_trapezoid_compatibility(source, filename=str(path))
        )

    checks.check(
        "all graph nodes have zero quadrature compatibility surface",
        all(
            result.legacy_references
            == result.current_references
            == result.eager_legacy_default_fallbacks
            == 0
            for result in compatibility_results
        ),
    )
    checks.check(
        "all direct authority dependencies are terminal",
        all(units[name]["disposition"] != "pending_adjudication" for name in TERMINAL_DEPENDENCIES),
    )
    checks.check(
        "cycle dependencies remain nonauthoritative",
        all(units[name]["disposition"] == "pending_adjudication" for name in CYCLE_DEPENDENCIES),
    )
    checks.check(
        "reverse consumers remain separately reviewable",
        all(units[name]["disposition"] == "pending_adjudication" for name in REVERSE_CONSUMERS),
    )
    checks.check(
        "GC3 is terminally qualified with the exact mapping",
        units["GC3"]["disposition"] == "qualified"
        and units["GC3"]["accepted_claims"] == ROOT_MAPPING,
    )

    current = yaml.safe_load((ROOT / "governance/releases/current.yaml").read_text())
    checks.check(
        "accepted release contains the new claim and its dependency closure",
        {"C-MIX-001", "C-MIX-002", "C-MIX-003"}
        <= set(current["accepted_claims"]),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
