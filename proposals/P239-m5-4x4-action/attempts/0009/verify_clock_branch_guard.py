"""Verify the Candidate-I clock-active spatial branch guard."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from substrate_framework.m5_covariant_action import (
    MINKOWSKI_MOSTLY_PLUS,
    spectral_clock_branch_guard,
)
from substrate_framework.verification import CheckLedger


HERE = Path(__file__).resolve().parent
ETA = sp.Matrix(MINKOWSKI_MOSTLY_PLUS)


def _rational_lorentz() -> sp.Matrix:
    transformation = sp.eye(4)
    transformation[0, 0] = transformation[1, 1] = sp.Rational(5, 3)
    transformation[0, 1] = transformation[1, 0] = sp.Rational(4, 3)
    return transformation


def main() -> int:
    ledger = CheckLedger("P239/clock-branch-guard")
    director, tangent_left, tangent_right = sp.symbols(
        "lambda_n lambda_theta lambda_phi", real=True
    )
    strength = sp.symbols("zeta", positive=True)
    guard = spectral_clock_branch_guard(
        director, (tangent_left, tangent_right), strength
    )
    ledger.check(
        "tangent-label exchange leaves the guard invariant",
        sp.simplify(
            guard
            - spectral_clock_branch_guard(
                director, (tangent_right, tangent_left), strength
            )
        )
        == 0,
    )
    ledger.check(
        "tangent-degenerate uniaxial family is exactly inactive",
        spectral_clock_branch_guard(director, (tangent_left, tangent_left), strength)
        == 0,
    )
    amplitude = sp.symbols("s", real=True)
    ledger.check(
        "complete pure-director amplitude path is unchanged",
        spectral_clock_branch_guard(amplitude, (0, 0), strength) == 0,
    )
    ledger.check(
        "a real simple clock branch has positive guard energy",
        spectral_clock_branch_guard(
            1, (sp.Rational(1, 4), -sp.Rational(1, 4)), strength
        )
        > 0,
    )

    epsilon = sp.symbols("epsilon", positive=True)
    left_closure = spectral_clock_branch_guard(1 + epsilon, (1, 0), strength)
    right_closure = spectral_clock_branch_guard(1 + epsilon, (0, 1), strength)
    ledger.check(
        "first clock-active director gap closure diverges",
        sp.limit(left_closure, epsilon, 0, dir="+") == sp.oo,
    )
    ledger.check(
        "second clock-active director gap closure diverges",
        sp.limit(right_closure, epsilon, 0, dir="+") == sp.oo,
    )

    g_value = sp.symbols("g", real=True)
    mixed = sp.diag(g_value, director, tangent_left, tangent_right)
    order_parameter = ETA * mixed
    transformation = _rational_lorentz()
    inverse = transformation.inv()
    transformed_order_parameter = inverse.T * order_parameter * inverse
    transformed_mixed = ETA.inv() * transformed_order_parameter
    ledger.check(
        "mixed-tensor spectrum is Lorentz invariant",
        sp.simplify(transformed_mixed.charpoly().as_expr() - mixed.charpoly().as_expr())
        == 0,
    )
    transformed_eigenvalues = tuple(transformed_mixed.eigenvals().keys())
    ledger.check(
        "guard inputs are the invariant spectral branches",
        set(transformed_eigenvalues)
        == {g_value, director, tangent_left, tangent_right},
    )

    finite_mutation = strength * (tangent_left - tangent_right) ** 4
    ledger.check(
        "deleting the denominator leaves permutation closure finite",
        finite_mutation.subs({tangent_left: 1, tangent_right: 0}) == strength,
    )
    zero_strength_mutation = guard.subs(strength, 0)
    ledger.check(
        "deleting the guard restores the open branch boundary",
        zero_strength_mutation == 0,
    )

    result = {
        "campaign": "P239",
        "attempt": "0009",
        "candidate": "I_clock_branch_guard",
        "term": (
            "zeta*(lambda_theta-lambda_phi)^4/"
            "((lambda_n-lambda_theta)^2*(lambda_n-lambda_phi)^2)"
        ),
        "domain": (
            "zeta>0 and the selected director eigenvalue is simple whenever "
            "the tangent plane is clock-biaxial"
        ),
        "verdict": (
            "The guard is a positive Lorentz-spectral scalar, is exactly zero "
            "on every uniaxial M5.17 director/amplitude field, and excludes "
            "both clock-active eigenvalue-permutation boundaries."
        ),
        "scope": (
            "This establishes the guard's structural fit only. A relaxed "
            "finite-gap Candidate-I hedgehog is still required."
        ),
        "check_count": len(ledger.passed),
    }
    (HERE / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
