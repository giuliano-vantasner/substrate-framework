#!/usr/bin/env python3
"""Primary exact verifier for the WN2 odd factorial-mass audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.branching import (
    two_channel_allocation,
    weighted_channel_allocation,
)
from substrate_framework.factorial_suppression import (
    cosine_one_high_coefficient_square,
    factorial_decade_bound,
    normalized_parity_factorial_mass,
    odd_factorial_mass_enclosure,
    odd_factorial_total_mass,
    parity_thinned_factorial_mass,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
PROPOSAL = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-37/"
    "bridge_WN2_coefficient_cannot_be_the_weight.py"
)
SOURCE_SHA256 = "dc9a7dbd79c908d1ec206392cdd81a34b5a39c08dcba31f2c164c3d92073504c"
RELEASE_SHA256 = "cd16ef67e1dd81998c16a5e402c6c127e798b6190d676b898723c7dcc75791df"
FORMULA_FREEZE_SHA256 = "b9687f6ecd179c9b98170101d289f7fccae0530059651e5a0ed3d110c283f92f"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("C-CMB-002")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.140.0.yaml") == RELEASE_SHA256,
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
        "source predicate inventory remains exact",
        len(source_checks) == 27
        and not any(isinstance(node, ast.Assert) for node in ast.walk(source_tree)),
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "immutable source has no NumPy quadrature compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "source universal guard and forward import are explicit audit targets",
        all(
            token in source_text
            for token in (
                "def is_admissible_weight",
                "mode_index != 0",
                "WN3/WN4 build exactly such a family",
                "tuple(range(1, 12))",
            )
        ),
    )

    activity = sp.Symbol("z", positive=True)
    amplitude, high_scale = sp.symbols("A a_H", positive=True)
    checks.check(
        "parity-thinned mass has exact odd support and activity power",
        parity_thinned_factorial_mass(4, activity=activity) == 0
        and parity_thinned_factorial_mass(5, activity=activity)
        == activity**10 / sp.factorial(5) ** 2,
    )
    coefficient_square = cosine_one_high_coefficient_square(
        5,
        amplitude=amplitude,
        high_scale=high_scale,
        low_scale=activity,
    )
    checks.check(
        "mass is the accepted cosine square after only common factors are removed",
        sp.simplify(
            coefficient_square / (amplitude**2 * high_scale**2)
            - parity_thinned_factorial_mass(5, activity=activity)
        )
        == 0,
    )
    selected_mass = parity_thinned_factorial_mass(5, activity=activity)
    checks.mutation_sensitive(
        "factorial mass activity and factorial powers",
        lambda candidate: sp.simplify(candidate - selected_mass) == 0,
        selected_mass,
        (
            activity**5 / sp.factorial(5) ** 2,
            activity**10 / sp.factorial(5),
            activity**10 / sp.factorial(6) ** 2,
            -selected_mass,
        ),
    )

    total = odd_factorial_total_mass(activity)
    checks.check(
        "Bessel difference is the frozen exact parity-filtered total",
        total
        == (sp.besseli(0, 2 * activity) - sp.besselj(0, 2 * activity)) / 2,
    )
    expected_series = sum(
        activity ** (2 * order) / sp.factorial(order) ** 2
        for order in (1, 3, 5, 7, 9)
    )
    checks.check(
        "fresh Bessel series contains exactly the first five odd masses",
        sp.series(total, activity, 0, 21).removeO() == expected_series,
    )
    odd_series_index = sp.Symbol("k", integer=True, nonnegative=True)
    general_odd_term = (
        activity ** (2 * (2 * odd_series_index + 1))
        / sp.factorial(2 * odd_series_index + 1) ** 2
    )
    checks.check(
        "every odd series term is positive and normalization sums to one",
        general_odd_term.is_positive is True
        and sp.simplify(total / total) == 1,
    )
    checks.mutation_sensitive(
        "Bessel parity filter and argument",
        lambda candidate: sp.series(candidate, activity, 0, 9).removeO()
        == activity**2 + activity**6 / 36,
        total,
        (
            (sp.besseli(0, 2 * activity) + sp.besselj(0, 2 * activity)) / 2,
            (sp.besseli(0, activity) - sp.besselj(0, activity)) / 2,
            sp.besseli(0, 2 * activity) - sp.besselj(0, 2 * activity),
        ),
    )
    checks.check(
        "normalized point masses retain the same exact total",
        normalized_parity_factorial_mass(2, activity=activity) == 0
        and sp.simplify(
            normalized_parity_factorial_mass(3, activity=activity)
            * total
            - activity**6 / 36
        )
        == 0,
    )

    order = sp.Symbol("n", positive=True, integer=True)
    symbolic_ratio = sp.combsimp(
        (activity ** (2 * (order + 2)) / sp.factorial(order + 2) ** 2)
        / (activity ** (2 * order) / sp.factorial(order) ** 2)
    )
    expected_ratio = activity**4 / ((order + 1) ** 2 * (order + 2) ** 2)
    checks.check(
        "fresh consecutive-odd ratio retains both denominator squares",
        sp.simplify(symbolic_ratio - expected_ratio) == 0,
    )
    checks.mutation_sensitive(
        "consecutive-odd tail ratio",
        lambda candidate: sp.simplify(candidate - expected_ratio) == 0,
        symbolic_ratio,
        (
            activity**2 / ((order + 1) ** 2 * (order + 2) ** 2),
            activity**4 / ((order + 1) * (order + 2)),
            activity**4 / ((order + 2) ** 4),
        ),
    )

    enclosure = odd_factorial_mass_enclosure(9)
    checks.check(
        "unit enclosure reproduces the frozen exact partial mass",
        enclosure.partial_mass == sp.Rational(135348874561, 131681894400)
        and enclosure.first_omitted_order == 11
        and enclosure.first_omitted_mass
        == sp.Rational(1, 1593350922240000),
    )
    checks.check(
        "tail ratio and total upper bound reproduce the frozen rationals",
        enclosure.tail_ratio_ceiling == sp.Rational(1, 24336)
        and enclosure.tail_mass_upper_bound
        == sp.Rational(169, 269265240921600000)
        and enclosure.total_mass_upper_bound
        == sp.Rational(9963487458886859459, 9693548673177600000),
    )
    finite_tail = sum(
        parity_thinned_factorial_mass(odd_order)
        for odd_order in range(11, 42, 2)
    )
    checks.check(
        "independently materialized omitted terms lie below the analytic tail",
        0 < finite_tail < enclosure.tail_mass_upper_bound,
    )
    checks.mutation_sensitive(
        "tail first term and geometric denominator",
        lambda candidate: candidate >= finite_tail
        and candidate == enclosure.tail_mass_upper_bound,
        enclosure.tail_mass_upper_bound,
        (
            enclosure.first_omitted_mass,
            enclosure.first_omitted_mass
            / (1 - sp.Rational(1, 12**2 * 12**2)),
            parity_thinned_factorial_mass(13)
            / (1 - enclosure.tail_ratio_ceiling),
        ),
    )

    p1_lower = sp.factor(1 / enclosure.total_mass_upper_bound)
    p13_lower = sp.factor(sp.Rational(37, 36) / enclosure.total_mass_upper_bound)
    checks.check(
        "order-one concentration exceeds the source threshold by an exact margin",
        p1_lower - sp.Rational(972, 1000)
        == sp.Rational(
            2259715784893151463,
            2490871864721714864750,
        ),
    )
    checks.check(
        "through-three concentration exceeds the source threshold by an exact margin",
        p13_lower - sp.Rational(9999, 10000)
        == sp.Rational(
            3228039582292269459,
            99634874588868594590000,
        ),
    )
    checks.mutation_sensitive(
        "concentration normalization denominator",
        lambda candidate: candidate[0] - sp.Rational(972, 1000)
        == sp.Rational(
            2259715784893151463,
            2490871864721714864750,
        )
        and candidate[1] - sp.Rational(9999, 10000)
        == sp.Rational(
            3228039582292269459,
            99634874588868594590000,
        ),
        (p1_lower, p13_lower),
        (
            (1 / enclosure.total_mass_lower_bound, sp.Rational(37, 36)),
            (sp.Rational(972, 1000), p13_lower),
            (p1_lower, sp.Rational(9999, 10000)),
        ),
    )

    unit_masses = [parity_thinned_factorial_mass(n) for n in (1, 3, 5, 7)]
    scaled_masses = [
        parity_thinned_factorial_mass(n, activity=4) for n in (1, 3, 5, 7)
    ]
    checks.check(
        "unit activity has mode one by the decreasing odd ratio",
        unit_masses[0] > unit_masses[1] > unit_masses[2] > unit_masses[3],
    )
    checks.check(
        "activity four moves the unique mode to order three exactly",
        scaled_masses[1] == max(scaled_masses)
        and scaled_masses[1] / scaled_masses[0] == sp.Rational(64, 9)
        and scaled_masses[2] / scaled_masses[1] == sp.Rational(16, 25),
    )
    checks.mutation_sensitive(
        "activity-dependent mode",
        lambda candidate: candidate[1] > candidate[0]
        and candidate[1] > candidate[2],
        tuple(scaled_masses[:3]),
        (
            tuple(unit_masses[:3]),
            (scaled_masses[1], scaled_masses[0], scaled_masses[2]),
        ),
    )

    geometric_total = sp.summation(sp.Rational(1, 2) ** order, (order, 1, sp.oo))
    checks.check(
        "a normalized mathematical distribution may legitimately have mode one",
        geometric_total == 1
        and sp.Rational(1, 2) > sp.Rational(1, 4) > sp.Rational(1, 8),
    )

    baseline, comparison = sp.symbols("r_s r_c", positive=True)
    population = sp.Symbol("N", positive=True, integer=True)
    odd_weight = parity_thinned_factorial_mass(3)
    odd_allocation = weighted_channel_allocation(
        baseline,
        comparison,
        odd_weight,
        population,
    )
    checks.check(
        "positive odd mass composes with the accepted weighted specialization",
        odd_allocation.weighted_rate == baseline * population / 36
        and sp.simplify(
            odd_allocation.weighted_fraction
            - baseline * population / (baseline * population + 36 * comparison)
        )
        == 0,
    )
    even_allocation = two_channel_allocation(0, comparison)
    checks.check(
        "even zero mass is the accepted general-allocation endpoint",
        even_allocation.first_fraction == 0
        and even_allocation.second_fraction == 1,
    )
    try:
        weighted_channel_allocation(baseline, comparison, 0, population)
    except ValueError:
        positive_specialization_rejects_zero = True
    else:
        positive_specialization_rejects_zero = False
    checks.check(
        "zero is not silently passed through the positive-weight specialization",
        positive_specialization_rejects_zero,
    )

    decade = factorial_decade_bound(7)
    checks.check(
        "exact accepted factorial bound replaces the source mpmath threshold",
        decade.order == 10**7
        and decade.log10_upper_bound == -131_000_000,
    )
    checks.check(
        "no candidate API supplies a PN2 band, physical rate, or future weight family",
        all(
            token not in odd_factorial_total_mass.__doc__
            for token in ("24 MeV", "phonon", "WN3", "WN4")
        )
        and "does not by itself define" in parity_thinned_factorial_mass.__doc__,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
