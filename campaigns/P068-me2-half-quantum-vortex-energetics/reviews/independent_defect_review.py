"""Independent P068 derivation without importing angular_defects."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P068-INDEPENDENT")
    radius, angle = sp.symbols("r phi", positive=True, real=True)
    stiffness, charge = sp.symbols("K q", positive=True, real=True)
    inner, outer = sp.symbols("xi R", positive=True, real=True)
    density_measure = stiffness * (charge / radius) ** 2 * radius / 2
    direct = sp.integrate(
        density_measure, (angle, 0, 2 * sp.pi), (radius, inner, outer)
    )
    target = sp.pi * stiffness * charge**2 * sp.log(outer / inner)
    ledger.check(
        "fresh polar-coordinate integration derives the annular energy",
        sp.simplify(direct - target) == 0,
    )
    circle_integral_lower = sp.simplify((2 * sp.pi * charge) ** 2 / (2 * sp.pi))
    ledger.check(
        "fresh circlewise Cauchy bound is saturated by uniform winding",
        circle_integral_lower == 2 * sp.pi * charge**2,
    )
    lower_energy = sp.integrate(
        stiffness * circle_integral_lower / (2 * radius),
        (radius, inner, outer),
    )
    ledger.check(
        "fresh fixed-degree lower bound equals the uniform annular energy",
        sp.simplify(lower_energy - target) == 0,
    )

    count = sp.symbols("n", positive=True, integer=True)
    split_scale = sp.symbols("d", positive=True, real=True)
    near = sp.pi * stiffness * charge**2 * sp.log(split_scale / inner) / count
    far = sp.pi * stiffness * charge**2 * sp.log(outer / split_scale)
    unsplit = target
    difference = sp.simplify(near + far - unsplit)
    ledger.check(
        "fresh matched-shell difference retains separation and total charge",
        sp.simplify(
            difference
            + sp.pi
            * stiffness
            * charge**2
            * (1 - 1 / count)
            * sp.log(split_scale / inner)
        )
        == 0,
    )
    concrete_ratio = sp.simplify(
        ((near + far) / unsplit).subs(
            {count: 2, inner: 1, split_scale: 4, outer: 16}
        )
    )
    ledger.check(
        "fresh common-domain half split gives three quarters not one half",
        concrete_ratio == sp.Rational(3, 4),
    )
    ledger.check(
        "fresh one-half ratio requires the far shell to vanish",
        sp.simplify(
            ((near + far) / unsplit).subs(
                {count: 2, inner: 1, split_scale: 16, outer: 16}
            )
        )
        == sp.Rational(1, 2),
    )

    def projective_class(index: int) -> int:
        return index % 2

    def full_deck(index: int) -> tuple[int, sp.Expr]:
        return ((-1) ** index, sp.pi * index)

    ledger.check(
        "fresh RP2 deck group has an order-two nontrivial element",
        projective_class(1) == 1 and projective_class(2) == 0,
    )
    ledger.check(
        "fresh full polar deck powers form an infinite integer group",
        full_deck(1) == (-1, sp.pi)
        and full_deck(2) == (1, 2 * sp.pi)
        and full_deck(3) == (-1, 3 * sp.pi),
    )
    ledger.check(
        "fresh full generator square is not the identity deck transformation",
        full_deck(2) != full_deck(0),
    )

    phase, director, logarithm = sp.symbols(
        "K_phase K_director L", positive=True, real=True
    )
    half_pair = sp.pi * (phase + director) * logarithm / 2
    integer = sp.pi * phase * logarithm
    ledger.check(
        "fresh two-stiffness field ratio is conditional",
        sp.simplify(half_pair / integer - (phase + director) / (2 * phase))
        == 0,
    )
    ledger.check(
        "fresh equal-stiffness limit is degenerate rather than one half",
        sp.simplify((half_pair - integer).subs(director, phase)) == 0,
    )
    half_core, integer_core = sp.symbols(
        "E_half E_integer", nonnegative=True, real=True
    )
    full_difference = sp.simplify(half_pair + 2 * half_core - integer - integer_core)
    ledger.check(
        "fresh preference residual retains both core energies",
        sp.simplify(
            full_difference
            - (
                sp.pi * (director - phase) * logarithm / 2
                + 2 * half_core
                - integer_core
            )
        )
        == 0,
    )
    ledger.mutation_sensitive(
        "fresh fixed-boundary oracle rejects independent-copy energy",
        lambda candidate: sp.simplify(candidate - (near + far)) == 0,
        near + far,
        [near, count * near, unsplit],
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
