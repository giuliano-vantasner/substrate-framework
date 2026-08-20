"""Verify the local covariant Candidate-J clock-axis lift."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from substrate_framework.m5_covariant_action import (
    MINKOWSKI_MOSTLY_PLUS,
    auxiliary_clock_constraint_density,
    clock_axis_constraint_residuals,
    spacelike_projector_from_vector,
)
from substrate_framework.verification import CheckLedger


HERE = Path(__file__).resolve().parent
ETA = sp.Matrix(MINKOWSKI_MOSTLY_PLUS)


def _rational_lorentz() -> sp.Matrix:
    boost = sp.eye(4)
    boost[0, 0] = boost[1, 1] = sp.Rational(5, 3)
    boost[0, 1] = boost[1, 0] = sp.Rational(4, 3)
    rotation = sp.eye(4)
    rotation[2, 2] = rotation[3, 3] = sp.Rational(3, 5)
    rotation[2, 3] = -sp.Rational(4, 5)
    rotation[3, 2] = sp.Rational(4, 5)
    return boost * rotation


def main() -> int:
    ledger = CheckLedger("P239/auxiliary-clock-axis")
    vector = sp.Matrix([0, 1, 0, 0])
    timelike = sp.diag(1, 0, 0, 0)
    spatial_mixed = sp.diag(0, 1, sp.Rational(1, 3), -sp.Rational(1, 4))
    projector = spacelike_projector_from_vector(vector)
    ledger.check("spacelike axis gives a rank-one projector", sp.trace(projector) == 1)
    ledger.check("spacelike projector is idempotent", projector**2 == projector)
    norm, orthogonality, idempotence, alignment = clock_axis_constraint_residuals(
        vector, timelike, spatial_mixed
    )
    ledger.check("axis has unit spacelike norm", norm == 0)
    ledger.check(
        "axis is orthogonal to the timelike line", orthogonality == sp.zeros(4, 1)
    )
    ledger.check(
        "constraint residual includes exact idempotence", idempotence == sp.zeros(4)
    )
    ledger.check("selected axis is a spatial eigenline", alignment == sp.zeros(4))

    transformation = _rational_lorentz()
    inverse = transformation.inv()
    transformed_vector = transformation * vector
    transformed_timelike = transformation * timelike * inverse
    transformed_spatial = transformation * spatial_mixed * inverse
    transformed_projector = spacelike_projector_from_vector(transformed_vector)
    ledger.check(
        "axis projector transforms by Lorentz similarity",
        sp.simplify(transformed_projector - transformation * projector * inverse)
        == sp.zeros(4),
    )
    transformed_residuals = clock_axis_constraint_residuals(
        transformed_vector, transformed_timelike, transformed_spatial
    )
    ledger.check(
        "all zero constraints remain zero in a boosted frame",
        transformed_residuals[0] == 0
        and transformed_residuals[1] == sp.zeros(4, 1)
        and transformed_residuals[2] == sp.zeros(4)
        and transformed_residuals[3] == sp.zeros(4),
    )

    probe_vector = sp.Matrix([0, 1, 2, -1])
    probe_norm, probe_orthogonality, _, probe_alignment = (
        clock_axis_constraint_residuals(probe_vector, timelike, spatial_mixed)
    )
    scalar_multiplier = sp.Integer(7)
    vector_multiplier = sp.Matrix([2, -1, 3, 4])
    matrix_multiplier = sp.Matrix(
        4, 4, lambda row, column: (2 * row - column + 3) % 5 - 2
    )
    baseline_density = auxiliary_clock_constraint_density(
        probe_norm,
        probe_orthogonality,
        probe_alignment,
        scalar_multiplier,
        vector_multiplier,
        matrix_multiplier,
    )
    transformed_probe = transformation * probe_vector
    transformed_probe_residuals = clock_axis_constraint_residuals(
        transformed_probe, transformed_timelike, transformed_spatial
    )
    transformed_density = auxiliary_clock_constraint_density(
        transformed_probe_residuals[0],
        transformed_probe_residuals[1],
        transformed_probe_residuals[3],
        scalar_multiplier,
        inverse.T * vector_multiplier,
        transformation * matrix_multiplier * inverse,
    )
    ledger.check(
        "local multiplier constraint density is Lorentz scalar",
        sp.simplify(transformed_density - baseline_density) == 0,
    )

    isotropic_spatial = sp.diag(0, 2, 2, 2)
    alternate_axis = sp.Matrix([0, 0, sp.Rational(3, 5), sp.Rational(4, 5)])
    first_isotropic = clock_axis_constraint_residuals(
        vector, timelike, isotropic_spatial
    )
    second_isotropic = clock_axis_constraint_residuals(
        alternate_axis, timelike, isotropic_spatial
    )
    ledger.check(
        "alignment constraint permits continuous axis data through an isotropic melt",
        first_isotropic[-1] == sp.zeros(4) and second_isotropic[-1] == sp.zeros(4),
    )
    ledger.check(
        "M alone cannot select an axis at the isotropic melt",
        vector != alternate_axis
        and spacelike_projector_from_vector(vector)
        != spacelike_projector_from_vector(alternate_axis),
    )

    tangent_value = sp.symbols("lambda_t", real=True)
    spatial_order_parameter = sp.diag(0, 1, tangent_value, tangent_value)
    generator = sp.zeros(4)
    generator[2, 3], generator[3, 2] = -1, 1
    clock_derivative = (
        generator * spatial_order_parameter + spatial_order_parameter * generator.T
    )
    ledger.check(
        "clock derivative vanishes on the uniaxial tangent-degenerate sector",
        clock_derivative == sp.zeros(4),
    )

    result = {
        "campaign": "P239",
        "attempt": "0011",
        "candidate": "J_auxiliary_clock_axis_lift",
        "fields": "M_ab plus constrained unit spacelike clock axis N^a",
        "constraints": [
            "eta(N,N)=1",
            "P_t N=0",
            "P_N^2=P_N",
            "[Y,P_N]=0",
        ],
        "verdict": (
            "The auxiliary eigenframe lift is local, Lorentz covariant, and "
            "parameter-free on shell. It selects the M5.17 director outside "
            "the core, remains continuous when M is isotropic, and contributes "
            "zero clock derivative throughout the tangent-degenerate uniaxial sector."
        ),
        "scope": (
            "This verifies the constrained field space only. The labeled-axis "
            "fixed-J branch must still pass stationarity and refinement."
        ),
        "check_count": len(ledger.passed),
    }
    (HERE / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
