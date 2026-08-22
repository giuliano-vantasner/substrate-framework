"""Tests for exact isotropic elasticity identities."""

from __future__ import annotations

import sympy as sp

from substrate_framework.elasticity import (
    acoustic_speeds_squared,
    christoffel_matrix,
    hooke_stress,
    isotropic_stiffness,
    navier_cauchy_operator,
    poisson_ratio,
    project_divergence_free,
    strong_elliptic,
)


def test_hooke_stress_matches_hand_contraction() -> None:
    stiffness = isotropic_stiffness(3, 5)
    strain = sp.Matrix([[2, 0, 0], [0, 0, 0], [0, 0, 0]])
    sigma = hooke_stress(stiffness, strain)
    assert sp.simplify(sigma[0, 0] - (3 * 2 + 2 * 5 * 2)) == 0
    assert sp.simplify(sigma[1, 1] - 3 * 2) == 0 and sigma[0, 1] == 0


def test_navier_cauchy_residual_zero_for_exact_solution() -> None:
    x, y, z, t = sp.symbols("x y z t")
    lam, mu, rho = sp.symbols("lam mu rho", positive=True)
    fields = [sp.Function(f"u{a}")(t, x, y, z) for a in range(3)]
    residual = navier_cauchy_operator(fields, (x, y, z), t, lam, mu, rho)
    expected_inertia = rho * sp.diff(fields[0], t, 2)
    laplace = sum(sp.diff(sp.diff(fields[0], v), v) for v in (x, y, z))
    div = sum(sp.diff(u, c) for u, c in zip(fields, (x, y, z)))
    elastic = mu * laplace + (lam + mu) * sp.diff(div, x)
    assert sp.simplify(residual[0] - (expected_inertia - elastic)) == 0


def test_christoffel_eigenvalues_are_wave_speed_squares() -> None:
    lam, mu, rho = sp.symbols("lam mu rho", positive=True)
    direction = sp.Matrix([1, 0, 0])
    matrix = christoffel_matrix(lam, mu, rho, direction)
    speeds = acoustic_speeds_squared(lam, mu, rho)
    spectrum = {sp.simplify(value) for value in matrix.eigenvals()}
    assert sp.simplify(speeds["P"]) in spectrum
    assert sp.simplify(speeds["S"]) in spectrum
    assert len(spectrum) == 2


def test_poisson_and_strong_ellipticity_limits() -> None:
    lam, mu = sp.symbols("lam mu", positive=True)
    assert sp.simplify(poisson_ratio(lam, mu) - lam / (2 * (lam + mu))) == 0
    assert sp.simplify(poisson_ratio(mu, mu)) == sp.Rational(1, 4)
    assert strong_elliptic(1, 1)
    assert not strong_elliptic(-3, 1)


def test_divergence_free_projection() -> None:
    k = sp.Matrix([2, 0, 0])
    amplitude = sp.Matrix([1, 3, 4])
    projected = project_divergence_free(k, amplitude)
    assert sp.simplify(projected[0]) == 0
    assert sp.simplify(projected[1] - 3) == 0
