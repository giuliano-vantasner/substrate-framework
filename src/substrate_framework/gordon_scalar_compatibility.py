"""Exact canonical-scalar compatibility for transverse Gordon geometry.

This module composes the accepted mostly-plus Gordon metric and canonical
four-dimensional scalar stress.  It keeps algebraic tensor proportionality
separate from the scalar Euler equation, boundary data, and any material or
physical-gravity interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp

from substrate_framework.einstein_scalar import (
    ScalarStressLedger,
    minimally_coupled_scalar_stress,
)
from substrate_framework.gordon_metric import (
    GordonMetric,
    TransverseProfileEinstein,
    gordon_metric_mostly_plus,
    transverse_profile_einstein,
)
from substrate_framework.linear_systems import (
    LinearSystemDiagnostics,
    diagnose_linear_system,
)


def _exact_real(value: Any, name: str) -> sp.Expr:
    result = sp.sympify(value)
    if result.has(sp.Float):
        raise ValueError(f"{name} must be exact")
    if result.is_real is not True:
        raise ValueError(f"{name} must be declared real")
    return sp.simplify(result)


def _positive_exact(value: Any, name: str) -> sp.Expr:
    result = _exact_real(value, name)
    if result.is_positive is not True:
        raise ValueError(f"{name} must be declared positive")
    return result


@dataclass(frozen=True)
class GordonScalarResidual:
    """Full covariant residual for ``G_ab-kappa*T_ab``."""

    geometry: TransverseProfileEinstein
    stress: ScalarStressLedger
    gravitational_coupling: sp.Expr
    residual_covariant: sp.Matrix


@dataclass(frozen=True)
class NonzeroBoostRaySystem:
    """Homogeneous jet system required to share the Gordon tensor ray."""

    metric: GordonMetric
    refractive_index: sp.Expr
    velocity: sp.Expr
    temporal_square: sp.Symbol
    transverse_square: sp.Symbol
    potential: sp.Symbol
    temporal_transverse_product: sp.Expr
    ray_conditions: tuple[sp.Expr, ...]
    coefficient_matrix: sp.Matrix
    diagnostics: LinearSystemDiagnostics
    first_three_minor: sp.Expr


@dataclass(frozen=True)
class RestBoostConditions:
    """Zero-component scalar-stress conditions at ``v=0``."""

    metric: GordonMetric
    refractive_index: sp.Expr
    temporal_square: sp.Symbol
    transverse_square: sp.Symbol
    potential: sp.Symbol
    tt_zero_condition: sp.Expr
    xx_zero_condition: sp.Expr
    square_sum_condition: sp.Expr
    potential_condition: sp.Expr


@dataclass(frozen=True)
class ReciprocalIndexIdentity:
    """Relation between the Gordon curvature kernel and ``(1/n)''``."""

    refractive_index: sp.Expr
    coordinate: sp.Symbol
    curvature_kernel: sp.Expr
    reciprocal_second_derivative: sp.Expr
    identity_residual: sp.Expr


def transverse_gordon_scalar_residual(
    refractive_index: Any,
    coordinate: sp.Symbol,
    velocity: Any,
    temporal_derivative: Any,
    transverse_derivative: Any,
    potential: Any,
    gravitational_coupling: Any,
) -> GordonScalarResidual:
    """Return every exact component of ``G_ab-kappa*T_ab``.

    The scalar gradient is declared to be ``(U_t,U_x,0,0)`` in coordinate
    order ``(t,x,y,z)``.  This is an algebraic jet calculation; callers must
    check the scalar Euler equation and global data separately.
    """

    coupling = _positive_exact(gravitational_coupling, "gravitational_coupling")
    time_gradient = _exact_real(temporal_derivative, "temporal_derivative")
    space_gradient = _exact_real(transverse_derivative, "transverse_derivative")
    scalar_potential = _exact_real(potential, "potential")
    geometry = transverse_profile_einstein(
        refractive_index,
        coordinate,
        velocity,
    )
    stress = minimally_coupled_scalar_stress(
        geometry.metric.covariant,
        [time_gradient, space_gradient, 0, 0],
        scalar_potential,
    )
    residual = (
        geometry.einstein_covariant - coupling * stress.covariant
    ).applyfunc(sp.simplify)
    return GordonScalarResidual(
        geometry=geometry,
        stress=stress,
        gravitational_coupling=coupling,
        residual_covariant=residual,
    )


def nonzero_boost_scalar_ray_system(
    refractive_index: Any,
    velocity: Any,
) -> NonzeroBoostRaySystem:
    """Return the exact scalar-jet conditions for a nonzero Gordon ray.

    The returned four-by-three homogeneous system imposes ``T_xx=0`` and the
    three nonzero-component ratios fixed by C-GOR-001.  ``T_tx`` is returned
    separately because it is bilinear in the two scalar derivatives rather
    than linear in their squares.  The velocity must be exact, nonzero, and
    provably subluminal.
    """

    index = _positive_exact(refractive_index, "refractive_index")
    speed = _exact_real(velocity, "velocity")
    if speed.is_zero is not False:
        raise ValueError("velocity must be provably nonzero")
    margin = sp.simplify(1 - speed**2)
    if margin.is_positive is not True:
        raise ValueError("velocity must satisfy |velocity| < 1 exactly")
    gamma = sp.sqrt(sp.simplify(1 / margin))
    metric = gordon_metric_mostly_plus(
        index,
        [gamma, 0, 0, sp.simplify(gamma * speed)],
    )

    temporal, transverse, scalar_potential = sp.symbols(
        "U_t U_x V", real=True
    )
    a, b = sp.symbols("a b", nonnegative=True)
    stress = minimally_coupled_scalar_stress(
        metric.covariant,
        [temporal, transverse, 0, 0],
        scalar_potential,
    ).covariant

    def jetify(expression: sp.Expr) -> sp.Expr:
        return sp.factor(
            sp.expand(expression)
            .subs(temporal**2, a)
            .subs(transverse**2, b)
        )

    tensor = stress.applyfunc(jetify)
    raw_conditions = (
        tensor[1, 1],
        tensor[0, 3] + tensor[0, 0] / speed,
        tensor[2, 2] - (speed**-2 - 1) * tensor[0, 0],
        tensor[3, 3] - speed**-2 * tensor[0, 0],
    )
    conditions = tuple(
        sp.factor(sp.together(item).as_numer_denom()[0])
        for item in raw_conditions
    )
    coefficients, rhs = sp.linear_eq_to_matrix(
        conditions,
        [a, b, scalar_potential],
    )
    diagnostics = diagnose_linear_system(coefficients, rhs)
    first_minor = sp.factor(coefficients[:3, :].det())
    return NonzeroBoostRaySystem(
        metric=metric,
        refractive_index=index,
        velocity=speed,
        temporal_square=a,
        transverse_square=b,
        potential=scalar_potential,
        temporal_transverse_product=sp.simplify(temporal * transverse),
        ray_conditions=conditions,
        coefficient_matrix=coefficients,
        diagnostics=diagnostics,
        first_three_minor=first_minor,
    )


def rest_boost_scalar_conditions(refractive_index: Any) -> RestBoostConditions:
    """Return the two zero-geometry conditions that close the rest branch."""

    index = _positive_exact(refractive_index, "refractive_index")
    metric = gordon_metric_mostly_plus(index, [1, 0, 0, 0])
    temporal, transverse, scalar_potential = sp.symbols(
        "U_t U_x V", real=True
    )
    a, b = sp.symbols("a b", nonnegative=True)
    stress = minimally_coupled_scalar_stress(
        metric.covariant,
        [temporal, transverse, 0, 0],
        scalar_potential,
    ).covariant

    def jetify(expression: sp.Expr) -> sp.Expr:
        return sp.factor(
            sp.expand(expression)
            .subs(temporal**2, a)
            .subs(transverse**2, b)
        )

    tt_condition = sp.factor(2 * index**2 * jetify(stress[0, 0]))
    xx_condition = sp.factor(2 * jetify(stress[1, 1]))
    square_sum = sp.factor((tt_condition + xx_condition) / 2)
    potential_condition = sp.factor((tt_condition - xx_condition) / 4)
    return RestBoostConditions(
        metric=metric,
        refractive_index=index,
        temporal_square=a,
        transverse_square=b,
        potential=scalar_potential,
        tt_zero_condition=tt_condition,
        xx_zero_condition=xx_condition,
        square_sum_condition=square_sum,
        potential_condition=potential_condition,
    )


def reciprocal_index_identity(
    refractive_index: Any,
    coordinate: sp.Symbol,
) -> ReciprocalIndexIdentity:
    """Return the exact identity ``(1/n)''=-K/n``."""

    if not isinstance(coordinate, sp.Symbol) or coordinate.is_real is not True:
        raise ValueError("coordinate must be a real SymPy Symbol")
    index = _positive_exact(refractive_index, "refractive_index")
    kernel = sp.factor(
        (
            index * sp.diff(index, coordinate, 2)
            - 2 * sp.diff(index, coordinate) ** 2
        )
        / index**2
    )
    reciprocal_second = sp.factor(sp.diff(1 / index, coordinate, 2))
    residual = sp.simplify(reciprocal_second + kernel / index)
    return ReciprocalIndexIdentity(
        refractive_index=index,
        coordinate=coordinate,
        curvature_kernel=kernel,
        reciprocal_second_derivative=reciprocal_second,
        identity_residual=residual,
    )
