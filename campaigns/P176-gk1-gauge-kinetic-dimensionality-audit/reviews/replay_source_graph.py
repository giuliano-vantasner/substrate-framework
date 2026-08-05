#!/usr/bin/env python3
"""Replay GK1's frozen dependency and reverse-consumer source graph."""

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


SOURCE_COMMIT = "6d1f4e02f87a0bd1dc326cb68af01872d1e88c64"


@dataclass(frozen=True)
class SourceNode:
    source_unit: str
    role: str
    relative_path: str
    sha256: str
    expected_checks: int
    expected_assertions: int = 1


NODES = (
    SourceNode("EM3", "declared_action_dependency", "merged-framework/bridges/phase-3/bridge_EM3_maxwell_coulomb_tail.py", "1c674bae211322b24a4504ff5aafc04424eb6a4bfe7813f63e5ec4337f783fc9", 11),
    SourceNode("EM5", "qualified_abelian_loop_dependency", "merged-framework/bridges/phase-3/bridge_EM5_induced_gauge_sector.py", "bcf2c49e1e98eefea98be0076afd29341ce80fd71a7b141618978139982e4ec0", 11),
    SourceNode("EM7", "qualified_Riesz_dependency", "merged-framework/bridges/phase-3/bridge_EM7_fractal_force_law.py", "c8bf044d846d22eaa652a0f4c11cd5f5e2a51f98e49d0578536fbc4e96f63f22", 17),
    SourceNode("W2", "accepted_SU2_basis_dependency", "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9),
    SourceNode("YM1", "qualified_SU2_loop_dependency", "merged-framework/bridges/phase-7/bridge_YM1_yang_mills_induction.py", "bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6", 9),
    SourceNode("YM2", "qualified_SU2_lift_dependency", "merged-framework/bridges/phase-7/bridge_YM2_yang_mills_3plus1_lift.py", "19c8708ea9b81eff719362ee713dd3d933b5422788759ae6e8933c705863b11c", 10),
    SourceNode("QCD1", "qualified_SU3_loop_dependency", "merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py", "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed", 11),
    SourceNode("QCD2", "qualified_SU3_lift_dependency", "merged-framework/bridges/phase-8/bridge_QCD2_su3_3plus1_lift.py", "64f8125a5c0ef194e23569711036ce6ec46f3ffef2b6eb94a7b5c97ed8bb566f", 10),
    SourceNode("AS3", "declared_gravity_analogy", "merged-framework/bridges/phase-21/bridge_AS3_sakharov_kappa_reduce.py", "f88cc85a3fb64d1b8aabdf53ced29168d78fce9470e586dc19564288a120903b", 8, 2),
    SourceNode("GK1", "adjudicated_root", "merged-framework/bridges/phase-35/bridge_GK1_gauge_kinetic_dimensionality_boundary.py", "c142538897e9168769483aeb978ea86587fa9a073e606aa204316238dfa24d74", 11),
    SourceNode("GK3D1", "pending_direct_consumer", "merged-framework/bridges/phase-41/bridge_GK3D1_master_polarization_general_D.py", "9a25110ba53adfb439d0cfd0570bd311b0a43a20f13d1351f45c3fa4075aeacb", 19),
    SourceNode("GK3D2", "pending_indirect_consumer", "merged-framework/bridges/phase-41/bridge_GK3D2_induced_kinetic_normalization.py", "856096aba38812dc17fb07ce5cf7c0fa13eb2623665ccf871810734ac3ca0886", 17),
    SourceNode("GK3D3", "pending_direct_consumer", "merged-framework/bridges/phase-41/bridge_GK3D3_transmutation_closes_the_log.py", "1c3f81d15ace3ec2c6326c89659596f5b9ff84ac23ef7f0143a53ad92b23b211", 14),
    SourceNode("GK3D4", "pending_direct_consumer", "merged-framework/bridges/phase-41/bridge_GK3D4_three_sectors_one_construction.py", "046273d9a06f92ddbe9cd666d3b6de0f321b9709c371aeee8103394dd2a2ad35", 11),
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
            timeout=180,
            check=False,
        )
        output = completed.stdout + completed.stderr
        terminal = re.search(
            rf"ALL\s+{node.expected_checks}\s+CHECKS\s+PASS", output
        ) is not None
        return ReplayResult(
            node=node,
            check_calls=check_calls,
            assertions=assertions,
            legacy_references=compatibility.legacy_references,
            current_references=compatibility.current_references,
            eager_fallbacks=compatibility.eager_legacy_default_fallbacks,
            returncode=completed.returncode,
            terminal_tally=terminal,
            text=source,
            output_tail="\n".join(output.splitlines()[-10:]),
        )
    except subprocess.TimeoutExpired as failure:
        return ReplayResult(
            node=node,
            check_calls=check_calls,
            assertions=assertions,
            legacy_references=compatibility.legacy_references,
            current_references=compatibility.current_references,
            eager_fallbacks=compatibility.eager_legacy_default_fallbacks,
            returncode=124,
            terminal_tally=False,
            text=source,
            output_tail="\n".join((failure.stdout or "").splitlines()[-10:]),
        )


def run(source_root: Path) -> int:
    checks = CheckLedger("P176-GK1-SOURCE-GRAPH")
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=source_root,
        capture_output=True,
        text=True,
        check=False,
    )
    checks.check(
        "source checkout remains at the governed commit",
        commit.returncode == 0 and commit.stdout.strip() == SOURCE_COMMIT,
    )
    selected_paths = [node.relative_path for node in NODES]
    selected_diff = subprocess.run(
        ["git", "diff", "--name-only", "--", *selected_paths],
        cwd=source_root,
        capture_output=True,
        text=True,
        check=False,
    )
    checks.check(
        "all selected source paths are clean despite unrelated source work",
        selected_diff.returncode == 0 and selected_diff.stdout.strip() == "",
    )

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda node: _replay(source_root, node), NODES))
    by_name = {result.node.source_unit: result for result in results}
    checks.check("fourteen frozen source graph nodes", len(results) == 14)
    for result in results:
        detail = (
            result.output_tail
            if result.returncode or not result.terminal_tally
            else ""
        )
        checks.check(
            f"{result.node.source_unit} hash shape exit and terminal tally",
            result.check_calls == result.node.expected_checks
            and result.assertions == result.node.expected_assertions
            and result.returncode == 0
            and result.terminal_tally,
            detail,
        )
        mode = "alias-only" if result.legacy_references else "native"
        print(
            f"SOURCE {result.node.source_unit}: role={result.node.role} "
            f"checks={result.node.expected_checks} assertions="
            f"{result.node.expected_assertions} mode={mode}"
        )

    checks.check(
        "graph predicate and assertion inventories are fixed",
        sum(result.node.expected_checks for result in results) == 168
        and sum(result.node.expected_assertions for result in results) == 15,
    )
    checks.check(
        "legacy compatibility is isolated and alias-only",
        {
            result.node.source_unit
            for result in results
            if result.legacy_references
        }
        == {"YM2", "QCD2"}
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
        "GK1's live documentation census is hash closed by the graph",
        all(
            by_name[name].node.sha256
            for name in ("EM5", "YM1", "QCD1", "EM7", "YM2", "QCD2")
        )
        and "read from the LIVE files at runtime" in by_name["GK1"].text,
    )
    checks.check(
        "the three predecessor scripts share a two-dimensional projector scaffold",
        "1+1D result" in by_name["EM5"].text
        and "this is the 1+1D induction" in by_name["YM1"].text
        and "this is the 1+1D induction" in by_name["QCD1"].text,
    )
    checks.check(
        "the three predecessor scripts also share the rejected scalar numerator",
        "integrand_general = u * (1 - u)" in by_name["EM5"].text
        and "integrand = u * (1 - u)" in by_name["GK1"].text
        and "a propagating gauge boson" in by_name["GK1"].text,
    )
    checks.check(
        "YM2 and QCD2 require alias replay but disclaim kinetic closure",
        "THE 3+1D KINETIC-TERM CEILING IS NOT CLOSED HERE" in by_name["YM2"].text
        and "THE 3+1D KINETIC-TERM CEILING IS NOT CLOSED HERE" in by_name["QCD2"].text,
    )
    checks.check(
        "EM7 supplies a normalized shape without a kinetic coefficient",
        "supplies and explains the FORCE-LAW SHAPE" in by_name["EM7"].text
        and "g_eff" not in by_name["EM7"].text,
    )
    checks.check(
        "AS3 is only the separately declared gravity analogy",
        "Sakharov" in by_name["AS3"].text
        and "GK1" not in by_name["AS3"].text,
    )
    checks.check(
        "all four phase-41 nodes consume the GK1 dimensional narrative",
        all("GK1" in by_name[name].text for name in ("GK3D1", "GK3D2", "GK3D3", "GK3D4")),
    )
    checks.check(
        "GK3D1 and GK3D3 specifically rely on the logarithm wording",
        "must be logarithmic" in by_name["GK3D1"].text
        and "treated exactly this as the wall" in by_name["GK3D3"].text,
    )
    checks.check(
        "reverse-consumer execution does not grant accepted authority",
        all(
            by_name[name].node.role.startswith("pending_")
            for name in ("GK3D1", "GK3D2", "GK3D3", "GK3D4")
        ),
    )

    tally = checks.finish()
    print(f"P176 SOURCE GRAPH ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(run(Path(arguments.source_root).resolve()))
