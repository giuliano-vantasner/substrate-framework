from __future__ import annotations

from collections import Counter
from fractions import Fraction

import pytest
import sympy as sp

from substrate_framework.su3 import invariants, triality_phase
from substrate_framework.su3_representations import (
    SU3Irrep,
    irreps_containing_hypercharge,
    minimal_dimension_hypercharge_matches,
    su3_gelfand_tsetlin_states,
    su3_irrep_dimension,
    su3_irrep_quadratic_casimir,
    su3_irrep_triality,
    su3_isospin_multiplets,
    su3_weight_multiplicities,
)


def _weight_counter(p: int, q: int) -> Counter[tuple[sp.Rational, sp.Rational]]:
    return Counter(
        {
            (weight.isospin_projection, weight.hypercharge): weight.multiplicity
            for weight in su3_weight_multiplicities(p, q)
        }
    )


@pytest.mark.parametrize(
    ("p", "q", "dimension", "casimir"),
    [
        (0, 0, 1, sp.Integer(0)),
        (1, 0, 3, sp.Rational(4, 3)),
        (0, 1, 3, sp.Rational(4, 3)),
        (2, 0, 6, sp.Rational(10, 3)),
        (1, 1, 8, sp.Integer(3)),
        (3, 0, 10, sp.Integer(6)),
        (0, 3, 10, sp.Integer(6)),
        (2, 2, 27, sp.Integer(8)),
    ],
)
def test_weyl_dimension_and_casimir_are_exact(
    p: int, q: int, dimension: int, casimir: sp.Rational
) -> None:
    irrep = SU3Irrep(p, q)
    assert irrep.dimension == dimension
    assert irrep.quadratic_casimir == casimir
    assert su3_irrep_dimension(p, q) == dimension
    assert su3_irrep_quadratic_casimir(p, q) == casimir


def test_fundamental_normalization_matches_accepted_generators() -> None:
    accepted = invariants()
    assert su3_irrep_quadratic_casimir(1, 0) == accepted.fundamental_casimir
    assert su3_irrep_quadratic_casimir(1, 1) == accepted.adjoint_casimir


def test_gelfand_tsetlin_enumeration_counts_every_basis_state() -> None:
    for p in range(6):
        for q in range(6):
            states = su3_gelfand_tsetlin_states(p, q)
            assert len(states) == su3_irrep_dimension(p, q)
            assert all(state.m12 >= state.m11 >= state.m22 for state in states)
            assert all(p + q >= state.m12 >= q >= state.m22 >= 0 for state in states)


def test_fundamental_and_sextet_hypercharges_use_one_convention() -> None:
    fundamental = SU3Irrep(1, 0)
    assert {
        (state.isospin_projection, state.hypercharge)
        for state in fundamental.states
    } == {
        (sp.Rational(1, 2), sp.Rational(1, 3)),
        (sp.Rational(-1, 2), sp.Rational(1, 3)),
        (sp.Integer(0), sp.Rational(-2, 3)),
    }
    assert {row.hypercharge for row in su3_isospin_multiplets(2, 0)} == {
        sp.Rational(2, 3),
        sp.Rational(-1, 3),
        sp.Rational(-4, 3),
    }


def test_adjoint_central_weight_has_multiplicity_two() -> None:
    weights = _weight_counter(1, 1)
    assert sum(weights.values()) == 8
    assert weights[(sp.Integer(0), sp.Integer(0))] == 2


def test_conjugate_irreps_have_negated_weight_multisets() -> None:
    for p in range(4):
        for q in range(4):
            original = _weight_counter(p, q)
            conjugate = _weight_counter(q, p)
            reflected = Counter(
                {(-i3, -hypercharge): multiplicity for (i3, hypercharge), multiplicity in original.items()}
            )
            assert conjugate == reflected


def test_triality_matches_the_accepted_abstract_center_character() -> None:
    for p in range(5):
        for q in range(5):
            triality = su3_irrep_triality(p, q)
            assert triality == (p + 2 * q) % 3
            assert triality_phase(triality) == triality_phase(p + 2 * q)


def test_y_one_filter_reports_conjugate_dimension_tie() -> None:
    matches = irreps_containing_hypercharge(1, max_p=3, max_q=3)
    assert [(match.p, match.q, match.dimension, match.isospins) for match in matches[:3]] == [
        (1, 1, 8, (sp.Rational(1, 2),)),
        (0, 3, 10, (sp.Rational(1, 2),)),
        (3, 0, 10, (sp.Rational(3, 2),)),
    ]
    assert [(match.p, match.q) for match in minimal_dimension_hypercharge_matches(
        sp.Integer(1), max_p=6, max_q=6
    )] == [(1, 1)]


def test_two_thirds_filter_repairs_the_source_guard() -> None:
    matches = irreps_containing_hypercharge(Fraction(2, 3), max_p=2, max_q=2)
    assert [(match.p, match.q, match.dimension) for match in matches[:2]] == [
        (0, 1, 3),
        (2, 0, 6),
    ]


@pytest.mark.parametrize(
    ("function", "args", "error"),
    [
        (su3_irrep_dimension, (-1, 0), ValueError),
        (su3_irrep_dimension, (sp.Rational(1, 2), 0), TypeError),
        (su3_irrep_quadratic_casimir, (True, 0), TypeError),
        (su3_irrep_triality, (0, -1), ValueError),
    ],
)
def test_dynkin_label_domain(function, args, error) -> None:
    with pytest.raises(error):
        function(*args)


def test_hypercharge_filter_rejects_inexact_or_unbounded_inputs() -> None:
    with pytest.raises(TypeError, match="exact rational"):
        irreps_containing_hypercharge(1.0, max_p=2, max_q=2)
    with pytest.raises(ValueError, match="max_p"):
        irreps_containing_hypercharge(1, max_p=-1, max_q=2)
