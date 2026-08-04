from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.nonabelian_holonomy import (
    endpoint_gauge_holonomy_evidence,
    ordered_segment_holonomy,
    su2_holonomy_evidence,
)


def _pauli() -> tuple[sp.ImmutableMatrix, ...]:
    return (
        sp.ImmutableMatrix([[0, 1], [1, 0]]),
        sp.ImmutableMatrix([[0, -sp.I], [sp.I, 0]]),
        sp.ImmutableMatrix([[1, 0], [0, -1]]),
    )


def test_ordered_segments_are_later_left_unitary_and_reversible() -> None:
    sigma_1, sigma_2, _ = _pauli()
    evidence = ordered_segment_holonomy((sp.pi * sigma_1 / 2, sp.pi * sigma_2 / 2))

    assert evidence.transporter == sp.I * sp.ImmutableMatrix([[1, 0], [0, -1]])
    assert evidence.unitary_certified
    assert evidence.determinant == 1
    assert evidence.determinant_certified
    assert evidence.reverse_transporter == evidence.transporter.H
    assert evidence.reverse_certified
    assert evidence.composition_certified
    assert evidence.cyclic_basepoint_certified
    assert not evidence.pairwise_commuting
    assert evidence.commuting_collapse_residual != sp.zeros(2)


def test_commuting_segments_collapse_to_one_exponential() -> None:
    _, _, sigma_3 = _pauli()
    alpha, beta = sp.symbols("alpha beta", real=True)
    evidence = ordered_segment_holonomy((alpha * sigma_3 / 2, beta * sigma_3 / 2))

    assert evidence.pairwise_commuting
    assert evidence.commuting_collapse_residual == sp.zeros(2)
    assert evidence.reverse_certified


def test_endpoint_gauges_telescope_for_an_open_path() -> None:
    sigma_1, sigma_2, sigma_3 = _pauli()
    factors = (sp.I * sigma_1, sp.I * sigma_2)
    gauges = (sp.eye(2), sp.I * sigma_3, sp.I * sigma_1)
    evidence = endpoint_gauge_holonomy_evidence(factors, gauges)

    assert evidence.endpoint_covariance_certified
    assert evidence.transformed_transporter == evidence.endpoint_prediction
    assert evidence.trace_residual is None
    assert not evidence.closed_conjugacy_certified


def test_closed_path_gauge_change_preserves_conjugacy_data() -> None:
    sigma_1, sigma_2, sigma_3 = _pauli()
    factors = (sp.I * sigma_1, sp.I * sigma_2)
    gauges = (sp.I * sigma_1, sp.I * sigma_3, sp.I * sigma_1)
    evidence = endpoint_gauge_holonomy_evidence(
        factors,
        gauges,
        closed_path=True,
    )

    assert evidence.endpoint_covariance_certified
    assert evidence.closed_conjugacy_certified
    assert evidence.trace_residual == 0
    assert evidence.determinant_residual == 0
    assert evidence.characteristic_polynomial_residual == 0
    assert evidence.transformed_transporter != evidence.transporter


def test_su2_center_and_representation_data_are_distinct() -> None:
    evidence = su2_holonomy_evidence()

    assert evidence.fundamental_2pi == -sp.eye(2)
    assert evidence.fundamental_4pi == sp.eye(2)
    assert evidence.adjoint_2pi == sp.eye(3)
    assert evidence.fundamental_2pi_trace == -2
    assert evidence.fundamental_2pi_normalized_trace == -1
    assert evidence.adjoint_2pi_trace == 3
    assert evidence.adjoint_2pi_normalized_trace == 1


def test_noncommuting_bch_coefficient_and_commuting_control() -> None:
    evidence = su2_holonomy_evidence()

    assert evidence.ordered_minus_naive != sp.zeros(2)
    assert evidence.bch_coefficient_certified
    assert evidence.leading_quadratic_coefficient == sp.I * evidence.generators[2] / 2
    assert evidence.commuting_residual == sp.zeros(2)


def test_swapping_noncommuting_segments_changes_the_matrix_not_necessarily_trace() -> None:
    sigma_1, sigma_2, _ = _pauli()
    forward = ordered_segment_holonomy((sp.pi * sigma_1 / 2, sp.pi * sigma_2 / 2))
    swapped = ordered_segment_holonomy((sp.pi * sigma_2 / 2, sp.pi * sigma_1 / 2))

    assert forward.transporter == -swapped.transporter
    assert forward.transporter != swapped.transporter
    assert forward.trace == swapped.trace == 0


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: ordered_segment_holonomy(()), "nonempty"),
        (lambda: ordered_segment_holonomy(([[1.0]],)), "exact"),
        (lambda: ordered_segment_holonomy(([[sp.I]],)), "Hermitian"),
        (
            lambda: ordered_segment_holonomy((sp.eye(2), sp.eye(3))),
            "same square shape",
        ),
        (
            lambda: endpoint_gauge_holonomy_evidence((), (sp.eye(2),)),
            "nonempty",
        ),
        (
            lambda: endpoint_gauge_holonomy_evidence((sp.eye(2),), (sp.eye(2),)),
            "one more matrix",
        ),
        (
            lambda: endpoint_gauge_holonomy_evidence(
                (sp.eye(2),),
                (sp.eye(2), sp.ImmutableMatrix([[1, 1], [0, 1]])),
            ),
            "unitary",
        ),
        (
            lambda: endpoint_gauge_holonomy_evidence(
                (sp.eye(2),),
                (sp.eye(2), -sp.eye(2)),
                closed_path=True,
            ),
            "equal endpoint",
        ),
        (lambda: su2_holonomy_evidence(sp.Symbol("z")), "explicitly real"),
    ],
)
def test_exact_input_contracts(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
