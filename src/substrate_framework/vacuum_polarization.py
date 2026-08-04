"""Conditional one-loop complex-scalar vacuum polarization in two dimensions.

This module starts from a separately declared Euclidean scalar-QED functional
determinant.  It does not quantize the framework's accepted classical complex
field, identify its U(1) charge with electric charge, or derive a physical
gauge sector.  The formulas require a massive complex scalar, a
shift-invariant gauge-preserving regulator, the scalar bubble and seagull, and
the quadratic effective-action convention stated by the APIs below.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import sympy as sp


def _positive(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_positive is not True:
        raise ValueError(f"{name} must be provably positive")
    return expression


def _positive_integer(value: Any, name: str) -> int:
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < 1:
        raise ValueError(f"{name} must be positive")
    return value


@dataclass(frozen=True)
class EuclideanTransverseProjector:
    """Exact nonzero-momentum Euclidean transverse-projector ledger."""

    momentum: sp.ImmutableMatrix
    momentum_squared: sp.Expr
    matrix: sp.ImmutableMatrix
    idempotence_residual: sp.ImmutableMatrix
    left_transversality_residual: sp.ImmutableMatrix
    right_transversality_residual: sp.ImmutableMatrix


def euclidean_transverse_projector(
    momentum: Sequence[Any],
) -> EuclideanTransverseProjector:
    r"""Return ``I-q*q.T/q^2`` for a declared nonzero Euclidean momentum.

    The projector is undefined at the zero vector.  Symbolic callers are
    responsible for restricting their domain to ``q^2>0``; this function
    rejects only a momentum whose squared norm simplifies identically to zero.
    """

    vector = sp.ImmutableMatrix([sp.sympify(component) for component in momentum])
    if vector.cols != 1 or vector.rows < 2:
        raise ValueError("momentum must contain at least two components")
    squared = sp.simplify((vector.T * vector)[0])
    if squared == 0:
        raise ValueError("transverse projector is undefined at zero momentum")
    identity = sp.eye(vector.rows)
    projector = sp.ImmutableMatrix(
        (identity - vector * vector.T / squared).applyfunc(sp.simplify)
    )
    return EuclideanTransverseProjector(
        momentum=vector,
        momentum_squared=squared,
        matrix=projector,
        idempotence_residual=sp.ImmutableMatrix(
            (projector * projector - projector).applyfunc(sp.simplify)
        ),
        left_transversality_residual=sp.ImmutableMatrix(
            (vector.T * projector).applyfunc(sp.simplify)
        ),
        right_transversality_residual=sp.ImmutableMatrix(
            (projector * vector).applyfunc(sp.simplify)
        ),
    )


@dataclass(frozen=True)
class ScalarQED2VacuumPolarization:
    r"""One massive-complex-scalar contribution to the Euclidean 1PI kernel.

    The tensor convention is

    ``Gamma^(2)=A_mu Pi_mu_nu A_nu/2`` and
    ``Pi_mu_nu=(q^2*delta_mu_nu-q_mu*q_nu)*form_factor``.

    Equivalently ``Pi_mu_nu=P_mu_nu*projector_coefficient`` at nonzero
    momentum.  The two scalar functions differ by an explicit factor of
    ``q^2``.  ``local_fmunu_squared_coefficient`` is the coefficient of
    ``F_mu_nu*F_mu_nu`` in the leading low-momentum effective Lagrangian; in
    two dimensions the coefficient of the single component ``F_01^2`` is
    twice that value.
    """

    momentum_squared: sp.Expr
    scalar_mass: sp.Expr
    charge_magnitude: sp.Expr
    species_count: int
    parameter: sp.Symbol
    projector_parameter_integrand: sp.Expr
    real_parameter: sp.Symbol
    dimensionless_ratio: sp.Expr
    real_integrand: sp.Expr
    real_antiderivative: sp.Expr
    antiderivative_residual: sp.Expr
    projector_coefficient: sp.Expr
    transverse_form_factor: sp.Expr
    zero_momentum_projector_limit: sp.Expr
    low_momentum_form_factor: sp.Expr
    local_fmunu_squared_coefficient: sp.Expr
    local_f01_squared_coefficient: sp.Expr
    massless_projector_limit: sp.Expr
    heavy_mass_projector_limit: sp.Expr
    bubble_ward_tadpole_coefficient: sp.Expr
    seagull_ward_tadpole_coefficient: sp.Expr
    ward_tadpole_residual: sp.Expr


def scalar_qed2_vacuum_polarization(
    momentum_squared: Any,
    scalar_mass: Any,
    charge_magnitude: Any,
    species_count: int = 1,
) -> ScalarQED2VacuumPolarization:
    r"""Return the exact massive scalar-QED2 one-loop transverse kernel.

    For ``Q=q_E^2>0``, mass ``m>0``, charge magnitude ``e>0``, and ``N``
    identical complex scalars, dimensional regularization or another
    shift-invariant gauge-preserving prescription gives

    ``Pi_hat(Q)=N*e^2*Q/(4*pi) * integral_0^1
    (1-2*x)^2/[m^2+Q*x*(1-x)] dx``.

    The scalar bubble contracts to ``+2*N*e^2*q_nu*I_tad`` and the seagull to
    ``-2*N*e^2*q_nu*I_tad``.  Their cancellation is the Ward identity; a
    projector ansatz alone is not its derivation.  The massless limit at fixed
    positive momentum diverges, so this scalar loop does not yield the finite
    fermionic Schwinger coefficient ``e^2/pi``.
    """

    q2 = _positive(momentum_squared, "momentum squared")
    mass = _positive(scalar_mass, "scalar mass")
    charge = _positive(charge_magnitude, "charge magnitude")
    count = _positive_integer(species_count, "species count")

    x = sp.Symbol("x", real=True)
    y = sp.Symbol("y", real=True)
    ratio = sp.simplify(sp.sqrt(q2) / sp.sqrt(q2 + 4 * mass**2))
    parameter_integrand = sp.simplify(
        count
        * charge**2
        * q2
        * (1 - 2 * x) ** 2
        / (4 * sp.pi * (mass**2 + q2 * x * (1 - x)))
    )
    real_integrand = y**2 / (1 - ratio**2 * y**2)
    real_antiderivative = sp.atanh(ratio * y) / ratio**3 - y / ratio**2
    antiderivative_residual = sp.simplify(
        sp.diff(real_antiderivative, y) - real_integrand
    )
    projector_coefficient = sp.simplify(
        count
        * charge**2
        / sp.pi
        * (sp.atanh(ratio) / ratio - 1)
    )
    form_factor = sp.simplify(projector_coefficient / q2)
    zero_momentum_limit = sp.simplify(
        sp.limit(projector_coefficient, q2, 0)
    )
    low_form_factor = sp.simplify(sp.limit(form_factor, q2, 0))
    massless_limit = sp.limit(projector_coefficient, mass, 0, dir="+")
    heavy_mass_limit = sp.limit(projector_coefficient, mass, sp.oo)
    bubble = sp.simplify(2 * count * charge**2)
    seagull = -bubble
    return ScalarQED2VacuumPolarization(
        momentum_squared=q2,
        scalar_mass=mass,
        charge_magnitude=charge,
        species_count=count,
        parameter=x,
        projector_parameter_integrand=parameter_integrand,
        real_parameter=y,
        dimensionless_ratio=ratio,
        real_integrand=real_integrand,
        real_antiderivative=real_antiderivative,
        antiderivative_residual=antiderivative_residual,
        projector_coefficient=projector_coefficient,
        transverse_form_factor=form_factor,
        zero_momentum_projector_limit=zero_momentum_limit,
        low_momentum_form_factor=low_form_factor,
        local_fmunu_squared_coefficient=sp.simplify(low_form_factor / 4),
        local_f01_squared_coefficient=sp.simplify(low_form_factor / 2),
        massless_projector_limit=massless_limit,
        heavy_mass_projector_limit=heavy_mass_limit,
        bubble_ward_tadpole_coefficient=bubble,
        seagull_ward_tadpole_coefficient=seagull,
        ward_tadpole_residual=sp.simplify(bubble + seagull),
    )
