"""Conditional stress-energy analysis of toronic flux-tube ensembles.

Authority status: conditional, unpromoted infrastructure linked to open goal
issue #26.  These symbols encode the ensemble/coarse-graining analysis of a
putative vacuum of oriented flux tubes (transverse toronic cell of side L,
one unit of Z2 't Hooft flux per tube).

Exact statements implemented:

[E-1] Single static tube along x3 with rho_t = -c L^-4 (any nonzero c):
      translation invariance along the tube gives p_parallel = -rho_t;
      transverse pressure from p_perp = -d(rho_t A)/dA with A = L^2 gives
      p_perp = +rho_t.  Isotropic orientation averaging of the tube stress
      then yields <T^ij> = (rho_t/3) delta^ij, i.e. w = +1/3, not the -1 of
      a Lorentz-invariant vacuum.
[E-2] No normalizable boost-invariant ensemble of timelike tubes exists:
      the invariant measure on the boost orbit has volume element
      sinh(eta) d eta (per transverse direction), whose integral diverges.
      The Euclidean analogue Gr(2,4) is compact with finite invariant
      volume - but an O(4) ensemble of spacetime membranes is not a static
      vacuum.
[E-3] Modulus instability: with the preprint's sign (c > 0, rho_t < 0) the
      energy is unbounded below as L -> 0; with the corrected sign (c < 0 in
      rho_t = -c L^-4, i.e. positive density) the twisted cell is disfavored
      at every L and L runs away to infinity.  No stationary point exists in
      either case.
"""

from __future__ import annotations

from typing import Any

import sympy as sp


def tube_transverse_pressure(coefficient: Any) -> sp.Expr:
    """p_perp for a tube with rho_t(L) = -coefficient * L^-4, A = L^2.

    p_perp = -d(rho_t A)/dA evaluated exactly: with rho_t = -c L^-4 one has
    rho_t + (L/2) rho_t' = -rho_t + ... -> p_perp = +rho_t = -c L^-4.
    """

    c = sp.sympify(coefficient)
    L = sp.Symbol("L", positive=True)
    rho = -c * L**-4
    area = L**2
    energy_per_length = rho * area
    p_perp = -sp.simplify(sp.diff(energy_per_length, L) / sp.diff(area, L))
    return p_perp


def tube_longitudinal_pressure(coefficient: Any) -> sp.Expr:
    """p_parallel = -rho_t for a static uniform tube (tension = energy/length)."""

    c = sp.sympify(coefficient)
    L = sp.Symbol("L", positive=True)
    rho = -c * L**-4
    return sp.simplify(-rho)


def isotropic_average_equation_of_state(coefficient: Any) -> sp.Expr:
    """w = p/rho of the isotropic ensemble of static tubes.

    <T^ij> = (1/3)(2 p_perp + p_parallel) delta^ij follows from the exact
    orientation average <n_i n_j> = delta_ij/3 over S^2.  Returns w.
    """

    c = sp.sympify(coefficient)
    L = sp.Symbol("L", positive=True)
    rho = -c * L**-4
    p_perp = tube_transverse_pressure(c)
    p_parallel = tube_longitudinal_pressure(c)
    p_avg = sp.simplify((2 * p_perp + p_parallel) / 3)
    return sp.simplify(p_avg / rho)


def orientation_average_nn(i: int, j: int) -> sp.Expr:
    """Exact <n_i n_j> over the unit sphere: delta_ij / 3."""

    theta, phi = sp.symbols("theta phi", positive=True)
    n = (
        sp.sin(theta) * sp.cos(phi),
        sp.sin(theta) * sp.sin(phi),
        sp.cos(theta),
    )
    measure = sp.sin(theta)
    average = sp.integrate(
        n[i] * n[j] * measure,
        (theta, 0, sp.pi),
        (phi, 0, 2 * sp.pi),
    ) / sp.integrate(measure, (theta, 0, sp.pi), (phi, 0, 2 * sp.pi))
    return sp.simplify(average)


def boost_orbit_measure_volume() -> sp.Expr:
    """Invariant volume of the boost orbit of a timelike tube: infinite.

    The rapidity measure per transverse direction is sinh(eta) d eta; the
    orbit integral diverges, so no normalizable Lorentz-invariant ensemble
    of timelike flux tubes exists.
    """

    eta = sp.Symbol("eta", positive=True)
    return sp.integrate(sp.sinh(eta), (eta, 0, sp.oo))


def euclidean_plane_measure_is_finite() -> bool:
    """Contrast: the Euclidean Gr(2,4) of 2-planes is compact.

    Encoded as the finiteness of the invariant angle integral over the
    compact domain; the boost (noncompact) counterpart diverges, see
    ``boost_orbit_measure_volume``.
    """

    theta = sp.Symbol("theta", positive=True)
    volume = sp.integrate(sp.sin(2 * theta) ** 2, (theta, 0, sp.pi / 2))
    return bool(sp.simplify(volume).is_finite)


def modulus_stationary_point_exists(coefficient_sign: int) -> bool:
    """[E-3]: d rho_t/dL = 0 has no solution at finite L, either sign."""

    if coefficient_sign not in (1, -1):
        raise ValueError("coefficient_sign must be +1 or -1")
    c = sp.Symbol("c", positive=True)
    L = sp.Symbol("L", positive=True)
    rho = -coefficient_sign * c * L**-4
    derivative = sp.simplify(sp.diff(rho, L))
    solutions = sp.solve(sp.Eq(derivative, 0), L)
    return len([s for s in solutions if s.is_positive]) > 0
