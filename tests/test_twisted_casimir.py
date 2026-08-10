"""Two-route verification of twisted-torus one-loop energetics (issue #26).

Route 1: functional-equation evaluation of the Epstein zeta and its
derivative at s = -1.  Route 2: direct Gaussian-regulated mode sums with
regulator refinement.  SymPy exact algebra covers the preprint's classical
transition-function claims and the Sec. 7 coefficient matching.
"""

from __future__ import annotations

import numpy as np
import pytest
import sympy as sp
from mpmath import mp, mpf

from substrate_framework.twisted_casimir import (
    CORRECTED_DELTA_V_COEFFICIENT,
    PREPRINT_DELTA_V_COEFFICIENT,
    TORON_ADJOINT_TWISTS,
    adjoint_twists,
    analytic_twist_spectrum,
    dirichlet_beta,
    dual_s_sum,
    epstein_square,
    epstein_square_derivative_minus_one,
    epstein_square_value_minus_one,
    higgs_quartic_from_gap_ansatz,
    lattice_adjoint_transverse_spectrum,
    matrix_commutant_basis,
    one_loop_density_scalar,
    regulated_mode_sum_difference,
    transition_matrices,
    vacuum_energy_difference,
    wilson_loop_commutator,
)

mp.dps = 30
CATALAN = mpf("0.915965594177219015054603514932384110774")


# ---------------------------------------------------------------------------
# exact symbolic algebra (preprint Secs. 3, 4, 6, 7)
# ---------------------------------------------------------------------------


def test_transition_matrices_are_su2_and_anticommute() -> None:
    p, q = transition_matrices()
    identity = sp.eye(2)
    assert sp.simplify(p * p.H) == identity
    assert sp.simplify(q * q.H) == identity
    assert sp.simplify(p.det()) == 1
    assert sp.simplify(q.det()) == 1
    assert sp.simplify(p * q + q * p) == sp.zeros(2)


def test_wilson_loop_commutator_is_minus_identity() -> None:
    assert wilson_loop_commutator() == -sp.eye(2)


def test_centralizer_of_transition_matrices_is_center_not_u1em() -> None:
    p, q = transition_matrices()
    basis = matrix_commutant_basis([p, q])
    assert len(basis) == 1
    (generator,) = basis
    ratio = sp.simplify(generator[0, 0] / generator[1, 1])
    assert ratio == 1
    assert sp.simplify(generator[0, 1]) == 0
    assert sp.simplify(generator[1, 0]) == 0
    # unitary + det 1 multiples of I are exactly +-I: stabilizer is Z2,
    # refuting the preprint's U(1)_em stabilizer (Eq. 66).


def test_u1em_generator_does_not_stabilize_q() -> None:
    from substrate_framework.su2_doublets import su2_fundamental_ledger

    t3 = su2_fundamental_ledger().generators[2]
    _, q = transition_matrices()
    assert sp.simplify(t3 * q - q * t3) != sp.zeros(2)


def test_commutant_basis_actually_commutes_for_generic_input() -> None:
    # Regression for the row-major reshape defect found in review: with a
    # non-transpose-invariant input, every returned basis element MUST
    # commute with the input exactly. The nilpotent Jordan block has
    # commutant span{I, M} (dimension 2).
    nilpotent = sp.Matrix([[0, 1], [0, 0]])
    basis = matrix_commutant_basis([nilpotent])
    assert len(basis) == 2
    for element in basis:
        assert sp.simplify(element * nilpotent - nilpotent * element) == sp.zeros(2)
    # A diagonalizable matrix with distinct eigenvalues: commutant is the
    # diagonal algebra (dimension 2).
    diagonal = sp.diag(1, 2)
    basis_diag = matrix_commutant_basis([diagonal])
    assert len(basis_diag) == 2
    for element in basis_diag:
        assert sp.simplify(element * diagonal - diagonal * element) == sp.zeros(2)
    # Combined generic pair: commutant of {nilpotent, diagonal} is scalars.
    both = matrix_commutant_basis([nilpotent, diagonal])
    assert len(both) == 1
    (scalar,) = both
    assert sp.simplify(scalar[0, 0] - scalar[1, 1]) == 0
    assert sp.simplify(scalar[0, 1]) == 0
    assert sp.simplify(scalar[1, 0]) == 0


def test_adjoint_twists_match_preprint() -> None:
    assert set(adjoint_twists()) == {
        (sp.Rational(1, 2), sp.Rational(0)),
        (sp.Rational(0), sp.Rational(1, 2)),
        (sp.Rational(1, 2), sp.Rational(1, 2)),
    }


def test_numerator_parity_identity() -> None:
    for m1_parity in (0, 1):
        for m2_parity in (0, 1):
            value = (
                3
                - (-1) ** m1_parity
                - (-1) ** m2_parity
                - (-1) ** (m1_parity + m2_parity)
            )
            expected = 0 if (m1_parity, m2_parity) == (0, 0) else 4
            assert value == expected


def test_higgs_quartic_sign_inconsistency() -> None:
    match = higgs_quartic_from_gap_ansatz()
    c, g = sp.symbols("c g", positive=True)
    assert sp.simplify(match["mu2_eff"] - c * g**2 * sp.Symbol("mu0", positive=True) ** 2) == 0
    # the gap ansatz yields a NEGATIVE quartic...
    assert match["lambda_eff"].is_negative is True
    # ... which is neither equal nor opposite-equal to the asserted Eq. (83)
    assert sp.simplify(match["lambda_eff"] - match["preprint_lambda_eff"]) != 0
    assert sp.simplify(match["lambda_eff"] + match["preprint_lambda_eff"]) != 0


# ---------------------------------------------------------------------------
# special values and [T-A]: E2(-1; alpha) = 0
# ---------------------------------------------------------------------------


def test_dirichlet_beta_minus_one_vanishes() -> None:
    assert abs(dirichlet_beta(-1)) < mpf(10) ** -25


def test_s_sum_periodic_matches_exact_factorization() -> None:
    exact = 4 * mp.zeta(2) * dirichlet_beta(2)
    assert abs(dual_s_sum((0, 0)) - exact) < mpf(10) ** -20
    assert abs(exact - 2 * mp.pi**2 * CATALAN / 3) < mpf(10) ** -25


def test_s_sum_twist_combination() -> None:
    total = sum(dual_s_sum(alpha) for alpha in TORON_ADJOINT_TWISTS)
    assert abs(total + mpf(3) / 4 * dual_s_sum((0, 0))) < mpf(10) ** -20


def test_epstein_at_minus_one_vanishes_everywhere() -> None:
    # [T-A]; the preprint's Eq. (46) claims E2(-1; alpha) = -S(alpha)/(4 pi^2)
    # (Eq. (47) is the definition of S(alpha)).
    for alpha in list(TORON_ADJOINT_TWISTS) + [(0.3, 0.7), (0.0, 0.0)]:
        assert abs(epstein_square_value_minus_one(alpha)) < mpf(10) ** -30


def test_preprint_eq46_is_refuted() -> None:
    # sensitivity: the preprint's claimed value is measurably nonzero, so the
    # vanishing above is not a trivially-passing predicate.
    claimed = -dual_s_sum((0.5, 0.0)) / (4 * mp.pi**2)
    assert abs(claimed) > mpf(10) ** -2


def test_dirichlet_beta_prime_identity_numeric_evidence() -> None:
    assert abs(mp.diff(dirichlet_beta, -1) - 2 * CATALAN / mp.pi) < mpf(10) ** -25


def test_epstein_derivative_formula_cross_check() -> None:
    # [T-B] per-pair: V1(alpha) - V1(0) = -(pi/(2 L^4)) D_pair with D_pair the
    # regulated lambda ln lambda difference; compare against direct mode sums.
    for alpha in [(0.5, 0.0), (0.3, 0.7)]:
        route1 = one_loop_density_scalar(alpha) - one_loop_density_scalar((0, 0))
        d_pair = regulated_mode_sum_difference([alpha], 900)
        route2 = -(mp.pi / 2) * mpf(d_pair)
        assert abs(route1 - route2) < mpf("5e-3") * abs(route1)


def test_periodic_casimir_density_is_negative() -> None:
    value = one_loop_density_scalar((0, 0))
    assert value < 0
    # V1(0) = (pi/2) E2'(-1;0) = -pi beta'(-1)/6 = -G/3
    assert abs(value + CATALAN / 3) < mpf(10) ** -30


def test_antiperiodic_twist_raises_energy() -> None:
    assert one_loop_density_scalar((0.5, 0.0)) > one_loop_density_scalar((0, 0))


# ---------------------------------------------------------------------------
# route agreement and the corrected DeltaV
# ---------------------------------------------------------------------------


def test_route1_closed_form_gauge_difference() -> None:
    delta_v = vacuum_energy_difference(TORON_ADJOINT_TWISTS)
    closed = mpf(str(CORRECTED_DELTA_V_COEFFICIENT.evalf(40)))
    assert abs(delta_v - closed) < mpf(10) ** -20
    assert delta_v > 0


def test_route2_regulated_sum_converges_to_route1() -> None:
    # DeltaV = -(pi/L^4) D for two polarizations; refine the regulator.
    target = -5 * CATALAN / (2 * mp.pi)
    residuals = []
    for regulator in (100, 400, 900):
        d_value = regulated_mode_sum_difference(TORON_ADJOINT_TWISTS, regulator)
        residuals.append(abs(mpf(d_value) - target))
    assert residuals[-1] < residuals[0]  # refinement improves the match
    assert residuals[-1] < mpf("2e-3")


def test_preprint_coefficient_is_refuted_by_both_routes() -> None:
    preprint = mpf(str(PREPRINT_DELTA_V_COEFFICIENT.evalf(40)))
    route1 = vacuum_energy_difference(TORON_ADJOINT_TWISTS)
    assert route1 * preprint < 0  # opposite signs
    assert abs(route1 - preprint) > 3  # |+2.29 - (-1.80)|
    d900 = regulated_mode_sum_difference(TORON_ADJOINT_TWISTS, 900)
    route2 = -mp.pi * mpf(d900)
    assert abs(route2 - preprint) > 3


def test_mutation_sensitivity_to_twist_values() -> None:
    mutated = ((0.4, 0.0),)
    baseline = ((0.5, 0.0),)
    route1_mut = vacuum_energy_difference(mutated, polarizations=1)
    route1_base = vacuum_energy_difference(baseline, polarizations=1)
    assert route1_mut != route1_base
    d_mut = regulated_mode_sum_difference(mutated, 900)
    route2_mut = -(mp.pi / 2) * mpf(d_mut)
    assert abs(route1_mut - route2_mut) < mpf("5e-3") * abs(route1_mut)


# ---------------------------------------------------------------------------
# lattice validation of the adjoint spectrum (method check)
# ---------------------------------------------------------------------------


def _merged_analytic_spectrum(twists, max_mode: int = 4) -> np.ndarray:
    return np.sort(
        np.concatenate(
            [analytic_twist_spectrum(alpha, max_mode) for alpha in twists]
        )
    )


def _low_mode_deviation(n_side: int, analytic: np.ndarray, modes: int = 12) -> float:
    spectrum = lattice_adjoint_transverse_spectrum(n_side)
    # compare the lowest nonzero modes (lattice dispersion distorts high modes)
    lattice_low = spectrum[spectrum > 1e-8][:modes]
    analytic_low = analytic[analytic > 1e-8][:modes]
    return float(np.max(np.abs(lattice_low - analytic_low) / analytic_low))


def test_lattice_adjoint_spectrum_validates_method() -> None:
    analytic = _merged_analytic_spectrum(TORON_ADJOINT_TWISTS)
    deviations = [
        _low_mode_deviation(n, analytic) for n in (12, 18, 24)
    ]
    assert deviations[-1] < deviations[0]  # refinement improves
    assert deviations[-1] < 0.02
