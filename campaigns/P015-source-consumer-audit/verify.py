#!/usr/bin/env python3
"""Deterministic, mutation-sensitive verifier for the P015 source audit."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path
import tempfile

import yaml

from substrate_framework.source_audit import SourceAudit, audit_source_tokens
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class AuditCandidate:
    action_pattern: str
    energy_pattern: str
    charge_pattern: str
    exclusions: tuple[str, ...]


def _records(audit: SourceAudit) -> list[dict[str, object]]:
    return [
        {
            "path": match.path,
            "sha256": match.sha256,
            "groups": list(match.groups),
        }
        for match in audit.matches
    ]


def _candidate_matches(
    candidate: AuditCandidate,
    source_root: Path,
    expected: dict,
) -> bool:
    audit = audit_source_tokens(
        source_root / expected["root"],
        {
            "action": candidate.action_pattern,
            "energy": candidate.energy_pattern,
            "charge": candidate.charge_pattern,
        },
        include_pattern=expected["include_pattern"],
        exclusions=candidate.exclusions,
    )
    return (
        audit.scanned_file_count == expected["scanned_file_count"]
        and _records(audit) == expected["matched_files"]
        and {
            group: len(audit.paths_for(group))
            for group in ("action", "energy", "charge")
        }
        == expected["group_counts"]
    )


def _tree_digest(source_root: Path) -> tuple[int, str]:
    records = sorted(path for path in source_root.rglob("*") if path.is_file())
    digest = hashlib.sha256()
    for path in records:
        relative = path.relative_to(source_root).as_posix()
        content_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(content_hash.encode("ascii"))
        digest.update(b"\n")
    return len(records), digest.hexdigest()


def run(source_root: Path) -> int:
    checks = CheckLedger("P015-SOURCE-AUDIT")
    framework_root = Path(__file__).resolve().parents[2]
    report = yaml.safe_load(
        (Path(__file__).parent / "evidence" / "consumer-report.yaml").read_text(
            encoding="utf-8"
        )
    )
    source_inventory = yaml.safe_load(
        (
            framework_root
            / "campaigns/P001-sine-gordon-root/evidence/source-inventory.yaml"
        ).read_text(encoding="utf-8")
    )
    main = report["main_scan"]
    patterns = main["token_patterns"]

    rebuilt_file_count, rebuilt_tree_hash = _tree_digest(source_root)
    checks.check(
        "the complete supplied source tree matches the pinned baseline digest",
        rebuilt_tree_hash == report["source_tree_sha256"]
        == source_inventory["tree_sha256"]
        and rebuilt_file_count == source_inventory["file_count"],
    )

    audit = audit_source_tokens(
        source_root / main["root"],
        patterns,
        include_pattern=main["include_pattern"],
        exclusions=tuple(main["exclusions"]),
    )
    expected_bridge_count = sum(
        record["phase"] != "phase-45"
        for record in source_inventory["bridge_records"]
    )
    checks.check(
        "the explicit exclusion leaves every and only non-phase-45 bridge file",
        audit.scanned_file_count == main["scanned_file_count"]
        == expected_bridge_count
        == 213,
    )
    checks.check(
        "the complete sorted matched-file report reproduces with exact hashes and groups",
        _records(audit) == main["matched_files"],
    )

    inventory_hashes = {
        record["path"]: record["sha256"] for record in source_inventory["files"]
    }
    checks.check(
        "every reported match hash agrees with the independent full-tree inventory",
        all(
            inventory_hashes[f"{main['root']}/{match.path}"] == match.sha256
            for match in audit.matches
        ),
    )
    checks.check(
        "the declared action tokens have no match outside the excluded phase",
        audit.paths_for("action") == ()
        and main["group_counts"]["action"] == 0,
    )
    checks.check(
        "the energy token group reproduces all 36 lexical consumers",
        len(audit.paths_for("energy")) == main["group_counts"]["energy"] == 36
        and "phase-1/bridge_T1E_E0_triple_oracle.py"
        in audit.paths_for("energy")
        and "phase-3/bridge_EM1_u1_noether_charge.py"
        in audit.paths_for("energy"),
    )
    expected_charge_paths = (
        "phase-11/bridge_FG1_charged_soliton_reconciliation.py",
        "phase-3/bridge_EM1_u1_noether_charge.py",
        "phase-3/bridge_EM5_induced_gauge_sector.py",
        "phase-46/bridge_EL2_lepton_is_baryonless_fermion.py",
    )
    checks.check(
        "the charge token group names the four pinned lexical matches",
        audit.paths_for("charge") == expected_charge_paths
        and main["group_counts"]["charge"] == 4,
    )
    checks.check(
        "the reported energy-action and charge-action lexical intersections are empty",
        audit.paths_with_all("energy", "action")
        == tuple(main["energy_action_intersection"])
        == ()
        and audit.paths_with_all("charge", "action")
        == tuple(main["charge_action_intersection"])
        == (),
    )

    for control_name, control in report["positive_controls"].items():
        control_audit = audit_source_tokens(
            source_root / control["root"],
            patterns,
            include_pattern="*.py",
        )
        expected_action = tuple(
            record["path"] for record in control["action_matches"]
        )
        checks.check(
            f"{control_name} positive control reproduces the five action matches",
            control_audit.scanned_file_count == control["scanned_file_count"] == 37
            and control_audit.paths_for("action") == expected_action
            and control_audit.paths_with_all("energy", "action")
            == tuple(control["energy_action_intersection"])
            == expected_action,
        )
        expected_hashes = {
            record["path"]: record["sha256"]
            for record in control["action_matches"]
        }
        checks.check(
            f"{control_name} positive-control action hashes match the pinned inventory",
            all(
                expected_hashes[path] == inventory_hashes[f"{control['root']}/{path}"]
                for path in expected_action
            ),
        )

    inclusive_audit = audit_source_tokens(
        source_root / main["root"],
        patterns,
        include_pattern=main["include_pattern"],
    )
    checks.check(
        "removing the phase exclusion reveals action-token matches and changes the census",
        inclusive_audit.scanned_file_count > audit.scanned_file_count
        and bool(inclusive_audit.paths_for("action")),
    )

    with tempfile.TemporaryDirectory(prefix="p015-source-audit-") as temporary:
        fixture_root = Path(temporary)
        source = fixture_root / "consumer.py"
        source.write_text("# hbar_eff appears only in a comment\nE0 = 1\n", encoding="utf-8")
        lexical = audit_source_tokens(fixture_root, patterns)
        checks.check(
            "a comment-only occurrence is a counterexample to semantic dependency inference",
            lexical.paths_with_all("action", "energy") == ("consumer.py",),
        )
        original_hash = lexical.matches[0].sha256
        source.write_text("E0 = 1\n", encoding="utf-8")
        mutated = audit_source_tokens(fixture_root, patterns)
        checks.check(
            "content mutation changes the hash and removes the action-token intersection",
            mutated.paths_with_all("action", "energy") == ()
            and mutated.matches[0].sha256 != original_hash,
        )

    baseline = AuditCandidate(
        action_pattern=patterns["action"],
        energy_pattern=patterns["energy"],
        charge_pattern=patterns["charge"],
        exclusions=tuple(main["exclusions"]),
    )
    checks.mutation_sensitive(
        "token families and exclusions are load-bearing",
        lambda candidate: _candidate_matches(candidate, source_root, main),
        baseline,
        [
            AuditCandidate(
                patterns["action"], patterns["energy"], patterns["charge"], ()
            ),
            AuditCandidate(
                patterns["action"] + r"|Q_N_closed",
                patterns["energy"],
                patterns["charge"],
                tuple(main["exclusions"]),
            ),
            AuditCandidate(
                patterns["action"],
                r"\bE0\b",
                patterns["charge"],
                tuple(main["exclusions"]),
            ),
        ],
    )

    total = checks.finish()
    print(f"P015 ALL {total} CHECKS PASS")
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
