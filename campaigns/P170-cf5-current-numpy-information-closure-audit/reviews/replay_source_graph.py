#!/usr/bin/env python3
"""Replay CF5 and its direct CF1/CF2/CF4 narrative graph."""

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
FRAMEWORK_ROOT = Path("/home/dan/substrate-framework")


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
        "CF1", "vortex_inputs_and_repeated_BVP",
        "merged-framework/bridges/phase-10/bridge_CF1_dual_superconductor_flux_tube.py",
        "a4ec97923804f1b7c624b7619bc6b6a1cbb62f42d659897799545b257ca33f5d",
        8, 8, 2,
    ),
    SourceNode(
        "CF2", "fixed_area_tube_equation",
        "merged-framework/bridges/phase-10/bridge_CF2_linear_potential.py",
        "e9651b9d4db9f23bb54d013a419c2f050725063347e63f253a968781598bfe6a",
        15, 15, 1,
    ),
    SourceNode(
        "CF4", "scale_deferral_context",
        "merged-framework/bridges/phase-10/bridge_CF4_dimensional_transmutation.py",
        "e8fa7072d78ba5462ef9410689090f4627528c3632d45afd528c0c118f863c6b",
        6, 6, 1,
    ),
    SourceNode(
        "CF5", "root",
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
    checks = CheckLedger("P170-CF5-SOURCE-GRAPH")
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
            f"{node.label} compatibility-aware replay exits cleanly",
            result.returncode == 0 and result.stderr == "",
            result.stderr[-500:],
        )
        checks.check(
            f"{node.label} runtime tally is exact",
            result.runtime_checks == node.runtime_checks and result.terminal_tally,
        )

    by_label = {result.node.label: result for result in results}
    checks.check(
        "the direct CF5 narrative graph contains exactly four pinned nodes",
        len(results) == 4 and set(by_label) == {"CF1", "CF2", "CF4", "CF5"},
    )
    checks.check(
        "the graph separates thirty-five predicates from six assertions",
        sum(node.lexical_checks for node in NODES) == 35
        and sum(node.runtime_checks for node in NODES) == 35
        and sum(node.assertions for node in NODES) == 6,
    )
    checks.check(
        "only immutable CF1 and CF5 need aliases backed by np.trapezoid",
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

    root_source = by_label["CF5"].source
    checks.check(
        "the CF5 script names CF1 and CF2 but imports neither neighbor",
        all(label in root_source for label in ("CF1", "CF2"))
        and all(
            token not in root_source
            for label in ("CF1", "CF2")
            for token in (f"import bridge_{label}", f"from bridge_{label}")
        ),
    )
    checks.check(
        "CF5 locally duplicates its BVP and inversion rather than importing canonical APIs",
        "def no_rhs" in root_source
        and "def solve_no" in root_source
        and "def sigma_of" in root_source
        and "A_eff = 0.5 * Phi_demo ** 2 / sigma_CF1" in root_source,
    )
    dossier_text = (
        SOURCE_ROOT / "merged-framework/bridges/phase-10/dossiers/CF5-dossier.md"
    ).read_text(encoding="utf-8")
    checks.check(
        "the CF5 dossier supplies the CF4 context and admits a non-unique window",
        "CF4 / scale-deferral" in dossier_text
        and "physical-sensibility window, not a unique prediction" in dossier_text,
    )

    p029 = yaml.safe_load(
        (FRAMEWORK_ROOT / "campaigns/P029-cf5-tension-consistency-audit/adjudication.yaml")
        .read_text(encoding="utf-8")
    )
    checks.check(
        "the accepted P029 adjudication already closes CF5 as duplicate evidence",
        p029["claims"] == []
        and p029["source_disposition"] == {"CF5": "duplicate_evidence"}
        and p029["duplicates"]["CF5"]
        == ["C-VTX-001", "C-VTX-002", "C-FLX-001"]
        and p029["debt"] == [],
    )

    total = checks.finish()
    print(f"P170 CF5 SOURCE GRAPH ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
