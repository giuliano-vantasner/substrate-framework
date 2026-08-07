import pytest
import sympy as sp

from substrate_framework.linearized_spin2 import (
    fierz_pauli_gauge_ledger,
    fierz_pauli_gauge_residual,
    supplied_tt_constraint_ledger,
    supplied_tt_constraint_matrix,
    symmetric_tensor_mode_count,
)


def test_supplied_gauge_invariance_selects_the_fierz_pauli_ray() -> None:
    ledger = fierz_pauli_gauge_ledger()
    assert ledger.sampled_constraint_rank == 3
    assert ledger.allowed_coefficient_dimension == 1
    assert ledger.normalized_coefficient_ray == (1, -2, 2, -1)
    assert ledger.symbolic_gauge_residual == sp.zeros(10, 4)


def test_fierz_pauli_coefficient_mutation_breaks_the_gauge_kernel() -> None:
    momentum = (1, 2, 3, 5)
    assert fierz_pauli_gauge_residual((1, -2, 2, -1), momentum) == sp.zeros(10, 4)
    assert (
        fierz_pauli_gauge_residual(
            (1, -2, 2, sp.Rational(-9, 10)),
            momentum,
        ).rank()
        > 0
    )


@pytest.mark.parametrize("wavevector", [(0, 0, 3), (1, 2, 3), (-2, 5, 1)])
def test_supplied_trace_and_transversality_leave_two_positive_amplitudes(
    wavevector: tuple[int, int, int],
) -> None:
    ledger = supplied_tt_constraint_ledger(wavevector)
    assert ledger.constraint_rank == 4
    assert ledger.remaining_amplitude_count == 2
    assert ledger.admissible_basis.shape == (6, 2)
    assert ledger.projected_frobenius_metric.is_positive_definite is True


def test_removing_supplied_trace_condition_retains_an_extra_amplitude() -> None:
    full = supplied_tt_constraint_matrix((1, 2, 3))
    without_trace = supplied_tt_constraint_matrix(
        (1, 2, 3),
        include_trace_constraint=False,
    )
    assert symmetric_tensor_mode_count(full) == 2
    assert symmetric_tensor_mode_count(without_trace) == 3


def test_supplied_tt_ledger_rejects_zero_or_inexact_wavevectors() -> None:
    with pytest.raises(ValueError, match="nonzero"):
        supplied_tt_constraint_ledger((0, 0, 0))
    with pytest.raises(ValueError, match="exact"):
        supplied_tt_constraint_ledger((1.0, 0, 0))
