from __future__ import annotations

import pytest
import sympy as sp

import substrate_framework as framework
from substrate_framework.generalized_dissipation import (
    energy_rate_with_external_work,
    metric_power_balance,
    power_balance_residual,
    rayleigh_dissipation,
    scalar_power_balance_force,
)


def test_metric_particular_force_closes_the_scalar_power_ledger() -> None:
    power, u, w, gx, gy = sp.symbols("P u w g_x g_y", positive=True)
    result = metric_power_balance(power, (u, w), sp.diag(gx, gy))
    denominator = gx * u**2 + gy * w**2
    assert result.squared_rate == denominator
    assert result.particular_force == sp.ImmutableMatrix(
        [-power * gx * u / denominator, -power * gy * w / denominator]
    )
    assert result.balance_residual == 0


def test_balance_has_a_work_free_affine_family_in_two_dimensions() -> None:
    power, u, w, alpha = sp.symbols("P u w alpha", positive=True)
    particular = metric_power_balance(power, (u, w)).particular_force
    work_free = sp.ImmutableMatrix([alpha * w, -alpha * u])
    alternate = particular + work_free
    assert power_balance_residual(power, (u, w), alternate) == 0
    assert alternate != particular


def test_declared_metric_changes_allocation_without_changing_total_work() -> None:
    power, u, w, weight = sp.symbols("P u w g", positive=True)
    euclidean = metric_power_balance(power, (u, w))
    weighted = metric_power_balance(power, (u, w), sp.diag(weight, 1))
    assert euclidean.balance_residual == weighted.balance_residual == 0
    assert sp.simplify(
        euclidean.particular_force[0] - weighted.particular_force[0]
    ) != 0


def test_scalar_force_is_unique_only_away_from_zero_rate() -> None:
    power, rate = sp.symbols("P v", positive=True)
    assert scalar_power_balance_force(power, rate) == -power / rate
    with pytest.raises(ValueError, match="explicitly nonzero"):
        scalar_power_balance_force(power, 0)
    arbitrary_force = sp.symbols("F", real=True)
    assert power_balance_residual(0, (0,), (arbitrary_force,)) == 0
    assert power_balance_residual(power, (0,), (arbitrary_force,)) == power


def test_rayleigh_matrix_derives_force_power_and_energy_loss() -> None:
    u, w, d1, d2 = sp.symbols("u w d_1 d_2", real=True, positive=True)
    result = rayleigh_dissipation((u, w), sp.diag(d1, d2))
    expected_power = d1 * u**2 + d2 * w**2
    assert result.rayleigh_function == expected_power / 2
    assert result.generalized_force == sp.ImmutableMatrix([-d1 * u, -d2 * w])
    assert result.dissipated_power == expected_power
    assert result.energy_rate_without_external_work == -expected_power


def test_external_work_is_a_separate_reservoir_term() -> None:
    u, d, applied = sp.symbols("u d F_ext", positive=True)
    result = rayleigh_dissipation((u,), sp.diag(d))
    assert sp.simplify(
        energy_rate_with_external_work(result, (applied,))
        - (applied * u - d * u**2)
    ) == 0
    assert energy_rate_with_external_work(result, (d * u,)) == 0


def test_semidefinite_cross_coupling_and_null_mode_are_retained() -> None:
    rate1, rate2, damping = sp.symbols("u_1 u_2 d", real=True, positive=True)
    matrix = damping * sp.ones(2)
    result = rayleigh_dissipation((rate1, rate2), matrix)
    assert result.dissipated_power == damping * (rate1 + rate2) ** 2
    assert result.dissipated_power.subs(rate2, -rate1) == 0


@pytest.mark.parametrize(
    "call",
    [
        lambda: metric_power_balance(1.0, (1,)),
        lambda: metric_power_balance(1, (1.0,)),
        lambda: metric_power_balance(-1, (1,)),
        lambda: metric_power_balance(1, (1, 2), sp.eye(1)),
        lambda: metric_power_balance(1, (1, 2), sp.Matrix([[1, 1], [0, 1]])),
        lambda: metric_power_balance(1, (1, 2), sp.diag(1, -1)),
        lambda: rayleigh_dissipation((1, 2), sp.Matrix([[1, 1], [0, 1]])),
        lambda: rayleigh_dissipation((1, 2), sp.diag(1, -1)),
        lambda: rayleigh_dissipation((1,), sp.Matrix([[1.0]])),
    ],
)
def test_invalid_or_inexact_balance_data_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()


def test_public_api_preserves_the_scope_ceiling() -> None:
    assert framework.metric_power_balance is metric_power_balance
    assert framework.rayleigh_dissipation is rayleigh_dissipation
    assert "does not normally select" in framework.generalized_dissipation.__doc__
