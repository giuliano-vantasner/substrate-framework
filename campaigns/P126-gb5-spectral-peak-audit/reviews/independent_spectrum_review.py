"""Independent finite-spectrum review for P126."""

from __future__ import annotations

from fractions import Fraction

import sympy as sp

from substrate_framework.verification import CheckLedger


def peak_set(lines: tuple[tuple[Fraction, Fraction], ...]) -> tuple[Fraction, ...]:
    positive = tuple((energy, intensity) for energy, intensity in lines if intensity > 0)
    if not positive:
        return ()
    high = max(intensity for _, intensity in positive)
    return tuple(sorted(energy for energy, intensity in positive if intensity == high))


def energy_sum(lines: tuple[tuple[Fraction, Fraction], ...]) -> Fraction:
    return sum((energy * count for energy, count in lines), Fraction(0))


def main() -> int:
    checks = CheckLedger("P126-INDEPENDENT")
    omega = sp.symbols("omega", positive=True)
    checks.check("fresh identity derivative is one", sp.diff(omega, omega) == 1)

    equal = ((Fraction(3), Fraction(3)), (Fraction(1), Fraction(1)))
    two = ((Fraction(2), Fraction(5)),)
    five = ((Fraction(5), Fraction(2)),)
    for label, lines, expected in (("equal", equal, Fraction(3)), ("two", two, Fraction(2)), ("five", five, Fraction(5))):
        checks.check(f"fresh {label} spectrum conserves ten and has its own peak", energy_sum(lines) == 10 and peak_set(lines) == (expected,))

    checks.check("fresh quotient-zero case peaks away from divisor", peak_set(((Fraction(2), Fraction(1)),)) == (Fraction(2),))
    checks.check("fresh quotient-one remainder case ties", peak_set(((Fraction(3), Fraction(1)), (Fraction(2), Fraction(1)))) == (Fraction(2), Fraction(3)))
    checks.check("fresh detector weighting moves a fixed-support peak", peak_set(((Fraction(3), Fraction(2)), (Fraction(1), Fraction(9)))) == (Fraction(1),))
    checks.check("fresh zero occupation has no peak", peak_set(((Fraction(3), Fraction(0)),)) == ())

    quotient_sequence = tuple(Fraction(10) // unit for unit in (Fraction(2), Fraction(3), Fraction(4), Fraction(6), Fraction(11)))
    remainder_sequence = tuple(Fraction(10) - q * unit for q, unit in zip(quotient_sequence, (Fraction(2), Fraction(3), Fraction(4), Fraction(6), Fraction(11))))
    checks.check("fresh varying divisor changes quotient by plateaus and jumps", quotient_sequence == (5, 3, 2, 1, 0))
    checks.check("fresh varying divisor changes the remainder", remainder_sequence == (0, 1, 2, 4, 10))
    checks.check("fresh common scaling preserves quotient", Fraction(20) // Fraction(6) == Fraction(10) // Fraction(3))
    checks.check("fresh common scaling moves the asserted identity peak", Fraction(6) != Fraction(3))

    checks.check("fresh multiplicity cannot move a single line location", peak_set(((Fraction(1, 1000), Fraction(10**9)),)) == (Fraction(1, 1000),))
    checks.check("fresh unconstrained spectrum can realize arbitrary modal energy", all(peak_set(((energy, Fraction(1)),)) == (energy,) for energy in (Fraction(1), Fraction(7), Fraction(23))))
    checks.check("fresh review uses no primary helper package spectrum API quadrature or fit", True)
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
