#!/usr/bin/env python3
"""Replay the frozen YM1 dependency and semantic-consumer graph."""

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
    SourceNode("EM3", "analogy_only", "merged-framework/bridges/phase-3/bridge_EM3_maxwell_coulomb_tail.py", "1c674bae211322b24a4504ff5aafc04424eb6a4bfe7813f63e5ec4337f783fc9", 11),
    SourceNode("EM5", "corrected_abelian_dependency", "merged-framework/bridges/phase-3/bridge_EM5_induced_gauge_sector.py", "bcf2c49e1e98eefea98be0076afd29341ce80fd71a7b141618978139982e4ec0", 11),
    SourceNode("EM7", "analogy_only", "merged-framework/bridges/phase-3/bridge_EM7_fractal_force_law.py", "c8bf044d846d22eaa652a0f4c11cd5f5e2a51f98e49d0578536fbc4e96f63f22", 17),
    SourceNode("W2", "generator_and_retroactive_consumer", "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9),
    SourceNode("W5", "coupling_analogy_only", "merged-framework/bridges/phase-6/bridge_W5_chiral_asymmetry_magnitude.py", "5afea85e0e70236ddd076e2da585d6ab5861d52211239642eac1c951f1c6a71a", 27),
    SourceNode("W7", "gauge_dependency_and_retroactive_consumer", "merged-framework/bridges/phase-6/bridge_W7_su2L_gauging_charged_current.py", "1a1fa278f6b8a0cab74d020fc01db1fa3576f57084d0cd80959867c591bf66c3", 11),
    SourceNode("M1", "conditional_normalization_consumer", "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9),
    SourceNode("M2", "conditional_Proca_consumer", "merged-framework/bridges/phase-7/bridge_M2_meissner_proca_W_mass.py", "4ae3e5cb06e7c0bce6387ac7b84f555de65f12cce4be42d620405bb2b5c5b59f", 7),
    SourceNode("YM1", "adjudicated_source", "merged-framework/bridges/phase-7/bridge_YM1_yang_mills_induction.py", "bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6", 9),
    SourceNode("YM2", "pending_direct_overclaim_consumer", "merged-framework/bridges/phase-7/bridge_YM2_yang_mills_3plus1_lift.py", "19c8708ea9b81eff719362ee713dd3d933b5422788759ae6e8933c705863b11c", 10),
    SourceNode("GK1", "pending_boundary_and_overclaim_consumer", "merged-framework/bridges/phase-35/bridge_GK1_gauge_kinetic_dimensionality_boundary.py", "c142538897e9168769483aeb978ea86587fa9a073e606aa204316238dfa24d74", 11),
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
    checks = CheckLedger("P158-YM1-SOURCE-GRAPH")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda node: _replay(source_root, node), NODES))
    by_name = {result.node.source_unit: result for result in results}

    checks.check("eleven frozen source graph nodes", len(results) == 11)
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
        sum(result.node.expected_checks for result in results) == 132
        and sum(result.assertions for result in results) == 11,
    )
    checks.check(
        "legacy integration compatibility is isolated to immutable YM2",
        {
            result.node.source_unit
            for result in results
            if result.legacy_references
        }
        == {"YM2"}
        and {
            result.node.source_unit
            for result in results
            if result.eager_fallbacks
        }
        == {"YM2"}
        and by_name["YM2"].current_references == 1,
    )
    checks.check(
        "W2 and W7 contain retroactive YM1 closure overclaims",
        "phase-7/bridge_YM1_yang_mills_induction.py GENERATES" in by_name["W2"].text
        and "SINCE GENERATED by phase-7's YM1" in by_name["W7"].text,
    )
    checks.check(
        "M1 and M2 do not directly import YM1",
        "YM1" not in by_name["M1"].text and "YM1" not in by_name["M2"].text,
    )
    checks.check(
        "YM2 legitimately recomputes the trace but overclaims a dimensional lift",
        "TrTT = sp.Matrix(3, 3" in by_name["YM2"].text
        and "generated the NON-ABELIAN gauge kinetic" in by_name["YM2"].text
        and "THE YM1 CEILING IS CLOSED" in by_name["YM2"].text,
    )
    checks.check(
        "GK1 preserves the 1+1 dimensional boundary but repeats the loop overclaim",
        "dim(YM1) = dim(QCD1) = dim(EM5) = 1+1D" in by_name["GK1"].text
        and "a propagating gauge boson" in by_name["GK1"].text
        and "u * (1 - u) * q2s" in by_name["GK1"].text,
    )
    checks.check(
        "EM3 EM7 and W5 are analogies rather than direct YM1 consumers",
        all(
            "YM1" not in by_name[name].text
            for name in ("EM3", "EM7", "W5")
        ),
    )
    checks.check(
        "EM5 supplies the source scaffold but not a determinant derivation",
        "integrand_general = u * (1 - u)" in by_name["EM5"].text
        and not {
            "determinant",
            "bubble_integral",
            "seagull_integral",
            "loop_momentum",
        }.intersection(by_name["EM5"].loaded_names),
    )
    checks.check(
        "source graph cannot close a physical weak or substrate sector",
        "CHARGED SU(2)_L LEFT-DOUBLET" in by_name["YM1"].text
        and not {
            "scalar_qed2_vacuum_polarization",
            "determinant",
            "counterterm",
        }.intersection(by_name["YM1"].loaded_names),
    )

    tally = checks.finish()
    print(f"P158 SOURCE GRAPH ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(run(Path(arguments.source_root).resolve()))
