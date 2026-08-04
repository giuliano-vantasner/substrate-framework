"""Conditional massive-scalar SU(2) vacuum polarization in two dimensions.

The theorem in this module requires a separately declared Euclidean complex
scalar multiplet, its exact Hermitian SU(2) representation, and a
translation- and background-gauge-preserving regulator.  It composes the
accepted scalar-QED2 loop with an explicitly derived representation trace and
checks the local background-field curvature coefficient independently.

It does not identify the scalar with substrate matter, fix a bare or
counterterm coefficient, produce a massless Schwinger pole, lift the result to
four dimensions, or establish a physical weak gauge sector.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import sympy as sp

from .vacuum_polarization import (
    ScalarQED2VacuumPolarization,
    scalar_qed2_vacuum_polarization,
)


def _exact_matrix(value: Any, name: str) -> sp.ImmutableMatrix:
    matrix = sp.Matrix(value)
    if matrix.rows == 0 or matrix.cols == 0:
        raise ValueError(f"{name} must be nonempty")
    if matrix.rows != matrix.cols:
        raise ValueError(f"{name} must be square")
    if any(entry.has(sp.Float) for entry in matrix):
        raise ValueError(f"{name} must contain exact entries")
    return sp.ImmutableMatrix(matrix.applyfunc(sp.simplify))


def _positive_exact(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.has(sp.Float):
        raise ValueError(f"{name} must be exact")
    if expression.is_real is not True:
        raise ValueError(f"{name} must be explicitly real")
    if expression.is_positive is not True:
        raise ValueError(f"{name} must be explicitly positive")
    return sp.simplify(expression)


def _zero(matrix: sp.MatrixBase) -> bool:
    simplified = sp.Matrix(matrix).applyfunc(sp.simplify)
    return simplified == sp.zeros(*simplified.shape)


@dataclass(frozen=True)
class SU2ScalarVacuumPolarization:
    r"""Exact representation and one-loop ledger for complex scalars in SU(2).

    With ``tr_R(T_a*T_b)=T(R)*delta_ab``, the color projector coefficient is
    ``delta_ab*T(R)`` times the accepted Abelian coefficient.  The coefficient
    of the component density ``sum_a F^a_mu_nu F^a_mu_nu`` therefore contains
    ``T(R)``.  The coefficient of ``tr_R(F_mu_nu F_mu_nu)`` does not, because
    the representation trace already supplies that factor.
    """

    generators: tuple[sp.ImmutableMatrix, sp.ImmutableMatrix, sp.ImmutableMatrix]
    carrier_dimension: int
    commutator_residuals: tuple[
        sp.ImmutableMatrix, sp.ImmutableMatrix, sp.ImmutableMatrix
    ]
    hermiticity_residuals: tuple[
        sp.ImmutableMatrix, sp.ImmutableMatrix, sp.ImmutableMatrix
    ]
    trace_metric: sp.ImmutableMatrix
    dynkin_index: sp.Expr
    trace_metric_residual: sp.ImmutableMatrix
    abelian_ledger: ScalarQED2VacuumPolarization
    color_projector_coefficient: sp.ImmutableMatrix
    color_transverse_form_factor: sp.ImmutableMatrix
    bubble_ward_tadpole_coefficient: sp.ImmutableMatrix
    seagull_ward_tadpole_coefficient: sp.ImmutableMatrix
    ward_tadpole_residual: sp.ImmutableMatrix
    local_component_fmunu_squared_coefficient: sp.Expr
    local_trace_fmunu_squared_coefficient: sp.Expr
    heat_kernel_curvature_weight: sp.Expr
    heat_kernel_free_factor: sp.Expr
    proper_time_mass_integral: sp.Expr
    heat_kernel_trace_fmunu_squared_coefficient: sp.Expr
    covariant_completion_residual: sp.Expr


def su2_scalar_qed2_vacuum_polarization(
    generators: Sequence[Any],
    momentum_squared: Any,
    scalar_mass: Any,
    coupling: Any,
    species_count: int = 1,
) -> SU2ScalarVacuumPolarization:
    r"""Return the conditional one-loop SU(2) complex-scalar kernel.

    The exact Hermitian generators must obey
    ``[T_1,T_2]=i*T_3`` and cyclic permutations, and their trace metric must be
    ``T(R)*I_3`` with a provably positive ``T(R)``.  The connection convention
    is ``D=partial-i*g*W^a*T_a``.

    The local trace-density coefficient is also reconstructed from the flat
    background-field heat-kernel factors ``(4*pi)^-1``, ``1/12``, and
    ``integral_0^infinity exp(-m^2*s) ds=1/m^2``.  Equality with the
    low-momentum two-point result is the covariant-completion check; projector
    transversality alone is not used as that proof.
    """

    if len(generators) != 3:
        raise ValueError("generators must contain exactly three SU(2) matrices")
    exact_generators = tuple(
        _exact_matrix(value, f"generator_{index}")
        for index, value in enumerate(generators)
    )
    shape = exact_generators[0].shape
    if any(generator.shape != shape for generator in exact_generators[1:]):
        raise ValueError("generators must have one common square shape")

    hermiticity = tuple(
        sp.ImmutableMatrix((generator - generator.H).applyfunc(sp.simplify))
        for generator in exact_generators
    )
    if not all(_zero(residual) for residual in hermiticity):
        raise ValueError("generators must be exactly Hermitian")

    cyclic_pairs = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    commutators = tuple(
        sp.ImmutableMatrix(
            (
                exact_generators[first] * exact_generators[second]
                - exact_generators[second] * exact_generators[first]
                - sp.I * exact_generators[result]
            ).applyfunc(sp.simplify)
        )
        for first, second, result in cyclic_pairs
    )
    if not all(_zero(residual) for residual in commutators):
        raise ValueError("generators must obey the exact SU(2) commutators")

    trace_metric = sp.ImmutableMatrix(
        3,
        3,
        lambda first, second: sp.simplify(
            sp.trace(exact_generators[first] * exact_generators[second])
        ),
    )
    index = _positive_exact(trace_metric[0, 0], "Dynkin index")
    trace_residual = sp.ImmutableMatrix(
        (trace_metric - index * sp.eye(3)).applyfunc(sp.simplify)
    )
    if not _zero(trace_residual):
        raise ValueError("generator trace metric must equal T(R) times delta_ab")

    q2 = _positive_exact(momentum_squared, "momentum squared")
    mass = _positive_exact(scalar_mass, "scalar mass")
    strength = _positive_exact(coupling, "coupling")
    abelian = scalar_qed2_vacuum_polarization(
        q2,
        mass,
        strength,
        species_count=species_count,
    )
    identity = sp.eye(3)
    color_projector = sp.ImmutableMatrix(
        identity * sp.simplify(index * abelian.projector_coefficient)
    )
    color_form_factor = sp.ImmutableMatrix(
        identity * sp.simplify(index * abelian.transverse_form_factor)
    )
    bubble = sp.ImmutableMatrix(
        identity * sp.simplify(index * abelian.bubble_ward_tadpole_coefficient)
    )
    seagull = sp.ImmutableMatrix(
        identity * sp.simplify(index * abelian.seagull_ward_tadpole_coefficient)
    )
    ward_residual = sp.ImmutableMatrix((bubble + seagull).applyfunc(sp.simplify))

    curvature_weight = sp.Rational(1, 12)
    free_factor = 1 / (4 * sp.pi)
    mass_integral = sp.simplify(1 / mass**2)
    heat_kernel_trace_coefficient = sp.simplify(
        species_count
        * strength**2
        * curvature_weight
        * free_factor
        * mass_integral
    )
    local_trace_coefficient = sp.simplify(
        abelian.local_fmunu_squared_coefficient
    )
    local_component_coefficient = sp.simplify(
        index * local_trace_coefficient
    )

    return SU2ScalarVacuumPolarization(
        generators=exact_generators,
        carrier_dimension=shape[0],
        commutator_residuals=commutators,
        hermiticity_residuals=hermiticity,
        trace_metric=trace_metric,
        dynkin_index=index,
        trace_metric_residual=trace_residual,
        abelian_ledger=abelian,
        color_projector_coefficient=color_projector,
        color_transverse_form_factor=color_form_factor,
        bubble_ward_tadpole_coefficient=bubble,
        seagull_ward_tadpole_coefficient=seagull,
        ward_tadpole_residual=ward_residual,
        local_component_fmunu_squared_coefficient=local_component_coefficient,
        local_trace_fmunu_squared_coefficient=local_trace_coefficient,
        heat_kernel_curvature_weight=curvature_weight,
        heat_kernel_free_factor=free_factor,
        proper_time_mass_integral=mass_integral,
        heat_kernel_trace_fmunu_squared_coefficient=heat_kernel_trace_coefficient,
        covariant_completion_residual=sp.simplify(
            heat_kernel_trace_coefficient - local_trace_coefficient
        ),
    )
