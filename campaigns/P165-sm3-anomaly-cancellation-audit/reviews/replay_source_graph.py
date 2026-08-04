#!/usr/bin/env python3
"""Replay the frozen SM3 dependency and declared reverse-consumer graph."""

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
    static_checks: int
    runtime_checks: int
    assertions: int


NODES = (
    SourceNode("SM3", "adjudicated_root", "merged-framework/bridges/phase-9/bridge_SM3_anomaly_cancellation.py", "3ace90aa5377050e4dcab5778996079eea92c9cc56a53c276a60a5508f63b529", 8, 8, 1),
    SourceNode("M1", "qualified_declared_hypercharge_antecedent_and_prose_consumer", "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9, 9, 1),
    SourceNode("QCD1", "qualified_fundamental_SU3_index_antecedent", "merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py", "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed", 11, 11, 1),
    SourceNode("SM2", "qualified_supplied_table_antecedent_and_reverse_reference", "merged-framework/bridges/phase-9/bridge_SM2_generation_hypercharge_charges.py", "cc5532e86128f010f6801dada96ae1ece5a6be845817127d69cf72810b9e33f1", 7, 7, 1),
    SourceNode("W2", "qualified_fundamental_SU2_boundary_antecedent", "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9, 9, 1),
    SourceNode("WM1", "qualified_retyped_charge_trace_antecedent_and_consumer", "merged-framework/bridges/phase-23/bridge_WM1_sin2thetaw_trace_ratio.py", "75dc34e168c39cd0af0a21cd4c7d039088ac74baefb6615ece98f5069f5b8953", 9, 9, 1),
    SourceNode("WM2", "duplicate_retyped_trace_antecedent_and_consumer", "merged-framework/bridges/phase-23/bridge_WM2_common_induction_normalization.py", "3c656894fc782dd40dcb495a91de5bbf5a46ec378bb3593eb30d7d4b387f34a3", 10, 10, 1),
    SourceNode("WM3", "qualified_running_antecedent_without_charge_selection", "merged-framework/bridges/phase-23/bridge_WM3_sin2thetaw_rg_running.py", "2328ae4d6e66e1caa14a39042c362e57258406383f14ecaa5f5f6c468105e298", 10, 10, 1),
    SourceNode("SM4", "pending_running_prose_consumer", "merged-framework/bridges/phase-9/bridge_SM4_coupling_running_unification.py", "c0cc7ed32343afc65cf582d81b2455fdba96d2550e64e3e595e4c995ee53e3ac", 8, 8, 1),
    SourceNode("CF3", "qualified_triality_prose_consumer", "merged-framework/bridges/phase-10/bridge_CF3_wilson_area_law.py", "8655579ef3173730c315d60aa821f7085cc131920ae49cb93c60b075d884889d", 6, 6, 1),
    SourceNode("FG3", "qualified_symbolic_per_generation_anomaly_consumer", "merged-framework/bridges/phase-11/bridge_FG3_flavor_mixing_matrix.py", "5030cf63716914a0effe2d89de2510c14a1c081784ffa2abfd73d24d982ea7cb", 6, 6, 1),
    SourceNode("FG4", "qualified_family_prose_consumer", "merged-framework/bridges/phase-11/bridge_FG4_cp_kobayashi_maskawa.py", "d9ebb32d440fb87540c7cb2d02a846b76dd4ee405288895308561762cd720ceb", 7, 7, 1),
    SourceNode("WM5", "qualified_dynamic_WM1_table_consumer", "merged-framework/bridges/phase-33/bridge_WM5_two_loop_coefficients.py", "8c3fbfeecb6f98d7d80c47e8f267fe1216dde724b81cc3f73f2a3bb17caf1bbc", 11, 11, 1),
    SourceNode("WM7", "pending_dynamic_WM1_table_consumer", "merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py", "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361", 10, 10, 1),
    SourceNode("GK3D4", "pending_trace_ratio_prose_consumer", "merged-framework/bridges/phase-41/bridge_GK3D4_three_sectors_one_construction.py", "046273d9a06f92ddbe9cd666d3b6de0f321b9709c371aeee8103394dd2a2ad35", 11, 11, 1),
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
    output_tail: str


ALIAS_WRAPPER = (
    "import numpy as np,runpy,sys;"
    "setattr(np,'trapz',np.trapezoid);"
    "runpy.run_path(sys.argv[1],run_name='__main__')"
)


def _replay(source_root: Path, node: SourceNode) -> ReplayResult:
    path = source_root / node.relative_path
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != node.sha256:
        return ReplayResult(node, -1, -1, -1, -1, -1, 99, False, "", digest)
    source = payload.decode("utf-8")
    tree = ast.parse(source, filename=str(path))
    check_calls = sum(
        isinstance(item, ast.Call)
        and isinstance(item.func, ast.Name)
        and item.func.id == "check"
        for item in ast.walk(tree)
    )
    assertions = sum(isinstance(item, ast.Assert) for item in ast.walk(tree))
    compatibility = audit_numpy_trapezoid_compatibility(source, filename=str(path))
    command = [sys.executable, str(path)]
    if compatibility.requires_legacy_alias:
        command = [sys.executable, "-c", ALIAS_WRAPPER, str(path)]
    try:
        completed = subprocess.run(
            command,
            cwd=source_root,
            capture_output=True,
            text=True,
            timeout=240,
            check=False,
        )
        output = completed.stdout + completed.stderr
        terminal = re.search(
            rf"ALL\s+{node.runtime_checks}\s+CHECKS\s+PASS",
            output,
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
            "\n".join(tail.splitlines()[-10:]),
        )


def run(source_root: Path) -> int:
    checks = CheckLedger("P165-SM3-SOURCE-GRAPH")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda node: _replay(source_root, node), NODES))
    by_name = {result.node.source_unit: result for result in results}

    checks.check("fifteen frozen source graph nodes", len(results) == 15)
    for result in results:
        detail = result.output_tail if result.returncode or not result.terminal_tally else ""
        checks.check(
            f"{result.node.source_unit} hash shape exit and terminal tally",
            result.check_calls == result.node.static_checks
            and result.assertions == result.node.assertions
            and result.returncode == 0
            and result.terminal_tally,
            detail,
        )
        mode = "alias-only" if result.legacy_references else "native"
        print(
            f"SOURCE {result.node.source_unit}: role={result.node.role} "
            f"static={result.node.static_checks} runtime={result.node.runtime_checks} "
            f"mode={mode}"
        )

    checks.check(
        "graph lexical runtime and assertion inventories are fixed",
        sum(result.node.static_checks for result in results) == 132
        and sum(result.node.runtime_checks for result in results) == 132
        and sum(result.assertions for result in results) == 15,
    )
    checks.check(
        "all frozen graph nodes are native in the current NumPy environment",
        all(result.legacy_references == 0 for result in results)
        and all(result.eager_fallbacks == 0 for result in results),
    )
    checks.check(
        "root verifies one supplied point but implements no solution classifier",
        "UNIQUE (up to overall scale)" in by_name["SM3"].text
        and "the one true freedom" in by_name["SM3"].text
        and "groebner" not in by_name["SM3"].text.lower()
        and "linsolve" not in by_name["SM3"].text.lower(),
    )
    checks.check(
        "accepted antecedents supply conventions rather than a selected carrier",
        "hypercharge coupling g' and the boson B_mu are DECLARED inputs" in by_name["M1"].text
        and "IMPORTED standard-SM values" in by_name["SM2"].text
        and "NO single shared hypercharge" in by_name["W2"].text,
    )
    checks.check(
        "accepted group antecedent supplies the fixed fundamental index",
        "half_delta = sp.Rational(1, 2) * sp.eye(N)" in by_name["QCD1"].text
        and "SU(3) fundamental Dynkin index" in by_name["QCD1"].text,
    )
    checks.check(
        "trace consumers retype or import supplied tables without executing SM3",
        "FIELDS = [" in by_name["WM1"].text
        and "FIELDS = [" in by_name["WM2"].text
        and "_wm1.FIELDS" in by_name["WM5"].text
        and "_wm1.FIELDS" in by_name["WM7"].text
        and all("_sm3" not in by_name[name].text for name in ("WM1", "WM2", "WM5", "WM7")),
    )
    checks.check(
        "family mixing leaves the anomaly coefficient symbolic rather than proving its zero",
        'A_gen = sp.Symbol("A_gen")' in by_name["FG3"].text
        and "anomaly_mass_basis = A_gen * trace_VdV" in by_name["FG3"].text,
    )
    checks.check(
        "other reverse consumers cite SM3 only as prose provenance",
        all(
            "SM3" in by_name[name].text and "_sm3" not in by_name[name].text
            for name in ("SM4", "CF3", "FG4", "GK3D4")
        ),
    )
    checks.check(
        "running antecedent takes declared low-energy inputs rather than deriving charges",
        "ALPHA_EM_INV" in by_name["WM3"].text
        and "ALPHA_S" in by_name["WM3"].text
        and "FIELDS" not in by_name["WM3"].text,
    )
    tally = checks.finish()
    print(f"P165 SOURCE GRAPH ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(run(Path(arguments.source_root).resolve()))
