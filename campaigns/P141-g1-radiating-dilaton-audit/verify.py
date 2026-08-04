from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.retarded_wave import (
    retarded_point_source_radiation,
    static_point_source_countermodel,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876"
DOSSIER_SHA256 = "55d1ecc6c1a19c7018befbdef520c3f925b996bc6fae4ccd0dcb31f40388916b"
FROZEN_PROPOSAL_SHA256 = "9e205c57c288ad1f3ed4b67cf84f7f81ee0d0eba37c7d950a23e248087d4a79f"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assignments(tree: ast.AST) -> dict[str, ast.AST]:
    result: dict[str, ast.AST] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value = node.value
            for target in targets:
                if isinstance(target, ast.Name) and value is not None:
                    result.setdefault(target.id, value)
    return result


def main(source_file: str, dossier_file: str) -> int:
    source_path = Path(source_file)
    dossier_path = Path(dossier_file)
    frozen_path = Path(__file__).parent / "evidence" / "frozen-proposal.yaml"
    source_text = source_path.read_text(encoding="utf-8")
    dossier_text = dossier_path.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(source_path))
    checks = CheckLedger("P141/C-RAD-001")

    checks.check("pinned G1 source hash", _sha256(source_path) == SOURCE_SHA256)
    checks.check("pinned G1 dossier hash", _sha256(dossier_path) == DOSSIER_SHA256)
    checks.check("frozen proposal hash", _sha256(frozen_path) == FROZEN_PROPOSAL_SHA256)

    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("ten source predicates", len(source_checks) == 10)
    checks.check("one source assertion", len(source_assertions) == 1)

    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(source_path))
    checks.check(
        "G1 compatibility event is exactly two direct legacy calls",
        compatibility.direct_legacy_attributes == 2
        and compatibility.legacy_references == 2
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "source header explicitly records its legacy NumPy environment",
        "NumPy 1.26.4 -- np.trapz NOT np.trapezoid" in source_text,
    )
    checks.check(
        "dossier explicitly classifies trapz choice by NumPy version",
        "`np.trapz` (old API)" in dossier_text
        and "`np.trapezoid` (numpy 2.0+)" in dossier_text,
    )

    assignments = _assignments(tree)
    far_field_assignment = assignments["h_t_inf"]
    far_field_names = {
        node.id for node in ast.walk(far_field_assignment) if isinstance(node, ast.Name)
    }
    far_field_constants = [
        node.value
        for node in ast.walk(far_field_assignment)
        if isinstance(node, ast.Constant)
    ]
    checks.check(
        "far-field derivative is inserted rather than derived",
        isinstance(far_field_assignment, ast.BinOp)
        and isinstance(far_field_assignment.op, ast.Mult)
        and any(isinstance(node, ast.USub) for node in ast.walk(far_field_assignment))
        and far_field_names == {"kappa", "Q0dot"}
        and far_field_constants == [2]
        and not any(isinstance(node, ast.Call) for node in ast.walk(far_field_assignment)),
    )
    checks.check(
        "two-side power coefficient is inserted as one over two kappa",
        "1 / (2 * kappa)" in ast.unparse(assignments["P_rad_sym"]),
    )
    checks.check(
        "weak-field coupling is selected backward from the target",
        ast.unparse(assignments["kappa_weak"]) == "4 * 0.001 / E0_val",
    )
    success_reads = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "sol"
        and node.attr == "success"
    ]
    checks.check("source never checks solve_ivp success", not success_reads)

    A, B, c = sp.symbols("A B c", positive=True)
    q = sp.symbols("q", real=True)
    retarded = retarded_point_source_radiation(A, B, c, q)
    checks.check(
        "canonical variation and retarded jump close",
        sp.simplify(-c**2 * retarded.derivative_jump - B * q / A) == 0,
    )
    checks.check(
        "retarded branches are outgoing on both sides",
        sp.simplify(retarded.time_derivative + c * retarded.right_space_derivative) == 0
        and sp.simplify(retarded.time_derivative - c * retarded.left_space_derivative) == 0,
    )
    checks.check(
        "exact one-side flux follows the declared action",
        retarded.right_outward_flux == B**2 * q**2 / (4 * A * c),
    )
    checks.check(
        "exact two-side flux equals source work",
        retarded.total_outward_power == B**2 * q**2 / (2 * A * c)
        and retarded.total_outward_power == retarded.source_work_rate,
    )
    checks.mutation_sensitive(
        "flux coefficient is load bearing",
        lambda value: sp.simplify(value - retarded.source_work_rate) == 0,
        retarded.total_outward_power,
        [
            retarded.right_outward_flux,
            retarded.total_outward_power / 4,
            2 * retarded.total_outward_power,
        ],
    )

    static = static_point_source_countermodel(A, B, c, q)
    checks.check(
        "static countermodel has same equation and jump",
        static.equation_delta_coefficient == retarded.equation_delta_coefficient
        and static.derivative_jump == retarded.derivative_jump,
    )
    checks.check(
        "boundary history is load bearing for radiation",
        static.total_outward_power == 0
        and retarded.total_outward_power != static.total_outward_power,
    )

    scale = sp.symbols("s", positive=True)
    rescaled = retarded_point_source_radiation(A / scale**2, B / scale, c, q)
    checks.check(
        "field rescaling preserves physical power",
        sp.simplify(rescaled.total_outward_power - retarded.total_outward_power) == 0,
    )
    checks.mutation_sensitive(
        "source coupling normalization is load bearing",
        lambda coupling: sp.simplify(
            retarded_point_source_radiation(A, coupling, c, q).total_outward_power
            - retarded.total_outward_power
        )
        == 0,
        B,
        [2 * B, B / 2, sp.Integer(0)],
    )

    kappa, qdot = sp.symbols("kappa qdot", positive=True)
    normalized = retarded_point_source_radiation(1 / kappa, 1, 1, q)
    source_power = kappa * qdot**2 / 8
    checks.check(
        "G1-normalized derivative depends on source not source derivative",
        normalized.time_derivative == kappa * q / 2,
    )
    checks.check(
        "G1 power is off by four even under its derivative substitution",
        sp.simplify(normalized.total_outward_power.subs(q, qdot) / source_power) == 4,
    )
    checks.check(
        "constant retarded source is a derivative-order counterexample",
        normalized.total_outward_power.subs(q, 1) != 0
        and source_power.subs(qdot, 0) == 0,
    )

    gamma, rest_trace = sp.symbols("gamma Q_rest", positive=True)
    fixed_lab_integral = rest_trace / gamma
    checks.check(
        "boosted scalar trace integrates with inverse gamma",
        sp.simplify(fixed_lab_integral * gamma - rest_trace) == 0,
    )
    checks.check(
        "source gamma boost is rejected",
        sp.simplify(fixed_lab_integral - gamma * rest_trace) != 0,
    )

    acceleration = sp.symbols("a", nonzero=True, real=True)
    checks.check(
        "accelerated kink centre has nonzero unsourced residual",
        -2 * acceleration != 0,
    )
    checks.check(
        "source same-RHS numerical leg cannot independently test the headline",
        "dEdt = E0_val * g**3 * v * vdot" in source_text
        and "return [dEdt]" in source_text
        and "dEdt_closed = E0_val * g_grid**3 * v_grid * vdot_grid" in source_text,
    )
    action_block = dossier_text.split("Action:", maxsplit=1)[1].split("```", maxsplit=1)[0]
    checks.check(
        "dilaton action does not declare canonical h kinetic density",
        "φ R − V(φ)" in action_block
        and "S_matter[g]" in action_block
        and "∂_t h" not in action_block
        and "∂_x h" not in action_block,
    )
    return checks.finish()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", required=True)
    parser.add_argument("--dossier-file", required=True)
    return parser


if __name__ == "__main__":
    arguments = _parser().parse_args()
    raise SystemExit(main(arguments.source_file, arguments.dossier_file))
