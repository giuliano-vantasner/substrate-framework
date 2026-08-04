#!/usr/bin/env python3
"""Replay the frozen QCD5 dependency and semantic-consumer graph."""

from __future__ import annotations

import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
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
    source_unit: str
    role: str
    relative_path: str
    sha256: str
    expected_static_checks: int
    expected_runtime_checks: int
    expected_assertions: int


NODES = (
    SourceNode("QCD5", "adjudicated_root", "merged-framework/bridges/phase-8/bridge_QCD5_d3_overdetermination.py", "60a2f5b8dbd76f3b4d6b0a48e4fcd5ed9edbc6a4e1d3869cb4a40bf30c87084c", 7, 7, 1),
    SourceNode("EM7", "qualified_Riesz_dependency", "merged-framework/bridges/phase-3/bridge_EM7_fractal_force_law.py", "c8bf044d846d22eaa652a0f4c11cd5f5e2a51f98e49d0578536fbc4e96f63f22", 17, 17, 1),
    SourceNode("YM2", "qualified_SU2_lift_analogy", "merged-framework/bridges/phase-7/bridge_YM2_yang_mills_3plus1_lift.py", "19c8708ea9b81eff719362ee713dd3d933b5422788759ae6e8933c705863b11c", 10, 10, 1),
    SourceNode("QCD2", "qualified_SU3_lift_analogy", "merged-framework/bridges/phase-8/bridge_QCD2_su3_3plus1_lift.py", "64f8125a5c0ef194e23569711036ce6ec46f3ffef2b6eb94a7b5c97ed8bb566f", 10, 10, 1),
    SourceNode("D3S", "qualified_rejected_endpoint_selection_provenance", "merged-framework/bridges/phase-19/bridge_D3S_coulomb_from_sg.py", "a5ff9c760cf8776115881d7a2e5e86c562cdf461f61f36784ff95c6381d24d71", 13, 13, 1),
    SourceNode("OD", "qualified_independent_rank_consumer", "merged-framework/bridges/phase-19/bridge_OD_over_determination_test.py", "300259218ca36063625d42487dc1d8f00def4b5d58ef6ffc0b4dc174852fdeb6", 8, 8, 1),
    SourceNode("AS4", "duplicate_overdetermination_consumer", "merged-framework/bridges/phase-21/bridge_AS4_over_determination_v2.py", "cdcfea3ac26c932a3db792c864baa026c761555d3c0e34c7b1bc025ea962745f", 7, 7, 1),
    SourceNode("MD1", "pending_counting_consumer", "merged-framework/bridges/phase-38/bridge_MD1_mode_count_is_a_counting_theorem.py", "e7408667dbb6644e4c88a0a1523b6eb5f9058c628b5650ff0bf72cfa3238e5ba", 19, 27, 0),
)


@dataclass(frozen=True)
class ReplayResult:
    node: SourceNode
    check_calls: int
    assertions: int
    legacy_references: int
    current_references: int
    eager_fallbacks: int
    returncode: int
    terminal_tally: bool
    text: str
    loaded_names: frozenset[str]
    attribute_calls: frozenset[str]
    output_tail: str


def _replay(source_root: Path, node: SourceNode) -> ReplayResult:
    path = source_root / node.relative_path
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != node.sha256:
        return ReplayResult(node, -1, -1, -1, -1, -1, 99, False, "", frozenset(), frozenset(), digest)
    source = payload.decode("utf-8")
    tree = ast.parse(source, filename=str(path))
    check_calls = sum(
        isinstance(item, ast.Call)
        and isinstance(item.func, ast.Name)
        and item.func.id == "check"
        for item in ast.walk(tree)
    )
    assertions = sum(isinstance(item, ast.Assert) for item in ast.walk(tree))
    loaded_names = frozenset(
        item.id
        for item in ast.walk(tree)
        if isinstance(item, ast.Name) and isinstance(item.ctx, ast.Load)
    )
    attribute_calls = frozenset(
        item.func.attr
        for item in ast.walk(tree)
        if isinstance(item, ast.Call) and isinstance(item.func, ast.Attribute)
    )
    compatibility = audit_numpy_trapezoid_compatibility(source, filename=str(path))
    if compatibility.legacy_references:
        wrapper = (
            "import numpy as np, runpy; "
            "np.trapz=np.trapezoid; "
            f"runpy.run_path({str(path)!r}, run_name='__main__')"
        )
        command = [sys.executable, "-c", wrapper]
    else:
        command = [sys.executable, str(path)]
    try:
        completed = subprocess.run(
            command,
            cwd=source_root,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        output = completed.stdout + completed.stderr
        terminal = re.search(
            rf"ALL\s+{node.expected_runtime_checks}\s+CHECKS\s+PASS", output
        ) is not None
        return ReplayResult(
            node,
            check_calls,
            assertions,
            compatibility.legacy_references,
            compatibility.current_references,
            compatibility.eager_legacy_default_fallbacks,
            completed.returncode,
            terminal,
            source,
            loaded_names,
            attribute_calls,
            "\n".join(output.splitlines()[-10:]),
        )
    except subprocess.TimeoutExpired as failure:
        tail = failure.stdout or ""
        if isinstance(tail, bytes):
            tail = tail.decode(errors="replace")
        return ReplayResult(
            node,
            check_calls,
            assertions,
            compatibility.legacy_references,
            compatibility.current_references,
            compatibility.eager_legacy_default_fallbacks,
            124,
            False,
            source,
            loaded_names,
            attribute_calls,
            "\n".join(tail.splitlines()[-10:]),
        )


def run(source_root: Path) -> int:
    checks = CheckLedger("P162-QCD5-SOURCE-GRAPH")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda node: _replay(source_root, node), NODES))
    by_name = {result.node.source_unit: result for result in results}

    checks.check("eight frozen source graph nodes", len(results) == 8)
    for result in results:
        detail = result.output_tail if result.returncode or not result.terminal_tally else ""
        checks.check(
            f"{result.node.source_unit} hash shape exit and terminal tally",
            result.check_calls == result.node.expected_static_checks
            and result.assertions == result.node.expected_assertions
            and result.returncode == 0
            and result.terminal_tally,
            detail,
        )
        mode = "alias-only" if result.legacy_references else "native"
        print(
            f"SOURCE {result.node.source_unit}: role={result.node.role} "
            f"static={result.node.expected_static_checks} "
            f"runtime={result.node.expected_runtime_checks} mode={mode}"
        )

    checks.check(
        "graph predicate and assertion inventories are fixed",
        sum(result.node.expected_static_checks for result in results) == 91
        and sum(result.node.expected_runtime_checks for result in results) == 99
        and sum(result.assertions for result in results) == 7,
    )
    checks.check(
        "legacy compatibility is isolated and alias-only",
        {result.node.source_unit for result in results if result.legacy_references}
        == {"YM2", "QCD2"}
        and {result.node.source_unit for result in results if result.eager_fallbacks}
        == {"YM2", "QCD2"}
        and by_name["YM2"].current_references == 1
        and by_name["QCD2"].current_references == 1,
    )
    checks.check(
        "QCD5 repeats one exponent equation and substitutes count for rank",
        "system = [sp.Eq(force_exp_shared(k), -2) for _, k in SECTORS]"
        in by_name["QCD5"].text
        and "over_determined = n_constraints > n_unknowns" in by_name["QCD5"].text
        and not ({"rank", "rref", "nullspace"} & by_name["QCD5"].attribute_calls),
    )
    checks.check(
        "QCD5 guard b admits the radial exponent is unchanged",
        "the r-power exponent is STILL 2s-d" in by_name["QCD5"].text
        and "sp.diff(sp.log(G), d_sym)" in by_name["QCD5"].text,
    )
    checks.check(
        "QCD5 retains a nonunit endpoint witness and hard-coded absence flag",
        "d_at_s34" in by_name["QCD5"].loaded_names
        and "no_sg_derivation_of_s = True" in by_name["QCD5"].text,
    )
    checks.check(
        "qualified lift analogies provide no accepted endpoint or rank authority",
        "THE 3+1D KINETIC-TERM CEILING IS NOT CLOSED HERE" in by_name["YM2"].text
        and "THE 3+1D KINETIC-TERM CEILING IS NOT CLOSED HERE" in by_name["QCD2"].text
        and not ({"rank", "rref", "nullspace"} & by_name["YM2"].attribute_calls)
        and not ({"rank", "rref", "nullspace"} & by_name["QCD2"].attribute_calls),
    )
    checks.check(
        "D3S takes the leading power as an assigned integer before solving s",
        "leading_power = sp.Integer(2)" in by_name["D3S"].text
        and "s_solved = sp.solve" in by_name["D3S"].text
        and "d=3 is QCD5's, not derived here" in by_name["D3S"].text,
    )
    checks.check(
        "OD uses an explicit rank and nullity diagnostic",
        "rank" in by_name["OD"].attribute_calls
        and "nullity = n_cols - rank_full" in by_name["OD"].text
        and "rank_full == 4 and nullity == 1" in by_name["OD"].text,
    )
    checks.check(
        "AS4 also uses explicit rows rank and nullity",
        "rank" in by_name["AS4"].attribute_calls
        and "M = sp.Matrix([[r[0], r[1]] for r in rows.values()])" in by_name["AS4"].text
        and "nullity = n_unknowns - rank_M" in by_name["AS4"].text,
    )
    checks.check(
        "MD1 consumes d3 as an input to a separate counting theorem",
        "d = 3" in by_name["MD1"].text
        and "N_cells = V/a**3" in by_name["MD1"].text
        and "M_count = 3*N_cells" in by_name["MD1"].text,
    )
    checks.check(
        "EM7 exposes the family rather than an endpoint selection",
        "2s-d-1" in by_name["EM7"].text
        and "NOT DERIVED -- s=1 selection" in by_name["EM7"].text,
    )
    tally = checks.finish()
    print(f"P162 SOURCE GRAPH ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(run(Path(arguments.source_root).resolve()))
