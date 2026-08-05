#!/usr/bin/env python3
"""Independent raw-SymPy rederivation of the P194 phase-scale result."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
PROPOSAL = Path(__file__).resolve().parents[1]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-37/"
    "bridge_WN6_scale_verdict_and_missing_bridge.py"
)
SOURCE_SHA256 = "07f049bac9eb99cb29ef6c3cd333aaecddc17492a73a8fc2aac7eb140ebcab10"
RELEASE_SHA256 = "07040ba6cc29e6087c954cfbad108da100b2d53d05ba8982bdf0ba77435f45da"
FORMULA_FREEZE_SHA256 = "b0a94810b20487c37209f6ec621edf154c882a8caaeaf0b8b3ab7283beb29cc6"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P194-WN6-INDEPENDENT")
    checks.check("source hash is independently pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release is independently pinned",
        _digest(ROOT / "governance/releases/v0.143.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze is independently pinned",
        _digest(PROPOSAL / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )

    y, t = sp.symbols("y t", nonnegative=True)
    raw_gap = y**2 / 2 - 1 + sp.cos(y)
    raw_bound = y**4 / 24
    twice_integrated = sp.integrate(
        (y - t) * 2 * sp.sin(t / 2) ** 2,
        (t, 0, y),
    )
    four_times_integrated = sp.integrate(
        (y - t) ** 3 * 2 * sp.sin(t / 2) ** 2 / 6,
        (t, 0, y),
    )
    checks.check(
        "raw twice-integrated square reconstructs the nonnegative gap",
        sp.simplify(twice_integrated - raw_gap) == 0,
    )
    checks.check(
        "raw four-times-integrated square reconstructs bound minus gap",
        sp.simplify(four_times_integrated - (raw_bound - raw_gap)) == 0,
    )
    checks.check(
        "both independent kernels are nonnegative on zero to y",
        sp.factor(2 * sp.sin(t / 2) ** 2).is_nonnegative is True,
    )
    checks.check(
        "raw relative bound is y squared over twelve",
        sp.cancel(raw_bound / (y**2 / 2)) == y**2 / 12,
    )

    epsilon = sp.Symbol("epsilon", positive=True)
    independent_radius = sp.sqrt(12 * epsilon)
    checks.check(
        "raw tolerance radius exactly saturates the sufficient bound",
        sp.simplify(independent_radius**2 / 12 - epsilon) == 0,
    )
    for tolerance in (
        sp.Rational(1, 1000),
        sp.Rational(1, 100),
        sp.Rational(1, 10),
    ):
        radius = sp.sqrt(12 * tolerance)
        exact_ratio = sp.simplify(
            (radius**2 / 2 - (1 - sp.cos(radius))) / (radius**2 / 2)
        )
        checks.check(
            f"exact boundary error stays below raw tolerance {tolerance}",
            exact_ratio >= 0 and exact_ratio <= tolerance,
        )
    barrier_ratio = sp.simplify(
        (sp.pi**2 / 2 - 2) / (sp.pi**2 / 2)
    )
    checks.check(
        "raw barrier ratio equals one minus four over pi squared",
        barrier_ratio == 1 - 4 / sp.pi**2
        and barrier_ratio > sp.Rational(59, 100),
    )
    checks.check(
        "a ten-percent small-error domain is strictly inside the barrier",
        sp.sqrt(sp.Rational(12, 10)) < sp.pi,
    )

    P, u = sp.symbols("P u", real=True)
    raw_average = sp.integrate(P**2 * sp.cos(u) ** 2, (u, 0, 2 * sp.pi)) / (2 * sp.pi)
    checks.check("raw cycle average is peak squared over two", raw_average == P**2 / 2)
    checks.check(
        "raw RMS is absolute peak over square root two",
        sp.sqrt(raw_average) == sp.sqrt(P**2) / sp.sqrt(2),
    )
    checks.check(
        "peak pi has mean square pi squared over two not pi squared",
        raw_average.subs(P, sp.pi) == sp.pi**2 / 2,
    )

    n = sp.Symbol("n", positive=True)
    checks.check(
        "RMS convention reaches equality at square root n",
        sp.simplify((sp.sqrt(n)) ** 2 - n) == 0,
    )
    checks.check(
        "peak convention reaches equality only at square root two n",
        sp.simplify((sp.sqrt(2 * n)) ** 2 / 2 - n) == 0,
    )
    checks.check(
        "signed-amplitude counterexample breaks the unqualified iff",
        (-3) ** 2 > 4 and not (-3 > sp.sqrt(4)),
    )

    M, A = sp.symbols("M A", positive=True)
    effective = sp.sqrt(M) * A
    checks.check(
        "raw effective-amplitude substitution absorbs the mode product",
        sp.expand(effective**2 - M * A**2) == 0,
    )
    equal_product_pairs = ((1, 6), (4, 3), (9, 2), (36, 1))
    checks.check(
        "four distinct mode-amplitude pairs have the same intensity product",
        len({m * a**2 for m, a in equal_product_pairs}) == 1,
    )
    checks.check(
        "supplying mode count alone leaves the limb free through amplitude",
        10**8 * sp.Rational(1, 10) ** 2 < 10**7
        and 10**8 * 1**2 > 10**7,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    checks.check(
        "source calls A RMS but uses the pointwise barrier as its same amplitude",
        "rms phase excursion" in source_text
        and "|phi_L| <= pi" in source_text
        and "S <= pi^2" in source_text,
    )
    checks.check(
        "source supplies no averaging integral or RMS implementation",
        "integrate" not in source_text and "mean(" not in source_text,
    )
    checks.check(
        "source supplies no spatial boundary definition of winding",
        "phi(+infty)" not in source_text and "phi(-infty)" not in source_text,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
