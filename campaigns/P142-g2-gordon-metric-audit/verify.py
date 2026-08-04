from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.gordon_metric import (
    gordon_metric_mostly_plus,
    transverse_profile_einstein,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "666df886d7567d87796615753143ace56a4f06fb6e1de4ea53208b1fc6ba0f88"
DOSSIER_SHA256 = "973422e36765607ef6bd67fe84e555924fce73bfd128c01cdf0acc6a89c28ecb"
FROZEN_PROPOSAL_SHA256 = "5e5ca74264b01858bb0bb44e7b149029559595ef1eae51aa1fa2d9d77ffdd71f"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _function_return(tree: ast.AST, name: str) -> ast.AST:
    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    if len(functions) != 1:
        raise AssertionError(f"expected one {name} definition")
    returns = [node for node in ast.walk(functions[0]) if isinstance(node, ast.Return)]
    if len(returns) != 1 or returns[0].value is None:
        raise AssertionError(f"expected one value return in {name}")
    return returns[0].value


def main(source_file: str, dossier_file: str) -> int:
    source_path = Path(source_file)
    dossier_path = Path(dossier_file)
    frozen_path = Path(__file__).parent / "evidence" / "frozen-proposal.yaml"
    source_text = source_path.read_text(encoding="utf-8")
    dossier_text = dossier_path.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(source_path))
    checks = CheckLedger("P142/C-GOR-001")

    checks.check("pinned G2 source hash", _sha256(source_path) == SOURCE_SHA256)
    checks.check("pinned G2 dossier hash", _sha256(dossier_path) == DOSSIER_SHA256)
    checks.check("frozen proposal hash", _sha256(frozen_path) == FROZEN_PROPOSAL_SHA256)

    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("six source predicates", len(source_checks) == 6)
    checks.check("one source assertion", len(source_assertions) == 1)

    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(source_path)
    )
    checks.check(
        "G2 has no NumPy integration compatibility event",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    source_return = ast.unparse(_function_return(tree, "gordon_contravariant"))
    checks.check(
        "source mixes mostly-plus normalization with mostly-minus coefficient",
        source_return == "eta_inv + (n_expr ** 2 - 1) * (u * u.T)"
        and "eta = diag(-1,+1,+1,+1)" in source_text
        and "u^mu normalized eta_{mu nu} u^mu u^nu = -1" in source_text,
    )
    assignments = {
        target.id: node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
    }
    checks.check(
        "source labels the spurious pole and selects n equals two plus x",
        "pole at n=sqrt2" in source_text
        and ast.unparse(assignments["n_profile"]) == "2 + x",
    )
    checks.check(
        "dossier claims a source without constructing tensor equality",
        "CAN source it consistently" in dossier_text
        and "free to be sourced" in dossier_text
        and "coupled PDE system" in dossier_text
        and "Finding a closed solution is NOT required by the rung" in dossier_text,
    )

    n = sp.symbols("n", positive=True)
    correct_rest = gordon_metric_mostly_plus(n, [1, 0, 0, 0])
    checks.check(
        "mostly-plus Gordon rest metric has the physical null speed",
        correct_rest.contravariant == sp.diag(-n**2, 1, 1, 1)
        and correct_rest.covariant == sp.diag(-1 / n**2, 1, 1, 1)
        and correct_rest.rest_phase_speed == 1 / n,
    )
    checks.check(
        "correct determinant has no positive-index pole",
        correct_rest.contravariant_determinant == -n**2
        and correct_rest.covariant_determinant == -1 / n**2,
    )

    gamma = 2 / sp.sqrt(3)
    corrected = gordon_metric_mostly_plus(2, [gamma, 0, 0, gamma / 2])
    source_wrong = sp.diag(-1, 1, 1, 1) + 3 * sp.Matrix(
        [gamma, 0, 0, gamma / 2]
    ) * sp.Matrix([gamma, 0, 0, gamma / 2]).T
    wrong_eigenvalues = source_wrong.eigenvals()
    checks.check(
        "source n equals two inverse metric is positive definite",
        all(value.is_positive is True for value in wrong_eigenvalues)
        and sum(wrong_eigenvalues.values()) == 4,
    )
    checks.check(
        "correct n equals two metric remains Lorentzian",
        corrected.contravariant.det() == -4
        and corrected.covariant.det() == -sp.Rational(1, 4),
    )
    checks.mutation_sensitive(
        "rank-one sign is load bearing",
        lambda coefficient: sp.simplify(
            (sp.diag(-1, 1, 1, 1) + coefficient * sp.Matrix([1, 0, 0, 0])
             * sp.Matrix([1, 0, 0, 0]).T).det()
            + n**2
        )
        == 0,
        1 - n**2,
        [n**2 - 1, 1 + n**2, sp.Integer(0)],
    )

    x = sp.symbols("x", real=True)
    profile = sp.Function("n", positive=True)(x)
    result = transverse_profile_einstein(profile, x, sp.Rational(1, 2))
    tensor = result.einstein_covariant
    witness = {profile: 2, sp.diff(profile, x): 1, sp.diff(profile, x, 2): 0}
    evaluated = tensor.applyfunc(lambda entry: sp.simplify(entry.subs(witness)))
    checks.check(
        "correct profile witness is one sixth rather than five sixths",
        evaluated[0, 0] == sp.Rational(1, 6)
        and evaluated[0, 0] != sp.Rational(5, 6),
    )
    checks.check(
        "fixed-half-boost component ratios survive only conditionally",
        evaluated[0, 3] == -2 * evaluated[0, 0]
        and evaluated[2, 2] == 3 * evaluated[0, 0]
        and evaluated[3, 3] == 4 * evaluated[0, 0]
        and evaluated[1, 1] == 0,
    )
    checks.mutation_sensitive(
        "curvature witness normalization is load bearing",
        lambda value: sp.simplify(value - evaluated[0, 0]) == 0,
        sp.Rational(1, 6),
        [sp.Rational(5, 6), -sp.Rational(1, 6), sp.Integer(0)],
    )

    constant = transverse_profile_einstein(sp.Integer(2), x, sp.Rational(1, 2))
    checks.check(
        "constant index limit is exactly flat",
        constant.einstein_covariant == sp.zeros(4) and constant.ricci_scalar == 0,
    )

    epsilon = sp.symbols("epsilon", real=True)
    correct_weak = sp.series(-1 / (1 + epsilon) ** 2, epsilon, 0, 2).removeO()
    optical_weak = sp.series(-1 / (1 + epsilon), epsilon, 0, 2).removeO()
    checks.check(
        "correct Gordon and optical families still differ at first order",
        correct_weak == -1 + 2 * epsilon
        and optical_weak == -1 + epsilon
        and sp.simplify(correct_weak - optical_weak) == epsilon,
    )

    coupling, energy_density = sp.symbols("kappa rho", positive=True)
    inferred_coupling = sp.solve(
        sp.Eq(evaluated[0, 0], coupling * energy_density), coupling
    )[0]
    checks.check(
        "one-plus-one breather fails the nonzero tz geometry component",
        inferred_coupling == 1 / (6 * energy_density)
        and evaluated[0, 3] != inferred_coupling * 0,
    )
    gordon_stress_names = [
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
        and 131 <= node.lineno < 290
        and node.id.lower().startswith("t")
        and node.id != "t"
    ]
    checks.check(
        "executable Gordon block contains no stress tensor substitution",
        not gordon_stress_names,
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
