"""Exact composition of paired-loss magnitudes with finite-window cycle factors.

The functions in this module compose conditional factors governed elsewhere in
the framework.  They do not turn a finite resolvent matrix element into a
probability or rate, and the nominal cycle count is not a phase-coherence or
survival observable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import sympy as sp

from substrate_framework.coherence_gates import activated_relative_response
from substrate_framework.damped_oscillator import (
    nominal_cycles_per_quadratic_envelope_efold,
    underdamped_cycles_per_quadratic_envelope_efold,
)
from substrate_framework.thermal import symmetric_two_level_gate


def _exact_real(value: Any, *, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.has(sp.Float):
        raise ValueError(f"{name} must be exact rather than floating")
    if expression.is_real is not True:
        raise ValueError(f"{name} must be explicitly real")
    return expression


def _exact_positive(value: Any, *, name: str) -> sp.Expr:
    expression = _exact_real(value, name=name)
    if expression.is_positive is not True:
        raise ValueError(f"{name} must be explicitly positive")
    return expression


def _exact_nonnegative(value: Any, *, name: str) -> sp.Expr:
    expression = _exact_real(value, name=name)
    if expression.is_nonnegative is not True:
        raise ValueError(f"{name} must be explicitly nonnegative")
    return expression


def _exact_nonzero(value: Any, *, name: str) -> sp.Expr:
    expression = _exact_real(value, name=name)
    if expression.is_zero is not False:
        raise ValueError(f"{name} must be explicitly nonzero")
    return expression


def _positive_integer(value: Any, *, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.has(sp.Float):
        raise ValueError(f"{name} must be exact rather than floating")
    if expression.is_integer is not True or expression.is_positive is not True:
        raise ValueError(f"{name} must be a positive integer")
    return expression


def _validated_pairs(
    detunings: Sequence[Any],
    coupling_products: Sequence[Any],
) -> tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]]:
    try:
        exact_detunings = tuple(
            _exact_nonzero(value, name=f"detunings[{index}]")
            for index, value in enumerate(detunings)
        )
        exact_products = tuple(
            _exact_nonnegative(value, name=f"coupling_products[{index}]")
            for index, value in enumerate(coupling_products)
        )
    except TypeError as error:
        raise ValueError("detunings and coupling_products must be finite sequences") from error
    if not exact_detunings or len(exact_detunings) != len(exact_products):
        raise ValueError("pair sequences must be nonempty and have equal length")
    if not any(product.is_positive is True for product in exact_products):
        raise ValueError("at least one coupling product must be explicitly positive")
    return exact_detunings, exact_products


def _positive_pair_kernel(
    detunings: Sequence[Any],
    coupling_products: Sequence[Any],
    loss: Any,
) -> tuple[sp.Expr, tuple[sp.Expr, ...], tuple[sp.Expr, ...]]:
    gamma = _exact_nonnegative(loss, name="loss")
    deltas, products = _validated_pairs(detunings, coupling_products)
    kernel = sp.simplify(
        sum(
            (
                product / (delta**2 + gamma**2 / 4)
                for delta, product in zip(deltas, products, strict=True)
            ),
            sp.Integer(0),
        )
    )
    return kernel, deltas, products


@dataclass(frozen=True)
class LossCycleComposition:
    """Exact open-interval and endpoint data for one declared composition."""

    pair_magnitude: sp.Expr
    nominal_cycles: sp.Expr
    nominal_product: sp.Expr
    nominal_loss_derivative: sp.Expr
    actual_cycles: sp.Expr
    actual_product: sp.Expr
    zero_loss_limit: sp.Expr
    nominal_critical_left_limit: sp.Expr
    actual_critical_left_limit: sp.Expr
    large_loss_inverse_square_coefficient: sp.Expr


def common_loss_pair_magnitude(
    detunings: Sequence[Any],
    coupling_products: Sequence[Any],
    loss: Any,
) -> sp.Expr:
    r"""Return ``Gamma*sum_j c_j/(Delta_j**2+Gamma**2/4)``.

    This is the magnitude of the common-loss, zero-energy C-RES-001 sum when
    the coupling products are real and nonnegative and at least one is
    positive.  It is a finite matrix-element magnitude, not a rate.
    """

    gamma = _exact_nonnegative(loss, name="loss")
    kernel, _, _ = _positive_pair_kernel(detunings, coupling_products, gamma)
    return sp.simplify(gamma * kernel)


def nominal_loss_cycle_product(
    detunings: Sequence[Any],
    coupling_products: Sequence[Any],
    loss: Any,
    natural_frequency: Any,
) -> sp.Expr:
    r"""Compose the pair magnitude with ``omega/(2*pi*Gamma)`` exactly.

    The domain is ``Gamma>0``.  The inverse-loss factor is the nominal count in
    a declared ``1/Gamma`` quadratic-envelope window; it is not actual
    near-critical oscillation count or phase coherence.
    """

    gamma = _exact_positive(loss, name="loss")
    omega = _exact_positive(natural_frequency, name="natural_frequency")
    magnitude = common_loss_pair_magnitude(
        detunings,
        coupling_products,
        gamma,
    )
    cycles = nominal_cycles_per_quadratic_envelope_efold(omega, gamma)
    return sp.simplify(magnitude * cycles)


def actual_loss_cycle_product(
    detunings: Sequence[Any],
    coupling_products: Sequence[Any],
    loss: Any,
    natural_frequency: Any,
) -> sp.Expr:
    r"""Compose with the actual underdamped count ``omega_d/(2*pi*Gamma)``.

    The caller must establish ``0<Gamma<2*omega_0``.  Exact numeric inputs are
    rejected by the oscillator API when that ordering fails.
    """

    gamma = _exact_positive(loss, name="loss")
    omega = _exact_positive(natural_frequency, name="natural_frequency")
    magnitude = common_loss_pair_magnitude(
        detunings,
        coupling_products,
        gamma,
    )
    cycles = underdamped_cycles_per_quadratic_envelope_efold(omega, gamma)
    return sp.simplify(magnitude * cycles)


def zero_cutoff_nominal_loss_cycle_product(
    detunings: Sequence[Any],
    coupling_products: Sequence[Any],
    loss: Any,
    natural_frequency: Any,
) -> sp.Expr:
    r"""Return the source-style zero-cutoff extension of the nominal product.

    The open expression is used only for ``0<Gamma<2*omega`` and zero is
    assigned elsewhere.  This convention is discontinuous at both endpoints;
    the function records that choice rather than silently taking a continuous
    extension.
    """

    gamma = _exact_nonnegative(loss, name="loss")
    omega = _exact_positive(natural_frequency, name="natural_frequency")
    kernel, _, _ = _positive_pair_kernel(detunings, coupling_products, gamma)
    open_product = sp.simplify(omega * kernel / (2 * sp.pi))
    if gamma.is_number and omega.is_number:
        if bool(sp.Eq(gamma, 0)) or bool(gamma >= 2 * omega):
            return sp.Integer(0)
        return open_product
    return sp.Piecewise(
        (open_product, sp.And(sp.Gt(gamma, 0), sp.Lt(gamma, 2 * omega))),
        (sp.Integer(0), True),
    )


def loss_cycle_composition(
    detunings: Sequence[Any],
    coupling_products: Sequence[Any],
    loss: Any,
    natural_frequency: Any,
) -> LossCycleComposition:
    """Return exact derivative, endpoint, and asymptotic composition data."""

    gamma = _exact_positive(loss, name="loss")
    omega = _exact_positive(natural_frequency, name="natural_frequency")
    kernel, deltas, products = _positive_pair_kernel(
        detunings,
        coupling_products,
        gamma,
    )
    pair_magnitude = sp.simplify(gamma * kernel)
    nominal_cycles = nominal_cycles_per_quadratic_envelope_efold(omega, gamma)
    nominal_product = sp.simplify(pair_magnitude * nominal_cycles)
    actual_cycles = underdamped_cycles_per_quadratic_envelope_efold(omega, gamma)
    actual_product = sp.simplify(pair_magnitude * actual_cycles)
    derivative = sp.simplify(
        -omega
        * gamma
        / (4 * sp.pi)
        * sum(
            (
                product / (delta**2 + gamma**2 / 4) ** 2
                for delta, product in zip(deltas, products, strict=True)
            ),
            sp.Integer(0),
        )
    )
    zero_limit = sp.simplify(
        omega
        / (2 * sp.pi)
        * sum(
            (
                product / delta**2
                for delta, product in zip(deltas, products, strict=True)
            ),
            sp.Integer(0),
        )
    )
    critical_nominal = sp.simplify(
        omega
        / (2 * sp.pi)
        * sum(
            (
                product / (delta**2 + omega**2)
                for delta, product in zip(deltas, products, strict=True)
            ),
            sp.Integer(0),
        )
    )
    large_coefficient = sp.simplify(
        2 * omega * sum(products, sp.Integer(0)) / sp.pi
    )
    return LossCycleComposition(
        pair_magnitude=pair_magnitude,
        nominal_cycles=nominal_cycles,
        nominal_product=nominal_product,
        nominal_loss_derivative=derivative,
        actual_cycles=actual_cycles,
        actual_product=actual_product,
        zero_loss_limit=zero_limit,
        nominal_critical_left_limit=critical_nominal,
        actual_critical_left_limit=sp.Integer(0),
        large_loss_inverse_square_coefficient=large_coefficient,
    )


def conditional_composite_factor(
    activation_barrier: Any,
    activation_scale: Any,
    subdivision_count: Any,
    collective_count: Any,
    detunings: Sequence[Any],
    coupling_products: Sequence[Any],
    loss: Any,
    natural_frequency: Any,
    thermal_splitting: Any,
) -> sp.Expr:
    r"""Compose typed positive factors on the open positive-loss interval.

    The result is
    ``exp(-E/Theta)*n*N*(K_loss*Q_nominal)*W(x)``.  It inherits the dimension
    of the finite resolvent matrix element and is not promoted to a rate by
    this multiplication.
    """

    count = _positive_integer(subdivision_count, name="subdivision_count")
    population = _positive_integer(collective_count, name="collective_count")
    splitting = _exact_positive(thermal_splitting, name="thermal_splitting")
    activation = activated_relative_response(
        activation_barrier,
        activation_scale,
    )
    loss_cycle = nominal_loss_cycle_product(
        detunings,
        coupling_products,
        loss,
        natural_frequency,
    )
    thermal = symmetric_two_level_gate(splitting)
    return sp.simplify(
        activation * count * population * loss_cycle * thermal
    )
