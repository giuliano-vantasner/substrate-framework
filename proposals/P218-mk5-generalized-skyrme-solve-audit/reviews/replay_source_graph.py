"""Hash-sensitive P218 source graph with proportional execution reuse."""

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
    frozen_disposition: str


NODES = (
    SourceNode("E1", "merged-framework/bridges/phase-29/bridge_E1_rational_map_integrals.py", "1afa9ba8ade88912e7361bbbd6f59a9fce5cc114c75ddf604a6439bc066ae2d1", 6, 1, "qualified"),
    SourceNode("E2", "merged-framework/bridges/phase-29/bridge_E2_multi_skyrmion_solutions.py", "fdde30878eaf1f8dff7fce9c2d9d4234d1d6e14566be6d2ee56dd1926481c46f", 6, 1, "qualified"),
    SourceNode("E3", "merged-framework/bridges/phase-29/bridge_E3_yield_coefficient_overbinding.py", "aa76b9e675d4fbb45594e9d3df5107af175e927a24840260ca71ffda1bad3315", 5, 1, "qualified"),
    SourceNode("E4", "merged-framework/bridges/phase-29/bridge_E4_bps_zero_binding_resolution.py", "f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7", 5, 1, "qualified"),
    SourceNode("HE4", "merged-framework/bridges/phase-45/bridge_HE4_dhn_action_variable.py", "0fae1f54748a5206214afaeb1fb7293f46c04c6146e1779c41837fddaf245f29", 16, 1, "qualified"),
    SourceNode("KI3", "merged-framework/bridges/phase-34/bridge_KI3_bracket_is_sharp.py", "10e92457cbd213782e5778f5b739660a6d07ea229c44746e24fe0132844fcbd3", 5, 1, "qualified"),
    SourceNode("KI4", "merged-framework/bridges/phase-34/bridge_KI4_backsolve_circularity.py", "138f204c2bf7e7278a1a4aadad4bed1680e11b6b6de7189a02640a81652f00cd", 5, 1, "qualified"),
    SourceNode("KI5", "merged-framework/bridges/phase-34/bridge_KI5_kappa_is_not_a_variational_bound.py", "5db475be67e6668f9064096055b0452bb2a762c435132ae324896cce3f9863fe", 5, 1, "qualified"),
    SourceNode("MK1", "merged-framework/bridges/phase-43/bridge_MK1_mu_from_medium_cosine.py", "98ff5459ae3c6cb64a9a7632fbaa8613f1f5b1adb68419de25ffa06b1c3a3222", 7, 1, "qualified"),
    SourceNode("MK2", "merged-framework/bridges/phase-43/bridge_MK2_lambda_from_medium_omega.py", "351136bca28e413ddd54f1b15bf7084dffe32af565fc87e7220d1437a525eb07", 7, 1, "qualified"),
    SourceNode("MK3", "merged-framework/bridges/phase-43/bridge_MK3_epsilon_pinned.py", "64254d0f6b9d6ff57f5a8b0a4b86a510e2bef230b4f3bec062533fac59516404", 6, 1, "qualified"),
    SourceNode("MK4", "merged-framework/bridges/phase-43/bridge_MK4_bps_compacton_and_pt_failure.py", "9f2e299032aace53c3ac2c2d1d5626372e4bdf1aa3b7b0650f574a9f7b8f7295", 6, 1, "qualified"),
    SourceNode("MK5", "merged-framework/bridges/phase-43/bridge_MK5_generalized_solve_kappa.py", "a5ecb5d0d2ba96cf8083a9cfb32ddb44c2a4f4841bf776ebbccb91bc12b246f8", 8, 1, "pending_adjudication"),
    SourceNode("MK6", "merged-framework/bridges/phase-43/bridge_MK6_confrontation_and_tension.py", "ef900954d9782bbf2589ff3e33045577ebdce3860d1a3ed7a6a6827e0ae81788", 6, 1, "pending_adjudication"),
    SourceNode("MR1", "merged-framework/bridges/phase-44/bridge_MR1_mass_unit_identity.py", "d065f592390fe9322d27fbd2cf55262d8ccb8d45e6510cf8628058f716b6c875", 7, 1, "duplicate_evidence"),
    SourceNode("MR2", "merged-framework/bridges/phase-44/bridge_MR2_bps_normalization_pi_squared.py", "2e62ce2d6cbee805a988046a27a742e622931291e8e013a9aede6ce16e48e990", 8, 1, "pending_adjudication"),
    SourceNode("MR3", "merged-framework/bridges/phase-44/bridge_MR3_no_double_counting.py", "c5eaabaeede15909adb5d9ddb951353c376aaa381e669e35c6256d7015e7eddc", 6, 3, "pending_adjudication"),
    SourceNode("MR4", "merged-framework/bridges/phase-44/bridge_MR4_e_from_rho_saturation.py", "cefe7192b935ec18992e9cd76fd348ef81934ed9d20843ced3627973cec9d3d7", 7, 1, "pending_adjudication"),
    SourceNode("MR5", "merged-framework/bridges/phase-44/bridge_MR5_solve_at_derived_e.py", "0da10adafe3badb7f3eab225543bc601996df45b142f2d59b5d0ddd6dd9117d7", 6, 1, "pending_adjudication"),
    SourceNode("MR6", "merged-framework/bridges/phase-44/bridge_MR6_ledger_and_confrontation.py", "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d", 6, 3, "pending_adjudication"),
)

PREDECESSORS = {"E1", "E2", "E3", "E4", "HE4", "KI3", "KI4", "KI5", "MK1", "MK2", "MK3", "MK4"}
REVERSE = {"MK6", "MR1", "MR2", "MR3", "MR4", "MR5", "MR6"}
SAFE_FALLBACKS = {"E1", "E2", "E3", "KI5"}


def main() -> int:
    checks = CheckLedger("P218-GRAPH")
    rows: list[dict[str, object]] = []
    paths = [node.path for node in NODES]
    source_status = subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "status", "--porcelain", "--", *paths],
        capture_output=True,
        text=True,
        check=True,
    )
    checks.check("all twenty pinned graph paths are clean", source_status.stdout == "")
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
    by_label = {str(row["label"]): row for row in rows}
    expected = {node.label: node for node in NODES}
    checks.check(
        "all graph nodes retain their pinned hashes",
        all(bool(row["hash_ok"]) for row in rows),
    )
    checks.check(
        "graph inventory pins 133 predicates and 24 assertions",
        sum(int(row["checks"]) for row in rows) == 133
        and sum(int(row["assertions"]) for row in rows) == 24
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
        "all twelve predecessors are consumed only at qualified dispositions",
        all(dispositions[label]["disposition"] == "qualified" for label in PREDECESSORS),
    )
    checks.check(
        "reverse consumers retain governed nonauthoritative dispositions",
        dispositions["MR1"]["disposition"] == "duplicate_evidence"
        and all(label not in dispositions for label in REVERSE - {"MR1"}),
    )
    checks.check(
        "all seven reverse consumers explicitly name MK5",
        all("MK5" in str(by_label[label]["text"]) for label in REVERSE),
    )

    root_reproduction = yaml.safe_load(
        (
            ROOT
            / "proposals/P218-mk5-generalized-skyrme-solve-audit/evidence/source-reproduction.yaml"
        ).read_text()
    )
    p215 = yaml.safe_load(
        (
            ROOT
            / "campaigns/P215-mk2-vector-sextic-matching-audit/evidence/source-graph-inventory.yaml"
        ).read_text()
    )
    p215_rows = {row["label"]: row for row in p215["replay"]}
    p174_script = (
        ROOT
        / "campaigns/P174-ki4-backsolve-circularity-audit/reviews/replay_source_graph.py"
    ).read_text()
    checks.check(
        "expensive unchanged executions are reused through pinned hashes",
        root_reproduction["native"]["runtime_checks"] == 8
        and all(
            p215_rows[label]["verdict"] == "clean_noncanonical"
            for label in ("MK6", "MR2", "MR6")
        )
        and expected["MR5"].sha256 in p174_script
        and 'Node("MR5"' in p174_script
        and "True" in p174_script.split('Node("MR5"', 1)[1].split(")", 1)[0],
    )
    checks.check(
        "safe current-first fallbacks are compatibility provenance only",
        {
            str(row["label"])
            for row in rows
            if int(row["legacy"]) or int(row["current"])
        }
        == SAFE_FALLBACKS
        and all(
            row["legacy"] == 1 and row["current"] == 1 and row["eager"] == 0
            for row in rows
            if row["label"] in SAFE_FALLBACKS
        )
        and all(
            row["legacy"] == 0 and row["current"] == 0 and row["eager"] == 0
            for row in rows
            if row["label"] not in SAFE_FALLBACKS
        ),
    )
    checks.check(
        "dirty later phase work is excluded from the pinned graph",
        all(not node.label.startswith(("BM", "CE")) for node in NODES),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
