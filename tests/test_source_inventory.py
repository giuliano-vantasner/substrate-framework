from __future__ import annotations

from scripts.inventory_source import build_inventory, classify


def test_source_inventory_classifies_and_cross_references_bridges(tmp_path) -> None:
    first = tmp_path / "merged-framework/bridges/phase-0/bridge_A1_root.py"
    second = tmp_path / "merged-framework/bridges/phase-1/bridge_B2_consumer.py"
    dossier = tmp_path / "merged-framework/bridges/phase-1/dossiers/B2.md"
    first.parent.mkdir(parents=True)
    second.parent.mkdir(parents=True)
    dossier.parent.mkdir(parents=True)
    first.write_text('"""RESULT DERIVED"""\n\ndef check(value):\n    return value\n', encoding="utf-8")
    second.write_text('"""B2 reuses A1 and is NUMERICAL"""\nimport scipy\n', encoding="utf-8")
    dossier.write_text("# B2\n", encoding="utf-8")

    inventory = build_inventory(tmp_path, "source@test")

    assert inventory["file_count"] == 3
    assert inventory["role_counts"] == {"bridge": 2, "dossier": 1}
    assert inventory["bridge_count"] == 2
    by_label = {record["label"]: record for record in inventory["bridge_records"]}
    assert by_label["A1"]["defines_local_check_helper"]
    assert by_label["B2"]["candidate_dependencies"] == ["A1"]
    assert by_label["B2"]["imports_scipy"]
    assert classify(dossier.relative_to(tmp_path)) == "dossier"


def test_tree_digest_changes_when_source_changes(tmp_path) -> None:
    source = tmp_path / "root.py"
    source.write_text("value = 1\n", encoding="utf-8")
    before = build_inventory(tmp_path, "source@test")["tree_sha256"]
    source.write_text("value = 2\n", encoding="utf-8")
    after = build_inventory(tmp_path, "source@test")["tree_sha256"]
    assert before != after
