"""Hash-sensitive P219 source graph with prior-execution reuse."""

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
    path: str
    sha256: str
    checks: int
    assertions: int


NODES = (
    SourceNode("B1", "merged-framework/bridges/phase-7/bridge_B1_disclination_berry_connection.py", "2de4faa60ecc1f87ca356afd55c2a531a89327c3c46e4296176052113de7b0b6", 8, 1),
    SourceNode("E2", "merged-framework/bridges/phase-29/bridge_E2_multi_skyrmion_solutions.py", "fdde30878eaf1f8dff7fce9c2d9d4234d1d6e14566be6d2ee56dd1926481c46f", 6, 1),
    SourceNode("E3", "merged-framework/bridges/phase-29/bridge_E3_yield_coefficient_overbinding.py", "aa76b9e675d4fbb45594e9d3df5107af175e927a24840260ca71ffda1bad3315", 5, 1),
    SourceNode("E4", "merged-framework/bridges/phase-29/bridge_E4_bps_zero_binding_resolution.py", "f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7", 5, 1),
    SourceNode("HE4", "merged-framework/bridges/phase-45/bridge_HE4_dhn_action_variable.py", "0fae1f54748a5206214afaeb1fb7293f46c04c6146e1779c41837fddaf245f29", 16, 1),
    SourceNode("MK1", "merged-framework/bridges/phase-43/bridge_MK1_mu_from_medium_cosine.py", "98ff5459ae3c6cb64a9a7632fbaa8613f1f5b1adb68419de25ffa06b1c3a3222", 7, 1),
    SourceNode("MK2", "merged-framework/bridges/phase-43/bridge_MK2_lambda_from_medium_omega.py", "351136bca28e413ddd54f1b15bf7084dffe32af565fc87e7220d1437a525eb07", 7, 1),
    SourceNode("MK3", "merged-framework/bridges/phase-43/bridge_MK3_epsilon_pinned.py", "64254d0f6b9d6ff57f5a8b0a4b86a510e2bef230b4f3bec062533fac59516404", 6, 1),
    SourceNode("MK4", "merged-framework/bridges/phase-43/bridge_MK4_bps_compacton_and_pt_failure.py", "9f2e299032aace53c3ac2c2d1d5626372e4bdf1aa3b7b0650f574a9f7b8f7295", 6, 1),
    SourceNode("MK5", "merged-framework/bridges/phase-43/bridge_MK5_generalized_solve_kappa.py", "a5ecb5d0d2ba96cf8083a9cfb32ddb44c2a4f4841bf776ebbccb91bc12b246f8", 8, 1),
    SourceNode("MK6", "merged-framework/bridges/phase-43/bridge_MK6_confrontation_and_tension.py", "ef900954d9782bbf2589ff3e33045577ebdce3860d1a3ed7a6a6827e0ae81788", 6, 1),
    SourceNode("NY1", "merged-framework/bridges/phase-24/bridge_NY1_skyrme_energy_unit.py", "b3531d7f906fe396a1326d44d68f34d09ae34988e86a8f721c360040c4aa0921", 9, 0),
    SourceNode("S5", "merged-framework/bridges/phase-4/bridge_S5_realizability_magnitude.py", "b92a9db67940169fcd9919f83fda6ae8c56b9b9e40b0d2cbebef5539a5dccde6", 28, 1),
    SourceNode("MR1", "merged-framework/bridges/phase-44/bridge_MR1_mass_unit_identity.py", "d065f592390fe9322d27fbd2cf55262d8ccb8d45e6510cf8628058f716b6c875", 7, 1),
    SourceNode("MR2", "merged-framework/bridges/phase-44/bridge_MR2_bps_normalization_pi_squared.py", "2e62ce2d6cbee805a988046a27a742e622931291e8e013a9aede6ce16e48e990", 8, 1),
    SourceNode("MR3", "merged-framework/bridges/phase-44/bridge_MR3_no_double_counting.py", "c5eaabaeede15909adb5d9ddb951353c376aaa381e669e35c6256d7015e7eddc", 6, 3),
    SourceNode("MR4", "merged-framework/bridges/phase-44/bridge_MR4_e_from_rho_saturation.py", "cefe7192b935ec18992e9cd76fd348ef81934ed9d20843ced3627973cec9d3d7", 7, 1),
    SourceNode("MR5", "merged-framework/bridges/phase-44/bridge_MR5_solve_at_derived_e.py", "0da10adafe3badb7f3eab225543bc601996df45b142f2d59b5d0ddd6dd9117d7", 6, 1),
    SourceNode("MR6", "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py", "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d", 6, 3),
)

QUALIFIED_PREDECESSORS = {
    "B1", "E2", "E3", "E4", "HE4", "MK1", "MK2", "MK3", "MK4", "MK5", "S5"
}
DIRECT_REVERSE = {"MR1", "MR2", "MR3", "MR6"}
PENDING_MR = {"MR2", "MR3", "MR4", "MR5", "MR6"}


def main() -> int:
    checks = CheckLedger("P219-GRAPH")
    paths = [node.path for node in NODES]
    status = subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "status", "--porcelain", "--", *paths],
        capture_output=True,
        text=True,
        check=True,
    )
    checks.check("all nineteen pinned source paths are clean", status.stdout == "")
    rows: list[dict[str, object]] = []
    for node in NODES:
        path = SOURCE_ROOT / node.path
        payload = path.read_bytes()
        text = payload.decode("utf-8")
        tree = ast.parse(text, filename=node.path)
        compatibility = audit_numpy_trapezoid_compatibility(text, filename=node.path)
        rows.append(
            {
                "label": node.label,
                "hash_ok": hashlib.sha256(payload).hexdigest() == node.sha256,
                "checks": sum(
                    isinstance(item, ast.Call)
                    and isinstance(item.func, ast.Name)
                    and item.func.id == "check"
                    for item in ast.walk(tree)
                ),
                "assertions": sum(isinstance(item, ast.Assert) for item in ast.walk(tree)),
                "legacy": compatibility.legacy_references,
                "current": compatibility.current_references,
                "eager": compatibility.eager_legacy_default_fallbacks,
                "text": text,
            }
        )
    expected = {node.label: node for node in NODES}
    by_label = {str(row["label"]): row for row in rows}
    checks.check(
        "all nodes retain pinned hashes and exact lexical inventories",
        all(bool(row["hash_ok"]) for row in rows)
        and sum(int(row["checks"]) for row in rows) == 157
        and sum(int(row["assertions"]) for row in rows) == 22
        and all(
            row["checks"] == expected[str(row["label"])].checks
            and row["assertions"] == expected[str(row["label"])].assertions
            for row in rows
        ),
    )
    dispositions = yaml.safe_load((ROOT / "migration/dispositions.yaml").read_text())[
        "units"
    ]
    checks.check(
        "accepted predecessors are consumed only at governed ceilings",
        all(dispositions[label]["disposition"] == "qualified" for label in QUALIFIED_PREDECESSORS)
        and dispositions["NY1"]["disposition"] == "duplicate_evidence",
    )
    checks.check(
        "root and later MR units remain nonauthoritative before P219 review",
        "MK6" not in dispositions
        and dispositions["MR1"]["disposition"] == "duplicate_evidence"
        and all(label not in dispositions for label in PENDING_MR),
    )
    checks.check(
        "all four direct reverse consumers name MK6 and later siblings grant no authority",
        all("MK6" in str(by_label[label]["text"]) for label in DIRECT_REVERSE)
        and all(label in by_label for label in PENDING_MR),
    )
    root_reproduction = yaml.safe_load(
        (CAMPAIGN := ROOT / "proposals/P219-mk6-confrontation-tension-audit")
        .joinpath("evidence/source-reproduction.yaml")
        .read_text()
    )
    p215 = yaml.safe_load(
        (ROOT / "campaigns/P215-mk2-vector-sextic-matching-audit/evidence/source-graph-inventory.yaml").read_text()
    )
    prior_rows = {row["label"]: row for row in p215["replay"]}
    checks.check(
        "native and expensive unchanged execution evidence is reused without reruns",
        root_reproduction["inventory"]["runtime_check_executions"] == 6
        and all(
            prior_rows[label]["verdict"] == "clean_noncanonical"
            for label in ("MR2", "MR4", "MR6")
        )
        and (ROOT / "campaigns/P174-ki4-backsolve-circularity-audit/reviews/replay_source_graph.py").read_text().find(expected["MR5"].sha256) >= 0,
    )
    checks.check(
        "legacy integration shapes remain compatibility provenance only",
        by_label["B1"]["legacy"] == 1
        and by_label["B1"]["current"] == 1
        and by_label["B1"]["eager"] == 1
        and all(
            by_label[label]["legacy"] == 1
            and by_label[label]["current"] == 1
            and by_label[label]["eager"] == 0
            for label in ("E2", "E3")
        )
        and all(
            row["legacy"] == 0 and row["current"] == 0 and row["eager"] == 0
            for row in rows
            if row["label"] not in {"B1", "E2", "E3"}
        ),
    )
    checks.check(
        "B1 eager legacy access is backed by prior alias-only provenance",
        "immutable_alias_only_replay"
        in (ROOT / "campaigns/P152-b1-berry-connection-audit/evidence/consumer-audit.yaml").read_text(),
    )
    checks.check(
        "dirty later source work is excluded from the pinned graph",
        all(not node.label.startswith(("BM", "CE")) for node in NODES),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
