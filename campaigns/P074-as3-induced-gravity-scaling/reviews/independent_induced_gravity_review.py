"""Independent exact P074 rederivation without canonical induced-gravity imports."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-21/"
    "bridge_AS3_sakharov_kappa_reduce.py"
)
SOURCE_SHA256 = "f88cc85a3fb64d1b8aabdf53ced29168d78fce9470e586dc19564288a120903b"


def main() -> int:
    checks = CheckLedger("P074-INDEPENDENT")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    checks.check(
        "independent route reads immutable AS3",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )

    matrix = sp.Matrix([[0, 0, 1], [1, 1, 2], [0, -1, -1]])
    dim_g = sp.Matrix([-1, 3, -2])
    dim_inverse_g = -dim_g
    g_solution = matrix.inv() * dim_g
    inverse_solution = matrix.inv() * dim_inverse_g
    checks.check("fresh primitive matrix is full rank", matrix.rank() == 3)
    checks.check("fresh G powers", g_solution == sp.Matrix([2, 3, -1]))
    checks.check(
        "fresh inverse G powers",
        inverse_solution == sp.Matrix([-2, -3, 1]),
    )
    checks.check(
        "fresh wrong powers fail",
        matrix * sp.Matrix([-1, -3, 1]) != dim_inverse_g
        and matrix * sp.Matrix([-4, -3, 1]) != dim_inverse_g,
    )
    checks.check(
        "fresh G over length squared retains dimensions",
        dim_g - sp.Matrix([0, 2, 0]) == sp.Matrix([-1, 1, -2]),
    )

    a, s, c, hbar, baseline = sp.symbols(
        "a s c hbar baseline", positive=True
    )
    energy_cutoff = hbar * c / a
    shift = s * hbar / (a**2 * c**3)
    energy_shift = s * energy_cutoff**2 / (hbar * c**5)
    pure_g = sp.simplify(1 / shift)
    total_inverse = baseline + shift
    checks.check("fresh cutoff map", energy_cutoff == hbar * c / a)
    checks.check("fresh cutoff and length forms", sp.simplify(shift - energy_shift) == 0)
    checks.check("fresh pure reciprocal", pure_g == a**2 * c**3 / (hbar * s))
    checks.check(
        "fresh coefficient sensitivity",
        sp.diff(pure_g, s) != 0 and sp.diff(shift, s) != 0,
    )
    checks.check(
        "fresh sign counterexample",
        sp.simplify(shift.subs(s, -s) + shift) == 0,
    )
    checks.check(
        "fresh baseline limit",
        sp.limit(total_inverse, a, sp.oo) == baseline,
    )
    target = sp.symbols("target", positive=True)
    checks.check(
        "fresh arbitrary-total counterfamily",
        sp.simplify((target - shift) + shift - target) == 0,
    )
    checks.check(
        "fresh cancellation counterfamily",
        sp.simplify((-shift) + shift) == 0,
    )

    design = sp.Matrix([[2, -1]])
    nullspace = design.nullspace()
    checks.check("fresh log row rank", design.rank() == 1)
    checks.check(
        "fresh log null direction",
        len(nullspace) == 1
        and design * nullspace[0] == sp.zeros(1, 1)
        and 2 * nullspace[0] == sp.Matrix([1, 2]),
    )
    checks.check(
        "fresh rescaling invariance",
        sp.simplify(
            pure_g.subs({a: sp.Symbol("rho", positive=True) * a, s: sp.Symbol("rho", positive=True) ** 2 * s})
            - pure_g
        )
        == 0,
    )
    first_covector = sp.Matrix([[1, 0]])
    second_covector = sp.Matrix([[0, 1]])
    checks.check(
        "fresh rowspace identifies neither coordinate",
        design.col_join(first_covector).rank() > design.rank()
        and design.col_join(second_covector).rank() > design.rank(),
    )

    operator = sp.Matrix([0, -2, 0])
    mass_density = sp.Matrix([1, -3, 0])
    energy_density = sp.Matrix([1, -1, -2])
    mass_coupling = operator - mass_density
    energy_coupling = operator - energy_density
    checks.check(
        "fresh mass-density normalization",
        mass_coupling - dim_g == sp.Matrix([0, -2, 2]),
    )
    checks.check(
        "fresh energy-density normalization",
        energy_coupling - dim_g == sp.Matrix([0, -4, 4]),
    )
    compatible_source = operator - dim_g
    checks.check(
        "fresh matching-source normalization",
        operator - compatible_source == dim_g,
    )

    checks.check(
        "fresh source audit sees imported induced premise",
        "IMPORTED (cited, FORM not magnitude" in source_text,
    )
    checks.check(
        "fresh source audit sees free coefficient in inverse",
        "sqrt(s_G hbar G_eff/c0^3)" in source_text,
    )
    checks.check(
        "fresh source audit sees pending coupling map",
        "kappa = 8 * sp.pi * G_eff" in source_text,
    )
    checks.check(
        "fresh source audit sees no baseline",
        "G_0" not in source_text and "baseline" not in source_text,
    )
    checks.check(
        "fresh source audit sees insensitive branch filter",
        "if s.is_positive or True" in source_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
