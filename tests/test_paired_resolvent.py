from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.paired_resolvent import (
    asymmetric_pair_resolvent,
    equal_pair_resolvent_sum,
    finite_resolvent_effective_block,
    symmetric_pair_loss_ledger,
    symmetric_pair_resolvent,
)


def test_symmetric_pair_general_and_zero_energy_forms() -> None:
    delta, gamma, product, energy = sp.symbols("Delta Gamma c E", positive=True)
    general = symmetric_pair_resolvent(
        delta,
        gamma,
        product,
        spectral_energy=energy,
    )
    expected_general = 2 * product * (energy + sp.I * gamma / 2) / (
        (energy + sp.I * gamma / 2) ** 2 - delta**2
    )
    assert sp.simplify(general - expected_general) == 0
    assert sp.simplify(
        symmetric_pair_resolvent(delta, gamma, product)
        + sp.I * product * gamma / (delta**2 + gamma**2 / 4)
    ) == 0


def test_zero_loss_cancellation_requires_zero_spectral_energy() -> None:
    delta, product, energy = sp.symbols("Delta c E", positive=True)
    assert symmetric_pair_resolvent(delta, 0, product) == 0
    off_shell = symmetric_pair_resolvent(
        delta,
        0,
        product,
        spectral_energy=energy,
    )
    assert sp.simplify(off_shell - 2 * product * energy / (energy**2 - delta**2)) == 0
    assert off_shell != 0


def test_asymmetric_zero_loss_cancellation_locus() -> None:
    delta = sp.symbols("Delta", positive=True)
    positive, negative = sp.symbols("c_plus c_minus")
    expression = asymmetric_pair_resolvent(delta, 0, positive, negative)
    assert sp.simplify(expression - (negative - positive) / delta) == 0
    assert sp.simplify(expression.subs(negative, positive)) == 0
    assert sp.simplify(expression.subs(negative, 2 * positive) - positive / delta) == 0


def test_loss_ledger_and_unique_one_pair_peak() -> None:
    delta, product, gamma = sp.symbols("Delta c Gamma", positive=True)
    ledger = symmetric_pair_loss_ledger(delta, product)
    assert ledger.small_loss_linear_coefficient == -sp.I * product / delta**2
    assert ledger.large_loss_inverse_coefficient == -4 * sp.I * product
    assert ledger.stationary_positive_loss == 2 * delta
    assert ledger.peak_magnitude == product / delta
    magnitude = product * gamma / (delta**2 + gamma**2 / 4)
    derivative = sp.factor(sp.diff(magnitude, gamma))
    assert sp.solve(sp.together(derivative), gamma) == [2 * delta]
    assert sp.diff(magnitude, gamma, 2).subs(gamma, 2 * delta) < 0


def test_small_and_large_loss_limits() -> None:
    delta, product, gamma = sp.symbols("Delta c Gamma", positive=True)
    expression = symmetric_pair_resolvent(delta, gamma, product)
    assert sp.limit(expression / gamma, gamma, 0, dir="+") == -sp.I * product / delta**2
    assert sp.limit(gamma * expression, gamma, sp.oo) == -4 * sp.I * product


def test_exact_block_schur_complement_matches_pair_sum() -> None:
    delta, gamma, coupling = sp.symbols("Delta Gamma g", positive=True)
    intermediate = sp.diag(
        delta - sp.I * gamma / 2,
        -delta - sp.I * gamma / 2,
    )
    endpoint = sp.zeros(2)
    to_intermediate = sp.Matrix([[coupling, coupling], [coupling, coupling]])
    effective = finite_resolvent_effective_block(
        endpoint,
        to_intermediate,
        intermediate,
        to_intermediate.T,
    )
    expected = symmetric_pair_resolvent(delta, gamma, coupling**2)
    assert sp.simplify(effective[0, 1] - expected) == 0
    assert effective[0, 0] == effective[0, 1] == effective[1, 1]


def test_pair_count_scaling_distinguishes_enlargement_from_fixed_sum() -> None:
    delta, gamma, product = sp.symbols("Delta Gamma c", positive=True)
    base = symmetric_pair_resolvent(delta, gamma, product)
    fixed_per_pair = equal_pair_resolvent_sum(6, delta, gamma, product)
    fixed_sum = equal_pair_resolvent_sum(
        6,
        delta,
        gamma,
        product,
        scaling="fixed_sum",
    )
    assert sp.simplify(fixed_per_pair - 6 * base) == 0
    assert sp.simplify(fixed_sum - base) == 0


def test_complex_coupling_products_and_shift_sign_are_load_bearing() -> None:
    delta, gamma = sp.symbols("Delta Gamma", positive=True)
    baseline = asymmetric_pair_resolvent(delta, gamma, 1, sp.I)
    changed_phase = asymmetric_pair_resolvent(delta, gamma, 1, -sp.I)
    assert sp.simplify(baseline - changed_phase) != 0
    correct = symmetric_pair_resolvent(delta, gamma)
    wrong_shift = sp.conjugate(correct)
    assert sp.simplify(correct - wrong_shift) != 0


@pytest.mark.parametrize(
    ("detuning", "loss"),
    [(0, 1), (sp.Symbol("Delta"), 1), (1, -1), (1, sp.Symbol("Gamma")), (sp.I, 1)],
)
def test_invalid_or_unresolved_pair_domains_are_rejected(
    detuning: sp.Expr | int,
    loss: sp.Expr | int,
) -> None:
    with pytest.raises(ValueError):
        symmetric_pair_resolvent(detuning, loss)


def test_shape_count_and_scaling_errors_are_rejected() -> None:
    with pytest.raises(ValueError):
        finite_resolvent_effective_block(
            sp.zeros(2),
            sp.zeros(2, 3),
            sp.eye(2),
            sp.zeros(2, 2),
        )
    with pytest.raises(ValueError):
        equal_pair_resolvent_sum(0, 1, 1)
    with pytest.raises(ValueError):
        equal_pair_resolvent_sum(2, 1, 1, scaling="mesh")  # type: ignore[arg-type]
