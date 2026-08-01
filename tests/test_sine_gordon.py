from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.sine_gordon import (
    breather_action,
    breather_action_lattice_adjacent_gap,
    breather_action_lattice_energy,
    breather_action_lattice_frequency,
    breather_action_secant_ratio,
    boosted_breather_energy_momentum,
    boosted_breather_phase_components,
    breather_energy,
    breather_energy_from_action,
    breather_field,
    breather_inverse_width,
    breather_frequency_from_action,
    breather_mean_gradient_integral,
    breather_peak_amplitude,
    breather_period,
    breather_secant_action_scale,
    breather_threshold_deficit,
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
    assert breather_threshold_deficit(omega) == sp.Rational(16, 5)
    assert breather_energy(omega) + breather_threshold_deficit(omega) == 16
    assert breather_period(omega) == 10 * sp.pi / 3
    assert breather_peak_amplitude(omega) == 4 * sp.atan(sp.Rational(4, 3))
    action = breather_action(omega)
    assert action == 16 * sp.acos(sp.Rational(3, 5))
    assert sp.simplify(breather_frequency_from_action(action) - omega) == 0
    assert sp.simplify(breather_energy_from_action(action) - breather_energy(omega)) == 0
    assert breather_mean_gradient_integral(omega) == 16 * (
        sp.Rational(4, 5) - sp.Rational(3, 5) * sp.acos(sp.Rational(3, 5))
    )
    assert breather_secant_action_scale(omega) == sp.Rational(64, 3)
    assert breather_action_secant_ratio(omega) == sp.Rational(3, 4) * sp.acos(
        sp.Rational(3, 5)
    )


def test_conditional_action_lattice_and_adjacent_gap() -> None:
    level = 2
    action_quantum = sp.pi
    assert breather_action_lattice_frequency(level, action_quantum) == sp.cos(
        sp.pi / 8
    )
    assert breather_action_lattice_energy(level, action_quantum) == 16 * sp.sin(
        sp.pi / 8
    )
    assert sp.simplify(
        breather_action_lattice_adjacent_gap(level, action_quantum)
        - 32 * sp.sin(sp.pi / 32) * sp.cos(5 * sp.pi / 32)
    ) == 0


def test_boosted_breather_vectors_share_the_secant_scale() -> None:
    omega = sp.Rational(4, 5)
    velocity = sp.Rational(3, 5)
    phase = boosted_breather_phase_components(omega, velocity)
    momentum = boosted_breather_energy_momentum(omega, velocity)
    assert phase == (1, sp.Rational(3, 5))
    assert momentum == (12, sp.Rational(36, 5))
    scale = breather_secant_action_scale(omega)
    assert scale == 12
    assert momentum == tuple(sp.simplify(scale * item) for item in phase)


@pytest.mark.parametrize("omega", [0, 1, -sp.Rational(1, 2), 2, sp.I])
def test_numeric_frequency_domain_is_enforced(omega: sp.Expr) -> None:
    with pytest.raises(ValueError, match="0 < omega < 1"):
        breather_threshold_deficit(omega)


@pytest.mark.parametrize("action", [0, 8 * sp.pi, -1, 9 * sp.pi, sp.I])
def test_numeric_action_domain_is_enforced(action: sp.Expr) -> None:
    with pytest.raises(ValueError, match=r"0 < action < 8\*pi"):
        breather_energy_from_action(action)


@pytest.mark.parametrize(
    ("level", "action_quantum", "message"),
    [
        (0, 1, "positive integer"),
        (sp.Rational(1, 2), 1, "positive integer"),
        (1, 0, "real and positive"),
        (1, 8 * sp.pi, r"0 < action < 8\*pi"),
        (2, 3 * sp.pi, r"0 < action < 8\*pi"),
    ],
)
def test_numeric_action_lattice_domain_is_enforced(
    level: sp.Expr, action_quantum: sp.Expr, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        breather_action_lattice_adjacent_gap(level, action_quantum)


@pytest.mark.parametrize("velocity", [-1, 1, 2, sp.I])
def test_numeric_velocity_domain_is_enforced(velocity: sp.Expr) -> None:
    with pytest.raises(ValueError, match=r"abs\(velocity\) < 1"):
        boosted_breather_phase_components(sp.Rational(1, 2), velocity)
