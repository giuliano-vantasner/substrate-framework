from __future__ import annotations

import numpy as np
import pytest
from scipy.special import jv

from substrate_framework.radial_harmonic_balance import (
    classify_harmonic_tail_channels,
    nonlinear_projection_remainder,
    odd_harmonics,
    project_sine_harmonics,
    reconstruct_radial_harmonics,
    sampled_harmonic_balance_residual,
    solve_radial_harmonic_balance,
)


def test_odd_harmonics_and_half_period_antisymmetry() -> None:
    modes = odd_harmonics(7)
    amplitudes = np.array([[1.2], [-0.3], [0.07], [-0.01]])
    phase = np.linspace(0.0, np.pi, 41)
    first = reconstruct_radial_harmonics(amplitudes, modes, phase)
    shifted = reconstruct_radial_harmonics(amplitudes, modes, phase + np.pi)

    assert modes == (1, 3, 5, 7)
    np.testing.assert_allclose(shifted, -first, atol=2.0e-15)
    with pytest.raises(ValueError):
        odd_harmonics(6)


def test_single_harmonic_projection_matches_jacobi_anger() -> None:
    amplitudes = np.array([[0.1, 1.0, 2.5]])
    targets = (1, 3, 5, 7)
    projected = project_sine_harmonics(
        amplitudes,
        (1,),
        target_harmonics=targets,
        temporal_samples=512,
    )
    expected = np.vstack(
        [
            2.0 * (-1.0) ** ((harmonic - 1) // 2) * jv(harmonic, amplitudes[0])
            for harmonic in targets
        ]
    )

    np.testing.assert_allclose(projected, expected, atol=5.0e-15)


def test_tail_channels_separate_fundamental_from_radiative_harmonics() -> None:
    channels = classify_harmonic_tail_channels((1, 3, 5), 0.9768739)

    assert [channel.behavior for channel in channels] == [
        "evanescent",
        "radiative",
        "radiative",
    ]
    assert channels[0].radial_rate == pytest.approx(
        np.sqrt(1.0 - 0.9768739**2)
    )
    threshold = classify_harmonic_tail_channels((1, 3), 1.0 / 3.0)
    assert threshold[1].behavior == "threshold"
    assert threshold[1].radial_rate == 0.0


def test_sampled_residual_rejects_a_fabricated_profile() -> None:
    radius = np.linspace(0.0, 20.0, 1001)
    zero = sampled_harmonic_balance_residual(radius, [np.zeros_like(radius)], (1,), 0.9)
    fabricated = 2.5 * np.exp(-np.square(radius / 2.0))
    wrong = sampled_harmonic_balance_residual(radius, [fabricated], (1,), 0.9769)

    assert np.max(np.abs(zero)) == 0.0
    assert np.sqrt(np.mean(wrong[:, 5:-5] ** 2)) > 0.1


def test_parameterized_branch_and_harmonic_continuation() -> None:
    one = solve_radial_harmonic_balance(
        (1,),
        central_fundamental=2.5,
        outer_radius=40.0,
        frequency_guess=0.9769,
        radial_points=240,
        temporal_samples=128,
        tolerance=2.0e-6,
    )
    three = solve_radial_harmonic_balance(
        (1, 3),
        central_fundamental=2.5,
        outer_radius=40.0,
        frequency_guess=one.frequency,
        temporal_samples=128,
        tolerance=2.0e-6,
        initial_solution=one,
    )
    one_remainder = nonlinear_projection_remainder(
        one.amplitudes, one.harmonics, temporal_samples=512
    )
    three_remainder = nonlinear_projection_remainder(
        three.amplitudes, three.harmonics, temporal_samples=512
    )

    assert one.completed and three.completed
    assert one.frequency == pytest.approx(0.976909, abs=3.0e-6)
    assert three.frequency == pytest.approx(0.976877, abs=4.0e-6)
    assert one.outer_conditions == ("decaying_robin",)
    assert three.outer_conditions == ("decaying_robin", "dirichlet_box")
    assert one.max_collocation_rms_residual < 2.1e-6
    assert three.max_collocation_rms_residual < 2.1e-6
    assert np.sqrt(np.mean(three_remainder**2)) < 0.2 * np.sqrt(
        np.mean(one_remainder**2)
    )
    np.testing.assert_allclose(three.central_amplitudes[0], 2.5, atol=2.0e-8)


def test_solver_rejects_nonodd_or_above_gap_inputs() -> None:
    with pytest.raises(ValueError):
        solve_radial_harmonic_balance(
            (1, 2),
            central_fundamental=2.5,
            outer_radius=40.0,
            frequency_guess=0.97,
        )
    with pytest.raises(ValueError):
        solve_radial_harmonic_balance(
            (1,),
            central_fundamental=2.5,
            outer_radius=40.0,
            frequency_guess=1.0,
        )
