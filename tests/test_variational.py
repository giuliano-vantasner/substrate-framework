from __future__ import annotations

import sympy as sp

from substrate_framework.variational import (
    euler_lagrange_expression,
    finite_functional_infimum_ledger,
    finite_functional_interaction_ledger,
    solve_euler_lagrange_acceleration,
)


def test_fixed_scale_factors_through_euler_lagrange_operator() -> None:
    time = sp.symbols("t", real=True)
    scale = sp.symbols("A", nonzero=True)
    coordinate = sp.Function("q", real=True)(time)
    potential = sp.Function("V")(coordinate)
    lagrangian = sp.diff(coordinate, time) ** 2 / 2 - potential
    assert sp.simplify(
        euler_lagrange_expression(scale**2 * lagrangian, coordinate, time)
        - scale**2 * euler_lagrange_expression(lagrangian, coordinate, time)
    ) == 0


def test_unique_acceleration_is_solved_from_lagrangian() -> None:
    time = sp.symbols("t", real=True)
    coordinate = sp.Function("q", real=True)(time)
    frequency = sp.symbols("omega", positive=True)
    lagrangian = (
        sp.diff(coordinate, time) ** 2 / 2
        - frequency**2 * coordinate**2 / 2
    )
    assert solve_euler_lagrange_acceleration(
        lagrangian, coordinate, time
    ) == -frequency**2 * coordinate


def test_degenerate_equation_has_no_unique_acceleration() -> None:
    time = sp.symbols("t", real=True)
    coordinate = sp.Function("q", real=True)(time)
    try:
        solve_euler_lagrange_acceleration(coordinate, coordinate, time)
    except ValueError as error:
        assert "one explicit acceleration" in str(error)
    else:
        raise AssertionError("degenerate Lagrangian unexpectedly produced an acceleration")


def test_finite_functional_infimum_ledger_has_exact_excess_identity() -> None:
    m1, m2 = sp.symbols("m1 m2", real=True)
    d1, d2 = sp.symbols("d1 d2", nonnegative=True)
    ledger = finite_functional_infimum_ledger((m1 + d1, m2 + d2), (m1, m2))
    assert ledger.component_excesses == (d1, d2)
    assert ledger.separate_infimum_sum == m1 + m2
    assert ledger.total_excess == d1 + d2
    assert ledger.identity_residual == 0


def test_common_minimizer_attains_sum_of_component_infima() -> None:
    coordinate = sp.symbols("x", real=True)
    ledger = finite_functional_infimum_ledger(
        (coordinate**2, 3 * coordinate**2),
        (0, 0),
    )
    assert sp.solve(sp.diff(ledger.summed_value, coordinate), coordinate) == [0]
    assert ledger.total_excess.subs(coordinate, 0) == 0


def test_incompatible_component_minimizers_make_joint_infimum_strict() -> None:
    coordinate = sp.symbols("x", real=True)
    ledger = finite_functional_infimum_ledger(
        ((coordinate - 1) ** 2, (coordinate + 1) ** 2),
        (0, 0),
    )
    stationary = sp.solve(sp.diff(ledger.summed_value, coordinate), coordinate)
    assert stationary == [0]
    assert ledger.total_excess.subs(coordinate, stationary[0]) == 2


def test_infimum_ledger_rejects_false_lower_bound_or_shape() -> None:
    for values, infima, message in (
        ((), (), "nonempty"),
        ((1, 2), (0,), "equal length"),
        ((0,), (1,), "below its supplied infimum"),
    ):
        try:
            finite_functional_infimum_ledger(values, infima)
        except ValueError as error:
            assert message in str(error)
        else:
            raise AssertionError("invalid functional ledger unexpectedly succeeded")


def _quadratic_minimum(expression: sp.Expr, coordinate: sp.Symbol) -> sp.Expr:
    stationary = sp.solve(sp.diff(expression, coordinate), coordinate)
    assert len(stationary) == 1
    return sp.simplify(expression.subs(coordinate, stationary[0]))


def test_functional_interaction_ledger_has_exact_mixed_identity() -> None:
    base, first, second, joint = sp.symbols("m_A m_AP m_AQ m_APQ", real=True)
    ledger = finite_functional_interaction_ledger(base, first, second, joint)
    assert ledger.first_increment == first - base
    assert ledger.second_increment == second - base
    assert ledger.joint_increment == joint - base
    assert ledger.interaction == base - first - second + joint
    assert ledger.identity_residual == 0


def test_functional_interaction_is_invariant_under_additive_constants() -> None:
    base, first, second, joint = sp.symbols("m_A m_AP m_AQ m_APQ", real=True)
    shift_base, shift_first, shift_second = sp.symbols("c_A c_P c_Q", real=True)
    original = finite_functional_interaction_ledger(base, first, second, joint)
    shifted = finite_functional_interaction_ledger(
        base + shift_base,
        first + shift_base + shift_first,
        second + shift_base + shift_second,
        joint + shift_base + shift_first + shift_second,
    )
    assert sp.simplify(shifted.interaction - original.interaction) == 0


def test_nonnegative_coercive_quadratics_realize_both_interaction_signs() -> None:
    coordinate = sp.symbols("x", real=True)
    base = coordinate**2
    first = (coordinate - 1) ** 2
    positive_second = (coordinate + 1) ** 2
    negative_second = (coordinate - 1) ** 2

    def interaction(second: sp.Expr) -> sp.Expr:
        return finite_functional_interaction_ledger(
            _quadratic_minimum(base, coordinate),
            _quadratic_minimum(base + first, coordinate),
            _quadratic_minimum(base + second, coordinate),
            _quadratic_minimum(base + first + second, coordinate),
        ).interaction

    assert interaction(positive_second) == 1
    assert interaction(negative_second) == -sp.Rational(1, 3)


def test_zero_interaction_does_not_imply_a_common_minimizer() -> None:
    coordinate = sp.symbols("x", real=True)
    displaced_center = 2 + sp.sqrt(3)
    base = coordinate**2
    first = (coordinate - 1) ** 2
    second = (coordinate - displaced_center) ** 2
    ledger = finite_functional_interaction_ledger(
        _quadratic_minimum(base, coordinate),
        _quadratic_minimum(base + first, coordinate),
        _quadratic_minimum(base + second, coordinate),
        _quadratic_minimum(base + first + second, coordinate),
    )
    assert ledger.interaction == 0
    minimizers = (
        set(sp.solve(sp.diff(base, coordinate), coordinate)),
        set(sp.solve(sp.diff(first, coordinate), coordinate)),
        set(sp.solve(sp.diff(second, coordinate), coordinate)),
    )
    assert set.intersection(*minimizers) == set()


def test_common_minimizer_forces_zero_interaction() -> None:
    coordinate = sp.symbols("x", real=True)
    base = coordinate**2
    first = 2 * coordinate**2
    second = 3 * coordinate**2
    ledger = finite_functional_interaction_ledger(
        _quadratic_minimum(base, coordinate),
        _quadratic_minimum(base + first, coordinate),
        _quadratic_minimum(base + second, coordinate),
        _quadratic_minimum(base + first + second, coordinate),
    )
    assert ledger.interaction == 0


def test_positive_scaling_realizes_every_nonzero_interaction_magnitude() -> None:
    magnitude = sp.symbols("r", positive=True)
    positive = finite_functional_interaction_ledger(
        0, magnitude / 2, magnitude / 2, 2 * magnitude
    )
    negative = finite_functional_interaction_ledger(
        0, 3 * magnitude / 2, 3 * magnitude / 2, 2 * magnitude
    )
    assert positive.interaction == magnitude
    assert negative.interaction == -magnitude


def test_interaction_ledger_rejects_nonfinite_or_nonreal_infima() -> None:
    for invalid in (sp.oo, -sp.oo, sp.zoo, sp.nan, sp.I):
        try:
            finite_functional_interaction_ledger(0, 0, 0, invalid)
        except ValueError as error:
            assert "finite real" in str(error)
        else:
            raise AssertionError("nonfinite or nonreal infimum unexpectedly accepted")
