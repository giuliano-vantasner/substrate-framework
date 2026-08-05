#!/usr/bin/env python3
"""Independent direct-coupling audit of WM10's nonconcurrent boundary solve."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import root

from substrate_framework.verification import CheckLedger


SOURCE = Path("/home/dan/substrate/merged-framework/bridges/phase-39/bridge_WM10_corrected_boundary_two_loop.py")
FREEZE = Path(__file__).resolve().parents[1] / "evidence/formula-freeze.yaml"
SOURCE_SHA256 = "a813f32841a4809f0ca301d8f01cb432d07d43c6bc46433970c1dcf60afe8d29"
FREEZE_SHA256 = "fca66fa2373f3d962ade6bbe0ef0f3583ce92fe6c697e27a94e973ad7571e81b"


def main() -> int:
    checks = CheckLedger("P207-INDEPENDENT-DIRECT-BOUNDARY")
    source_bytes = SOURCE.read_bytes()
    tree = ast.parse(source_bytes.decode("utf-8"), filename=str(SOURCE))
    checks.check("fresh source hash remains pinned", hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256)
    checks.check("fresh formula freeze remains pinned", hashlib.sha256(FREEZE.read_bytes()).hexdigest() == FREEZE_SHA256)
    checks.check("fresh AST finds seven source predicates", sum(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "check" for node in ast.walk(tree)) == 7)

    b = np.array([4.1, -19.0 / 6.0, -7.0])
    matrix = np.array([[199.0 / 50.0, 27.0 / 10.0, 44.0 / 5.0], [9.0 / 10.0, 35.0 / 6.0, 12.0], [11.0 / 10.0, 9.0 / 2.0, -26.0]])
    base_boundary = np.array([4.0, 4.0, 4.0])
    corrected_boundary = np.array([4.1, 25.0 / 6.0, 4.0])
    constraints = np.array([[0.0, 0.0, 1.0], [5.0 / 3.0, 1.0, 0.0]])
    targets = np.array([500.0 / 59.0, 1279.0 / 10.0])
    loop = 16.0 * np.pi**2

    def integrate(log_parameters: np.ndarray, boundary: np.ndarray, matrix_scale: float, method: str):
        amplitude, span = np.exp(log_parameters)
        initial_inverse = amplitude * boundary
        initial_g = np.sqrt(4.0 * np.pi / initial_inverse)

        def rhs(_u: float, coupling: np.ndarray) -> np.ndarray:
            if np.any(coupling <= 0.0):
                raise RuntimeError("direct couplings left the positive domain")
            return -(b * coupling**3 / loop + matrix_scale * coupling**3 * (matrix @ coupling**2) / loop**2)

        result = solve_ivp(rhs, (0.0, span), initial_g, method=method, rtol=1e-11, atol=1e-13, t_eval=np.linspace(0.0, span, 301))
        if not result.success or np.any(result.y <= 0.0):
            raise RuntimeError(result.message)
        low_inverse = 4.0 * np.pi / result.y[:, -1] ** 2
        return result, low_inverse

    def solve(boundary: np.ndarray, matrix_scale: float, method: str, guess=(10.1, 28.5), current_targets=targets):
        def residual(log_parameters: np.ndarray) -> np.ndarray:
            _result, low_inverse = integrate(log_parameters, boundary, matrix_scale, method)
            return (constraints @ low_inverse - current_targets) / current_targets

        root_result = root(residual, np.log(guess), method="hybr", tol=1e-10)
        if not root_result.success:
            raise RuntimeError(root_result.message)
        integration, low_inverse = integrate(root_result.x, boundary, matrix_scale, method)
        raw_residual = constraints @ low_inverse - current_targets
        return np.exp(root_result.x), low_inverse, low_inverse[1] / targets[1], integration, raw_residual

    exact_a = sp.Rational(1639681, 590) / 275
    exact_q = -sp.Rational(2, 295) * (1250 - 186383) / 275
    exact_readout = sp.Rational(19) * (91299 + 1325644) / (sp.Rational(452766) * 275)
    one_parameters, _one_low, one_readout, one_integration, one_residual = solve(corrected_boundary, 0, "Radau")
    checks.check("fresh direct-g Radau route reproduces corrected-boundary exact amplitude and span", abs(one_parameters[0] - float(exact_a)) < 2e-8 and abs(one_parameters[1] - float(2 * sp.pi * exact_q)) < 2e-8)
    checks.check("fresh direct-g one-loop readout and constraints match exact values", abs(one_readout - float(exact_readout)) < 2e-10 and np.max(np.abs(one_residual)) < 1e-8 and np.min(one_integration.y) > 0)

    parameters, low, readout, integration, residual = solve(corrected_boundary, 1, "Radau")
    checks.check("fresh direct-g combined solve closes status residual and positivity", np.max(np.abs(residual)) < 1e-8 and np.min(integration.y) > 0 and integration.nfev > 0)
    checks.check("fresh direct-g combined output reproduces conditional WM10 value", abs(readout - 0.2192066478076030) < 3e-9 and abs(91.1876 * np.exp(parameters[1]) - 1.61833158457e14) / 1.61833158457e14 < 3e-8)

    rk_parameters, rk_low, rk_readout, rk_integration, rk_residual = solve(corrected_boundary, 1, "DOP853", guess=(11.0, 30.0))
    checks.check("fresh direct-g Radau and DOP853 routes agree", abs(rk_readout - readout) < 3e-9 and np.max(np.abs(rk_low - low)) < 3e-7 and np.max(np.abs(rk_residual)) < 1e-8 and rk_integration.nfev > 0 and abs(rk_parameters[1] - parameters[1]) < 2e-7)

    base_parameters, _base_low, base_readout, _base_integration, base_residual = solve(base_boundary, 0, "Radau", guess=(10.4, 29.6))
    matrix_parameters, _matrix_low, matrix_readout, _matrix_integration, matrix_residual = solve(base_boundary, 1, "Radau", guess=(10.4, 29.2))
    checks.check("fresh equal-boundary axes reproduce base and matrix corners", abs(base_readout - 0.2075735012801249) < 3e-9 and abs(matrix_readout - 0.2106411357493541) < 3e-9 and np.max(np.abs(base_residual)) < 1e-8 and np.max(np.abs(matrix_residual)) < 1e-8 and base_parameters[0] > 0 and matrix_parameters[0] > 0)
    cross_term = readout - one_readout - matrix_readout + base_readout
    checks.check("fresh four-corner interaction is negative and nonzero", abs(cross_term + 8.2787754902e-5) < 3e-9 and cross_term < 0)

    _sign_parameters, sign_low, sign_readout, _sign_integration, sign_residual = solve(corrected_boundary, -1, "Radau")
    checks.check("fresh sign mutation changes the readout while retaining a solved problem", abs(sign_readout - readout) > 1e-3 and np.max(np.abs(sign_residual)) < 1e-8 and np.min(sign_low) > 0)
    changed_targets = targets + np.array([1.0, 0.0])
    _target_parameters, _target_low, target_readout, _target_integration, target_residual = solve(corrected_boundary, 1, "Radau", current_targets=changed_targets)
    checks.check("fresh supplied-target mutation changes the readout", abs(target_readout - readout) > 1e-4 and np.max(np.abs(target_residual)) < 1e-8)
    checks.check("fresh independent matching offset changes reported coordinate", abs((low[1] + 1.0) / targets[1] - readout) > 0.007)

    own_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"), filename=__file__)
    imports = {node.module for node in ast.walk(own_tree) if isinstance(node, ast.ImportFrom) and node.module is not None} | {alias.name for node in ast.walk(own_tree) if isinstance(node, ast.Import) for alias in node.names}
    checks.check("independent review imports no preferred beta or running API", not any(name.startswith("substrate_framework.gauge_") for name in imports))
    integration_attrs = {node.attr for node in ast.walk(own_tree) if isinstance(node, ast.Attribute) and node.attr in {"trapz", "trapezoid"}}
    checks.check("independent review has no NumPy quadrature compatibility surface", integration_attrs == set())
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
