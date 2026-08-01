"""Conditional scalar fluctuation spectrum of the quartic Q-ball profile.

This module describes the unconstrained second variation of the declared
one-field quartic energy functional.  Its negative and translation modes are
not particle generations or positive masses, and this scalar operator alone
does not prove constrained Q-ball stability.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import sympy as sp
from scipy.linalg import eigh_tridiagonal

from .quartic_qball import (
    quartic_qball_inverse_width,
    quartic_qball_profile,
)


def quartic_qball_effective_potential(field_value: Any, omega: Any) -> sp.Expr:
    """Return ``kappa**2*f**2/2-f**4/48`` for the declared stationary energy."""

    field = sp.sympify(field_value)
    kappa = quartic_qball_inverse_width(omega)
    return sp.simplify(kappa**2 * field**2 / 2 - field**4 / 48)


def quartic_fluctuation_potential(
    coordinate: Any, omega: Any, center: Any = 0
) -> sp.Expr:
    """Return ``kappa**2-6*kappa**2*sech(kappa*(x-center))**2``."""

    x = sp.sympify(coordinate)
    origin = sp.sympify(center)
    kappa = quartic_qball_inverse_width(omega)
    return sp.simplify(
        kappa**2
        - 6 * kappa**2 * sp.sech(kappa * (x - origin)) ** 2
    )


def quartic_fluctuation_operator(
    mode: Any,
    coordinate: sp.Symbol,
    omega: Any,
    center: Any = 0,
) -> sp.Expr:
    """Apply the scalar second-variation operator to ``mode``."""

    function = sp.sympify(mode)
    return (
        -sp.diff(function, coordinate, 2)
        + quartic_fluctuation_potential(coordinate, omega, center)
        * function
    )


def quartic_fluctuation_bound_eigenvalues(omega: Any) -> tuple[sp.Expr, sp.Expr]:
    """Return the exact bound eigenvalues ``(-3*kappa**2, 0)``."""

    kappa = quartic_qball_inverse_width(omega)
    return sp.simplify(-3 * kappa**2), sp.Integer(0)


def quartic_fluctuation_bound_modes(
    coordinate: Any, omega: Any, center: Any = 0
) -> tuple[sp.Expr, sp.Expr]:
    """Return unnormalized even negative and odd translation eigenmodes."""

    x = sp.sympify(coordinate)
    origin = sp.sympify(center)
    kappa = quartic_qball_inverse_width(omega)
    argument = kappa * (x - origin)
    return sp.sech(argument) ** 2, sp.sech(argument) * sp.tanh(argument)


def quartic_fluctuation_continuum_threshold(omega: Any) -> sp.Expr:
    """Return the asymptotic continuum threshold ``kappa**2``."""

    kappa = quartic_qball_inverse_width(omega)
    return sp.simplify(kappa**2)


@dataclass(frozen=True)
class FluctuationSpectrumEvidence:
    """Finite-box regression evidence for the exact quartic spectrum."""

    frequency: float
    half_extent: float
    points: int
    spacing: float
    continuum_threshold: float
    bound_eigenvalues: tuple[float, ...]


def solve_quartic_fluctuation_spectrum(
    omega: Any,
    *,
    half_extent_in_widths: float = 24.0,
    points: int = 4001,
    threshold_margin: float = 1.0e-6,
) -> FluctuationSpectrumEvidence:
    """Solve the Dirichlet finite-box spectrum below the exact threshold."""

    kappa_expression = quartic_qball_inverse_width(omega)
    if kappa_expression.is_number is not True:
        raise ValueError("omega must be numeric for the finite-difference spectrum")
    if half_extent_in_widths <= 0.0:
        raise ValueError("half_extent_in_widths must be positive")
    if points < 101:
        raise ValueError("points must be at least 101")
    if threshold_margin <= 0.0:
        raise ValueError("threshold_margin must be positive")
    frequency = float(sp.sympify(omega))
    kappa = float(kappa_expression)
    threshold = kappa**2
    half_extent = half_extent_in_widths / kappa
    grid = np.linspace(-half_extent, half_extent, points)
    spacing = float(grid[1] - grid[0])
    potential = threshold - 6.0 * threshold / np.cosh(kappa * grid) ** 2
    diagonal = 2.0 / spacing**2 + potential[1:-1]
    off_diagonal = -np.ones(len(diagonal) - 1) / spacing**2
    eigenvalues = eigh_tridiagonal(
        diagonal,
        off_diagonal,
        select="v",
        select_range=(-10.0 * threshold, threshold - threshold_margin),
        eigvals_only=True,
    )
    return FluctuationSpectrumEvidence(
        frequency=frequency,
        half_extent=half_extent,
        points=points,
        spacing=spacing,
        continuum_threshold=threshold,
        bound_eigenvalues=tuple(float(value) for value in eigenvalues),
    )
