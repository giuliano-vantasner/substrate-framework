"""Exact normalized two-level occupation and symmetric gate utilities."""

from __future__ import annotations

from typing import Any

import sympy as sp


def _real_splitting(splitting: Any) -> sp.Expr:
    value = sp.sympify(splitting)
    if value.is_number and value.is_real is not True:
        raise ValueError("splitting must be real and dimensionless")
    return value


def two_level_upper_occupation(splitting: Any) -> sp.Expr:
    """Return ``P = exp(-x)/(1+exp(-x)) = 1/(1+exp(x))``."""

    x = _real_splitting(splitting)
    return 1 / (1 + sp.exp(x))


def two_level_occupation_variance(splitting: Any) -> sp.Expr:
    """Return the Bernoulli upper-state variance ``P*(1-P)``."""

    probability = two_level_upper_occupation(splitting)
    return sp.simplify(probability * (1 - probability))


def symmetric_two_level_gate(splitting: Any) -> sp.Expr:
    """Return ``W = 2*P*(1-P) = sech(x/2)**2/2``."""

    return sp.simplify(2 * two_level_occupation_variance(splitting))
