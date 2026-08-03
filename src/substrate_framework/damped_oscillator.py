"""Exact linearly damped oscillator identities and sine-Gordon mode mapping.

The abstract oscillator convention is

``q_tt + gamma*q_t + omega_0**2*q = 0``.

For the normalized damped sine-Gordon linearization

``psi_tt - psi_xx + psi = -gamma*psi_t``,

a real spatial Fourier mode with wavenumber ``k`` has
``omega_0=sqrt(1+k**2)``.  This module keeps natural frequency, damped
frequency, amplitude envelope, quadratic envelope, instantaneous mechanical
energy, and exact periodic existence as separate concepts.
"""

from __future__ import annotations

from typing import Any

import sympy as sp


def _positive_real(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_number:
        if expression.is_real is not True or not float(expression) > 0.0:
            raise ValueError(f"{name} must be real and positive")
    return expression


def _nonnegative_real(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_number:
        if expression.is_real is not True or float(expression) < 0.0:
            raise ValueError(f"{name} must be real and nonnegative")
    return expression


def _real(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_number and expression.is_real is not True:
        raise ValueError(f"{name} must be real")
    return expression


def damped_oscillator_discriminant(omega_0: Any, gamma: Any) -> sp.Expr:
    """Return ``gamma**2-4*omega_0**2`` for the characteristic polynomial."""

    frequency = _positive_real(omega_0, "omega_0")
    damping = _nonnegative_real(gamma, "gamma")
    return sp.expand(damping**2 - 4 * frequency**2)


def damped_oscillator_characteristic_roots(
    omega_0: Any,
    gamma: Any,
) -> tuple[sp.Expr, sp.Expr]:
    """Return the two exact roots of ``r**2+gamma*r+omega_0**2``."""

    frequency = _positive_real(omega_0, "omega_0")
    damping = _nonnegative_real(gamma, "gamma")
    radical = sp.sqrt(damping**2 - 4 * frequency**2)
    return (
        sp.simplify((-damping + radical) / 2),
        sp.simplify((-damping - radical) / 2),
    )


def damped_oscillator_regime(omega_0: Any, gamma: Any) -> str:
    """Return ``underdamped``, ``critical``, or ``overdamped`` when decidable.

    Symbolic inputs whose ordering cannot be inferred raise ``ValueError``;
    callers must state the missing inequality instead of receiving a guessed
    branch.
    """

    discriminant = sp.simplify(damped_oscillator_discriminant(omega_0, gamma))
    if discriminant.is_negative is True:
        return "underdamped"
    if discriminant.is_zero is True:
        return "critical"
    if discriminant.is_positive is True:
        return "overdamped"
    raise ValueError("oscillator regime is undecidable without an ordering assumption")


def underdamped_angular_frequency(omega_0: Any, gamma: Any) -> sp.Expr:
    """Return ``sqrt(omega_0**2-gamma**2/4)``.

    Numeric inputs are required to be strictly underdamped.  For symbolic
    inputs, the caller is responsible for the assumption ``gamma<2*omega_0``.
    """

    frequency = _positive_real(omega_0, "omega_0")
    damping = _nonnegative_real(gamma, "gamma")
    if frequency.is_number and damping.is_number:
        if not float(damping) < 2.0 * float(frequency):
            raise ValueError("underdamped frequency requires gamma < 2*omega_0")
    return sp.sqrt(frequency**2 - damping**2 / 4)


def underdamped_oscillator_solution(
    time: Any,
    omega_0: Any,
    gamma: Any,
    cosine_coefficient: Any,
    sine_coefficient: Any,
) -> sp.Expr:
    """Return the general real underdamped solution in coefficient form."""

    t = _real(time, "time")
    damping = _nonnegative_real(gamma, "gamma")
    omega_d = underdamped_angular_frequency(omega_0, damping)
    cosine = sp.sympify(cosine_coefficient)
    sine = sp.sympify(sine_coefficient)
    return sp.exp(-damping * t / 2) * (
        cosine * sp.cos(omega_d * t) + sine * sp.sin(omega_d * t)
    )


def oscillator_amplitude_envelope_factor(gamma: Any, time: Any) -> sp.Expr:
    """Return the underdamped coordinate-envelope factor ``exp(-gamma*t/2)``."""

    damping = _nonnegative_real(gamma, "gamma")
    t = _real(time, "time")
    return sp.exp(-damping * t / 2)


def oscillator_quadratic_envelope_factor(gamma: Any, time: Any) -> sp.Expr:
    """Return ``exp(-gamma*t)``, the square of the amplitude envelope.

    This is not a claim that instantaneous mechanical energy is exactly a
    single exponential; its phase-dependent kinetic and potential parts obey
    the exact balance returned by :func:`mechanical_energy_derivative_on_shell`.
    """

    amplitude_factor = oscillator_amplitude_envelope_factor(gamma, time)
    return sp.simplify(amplitude_factor**2)


def oscillator_amplitude_envelope_efold_time(gamma: Any) -> sp.Expr:
    """Return ``2/gamma`` for the coordinate-amplitude envelope."""

    damping = _positive_real(gamma, "gamma")
    return 2 / damping


def oscillator_quadratic_envelope_efold_time(gamma: Any) -> sp.Expr:
    """Return ``1/gamma`` for the quadratic-amplitude envelope."""

    damping = _positive_real(gamma, "gamma")
    return 1 / damping


def nominal_cycles_per_quadratic_envelope_efold(
    omega_0: Any,
    gamma: Any,
) -> sp.Expr:
    """Return ``omega_0/(2*pi*gamma)`` using the undamped natural frequency.

    This weak-damping convention is nominal.  It is not the actual oscillation
    count near the critical boundary.
    """

    frequency = _positive_real(omega_0, "omega_0")
    damping = _positive_real(gamma, "gamma")
    return frequency / (2 * sp.pi * damping)


def underdamped_cycles_per_quadratic_envelope_efold(
    omega_0: Any,
    gamma: Any,
) -> sp.Expr:
    """Return ``omega_d/(2*pi*gamma)`` in a ``1/gamma`` envelope window."""

    damping = _positive_real(gamma, "gamma")
    return underdamped_angular_frequency(omega_0, damping) / (
        2 * sp.pi * damping
    )


def oscillator_mechanical_energy(
    displacement: Any,
    velocity: Any,
    omega_0: Any,
) -> sp.Expr:
    """Return ``(velocity**2+omega_0**2*displacement**2)/2``."""

    position = sp.sympify(displacement)
    speed = sp.sympify(velocity)
    frequency = _positive_real(omega_0, "omega_0")
    return sp.expand((speed**2 + frequency**2 * position**2) / 2)


def mechanical_energy_derivative_on_shell(velocity: Any, gamma: Any) -> sp.Expr:
    """Return the exact oscillator balance ``dE/dt=-gamma*velocity**2``."""

    speed = sp.sympify(velocity)
    damping = _nonnegative_real(gamma, "gamma")
    return sp.expand(-damping * speed**2)


def normalized_sine_gordon_mode_natural_frequency(wavenumber: Any) -> sp.Expr:
    """Return ``sqrt(1+k**2)`` for a real Fourier mode of the linearization."""

    k = _real(wavenumber, "wavenumber")
    return sp.sqrt(1 + k**2)


def normalized_sine_gordon_mode_critical_damping(wavenumber: Any) -> sp.Expr:
    """Return ``2*sqrt(1+k**2)`` for the mode's critical damping value."""

    return 2 * normalized_sine_gordon_mode_natural_frequency(wavenumber)


def normalized_damped_sine_gordon_mode_residual(
    mode_amplitude: Any,
    time: sp.Symbol,
    wavenumber: Any,
    gamma: Any,
) -> sp.Expr:
    """Return the Fourier-mode ODE residual ``q_tt+gamma*q_t+(1+k**2)q``."""

    amplitude = sp.sympify(mode_amplitude)
    k = _real(wavenumber, "wavenumber")
    damping = _nonnegative_real(gamma, "gamma")
    return sp.expand(
        sp.diff(amplitude, time, 2)
        + damping * sp.diff(amplitude, time)
        + (1 + k**2) * amplitude
    )


def period_integrated_energy_change(
    gamma: Any,
    integrated_velocity_square: Any,
    integrated_boundary_flux: Any = 0,
) -> sp.Expr:
    """Return the exact energy change over a declared time interval.

    The normalized damped sine-Gordon identity is
    ``Delta E = integrated_boundary_flux - gamma*integral(phi_t**2 dx dt)``.
    For a periodic finite-energy field with vanishing boundary flux,
    ``Delta E=0`` and positive ``gamma`` force the nonnegative velocity-square
    integral to vanish.  The caller remains responsible for regularity and
    boundary hypotheses.
    """

    damping = _nonnegative_real(gamma, "gamma")
    loss_integral = _nonnegative_real(
        integrated_velocity_square,
        "integrated_velocity_square",
    )
    boundary_flux = sp.sympify(integrated_boundary_flux)
    return sp.expand(boundary_flux - damping * loss_integral)
