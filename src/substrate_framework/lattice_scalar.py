"""Exact nearest-neighbour scalar-lattice and continuum-limit ledgers.

The spatial lattice is one-dimensional, uniform, and periodic, with positive
spacing ``a``.  In normalized sine-Gordon units the continuum target is

``phi_tt - phi_xx + m**2*sin(phi) = 0``.

This module keeps four statements separate: the exact finite-spacing stencil,
its local smooth-field Taylor expansion, the Riemann-normalized discrete
action, and modewise long-wave convergence.  It does not derive a lattice,
choose its spacing, or establish convergence of nonlinear solutions.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import sympy as sp


def _positive(value: Any, name: str) -> sp.Expr:
    result = sp.sympify(value)
    if result.is_number and (result.is_real is not True or result.is_positive is not True):
        raise ValueError(f"{name} must be positive and real")
    return result


def _nonnegative(value: Any, name: str) -> sp.Expr:
    result = sp.sympify(value)
    if result.is_number and (
        result.is_real is not True or result.is_nonnegative is not True
    ):
        raise ValueError(f"{name} must be nonnegative and real")
    return result


def _periodic_state(values: Sequence[Any], name: str) -> tuple[sp.Expr, ...]:
    result = tuple(sp.sympify(value) for value in values)
    if len(result) < 2:
        raise ValueError(f"{name} must contain at least two periodic sites")
    return result


def forward_difference(left: Any, right: Any, spacing: Any) -> sp.Expr:
    """Return the oriented nearest-neighbour difference ``(right-left)/a``."""

    a = _positive(spacing, "spacing")
    return sp.simplify((sp.sympify(right) - sp.sympify(left)) / a)


def centered_second_difference(
    left: Any,
    center: Any,
    right: Any,
    spacing: Any,
) -> sp.Expr:
    """Return ``(right - 2*center + left)/a**2``."""

    a = _positive(spacing, "spacing")
    return sp.simplify(
        (sp.sympify(right) - 2 * sp.sympify(center) + sp.sympify(left)) / a**2
    )


def centered_taylor_laplacian(
    derivatives: Sequence[Any],
    spacing: Any,
) -> sp.Expr:
    """Derive the centered stencil from a finite Taylor jet.

    ``derivatives[r]`` denotes the derivative of order ``r`` at the center.
    The highest supplied order must be even and at least two.  Both neighbour
    series are constructed explicitly, so cancellation of odd derivatives and
    every surviving factorial coefficient are derived rather than inserted.
    """

    jet = tuple(sp.sympify(value) for value in derivatives)
    highest = len(jet) - 1
    if highest < 2 or highest % 2:
        raise ValueError("Taylor jet must end at an even order of at least two")
    a = _positive(spacing, "spacing")
    plus = sp.Add(
        *(jet[order] * a**order / sp.factorial(order) for order in range(highest + 1))
    )
    minus = sp.Add(
        *(
            jet[order] * (-a) ** order / sp.factorial(order)
            for order in range(highest + 1)
        )
    )
    return sp.expand((plus - 2 * jet[0] + minus) / a**2)


def centered_taylor_remainder_bound(
    spacing: Any,
    next_even_derivative_bound: Any,
    *,
    retained_derivative_order: int = 6,
) -> sp.Expr:
    """Bound the centered-stencil remainder after an even derivative order.

    If ``phi`` has derivative order ``r+2`` bounded by ``M`` on
    ``[x-a,x+a]`` and the modified equation retains even derivatives through
    order ``r``, the two Lagrange remainders give

    ``abs(remainder) <= 2*M*a**r/(r+2)!``.
    """

    if (
        isinstance(retained_derivative_order, bool)
        or retained_derivative_order < 2
        or retained_derivative_order % 2
    ):
        raise ValueError("retained_derivative_order must be an even integer at least two")
    a = _positive(spacing, "spacing")
    bound = _nonnegative(next_even_derivative_bound, "derivative bound")
    return sp.simplify(
        2
        * bound
        * a**retained_derivative_order
        / sp.factorial(retained_derivative_order + 2)
    )


def lattice_laplacian_symbol(wavenumber: Any, spacing: Any) -> sp.Expr:
    """Return the exact centered-Laplacian Fourier symbol.

    For the mode ``exp(I*k*j*a)`` the symbol is
    ``-4*sin(k*a/2)**2/a**2``.  It is even and periodic under
    ``k -> k + 2*pi/a``; a unique physical representative therefore requires
    a declared first-Brillouin-zone convention.
    """

    k = sp.sympify(wavenumber)
    a = _positive(spacing, "spacing")
    return -4 * sp.sin(k * a / 2) ** 2 / a**2


def lattice_spatial_frequency_squared(wavenumber: Any, spacing: Any) -> sp.Expr:
    """Return the nonnegative exact lattice quantity ``-Delta_a(k)``."""

    return -lattice_laplacian_symbol(wavenumber, spacing)


def linearized_lattice_dispersion_squared(
    wavenumber: Any,
    spacing: Any,
    mass: Any = 1,
) -> sp.Expr:
    """Return ``omega**2=m**2+4*sin(k*a/2)**2/a**2``.

    This is the exact plane-wave dispersion of the linearization about a
    cosine-potential minimum.  It is not the nonlinear dispersion of a finite
    amplitude sine-Gordon solution.
    """

    m = _nonnegative(mass, "mass")
    return sp.simplify(m**2 + lattice_spatial_frequency_squared(wavenumber, spacing))


def lattice_mode_relative_deficit(wavenumber: Any, spacing: Any) -> sp.Expr:
    """Return ``1-kappa_a**2/k**2`` for a nonzero continuum wave number.

    The removable ``k=0`` value is zero.  A concrete zero input is rejected so
    callers cannot silently divide by zero; symbolic callers may take the
    limit explicitly.
    """

    k = sp.sympify(wavenumber)
    if k.is_number and sp.simplify(k) == 0:
        raise ValueError("wavenumber must be nonzero for a relative deficit")
    return sp.simplify(1 - lattice_spatial_frequency_squared(k, spacing) / k**2)


def periodic_lattice_lagrangian(
    field: Sequence[Any],
    velocity: Sequence[Any],
    spacing: Any,
    mass: Any = 1,
) -> sp.Expr:
    """Return the Riemann-normalized periodic lattice Lagrangian.

    For ``N`` sites this is

    ``a*sum_j[dot(phi_j)**2/2 - ((phi_(j+1)-phi_j)/a)**2/2
              - m**2*(1-cos(phi_j))]``.

    The wraparound bond from site ``N-1`` to site zero is included exactly.
    """

    phi = _periodic_state(field, "field")
    speed = _periodic_state(velocity, "velocity")
    if len(phi) != len(speed):
        raise ValueError("field and velocity must have the same number of sites")
    a = _positive(spacing, "spacing")
    m = _nonnegative(mass, "mass")
    density = []
    for index, value in enumerate(phi):
        gradient = forward_difference(value, phi[(index + 1) % len(phi)], a)
        density.append(
            speed[index] ** 2 / 2
            - gradient**2 / 2
            - m**2 * (1 - sp.cos(value))
        )
    return sp.simplify(a * sp.Add(*density))


def periodic_lattice_eom_residual(
    field: Sequence[Any],
    acceleration: Sequence[Any],
    spacing: Any,
    mass: Any = 1,
) -> tuple[sp.Expr, ...]:
    """Return every exact periodic discrete sine-Gordon EOM residual.

    Each entry is ``ddot(phi_j)-Delta_a(phi)_j+m**2*sin(phi_j)`` and follows
    from :func:`periodic_lattice_lagrangian` by sitewise variation.
    """

    phi = _periodic_state(field, "field")
    accel = _periodic_state(acceleration, "acceleration")
    if len(phi) != len(accel):
        raise ValueError("field and acceleration must have the same number of sites")
    a = _positive(spacing, "spacing")
    m = _nonnegative(mass, "mass")
    return tuple(
        sp.simplify(
            accel[index]
            - centered_second_difference(
                phi[(index - 1) % len(phi)],
                value,
                phi[(index + 1) % len(phi)],
                a,
            )
            + m**2 * sp.sin(value)
        )
        for index, value in enumerate(phi)
    )


def periodic_action_error_bound(
    length: Any,
    time_duration: Any,
    spacing: Any,
    max_abs_phi_x: Any,
    max_abs_phi_xx: Any,
    max_abs_phi_t: Any,
    max_abs_phi_tx: Any,
    mass: Any = 1,
) -> sp.Expr:
    """Return a sufficient sampled-action error bound for a smooth field.

    Let ``a=L/N`` and sample an ``L``-periodic field on left endpoints.  Assume
    the four supplied uniform derivative bounds hold on the space-time
    cylinder.  The left-Riemann error and the forward-gradient Taylor error
    give the absolute action difference bound

    ``T*L*(a*Mt*Mtx/2 + a*m**2*Mx/2 + a*Mx*Mxx
            + a**2*Mxx**2/8)``.

    Hence the sampled discrete action converges to the continuum action at
    least linearly as ``a -> 0`` under these fixed bounds.  This is an action
    statement, not a nonlinear solution-convergence theorem.
    """

    interval = _positive(length, "length")
    duration = _positive(time_duration, "time duration")
    a = _positive(spacing, "spacing")
    mx = _nonnegative(max_abs_phi_x, "max_abs_phi_x")
    mxx = _nonnegative(max_abs_phi_xx, "max_abs_phi_xx")
    mt = _nonnegative(max_abs_phi_t, "max_abs_phi_t")
    mtx = _nonnegative(max_abs_phi_tx, "max_abs_phi_tx")
    m = _nonnegative(mass, "mass")
    instantaneous = (
        a * mt * mtx / 2
        + a * m**2 * mx / 2
        + a * mx * mxx
        + a**2 * mxx**2 / 8
    )
    return sp.simplify(duration * interval * instantaneous)
