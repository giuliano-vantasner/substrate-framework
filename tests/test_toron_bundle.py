"""Structural tests for the toronic bundle and flux background (issue #28)."""

from __future__ import annotations

import numpy as np
import sympy as sp

from substrate_framework.toron_bundle import (
    best_constant_twist_residual,
    cover_holonomy_commutator,
    cycle_two_holonomy,
    flat_toron_connection_exists,
    flux_background_candidates,
    landau_ground_dimensionless,
    minimal_flux_classical_energy_density,
    plaquette_holonomies,
    spectrum_from_links,
    transition_function_cocycle,
    uniform_flux_links,
)
from substrate_framework.twisted_casimir import (
    TORON_ADJOINT_TWISTS,
    vacuum_energy_difference,
)


# ---------------------------------------------------------------------------
# exact topology: the cocycle, the cover commutator, kernel membership
# ---------------------------------------------------------------------------


def test_cocycle_is_minus_identity_pair() -> None:
    z_su2, z_phase = transition_function_cocycle()
    assert z_su2 == -sp.eye(2)
    assert sp.simplify(z_phase - 1) == 0


def test_cover_commutator_is_phase_independent() -> None:
    su2_part, phase = cover_holonomy_commutator()
    assert su2_part == -sp.eye(2)
    assert sp.simplify(phase - 1) == 0  # for ALL symbolic lift phases a, b


def test_no_flat_connection_with_diagonal_z2_quotient() -> None:
    # the preprint's Sec. 10 quotient: no flat connection with fundamentals
    assert flat_toron_connection_exists("diagonal_z2") is False


def test_wrong_kernel_mutation_flips_verdict() -> None:
    # mutation sensitivity: PSU(2) x U(1) contains the cocycle, so flat
    # torons exist there; without any quotient the exact cocycle fails
    assert flat_toron_connection_exists("psu2_times_u1") is True
    assert flat_toron_connection_exists("no_quotient") is False


# ---------------------------------------------------------------------------
# classical flux energy
# ---------------------------------------------------------------------------


def test_flux_candidates_and_minimum() -> None:
    g = sp.Rational(65, 100)
    g_prime = sp.Rational(357, 1000)
    candidates = flux_background_candidates(g, g_prime)
    assert sp.simplify(candidates["su2"] - 2 * sp.pi**2 / g**2) == 0
    assert sp.simplify(candidates["u1_hypercharge"] - 2 * sp.pi**2 / g_prime**2) == 0
    minimum = minimal_flux_classical_energy_density(g, g_prime)
    # g > g' makes the su(2) representative the minimum
    assert sp.simplify(minimum - candidates["su2"]) == 0


def test_flux_classical_energy_dominates_one_loop() -> None:
    g = sp.Rational(65, 100)
    g_prime = sp.Rational(357, 1000)  # declared input: SU(2)l U(1)y coupling
    e_cl = minimal_flux_classical_energy_density(g, g_prime, 1)
    gauge_one_loop = vacuum_energy_difference(TORON_ADJOINT_TWISTS)
    ratio = float(e_cl.evalf()) / float(gauge_one_loop)
    assert ratio > 10


# ---------------------------------------------------------------------------
# lattice construction checks
# ---------------------------------------------------------------------------


def test_interior_plaquettes_exactly_uniform() -> None:
    n = 12
    links = uniform_flux_links(n)
    plaquettes = plaquette_holonomies(links)
    angle = np.pi / n**2
    target = np.diag([np.exp(1j * angle), np.exp(-1j * angle)])
    assert np.max(np.abs(plaquettes[:-1, :] - target)) < 1e-12


def test_wrap_plaquette_defect_vanishes_under_refinement() -> None:
    deviations = []
    for n in (8, 16, 24):
        links = uniform_flux_links(n)
        plaquettes = plaquette_holonomies(links)
        angle = np.pi / n**2
        target = np.diag([np.exp(1j * angle), np.exp(-1j * angle)])
        deviations.append(float(np.max(np.abs(plaquettes[-1, :] - target))))
    assert deviations[1] < deviations[0]
    assert deviations[2] < deviations[1]
    assert deviations[2] < 2 * np.pi / 24  # O(1/N)


def test_cycle_two_holonomy_winds_to_minus_identity() -> None:
    distances = []
    for n in (8, 16, 24):
        links = uniform_flux_links(n)
        holonomy = cycle_two_holonomy(links, n - 1)
        distances.append(float(np.max(np.abs(holonomy + np.eye(2)))))
    assert distances[1] < distances[0]
    assert distances[2] < distances[1]
    assert distances[2] < 0.15  # -> 0 as 1/N; the bundle class is nontrivial


def test_spectrum_gauge_covariance() -> None:
    n = 8
    links = uniform_flux_links(n)
    rng = np.random.default_rng(0)
    # random SU(2) gauge transformation at every site
    gauge = np.zeros((n, n, 2, 2), dtype=complex)
    for n1 in range(n):
        for n2 in range(n):
            a = rng.normal(size=3)
            a = a / np.linalg.norm(a)
            theta = rng.uniform(0, 2 * np.pi)
            sigma = np.array(
                [[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], complex
            )
            gauge[n1, n2] = np.cos(theta) * np.eye(2) + 1j * np.sin(theta) * np.tensordot(a, sigma, 1)
    u1, u2 = links
    g1 = np.zeros((n, n, 2, 2), dtype=complex)
    g2 = np.zeros((n, n, 2, 2), dtype=complex)
    for n1 in range(n):
        for n2 in range(n):
            g1[n1, n2] = gauge[n1, n2] @ u1[n1, n2] @ gauge[(n1 + 1) % n, n2].conj().T
            g2[n1, n2] = gauge[n1, n2] @ u2[n1, n2] @ gauge[n1, (n2 + 1) % n].conj().T
    original = spectrum_from_links(links)
    transformed = spectrum_from_links((g1, g2))
    assert np.max(np.abs(original - transformed)) < 1e-8


def test_ground_state_converges_to_landau_ground() -> None:
    target = float(landau_ground_dimensionless().evalf())
    deviations = []
    for n in (12, 18, 24):
        spectrum = spectrum_from_links(uniform_flux_links(n))
        ground = spectrum[spectrum > 1e-8][0]
        deviations.append(abs(ground / target - 1))
    assert deviations[-1] < deviations[0]  # refinement improves
    assert deviations[-1] < 0.1


def test_no_constant_twist_fits_continuous() -> None:
    # continuous falsifier: differential evolution over [0,1)^2
    spectrum = spectrum_from_links(uniform_flux_links(16))
    (_, _), best = best_constant_twist_residual(spectrum, modes=8)
    assert best > 0.05
