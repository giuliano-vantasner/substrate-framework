from __future__ import annotations

import hashlib

import pytest

from substrate_framework.source_audit import audit_source_tokens


PATTERNS = {
    "action": r"hbar_eff|de[ _]Broglie",
    "energy": r"\bE0\b|E_breather",
}


def test_source_audit_is_sorted_hashed_and_grouped(tmp_path) -> None:
    later = tmp_path / "phase-2" / "b.py"
    earlier = tmp_path / "phase-1" / "a.py"
    later.parent.mkdir(parents=True)
    earlier.parent.mkdir(parents=True)
    later.write_text("E0 = 1\nhbar_eff = E0 / omega\n", encoding="utf-8")
    earlier.write_text("E_breather = 2\n", encoding="utf-8")

    audit = audit_source_tokens(tmp_path, PATTERNS)

    assert audit.scanned_file_count == 2
    assert tuple(match.path for match in audit.matches) == (
        "phase-1/a.py",
        "phase-2/b.py",
    )
    assert audit.paths_for("energy") == ("phase-1/a.py", "phase-2/b.py")
    assert audit.paths_for("action") == ("phase-2/b.py",)
    assert audit.paths_with_all("action", "energy") == ("phase-2/b.py",)
    assert audit.matches[1].sha256 == hashlib.sha256(later.read_bytes()).hexdigest()


def test_exclusions_are_component_aware(tmp_path) -> None:
    excluded = tmp_path / "phase-45" / "bridge.py"
    similarly_named = tmp_path / "phase-450" / "bridge.py"
    excluded.parent.mkdir(parents=True)
    similarly_named.parent.mkdir(parents=True)
    excluded.write_text("hbar_eff", encoding="utf-8")
    similarly_named.write_text("hbar_eff", encoding="utf-8")

    audit = audit_source_tokens(tmp_path, PATTERNS, exclusions=("phase-45",))

    assert audit.scanned_file_count == 1
    assert audit.paths_for("action") == ("phase-450/bridge.py",)


def test_lexical_audit_intentionally_matches_comments(tmp_path) -> None:
    source = tmp_path / "comment.py"
    source.write_text("# de Broglie is mentioned, not imported\n", encoding="utf-8")

    audit = audit_source_tokens(tmp_path, PATTERNS)

    assert audit.paths_for("action") == ("comment.py",)


def test_hash_and_matches_change_with_content(tmp_path) -> None:
    source = tmp_path / "source.py"
    source.write_text("E0 = 1\n", encoding="utf-8")
    before = audit_source_tokens(tmp_path, PATTERNS)
    source.write_text("hbar_eff = 1\n", encoding="utf-8")
    after = audit_source_tokens(tmp_path, PATTERNS)

    assert before.matches[0].sha256 != after.matches[0].sha256
    assert before.paths_for("energy") == ("source.py",)
    assert after.paths_for("energy") == ()
    assert after.paths_for("action") == ("source.py",)


def test_invalid_scope_and_groups_are_rejected(tmp_path) -> None:
    with pytest.raises(ValueError, match="source root"):
        audit_source_tokens(tmp_path / "missing", PATTERNS)
    with pytest.raises(ValueError, match="relative exclusion"):
        audit_source_tokens(tmp_path, PATTERNS, exclusions=("../outside",))
    with pytest.raises(ValueError, match="token pattern"):
        audit_source_tokens(tmp_path, {"empty": ""})

    audit = audit_source_tokens(tmp_path, PATTERNS)
    with pytest.raises(KeyError, match="unknown token group"):
        audit.paths_for("charge")
