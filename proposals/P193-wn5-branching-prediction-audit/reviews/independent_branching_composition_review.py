#!/usr/bin/env python3
"""Independent raw-SymPy WN5 composition rederivation for P193."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
PROPOSAL = Path(__file__).resolve().parents[1]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-37/"
    "bridge_WN5_gb4_preserved_and_new_prediction.py"
)
SOURCE_SHA256 = "5618ba007e041512a7d207026dc6369c8277312acba4c250219a1629585a7fbc"
RELEASE_SHA256 = "07040ba6cc29e6087c954cfbad108da100b2d53d05ba8982bdf0ba77435f45da"
FORMULA_FREEZE_SHA256 = "cacdf392e3956657e0b65d24cf236f39041d00b2a6a5e8ce0502edb8df6c7511"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _weight(order: int | sp.Expr, intensity: sp.Expr) -> sp.Expr:
    return intensity**order / sp.factorial(order)


def _branch(order: int, intensity: sp.Expr, population: sp.Expr, rho: sp.Expr) -> sp.Expr:
    return sp.factor(rho / (population * _weight(order, intensity) + rho))


def main() -> int:
    checks = CheckLedger("P193-WN5-INDEPENDENT")
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

    S, N, rho = sp.symbols("S N rho", positive=True)
    n = sp.Symbol("n", integer=True, nonnegative=True)
    w_n = sp.Symbol("w_n", positive=True)
    w_next = w_n * S / (n + 1)
    branch_n = rho / (N * w_n + rho)
    branch_next = rho / (N * w_next + rho)
    adjacent = sp.factor(branch_next - branch_n)
    expected = sp.factor(
        rho
        * N
        * w_n
        * (n + 1 - S)
        / ((n + 1) * (N * w_next + rho) * (N * w_n + rho))
    )
    checks.check(
        "raw fraction subtraction gives the exact adjacent difference",
        sp.simplify(adjacent - expected) == 0,
    )
    checks.check(
        "raw difference has only the n plus one minus S sign factor",
        sp.simplify(adjacent / expected) == 1,
    )
    wrong_squared_ratio = w_n * S / (n + 1) ** 2
    wrong_adjacent = sp.factor(
        rho / (N * wrong_squared_ratio + rho) - branch_n
    )
    checks.check(
        "a squared-factorial mutation changes the turnover threshold",
        sp.simplify(wrong_adjacent - adjacent) != 0,
    )

    for intensity in (
        sp.Rational(1, 3),
        sp.Rational(2, 3),
        sp.Rational(5, 2),
        sp.Integer(1),
        sp.Integer(2),
        sp.Integer(5),
        sp.Integer(25),
    ):
        upper = int(sp.ceiling(intensity)) + 8
        weights = [_weight(index, intensity) for index in range(upper)]
        maximum = max(weights)
        weight_modes = tuple(
            index for index, value in enumerate(weights) if value == maximum
        )
        branches = [
            _branch(index, intensity, sp.Integer(4), sp.Rational(1, 2))
            for index in range(upper)
        ]
        minimum = min(branches)
        branch_minima = tuple(
            index for index, value in enumerate(branches) if value == minimum
        )
        expected_modes = (
            (int(intensity) - 1, int(intensity))
            if intensity.is_integer
            else (int(sp.floor(intensity)),)
        )
        checks.check(
            f"raw exact grid preserves the complete inverse mode set at S={intensity}",
            weight_modes == branch_minima == expected_modes,
        )
    checks.check(
        "raw subunit intensity exposes the source grid's omitted zero endpoint",
        _branch(0, sp.Rational(1, 3), 4, sp.Rational(1, 2))
        < _branch(1, sp.Rational(1, 3), 4, sp.Rational(1, 2)),
    )

    m = sp.Symbol("m", integer=True, positive=True)
    enhancement = N * S ** (m - 1) / sp.factorial(m)
    next_enhancement = N * S**m / sp.factorial(m + 1)
    checks.check(
        "raw relative-odds adjacent ratio is S over m plus one",
        sp.combsimp(next_enhancement / enhancement) == S / (m + 1),
    )
    threshold = sp.factorial(m) / S ** (m - 1)
    checks.check(
        "raw enhancement equals one exactly at its supplied population threshold",
        sp.simplify(enhancement.subs(N, threshold) - 1) == 0,
    )
    checks.check(
        "omitting population changes the raw enhancement",
        sp.simplify(enhancement - S ** (m - 1) / sp.factorial(m)) != 0,
    )
    for intensity, order in (
        (sp.Rational(1, 2), 4),
        (sp.Rational(3, 2), 3),
        (sp.Integer(5), 6),
    ):
        exact_threshold = sp.factorial(order) / intensity ** (order - 1)
        integer_above = int(sp.floor(exact_threshold)) + 1
        checks.check(
            f"smallest integer above the raw threshold gives strict enhancement at S={intensity} n={order}",
            integer_above > exact_threshold
            and sp.simplify(
                integer_above * intensity ** (order - 1) / sp.factorial(order)
            )
            > 1,
        )

    x = sp.Symbol("x", positive=True)
    path_weight = sp.Function("u")(x)
    path_branch = rho / (x * path_weight + rho)
    path_derivative = sp.diff(path_branch, x)
    expected_path = -rho * (
        path_weight + x * sp.diff(path_weight, x)
    ) / (x * path_weight + rho) ** 2
    checks.check(
        "raw total derivative retains the path-weight derivative",
        sp.simplify(path_derivative - expected_path) == 0,
    )
    checks.check(
        "raw inverse-population path has constant comparison fraction",
        sp.simplify(path_derivative.subs(path_weight, 1 / x).doit()) == 0,
    )
    alpha = sp.Symbol("alpha", positive=True)
    exponential_path = sp.factor(
        path_derivative.subs(path_weight, sp.exp(-alpha * x)).doit()
    )
    checks.check(
        "raw exponential path has the alpha times x minus one sign factor",
        exponential_path
        == rho * (alpha * x - 1) * sp.exp(alpha * x)
        / (rho * sp.exp(alpha * x) + x) ** 2,
    )

    k = sp.Symbol("k", positive=True)
    named_weights = (x, x**k, sp.exp(-alpha * x))
    expected_signs = (-1, -1, 1)
    for index, (named_weight, sign) in enumerate(
        zip(named_weights, expected_signs, strict=True),
        start=1,
    ):
        derivative = sp.factor(sp.diff(rho / (N * named_weight + rho), x))
        checks.check(
            f"raw named-family derivative {index} has its exact monotonic sign",
            (derivative.is_negative is True if sign < 0 else derivative.is_positive is True),
        )

    coupling, spectral_density = sp.symbols("g sigma", real=True)
    positive_fraction = _branch(4, sp.Integer(5), 6, sp.Rational(3, 5))
    putative_rate = coupling**2 * spectral_density * positive_fraction
    checks.check(
        "raw zero-interaction countermodels block physical prediction semantics",
        0 < positive_fraction < 1
        and putative_rate.subs(coupling, 0) == 0
        and putative_rate.subs(spectral_density, 0) == 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
