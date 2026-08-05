from __future__ import annotations

import pytest
import sympy as sp

import substrate_framework as framework
from substrate_framework.factorial_suppression import (
    OddFactorialMassEnclosure,
    normalized_parity_factorial_mass,
    odd_factorial_mass_enclosure,
    odd_factorial_total_mass,
    parity_thinned_factorial_mass,
)


def test_parity_thinned_mass_retains_activity_and_factorial_square() -> None:
    activity = sp.Symbol("z", positive=True)
    assert parity_thinned_factorial_mass(4, activity=activity) == 0
    assert parity_thinned_factorial_mass(
        5,
        activity=activity,
    ) == activity**10 / sp.factorial(5) ** 2
    assert parity_thinned_factorial_mass(3) == sp.Rational(1, 36)


def test_total_mass_is_the_exact_odd_parity_filter() -> None:
    activity = sp.Symbol("z", positive=True)
    total = odd_factorial_total_mass(activity)
    expected = (
        sp.besseli(0, 2 * activity) - sp.besselj(0, 2 * activity)
    ) / 2
    assert total == expected
    expected_series = sum(
        activity ** (2 * order) / sp.factorial(order) ** 2
        for order in (1, 3, 5, 7)
    )
    assert sp.series(total, activity, 0, 17).removeO() == expected_series


def test_normalized_mass_uses_the_declared_infinite_total() -> None:
    total = odd_factorial_total_mass()
    assert normalized_parity_factorial_mass(2) == 0
    assert sp.simplify(normalized_parity_factorial_mass(1) - 1 / total) == 0
    assert sp.simplify(
        normalized_parity_factorial_mass(3) - sp.Rational(1, 36) / total
    ) == 0


def test_unit_activity_enclosure_reproduces_exact_concentration_margins() -> None:
    enclosure = odd_factorial_mass_enclosure(9)
    assert enclosure == OddFactorialMassEnclosure(
        activity=sp.Rational(1),
        maximum_odd_order=9,
        partial_mass=sp.Rational(135348874561, 131681894400),
        first_omitted_order=11,
        first_omitted_mass=sp.Rational(1, 1593350922240000),
        tail_ratio_ceiling=sp.Rational(1, 24336),
        tail_mass_upper_bound=sp.Rational(169, 269265240921600000),
        total_mass_lower_bound=sp.Rational(135348874561, 131681894400),
        total_mass_upper_bound=sp.Rational(
            9963487458886859459,
            9693548673177600000,
        ),
        normalized_tail_upper_bound=sp.Rational(
            6084,
            9963487458886853375,
        ),
    )
    p1_lower = sp.factor(1 / enclosure.total_mass_upper_bound)
    p13_lower = sp.factor(sp.Rational(37, 36) / enclosure.total_mass_upper_bound)
    assert p1_lower - sp.Rational(972, 1000) == sp.Rational(
        2259715784893151463,
        2490871864721714864750,
    )
    assert p13_lower - sp.Rational(9999, 10000) == sp.Rational(
        3228039582292269459,
        99634874588868594590000,
    )


def test_tail_enclosure_dominates_a_fresh_finite_tail() -> None:
    enclosure = odd_factorial_mass_enclosure(9)
    finite_tail = sum(
        parity_thinned_factorial_mass(order)
        for order in range(11, 32, 2)
    )
    assert finite_tail < enclosure.tail_mass_upper_bound
    assert enclosure.total_mass_lower_bound < enclosure.total_mass_upper_bound


def test_activity_changes_the_mode_without_changing_parity_or_factorials() -> None:
    unit = [parity_thinned_factorial_mass(order) for order in (1, 3, 5, 7)]
    scaled = [
        parity_thinned_factorial_mass(order, activity=4)
        for order in (1, 3, 5, 7)
    ]
    assert max(range(4), key=unit.__getitem__) == 0
    assert max(range(4), key=scaled.__getitem__) == 1
    assert scaled[1] / scaled[0] == sp.Rational(64, 9)
    assert scaled[2] / scaled[1] == sp.Rational(16, 25)


@pytest.mark.parametrize(
    "call",
    [
        lambda: parity_thinned_factorial_mass(0),
        lambda: parity_thinned_factorial_mass(1, activity=0),
        lambda: parity_thinned_factorial_mass(1, activity=1.0),
        lambda: odd_factorial_total_mass(sp.Symbol("z", real=True)),
        lambda: odd_factorial_mass_enclosure(4),
        lambda: odd_factorial_mass_enclosure(1, activity=100),
        lambda: odd_factorial_mass_enclosure(9, activity=sp.sqrt(2)),
    ],
)
def test_domains_are_explicit_and_exact(call) -> None:
    with pytest.raises(ValueError):
        call()


def test_public_exports_match_the_canonical_module() -> None:
    assert framework.OddFactorialMassEnclosure is OddFactorialMassEnclosure
    assert framework.parity_thinned_factorial_mass is parity_thinned_factorial_mass
    assert framework.odd_factorial_total_mass is odd_factorial_total_mass
    assert framework.normalized_parity_factorial_mass is normalized_parity_factorial_mass
    assert framework.odd_factorial_mass_enclosure is odd_factorial_mass_enclosure
