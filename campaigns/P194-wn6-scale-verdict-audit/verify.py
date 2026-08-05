#!/usr/bin/env python3
"""Primary exact verifier for the P194 WN6 phase-scale theorem."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.cosine_vertices import (
    cosine_quadratic_gap,
    cosine_quadratic_gap_bound,
    harmonic_cycle_mean_square,
    harmonic_rms_from_peak,
    sufficient_cosine_quadratic_domain,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
PROPOSAL = Path(__file__).resolve().parent
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
    checks = CheckLedger("P194-WN6-PHASE-SCALE")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.143.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned",
        _digest(PROPOSAL / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source inventory separates sites runtime executions and assertions",
        len(source_checks) == 24
        and not any(isinstance(node, ast.Assert) for node in ast.walk(source_tree)),
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "immutable source has no NumPy integration compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "source load-bearing interpretation remains visible for adjudication",
        all(
            token in source_text
            for token in (
                "rms phase excursion",
                "single-vacuum small-oscillation reading holds only",
                "cannot be absorbed into a redefinition of A alone",
                "FULL 2pi WINDINGS",
            )
        ),
    )

    x = sp.Symbol("x", real=True)
    exact_gap = x**2 / 2 - (1 - sp.cos(x))
    checks.check(
        "canonical API returns the exact quadratic minus cosine gap",
        sp.simplify(cosine_quadratic_gap(x) - exact_gap) == 0,
    )
    checks.check(
        "canonical API returns the exact fourth-order upper bound",
        cosine_quadratic_gap_bound(x) == x**4 / 24,
    )

    y, t = sp.symbols("y t", nonnegative=True)
    lower_kernel = (y - t) * (1 - sp.cos(t))
    lower_certificate = sp.integrate(lower_kernel, (t, 0, y))
    checks.check(
        "twice-integrated nonnegative cosine kernel equals the gap",
        sp.simplify(lower_certificate - cosine_quadratic_gap(y)) == 0,
    )
    checks.check(
        "lower certificate kernel exposes only nonnegative factors",
        sp.simplify(1 - sp.cos(t) - 2 * sp.sin(t / 2) ** 2) == 0
        and (y - t).is_nonnegative is None,
        "the interval condition zero<=t<=y supplies the first factor sign",
    )
    upper_kernel = (y - t) ** 3 * (1 - sp.cos(t)) / 6
    upper_certificate = sp.integrate(upper_kernel, (t, 0, y))
    checks.check(
        "four-times-integrated nonnegative kernel equals bound minus gap",
        sp.simplify(
            upper_certificate
            - (cosine_quadratic_gap_bound(y) - cosine_quadratic_gap(y))
        )
        == 0,
    )
    checks.check(
        "gap and upper-bound complements have four zero-origin data",
        all(sp.diff(upper_certificate, y, order).subs(y, 0) == 0 for order in range(4))
        and cosine_quadratic_gap(0) == 0,
    )

    relative_bound = sp.simplify(cosine_quadratic_gap_bound(x) / (x**2 / 2))
    checks.check(
        "relative-to-quadratic upper bound retains x squared over twelve",
        relative_bound == x**2 / 12,
    )
    epsilon = sp.Symbol("epsilon", positive=True)
    radius = sufficient_cosine_quadratic_domain(epsilon)
    checks.check(
        "tolerance domain saturates the exact sufficient relative bound",
        sp.simplify(radius**2 / 12 - epsilon) == 0,
    )
    checks.mutation_sensitive(
        "tolerance radius retains the factor twelve",
        lambda candidate: sp.simplify(candidate**2 / 12 - epsilon) == 0,
        radius,
        (sp.sqrt(2 * epsilon), sp.sqrt(6 * epsilon), sp.sqrt(24 * epsilon)),
    )

    barrier_relative_gap = sp.simplify(
        cosine_quadratic_gap(sp.pi) / (sp.pi**2 / 2)
    )
    checks.check(
        "barrier-top relative error is exact and not a small-error oracle",
        sp.simplify(barrier_relative_gap - (1 - 4 / sp.pi**2)) == 0
        and barrier_relative_gap > sp.Rational(59, 100),
    )
    for value in (sp.Rational(1, 10), sp.Rational(1, 2), 1, 2, sp.pi, 10):
        gap = cosine_quadratic_gap(value)
        checks.check(
            f"exact sample respects both global gap bounds at x={value}",
            gap >= 0 and sp.simplify(cosine_quadratic_gap_bound(value) - gap) >= 0,
        )
    checks.mutation_sensitive(
        "fourth-order denominator is load bearing",
        lambda denominator: all(
            sp.N(value**4 / denominator - cosine_quadratic_gap(value), 50) >= 0
            for value in (sp.Rational(1, 10), 1, 2, sp.pi)
        ),
        sp.Integer(24),
        (sp.Integer(25), sp.Integer(30), sp.Integer(48)),
    )

    peak, phase = sp.symbols("P u", real=True)
    direct_mean_square = sp.integrate(
        (peak * sp.cos(phase)) ** 2,
        (phase, 0, 2 * sp.pi),
    ) / (2 * sp.pi)
    checks.check(
        "direct full-cycle integration derives peak squared over two",
        sp.simplify(direct_mean_square - harmonic_cycle_mean_square(peak)) == 0
        and harmonic_cycle_mean_square(peak) == peak**2 / 2,
    )
    checks.check(
        "harmonic RMS keeps the absolute peak and square-root-two factor",
        harmonic_rms_from_peak(peak) == sp.Abs(peak) / sp.sqrt(2),
    )
    checks.mutation_sensitive(
        "harmonic mean-square factor is load bearing",
        lambda candidate: sp.simplify(candidate - direct_mean_square) == 0,
        peak**2 / 2,
        (peak**2, peak**2 / 4, 2 * peak**2),
    )
    checks.check(
        "harmonic pointwise barrier implies the sharper RMS-square ceiling",
        harmonic_cycle_mean_square(sp.pi) == sp.pi**2 / 2
        and sp.pi**2 / 2 < sp.pi**2,
    )

    n = sp.Symbol("n", positive=True)
    rms_threshold = sp.sqrt(n)
    peak_threshold = sp.sqrt(2 * n)
    checks.check(
        "RMS and peak intensity maps give distinct exact limb thresholds",
        sp.simplify(rms_threshold**2 - n) == 0
        and sp.simplify(peak_threshold**2 / 2 - n) == 0
        and sp.simplify(peak_threshold / rms_threshold - sp.sqrt(2)) == 0,
    )
    checks.check(
        "positive-amplitude domain is load bearing for the source iff",
        (-2) ** 2 > 1 and not (-2 > sp.sqrt(1)),
    )
    q0 = sp.Symbol("q_0", positive=True)
    classical_rms = sp.Symbol("A_RMS", positive=True)
    checks.check(
        "Fock-coordinate and classical-RMS intensities remain independent",
        sp.simplify(q0**2 - classical_rms**2) != 0,
    )

    M, amplitude = sp.symbols("M amplitude", positive=True)
    checks.check(
        "multi-mode product is algebraically absorbable into effective amplitude",
        sp.simplify(M * amplitude**2 - (sp.sqrt(M) * amplitude) ** 2) == 0,
    )
    checks.check(
        "mode count and amplitude are not separately identifiable from their product",
        1 * 2**2 == 4 * 1**2,
    )
    checks.check(
        "period-count label has no accepted winding boundary data in the source",
        "phi(+infty)" not in source_text
        and "phi(-infty)" not in source_text
        and "FULL 2pi WINDINGS" in source_text,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
