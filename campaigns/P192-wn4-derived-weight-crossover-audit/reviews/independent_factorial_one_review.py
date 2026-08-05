#!/usr/bin/env python3
"""Independent raw-SymPy rederivation for the P192 claim candidate."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
PROPOSAL = Path(__file__).resolve().parents[1]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-37/"
    "bridge_WN4_derived_weight_and_crossover.py"
)
SOURCE_SHA256 = "2377bb4ba817cd20c188d4adeeeb9169253e9b1231477ac2069b36cc923fc7e2"
RELEASE_SHA256 = "f8ff33a61925f9e537f5a296aa7e674238399a22fc59e7eec7ec8520f4e3a852"
FORMULA_FREEZE_SHA256 = "6e486347ee07823b76057c36d0401df5bae1317fc362d684ffeb92ebfdc3caf9"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _mass(order: int | sp.Expr, intensity: sp.Expr) -> sp.Expr:
    return intensity**order / sp.factorial(order)


def _normalized(order: int | sp.Expr, intensity: sp.Expr) -> sp.Expr:
    return sp.exp(-intensity) * _mass(order, intensity)


def main() -> int:
    checks = CheckLedger("C-CMB-003-INDEPENDENT")
    checks.check("source hash is independently pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release is independently pinned",
        _digest(ROOT / "governance/releases/v0.142.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze is independently pinned",
        _digest(PROPOSAL / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )

    intensity = sp.Symbol("S", positive=True)
    order = sp.Symbol("n", integer=True, positive=True)
    ratio = sp.combsimp(
        _mass(order, intensity) ** 2
        / (_mass(order - 1, intensity) * _mass(order + 1, intensity))
    )
    checks.check(
        "raw neighboring coefficients give the exact log-concavity quotient",
        ratio == (order + 1) / order,
    )
    checks.check(
        "the quotient is strictly above one on the full positive integer domain",
        sp.simplify(ratio - 1) == 1 / order and order.is_positive is True,
    )
    wrong_ratio = sp.combsimp(
        (_mass(order, intensity) / sp.factorial(order)) ** 2
        / (
            (_mass(order - 1, intensity) / sp.factorial(order - 1))
            * (_mass(order + 1, intensity) / sp.factorial(order + 1))
        )
    )
    checks.check(
        "a squared-factorial mutation changes the load-bearing quotient",
        sp.simplify(wrong_ratio - ratio) != 0,
    )

    for value in (1, 2, 4, 9, 25):
        masses = [_mass(index, sp.Integer(value)) for index in range(value + 7)]
        maximum = max(masses)
        modes = tuple(index for index, mass in enumerate(masses) if mass == maximum)
        checks.check(
            f"raw integer intensity {value} has the adjacent pair not one mode",
            modes == (value - 1, value)
            and masses[value - 1] == masses[value],
        )
    for value in (sp.Rational(1, 2), sp.Rational(5, 2), sp.Rational(25, 2)):
        upper = int(sp.ceiling(value)) + 7
        masses = [_mass(index, value) for index in range(upper)]
        maximum = max(masses)
        modes = tuple(index for index, mass in enumerate(masses) if mass == maximum)
        checks.check(
            f"raw noninteger intensity {value} has its unique floor mode",
            modes == (int(sp.floor(value)),),
        )

    variable = sp.Symbol("t", real=True)
    index = sp.Symbol("j", integer=True, nonnegative=True)
    raw_series = sp.summation(
        sp.exp(-intensity) * (intensity * variable) ** index / sp.factorial(index),
        (index, 0, sp.oo),
    )
    checks.check(
        "raw exponential series gives the normalized PGF",
        sp.simplify(raw_series - sp.exp(intensity * (variable - 1))) == 0,
    )
    checks.check("raw PGF is normalized at one", raw_series.subs(variable, 1) == 1)
    for moment_order in range(8):
        derivative = sp.diff(raw_series, variable, moment_order).subs(variable, 1)
        checks.check(
            f"raw PGF derivative {moment_order} gives S^{moment_order}",
            sp.simplify(derivative - intensity**moment_order) == 0,
        )
    mean = sp.diff(raw_series, variable).subs(variable, 1)
    second_falling = sp.diff(raw_series, variable, 2).subs(variable, 1)
    checks.check(
        "independent raw-moment conversion gives variance S",
        sp.simplify(second_falling + mean - mean**2 - intensity) == 0,
    )

    sample_intensity = sp.Integer(5)
    start = 9
    initial = _normalized(start, sample_intensity)
    for steps in range(10):
        actual = _normalized(start + steps, sample_intensity)
        checks.check(
            f"raw coefficient ratio obeys the half-geometric bound at step {steps}",
            sp.simplify(actual / initial) <= sp.Rational(1, 2**steps),
        )
    offset = sp.Symbol("k", integer=True, nonnegative=True)
    later_ratio = sp.simplify(
        _normalized(start + offset + 1, sample_intensity)
        / _normalized(start + offset, sample_intensity)
    )
    checks.check(
        "the raw later ratio is universally at most one half",
        later_ratio == 5 / (offset + 10)
        and sp.simplify(
            sp.Rational(1, 2)
            - later_ratio
            - offset / (2 * (offset + 10))
        )
        == 0
        and (offset / (2 * (offset + 10))).is_nonnegative is True,
    )
    checks.check(
        "independent geometric summation gives the strict upper-tail majorant",
        sp.summation(initial / 2**offset, (offset, 1, sp.oo)) == initial,
    )
    wrong_start_ratio = sp.simplify(
        _normalized(start, sample_intensity)
        / _normalized(start - 1, sample_intensity)
    )
    checks.check(
        "one-step-earlier threshold mutation exceeds one half",
        wrong_start_ratio == sp.Rational(5, 9) > sp.Rational(1, 2),
    )

    for power in range(7):
        contraction = sp.Rational(1, 3)
        threshold = sp.Rational(3, 2) * 2**power / contraction
        starting_order = max(1, int(sp.ceiling(threshold)) - 1)
        exact_scaled_ratio = sp.simplify(
            sp.Rational(3, 2)
            / (starting_order + 1)
            * sp.Rational(starting_order + 1, starting_order) ** power
        )
        checks.check(
            f"raw scaled-mass ratio for power {power} contracts beyond its threshold",
            starting_order + 1 >= threshold
            and exact_scaled_ratio
            <= sp.Rational(3, 2) * 2**power / (starting_order + 1)
            <= contraction,
        )

    coupling, spectral_density = sp.symbols("g rho", real=True)
    raw_probability = _normalized(4, sample_intensity)
    putative_rate = coupling**2 * spectral_density * raw_probability
    checks.check(
        "independent zero-premise probes block a physical-rate inference",
        raw_probability > 0
        and putative_rate.subs(coupling, 0) == 0
        and putative_rate.subs(spectral_density, 0) == 0,
    )
    checks.check(
        "exact adjacent-step residual is S minus n plus one",
        sp.simplify(
            sp.combsimp(
                _mass(index + 1, intensity) / _mass(index, intensity) - 1
            )
            - (intensity - index - 1) / (index + 1)
        )
        == 0,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
