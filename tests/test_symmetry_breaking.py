from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.symmetry_breaking import (
    leading_exponential_kinetic_metric,
    linear_symmetry_hessian_evidence,
    orthogonal_generators,
    positive_kinetic_mass_evidence,
    radial_quartic_potential,
)


def zero_matrix(matrix: sp.MatrixBase) -> bool:
    return matrix.applyfunc(sp.simplify) == sp.zeros(*matrix.shape)


def test_general_identity_requires_invariance_and_stationarity_for_kernel() -> None:
    x, y, radius = sp.symbols("x y r", real=True)
    generator = sp.Matrix([[0, 1], [-1, 0]])
    potential = (x**2 + y**2 - radius**2) ** 2
    evidence = linear_symmetry_hessian_evidence(
        potential,
        (x, y),
        (radius, 0),
        (generator,),
    )
    assert evidence.invariant
    assert evidence.stationary
    assert evidence.theorem_hypotheses_hold
    assert evidence.differentiated_identity_residual == sp.zeros(2, 1)
    assert evidence.generator_tangents == sp.Matrix([0, -radius])
    assert evidence.broken_tangent_rank == 1
    assert evidence.tangent_kernel_certified

    nonstationary = linear_symmetry_hessian_evidence(
        potential,
        (x, y),
        (radius / 2, 0),
        (generator,),
    )
    assert nonstationary.invariant
    assert not nonstationary.stationary
    assert not nonstationary.theorem_hypotheses_hold
    assert not nonstationary.tangent_kernel_certified
    assert nonstationary.differentiated_identity_residual == sp.zeros(2, 1)


def test_full_o4_orbit_rank_stabilizer_and_radial_hessian_are_exact() -> None:
    sigma, pi1, pi2, pi3 = sp.symbols("sigma pi1 pi2 pi3", real=True)
    coupling, scale = sp.symbols("lambda v", positive=True)
    fields = (sigma, pi1, pi2, pi3)
    generators = orthogonal_generators(4)
    potential = radial_quartic_potential(fields, coupling, scale)
    evidence = linear_symmetry_hessian_evidence(
        potential,
        fields,
        (scale, 0, 0, 0),
        generators,
    )
    assert len(generators) == 6
    assert evidence.generator_span_rank == 6
    assert evidence.generators_independent
    assert evidence.broken_tangent_rank == 3
    assert evidence.stabilizer_dimension == 3
    assert evidence.hessian_at_vacuum == sp.diag(8 * coupling * scale**2, 0, 0, 0)
    assert evidence.tangent_kernel_certified
    characteristic = evidence.hessian_at_vacuum.charpoly()
    expected_characteristic = characteristic.gen**3 * (
        characteristic.gen - 8 * coupling * scale**2
    )
    assert sp.simplify(characteristic.as_expr() - expected_characteristic) == 0

    mass = positive_kinetic_mass_evidence(
        evidence.hessian_at_vacuum,
        sp.eye(4),
        evidence.generator_tangents,
    )
    assert mass.zero_direction_rank == 3
    assert mass.zero_directions_certified


def test_symmetric_vacuum_and_dependent_generators_are_not_overcounted() -> None:
    x, y, scale = sp.symbols("x y v", real=True)
    generator = orthogonal_generators(2)[0]
    potential = radial_quartic_potential((x, y), 1, scale)
    symmetric = linear_symmetry_hessian_evidence(
        potential,
        (x, y),
        (0, 0),
        (generator,),
    )
    assert symmetric.invariant and symmetric.stationary
    assert symmetric.broken_tangent_rank == 0
    assert symmetric.stabilizer_dimension == 1

    repeated = linear_symmetry_hessian_evidence(
        potential,
        (x, y),
        (scale, 0),
        (generator, 2 * generator),
    )
    assert repeated.generator_span_rank == 1
    assert repeated.broken_tangent_rank == 1
    assert repeated.coefficient_kernel_dimension == 1
    with pytest.raises(ValueError, match="independent generator basis"):
        _ = repeated.stabilizer_dimension


def test_explicit_breaking_exposes_nonzero_residual_and_transverse_lift() -> None:
    sigma, pion = sp.symbols("sigma pion", real=True)
    coupling, scale, source, shifted = sp.symbols(
        "lambda v c s0", positive=True
    )
    generator = orthogonal_generators(2)[0]
    symmetric_potential = radial_quartic_potential(
        (sigma, pion), coupling, scale
    )
    broken_potential = symmetric_potential - source * sigma
    stationary_source = 4 * coupling * shifted * (shifted**2 - scale**2)
    evidence = linear_symmetry_hessian_evidence(
        broken_potential.subs(source, stationary_source),
        (sigma, pion),
        (shifted, 0),
        (generator,),
    )
    transverse_curvature = sp.simplify(evidence.hessian_at_vacuum[1, 1])
    assert evidence.stationary
    assert not evidence.invariant
    assert not evidence.theorem_hypotheses_hold
    assert transverse_curvature == sp.simplify(stationary_source / shifted)
    assert not evidence.tangent_kernel_certified
    assert zero_matrix(
        evidence.hessian_tangent_residual - sp.Matrix([0, -stationary_source])
    )


def test_pauli_trace_derives_both_prefactor_conventions() -> None:
    scale = sp.symbols("F", positive=True)
    pauli = (
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -sp.I], [sp.I, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    )
    physicist = leading_exponential_kinetic_metric(
        pauli,
        scale,
        scale**2 / 4,
    )
    anw = leading_exponential_kinetic_metric(
        pauli,
        scale,
        scale**2 / 16,
    )
    assert physicist.trace_gram == 2 * sp.eye(3)
    assert physicist.kinetic_metric == sp.eye(3)
    assert anw.kinetic_metric == sp.eye(3) / 4
    assert anw.kinetic_metric != physicist.kinetic_metric


def test_positive_kinetic_metric_preserves_but_does_not_create_hessian_zeros() -> None:
    k1, k2 = sp.symbols("k1 k2", positive=True)
    hessian = sp.diag(3, 0)
    evidence = positive_kinetic_mass_evidence(
        hessian,
        sp.diag(k1, k2),
        sp.Matrix([0, 1]),
    )
    assert evidence.generalized_mass_operator == sp.diag(3 / k1, 0)
    assert evidence.zero_directions_certified

    lifted = positive_kinetic_mass_evidence(
        sp.diag(3, 2),
        sp.diag(k1, k2),
        sp.Matrix([0, 1]),
    )
    assert not lifted.zero_directions_certified
    assert lifted.zero_direction_residual == sp.Matrix([0, 2 / k2])


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: linear_symmetry_hessian_evidence(0, (), (), (sp.eye(1),)),
            "fields must be non-empty",
        ),
        (
            lambda: linear_symmetry_hessian_evidence(
                0, (sp.Symbol("x"),), (), (sp.eye(1),)
            ),
            "vacuum must match",
        ),
        (
            lambda: linear_symmetry_hessian_evidence(
                0, (sp.Symbol("x"),), (0,), (sp.eye(2),)
            ),
            "generator.*field dimension",
        ),
        (lambda: orthogonal_generators(1), "at least two"),
        (
            lambda: positive_kinetic_mass_evidence(
                sp.eye(2), sp.diag(1, -1), sp.Matrix([1, 0])
            ),
            "positive definite",
        ),
        (
            lambda: leading_exponential_kinetic_metric(
                (sp.Matrix([[0, 1], [-1, 0]]),), 1, 1
            ),
            "Hermitian",
        ),
    ],
)
def test_invalid_or_unproved_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
