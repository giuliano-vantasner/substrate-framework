"""Run the complete P241 oracle and disposition-closure boundary."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
CORPUS = REPOSITORY / "corpus"
EXPECTED_IDS = {f"P241-S{index:02d}" for index in range(1, 24)}
PAPER_SHA256 = (
    "dc23cbd98a551cb95d2409ab6bef0b1720303d420b6fb0d2b44a9ddd2f580783"
)
REVIEW_OUTCOMES = {"supported", "revision_required"}
REVISION_IDS = {
    "P241-S02",
    "P241-S05",
    "P241-S06",
    "P241-S08",
    "P241-S10",
    "P241-S18",
    "P241-S19",
    "P241-S20",
    "P241-S21",
    "P241-S23",
}
LEAN_FILES = [
    CORPUS / "lean" / "P241PaperChecks.lean",
    CORPUS / "lean" / "P241ReplacementProofs.lean",
]


def run_json(path: Path) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(path.parent),
        check=True,
        capture_output=True,
        text=True,
        timeout=1800,
    )
    return json.loads(completed.stdout)


def run_lean() -> list[subprocess.CompletedProcess[str]]:
    project_dir = os.environ.get("LEAN_PROJECT_DIR")
    results = []
    for lean_file in LEAN_FILES:
        if project_dir:
            cmd = ["lake", "env", "lean", str(lean_file)]
            results.append(subprocess.run(
                cmd, cwd=project_dir, capture_output=True, text=True,
                timeout=600))
        else:
            results.append(subprocess.run(
                ["lake", "env", "lean", lean_file.name],
                cwd=str(lean_file.parent), capture_output=True, text=True,
                timeout=600))
    return results


def main() -> int:
    inventory = yaml.safe_load((REPOSITORY / "claims" / "inventory.yaml").read_text())
    results = yaml.safe_load((REPOSITORY / "claims" / "results.yaml").read_text())

    inventory_ids = {item["id"] for item in inventory["claims"]}
    result_items = results["claims"]
    result_ids = {item["id"] for item in result_items}
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
    revision_ids = {
        item["id"] for item in result_items
        if item["disposition"] == "revision_required"
    }

    sympy_result = run_json(CORPUS / "checks" / "run_sympy.py")
    scipy_result = run_json(CORPUS / "checks" / "run_scipy.py")
    records_result = run_json(CORPUS / "replacements" / "records.py")

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "p241_records", CORPUS / "replacements" / "records.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    record_claims = set()
    for record in module.RECORDS:
        # claims field like "P241-S05/S06": collect every P241-Sxx mentioned
        for token in str(record["claim"]).replace("/", " ").split():
            token = token.strip()
            if token.startswith("P241-S"):
                record_claims.add(token)
            elif token.startswith("S") and token[1:].isdigit():
                record_claims.add(f"P241-{token}")

    lean_results = run_lean()
    lean_theorems = sum(
        len([line for line in f.read_text().splitlines()
             if line.startswith(("theorem ", "lemma "))])
        for f in LEAN_FILES
    )

    checks = {
        "inventory_exact": inventory_ids == EXPECTED_IDS,
        "results_exact": result_ids == EXPECTED_IDS and len(result_items) == 23,
        "reviews_complete": reviews_complete,
        "revision_set_matches": revision_ids == REVISION_IDS,
        "counts_match": counts == {"revision_required": 10, "supported": 13},
        "no_open_debt": results.get("open_debt") == [],
        "paper_sha_matches": inventory.get("paper_sha256") == PAPER_SHA256,
        "sympy": all(c["passed"] for c in sympy_result["checks"]),
        "scipy": all(c["passed"] for c in scipy_result["checks"]),
        "replacement_records": bool(records_result["passed"]),
        "revision_replacement_coverage": (
            REVISION_IDS <= record_claims and record_claims <= EXPECTED_IDS
        ),
        "lean": all(r.returncode == 0 for r in lean_results),
    }
    report = {
        "campaign": "P241",
        "checks": checks,
        "oracle_counts": {
            "sympy_modules": len(sympy_result["checks"]),
            "scipy_modules": len(scipy_result["checks"]),
            "lean_theorems": lean_theorems,
            "replacement_records": len(module.RECORDS),
        },
        "claim_counts": counts,
        "lean_stderr": [r.stderr[-500:] for r in lean_results if r.returncode],
    }
    print(json.dumps(report, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
