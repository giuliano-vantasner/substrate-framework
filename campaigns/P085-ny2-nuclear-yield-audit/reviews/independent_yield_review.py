"""Independent exact P085 review without importing canonical Skyrme APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P085-INDEPENDENT")
    scale, coefficient, target = sp.symbols("U kappa Q", positive=True)
    family = coefficient * scale
    inverse = sp.solve(sp.Eq(family, target), coefficient)[0]
    checks.check(
        "fresh same-unit algebra retains a free dimensionless coefficient",
        inverse == target / scale and coefficient in family.free_symbols,
    )
    checks.check(
        "fresh inverse realizes every positive target",
        sp.simplify(family.subs(coefficient, inverse) - target) == 0,
    )
    checks.check(
        "fresh coefficient-one choice is neither unique nor stationary",
        family.subs(coefficient, 1) == scale
        and family.subs(coefficient, sp.Rational(9, 10)) != scale
        and sp.diff(family, coefficient).subs(coefficient, 1) == scale,
    )

    electron_mev = sp.Rational(10219979, 20000000)
    unit = sp.simplify(16 * sp.pi * electron_mev)
    empirical = sp.Rational(1193, 50)
    old_engine = sp.Integer(24)
    k_empirical = sp.factor(empirical / unit)
    k_engine = sp.factor(old_engine / unit)
    checks.check(
        "fresh comparator inversion gives distinct nonunit coefficients",
        k_empirical == sp.Rational(29825000, 10219979) / sp.pi
        and k_engine == sp.Rational(30000000, 10219979) / sp.pi
        and len({k_empirical, k_engine, sp.Integer(1)}) == 3,
    )
    checks.check(
        "fresh broad-band counterexample admits incompatible yields",
        sp.Rational(17, 20) <= sp.Rational(9, 10) <= sp.Rational(23, 20)
        and sp.Rational(17, 20) <= sp.Rational(11, 10) <= sp.Rational(23, 20)
        and sp.Rational(9, 10) * unit != sp.Rational(11, 10) * unit,
    )

    mass_two, mass_four = sp.symbols("a_2 a_4", real=True)
    binding = sp.factor((2 * mass_two * unit - mass_four * unit) / unit)
    checks.check(
        "fresh multi-soliton factorization leaves two free mass coefficients",
        binding == 2 * mass_two - mass_four
        and binding.free_symbols == {mass_two, mass_four},
    )
    checks.check(
        "fresh binding countermodels span both signs and zero",
        {
            binding.subs({mass_two: 2, mass_four: 3}),
            binding.subs({mass_two: 2, mass_four: 4}),
            binding.subs({mass_two: 2, mass_four: 5}),
        }
        == {-1, 0, 1},
    )
    arbitrary = sp.Symbol("b", positive=True)
    checks.check(
        "fresh exothermic family still realizes every positive binding factor",
        sp.simplify(
            binding.subs({mass_two: (arbitrary + 2) / 2, mass_four: 2})
            - arbitrary
        )
        == 0,
    )

    total, release = sp.symbols("W Delta", positive=True)
    product = total - release
    photon = sp.factor((total**2 - product**2) / (2 * total))
    checks.check(
        "fresh CM kinematics requires another final carrier for positive release",
        total - product == release and release != 0,
    )
    checks.check(
        "fresh radiative kinematics partitions photon and recoil energies",
        sp.simplify(photon - (release - release**2 / (2 * total))) == 0
        and sp.simplify(release - photon) == release**2 / (2 * total),
    )
    checks.check(
        "fresh derivation uses neither numerical solver nor quadrature",
        not any(expression.has(sp.Integral) for expression in (inverse, binding, photon)),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
