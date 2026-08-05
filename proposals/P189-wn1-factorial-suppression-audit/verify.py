#!/usr/bin/env python3
"""Primary exact verifier for the WN1 factorial-suppression audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.factorial_suppression import (
    cosine_one_high_coefficient_square,
    exact_rational_log10_floor,
    factorial_decade_bound,
    factorial_superpolynomial_tail,
    factorial_suppression_evidence,
)
from substrate_framework.cosine_vertices import cosine_mixed_coefficient
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
PROPOSAL = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-37/"
    "bridge_WN1_vertex_coefficient_magnitude.py"
)
SOURCE_SHA256 = "3764b29955c3bd51c10278159e08a52ff616a7041510e56917b091f1a802cdde"
RELEASE_SHA256 = "0617c10955594b30c6d0d122476e360494d9e1b065efdf4f5c67728583388bb8"
FORMULA_FREEZE_SHA256 = "7a10a60383d40b74db4f0a2951a3cad7018a18e7fc387c65f4866ed6667ce289"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _exact_inverse_square_factorial(order: int) -> sp.Rational:
    return sp.Rational(1, int(sp.factorial(order)) ** 2)


def main() -> int:
    checks = CheckLedger("C-CMB-001")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.139.0.yaml") == RELEASE_SHA256,
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
    source_assertions = [
        node for node in ast.walk(source_tree) if isinstance(node, ast.Assert)
    ]
    checks.check(
        "source predicate inventory remains exact",
        len(source_checks) == 20 and not source_assertions,
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
        "source coefficient is explicitly the unit-normalized vacuum specialization",
        all(
            token in source_text
            for token in (
                "V = 1 - sp.cos(phi_H + phi_L)",
                "return sp.Integer(-1)**((n - 1) // 2) / sp.factorial(n)",
                "return sp.Rational(1, 1) / sp.factorial(n)**2",
            )
        ),
    )
    checks.check(
        "source universal labels are operationally finite",
        all(
            token in source_text
            for token in (
                "for n in [1, 2, 3, 5, 8, 13, 21, 34]",
                "for n in [7, 15, 31, 51]",
                "for p in (2, 4, 8)",
                "mp.mp.dps = 60",
            )
        ),
    )

    amplitude, high_scale, low_scale = sp.symbols("A a_H a_L", real=True)
    odd_square = cosine_one_high_coefficient_square(
        5,
        amplitude=amplitude,
        high_scale=high_scale,
        low_scale=low_scale,
    )
    expected_odd_square = (
        amplitude**2 * high_scale**2 * low_scale**10 / sp.factorial(5) ** 2
    )
    checks.check(
        "general odd coefficient square retains every declared normalization",
        sp.simplify(odd_square - expected_odd_square) == 0,
    )
    checks.check(
        "vacuum even-order square vanishes",
        cosine_one_high_coefficient_square(
            4,
            amplitude=amplitude,
            high_scale=high_scale,
            low_scale=low_scale,
        )
        == 0,
    )
    background = sp.Symbol("phi_0", real=True)
    background_mutated = cosine_mixed_coefficient(
        1,
        4,
        amplitude=amplitude,
        high_scale=high_scale,
        low_scale=low_scale,
        background=background,
    )
    checks.check(
        "background mutation removes the vacuum even-order support rule",
        background_mutated.subs(background, 0) == 0
        and background_mutated.subs(background, sp.pi / 2) != 0,
    )
    checks.mutation_sensitive(
        "coefficient-square normalization",
        lambda candidate: sp.simplify(candidate - expected_odd_square) == 0,
        odd_square,
        (
            odd_square / sp.factorial(5) ** 2,
            amplitude * high_scale**2 * low_scale**10 / sp.factorial(5) ** 2,
            amplitude**2 * high_scale**2 * low_scale**5 / sp.factorial(5) ** 2,
            4 * odd_square,
        ),
    )

    sequence = [factorial_suppression_evidence(order) for order in range(1, 18)]
    checks.check(
        "inverse-square factorial values are exact and positive",
        all(
            item.inverse_square_factorial
            == _exact_inverse_square_factorial(item.order)
            and item.inverse_square_factorial > 0
            for item in sequence
        ),
    )
    checks.check(
        "exact recurrence makes the positive sequence strictly decreasing",
        all(
            item.recurrence_ratio == sp.Rational(1, (item.order + 1) ** 2)
            and item.next_inverse_square_factorial < item.inverse_square_factorial
            for item in sequence
        ),
    )
    recurrence_order = 11
    recurrence = factorial_suppression_evidence(recurrence_order).recurrence_ratio
    checks.mutation_sensitive(
        "inverse-square recurrence denominator",
        lambda candidate: candidate == sp.Rational(1, (recurrence_order + 1) ** 2),
        recurrence,
        (
            sp.Rational(1, recurrence_order + 1),
            sp.Rational(1, recurrence_order**2),
            sp.Rational(1, (recurrence_order + 1) ** 3),
        ),
    )

    expected_floors = {1: 0, 3: -2, 5: -5, 7: -8, 15: -25, 31: -68, 51: -133}
    actual_floors = {
        order: exact_rational_log10_floor(_exact_inverse_square_factorial(order))
        for order in expected_floors
    }
    checks.check("exact decimal floors reproduce the source table", actual_floors == expected_floors)
    checks.check(
        "decimal floors are certified by adjacent integer powers",
        all(
            sp.Integer(10) ** exponent
            <= _exact_inverse_square_factorial(order)
            < sp.Integer(10) ** (exponent + 1)
            for order, exponent in actual_floors.items()
        ),
    )

    finite_sum = sum(sp.Rational(1, sp.factorial(k)) for k in range(4))
    geometric_tail_majorant = sp.Rational(1, 24) * sum(
        sp.Rational(1, 5) ** offset for offset in range(40)
    ) + sp.Rational(1, 24) * sp.Rational(1, 5) ** 40 / (1 - sp.Rational(1, 5))
    series_bound = finite_sum + sp.Rational(1, 18)
    checks.check(
        "fresh exponential-series tail gives e below forty-nine eighteenths",
        finite_sum == sp.Rational(8, 3)
        and geometric_tail_majorant == sp.Rational(5, 96)
        and geometric_tail_majorant < sp.Rational(1, 18)
        and series_bound == sp.Rational(49, 18),
    )
    checks.check(
        "fresh rational comparison gives the convenient eleven-fourths bound",
        sp.Rational(49, 18) < sp.Rational(11, 4),
    )
    left_power = 11**20
    right_power = 10**9 * 4**20
    checks.check(
        "fresh integer power comparison has the frozen positive margin",
        left_power == 672_749_994_932_560_009_201
        and right_power == 1_099_511_627_776_000_000_000
        and right_power - left_power == 426_761_632_843_439_990_799,
    )
    checks.mutation_sensitive(
        "rational exponential ceiling",
        lambda candidate: candidate[0] == sp.Rational(8, 3)
        and candidate[1] < sp.Rational(1, 18)
        and candidate[0] + sp.Rational(1, 18) < candidate[2],
        (finite_sum, geometric_tail_majorant, sp.Rational(11, 4)),
        (
            (finite_sum, sp.Rational(1, 18), sp.Rational(11, 4)),
            (finite_sum, geometric_tail_majorant, sp.Rational(49, 18)),
            (finite_sum + 1, geometric_tail_majorant, sp.Rational(11, 4)),
        ),
    )

    # For every positive integer n, the k=n term is positive and the k=0
    # term is a separate positive term of exp(n). Taking positive nth roots
    # and reciprocals then yields the strict inverse-square bound. The finite
    # values below are sensitivity probes for the algebra, not its quantifier.
    for order in (1, 2, 3, 5, 8, 13, 21, 34):
        selected_term = sp.Rational(order**order, int(sp.factorial(order)))
        partial = sum(
            sp.Rational(order**power, int(sp.factorial(power)))
            for power in range(order + 1)
        )
        checks.check(
            f"positive-series consequence is strict at sensitivity order {order}",
            partial > selected_term
            and _exact_inverse_square_factorial(order)
            < (sp.E / order) ** (2 * order),
        )
    lower, positive_gap = sp.symbols("x delta", positive=True)
    reciprocal_gap = sp.factor(1 / lower**2 - 1 / (lower + positive_gap) ** 2)
    checks.check(
        "universal bound direction follows from positive root and reciprocal order",
        reciprocal_gap
        == positive_gap
        * (2 * lower + positive_gap)
        / (lower**2 * (lower + positive_gap) ** 2)
        and all(item.exponential_upper_bound > item.inverse_square_factorial for item in sequence),
    )
    selected_bound = factorial_suppression_evidence(13)
    checks.mutation_sensitive(
        "exponential inverse-square bound direction",
        lambda candidate: candidate[0] < candidate[1],
        (
            selected_bound.inverse_square_factorial,
            selected_bound.exponential_upper_bound,
        ),
        (
            (
                selected_bound.exponential_upper_bound,
                selected_bound.inverse_square_factorial,
            ),
            (
                selected_bound.exponential_upper_bound,
                selected_bound.exponential_upper_bound,
            ),
        ),
    )

    expected_decades = {7: -131_000_000, 9: -17_100_000_000, 11: -2_110_000_000_000}
    decade_bounds = {decade: factorial_decade_bound(decade) for decade in expected_decades}
    checks.check(
        "exact decade grouping reproduces every exposed exponent ceiling",
        all(
            bound.order == 10**decade
            and bound.positive_exponent == (20 * decade - 9) * 10**decade // 10
            and bound.log10_upper_bound == expected_decades[decade]
            for decade, bound in decade_bounds.items()
        ),
    )
    checks.check(
        "decade exponents are strictly stronger along the exposed sequence",
        expected_decades[7] > expected_decades[9] > expected_decades[11],
    )
    decade = 9
    baseline_exponent = decade_bounds[decade].positive_exponent
    checks.mutation_sensitive(
        "decade block length and exponent",
        lambda candidate: candidate == (20 * decade - 9) * 10**decade // 10,
        baseline_exponent,
        (
            (20 * decade - 9) * 10**decade,
            (2 * decade - 9) * 10**decade // 10,
            (20 * decade - 8) * 10**decade // 10,
        ),
    )

    n_symbol = sp.Symbol("n", positive=True, integer=True)
    p_symbol = sp.Symbol("p", nonnegative=True, integer=True)
    exact_ratio = sp.simplify(
        ((n_symbol + 1) ** p_symbol / sp.factorial(n_symbol + 1) ** 2)
        / (n_symbol**p_symbol / sp.factorial(n_symbol) ** 2)
    )
    checks.check(
        "fresh consecutive-ratio derivation retains the factorial square",
        sp.combsimp(
            exact_ratio
            / (((n_symbol + 1) / n_symbol) ** p_symbol / (n_symbol + 1) ** 2)
        )
        == 1,
    )
    tail_certificates = [factorial_superpolynomial_tail(power) for power in range(33)]
    checks.check(
        "every sampled fixed-power certificate starts a geometric half-tail",
        all(
            certificate.exact_ratio_at_start <= certificate.ratio_ceiling
            and certificate.ratio_ceiling == sp.Rational(1, 2)
            for certificate in tail_certificates
        ),
    )
    arbitrary_large_power = factorial_superpolynomial_tail(257)
    checks.check(
        "integer ceiling construction works without a finite-power theorem cutoff",
        all(
            (certificate.start_order + 1) ** 2 >= 2 ** (certificate.power + 1)
            for certificate in (*tail_certificates, arbitrary_large_power)
        )
        and arbitrary_large_power.power == 257,
    )
    selected_tail = factorial_superpolynomial_tail(17)
    checks.mutation_sensitive(
        "superpolynomial half-tail start",
        lambda candidate: candidate >= 1
        and (candidate + 1) ** 2 >= 2**18,
        selected_tail.start_order,
        (selected_tail.start_order - 1, 20, 1),
    )

    exact_large = factorial_suppression_evidence(171).inverse_square_factorial
    try:
        machine_large = 1.0 / float(sp.factorial(171)) ** 2
    except OverflowError:
        machine_large = 0.0
    checks.check(
        "machine zero is separated from exact positivity",
        machine_large == 0.0 and exact_large > 0,
    )

    unit_classical_square = cosine_one_high_coefficient_square(3)
    interaction_scale, spectral_density = sp.symbols("g rho", nonnegative=True)
    conditional_rate = sp.simplify(
        2 * sp.pi * interaction_scale**2 * spectral_density * unit_classical_square
    )
    checks.check(
        "zero interaction countermodel preserves the coefficient but kills a conditional rate",
        unit_classical_square == sp.Rational(1, 36)
        and conditional_rate.subs(interaction_scale, 0) == 0,
    )
    checks.check(
        "zero spectral-density countermodel preserves the coefficient but kills a conditional rate",
        unit_classical_square > 0 and conditional_rate.subs(spectral_density, 0) == 0,
    )
    pn2_text = (ROOT / "campaigns/P110-pn2-energy-subdivision-count-audit/adjudication.yaml").read_text(
        encoding="utf-8"
    )
    registry_text = (ROOT / "governance/claims.yaml").read_text(encoding="utf-8")
    checks.check(
        "accepted PN2 adjudication supplies no physical subdivision claim",
        "claims: []" in pn2_text and "PN2: qualified" in pn2_text,
    )
    checks.check(
        "accepted spin theorem independently excludes coefficient-square rate inference",
        "A squared ladder coefficient is not a rate." in registry_text
        and "Fermi-Golden-Rule regime" in registry_text,
    )

    own_compatibility = audit_numpy_trapezoid_compatibility(
        Path(__file__).read_text(encoding="utf-8"),
        filename=str(Path(__file__)),
    )
    module_compatibility = audit_numpy_trapezoid_compatibility(
        (ROOT / "src/substrate_framework/factorial_suppression.py").read_text(
            encoding="utf-8"
        ),
        filename="factorial_suppression.py",
    )
    checks.check(
        "mutable implementation and verifier have no legacy quadrature surface",
        own_compatibility.legacy_references == 0
        and module_compatibility.legacy_references == 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
