#!/usr/bin/env python3
"""Replay the frozen QCD2 dependency and semantic-consumer graph."""

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
    expected_checks: int


NODES = (
    SourceNode("QCD2", "adjudicated_root", "merged-framework/bridges/phase-8/bridge_QCD2_su3_3plus1_lift.py", "64f8125a5c0ef194e23569711036ce6ec46f3ffef2b6eb94a7b5c97ed8bb566f", 10),
    SourceNode("QCD1", "qualified_SU3_predecessor", "merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py", "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed", 11),
    SourceNode("QCD3", "qualified_SU3_algebra_provenance", "merged-framework/bridges/phase-8/bridge_QCD3_asymptotic_freedom.py", "7d7c9a9bc2f04c933fc62484fec3329c0eb7769bb54ba8cd67701da5110af0ca", 9),
    SourceNode("YM2", "qualified_SU2_sibling", "merged-framework/bridges/phase-7/bridge_YM2_yang_mills_3plus1_lift.py", "19c8708ea9b81eff719362ee713dd3d933b5422788759ae6e8933c705863b11c", 10),
    SourceNode("YM1", "qualified_SU2_predecessor", "merged-framework/bridges/phase-7/bridge_YM1_yang_mills_induction.py", "bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6", 9),
    SourceNode("EM7", "qualified_Riesz_dependency", "merged-framework/bridges/phase-3/bridge_EM7_fractal_force_law.py", "c8bf044d846d22eaa652a0f4c11cd5f5e2a51f98e49d0578536fbc4e96f63f22", 17),
    SourceNode("D3S", "qualified_endpoint_provenance", "merged-framework/bridges/phase-19/bridge_D3S_coulomb_from_sg.py", "a5ff9c760cf8776115881d7a2e5e86c562cdf461f61f36784ff95c6381d24d71", 13),
    SourceNode("EM3", "qualified_static_analogy", "merged-framework/bridges/phase-3/bridge_EM3_maxwell_coulomb_tail.py", "1c674bae211322b24a4504ff5aafc04424eb6a4bfe7813f63e5ec4337f783fc9", 11),
    SourceNode("EM5", "qualified_loop_analogy", "merged-framework/bridges/phase-3/bridge_EM5_induced_gauge_sector.py", "bcf2c49e1e98eefea98be0076afd29341ce80fd71a7b141618978139982e4ec0", 11),
    SourceNode("G1", "qualified_gravity_analogy", "merged-framework/bridges/phase-5/bridge_G1_radiating_dilaton_source.py", "580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876", 10),
    SourceNode("G2", "qualified_gravity_analogy", "merged-framework/bridges/phase-5/bridge_G2_gordon_metric_3plus1.py", "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88", 6),
    SourceNode("QCD5", "pending_dimension_consumer", "merged-framework/bridges/phase-8/bridge_QCD5_d3_overdetermination.py", "60a2f5b8dbd76f3b4d6b0a48e4fcd5ed9edbc6a4e1d3869cb4a40bf30c87084c", 7),
    SourceNode("GK1", "pending_boundary_consumer", "merged-framework/bridges/phase-35/bridge_GK1_gauge_kinetic_dimensionality_boundary.py", "c142538897e9168769483aeb978ea86587fa9a073e606aa204316238dfa24d74", 11),
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
    output_tail: str


def _replay(source_root: Path, node: SourceNode) -> ReplayResult:
    path = source_root / node.relative_path
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != node.sha256:
        return ReplayResult(node, -1, -1, -1, -1, -1, 99, False, "", frozenset(), digest)
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
            rf"ALL\s+{node.expected_checks}\s+CHECKS\s+PASS", output
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
            "\n".join(output.splitlines()[-10:]),
        )
    except subprocess.TimeoutExpired as failure:
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
            "\n".join((failure.stdout or "").splitlines()[-10:]),
        )


def run(source_root: Path) -> int:
    checks = CheckLedger("P161-QCD2-SOURCE-GRAPH")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda node: _replay(source_root, node), NODES))
    by_name = {result.node.source_unit: result for result in results}

    checks.check("thirteen frozen source graph nodes", len(results) == 13)
    for result in results:
        detail = result.output_tail if result.returncode or not result.terminal_tally else ""
        checks.check(
            f"{result.node.source_unit} hash shape exit and terminal tally",
            result.check_calls == result.node.expected_checks
            and result.assertions == 1
            and result.returncode == 0
            and result.terminal_tally,
            detail,
        )
        mode = "alias-only" if result.legacy_references else "native"
        print(
            f"SOURCE {result.node.source_unit}: role={result.node.role} "
            f"checks={result.node.expected_checks} mode={mode}"
        )

    checks.check(
        "graph predicate and assertion inventories are fixed",
        sum(result.node.expected_checks for result in results) == 135
        and sum(result.assertions for result in results) == 13,
    )
    checks.check(
        "legacy compatibility is isolated and alias-only",
        {
            result.node.source_unit
            for result in results
            if result.legacy_references
        }
        == {"G1", "YM2", "QCD2"}
        and {
            result.node.source_unit
            for result in results
            if result.eager_fallbacks
        }
        == {"YM2", "QCD2"}
        and by_name["YM2"].current_references == 1
        and by_name["QCD2"].current_references == 1,
    )
    checks.check(
        "QCD2 defines a direct trace-times-kernel product without inversion",
        "return TrTT[a, b] * G_abelian" in by_name["QCD2"].text
        and "THE 3+1D KINETIC-TERM CEILING IS NOT CLOSED HERE" in by_name["QCD2"].text
        and "inv" not in by_name["QCD2"].loaded_names,
    )
    checks.check(
        "YM2 supplies only the already-qualified sibling pattern",
        "return TrTT[a, b] * G_abelian" in by_name["YM2"].text
        and "THE 3+1D KINETIC-TERM CEILING IS NOT CLOSED HERE" in by_name["YM2"].text
        and "inv" not in by_name["YM2"].loaded_names,
    )
    checks.check(
        "QCD1 names QCD2 but contains no dimensional map",
        "QCD2 supplies the 3+1D" in by_name["QCD1"].text
        and "intertwiner" not in by_name["QCD1"].loaded_names
        and "pushforward" not in by_name["QCD1"].loaded_names,
    )
    checks.check(
        "QCD3 supplies independent SU3 algebra not lift authority",
        "QCD1" not in by_name["QCD3"].text
        and "C_A_from_ff" in by_name["QCD3"].loaded_names
        and "G_abelian" not in by_name["QCD3"].loaded_names,
    )
    checks.check(
        "QCD5 repeats one supplied exponent equation across sectors",
        "3 constraints, 1 unknown" in by_name["QCD5"].text
        and "CONDITIONAL on s=1" in by_name["QCD5"].text
        and "d_at_s34" in by_name["QCD5"].loaded_names,
    )
    checks.check(
        "GK1 correctly separates static shape from kinetic normalization",
        "lift_independent_of_geff" in by_name["GK1"].loaded_names
        and "CANNOT close a kinetic-term ceiling" in by_name["GK1"].text
        and "THE 3+1D KINETIC-TERM CEILING IS NOT CLOSED HERE" in by_name["GK1"].text,
    )
    checks.check(
        "D3S cannot authorize the endpoint selection",
        "leading_power = sp.Integer(2)" in by_name["D3S"].text
        and "d=3" in by_name["D3S"].text,
    )
    checks.check(
        "gravity analogies contain no QCD2 construction",
        "QCD2" not in by_name["G1"].text
        and "QCD2" not in by_name["G2"].text,
    )
    checks.check(
        "source graph does not import the accepted canonical QCD2 composition",
        "finite_lie_scalar_qed2_vacuum_polarization" not in by_name["QCD2"].loaded_names
        and "riesz_green_kernel" not in by_name["QCD2"].loaded_names,
    )
    tally = checks.finish()
    print(f"P161 SOURCE GRAPH ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(run(Path(arguments.source_root).resolve()))
