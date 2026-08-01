#!/usr/bin/env python3
"""Generate accepted claim and release memory from governed registry state."""

from __future__ import annotations

import argparse
from pathlib import Path

from substrate_framework.governance import (
    GovernanceError,
    load_yaml,
    render_claim_memory,
    render_release_memory,
    validate_registry,
    validate_release,
)


def expected_memory(root: Path) -> dict[Path, str]:
    registry = load_yaml(root / "governance" / "claims.yaml")
    validate_registry(registry)
    release_dir = root / "governance" / "releases"
    releases: dict[str, dict] = {}
    for path in sorted(release_dir.glob("*.yaml")):
        if path.name == "current.yaml":
            continue
        data = load_yaml(path)
        validate_release(data, registry, source=str(path.relative_to(root)))
        releases[data["release"]] = data

    output: dict[Path, str] = {}
    for claim in registry["claims"]:
        accepted_in = claim["accepted_in"]
        if accepted_in is None:
            continue
        if accepted_in not in releases:
            raise GovernanceError(
                f"{claim['id']}: accepted_in {accepted_in!r} has no pinned release"
            )
        output[
            root / "memory" / "framework" / "claims" / f"{claim['id']}.md"
        ] = render_claim_memory(claim, releases[accepted_in]["released_at"])

    for release_id, release in releases.items():
        output[
            root / "memory" / "framework" / "releases" / f"{release_id}.md"
        ] = render_release_memory(release, registry)
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    expected = expected_memory(root)
    generated_root = root / "memory" / "framework"
    actual = set(generated_root.rglob("*.md")) if generated_root.exists() else set()

    if args.check:
        if actual != set(expected):
            raise SystemExit("generated accepted memory file set is stale; run scripts/render_memory.py")
        for path, content in expected.items():
            if path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"generated accepted memory is stale: {path.relative_to(root)}")
    else:
        unexpected = actual - set(expected)
        if unexpected:
            names = ", ".join(str(path.relative_to(root)) for path in sorted(unexpected))
            raise SystemExit(f"refusing to overwrite unexpected generated memory: {names}")
        for path, content in expected.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
