"""Primary exact and governance verifier for the P222 MR4 audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.hls_reduction import (
    conditional_hls_ksrf_matching,
    leading_hls_connection_reduction,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


CAMPAIGN = Path(__file__).resolve().parent
ROOT = CAMPAIGN.parents[1]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-44/"
    "bridge_MR4_e_from_rho_saturation.py"
)
SOURCE_SHA = "cefe7192b935ec18992e9cd76fd348ef81934ed9d20843ced3627973cec9d3d7"
FREEZE_SHA = "375d0739c85ed2ef8150125613ac630b0028c1c41654ef26d01a681faf24138f"


def _assignments(tree: ast.AST) -> dict[str, ast.AST]:
    return {
        target.id: node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
    }


def main() -> int:
    checks = CheckLedger("P222")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    tree = ast.parse(source_text)
    checks.check(
        "source and preregistered formula surface are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA
        and hashlib.sha256(
            (CAMPAIGN / "evidence/formula-freeze.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source inventory separates seven predicates and one assertion",
        len(source_checks) == 7 and len(source_assertions) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check(
        "MR4 has no sampled integration or version compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0
        and "numpy" not in source_text
        and "scipy" not in source_text,
    )
    reproduction = yaml.safe_load(
        (CAMPAIGN / "evidence/source-reproduction.yaml").read_text()
    )
    checks.check(
        "hash-identical P215 execution is reused without a ceremonial rerun",
        reproduction["execution_reuse"]["source_hash_identical"] is True
        and reproduction["execution_reuse"]["exit_status"] == 0
        and reproduction["inventory"]["runtime_check_executions"] == 7
        and reproduction["execution_reuse"]["verdict"] == "clean_noncanonical",
    )

    x, y, g, kappa = sp.symbols("x y g kappa", positive=True)
    reduction = leading_hls_connection_reduction(
        [[x, 0, 0], [0, y, 0]],
        g,
        mass_coefficient=kappa,
    )
    checks.check(
        "canonical general reduction owns the nondegenerate half connection",
        reduction.stationary_vector_components
        == sp.Matrix([[x / 2, 0, 0], [0, y / 2, 0]])
        and reduction.mass_hessian == 2 * kappa * sp.eye(6),
    )
    checks.check(
        "canonical Maurer Cartan curvature carries minus one quarter",
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
        "leading curvature and equally normalized Skyrme densities give e equals g",
        sp.simplify(
            reduction.leading_curvature_energy - reduction.matched_skyrme_energy
        )
        == 0
        and reduction.matched_skyrme_coupling == g,
    )
    checks.check(
        "e equals g is explicitly a p4 rather than full-vector theorem",
        reduction.derivative_orders.leading_quartic_energy == 4
        and reduction.derivative_orders.kinetic_eom_residual == 3
        and reduction.derivative_orders.first_backreaction_energy == 6,
    )

    assignments = _assignments(tree)
    point_assignment = assignments["PT"]
    checks.check(
        "MR4.1 and MR4.2 source residuals are evaluated at one point",
        isinstance(point_assignment, ast.Dict)
        and ast.unparse(point_assignment).find("37") >= 0
        and ast.unparse(point_assignment).find("-53") >= 0
        and ".subs(PT)" in source_text,
    )
    checks.check(
        "the source full-vector equation is a prose substitution not a solved EOM",
        "V_mu = alpha_par_mu" in source_text
        and "kinetic_eom_residual" not in source_text
        and "backreaction" not in source_text.lower(),
    )

    mass, decay, parameter = sp.symbols("m_V F a", positive=True)
    matching = conditional_hls_ksrf_matching(
        mass,
        decay,
        hls_parameter=parameter,
    )
    checks.check(
        "canonical KSRF API keeps mass scale and a visible",
        matching.relation_residual == 0
        and matching.skyrme_coupling == mass / (sp.sqrt(parameter) * decay)
        and matching.skyrme_coupling.free_symbols == {mass, decay, parameter},
    )
    common_unit, e_sk = sp.symbols("U e", positive=True)
    solutions = sp.solve(
        [
            sp.Eq(e_sk, g),
            sp.Eq(mass**2, parameter * g**2 * decay**2),
            sp.Eq(decay, e_sk * common_unit),
        ],
        [e_sk, g, decay],
        dict=True,
    )
    expected = sp.sqrt(mass) / (sp.sqrt(common_unit) * parameter ** sp.Rational(1, 4))
    checks.check(
        "fresh simultaneous elimination gives the conditional square-root closure",
        len(solutions) == 1
        and sp.simplify(solutions[0][e_sk] - expected) == 0
        and sp.simplify(expected**2 - mass / (sp.sqrt(parameter) * common_unit))
        == 0,
    )
    checks.check(
        "the closure retains exactly mass common-unit and KSRF inputs",
        expected.free_symbols == {mass, common_unit, parameter},
    )
    checks.mutation_sensitive(
        "the KSRF parameter is load bearing",
        lambda candidate: sp.simplify(
            candidate - sp.sqrt(mass / (sp.sqrt(2) * common_unit))
        )
        == 0,
        expected.subs(parameter, 2),
        (expected.subs(parameter, 1), expected.subs(parameter, 4)),
    )
    checks.mutation_sensitive(
        "the declared common-unit coefficient is load bearing",
        lambda coefficient: sp.simplify(
            expected.subs({parameter: 2, common_unit: coefficient * sp.pi * sp.Symbol("E", positive=True)})
            - sp.sqrt(
                mass
                / (
                    16
                    * sp.sqrt(2)
                    * sp.pi
                    * sp.Symbol("E", positive=True)
                )
            )
        )
        == 0,
        16,
        (8, 32),
    )

    electron = sp.symbols("m_e", positive=True)
    source_root = expected.subs(
        {parameter: 2, common_unit: 16 * sp.pi * electron}
    )
    source_target = sp.sqrt(mass / (16 * sp.sqrt(2) * sp.pi * electron))
    checks.check(
        "the MR4 square-root expression is the exact a-two specialization",
        sp.simplify(source_root - source_target) == 0,
    )
    supplied_value = source_target.subs(
        {mass: sp.Rational(77526, 100), electron: sp.Rational(511, 1000)}
    )
    checks.check(
        "4.61976 is a supplied mass-ratio substitution only",
        abs(float(supplied_value) - 4.619774866381011) < 1.0e-12
        and source_target.free_symbols == {mass, electron},
    )
    rho = sp.symbols("rho", positive=True)
    checks.check(
        "common mass-unit scaling leaves a free ratio rather than predicting it",
        sp.simplify(
            source_target.subs({mass: rho * mass, electron: rho * electron})
            - source_target
        )
        == 0
        and sp.diff(source_target, mass) != 0
        and sp.diff(source_target, electron) != 0,
    )

    alternative = expected.subs(
        {parameter: sp.Rational(1, 2), common_unit: 16 * sp.pi * electron}
    )
    checks.check(
        "the alternative convention is a coefficient mutation by sqrt two",
        sp.simplify(alternative / source_target - sp.sqrt(2)) == 0,
    )
    arbitrary_coupling = sp.symbols("e_target", positive=True)
    parameter_for_target = (
        mass / (common_unit * arbitrary_coupling**2)
    ) ** 2
    checks.check(
        "an unfixed KSRF coefficient permits every positive coupling not a bracket",
        sp.simplify(expected.subs(parameter, parameter_for_target) - arbitrary_coupling)
        == 0,
    )

    loaded_in_inside = {
        node.id
        for node in ast.walk(assignments["inside"])
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    sixth_condition_names = {
        node.id
        for node in ast.walk(sorted(source_checks, key=lambda node: node.lineno)[5].args[1])
        if isinstance(node, ast.Name)
    }
    checks.check(
        "the imported ANW fit is load bearing in MR4.6",
        "E_ANW_IMPORTED" in loaded_in_inside and "inside" in sixth_condition_names,
    )
    checks.check(
        "MR4.7 is a selected-needle guard rather than dependency closure",
        isinstance(assignments["FORBIDDEN"], ast.List)
        and "E_ANW_IMPORTED = 5.45" in source_text
        and ast.unparse(assignments["derived_clean"])
        == "e_closed.free_symbols == {m_V, m_e}",
    )

    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())
    claims = {entry["id"]: entry for entry in registry["claims"]}
    checks.check(
        "accepted owners already contain every exact MR4 survivor",
        claims["C-VEC-001"]["review"] == "accepted"
        and "e=g=m_V/(sqrt(a)*F)" in claims["C-VEC-001"]["statement"]
        and claims["C-SK-001"]["review"] == "accepted"
        and "F_pi/e=16*pi*E_e" in claims["C-SK-001"]["statement"],
    )
    delta = yaml.safe_load(
        (CAMPAIGN / "evidence/post-source-claim-delta.yaml").read_text()
    )
    checks.check(
        "exact nonduplication retains no claim or API delta",
        delta["provisional_claims"] == []
        and delta["decision"] == "retain_no_claim_or_canonical_API"
        and delta["expected_disposition"] == "duplicate_evidence",
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
