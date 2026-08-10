"""Exact induced geometry for narrowly named Lorentz-group orbits.

Authority status: conditional, unpromoted infrastructure linked to open goal
issue #28 (vantasnerdan/substrate-framework). The current public surface
describes only the Lorentz orbit of one future-directed unit timelike vector,
namely ``H^3``. It does not describe a timelike two-plane or tube worldsheet
orbit and makes no claim about a Lorentz-invariant tube ensemble.
"""

from __future__ import annotations

from typing import Sequence

import sympy as sp


def _induced_metric(
    embedding: sp.Matrix,
    parameters: Sequence[sp.Symbol],
    signature: Sequence[int],
) -> sp.Matrix:
    """Pull back a constant ambient metric to the supplied parameters."""

    dimension = len(parameters)
    ambient_metric = sp.diag(*signature)
    return sp.Matrix(
        dimension,
        dimension,
        lambda i, j: sp.trigsimp(
            (
                embedding.diff(parameters[i]).T
                * ambient_metric
                * embedding.diff(parameters[j])
            )[0]
        ),
    )


def unit_timelike_vector_orbit_metric() -> sp.Matrix:
    """Return the induced metric on the future unit-vector orbit ``H^3``.

    For ``u=(cosh eta, sinh eta*n(theta,phi))`` in signature ``(-,+,+,+)``,
    the result is ``diag(1, sinh(eta)^2, sinh(eta)^2*sin(theta)^2)``.
    """

    eta, theta, phi = sp.symbols("eta theta phi", positive=True, real=True)
    unit_vector = sp.Matrix(
        [
            sp.cosh(eta),
            sp.sinh(eta) * sp.sin(theta) * sp.cos(phi),
            sp.sinh(eta) * sp.sin(theta) * sp.sin(phi),
            sp.sinh(eta) * sp.cos(theta),
        ]
    )
    return _induced_metric(unit_vector, [eta, theta, phi], [-1, 1, 1, 1])


def unit_timelike_vector_orbit_volume() -> sp.Expr:
    """Return the infinite invariant volume of the unit-vector orbit ``H^3``.

    The induced volume element is
    ``sinh(eta)^2 sin(theta) d eta d theta d phi``. This result applies only to
    a unit timelike vector, not to a tube worldsheet orbit.
    """

    eta = sp.Symbol("eta", positive=True, real=True)
    radial_antiderivative = (
        sp.integrate(sp.sinh(eta) ** 2, eta).rewrite(sp.exp).expand()
    )
    radial_volume = sp.limit(radial_antiderivative, eta, sp.oo)
    theta, phi = sp.symbols("theta phi", positive=True)
    angular_volume = sp.integrate(
        sp.sin(theta),
        (theta, 0, sp.pi),
        (phi, 0, 2 * sp.pi),
    )
    return radial_volume * angular_volume
