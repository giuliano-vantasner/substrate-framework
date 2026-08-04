#!/usr/bin/env python3
"""Replay the frozen YM2 dependency and semantic-consumer graph."""

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
    SourceNode("YM2", "adjudicated_root", "merged-framework/bridges/phase-7/bridge_YM2_yang_mills_3plus1_lift.py", "19c8708ea9b81eff719362ee713dd3d933b5422788759ae6e8933c705863b11c", 10),
    SourceNode("YM1", "qualified_predecessor", "merged-framework/bridges/phase-7/bridge_YM1_yang_mills_induction.py", "bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6", 9),
    SourceNode("EM7", "qualified_Riesz_dependency", "merged-framework/bridges/phase-3/bridge_EM7_fractal_force_law.py", "c8bf044d846d22eaa652a0f4c11cd5f5e2a51f98e49d0578536fbc4e96f63f22", 17),
    SourceNode("D3S", "qualified_endpoint_provenance", "merged-framework/bridges/phase-19/bridge_D3S_coulomb_from_sg.py", "a5ff9c760cf8776115881d7a2e5e86c562cdf461f61f36784ff95c6381d24d71", 13),
    SourceNode("EM3", "qualified_static_analogy", "merged-framework/bridges/phase-3/bridge_EM3_maxwell_coulomb_tail.py", "1c674bae211322b24a4504ff5aafc04424eb6a4bfe7813f63e5ec4337f783fc9", 11),
    SourceNode("EM5", "qualified_loop_analogy", "merged-framework/bridges/phase-3/bridge_EM5_induced_gauge_sector.py", "bcf2c49e1e98eefea98be0076afd29341ce80fd71a7b141618978139982e4ec0", 11),
    SourceNode("W2", "qualified_representation_provenance", "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9),
    SourceNode("G1", "qualified_gravity_analogy", "merged-framework/bridges/phase-5/bridge_G1_radiating_dilaton_source.py", "580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876", 10),
    SourceNode("G2", "qualified_gravity_analogy", "merged-framework/bridges/phase-5/bridge_G2_gordon_metric_3plus1.py", "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88", 6),
    SourceNode("GK1", "pending_boundary_consumer", "merged-framework/bridges/phase-35/bridge_GK1_gauge_kinetic_dimensionality_boundary.py", "c142538897e9168769483aeb978ea86587fa9a073e606aa204316238dfa24d74", 11),
    SourceNode("QCD1", "pending_SU3_predecessor", "merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py", "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed", 11),
    SourceNode("QCD2", "pending_SU3_sibling", "merged-framework/bridges/phase-8/bridge_QCD2_su3_3plus1_lift.py", "64f8125a5c0ef194e23569711036ce6ec46f3ffef2b6eb94a7b5c97ed8bb566f", 10),
    SourceNode("QCD5", "pending_dimension_consumer", "merged-framework/bridges/phase-8/bridge_QCD5_d3_overdetermination.py", "60a2f5b8dbd76f3b4d6b0a48e4fcd5ed9edbc6a4e1d3869cb4a40bf30c87084c", 7),
    SourceNode("M1", "qualified_normalization_consumer", "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9),
    SourceNode("CF2", "qualified_Riesz_consumer", "merged-framework/bridges/phase-10/bridge_CF2_linear_potential.py", "e9651b9d4db9f23bb54d013a419c2f050725063347e63f253a968781598bfe6a", 15),
    SourceNode("CF3", "qualified_Riesz_consumer", "merged-framework/bridges/phase-10/bridge_CF3_wilson_area_law.py", "8655579ef3173730c315d60aa821f7085cc131920ae49cb93c60b075d884889d", 6),
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
    checks = CheckLedger("P159-YM2-SOURCE-GRAPH")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda node: _replay(source_root, node), NODES))
    by_name = {result.node.source_unit: result for result in results}

    checks.check("sixteen frozen source graph nodes", len(results) == 16)
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
        sum(result.node.expected_checks for result in results) == 165
        and sum(result.assertions for result in results) == 16,
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
        "YM2 defines a direct trace-times-kernel product without inversion",
        "return TrTT[a, b] * G_abelian" in by_name["YM2"].text
        and "THE 3+1D KINETIC-TERM CEILING IS NOT CLOSED HERE" in by_name["YM2"].text
        and "inv" not in by_name["YM2"].loaded_names,
    )
    checks.check(
        "QCD2 repeats the trace-times-kernel and lift overclaim",
        "return TrTT[a, b] * G_abelian" in by_name["QCD2"].text
        and "fractional-Laplacian / Riesz family lifts the QCD1" in by_name["QCD2"].text
        and "inv" not in by_name["QCD2"].loaded_names,
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
        "gravity analogies contain no YM2 construction",
        "YM2" not in by_name["G1"].text
        and "YM2" not in by_name["G2"].text,
    )
    checks.check(
        "qualified Riesz consumers do not depend on YM2",
        "YM2" not in by_name["CF2"].text
        and "YM2" not in by_name["CF3"].text,
    )
    checks.check(
        "accepted predecessor claims do not gain lift authority",
        "YM2" in by_name["YM1"].text
        and "3+1D lift" in by_name["M1"].text
        and "scalar_qed2_vacuum_polarization" not in by_name["YM2"].loaded_names,
    )
    tally = checks.finish()
    print(f"P159 SOURCE GRAPH ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(run(Path(arguments.source_root).resolve()))
