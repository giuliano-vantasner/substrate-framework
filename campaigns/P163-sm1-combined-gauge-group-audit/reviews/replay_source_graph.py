#!/usr/bin/env python3
"""Replay the frozen SM1 antecedent and semantic-sibling source graph."""

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
    SourceNode("SM1", "adjudicated_root", "merged-framework/bridges/phase-9/bridge_SM1_combined_gauge_group.py", "bb7b70bc2ac0dd703f95ccbbaf843d40e78279f357795b9be74d6eee484749f2", 6, 6, 1),
    SourceNode("EM2", "qualified_U1_antecedent", "merged-framework/bridges/phase-3/bridge_EM2_gauge_u1_minimal_coupling.py", "9787ae25521e19d926de0f9addafd16353bebc149cea83f3d9dd4c491fef91d6", 11, 11, 1),
    SourceNode("W2", "qualified_SU2_representation_antecedent", "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9, 9, 1),
    SourceNode("YM1", "qualified_SU2_loop_antecedent", "merged-framework/bridges/phase-7/bridge_YM1_yang_mills_induction.py", "bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6", 9, 9, 1),
    SourceNode("QCD1", "qualified_SU3_antecedent", "merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py", "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed", 11, 11, 1),
    SourceNode("SM2", "pending_representation_table_sibling", "merged-framework/bridges/phase-9/bridge_SM2_generation_hypercharge_charges.py", "cc5532e86128f010f6801dada96ae1ece5a6be845817127d69cf72810b9e33f1", 7, 7, 1),
    SourceNode("SM3", "pending_anomaly_table_sibling", "merged-framework/bridges/phase-9/bridge_SM3_anomaly_cancellation.py", "3ace90aa5377050e4dcab5778996079eea92c9cc56a53c276a60a5508f63b529", 8, 8, 1),
    SourceNode("SM4", "pending_running_sibling", "merged-framework/bridges/phase-9/bridge_SM4_coupling_running_unification.py", "c0cc7ed32343afc65cf582d81b2455fdba96d2550e64e3e595e4c995ee53e3ac", 8, 8, 1),
    SourceNode("GK1", "pending_dimensional_boundary_consumer", "merged-framework/bridges/phase-35/bridge_GK1_gauge_kinetic_dimensionality_boundary.py", "c142538897e9168769483aeb978ea86587fa9a073e606aa204316238dfa24d74", 11, 11, 1),
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
    completed = subprocess.run(
        [sys.executable, str(path)],
        cwd=source_root,
        capture_output=True,
        text=True,
        timeout=120,
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


def run(source_root: Path) -> int:
    checks = CheckLedger("P163-SM1-SOURCE-GRAPH")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda node: _replay(source_root, node), NODES))
    by_name = {result.node.source_unit: result for result in results}

    checks.check("nine frozen source graph nodes", len(results) == 9)
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
        print(
            f"SOURCE {result.node.source_unit}: role={result.node.role} "
            f"static={result.node.static_checks} runtime={result.node.runtime_checks} mode=native"
        )

    checks.check(
        "graph static runtime and assertion inventories are fixed",
        sum(result.node.static_checks for result in results) == 80
        and sum(result.node.runtime_checks for result in results) == 80
        and sum(result.assertions for result in results) == 9,
    )
    checks.check(
        "all graph nodes are native current-environment sources",
        all(result.legacy_references == 0 for result in results)
        and all(result.eager_fallbacks == 0 for result in results),
    )
    checks.check(
        "SM1 substitutes a nonzero weight only inside its rank probe",
        'Y = sp.Symbol("Y", real=True)' in by_name["SM1"].text
        and "YB6.subs(Y, 1)" in by_name["SM1"].text,
    )
    checks.check(
        "SM1 supplies local matrices but no global group discriminator",
        "DIRECT PRODUCT" in by_name["SM1"].text
        and "quotient" not in by_name["SM1"].text.lower()
        and "kernel" not in by_name["SM1"].text.lower(),
    )
    checks.check(
        "EM2 explicitly leaves the Maxwell kinetic term ungenerated",
        "the Maxwell kinetic term is NOT generated here" in by_name["EM2"].text,
    )
    checks.check(
        "W2 explicitly leaves bosons coupling and kinetic term absent",
        "No dynamical W/Z boson, no coupling g, no Yang-Mills kinetic" in by_name["W2"].text
        and "gauge_field_built" in by_name["W2"].loaded_names,
    )
    checks.check(
        "YM1 and QCD1 retain their one-plus-one-dimensional source ceilings",
        "this is the 1+1D induction" in by_name["YM1"].text
        and "this is the 1+1D induction" in by_name["QCD1"].text,
    )
    checks.check(
        "SM2 imports rather than derives its representation table",
        "IMPORTED standard-SM values" in by_name["SM2"].text
        and "Rep ASSIGNMENT imported" in by_name["SM2"].text,
    )
    checks.check(
        "SM3 separately declares the matter content and charge convention",
        "DECLARED      -- the matter content" in by_name["SM3"].text
        and "the convention Q = T_3 + Y" in by_name["SM3"].text,
    )
    checks.check(
        "SM4 separately imports measured boundary couplings and normalization",
        "Take the three SM gauge couplings at M_Z" in by_name["SM4"].text
        and "DECLARED      -- the Amaldi-Ellis convention" in by_name["SM4"].text,
    )
    checks.check(
        "GK1 denies a three-plus-one-dimensional kinetic closure for every factor",
        "no gauge sector -- abelian or non-abelian -- has its 3+1D" in by_name["GK1"].text
        and "the 3+1D term remains an" in by_name["GK1"].text,
    )
    checks.check(
        "phase-nine siblings contain no executable SM1 import",
        all("SM1" not in by_name[name].loaded_names for name in ("SM2", "SM3", "SM4")),
    )
    tally = checks.finish()
    print(f"P163 SOURCE GRAPH ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(run(Path(arguments.source_root).resolve()))
