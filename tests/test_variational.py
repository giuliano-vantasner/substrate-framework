from __future__ import annotations

import sympy as sp

from substrate_framework.variational import (
    euler_lagrange_expression,
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
