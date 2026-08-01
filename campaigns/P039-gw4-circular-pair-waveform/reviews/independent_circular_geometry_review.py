#!/usr/bin/env python3
"""Independent particle, viewing-geometry, and refinement review for P039."""

from __future__ import annotations

import numpy as np
import sympy as sp

from substrate_framework.verification import CheckLedger


def frobenius(tensor: sp.Matrix) -> sp.Expr:
    return sp.simplify(sum(tensor[i, j] ** 2 for i in range(3) for j in range(3)))


def numeric_third_error(points: int, frequency: float) -> float:
    """Repeated centered differences for one exact normalized-STF component."""

    times = np.linspace(0.0, 4 * np.pi / frequency, points)
    step = times[1] - times[0]
    values = np.cos(2 * frequency * times)
    derivative = values
    for _ in range(3):
        next_derivative = np.full_like(derivative, np.nan)
        next_derivative[1:-1] = (
            derivative[2:] - derivative[:-2]
        ) / (2 * step)
        derivative = next_derivative
    interior = slice(8, -8)
    exact = (2 * frequency) ** 3 * np.sin(2 * frequency * times[interior])
    return float(np.max(np.abs(derivative[interior] - exact)))


def main() -> int:
    ledger = CheckLedger("P039-INDEPENDENT")
    time, mass, radius, frequency = sp.symbols(
        "t m a Omega", positive=True, real=True
    )
    relative = sp.Matrix(
        [radius * sp.cos(frequency * time), radius * sp.sin(frequency * time), 0]
    )
    second_moment = sp.simplify(2 * mass * relative * relative.T)
    normalized = sp.simplify(
        second_moment - sp.eye(3) * sp.trace(second_moment) / 3
    )
    second = sp.simplify(normalized.diff(time, 2))
    third = sp.simplify(normalized.diff(time, 3))
    ledger.check(
        "direct particle dyads independently give the normalized STF moment",
        sp.trigsimp(sp.trace(normalized)) == 0
        and sp.simplify(normalized - normalized.T) == sp.zeros(3),
    )
    ledger.check(
        "direct differentiation independently gives the 32 and 128 norms",
        sp.trigsimp(frobenius(second) - 32 * mass**2 * radius**4 * frequency**4)
        == 0
        and sp.trigsimp(
            frobenius(third) - 128 * mass**2 * radius**4 * frequency**6
        )
        == 0,
    )
    reduced_mass = mass / 2
    separation = 2 * radius
    ledger.check(
        "the orbital-radius factor agrees with reduced-mass separation notation",
        sp.simplify(
            32 * reduced_mass**2 * separation**4
            - 128 * mass**2 * radius**4
        )
        == 0,
    )

    inclination = sp.symbols("i", real=True)
    line_of_sight = sp.Matrix([sp.sin(inclination), 0, sp.cos(inclination)])
    first = sp.Matrix([sp.cos(inclination), 0, -sp.sin(inclination)])
    second_axis = sp.Matrix([0, 1, 0])
    plus = (first * first.T - second_axis * second_axis.T) / sp.sqrt(2)
    cross = (first * second_axis.T + second_axis * first.T) / sp.sqrt(2)
    plus_coordinate = sp.trigsimp(
        sum(plus[i, j] * second[i, j] for i in range(3) for j in range(3))
    )
    cross_coordinate = sp.trigsimp(
        sum(cross[i, j] * second[i, j] for i in range(3) for j in range(3))
    )
    phase = 2 * frequency * time
    ledger.check(
        "independent viewing-frame contraction gives the arbitrary-inclination plus factor",
        sp.trigsimp(
            plus_coordinate
            + 2
            * sp.sqrt(2)
            * mass
            * radius**2
            * frequency**2
            * (1 + sp.cos(inclination) ** 2)
            * sp.cos(phase)
        )
        == 0,
    )
    ledger.check(
        "independent viewing-frame contraction gives the arbitrary-inclination cross factor",
        sp.trigsimp(
            cross_coordinate
            + 4
            * sp.sqrt(2)
            * mass
            * radius**2
            * frequency**2
            * sp.cos(inclination)
            * sp.sin(phase)
        )
        == 0,
    )
    ledger.check(
        "the chosen viewing frame is exactly transverse and oriented",
        line_of_sight.dot(first) == 0
        and line_of_sight.dot(second_axis) == 0
        and sp.simplify(first.cross(second_axis) - line_of_sight)
        == sp.zeros(3, 1),
    )

    errors = [numeric_third_error(points, 0.37) for points in (1000, 2000, 4000)]
    ledger.check(
        "independent finite differences converge under two refinements",
        errors[1] < errors[0]
        and errors[2] < errors[1]
        and errors[0] / errors[1] > 3.8
        and errors[1] / errors[2] > 3.8,
    )
    ledger.check(
        "triple quadrupole with an unscaled waveform coefficient is a factor-three field error",
        sp.simplify(2 * normalized - sp.Rational(2, 3) * (3 * normalized))
        == sp.zeros(3)
        and sp.simplify(2 * (3 * normalized) - 3 * (2 * normalized))
        == sp.zeros(3),
    )
    ledger.check(
        "the declared orbit needs acceleration and therefore an unmodeled force or stress",
        sp.simplify(relative.diff(time, 2)) != sp.zeros(3, 1),
    )
    count = ledger.finish()
    print(f"P039 INDEPENDENT CIRCULAR-GEOMETRY REVIEW ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
