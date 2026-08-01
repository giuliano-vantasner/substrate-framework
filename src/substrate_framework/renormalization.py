"""Exact conditional relations for one-loop running couplings."""

from __future__ import annotations

from typing import Any

import sympy as sp


def _positive(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_number and expression.is_positive is not True:
        raise ValueError(f"{name} must be positive")
    return expression


def one_loop_inverse_coupling_squared(
    scale: Any,
    reference_scale: Any,
    reference_coupling: Any,
    beta_coefficient: Any,
) -> sp.Expr:
    """Return the exact solution for ``1/g(scale)**2`` of a declared flow.

    The premise is
    ``scale*dg/dscale = -beta_coefficient*g**3/(16*pi**2)``.
    This helper does not derive the beta function or its coefficient.
    """

    scale_value = _positive(scale, "scale")
    reference_value = _positive(reference_scale, "reference_scale")
    coupling_value = _positive(reference_coupling, "reference_coupling")
    coefficient_value = _positive(beta_coefficient, "beta_coefficient")
    return sp.simplify(
        1 / coupling_value**2
        + coefficient_value
        * sp.log(scale_value / reference_value)
        / (8 * sp.pi**2)
    )


def one_loop_transmutation_scale(
    reference_scale: Any,
    reference_coupling: Any,
    beta_coefficient: Any,
) -> sp.Expr:
    """Return the conditional zero of the inverse one-loop coupling.

    The returned expression is invariant under changes of reference point only
    when the reference coupling runs according to the declared one-loop flow.
    """

    reference_value = _positive(reference_scale, "reference_scale")
    coupling_value = _positive(reference_coupling, "reference_coupling")
    coefficient_value = _positive(beta_coefficient, "beta_coefficient")
    return sp.simplify(
        reference_value
        * sp.exp(-8 * sp.pi**2 / (coefficient_value * coupling_value**2))
    )


def transmuted_mass_coordinate(
    coupling_squared: Any,
    beta_coefficient: Any,
    mass_energy_ratio: Any,
) -> sp.Expr:
    """Return a conditional mass coordinate tied to a transmuted scale.

    If ``mu0=S*c/a``, ``Lambda=mu0*exp(-8*pi**2/(b0*g0**2))``, and
    ``m*c**2=q*Lambda``, then ``m*c*a/S=q*exp(-8*pi**2/(b0*g0**2))``.
    The coupling squared, beta coefficient, and mass-energy ratio ``q`` remain
    independent inputs.
    """

    coupling_value = _positive(coupling_squared, "coupling_squared")
    coefficient_value = _positive(beta_coefficient, "beta_coefficient")
    ratio_value = _positive(mass_energy_ratio, "mass_energy_ratio")
    return sp.simplify(
        ratio_value
        * sp.exp(-8 * sp.pi**2 / (coefficient_value * coupling_value))
    )
