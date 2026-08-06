"""Pinned predecessor and reverse-consumer replay for the P215 MK2 audit."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
import subprocess
import time

import numpy as np

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")


@dataclass(frozen=True)
class SourceNode:
    label: str
    path: str
    sha256: str
    lexical_checks: int
    assertions: int
    relation: str


NODES = (
    SourceNode("S4", "merged-framework/bridges/phase-4/bridge_S4_c4_vector_meson_closure.py", "49c7b2392bbe23d2824f4f73030ccd30f245e1750e0c7736dc420d3f64d7a780", 11, 1, "qualified_predecessor"),
    SourceNode("WZ2", "merged-framework/bridges/phase-17/bridge_WZ2_level_quantization_pi5.py", "f991e222f038268077d3f50e759beeec95ac65f06a8369011ecc0e0ad79ce3ff", 8, 1, "qualified_predecessor"),
    SourceNode("WZ3", "merged-framework/bridges/phase-17/bridge_WZ3_goldstone_wilczek_baryon_current.py", "30da2ac41a0d46c48bd4e1b9733c3712d0b6c1c9b4838f1a1df3c4db22cc3569", 7, 1, "qualified_predecessor_alias_only"),
    SourceNode("WZ4", "merged-framework/bridges/phase-17/bridge_WZ4_hls_vector_meson_anomalous.py", "fca6b9c1d95bdf49e99b863470c7e800880e493b3f716159aa2341f8cf963d2b", 9, 1, "qualified_predecessor"),
    SourceNode("KI1", "merged-framework/bridges/phase-34/bridge_KI1_exhaustive_coupling_search.py", "a1ec5f8e64e56165d2c51ad2389ecb455870572ba4ef9eca292151bde4ddb42b", 5, 1, "refuted_predecessor"),
    SourceNode("KI2", "merged-framework/bridges/phase-34/bridge_KI2_epsilon_underdetermination.py", "9e16fc6fafa940f43d559ea0f6a9c2730940d1247f36f655375c2f75f6fd1e81", 6, 1, "qualified_predecessor"),
    SourceNode("MK1", "merged-framework/bridges/phase-43/bridge_MK1_mu_from_medium_cosine.py", "98ff5459ae3c6cb64a9a7632fbaa8613f1f5b1adb68419de25ffa06b1c3a3222", 7, 1, "qualified_predecessor"),
    SourceNode("MK2", "merged-framework/bridges/phase-43/bridge_MK2_lambda_from_medium_omega.py", "351136bca28e413ddd54f1b15bf7084dffe32af565fc87e7220d1437a525eb07", 7, 1, "audited_root"),
    SourceNode("MK3", "merged-framework/bridges/phase-43/bridge_MK3_epsilon_pinned.py", "64254d0f6b9d6ff57f5a8b0a4b86a510e2bef230b4f3bec062533fac59516404", 6, 1, "pending_reverse_consumer"),
    SourceNode("MK4", "merged-framework/bridges/phase-43/bridge_MK4_bps_compacton_and_pt_failure.py", "9f2e299032aace53c3ac2c2d1d5626372e4bdf1aa3b7b0650f574a9f7b8f7295", 6, 1, "pending_reverse_consumer"),
    SourceNode("MK5", "merged-framework/bridges/phase-43/bridge_MK5_generalized_solve_kappa.py", "a5ecb5d0d2ba96cf8083a9cfb32ddb44c2a4f4841bf776ebbccb91bc12b246f8", 8, 1, "pending_reverse_consumer"),
    SourceNode("MK6", "merged-framework/bridges/phase-43/bridge_MK6_confrontation_and_tension.py", "ef900954d9782bbf2589ff3e33045577ebdce3860d1a3ed7a6a6827e0ae81788", 6, 1, "pending_reverse_consumer"),
    SourceNode("MR2", "merged-framework/bridges/phase-44/bridge_MR2_bps_normalization_pi_squared.py", "2e62ce2d6cbee805a988046a27a742e622931291e8e013a9aede6ce16e48e990", 8, 1, "pending_reverse_consumer"),
    SourceNode("MR4", "merged-framework/bridges/phase-44/bridge_MR4_e_from_rho_saturation.py", "cefe7192b935ec18992e9cd76fd348ef81934ed9d20843ced3627973cec9d3d7", 7, 1, "pending_reverse_consumer"),
    SourceNode("MR6", "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py", "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d", 6, 3, "pending_reverse_consumer"),
)

REVERSE_CONSUMERS = {"MK3", "MK4", "MK5", "MK6", "MR2", "MR4", "MR6"}
TALLY = re.compile(r"ALL\s+(\d+)\s+CHECKS\s+PASS(?:ED)?", re.IGNORECASE)


def _command(node: SourceNode, path: Path) -> list[str]:
    if node.label != "WZ3":
        return [str(ROOT / ".venv/bin/python"), str(path)]
    return [
        str(ROOT / ".venv/bin/python"),
        "-c",
        (
            "import numpy as np, runpy; "
            "np.trapz=np.trapezoid; "
            f"runpy.run_path({str(path)!r}, run_name='__main__')"
        ),
    ]


def main() -> int:
    checks = CheckLedger("P215-GRAPH")
    rows: list[dict[str, object]] = []
    for node in NODES:
        path = SOURCE_ROOT / node.path
        payload = path.read_bytes()
        text = payload.decode("utf-8")
        tree = ast.parse(text, filename=node.path)
        compatibility = audit_numpy_trapezoid_compatibility(text, filename=node.path)
        started = time.monotonic()
        result = subprocess.run(
            _command(node, path),
            cwd=SOURCE_ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=150,
        )
        elapsed = time.monotonic() - started
        terminal = TALLY.findall(result.stdout)
        rows.append(
            {
                "label": node.label,
                "hash_ok": hashlib.sha256(payload).hexdigest() == node.sha256,
                "lexical_checks": sum(
                    isinstance(item, ast.Call)
                    and isinstance(item.func, ast.Name)
                    and item.func.id == "check"
                    for item in ast.walk(tree)
                ),
                "assertions": sum(
                    isinstance(item, ast.Assert) for item in ast.walk(tree)
                ),
                "legacy": compatibility.legacy_references,
                "current": compatibility.current_references,
                "eager": compatibility.eager_legacy_default_fallbacks,
                "returncode": result.returncode,
                "terminal": int(terminal[-1]) if terminal else None,
                "elapsed": elapsed,
                "mentions_MK2": "MK2" in text,
            }
        )

    by_label = {str(row["label"]): row for row in rows}
    expected = {node.label: node for node in NODES}
    checks.check(
        "all fifteen source nodes retain their pinned hashes",
        len(rows) == 15 and all(bool(row["hash_ok"]) for row in rows),
    )
    checks.check(
        "graph inventory pins 107 lexical predicates and 17 assertions",
        sum(int(row["lexical_checks"]) for row in rows) == 107
        and sum(int(row["assertions"]) for row in rows) == 17
        and all(
            row["lexical_checks"] == expected[str(row["label"])].lexical_checks
            and row["assertions"] == expected[str(row["label"])].assertions
            for row in rows
        ),
    )
    checks.check(
        "every nonrefuted node exits cleanly with its full runtime tally",
        all(
            row["returncode"] == 0
            and row["terminal"] == row["lexical_checks"]
            for row in rows
            if row["label"] != "KI1"
        ),
    )
    checks.check(
        "KI1 alone stops at its governed refutation rather than becoming authority",
        by_label["KI1"]["returncode"] != 0
        and by_label["KI1"]["terminal"] is None,
    )
    checks.check(
        "WZ3 is the sole direct legacy surface and receives alias-only replay",
        hasattr(np, "trapezoid")
        and not hasattr(np, "trapz")
        and {
            str(row["label"])
            for row in rows
            if int(row["legacy"]) > 0 or int(row["current"]) > 0
        }
        == {"WZ3"}
        and by_label["WZ3"]["legacy"] == 1
        and by_label["WZ3"]["current"] == 0
        and all(int(row["eager"]) == 0 for row in rows),
    )
    checks.check(
        "all seven in-scope reverse consumers name MK2 explicitly",
        all(bool(by_label[label]["mentions_MK2"]) for label in REVERSE_CONSUMERS),
    )
    checks.check(
        "dirty untracked phase47 and phase48 files are excluded from the pinned graph",
        not any(node.label.startswith(("BM", "CE")) for node in NODES),
    )

    for row in rows:
        print(
            "GRAPH",
            row["label"],
            f"checks={row['terminal']}",
            f"assertions={row['assertions']}",
            f"legacy={row['legacy']}",
            f"current={row['current']}",
            f"eager={row['eager']}",
            f"seconds={float(row['elapsed']):.3f}",
        )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
