#!/usr/bin/env python3
"""Replay CF1 and its declared narrative neighbors with exact inventories."""

from __future__ import annotations

import ast
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
    SourceNode("M1", "declared_scale_reference", "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9, 9, 1),
    SourceNode("M2", "declared_screening_template", "merged-framework/bridges/phase-7/bridge_M2_meissner_proca_W_mass.py", "4ae3e5cb06e7c0bce6387ac7b84f555de65f12cce4be42d620405bb2b5c5b59f", 7, 7, 1),
    SourceNode("CF1", "root", "merged-framework/bridges/phase-10/bridge_CF1_dual_superconductor_flux_tube.py", "a4ec97923804f1b7c624b7619bc6b6a1cbb62f42d659897799545b257ca33f5d", 8, 8, 2),
    SourceNode("CF2", "declared_downstream_tube", "merged-framework/bridges/phase-10/bridge_CF2_linear_potential.py", "e9651b9d4db9f23bb54d013a419c2f050725063347e63f253a968781598bfe6a", 15, 15, 1),
    SourceNode("CF3", "declared_downstream_loop", "merged-framework/bridges/phase-10/bridge_CF3_wilson_area_law.py", "8655579ef3173730c315d60aa821f7085cc131920ae49cb93c60b075d884889d", 6, 6, 1),
    SourceNode("CF4", "declared_downstream_scale", "merged-framework/bridges/phase-10/bridge_CF4_dimensional_transmutation.py", "e8fa7072d78ba5462ef9410689090f4627528c3632d45afd528c0c118f863c6b", 6, 6, 1),
)


def _runtime(node: SourceNode, *, needs_alias: bool) -> subprocess.CompletedProcess[str]:
    path = SOURCE_ROOT / node.relative_path
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    if not needs_alias:
        return subprocess.run(
            [sys.executable, str(path)], check=False, capture_output=True, text=True, env=environment
        )
    code = (
        "import runpy; import numpy as np; "
        "setattr(np, 'trapz', np.trapezoid); "
        f"runpy.run_path({str(path)!r}, run_name='__main__')"
    )
    return subprocess.run(
        [sys.executable, "-c", code], check=False, capture_output=True, text=True, env=environment
    )


def main() -> int:
    checks = CheckLedger("P167-CF1-NARRATIVE-SOURCE-GRAPH")
    legacy: dict[str, int] = {}
    current: dict[str, int] = {}
    texts: dict[str, str] = {}
    for node in NODES:
        path = SOURCE_ROOT / node.relative_path
        payload = path.read_bytes()
        source = payload.decode("utf-8")
        texts[node.label] = source
        tree = ast.parse(source, filename=str(path))
        lexical = sum(
            isinstance(item, ast.Call)
            and isinstance(item.func, ast.Name)
            and item.func.id == "check"
            for item in ast.walk(tree)
        )
        assertions = sum(isinstance(item, ast.Assert) for item in ast.walk(tree))
        compatibility = audit_numpy_trapezoid_compatibility(source, filename=str(path))
        if compatibility.legacy_references:
            legacy[node.label] = compatibility.legacy_references
        if compatibility.current_references:
            current[node.label] = compatibility.current_references
        checks.check(f"{node.label} hash is pinned", hashlib.sha256(payload).hexdigest() == node.sha256)
        checks.check(
            f"{node.label} lexical and assertion inventories are exact",
            lexical == node.lexical_checks and assertions == node.assertions,
        )
        process = _runtime(node, needs_alias=compatibility.legacy_references > 0)
        checks.check(f"{node.label} replay exits cleanly", process.returncode == 0 and process.stderr == "")
        checks.check(
            f"{node.label} runtime tally is exact",
            process.stdout.count("  PASS\n") == node.runtime_checks
            and f"ALL {node.runtime_checks} CHECKS PASS" in process.stdout,
        )

    checks.check("the declared graph contains exactly six nodes", len(NODES) == 6)
    checks.check(
        "the graph separates fifty-one lexical and runtime checks from seven assertions",
        sum(node.lexical_checks for node in NODES) == 51
        and sum(node.runtime_checks for node in NODES) == 51
        and sum(node.assertions for node in NODES) == 7,
    )
    checks.check(
        "only immutable CF1 needs the legacy-name compatibility alias",
        legacy == {"CF1": 3} and current == {},
    )
    checks.check(
        "CF1 has no executable import from its declared narrative neighbors",
        all(
            token not in texts["CF1"]
            for token in (
                "import bridge_M1",
                "import bridge_M2",
                "import bridge_CF2",
                "import bridge_CF3",
                "import bridge_CF4",
            )
        ),
    )
    checks.check(
        "the source itself declares CF2 CF3 CF4 outputs negative for CF1",
        "NEGATIVE (not claimed here): the linear potential" in texts["CF1"]
        and "the Wilson-loop area law" in texts["CF1"]
        and "confinement-from-AF by dimensional transmutation" in texts["CF1"],
    )
    checks.check(
        "M1 and M2 are templates rather than accepted physical authority for CF1",
        "v = condensate VEV [M1]" in texts["CF1"]
        and "DUALIZE M2's London screening" in texts["CF1"],
    )

    total = checks.finish()
    print(f"P167 CF1 SOURCE GRAPH ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
