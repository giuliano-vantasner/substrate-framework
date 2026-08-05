#!/usr/bin/env python3
"""Primary exact verifier for the P193 WN5 accepted composition audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.bosonic_fock import factorial_one_mass, factorial_one_modes
from substrate_framework.branching import (
    relative_weighted_odds_enhancement,
    weighted_channel_allocation,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
PROPOSAL = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-37/"
    "bridge_WN5_gb4_preserved_and_new_prediction.py"
)
SOURCE_SHA256 = "5618ba007e041512a7d207026dc6369c8277312acba4c250219a1629585a7fbc"
RELEASE_SHA256 = "07040ba6cc29e6087c954cfbad108da100b2d53d05ba8982bdf0ba77435f45da"
FORMULA_FREEZE_SHA256 = "cacdf392e3956657e0b65d24cf236f39041d00b2a6a5e8ce0502edb8df6c7511"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _raw_weight(order: int, intensity: sp.Expr) -> sp.Expr:
    return sp.factor(intensity**order / sp.factorial(order))


def _comparison_fraction(weight: sp.Expr, population: sp.Expr, rho: sp.Expr) -> sp.Expr:
    return sp.factor(rho / (population * weight + rho))


def main() -> int:
    checks = CheckLedger("P193-WN5-COMPOSITION")
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
        len(source_checks) == 22
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
        "source headline and load-bearing finite oracle remain visible",
        all(
            token in source_text
            for token in (
                "NEW PREDICTION (discriminating)",
                "grid = list(range(1, 61))",
                "key=lambda i: Bg_vals[i]",
                "abs(grid[imin] - S_s) <= 1",
            )
        ),
    )

    rho = sp.Rational(3, 5)
    baseline = sp.Rational(7, 4)
    comparison = sp.factor(baseline * rho)
    population = 6
    for intensity, order in (
        (sp.Rational(1, 3), 0),
        (sp.Rational(1, 3), 4),
        (sp.Rational(5, 2), 2),
        (sp.Integer(5), 4),
        (sp.Integer(5), 5),
        (sp.Integer(25), 60),
    ):
        weight = factorial_one_mass(
            order,
            intensity=intensity,
            support="all_nonnegative",
        )
        allocation = weighted_channel_allocation(
            baseline,
            comparison,
            weight,
            population,
        )
        checks.check(
            f"accepted APIs compose the exact branch fraction at S={intensity} n={order}",
            weight == _raw_weight(order, intensity)
            and allocation.baseline_ratio == rho
            and sp.simplify(
                allocation.comparison_fraction
                - _comparison_fraction(weight, population, rho)
            )
            == 0
            and sp.simplify(
                allocation.weighted_fraction
                + allocation.comparison_fraction
                - 1
            )
            == 0,
        )

    N, w, rho_symbol = sp.symbols("N w rho", positive=True)
    generic = _comparison_fraction(w, N, rho_symbol)
    fixed_partial = sp.diff(generic, N)
    checks.check(
        "fixed-weight population partial is exactly negative",
        sp.simplify(fixed_partial + rho_symbol * w / (N * w + rho_symbol) ** 2)
        == 0
        and fixed_partial.is_negative is True,
    )
    checks.mutation_sensitive(
        "population partial retains weight numerator and squared denominator",
        lambda candidate: sp.simplify(candidate - fixed_partial) == 0,
        -rho_symbol * w / (N * w + rho_symbol) ** 2,
        (
            -rho_symbol / (N * w + rho_symbol) ** 2,
            rho_symbol * w / (N * w + rho_symbol) ** 2,
            -rho_symbol * w / (N * w + rho_symbol),
        ),
    )

    path_weight = sp.Function("w")(N)
    path_fraction = rho_symbol / (N * path_weight + rho_symbol)
    path_derivative = sp.diff(path_fraction, N)
    expected_path = -rho_symbol * (
        path_weight + N * sp.diff(path_weight, N)
    ) / (N * path_weight + rho_symbol) ** 2
    checks.check(
        "population-dependent continuous path retains the N times weight derivative",
        sp.simplify(path_derivative - expected_path) == 0,
    )
    checks.check(
        "inverse-population weight is the exact constant-fraction counterpath",
        sp.simplify(path_derivative.subs(path_weight, 1 / N).doit()) == 0,
    )
    alpha = sp.Symbol("alpha", positive=True)
    exponential_path = sp.simplify(
        path_derivative.subs(path_weight, sp.exp(-alpha * N)).doit()
    )
    checks.check(
        "exponential population path changes sign at alpha times N equals one",
        sp.factor(exponential_path)
        == rho_symbol * (alpha * N - 1) * sp.exp(alpha * N)
        / (N + rho_symbol * sp.exp(alpha * N)) ** 2,
    )
    checks.mutation_sensitive(
        "total path derivative does not collapse to the fixed-weight partial",
        lambda candidate: sp.simplify(candidate - expected_path) == 0,
        path_derivative,
        (
            -rho_symbol * path_weight / (N * path_weight + rho_symbol) ** 2,
            -rho_symbol * sp.diff(path_weight, N) / (N * path_weight + rho_symbol) ** 2,
            rho_symbol * (path_weight + N * sp.diff(path_weight, N))
            / (N * path_weight + rho_symbol) ** 2,
        ),
    )

    n = sp.Symbol("n", integer=True, nonnegative=True)
    S = sp.Symbol("S", positive=True)
    weight_n = sp.Symbol("w_n", positive=True)
    weight_next = weight_n * S / (n + 1)
    branch_n = _comparison_fraction(weight_n, N, rho_symbol)
    branch_next = _comparison_fraction(weight_next, N, rho_symbol)
    adjacent_difference = sp.factor(branch_next - branch_n)
    expected_difference = sp.factor(
        rho_symbol
        * N
        * weight_n
        * (n + 1 - S)
        / (
            (n + 1)
            * (N * weight_next + rho_symbol)
            * (N * weight_n + rho_symbol)
        )
    )
    checks.check(
        "exact adjacent branch-fraction difference has sign n plus one minus S",
        sp.simplify(adjacent_difference - expected_difference) == 0,
    )
    wrong_squared_difference = sp.factor(
        _comparison_fraction(weight_n * S / (n + 1) ** 2, N, rho_symbol)
        - branch_n
    )
    checks.mutation_sensitive(
        "adjacent sign keeps the off-by-one threshold and orientation",
        lambda candidate: sp.simplify(candidate - expected_difference) == 0,
        adjacent_difference,
        (
            expected_difference.subs(n + 1 - S, n - S),
            -expected_difference,
            wrong_squared_difference,
        ),
    )

    for intensity in (
        sp.Rational(1, 3),
        sp.Rational(5, 2),
        sp.Integer(5),
        sp.Integer(25),
    ):
        modes = factorial_one_modes(
            intensity=intensity,
            support="all_nonnegative",
        )
        upper = int(sp.ceiling(intensity)) + 8
        values = [
            _comparison_fraction(_raw_weight(order, intensity), 4, sp.Rational(1, 2))
            for order in range(upper)
        ]
        minimum = min(values)
        brute_minima = tuple(index for index, value in enumerate(values) if value == minimum)
        checks.check(
            f"inverse allocation preserves every exact mass mode at S={intensity}",
            brute_minima == modes,
        )
    checks.check(
        "the omitted order-zero endpoint is the minimum when zero is less than S less than one",
        factorial_one_modes(
            intensity=sp.Rational(1, 3),
            support="all_nonnegative",
        )
        == (0,),
    )
    checks.mutation_sensitive(
        "integer intensity retains two adjacent minima",
        lambda candidate: candidate == (24, 25),
        factorial_one_modes(intensity=25, support="all_nonnegative"),
        ((25,), (24,), (23, 24)),
    )

    for intensity, order, count in (
        (sp.Rational(2, 3), 1, 1),
        (sp.Rational(2, 3), 4, 7),
        (sp.Rational(5, 2), 2, 3),
        (sp.Integer(5), 6, 11),
    ):
        weight = _raw_weight(order, intensity)
        exact = relative_weighted_odds_enhancement(weight, count, intensity)
        expected = sp.factor(count * intensity ** (order - 1) / sp.factorial(order))
        checks.check(
            f"relative odds retain N S^(n-1)/n! at S={intensity} n={order}",
            sp.simplify(exact - expected) == 0,
        )
    order = sp.Symbol("m", integer=True, positive=True)
    enhancement = N * S ** (order - 1) / sp.factorial(order)
    enhancement_next = N * S**order / sp.factorial(order + 1)
    checks.check(
        "relative-odds adjacent ratio is the accepted factorial-one ratio",
        sp.combsimp(enhancement_next / enhancement) == S / (order + 1),
    )
    threshold = sp.factorial(order) / S ** (order - 1)
    checks.check(
        "relative-odds equality retains its supplied population threshold",
        sp.simplify(enhancement.subs(N, threshold) - 1) == 0,
    )
    checks.mutation_sensitive(
        "enhancement retains population intensity power and order factorial",
        lambda candidate: sp.simplify(candidate - enhancement) == 0,
        N * S ** (order - 1) / sp.factorial(order),
        (
            S ** (order - 1) / sp.factorial(order),
            N * S**order / sp.factorial(order),
            N * S ** (order - 1) / sp.factorial(order) ** 2,
        ),
    )

    x, exponent = sp.symbols("x k", positive=True)
    named_weights = {
        "linear": x,
        "positive power": x**exponent,
        "decaying exponential": sp.exp(-alpha * x),
    }
    expected_weight_derivative_signs = {
        "linear": 1,
        "positive power": 1,
        "decaying exponential": -1,
    }
    for label, named_weight in named_weights.items():
        derivative = sp.diff(named_weight, x)
        branch_derivative = sp.factor(
            sp.diff(rho_symbol / (N * named_weight + rho_symbol), x)
        )
        checks.check(
            f"named {label} branch shape follows the exact weight derivative with opposite sign",
            derivative.is_positive
            == (expected_weight_derivative_signs[label] > 0)
            and branch_derivative.is_negative
            == (expected_weight_derivative_signs[label] > 0)
            and branch_derivative.is_positive
            == (expected_weight_derivative_signs[label] < 0),
        )

    coupling, spectral_density = sp.symbols("g sigma", real=True)
    mathematical_fraction = _comparison_fraction(sp.Rational(5, 6), 4, rho)
    putative_rate = coupling**2 * spectral_density * mathematical_fraction
    checks.check(
        "zero interaction and zero spectral density block physical prediction semantics",
        0 < mathematical_fraction < 1
        and putative_rate.subs(coupling, 0) == 0
        and putative_rate.subs(spectral_density, 0) == 0,
    )
    checks.check(
        "accepted public APIs already express the complete warranted composition",
        callable(weighted_channel_allocation)
        and callable(relative_weighted_odds_enhancement)
        and callable(factorial_one_mass)
        and callable(factorial_one_modes),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
