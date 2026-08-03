from __future__ import annotations

from itertools import combinations

import pytest
import sympy as sp

from substrate_framework.symmetric_spin import (
    ground_coupling_ledger,
    symmetric_spin_ladder_coefficient,
    symmetric_spin_rung,
)


def _normalized_dicke_state(particle_count: int, excitation_count: int) -> sp.ImmutableMatrix:
    dimension = 1 << particle_count
    entries = [sp.Integer(0)] * dimension
    normalization = sp.sqrt(sp.binomial(particle_count, excitation_count))
    for excited in combinations(range(particle_count), excitation_count):
        index = sum(1 << site for site in excited)
        entries[index] = 1 / normalization
    return sp.ImmutableMatrix(entries)


def _collective_raise_matrix(particle_count: int) -> sp.ImmutableMatrix:
    dimension = 1 << particle_count
    matrix = sp.zeros(dimension)
    for source in range(dimension):
        for site in range(particle_count):
            if source & (1 << site) == 0:
                matrix[source | (1 << site), source] += 1
    return sp.ImmutableMatrix(matrix)


def test_computational_basis_rederives_every_small_rung() -> None:
    for particle_count in range(1, 7):
        raising = _collective_raise_matrix(particle_count)
        for excitation_count in range(particle_count):
            source = _normalized_dicke_state(particle_count, excitation_count)
            target = _normalized_dicke_state(particle_count, excitation_count + 1)
            actual = sp.simplify((target.T * raising * source)[0])
            expected = symmetric_spin_ladder_coefficient(
                particle_count,
                excitation_count,
            )
            assert sp.simplify(actual - expected) == 0


def test_all_rung_formula_coordinates_and_edges() -> None:
    scale = sp.symbols("hbar", positive=True)
    for particle_count in range(1, 12):
        for excitation_count in range(particle_count + 1):
            rung = symmetric_spin_rung(
                particle_count,
                excitation_count,
                operator_scale=scale,
            )
            assert rung.total_spin == sp.Rational(particle_count, 2)
            assert rung.magnetic_number == sp.Rational(
                2 * excitation_count - particle_count,
                2,
            )
            assert rung.raising_coefficient == scale * sp.sqrt(
                (particle_count - excitation_count) * (excitation_count + 1)
            )
            assert rung.lowering_coefficient == scale * sp.sqrt(
                excitation_count * (particle_count - excitation_count + 1)
            )
        assert symmetric_spin_rung(particle_count, particle_count).raising_coefficient == 0
        assert symmetric_spin_rung(particle_count, 0).lowering_coefficient == 0


def test_adjoint_rungs_have_identical_coefficients() -> None:
    for particle_count in range(1, 20):
        for excitation_count in range(particle_count):
            raised = symmetric_spin_ladder_coefficient(
                particle_count,
                excitation_count,
                direction="raise",
            )
            lowered = symmetric_spin_ladder_coefficient(
                particle_count,
                excitation_count + 1,
                direction="lower",
            )
            assert raised == lowered


def test_ground_edge_is_sqrt_n_but_middle_rung_is_order_n() -> None:
    count = 100
    ground = symmetric_spin_ladder_coefficient(count, 0)
    middle = symmetric_spin_ladder_coefficient(count, count // 2)
    assert ground == 10
    assert middle == 5 * sp.sqrt(102)
    assert middle > 5 * ground
    assert sp.limit(
        sp.sqrt((sp.Symbol("n", positive=True) / 2) * (sp.Symbol("n", positive=True) / 2 + 1))
        / sp.Symbol("n", positive=True),
        sp.Symbol("n", positive=True),
        sp.oo,
    ) == sp.Rational(1, 2)


def test_operator_normalization_is_load_bearing() -> None:
    scale = sp.symbols("s", real=True, nonzero=True)
    rung = symmetric_spin_rung(9, 0, operator_scale=scale)
    assert rung.raising_coefficient == 3 * scale
    assert rung.raising_coefficient_squared == 9 * scale**2
    assert symmetric_spin_rung(9, 0, operator_scale=scale / 9).raising_coefficient == scale / 3


def test_equal_couplings_are_purely_symmetric() -> None:
    coupling, scale = sp.symbols("g hbar", real=True)
    ledger = ground_coupling_ledger([coupling] * 9, operator_scale=scale)
    assert ledger.symmetric_amplitude == 3 * coupling * scale
    assert ledger.symmetric_norm_squared == 9 * coupling**2 * scale**2
    assert ledger.total_norm_squared == 9 * coupling**2 * scale**2
    assert ledger.dark_norm_squared == 0


def test_unequal_phases_can_cancel_only_the_symmetric_projection() -> None:
    ledger = ground_coupling_ledger([1, -1])
    assert ledger.symmetric_amplitude == 0
    assert ledger.symmetric_norm_squared == 0
    assert ledger.total_norm_squared == 2
    assert ledger.dark_norm_squared == 2

    partial = ground_coupling_ledger([1, sp.I])
    assert partial.symmetric_amplitude == sp.sqrt(2) * (1 + sp.I) / 2
    assert partial.symmetric_norm_squared == 1
    assert partial.total_norm_squared == 2
    assert partial.dark_norm_squared == 1


@pytest.mark.parametrize(
    ("particle_count", "excitation_count"),
    [(0, 0), (-1, 0), (2, -1), (2, 3), (sp.Rational(3, 2), 0), (sp.Symbol("N"), 0)],
)
def test_invalid_or_unresolved_domains_are_rejected(
    particle_count: sp.Expr | int,
    excitation_count: sp.Expr | int,
) -> None:
    with pytest.raises(ValueError):
        symmetric_spin_rung(particle_count, excitation_count)


def test_invalid_direction_and_empty_couplings_are_rejected() -> None:
    with pytest.raises(ValueError):
        symmetric_spin_ladder_coefficient(2, 0, direction="sideways")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        ground_coupling_ledger([])
    with pytest.raises(ValueError):
        symmetric_spin_rung(2, 0, operator_scale=sp.I)
