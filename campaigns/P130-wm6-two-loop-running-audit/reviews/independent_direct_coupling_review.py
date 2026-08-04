"""Independent direct-coupling P130 solve without the canonical running API."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import root

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-33/"
    "bridge_WM6_two_loop_running.py"
)
FROZEN = Path(
    "campaigns/P130-wm6-two-loop-running-audit/evidence/frozen-proposal.yaml"
)
SOURCE_SHA = "6d1ea4245adcf490466974d4a40b24843cd92e883c6e885936fb030cd1b31d57"
FREEZE_SHA = "7800f2aed53ad54f436b4d77a1f43fd5b735b0d4a18cab90b6e883ebedfeed97"


def main() -> int:
    checks = CheckLedger("WM6-INDEPENDENT-DIRECT-COUPLING-REVIEW")
    source_bytes = SOURCE.read_bytes()
    source_tree = ast.parse(source_bytes.decode("utf-8"))
    checks.check(
        "independently read source bytes retain their pinned hash",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA,
    )
    checks.check(
        "independently read preregistration remains byte identical",
        hashlib.sha256(FROZEN.read_bytes()).hexdigest() == FREEZE_SHA,
    )
    checks.check(
        "fresh AST walk finds eleven source predicates",
        sum(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            for node in ast.walk(source_tree)
        )
        == 11,
    )

    b = np.array([4.1, -19.0 / 6.0, -7.0])
    matrix = np.array(
        [
            [199.0 / 50.0, 27.0 / 10.0, 44.0 / 5.0],
            [9.0 / 10.0, 35.0 / 6.0, 12.0],
            [11.0 / 10.0, 9.0 / 2.0, -26.0],
        ]
    )
    constraints = np.array([[0.0, 0.0, 1.0], [5.0 / 3.0, 1.0, 0.0]])
    targets = np.array([500.0 / 59.0, 1279.0 / 10.0])
    loop = 16.0 * np.pi**2

    def integrate(log_parameters: np.ndarray, matrix_scale: float, method: str):
        amplitude, span = np.exp(log_parameters)
        initial_inverse = np.full(3, amplitude)
        initial_g = np.sqrt(4.0 * np.pi / initial_inverse)

        def rhs(_downward_log: float, coupling: np.ndarray) -> np.ndarray:
            if np.any(coupling <= 0.0):
                raise RuntimeError("direct couplings left the positive domain")
            return -(
                b * coupling**3 / loop
                + matrix_scale * coupling**3 * (matrix @ coupling**2) / loop**2
            )

        result = solve_ivp(
            rhs,
            (0.0, span),
            initial_g,
            method=method,
            rtol=1.0e-11,
            atol=1.0e-13,
            t_eval=np.linspace(0.0, span, 301),
        )
        if not result.success or np.any(result.y <= 0.0):
            raise RuntimeError(result.message)
        low_inverse = 4.0 * np.pi / result.y[:, -1] ** 2
        return result, low_inverse

    def solve(matrix_scale: float, method: str, guess=(41.0, 29.0)):
        def residual(log_parameters: np.ndarray) -> np.ndarray:
            _result, low_inverse = integrate(log_parameters, matrix_scale, method)
            return (constraints @ low_inverse - targets) / targets

        root_result = root(residual, np.log(guess), method="hybr", tol=1.0e-10)
        if not root_result.success:
            raise RuntimeError(root_result.message)
        integration, low_inverse = integrate(root_result.x, matrix_scale, method)
        raw_residual = constraints @ low_inverse - targets
        return (
            np.exp(root_result.x),
            low_inverse,
            low_inverse[1] / targets[1],
            integration,
            raw_residual,
        )

    exact_a = sp.Rational(1639681, 39530)
    exact_q = sp.Rational(186383, 39530)
    exact_readout = sp.Rational(6296809, 30335322)
    one_parameters, one_low, one_readout, one_integration, one_residual = solve(0, "Radau")
    checks.check(
        "fresh direct-g Radau route reproduces the exact one-loop amplitude and span",
        abs(one_parameters[0] - float(exact_a)) < 2e-8
        and abs(one_parameters[1] - float(2 * sp.pi * exact_q)) < 2e-8,
    )
    checks.check(
        "fresh direct-g one-loop readout and constraints match exactly bounded values",
        abs(one_readout - float(exact_readout)) < 2e-10
        and np.max(np.abs(one_residual)) < 1e-8
        and np.min(one_integration.y) > 0,
    )

    parameters, low, readout, integration, residual = solve(1, "Radau")
    checks.check(
        "fresh direct-g two-loop solve closes root integration and positivity gates",
        np.max(np.abs(residual)) < 1e-8
        and np.min(integration.y) > 0
        and integration.nfev > 0,
    )
    checks.check(
        "fresh direct-g two-loop output reproduces the conditional source specialization",
        abs(readout - 0.210641) < 1e-6
        and abs(np.log10(91.1876 * np.exp(parameters[1])) - 14.616) < 2e-3,
    )
    rk_parameters, rk_low, rk_readout, rk_integration, rk_residual = solve(1, "DOP853", guess=(44, 32))
    checks.check(
        "fresh direct-g Radau and DOP853 routes agree",
        abs(rk_readout - readout) < 2e-9
        and np.max(np.abs(rk_low - low)) < 2e-7
        and np.max(np.abs(rk_residual)) < 1e-8
        and rk_integration.nfev > 0,
    )

    sign_parameters, sign_low, sign_readout, _sign_integration, sign_residual = solve(-1, "Radau")
    checks.check(
        "fresh sign mutant moves the readout while retaining a solved inverse problem",
        abs(sign_readout - readout) > 1e-3
        and np.max(np.abs(sign_residual)) < 1e-8
        and sign_parameters[0] > 0
        and np.min(sign_low) > 0,
    )
    checks.check(
        "the two supplied constraints leave the reported weak coordinate as a third readout",
        np.linalg.matrix_rank(constraints) == 2
        and not np.allclose(constraints[0], [0, 1, 0])
        and not np.allclose(constraints[1], [0, 1, 0]),
    )

    three_loop_tensor = np.eye(3).reshape(-1)
    two_loop_direction = matrix.reshape(-1)
    checks.check(
        "an independent higher-order tensor direction is not a uniform rescaling of B",
        np.linalg.matrix_rank(np.column_stack((two_loop_direction, three_loop_tensor))) == 2,
    )
    checks.check(
        "a finite matching offset can change the readout without changing either beta coefficient array",
        abs((low[1] + 1.0) / targets[1] - readout) > 1.0 / 200.0
        and np.array_equal(b, np.array([4.1, -19.0 / 6.0, -7.0]))
        and matrix[0, 0] == 199.0 / 50.0,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
