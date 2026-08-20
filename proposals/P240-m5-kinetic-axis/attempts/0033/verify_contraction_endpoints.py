"""Exact P240 audit of issue-147's parameter-free contraction endpoints."""

from __future__ import annotations

from itertools import combinations, product
import json
from pathlib import Path

import sympy as sp

from substrate_framework.m5_covariant_action import (
    MINKOWSKI_MOSTLY_PLUS,
    double_two_form_contraction,
    eta_commutator,
    m5_curvature_from_derivatives,
    spectral_cartan_hamiltonian_density,
    spectral_cartan_inverse_metric,
    spectral_cartan_lagrangian_density,
)
from substrate_framework.verification import CheckLedger


HERE = Path(__file__).resolve().parent
ETA = sp.Matrix(MINKOWSKI_MOSTLY_PLUS)
PAIRS = tuple(combinations(range(4), 2))


def tensor_from_pair_matrix(matrix: sp.MatrixBase):
    tensor = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    for row, (a, b) in enumerate(PAIRS):
        for column, (c, d) in enumerate(PAIRS):
            value = matrix[row, column]
            tensor[a, b, c, d] = value
            tensor[b, a, c, d] = -value
            tensor[a, b, d, c] = -value
            tensor[b, a, d, c] = value
    return sp.ImmutableDenseNDimArray(tensor)


def pair_transform(covector: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(
        6,
        6,
        lambda new, old: sp.expand(
            covector[PAIRS[old][0], PAIRS[new][0]]
            * covector[PAIRS[old][1], PAIRS[new][1]]
            - covector[PAIRS[old][1], PAIRS[new][0]]
            * covector[PAIRS[old][0], PAIRS[new][1]]
        ),
    )


def transform_curvature(curvature, transformation: sp.MatrixBase):
    matrix = sp.Matrix(
        6,
        6,
        lambda row, column: curvature[
            PAIRS[row][0], PAIRS[row][1], PAIRS[column][0], PAIRS[column][1]
        ],
    )
    induced = pair_transform(transformation.inv().T)
    return tensor_from_pair_matrix(induced * matrix * induced.T)


def main() -> int:
    ledger = CheckLedger("P240/attempt-0033/contraction-endpoints")

    eigenvalues = (sp.Integer(8), sp.Integer(1), sp.Rational(1, 3), sp.Integer(0))
    mixed_vacuum = sp.diag(*eigenvalues)
    vacuum = ETA * mixed_vacuum
    cartan = spectral_cartan_inverse_metric(vacuum, eigenvalues[0], eigenvalues)
    ledger.check("spectral Cartan metric is Euclidean in the vacuum frame", cartan == sp.eye(4))
    ledger.check("spectral Cartan metric is positive definite in that frame", all(cartan[:n, :n].det() > 0 for n in range(1, 5)))

    boost = sp.eye(4)
    boost[0, 0] = boost[1, 1] = sp.Rational(5, 3)
    boost[0, 1] = boost[1, 0] = sp.Rational(4, 3)
    ledger.check("rational boost preserves mostly-plus eta", boost.T * ETA * boost == ETA)
    covector = boost.inv().T
    boosted_vacuum = covector * vacuum * covector.T
    boosted_cartan = spectral_cartan_inverse_metric(
        boosted_vacuum, eigenvalues[0], eigenvalues
    )
    ledger.check(
        "field-derived Cartan metric transforms contravariantly",
        sp.simplify(boosted_cartan - boost * cartan * boost.T) == sp.zeros(4),
    )
    ledger.check(
        "boosted field-derived Cartan metric remains positive definite",
        all(sp.factor(boosted_cartan[:n, :n].det()) > 0 for n in range(1, 5)),
    )

    generic_pair_matrix = sp.Matrix(
        6,
        6,
        lambda row, column: ((7 * row - 3 * column + 2 * row * column) % 11) - 5,
    )
    generic_curvature = tensor_from_pair_matrix(generic_pair_matrix)
    boosted_curvature = transform_curvature(generic_curvature, boost)
    rest_density = spectral_cartan_lagrangian_density(generic_curvature, cartan)
    covariant_density = spectral_cartan_lagrangian_density(
        boosted_curvature, boosted_cartan
    )
    fixed_frobenius_density = spectral_cartan_lagrangian_density(
        boosted_curvature, sp.eye(4)
    )
    ledger.check("spectral-Cartan endpoint is an exact Lorentz scalar", sp.simplify(covariant_density - rest_density) == 0)
    ledger.check("fixed-Frobenius endpoint fails the exact boost mutation", sp.simplify(fixed_frobenius_density - rest_density) != 0)

    spatial_symbols = sp.symbols("s0:9")
    spatial_matrix = sp.zeros(6)
    offset = 0
    for row, column in product((3, 4, 5), repeat=2):
        spatial_matrix[row, column] = spatial_symbols[offset]
        offset += 1
    spatial_curvature = tensor_from_pair_matrix(spatial_matrix)
    baseline_spatial = -sp.Rational(1, 2) * double_two_form_contraction(
        spatial_curvature, ETA, ETA
    )
    frobenius_spatial = spectral_cartan_lagrangian_density(
        spatial_curvature, sp.eye(4)
    )
    cartan_spatial = spectral_cartan_lagrangian_density(spatial_curvature, cartan)
    ledger.check("fixed Frobenius recovers the arbitrary static 3x3 action identically", sp.expand(frobenius_spatial - baseline_spatial) == 0)
    ledger.check("spectral Cartan recovers the arbitrary static 3x3 action identically", sp.expand(cartan_spatial - baseline_spatial) == 0)

    positive_hamiltonian = spectral_cartan_hamiltonian_density(
        generic_curvature, cartan
    )
    expected_hamiltonian = 2 * sum(value**2 for value in generic_pair_matrix)
    ledger.check("Cartan Hamiltonian is the explicit positive curvature-square sum", sp.expand(positive_hamiltonian - expected_hamiltonian) == 0)
    ledger.check("nonzero generic curvature has strictly positive Cartan Hamiltonian", positive_hamiltonian > 0)

    omega = sp.symbols("omega", real=True)
    clock_derivatives = [sp.diag(omega, 0, 0, 0), sp.zeros(4), sp.zeros(4), sp.zeros(4)]
    clock_derivatives[1][0, 1] = clock_derivatives[1][1, 0] = 1
    clock_curvature = m5_curvature_from_derivatives(tuple(clock_derivatives))
    baseline_clock = -sp.Rational(1, 2) * double_two_form_contraction(
        clock_curvature, ETA, ETA
    )
    cartan_clock = spectral_cartan_lagrangian_density(clock_curvature, cartan)
    ledger.check("baseline clock kinetic coefficient is negative", sp.expand(baseline_clock).coeff(omega, 2) < 0)
    ledger.check("spectral-Cartan clock kinetic coefficient is positive", sp.expand(cartan_clock).coeff(omega, 2) > 0)
    ledger.check("Cartan endpoint reverses the affine clock sign exactly", sp.expand(cartan_clock + baseline_clock) == 0)

    epsilon = sp.symbols("epsilon", real=True)
    derivative_seeds = (
        sp.Matrix([[1, 2, 0, 1], [2, 0, 1, 0], [0, 1, -1, 2], [1, 0, 2, 3]]),
        sp.Matrix([[0, 1, 1, 2], [1, 2, 0, 1], [1, 0, 3, -1], [2, 1, -1, 0]]),
        sp.Matrix([[2, 0, 1, 0], [0, 1, 2, 1], [1, 2, 0, 2], [0, 1, 2, -2]]),
        sp.Matrix([[1, -1, 0, 2], [-1, 0, 2, 1], [0, 2, 1, 0], [2, 1, 0, 2]]),
    )
    scaled_curvature = m5_curvature_from_derivatives(
        tuple(epsilon * value for value in derivative_seeds)
    )
    scaled_density = spectral_cartan_lagrangian_density(scaled_curvature, cartan)
    ledger.check("curvature density has no quadratic derivative term about a constant vacuum", sp.diff(scaled_density, epsilon, 2).subs(epsilon, 0) == 0)
    ledger.check("first nonzero derivative-order coefficient is quartic", sp.diff(scaled_density, epsilon, 4).subs(epsilon, 0) != 0)
    ledger.check("the exact scaled density is homogeneous of derivative order four", sp.expand(scaled_density - epsilon**4 * scaled_density.subs(epsilon, 1)) == 0)

    u = sp.symbols("u", real=True)
    orbit_boost = sp.Matrix(
        [
            [sp.cosh(u), sp.sinh(u), 0, 0],
            [sp.sinh(u), sp.cosh(u), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    orbit = orbit_boost * vacuum * orbit_boost.T
    orbit_tangent = sp.diff(orbit, u)
    gradient_coefficients = sp.symbols("u0:4", real=True)
    orbit_derivatives = tuple(value * orbit_tangent for value in gradient_coefficients)
    orbit_curvature = m5_curvature_from_derivatives(orbit_derivatives)
    ledger.check(
        "single-scalar fixed-axis boost orbit has identically zero curvature",
        all(
            orbit_curvature[indices] == 0
            for indices in product(range(4), repeat=4)
        ),
    )
    ledger.check("single-scalar boost orbit has no Cartan gradient density", spectral_cartan_lagrangian_density(orbit_curvature, cartan) == 0)

    momentum, inertia = sp.symbols("J I", positive=True)
    frequency = momentum / (2 * inertia)
    ledger.check("positive finite inertia gives a conditional finite nonzero fixed-J frequency", frequency > 0)
    ledger.check("that frequency statement remains conditional on a stationary finite-inertia field", sp.diff(momentum**2 / (4 * inertia), momentum) == frequency)

    result = {
        "campaign": "P240",
        "attempt": "0033",
        "candidate": "B_contraction_signature_parameter_free_endpoints",
        "fixed_frobenius": {
            "static_3x3_recovery": "exact",
            "hamiltonian": "positive in the preferred frame",
            "symmetry": "SO(3), exact rational boost mutation fails",
            "disposition": "not selected because the spectral-Cartan endpoint supplies the same sign repair covariantly",
        },
        "spectral_cartan": {
            "action": "L=-1/2 F_munuab F_rscd eta^murho eta^nusigma h^ac(M) h^bd(M)-V",
            "internal_metric": "h^ab=eta^ab-2 P_t^a_c eta^cb",
            "static_3x3_recovery": "exact",
            "hamiltonian": "positive on the simple timelike spectral branch",
            "symmetry": "local proper Lorentz scalar",
            "affine_clock_sign": "repaired exactly",
            "constant_vacuum_derivative_order": 4,
            "single_scalar_fixed_axis_boost_curvature": 0,
        },
        "goal_scope": "The spectral-Cartan endpoint is retained as the parameter-free positive covariant base action. By itself it supplies neither a quadratic mass-gradient kernel about a constant vacuum nor any curvature for a single-scalar fixed-axis boost orbit. The conditional formula omega=J/(2I) does not establish a stationary hedgehog. A nonlinear two-clock/textured interaction remains open and is a distinct issue-147 candidate, so no endpoint-only numerical validation is opened here.",
        "verdict": "retain_spectral_cartan_base_continue_to_two_clock_interaction",
        "check_count": len(ledger.passed),
    }
    (HERE / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
