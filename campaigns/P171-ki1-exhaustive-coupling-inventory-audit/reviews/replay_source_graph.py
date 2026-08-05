#!/usr/bin/env python3
"""Replay KI1's direct source graph with its refutation as the expected root result."""

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
    path: str
    sha256: str
    checks: int
    assertions: int
    root_refutation: bool = False


NODES = (
    SourceNode(
        "WZ4", "free_omega_symbol_context",
        "merged-framework/bridges/phase-17/bridge_WZ4_hls_vector_meson_anomalous.py",
        "fca6b9c1d95bdf49e99b863470c7e800880e493b3f716159aa2341f8cf963d2b", 9, 1,
    ),
    SourceNode(
        "E4", "symbolic_BPS_coupling_origin",
        "merged-framework/bridges/phase-29/bridge_E4_bps_zero_binding_resolution.py",
        "f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7", 5, 1,
    ),
    SourceNode(
        "KI1", "refuted_root",
        "merged-framework/bridges/phase-34/bridge_KI1_exhaustive_coupling_search.py",
        "a1ec5f8e64e56165d2c51ad2389ecb455870572ba4ef9eca292151bde4ddb42b", 5, 1,
        True,
    ),
    SourceNode(
        "KI2", "narrative_downstream_consumer",
        "merged-framework/bridges/phase-34/bridge_KI2_epsilon_underdetermination.py",
        "9e16fc6fafa940f43d559ea0f6a9c2730940d1247f36f655375c2f75f6fd1e81", 6, 1,
    ),
    SourceNode(
        "MK1", "later_mu_candidate_counterevidence",
        "merged-framework/bridges/phase-43/bridge_MK1_mu_from_medium_cosine.py",
        "98ff5459ae3c6cb64a9a7632fbaa8613f1f5b1adb68419de25ffa06b1c3a3222", 7, 1,
    ),
    SourceNode(
        "MK2", "later_lambda_candidate_counterevidence",
        "merged-framework/bridges/phase-43/bridge_MK2_lambda_from_medium_omega.py",
        "351136bca28e413ddd54f1b15bf7084dffe32af565fc87e7220d1437a525eb07", 7, 1,
    ),
    SourceNode(
        "MK3", "later_epsilon_candidate_counterevidence",
        "merged-framework/bridges/phase-43/bridge_MK3_epsilon_pinned.py",
        "64254d0f6b9d6ff57f5a8b0a4b86a510e2bef230b4f3bec062533fac59516404", 6, 1,
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
    stdout: str
    stderr: str
    source: str


def _replay(node: SourceNode) -> Replay:
    path = SOURCE_ROOT / node.path
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
        stdout=process.stdout,
        stderr=process.stderr,
        source=source,
    )


def main() -> int:
    checks = CheckLedger("P171-KI1-SOURCE-GRAPH")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(_replay, NODES))

    for result in results:
        node = result.node
        checks.check(f"{node.label} source hash remains pinned", result.digest == node.sha256)
        checks.check(
            f"{node.label} predicate and assertion inventories are exact",
            result.lexical_checks == node.checks and result.assertions == node.assertions,
        )
        checks.check(
            f"{node.label} compatibility surface is explicit and has no eager fallback",
            result.eager_fallbacks == 0
            and result.legacy_references == 0
            and result.current_references == 0,
        )
        if node.root_refutation:
            expected = (
                result.returncode != 0
                and result.stdout.count("  PASS\n") == 1
                and "KI1.1" in result.stdout
                and "CHECK FAILED: KI1.2" in result.stderr
                and "ALL 5 CHECKS PASS" not in result.stdout
            )
            label = "fails exactly at the expected refuted root predicate"
        else:
            expected = (
                result.returncode == 0
                and result.stderr == ""
                and result.stdout.count("  PASS\n") == node.checks
                and f"ALL {node.checks} CHECKS PASS" in result.stdout
            )
            label = "replays cleanly with its exact terminal tally"
        checks.check(f"{node.label} {label}", expected, result.stderr[-500:])

    by_label = {result.node.label: result for result in results}
    checks.check(
        "the typed source graph contains exactly seven pinned nodes",
        set(by_label) == {"WZ4", "E4", "KI1", "KI2", "MK1", "MK2", "MK3"}
        and len(results) == 7,
    )
    checks.check(
        "the graph separates forty-five predicates from seven assertions",
        sum(node.checks for node in NODES) == 45
        and sum(node.assertions for node in NODES) == 7,
    )
    checks.check(
        "no graph node needs a NumPy compatibility alias",
        all(result.legacy_references == 0 for result in results),
    )
    checks.check(
        "KI2 cites KI1 narratively but imports no executable KI1 result",
        "KI1" in by_label["KI2"].source
        and "import bridge_KI1" not in by_label["KI2"].source
        and "from bridge_KI1" not in by_label["KI2"].source,
    )
    checks.check(
        "the later MK counterevidence has the exact KI citation map",
        all(label not in by_label["KI1"].source for label in ("MK1", "MK2", "MK3"))
        and "KI1" not in by_label["MK1"].source
        and "KI1" in by_label["MK2"].source
        and "KI1" not in by_label["MK3"].source
        and all("KI2" in by_label[label].source for label in ("MK1", "MK2", "MK3")),
    )
    checks.check(
        "MK2 still repeats the stale 1502-file KI1 premise despite deriving a candidate route",
        "all 1502 tracked files" in by_label["MK2"].source
        and "lam_expected = N_c / (4 * F_pi)" in by_label["MK2"].source,
    )

    total = checks.finish()
    print(f"P171 KI1 SOURCE GRAPH ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
