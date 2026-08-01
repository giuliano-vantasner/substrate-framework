#!/usr/bin/env python3
"""Validate the required skill structure and frontmatter."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


def validate(skill_path: Path) -> None:
    skill_file = skill_path / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md needs YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict) or set(frontmatter) != {"name", "description"}:
        raise ValueError("frontmatter must contain only name and description")
    name = frontmatter["name"]
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("skill name must be hyphen-case")
    if len(name) > 64:
        raise ValueError("skill name exceeds 64 characters")
    description = frontmatter["description"]
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        raise ValueError("skill description must contain 1-1024 characters")
    for relative in (
        "agents/openai.yaml",
        "references/governance.md",
        "references/oracles.md",
        "scripts/preflight.sh",
        "assets/verify_claim.py",
        "assets/verify_pde.py",
    ):
        if not (skill_path / relative).is_file():
            raise ValueError(f"missing skill resource: {relative}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_skill.py <skill-directory>")
    validate(Path(sys.argv[1]))
    print("Skill is valid!")
