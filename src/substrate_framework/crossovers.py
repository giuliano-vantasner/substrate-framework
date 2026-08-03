"""Exact conditional horizontal-level crossover utilities.

These functions classify mathematical response levels. They do not identify a
physical channel, common observable normalization, rate, material crossover,
yield, heat signal, or observation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

import sympy as sp

from substrate_framework.screened_barrier import (
    shifted_inverse_sqrt_barrier_factor,
)


RangeLocation = Literal[
    "below_range",
    "lower_endpoint",
    "unique_interior",
    "upper_limit_only",
    "above_range",
]


def _exact_real(value: Any, *, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.has(sp.Float):
        raise ValueError(f"{name} must be exact rather than floating")
    if expression.is_real is not True:
        raise ValueError(f"{name} must be explicitly real")
    return expression


def _exact_positive(value: Any, *, name: str) -> sp.Expr:
    expression = _exact_real(value, name=name)
    if expression.is_positive is not True:
        raise ValueError(f"{name} must be explicitly positive")
    return expression


def _exact_nonnegative(value: Any, *, name: str) -> sp.Expr:
    expression = _exact_real(value, name=name)
    if expression.is_nonnegative is not True:
        raise ValueError(f"{name} must be explicitly nonnegative")
    return expression


def _finite_unit_level(value: Any, *, include_zero: bool) -> sp.Expr:
    level = _exact_real(value, name="level")
    if level.is_number:
        lower_ok = bool(level >= 0) if include_zero else bool(level > 0)
        if not lower_ok or not bool(level < 1):
            interval = "[0,1)" if include_zero else "(0,1)"
            raise ValueError(f"level must lie in {interval}")
    elif include_zero:
        if level.is_nonnegative is not True:
            raise ValueError("symbolic level must be explicitly nonnegative")
    elif level.is_positive is not True:
        raise ValueError("symbolic level must be explicitly positive")
    return level


@dataclass(frozen=True)
class ExponentialCrossoverLedger:
    """Exact inverse and sensitivities for ``1-exp(-E/E0)=c``."""

    scale: sp.Expr
    level: sp.Expr
    crossover_energy: sp.Expr
    level_derivative: sp.Expr
    scale_derivative: sp.Expr
    level_second_derivative: sp.Expr


@dataclass(frozen=True)
class ShiftedBarrierCrossoverLedger:
    """Exact C-SCR-001 floor, inverse, and sensitivities."""

    barrier_scale: sp.Expr
    energy_shift: sp.Expr
    level: sp.Expr
    zero_energy_floor: sp.Expr
    crossover_energy: sp.Expr
    level_derivative: sp.Expr
    barrier_derivative: sp.Expr
    shift_derivative: sp.Expr


def monotone_range_location(
    lower_endpoint: Any,
    upper_unattained_limit: Any,
    level: Any,
) -> RangeLocation:
    """Classify a level for an increasing map on ``[0,infinity)``.

    The map is separately assumed continuous and strictly increasing, to attain
    ``lower_endpoint`` at zero, and to approach but never attain
    ``upper_unattained_limit``. Exact numeric values are required because this
    helper classifies ordering rather than guessing symbolic inequalities.
    """

    lower = _exact_real(lower_endpoint, name="lower_endpoint")
    upper = _exact_real(upper_unattained_limit, name="upper_unattained_limit")
    target = _exact_real(level, name="level")
    if not (lower.is_number and upper.is_number and target.is_number):
        raise ValueError("range classification requires exact numeric values")
    if not bool(lower < upper):
        raise ValueError("lower_endpoint must be below upper_unattained_limit")
    if bool(target < lower):
        return "below_range"
    if bool(sp.Eq(target, lower)):
        return "lower_endpoint"
    if bool(target < upper):
        return "unique_interior"
    if bool(sp.Eq(target, upper)):
        return "upper_limit_only"
    return "above_range"


def exponential_saturation(energy: Any, energy_scale: Any) -> sp.Expr:
    """Return ``1-exp(-E/E0)`` for exact ``E>=0`` and ``E0>0``."""

    input_energy = _exact_nonnegative(energy, name="energy")
    scale = _exact_positive(energy_scale, name="energy_scale")
    return 1 - sp.exp(-input_energy / scale)


def exponential_crossover_energy(energy_scale: Any, level: Any) -> sp.Expr:
    """Return the unique finite ``E>=0`` with ``1-exp(-E/E0)=c``.

    Numeric ``c`` must lie in ``[0,1)``. Symbolic callers retain the explicit
    premise ``c<1``.
    """

    scale = _exact_positive(energy_scale, name="energy_scale")
    target = _finite_unit_level(level, include_zero=True)
    return -scale * sp.log(1 - target)


def exponential_crossover_ledger(
    energy_scale: Any,
    level: Any,
) -> ExponentialCrossoverLedger:
    """Return the exact inverse and its level and scale sensitivities."""

    scale = _exact_positive(energy_scale, name="energy_scale")
    target = _finite_unit_level(level, include_zero=True)
    crossing = exponential_crossover_energy(scale, target)
    return ExponentialCrossoverLedger(
        scale=scale,
        level=target,
        crossover_energy=crossing,
        level_derivative=sp.simplify(scale / (1 - target)),
        scale_derivative=sp.simplify(-sp.log(1 - target)),
        level_second_derivative=sp.simplify(scale / (1 - target) ** 2),
    )


def shifted_barrier_zero_energy_floor(
    barrier_scale: Any,
    energy_shift: Any,
) -> sp.Expr:
    """Return the continuous zero-energy floor for positive shift.

    Zero shift has limiting floor zero and is represented exactly by zero.
    """

    barrier = _exact_positive(barrier_scale, name="barrier_scale")
    shift = _exact_nonnegative(energy_shift, name="energy_shift")
    if shift.is_zero is True:
        return sp.Integer(0)
    return sp.exp(-sp.sqrt(barrier / shift))


def shifted_barrier_crossover_energy(
    barrier_scale: Any,
    energy_shift: Any,
    level: Any,
) -> sp.Expr:
    """Return the positive C-SCR-001 energy crossing an interior level.

    Numeric levels must lie strictly between the zero-energy floor and one.
    Symbolic callers are responsible for carrying that range premise.
    """

    barrier = _exact_positive(barrier_scale, name="barrier_scale")
    shift = _exact_nonnegative(energy_shift, name="energy_shift")
    target = _finite_unit_level(level, include_zero=False)
    floor = shifted_barrier_zero_energy_floor(barrier, shift)
    crossing = sp.simplify(barrier / sp.log(target) ** 2 - shift)
    if target.is_number and floor.is_number:
        if not bool(target > floor):
            raise ValueError("level must exceed the shifted zero-energy floor")
    return crossing


def shifted_barrier_crossover_ledger(
    barrier_scale: Any,
    energy_shift: Any,
    level: Any,
) -> ShiftedBarrierCrossoverLedger:
    """Return the exact shifted-factor inverse and partial sensitivities."""

    barrier = _exact_positive(barrier_scale, name="barrier_scale")
    shift = _exact_nonnegative(energy_shift, name="energy_shift")
    target = _finite_unit_level(level, include_zero=False)
    crossing = shifted_barrier_crossover_energy(barrier, shift, target)
    return ShiftedBarrierCrossoverLedger(
        barrier_scale=barrier,
        energy_shift=shift,
        level=target,
        zero_energy_floor=shifted_barrier_zero_energy_floor(barrier, shift),
        crossover_energy=crossing,
        level_derivative=sp.simplify(
            -2 * barrier / (target * sp.log(target) ** 3)
        ),
        barrier_derivative=sp.simplify(1 / sp.log(target) ** 2),
        shift_derivative=sp.Integer(-1),
    )


def shifted_barrier_crossover_residual(
    barrier_scale: Any,
    energy_shift: Any,
    level: Any,
) -> sp.Expr:
    """Substitute the exact crossing back into the canonical shifted factor."""

    crossing = shifted_barrier_crossover_energy(
        barrier_scale,
        energy_shift,
        level,
    )
    return sp.simplify(
        shifted_inverse_sqrt_barrier_factor(
            crossing,
            barrier_scale,
            energy_shift,
        )
        - sp.sympify(level)
    )
