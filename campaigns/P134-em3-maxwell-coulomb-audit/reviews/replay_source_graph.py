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
    SourceNode("EM2", "dependency_and_consumer", "merged-framework/bridges/phase-3/bridge_EM2_gauge_u1_minimal_coupling.py", "9787ae25521e19d926de0f9addafd16353bebc149cea83f3d9dd4c491fef91d6", 11),
    SourceNode("G1", "declared_dependency", "merged-framework/bridges/phase-5/bridge_G1_radiating_dilaton_source.py", "580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876", 10),
    SourceNode("G2", "declared_dependency", "merged-framework/bridges/phase-5/bridge_G2_gordon_metric_3plus1.py", "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88", 6),
    SourceNode("G3", "declared_dependency", "merged-framework/bridges/phase-5/bridge_G3_horndeski_scalar_tensor.py", "8d462ce2bfd57bfced9fdedd511e9d2711e0c2454bc0d0441c681288495719ba", 11),
    SourceNode("EM5", "consumer", "merged-framework/bridges/phase-3/bridge_EM5_induced_gauge_sector.py", "bcf2c49e1e98eefea98be0076afd29341ce80fd71a7b141618978139982e4ec0", 11),
    SourceNode("EM7", "consumer", "merged-framework/bridges/phase-3/bridge_EM7_fractal_force_law.py", "c8bf044d846d22eaa652a0f4c11cd5f5e2a51f98e49d0578536fbc4e96f63f22", 17),
    SourceNode("S5", "consumer", "merged-framework/bridges/phase-4/bridge_S5_realizability_magnitude.py", "b92a9db67940169fcd9919f83fda6ae8c56b9b9e40b0d2cbebef5539a5dccde6", 28),
    SourceNode("W2", "consumer", "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py", "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16", 9),
    SourceNode("W7", "consumer", "merged-framework/bridges/phase-6/bridge_W7_su2L_gauging_charged_current.py", "1a1fa278f6b8a0cab74d020fc01db1fa3576f57084d0cd80959867c591bf66c3", 11),
    SourceNode("M1", "consumer", "merged-framework/bridges/phase-7/bridge_M1_anderson_higgs_mass_matrix.py", "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f", 9),
    SourceNode("YM1", "consumer", "merged-framework/bridges/phase-7/bridge_YM1_yang_mills_induction.py", "bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6", 9),
    SourceNode("YM2", "consumer", "merged-framework/bridges/phase-7/bridge_YM2_yang_mills_3plus1_lift.py", "19c8708ea9b81eff719362ee713dd3d933b5422788759ae6e8933c705863b11c", 10),
    SourceNode("QCD2", "consumer", "merged-framework/bridges/phase-8/bridge_QCD2_su3_3plus1_lift.py", "64f8125a5c0ef194e23569711036ce6ec46f3ffef2b6eb94a7b5c97ed8bb566f", 10),
    SourceNode("CF2", "consumer", "merged-framework/bridges/phase-10/bridge_CF2_linear_potential.py", "e9651b9d4db9f23bb54d013a419c2f050725063347e63f253a968781598bfe6a", 15),
    SourceNode("D3S", "consumer", "merged-framework/bridges/phase-19/bridge_D3S_coulomb_from_sg.py", "a5ff9c760cf8776115881d7a2e5e86c562cdf461f61f36784ff95c6381d24d71", 13),
    SourceNode("GK1", "consumer", "merged-framework/bridges/phase-35/bridge_GK1_gauge_kinetic_dimensionality_boundary.py", "c142538897e9168769483aeb978ea86587fa9a073e606aa204316238dfa24d74", 11),
    SourceNode("GK3D1", "consumer", "merged-framework/bridges/phase-41/bridge_GK3D1_master_polarization_general_D.py", "9a25110ba53adfb439d0cfd0570bd311b0a43a20f13d1351f45c3fa4075aeacb", 19),
    SourceNode("GK3D2", "consumer", "merged-framework/bridges/phase-41/bridge_GK3D2_induced_kinetic_normalization.py", "856096aba38812dc17fb07ce5cf7c0fa13eb2623665ccf871810734ac3ca0886", 17),
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
    compatibility = audit_numpy_trapezoid_compatibility(
        source,
        filename=str(path),
    )
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
        tally = re.search(
            rf"ALL\s+{node.expected_checks}\s+CHECKS\s+PASS",
            output,
        ) is not None
        tail = "\n".join(output.splitlines()[-12:])
        return ReplayResult(
            node,
            check_calls,
            legacy,
            current,
            compatibility.eager_legacy_default_fallbacks,
            completed.returncode,
            tally,
            tail,
        )
    except subprocess.TimeoutExpired as failure:
        tail = "\n".join((failure.stdout or "").splitlines()[-12:])
        return ReplayResult(
            node,
            check_calls,
            legacy,
            current,
            compatibility.eager_legacy_default_fallbacks,
            124,
            False,
            tail,
        )


def main(source_root: str) -> int:
    root = Path(source_root).resolve()
    ledger = CheckLedger("P134-source-graph")
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

    legacy_units = {
        result.node.source_unit
        for result in results
        if result.legacy_trapz_calls
    }
    ledger.check(
        "legacy integration compatibility is isolated and classified",
        legacy_units == {"G1", "YM2", "QCD2"}
        and {
            result.node.source_unit
            for result in results
            if result.eager_legacy_default_fallbacks
        }
        == {"YM2", "QCD2"},
    )
    ledger.check(
        "replayed predicate total is fixed",
        sum(result.node.expected_checks for result in results) == 227,
    )
    return int(ledger.finish())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True)
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_root))
