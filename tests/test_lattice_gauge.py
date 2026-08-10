"""Construction-independent tests for periodic lattice gauge-link utilities."""

from __future__ import annotations

import numpy as np
import pytest

from substrate_framework.lattice_gauge import (
    covariant_laplacian_spectrum,
    cycle_holonomy,
    plaquette_holonomies,
)


def _identity_links(n_side: int, dimension: int = 2) -> tuple[np.ndarray, np.ndarray]:
    identity = np.eye(dimension, dtype=complex)
    shape = (n_side, n_side, dimension, dimension)
    return np.broadcast_to(identity, shape).copy(), np.broadcast_to(identity, shape).copy()


def _periodic_free_spectrum(n_side: int, dimension: int) -> np.ndarray:
    values = [
        4 * np.sin(np.pi * k1 / n_side) ** 2
        + 4 * np.sin(np.pi * k2 / n_side) ** 2
        for k1 in range(n_side)
        for k2 in range(n_side)
        for _ in range(dimension)
    ]
    return np.sort(np.asarray(values))


def _random_su2_field(n_side: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    pauli = np.asarray(
        [
            [[0, 1], [1, 0]],
            [[0, -1j], [1j, 0]],
            [[1, 0], [0, -1]],
        ],
        dtype=complex,
    )
    gauge = np.empty((n_side, n_side, 2, 2), dtype=complex)
    for n1 in range(n_side):
        for n2 in range(n_side):
            axis = rng.normal(size=3)
            axis /= np.linalg.norm(axis)
            angle = rng.uniform(0, 2 * np.pi)
            gauge[n1, n2] = (
                np.cos(angle) * np.eye(2)
                + 1j * np.sin(angle) * np.tensordot(axis, pauli, axes=1)
            )
    return gauge


def _gauge_transform(
    links: tuple[np.ndarray, np.ndarray], gauge: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    first, second = links
    n_side = first.shape[0]
    transformed_first = np.empty_like(first)
    transformed_second = np.empty_like(second)
    for n1 in range(n_side):
        for n2 in range(n_side):
            transformed_first[n1, n2] = (
                gauge[n1, n2]
                @ first[n1, n2]
                @ gauge[(n1 + 1) % n_side, n2].conj().T
            )
            transformed_second[n1, n2] = (
                gauge[n1, n2]
                @ second[n1, n2]
                @ gauge[n1, (n2 + 1) % n_side].conj().T
            )
    return transformed_first, transformed_second


def test_identity_links_have_trivial_plaquettes_and_cycles() -> None:
    links = _identity_links(4)
    identity = np.eye(2)
    assert np.allclose(plaquette_holonomies(links), identity)
    for direction in (0, 1):
        for fixed_coordinate in range(4):
            assert np.allclose(
                cycle_holonomy(links, direction, fixed_coordinate), identity
            )


def test_identity_link_spectrum_matches_independent_fourier_formula() -> None:
    n_side = 5
    dimension = 2
    computed = covariant_laplacian_spectrum(_identity_links(n_side, dimension))
    expected = _periodic_free_spectrum(n_side, dimension)
    assert np.max(np.abs(computed - expected)) < 1e-12


def test_local_gauge_transform_preserves_spectrum_and_trivial_curvature() -> None:
    n_side = 4
    links = _identity_links(n_side)
    transformed = _gauge_transform(links, _random_su2_field(n_side, seed=0))
    original_spectrum = covariant_laplacian_spectrum(links)
    transformed_spectrum = covariant_laplacian_spectrum(transformed)
    assert np.max(np.abs(original_spectrum - transformed_spectrum)) < 1e-12
    transformed_plaquettes = plaquette_holonomies(transformed)
    assert np.max(np.abs(transformed_plaquettes - np.eye(2))) < 1e-12


def test_link_input_contract_rejects_nonunitary_and_malformed_fields() -> None:
    valid = _identity_links(4)
    nonunitary = (valid[0].copy(), valid[1].copy())
    nonunitary[0][0, 0, 0, 0] = 2
    with pytest.raises(ValueError, match="must be unitary"):
        plaquette_holonomies(nonunitary)
    with pytest.raises(ValueError, match="identical shapes"):
        plaquette_holonomies((valid[0], valid[1][:-1]))
    with pytest.raises(ValueError, match="direction must be 0 or 1"):
        cycle_holonomy(valid, 2, 0)
    with pytest.raises(ValueError, match="finite and positive"):
        covariant_laplacian_spectrum(valid, lattice_spacing=0)
