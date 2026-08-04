#!/usr/bin/env python3
"""Replay the pinned QCD1 dependency and semantic-consumer graph."""

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
    SourceNode(
        "EM5",
        "qualified_scalar_loop_source_context",
        "merged-framework/bridges/phase-3/bridge_EM5_induced_gauge_sector.py",
        "bcf2c49e1e98eefea98be0076afd29341ce80fd71a7b141618978139982e4ec0",
        11,
    ),
    SourceNode(
        "W7",
        "qualified_connection_source_context",
        "merged-framework/bridges/phase-6/bridge_W7_su2L_gauging_charged_current.py",
        "1a1fa278f6b8a0cab74d020fc01db1fa3576f57084d0cd80959867c591bf66c3",
        11,
    ),
    SourceNode(
        "YM1",
        "qualified_SU2_predecessor",
        "merged-framework/bridges/phase-7/bridge_YM1_yang_mills_induction.py",
        "bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6",
        9,
    ),
    SourceNode(
        "QCD1",
        "adjudicated_root",
        "merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py",
        "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed",
        11,
    ),
    SourceNode(
        "QCD2",
        "pending_dimensional_lift_consumer",
        "merged-framework/bridges/phase-8/bridge_QCD2_su3_3plus1_lift.py",
        "64f8125a5c0ef194e23569711036ce6ec46f3ffef2b6eb94a7b5c97ed8bb566f",
        10,
    ),
    SourceNode(
        "QCD3",
        "qualified_independent_SU3_algebra_provenance",
        "merged-framework/bridges/phase-8/bridge_QCD3_asymptotic_freedom.py",
        "7d7c9a9bc2f04c933fc62484fec3329c0eb7769bb54ba8cd67701da5110af0ca",
        9,
    ),
    SourceNode(
        "SM1",
        "pending_product_group_consumer",
        "merged-framework/bridges/phase-9/bridge_SM1_combined_gauge_group.py",
        "bb7b70bc2ac0dd703f95ccbbaf843d40e78279f357795b9be74d6eee484749f2",
        6,
    ),
    SourceNode(
        "SM3",
        "pending_trace_index_consumer",
        "merged-framework/bridges/phase-9/bridge_SM3_anomaly_cancellation.py",
        "3ace90aa5377050e4dcab5778996079eea92c9cc56a53c276a60a5508f63b529",
        8,
    ),
    SourceNode(
        "SM4",
        "pending_running_consumer",
        "merged-framework/bridges/phase-9/bridge_SM4_coupling_running_unification.py",
        "c0cc7ed32343afc65cf582d81b2455fdba96d2550e64e3e595e4c995ee53e3ac",
        8,
    ),
    SourceNode(
        "CF3",
        "qualified_algebra_only_consumer",
        "merged-framework/bridges/phase-10/bridge_CF3_wilson_area_law.py",
        "8655579ef3173730c315d60aa821f7085cc131920ae49cb93c60b075d884889d",
        6,
    ),
    SourceNode(
        "WM1",
        "qualified_trace_ratio_consumer",
        "merged-framework/bridges/phase-23/bridge_WM1_sin2thetaw_trace_ratio.py",
        "75dc34e168c39cd0af0a21cd4c7d039088ac74baefb6615ece98f5069f5b8953",
        9,
    ),
    SourceNode(
        "WM2",
        "duplicate_common_induction_consumer",
        "merged-framework/bridges/phase-23/bridge_WM2_common_induction_normalization.py",
        "3c656894fc782dd40dcb495a91de5bbf5a46ec378bb3593eb30d7d4b387f34a3",
        10,
    ),
    SourceNode(
        "WM5",
        "qualified_Casimir_consumer",
        "merged-framework/bridges/phase-33/bridge_WM5_two_loop_coefficients.py",
        "8c3fbfeecb6f98d7d80c47e8f267fe1216dde724b81cc3f73f2a3bb17caf1bbc",
        11,
    ),
    SourceNode(
        "GK1",
        "pending_dimensional_boundary_consumer",
        "merged-framework/bridges/phase-35/bridge_GK1_gauge_kinetic_dimensionality_boundary.py",
        "c142538897e9168769483aeb978ea86587fa9a073e606aa204316238dfa24d74",
        11,
    ),
    SourceNode(
        "WM7",
        "pending_induction_field_content_consumer",
        "merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py",
        "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361",
        10,
    ),
    SourceNode(
        "GK3D1",
        "pending_general_dimension_loop_consumer",
        "merged-framework/bridges/phase-41/bridge_GK3D1_master_polarization_general_D.py",
        "9a25110ba53adfb439d0cfd0570bd311b0a43a20f13d1351f45c3fa4075aeacb",
        19,
    ),
    SourceNode(
        "GK3D4",
        "pending_three_sector_construction_consumer",
        "merged-framework/bridges/phase-41/bridge_GK3D4_three_sectors_one_construction.py",
        "046273d9a06f92ddbe9cd666d3b6de0f321b9709c371aeee8103394dd2a2ad35",
        11,
    ),
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
        return ReplayResult(
            node, -1, -1, -1, -1, -1, 99, False, "", frozenset(), digest
        )
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
    checks = CheckLedger("P160-QCD1-SOURCE-GRAPH")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda node: _replay(source_root, node), NODES))
    by_name = {result.node.source_unit: result for result in results}

    checks.check("seventeen frozen source graph nodes", len(results) == 17)
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
        sum(result.node.expected_checks for result in results) == 170
        and sum(result.assertions for result in results) == 17,
    )
    checks.check(
        "legacy compatibility is isolated to immutable QCD2 and alias only",
        {
            result.node.source_unit
            for result in results
            if result.legacy_references
        }
        == {"QCD2"}
        and {
            result.node.source_unit
            for result in results
            if result.eager_fallbacks
        }
        == {"QCD2"}
        and by_name["QCD2"].current_references == 1,
    )
    checks.check(
        "QCD3 supplies independent accepted SU3 algebra not QCD1 loop authority",
        "QCD1" not in by_name["QCD3"].text
        and "C_A_from_ff" in by_name["QCD3"].loaded_names
        and "Pi_nonabelian" not in by_name["QCD3"].loaded_names,
    )
    checks.check(
        "QCD2 repeats the trace-times-kernel dimensional overclaim",
        "return TrTT[a, b] * G_abelian" in by_name["QCD2"].text
        and "fractional-Laplacian / Riesz family lifts the QCD1" in by_name["QCD2"].text
        and "inv" not in by_name["QCD2"].loaded_names,
    )
    checks.check(
        "qualified CF3 consumes only accepted SU3 algebra from QCD1",
        "NO center, NO loop" in by_name["CF3"].text
        and "TrTT" in by_name["CF3"].loaded_names
        and "Pi_nonabelian" not in by_name["CF3"].loaded_names,
    )
    checks.check(
        "trace and running consumers use already accepted group invariants",
        "T_DYNKIN = R(1, 2)" in by_name["SM3"].text
        and "C_A = 3" in by_name["SM4"].text
        and "T_FUND3 = R(1, 2)" in by_name["WM5"].text
        and all(
            "Pi_nonabelian" not in by_name[name].loaded_names
            for name in ("SM3", "SM4", "WM1", "WM5")
        ),
    )
    checks.check(
        "SM1 executable builds block algebra but not a QCD1 loop",
        "f_proj" in by_name["SM1"].loaded_names
        and "Pi_nonabelian" not in by_name["SM1"].loaded_names
        and "each with a GENERATED kinetic term" in by_name["SM1"].text,
    )
    checks.check(
        "WM2 declares rather than derives the common induction constant",
        "C = sp.Symbol(\"C\", positive=True)" in by_name["WM2"].text
        and "DECLARED      -- the SINGLE-MEDIUM premise" in by_name["WM2"].text
        and "functional_determinant" not in by_name["WM2"].loaded_names,
    )
    checks.check(
        "later induction sources remain separate pending proposals",
        "C2G" in by_name["WM7"].loaded_names
        and "Phase-35's GK1 established the boundary honestly" in by_name["GK3D1"].text
        and "GK3D1-GK3D3 derived the 3+1D term" in by_name["GK3D4"].text
        and "scalar_qed2_vacuum_polarization"
        not in by_name["GK3D4"].loaded_names,
    )
    checks.check(
        "GK1 correctly preserves the QCD1 dimensional ceiling",
        "dim(YM1) = dim(QCD1) = dim(EM5) = 1+1D" in by_name["GK1"].text
        and "THE 3+1D KINETIC-TERM CEILING IS NOT CLOSED HERE" in by_name["GK1"].text,
    )
    tally = checks.finish()
    print(f"P160 SOURCE GRAPH ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(run(Path(arguments.source_root).resolve()))
