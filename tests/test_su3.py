from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.su3 import (
    SU3SymmetricTensorEvidence,
    center_conjugation,
    center_element,
    center_elements,
    conditional_one_loop_coefficient,
    fundamental_commutant_basis,
    fundamental_generators,
    invariants,
    structure_constant,
    symmetric_structure_constant,
    symmetric_tensor_evidence,
    triality_phase,
)


def test_generators_have_exact_trace_normalization() -> None:
    generators = fundamental_generators()
    gram = sp.Matrix(
        8, 8, lambda a, b: sp.trace(generators[a] * generators[b])
    )
    assert gram == sp.eye(8) / 2


def test_structure_constants_and_casimirs_are_exact() -> None:
    assert structure_constant(0, 1, 2) == 1
    assert structure_constant(3, 4, 7) == sp.sqrt(3) / 2
    values = invariants()
    assert values.dynkin_index == sp.Rational(1, 2)
    assert values.fundamental_casimir == sp.Rational(4, 3)
    assert values.adjoint_casimir == 3


def test_symmetric_tensor_and_anticommutator_reconstruction_are_exact() -> None:
    evidence = symmetric_tensor_evidence()

    assert isinstance(evidence, SU3SymmetricTensorEvidence)
    assert evidence.fully_symmetric
    assert all(residual == sp.zeros(3) for residual in evidence.anticommutator_residuals)
    assert symmetric_structure_constant(0, 0, 7) == 1 / sp.sqrt(3)
    assert symmetric_structure_constant(7, 7, 7) == -1 / sp.sqrt(3)
    assert symmetric_structure_constant(0, 3, 5) == sp.Rational(1, 2)


def test_symmetric_tensor_restricts_to_standard_su2_but_not_globally() -> None:
    evidence = symmetric_tensor_evidence()

    assert evidence.embedded_su2_all_zero
    assert all(
        evidence.tensor[a, b, c] == 0
        for a in range(3)
        for b in range(3)
        for c in range(3)
    )
    assert evidence.outside_nonzero_witness == (0, 0, 7, 1 / sp.sqrt(3))


def test_symmetric_tensor_normalization_is_load_bearing() -> None:
    generators = fundamental_generators()
    mutated = tuple(2 * generator for generator in generators)
    d118_mutated = sp.simplify(
        2
        * sp.trace(
            (mutated[0] * mutated[0] + mutated[0] * mutated[0]) * mutated[7]
        )
    )

    assert d118_mutated == 8 / sp.sqrt(3)
    assert d118_mutated != symmetric_structure_constant(0, 0, 7)


def test_declared_loop_weights_remain_explicit() -> None:
    flavors, gauge, matter = sp.symbols("n_f c_g c_m", nonnegative=True)
    coefficient = conditional_one_loop_coefficient(flavors, gauge, matter)
    assert coefficient == 3 * gauge - matter * flavors / 2
    assert conditional_one_loop_coefficient(
        flavors, sp.Rational(11, 3), sp.Rational(4, 3)
    ) == 11 - 2 * flavors / 3


@pytest.mark.parametrize("value", [-1, sp.Rational(1, 2)])
def test_flavor_count_domain(value) -> None:
    with pytest.raises(ValueError, match="flavor_count"):
        conditional_one_loop_coefficient(value, 1, 1)


def test_generator_index_domain() -> None:
    assert structure_constant(sp.Integer(0), sp.Integer(1), sp.Integer(2)) == 1
    assert symmetric_structure_constant(
        sp.Integer(0), sp.Integer(0), sp.Integer(7)
    ) == 1 / sp.sqrt(3)
    with pytest.raises(IndexError):
        structure_constant(8, 0, 0)
    with pytest.raises(IndexError):
        symmetric_structure_constant(0, 8, 0)
    with pytest.raises(IndexError):
        structure_constant(True, 0, 0)
    with pytest.raises(IndexError):
        symmetric_structure_constant(0.0, 0, 0)


def test_full_fundamental_commutant_is_scalar() -> None:
    assert fundamental_commutant_basis() == (sp.eye(3),)


def test_center_is_exact_z3_inside_su3() -> None:
    generators = fundamental_generators()
    elements = center_elements()
    assert len(elements) == 3
    assert len({sp.srepr(element) for element in elements}) == 3
    for element in elements:
        assert sp.simplify(element.det()) == 1
        assert sp.simplify(element.H * element) == sp.eye(3)
        assert all(
            element * generator == generator * element
            for generator in generators
        )
    assert sp.simplify(center_element(1) ** 3) == sp.eye(3)
    assert center_element(-1) == center_element(2)


def test_center_response_depends_only_on_abstract_triality() -> None:
    omega = center_element()[0, 0]
    assert triality_phase(1) == omega
    assert triality_phase(0) == 1
    assert triality_phase(3) == 1
    assert sp.simplify(triality_phase(1) * triality_phase(2)) == 1
    matrix = sp.Matrix(3, 3, sp.symbols("x0:9"))
    assert center_conjugation(matrix) == matrix


def test_center_api_domains() -> None:
    with pytest.raises(TypeError, match="power"):
        center_element(sp.Integer(1))
    with pytest.raises(TypeError, match="triality"):
        triality_phase(sp.Integer(1))
    with pytest.raises(ValueError, match="3 by 3"):
        center_conjugation(sp.eye(2))
