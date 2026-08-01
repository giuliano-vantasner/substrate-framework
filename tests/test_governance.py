from __future__ import annotations

import pytest

from substrate_framework.governance import GovernanceError, validate_registry
from substrate_framework.verification import CheckFailure, CheckLedger


def claim(claim_id: str, dependencies: list[str], accepted: bool = True) -> dict:
    return {
        "id": claim_id,
        "statement": f"statement for {claim_id}",
        "provenance": "proposal-P000",
        "verification": "symbolic_verified" if accepted else "unverified",
        "review": "accepted" if accepted else "unaudited",
        "compatibility": "native" if accepted else "unassessed",
        "epistemic": "active" if accepted else "proposed",
        "dependencies": dependencies,
        "evidence": ["tests/test_governance.py"] if accepted else [],
        "assumptions": [],
        "comparators": [],
        "accepted_in": "v-test" if accepted else None,
    }


def test_empty_registry_is_valid_bootstrap() -> None:
    assert validate_registry({"schema_version": 1, "claims": []}) == []


def test_accepted_dependency_closure_is_valid() -> None:
    data = {"schema_version": 1, "claims": [claim("C1", []), claim("C2", ["C1"])]}
    assert validate_registry(data) == ["C1", "C2"]


def test_accepted_claim_cannot_depend_on_proposal() -> None:
    data = {
        "schema_version": 1,
        "claims": [claim("C1", [], accepted=False), claim("C2", ["C1"])],
    }
    with pytest.raises(GovernanceError, match="depends on noncurrent"):
        validate_registry(data)


def test_dependency_cycle_fails() -> None:
    data = {"schema_version": 1, "claims": [claim("C1", ["C2"]), claim("C2", ["C1"])]}
    with pytest.raises(GovernanceError, match="dependency cycle"):
        validate_registry(data)


def test_mutation_gate_rejects_insensitive_check() -> None:
    ledger = CheckLedger("C-test")
    with pytest.raises(CheckFailure, match="insensitive"):
        ledger.mutation_sensitive("value", lambda _: True, 1, [2])


def test_supersession_preserves_historical_claim() -> None:
    old = claim("C1", [])
    old["epistemic"] = "superseded"
    old["compatibility"] = "conflict"
    new = claim("C2", [])
    new["supersedes"] = ["C1"]
    assert validate_registry({"schema_version": 1, "claims": [old, new]}) == ["C1", "C2"]
