from __future__ import annotations

import pytest
import sympy as sp

import substrate_framework as sf
from substrate_framework.bps_energy import (
    BogomolnyDensityDecomposition,
    NearBpsDifference,
    bogomolny_density_decomposition,
    bps_bound_per_absolute_degree,
    bps_topological_lower_bound,
    conditional_attained_bps_sector_energy,
    degree_weighted_target_pairing,
    near_bps_mass_difference,
    normalized_sqrt_potential_average,
    target_three_sphere_volume,
)


def test_bps_energy_api_is_package_exported() -> None:
    assert sf.BogomolnyDensityDecomposition is BogomolnyDensityDecomposition
    assert sf.NearBpsDifference is NearBpsDifference
    assert sf.bogomolny_density_decomposition is bogomolny_density_decomposition
    assert sf.bps_topological_lower_bound is bps_topological_lower_bound
    assert sf.near_bps_mass_difference is near_bps_mass_difference


def test_square_completion_is_exact_for_both_orientations() -> None:
    lam, mu, density, potential = sp.symbols(
        "lambda mu b_0 V",
        positive=True,
    )
    for orientation in (-1, 1):
        result = bogomolny_density_decomposition(
            density,
            potential,
            lam,
            mu,
            orientation=orientation,
        )
        assert result.identity_residual == 0
        assert result.square_density == result.saturation_residual**2
        saturated_density = orientation * mu * sp.sqrt(potential) / (
            lam * sp.pi**2
        )
        assert sp.simplify(
            result.saturation_residual.subs(density, saturated_density)
        ) == 0


def test_target_average_and_degree_pairing_keep_the_normalization_explicit() -> None:
    target_integral = 6 * sp.pi**2
    average = normalized_sqrt_potential_average(target_integral)
    assert target_three_sphere_volume() == 2 * sp.pi**2
    assert average == 3
    assert degree_weighted_target_pairing(2, average) == 6
    assert degree_weighted_target_pairing(-2, average) == -6


def test_bound_is_orientation_symmetric_but_pairing_is_signed() -> None:
    lam, mu, average = sp.symbols("lambda mu W", positive=True)
    coefficient = bps_bound_per_absolute_degree(lam, mu, average)
    assert coefficient == 2 * sp.pi**2 * lam * mu * average
    assert bps_topological_lower_bound(3, lam, mu, average) == 3 * coefficient
    assert bps_topological_lower_bound(-3, lam, mu, average) == 3 * coefficient
    assert degree_weighted_target_pairing(-3, average) == -3 * average


def test_attained_sector_energy_is_linear_only_under_its_named_premise() -> None:
    lam, mu, average = sp.symbols("lambda mu W", positive=True)
    mass_a = conditional_attained_bps_sector_energy(2, lam, mu, average)
    mass_na = conditional_attained_bps_sector_energy(6, lam, mu, average)
    assert sp.simplify(3 * mass_a - mass_na) == 0
    assert conditional_attained_bps_sector_energy(
        -2,
        lam,
        mu,
        average,
    ) == mass_a


def test_zero_potential_exposes_nonattainment_for_nonzero_degree() -> None:
    lam, mu = sp.symbols("lambda mu", positive=True)
    density = sp.Symbol("b_0", real=True)
    result = bogomolny_density_decomposition(
        density,
        0,
        lam,
        mu,
        orientation=1,
    )
    forced_density = sp.solve(sp.Eq(result.saturation_residual, 0), density)
    assert forced_density == [0]
    assert degree_weighted_target_pairing(1, 0) == 0
    # Saturation would force the normalized density integral to zero, contrary
    # to the separately declared nonzero degree.
    assert forced_density[0] != 1


def test_near_bps_ledger_cancels_only_the_balanced_linear_sector_term() -> None:
    epsilon, delta_a, delta_na, rho_a, rho_na, coefficient = sp.symbols(
        "epsilon Delta_A Delta_nA rho_A rho_nA K",
    )
    balanced = near_bps_mass_difference(
        2,
        6,
        multiplicity=3,
        bps_energy_per_degree=coefficient,
        epsilon=epsilon,
        base_correction=delta_a,
        composite_correction=delta_na,
        base_remainder=epsilon**2 * rho_a,
        composite_remainder=epsilon**2 * rho_na,
    )
    assert balanced.degree_balance == 0
    assert balanced.bps_term == 0
    assert balanced.linear_coefficient == 3 * delta_a - delta_na
    assert sp.simplify(
        balanced.remainder - epsilon**2 * (3 * rho_a - rho_na)
    ) == 0
    assert sp.simplify(
        balanced.expression
        - epsilon * (3 * delta_a - delta_na)
        - epsilon**2 * (3 * rho_a - rho_na)
    ) == 0

    unbalanced = near_bps_mass_difference(
        2,
        5,
        multiplicity=3,
        bps_energy_per_degree=coefficient,
        epsilon=epsilon,
        base_correction=delta_a,
        composite_correction=delta_na,
    )
    assert unbalanced.bps_term == coefficient
    assert unbalanced.expression.subs(epsilon, 0) == coefficient


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: normalized_sqrt_potential_average(-1), "nonnegative"),
        (lambda: degree_weighted_target_pairing(0, 1), "nonzero integer"),
        (
            lambda: bogomolny_density_decomposition(1, -1, 1, 1, orientation=1),
            "nonnegative",
        ),
        (
            lambda: bogomolny_density_decomposition(1, 1, 1, 1, orientation=0),
            "orientation",
        ),
        (lambda: bps_topological_lower_bound(1, 0, 1, 1), "positive"),
        (
            lambda: near_bps_mass_difference(
                1,
                2,
                multiplicity=0,
                bps_energy_per_degree=1,
                epsilon=sp.Symbol("epsilon"),
                base_correction=0,
                composite_correction=0,
            ),
            "positive integer",
        ),
    ],
)
def test_invalid_bps_inputs_fail_explicitly(call, message: str) -> None:
    with pytest.raises((TypeError, ValueError), match=message):
        call()
