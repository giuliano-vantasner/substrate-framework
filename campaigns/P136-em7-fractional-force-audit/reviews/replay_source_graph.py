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
    SourceNode("EM7", "root", "merged-framework/bridges/phase-3/bridge_EM7_fractal_force_law.py", "c8bf044d846d22eaa652a0f4c11cd5f5e2a51f98e49d0578536fbc4e96f63f22", 17),
    SourceNode("EM3", "declared_dependency", "merged-framework/bridges/phase-3/bridge_EM3_maxwell_coulomb_tail.py", "1c674bae211322b24a4504ff5aafc04424eb6a4bfe7813f63e5ec4337f783fc9", 11),
    SourceNode("D3S", "dependency_and_consumer", "merged-framework/bridges/phase-19/bridge_D3S_coulomb_from_sg.py", "a5ff9c760cf8776115881d7a2e5e86c562cdf461f61f36784ff95c6381d24d71", 13),
    SourceNode("QCD5", "dependency_and_consumer", "merged-framework/bridges/phase-8/bridge_QCD5_d3_overdetermination.py", "60a2f5b8dbd76f3b4d6b0a48e4fcd5ed9edbc6a4e1d3869cb4a40bf30c87084c", 7),
    SourceNode("EM5", "consumer", "merged-framework/bridges/phase-3/bridge_EM5_induced_gauge_sector.py", "bcf2c49e1e98eefea98be0076afd29341ce80fd71a7b141618978139982e4ec0", 11),
    SourceNode("M1", "consumer", "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9),
    SourceNode("YM1", "consumer", "merged-framework/bridges/phase-7/bridge_YM1_yang_mills_induction.py", "bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6", 9),
    SourceNode("YM2", "consumer", "merged-framework/bridges/phase-7/bridge_YM2_yang_mills_3plus1_lift.py", "19c8708ea9b81eff719362ee713dd3d933b5422788759ae6e8933c705863b11c", 10),
    SourceNode("QCD1", "consumer", "merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py", "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed", 11),
    SourceNode("QCD2", "consumer", "merged-framework/bridges/phase-8/bridge_QCD2_su3_3plus1_lift.py", "64f8125a5c0ef194e23569711036ce6ec46f3ffef2b6eb94a7b5c97ed8bb566f", 10),
    SourceNode("CF2", "consumer", "merged-framework/bridges/phase-10/bridge_CF2_linear_potential.py", "e9651b9d4db9f23bb54d013a419c2f050725063347e63f253a968781598bfe6a", 15),
    SourceNode("CF3", "consumer", "merged-framework/bridges/phase-10/bridge_CF3_wilson_area_law.py", "8655579ef3173730c315d60aa821f7085cc131920ae49cb93c60b075d884889d", 6),
    SourceNode("GK1", "consumer", "merged-framework/bridges/phase-35/bridge_GK1_gauge_kinetic_dimensionality_boundary.py", "c142538897e9168769483aeb978ea86587fa9a073e606aa204316238dfa24d74", 11),
)


@dataclass(frozen=True)
class ReplayResult:
    node: SourceNode
    check_calls: int
    legacy_trapz_calls: int
    trapezoid_calls: int
    eager_legacy_default_fallbacks: int
    returncode: int
    terminal_tally: bool
    output_tail: str


def _replay(source_root: Path, node: SourceNode) -> ReplayResult:
    path = source_root / node.relative_path
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != node.sha256:
        return ReplayResult(node, -1, -1, -1, -1, 99, False, f"hash mismatch: {digest}")
    source = payload.decode("utf-8")
    tree = ast.parse(source)
    check_calls = sum(
        isinstance(item, ast.Call)
        and isinstance(item.func, ast.Name)
        and item.func.id == "check"
        for item in ast.walk(tree)
    )
    compatibility = audit_numpy_trapezoid_compatibility(source, filename=str(path))
    legacy = compatibility.legacy_references
    current = compatibility.current_references
    if legacy:
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
        terminal_tally = re.search(
            rf"ALL\s+{node.expected_checks}\s+CHECKS\s+PASS", output
        ) is not None
        return ReplayResult(
            node,
            check_calls,
            legacy,
            current,
            compatibility.eager_legacy_default_fallbacks,
            completed.returncode,
            terminal_tally,
            "\n".join(output.splitlines()[-12:]),
        )
    except subprocess.TimeoutExpired as failure:
        return ReplayResult(
            node,
            check_calls,
            legacy,
            current,
            compatibility.eager_legacy_default_fallbacks,
            124,
            False,
            "\n".join((failure.stdout or "").splitlines()[-12:]),
        )


def main(source_root: str) -> int:
    root = Path(source_root).resolve()
    ledger = CheckLedger("P136-source-graph")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda node: _replay(root, node), NODES))

    for result in results:
        detail = result.output_tail if result.returncode or not result.terminal_tally else ""
        ledger.check(
            f"{result.node.source_unit} hash inventory exit and terminal tally",
            result.check_calls == result.node.expected_checks
            and result.returncode == 0
            and result.terminal_tally,
            detail,
        )
        mode = "alias-only" if result.legacy_trapz_calls else "native"
        print(
            f"  SOURCE {result.node.source_unit}: role={result.node.role} "
            f"checks={result.node.expected_checks} mode={mode} "
            f"np.trapz={result.legacy_trapz_calls} "
            f"np.trapezoid={result.trapezoid_calls} "
            f"eager_default={result.eager_legacy_default_fallbacks}"
        )

    ledger.check(
        "legacy integration compatibility is isolated and classified",
        {result.node.source_unit for result in results if result.legacy_trapz_calls}
        == {"YM2", "QCD2"}
        and {
            result.node.source_unit
            for result in results
            if result.eager_legacy_default_fallbacks
        }
        == {"YM2", "QCD2"},
    )
    ledger.check(
        "replayed predicate total is fixed",
        sum(result.node.expected_checks for result in results) == 140,
    )
    return int(ledger.finish())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True)
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
