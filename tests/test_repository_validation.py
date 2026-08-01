from __future__ import annotations

import pytest

from scripts.validate_repository import (
    validate_accepted_artifact_paths,
    validate_memory_contract_categories,
)
from substrate_framework.governance import GovernanceError


def test_memory_contract_category_validation_is_sensitive(tmp_path) -> None:
    templates = tmp_path / "memory-templates"
    templates.mkdir()
    (templates / "effort.md").write_text("category: efforts\n", encoding="utf-8")
    (tmp_path / ".agent-memory.yaml").write_text(
        "categories:\n  - proposals\n", encoding="utf-8"
    )

    with pytest.raises(GovernanceError, match="unconfigured categories"):
        validate_memory_contract_categories(tmp_path)

    (tmp_path / ".agent-memory.yaml").write_text(
        "categories:\n  - efforts\n", encoding="utf-8"
    )
    validate_memory_contract_categories(tmp_path)


def test_accepted_artifact_validation_rejects_missing_evidence(tmp_path) -> None:
    claim = {
        "id": "C1",
        "accepted_in": "v1",
        "provenance": "campaigns/P1/adjudication.yaml",
        "evidence": ["tests/test_claim.py"],
    }
    registry = {"claims": [claim]}

    with pytest.raises(GovernanceError, match="does not exist"):
        validate_accepted_artifact_paths(tmp_path, registry)

    provenance = tmp_path / claim["provenance"]
    evidence = tmp_path / claim["evidence"][0]
    provenance.parent.mkdir(parents=True)
    evidence.parent.mkdir(parents=True)
    provenance.write_text("status: accepted\n", encoding="utf-8")
    evidence.write_text("def test_claim(): pass\n", encoding="utf-8")
    validate_accepted_artifact_paths(tmp_path, registry)
