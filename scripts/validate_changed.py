#!/usr/bin/env python3
"""Select the smallest safe repository-validation mode for a pull request."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]

FULL_EXACT_PATHS = {
    ".agent-memory.yaml",
    "pyproject.toml",
    "tests/conftest.py",
    "src/substrate_framework/exact_symbolic.py",
    "src/substrate_framework/numerics.py",
    "src/substrate_framework/verification.py",
    "tools/agent-memory/pyproject.toml",
}
FULL_PREFIXES = (
    "governance/",
    "migration/",
    "tools/agent-memory/src/",
)
PROCESS_POLICY_PATHS = {
    "AGENTS.md",
    "AGENTS_START_HERE.md",
    "CONTRIBUTING.md",
    ".github/pull_request_template.md",
}
VALIDATION_DRIVER_PATHS = {
    ".github/workflows/validate.yml",
    "scripts/validate.sh",
    "scripts/validate_changed.py",
}


@dataclass(frozen=True)
class Change:
    status: str
    path: str


@dataclass(frozen=True)
class ValidationDecision:
    mode: str
    selectors: tuple[str, ...]
    reasons: tuple[str, ...]


def parse_name_status(output: str) -> list[Change]:
    """Parse ``git diff --name-status`` output, using the destination path."""

    changes: list[Change] = []
    for line in output.splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        raw_status = fields[0]
        status = raw_status[:1]
        path = fields[-1] if status in {"R", "C"} else fields[1]
        changes.append(Change(status=status, path=path))
    return changes


def _has_removed_content(diff: str) -> bool:
    return any(
        line.startswith("-") and not line.startswith("---")
        for line in diff.splitlines()
    )


def _existing_selector(path: str, repo_root: Path) -> str | None:
    return path if (repo_root / path.split("::", 1)[0]).is_file() else None


def choose_validation_scope(
    changes: list[Change],
    *,
    repo_root: Path = ROOT,
    package_init_diff: str = "",
) -> ValidationDecision:
    """Return a conservative full, scoped, or fixed-only validation decision."""

    paths = {change.path for change in changes}
    full_reasons: list[str] = []
    selectors: set[str] = set()

    for path in sorted(paths):
        if path in FULL_EXACT_PATHS or path.startswith(FULL_PREFIXES):
            full_reasons.append(f"cross-cutting path changed: {path}")

    package_changes = [
        change
        for change in changes
        if change.path.startswith("src/substrate_framework/")
        and change.path.endswith(".py")
        and change.path != "src/substrate_framework/__init__.py"
    ]
    added_modules = [change for change in package_changes if change.status == "A"]
    changed_existing_modules = [
        change for change in package_changes if change.status != "A"
    ]
    if changed_existing_modules:
        names = ", ".join(sorted(change.path for change in changed_existing_modules))
        full_reasons.append(f"existing framework module changed: {names}")
    if len(added_modules) > 1:
        full_reasons.append("multiple framework modules added; sector boundary is uncertain")
    for change in added_modules:
        stem = Path(change.path).stem
        expected = f"tests/test_{stem}.py"
        selector = _existing_selector(expected, repo_root)
        if selector is None:
            full_reasons.append(f"new framework module has no matching test file: {change.path}")
        else:
            selectors.add(selector)

    package_init_changed = "src/substrate_framework/__init__.py" in paths
    if package_init_changed and _has_removed_content(package_init_diff):
        full_reasons.append("package public surface removes or changes existing content")
    elif package_init_changed and not added_modules:
        full_reasons.append(
            "package public surface changed without one tested new framework module"
        )

    removed_or_renamed_tests = [
        change
        for change in changes
        if (
            change.path.startswith("tests/")
            or change.path.startswith("tools/agent-memory/tests/")
        )
        and change.path.endswith(".py")
        and change.status in {"D", "R"}
    ]
    if removed_or_renamed_tests:
        full_reasons.append("test coverage was removed or renamed")

    unknown_scripts = {
        path
        for path in paths
        if path.startswith("scripts/")
        and path.endswith((".py", ".sh"))
        and path not in VALIDATION_DRIVER_PATHS
    }
    if unknown_scripts:
        full_reasons.append(
            "validation impact is uncertain for executable scripts: "
            + ", ".join(sorted(unknown_scripts))
        )

    if full_reasons:
        return ValidationDecision("full", (), tuple(full_reasons))

    for path in sorted(paths):
        if (
            path.startswith("tests/")
            or path.startswith("tools/agent-memory/tests/")
        ) and path.endswith(".py"):
            selector = _existing_selector(path, repo_root)
            if selector is not None:
                selectors.add(selector)

    policy_changed = bool(paths & PROCESS_POLICY_PATHS) or any(
        path.startswith(".agents/skills/")
        or path.startswith("memory-templates/")
        for path in paths
    )
    if policy_changed:
        for path in (
            "tests/test_public_contribution_surfaces.py",
            "tests/test_repository_validation.py",
        ):
            selector = _existing_selector(path, repo_root)
            if selector is not None:
                selectors.add(selector)

    if paths & VALIDATION_DRIVER_PATHS:
        for path in (
            "tests/test_validate_script.py",
            "tests/test_validate_changed.py",
            "tests/test_public_contribution_surfaces.py",
        ):
            selector = _existing_selector(path, repo_root)
            if selector is not None:
                selectors.add(selector)

    if selectors:
        return ValidationDecision(
            "scoped",
            tuple(sorted(selectors)),
            ("affected tests selected from changed paths",),
        )
    return ValidationDecision(
        "fixed-only",
        (),
        ("no changed path maps to an affected pytest scope",),
    )


def _git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def decision_for_refs(base: str, head: str) -> ValidationDecision:
    changes = parse_name_status(
        _git_output("diff", "--name-status", "--find-renames", f"{base}...{head}")
    )
    init_diff = _git_output(
        "diff",
        "--unified=0",
        f"{base}...{head}",
        "--",
        "src/substrate_framework/__init__.py",
    )
    return choose_validation_scope(changes, package_init_diff=init_diff)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="base commit or ref")
    parser.add_argument("--head", default="HEAD", help="head commit or ref")
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="print the decision without running validation",
    )
    arguments = parser.parse_args(argv)

    decision = decision_for_refs(arguments.base, arguments.head)
    print(f"Validation mode: {decision.mode}")
    for reason in decision.reasons:
        print(f"Reason: {reason}")
    if decision.selectors:
        print("Pytest selectors:")
        for selector in decision.selectors:
            print(f"  {selector}")
    if arguments.print_only:
        return 0

    command = [str(ROOT / "scripts/validate.sh")]
    if decision.mode == "full":
        command.append("--full")
    elif decision.mode == "fixed-only":
        command.append("--fixed-only")
    else:
        command.extend(("--pytest-scope", *decision.selectors))
    return subprocess.run(command, cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    sys.exit(main())
