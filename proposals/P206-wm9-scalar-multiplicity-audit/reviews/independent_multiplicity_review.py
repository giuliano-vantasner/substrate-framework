#!/usr/bin/env python3
"""Independent raw-SymPy countermodel audit of WM9's multiplicity inference."""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-39/"
    "bridge_WM9_scalar_multiplicity_from_condensate.py"
)


def symbols(expressions: list[sp.Expr]) -> set[sp.Symbol]:
    return set().union(*(expression.free_symbols for expression in expressions))


def main() -> int:
    checks = CheckLedger("P206-INDEPENDENT-MULTIPLICITY")
    amplitude = sp.Symbol("A", real=True)
    coefficients = [sp.Rational(2, 3), sp.Rational(3, 5), sp.Rational(9, 16)]
    one_symbol_overlaps = [coefficient * amplitude for coefficient in coefficients]
    checks.check("fresh shared-amplitude overlaps are pairwise distinct", len(set(one_symbol_overlaps)) == 3)
    checks.check("fresh shared-amplitude overlaps expose one symbol", symbols(one_symbol_overlaps) == {amplitude})

    labels = ("H_1", "H_2", "H_3")
    profiles = {label: one_symbol_overlaps[index] for index, label in enumerate(labels)}
    checks.check("fresh three-label model has three species and one symbol", len(profiles) == 3 and symbols(list(profiles.values())) == {amplitude})

    independent = sp.symbols("A_1:4", real=True)
    before_constraint = [coefficients[index] * independent[index] for index in range(3)]
    after_constraint = [value.subs(dict.fromkeys(independent, amplitude)) for value in before_constraint]
    checks.check("fresh equality constraint preserves three labels", len(labels) == len(after_constraint) == 3)
    checks.check("fresh equality constraint collapses symbol cardinality", len(symbols(before_constraint)) == 3 and symbols(after_constraint) == {amplitude})

    lambdas = sp.symbols("lambda_1:4", real=True)
    single_field_three_modes = [amplitude * lambdas[index] * coefficients[index] for index in range(3)]
    checks.check("fresh one-field mode model exposes four symbols", len(symbols(single_field_three_modes)) == 4)
    checks.check("fresh field count is separately declared from expression symbols", len({"H"}) == 1 and len(symbols(single_field_three_modes)) != 1)

    checks.check("fresh inert species contributes no overlap symbol", len({"H_inert"}) == 1 and symbols([sp.Integer(0)]) == set())
    checks.check("fresh duplicate equal profiles retain distinct labels", len({"H_a": amplitude, "H_b": amplitude}) == 2 and symbols([amplitude, amplitude]) == {amplitude})

    source_tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    assignments = {
        target.id: ast.unparse(node.value)
        for node in source_tree.body
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
    }
    checks.check("fresh AST finds literal three-mode premise", assignments["MODES"] == "(1, 2, 3)")
    checks.check("fresh AST finds symbol-cardinality scalar count", assignments["n_condensates"] == "len(amplitude_symbols)")
    checks.check("fresh AST finds literal mode-cardinality generation count", assignments["n_modes"] == "len(MODES)")

    source_text = SOURCE.read_text(encoding="utf-8")
    checks.check("fresh AST route confirms alternative symbols are source declarations", "A1, A2, A3 = sp.symbols" in source_text and "three_condensate_amplitudes = {A1, A2, A3}" in source_text)
    checks.check("fresh source route supplies no field-action multiplicity parser", not any(isinstance(node, (ast.FunctionDef, ast.ClassDef)) and "multiplicity" in node.name for node in ast.walk(source_tree)))

    own_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"), filename=__file__)
    imports = {
        node.module
        for node in ast.walk(own_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    } | {
        alias.name
        for node in ast.walk(own_tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check("independent review imports no overlap beta or representation API", not any(name.startswith("substrate_framework.normalized_overlaps") or name.startswith("substrate_framework.gauge_") or name.startswith("substrate_framework.multiplet") for name in imports))
    integration_attrs = {node.attr for node in ast.walk(own_tree) if isinstance(node, ast.Attribute) and node.attr in {"trapz", "trapezoid"}}
    checks.check("independent review has no NumPy compatibility surface", "numpy" not in imports and integration_attrs == set())
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
