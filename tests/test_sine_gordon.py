from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.sine_gordon import (
    breather_energy,
    breather_field,
    breather_inverse_width,
    breather_peak_amplitude,
    breather_period,
    sine_gordon_residual,
)


def test_exact_breather_residual_vanishes() -> None:
    x, t = sp.symbols("x t", real=True)
    omega = sp.symbols("omega", positive=True)
    field = breather_field(x, t, omega)
    assert sp.simplify(sine_gordon_residual(field, x, t)) == 0


def test_breather_formulas_at_exact_frequency() -> None:
    omega = sp.Rational(3, 5)
    assert breather_inverse_width(omega) == sp.Rational(4, 5)
    assert breather_energy(omega) == sp.Rational(64, 5)
    assert breather_period(omega) == 10 * sp.pi / 3
    assert breather_peak_amplitude(omega) == 4 * sp.atan(sp.Rational(4, 3))


@pytest.mark.parametrize("omega", [0, 1, -sp.Rational(1, 2), 2, sp.I])
def test_numeric_frequency_domain_is_enforced(omega: sp.Expr) -> None:
    with pytest.raises(ValueError, match="0 < omega < 1"):
        breather_energy(omega)
