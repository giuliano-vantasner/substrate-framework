from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.damped_oscillator import (
    damped_oscillator_characteristic_roots,
    damped_oscillator_discriminant,
    damped_oscillator_regime,
    mechanical_energy_derivative_on_shell,
    nominal_cycles_per_quadratic_envelope_efold,
    normalized_damped_sine_gordon_mode_residual,
    normalized_sine_gordon_mode_critical_damping,
    normalized_sine_gordon_mode_natural_frequency,
    oscillator_amplitude_envelope_efold_time,
    oscillator_amplitude_envelope_factor,
    oscillator_mechanical_energy,
    oscillator_quadratic_envelope_efold_time,
    oscillator_quadratic_envelope_factor,
    period_integrated_energy_change,
    underdamped_angular_frequency,
    underdamped_cycles_per_quadratic_envelope_efold,
    underdamped_oscillator_solution,
)


def test_characteristic_roots_and_regimes_are_exact() -> None:
    omega_0, gamma, root = sp.symbols("omega_0 Gamma r", positive=True, real=True)
    roots = damped_oscillator_characteristic_roots(omega_0, gamma)
    polynomial = root**2 + gamma * root + omega_0**2
    assert all(sp.simplify(polynomial.subs(root, item)) == 0 for item in roots)
    assert damped_oscillator_discriminant(1, sp.Rational(1, 2)) == -sp.Rational(
        15, 4
    )
    assert damped_oscillator_regime(1, sp.Rational(1, 2)) == "underdamped"
    assert damped_oscillator_regime(1, 2) == "critical"
    assert damped_oscillator_regime(1, 3) == "overdamped"


def test_underdamped_solution_satisfies_declared_ode() -> None:
    t = sp.symbols("t", real=True)
    omega_0, gamma = sp.symbols("omega_0 Gamma", positive=True, real=True)
    cosine, sine = sp.symbols("A B", real=True)
    solution = underdamped_oscillator_solution(
        t,
        omega_0,
        gamma,
        cosine,
        sine,
    )
    residual = (
        sp.diff(solution, t, 2)
        + gamma * sp.diff(solution, t)
        + omega_0**2 * solution
    )
    assert sp.simplify(sp.expand_trig(residual)) == 0


def test_envelopes_and_cycle_conventions_are_not_conflated() -> None:
    gamma, t = sp.symbols("Gamma t", positive=True, real=True)
    assert oscillator_amplitude_envelope_factor(gamma, t) == sp.exp(-gamma * t / 2)
    assert oscillator_quadratic_envelope_factor(gamma, t) == sp.exp(-gamma * t)
    assert oscillator_amplitude_envelope_efold_time(gamma) == 2 / gamma
    assert oscillator_quadratic_envelope_efold_time(gamma) == 1 / gamma

    assert nominal_cycles_per_quadratic_envelope_efold(1, 1) == 1 / (2 * sp.pi)
    assert underdamped_cycles_per_quadratic_envelope_efold(1, 1) == (
        sp.sqrt(3) / (4 * sp.pi)
    )
    assert sp.limit(
        underdamped_cycles_per_quadratic_envelope_efold(1, gamma),
        gamma,
        2,
        dir="-",
    ) == 0
    assert nominal_cycles_per_quadratic_envelope_efold(1, 2) == 1 / (4 * sp.pi)


def test_mechanical_energy_has_exact_phase_dependent_balance() -> None:
    t = sp.symbols("t", real=True)
    omega_0, gamma = sp.symbols("omega_0 Gamma", positive=True, real=True)
    displacement = sp.Function("q")(t)
    velocity = sp.diff(displacement, t)
    energy = oscillator_mechanical_energy(displacement, velocity, omega_0)
    on_shell = sp.diff(energy, t).subs(
        sp.diff(displacement, t, 2),
        -gamma * velocity - omega_0**2 * displacement,
    )
    assert sp.simplify(
        on_shell - mechanical_energy_derivative_on_shell(velocity, gamma)
    ) == 0

    # At a turning point, exact energy loss vanishes instantaneously even
    # though a pointwise E'=-Gamma*E exponential model predicts nonzero loss.
    assert mechanical_energy_derivative_on_shell(0, gamma) == 0
    assert -gamma * oscillator_mechanical_energy(1, 0, omega_0) != 0


def test_normalized_sine_gordon_modes_have_gap_one() -> None:
    k = sp.symbols("k", real=True)
    assert normalized_sine_gordon_mode_natural_frequency(k) == sp.sqrt(k**2 + 1)
    assert normalized_sine_gordon_mode_natural_frequency(0) == 1
    assert normalized_sine_gordon_mode_critical_damping(0) == 2

    t = sp.symbols("t", real=True)
    gamma = sp.Rational(6, 5)
    mode = underdamped_oscillator_solution(t, 1, gamma, 1, 0)
    assert sp.simplify(
        normalized_damped_sine_gordon_mode_residual(mode, t, 0, gamma)
    ) == 0

    # Same Gamma, but substituting a sub-gap breather frequency as omega_0
    # reverses the classification. That substitution is not a real SG mode.
    assert damped_oscillator_regime(1, gamma) == "underdamped"
    assert damped_oscillator_regime(sp.Rational(1, 2), gamma) == "overdamped"


def test_positive_damping_excludes_nontrivial_exact_periodicity() -> None:
    gamma, loss = sp.symbols("Gamma I", positive=True, real=True)
    assert period_integrated_energy_change(gamma, loss) == -gamma * loss
    assert period_integrated_energy_change(1, 3) == -3
    assert period_integrated_energy_change(1, 0) == 0
    assert period_integrated_energy_change(1, 3, 3) == 0
    assert period_integrated_energy_change(1, 3, -3) == -6


@pytest.mark.parametrize(
    ("call", "match"),
    [
        (lambda: damped_oscillator_characteristic_roots(0, 1), "omega_0"),
        (lambda: damped_oscillator_characteristic_roots(1, -1), "gamma"),
        (lambda: underdamped_angular_frequency(1, 2), "underdamped"),
        (lambda: oscillator_quadratic_envelope_efold_time(0), "gamma"),
        (lambda: normalized_sine_gordon_mode_natural_frequency(sp.I), "wavenumber"),
        (lambda: period_integrated_energy_change(1, -1), "velocity_square"),
    ],
)
def test_invalid_numeric_inputs_are_rejected(call: object, match: str) -> None:
    with pytest.raises(ValueError, match=match):
        call()  # type: ignore[operator]


def test_undecidable_symbolic_regime_is_not_guessed() -> None:
    omega_0, gamma = sp.symbols("omega_0 Gamma", positive=True, real=True)
    with pytest.raises(ValueError, match="undecidable"):
        damped_oscillator_regime(omega_0, gamma)
