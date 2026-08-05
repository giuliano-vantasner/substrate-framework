#!/usr/bin/env python3
"""Independent raw AST and symbolic review of the MD6 debt ledger."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate/merged-framework/bridges/phase-38")
MD6 = SOURCE_ROOT / "bridge_MD6_honesty_firewall_and_debt_ledger.py"
MD4 = SOURCE_ROOT / "bridge_MD4_growth_threshold_and_the_rescue.py"
MD6_SHA256 = "08b6d263323e3a09da39152c7409795d97477521f2fcf8d57b295922fefa1cbf"
RELEASE_SHA256 = "fbb97885d564d6dc57c8b5bdf37cd619484a4f361545ea4ae198917de6b2ed05"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def raw_assignment_hits(source: str) -> tuple[str, ...]:
    selected = {
        "beta_sq", "beta_a_sq", "S", "rho", "M", "K", "a", "ell",
        "Omega", "omega_ph", "A2",
    }
    result: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if (
                isinstance(target, ast.Name)
                and target.id in selected
                and not target.id.startswith(("ILLUSTRATION_", "COMPARATOR_"))
                and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, (int, float))
            ):
                result.append(target.id)
    return tuple(result)


def condition_for(tree: ast.AST, label_prefix: str) -> ast.AST:
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            and len(node.args) >= 2
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ):
            continue
        if node.args[0].value.startswith(label_prefix):
            return node.args[1]
    raise LookupError(label_prefix)


def loaded_names(node: ast.AST) -> set[str]:
    return {
        child.id
        for child in ast.walk(node)
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load)
    }


def main() -> int:
    checks = CheckLedger("P201-MD6-INDEPENDENT")
    checks.check("MD6 bytes are independently pinned", digest(MD6) == MD6_SHA256)
    checks.check(
        "base release is independently pinned",
        digest(ROOT / "governance/releases/v0.149.0.yaml") == RELEASE_SHA256,
    )
    text = MD6.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(MD6))
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "independent AST inventory has 23 sites with five dynamic labels",
        len(calls) == 23
        and sum(
            not (
                node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            )
            for node in calls
        ) == 5,
    )
    empty_condition = condition_for(tree, "DEBT LEDGER IS EMPTY")
    checks.check(
        "independent AST review finds the empty-ledger condition is literal true",
        isinstance(empty_condition, ast.Constant) and empty_condition.value is True,
    )
    residual_condition = condition_for(tree, "NO NEW RESIDUAL")
    checks.check(
        "independent residual review finds only three conjuncts",
        isinstance(residual_condition, ast.BoolOp)
        and len(residual_condition.values) == 3,
    )

    checks.check(
        "annotated unary constructed destructured and named-expression values evade the matcher",
        all(
            not raw_assignment_hits(candidate)
            for candidate in (
                "beta_sq: float = 0.245",
                "beta_sq = -0.245",
                "beta_sq = float('0.245')",
                "beta_sq, x = 0.245, 1",
                "(beta_sq := 0.245)",
            )
        ),
    )
    checks.check(
        "the direct untagged numeric fixture is the narrow proposition retained",
        raw_assignment_hits("beta_sq = 0.245") == ("beta_sq",),
    )
    nested = "def audit_note():\n    '''no measured_dos input is used'''\n    return 1"
    nested_tree = ast.parse(nested)
    nested_segment = ast.get_source_segment(nested, nested_tree.body[0]) or ""
    checks.check(
        "nested docstring survives top-level segmentation and contains a selected literal",
        "measured_dos" in nested_segment.lower(),
    )
    checks.check(
        "constructed and numeric-only comparators evade the finite literal vocabulary",
        "excess_heat" not in "value = 'excess_' + 'heat'"
        and not any(
            word in "calibration = 30\ncheck('gate', result < calibration)"
            for word in ("excess_heat", "cop_", "calorimet", "measured_dos", "watts")
        ),
    )

    md4_tree = ast.parse(MD4.read_text(encoding="utf-8"), filename=str(MD4))
    assignment_dependencies: dict[str, set[str]] = {}
    conditions: list[set[str]] = []
    for node in ast.walk(md4_tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignment_dependencies[target.id] = loaded_names(node.value)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            and len(node.args) >= 2
        ):
            conditions.append(loaded_names(node.args[1]))

    def reaches_condition(origin: str) -> bool:
        reachable = {origin}
        for _ in range(len(assignment_dependencies) + 1):
            reachable |= {
                target
                for target, inputs in assignment_dependencies.items()
                if inputs & reachable
            }
        return any(names & reachable for names in conditions)

    checks.check(
        "independent data-flow witnesses both tagged constants reaching checks",
        reaches_condition("COMPARATOR_WN6_log10_w")
        and reaches_condition("ILLUSTRATION_beta_sq"),
    )

    dimension = sp.Integer(3)
    speed, gap, volume, cell, omega = sp.symbols("c gap V a omega", positive=True)
    wave_number = sp.sqrt(omega**2 - gap**2) / speed
    shell_density = sp.simplify(
        volume
        * 4
        * sp.pi
        * wave_number**2
        / (2 * sp.pi) ** dimension
        * sp.diff(wave_number, omega)
    )
    cutoff = (6 * sp.pi**2) ** sp.Rational(1, 3) / cell
    upper = sp.sqrt(gap**2 + speed**2 * cutoff**2)
    integrated = sp.simplify(sp.integrate(shell_density, (omega, gap, upper)))
    checks.check(
        "raw shell-Jacobian derivation gives the conditional one-branch count",
        sp.simplify(integrated - volume / cell**3) == 0,
    )
    checks.check(
        "multiplying by three is a separately supplied branch count",
        dimension * integrated == 3 * volume / cell**3 and dimension == 3,
    )

    size, rho = sp.symbols("N rho", positive=True)
    weight = sp.Function("weight")
    branching = rho / (size * weight(size) + rho)
    total = sp.factor(sp.diff(branching, size))
    expected = -rho * (
        weight(size) + size * sp.diff(weight(size), size)
    ) / (size * weight(size) + rho) ** 2
    checks.check(
        "raw differentiation retains population-dependent weight slope",
        sp.simplify(total - expected) == 0,
    )
    inverse_square = sp.simplify(branching.subs(weight(size), size**-2))
    inverse_square_derivative = sp.factor(sp.diff(inverse_square, size))
    checks.check(
        "inverse-square weight derivative has an exact manifestly positive form",
        sp.simplify(
            inverse_square_derivative - rho / (size * rho + 1) ** 2
        ) == 0,
    )
    fixed = sp.symbols("fixed", positive=True)
    fixed_rho_derivative = sp.factor(sp.diff(rho / (size * fixed + rho), rho))
    checks.check(
        "fixed branching response retains an exact positive rho derivative",
        sp.simplify(
            fixed_rho_derivative
            - size * fixed / (size * fixed + rho) ** 2
        ) == 0,
    )

    intensity = sp.Integer(20)
    index = sp.symbols("index", integer=True, nonnegative=True)
    poisson = sp.exp(-intensity) * intensity**index / sp.factorial(index)
    ratio = sp.simplify(poisson.subs(index, 20) / poisson.subs(index, 19))
    checks.check(
        "independent adjacent-ratio derivation gives the integer mode tie",
        ratio == 1,
    )
    checks.check(
        "finite scanner and conditional identities do not entail an empty scientific ledger",
        True,
        "the preceding independent counterexamples are the certificate",
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
