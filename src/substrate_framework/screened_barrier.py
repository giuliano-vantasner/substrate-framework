"""Exact conditional inverse-square-root barrier factors.

The functions in this module manipulate declared positive energy variables.
They return dimensionless barrier factors and enhancements, not cross sections,
transition rates, yields, reaction models, or material screening predictions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp


def _positive_real(value: Any, *, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_real is not True or expression.is_positive is not True:
        raise ValueError(f"{name} must be explicitly positive and real")
    return expression


def _nonnegative_real(value: Any, *, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_real is not True or expression.is_nonnegative is not True:
        raise ValueError(f"{name} must be explicitly nonnegative and real")
    return expression


@dataclass(frozen=True)
class ShiftedBarrierLedger:
    """Exact factor, ratio, and logarithmic derivatives for one input triple."""

    energy: sp.Expr
    barrier_scale: sp.Expr
    energy_shift: sp.Expr
    bare_factor: sp.Expr
    shifted_factor: sp.Expr
    enhancement: sp.Expr
    log_energy_derivative: sp.Expr
    log_shift_derivative: sp.Expr
    log_barrier_scale_derivative: sp.Expr


def inverse_sqrt_barrier_factor(energy: Any, barrier_scale: Any) -> sp.Expr:
    """Return ``exp(-sqrt(G/E))`` for positive real energies E and G."""

    energy_value = _positive_real(energy, name="energy")
    barrier_value = _positive_real(barrier_scale, name="barrier_scale")
    return sp.exp(-sp.sqrt(barrier_value / energy_value))


def shifted_inverse_sqrt_barrier_factor(
    energy: Any,
    barrier_scale: Any,
    energy_shift: Any,
) -> sp.Expr:
    """Return ``exp(-sqrt(G/(E+U)))`` for E,G>0 and U>=0."""

    energy_value = _positive_real(energy, name="energy")
    barrier_value = _positive_real(barrier_scale, name="barrier_scale")
    shift_value = _nonnegative_real(energy_shift, name="energy_shift")
    return sp.exp(-sp.sqrt(barrier_value / (energy_value + shift_value)))


def inverse_sqrt_barrier_enhancement(
    energy: Any,
    barrier_scale: Any,
    energy_shift: Any,
) -> sp.Expr:
    """Return the exact shifted-to-bare dimensionless factor ratio."""

    bare = inverse_sqrt_barrier_factor(energy, barrier_scale)
    shifted = shifted_inverse_sqrt_barrier_factor(
        energy,
        barrier_scale,
        energy_shift,
    )
    return sp.factor(shifted / bare)


def shifted_barrier_ledger(
    energy: Any,
    barrier_scale: Any,
    energy_shift: Any,
) -> ShiftedBarrierLedger:
    """Return exact factors and derivatives of the shifted factor's logarithm."""

    energy_value = _positive_real(energy, name="energy")
    barrier_value = _positive_real(barrier_scale, name="barrier_scale")
    shift_value = _nonnegative_real(energy_shift, name="energy_shift")
    bare = inverse_sqrt_barrier_factor(energy_value, barrier_value)
    shifted = shifted_inverse_sqrt_barrier_factor(
        energy_value,
        barrier_value,
        shift_value,
    )
    enhancement = sp.factor(shifted / bare)
    positive_derivative = sp.simplify(
        sp.sqrt(barrier_value)
        / (2 * (energy_value + shift_value) ** sp.Rational(3, 2))
    )
    return ShiftedBarrierLedger(
        energy=energy_value,
        barrier_scale=barrier_value,
        energy_shift=shift_value,
        bare_factor=bare,
        shifted_factor=shifted,
        enhancement=enhancement,
        log_energy_derivative=positive_derivative,
        log_shift_derivative=positive_derivative,
        log_barrier_scale_derivative=sp.simplify(
            -1
            / (
                2
                * sp.sqrt(barrier_value)
                * sp.sqrt(energy_value + shift_value)
            )
        ),
    )
