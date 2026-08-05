#!/usr/bin/env python3
"""Independent raw-SymPy review of the P196 continuum DOS theorem."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
PROPOSAL = Path(__file__).resolve().parents[1]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-38/"
    "bridge_MD1_mode_count_is_a_counting_theorem.py"
)
SOURCE_SHA256 = "e7408667dbb6644e4c88a0a1523b6eb5f9058c628b5650ff0bf72cfa3238e5ba"
RELEASE_SHA256 = "b995916d6e708d29f0f493562741d7ba35bc202ce2784f4aaed7d1dfd5232a0a"
FORMULA_FREEZE_SHA256 = "de520bd631c3e244b2e538a92dbc65f92e26301a4d927b7b8b48280423b94540"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def raw_surface(dimension: int) -> sp.Expr:
    return sp.simplify(
        2
        * sp.pi ** sp.Rational(dimension, 2)
        / sp.gamma(sp.Rational(dimension, 2))
    )


def main() -> int:
    checks = CheckLedger("P196-MD1-INDEPENDENT")
    checks.check("MD1 bytes are independently pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release is independently pinned",
        digest(ROOT / "governance/releases/v0.144.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze is independently pinned",
        digest(PROPOSAL / "evidence/formula-freeze.yaml") == FORMULA_FREEZE_SHA256,
    )

    omega, omega_0, k, c, V, K, a = sp.symbols(
        "omega omega_0 k c V K a", positive=True
    )
    inverse = sp.sqrt(omega**2 - omega_0**2) / c
    derivative = sp.diff(inverse, omega)
    checks.check(
        "raw inverse substitution reconstructs the dispersion",
        sp.simplify(omega_0**2 + c**2 * inverse**2 - omega**2) == 0,
    )
    checks.check(
        "raw Jacobian has the inverse square-root threshold factor",
        sp.simplify(
            derivative - omega / (c * sp.sqrt(omega**2 - omega_0**2))
        )
        == 0,
    )
    checks.check(
        "raw unit-sphere sequence begins two two-pi four-pi",
        tuple(raw_surface(dimension) for dimension in (1, 2, 3))
        == (2, 2 * sp.pi, 4 * sp.pi),
    )

    raw_densities: dict[int, sp.Expr] = {}
    for dimension in (1, 2, 3, 4):
        raw = sp.simplify(
            V
            * raw_surface(dimension)
            * inverse ** (dimension - 1)
            * derivative
            / (2 * sp.pi) ** dimension
        )
        closed = sp.simplify(
            V
            * raw_surface(dimension)
            * omega
            * (omega**2 - omega_0**2) ** sp.Rational(dimension - 2, 2)
            / ((2 * sp.pi) ** dimension * c**dimension)
        )
        raw_densities[dimension] = raw
        checks.check(
            f"raw shell change of variables gives the d={dimension} closed form",
            sp.simplify(raw - closed) == 0,
        )

    checks.check(
        "raw d1 threshold divergence is integrable but has no finite edge value",
        sp.limit(raw_densities[1], omega, omega_0, dir="+") == sp.oo,
    )
    checks.check(
        "raw d2 edge is finite and raw d3 edge vanishes",
        sp.limit(raw_densities[2], omega, omega_0, dir="+")
        == V * omega_0 / (2 * sp.pi * c**2)
        and sp.limit(raw_densities[3], omega, omega_0, dir="+") == 0,
    )

    upper = sp.sqrt(omega_0**2 + c**2 * K**2)
    for dimension in (1, 2, 3, 4):
        integrated = sp.simplify(
            sp.integrate(raw_densities[dimension], (omega, omega_0, upper))
        )
        raw_ball = sp.simplify(
            V
            * raw_surface(dimension)
            * K**dimension
            / (dimension * (2 * sp.pi) ** dimension)
        )
        checks.check(
            f"raw d={dimension} integral equals the supplied-measure ball volume",
            sp.simplify(integrated - raw_ball) == 0,
        )
        checks.check(
            f"raw d={dimension} integral loses gap dependence at fixed K",
            sp.simplify(sp.diff(integrated, omega_0)) == 0,
        )

    per_branch_d3 = V * K**3 / (6 * sp.pi**2)
    raw_cutoff = (6 * sp.pi**2) ** sp.Rational(1, 3) / a
    checks.check(
        "raw MD1 cutoff solves a supplied per-branch target",
        sp.simplify(per_branch_d3.subs(K, raw_cutoff) - V / a**3) == 0,
    )
    checks.check(
        "raw three-branch result multiplies rather than derives degeneracy",
        sp.simplify(3 * per_branch_d3.subs(K, raw_cutoff) - 3 * V / a**3) == 0,
    )
    checks.check(
        "same d3 geometry admits independent one and three component ranks",
        7 * 1 == 7 and 7 * 3 == 21 and 7 != 21,
    )

    exact_periodic_points = tuple(index for index in range(-1, 2) if abs(index) <= 1)
    continuum_points = sp.simplify(
        2 * sp.pi * raw_surface(1) * 1 / (1 * (2 * sp.pi))
    )
    checks.check(
        "raw finite periodic counterexample separates lattice rank from phase volume",
        len(exact_periodic_points) == 3 and continuum_points == 2,
    )
    checks.check(
        "boundary convention changes exact discrete count at fixed continuum inputs",
        len(tuple(index for index in range(-1, 2) if abs(index) < 1)) == 1
        and len(exact_periodic_points) == 3,
    )
    checks.check(
        "total rank leaves active coupling support undetermined",
        len((0, 0, 1, 0)) == len((1, 1, 1, 1)) == 4
        and sum(value != 0 for value in (0, 0, 1, 0)) == 1
        and sum(value != 0 for value in (1, 1, 1, 1)) == 4,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    checks.check(
        "source supplies no discrete wavevector boundary or branch derivation",
        "periodic" not in source_text
        and "polarization" not in source_text
        and "M_count = 3*N_cells" in source_text,
    )
    checks.check(
        "source equates total counting with participation without interaction data",
        "participating-mode count" in source_text
        and "interaction" not in source_text
        and "coupling" not in source_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
