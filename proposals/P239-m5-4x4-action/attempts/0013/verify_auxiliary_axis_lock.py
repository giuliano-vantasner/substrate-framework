"""Verify the Candidate-K auxiliary clock-axis lock potential."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from substrate_framework.m5_covariant_action import (
    MINKOWSKI_MOSTLY_PLUS,
    auxiliary_clock_axis_lock_potential,
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
    ledger = CheckLedger("P239/auxiliary-axis-lock")
    director, tangent_left, tangent_right = sp.symbols(
        "lambda_n lambda_theta lambda_phi", real=True
    )
    strength = sp.symbols("zeta", positive=True)
    spatial = sp.diag(0, director, tangent_left, tangent_right)
    axis_projector = sp.diag(0, 1, 0, 0)
    lock = auxiliary_clock_axis_lock_potential(spatial, axis_projector, strength)
    ledger.check(
        "aligned lock is the tangent squared amplitude",
        sp.simplify(lock - strength * (tangent_left**2 + tangent_right**2)) == 0,
    )
    ledger.check(
        "aligned lock is nonnegative",
        auxiliary_clock_axis_lock_potential(
            sp.diag(0, 1, sp.Rational(1, 3), -sp.Rational(1, 4)),
            axis_projector,
            strength,
        )
        > 0,
    )
    amplitude = sp.symbols("s", real=True)
    ledger.check(
        "every aligned pure-director amplitude is unchanged",
        auxiliary_clock_axis_lock_potential(
            sp.diag(0, amplitude, 0, 0), axis_projector, strength
        )
        == 0,
    )
    ledger.check(
        "the isotropic melt remains allowed",
        auxiliary_clock_axis_lock_potential(sp.zeros(4), axis_projector, strength) == 0,
    )
    ledger.check(
        "first permuted uniaxial vacuum has positive cost",
        auxiliary_clock_axis_lock_potential(
            sp.diag(0, 0, 1, 0), axis_projector, strength
        )
        == strength,
    )
    ledger.check(
        "second permuted uniaxial vacuum has positive cost",
        auxiliary_clock_axis_lock_potential(
            sp.diag(0, 0, 0, 1), axis_projector, strength
        )
        == strength,
    )

    transformation = _rational_lorentz()
    inverse = transformation.inv()
    transformed_spatial = transformation * spatial * inverse
    transformed_axis = transformation * axis_projector * inverse
    ledger.check(
        "axis-lock potential is a Lorentz scalar",
        sp.simplify(
            auxiliary_clock_axis_lock_potential(
                transformed_spatial, transformed_axis, strength
            )
            - lock
        )
        == 0,
    )
    trace_only_mutation = strength * sp.trace(spatial**2)
    ledger.check(
        "deleting P_N destroys aligned-uniaxial inactivity",
        trace_only_mutation.subs(
            {director: amplitude, tangent_left: 0, tangent_right: 0}
        )
        == strength * amplitude**2,
    )

    result = {
        "campaign": "P239",
        "attempt": "0013",
        "candidate": "K_auxiliary_axis_lock",
        "term": "zeta*(Tr(Y^2)-Tr(P_N Y)^2)",
        "constrained_form": "zeta*(lambda_theta^2+lambda_phi^2)",
        "verdict": (
            "The axis lock is a positive Lorentz scalar on the Candidate-J "
            "constraint surface. It is exactly zero for every aligned M5.17 "
            "pure-director amplitude and positive for both permuted uniaxial vacua."
        ),
        "scope": "A stationary Candidate-K branch remains required.",
        "check_count": len(ledger.passed),
    }
    (HERE / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
