"""Conditional stress-energy analysis of toronic flux-tube ensembles.

Authority status: conditional, unpromoted infrastructure linked to open goal
issue #28 (vantasnerdan/substrate-framework), split from the issue #26 audit
per the 2026-08-10 harvest review.  No accepted claim backs these symbols.

Exact statements implemented:

[E-1] Single static tube along x3 with rho_t = -c L^-4 (any nonzero c):
      translation invariance along the tube gives p_parallel = -rho_t;
      transverse pressure from p_perp = -d(rho_t A)/dA with A = L^2 gives
      p_perp = +rho_t.  Isotropic orientation averaging of the tube stress
      then yields <T^ij> = (rho_t/3) delta^ij, i.e. w = +1/3, not the -1 of
      a Lorentz-invariant vacuum.
[E-2] Orbit measures are DERIVED, not declared.  The Lorentz orbit of a
      timelike tube axis is the hyperboloid H^k in R^{1,k}; its invariant
      measure is the induced metric measure, computed here from the
      embedding u(eta, angles): for k = 3 the induced metric is
      diag(1, sinh^2 eta, sinh^2 eta sin^2 theta), the radial integral of
      sinh^2 eta diverges, and the orbit volume is infinite - no
      normalizable boost-invariant ensemble of timelike tubes exists.  The
      Euclidean contrast: the oriented Grassmannian Gr~(2,4) is diffeomorphic
      to S^2 x S^2 via the self-dual/anti-self-dual split of e1 wedge e2
      (|omega_+|^2 = |omega_-|^2 = 1/2, verified symbolically; SO(4)
      invariance makes the split constant on the orbit), so its invariant
      volume is vol(S^2)^2 = 16 pi^2, finite - but an O(4) ensemble of
      spacetime membranes is not a static vacuum.
[E-3] Modulus instability: with the preprint's sign (c > 0, rho_t < 0) the
      energy is unbounded below as L -> 0; with the corrected sign the
      twisted cell is disfavored at every L and L runs away to infinity.
      No stationary point exists in either case.
"""

from __future__ import annotations

from typing import Any

import sympy as sp

# ---------------------------------------------------------------------------
# single-tube stress and isotropic average
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# derived orbit measures
# ---------------------------------------------------------------------------


def _induced_metric(embedding: sp.Matrix, parameters: list, signature: list[int]) -> sp.Matrix:
    """Pullback of the ambient constant metric to the orbit parameters."""

    dim = len(parameters)
    sig = sp.diag(*signature)
    return sp.Matrix(
        dim,
        dim,
        lambda i, j: sp.trigsimp(
            (embedding.diff(parameters[i]).T * sig * embedding.diff(parameters[j]))[0]
        ),
    )


def timelike_axis_induced_metric() -> sp.Matrix:
    """Induced metric on the timelike-axis orbit H^3 in R^{1,3}.

    u(eta, theta, phi) = (cosh eta, sinh eta n(theta, phi)) with ambient
    signature (-,+,+,+).  Returns diag(1, sinh^2 eta, sinh^2 eta sin^2 theta).
    """

    eta, theta, phi = sp.symbols("eta theta phi", positive=True, real=True)
    u = sp.Matrix(
        [
            sp.cosh(eta),
            sp.sinh(eta) * sp.sin(theta) * sp.cos(phi),
            sp.sinh(eta) * sp.sin(theta) * sp.sin(phi),
            sp.sinh(eta) * sp.cos(theta),
        ]
    )
    return _induced_metric(u, [eta, theta, phi], [-1, 1, 1, 1])


def timelike_axis_orbit_volume() -> sp.Expr:
    """Invariant volume of the timelike-axis orbit H^3: infinite (derived).

    The invariant measure is the induced-metric measure
    sinh^2(eta) sin(theta) d eta d theta d phi.  The radial integral is
    computed from the antiderivative in exponential form (sympy's hyperbolic
    limiter is unreliable): sinh^2(eta) integrates to
    sinh(2 eta)/4 - eta/2, which diverges to +infinity.
    """

    eta = sp.Symbol("eta", positive=True, real=True)
    radial_antiderivative = sp.integrate(sp.sinh(eta) ** 2, eta).rewrite(sp.exp).expand()
    radial = sp.limit(radial_antiderivative, eta, sp.oo)
    theta, phi = sp.symbols("theta phi", positive=True)
    angular = sp.integrate(sp.sin(theta), (theta, 0, sp.pi)) * sp.integrate(
        sp.Integer(1), (phi, 0, 2 * sp.pi)
    )
    return radial * angular


def _s2_volume() -> sp.Expr:
    """vol(S^2) = 4 pi from the induced metric of the standard embedding."""

    theta, phi = sp.symbols("theta phi", positive=True)
    u = sp.Matrix(
        [sp.sin(theta) * sp.cos(phi), sp.sin(theta) * sp.sin(phi), sp.cos(theta)]
    )
    metric = _induced_metric(u, [theta, phi], [1, 1, 1])
    element = sp.sqrt(sp.trigsimp(metric.det()))
    return sp.integrate(element, (theta, 0, sp.pi), (phi, 0, 2 * sp.pi))


def self_dual_split_norms_constant() -> bool:
    """|omega_+|^2 = |omega_-|^2 = 1/2 for omega = e1 wedge e2, exact.

    omega_± = (omega ± *omega)/2 on Lambda^2 R^4.  The norms are
    SO(4)-invariant functions of the oriented plane (basis change e1, e2 ->
    O(2) rotates omega by a sign at most), and SO(4) acts transitively on
    Gr~(2,4), so checking a symbolic two-parameter family of planes fixes
    the constant everywhere.
    """

    a, b = sp.symbols("a b", real=True)
    e1 = sp.Matrix([sp.cos(a), sp.sin(a), 0, 0])
    e2 = sp.Matrix([0, 0, sp.cos(b), sp.sin(b)])
    # omega as a 2-form in the six basis planes (12, 13, 14, 23, 24, 34)
    omega = sp.Matrix(
        [e1[i] * e2[j] - e1[j] * e2[i] for (i, j) in
         ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))]
    )
    # Hodge star on Lambda^2 R^4 in the ordered basis (12,13,14,23,24,34):
    # *12 = 34, *13 = -24, *14 = 23, *23 = 14, *24 = -13, *34 = 12
    star = sp.Matrix(
        [
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, -1, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, -1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
        ]
    )
    omega_plus = (omega + star * omega) / 2
    omega_minus = (omega - star * omega) / 2
    norm_plus = sp.trigsimp((omega_plus.T * omega_plus)[0])
    norm_minus = sp.trigsimp((omega_minus.T * omega_minus)[0])
    return bool(norm_plus == sp.Rational(1, 2) and norm_minus == sp.Rational(1, 2))


def oriented_grassmannian_2_4_volume() -> sp.Expr:
    """Invariant volume of oriented Gr~(2,4) ~ S^2 x S^2: 16 pi^2 (derived).

    The self-dual split maps a plane to (sqrt(2) omega_+, sqrt(2) omega_-)
    on unit spheres (norms verified by ``self_dual_split_norms_constant``);
    the unique SO(4)-invariant measure pushes to the product of round
    measures, each derived from the induced S^2 metric.
    """

    if not self_dual_split_norms_constant():
        raise RuntimeError("self-dual split identity failed")
    s2 = _s2_volume()
    return sp.simplify(s2 * s2)


# ---------------------------------------------------------------------------
# modulus analysis
# ---------------------------------------------------------------------------


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
