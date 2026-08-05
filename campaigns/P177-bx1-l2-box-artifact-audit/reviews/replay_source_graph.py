#!/usr/bin/env python3
"""Replay BX1's frozen dependency and reverse-consumer source graph."""

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

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE_COMMIT = "6d1f4e02f87a0bd1dc326cb68af01872d1e88c64"
FRAMEWORK_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class SourceNode:
    source_unit: str
    role: str
    relative_path: str
    sha256: str
    expected_checks: int
    expected_assertions: int


NODES = (
    SourceNode("GW3", "qualified_TT_dependency", "merged-framework/bridges/phase-12/bridge_GW3_TT_projector_two_polarizations.py", "3b941debf6933729b693b928579d4a7f1d73d906911c2fcedb9316ad08038326", 15, 2),
    SourceNode("P3D2", "qualified_spherical_null_dependency", "merged-framework/bridges/phase-14/bridge_P3D2_spherical_quadrupole_null.py", "72802a3bb3ed46be3bf7b96e035028b0ded352ae02e587cb14b9db902b2125cb", 4, 1),
    SourceNode("QB1", "qualified_finite_box_background_dependency", "merged-framework/bridges/phase-16/bridge_QB1_radial_eigenvalue_quasibreather.py", "1f387c140ca80be0e457efd17146267bdecab1cbdbcdd10dd34287bc5de2dc7a", 6, 1),
    SourceNode("QB3", "qualified_averaged_mode_object_under_audit", "merged-framework/bridges/phase-16/bridge_QB3_triaxial_nonaxisymmetric.py", "e9626f2e4829084635386eea271d0abdd39c81dfcd6899765d2f4bffac83e0c8", 4, 1),
    SourceNode("QB4", "qualified_conditional_waveform_dependency", "merged-framework/bridges/phase-16/bridge_QB4_two_polarization_waveform.py", "4523ad68636413bf628cd353e496c61b25af3c7f30bdf3e1e061930054fb9291", 5, 1),
    SourceNode("BX1", "adjudicated_root", "merged-framework/bridges/phase-36/bridge_BX1_l2_mode_box_artifact.py", "a80364df834f23b5ad006b54e7097e0a38d846405ba40408e558a8773aa74fb3", 8, 1),
    SourceNode("SC2", "pending_direct_consumer", "merged-framework/bridges/phase-36/bridge_SC2_horndeski_selfconsistent_solve.py", "64dfc9c31edd8368cb0e2359ca646fc8f62fe306d6af7a326ff8934070b96425", 7, 4),
    SourceNode("TX1", "pending_direct_consumer", "merged-framework/bridges/phase-40/bridge_TX1_b2_intrinsic_quadrupole.py", "30161731af4e3ffda219adbdc7af9db66f6829fbbd3736a3198ed19a644ac8ff", 9, 2),
    SourceNode("TX2", "pending_direct_consumer", "merged-framework/bridges/phase-40/bridge_TX2_rotating_triaxial_quadrupole.py", "7dd6852af20ef060ffa2f17950219fb79d7943e50fc64235a75a10d098f7d3b7", 7, 1),
    SourceNode("TX3", "pending_direct_consumer", "merged-framework/bridges/phase-40/bridge_TX3_two_polarizations_omega_free.py", "ce6db5f59e61829c287e7cced5a53506838d31c77ba9e651dbceb9a241275837", 7, 1),
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
    source: str
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
            "setattr(np, 'trapz', np.trapezoid); "
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
            timeout=360,
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
            source=source,
            output_tail="\n".join(output.splitlines()[-12:]),
        )
    except subprocess.TimeoutExpired as failure:
        output = (failure.stdout or "") + (failure.stderr or "")
        return ReplayResult(
            node=node,
            check_calls=check_calls,
            assertions=assertions,
            legacy_references=compatibility.legacy_references,
            current_references=compatibility.current_references,
            eager_fallbacks=compatibility.eager_legacy_default_fallbacks,
            returncode=124,
            terminal_tally=False,
            source=source,
            output_tail="\n".join(output.splitlines()[-12:]),
        )


def run(source_root: Path) -> int:
    checks = CheckLedger("P177-BX1-SOURCE-GRAPH")
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
    checks.check("ten frozen source graph nodes", len(results) == 10)
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
        sum(result.node.expected_checks for result in results) == 72
        and sum(result.node.expected_assertions for result in results) == 15,
    )
    alias_nodes = {
        result.node.source_unit for result in results if result.legacy_references
    }
    checks.check(
        "legacy compatibility is isolated and backed by numpy.trapezoid",
        alias_nodes == {"P3D2", "QB3", "QB4", "TX1"}
        and all(
            result.current_references == 1 and result.eager_fallbacks == 0
            for result in results
            if result.node.source_unit in alias_nodes
        ),
    )

    inventory = yaml.safe_load(
        (
            FRAMEWORK_ROOT
            / "campaigns/P001-sine-gordon-root/evidence/source-inventory.yaml"
        ).read_text(encoding="utf-8")
    )["bridge_records"]
    inventory_by_name = {record["label"]: record for record in inventory}
    checks.check(
        "BX1 candidate dependencies are exactly the frozen five nodes",
        inventory_by_name["BX1"]["candidate_dependencies"]
        == ["GW3", "P3D2", "QB1", "QB3", "QB4"],
    )
    reverse_consumers = {
        record["label"]
        for record in inventory
        if "BX1" in record.get("candidate_dependencies", [])
    }
    checks.check(
        "BX1 has exactly four frozen reverse consumers",
        reverse_consumers == {"SC2", "TX1", "TX2", "TX3"},
    )

    queue = yaml.safe_load(
        (FRAMEWORK_ROOT / "migration/source-claims.yaml").read_text(encoding="utf-8")
    )["units"]
    queue_by_name = {record["source_unit"]: record for record in queue}
    expected_mappings = {
        "GW3": ["C-GW-001", "C-GW-002"],
        "P3D2": ["C-MOM-003", "C-PDE-002"],
        "QB1": ["C-PDE-005", "C-PDE-006"],
        "QB3": ["C-PDE-009", "C-GW-007"],
        "QB4": ["C-GW-008"],
    }
    checks.check(
        "all five dependency nodes retain accepted qualified mappings",
        all(
            queue_by_name[name]["disposition"] == "qualified"
            and queue_by_name[name]["accepted_claims"] == mapping
            for name, mapping in expected_mappings.items()
        ),
    )
    checks.check(
        "all reverse consumers remain pending without accepted mappings",
        all(
            queue_by_name[name]["disposition"] == "pending_adjudication"
            and queue_by_name[name]["accepted_claims"] == []
            for name in reverse_consumers
        ),
    )
    checks.check(
        "QB3 and BX1 share the imposed-tail localization defect",
        "g_r[rc > R_mode] = 0.0" in by_name["QB3"].source
        and "g_vac[rc > R_mode_qb3] = 0.0" in by_name["BX1"].source,
    )
    checks.check(
        "BX1 does not invalidate accepted conditional TT or STF kinematics",
        "KINEMATICS" in by_name["BX1"].source
        and "What survives fully" in by_name["BX1"].source
        and all(by_name[name].terminal_tally for name in ("GW3", "P3D2", "QB4")),
    )
    checks.check(
        "reverse consumers import BX1 narrative but receive no authority",
        all("BX1" in by_name[name].source for name in reverse_consumers)
        and all(
            by_name[name].node.role == "pending_direct_consumer"
            for name in reverse_consumers
        ),
    )
    checks.check(
        "TX consumers repeat the overbroad no-bound-state premise",
        "NO bound state" in by_name["TX1"].source
        and "failed to build" in by_name["TX2"].source
        and "Dirichlet-box artifact" in by_name["TX3"].source,
    )
    checks.check(
        "SC2 uses BX1 only as a claimed route closure not a derived input",
        "BX1" in by_name["SC2"].source
        and "candidate_dependencies" not in by_name["SC2"].source,
    )

    tally = checks.finish()
    print(f"P177 SOURCE GRAPH ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root")
    arguments = parser.parse_args()
    raise SystemExit(run(Path(arguments.source_root).resolve()))
