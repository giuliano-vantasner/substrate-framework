"""Machine-check the P232 Lean corpus census against the registry and the artifacts.

The census is the #92 work-item-2 deliverable: every theorem of every ingested file is
classified, every corroborating attachment appears as reviewed Lean verification evidence
on the accepted claim with the exact census scope and theorem set, every promotion points
at its campaign, and every artifact path resolves. These checks are consistency checks over
governance state; the separate Lean gate audits the formal surface.
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
                entrypoint = entry["entrypoint"].split(".")[-1]
                assert entrypoint in entry["theorems"], (record["file"], entry["claim"])
                assert entrypoint in declared
            classified.update(entry["theorems"])
        assert classified == declared, record["file"]


def test_attachments_match_registry_evidence() -> None:
    census = yaml.safe_load(CENSUS.read_text(encoding="utf-8"))
    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text(encoding="utf-8"))
    adjudication = yaml.safe_load(
        (ROOT / "campaigns/P232-lean-corpus-census/adjudication.yaml").read_text(encoding="utf-8")
    )
    by_id = {c["id"]: c for c in registry["claims"]}
    census_records: dict[tuple[str, str], dict] = {}
    for record in census["files"]:
        for entry in record["entries"]:
            if entry["class"] != "corroborates_accepted_claim":
                continue
            claim = by_id[entry["claim"]]
            assert claim["accepted_in"] is not None, entry["claim"]
            artifact = f"formal/SubstrateFramework/Ingested/{record['file']}"
            records = claim.get("verification_evidence", [])
            matching = [r for r in records if r.get("artifact") == artifact]
            assert len(matching) == 1, f"{entry['claim']}: expected one lean record for {artifact}"
            assert matching[0]["method"] == "lean"
            assert matching[0]["scope"] == entry["scope"]
            assert artifact in claim["evidence"], f"{entry['claim']}: {artifact} not in evidence"
            key = (entry["claim"], artifact)
            assert key not in census_records
            census_records[key] = entry

    adjudicated_records: dict[tuple[str, str], set[str]] = {}
    for attachment in adjudication["attachments"]:
        assert attachment["decision"] == "accepted"
        for record in attachment["records"]:
            key = (attachment["claim"], record["artifact"])
            assert key not in adjudicated_records
            adjudicated_records[key] = set(record["entrypoints"])

    assert len(census_records) == 55
    assert len({claim for claim, _ in census_records}) == 39
    assert set(adjudicated_records) == set(census_records)
    for key, entrypoints in adjudicated_records.items():
        assert entrypoints == set(census_records[key]["theorems"]), key

    registry_records = {
        (claim["id"], record["artifact"])
        for claim in registry["claims"]
        for record in claim.get("verification_evidence", [])
        if record.get("method") == "lean"
        and record.get("artifact", "").startswith("formal/SubstrateFramework/Ingested/")
    }
    assert registry_records == set(census_records)


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
    assert len(promoted) == 10
    for claim_id, campaign in promoted.items():
        claim = by_id[claim_id]
        assert claim["accepted_in"] == "v0.163.0"
        assert claim["verification"] == "formal_verified"
        assert claim["review"] == "accepted"
        assert claim["epistemic"] == "active"
        assert campaign == "P233"
        suffix = "P233-lean-discrete-facts"
        adjudication = yaml.safe_load(
            (ROOT / f"campaigns/{suffix}/adjudication.yaml").read_text(encoding="utf-8")
        )
        assert claim_id in [c["id"] for c in adjudication["claims"]]
        assert entry_class(claim) == "new_standalone_exact_fact"
        assert "category" not in claim


def test_rejected_lookup_syntheses_stay_out_of_registry() -> None:
    census = yaml.safe_load(CENSUS.read_text(encoding="utf-8"))
    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text(encoding="utf-8"))
    registry_ids = {claim["id"] for claim in registry["claims"]}
    assert {"C-GW-013", "C-GW-014"}.isdisjoint(registry_ids)
    for suffix, claim_id in {
        "P234-lean-polarization-split": "C-GW-013",
        "P235-lean-radiating-channel": "C-GW-014",
    }.items():
        adjudication = yaml.safe_load(
            (ROOT / f"campaigns/{suffix}/adjudication.yaml").read_text(encoding="utf-8")
        )
        decision = next(c for c in adjudication["claims"] if c["id"] == claim_id)
        assert decision["review"] == "rejected"
        assert decision["epistemic"] == "refuted"
    assert all(
        entry["class"] != "composes_accepted_claims"
        for record in census["files"]
        for entry in record["entries"]
    )


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
    assert len(list(review_dir.glob("*.md"))) == 39
