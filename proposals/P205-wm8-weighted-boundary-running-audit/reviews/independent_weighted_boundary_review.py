#!/usr/bin/env python3
"""Independent raw-SymPy rederivation of WM8's weighted boundary solve."""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path("/home/dan/substrate/merged-framework/bridges/phase-39/bridge_WM8_corrected_boundary_running.py")
R = sp.Rational


def solve_raw(boundary: sp.Matrix, beta: sp.Matrix, offsets: sp.Matrix | None = None):
    C = sp.Matrix([[0, 0, 1], [R(5, 3), 1, 0]])
    d = sp.Matrix([R(500, 59), R(1279, 10)])
    z = sp.zeros(3, 1) if offsets is None else offsets
    design = sp.Matrix.hstack(C * boundary, C * beta)
    parameters = sp.simplify(design.inv() * (d - C * z))
    low = sp.simplify(parameters[0] * boundary + parameters[1] * beta + z)
    return design, parameters, low, sp.factor(low[1] / R(1279, 10))


def main() -> int:
    checks = CheckLedger("P205-INDEPENDENT-WEIGHTED-BOUNDARY")
    n = sp.Symbol("N_H", real=True)
    boundary = sp.Matrix([4 + n / 10, 4 + n / 6, 4])
    fixed_beta = sp.Matrix([R(41, 10), -R(19, 6), -7])
    design, parameters, low, readout = solve_raw(boundary, fixed_beta)
    checks.check("fresh design determinant is seven N plus 268 over three", sp.simplify(design.det() - (7 * n + 268) / 3) == 0)
    checks.check("fresh boundary amplitude is exact", sp.simplify(parameters[0] - R(1639681, 590) / (7 * n + 268)) == 0)
    checks.check("fresh scaled span is exact", sp.simplify(parameters[1] + R(2, 295) * (1250 * n - 186383) / (7 * n + 268)) == 0)
    checks.check("fresh low constraints backsubstitute identically", low[2] == R(500, 59) and sp.simplify(R(5, 3) * low[0] + low[1] - R(1279, 10)) == 0)
    checks.check("fresh fixed-running readout is exact", sp.simplify(readout - 19 * (91299 * n + 1325644) / (452766 * (7 * n + 268))) == 0)
    checks.check("fresh fixed-running derivative is positive on its domain", sp.simplify(sp.diff(readout, n) - R(144291928, 226383) / (7 * n + 268) ** 2) == 0)
    checks.check("fresh N zero one and three values reproduce source arithmetic", all(abs(float(readout.subs(n, k)) - expected) < 1e-12 for k, expected in [(0, 0.207573501280), (1, 0.216221801107), (3, 0.232261554419)]))

    coherent_beta = sp.Matrix([4 + n / 10, -R(10, 3) + n / 6, -7])
    coherent_design, coherent_parameters, coherent_low, coherent_readout = solve_raw(boundary, coherent_beta)
    checks.check("fresh coherent determinant is eleven N plus 264 over three", sp.simplify(coherent_design.det() - 11 * (n + 24) / 3) == 0)
    checks.check("fresh coherent constraints backsubstitute identically", coherent_low[2] == R(500, 59) and sp.simplify(R(5, 3) * coherent_low[0] + coherent_low[1] - R(1279, 10)) == 0)
    checks.check("fresh coherent readout is exact", sp.simplify(coherent_readout - (236383 * n + 2211064) / (452766 * (n + 24))) == 0)
    checks.check("fresh coherent derivative is positive on its domain", sp.simplify(sp.diff(coherent_readout, n) - R(1731064, 226383) / (n + 24) ** 2) == 0)
    checks.check("fresh coherent and source paths agree only at one scalar among sampled counts", [sp.simplify(coherent_readout.subs(n, k) - readout.subs(n, k)) == 0 for k in range(4)] == [False, True, False, False])
    checks.check("fresh coherent three-scalar value is not the source near-hit", abs(float(coherent_readout.subs(n, 3)) - 0.238878442809) < 1e-12)

    _, _, _, offset_readout = solve_raw(sp.Matrix(boundary.subs(n, 1)), fixed_beta, sp.Matrix([0, 1, 0]))
    checks.check("fresh matching offset changes the selected readout", offset_readout != readout.subs(n, 1))
    target_shift = R(1, 10)
    shifted_d = sp.Matrix([R(500, 59), R(1279, 10) + target_shift])
    shifted_parameters = design.subs(n, 1).inv() * shifted_d
    shifted_low = shifted_parameters[0] * boundary.subs(n, 1) + shifted_parameters[1] * fixed_beta
    checks.check("fresh low-coordinate mutation changes the selected readout", sp.simplify(shifted_low[1] / R(1279, 10) - readout.subs(n, 1)) != 0)

    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    solve_function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "solve_boundary")
    checks.check("fresh AST route finds no comparator name inside solve_boundary", all(not (isinstance(node, ast.Name) and node.id == "SIN2_MEASURED") for node in ast.walk(solve_function)))
    checks.check("fresh AST route finds fixed beta globals inside solve_boundary", {node.id for node in ast.walk(solve_function) if isinstance(node, ast.Name)} >= {"b1", "b2", "b3"})
    own_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"), filename=__file__)
    import_names = {
        node.module
        for node in ast.walk(own_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    } | {
        alias.name
        for node in ast.walk(own_tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check("independent review imports no preferred beta or running API", not any(name.startswith("substrate_framework.gauge_") for name in import_names))
    integration_attrs = {node.attr for node in ast.walk(own_tree) if isinstance(node, ast.Attribute) and node.attr in {"trapz", "trapezoid"}}
    checks.check("independent review has no NumPy compatibility surface", "numpy" not in import_names and integration_attrs == set())
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
