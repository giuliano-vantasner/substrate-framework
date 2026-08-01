from __future__ import annotations

from scripts.inventory_claims import build_claim_inventory
from scripts.inventory_source import build_inventory


def test_claim_inventory_extracts_bridge_queue_and_disposition(tmp_path) -> None:
    bridge = tmp_path / "merged-framework/bridges/phase-1/bridge_A1_root.py"
    bridge.parent.mkdir(parents=True)
    bridge.write_text(
        '''"""Bridge A1 root.\n\nQUESTION\n  Does the root close?\nRESULT\n  Yes, symbolically.\n"""\nimport sympy\ndef check(*args): pass\ncheck("literal", True, "wrong")\nfor i in range(2): check(f"dynamic {i}", True, "wrong")\nprint("ALL 3 CHECKS PASS")\n''',
        encoding="utf-8",
    )
    source = build_inventory(tmp_path, "source@test")
    scope = {
        "source_baseline": "source@test",
        "tree_sha256": source["tree_sha256"],
        "primary_unit_role": "bridge",
    }
    dispositions = {
        "source_baseline": "source@test",
        "units": {
            "A1": {
                "disposition": "partially_migrated",
                "accepted_claims": ["C1"],
                "remaining_scope": "one subclaim",
            }
        },
    }

    result = build_claim_inventory(tmp_path, source, scope, dispositions)
    unit = result["units"][0]
    assert result["primary_unit_count"] == 1
    assert result["disposition_counts"] == {"partially_migrated": 1}
    assert unit["headline"] == "Bridge A1 root."
    assert unit["question_excerpt"] == "Does the root close?"
    assert unit["result_excerpt"] == "Yes, symbolically."
    assert unit["static_check_calls"] == 2
    assert unit["literal_check_calls"] == 1
    assert unit["dynamic_check_calls"] == 1
    assert unit["terminal_tally_literal_present"]
    assert unit["accepted_claims"] == ["C1"]


def test_claim_inventory_preserves_qualified_evidence(tmp_path) -> None:
    bridge = tmp_path / "merged-framework/bridges/phase-1/bridge_A1_root.py"
    bridge.parent.mkdir(parents=True)
    bridge.write_text('"""Bridge A1."""\n', encoding="utf-8")
    source = build_inventory(tmp_path, "source@test")
    scope = {
        "source_baseline": "source@test",
        "tree_sha256": source["tree_sha256"],
        "primary_unit_role": "bridge",
    }
    dispositions = {
        "source_baseline": "source@test",
        "units": {
            "A1": {
                "disposition": "qualified",
                "accepted_claims": ["C1"],
                "qualification": "only the exact subclaim survives",
                "evidence": ["campaigns/P1/source-adjudication.md"],
            }
        },
    }

    unit = build_claim_inventory(tmp_path, source, scope, dispositions)["units"][0]
    assert unit["qualification"] == "only the exact subclaim survives"
    assert unit["evidence"] == ["campaigns/P1/source-adjudication.md"]
