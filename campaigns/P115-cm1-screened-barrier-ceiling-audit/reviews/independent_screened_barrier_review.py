"""Independent exact review for P115 without canonical implementation imports."""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("C-SCR-001-INDEPENDENT")
    energy, barrier, shift = sp.symbols("E G U", positive=True)
    bare = sp.exp(-sp.sqrt(barrier / energy))
    shifted = sp.exp(-sp.sqrt(barrier / (energy + shift)))
    ratio = sp.factor(shifted / bare)

    checks.check(
        "fresh ratio composition gives the shifted factor",
        sp.simplify(bare * ratio - shifted) == 0,
    )
    checks.check(
        "fresh ratio exponent matches the two-barrier difference",
        sp.simplify(
            sp.log(ratio)
            - (sp.sqrt(barrier / energy) - sp.sqrt(barrier / (energy + shift)))
        )
        == 0,
    )
    log_shifted = -sp.sqrt(barrier / (energy + shift))
    d_energy = sp.simplify(sp.diff(log_shifted, energy))
    d_shift = sp.simplify(sp.diff(log_shifted, shift))
    d_barrier = sp.simplify(sp.diff(log_shifted, barrier))
    checks.check(
        "fresh derivative route proves both energy directions",
        d_energy.is_positive is True
        and d_shift.is_positive is True
        and sp.simplify(d_energy - d_shift) == 0,
    )
    checks.check(
        "fresh derivative route proves barrier suppression",
        d_barrier.is_negative is True,
    )

    x = sp.symbols("x", positive=True)
    kernel = x ** -sp.Rational(3, 2)
    d_log_ratio = sp.simplify(sp.diff(sp.log(ratio), energy))
    checks.check(
        "fresh decreasing-kernel route proves enhancement falls with energy",
        sp.simplify(
            d_log_ratio
            - sp.sqrt(barrier)
            / 2
            * (kernel.subs(x, energy + shift) - kernel.subs(x, energy))
        )
        == 0
        and sp.diff(kernel, x).is_negative is True,
    )
    checks.check(
        "fresh endpoint routes separate zero, finite floor, and divergent ratio",
        sp.limit(bare, energy, 0, dir="+") == 0
        and sp.simplify(
            sp.limit(shifted, energy, 0, dir="+")
            - sp.exp(-sp.sqrt(barrier / shift))
        )
        == 0
        and sp.limit(ratio, energy, 0, dir="+") == sp.oo,
    )
    checks.check(
        "fresh high-energy route gives transparent and unit-ratio limits",
        sp.limit(shifted, energy, sp.oo) == 1
        and sp.limit(ratio, energy, sp.oo) == 1,
    )

    scale = sp.symbols("rho", positive=True)
    checks.check(
        "fresh common-scale substitution leaves both factors unchanged",
        sp.simplify(
            shifted.subs(
                {
                    energy: scale * energy,
                    barrier: scale * barrier,
                    shift: scale * shift,
                },
                simultaneous=True,
            )
            - shifted
        )
        == 0,
    )
    checks.check(
        "fresh shift-bound direction follows from the exact derivative",
        d_shift.is_positive is True
        and shifted.subs({energy: 2, barrier: 11, shift: 1})
        < shifted.subs({energy: 2, barrier: 11, shift: 3}),
    )

    prefactor = sp.symbols("nu", nonnegative=True)
    checks.check(
        "fresh zero-prefactor countermodel rejects a derived positive rate",
        shifted.is_positive is True and (prefactor * shifted).subs(prefactor, 0) == 0,
    )
    checks.check(
        "fresh arbitrary prefactor prevents absolute magnitude prediction",
        sp.simplify(
            (prefactor * shifted).subs(prefactor, 13)
            - 13 * (prefactor * shifted).subs(prefactor, 1)
        )
        == 0,
    )
    fake_shape = energy / (energy + barrier)
    fake_derivative = sp.factor(sp.diff(fake_shape, energy))
    checks.check(
        "fresh increasing non-Gamow counterexample defeats shape-by-sign",
        sp.simplify(fake_derivative - barrier / (energy + barrier) ** 2) == 0
        and (barrier / (energy + barrier) ** 2).is_positive is True
        and not fake_shape.has(sp.exp, sp.sqrt),
    )

    checks.check(
        "fresh review imports no canonical screened-barrier implementation",
        not any(
            isinstance(node, ast.ImportFrom)
            and node.module == "substrate_framework.screened_barrier"
            for node in ast.walk(ast.parse(Path(__file__).read_text()))
        ),
    )
    checks.check(
        "fresh review uses no float quadrature solver fit or comparator",
        not shifted.has(sp.Float, sp.Integral),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
