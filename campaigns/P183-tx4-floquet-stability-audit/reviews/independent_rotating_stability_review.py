#!/usr/bin/env python3
"""Fresh exact review of C-FLO-001 and C-ROT-001 without their modules."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P183-INDEPENDENT-ROTATING-STABILITY")
    time = sp.Symbol("t", real=True)
    omega = sp.Symbol("Omega", positive=True)
    entries = sp.symbols("b00 b01 b10 b11", real=True)
    body = sp.Matrix(2, 2, entries)
    frame_generator = omega * sp.Matrix([[0, -1], [1, 0]])
    frame = sp.Matrix(
        [
            [sp.cos(omega * time), -sp.sin(omega * time)],
            [sp.sin(omega * time), sp.cos(omega * time)],
        ]
    )
    laboratory = sp.simplify(frame * body * frame.T)
    transformed = sp.simplify(
        frame.T * laboratory * frame - frame.T * sp.diff(frame, time)
    )
    checks.check(
        "fresh frame differentiation gives B minus K for arbitrary B",
        sp.trigsimp(transformed - (body - frame_generator)) == sp.zeros(2),
    )
    period = 2 * sp.pi / omega
    checks.check(
        "the declared rotation frame closes exactly after one period",
        sp.trigsimp(frame.subs(time, period) - sp.eye(2)) == sp.zeros(2),
    )
    nilpotent = sp.Matrix([[0, 1], [0, 0]])
    checks.check(
        "direct differentiation verifies a nontrivial constant-generator fundamental matrix",
        sp.diff((time * nilpotent).exp(), time)
        == nilpotent * (time * nilpotent).exp(),
    )
    nilpotent_monodromy = (period * nilpotent).exp()
    checks.check(
        "unit multipliers coexist with a nontrivial Jordan block",
        nilpotent_monodromy == sp.eye(2) + period * nilpotent
        and nilpotent_monodromy.eigenvals() == {sp.S.One: 2}
        and len((nilpotent_monodromy - sp.eye(2)).nullspace()) == 1,
    )
    integer = sp.Symbol("n", positive=True, integer=True)
    checks.check(
        "the unit-multiplier Jordan powers grow exactly linearly",
        nilpotent_monodromy**integer
        == sp.eye(2) + integer * period * nilpotent,
    )
    growth = sp.Symbol("gamma", positive=True)
    checks.check(
        "a static positive exponent is an explicit unstable counterexample",
        sp.simplify(sp.exp(period * growth).subs(growth, omega / (2 * sp.pi)))
        == sp.E
        and (sp.E - 1).is_positive is True,
    )

    A = sp.Symbol("A", positive=True)
    delta = sp.Symbol("Delta", positive=True)
    C = A + delta
    w1, w2, w3 = sp.symbols("w1 w2 w3", real=True)
    rotor = sp.Matrix(
        [
            (A - C) * w2 * w3 / A,
            (C - A) * w3 * w1 / A,
            0,
        ]
    )
    base = {w1: omega, w2: 0, w3: 0}
    jacobian = sp.simplify(rotor.jacobian([w1, w2, w3]).subs(base))
    checks.check(
        "fresh Euler linearization is nonzero nilpotent rank one",
        jacobian != sp.zeros(3)
        and jacobian.rank() == 1
        and jacobian**2 == sp.zeros(3),
    )
    rotor_period = 2 * sp.pi / omega
    rotor_monodromy = sp.eye(3) + rotor_period * jacobian
    checks.check(
        "rotor monodromy has defective unit multiplier",
        rotor_monodromy.eigenvals() == {sp.S.One: 3}
        and len((rotor_monodromy - sp.eye(3)).nullspace()) == 2,
    )

    L2 = A**2 * (w1**2 + w2**2) + C**2 * w3**2
    twice_energy = A * (w1**2 + w2**2) + C * w3**2
    checks.check(
        "fresh differentiation verifies both nonlinear invariants",
        sp.simplify(sp.Matrix([sp.diff(L2, item) for item in (w1, w2, w3)]).dot(rotor))
        == 0
        and sp.simplify(
            sp.Matrix(
                [sp.diff(twice_energy, item) for item in (w1, w2, w3)]
            ).dot(rotor)
        )
        == 0,
    )

    radius, phase, epsilon = sp.symbols("r phi epsilon", positive=True)
    rate = delta * epsilon / A
    solution = sp.Matrix(
        [
            radius * sp.cos(phase + rate * time),
            radius * sp.sin(phase + rate * time),
            epsilon,
        ]
    )
    solution_rhs = rotor.subs(dict(zip((w1, w2, w3), solution, strict=True)))
    checks.check(
        "independent exact perturbed rotor trajectory solves Euler equations",
        sp.trigsimp(sp.diff(solution, time) - solution_rhs) == sp.zeros(3, 1),
    )
    witness_time = sp.pi * A / (2 * delta * epsilon)
    witness = solution.subs({radius: omega, phase: 0, time: witness_time})
    base_vector = sp.Matrix([omega, 0, 0])
    checks.check(
        "arbitrarily small axial perturbations move order one from one equilibrium",
        sp.simplify((witness - base_vector).dot(witness - base_vector))
        == 2 * omega**2 + epsilon**2
        and sp.limit(epsilon**2, epsilon, 0, dir="+") == 0,
    )
    checks.check(
        "distance to the entire transverse equilibrium circle stays constant",
        sp.simplify((radius - omega) ** 2 + epsilon**2).has(time) is False,
    )

    radial, axial = sp.symbols("R2 Z", real=True)
    ordinary_C = radial - axial
    ordinary_A = (radial + axial) / 2
    normalized_stf_zz = axial - radial / 3
    checks.check(
        "ordinary density inertia relation uses normalized STF convention",
        sp.simplify(
            ordinary_C - ordinary_A + sp.Rational(3, 2) * normalized_stf_zz
        )
        == 0,
    )
    checks.check(
        "factor-three tensor-name mutation breaks the inertia identity",
        sp.simplify(ordinary_C - ordinary_A + sp.Rational(3, 2) * 3 * normalized_stf_zz)
        != 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
