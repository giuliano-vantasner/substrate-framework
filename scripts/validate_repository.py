#!/usr/bin/env python3
"""Validate governance state, proposal manifests, releases, and generated docs."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from substrate_framework.governance import (
    GovernanceError,
    load_yaml,
    render_claim_index,
    validate_proposal,
    validate_registry,
    validate_release,
)


def validate_memory_contract_categories(root: Path) -> None:
    """Ensure every durable template can be instantiated by the memory CLI."""

    config = load_yaml(root / ".agent-memory.yaml")
    categories = config.get("categories")
    if not isinstance(categories, list) or not all(
        isinstance(category, str) and category for category in categories
    ):
        raise GovernanceError(".agent-memory.yaml categories must be a list of strings")

    configured = set(categories)
    used: set[str] = set()
    for template in sorted((root / "memory-templates").glob("*.md")):
        matches = re.findall(r"^category:\s*([A-Za-z0-9_-]+)\s*$", template.read_text(), re.MULTILINE)
        if len(matches) != 1:
            relative = template.relative_to(root)
            raise GovernanceError(f"{relative}: expected exactly one contract category")
        used.add(matches[0])

    missing = used - configured
    if missing:
        raise GovernanceError(
            f"memory templates use unconfigured categories: {sorted(missing)}"
        )


def validate_repository_skills(root: Path) -> int:
    """Validate discoverable repository skills and their UI metadata."""

    count = 0
    for skill_file in sorted((root / ".agents/skills").glob("*/SKILL.md")):
        count += 1
        relative = skill_file.relative_to(root)
        content = skill_file.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            raise GovernanceError(f"{relative}: missing YAML frontmatter")
        frontmatter = yaml.safe_load(match.group(1))
        if not isinstance(frontmatter, dict) or set(frontmatter) != {
            "name",
            "description",
        }:
            raise GovernanceError(
                f"{relative}: frontmatter must contain only name and description"
            )
        name = frontmatter["name"]
        if name != skill_file.parent.name or not re.fullmatch(
            r"[a-z0-9]+(?:-[a-z0-9]+)*", name
        ):
            raise GovernanceError(f"{relative}: skill name must match its directory")
        description = frontmatter["description"]
        if not isinstance(description, str) or not description.strip():
            raise GovernanceError(f"{relative}: description must be non-empty")

        metadata_path = skill_file.parent / "agents/openai.yaml"
        metadata = load_yaml(metadata_path)
        interface = metadata.get("interface")
        if not isinstance(interface, dict):
            raise GovernanceError(
                f"{metadata_path.relative_to(root)}: interface must be a mapping"
            )
        for field in ("display_name", "short_description", "default_prompt"):
            value = interface.get(field)
            if not isinstance(value, str) or not value.strip():
                raise GovernanceError(
                    f"{metadata_path.relative_to(root)}: {field} must be non-empty"
                )
        if not 25 <= len(interface["short_description"]) <= 64:
            raise GovernanceError(
                f"{metadata_path.relative_to(root)}: short_description must be 25-64 characters"
            )
        if f"${name}" not in interface["default_prompt"]:
            raise GovernanceError(
                f"{metadata_path.relative_to(root)}: default_prompt must mention ${name}"
            )
    return count


def validate_accepted_artifact_paths(root: Path, registry: dict) -> None:
    """Require accepted provenance and evidence to resolve inside the repository."""

    for claim in registry["claims"]:
        if claim["accepted_in"] is None:
            continue
        artifacts = [claim["provenance"], *claim["evidence"]]
        composition = claim.get("composition")
        if isinstance(composition, dict) and isinstance(composition.get("glue"), dict):
            artifacts.append(composition["glue"].get("artifact"))
        artifacts.extend(
            record.get("artifact")
            for record in claim.get("verification_evidence", [])
            if isinstance(record, dict)
        )
        for artifact in dict.fromkeys(artifacts):
            if not isinstance(artifact, str) or not artifact:
                raise GovernanceError(f"{claim['id']}: accepted artifact path must be a string")
            relative = Path(artifact)
            if relative.is_absolute() or ".." in relative.parts:
                raise GovernanceError(
                    f"{claim['id']}: accepted artifact must be repository-relative: {artifact}"
                )
            if not (root / relative).is_file():
                raise GovernanceError(
                    f"{claim['id']}: accepted artifact does not exist: {artifact}"
                )


def validate_reserved_claim_identifiers(root: Path, registry: dict) -> None:
    """Prevent accepted claims from reusing an adjudicated rejected identifier."""

    accepted = {
        claim["id"] for claim in registry["claims"] if claim["accepted_in"] is not None
    }
    rejected: dict[str, list[str]] = {}
    for path in sorted((root / "campaigns").glob("*/adjudication.yaml")):
        data = load_yaml(path)
        candidates: list[dict] = []
        for entry in data.get("rejected_claims", []) or []:
            if isinstance(entry, dict):
                candidates.append(entry)
        for entry in data.get("claims", []) or []:
            if isinstance(entry, dict) and (
                entry.get("review") == "rejected"
                or entry.get("epistemic") == "refuted"
            ):
                candidates.append(entry)
        for entry in candidates:
            claim_id = entry.get("id")
            if not isinstance(claim_id, str) or not claim_id:
                raise GovernanceError(
                    f"{path.relative_to(root)}: rejected claim needs a non-empty id"
                )
            rejected.setdefault(claim_id, []).append(str(path.relative_to(root)))

    collisions = sorted(accepted & rejected.keys())
    if collisions:
        details = "; ".join(
            f"{claim_id} reserved by {', '.join(rejected[claim_id])}"
            for claim_id in collisions
        )
        raise GovernanceError(
            "accepted claim identifiers reuse adjudicated rejected provenance: "
            f"{details}"
        )


def validate_migration_unit_disposition(
    root: Path,
    unit: dict,
    allowed: set[str],
    accepted_registry: set[str],
) -> None:
    """Validate one source-unit disposition and its durable support."""

    unit_id = unit.get("source_unit")
    disposition = unit.get("disposition")
    if disposition not in allowed:
        raise GovernanceError(f"{unit_id}: invalid migration disposition {disposition!r}")
    mapped = unit.get("accepted_claims")
    if not isinstance(mapped, list) or not all(isinstance(item, str) for item in mapped):
        raise GovernanceError(f"{unit_id}: accepted_claims must be a list of strings")
    unknown_claims = set(mapped) - accepted_registry
    if unknown_claims:
        raise GovernanceError(
            f"{unit_id}: maps to unknown accepted claims {sorted(unknown_claims)}"
        )
    if disposition == "pending_adjudication" and mapped:
        raise GovernanceError(f"{unit_id}: pending unit cannot map accepted claims")
    if disposition in {"migrated", "partially_migrated"} and not mapped:
        raise GovernanceError(f"{unit_id}: migrated unit must map accepted claims")
    if disposition == "partially_migrated" and not unit.get("remaining_scope"):
        raise GovernanceError(f"{unit_id}: partial migration must name remaining scope")
    if disposition in {"refuted", "out_of_scope"} and mapped:
        raise GovernanceError(
            f"{unit_id}: {disposition} unit cannot map accepted claims; use qualified for mixed scope"
        )

    required_text = {
        "qualified": "qualification",
        "refuted": "refutation",
        "out_of_scope": "scope_basis",
    }
    text_field = required_text.get(disposition)
    if text_field is not None:
        value = unit.get(text_field)
        if not isinstance(value, str) or not value.strip():
            raise GovernanceError(
                f"{unit_id}: {disposition} disposition must name {text_field}"
            )
    if disposition == "duplicate_evidence":
        duplicates = unit.get("duplicates")
        if not isinstance(duplicates, list) or not duplicates or not all(
            isinstance(item, str) and item.strip() for item in duplicates
        ):
            raise GovernanceError(
                f"{unit_id}: duplicate_evidence disposition must name duplicates"
            )

    terminal = {"qualified", "refuted", "duplicate_evidence", "out_of_scope"}
    if disposition in terminal:
        evidence = unit.get("evidence")
        if not isinstance(evidence, list) or not evidence or not all(
            isinstance(item, str) and item.strip() for item in evidence
        ):
            raise GovernanceError(
                f"{unit_id}: {disposition} disposition needs evidence paths"
            )
        for artifact in evidence:
            relative = Path(artifact)
            if relative.is_absolute() or ".." in relative.parts:
                raise GovernanceError(
                    f"{unit_id}: disposition evidence must be repository-relative: {artifact}"
                )
            if not (root / relative).is_file():
                raise GovernanceError(
                    f"{unit_id}: disposition evidence does not exist: {artifact}"
                )


def validate_migration_inventory(root: Path, registry: dict) -> dict[str, int]:
    """Validate the measurable predecessor scope without promoting its units."""

    scope = load_yaml(root / "migration" / "scope.yaml")
    dispositions = load_yaml(root / "migration" / "dispositions.yaml")
    candidates = load_yaml(root / "migration" / "source-claims.yaml")
    source_inventory = load_yaml(root / scope["source_inventory"])

    for data, name in (
        (scope, "scope"),
        (dispositions, "dispositions"),
        (candidates, "source claims"),
    ):
        if data.get("schema_version") != 1:
            raise GovernanceError(f"migration {name} must declare schema_version: 1")

    baseline = source_inventory["source_baseline"]
    tree_sha = source_inventory["tree_sha256"]
    for data, name in (
        (scope, "scope"),
        (dispositions, "dispositions"),
        (candidates, "source claims"),
    ):
        if data.get("source_baseline") != baseline:
            raise GovernanceError(f"migration {name} source baseline disagrees")
    if scope.get("tree_sha256") != tree_sha or candidates.get("tree_sha256") != tree_sha:
        raise GovernanceError("migration inventory tree SHA-256 disagrees with source inventory")

    bridge_records = source_inventory["bridge_records"]
    expected = {
        record["label"]: (record["path"], record["sha256"])
        for record in bridge_records
    }
    units = candidates.get("units")
    if not isinstance(units, list):
        raise GovernanceError("migration source claims units must be a list")
    actual: dict[str, tuple[str, str]] = {}
    allowed = set(dispositions.get("allowed_dispositions", []))
    accepted_registry = {
        claim["id"] for claim in registry["claims"] if claim["accepted_in"] is not None
    }
    counts: dict[str, int] = {}
    for unit in units:
        if not isinstance(unit, dict):
            raise GovernanceError("migration source claim unit must be a mapping")
        unit_id = unit.get("source_unit")
        if not isinstance(unit_id, str) or not unit_id:
            raise GovernanceError("migration source unit needs a non-empty id")
        if unit_id in actual:
            raise GovernanceError(f"duplicate migration source unit: {unit_id}")
        actual[unit_id] = (unit.get("path"), unit.get("sha256"))
        disposition = unit.get("disposition")
        validate_migration_unit_disposition(
            root, unit, allowed, accepted_registry
        )
        counts[disposition] = counts.get(disposition, 0) + 1

    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        changed = sorted(
            unit_id
            for unit_id in set(actual) & set(expected)
            if actual[unit_id] != expected[unit_id]
        )
        raise GovernanceError(
            f"migration candidate queue mismatch: missing={missing}, extra={extra}, changed={changed}"
        )
    expected_count = scope.get("expected_primary_units")
    if len(units) != expected_count or candidates.get("primary_unit_count") != expected_count:
        raise GovernanceError("migration primary-unit count disagrees with scope")
    actual_counts = dict(sorted(counts.items()))
    recorded_counts = candidates.get("disposition_counts")
    if recorded_counts != actual_counts:
        raise GovernanceError(
            "migration disposition summary is stale: "
            f"recorded={recorded_counts}, actual={actual_counts}"
        )
    return dict(sorted(counts.items()))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    validate_memory_contract_categories(root)
    skill_count = validate_repository_skills(root)
    registry_path = root / "governance" / "claims.yaml"
    registry = load_yaml(registry_path)
    claim_ids = validate_registry(registry)
    validate_accepted_artifact_paths(root, registry)
    validate_reserved_claim_identifiers(root, registry)
    migration_counts = validate_migration_inventory(root, registry)

    proposal_count = 0
    for manifest in sorted((root / "proposals").glob("*/proposal.yaml")):
        validate_proposal(load_yaml(manifest), str(manifest.relative_to(root)))
        proposal_count += 1

    release_dir = root / "governance" / "releases"
    pinned_releases: dict[str, dict] = {}
    for release_path in sorted(release_dir.glob("*.yaml")):
        if release_path.name == "current.yaml":
            continue
        relative = str(release_path.relative_to(root))
        release_data = load_yaml(release_path)
        validate_release(release_data, registry, source=relative)
        release_id = release_data["release"]
        if release_id != release_path.stem:
            raise GovernanceError(
                f"{relative}: release id {release_id!r} must match filename stem"
            )
        pinned_releases[release_id] = release_data

    current_path = release_dir / "current.yaml"
    current = load_yaml(current_path)
    release_ids = validate_release(
        current, registry, source="governance/releases/current.yaml", require_current_set=True
    )
    current_id = current["release"]
    if current_id is not None:
        if current_id not in pinned_releases:
            raise GovernanceError(f"current release {current_id!r} has no pinned manifest")
        pinned = pinned_releases[current_id]
        if current != pinned:
            differing = sorted(
                field
                for field in current.keys() | pinned.keys()
                if current.get(field) != pinned.get(field)
            )
            raise GovernanceError(
                f"current release disagrees with pinned {current_id}: {differing}"
            )
    accepted_ids = set(release_ids)

    generated = root / "docs" / "generated" / "claim-index.md"
    expected = render_claim_index(registry)
    if generated.read_text(encoding="utf-8") != expected:
        raise GovernanceError("generated claim index is stale; run scripts/render_docs.py")

    print(
        f"WORKFLOW VALID: {len(claim_ids)} claims, {len(accepted_ids)} accepted, "
        f"{proposal_count} proposals, {skill_count} skills; "
        f"MIGRATION QUEUE: {sum(migration_counts.values())} units, "
        f"{migration_counts.get('pending_adjudication', 0)} pending, "
        f"{migration_counts.get('partially_migrated', 0)} partial"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
