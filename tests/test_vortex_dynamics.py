"""Tests for periodic point-vortex dynamics."""

from __future__ import annotations

import numpy as np
import pytest

from substrate_framework.vortex_dynamics import (
    deviatoric_kinetic_stress,
    ensemble_projection_record,
    hamiltonian,
    impulse,
    pair_separations,
    rk4_step,
    velocities,
)


def test_dipole_translates_perpendicular_to_axis() -> None:
    box = 2.0 * np.pi
    positions = np.array([[1.0, 1.0], [1.5, 1.0]])
    circulations = np.array([1.0, -1.0])
    vel = velocities(positions, circulations, box)
    assert np.allclose(vel[0], vel[1], atol=1e-12)
    assert vel[0][1] > 0.0 and abs(vel[0][0]) < 1e-12


def test_pair_speed_matches_closed_form_kernel() -> None:
    box = 2.0 * np.pi
    separation = 0.5
    positions = np.array([[1.0, 1.0], [1.0 + separation, 1.0]])
    circulations = np.array([1.0, 1.0])
    speed = float(np.linalg.norm(velocities(positions, circulations, box)[0]))
    angle = 2.0 * np.pi * separation / box
    expected = float(np.sinh(angle) / (2.0 * box * (np.cosh(angle) - 1.0)))
    assert speed == pytest.approx(expected, rel=1e-12)


def test_minimum_image_separations_wrap() -> None:
    box = 2.0
    positions = np.array([[0.1, 0.5], [1.9, 0.5]])
    dx, _ = pair_separations(positions, box)
    assert dx[0, 1] == pytest.approx(0.2)
    assert dx[1, 0] == pytest.approx(-0.2)


def test_hamiltonian_and_impulse_conserved_under_evolution() -> None:
    box = 2.0 * np.pi
    rng = np.random.default_rng(21)
    positions = rng.uniform(0.0, box, size=(16, 2))
    circulations = np.ones(16)
    dt, steps = 1.0e-3, 1500
    energy_zero = hamiltonian(positions, circulations, box)
    current = positions
    for _ in range(steps):
        current = np.mod(rk4_step(current, circulations, box, dt), box)
    drift = abs(hamiltonian(current, circulations, box) - energy_zero) / abs(
        energy_zero
    )
    assert drift < 1e-4
    initial_impulse = np.sum(impulse(positions, circulations), axis=0) % box
    final_impulse = np.sum(impulse(current, circulations), axis=0) % box
    assert np.allclose(initial_impulse, final_impulse, atol=1e-8)


def test_deviatoric_stress_is_trace_free_symmetric() -> None:
    box = 2.0 * np.pi
    rng = np.random.default_rng(5)
    positions = rng.uniform(0.0, box, size=(24, 2))
    circulations = np.ones(24)
    stress = deviatoric_kinetic_stress(positions, circulations, box)
    assert np.allclose(stress, stress.T, atol=1e-14)
    assert float(np.trace(stress)) == pytest.approx(0.0, abs=1e-12)


def test_frozen_configuration_has_unit_persistence() -> None:
    from substrate_framework.vortex_dynamics import stress_projection_record

    box = 2.0 * np.pi
    rng = np.random.default_rng(9)
    positions = rng.uniform(0.0, box, size=(20, 2))
    circulations = np.ones(20)
    record = stress_projection_record(
        positions.copy(), circulations, box, dt=1.0e-3, steps=1, sample_every=1
    )
    assert record["initial_projection"] == pytest.approx(1.0)
