"""Aggregate runner for the P241 SymPy audit modules.

Runs every per-claim module in this directory as a subprocess, collects the
JSON check records, and prints one combined report.

Usage: python3 run_sympy.py            (from anywhere)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    modules = sorted(HERE.glob("scipy/N*.py"))
    if not modules:
        print(json.dumps({"error": "no check modules found"}, indent=2))
    checks: list[dict[str, object]] = []
    failed_runs: list[str] = []
    for module in modules:
        proc = subprocess.run(
            [sys.executable, str(module)],
            capture_output=True,
            text=True,
            cwd=str(HERE),
            timeout=600,
        )
        try:
            record = json.loads(proc.stdout)
        except json.JSONDecodeError:
            failed_runs.append(module.name)
            checks.append({
                "name": module.stem,
                "claim": "P241",
                "passed": False,
                "detail": f"runner failure (rc={proc.returncode}): "
                          f"{proc.stderr.strip()[-400:]}",
            })
            continue
        record["module"] = module.name
        checks.append(record)
    report = {
        "suite": "p241-scipy-audit",
        "modules": len(modules),
        "checks": checks,
        "failed_runs": failed_runs,
        "passed": all(c["passed"] for c in checks) and not failed_runs,
    }
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
