"""Run the complete P238 oracle and disposition-closure boundary."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPECTED_IDS = {f"P238-S{index:02d}" for index in range(1, 19)}
TERMINAL_DISPOSITIONS = {"pass", "qualified", "fail"}


def run_json(path: Path) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> int:
    inventory = yaml.safe_load((HERE / "evidence" / "claim-inventory.yaml").read_text())
    results = yaml.safe_load((HERE / "evidence" / "claim-results.yaml").read_text())

    inventory_ids = {item["id"] for item in inventory["claims"]}
    result_items = results["claims"]
    result_ids = {item["id"] for item in result_items}
    issues_complete = all(item.get("issue", "").startswith("https://github.com/") for item in result_items)
    dispositions_terminal = all(
        item.get("resolved") is True and item.get("disposition") in TERMINAL_DISPOSITIONS
        for item in result_items
    )
    counts = {
        disposition: sum(item["disposition"] == disposition for item in result_items)
        for disposition in sorted(TERMINAL_DISPOSITIONS)
    }

    sympy_result = run_json(HERE / "companion" / "sympy_checks.py")
    scipy_result = run_json(HERE / "companion" / "scipy_checks.py")
    lean_file = HERE / "companion" / "P238PaperChecks.lean"
    lean_result = subprocess.run(
        ["lake", "env", "lean", str(lean_file)],
        cwd=ROOT / "formal",
        capture_output=True,
        text=True,
    )

    checks = {
        "inventory_exact": inventory_ids == EXPECTED_IDS,
        "results_exact": result_ids == EXPECTED_IDS and len(result_items) == 18,
        "issues_complete": issues_complete,
        "dispositions_terminal": dispositions_terminal,
        "counts_match": counts == {"fail": 9, "pass": 5, "qualified": 4},
        "no_open_debt": results.get("open_debt") == [],
        "sympy": all(item["passed"] for item in sympy_result["checks"]),
        "scipy": all(item["passed"] for item in scipy_result["checks"]),
        "lean": lean_result.returncode == 0,
    }
    report = {
        "campaign": "P238",
        "checks": checks,
        "oracle_counts": {
            "sympy": len(sympy_result["checks"]),
            "scipy": len(scipy_result["checks"]),
            "lean_theorems": 10,
        },
        "claim_counts": counts,
        "lean_stderr": lean_result.stderr,
    }
    print(json.dumps(report, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
