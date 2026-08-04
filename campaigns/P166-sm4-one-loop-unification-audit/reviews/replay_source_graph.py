"""Replay SM4 and its direct executable consumers with semantic inventories."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import subprocess
import sys

from substrate_framework.verification import CheckLedger


ROOT = Path("/home/dan/substrate")


@dataclass(frozen=True)
class SourceNode:
    label: str
    relative_path: str
    sha256: str
    static_checks: int
    runtime_checks: int
    assertions: int


NODES = (
    SourceNode("SM4", "merged-framework/bridges/phase-9/bridge_SM4_coupling_running_unification.py", "c0cc7ed32343afc65cf582d81b2455fdba96d2550e64e3e595e4c995ee53e3ac", 8, 8, 1),
    SourceNode("WM3", "merged-framework/bridges/phase-23/bridge_WM3_sin2thetaw_rg_running.py", "2328ae4d6e66e1caa14a39042c362e57258406383f14ecaa5f5f6c468105e298", 10, 10, 1),
    SourceNode("WM4", "merged-framework/bridges/phase-33/bridge_WM4_nearmiss_identity_map.py", "443406419edc1021a929a6041dec025f73af6d947cf770eebe9cde25d74cd8c9", 11, 11, 1),
    SourceNode("WM5", "merged-framework/bridges/phase-33/bridge_WM5_two_loop_coefficients.py", "8c3fbfeecb6f98d7d80c47e8f267fe1216dde724b81cc3f73f2a3bb17caf1bbc", 11, 11, 1),
    SourceNode("WM7", "merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py", "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361", 10, 10, 1),
)


def _check_count(tree: ast.AST) -> int:
    return sum(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
        for node in ast.walk(tree)
    )


def main() -> int:
    checks = CheckLedger("SM4-DIRECT-CONSUMER-GRAPH")
    for node in NODES:
        path = ROOT / node.relative_path
        payload = path.read_bytes()
        text = payload.decode("utf-8")
        tree = ast.parse(text)
        checks.check(f"{node.label} bytes are hash pinned", hashlib.sha256(payload).hexdigest() == node.sha256)
        checks.check(f"{node.label} static check inventory is exact", _check_count(tree) == node.static_checks)
        checks.check(
            f"{node.label} assertion inventory is exact",
            sum(isinstance(item, ast.Assert) for item in ast.walk(tree)) == node.assertions,
        )
        checks.check(
            f"{node.label} has no legacy numerical integration access",
            all(token not in text for token in ("np.trapz", "getattr(np, \"trapz\"", "getattr(np, 'trapz'")),
        )
        process = subprocess.run(
            [sys.executable, str(path)],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        checks.check(f"{node.label} exits cleanly", process.returncode == 0)
        checks.check(
            f"{node.label} terminal tally is exact",
            f"ALL {node.runtime_checks} CHECKS PASS" in process.stdout
            and process.stdout.count("  PASS\n") == node.runtime_checks,
        )
    checks.check("the direct graph contains five nodes", len(NODES) == 5)
    checks.check("the graph totals fifty lexical and runtime checks", sum(node.static_checks for node in NODES) == 50 and sum(node.runtime_checks for node in NODES) == 50)
    checks.check("the graph totals five assertion nodes", sum(node.assertions for node in NODES) == 5)
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
