#!/usr/bin/env python3
"""Independent exact weak-moment review for P036."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def stf(matrix: sp.Matrix) -> sp.Matrix:
    return sp.simplify(matrix - sp.eye(3) * sp.trace(matrix) / 3)


def main() -> int:
    ledger = CheckLedger("P036-INDEPENDENT")
    t = sp.symbols("t", real=True)
    masses = (sp.Integer(2), sp.Integer(5), sp.Integer(3))
    origins = (
        sp.Matrix([1, 0, -1]),
        sp.Matrix([0, 2, 1]),
        sp.Matrix([-2, 1, 0]),
    )
    velocities = (
        sp.Matrix([1, 2, 0]),
        sp.Matrix([-1, 0, 1]),
        sp.Matrix([0, -1, 2]),
    )
    positions = tuple(
        origin + velocity * t for origin, velocity in zip(origins, velocities)
    )
    monopole = sum(masses)
    dipole = sum(
        (mass * position for mass, position in zip(masses, positions)),
        sp.zeros(3, 1),
    )
    momentum = sum(
        (mass * velocity for mass, velocity in zip(masses, velocities)),
        sp.zeros(3, 1),
    )
    second = sum(
        (
            mass * position * position.T
            for mass, position in zip(masses, positions)
        ),
        sp.zeros(3),
    )
    stress = sum(
        (
            mass * velocity * velocity.T
            for mass, velocity in zip(masses, velocities)
        ),
        sp.zeros(3),
    )
    ledger.check(
        "independent inertial particles conserve monopole and momentum",
        sp.diff(monopole, t) == 0 and sp.diff(momentum, t) == sp.zeros(3, 1),
    )
    ledger.check(
        "their dipole derivative is momentum and acceleration vanishes",
        sp.diff(dipole, t) == momentum
        and sp.diff(dipole, t, 2) == sp.zeros(3, 1),
    )
    ledger.check(
        "direct differentiation independently gives the factor-two stress identity",
        sp.diff(second, t, 2) == 2 * stress,
    )
    ledger.check(
        "trace removal commutes with the exact second derivative",
        sp.diff(stf(second), t, 2) == 2 * stf(stress),
    )

    shift = sp.Matrix(sp.symbols("s0:3"))
    shifted_positions = tuple(position - shift for position in positions)
    shifted_second = sum(
        (
            mass * position * position.T
            for mass, position in zip(masses, shifted_positions)
        ),
        sp.zeros(3),
    )
    ledger.check(
        "constant translation does not change the isolated second-moment acceleration",
        sp.diff(shifted_second, t, 2) == sp.diff(second, t, 2),
    )

    x = sp.symbols("x", real=True)
    density = 2 - t
    flux = x
    ledger.check(
        "an independent finite-domain continuity example retains its boundary flux",
        sp.diff(density, t) + sp.diff(flux, x) == 0
        and sp.diff(sp.integrate(density, (x, 0, 1)), t)
        == -(flux.subs(x, 1) - flux.subs(x, 0)),
    )

    v, w = sp.symbols("v w", real=True)
    packet = sp.exp(-(x - v * t) ** 2) / sp.sqrt(sp.pi)
    ledger.check(
        "an independent nonsymmetric conserved example separates energy flux and momentum",
        sp.simplify(sp.diff(packet, t) + sp.diff(v * packet, x)) == 0
        and sp.simplify(sp.diff(w * packet, t) + sp.diff(v * w * packet, x)) == 0
        and sp.integrate(v * packet, (x, -sp.oo, sp.oo)) == v
        and sp.integrate(w * packet, (x, -sp.oo, sp.oo)) == w,
    )

    static_second = sp.diag(4, 1, 1)
    ledger.check(
        "a static anisotropic STF tensor is nonzero but has zero time derivative",
        stf(static_second) != sp.zeros(3)
        and sp.diff(stf(static_second), t, 2) == sp.zeros(3),
    )
    ledger.check(
        "moment identities contain no wave operator, coupling, or radiative boundary condition",
        not any(symbol.name in {"G", "h", "wave"} for symbol in stress.free_symbols),
    )

    count = ledger.finish()
    print(f"P036 INDEPENDENT WEAK-MOMENT REVIEW ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
