from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.bosonic_fock import (
    factorial_one_falling_factorial_moment,
    factorial_one_geometric_point_bound,
    factorial_one_geometric_tail_bound,
    factorial_one_log_concavity_ratio,
    factorial_one_modes,
    factorial_one_polynomial_tail_certificate,
    factorial_one_probability_generating_function,
    normalized_factorial_one_mass,
)


def test_log_concavity_is_exact_but_preserves_integer_mode_ties() -> None:
    intensity = sp.symbols("S", positive=True)
    for order in range(1, 18):
        mass = lambda n: intensity**n / sp.factorial(n)
        raw_ratio = sp.simplify(
            mass(order) ** 2 / (mass(order - 1) * mass(order + 1))
        )
        assert raw_ratio == factorial_one_log_concavity_ratio(order)
        assert raw_ratio == sp.Rational(order + 1, order)
        assert raw_ratio > 1

        wrong_mass = lambda n: intensity**n / sp.factorial(n) ** 2
        wrong_ratio = sp.simplify(
            wrong_mass(order) ** 2
            / (wrong_mass(order - 1) * wrong_mass(order + 1))
        )
        assert wrong_ratio != raw_ratio

    for integer in range(1, 12):
        assert factorial_one_modes(
            intensity=integer,
            support="all_nonnegative",
        ) == (integer - 1, integer)
    assert factorial_one_modes(
        intensity=sp.Rational(25, 2),
        support="all_nonnegative",
    ) == (12,)


def test_probability_generating_function_rederives_every_coefficient() -> None:
    intensity, variable = sp.symbols("S t", positive=True, real=True)
    generating = factorial_one_probability_generating_function(
        intensity=intensity,
        variable=variable,
    )
    assert generating == sp.exp(intensity * (variable - 1))
    assert generating.subs(variable, 1) == 1
    for order in range(8):
        coefficient = sp.diff(generating, variable, order).subs(variable, 0)
        coefficient = sp.simplify(coefficient / sp.factorial(order))
        expected = normalized_factorial_one_mass(
            order,
            intensity=intensity,
            support="all_nonnegative",
        )
        assert sp.simplify(coefficient - expected) == 0

    wrong_generating = sp.exp(intensity * (variable + 1))
    assert wrong_generating.subs(variable, 1) != 1


def test_pgf_derivatives_rederive_all_falling_factorial_moments() -> None:
    intensity, variable = sp.symbols("S t", positive=True, real=True)
    generating = sp.exp(intensity * (variable - 1))
    for order in range(8):
        direct = sp.diff(generating, variable, order).subs(variable, 1)
        actual = factorial_one_falling_factorial_moment(
            order,
            intensity=intensity,
        )
        assert sp.simplify(actual - direct) == 0
        assert actual == intensity**order

    mean = factorial_one_falling_factorial_moment(1, intensity=intensity)
    second_falling = factorial_one_falling_factorial_moment(
        2,
        intensity=intensity,
    )
    variance = sp.simplify(second_falling + mean - mean**2)
    assert variance == intensity
    assert sp.simplify(second_falling - intensity**2) == 0


def test_geometric_point_and_upper_tail_bounds_use_exact_threshold() -> None:
    intensity = sp.Integer(5)
    alpha = sp.log(2)
    starting_order = 9
    initial = normalized_factorial_one_mass(
        starting_order,
        intensity=intensity,
        support="all_nonnegative",
    )
    for steps in range(9):
        actual = normalized_factorial_one_mass(
            starting_order + steps,
            intensity=intensity,
            support="all_nonnegative",
        )
        bound = factorial_one_geometric_point_bound(
            steps,
            intensity=intensity,
            alpha=alpha,
            starting_order=starting_order,
        )
        assert sp.simplify(bound - initial / 2**steps) == 0
        assert sp.simplify(actual / initial) <= sp.Rational(1, 2**steps)

    upper_tail = 1 - sum(
        normalized_factorial_one_mass(
            order,
            intensity=intensity,
            support="all_nonnegative",
        )
        for order in range(starting_order + 1)
    )
    bound = factorial_one_geometric_tail_bound(
        intensity=intensity,
        alpha=alpha,
        starting_order=starting_order,
    )
    assert bound == initial
    assert sp.N(bound - upper_tail, 40) > 0

    with pytest.raises(ValueError):
        factorial_one_geometric_tail_bound(
            intensity=intensity,
            alpha=alpha,
            starting_order=starting_order - 1,
        )


def test_polynomial_tail_certificate_gives_a_conservative_contraction() -> None:
    certificate = factorial_one_polynomial_tail_certificate(
        4,
        intensity=sp.Rational(3, 2),
        contraction=sp.Rational(1, 3),
    )
    assert certificate.threshold == 72
    assert certificate.starting_order == 71
    assert certificate.ratio_bound == sp.Rational(1, 3)
    assert certificate.scaled_mass_tends_to_zero is True
    assert certificate.physical_power_law_interpretation_is_separate_premise is True

    for order in range(certificate.starting_order, certificate.starting_order + 8):
        exact_ratio = sp.simplify(
            sp.Rational(3, 2)
            / (order + 1)
            * sp.Rational(order + 1, order) ** 4
        )
        conservative = sp.Rational(3, 2) * 2**4 / (order + 1)
        assert exact_ratio <= conservative <= certificate.contraction

    stronger_power = factorial_one_polynomial_tail_certificate(
        5,
        intensity=sp.Rational(3, 2),
        contraction=sp.Rational(1, 3),
    )
    assert stronger_power.starting_order > certificate.starting_order


@pytest.mark.parametrize("bad_order", [0, -1, sp.Rational(3, 2)])
def test_log_concavity_rejects_nonpositive_or_nonintegral_order(
    bad_order: sp.Expr | int,
) -> None:
    with pytest.raises(ValueError):
        factorial_one_log_concavity_ratio(bad_order)


def test_tail_and_moment_domains_are_explicit() -> None:
    with pytest.raises(ValueError):
        factorial_one_falling_factorial_moment(-1, intensity=2)
    with pytest.raises(ValueError):
        factorial_one_probability_generating_function(
            intensity=2,
            variable=sp.I,
        )
    with pytest.raises(ValueError):
        factorial_one_polynomial_tail_certificate(
            2,
            intensity=2,
            contraction=1,
        )
    with pytest.raises(ValueError):
        factorial_one_geometric_point_bound(
            1,
            intensity=2,
            alpha=-1,
            starting_order=10,
        )
