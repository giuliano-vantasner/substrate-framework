"""Exact screen of the P240 alternating derivative-sextic Skyrme current."""

from __future__ import annotations

from itertools import product

import sympy as sp

from substrate_framework.verification import CheckLedger


ETA = sp.diag(-1, 1, 1, 1)


def _alternating_current(currents: tuple[sp.Matrix, ...]) -> sp.Matrix:
    return sp.Matrix(
        4,
        1,
        lambda mu, _: sp.factor(
            sum(
                sp.LeviCivita(mu, nu, rho, sigma)
                * sp.trace(currents[nu] * currents[rho] * currents[sigma])
                for nu, rho, sigma in product(range(4), repeat=3)
            )
            / 6
        ),
    )


def _generator(left: int, right: int) -> sp.Matrix:
    value = sp.zeros(3)
    value[left, right] = -1
    value[right, left] = 1
    return value


def _symmetric_preimage(y: sp.Matrix, generator: sp.Matrix) -> sp.Matrix:
    result = sp.zeros(3)
    for left in range(3):
        for right in range(left + 1, 3):
            if generator[left, right] != 0:
                result[left, right] = result[right, left] = (
                    generator[left, right] / (y[left, left] - y[right, right])
                )
    return result


def main() -> int:
    ledger = CheckLedger("P240/alternating-sextic")
    y = sp.diag(1, 2, 4)
    target_currents = (
        _generator(1, 2),
        _generator(2, 0),
        _generator(0, 1),
        sp.zeros(3),
    )
    derivatives = tuple(_symmetric_preimage(y, value) for value in target_currents)
    currents = tuple(y * value - value * y for value in derivatives)
    ledger.check(
        "all witness currents are generated from one Y and symmetric Z_mu",
        currents == target_currents
        and all(value == value.T for value in derivatives),
    )
    alternating = _alternating_current(currents)
    ledger.check(
        "alternating current has a nonzero spatial clock component",
        alternating[3] != 0
        and alternating[0] == alternating[1] == alternating[2] == 0,
    )
    mutated = _alternating_current((currents[0], currents[1], sp.zeros(3), currents[3]))
    ledger.check(
        "removing one load-bearing spatial current kills the witness",
        mutated == sp.zeros(4, 1),
    )

    s1, s2, s3 = sp.symbols("s1 s2 s3", real=True)
    static_currents = (
        sp.zeros(3),
        s1 * _generator(1, 2),
        s2 * _generator(2, 0),
        s3 * _generator(0, 1),
    )
    static_alternating = _alternating_current(static_currents)
    spatial_metric = sp.diag(0, 1, 1, 1)
    ledger.check(
        "spatially projected density is identically static null",
        sp.factor((static_alternating.T * spatial_metric * static_alternating)[0])
        == 0
        and static_alternating[0] != 0,
    )
    omega, kappa, n = sp.symbols("omega kappa n", positive=True)
    velocity_currents = (omega * currents[0], *currents[1:])
    velocity_current = _alternating_current(velocity_currents)
    density = sp.factor(
        kappa * n**2 * (velocity_current.T * spatial_metric * velocity_current)[0]
    )
    ledger.check(
        "comoving density is a positive velocity square",
        density.subs(omega, 1) > 0
        and sp.diff(density, omega, 2) != 0
        and sp.diff(velocity_current[3], omega, 2) == 0,
    )
    ledger.check("zero-eigenline axis weight kills the density", density.subs(n, 0) == 0)

    boost = sp.eye(4)
    boost[0, 0] = boost[1, 1] = sp.Rational(5, 3)
    boost[0, 1] = boost[1, 0] = sp.Rational(4, 3)
    inverse = boost.inv()
    transformed_currents = tuple(
        sp.simplify(
            sum((inverse[rho, mu] * currents[rho] for rho in range(4)), sp.zeros(3))
        )
        for mu in range(4)
    )
    transformed_alternating = _alternating_current(transformed_currents)
    time_vector = sp.Matrix([1, 0, 0, 0])
    boosted_time = boost * time_vector
    time_covariant = ETA * boosted_time
    boosted_spatial_metric = ETA + time_covariant * time_covariant.T
    ledger.check(
        "alternating spatial norm is an exact proper-Lorentz scalar",
        boost.T * ETA * boost == ETA
        and sp.simplify(transformed_alternating - boost * alternating) == sp.zeros(4, 1)
        and sp.simplify(
            (transformed_alternating.T * boosted_spatial_metric * transformed_alternating)[0]
            - (alternating.T * spatial_metric * alternating)[0]
        )
        == 0,
    )
    parity = sp.diag(1, -1, 1, 1)
    parity_currents = tuple(
        sp.simplify(
            sum((parity[rho, mu] * currents[rho] for rho in range(4)), sp.zeros(3))
        )
        for mu in range(4)
    )
    parity_alternating = _alternating_current(parity_currents)
    ledger.check(
        "alternating current is pseudo while its spatial square is parity even",
        parity_alternating == -parity * alternating
        and sp.simplify(
            (parity_alternating.T * spatial_metric * parity_alternating)[0]
            - (alternating.T * spatial_metric * alternating)[0]
        )
        == 0,
    )
    radius, curvature, potential, inertia, momentum = sp.symbols(
        "R A B I_0 J", positive=True
    )
    scale_energy = curvature / radius + potential * radius**3 + momentum**2 * radius / (4 * inertia)
    ledger.check(
        "derivative-sextic inertia has the distinct I over R scaling",
        sp.limit(momentum**2 * radius / (4 * inertia), radius, 0, dir="+") == 0
        and sp.limit(momentum**2 * radius / (4 * inertia), radius, sp.oo) == sp.oo,
    )
    ledger.check(
        "full fixed-J scale energy has a finite strict minimum",
        sp.limit(scale_energy, radius, 0, dir="+") == sp.oo
        and sp.limit(scale_energy, radius, sp.oo) == sp.oo
        and sp.simplify(
            sp.diff(scale_energy, radius, 2)
            - (2 * curvature / radius**3 + 6 * potential * radius)
        )
        == 0
        and (2 * curvature / radius**3 + 6 * potential * radius).is_positive
        is True,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
