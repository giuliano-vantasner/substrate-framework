#!/usr/bin/env python3
"""Select the smallest safe repository-validation mode for a pull request."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys

import yaml


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
    "scripts/validate.sh",
    "scripts/validate_changed.py",
}
SCRIPT_TEST_MAP = {
    "scripts/bootstrap.sh": "tests/test_lean_scaffold.py",
    "scripts/check_lean.sh": "tests/test_lean_scaffold.py",
    "scripts/setup_lean.sh": "tests/test_lean_scaffold.py",
    "scripts/find_synthesis_candidates.py": "tests/test_claim_graph.py",
    "scripts/validate_repository.py": "tests/test_repository_validation.py",
}
LEAN_SETUP_PATHS = {
    "scripts/bootstrap.sh",
    "scripts/check_lean.sh",
    "scripts/setup_lean.sh",
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
    additional_checks: tuple[str, ...] = ()


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


def _additive_governance_paths_only(changes: list[Change]) -> bool:
    for change in changes:
        path = change.path
        if not path.startswith("governance/"):
            continue
        if path in {"governance/claims.yaml", "governance/releases/current.yaml"}:
            continue
        if (
            path.startswith("governance/releases/")
            and path.endswith(".yaml")
            and change.status == "A"
        ):
            continue
        return False
    return True


def is_additive_leaf_theorem_promotion(
    old_registry: dict,
    new_registry: dict,
    old_release: dict,
    new_release: dict,
) -> bool:
    """Recognize an append-only synthesized theorem promotion boundary."""

    try:
        old_claims = {claim["id"]: claim for claim in old_registry["claims"]}
        new_claims = {claim["id"]: claim for claim in new_registry["claims"]}
        old_release_ids = old_release["accepted_claims"]
        new_release_ids = new_release["accepted_claims"]
    except (KeyError, TypeError):
        return False
    if not isinstance(old_release_ids, list) or not isinstance(new_release_ids, list):
        return False
    if any(new_claims.get(claim_id) != claim for claim_id, claim in old_claims.items()):
        return False
    added_ids = set(new_claims) - set(old_claims)
    if not added_ids:
        return False
    if new_release.get("release") == old_release.get("release"):
        return False
    if new_release_ids[: len(old_release_ids)] != old_release_ids:
        return False
    if set(new_release_ids[len(old_release_ids) :]) != added_ids:
        return False
    for claim_id in added_ids:
        claim = new_claims[claim_id]
        if claim.get("category") != "synthesized":
            return False
        if claim.get("review") != "accepted" or claim.get("accepted_in") != new_release.get(
            "release"
        ):
            return False
        dependencies = claim.get("dependencies")
        if (
            not isinstance(dependencies, list)
            or len(dependencies) < 2
            or len(dependencies) != len(set(dependencies))
        ):
            return False
        if not set(dependencies) <= set(old_claims):
            return False
        if any(
            old_claims[dependency].get("accepted_in") is None
            or old_claims[dependency].get("epistemic") not in {"active", "qualified"}
            for dependency in dependencies
        ):
            return False
    return True


def choose_validation_scope(
    changes: list[Change],
    *,
    repo_root: Path = ROOT,
    package_init_diff: str = "",
    additive_leaf_promotion: bool = False,
) -> ValidationDecision:
    """Return a conservative full, scoped, or fixed-only validation decision."""

    paths = {change.path for change in changes}
    full_reasons: list[str] = []
    selectors: set[str] = set()
    additional_checks = (
        ("scripts/check_lean.sh",)
        if any(path.startswith("formal/") for path in paths)
        or bool(paths & LEAN_SETUP_PATHS)
        else ()
    )

    for path in sorted(paths):
        if path in FULL_EXACT_PATHS or path.startswith(FULL_PREFIXES):
            full_reasons.append(f"cross-cutting path changed: {path}")

    governance_changes = [
        change for change in changes if change.path.startswith("governance/")
    ]
    if governance_changes:
        if additive_leaf_promotion and _additive_governance_paths_only(changes):
            for path in ("tests/test_governance.py", "tests/test_repository_validation.py"):
                selector = _existing_selector(path, repo_root)
                if selector is not None:
                    selectors.add(selector)
        else:
            full_reasons.append("claim or release governance semantics changed")

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
        and path not in VALIDATION_DRIVER_PATHS | SCRIPT_TEST_MAP.keys()
    }
    if unknown_scripts:
        full_reasons.append(
            "validation impact is uncertain for executable scripts: "
            + ", ".join(sorted(unknown_scripts))
        )

    if full_reasons:
        return ValidationDecision(
            "full", (), tuple(full_reasons), additional_checks
        )

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

    for script, test_path in SCRIPT_TEST_MAP.items():
        if script in paths:
            selector = _existing_selector(test_path, repo_root)
            if selector is not None:
                selectors.add(selector)

    if any(path.startswith("formal/") for path in paths):
        selector = _existing_selector("tests/test_lean_scaffold.py", repo_root)
        if selector is not None:
            selectors.add(selector)

    if selectors:
        return ValidationDecision(
            "scoped",
            tuple(sorted(selectors)),
            ("affected tests selected from changed paths",),
            additional_checks,
        )
    return ValidationDecision(
        "fixed-only",
        (),
        ("no changed path maps to an affected pytest scope",),
        additional_checks,
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


def _git_yaml(ref: str, path: str) -> dict:
    data = yaml.safe_load(_git_output("show", f"{ref}:{path}"))
    return data if isinstance(data, dict) else {}


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
    try:
        additive_leaf_promotion = is_additive_leaf_theorem_promotion(
            _git_yaml(base, "governance/claims.yaml"),
            _git_yaml(head, "governance/claims.yaml"),
            _git_yaml(base, "governance/releases/current.yaml"),
            _git_yaml(head, "governance/releases/current.yaml"),
        )
    except subprocess.CalledProcessError:
        additive_leaf_promotion = False
    return choose_validation_scope(
        changes,
        package_init_diff=init_diff,
        additive_leaf_promotion=additive_leaf_promotion,
    )


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
    if decision.additional_checks:
        print("Additional checks:")
        for check in decision.additional_checks:
            print(f"  {check}")
    if arguments.print_only:
        return 0

    command = [str(ROOT / "scripts/validate.sh")]
    if decision.mode == "full":
        command.append("--full")
    elif decision.mode == "fixed-only":
        command.append("--fixed-only")
    else:
        command.extend(("--pytest-scope", *decision.selectors))
    result = subprocess.run(command, cwd=ROOT, check=False)
    if result.returncode != 0:
        return result.returncode
    for check in decision.additional_checks:
        result = subprocess.run([str(ROOT / check)], cwd=ROOT, check=False)
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
