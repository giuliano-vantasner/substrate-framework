#!/usr/bin/env python3
"""Independent direct-pathlib reconstruction of the P015 lexical census."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re

import yaml

from substrate_framework.verification import CheckLedger


def direct_matches(
    root: Path, pattern: str, *, exclude_part: str | None = None
) -> tuple[tuple[str, str], ...]:
    regex = re.compile(pattern, re.IGNORECASE)
    records: list[tuple[str, str]] = []
    for path in root.rglob("*.py"):
        relative = path.relative_to(root)
        if exclude_part is not None and exclude_part in relative.parts:
            continue
        payload = path.read_bytes()
        if regex.search(payload.decode("utf-8", errors="replace")):
            records.append((relative.as_posix(), hashlib.sha256(payload).hexdigest()))
    return tuple(sorted(records))


def run(source_root: Path) -> int:
    checks = CheckLedger("P015-INDEPENDENT")
    report = yaml.safe_load(
        (Path(__file__).parents[1] / "evidence/consumer-report.yaml").read_text(
            encoding="utf-8"
        )
    )
    main = report["main_scan"]
    bridge_root = source_root / main["root"]
    action = direct_matches(
        bridge_root, main["token_patterns"]["action"], exclude_part="phase-45"
    )
    energy = direct_matches(
        bridge_root, main["token_patterns"]["energy"], exclude_part="phase-45"
    )
    charge = direct_matches(
        bridge_root, main["token_patterns"]["charge"], exclude_part="phase-45"
    )

    checks.check("direct traversal independently finds zero action matches", action == ())
    checks.check("direct traversal independently finds 36 energy matches", len(energy) == 36)
    checks.check("direct traversal independently finds four charge matches", len(charge) == 4)
    expected_by_group = {
        group: tuple(
            (record["path"], record["sha256"])
            for record in main["matched_files"]
            if group in record["groups"]
        )
        for group in ("energy", "charge")
    }
    checks.check(
        "direct energy paths and hashes equal the durable report",
        energy == expected_by_group["energy"],
    )
    checks.check(
        "direct charge paths and hashes equal the durable report",
        charge == expected_by_group["charge"],
    )

    shadow = report["positive_controls"]["shadow"]
    shadow_action = direct_matches(
        source_root / shadow["root"], main["token_patterns"]["action"]
    )
    checks.check(
        "direct positive-control traversal finds the five expected files",
        tuple(path for path, _ in shadow_action)
        == tuple(record["path"] for record in shadow["action_matches"]),
    )

    total = checks.finish()
    print(f"P015 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
