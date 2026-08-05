#!/usr/bin/env python3
"""Audit KI4's typed source graph with proportional execution reuse."""

from __future__ import annotations

import ast
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import subprocess
import sys

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE_ROOT = Path("/home/dan/substrate")
ROOT = Path("/home/dan/substrate-framework")


@dataclass(frozen=True)
class Node:
    label: str
    relation: str
    path: str
    sha256: str
    checks: int
    assertions: int
    execute: bool = False


NODES = (
    Node("E3", "qualified_comparator_context", "merged-framework/bridges/phase-29/bridge_E3_yield_coefficient_overbinding.py", "aa76b9e675d4fbb45594e9d3df5107af175e927a24840260ca71ffda1bad3315", 5, 1),
    Node("KI2", "qualified_parameter_family_context", "merged-framework/bridges/phase-34/bridge_KI2_epsilon_underdetermination.py", "9e16fc6fafa940f43d559ea0f6a9c2730940d1247f36f655375c2f75f6fd1e81", 6, 1),
    Node("KI3", "qualified_inverse_example_context", "merged-framework/bridges/phase-34/bridge_KI3_bracket_is_sharp.py", "10e92457cbd213782e5778f5b739660a6d07ea229c44746e24fe0132844fcbd3", 5, 1),
    Node("KI4", "audited_root", "merged-framework/bridges/phase-34/bridge_KI4_backsolve_circularity.py", "138f204c2bf7e7278a1a4aadad4bed1680e11b6b6de7189a02640a81652f00cd", 5, 1),
    Node("MK3", "pending_direct_reverse_consumer", "merged-framework/bridges/phase-43/bridge_MK3_epsilon_pinned.py", "64254d0f6b9d6ff57f5a8b0a4b86a510e2bef230b4f3bec062533fac59516404", 6, 1, True),
    Node("MK5", "pending_direct_reverse_consumer", "merged-framework/bridges/phase-43/bridge_MK5_generalized_solve_kappa.py", "a5ecb5d0d2ba96cf8083a9cfb32ddb44c2a4f4841bf776ebbccb91bc12b246f8", 8, 1),
    Node("MR5", "pending_direct_reverse_consumer", "merged-framework/bridges/phase-44/bridge_MR5_solve_at_derived_e.py", "0da10adafe3badb7f3eab225543bc601996df45b142f2d59b5d0ddd6dd9117d7", 6, 1, True),
)


@dataclass(frozen=True)
class Inventory:
    node: Node
    source: str
    digest: str
    checks: int
    assertions: int
    legacy: int
    current: int
    eager: int


def _inventory(node: Node) -> Inventory:
    path = SOURCE_ROOT / node.path
    payload = path.read_bytes()
    source = payload.decode("utf-8")
    tree = ast.parse(source, filename=str(path))
    compatibility = audit_numpy_trapezoid_compatibility(source, filename=str(path))
    return Inventory(
        node, source, hashlib.sha256(payload).hexdigest(),
        sum(isinstance(item, ast.Call) and isinstance(item.func, ast.Name) and item.func.id == "check" for item in ast.walk(tree)),
        sum(isinstance(item, ast.Assert) for item in ast.walk(tree)),
        compatibility.legacy_references, compatibility.current_references,
        compatibility.eager_legacy_default_fallbacks,
    )


def _execute(item: Inventory) -> subprocess.CompletedProcess[str]:
    path = SOURCE_ROOT / item.node.path
    command = [sys.executable, str(path)]
    if item.legacy and not item.current:
        command = [sys.executable, "-c", (
            "import runpy; import numpy as np; setattr(np, 'trapz', np.trapezoid); "
            f"runpy.run_path({str(path)!r}, run_name='__main__')"
        )]
    return subprocess.run(
        command, cwd=SOURCE_ROOT, check=False, capture_output=True, text=True,
        timeout=300, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def main() -> int:
    checks = CheckLedger("P174-KI4-SOURCE-GRAPH")
    paths = [node.path for node in NODES]
    state = subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "status", "--porcelain", "--", *paths],
        check=True, capture_output=True, text=True,
    )
    checks.check("all pinned graph paths are clean", state.stdout == "", state.stdout)
    inventories = [_inventory(node) for node in NODES]
    for item in inventories:
        checks.check(f"{item.node.label} source hash remains pinned", item.digest == item.node.sha256)
        checks.check(
            f"{item.node.label} predicate and assertion inventories are exact",
            item.checks == item.node.checks and item.assertions == item.node.assertions,
        )
        checks.check(f"{item.node.label} has no eager NumPy legacy fallback", item.eager == 0)

    prior_graph = ROOT / "campaigns/P173-ki3-bracket-sharpness-audit/attempts/0010/result.yaml"
    current_native = ROOT / "campaigns/P174-ki4-backsolve-circularity-audit/attempts/0002/result.yaml"
    checks.check(
        "unchanged E3 KI2 KI3 and MK5 executions reuse P173's pinned graph result",
        hashlib.sha256(prior_graph.read_bytes()).hexdigest() == "6bc3b16bc21c767615250d77efc9db8d92cdeba8e6df4e274d4536fb3b3c280c",
    )
    checks.check(
        "KI4 execution reuses P174's native reproduction",
        hashlib.sha256(current_native.read_bytes()).hexdigest() == "901ae902561729eb9fd71b89b81843d62e82d8dd3a7eab9f4d0f6169a84d790a",
    )
    fresh = [item for item in inventories if item.node.execute]
    with ThreadPoolExecutor(max_workers=2) as pool:
        executions = list(pool.map(_execute, fresh))
    for item, process in zip(fresh, executions, strict=True):
        checks.check(
            f"{item.node.label} freshly replays its local terminal tally",
            process.returncode == 0 and process.stderr == ""
            and f"ALL {item.node.checks} CHECKS PASS" in process.stdout,
            process.stderr[-500:],
        )

    by_label = {item.node.label: item for item in inventories}
    checks.check(
        "the graph has seven typed nodes and forty-one predicate sites",
        set(by_label) == {"E3", "KI2", "KI3", "KI4", "MK3", "MK5", "MR5"}
        and sum(node.checks for node in NODES) == 41
        and sum(node.assertions for node in NODES) == 7,
    )
    checks.check(
        "E3 alone has a current-first lazy compatibility reference",
        by_label["E3"].legacy == 1 and by_label["E3"].current == 1
        and all(item.legacy == 0 for label, item in by_label.items() if label != "E3"),
    )
    root = by_label["KI4"].source
    checks.check(
        "KI4 narratively imports E3 KI2 and KI3 but no governed API",
        all(token in root for token in ("E3", "KI2", "KI3")) and "from substrate_framework" not in root,
    )
    checks.check(
        "three pending descendants explicitly consume KI4's circularity label",
        all("KI4" in by_label[label].source and "circular" in by_label[label].source.lower()
            for label in ("MK3", "MK5", "MR5")),
    )
    inventory = yaml.safe_load((ROOT / "migration/source-claims.yaml").read_text(encoding="utf-8"))
    units = {entry["source_unit"]: entry for entry in inventory["units"]}
    checks.check(
        "qualified inputs and pending root and descendants remain typed",
        all(units[label]["disposition"] == "qualified" for label in ("E3", "KI2", "KI3"))
        and all(units[label]["disposition"] == "pending_adjudication" for label in ("KI4", "MK3", "MK5", "MR5")),
    )
    checks.check(
        "pending descendants supply no accepted claim authority",
        all(units[label]["accepted_claims"] == [] for label in ("KI4", "MK3", "MK5", "MR5")),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
