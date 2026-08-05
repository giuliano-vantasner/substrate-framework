#!/usr/bin/env python3
"""Replay KI3's pinned direct dependencies and reverse-consumer graph."""

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


@dataclass(frozen=True)
class SourceNode:
    label: str
    relation: str
    path: str
    sha256: str
    checks: int
    assertions: int


NODES = (
    SourceNode(
        "E3", "qualified_classical_coordinate_context",
        "merged-framework/bridges/phase-29/bridge_E3_yield_coefficient_overbinding.py",
        "aa76b9e675d4fbb45594e9d3df5107af175e927a24840260ca71ffda1bad3315", 5, 1,
    ),
    SourceNode(
        "E4", "qualified_local_BPS_context",
        "merged-framework/bridges/phase-29/bridge_E4_bps_zero_binding_resolution.py",
        "f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7", 5, 1,
    ),
    SourceNode(
        "KI2", "qualified_parameter_family_premise",
        "merged-framework/bridges/phase-34/bridge_KI2_epsilon_underdetermination.py",
        "9e16fc6fafa940f43d559ea0f6a9c2730940d1247f36f655375c2f75f6fd1e81", 6, 1,
    ),
    SourceNode(
        "KI3", "audited_root",
        "merged-framework/bridges/phase-34/bridge_KI3_bracket_is_sharp.py",
        "10e92457cbd213782e5778f5b739660a6d07ea229c44746e24fe0132844fcbd3", 5, 1,
    ),
    SourceNode(
        "KI4", "direct_reverse_consumer",
        "merged-framework/bridges/phase-34/bridge_KI4_backsolve_circularity.py",
        "138f204c2bf7e7278a1a4aadad4bed1680e11b6b6de7189a02640a81652f00cd", 5, 1,
    ),
    SourceNode(
        "MK4", "pending_interpolation_challenge",
        "merged-framework/bridges/phase-43/bridge_MK4_bps_compacton_and_pt_failure.py",
        "9f2e299032aace53c3ac2c2d1d5626372e4bdf1aa3b7b0650f574a9f7b8f7295", 6, 1,
    ),
    SourceNode(
        "MK5", "pending_bracket_challenge",
        "merged-framework/bridges/phase-43/bridge_MK5_generalized_solve_kappa.py",
        "a5ecb5d0d2ba96cf8083a9cfb32ddb44c2a4f4841bf776ebbccb91bc12b246f8", 8, 1,
    ),
    SourceNode(
        "MK6", "pending_indirect_consumer",
        "merged-framework/bridges/phase-43/bridge_MK6_confrontation_and_tension.py",
        "ef900954d9782bbf2589ff3e33045577ebdce3860d1a3ed7a6a6827e0ae81788", 6, 1,
    ),
    SourceNode(
        "MR6", "pending_indirect_ledger_consumer",
        "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py",
        "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d", 6, 3,
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
        command = [
            sys.executable,
            "-c",
            (
                "import runpy; import numpy as np; "
                "setattr(np, 'trapz', np.trapezoid); "
                f"runpy.run_path({str(path)!r}, run_name='__main__')"
            ),
        ]
    else:
        command = [sys.executable, str(path)]
    process = subprocess.run(
        command,
        cwd=SOURCE_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=300,
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
    checks = CheckLedger("P173-KI3-SOURCE-GRAPH")
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
        checks.check(
            f"{node.label} replays its exact local terminal tally",
            result.returncode == 0
            and result.stderr == ""
            and f"ALL {node.checks} CHECKS PASS" in result.stdout,
            result.stderr[-500:],
        )

    by_label = {result.node.label: result for result in results}
    checks.check(
        "the graph has exactly nine typed executable nodes",
        len(results) == 9
        and set(by_label)
        == {"E3", "E4", "KI2", "KI3", "KI4", "MK4", "MK5", "MK6", "MR6"},
    )
    checks.check(
        "the graph separates fifty-two predicates from eleven assertions",
        sum(node.checks for node in NODES) == 52
        and sum(node.assertions for node in NODES) == 11,
    )
    checks.check(
        "E3 uses a current-first fallback and no graph node needs an injected alias",
        by_label["E3"].legacy_references == 1
        and by_label["E3"].current_references == 1
        and not by_label["E3"].alias_injected
        and all(
            result.legacy_references == 0 and not result.alias_injected
            for label, result in by_label.items()
            if label != "E3"
        ),
    )

    root = by_label["KI3"].source
    checks.check(
        "KI3 narratively imports E3 E4 and KI2 but no governed implementation",
        all(token in root for token in ("E3", "E4", "KI2"))
        and "from substrate_framework" not in root,
    )
    checks.check(
        "KI3 declares the excluding codomain before its sharpness conclusion",
        "continuous kappa:(0,inf)->(0,kappa_cl)" in root
        and "bracket is SHARP" in root,
    )
    checks.check(
        "KI4 consumes KI3's whole-open-bracket prior and illustrative maps",
        "KI3's sharpness" in by_label["KI4"].source
        and "Take the admissible interpolants of KI3" in by_label["KI4"].source
        and "Prior admissible set for kappa, from KI3's sharpness" in by_label["KI4"].source,
    )
    checks.check(
        "pending MK4 and MK5 challenge KI3 without supplying accepted authority",
        "KI3's 'interpolating function'" in by_label["MK4"].source
        and "KI3's BRACKET IS REFUTED" in by_label["MK5"].source,
    )
    checks.check(
        "pending MR6 consumes MK5's claimed refutation only as narrative",
        "KI3's bracket [0, 8.46]" in by_label["MR6"].source
        and "refuted by MK5.7" in by_label["MR6"].source,
    )

    inventory = yaml.safe_load(
        (FRAMEWORK_ROOT / "migration/source-claims.yaml").read_text(encoding="utf-8")
    )
    units = {entry["source_unit"]: entry for entry in inventory["units"]}
    checks.check(
        "qualified dependencies and pending reverse consumers remain governance-typed",
        all(units[label]["disposition"] == "qualified" for label in ("E3", "E4", "KI2"))
        and units["KI3"]["disposition"] == "pending_adjudication"
        and all(
            units[label]["disposition"] == "pending_adjudication"
            for label in ("KI4", "MK4", "MK5", "MK6", "MR6")
        ),
    )
    checks.check(
        "pending challenges do not supersede accepted claims",
        all(units[label]["accepted_claims"] == [] for label in ("KI3", "KI4", "MK4", "MK5", "MK6", "MR6")),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
