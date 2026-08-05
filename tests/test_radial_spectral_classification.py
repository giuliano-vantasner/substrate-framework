from __future__ import annotations

import numpy as np
import pytest
import sympy as sp

from substrate_framework.radial_spectral_classification import (
    bracketed_spherical_bessel_zero,
    central_radial_liouville_evidence,
    endpoint_decay_evidence,
    hard_zero_endpoint_counterexample,
    radial_threshold_form_evidence,
    vacuum_dirichlet_ball_evidence,
)


def test_liouville_reduction_norm_and_origin_power_are_exact() -> None:
    radius = sp.symbols("r", positive=True)
    energy = sp.symbols("E", real=True)
    potential = sp.Function("V")(radius)
    transformed = sp.Function("chi")(radius)
    evidence = central_radial_liouville_evidence(
        transformed,
        potential,
        energy,
        radius,
        2,
    )
    assert evidence.scaled_residual_difference == 0
    assert evidence.norm_density_difference == 0
    assert evidence.regular_radial_power == 2
    assert evidence.regular_transformed_power == 3
    assert sp.simplify(
        evidence.transformed_residual
        + sp.diff(transformed, radius, 2)
        - (6 / radius**2 + potential - energy) * transformed
    ) == 0


def test_wrong_liouville_power_leaves_a_load_bearing_residual() -> None:
    radius = sp.symbols("r", positive=True)
    transformed = sp.Function("chi")(radius)
    wrong_radial_mode = transformed / radius**2
    wrong_residual = sp.simplify(
        radius
        * (
            -sp.diff(wrong_radial_mode, radius, 2)
            - 2 * sp.diff(wrong_radial_mode, radius) / radius
            + 6 * wrong_radial_mode / radius**2
        )
        - (-sp.diff(transformed, radius, 2) + 6 * transformed / radius**2)
    )
    assert wrong_residual != 0
    assert wrong_residual.has(sp.diff(transformed, radius))


def test_vacuum_ball_mode_and_inverse_wall_square_are_exact() -> None:
    coordinate = sp.symbols("r", positive=True)
    radius, threshold, zero = sp.symbols("R mu2 z", positive=True)
    evidence = vacuum_dirichlet_ball_evidence(radius, threshold, zero, coordinate, 2)
    assert evidence.differential_residual == 0
    assert evidence.spectral_value == threshold + zero**2 / radius**2
    doubled = vacuum_dirichlet_ball_evidence(2 * radius, threshold, zero, coordinate, 2)
    assert sp.simplify(
        (evidence.spectral_value - threshold)
        / (doubled.spectral_value - threshold)
        - 4
    ) == 0
    wrong_centrifugal_residual = sp.simplify(
        evidence.differential_residual - evidence.radial_mode / coordinate**2
    )
    assert wrong_centrifugal_residual != 0


def test_bracketed_l2_zero_rederives_boundary_and_level() -> None:
    root = bracketed_spherical_bessel_zero(2, (5.0, 6.5))
    assert root.zero == pytest.approx(5.76345919689455, rel=0.0, abs=2.0e-13)
    assert root.absolute_residual < 2.0e-16
    coordinate = sp.symbols("r", positive=True)
    evidence = vacuum_dirichlet_ball_evidence(40.0, 1.0, root.zero, coordinate, 2)
    assert float(evidence.spectral_value) == pytest.approx(1.02076091369642, abs=2.0e-13)
    boundary = float(sp.N(evidence.outer_boundary_value, 17))
    assert abs(boundary) < 2.0e-16
    with pytest.raises(ValueError, match="strict spherical-Bessel sign change"):
        bracketed_spherical_bessel_zero(2, (1.0, 2.0))


def test_threshold_form_exposes_conditional_premise_and_negative_mutation() -> None:
    radius = sp.symbols("r", positive=True)
    transformed = sp.Function("chi")(radius)
    threshold = sp.symbols("mu2", real=True)
    nonnegative = radial_threshold_form_evidence(
        transformed,
        threshold,
        threshold,
        radius,
        2,
    )
    assert nonnegative.excess_potential == 6 / radius**2
    assert sp.simplify(
        nonnegative.quadratic_form_density
        - sp.diff(transformed, radius) ** 2
        - 6 * transformed**2 / radius**2
    ) == 0
    attractive = radial_threshold_form_evidence(
        transformed,
        threshold - 7 / radius**2,
        threshold,
        radius,
        2,
    )
    assert attractive.excess_potential == -1 / radius**2


def test_forced_zero_endpoint_passes_but_is_not_discriminating() -> None:
    forced = hard_zero_endpoint_counterexample(0.2)
    assert forced.passes
    assert forced.endpoint_forced
    assert not forced.endpoint_value_is_discriminating
    unforced = endpoint_decay_evidence(0.2, 0.02)
    assert not unforced.passes
    assert unforced.endpoint_value_is_discriminating
    too_small = hard_zero_endpoint_counterexample(1.0e-4)
    assert not too_small.passes


@pytest.mark.parametrize("bad_ell", [-1, 1.5, True])
def test_invalid_angular_momentum_is_rejected(bad_ell: object) -> None:
    radius = sp.symbols("r", positive=True)
    with pytest.raises(ValueError, match="nonnegative integer"):
        central_radial_liouville_evidence(
            sp.Function("chi")(radius),
            1,
            1,
            radius,
            bad_ell,  # type: ignore[arg-type]
        )


def test_endpoint_inputs_are_finite_and_thresholds_are_typed() -> None:
    with pytest.raises(ValueError, match="finite"):
        endpoint_decay_evidence(np.nan, 0.0)
    with pytest.raises(ValueError, match="smaller than one"):
        endpoint_decay_evidence(1.0, 0.0, relative_tolerance=1.0)
    with pytest.raises(ValueError, match="boolean"):
        endpoint_decay_evidence(1.0, 0.0, endpoint_forced=1)  # type: ignore[arg-type]
