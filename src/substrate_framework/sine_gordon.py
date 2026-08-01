"""Exact normalized sine-Gordon breather definitions.

The convention is

``phi_tt - phi_xx + sin(phi) = 0``

with Hamiltonian density ``(phi_t**2 + phi_x**2)/2 + 1 - cos(phi)``.
Coordinates and fields are dimensionless (``c = m = beta = 1``).  Breather
frequencies lie in the open interval ``0 < omega < 1``.
"""

from __future__ import annotations

from typing import Any

import sympy as sp


def _frequency(omega: Any) -> sp.Expr:
    value = sp.sympify(omega)
    if value.is_number:
        if value.is_real is not True or not 0.0 < float(value) < 1.0:
            raise ValueError("omega must be real and satisfy 0 < omega < 1")
    return value


def _velocity(velocity: Any) -> sp.Expr:
    value = sp.sympify(velocity)
    if value.is_number:
        if value.is_real is not True or not abs(float(value)) < 1.0:
            raise ValueError("velocity must be real and satisfy abs(velocity) < 1")
    return value


def _action(action: Any) -> sp.Expr:
    value = sp.sympify(action)
    if value.is_number:
        if value.is_real is not True or not 0.0 < float(value) < float(8 * sp.pi):
            raise ValueError("action must be real and satisfy 0 < action < 8*pi")
    return value


def _positive_action_quantum(action_quantum: Any) -> sp.Expr:
    value = sp.sympify(action_quantum)
    if value.is_number:
        if value.is_real is not True or not float(value) > 0.0:
            raise ValueError("action_quantum must be real and positive")
    return value


def _positive_integer_level(level: Any) -> sp.Expr:
    value = sp.sympify(level)
    if value.is_number:
        if value.is_integer is not True or int(value) <= 0:
            raise ValueError("level must be a positive integer")
    return value


def _lattice_action(level: Any, action_quantum: Any, offset: int = 0) -> sp.Expr:
    level_value = _positive_integer_level(level)
    quantum = _positive_action_quantum(action_quantum)
    return _action((level_value + offset) * quantum)


def breather_inverse_width(omega: Any) -> sp.Expr:
    """Return ``eta = sqrt(1 - omega**2)`` in normalized units."""

    frequency = _frequency(omega)
    return sp.sqrt(1 - frequency**2)


def breather_field_with_width(x: Any, t: Any, omega: Any, eta: Any) -> sp.Expr:
    """Return the direct arctangent profile for an explicit inverse width.

    This lower-level construction is on shell only when
    ``eta**2 + omega**2 = 1``.  Exposing ``eta`` makes that load-bearing
    relation available to verifier mutations without redefining the profile.
    """

    coordinate = sp.sympify(x)
    time = sp.sympify(t)
    frequency = _frequency(omega)
    inverse_width = sp.sympify(eta)
    argument = (
        inverse_width
        * sp.sin(frequency * time)
        / (frequency * sp.cosh(inverse_width * coordinate))
    )
    return 4 * sp.atan(argument)


def breather_field(x: Any, t: Any, omega: Any) -> sp.Expr:
    """Return the exact rest-frame breather field for ``0 < omega < 1``."""

    frequency = _frequency(omega)
    return breather_field_with_width(
        x, t, frequency, breather_inverse_width(frequency)
    )


def sine_gordon_residual(field: Any, x: sp.Symbol, t: sp.Symbol) -> sp.Expr:
    """Return ``phi_tt - phi_xx + sin(phi)`` for a symbolic field."""

    expression = sp.sympify(field)
    return sp.diff(expression, t, 2) - sp.diff(expression, x, 2) + sp.sin(expression)


def naive_chiral_currents(
    field: Any,
    x: sp.Symbol,
    t: sp.Symbol,
) -> tuple[sp.Expr, sp.Expr]:
    """Return the characteristic derivatives ``(J_plus, J_minus)``.

    The convention is ``J_plus=phi_t+phi_x`` and
    ``J_minus=phi_t-phi_x``.  These are not independently conserved in the
    normalized sine-Gordon theory.
    """

    expression = sp.sympify(field)
    field_t = sp.diff(expression, t)
    field_x = sp.diff(expression, x)
    return sp.simplify(field_t + field_x), sp.simplify(field_t - field_x)


def naive_chiral_transport_defects(
    field: Any,
    x: sp.Symbol,
    t: sp.Symbol,
) -> tuple[sp.Expr, sp.Expr]:
    """Return ``(d_t J_plus-d_x J_plus, d_t J_minus+d_x J_minus)``.

    Both entries equal ``phi_tt-phi_xx`` off shell.  On the sine-Gordon
    equation they therefore equal ``-sin(phi)``; with light-cone derivatives
    ``d_plus=(d_t+d_x)/2`` and ``d_minus=(d_t-d_x)/2``, both corresponding
    sources are ``-sin(phi)/2``.
    """

    current_plus, current_minus = naive_chiral_currents(field, x, t)
    return (
        sp.simplify(sp.diff(current_plus, t) - sp.diff(current_plus, x)),
        sp.simplify(sp.diff(current_minus, t) + sp.diff(current_minus, x)),
    )


def sine_gordon_chiral_sources(field: Any) -> tuple[sp.Expr, sp.Expr]:
    """Return the two on-shell transport sources ``(-sin(phi), -sin(phi))``."""

    source = -sp.sin(sp.sympify(field))
    return source, source


def sine_gordon_light_cone_chiral_sources(
    field: Any,
) -> tuple[sp.Expr, sp.Expr]:
    """Return ``(d_minus J_plus, d_plus J_minus)`` on shell.

    Light-cone derivatives include the explicit one-half convention.
    """

    source_plus, source_minus = sine_gordon_chiral_sources(field)
    return sp.simplify(source_plus / 2), sp.simplify(source_minus / 2)


def topological_current(
    field: Any,
    x: sp.Symbol,
    t: sp.Symbol,
) -> tuple[sp.Expr, sp.Expr]:
    """Return ``(j0,j1)=(phi_x,-phi_t)/(2*pi)`` for ``epsilon**01=+1``.

    This current is distinct from the Noether current of an independently
    declared complex field.  Its divergence vanishes identically for every
    sufficiently smooth real field, without using the sine-Gordon equation.
    """

    expression = sp.sympify(field)
    return (
        sp.diff(expression, x) / (2 * sp.pi),
        -sp.diff(expression, t) / (2 * sp.pi),
    )


def topological_current_divergence(
    field: Any,
    x: sp.Symbol,
    t: sp.Symbol,
) -> sp.Expr:
    """Return ``d_t j0+d_x j1``, an off-shell mixed-partial identity."""

    density, flux = topological_current(field, x, t)
    return sp.simplify(sp.diff(density, t) + sp.diff(flux, x))


def topological_charge_from_boundaries(
    field_minus_infinity: Any,
    field_plus_infinity: Any,
) -> sp.Expr:
    """Return ``(phi(+infinity)-phi(-infinity))/(2*pi)``.

    Existence of the two boundary limits is a caller hypothesis.  The result
    is integer-valued only when both limits are sine-Gordon vacua ``2*pi*n``.
    """

    lower = sp.sympify(field_minus_infinity)
    upper = sp.sympify(field_plus_infinity)
    return sp.simplify((upper - lower) / (2 * sp.pi))


def spatial_parity_transform(field: Any, x: sp.Symbol) -> sp.Expr:
    """Return the scalar-field parity image ``phi(t,-x)``."""

    return sp.sympify(field).subs(x, -x)


def static_kink_field(
    x: Any,
    center: Any = 0,
    orientation: int = 1,
) -> sp.Expr:
    """Return the unit kink or antikink ``4*atan(exp(s*(x-x0)))``.

    ``orientation=1`` has winding ``+1`` and ``orientation=-1`` has winding
    ``-1``.  Both are static solutions in the normalized convention.
    """

    if orientation not in (-1, 1):
        raise ValueError("orientation must be +1 or -1")
    coordinate = sp.sympify(x)
    origin = sp.sympify(center)
    return 4 * sp.atan(sp.exp(orientation * (coordinate - origin)))


def hamiltonian_density(field: Any, x: sp.Symbol, t: sp.Symbol) -> sp.Expr:
    """Return the normalized sine-Gordon Hamiltonian density."""

    expression = sp.sympify(field)
    return (
        sp.diff(expression, t) ** 2 / 2
        + sp.diff(expression, x) ** 2 / 2
        + 1
        - sp.cos(expression)
    )


def breather_energy(omega: Any) -> sp.Expr:
    """Return the exact conserved rest energy ``16*sqrt(1-omega**2)``."""

    return 16 * breather_inverse_width(omega)


def breather_energy_second_moment(
    omega: Any,
    time: Any,
) -> sp.Expr:
    """Return ``integral_R x**2*T00(x,t) dx`` for the rest breather.

    This is a scalar width functional of the normalized 1+1 Hamiltonian
    density.  It is not a three-dimensional STF mass quadrupole.  The exact
    result follows from the spatial Fourier transform of
    ``1/(cosh(y)**2 + b**2)`` with
    ``y=sqrt(1-omega**2)*x`` and
    ``b=sqrt(1-omega**2)*sin(omega*t)/omega``.
    """

    frequency = _frequency(omega)
    instant = sp.sympify(time)
    inverse_width = breather_inverse_width(frequency)
    phase_ratio = (
        inverse_width * sp.sin(frequency * instant) / frequency
    )
    return sp.simplify(
        4 * sp.pi**2 / (3 * inverse_width)
        + 16 * sp.asinh(phase_ratio) ** 2 / inverse_width
    )


def breather_energy_second_moment_derivative(
    omega: Any,
    time: Any,
    order: int,
) -> sp.Expr:
    """Return an exact time derivative of the breather energy moment.

    A private symbolic time is differentiated before the requested instant is
    substituted, so callers may use either a symbolic coordinate or an exact
    numeric instant.  This remains a derivative of the centered scalar 1+1
    energy moment; it does not construct a three-dimensional source.
    """

    derivative_order = sp.sympify(order)
    if derivative_order.is_integer is not True or int(derivative_order) < 0:
        raise ValueError("order must be a nonnegative integer")
    frequency = _frequency(omega)
    instant = sp.sympify(time)
    auxiliary_time = sp.Dummy("moment_time", real=True)
    moment = breather_energy_second_moment(frequency, auxiliary_time)
    return sp.simplify(
        sp.diff(moment, auxiliary_time, int(derivative_order)).subs(
            auxiliary_time,
            instant,
        )
    )


def breather_energy_second_moment_extrema(
    omega: Any,
) -> tuple[sp.Expr, sp.Expr]:
    """Return the exact minimum and maximum over a rest-breather cycle."""

    frequency = _frequency(omega)
    inverse_width = breather_inverse_width(frequency)
    minimum = 4 * sp.pi**2 / (3 * inverse_width)
    maximum = minimum + 16 * sp.asinh(inverse_width / frequency) ** 2 / inverse_width
    return sp.simplify(minimum), sp.simplify(maximum)


def breather_threshold_deficit(omega: Any) -> sp.Expr:
    """Return the energy deficit ``16-E(omega)`` below the two-kink threshold."""

    return sp.simplify(16 - breather_energy(omega))


def breather_secant_action_scale(omega: Any) -> sp.Expr:
    """Return the energy-frequency secant scale ``H = E(omega)/omega``.

    The result has action dimension in dimensional conventions, but it is not
    the canonical action variable returned by :func:`breather_action`.
    """

    frequency = _frequency(omega)
    return sp.simplify(breather_energy(frequency) / frequency)


def lorentz_factor(velocity: Any) -> sp.Expr:
    """Return ``gamma = 1/sqrt(1-v**2)`` for ``|v|<1`` in units ``c=1``."""

    speed = _velocity(velocity)
    return 1 / sp.sqrt(1 - speed**2)


def boosted_breather_phase_components(
    omega: Any, velocity: Any
) -> tuple[sp.Expr, sp.Expr]:
    """Return ``(Omega, k)`` for phase ``Omega*t-k*x`` after a boost."""

    frequency = _frequency(omega)
    speed = _velocity(velocity)
    gamma = lorentz_factor(speed)
    return sp.simplify(gamma * frequency), sp.simplify(
        gamma * frequency * speed
    )


def boosted_breather_energy_momentum(
    omega: Any, velocity: Any
) -> tuple[sp.Expr, sp.Expr]:
    """Return the boosted breather ``(E, P)`` in normalized units ``c=1``."""

    frequency = _frequency(omega)
    speed = _velocity(velocity)
    gamma = lorentz_factor(speed)
    rest_energy = breather_energy(frequency)
    return sp.simplify(gamma * rest_energy), sp.simplify(
        gamma * rest_energy * speed
    )


def breather_action_secant_ratio(omega: Any) -> sp.Expr:
    """Return the dimensionless ratio ``J(omega)/(E(omega)/omega)``."""

    frequency = _frequency(omega)
    return sp.simplify(
        breather_action(frequency) / breather_secant_action_scale(frequency)
    )


def breather_period(omega: Any) -> sp.Expr:
    """Return the time period ``2*pi/omega``."""

    return 2 * sp.pi / _frequency(omega)


def breather_peak_amplitude(omega: Any) -> sp.Expr:
    """Return the positive peak field amplitude at the spatial center."""

    frequency = _frequency(omega)
    return 4 * sp.atan(breather_inverse_width(frequency) / frequency)


def breather_action(omega: Any) -> sp.Expr:
    """Return the canonical action variable ``J = 16*acos(omega)``."""

    return 16 * sp.acos(_frequency(omega))


def breather_frequency_from_action(action: Any) -> sp.Expr:
    """Return ``omega = cos(J/16)`` for ``0 < J < 8*pi``."""

    return sp.cos(_action(action) / 16)


def breather_energy_from_action(action: Any) -> sp.Expr:
    """Return ``E = 16*sin(J/16)`` for ``0 < J < 8*pi``."""

    return 16 * sp.sin(_action(action) / 16)


def breather_action_lattice_frequency(level: Any, action_quantum: Any) -> sp.Expr:
    """Return ``cos(n*h/16)`` conditional on ``J_n=n*h`` in the action domain."""

    return breather_frequency_from_action(_lattice_action(level, action_quantum))


def breather_action_lattice_energy(level: Any, action_quantum: Any) -> sp.Expr:
    """Return ``16*sin(n*h/16)`` conditional on ``J_n=n*h``."""

    return breather_energy_from_action(_lattice_action(level, action_quantum))


def breather_action_lattice_adjacent_gap(
    level: Any, action_quantum: Any
) -> sp.Expr:
    """Return the exact adjacent gap ``E_(n+1)-E_n``.

    Both ``n*h`` and ``(n+1)*h`` must lie in the accepted open action domain.
    """

    current_action = _lattice_action(level, action_quantum)
    next_action = _lattice_action(level, action_quantum, offset=1)
    return sp.simplify(
        breather_energy_from_action(next_action)
        - breather_energy_from_action(current_action)
    )


def breather_mean_gradient_integral(omega: Any) -> sp.Expr:
    """Return the period average of ``integral(phi_x**2, x)``.

    This is the squared-gradient integral itself, not the half-weighted
    gradient contribution to the Hamiltonian.
    """

    frequency = _frequency(omega)
    return sp.simplify(
        breather_energy(frequency) - frequency * breather_action(frequency)
    )
