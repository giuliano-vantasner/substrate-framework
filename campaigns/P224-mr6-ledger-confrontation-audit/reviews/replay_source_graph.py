"""Hash-sensitive final MR6 source and migration-closure replay."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


CAMPAIGN = Path(__file__).resolve().parents[1]
ROOT = CAMPAIGN.parents[1]
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCE_PATH = "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py"
SOURCE_SHA = "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d"


def main() -> int:
    checks = CheckLedger("P224-GRAPH")
    status = subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "status", "--porcelain", "--", SOURCE_PATH],
        capture_output=True,
        text=True,
        check=True,
    )
    checks.check("the pinned final source path is clean", status.stdout == "")
    payload = (SOURCE_ROOT / SOURCE_PATH).read_bytes()
    source = payload.decode("utf-8")
    tree = ast.parse(source)
    check_count = sum(
        isinstance(item, ast.Call)
        and isinstance(item.func, ast.Name)
        and item.func.id == "check"
        for item in ast.walk(tree)
    )
    assertion_count = sum(isinstance(item, ast.Assert) for item in ast.walk(tree))
    checks.check(
        "MR6 retains its pinned hash six predicates and three assertions",
        hashlib.sha256(payload).hexdigest() == SOURCE_SHA
        and check_count == 6
        and assertion_count == 3,
    )
    compatibility = audit_numpy_trapezoid_compatibility(source, filename=SOURCE_PATH)
    checks.check(
        "MR6 uses current SciPy trapezoid with no legacy access",
        "from scipy.integrate import solve_bvp, trapezoid" in source
        and compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    p215 = yaml.safe_load(
        (
            ROOT
            / "campaigns/P215-mk2-vector-sextic-matching-audit/evidence/source-graph-inventory.yaml"
        ).read_text()
    )
    reused = {row["label"]: row for row in p215["replay"]}["MR6"]
    checks.check(
        "hash-identical final native execution is reused without rerun",
        reused["runtime_checks"] == 6
        and reused["assertions"] == 3
        and reused["verdict"] == "clean_noncanonical",
    )
    inventory = yaml.safe_load((ROOT / "migration/source-claims.yaml").read_text())
    units = {entry["source_unit"]: entry for entry in inventory["units"]}
    proposal = yaml.safe_load((CAMPAIGN / "proposal.yaml").read_text())
    if proposal["status"] == "accepted":
        adjudication = yaml.safe_load((CAMPAIGN / "adjudication.yaml").read_text())
        expected_disposition = adjudication["source_disposition"]["MR6"]
        expected_claims = set(adjudication["accepted_mappings"])
        expected_pending = 0
    else:
        expected_disposition = "pending_adjudication"
        expected_claims = set()
        expected_pending = 1
    checks.check(
        "MR6 state agrees exactly with its governed campaign transaction",
        units["MR6"]["disposition"] == expected_disposition
        and set(units["MR6"]["accepted_claims"]) == expected_claims,
    )
    pending = [
        label
        for label, unit in units.items()
        if unit["disposition"] == "pending_adjudication"
    ]
    checks.check(
        "the global pending queue matches the final campaign state",
        len(pending) == expected_pending
        and (pending == ["MR6"] if expected_pending else pending == []),
    )
    dispositions = yaml.safe_load((ROOT / "migration/dispositions.yaml").read_text())[
        "units"
    ]
    checks.check(
        "all predecessor MK and MR units remain individually terminal",
        all(
            dispositions[label]["disposition"] != "pending_adjudication"
            for label in (
                "MK1", "MK2", "MK3", "MK4", "MK5", "MK6",
                "MR1", "MR2", "MR3", "MR4", "MR5",
            )
        ),
    )
    checks.check(
        "MR6 adds no package API claim or backward authority",
        proposal["claims_proposed"] == []
        and "substrate_framework" not in source
        and yaml.safe_load(
            (CAMPAIGN / "evidence/post-source-claim-delta.yaml").read_text()
        )["package_change"]
        == "none",
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
