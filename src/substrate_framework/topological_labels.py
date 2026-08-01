"""Exact algebra for integer winding labels.

The parity label defined here is a group character. Calling it a fermion or
boson statistic requires an additional physical spin-statistics map.
"""

from __future__ import annotations

from typing import Any

import sympy as sp


def _integer(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_integer is not True:
        raise ValueError(f"{name} must be an integer")
    return expression


def winding_parity(winding: Any) -> sp.Expr:
    """Return the multiplicative label ``(-1)**winding`` for integer winding."""

    value = _integer(winding, "winding")
    return sp.simplify((-1) ** value)


def combined_winding_parity(anchor_winding: Any, dressing_winding: Any) -> sp.Expr:
    """Return parity after adding integer anchor and dressing windings."""

    anchor = _integer(anchor_winding, "anchor_winding")
    dressing = _integer(dressing_winding, "dressing_winding")
    return winding_parity(anchor + dressing)
