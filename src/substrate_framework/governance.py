"""Validation and rendering for the scientific claim graph.

The functions here are deliberately importable. Campaign scripts should consume
canonical definitions from the package instead of copying constants or helpers.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

import yaml


class GovernanceError(ValueError):
    """Raised when a registry or proposal violates framework governance."""


REQUIRED_CLAIM_FIELDS = {
    "id",
    "statement",
    "provenance",
    "verification",
    "review",
    "compatibility",
    "epistemic",
    "dependencies",
    "evidence",
    "assumptions",
    "comparators",
    "accepted_in",
}

REQUIRED_PROPOSAL_FIELDS = {
    "id",
    "base_release",
    "source_baseline",
    "question",
    "invariants",
    "allowed_imports",
    "candidates",
    "selection_criteria",
    "claims_proposed",
    "comparators_blinded_until",
    "status",
}

REQUIRED_RELEASE_FIELDS = {
    "schema_version",
    "release",
    "source_baseline",
    "released_at",
    "accepted_claims",
}


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML mapping from *path*."""

    source = Path(path)
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise GovernanceError(f"{source}: top level must be a mapping")
    return data


def _as_string_list(value: Any, field: str, owner: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise GovernanceError(f"{owner}: {field} must be a list of strings")
    return value


def _detect_dependency_cycles(graph: dict[str, list[str]]) -> None:
    active: set[str] = set()
    complete: set[str] = set()

    def visit(node: str, trail: tuple[str, ...]) -> None:
        if node in active:
            cycle = " -> ".join((*trail, node))
            raise GovernanceError(f"claim dependency cycle: {cycle}")
        if node in complete:
            return
        active.add(node)
        for dependency in graph[node]:
            visit(dependency, (*trail, node))
        active.remove(node)
        complete.add(node)

    for claim_id in graph:
        visit(claim_id, ())


def validate_registry(data: dict[str, Any]) -> list[str]:
    """Validate claim identity, status axes, dependency closure, and promotion gates."""

    if data.get("schema_version") != 1:
        raise GovernanceError("claims registry must declare schema_version: 1")
    claims = data.get("claims")
    if not isinstance(claims, list):
        raise GovernanceError("claims must be a list")

    by_id: dict[str, dict[str, Any]] = {}
    for index, claim in enumerate(claims):
        owner = f"claims[{index}]"
        if not isinstance(claim, dict):
            raise GovernanceError(f"{owner} must be a mapping")
        missing = REQUIRED_CLAIM_FIELDS - claim.keys()
        if missing:
            raise GovernanceError(f"{owner} missing fields: {sorted(missing)}")
        claim_id = claim["id"]
        if not isinstance(claim_id, str) or not claim_id:
            raise GovernanceError(f"{owner}.id must be a non-empty string")
        if claim_id in by_id:
            raise GovernanceError(f"duplicate claim id: {claim_id}")
        by_id[claim_id] = claim

    graph: dict[str, list[str]] = {}
    allowed_review = {"unaudited", "audited", "accepted", "rejected"}
    allowed_compatibility = {"unassessed", "native", "compatible_extension", "conflict"}
    allowed_epistemic = {"proposed", "active", "qualified", "superseded", "refuted"}
    allowed_verification = {
        "unverified",
        "symbolic_verified",
        "formal_verified",
        "numeric_evidence",
        "simulation_evidence",
    }

    superseding_targets: set[str] = set()
    for claim_id, claim in by_id.items():
        dependencies = _as_string_list(claim["dependencies"], "dependencies", claim_id)
        _as_string_list(claim["evidence"], "evidence", claim_id)
        _as_string_list(claim["assumptions"], "assumptions", claim_id)
        _as_string_list(claim["comparators"], "comparators", claim_id)
        graph[claim_id] = dependencies
        unknown = set(dependencies) - by_id.keys()
        if unknown:
            raise GovernanceError(f"{claim_id}: unknown dependencies {sorted(unknown)}")
        if claim["review"] not in allowed_review:
            raise GovernanceError(f"{claim_id}: invalid review status {claim['review']!r}")
        if claim["compatibility"] not in allowed_compatibility:
            raise GovernanceError(
                f"{claim_id}: invalid compatibility status {claim['compatibility']!r}"
            )
        if claim["epistemic"] not in allowed_epistemic:
            raise GovernanceError(f"{claim_id}: invalid epistemic status {claim['epistemic']!r}")
        if claim["verification"] not in allowed_verification:
            raise GovernanceError(
                f"{claim_id}: invalid verification status {claim['verification']!r}"
            )

        accepted_in = claim["accepted_in"]
        was_accepted = accepted_in is not None
        is_current = was_accepted and claim["epistemic"] in {"active", "qualified"}
        if was_accepted:
            if not isinstance(accepted_in, str) or not accepted_in:
                raise GovernanceError(f"{claim_id}: accepted_in must be null or a release id")
            if claim["review"] != "accepted":
                raise GovernanceError(f"{claim_id}: accepted claim must have review: accepted")
            if claim["verification"] == "unverified":
                raise GovernanceError(f"{claim_id}: accepted claim must have verifier evidence")
            if not claim["evidence"]:
                raise GovernanceError(f"{claim_id}: accepted claim must cite evidence")
        if is_current:
            if claim["compatibility"] not in {"native", "compatible_extension"}:
                raise GovernanceError(f"{claim_id}: current accepted claim must fit the framework")
            for dependency in dependencies:
                dependency_claim = by_id[dependency]
                if dependency_claim["accepted_in"] is None or dependency_claim["epistemic"] not in {
                    "active",
                    "qualified",
                }:
                    raise GovernanceError(
                        f"{claim_id}: current claim depends on noncurrent {dependency}"
                    )

        challenges = _as_string_list(claim.get("challenges", []), "challenges", claim_id)
        supersedes = _as_string_list(claim.get("supersedes", []), "supersedes", claim_id)
        unknown_relationships = (set(challenges) | set(supersedes)) - by_id.keys()
        if unknown_relationships:
            raise GovernanceError(
                f"{claim_id}: unknown relationship targets {sorted(unknown_relationships)}"
            )
        if supersedes:
            if not is_current or claim["review"] != "accepted":
                raise GovernanceError(
                    f"{claim_id}: only current accepted claims may supersede; proposals use challenges"
                )
            superseding_targets.update(supersedes)

    _detect_dependency_cycles(graph)
    for target in superseding_targets:
        if by_id[target]["epistemic"] != "superseded":
            raise GovernanceError(
                f"{target}: target of supersedes must have epistemic: superseded"
            )
    return sorted(by_id)


def validate_proposal(data: dict[str, Any], source: str = "proposal") -> None:
    """Validate the pre-registered inputs required before a campaign begins."""

    missing = REQUIRED_PROPOSAL_FIELDS - data.keys()
    if missing:
        raise GovernanceError(f"{source} missing fields: {sorted(missing)}")
    if data["status"] not in {"draft", "active", "in_review", "accepted", "rejected", "rework"}:
        raise GovernanceError(f"{source}: invalid status {data['status']!r}")
    if not isinstance(data["source_baseline"], str) or not data["source_baseline"].strip():
        raise GovernanceError(f"{source}: source_baseline must name an immutable source revision")
    for field in ("invariants", "allowed_imports", "selection_criteria", "claims_proposed"):
        _as_string_list(data[field], field, source)
    candidates = data["candidates"]
    uniqueness = data.get("uniqueness_evidence")
    if not isinstance(candidates, list) or not candidates:
        raise GovernanceError(f"{source}: register at least one candidate approach")
    if len(candidates) < 2 and not (isinstance(uniqueness, str) and uniqueness.strip()):
        raise GovernanceError(
            f"{source}: register at least two candidates or cite uniqueness_evidence"
        )
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict) or not {"id", "description"} <= candidate.keys():
            raise GovernanceError(
                f"{source}: candidates[{index}] needs id and description"
            )


def validate_release(
    data: dict[str, Any],
    registry: dict[str, Any],
    *,
    source: str = "release",
    require_current_set: bool = False,
) -> list[str]:
    """Validate a pinned release claim set and its dependency closure."""

    missing = REQUIRED_RELEASE_FIELDS - data.keys()
    if missing:
        raise GovernanceError(f"{source} missing fields: {sorted(missing)}")
    if data["schema_version"] != 1:
        raise GovernanceError(f"{source}: schema_version must be 1")

    release_id = data["release"]
    source_baseline = data["source_baseline"]
    released_at = data["released_at"]
    release_ids = _as_string_list(data["accepted_claims"], "accepted_claims", source)
    if len(release_ids) != len(set(release_ids)):
        raise GovernanceError(f"{source}: accepted_claims must not contain duplicates")

    validate_registry(registry)
    by_id = {claim["id"]: claim for claim in registry["claims"]}
    if release_id is None:
        if source_baseline is not None or released_at is not None or release_ids:
            raise GovernanceError(f"{source}: null release must have null source and no claims")
        return []
    if not isinstance(release_id, str) or not release_id:
        raise GovernanceError(f"{source}: release must be null or a non-empty id")
    if not isinstance(source_baseline, str) or not source_baseline.strip():
        raise GovernanceError(f"{source}: accepted release must pin source_baseline")
    if not isinstance(released_at, str) or not released_at.strip():
        raise GovernanceError(f"{source}: accepted release must record released_at")

    unknown = set(release_ids) - by_id.keys()
    if unknown:
        raise GovernanceError(f"{source}: unknown claims {sorted(unknown)}")
    release_set = set(release_ids)
    for claim_id in release_ids:
        claim = by_id[claim_id]
        if claim["accepted_in"] is None or claim["review"] != "accepted":
            raise GovernanceError(f"{source}: {claim_id} is not an accepted claim")
        missing_dependencies = set(claim["dependencies"]) - release_set
        if missing_dependencies:
            raise GovernanceError(
                f"{source}: {claim_id} has dependencies outside release: "
                f"{sorted(missing_dependencies)}"
            )

    if require_current_set:
        current_ids = {
            claim_id
            for claim_id, claim in by_id.items()
            if claim["accepted_in"] is not None
            and claim["epistemic"] in {"active", "qualified"}
        }
        if release_set != current_ids:
            missing_current = current_ids - release_set
            historical_only = release_set - current_ids
            raise GovernanceError(
                f"{source}: current set mismatch; missing {sorted(missing_current)}, "
                f"noncurrent {sorted(historical_only)}"
            )
    return release_ids


def render_claim_memory(claim: dict[str, Any], released_at: str) -> str:
    """Render a deterministic accepted-claim memory entry from registry state."""

    status = "active" if claim["epistemic"] in {"active", "qualified"} else "archived"
    frontmatter = {
        "description": f"Accepted framework claim {claim['id']}",
        "author": "framework-registry",
        "created": released_at,
        "updated": released_at,
        "tags": ["substrate-framework", "accepted-claim", claim["id"]],
        "category": "claims",
        "confidence": "established",
        "status": status,
    }
    header = yaml.safe_dump(frontmatter, sort_keys=False).strip()
    dependencies = ", ".join(claim["dependencies"]) or "none"
    assumptions = ", ".join(claim["assumptions"]) or "none"
    comparators = ", ".join(claim["comparators"]) or "none"
    evidence = "\n".join(f"- `{item}`" for item in claim["evidence"])
    return (
        f"---\n{header}\n---\n"
        f"# {claim['id']}\n\n"
        "## Statement\n"
        "The accepted statement is reproduced exactly from the claim registry.\n\n"
        f"{claim['statement']}\n\n"
        "## Status Axes\n"
        "The four governance axes remain independent.\n\n"
        f"Verification is `{claim['verification']}`; review is `{claim['review']}`; "
        f"compatibility is `{claim['compatibility']}`; epistemic status is "
        f"`{claim['epistemic']}`.\n\n"
        "## Dependency and Import Closure\n"
        "The registry records the accepted closure and declared non-claim inputs.\n\n"
        f"Dependencies: {dependencies}. Assumptions: {assumptions}. "
        f"Comparators: {comparators}.\n\n"
        "## Provenance and Evidence\n"
        "The accepted release and immutable campaign evidence are the authoritative pointers.\n\n"
        f"Accepted in `{claim['accepted_in']}` with provenance `{claim['provenance']}`.\n\n"
        f"{evidence}\n"
    )


def render_release_memory(
    release: dict[str, Any], registry: dict[str, Any]
) -> str:
    """Render a deterministic accepted-release memory entry."""

    by_id = {claim["id"]: claim for claim in registry["claims"]}
    release_id = release["release"]
    released_at = release["released_at"]
    frontmatter = {
        "description": f"Accepted framework release {release_id}",
        "author": "framework-registry",
        "created": released_at,
        "updated": released_at,
        "tags": ["substrate-framework", "accepted-release", release_id],
        "category": "releases",
        "confidence": "established",
        "status": "active",
    }
    header = yaml.safe_dump(frontmatter, sort_keys=False).strip()
    claim_lines = "\n".join(
        f"- `{claim_id}` — {by_id[claim_id]['statement']}"
        for claim_id in release["accepted_claims"]
    )
    return (
        f"---\n{header}\n---\n"
        f"# Release {release_id}\n\n"
        "## Source Boundary\n"
        "This release pins its predecessor evidence boundary and acceptance time.\n\n"
        f"Source baseline: `{release['source_baseline']}`. Released at: `{released_at}`.\n\n"
        "## Accepted Claim Set\n"
        "The release materializes this dependency-closed claim set.\n\n"
        f"{claim_lines}\n"
    )


def accepted_claims(data: dict[str, Any]) -> Iterable[dict[str, Any]]:
    """Yield accepted claims in stable identifier order."""

    validate_registry(data)
    claims = (
        claim
        for claim in data["claims"]
        if claim["accepted_in"] is not None and claim["epistemic"] in {"active", "qualified"}
    )
    return sorted(claims, key=lambda claim: claim["id"])


def render_claim_index(data: dict[str, Any]) -> str:
    """Render canonical documentation solely from accepted registry state."""

    lines = [
        "<!-- GENERATED: scripts/render_docs.py; DO NOT EDIT -->",
        "# Accepted claim index",
        "",
        "This document is generated from `governance/claims.yaml`.",
        "",
    ]
    claims = list(accepted_claims(data))
    if not claims:
        lines.append("No scientific claims have been accepted into this repository yet.")
    for claim in claims:
        lines.extend(
            [
                f"## {claim['id']}",
                "",
                str(claim["statement"]),
                "",
                f"- Accepted in: `{claim['accepted_in']}`",
                f"- Verification: `{claim['verification']}`",
                f"- Compatibility: `{claim['compatibility']}`",
                f"- Dependencies: {', '.join(claim['dependencies']) or 'none'}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
