from __future__ import annotations

import sympy as sp

from substrate_framework.variational import (
    euler_lagrange_expression,
    finite_functional_infimum_ledger,
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
