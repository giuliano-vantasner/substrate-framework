from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.sine_gordon import (
    breather_action,
    breather_energy,
    breather_energy_from_action,
    breather_field,
    breather_inverse_width,
    breather_frequency_from_action,
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
    action = breather_action(omega)
    assert action == 16 * sp.acos(sp.Rational(3, 5))
    assert sp.simplify(breather_frequency_from_action(action) - omega) == 0
    assert sp.simplify(breather_energy_from_action(action) - breather_energy(omega)) == 0


@pytest.mark.parametrize("omega", [0, 1, -sp.Rational(1, 2), 2, sp.I])
def test_numeric_frequency_domain_is_enforced(omega: sp.Expr) -> None:
    with pytest.raises(ValueError, match="0 < omega < 1"):
        breather_energy(omega)


@pytest.mark.parametrize("action", [0, 8 * sp.pi, -1, 9 * sp.pi, sp.I])
def test_numeric_action_domain_is_enforced(action: sp.Expr) -> None:
    with pytest.raises(ValueError, match=r"0 < action < 8\*pi"):
        breather_energy_from_action(action)
