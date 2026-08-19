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
ISSUE_BASE = "https://github.com/vantasnerdan/substrate-framework/issues"
EXPECTED_ISSUES = {
    f"P238-S{index:02d}": f"{ISSUE_BASE}/{108 + index}"
    for index in range(1, 19)
}
REVIEW_OUTCOMES = {"supported", "revision_required"}
REVISION_IDS = {
    "P238-S01",
    "P238-S02",
    "P238-S03",
    "P238-S05",
    "P238-S06",
    "P238-S07",
    "P238-S08",
    "P238-S11",
    "P238-S12",
    "P238-S15",
    "P238-S16",
    "P238-S17",
    "P238-S18",
}


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
    reuse_audit = yaml.safe_load(
        (HERE / "evidence" / "solution-reuse-audit.yaml").read_text()
    )

    inventory_ids = {item["id"] for item in inventory["claims"]}
    result_items = results["claims"]
    result_ids = {item["id"] for item in result_items}
    issues_complete = all(
        item.get("issue") == EXPECTED_ISSUES[item["id"]] for item in result_items
    )
    reviews_complete = all(
        item.get("resolved") is True
        and item.get("disposition") in REVIEW_OUTCOMES
        and bool(item.get("repair_class"))
        for item in result_items
    )
    counts = {
        disposition: sum(item["disposition"] == disposition for item in result_items)
        for disposition in sorted(REVIEW_OUTCOMES)
    }

    sympy_result = run_json(HERE / "companion" / "sympy_checks.py")
    scipy_result = run_json(HERE / "companion" / "scipy_checks.py")
    sympy_replacements = run_json(HERE / "companion" / "sympy_replacements.py")
    scipy_replacement = run_json(HERE / "companion" / "scipy_replacements.py")
    replacement_claim_ids = {
        claim_id
        for replacement in sympy_replacements["replacements"]
        for claim_id in replacement["claims"].split()
    }
    replacement_claim_ids.update(
        scipy_claim_id for scipy_claim_id in scipy_replacement["claims"].split()
    )
    reused_solution_claim_ids = {
        claim_id
        for replacement in reuse_audit["replacement_claims"]
        for claim_id in replacement["claims"]
    }
    lean_files = [
        HERE / "companion" / "P238PaperChecks.lean",
        HERE / "companion" / "P238ReplacementProofs.lean",
    ]
    lean_results = [
        subprocess.run(
            ["lake", "env", "lean", str(lean_file)],
            cwd=ROOT / "formal",
            capture_output=True,
            text=True,
        )
        for lean_file in lean_files
    ]

    checks = {
        "inventory_exact": inventory_ids == EXPECTED_IDS,
        "results_exact": result_ids == EXPECTED_IDS and len(result_items) == 18,
        "issues_complete": issues_complete,
        "reviews_complete": reviews_complete,
        "counts_match": counts == {"revision_required": 13, "supported": 5},
        "no_open_debt": results.get("open_debt") == [],
        "sympy": all(item["passed"] for item in sympy_result["checks"]),
        "scipy": all(item["passed"] for item in scipy_result["checks"]),
        "sympy_replacements": all(
            item["passed"] for item in sympy_replacements["replacements"]
        ),
        "scipy_replacement": scipy_replacement["passed"],
        "revision_replacement_coverage": replacement_claim_ids == REVISION_IDS,
        "repository_solution_reuse_coverage": (
            reused_solution_claim_ids == REVISION_IDS
            and reuse_audit.get("scientific_role", "").startswith(
                "Implementation source only."
            )
        ),
        "lean": all(result.returncode == 0 for result in lean_results),
    }
    report = {
        "campaign": "P238",
        "checks": checks,
        "oracle_counts": {
            "sympy": len(sympy_result["checks"]),
            "scipy": len(scipy_result["checks"]),
            "lean_theorems": 11,
            "sympy_replacements": len(sympy_replacements["replacements"]),
            "scipy_replacements": 2,
            "lean_replacement_theorems": 9,
        },
        "claim_counts": counts,
        "lean_stderr": [result.stderr for result in lean_results],
    }
    print(json.dumps(report, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
