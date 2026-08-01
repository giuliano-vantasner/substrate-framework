#!/usr/bin/env python3
"""Generate a review queue from the pinned predecessor bridge corpus.

The output is deliberately a candidate-unit inventory, not a claim registry.
One bridge can contain several claims, imports, or negative attempts; promotion
still requires claim-level decomposition and review.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


SECTION_MARKERS = (
    "QUESTION",
    "RESULT",
    "PROVENANCE",
    "RUN",
    "IMPORTS",
    "DERIVED",
    "DECLARED",
    "CEILING",
    "HONEST",
)


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def _collapse(lines: list[str], limit: int = 700) -> str:
    text = re.sub(r"\s+", " ", " ".join(line.strip() for line in lines)).strip()
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def _section_excerpt(docstring: str, marker: str) -> str | None:
    lines = docstring.splitlines()
    start: int | None = None
    inline: list[str] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == marker or stripped.startswith(f"{marker} ("):
            start = index + 1
            break
        if stripped.startswith(f"{marker}:"):
            inline.append(stripped.split(":", 1)[1])
            start = index + 1
            break
    if start is None:
        return None

    collected = inline
    for line in lines[start:]:
        stripped = line.strip()
        if any(
            stripped == candidate
            or stripped.startswith(f"{candidate} (")
            or stripped.startswith(f"{candidate}:")
            for candidate in SECTION_MARKERS
            if candidate != marker
        ):
            break
        if stripped:
            collected.append(stripped)
        if len(collected) >= 10:
            break
    return _collapse(collected) or None


def _headline(docstring: str, fallback: str) -> str:
    for line in docstring.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped[:500]
    return fallback


def _static_checks(tree: ast.AST) -> tuple[int, int, int]:
    total = 0
    literal = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        name = function.id if isinstance(function, ast.Name) else None
        if name != "check":
            continue
        total += 1
        if node.args and isinstance(node.args[0], ast.Constant) and isinstance(
            node.args[0].value, str
        ):
            literal += 1
    return total, literal, total - literal


def extract_candidate(
    source_root: Path,
    source_record: dict[str, Any],
    disposition: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Extract navigation metadata for one hash-pinned bridge."""

    relative = Path(source_record["path"])
    path = source_root / relative
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != source_record["sha256"]:
        raise ValueError(f"{relative}: SHA-256 differs from the pinned source inventory")
    text = payload.decode("utf-8")
    tree = ast.parse(text)
    docstring = ast.get_docstring(tree, clean=False) or ""
    static_total, literal_total, dynamic_total = _static_checks(tree)

    oracle_hints: list[str] = []
    if source_record["imports_sympy"]:
        oracle_hints.append("symbolic")
    if source_record["imports_numpy"] or source_record["imports_scipy"]:
        oracle_hints.append("numeric")

    override = disposition or {}
    status = override.get("disposition", "pending_adjudication")
    record: dict[str, Any] = {
        "source_unit": source_record["label"],
        "phase": source_record["phase"],
        "path": source_record["path"],
        "sha256": digest,
        "headline": _headline(docstring, relative.stem),
        "question_excerpt": _section_excerpt(docstring, "QUESTION"),
        "result_excerpt": _section_excerpt(docstring, "RESULT"),
        "declared_status_words": source_record["declared_status_words"],
        "candidate_dependencies": source_record["candidate_dependencies"],
        "oracle_hints": oracle_hints,
        "static_check_calls": static_total,
        "literal_check_calls": literal_total,
        "dynamic_check_calls": dynamic_total,
        "assert_statements": sum(isinstance(node, ast.Assert) for node in ast.walk(tree)),
        "terminal_tally_literal_present": bool(
            re.search(r"ALL[^\n]{0,80}CHECKS PASS", text)
        ),
        "disposition": status,
        "accepted_claims": override.get("accepted_claims", []),
    }
    if "remaining_scope" in override:
        record["remaining_scope"] = override["remaining_scope"]
    if "note" in override:
        record["note"] = override["note"]
    return record


def build_claim_inventory(
    source_root: Path,
    source_inventory: dict[str, Any],
    scope: dict[str, Any],
    dispositions: dict[str, Any],
) -> dict[str, Any]:
    """Build the bridge-level candidate queue and its measurable summary."""

    baseline = source_inventory["source_baseline"]
    tree_sha = source_inventory["tree_sha256"]
    if scope.get("source_baseline") != baseline or scope.get("tree_sha256") != tree_sha:
        raise ValueError("scope does not match the pinned source inventory")
    if dispositions.get("source_baseline") != baseline:
        raise ValueError("dispositions do not match the pinned source baseline")

    overrides = dispositions.get("units", {})
    if not isinstance(overrides, dict):
        raise ValueError("dispositions.units must be a mapping")
    labels = {record["label"] for record in source_inventory["bridge_records"]}
    unknown = set(overrides) - labels
    if unknown:
        raise ValueError(f"dispositions name unknown source units: {sorted(unknown)}")

    records = [
        extract_candidate(source_root, record, overrides.get(record["label"]))
        for record in source_inventory["bridge_records"]
    ]
    records.sort(key=lambda item: (int(item["phase"].split("-")[1]), item["source_unit"]))
    disposition_counts = Counter(record["disposition"] for record in records)
    phase_counts = Counter(record["phase"] for record in records)

    return {
        "schema_version": 1,
        "source_baseline": baseline,
        "tree_sha256": tree_sha,
        "scope_policy": "migration/scope.yaml",
        "authority_warning": (
            "These are source candidate units and navigation hints, not accepted claims. "
            "Each unit still requires exact claim decomposition, dependency audit, and review."
        ),
        "primary_unit_role": scope["primary_unit_role"],
        "primary_unit_count": len(records),
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "phase_counts": dict(
            sorted(phase_counts.items(), key=lambda item: int(item[0].split("-")[1]))
        ),
        "units": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-inventory", type=Path, required=True)
    parser.add_argument("--scope", type=Path, required=True)
    parser.add_argument("--dispositions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    inventory = build_claim_inventory(
        args.source_root.resolve(),
        _load_yaml(args.source_inventory),
        _load_yaml(args.scope),
        _load_yaml(args.dispositions),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(inventory, sort_keys=False, width=100),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
