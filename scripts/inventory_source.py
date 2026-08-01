#!/usr/bin/env python3
"""Inventory a pinned predecessor snapshot without granting its claims authority."""

from __future__ import annotations

import argparse
import ast
import hashlib
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


BRIDGE_NAME = re.compile(r"^bridge_([A-Za-z0-9]+)(?:_|$)")
STATUS_WORDS = ("DERIVED", "IMPORTED", "DECLARED", "NEGATIVE", "NUMERICAL")


def classify(relative: Path) -> str:
    """Classify a predecessor artifact by its durable role."""

    parts = relative.parts
    posix = relative.as_posix()
    if parts and parts[0] == "agent-memory":
        return "memory"
    if parts and parts[0] == "engineering":
        return "engineering"
    if "/campaigns/" in f"/{posix}/":
        return "campaign"
    if (
        len(parts) >= 4
        and parts[0] == "merged-framework"
        and parts[1] == "bridges"
        and relative.name.startswith("bridge_")
        and relative.suffix == ".py"
    ):
        return "bridge"
    if "dossiers" in parts and relative.suffix == ".md":
        return "dossier"
    if "sympy" in parts and "rungs" in parts and relative.suffix == ".py":
        return "legacy_rung"
    if relative.suffix == ".lean":
        return "formalization"
    if relative.suffix == ".md":
        return "narrative"
    if relative.suffix in {".py", ".js", ".ts"}:
        return "source"
    return "other"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def python_docstring(path: Path) -> str:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return ""
    return ast.get_docstring(tree, clean=False) or ""


def bridge_label(path: Path) -> str | None:
    match = BRIDGE_NAME.match(path.stem)
    return None if match is None else match.group(1)


def build_inventory(source_root: Path, source_baseline: str) -> dict[str, Any]:
    """Build a hash-locked role and bridge-reference inventory."""

    root = source_root.resolve()
    files = sorted(path for path in root.rglob("*") if path.is_file())
    records: list[dict[str, Any]] = []
    role_counts: Counter[str] = Counter()

    for path in files:
        relative = path.relative_to(root)
        role = classify(relative)
        role_counts[role] += 1
        records.append(
            {
                "path": relative.as_posix(),
                "role": role,
                "sha256": file_sha256(path),
            }
        )

    bridges = [record for record in records if record["role"] == "bridge"]
    known_labels = {
        label
        for record in bridges
        if (label := bridge_label(Path(record["path"]))) is not None
    }
    bridge_records: list[dict[str, Any]] = []
    for record in bridges:
        relative = Path(record["path"])
        path = root / relative
        text = path.read_text(encoding="utf-8")
        docstring = python_docstring(path)
        label = bridge_label(relative)
        referenced = sorted(
            candidate
            for candidate in known_labels
            if candidate != label and re.search(rf"(?<![A-Za-z0-9]){re.escape(candidate)}(?![A-Za-z0-9])", text)
        )
        phase = next((part for part in relative.parts if part.startswith("phase-")), None)
        bridge_records.append(
            {
                "label": label,
                "phase": phase,
                "path": record["path"],
                "sha256": record["sha256"],
                "declared_status_words": [word for word in STATUS_WORDS if word in docstring],
                "candidate_dependencies": referenced,
                "defines_local_check_helper": bool(re.search(r"^def check\s*\(", text, re.MULTILINE)),
                "imports_sympy": bool(re.search(r"(?:import|from)\s+sympy", text)),
                "imports_numpy": bool(re.search(r"(?:import|from)\s+numpy", text)),
                "imports_scipy": bool(re.search(r"(?:import|from)\s+scipy", text)),
            }
        )

    tree_digest = hashlib.sha256()
    for record in records:
        tree_digest.update(record["path"].encode("utf-8"))
        tree_digest.update(b"\0")
        tree_digest.update(record["sha256"].encode("ascii"))
        tree_digest.update(b"\n")

    return {
        "schema_version": 1,
        "source_baseline": source_baseline,
        "source_root_role": "isolated immutable snapshot",
        "authority_warning": (
            "This inventory is a provenance and navigation artifact. Labels, status words, "
            "and candidate dependencies are not accepted claims or authoritative graph edges."
        ),
        "tree_sha256": tree_digest.hexdigest(),
        "file_count": len(records),
        "role_counts": dict(sorted(role_counts.items())),
        "bridge_count": len(bridge_records),
        "bridge_records": bridge_records,
        "files": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-baseline", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    inventory = build_inventory(args.source_root, args.source_baseline)
    rendered = yaml.safe_dump(inventory, sort_keys=False, width=100)
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
