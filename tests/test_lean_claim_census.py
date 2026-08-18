"""Machine-check the P232 Lean corpus census against the registry and the artifacts.

The census is the #92 work-item-2 deliverable: every theorem of every ingested file is
classified, every corroborating attachment appears as reviewed lean verification evidence
on the accepted claim, every promotion points at its campaign, and every artifact path
resolves. These checks are consistency checks over governance state; they do not rebuild
the Lean corpus (the gate passed at the ingestion commit and the formal surface is
unchanged by governance-only edits).
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "campaigns/P232-lean-corpus-census/census.yaml"
PROVENANCE = ROOT / "formal/SubstrateFramework/Ingested/provenance.yaml"
ING = ROOT / "formal/SubstrateFramework/Ingested"

DECL = re.compile(r"^(?:private\s+)?(?:theorem|lemma)\s+([A-Za-z_][A-Za-z0-9_.!?]*)", re.MULTILINE)


def _lean_theorems(path: Path) -> set[str]:
    source = re.sub(r"--[^\n]*", "", path.read_text(encoding="utf-8"))
    return {m.group(1).split(".")[-1] for m in DECL.finditer(source)}


def test_census_covers_every_ingested_file_and_theorem() -> None:
    census = yaml.safe_load(CENSUS.read_text(encoding="utf-8"))
    provenance = yaml.safe_load(PROVENANCE.read_text(encoding="utf-8"))
    manifest_files = {record["file"] for record in provenance["files"]}
    census_files = {record["file"] for record in census["files"]}
    assert census_files == manifest_files
    assert census["source_corpus"]["ingested_files"] == len(manifest_files)
    assert census["source_corpus"]["ingested_theorems"] == sum(
        r["theorems"] for r in provenance["files"]
    )
    for record in census["files"]:
        source = ING / record["file"]
        declared = _lean_theorems(source)
        classified: set[str] = set()
        for entry in record["entries"]:
            assert entry["class"] in {
                "corroborates_accepted_claim",
                "new_standalone_exact_fact",
                "composes_accepted_claims",
                "infrastructure_or_disposition",
            }
            if entry["class"] == "infrastructure_or_disposition":
                assert entry["disposition"].strip()
            else:
                assert entry["claim"] and entry["theorems"]
            if entry["class"] == "corroborates_accepted_claim":
                assert entry["scope"].strip()
            if entry["class"] in {"new_standalone_exact_fact", "composes_accepted_claims"}:
                assert entry["campaign"] in {"P233", "P234", "P235"}
                assert entry["entrypoint"].split(".")[-1] in declared
            classified.update(entry["theorems"])
        assert classified == declared, record["file"]


def test_attachments_match_registry_evidence() -> None:
    census = yaml.safe_load(CENSUS.read_text(encoding="utf-8"))
    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text(encoding="utf-8"))
    by_id = {c["id"]: c for c in registry["claims"]}
    attached: dict[str, set[str]] = {}
    for record in census["files"]:
        for entry in record["entries"]:
            if entry["class"] != "corroborates_accepted_claim":
                continue
            claim = by_id[entry["claim"]]
            assert claim["accepted_in"] is not None, entry["claim"]
            artifact = f"formal/SubstrateFramework/Ingested/{record['file']}"
            records = claim.get("verification_evidence", [])
            matching = [r for r in records if r.get("artifact") == artifact]
            assert matching, f"{entry['claim']}: no lean record for {artifact}"
            assert artifact in claim["evidence"], f"{entry['claim']}: {artifact} not in evidence"
            attached.setdefault(entry["claim"], set()).update(
                t for t in entry["theorems"]
            )
    assert len(attached) == 43
    for claim_id in attached:
        assert by_id[claim_id].get("verification_evidence"), claim_id


def test_promotions_match_registry_entries() -> None:
    census = yaml.safe_load(CENSUS.read_text(encoding="utf-8"))
    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text(encoding="utf-8"))
    by_id = {c["id"]: c for c in registry["claims"]}
    promoted: dict[str, str] = {}
    for record in census["files"]:
        for entry in record["entries"]:
            if entry["class"] not in {"new_standalone_exact_fact", "composes_accepted_claims"}:
                continue
            promoted[entry["claim"]] = entry["campaign"]
    assert len(promoted) == 12
    for claim_id, campaign in promoted.items():
        claim = by_id[claim_id]
        assert claim["accepted_in"] == "v0.163.0"
        assert claim["verification"] == "formal_verified"
        assert claim["review"] == "accepted"
        assert claim["epistemic"] == "active"
        suffix = {
            "P233": "P233-lean-discrete-facts",
            "P234": "P234-lean-polarization-split",
            "P235": "P235-lean-radiating-channel",
        }[campaign]
        adjudication = yaml.safe_load(
            (ROOT / f"campaigns/{suffix}/adjudication.yaml").read_text(encoding="utf-8")
        )
        assert claim_id in [c["id"] for c in adjudication["claims"]]
        if entry_class(claim) == "composes_accepted_claims":
            assert claim["category"] == "synthesized"
            assert claim["composition"]["glue"]["method"] == "lean"
            assert (ROOT / claim["composition"]["glue"]["artifact"]).is_file()
        else:
            assert "category" not in claim


def entry_class(claim: dict) -> str:
    census = yaml.safe_load(CENSUS.read_text(encoding="utf-8"))
    for record in census["files"]:
        for entry in record["entries"]:
            if entry.get("claim") == claim["id"] and entry["class"] in {
                "new_standalone_exact_fact",
                "composes_accepted_claims",
            }:
                return entry["class"]
    raise AssertionError(claim["id"])


def test_census_artifacts_resolve() -> None:
    census = yaml.safe_load(CENSUS.read_text(encoding="utf-8"))
    for record in census["files"]:
        assert (ING / record["file"]).is_file()
    adjudication = yaml.safe_load(
        (ROOT / "campaigns/P232-lean-corpus-census/adjudication.yaml").read_text(encoding="utf-8")
    )
    review_dir = ROOT / "campaigns/P232-lean-corpus-census/reviews"
    for attachment in adjudication["attachments"]:
        for rec in attachment["records"]:
            review = ROOT / rec["scope_review"]
            assert review.is_file(), review
        for rec in attachment["records"]:
            assert (ROOT / rec["artifact"]).is_file(), rec["artifact"]
    assert len(list(review_dir.glob("*.md"))) == 43
