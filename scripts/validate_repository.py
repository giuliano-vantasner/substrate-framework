#!/usr/bin/env python3
"""Validate governance state, proposal manifests, releases, and generated docs."""

from __future__ import annotations

from pathlib import Path

from substrate_framework.governance import (
    GovernanceError,
    load_yaml,
    render_claim_index,
    validate_proposal,
    validate_registry,
)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    registry_path = root / "governance" / "claims.yaml"
    registry = load_yaml(registry_path)
    claim_ids = validate_registry(registry)

    proposal_count = 0
    for manifest in sorted((root / "proposals").glob("*/proposal.yaml")):
        validate_proposal(load_yaml(manifest), str(manifest.relative_to(root)))
        proposal_count += 1

    current = load_yaml(root / "governance" / "releases" / "current.yaml")
    if current.get("schema_version") != 1:
        raise GovernanceError("current release must declare schema_version: 1")
    accepted_ids = {
        claim["id"]
        for claim in registry["claims"]
        if claim["accepted_in"] is not None and claim["epistemic"] in {"active", "qualified"}
    }
    release_ids = current.get("accepted_claims")
    if not isinstance(release_ids, list) or not all(isinstance(item, str) for item in release_ids):
        raise GovernanceError("current release accepted_claims must be a list of strings")
    unknown_release_claims = set(release_ids) - accepted_ids
    if unknown_release_claims:
        raise GovernanceError(
            f"current release references non-accepted claims: {sorted(unknown_release_claims)}"
        )
    if set(release_ids) != accepted_ids:
        missing = accepted_ids - set(release_ids)
        raise GovernanceError(
            f"current release does not materialize all current accepted claims: {sorted(missing)}"
        )

    generated = root / "docs" / "generated" / "claim-index.md"
    expected = render_claim_index(registry)
    if generated.read_text(encoding="utf-8") != expected:
        raise GovernanceError("generated claim index is stale; run scripts/render_docs.py")

    print(
        f"WORKFLOW VALID: {len(claim_ids)} claims, {len(accepted_ids)} accepted, "
        f"{proposal_count} proposals"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
