"""Static hash-sensitive MR2 graph replay with durable execution reuse."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from pathlib import Path
import subprocess

import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate")


@dataclass(frozen=True)
class SourceNode:
    label: str
    relation: str
    path: str
    sha256: str
    checks: int
    assertions: int


NODES = (
    SourceNode("E2", "accepted_input", "merged-framework/bridges/phase-29/bridge_E2_multi_skyrmion_solutions.py", "fdde30878eaf1f8dff7fce9c2d9d4234d1d6e14566be6d2ee56dd1926481c46f", 6, 1),
    SourceNode("E3", "accepted_input", "merged-framework/bridges/phase-29/bridge_E3_yield_coefficient_overbinding.py", "aa76b9e675d4fbb45594e9d3df5107af175e927a24840260ca71ffda1bad3315", 5, 1),
    SourceNode("E4", "accepted_input", "merged-framework/bridges/phase-29/bridge_E4_bps_zero_binding_resolution.py", "f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7", 5, 1),
    SourceNode("S3", "accepted_input", "merged-framework/bridges/phase-4/bridge_S3_su3_wzw_baryon_reps.py", "44d8cd1f3a3b3d0a316d0984db92d5e47e13cac9dcf3d476e2d996bf09f13b9a", 10, 2),
    SourceNode("MK1", "accepted_input", "merged-framework/bridges/phase-43/bridge_MK1_mu_from_medium_cosine.py", "98ff5459ae3c6cb64a9a7632fbaa8613f1f5b1adb68419de25ffa06b1c3a3222", 7, 1),
    SourceNode("MK2", "accepted_input", "merged-framework/bridges/phase-43/bridge_MK2_lambda_from_medium_omega.py", "351136bca28e413ddd54f1b15bf7084dffe32af565fc87e7220d1437a525eb07", 7, 1),
    SourceNode("MK3", "accepted_input", "merged-framework/bridges/phase-43/bridge_MK3_epsilon_pinned.py", "64254d0f6b9d6ff57f5a8b0a4b86a510e2bef230b4f3bec062533fac59516404", 6, 1),
    SourceNode("MK4", "accepted_input", "merged-framework/bridges/phase-43/bridge_MK4_bps_compacton_and_pt_failure.py", "9f2e299032aace53c3ac2c2d1d5626372e4bdf1aa3b7b0650f574a9f7b8f7295", 6, 1),
    SourceNode("MK5", "accepted_input", "merged-framework/bridges/phase-43/bridge_MK5_generalized_solve_kappa.py", "a5ecb5d0d2ba96cf8083a9cfb32ddb44c2a4f4841bf776ebbccb91bc12b246f8", 8, 1),
    SourceNode("MK6", "accepted_input", "merged-framework/bridges/phase-43/bridge_MK6_confrontation_and_tension.py", "ef900954d9782bbf2589ff3e33045577ebdce3860d1a3ed7a6a6827e0ae81788", 6, 1),
    SourceNode("MR1", "duplicate_predecessor", "merged-framework/bridges/phase-44/bridge_MR1_mass_unit_identity.py", "d065f592390fe9322d27fbd2cf55262d8ccb8d45e6510cf8628058f716b6c875", 7, 1),
    SourceNode("MR2", "audited_root", "merged-framework/bridges/phase-44/bridge_MR2_bps_normalization_pi_squared.py", "2e62ce2d6cbee805a988046a27a742e622931291e8e013a9aede6ce16e48e990", 8, 1),
    SourceNode("MR3", "pending_future_dependency_and_consumer", "merged-framework/bridges/phase-44/bridge_MR3_no_double_counting.py", "c5eaabaeede15909adb5d9ddb951353c376aaa381e669e35c6256d7015e7eddc", 6, 3),
    SourceNode("MR5", "pending_reverse_consumer", "merged-framework/bridges/phase-44/bridge_MR5_solve_at_derived_e.py", "0da10adafe3badb7f3eab225543bc601996df45b142f2d59b5d0ddd6dd9117d7", 6, 1),
    SourceNode("MR6", "pending_reverse_consumer", "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py", "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d", 6, 3),
)


def main() -> int:
    checks = CheckLedger("P220-GRAPH")
    paths = [node.path for node in NODES]
    source_status = subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "status", "--porcelain", "--", *paths],
        capture_output=True,
        text=True,
        check=True,
    )
    checks.check("all fifteen pinned graph paths are clean", source_status.stdout == "")

    rows: dict[str, dict[str, object]] = {}
    for node in NODES:
        path = SOURCE_ROOT / node.path
        payload = path.read_bytes()
        source = payload.decode("utf-8")
        tree = ast.parse(source, filename=node.path)
        compatibility = audit_numpy_trapezoid_compatibility(source, filename=node.path)
        rows[node.label] = {
            "hash_ok": hashlib.sha256(payload).hexdigest() == node.sha256,
            "checks": sum(
                isinstance(item, ast.Call)
                and isinstance(item.func, ast.Name)
                and item.func.id == "check"
                for item in ast.walk(tree)
            ),
            "assertions": sum(isinstance(item, ast.Assert) for item in ast.walk(tree)),
            "legacy": compatibility.legacy_references,
            "eager": compatibility.eager_legacy_default_fallbacks,
            "source": source,
        }
    checks.check(
        "all nodes retain pinned hashes and exact lexical inventories",
        all(bool(row["hash_ok"]) for row in rows.values())
        and sum(int(row["checks"]) for row in rows.values()) == 99
        and sum(int(row["assertions"]) for row in rows.values()) == 20
        and all(
            rows[node.label]["checks"] == node.checks
            and rows[node.label]["assertions"] == node.assertions
            for node in NODES
        ),
    )

    inventory = yaml.safe_load((ROOT / "migration/source-claims.yaml").read_text())
    units = {entry["source_unit"]: entry for entry in inventory["units"]}
    accepted_inputs = {"E2", "E3", "E4", "S3", "MK1", "MK2", "MK3", "MK4", "MK5", "MK6"}
    checks.check(
        "accepted source inputs are consumed only at governed qualified ceilings",
        all(units[label]["disposition"] == "qualified" for label in accepted_inputs)
        and units["MR1"]["disposition"] == "duplicate_evidence",
    )
    checks.check(
        "root and later MR units have no backward accepted authority",
        all(
            units[label]["disposition"] == "pending_adjudication"
            and units[label]["accepted_claims"] == []
            for label in ("MR2", "MR3", "MR5", "MR6")
        ),
    )
    checks.check(
        "all three direct reverse consumers explicitly name MR2",
        all("MR2" in str(rows[label]["source"]) for label in ("MR3", "MR5", "MR6")),
    )
    checks.check(
        "MR3's forward reference is prose rather than backward authority",
        "CONSEQUENCE (developed in MR3)" in str(rows["MR2"]["source"])
        and units["MR3"]["accepted_claims"] == [],
    )

    p215 = yaml.safe_load(
        (ROOT / "campaigns/P215-mk2-vector-sextic-matching-audit/evidence/source-graph-inventory.yaml").read_text()
    )
    p215_rows = {entry["label"]: entry for entry in p215["replay"]}
    p174_graph = (
        ROOT / "campaigns/P174-ki4-backsolve-circularity-audit/evidence/source-graph-inventory.yaml"
    ).read_text()
    checks.check(
        "unchanged native execution evidence is reused without scientific reruns",
        p215_rows["MR2"]["verdict"] == "clean_noncanonical"
        and p215_rows["MR2"]["runtime_checks"] == 8
        and p215_rows["MR6"]["verdict"] == "clean_noncanonical"
        and "MR5: {relation: pending_reverse_consumer, checks: 6, assertions: 1, execution: fresh_clean}"
        in p174_graph,
    )
    checks.check(
        "MR3 is deliberately static until its own frozen campaign",
        "static_only: [MR1, MR3]"
        in (
            ROOT / "campaigns/P219-mk6-confrontation-tension-audit/evidence/source-graph-inventory.yaml"
        ).read_text(),
    )
    checks.check(
        "legacy aliases in immutable inputs are compatibility provenance only",
        rows["E2"]["legacy"] == 1
        and rows["E3"]["legacy"] == 1
        and all(
            rows[label]["legacy"] == 0 and rows[label]["eager"] == 0
            for label in rows
            if label not in {"E2", "E3"}
        ),
    )
    checks.check(
        "pending numeric consumers use current SciPy trapezoid rather than trapz",
        all(
            "from scipy.integrate import" in str(rows[label]["source"])
            and "trapezoid" in str(rows[label]["source"])
            and "trapz" not in str(rows[label]["source"])
            for label in ("MR3", "MR5", "MR6")
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
