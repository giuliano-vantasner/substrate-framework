from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework import (
    ImmigrationDeathLedger,
    immigration_death_generator_action,
    immigration_death_ledger,
    immigration_death_local_drift,
    immigration_death_mean,
    immigration_death_probability_generating_function,
    immigration_death_rates,
    immigration_death_stationary_mass,
    immigration_death_transition_probability,
    reversible_factorial_one_rates,
)


def test_rates_include_the_nonnegative_boundary() -> None:
    assert immigration_death_rates(0, stationary_mean=5, rate=3) == (15, 0)
    assert immigration_death_rates(4, stationary_mean=5, rate=3) == (15, 12)


def test_generator_on_identity_is_the_local_drift() -> None:
    S, r = sp.symbols("S r", positive=True)
    for state in range(6):
        action = immigration_death_generator_action(
            state,
            lower_value=state - 1,
            current_value=state,
            upper_value=state + 1,
            stationary_mean=S,
            rate=r,
        )
        assert sp.simplify(action - r * (S - state)) == 0
        assert immigration_death_local_drift(
            state,
            stationary_mean=S,
            rate=r,
        ) == action


def test_generator_on_constant_is_zero_even_at_boundary() -> None:
    for state in range(5):
        assert (
            immigration_death_generator_action(
                state,
                lower_value=1,
                current_value=1,
                upper_value=1,
                stationary_mean=7,
                rate=2,
            )
            == 0
        )


def test_stationary_mass_is_normalized_exactly() -> None:
    S = sp.symbols("S", positive=True)
    n = sp.symbols("n", integer=True, nonnegative=True)
    total = sp.summation(
        sp.exp(-S) * S**n / sp.factorial(n),
        (n, 0, sp.oo),
    )
    assert sp.simplify(total - 1) == 0
    for state in range(6):
        assert immigration_death_stationary_mass(
            state,
            stationary_mean=S,
        ) == sp.exp(-S) * S**state / sp.factorial(state)


def test_immigration_death_detailed_balance_is_exact() -> None:
    S, r = sp.symbols("S r", positive=True)
    for state in range(7):
        current = immigration_death_stationary_mass(state, stationary_mean=S)
        following = immigration_death_stationary_mass(state + 1, stationary_mean=S)
        birth, _ = immigration_death_rates(state, stationary_mean=S, rate=r)
        _, next_death = immigration_death_rates(
            state + 1,
            stationary_mean=S,
            rate=r,
        )
        assert sp.simplify(current * birth - following * next_death) == 0


def test_mean_solves_the_exact_relaxation_equation() -> None:
    t = sp.symbols("t", nonnegative=True)
    S, r, m0 = sp.symbols("S r m0", positive=True)
    mean = immigration_death_mean(
        t,
        initial_mean=m0,
        stationary_mean=S,
        rate=r,
    )
    assert mean.subs(t, 0) == m0
    assert sp.simplify(sp.diff(mean, t) - r * (S - mean)) == 0
    assert sp.limit(mean, t, sp.oo) == S


def test_pgf_has_initial_and_stationary_limits() -> None:
    z, t = sp.symbols("z t", nonnegative=True)
    S, r = sp.symbols("S r", positive=True)
    initial = z**4
    pgf = immigration_death_probability_generating_function(
        z,
        t,
        initial_generating_function=initial,
        stationary_mean=S,
        rate=r,
    )
    assert sp.simplify(pgf.subs(t, 0) - initial) == 0
    assert sp.simplify(pgf.subs(z, 1) - 1) == 0
    assert sp.simplify(sp.limit(pgf, t, sp.oo) - sp.exp(S * (z - 1))) == 0


def test_pgf_mean_agrees_with_mean_solution_for_deterministic_initial_state() -> None:
    z, t = sp.symbols("z t", nonnegative=True)
    S, r = sp.symbols("S r", positive=True)
    pgf = immigration_death_probability_generating_function(
        z,
        t,
        initial_generating_function=z**4,
        stationary_mean=S,
        rate=r,
    )
    pgf_mean = sp.diff(pgf, z).subs(z, 1)
    expected = immigration_death_mean(
        t,
        initial_mean=4,
        stationary_mean=S,
        rate=r,
    )
    assert sp.simplify(pgf_mean - expected) == 0


def test_transition_probability_has_delta_initial_limit() -> None:
    for final in range(7):
        actual = immigration_death_transition_probability(
            final,
            initial_state=3,
            time=0,
            stationary_mean=5,
            rate=2,
        )
        assert actual == (1 if final == 3 else 0)


def test_transition_probability_matches_binomial_poisson_pgf() -> None:
    z = sp.symbols("z")
    t = sp.Rational(2, 3)
    S = sp.Integer(5)
    r = sp.Rational(3, 2)
    pgf = immigration_death_probability_generating_function(
        z,
        t,
        initial_generating_function=z**3,
        stationary_mean=S,
        rate=r,
    )
    for final in range(7):
        coefficient = sp.diff(pgf, z, final).subs(z, 0) / sp.factorial(final)
        probability = immigration_death_transition_probability(
            final,
            initial_state=3,
            time=t,
            stationary_mean=S,
            rate=r,
        )
        assert sp.simplify(coefficient - probability) == 0


def test_transition_probability_converges_to_stationary_mass() -> None:
    t = sp.symbols("t", nonnegative=True)
    for final in range(6):
        transition = immigration_death_transition_probability(
            final,
            initial_state=4,
            time=t,
            stationary_mean=3,
            rate=2,
        )
        stationary = immigration_death_stationary_mass(final, stationary_mean=3)
        assert sp.simplify(sp.limit(transition, t, sp.oo) - stationary) == 0


def test_rate_scale_changes_transients_but_not_stationary_mass() -> None:
    t = sp.symbols("t", positive=True)
    slow = immigration_death_mean(t, initial_mean=0, stationary_mean=5, rate=1)
    fast = immigration_death_mean(t, initial_mean=0, stationary_mean=5, rate=2)
    assert sp.simplify(slow - fast) != 0
    assert immigration_death_stationary_mass(
        3,
        stationary_mean=5,
    ) == immigration_death_stationary_mass(3, stationary_mean=5)


def test_alternative_rates_have_same_detailed_balance_ratio() -> None:
    S, r = sp.symbols("S r", positive=True)
    for state in range(7):
        alternative_birth, _ = reversible_factorial_one_rates(
            state,
            stationary_mean=S,
            rate=r,
        )
        _, alternative_next_death = reversible_factorial_one_rates(
            state + 1,
            stationary_mean=S,
            rate=r,
        )
        assert sp.simplify(
            alternative_birth / alternative_next_death - S / (state + 1)
        ) == 0


def test_alternative_generator_is_genuinely_different() -> None:
    primary = immigration_death_rates(3, stationary_mean=5, rate=2)
    alternative = reversible_factorial_one_rates(3, stationary_mean=5, rate=2)
    assert primary != alternative
    assert primary == (10, 6)
    assert alternative == (sp.Rational(5, 2), 2)


def test_adjacent_stationary_ratio_is_not_a_time_derivative() -> None:
    ledger = immigration_death_ledger(2, stationary_mean=5, rate=3)
    assert ledger.adjacent_stationary_ratio == sp.Rational(5, 3)
    assert ledger.local_drift == 9
    assert ledger.adjacent_stationary_ratio != ledger.local_drift


def test_positive_local_drift_does_not_remove_death_jumps() -> None:
    ledger = immigration_death_ledger(2, stationary_mean=5, rate=3)
    assert ledger.local_drift > 0
    assert ledger.death_rate > 0
    assert not ledger.positive_drift_implies_monotone_sample_paths


def test_ledger_records_interpretation_ceilings() -> None:
    ledger = immigration_death_ledger(0, stationary_mean=5, rate=3)
    assert isinstance(ledger, ImmigrationDeathLedger)
    assert ledger.boundary_death_rate_is_zero
    assert not ledger.static_mass_selects_unique_dynamics
    assert ledger.material_process_is_separate_premise


@pytest.mark.parametrize("bad", [-1, sp.Rational(1, 2), 1.0])
def test_invalid_states_are_rejected(bad: object) -> None:
    with pytest.raises(ValueError, match="nonnegative integer"):
        immigration_death_rates(bad, stationary_mean=5, rate=3)


@pytest.mark.parametrize("bad", [0, -1, 0.5])
def test_nonpositive_or_inexact_model_inputs_are_rejected(bad: object) -> None:
    with pytest.raises(ValueError):
        immigration_death_rates(0, stationary_mean=bad, rate=3)
    with pytest.raises(ValueError):
        immigration_death_rates(0, stationary_mean=5, rate=bad)


def test_negative_or_inexact_time_is_rejected() -> None:
    for bad in (-1, 0.5):
        with pytest.raises(ValueError):
            immigration_death_mean(
                bad,
                initial_mean=0,
                stationary_mean=5,
                rate=3,
            )


def test_public_docstrings_preserve_physical_ceilings() -> None:
    generator_text = " ".join(immigration_death_generator_action.__doc__.split())
    rates_text = " ".join(reversible_factorial_one_rates.__doc__.split())
    assert "not monotone sample-path growth" in generator_text
    assert "nonuniqueness" in rates_text
