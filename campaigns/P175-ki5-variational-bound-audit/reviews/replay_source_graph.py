#!/usr/bin/env python3
"""Audit KI5's typed dependency and reverse-consumer graph with evidence reuse."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from pathlib import Path
import subprocess

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


NODES = (
    Node("E1", "qualified_angular_input", "merged-framework/bridges/phase-29/bridge_E1_rational_map_integrals.py", "1afa9ba8ade88912e7361bbbd6f59a9fce5cc114c75ddf604a6439bc066ae2d1", 6, 1),
    Node("E2", "qualified_stationary_profile_input", "merged-framework/bridges/phase-29/bridge_E2_multi_skyrmion_solutions.py", "fdde30878eaf1f8dff7fce9c2d9d4234d1d6e14566be6d2ee56dd1926481c46f", 6, 1),
    Node("E3", "qualified_signed_difference_input", "merged-framework/bridges/phase-29/bridge_E3_yield_coefficient_overbinding.py", "aa76b9e675d4fbb45594e9d3df5107af175e927a24840260ca71ffda1bad3315", 5, 1),
    Node("KI5", "audited_root", "merged-framework/bridges/phase-34/bridge_KI5_kappa_is_not_a_variational_bound.py", "5db475be67e6668f9064096055b0452bb2a762c435132ae324896cce3f9863fe", 5, 1),
    Node("MK5", "pending_direct_reverse_consumer", "merged-framework/bridges/phase-43/bridge_MK5_generalized_solve_kappa.py", "a5ecb5d0d2ba96cf8083a9cfb32ddb44c2a4f4841bf776ebbccb91bc12b246f8", 8, 1),
    Node("MR5", "pending_indirect_reverse_consumer", "merged-framework/bridges/phase-44/bridge_MR5_solve_at_derived_e.py", "0da10adafe3badb7f3eab225543bc601996df45b142f2d59b5d0ddd6dd9117d7", 6, 1),
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
        node=node,
        source=source,
        digest=hashlib.sha256(payload).hexdigest(),
        checks=sum(
            isinstance(item, ast.Call)
            and isinstance(item.func, ast.Name)
            and item.func.id == "check"
            for item in ast.walk(tree)
        ),
        assertions=sum(isinstance(item, ast.Assert) for item in ast.walk(tree)),
        legacy=compatibility.legacy_references,
        current=compatibility.current_references,
        eager=compatibility.eager_legacy_default_fallbacks,
    )


def _acyclic(edges: dict[str, tuple[str, ...]]) -> bool:
    nodes = set(edges) | {target for targets in edges.values() for target in targets}
    indegree = {node: 0 for node in nodes}
    for targets in edges.values():
        for target in targets:
            indegree[target] += 1
    queue = [node for node, degree in indegree.items() if degree == 0]
    visited = 0
    while queue:
        node = queue.pop()
        visited += 1
        for target in edges.get(node, ()):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    return visited == len(nodes)


def main() -> int:
    checks = CheckLedger("P175-KI5-SOURCE-GRAPH")
    paths = [node.path for node in NODES]
    state = subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "status", "--porcelain", "--", *paths],
        check=True, capture_output=True, text=True,
    )
    checks.check("all six pinned graph paths are clean", state.stdout == "", state.stdout)
    inventories = [_inventory(node) for node in NODES]
    for item in inventories:
        checks.check(f"{item.node.label} source hash remains pinned", item.digest == item.node.sha256)
        checks.check(
            f"{item.node.label} predicate and assertion inventories are exact",
            item.checks == item.node.checks and item.assertions == item.node.assertions,
        )
        checks.check(f"{item.node.label} has no eager NumPy legacy fallback", item.eager == 0)

    evidence = {
        "E1": (ROOT / "campaigns/P104-e1-rational-map-angular-audit/attempts/0001/result.yaml", "f76b3ce49fa6c413629b903fdcf9b4185efdfcb996f311aabe8827c6fe74b07f"),
        "E2": (ROOT / "campaigns/P105-e2-rational-map-radial-profiles/attempts/0001/result.yaml", "d8461b153a5ac42be963c5b3940f976c9cdc79ba3b0486d03bd4eb17a1d373e6"),
        "E3": (ROOT / "campaigns/P106-e3-conditional-energy-difference-audit/attempts/0001/result.yaml", "0432bbc4c0150b6850c9aa2f41e8940a1181253cc4c1bf47eac355b2a37e66d5"),
        "MK5_MR5": (ROOT / "campaigns/P174-ki4-backsolve-circularity-audit/attempts/0005/result.yaml", "fca6c61a19d4d34618521e74bba281596e89e1036fa0a144779c37f6383de775"),
    }
    for label, (path, expected) in evidence.items():
        checks.check(f"{label} execution evidence retains pinned bytes", hashlib.sha256(path.read_bytes()).hexdigest() == expected)

    by_label = {item.node.label: item for item in inventories}
    checks.check(
        "the graph has six nodes thirty-six predicate sites and six assertions",
        set(by_label) == {"E1", "E2", "E3", "KI5", "MK5", "MR5"}
        and sum(node.checks for node in NODES) == 36
        and sum(node.assertions for node in NODES) == 6,
    )
    checks.check(
        "E1 E2 E3 and KI5 use current-first lazy NumPy aliases",
        all(by_label[label].legacy == 1 and by_label[label].current == 1 for label in ("E1", "E2", "E3", "KI5"))
        and all(by_label[label].legacy == 0 and by_label[label].current == 0 for label in ("MK5", "MR5")),
    )
    edges = {
        "E1": ("E2", "KI5"),
        "E2": ("E3", "KI5"),
        "E3": ("KI5", "MK5", "MR5"),
        "KI5": ("MK5",),
        "MK5": ("MR5",),
    }
    checks.check("the typed dependency graph is acyclic", _acyclic(edges))
    checks.check(
        "KI5 duplicates E1 E2 and E3 machinery instead of importing governed APIs",
        all(token in by_label["KI5"].source for token in ("I_integral", "solve_profile", "KAPPA_OPT"))
        and "from substrate_framework" not in by_label["KI5"].source,
    )
    checks.check(
        "MK5 directly consumes KI5's no-variational-bound label and stale coordinate",
        "consistent with Phase-34 KI5" in by_label["MK5"].source
        and "8.46" in by_label["MK5"].source,
    )
    checks.check(
        "MR5 indirectly consumes MK5 and E3's stale anchor",
        "MK5 solved the model" in by_label["MR5"].source
        and "E3's kappa = 8.46" in by_label["MR5"].source,
    )

    inventory = yaml.safe_load((ROOT / "migration/source-claims.yaml").read_text(encoding="utf-8"))
    units = {entry["source_unit"]: entry for entry in inventory["units"]}
    checks.check(
        "qualified dependencies and audited root plus pending consumers remain typed",
        all(units[label]["disposition"] == "qualified" for label in ("E1", "E2", "E3"))
        and units["KI5"]["disposition"] == "qualified"
        and all(units[label]["disposition"] == "pending_adjudication" for label in ("MK5", "MR5")),
    )
    checks.check(
        "KI5 maps existing claims while pending consumers supply no accepted authority",
        set(units["KI5"]["accepted_claims"]) == {"C-RDIFF-001", "C-RDIFF-002", "C-RPROF-002"}
        and all(units[label]["accepted_claims"] == [] for label in ("MK5", "MR5")),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
