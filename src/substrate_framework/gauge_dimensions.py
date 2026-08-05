"""Exact mass-dimension ledgers for gauge-field normalization conventions.

The APIs in this module perform dimensional and coordinate bookkeeping only.
They do not derive a quantum determinant, regulator, counterterm, kinetic
coefficient, preferred spacetime dimension, propagating gauge particle,
physical gauge group, or substrate mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp


def _positive_exact(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.has(sp.Float):
        raise ValueError(f"{name} must be exact")
    if expression.is_real is not True:
        raise ValueError(f"{name} must be explicitly real")
    if expression.is_positive is not True:
        raise ValueError(f"{name} must be explicitly positive")
    return sp.simplify(expression)


@dataclass(frozen=True)
class CanonicalGaugeDimensionLedger:
    """Mass exponents for a canonically normalized gauge potential."""

    spacetime_dimension: sp.Expr
    derivative: sp.Expr
    lagrangian_density: sp.Expr
    potential: sp.Expr
    coupling: sp.Expr
    coupling_squared: sp.Expr
    curvature: sp.Expr
    curvature_squared: sp.Expr
    local_kinetic_coefficient: sp.Expr
    projector_coefficient: sp.Expr


def canonical_gauge_dimensions(
    spacetime_dimension: Any,
) -> CanonicalGaugeDimensionLedger:
    r"""Return exact natural-unit dimensions in the canonical-field convention.

    The declared convention has ``[partial]=1``, dimensionless action,
    canonical density ``F(A)^2/4``, and minimal coupling
    ``D=partial-i*g*A``.  Consequently ``[A]=(D-2)/2``,
    ``[g]=(4-D)/2``, and a coefficient multiplying the dimensionless
    transverse projector in the quadratic momentum kernel has dimension two.
    """

    dimension = _positive_exact(spacetime_dimension, "spacetime dimension")
    potential = sp.simplify((dimension - 2) / 2)
    coupling = sp.simplify(1 - potential)
    curvature = sp.simplify(potential + 1)
    return CanonicalGaugeDimensionLedger(
        spacetime_dimension=dimension,
        derivative=sp.Integer(1),
        lagrangian_density=dimension,
        potential=potential,
        coupling=coupling,
        coupling_squared=sp.simplify(2 * coupling),
        curvature=curvature,
        curvature_squared=sp.simplify(2 * curvature),
        local_kinetic_coefficient=sp.Integer(0),
        projector_coefficient=sp.Integer(2),
    )


@dataclass(frozen=True)
class ConnectionGaugeDimensionLedger:
    """Mass exponents after the coupling is absorbed into the connection."""

    spacetime_dimension: sp.Expr
    connection_potential: sp.Expr
    connection_curvature: sp.Expr
    connection_curvature_squared: sp.Expr
    kinetic_coefficient: sp.Expr


def connection_gauge_dimensions(
    spacetime_dimension: Any,
) -> ConnectionGaugeDimensionLedger:
    r"""Return dimensions for ``B=g*A`` and ``F(B)=g*F(A)``.

    In this convention ``[B]=1`` and ``[F(B)]=2`` in every spacetime
    dimension.  A coefficient multiplying ``F(B)^2`` therefore has mass
    exponent ``D-4``.  This is the same action as the canonical convention
    only when the coefficient is transformed with the fields.
    """

    dimension = _positive_exact(spacetime_dimension, "spacetime dimension")
    return ConnectionGaugeDimensionLedger(
        spacetime_dimension=dimension,
        connection_potential=sp.Integer(1),
        connection_curvature=sp.Integer(2),
        connection_curvature_squared=sp.Integer(4),
        kinetic_coefficient=sp.simplify(dimension - 4),
    )


@dataclass(frozen=True)
class GaugeConventionTranslation:
    """Exact field, curvature, and coefficient translation ledger."""

    spacetime_dimension: sp.Expr
    coupling: sp.Expr
    canonical_coefficient: sp.Expr
    canonical_potential: sp.Symbol
    canonical_curvature: sp.Symbol
    connection_potential: sp.Expr
    connection_curvature: sp.Expr
    connection_coefficient: sp.Expr
    canonical_density: sp.Expr
    connection_density: sp.Expr
    density_residual: sp.Expr
    canonical_dimensions: CanonicalGaugeDimensionLedger
    connection_dimensions: ConnectionGaugeDimensionLedger


def gauge_convention_translation(
    spacetime_dimension: Any,
    coupling: Any,
    canonical_coefficient: Any = sp.Integer(1),
) -> GaugeConventionTranslation:
    r"""Translate ``kappa_A F(A)^2/4`` to the ``B=g*A`` convention.

    With ``F(B)=g*F(A)``, the connection-field coefficient is
    ``kappa_B=kappa_A/g^2``.  The returned residual proves the two displayed
    densities identical; it does not assign a value to either coefficient.
    """

    dimension = _positive_exact(spacetime_dimension, "spacetime dimension")
    strength = _positive_exact(coupling, "coupling")
    coefficient = _positive_exact(canonical_coefficient, "canonical coefficient")
    potential = sp.Symbol("A_c", real=True)
    curvature = sp.Symbol("F_c", real=True)
    connection_potential = sp.simplify(strength * potential)
    connection_curvature = sp.simplify(strength * curvature)
    connection_coefficient = sp.simplify(coefficient / strength**2)
    canonical_density = sp.simplify(coefficient * curvature**2 / 4)
    connection_density = sp.simplify(
        connection_coefficient * connection_curvature**2 / 4
    )
    return GaugeConventionTranslation(
        spacetime_dimension=dimension,
        coupling=strength,
        canonical_coefficient=coefficient,
        canonical_potential=potential,
        canonical_curvature=curvature,
        connection_potential=connection_potential,
        connection_curvature=connection_curvature,
        connection_coefficient=connection_coefficient,
        canonical_density=canonical_density,
        connection_density=connection_density,
        density_residual=sp.simplify(connection_density - canonical_density),
        canonical_dimensions=canonical_gauge_dimensions(dimension),
        connection_dimensions=connection_gauge_dimensions(dimension),
    )


@dataclass(frozen=True)
class PolarizationDimensionLedger:
    """Exact dimensional scope and counterfamily for a projector coefficient."""

    spacetime_dimension: sp.Expr
    required_projector_coefficient_dimension: sp.Expr
    pure_coupling_dimension: sp.Expr
    pure_coupling_residual: sp.Expr
    unique_pure_coupling_dimension: sp.Expr
    scale_completion_mass_power: sp.Expr
    scale_completed_dimension: sp.Expr
    scale_completed_residual: sp.Expr


def polarization_dimensions(
    spacetime_dimension: Any,
) -> PolarizationDimensionLedger:
    r"""Return the narrow pure-coupling result and its mass-scale counterfamily.

    A quadratic projector coefficient always has mass dimension two in the
    canonical convention.  The special ansatz ``Pi_hat=g^2*c`` with nonzero
    dimensionless ``c`` is homogeneous only at ``D=2``.  This is not a
    universal no-go: ``g^2*M^(D-2)`` has dimension two for every ``D`` once a
    positive mass scale ``M`` is independently supplied.
    """

    dimension = _positive_exact(spacetime_dimension, "spacetime dimension")
    canonical = canonical_gauge_dimensions(dimension)
    required = canonical.projector_coefficient
    pure = canonical.coupling_squared
    mass_power = sp.simplify(dimension - 2)
    completed = sp.simplify(pure + mass_power)
    return PolarizationDimensionLedger(
        spacetime_dimension=dimension,
        required_projector_coefficient_dimension=required,
        pure_coupling_dimension=pure,
        pure_coupling_residual=sp.simplify(pure - required),
        unique_pure_coupling_dimension=sp.Integer(2),
        scale_completion_mass_power=mass_power,
        scale_completed_dimension=completed,
        scale_completed_residual=sp.simplify(completed - required),
    )


@dataclass(frozen=True)
class FourDimensionalFormFactorExamples:
    """Three exact scale-invariant form factors and their dimension-two kernels."""

    momentum_squared: sp.Expr
    mass: sp.Expr
    scale: sp.Symbol
    constant_form_factor: sp.Expr
    rational_form_factor: sp.Expr
    logarithmic_form_factor: sp.Expr
    projector_coefficients: tuple[sp.Expr, sp.Expr, sp.Expr]
    form_factor_scale_residuals: tuple[sp.Expr, sp.Expr, sp.Expr]
    projector_scale_residuals: tuple[sp.Expr, sp.Expr, sp.Expr]


def four_dimensional_form_factor_examples(
    momentum_squared: Any,
    mass: Any,
) -> FourDimensionalFormFactorExamples:
    r"""Return counterexamples to selecting a logarithm by dimensions alone.

    In four dimensions ``Q`` and ``M^2`` both have mass dimension two.  A
    constant, ``Q/(Q+M^2)``, and ``log(1+Q/M^2)`` are distinct dimensionless
    form factors.  Multiplication by ``Q`` gives a dimension-two transverse
    projector coefficient in every case.  No loop dynamics is inferred.
    """

    q2 = _positive_exact(momentum_squared, "momentum squared")
    scalar_mass = _positive_exact(mass, "mass")
    scale = sp.Symbol("lambda_scale", positive=True)
    form_factors = (
        sp.Integer(1),
        sp.simplify(q2 / (q2 + scalar_mass**2)),
        sp.log(1 + q2 / scalar_mass**2),
    )
    scaled_form_factors = (
        sp.Integer(1),
        sp.simplify(scale**2 * q2 / (scale**2 * q2 + (scale * scalar_mass) ** 2)),
        sp.log(1 + scale**2 * q2 / (scale * scalar_mass) ** 2),
    )
    coefficients = tuple(sp.simplify(q2 * value) for value in form_factors)
    scaled_coefficients = tuple(
        sp.simplify(scale**2 * q2 * value) for value in scaled_form_factors
    )
    return FourDimensionalFormFactorExamples(
        momentum_squared=q2,
        mass=scalar_mass,
        scale=scale,
        constant_form_factor=form_factors[0],
        rational_form_factor=form_factors[1],
        logarithmic_form_factor=form_factors[2],
        projector_coefficients=coefficients,
        form_factor_scale_residuals=tuple(
            sp.simplify(scaled - original)
            for scaled, original in zip(
                scaled_form_factors, form_factors, strict=True
            )
        ),
        projector_scale_residuals=tuple(
            sp.simplify(scaled - scale**2 * original)
            for scaled, original in zip(
                scaled_coefficients, coefficients, strict=True
            )
        ),
    )


@dataclass(frozen=True)
class RepresentationRescalingLedger:
    """Exact trace-index and coupling transformation under generator rescaling."""

    trace_index: sp.Expr
    coupling: sp.Expr
    generator_scale: sp.Expr
    rescaled_trace_index: sp.Expr
    rescaled_coupling: sp.Expr
    original_weight: sp.Expr
    rescaled_weight: sp.Expr
    invariant_residual: sp.Expr


def representation_rescaling(
    trace_index: Any,
    coupling: Any,
    generator_scale: Any,
) -> RepresentationRescalingLedger:
    r"""Return the convention-preserving map ``T'=rho*T``, ``g'=g/rho``.

    The trace index scales as ``T(R)'=rho^2*T(R)`` while the covariant-
    derivative weight ``g^2*T(R)`` is invariant.  A trace factor cannot be
    changed independently and still be called the same normalization limit.
    """

    index = _positive_exact(trace_index, "trace index")
    strength = _positive_exact(coupling, "coupling")
    scale = _positive_exact(generator_scale, "generator scale")
    rescaled_index = sp.simplify(scale**2 * index)
    rescaled_strength = sp.simplify(strength / scale)
    original_weight = sp.simplify(strength**2 * index)
    rescaled_weight = sp.simplify(rescaled_strength**2 * rescaled_index)
    return RepresentationRescalingLedger(
        trace_index=index,
        coupling=strength,
        generator_scale=scale,
        rescaled_trace_index=rescaled_index,
        rescaled_coupling=rescaled_strength,
        original_weight=original_weight,
        rescaled_weight=rescaled_weight,
        invariant_residual=sp.simplify(rescaled_weight - original_weight),
    )
