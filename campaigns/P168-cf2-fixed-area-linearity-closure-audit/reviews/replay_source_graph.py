#!/usr/bin/env python3
"""Replay CF2 and its five declared narrative neighbors with exact inventories."""

from __future__ import annotations

import ast
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import subprocess
import sys

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE_ROOT = Path("/home/dan/substrate")


@dataclass(frozen=True)
class SourceNode:
    label: str
    relation: str
    relative_path: str
    sha256: str
    lexical_checks: int
    runtime_checks: int
    assertions: int


NODES = (
    SourceNode(
        "EM3", "declared_radial_comparison",
        "merged-framework/bridges/phase-3/bridge_EM3_maxwell_coulomb_tail.py",
        "1c674bae211322b24a4504ff5aafc04424eb6a4bfe7813f63e5ec4337f783fc9",
        11, 11, 1,
    ),
    SourceNode(
        "EM7", "declared_exponent_analogy",
        "merged-framework/bridges/phase-3/bridge_EM7_fractal_force_law.py",
        "c8bf044d846d22eaa652a0f4c11cd5f5e2a51f98e49d0578536fbc4e96f63f22",
        17, 17, 1,
    ),
    SourceNode(
        "QCD3", "declared_uv_premise",
        "merged-framework/bridges/phase-8/bridge_QCD3_asymptotic_freedom.py",
        "7d7c9a9bc2f04c933fc62484fec3329c0eb7769bb54ba8cd67701da5110af0ca",
        9, 9, 1,
    ),
    SourceNode(
        "CF1", "declared_upstream_tube",
        "merged-framework/bridges/phase-10/bridge_CF1_dual_superconductor_flux_tube.py",
        "a4ec97923804f1b7c624b7619bc6b6a1cbb62f42d659897799545b257ca33f5d",
        8, 8, 2,
    ),
    SourceNode(
        "CF2", "root",
        "merged-framework/bridges/phase-10/bridge_CF2_linear_potential.py",
        "e9651b9d4db9f23bb54d013a419c2f050725063347e63f253a968781598bfe6a",
        15, 15, 1,
    ),
    SourceNode(
        "CF5", "later_reconciliation_attempt",
        "merged-framework/bridges/phase-10/bridge_CF5_flux_tube_tension_consistency.py",
        "0a449f8b95bc0a83fb0316992fb0d1776a6157e1445029623b4608246dc256f7",
        6, 6, 2,
    ),
)


@dataclass(frozen=True)
class Replay:
    node: SourceNode
    digest: str
    lexical_checks: int
    assertions: int
    legacy_references: int
    current_references: int
    eager_fallbacks: int
    returncode: int
    stderr: str
    runtime_checks: int
    terminal_tally: bool
    source: str


def _replay(node: SourceNode) -> Replay:
    path = SOURCE_ROOT / node.relative_path
    payload = path.read_bytes()
    source = payload.decode("utf-8")
    tree = ast.parse(source, filename=str(path))
    compatibility = audit_numpy_trapezoid_compatibility(source, filename=str(path))
    if compatibility.requires_legacy_alias:
        code = (
            "import runpy; import numpy as np; "
            "setattr(np, 'trapz', np.trapezoid); "
            f"runpy.run_path({str(path)!r}, run_name='__main__')"
        )
        command = [sys.executable, "-c", code]
    else:
        command = [sys.executable, str(path)]
    process = subprocess.run(
        command,
        cwd=SOURCE_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return Replay(
        node=node,
        digest=hashlib.sha256(payload).hexdigest(),
        lexical_checks=sum(
            isinstance(item, ast.Call)
            and isinstance(item.func, ast.Name)
            and item.func.id == "check"
            for item in ast.walk(tree)
        ),
        assertions=sum(isinstance(item, ast.Assert) for item in ast.walk(tree)),
        legacy_references=compatibility.legacy_references,
        current_references=compatibility.current_references,
        eager_fallbacks=compatibility.eager_legacy_default_fallbacks,
        returncode=process.returncode,
        stderr=process.stderr,
        runtime_checks=process.stdout.count("  PASS\n"),
        terminal_tally=f"ALL {node.runtime_checks} CHECKS PASS" in process.stdout,
        source=source,
    )


def main() -> int:
    checks = CheckLedger("P168-CF2-SOURCE-GRAPH")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(_replay, NODES))

    for result in results:
        node = result.node
        checks.check(
            f"{node.label} hash remains pinned",
            result.digest == node.sha256,
        )
        checks.check(
            f"{node.label} lexical and assertion inventories are exact",
            result.lexical_checks == node.lexical_checks
            and result.assertions == node.assertions,
        )
        checks.check(
            f"{node.label} replay exits cleanly",
            result.returncode == 0 and result.stderr == "",
            result.stderr[-500:],
        )
        checks.check(
            f"{node.label} runtime tally is exact",
            result.runtime_checks == node.runtime_checks and result.terminal_tally,
        )

    by_label = {result.node.label: result for result in results}
    checks.check(
        "the direct narrative graph contains exactly six pinned nodes",
        len(results) == 6 and set(by_label) == {"EM3", "EM7", "QCD3", "CF1", "CF2", "CF5"},
    )
    checks.check(
        "the graph separates sixty-six predicates from eight ledger assertions",
        sum(node.lexical_checks for node in NODES) == 66
        and sum(node.runtime_checks for node in NODES) == 66
        and sum(node.assertions for node in NODES) == 8,
    )
    checks.check(
        "only immutable CF1 and CF5 require legacy-name aliases backed by np.trapezoid",
        {
            label: result.legacy_references
            for label, result in by_label.items()
            if result.legacy_references
        }
        == {"CF1": 3, "CF5": 1}
        and all(result.current_references == 0 for result in results),
    )
    checks.check(
        "the graph contains no eager legacy fallback expression",
        all(result.eager_fallbacks == 0 for result in results),
    )

    root_source = by_label["CF2"].source
    checks.check(
        "CF2 names every graph neighbor narratively",
        all(label in root_source for label in ("EM3", "EM7", "QCD3", "CF1", "CF5")),
    )
    checks.check(
        "CF2 imports none of its narrative neighbors",
        all(
            token not in root_source
            for label in ("EM3", "EM7", "QCD3", "CF1", "CF5")
            for token in (f"import bridge_{label}", f"from bridge_{label}")
        ),
    )
    checks.check(
        "CF2's runtime output does not establish a physical dependency edge",
        "DECLARED -- (Phi, A)" in root_source
        and "NOT IMPORTED -- any absolute sigma number" in root_source,
    )

    total = checks.finish()
    print(f"P168 CF2 SOURCE GRAPH ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
