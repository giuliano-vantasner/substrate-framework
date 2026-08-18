from __future__ import annotations

from substrate_framework.claim_graph import (
    claim_sector,
    rank_intersections,
    synthesis_frontier,
)


def _claim(claim_id: str, dependencies: list[str]) -> dict:
    return {
        "id": claim_id,
        "statement": claim_id,
        "provenance": "tests/test_claim_graph.py",
        "verification": "symbolic_verified",
        "review": "accepted",
        "compatibility": "native",
        "epistemic": "active",
        "dependencies": dependencies,
        "evidence": ["tests/test_claim_graph.py"],
        "assumptions": [],
        "comparators": [],
        "accepted_in": "v-test",
    }


def _registry() -> dict:
    return {
        "schema_version": 1,
        "claims": [
            _claim("C-SG-001", []),
            _claim("C-MOM-001", []),
            _claim("C-GW-001", ["C-SG-001", "C-MOM-001"]),
            _claim("C-GW-002", ["C-GW-001"]),
            _claim("C-VAC-001", []),
        ],
    }


def test_claim_sector_uses_durable_identifier_token() -> None:
    assert claim_sector("C-RGE-002") == "RGE"
    assert claim_sector("unexpected") == "OTHER"


def test_intersection_ranking_is_stable_and_cross_sector() -> None:
    ranked = rank_intersections(_registry())

    assert [item.claim_id for item in ranked] == ["C-GW-001", "C-GW-002"]
    assert ranked[0].sectors == ("GW", "MOM", "SG")
    assert ranked[0].downstream_consumers == 1


def test_frontier_reports_bridges_and_sector_seeds_without_gating() -> None:
    report = synthesis_frontier(_registry(), {"SG", "MOM", "GW"})

    assert report.sectors == ("GW", "MOM", "SG")
    assert [item.claim_id for item in report.existing_bridges] == [
        "C-GW-001",
        "C-GW-002",
    ]
    assert {seed.sector: seed.claim_ids for seed in report.seeds} == {
        "GW": ("C-GW-001", "C-GW-002"),
        "MOM": ("C-MOM-001",),
        "SG": ("C-SG-001",),
    }
