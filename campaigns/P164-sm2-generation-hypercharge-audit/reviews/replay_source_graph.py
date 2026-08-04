#!/usr/bin/env python3
"""Replay the frozen SM2 dependency and declared reverse-consumer graph."""

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
    SourceNode("SM2", "adjudicated_root", "merged-framework/bridges/phase-9/bridge_SM2_generation_hypercharge_charges.py", "cc5532e86128f010f6801dada96ae1ece5a6be845817127d69cf72810b9e33f1", 7, 7, 1),
    SourceNode("M1", "qualified_hypercharge_convention_antecedent", "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9, 9, 1),
    SourceNode("W2", "qualified_doublet_antecedent_and_reverse_annotation", "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9, 9, 1),
    SourceNode("SM3", "pending_anomaly_candidate_and_reverse_consumer", "merged-framework/bridges/phase-9/bridge_SM3_anomaly_cancellation.py", "3ace90aa5377050e4dcab5778996079eea92c9cc56a53c276a60a5508f63b529", 8, 8, 1),
    SourceNode("FG2", "qualified_family_count_prose_consumer", "merged-framework/bridges/phase-11/bridge_FG2_family_tower.py", "aef0ed225fca1f12fcccb284015d97ce3faa25291f07addda24e82ebbc5ae166", 7, 7, 3),
    SourceNode("FG3", "qualified_mixing_prose_consumer", "merged-framework/bridges/phase-11/bridge_FG3_flavor_mixing_matrix.py", "5030cf63716914a0effe2d89de2510c14a1c081784ffa2abfd73d24d982ea7cb", 6, 6, 1),
    SourceNode("FG4", "qualified_cp_prose_consumer", "merged-framework/bridges/phase-11/bridge_FG4_cp_kobayashi_maskawa.py", "d9ebb32d440fb87540c7cb2d02a846b76dd4ee405288895308561762cd720ceb", 7, 7, 1),
    SourceNode("WM1", "qualified_retyped_charge_trace_consumer", "merged-framework/bridges/phase-23/bridge_WM1_sin2thetaw_trace_ratio.py", "75dc34e168c39cd0af0a21cd4c7d039088ac74baefb6615ece98f5069f5b8953", 9, 9, 1),
    SourceNode("WM5", "qualified_dynamic_higgs_only_consumer", "merged-framework/bridges/phase-33/bridge_WM5_two_loop_coefficients.py", "8c3fbfeecb6f98d7d80c47e8f267fe1216dde724b81cc3f73f2a3bb17caf1bbc", 11, 11, 1),
    SourceNode("WM6", "qualified_transitive_running_consumer", "merged-framework/bridges/phase-33/bridge_WM6_two_loop_running.py", "6d1ea4245adcf490466974d4a40b24843cd92e883c6e885936fb030cd1b31d57", 11, 11, 1),
    SourceNode("WM7", "pending_dynamic_higgs_and_count_consumer", "merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py", "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361", 10, 10, 1),
    SourceNode("WM8", "pending_scalar_ratio_prose_consumer", "merged-framework/bridges/phase-39/bridge_WM8_corrected_boundary_running.py", "741497f63cc39ee96c71e9a999c49ef9e821cf612d8b48b2959d05f9e6940518", 10, 10, 1),
    SourceNode("WM9", "pending_scalar_count_provenance_consumer", "merged-framework/bridges/phase-39/bridge_WM9_scalar_multiplicity_from_condensate.py", "d0d94417f5abd572e2e306c1f33dc264d42cfef94e4281dbc258ea9fa83ffd4d", 8, 8, 1),
    SourceNode("EL2", "qualified_redeclared_slot_consumer", "merged-framework/bridges/phase-46/bridge_EL2_lepton_is_baryonless_fermion.py", "db90b921e0b3d6966597a39817ad48219cd94fa27ff8aa2a1de4a64c3ccf6965", 11, 11, 3),
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
            rf"ALL\s+{node.runtime_checks}\s+CHECKS\s+PASS", output
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
            "\n".join(tail.splitlines()[-10:]),
        )


def run(source_root: Path) -> int:
    checks = CheckLedger("P164-SM2-SOURCE-GRAPH")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda node: _replay(source_root, node), NODES))
    by_name = {result.node.source_unit: result for result in results}

    checks.check("fourteen frozen source graph nodes", len(results) == 14)
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
        sum(result.node.static_checks for result in results) == 123
        and sum(result.node.runtime_checks for result in results) == 123
        and sum(result.assertions for result in results) == 18,
    )
    checks.check(
        "all frozen graph nodes are native in the current NumPy environment",
        all(result.legacy_references == 0 for result in results)
        and all(result.eager_fallbacks == 0 for result in results),
    )
    checks.check(
        "SM2 imports both the hypercharge table and its target charges",
        "IMPORTED standard-SM values" in by_name["SM2"].text
        and "Observed electric charges (the target" in by_name["SM2"].text,
    )
    checks.check(
        "accepted M1 and W2 leave the physical matter table outside their claims",
        "The hypercharge coupling g' and the boson B_mu are DECLARED inputs"
        in by_name["M1"].text
        and "the U(1)_Y sector is deliberately NOT folded in" in by_name["W2"].text,
    )
    checks.check(
        "pending SM3 uses a distinct left-handed conjugate table and declares its content",
        "LEFT-HANDED Weyl basis" in by_name["SM3"].text
        and '"u_R^c"' in by_name["SM3"].text
        and "DECLARED      -- the matter content" in by_name["SM3"].text,
    )
    checks.check(
        "family consumers cite SM2 only as prose provenance",
        all(
            "SM2" in by_name[name].text and "SM2" not in by_name[name].loaded_names
            for name in ("FG2", "FG3", "FG4")
        ),
    )
    checks.check(
        "WM1 retypes its supplied Weyl table rather than importing SM2",
        "FIELDS = [" in by_name["WM1"].text
        and "SM2" not in by_name["WM1"].loaded_names,
    )
    checks.check(
        "WM5 and pending WM7 dynamically consume only SM2's Higgs row value",
        all(
            "_sm2.Y_H_PS" in by_name[name].text
            and "_sm2.FIELDS" not in by_name[name].text
            for name in ("WM5", "WM7")
        ),
    )
    checks.check(
        "later running and scalar consumers grant no multiplet-table derivation",
        "never re-typed here" in by_name["WM6"].text
        and "SM2 builds ONE Higgs doublet" in by_name["WM8"].text
        and "inherited a count from SM2's construction" in by_name["WM9"].text,
    )
    checks.check(
        "EL2 explicitly redeclares rather than imports the charged-lepton slot",
        "SM2's own table" in by_name["EL2"].text
        and "re-declared" in by_name["EL2"].text
        and "SM2" not in by_name["EL2"].loaded_names,
    )
    tally = checks.finish()
    print(f"P164 SOURCE GRAPH ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(run(Path(arguments.source_root).resolve()))
