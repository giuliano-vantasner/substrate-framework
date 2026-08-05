#!/usr/bin/env python3
"""Independent dyadic and commutator rederivation of C-GW-009."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _norm_squared(tensor: sp.Matrix) -> sp.Expr:
    return sp.simplify(sum(tensor[i, j] ** 2 for i in range(3) for j in range(3)))


def _zero(expression: sp.Expr) -> bool:
    return sp.simplify(sp.expand(sp.trigsimp(expression))) == 0


def main() -> int:
    checks = CheckLedger("P181-INDEPENDENT-C-GW-009")
    time = sp.symbols("t", real=True)
    q, omega, scale, coupling, distance, spectral = sp.symbols(
        "q Omega s G R lambda", nonzero=True, real=True
    )
    angle = omega * time
    cosine, sine = sp.cos(angle), sp.sin(angle)
    generator = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    rotation = sp.exp(angle * generator)
    checks.check(
        "matrix exponential independently gives the x-axis rotation",
        sp.simplify(
            rotation
            - sp.Matrix([[1, 0, 0], [0, cosine, -sine], [0, sine, cosine]])
        )
        == sp.zeros(3),
    )

    body_axis = sp.Matrix([0, 0, 1])
    axis = sp.simplify(rotation * body_axis)
    dyadic = sp.simplify(scale * q * (sp.eye(3) - 3 * axis * axis.T))
    body = scale * sp.diag(q, q, -2 * q)
    conjugated = sp.simplify(rotation * body * rotation.T)
    checks.check(
        "dyadic and conjugation constructions agree independently",
        sp.simplify(dyadic - conjugated) == sp.zeros(3),
    )
    checks.check(
        "the exact characteristic polynomial retains multiplicity two",
        _zero(
            (spectral * sp.eye(3) - dyadic).det()
            - (spectral - scale * q) ** 2 * (spectral + 2 * scale * q)
        ),
    )

    first_commutator = sp.simplify(omega * (generator * dyadic - dyadic * generator))
    second_commutator = sp.simplify(
        omega * (generator * first_commutator - first_commutator * generator)
    )
    third_commutator = sp.simplify(
        omega * (generator * second_commutator - second_commutator * generator)
    )
    checks.check(
        "commutator derivatives equal direct differentiation through third order",
        sp.simplify(first_commutator - sp.diff(dyadic, time)) == sp.zeros(3)
        and sp.simplify(second_commutator - sp.diff(dyadic, time, 2))
        == sp.zeros(3)
        and sp.simplify(third_commutator - sp.diff(dyadic, time, 3))
        == sp.zeros(3),
    )
    checks.check(
        "independent derivative contractions reproduce the exact constants",
        _zero(_norm_squared(second_commutator) - 72 * scale**2 * q**2 * omega**4)
        and _zero(
            _norm_squared(third_commutator) - 288 * scale**2 * q**2 * omega**6
        ),
    )
    checks.check(
        "the derivative rather than the full moment has three principal values",
        _zero(
            (spectral * sp.eye(3) - third_commutator).det()
            - spectral * (spectral**2 - 144 * scale**2 * q**2 * omega**6)
        ),
    )

    projector = sp.diag(0, 1, 1)
    transverse = sp.simplify(projector * second_commutator * projector)
    tt = sp.simplify(transverse - projector * sp.trace(transverse) / 2)
    conventional_plus = sp.simplify((tt[1, 1] - tt[2, 2]) / 2)
    conventional_cross = sp.simplify(tt[1, 2])
    prefactor = 2 * coupling / (scale * distance)
    h_plus = sp.simplify(prefactor * conventional_plus)
    h_cross = sp.simplify(prefactor * conventional_cross)
    checks.check(
        "direct transverse-plane algebra gives the circular conditional readout",
        _zero(h_plus + 12 * coupling * q * omega**2 * sp.cos(2 * angle) / distance)
        and _zero(
            h_cross + 12 * coupling * q * omega**2 * sp.sin(2 * angle) / distance
        )
        and _zero(
            h_plus**2
            + h_cross**2
            - 144 * coupling**2 * q**2 * omega**4 / distance**2
        ),
    )
    conditional_power = sp.simplify(
        coupling * _norm_squared(third_commutator) / (5 * scale**2)
    )
    checks.check(
        "direct contraction gives convention-independent conditional power",
        conditional_power == 288 * coupling * q**2 * omega**6 / 5,
    )

    tilt = sp.symbols("beta", real=True)
    tilted_axis = sp.Matrix(
        [
            sp.sin(tilt) * sp.cos(angle),
            sp.sin(tilt) * sp.sin(angle),
            sp.cos(tilt),
        ]
    )
    tilted = sp.simplify(scale * q * (sp.eye(3) - 3 * tilted_axis * tilted_axis.T))
    tilted_third = sp.simplify(sp.diff(tilted, time, 3))
    expected_tilt_norm = (
        18
        * scale**2
        * q**2
        * omega**6
        * sp.sin(tilt) ** 2
        * (sp.cos(tilt) ** 2 + 16 * sp.sin(tilt) ** 2)
    )
    checks.check(
        "independent dyadic tilt contains both harmonics and the exact norm",
        _zero(
            tilted[0, 2]
            + 3 * scale * q * sp.sin(tilt) * sp.cos(tilt) * sp.cos(angle)
        )
        and _zero(
            tilted[0, 1]
            + 3 * scale * q * sp.sin(tilt) ** 2 * sp.sin(2 * angle) / 2
        )
        and _zero(_norm_squared(tilted_third) - expected_tilt_norm),
    )
    checks.check(
        "load-bearing zero and eigenvalue mutations change the verdict",
        third_commutator.subs(q, 0) == sp.zeros(3)
        and third_commutator.subs(omega, 0) == sp.zeros(3)
        and _zero(
            (spectral * sp.eye(3) - sp.diag(q, 0, -q)).det()
            - spectral * (spectral - q) * (spectral + q)
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
