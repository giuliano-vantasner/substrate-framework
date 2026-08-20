"""Verify the conditional local spectral-Cartan M5 action exactly.

This is proposal evidence, not an accepted-claim verifier.  It proves the
action-level statements that can be settled before solving a hedgehog or a
relaxed pair: locality on a simple timelike spectral branch, Lorentz scalar
behavior, a positive Hamiltonian, exact M5.17 recovery, and repair of an
explicit source-admissible negative clock direction.
"""

from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

import sympy as sp

from substrate_framework.m5_covariant_action import (
    MINKOWSKI_MOSTLY_PLUS,
    double_two_form_contraction,
    m5_curvature_from_derivatives,
    spectral_cartan_curvature_scalar,
    spectral_cartan_hamiltonian_density,
    spectral_cartan_inverse_metric,
    spectral_cartan_lagrangian_density,
    spectral_projector_from_eigenvalues,
    spectral_trace_potential,
)
from substrate_framework.verification import CheckLedger


HERE = Path(__file__).resolve().parent
ETA = sp.Matrix(MINKOWSKI_MOSTLY_PLUS)
PAIRS = tuple(combinations(range(4), 2))


def _rational_lorentz() -> sp.Matrix:
    boost = sp.eye(4)
    boost[0, 0] = boost[1, 1] = sp.Rational(5, 3)
    boost[0, 1] = boost[1, 0] = sp.Rational(4, 3)
    rotation = sp.eye(4)
    rotation[2, 2] = rotation[3, 3] = sp.Rational(3, 5)
    rotation[2, 3] = -sp.Rational(4, 5)
    rotation[3, 2] = sp.Rational(4, 5)
    return boost * rotation


def _pair_transform(covector_transform: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        6,
        6,
        lambda new, old: sp.expand(
            covector_transform[PAIRS[old][0], PAIRS[new][0]]
            * covector_transform[PAIRS[old][1], PAIRS[new][1]]
            - covector_transform[PAIRS[old][1], PAIRS[new][0]]
            * covector_transform[PAIRS[old][0], PAIRS[new][1]]
        ),
    )


def _tensor_from_pair_matrix(matrix: sp.Matrix) -> sp.ImmutableDenseNDimArray:
    tensor = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    for row, (mu, nu) in enumerate(PAIRS):
        for column, (internal_a, internal_b) in enumerate(PAIRS):
            value = matrix[row, column]
            tensor[mu, nu, internal_a, internal_b] = value
            tensor[nu, mu, internal_a, internal_b] = -value
            tensor[mu, nu, internal_b, internal_a] = -value
            tensor[nu, mu, internal_b, internal_a] = value
    return sp.ImmutableDenseNDimArray(tensor)


def _transform_curvature(
    curvature: sp.NDimArray, transformation: sp.Matrix
) -> sp.ImmutableDenseNDimArray:
    covector = transformation.inv().T
    pair_transform = _pair_transform(covector)
    pair_matrix = sp.Matrix(
        6,
        6,
        lambda row, column: curvature[
            PAIRS[row][0], PAIRS[row][1], PAIRS[column][0], PAIRS[column][1]
        ],
    )
    return _tensor_from_pair_matrix(pair_transform * pair_matrix * pair_transform.T)


def _clock_curvature(omega: sp.Symbol) -> sp.ImmutableDenseNDimArray:
    velocity = sp.diag(omega, 0, 0, 0)
    gradient = sp.zeros(4)
    gradient[0, 1] = gradient[1, 0] = 1
    return m5_curvature_from_derivatives((velocity, gradient, sp.zeros(4), sp.zeros(4)))


def main():
    ledger = CheckLedger("P239/spectral-Cartan-action")
    transformation = _rational_lorentz()
    covector = transformation.inv().T
    ledger.check(
        "rational transformation preserves mostly-plus eta",
        transformation.T * ETA * transformation == ETA,
    )

    eigenvalues = (
        sp.Integer(4),
        sp.Integer(1),
        sp.Rational(1, 3),
        sp.Integer(0),
    )
    mixed_vacuum = sp.diag(*eigenvalues)
    vacuum = ETA * mixed_vacuum
    projector = spectral_projector_from_eigenvalues(
        mixed_vacuum, eigenvalues[0], eigenvalues
    )
    cartan = spectral_cartan_inverse_metric(vacuum, eigenvalues[0], eigenvalues)
    ledger.check("selected projector is rank one", projector.rank() == 1)
    ledger.check("selected projector is idempotent", projector**2 == projector)
    ledger.check(
        "selected projector is eta self-adjoint", projector.T * ETA == ETA * projector
    )
    ledger.check(
        "selected eigenline is timelike on the g branch",
        (sp.Matrix([1, 0, 0, 0]).T * ETA * sp.Matrix([1, 0, 0, 0]))[0] < 0,
    )
    ledger.check(
        "Cartan inverse metric is Euclidean in the vacuum frame", cartan == sp.eye(4)
    )

    transformed_vacuum = covector * vacuum * covector.T
    transformed_mixed = ETA * transformed_vacuum
    transformed_projector = spectral_projector_from_eigenvalues(
        transformed_mixed, eigenvalues[0], eigenvalues
    )
    transformed_cartan = spectral_cartan_inverse_metric(
        transformed_vacuum, eigenvalues[0], eigenvalues
    )
    ledger.check(
        "spectral projector transforms by similarity",
        sp.simplify(
            transformed_projector - transformation * projector * transformation.inv()
        )
        == sp.zeros(4),
    )
    ledger.check(
        "Cartan inverse metric transforms contravariantly",
        sp.simplify(transformed_cartan - transformation * cartan * transformation.T)
        == sp.zeros(4),
    )
    leading_minors = tuple(
        sp.factor(transformed_cartan[:size, :size].det()) for size in range(1, 5)
    )
    ledger.check(
        "transformed Cartan metric is positive definite by Sylvester",
        all(value > 0 for value in leading_minors),
    )

    generic_pair_matrix = sp.Matrix(
        6,
        6,
        lambda row, column: ((5 * row - 2 * column + row * column) % 7) - 3,
    )
    curvature = _tensor_from_pair_matrix(generic_pair_matrix)
    transformed_curvature = _transform_curvature(curvature, transformation)
    curvature_scalar = spectral_cartan_curvature_scalar(curvature, cartan)
    transformed_scalar = spectral_cartan_curvature_scalar(
        transformed_curvature, transformed_cartan
    )
    fixed_frobenius_mutation = spectral_cartan_curvature_scalar(
        transformed_curvature, sp.eye(4)
    )
    ledger.check(
        "spectral-Cartan curvature density is an exact Lorentz scalar",
        sp.simplify(transformed_scalar - curvature_scalar) == 0,
    )
    ledger.check(
        "fixed Frobenius mutation breaks boost covariance",
        sp.simplify(fixed_frobenius_mutation - curvature_scalar) != 0,
    )

    off_target = ETA * sp.diag(5, 2, sp.Rational(1, 2), -1)
    transformed_off_target = covector * off_target * covector.T
    potential = spectral_trace_potential(off_target, eigenvalues)
    transformed_potential = spectral_trace_potential(
        transformed_off_target, eigenvalues
    )
    ledger.check("spectrum potential is nontrivial off target", potential > 0)
    ledger.check(
        "spectrum potential is an exact Lorentz scalar",
        sp.simplify(transformed_potential - potential) == 0,
    )
    ledger.check(
        "preferred mixed spectrum has zero potential",
        spectral_trace_potential(vacuum, eigenvalues) == 0,
    )

    spatial_matrix = sp.zeros(6)
    for row, column in product((3, 4, 5), repeat=2):
        spatial_matrix[row, column] = row + 2 * column - 7
    spatial_curvature = _tensor_from_pair_matrix(spatial_matrix)
    source_spatial_action = -sp.Rational(1, 2) * double_two_form_contraction(
        spatial_curvature, ETA, ETA
    )
    candidate_spatial_action = spectral_cartan_lagrangian_density(
        spatial_curvature, cartan
    )
    ledger.check(
        "full static 3x3 curvature action is recovered coefficient-exactly",
        candidate_spatial_action == source_spatial_action,
    )

    expected_positive_energy = 2 * sum(value**2 for value in generic_pair_matrix)
    hamiltonian = spectral_cartan_hamiltonian_density(curvature, cartan)
    ledger.check(
        "Hamiltonian is the explicit positive sum of curvature squares",
        hamiltonian == expected_positive_energy,
    )
    ledger.check("generic curvature Hamiltonian is strictly positive", hamiltonian > 0)

    omega = sp.symbols("omega", real=True)
    clock_curvature = _clock_curvature(omega)
    source_clock = -sp.Rational(1, 2) * double_two_form_contraction(
        clock_curvature, ETA, ETA
    )
    candidate_clock = spectral_cartan_lagrangian_density(clock_curvature, cartan)
    source_clock_coefficient = sp.expand(source_clock).coeff(omega, 2)
    candidate_clock_coefficient = sp.expand(candidate_clock).coeff(omega, 2)
    ledger.check("source clock coefficient is negative", source_clock_coefficient < 0)
    ledger.check(
        "candidate clock coefficient is positive", candidate_clock_coefficient > 0
    )
    ledger.check(
        "Cartan contraction exactly reverses this internal clock sign",
        candidate_clock_coefficient == -source_clock_coefficient,
    )

    inertia, angular_momentum, static_energy = sp.symbols("I J E_static", positive=True)
    fixed_j_energy = static_energy + angular_momentum**2 / (4 * inertia)
    frequency = angular_momentum / (2 * inertia)
    ledger.check("fixed-J frequency is finite and nonzero under I,J>0", frequency > 0)
    ledger.check(
        "fixed-J energy derivative returns the angular frequency",
        sp.diff(fixed_j_energy, angular_momentum) == frequency,
    )
    ledger.check(
        "fixed-J energy is strictly convex in angular momentum",
        sp.diff(fixed_j_energy, angular_momentum, 2) > 0,
    )

    result = {
        "campaign": "P239",
        "attempt": "0002",
        "candidate": "E_spectral_cartan",
        "action": (
            "L=-sum_(mu<nu) eta^mumu eta^nunu " "F_munuab F_munucd h^ac h^bd - V_spec"
        ),
        "cartan_inverse_metric": "h^ab=eta^ab-2 P_t^a_c eta^cb",
        "spectral_branch": (
            "P_t is the simple real timelike spectral idempotent of eta^-1 M "
            "continuously connected to the vacuum g eigenline"
        ),
        "hamiltonian": ("H=sum_(mu<nu) F_munuab F_munucd h^ac h^bd + V_spec >= 0"),
        "leading_principal_minors_under_test_boost": [
            str(value) for value in leading_minors
        ],
        "clock_coefficients": {
            "source": str(source_clock_coefficient),
            "spectral_cartan": str(candidate_clock_coefficient),
        },
        "fixed_j_implication": {
            "energy": "E_static+J^2/(4I)",
            "frequency": "J/(2I)",
            "scope": (
                "algebraic consequence for any stationary branch with finite "
                "positive inertia; existence of the relaxed branch is not proved here"
            ),
        },
        "check_count": len(ledger.passed),
    }
    (HERE / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
