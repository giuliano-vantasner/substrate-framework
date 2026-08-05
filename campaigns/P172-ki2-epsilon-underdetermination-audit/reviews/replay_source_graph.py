#!/usr/bin/env python3
"""Replay KI2's pinned dependency and reverse-consumer source graph."""

from __future__ import annotations

import ast
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import subprocess
import sys

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE_ROOT = Path("/home/dan/substrate")
FRAMEWORK_ROOT = Path("/home/dan/substrate-framework")
SOURCE_COMMIT = "6d1f4e02f87a0bd1dc326cb68af01872d1e88c64"


@dataclass(frozen=True)
class SourceNode:
    label: str
    relation: str
    path: str
    sha256: str
    checks: int
    assertions: int
    expected_refutation: bool = False


NODES = (
    SourceNode(
        "E3", "accepted_standard_sector_context",
        "merged-framework/bridges/phase-29/bridge_E3_yield_coefficient_overbinding.py",
        "aa76b9e675d4fbb45594e9d3df5107af175e927a24840260ca71ffda1bad3315", 5, 1,
    ),
    SourceNode(
        "E4", "accepted_BPS_energy_context",
        "merged-framework/bridges/phase-29/bridge_E4_bps_zero_binding_resolution.py",
        "f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7", 5, 1,
    ),
    SourceNode(
        "S4", "accepted_standard_scale_context",
        "merged-framework/bridges/phase-4/bridge_S4_c4_vector_meson_closure.py",
        "49c7b2392bbe23d2824f4f73030ccd30f245e1750e0c7736dc420d3f64d7a780", 11, 1,
    ),
    SourceNode(
        "NY1", "accepted_standard_scale_context",
        "merged-framework/bridges/phase-24/bridge_NY1_skyrme_energy_unit.py",
        "b3531d7f906fe396a1326d44d68f34d09ae34988e86a8f721c360040c4aa0921", 9, 0,
    ),
    SourceNode(
        "NY2", "accepted_standard_scale_consumer_context",
        "merged-framework/bridges/phase-24/bridge_NY2_nuclear_yield_one_skyrme_unit.py",
        "a0ab1c713ff4224a3f4e39e6770c1a1c8c5bdc4c2f7ef2bd8b18ab8fc87c18a3", 10, 0,
    ),
    SourceNode(
        "KI1", "refuted_load_bearing_premise",
        "merged-framework/bridges/phase-34/bridge_KI1_exhaustive_coupling_search.py",
        "a1ec5f8e64e56165d2c51ad2389ecb455870572ba4ef9eca292151bde4ddb42b", 5, 1, True,
    ),
    SourceNode(
        "KI2", "qualified_root",
        "merged-framework/bridges/phase-34/bridge_KI2_epsilon_underdetermination.py",
        "9e16fc6fafa940f43d559ea0f6a9c2730940d1247f36f655375c2f75f6fd1e81", 6, 1,
    ),
    SourceNode(
        "KI3", "pending_reverse_consumer",
        "merged-framework/bridges/phase-34/bridge_KI3_bracket_is_sharp.py",
        "10e92457cbd213782e5778f5b739660a6d07ea229c44746e24fe0132844fcbd3", 5, 1,
    ),
    SourceNode(
        "KI4", "pending_reverse_consumer",
        "merged-framework/bridges/phase-34/bridge_KI4_backsolve_circularity.py",
        "138f204c2bf7e7278a1a4aadad4bed1680e11b6b6de7189a02640a81652f00cd", 5, 1,
    ),
    SourceNode(
        "MK1", "pending_counterrelation",
        "merged-framework/bridges/phase-43/bridge_MK1_mu_from_medium_cosine.py",
        "98ff5459ae3c6cb64a9a7632fbaa8613f1f5b1adb68419de25ffa06b1c3a3222", 7, 1,
    ),
    SourceNode(
        "MK2", "pending_counterrelation",
        "merged-framework/bridges/phase-43/bridge_MK2_lambda_from_medium_omega.py",
        "351136bca28e413ddd54f1b15bf7084dffe32af565fc87e7220d1437a525eb07", 7, 1,
    ),
    SourceNode(
        "MK3", "pending_counterrelation",
        "merged-framework/bridges/phase-43/bridge_MK3_epsilon_pinned.py",
        "64254d0f6b9d6ff57f5a8b0a4b86a510e2bef230b4f3bec062533fac59516404", 6, 1,
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
    alias_injected: bool
    returncode: int
    stdout: str
    stderr: str
    source: str


def _replay(node: SourceNode) -> Replay:
    path = SOURCE_ROOT / node.path
    payload = path.read_bytes()
    source = payload.decode("utf-8")
    tree = ast.parse(source, filename=str(path))
    compatibility = audit_numpy_trapezoid_compatibility(source, filename=str(path))
    alias_injected = (
        compatibility.legacy_references > 0
        and (
            compatibility.current_references == 0
            or compatibility.eager_legacy_default_fallbacks > 0
        )
    )
    if alias_injected:
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
        timeout=180,
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
        alias_injected=alias_injected,
        returncode=process.returncode,
        stdout=process.stdout,
        stderr=process.stderr,
        source=source,
    )


def main() -> int:
    checks = CheckLedger("P172-KI2-SOURCE-GRAPH")
    paths = [node.path for node in NODES]
    path_state = subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "status", "--porcelain", "--", *paths],
        check=True,
        capture_output=True,
        text=True,
    )
    checks.check(
        "every pinned graph path is clean at the predecessor worktree",
        path_state.stdout == "",
        path_state.stdout,
    )
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(_replay, NODES))

    for result in results:
        node = result.node
        checks.check(f"{node.label} source hash remains pinned", result.digest == node.sha256)
        checks.check(
            f"{node.label} predicate and assertion inventories are exact",
            result.lexical_checks == node.checks and result.assertions == node.assertions,
        )
        checks.check(
            f"{node.label} has no eager NumPy legacy fallback",
            result.eager_fallbacks == 0,
        )
        if node.expected_refutation:
            expected = (
                result.returncode != 0
                and "KI1.1" in result.stdout
                and "CHECK FAILED: KI1.2" in result.stderr
                and "ALL 5 CHECKS PASS" not in result.stdout
            )
            verdict = "fails exactly at its governed refutation"
        else:
            expected = (
                result.returncode == 0
                and result.stderr == ""
                and f"ALL {node.checks} CHECKS PASS" in result.stdout
            )
            verdict = "replays its exact local terminal tally"
        checks.check(f"{node.label} {verdict}", expected, result.stderr[-500:])

    by_label = {result.node.label: result for result in results}
    checks.check(
        "the pinned graph has exactly twelve typed executable nodes",
        len(results) == 12
        and set(by_label)
        == {"E3", "E4", "S4", "NY1", "NY2", "KI1", "KI2", "KI3", "KI4", "MK1", "MK2", "MK3"},
    )
    checks.check(
        "the graph separates eighty-one predicates from ten assertions",
        sum(node.checks for node in NODES) == 81
        and sum(node.assertions for node in NODES) == 10,
    )
    checks.check(
        "E3 uses a current-first trapezoid branch and no node needs an injected alias",
        by_label["E3"].legacy_references == 1
        and by_label["E3"].current_references == 1
        and not by_label["E3"].alias_injected
        and all(
            result.legacy_references == 0 and not result.alias_injected
            for label, result in by_label.items()
            if label != "E3"
        ),
    )
    root = by_label["KI2"].source
    checks.check(
        "KI2 explicitly depends on refuted KI1 but imports no executable result",
        "FROM KI1" in root
        and "NO framework-derived quantity depends on lambda or mu" in root
        and "import bridge_KI1" not in root
        and "from bridge_KI1" not in root,
    )
    checks.check(
        "KI2's alleged complete invariant set excludes its accepted BPS dependency",
        "derived_quantities" in root
        and "lambda*pi^2*B0" not in root
        and "2*lambda*mu*pi^2" not in root,
    )
    checks.check(
        "KI3 and KI4 consume the all-positive-epsilon conclusion narratively",
        all("KI2" in by_label[label].source for label in ("KI3", "KI4"))
        and "every epsilon" in by_label["KI3"].source
        and "every epsilon" in by_label["KI4"].source,
    )
    checks.check(
        "all three pending MK counterrelations consume KI2 without becoming authority",
        all("KI2" in by_label[label].source for label in ("MK1", "MK2", "MK3")),
    )

    inventory = yaml.safe_load(
        (FRAMEWORK_ROOT / "migration/source-claims.yaml").read_text(encoding="utf-8")
    )
    units = {entry["source_unit"]: entry for entry in inventory["units"]}
    checks.check(
        "accepted upstream mappings refuted KI1 and pending reverse consumers stay typed",
        all(units[label]["disposition"] in {"qualified", "duplicate_evidence"}
            for label in ("E3", "E4", "S4", "NY1", "NY2"))
        and units["KI1"]["disposition"] == "refuted"
        and all(units[label]["disposition"] == "pending_adjudication"
                for label in ("KI2", "KI3", "KI4", "MK1", "MK2", "MK3")),
    )

    untracked_bm11 = "merged-framework/bridges/phase-47/bridge_BM11_bps_coupling_scope.py"
    baseline_lookup = subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "cat-file", "-e", f"{SOURCE_COMMIT}:{untracked_bm11}"],
        check=False,
        capture_output=True,
        text=True,
    )
    current_state = subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "status", "--porcelain", "--", untracked_bm11],
        check=True,
        capture_output=True,
        text=True,
    )
    checks.check(
        "untracked BM11 is excluded from the pinned baseline and scientific authority",
        baseline_lookup.returncode != 0
        and current_state.stdout.startswith("?? ")
        and "BM11" not in units,
    )

    lean_path = SOURCE_ROOT / "merged-framework/bridges/phase-34/lean/Phase34KIKernel.lean"
    lean_source = lean_path.read_text(encoding="utf-8")
    checks.check(
        "the pinned Lean theorem proves only local ratio scaling and F-over-e invariance",
        hashlib.sha256(lean_path.read_bytes()).hexdigest()
        == "269c2b6b023fb1bfacb7dede2e708f09d3e08cad00bcc933e5149357ef5870f5"
        and "theorem eps_flow_scales" in lean_source
        and "theorem derivedScale_flow_invariant" in lean_source
        and "def derivedScale (p : Params) : ℝ := p.1 / p.2.1" in lean_source
        and "B0" not in lean_source
        and "energyDensity" not in lean_source
        and "bpsBound" not in lean_source,
    )

    total = checks.finish()
    print(f"P172 KI2 SOURCE GRAPH ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
