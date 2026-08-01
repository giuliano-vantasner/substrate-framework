"""Pure symbolic Euler-Lagrange utilities."""

from __future__ import annotations

from typing import Any

import sympy as sp


def euler_lagrange_expression(
    lagrangian: Any,
    coordinate: sp.Expr,
    parameter: sp.Symbol,
) -> sp.Expr:
    """Return ``d/dt(dL/dqdot) - dL/dq`` for one coordinate."""

    expression = sp.sympify(lagrangian)
    velocity = sp.diff(coordinate, parameter)
    return sp.simplify(
        sp.diff(sp.diff(expression, velocity), parameter)
        - sp.diff(expression, coordinate)
    )


def solve_euler_lagrange_acceleration(
    lagrangian: Any,
    coordinate: sp.Expr,
    parameter: sp.Symbol,
) -> sp.Expr:
    """Solve a one-coordinate Euler-Lagrange equation for its acceleration."""

    acceleration = sp.diff(coordinate, parameter, 2)
    placeholder = sp.Dummy("acceleration")
    residual = euler_lagrange_expression(lagrangian, coordinate, parameter)
    solutions = sp.solve(residual.subs(acceleration, placeholder), placeholder)
    if len(solutions) != 1:
        raise ValueError(
            "Euler-Lagrange equation must have one explicit acceleration solution"
        )
    return sp.simplify(solutions[0])
