from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.hls_reduction import (
    conditional_hls_ksrf_matching,
    leading_hls_connection_reduction,
    su2_current_quartic,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "49c7b2392bbe23d2824f4f73030ccd30f245e1750e0c7736dc420d3f64d7a780"
DOSSIER_SHA256 = "1680127b0678d8969f7f08da0463ddab10f34e75554d3a842813275868030ed9"
FROZEN_PROPOSAL_SHA256 = "a10f782694ccadae2fa45509299196d0cff76df7e9df1f281f186aa05a329084"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assignments(tree: ast.AST) -> dict[str, ast.AST]:
    result: dict[str, ast.AST] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    result.setdefault(target.id, node.value)
    return result


def main(source_file: str, dossier_file: str) -> int:
    source_path = Path(source_file)
    dossier_path = Path(dossier_file)
    frozen_path = Path(__file__).parent / "evidence" / "frozen-proposal.yaml"
    source_text = source_path.read_text(encoding="utf-8")
    dossier_text = dossier_path.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(source_path))
    checks = CheckLedger("P140/C-VEC-001")

    checks.check("pinned S4 source hash", _sha256(source_path) == SOURCE_SHA256)
    checks.check("pinned S4 dossier hash", _sha256(dossier_path) == DOSSIER_SHA256)
    checks.check("frozen proposal hash", _sha256(frozen_path) == FROZEN_PROPOSAL_SHA256)

    source_checks = sorted(
        (
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
        ),
        key=lambda node: node.lineno,
    )
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("eleven source predicates", len(source_checks) == 11)
    checks.check("one source assertion", len(source_assertions) == 1)

    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(source_path),
    )
    checks.check(
        "S4 has no NumPy trapezoid compatibility event",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    assignments = _assignments(tree)
    inserted_effective_term = assignments["L_eff"]
    inserted_effective_names = {
        node.id
        for node in ast.walk(inserted_effective_term)
        if isinstance(node, ast.Name)
    }
    checks.check(
        "source assigns the claimed effective term without eliminating a field",
        isinstance(inserted_effective_term, ast.BinOp)
        and isinstance(inserted_effective_term.op, ast.Mult)
        and inserted_effective_names == {"g", "m_rho", "Tr_comm_sq"}
        and not any(
            name in inserted_effective_names
            for name in {"rho", "vector_field", "kernel", "source"}
        ),
    )
    checks.check(
        "source assigns rho tensor equal to the desired tensor",
        ast.unparse(assignments["rho_on_config"]) == "skyrme_struct",
    )
    checks.check(
        "source beta ratios are literals",
        ast.unparse(assignments["beta_over_alpha_rho"]) == "sp.Rational(-1, 1)"
        and ast.unparse(assignments["beta_over_alpha_lat"])
        == "sp.Rational(2, 1)",
    )
    seventh_condition_names = {
        node.id
        for node in ast.walk(source_checks[6].args[1])
        if isinstance(node, ast.Name)
    }
    checks.check(
        "numeric c4 check does not depend on rho or KSRF variables",
        seventh_condition_names == {"target_ok", "J1_sane", "rho_not_floppy"},
    )
    loaded_names = [
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    ]
    checks.check(
        "declared particle values do not enter any source check",
        loaded_names.count("F_pi_val") == 0 and loaded_names.count("m_rho_MeV") == 0,
    )
    checks.check(
        "dossier records its own dimensional mismatch",
        "not dimensionless" in dossier_text
        and "need F_π units careful" in dossier_text,
    )

    x = sp.Matrix([[1, 2, 0], [0, 1, 3], [2, 0, 1]])
    quartic = su2_current_quartic(x)
    checks.check(
        "general current identity closes beyond the source special case",
        quartic.wedge_norm_squared
        == quartic.invariant_one - quartic.invariant_two,
    )
    checks.check(
        "general Pauli trace normalization closes",
        quartic.trace_commutator_sum == -8 * quartic.wedge_norm_squared,
    )
    checks.check("noncommuting current has positive wedge", quartic.wedge_norm_squared > 0)
    checks.check(
        "rank-one counterexample has no quartic term",
        su2_current_quartic([[1, 2, 3]]).wedge_norm_squared == 0,
    )

    spatial_rotation = sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])
    internal_rotation = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    rotated = su2_current_quartic(spatial_rotation * x * internal_rotation)
    checks.check(
        "full quartic is spatially and internally orthogonal invariant",
        rotated.wedge_norm_squared == quartic.wedge_norm_squared
        and rotated.trace_commutator_sum == quartic.trace_commutator_sum,
    )

    g, kappa = sp.symbols("g kappa", positive=True)
    reduction = leading_hls_connection_reduction(x, g, mass_coefficient=kappa)
    checks.check(
        "declared mass term selects the half connection",
        reduction.stationary_vector_components == x / 2
        and reduction.mass_stationarity_residual == sp.zeros(3, 3),
    )
    checks.check(
        "half connection has positive mass Hessian",
        reduction.mass_hessian == 2 * kappa * sp.eye(9),
    )
    checks.check(
        "Maurer Cartan curvature fixes minus one quarter",
        all(
            (
                sp.Matrix(pair.connection_curvature)
                + sp.Matrix(pair.current_commutator) / 4
            ).applyfunc(sp.simplify)
            == sp.zeros(2)
            for pair in reduction.curvature_pairs
        ),
    )
    checks.check(
        "leading vector curvature equals the Skyrme density",
        sp.simplify(
            reduction.leading_curvature_energy - reduction.matched_skyrme_energy
        )
        == 0,
    )
    checks.check(
        "leading positive density has inverse dimensionless coupling squared",
        sp.simplify(
            reduction.leading_curvature_energy
            - quartic.wedge_norm_squared / (4 * g**2)
        )
        == 0,
    )
    checks.check(
        "equally normalized Skyrme matching is e equals g",
        reduction.matched_skyrme_coupling == g,
    )
    checks.check(
        "mass coefficient cannot fit the leading quartic",
        not reduction.leading_curvature_energy.has(kappa),
    )
    checks.check(
        "full vector backreaction stays beyond the claimed p4 order",
        reduction.derivative_orders.kinetic_eom_residual == 3
        and reduction.derivative_orders.leading_quartic_energy == 4
        and reduction.derivative_orders.first_backreaction_energy == 6,
    )

    mass, decay, parameter = sp.symbols("m F a", positive=True)
    matching = conditional_hls_ksrf_matching(
        mass,
        decay,
        hls_parameter=parameter,
    )
    checks.check("conditional KSRF residual vanishes", matching.relation_residual == 0)
    checks.check(
        "conditional KSRF gives a dimensionless mass ratio",
        matching.skyrme_coupling == mass / (sp.sqrt(parameter) * decay),
    )
    checks.mutation_sensitive(
        "HLS parameter is load bearing",
        lambda value: sp.simplify(value - mass / (sp.sqrt(2) * decay)) == 0,
        conditional_hls_ksrf_matching(mass, decay).gauge_coupling,
        [
            conditional_hls_ksrf_matching(mass, decay, hls_parameter=1).gauge_coupling,
            mass / (2 * decay),
        ],
    )
    numerical = conditional_hls_ksrf_matching(775, sp.Rational(924, 10))
    checks.check(
        "a two particle-value regression gives dimensionless order six coupling",
        5.9 < float(numerical.skyrme_coupling) < 6.0,
    )
    checks.check(
        "source e equals F over two mutation is rejected",
        numerical.skyrme_coupling != sp.Rational(924, 20),
    )

    mass_dimensions = {"g": 0, "m_rho": 1, "current_commutator_squared": 4}

    def mass_degree(powers: dict[str, int]) -> int:
        return sum(mass_dimensions[name] * power for name, power in powers.items())

    source_density_degree = mass_degree(
        {"g": 2, "m_rho": -2, "current_commutator_squared": 1}
    )
    canonical_density_degree = mass_degree(
        {"g": -2, "current_commutator_squared": 1}
    )
    checks.check(
        "source coefficient has the wrong four-dimensional mass degree",
        source_density_degree == 2 and source_density_degree != 4,
    )
    checks.check(
        "canonical coefficient has the correct four-dimensional mass degree",
        canonical_density_degree == 4,
    )
    checks.check(
        "B1 is absent from the accepted conditional reduction",
        "B1" not in str(reduction) and "B1" not in str(matching),
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
