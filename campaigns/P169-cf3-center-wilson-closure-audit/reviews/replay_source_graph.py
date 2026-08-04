#!/usr/bin/env python3
"""Replay CF3 and its seven declared narrative neighbors with exact inventories."""

from __future__ import annotations

import ast
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import subprocess
import sys

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE_ROOT = Path("/home/dan/substrate")


@dataclass(frozen=True)
class SourceNode:
    label: str
    relation: str
    relative_path: str
    sha256: str
    lexical_checks: int
    runtime_checks: int
    assertions: int


NODES = (
    SourceNode(
        "EM7", "declared_exponent_analogy",
        "merged-framework/bridges/phase-3/bridge_EM7_fractal_force_law.py",
        "c8bf044d846d22eaa652a0f4c11cd5f5e2a51f98e49d0578536fbc4e96f63f22",
        17, 17, 1,
    ),
    SourceNode(
        "NA1", "declared_SU2_center_analogy",
        "merged-framework/bridges/phase-7/bridge_NA1_su2L_wilson_loop.py",
        "c36b2eeace179a95b44400ea42b74f6263671fd4b4a8441fc682c480bc9372c8",
        5, 5, 1,
    ),
    SourceNode(
        "QCD1", "declared_generator_provider",
        "merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py",
        "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed",
        11, 11, 1,
    ),
    SourceNode(
        "SM3", "declared_triality_label_context",
        "merged-framework/bridges/phase-9/bridge_SM3_anomaly_cancellation.py",
        "3ace90aa5377050e4dcab5778996079eea92c9cc56a53c276a60a5508f63b529",
        8, 8, 1,
    ),
    SourceNode(
        "CF1", "sibling_vortex_narrative",
        "merged-framework/bridges/phase-10/bridge_CF1_dual_superconductor_flux_tube.py",
        "a4ec97923804f1b7c624b7619bc6b6a1cbb62f42d659897799545b257ca33f5d",
        8, 8, 2,
    ),
    SourceNode(
        "CF2", "sibling_linear_tube_narrative",
        "merged-framework/bridges/phase-10/bridge_CF2_linear_potential.py",
        "e9651b9d4db9f23bb54d013a419c2f050725063347e63f253a968781598bfe6a",
        15, 15, 1,
    ),
    SourceNode(
        "CF3", "root",
        "merged-framework/bridges/phase-10/bridge_CF3_wilson_area_law.py",
        "8655579ef3173730c315d60aa821f7085cc131920ae49cb93c60b075d884889d",
        6, 6, 1,
    ),
    SourceNode(
        "CF4", "sibling_scale_narrative",
        "merged-framework/bridges/phase-10/bridge_CF4_dimensional_transmutation.py",
        "e8fa7072d78ba5462ef9410689090f4627528c3632d45afd528c0c118f863c6b",
        6, 6, 1,
    ),
)


@dataclass(frozen=True)
class Replay:
    node: SourceNode
    digest: str
    lexical_checks: int
    assertions: int
    legacy_references: int
    current_references: int
    eager_fallbacks: int
    returncode: int
    stderr: str
    runtime_checks: int
    terminal_tally: bool
    source: str


def _replay(node: SourceNode) -> Replay:
    path = SOURCE_ROOT / node.relative_path
    payload = path.read_bytes()
    source = payload.decode("utf-8")
    tree = ast.parse(source, filename=str(path))
    compatibility = audit_numpy_trapezoid_compatibility(source, filename=str(path))
    if compatibility.requires_legacy_alias:
        code = (
            "import runpy; import numpy as np; "
            "setattr(np, 'trapz', np.trapezoid); "
            f"runpy.run_path({str(path)!r}, run_name='__main__')"
        )
        command = [sys.executable, "-c", code]
    else:
        command = [sys.executable, str(path)]
    process = subprocess.run(
        command,
        cwd=SOURCE_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return Replay(
        node=node,
        digest=hashlib.sha256(payload).hexdigest(),
        lexical_checks=sum(
            isinstance(item, ast.Call)
            and isinstance(item.func, ast.Name)
            and item.func.id == "check"
            for item in ast.walk(tree)
        ),
        assertions=sum(isinstance(item, ast.Assert) for item in ast.walk(tree)),
        legacy_references=compatibility.legacy_references,
        current_references=compatibility.current_references,
        eager_fallbacks=compatibility.eager_legacy_default_fallbacks,
        returncode=process.returncode,
        stderr=process.stderr,
        runtime_checks=process.stdout.count("  PASS\n"),
        terminal_tally=f"ALL {node.runtime_checks} CHECKS PASS" in process.stdout,
        source=source,
    )


def main() -> int:
    checks = CheckLedger("P169-CF3-SOURCE-GRAPH")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(_replay, NODES))

    for result in results:
        node = result.node
        checks.check(
            f"{node.label} hash remains pinned",
            result.digest == node.sha256,
        )
        checks.check(
            f"{node.label} lexical and assertion inventories are exact",
            result.lexical_checks == node.lexical_checks
            and result.assertions == node.assertions,
        )
        checks.check(
            f"{node.label} replay exits cleanly",
            result.returncode == 0 and result.stderr == "",
            result.stderr[-500:],
        )
        checks.check(
            f"{node.label} runtime tally is exact",
            result.runtime_checks == node.runtime_checks and result.terminal_tally,
        )

    by_label = {result.node.label: result for result in results}
    checks.check(
        "the direct narrative graph contains exactly eight pinned nodes",
        len(results) == 8
        and set(by_label)
        == {"EM7", "NA1", "QCD1", "SM3", "CF1", "CF2", "CF3", "CF4"},
    )
    checks.check(
        "the graph separates seventy-six predicates from nine assertions",
        sum(node.lexical_checks for node in NODES) == 76
        and sum(node.runtime_checks for node in NODES) == 76
        and sum(node.assertions for node in NODES) == 9,
    )
    checks.check(
        "only immutable CF1 requires a legacy-name alias backed by np.trapezoid",
        {
            label: result.legacy_references
            for label, result in by_label.items()
            if result.legacy_references
        }
        == {"CF1": 3}
        and all(result.current_references == 0 for result in results),
    )
    checks.check(
        "the graph contains no eager legacy fallback expression",
        all(result.eager_fallbacks == 0 for result in results),
    )

    root_source = by_label["CF3"].source
    checks.check(
        "CF3 names every graph neighbor narratively",
        all(label in root_source for label in ("EM7", "NA1", "QCD1", "SM3", "CF1", "CF2", "CF4")),
    )
    checks.check(
        "CF3 imports none of its narrative neighbors",
        all(
            token not in root_source
            for label in ("EM7", "NA1", "QCD1", "SM3", "CF1", "CF2", "CF4")
            for token in (f"import bridge_{label}", f"from bridge_{label}")
        ),
    )
    checks.check(
        "CF3 explicitly marks the loop models and physical map as declared or imported",
        "DECLARED:" in root_source
        and "the area-law model is <W>=exp(-sigma R T)" in root_source
        and "the Wilson-loop construction" in root_source
        and "IMPORTED (cited, not re-derived)" in root_source,
    )
    accepted_review = (
        Path(
            "/home/dan/substrate-framework/campaigns/P028-su3-center-wilson/"
            "reviews/source_adjudication.md"
        )
        .read_text(encoding="utf-8")
        .casefold()
    )
    checks.check(
        "source-graph execution grants no center-to-loop-law selection edge",
        "same exact su(3) center can be paired" in accepted_review
        and "declared loop laws" in accepted_review
        and "does not derive a general su(n) theorem" in accepted_review,
    )

    total = checks.finish()
    print(f"P169 CF3 SOURCE GRAPH ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
