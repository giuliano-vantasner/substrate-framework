"""Shared numerical helpers for the P241 SciPy audit modules."""

from __future__ import annotations

import numpy as np

# Two-step compatibility fallback (numpy >= 2.0 renamed trapz -> trapezoid).
_trapezoid = getattr(np, "trapezoid", None)
if _trapezoid is None:  # numpy < 2.0
    _trapezoid = np.trapz


def trapezoid(y, x):
    """Sampled trapezoidal integral, version-portable."""
    return _trapezoid(y, x)


def radial_laplacian(field: np.ndarray, dr: float) -> np.ndarray:
    """3D radial Laplacian on a uniform grid incl. regularity at r = 0."""
    r = np.arange(field.size, dtype=float) * dr
    lap = np.empty_like(field)
    lap[1:-1] = (
        (field[2:] - 2.0 * field[1:-1] + field[:-2]) / dr**2
        + (field[2:] - field[:-2]) / (dr * r[1:-1])
    )
    lap[0] = 3.0 * (field[1] - field[0]) / dr**2
    return lap
