"""Pure symbolic variational utilities with explicit functional scope."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

import sympy as sp


@dataclass(frozen=True)
class FiniteFunctionalInfimumLedger:
    """Exact pointwise excess ledger relative to supplied component infima.

    The caller supplies the true finite component infima on one common
    nonempty admissible set.  The ledger does not infer those infima or claim
    that they are attained.  For any common configuration, every component
    excess is nonnegative and their sum is the excess of the functional sum
    above the sum of the separate infima.
    """

    component_values: tuple[sp.Expr, ...]
    component_infima: tuple[sp.Expr, ...]
    component_excesses: tuple[sp.Expr, ...]
    summed_value: sp.Expr
    separate_infimum_sum: sp.Expr
    total_excess: sp.Expr

    @property
    def identity_residual(self) -> sp.Expr:
        """Return the exact sum-of-excesses identity residual."""

        return sp.simplify(
            self.total_excess - sum(self.component_excesses, sp.S.Zero)
        )


def _nonempty_expressions(values: Iterable[Any], name: str) -> tuple[sp.Expr, ...]:
    result = tuple(sp.sympify(value) for value in values)
    if not result:
        raise ValueError(f"{name} must be nonempty")
    return result


def finite_functional_infimum_ledger(
    component_values: Iterable[Any],
    component_infima: Iterable[Any],
) -> FiniteFunctionalInfimumLedger:
    """Return an exact common-configuration functional excess ledger.

    ``component_values`` must all be evaluated on the same admissible
    configuration. ``component_infima`` are separately supplied lower bounds
    that are assumed to be the corresponding exact infima.  Provably negative
    component excesses are rejected because they contradict that premise.
    """

    values = _nonempty_expressions(component_values, "component_values")
    infima = _nonempty_expressions(component_infima, "component_infima")
    if len(values) != len(infima):
        raise ValueError("component_values and component_infima must have equal length")
    excesses = tuple(sp.simplify(value - infimum) for value, infimum in zip(values, infima))
    if any(excess.is_negative is True for excess in excesses):
        raise ValueError("component value cannot lie below its supplied infimum")
    summed_value = sp.simplify(sum(values, sp.S.Zero))
    separate_sum = sp.simplify(sum(infima, sp.S.Zero))
    return FiniteFunctionalInfimumLedger(
        component_values=values,
        component_infima=infima,
        component_excesses=excesses,
        summed_value=summed_value,
        separate_infimum_sum=separate_sum,
        total_excess=sp.simplify(summed_value - separate_sum),
    )


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
