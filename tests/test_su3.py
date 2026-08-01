from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.su3 import (
    conditional_one_loop_coefficient,
    fundamental_generators,
    invariants,
    structure_constant,
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
    with pytest.raises(IndexError):
        structure_constant(8, 0, 0)
