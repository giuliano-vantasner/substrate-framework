from __future__ import annotations

from pathlib import Path

from scripts.validate_changed import (
    Change,
    choose_validation_scope,
    is_additive_leaf_theorem_promotion,
    parse_name_status,
)


def _touch(root: Path, *paths: str) -> None:
    for path in paths:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# test fixture\n", encoding="utf-8")


def test_name_status_parser_uses_rename_destination() -> None:
    changes = parse_name_status(
        "M\tAGENTS.md\nA\ttests/test_new.py\nR100\told.py\tnew.py\n"
    )
    assert changes == [
        Change("M", "AGENTS.md"),
        Change("A", "tests/test_new.py"),
        Change("R", "new.py"),
    ]


def test_policy_change_selects_policy_and_repository_tests(tmp_path: Path) -> None:
    _touch(
        tmp_path,
        "tests/test_public_contribution_surfaces.py",
        "tests/test_repository_validation.py",
    )
    decision = choose_validation_scope(
        [Change("M", "AGENTS.md")], repo_root=tmp_path
    )
    assert decision.mode == "scoped"
    assert decision.selectors == (
        "tests/test_public_contribution_surfaces.py",
        "tests/test_repository_validation.py",
    )


def test_unmapped_documentation_change_uses_fixed_checks_only(tmp_path: Path) -> None:
    decision = choose_validation_scope(
        [Change("M", "README.md")], repo_root=tmp_path
    )
    assert decision.mode == "fixed-only"
    assert decision.selectors == ()


def test_new_module_with_matching_test_and_additive_export_is_scoped(
    tmp_path: Path,
) -> None:
    _touch(tmp_path, "tests/test_new_atom.py")
    decision = choose_validation_scope(
        [
            Change("A", "src/substrate_framework/new_atom.py"),
            Change("M", "src/substrate_framework/__init__.py"),
            Change("A", "tests/test_new_atom.py"),
        ],
        repo_root=tmp_path,
        package_init_diff="@@ -1,0 +2 @@\n+from .new_atom import value\n",
    )
    assert decision.mode == "scoped"
    assert decision.selectors == ("tests/test_new_atom.py",)


def test_new_module_without_matching_test_forces_full(tmp_path: Path) -> None:
    decision = choose_validation_scope(
        [Change("A", "src/substrate_framework/untested.py")],
        repo_root=tmp_path,
    )
    assert decision.mode == "full"
    assert "no matching test" in decision.reasons[0]


def test_existing_framework_module_change_forces_full(tmp_path: Path) -> None:
    decision = choose_validation_scope(
        [Change("M", "src/substrate_framework/model.py")],
        repo_root=tmp_path,
    )
    assert decision.mode == "full"
    assert "existing framework module" in decision.reasons[0]


def test_removed_package_export_forces_full(tmp_path: Path) -> None:
    decision = choose_validation_scope(
        [Change("M", "src/substrate_framework/__init__.py")],
        repo_root=tmp_path,
        package_init_diff="@@ -2 +1,0 @@\n-from .old_api import value\n",
    )
    assert decision.mode == "full"
    assert "public surface" in decision.reasons[0]


def test_unpaired_additive_package_export_forces_full(tmp_path: Path) -> None:
    decision = choose_validation_scope(
        [Change("M", "src/substrate_framework/__init__.py")],
        repo_root=tmp_path,
        package_init_diff="@@ -1,0 +2 @@\n+from .existing_api import value\n",
    )
    assert decision.mode == "full"
    assert "without one tested new framework module" in decision.reasons[0]


def test_removed_test_forces_full(tmp_path: Path) -> None:
    decision = choose_validation_scope(
        [Change("D", "tests/test_deleted.py")], repo_root=tmp_path
    )
    assert decision.mode == "full"
    assert "coverage was removed" in decision.reasons[0]


def test_governance_change_forces_full(tmp_path: Path) -> None:
    decision = choose_validation_scope(
        [Change("M", "governance/claims.yaml")], repo_root=tmp_path
    )
    assert decision.mode == "full"
    assert "governance semantics" in decision.reasons[0]


def test_additive_leaf_theorem_promotion_can_remain_scoped(tmp_path: Path) -> None:
    _touch(
        tmp_path,
        "tests/test_governance.py",
        "tests/test_repository_validation.py",
        "tests/test_lean_scaffold.py",
    )
    decision = choose_validation_scope(
        [
            Change("M", "governance/claims.yaml"),
            Change("M", "governance/releases/current.yaml"),
            Change("A", "governance/releases/v2.yaml"),
            Change("A", "formal/SubstrateFramework/NewTheorem.lean"),
        ],
        repo_root=tmp_path,
        additive_leaf_promotion=True,
    )
    assert decision.mode == "scoped"
    assert decision.selectors == (
        "tests/test_governance.py",
        "tests/test_lean_scaffold.py",
        "tests/test_repository_validation.py",
    )
    assert decision.additional_checks == ("scripts/check_lean.sh",)


def test_additive_leaf_classifier_rejects_changed_existing_claim() -> None:
    atom = {"id": "C1", "accepted_in": "v1", "epistemic": "active"}
    other_atom = {"id": "C0", "accepted_in": "v1", "epistemic": "active"}
    old_registry = {"claims": [other_atom, atom]}
    theorem = {
        "id": "C2",
        "category": "synthesized",
        "review": "accepted",
        "accepted_in": "v2",
        "epistemic": "active",
        "dependencies": ["C0", "C1"],
    }
    new_registry = {"claims": [dict(other_atom), dict(atom), theorem]}
    old_release = {"release": "v1", "accepted_claims": ["C0", "C1"]}
    new_release = {"release": "v2", "accepted_claims": ["C0", "C1", "C2"]}

    assert is_additive_leaf_theorem_promotion(
        old_registry, new_registry, old_release, new_release
    )
    new_registry["claims"][0]["statement"] = "changed"
    assert not is_additive_leaf_theorem_promotion(
        old_registry, new_registry, old_release, new_release
    )


def test_validation_driver_change_selects_its_regressions(tmp_path: Path) -> None:
    _touch(
        tmp_path,
        "tests/test_validate_changed.py",
        "tests/test_validate_script.py",
        "tests/test_public_contribution_surfaces.py",
    )
    decision = choose_validation_scope(
        [Change("M", "scripts/validate.sh")], repo_root=tmp_path
    )
    assert decision.mode == "scoped"
    assert decision.selectors == (
        "tests/test_public_contribution_surfaces.py",
        "tests/test_validate_changed.py",
        "tests/test_validate_script.py",
    )
