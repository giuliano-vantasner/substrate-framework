#!/usr/bin/env python3
"""Primary exact verifier for the WN4 factorial-one shape and tail audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.bosonic_fock import (
    factorial_one_falling_factorial_moment,
    factorial_one_geometric_point_bound,
    factorial_one_geometric_tail_bound,
    factorial_one_log_concavity_ratio,
    factorial_one_mass,
    factorial_one_modes,
    factorial_one_polynomial_tail_certificate,
    factorial_one_probability_generating_function,
    normalized_factorial_one_mass,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
PROPOSAL = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-37/"
    "bridge_WN4_derived_weight_and_crossover.py"
)
SOURCE_SHA256 = "2377bb4ba817cd20c188d4adeeeb9169253e9b1231477ac2069b36cc923fc7e2"
RELEASE_SHA256 = "f8ff33a61925f9e537f5a296aa7e674238399a22fc59e7eec7ec8520f4e3a852"
FORMULA_FREEZE_SHA256 = "6e486347ee07823b76057c36d0401df5bae1317fc362d684ffeb92ebfdc3caf9"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _raises_value_error(callback: object) -> bool:
    try:
        callback()  # type: ignore[operator]
    except ValueError:
        return True
    return False


def main() -> int:
    checks = CheckLedger("C-CMB-003")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.142.0.yaml") == RELEASE_SHA256,
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
        "source predicate inventory separates sites executions and assertions",
        len(source_checks) == 27
        and not any(isinstance(node, ast.Assert) for node in ast.walk(source_tree)),
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "immutable source has no NumPy compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "source overclaim edges remain explicit audit targets",
        all(
            token in source_text
            for token in (
                "SINGLE interior mode",
                "S is therefore the",
                "SIGN OF (S - n)",
                "power-law family n^k interpolates",
            )
        ),
    )

    intensity = sp.Symbol("S", positive=True)
    for order in range(1, 21):
        mass = lambda index: intensity**index / sp.factorial(index)
        raw_ratio = sp.combsimp(
            mass(order) ** 2 / (mass(order - 1) * mass(order + 1))
        )
        checks.check(
            f"order {order} has exact intensity-independent strict log-concavity",
            raw_ratio == factorial_one_log_concavity_ratio(order)
            and raw_ratio == sp.Rational(order + 1, order)
            and raw_ratio > 1,
        )
    expected_ratio = sp.Rational(6, 5)
    checks.mutation_sensitive(
        "log-concavity quotient uses one factorial and the correct neighbors",
        lambda candidate: sp.simplify(candidate - expected_ratio) == 0,
        factorial_one_log_concavity_ratio(5),
        (
            sp.Rational(36, 25),
            sp.Rational(5, 6),
            sp.Integer(1),
        ),
    )

    for integer in range(1, 13):
        masses = [
            factorial_one_mass(
                order,
                intensity=integer,
                support="all_nonnegative",
            )
            for order in range(0, integer + 8)
        ]
        maximum = max(masses)
        brute_modes = tuple(
            order for order, mass in enumerate(masses) if mass == maximum
        )
        checks.check(
            f"integer intensity {integer} preserves both adjacent exact modes",
            brute_modes == (integer - 1, integer)
            and factorial_one_modes(
                intensity=integer,
                support="all_nonnegative",
            )
            == brute_modes,
        )
    checks.check(
        "noninteger rational intensities have the unique floor mode",
        all(
            factorial_one_modes(
                intensity=value,
                support="all_nonnegative",
            )
            == (int(sp.floor(value)),)
            for value in (
                sp.Rational(1, 3),
                sp.Rational(5, 2),
                sp.Rational(25, 2),
                sp.Rational(101, 4),
            )
        ),
    )
    checks.mutation_sensitive(
        "mode predicate retains integer ties",
        lambda candidate: candidate == (24, 25),
        factorial_one_modes(intensity=25, support="all_nonnegative"),
        ((25,), (24,), (23, 24)),
    )

    variable = sp.Symbol("t", real=True)
    generating = factorial_one_probability_generating_function(
        intensity=intensity,
        variable=variable,
    )
    checks.check(
        "probability generating function has exact normalized exponential form",
        generating == sp.exp(intensity * (variable - 1))
        and generating.subs(variable, 1) == 1,
    )
    for order in range(10):
        coefficient = sp.simplify(
            sp.diff(generating, variable, order).subs(variable, 0)
            / sp.factorial(order)
        )
        checks.check(
            f"PGF coefficient {order} equals the canonical normalized mass",
            sp.simplify(
                coefficient
                - normalized_factorial_one_mass(
                    order,
                    intensity=intensity,
                    support="all_nonnegative",
                )
            )
            == 0,
        )
    checks.mutation_sensitive(
        "PGF sign shift and normalization",
        lambda candidate: sp.simplify(candidate - generating) == 0,
        sp.exp(intensity * (variable - 1)),
        (
            sp.exp(intensity * (variable + 1)),
            sp.exp(intensity * variable),
            sp.exp(-intensity * (variable - 1)),
        ),
    )

    for order in range(10):
        direct = sp.diff(generating, variable, order).subs(variable, 1)
        checks.check(
            f"falling-factorial moment {order} is the PGF derivative S^{order}",
            direct
            == factorial_one_falling_factorial_moment(
                order,
                intensity=intensity,
            )
            == intensity**order,
        )
    mean = factorial_one_falling_factorial_moment(1, intensity=intensity)
    second_falling = factorial_one_falling_factorial_moment(
        2,
        intensity=intensity,
    )
    checks.check(
        "mean and variance are S on the mathematical sample space",
        mean == intensity
        and second_falling == intensity**2
        and sp.simplify(second_falling + mean - mean**2) == intensity,
    )
    checks.mutation_sensitive(
        "second moment conversion distinguishes falling raw and variance",
        lambda candidate: candidate
        == (intensity**2, intensity**2 + intensity, intensity),
        (second_falling, second_falling + mean, second_falling + mean - mean**2),
        (
            (intensity**2 + intensity, intensity**2 + intensity, intensity),
            (intensity**2, intensity**2, 0),
            (intensity**2, intensity**2 + intensity, intensity**2),
        ),
    )

    sample_intensity = sp.Integer(5)
    alpha = sp.log(2)
    start = 9
    initial = normalized_factorial_one_mass(
        start,
        intensity=sample_intensity,
        support="all_nonnegative",
    )
    for steps in range(12):
        actual = normalized_factorial_one_mass(
            start + steps,
            intensity=sample_intensity,
            support="all_nonnegative",
        )
        bound = factorial_one_geometric_point_bound(
            steps,
            intensity=sample_intensity,
            alpha=alpha,
            starting_order=start,
        )
        checks.check(
            f"geometric point bound holds exactly at step {steps}",
            sp.simplify(bound - initial / 2**steps) == 0
            and sp.simplify(actual / initial) <= sp.Rational(1, 2**steps),
        )
    later = sp.Symbol("j", integer=True, nonnegative=True)
    checks.check(
        "every later ratio is bounded by one half from the exact threshold",
        sp.simplify(
            sp.Rational(1, 2)
            - sample_intensity / (start + 1 + later)
            - later / (2 * (later + 10))
        )
        == 0
        and (later / (2 * (later + 10))).is_nonnegative is True,
    )
    tail_bound = factorial_one_geometric_tail_bound(
        intensity=sample_intensity,
        alpha=alpha,
        starting_order=start,
    )
    checks.check(
        "strict upper-tail bound is the summed exact geometric majorant",
        sp.simplify(tail_bound - initial) == 0
        and sp.summation(initial / 2**later, (later, 1, sp.oo)) == initial,
    )
    checks.check(
        "one-step-earlier threshold mutation is rejected",
        _raises_value_error(
            lambda: factorial_one_geometric_tail_bound(
                intensity=sample_intensity,
                alpha=alpha,
                starting_order=start - 1,
            )
        ),
    )
    point_baseline = factorial_one_geometric_point_bound(
        4,
        intensity=sample_intensity,
        alpha=alpha,
        starting_order=start,
    )
    checks.mutation_sensitive(
        "geometric point exponent and starting mass",
        lambda candidate: sp.simplify(candidate - point_baseline) == 0,
        initial / 2**4,
        (initial / 2**3, initial / 2**5, 2 * initial / 2**4),
    )

    for power in range(7):
        certificate = factorial_one_polynomial_tail_certificate(
            power,
            intensity=sp.Rational(3, 2),
            contraction=sp.Rational(1, 3),
        )
        exact_ratio = sp.simplify(
            sp.Rational(3, 2)
            / (certificate.starting_order + 1)
            * sp.Rational(
                certificate.starting_order + 1,
                certificate.starting_order,
            )
            ** power
        )
        conservative = (
            sp.Rational(3, 2)
            * 2**power
            / (certificate.starting_order + 1)
        )
        checks.check(
            f"power {power} certificate has an exact eventual contraction",
            certificate.starting_order >= 1
            and certificate.starting_order + 1 >= certificate.threshold
            and exact_ratio <= conservative <= certificate.contraction
            and certificate.scaled_mass_tends_to_zero,
        )
    certificate = factorial_one_polynomial_tail_certificate(
        4,
        intensity=sp.Rational(3, 2),
        contraction=sp.Rational(1, 3),
    )
    checks.mutation_sensitive(
        "polynomial-tail threshold retains intensity power and contraction",
        lambda candidate: candidate == (sp.Integer(72), 71, sp.Rational(1, 3)),
        (certificate.threshold, certificate.starting_order, certificate.contraction),
        (
            (sp.Integer(36), 35, sp.Rational(1, 3)),
            (sp.Integer(24), 23, sp.Rational(1, 3)),
            (sp.Integer(72), 71, sp.Rational(1, 2)),
        ),
    )

    coupling, spectral_density = sp.symbols("g rho", real=True)
    mathematical_mass = normalized_factorial_one_mass(
        4,
        intensity=sample_intensity,
        support="all_nonnegative",
    )
    putative_rate = coupling**2 * spectral_density * mathematical_mass
    checks.check(
        "zero coupling and zero spectral density block a physical rate reading",
        mathematical_mass > 0
        and putative_rate.subs(coupling, 0) == 0
        and putative_rate.subs(spectral_density, 0) == 0,
    )
    checks.check(
        "mathematical distribution and tail APIs state their physical ceilings",
        "does not assert a physical Poisson process"
        in " ".join(factorial_one_probability_generating_function.__doc__.split())
        and "mathematical mass only"
        in " ".join(factorial_one_geometric_point_bound.__doc__.split())
        and certificate.physical_power_law_interpretation_is_separate_premise
        is True,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
