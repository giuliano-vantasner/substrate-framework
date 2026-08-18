from __future__ import annotations

import pytest

from scripts.validate_repository import (
    validate_accepted_artifact_paths,
    validate_memory_contract_categories,
    validate_migration_inventory,
    validate_migration_unit_disposition,
    validate_repository_skills,
    validate_reserved_claim_identifiers,
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


def test_repository_skill_validation_checks_discovery_metadata(tmp_path) -> None:
    skill = tmp_path / ".agents/skills/theorem-synthesis"
    (skill / "agents").mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\n"
        "name: theorem-synthesis\n"
        "description: Compose accepted claims.\n"
        "---\n"
        "# Theorem Synthesis\n",
        encoding="utf-8",
    )
    (skill / "agents/openai.yaml").write_text(
        "interface:\n"
        '  display_name: "Theorem Synthesis"\n'
        '  short_description: "Compose claims into higher theorems"\n'
        '  default_prompt: "Use $theorem-synthesis to prove a higher theorem."\n',
        encoding="utf-8",
    )

    assert validate_repository_skills(tmp_path) == 1
    metadata = skill / "agents/openai.yaml"
    metadata.write_text(
        metadata.read_text(encoding="utf-8").replace(
            "$theorem-synthesis", "$wrong-skill"
        ),
        encoding="utf-8",
    )
    with pytest.raises(GovernanceError, match="must mention"):
        validate_repository_skills(tmp_path)


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


def test_accepted_artifact_validation_includes_glue_and_secondary_evidence(
    tmp_path,
) -> None:
    claim = {
        "id": "C3",
        "accepted_in": "v1",
        "provenance": "campaigns/P1/adjudication.yaml",
        "evidence": ["tests/test_claim.py"],
        "composition": {
            "glue": {"artifact": "formal/SubstrateFramework/Glue.lean"}
        },
        "verification_evidence": [
            {"artifact": "campaigns/P1/evidence/measurement.json"}
        ],
    }
    for artifact in (claim["provenance"], *claim["evidence"]):
        path = tmp_path / artifact
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("evidence\n", encoding="utf-8")

    with pytest.raises(GovernanceError, match="Glue.lean"):
        validate_accepted_artifact_paths(tmp_path, {"claims": [claim]})

    glue = tmp_path / "formal/SubstrateFramework/Glue.lean"
    glue.parent.mkdir(parents=True)
    glue.write_text("theorem glue : True := by trivial\n", encoding="utf-8")
    with pytest.raises(GovernanceError, match="measurement.json"):
        validate_accepted_artifact_paths(tmp_path, {"claims": [claim]})

    measurement = tmp_path / "campaigns/P1/evidence/measurement.json"
    measurement.parent.mkdir(parents=True)
    measurement.write_text("{}\n", encoding="utf-8")
    validate_accepted_artifact_paths(tmp_path, {"claims": [claim]})


def test_rejected_claim_identifier_remains_reserved(tmp_path) -> None:
    campaign = tmp_path / "campaigns/P1"
    campaign.mkdir(parents=True)
    (campaign / "adjudication.yaml").write_text(
        "rejected_claims:\n"
        "  - id: C-SG-014\n"
        "    review: rejected\n"
        "    epistemic: refuted\n",
        encoding="utf-8",
    )
    registry = {
        "claims": [{"id": "C-SG-014", "accepted_in": "v2"}]
    }
    with pytest.raises(GovernanceError, match="reuse adjudicated rejected"):
        validate_reserved_claim_identifiers(tmp_path, registry)

    registry["claims"][0]["id"] = "C-SG-015"
    validate_reserved_claim_identifiers(tmp_path, registry)


def test_migration_inventory_rejects_unknown_accepted_mapping(tmp_path) -> None:
    migration = tmp_path / "migration"
    evidence = tmp_path / "campaigns/P001/evidence"
    migration.mkdir(parents=True)
    evidence.mkdir(parents=True)
    source_inventory = {
        "source_baseline": "source@abc",
        "tree_sha256": "tree",
        "bridge_records": [
            {"label": "A1", "path": "bridge_A1.py", "sha256": "file"}
        ],
    }
    (evidence / "source-inventory.yaml").write_text(
        __import__("yaml").safe_dump(source_inventory), encoding="utf-8"
    )
    (migration / "scope.yaml").write_text(
        __import__("yaml").safe_dump(
            {
                "schema_version": 1,
                "source_baseline": "source@abc",
                "tree_sha256": "tree",
                "source_inventory": "campaigns/P001/evidence/source-inventory.yaml",
                "expected_primary_units": 1,
            }
        ),
        encoding="utf-8",
    )
    (migration / "dispositions.yaml").write_text(
        __import__("yaml").safe_dump(
            {
                "schema_version": 1,
                "source_baseline": "source@abc",
                "allowed_dispositions": ["migrated"],
            }
        ),
        encoding="utf-8",
    )
    (migration / "source-claims.yaml").write_text(
        __import__("yaml").safe_dump(
            {
                "schema_version": 1,
                "source_baseline": "source@abc",
                "tree_sha256": "tree",
                "primary_unit_count": 1,
                "disposition_counts": {"migrated": 1},
                "units": [
                    {
                        "source_unit": "A1",
                        "path": "bridge_A1.py",
                        "sha256": "file",
                        "disposition": "migrated",
                        "accepted_claims": ["C-UNKNOWN"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(GovernanceError, match="unknown accepted claims"):
        validate_migration_inventory(tmp_path, {"claims": []})


def test_terminal_migration_disposition_requires_reason_and_evidence(tmp_path) -> None:
    allowed = {"qualified", "refuted", "duplicate_evidence", "out_of_scope"}
    base = {
        "source_unit": "A1",
        "accepted_claims": ["C1"],
        "disposition": "qualified",
        "qualification": "narrow exact content only",
    }
    with pytest.raises(GovernanceError, match="needs evidence paths"):
        validate_migration_unit_disposition(tmp_path, base, allowed, {"C1"})

    artifact = tmp_path / "campaigns/P1/source-adjudication.md"
    artifact.parent.mkdir(parents=True)
    artifact.write_text("qualified with exact reasons\n", encoding="utf-8")
    base["evidence"] = ["campaigns/P1/source-adjudication.md"]
    validate_migration_unit_disposition(tmp_path, base, allowed, {"C1"})

    refuted = {
        "source_unit": "A2",
        "accepted_claims": [],
        "disposition": "refuted",
        "evidence": ["campaigns/P1/source-adjudication.md"],
    }
    with pytest.raises(GovernanceError, match="must name refutation"):
        validate_migration_unit_disposition(tmp_path, refuted, allowed, {"C1"})
