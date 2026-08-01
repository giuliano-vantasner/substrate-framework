from __future__ import annotations

import pytest

from substrate_framework.governance import (
    GovernanceError,
    validate_proposal,
    validate_registry,
    validate_release,
)
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


def test_proposal_requires_immutable_source_baseline() -> None:
    proposal = {
        "id": "P000",
        "base_release": None,
        "source_baseline": "substrate@6d1f4e0",
        "question": "derive a positive root claim",
        "invariants": ["normalized sine-Gordon convention"],
        "allowed_imports": ["real analysis"],
        "candidates": [
            {"id": "A", "description": "closed-form construction"},
            {"id": "B", "description": "independent transform construction"},
        ],
        "selection_criteria": ["exact dependency closure"],
        "claims_proposed": ["C-SG-001"],
        "comparators_blinded_until": "structural review complete",
        "status": "draft",
    }

    validate_proposal(proposal)
    proposal["source_baseline"] = ""
    with pytest.raises(GovernanceError, match="immutable source revision"):
        validate_proposal(proposal)


def test_release_requires_dependency_closed_claim_set() -> None:
    registry = {
        "schema_version": 1,
        "claims": [claim("C1", []), claim("C2", ["C1"])],
    }
    release = {
        "schema_version": 1,
        "release": "v-test",
        "source_baseline": "source@abc123",
        "released_at": "2026-08-01T00:00:00Z",
        "accepted_claims": ["C2"],
    }

    with pytest.raises(GovernanceError, match="dependencies outside release"):
        validate_release(release, registry)

    release["accepted_claims"] = ["C1", "C2"]
    assert validate_release(release, registry, require_current_set=True) == ["C1", "C2"]
