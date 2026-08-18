"""Advisory graph analysis for finding theorem-synthesis frontiers.

The graph ranks accepted claim intersections. It does not propose a scientific
statement, prove glue, or decide promotion.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any

from substrate_framework.governance import validate_registry


_CLAIM_SECTOR = re.compile(r"^C-([A-Z0-9]+)-")


@dataclass(frozen=True)
class Intersection:
    """One accepted claim whose dependency closure crosses sector boundaries."""

    claim_id: str
    sectors: tuple[str, ...]
    direct_dependencies: tuple[str, ...]
    downstream_consumers: int
    score: int

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SectorSeed:
    """Central accepted claims in one requested sector."""

    sector: str
    claim_ids: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Frontier:
    """Advisory coverage report for a requested set of sectors."""

    sectors: tuple[str, ...]
    existing_bridges: tuple[Intersection, ...]
    seeds: tuple[SectorSeed, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "sectors": list(self.sectors),
            "existing_bridges": [bridge.as_dict() for bridge in self.existing_bridges],
            "seeds": [seed.as_dict() for seed in self.seeds],
        }


def claim_sector(claim_id: str) -> str:
    """Return the durable sector token embedded in a claim identifier."""

    match = _CLAIM_SECTOR.match(claim_id)
    return match.group(1) if match else "OTHER"


def _accepted_graph(
    registry: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, tuple[str, ...]]]:
    validate_registry(registry)
    claims = {
        claim["id"]: claim
        for claim in registry["claims"]
        if claim["accepted_in"] is not None
        and claim["epistemic"] in {"active", "qualified"}
    }
    graph = {
        claim_id: tuple(
            dependency for dependency in claim["dependencies"] if dependency in claims
        )
        for claim_id, claim in claims.items()
    }
    return claims, graph


def _dependency_closure(
    claim_id: str, graph: dict[str, tuple[str, ...]]
) -> frozenset[str]:
    discovered: set[str] = set()
    frontier = list(graph[claim_id])
    while frontier:
        dependency = frontier.pop()
        if dependency in discovered:
            continue
        discovered.add(dependency)
        frontier.extend(graph[dependency])
    return frozenset(discovered)


def _consumer_counts(graph: dict[str, tuple[str, ...]]) -> dict[str, int]:
    counts = {claim_id: 0 for claim_id in graph}
    for consumer in graph:
        for dependency in _dependency_closure(consumer, graph):
            counts[dependency] += 1
    return counts


def rank_intersections(
    registry: dict[str, Any],
    *,
    sectors: set[str] | None = None,
    limit: int = 20,
) -> list[Intersection]:
    """Rank existing accepted cross-sector intersections deterministically."""

    if limit < 1:
        raise ValueError("limit must be positive")
    _, graph = _accepted_graph(registry)
    consumers = _consumer_counts(graph)
    requested = {sector.upper() for sector in sectors} if sectors else None
    ranked: list[Intersection] = []
    for claim_id, dependencies in graph.items():
        closure = _dependency_closure(claim_id, graph)
        closure_sectors = {claim_sector(item) for item in {*closure, claim_id}}
        visible_sectors = closure_sectors & requested if requested else closure_sectors
        if len(visible_sectors) < 2:
            continue
        direct_sectors = {claim_sector(item) for item in dependencies}
        score = (
            100 * len(visible_sectors)
            + 10 * len(direct_sectors)
            + consumers[claim_id]
        )
        ranked.append(
            Intersection(
                claim_id=claim_id,
                sectors=tuple(sorted(visible_sectors)),
                direct_dependencies=dependencies,
                downstream_consumers=consumers[claim_id],
                score=score,
            )
        )
    return sorted(
        ranked,
        key=lambda item: (
            -len(item.sectors),
            -item.score,
            -item.downstream_consumers,
            item.claim_id,
        ),
    )[:limit]


def synthesis_frontier(
    registry: dict[str, Any],
    sectors: set[str],
    *,
    seeds_per_sector: int = 3,
    bridge_limit: int = 10,
) -> Frontier:
    """Return existing bridges and central accepted seeds for requested sectors."""

    normalized = {sector.upper() for sector in sectors if sector.strip()}
    if len(normalized) < 2:
        raise ValueError("frontier analysis needs at least two sectors")
    _, graph = _accepted_graph(registry)
    consumers = _consumer_counts(graph)
    sector_seeds: list[SectorSeed] = []
    for sector in sorted(normalized):
        candidates = [
            claim_id for claim_id in graph if claim_sector(claim_id) == sector
        ]
        candidates.sort(
            key=lambda claim_id: (
                -consumers[claim_id],
                -len(_dependency_closure(claim_id, graph)),
                claim_id,
            )
        )
        sector_seeds.append(
            SectorSeed(sector=sector, claim_ids=tuple(candidates[:seeds_per_sector]))
        )
    return Frontier(
        sectors=tuple(sorted(normalized)),
        existing_bridges=tuple(
            rank_intersections(
                registry,
                sectors=normalized,
                limit=bridge_limit,
            )
        ),
        seeds=tuple(sector_seeds),
    )
