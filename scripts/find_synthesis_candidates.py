#!/usr/bin/env python3
"""Surface advisory cross-sector theorem-synthesis frontiers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from substrate_framework.claim_graph import rank_intersections, synthesis_frontier
from substrate_framework.governance import load_yaml


def _sectors(value: str) -> set[str]:
    return {item.strip().upper() for item in value.split(",") if item.strip()}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Rank accepted claim intersections as theorem-discovery hints. "
            "The output is advisory and never a promotion gate."
        )
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("governance/claims.yaml"),
        help="claim registry path",
    )
    parser.add_argument(
        "--sectors",
        type=_sectors,
        help="comma-separated frontier sectors, for example SG,MOM,GW",
    )
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    registry = load_yaml(args.registry)
    if args.sectors:
        report = synthesis_frontier(
            registry,
            args.sectors,
            bridge_limit=args.limit,
        )
        payload = report.as_dict()
    else:
        payload = {
            "intersections": [
                item.as_dict()
                for item in rank_intersections(registry, limit=args.limit)
            ]
        }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    print("ADVISORY ONLY — candidates still need an exact theorem statement and glue proof.")
    if args.sectors:
        print(f"Requested sectors: {', '.join(payload['sectors'])}")
        for seed in payload["seeds"]:
            claims = ", ".join(seed["claim_ids"]) or "none"
            print(f"  {seed['sector']} seeds: {claims}")
        print("Existing cross-sector bridges:")
        intersections = payload["existing_bridges"]
    else:
        print("Accepted cross-sector intersections:")
        intersections = payload["intersections"]
    for item in intersections:
        print(
            f"  {item['claim_id']}: sectors={','.join(item['sectors'])} "
            f"consumers={item['downstream_consumers']} score={item['score']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
