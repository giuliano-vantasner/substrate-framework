#!/usr/bin/env python3
"""Primary exact verifier for C-VOP-001 and the P198 MD3 disposition."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.bosonic_fock import truncated_bosonic_fock_ladder
from substrate_framework.coherent_states import (
    coherent_state_coefficient,
    coherent_state_intensity,
    coherent_state_ledger,
    coherent_state_number_modes,
    coherent_state_number_probability,
    coherent_state_overlap,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN_ROOT = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-38/"
    "bridge_MD3_vertex_operator_removes_the_single_vacuum_bound.py"
)
SOURCE_SHA256 = "2c50b4cacb8746a35f99c26d9f0edd0227314ab9410677aebc54c29812daf128"
RELEASE_SHA256 = "ac66e5ae6e46e878c6392892fb534a5fb7115dd6a2e50d59e2e4a429d8b82581"
FREEZE_SHA256 = "11fb7395aaf0a33389fbd51940eb67668ddc3427a106c2bae6d5157232db2d85"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P198-MD3-PRIMARY")
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("MD3 source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "immutable base release remains pinned",
        digest(ROOT / "governance/releases/v0.146.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned across proposal and campaign paths",
        digest(CAMPAIGN_ROOT / "evidence/formula-freeze.yaml") == FREEZE_SHA256,
    )

    call_sites = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    literal_sites = [
        node
        for node in call_sites
        if node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ]
    checks.check(
        "source inventory separates 20 sites from 41 executions",
        len(call_sites) == 20
        and len(literal_sites) == 13
        and len(call_sites) - len(literal_sites) == 7
        and sum(isinstance(node, ast.Assert) for node in ast.walk(source_tree)) == 0,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "MD3 has no NumPy quadrature compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    x, y = sp.symbols("x y", real=True)
    alpha = x + sp.I * y
    intensity = x**2 + y**2
    checks.check(
        "complex displacement intensity is exact",
        coherent_state_intensity(alpha) == intensity,
    )
    for order in range(6):
        expected = sp.exp(-intensity / 2) * alpha**order / sp.sqrt(
            sp.factorial(order)
        )
        checks.check(
            f"coherent coefficient order {order} has exact normalization",
            sp.simplify(
                coherent_state_coefficient(order, displacement=alpha) - expected
            )
            == 0,
        )

    numeric_alpha = 1 + 2 * sp.I
    for order in range(6):
        coefficient = coherent_state_coefficient(
            order,
            displacement=numeric_alpha,
        )
        probability = coherent_state_number_probability(
            order,
            displacement=numeric_alpha,
        )
        checks.check(
            f"Born probability order {order} is coefficient modulus square",
            sp.simplify(sp.conjugate(coefficient) * coefficient - probability) == 0,
        )

    S = sp.symbols("S", positive=True)
    n = sp.symbols("n", integer=True, nonnegative=True)
    raw_probability = sp.exp(-S) * S**n / sp.factorial(n)
    total = sp.summation(raw_probability, (n, 0, sp.oo))
    checks.check("number probabilities normalize exactly", sp.simplify(total - 1) == 0)

    generating = sp.exp(S * (sp.Symbol("t") - 1))
    t = next(iter(generating.free_symbols - {S}))
    mean = sp.diff(generating, t).subs(t, 1)
    second_falling = sp.diff(generating, t, 2).subs(t, 1)
    checks.check("coherent number mean is S", sp.simplify(mean - S) == 0)
    checks.check(
        "coherent number variance is S",
        sp.simplify(second_falling + mean - mean**2 - S) == 0,
    )

    for order in range(6):
        recurrence = sp.sqrt(order + 1) * coherent_state_coefficient(
            order + 1,
            displacement=numeric_alpha,
        ) - numeric_alpha * coherent_state_coefficient(
            order,
            displacement=numeric_alpha,
        )
        checks.check(
            f"annihilation eigenvector recurrence holds at order {order}",
            sp.simplify(recurrence) == 0,
        )

    checks.check(
        "coherent overlap has unit diagonal",
        sp.simplify(coherent_state_overlap(numeric_alpha, numeric_alpha) - 1) == 0,
    )
    checks.check(
        "vacuum overlap retains amplitude-probability distinction",
        coherent_state_overlap(0, numeric_alpha) == sp.exp(-sp.Rational(5, 2))
        and coherent_state_ledger(
            displacement=numeric_alpha
        ).vacuum_probability
        == sp.exp(-5),
    )
    checks.check(
        "zero displacement is the vacuum-only state",
        coherent_state_ledger(displacement=0).occupation_support == "vacuum_only"
        and coherent_state_number_probability(0, displacement=0) == 1
        and coherent_state_number_probability(1, displacement=0) == 0,
    )
    checks.check(
        "nonzero displacement has all nonnegative occupation support",
        coherent_state_ledger(
            displacement=sp.I / 2
        ).occupation_support
        == "all_nonnegative",
    )
    checks.check(
        "integer intensity retains both adjacent number modes",
        coherent_state_number_modes(displacement=3 + 4 * sp.I) == (24, 25),
    )
    checks.check(
        "arbitrarily large declared rational intensity has unbounded mode family",
        coherent_state_number_modes(displacement=10**6) == (10**12 - 1, 10**12),
    )

    gamma = sp.symbols("gamma", real=True)
    mutated_norm = sp.exp((1 - 2 * gamma) * S)
    checks.mutation_sensitive(
        "Gaussian half factor is load bearing",
        lambda candidate: sp.simplify(mutated_norm.subs(gamma, candidate) - 1) == 0,
        sp.Rational(1, 2),
        [0, 1],
    )
    wrong_current = (
        sp.sqrt(4)
        * sp.exp(-2)
        * sp.Integer(2) ** 4
        / sp.factorial(4)
    )
    wrong_previous = sp.Integer(2) * sp.exp(-2) * sp.Integer(2) ** 3 / sp.factorial(3)
    checks.check(
        "factorial instead of square-root factorial breaks eigenvector recurrence",
        sp.simplify(wrong_current - wrong_previous) != 0,
    )

    ladder = truncated_bosonic_fock_ladder(5)
    matrix_alpha = 1 + 2 * sp.I
    generator = (
        matrix_alpha * ladder.creation
        - sp.conjugate(matrix_alpha) * ladder.annihilation
    )
    wrong_generator = matrix_alpha * (
        ladder.creation - ladder.annihilation
    )
    checks.check(
        "conjugated Weyl generator is anti-Hermitian",
        sp.simplify(generator.H + generator) == sp.zeros(5),
    )
    checks.check(
        "erasing conjugation breaks anti-Hermiticity for complex displacement",
        sp.simplify(wrong_generator.H + wrong_generator) != sp.zeros(5),
    )

    lam = sp.symbols("lam", positive=True)
    source_ladder = truncated_bosonic_fock_ladder(12)
    A = sp.I * lam * source_ladder.creation
    B = sp.I * lam * source_ladder.annihilation
    commutator = sp.simplify(A * B - B * A)
    nested = sp.simplify(A * commutator - commutator * A)
    checks.check(
        "finite truncated commutator is not globally central",
        commutator != lam**2 * sp.eye(12),
    )
    checks.check(
        "finite truncated BCH has a nonzero edge nested commutator",
        nested != sp.zeros(12),
    )

    weight_function = next(
        node
        for node in source_tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "weight"
    )
    weight_names = {
        node.id for node in ast.walk(weight_function) if isinstance(node, ast.Name)
    }
    checks.check(
        "source weight check hard-codes normal-ordered coefficients rather than exponentiating phi",
        {"lam", "al"} <= weight_names
        and "phi" not in weight_names
        and "b" not in weight_names
        and "bd" not in weight_names,
    )

    phase = sp.symbols("phase", real=True)
    charge = sp.symbols("m", integer=True)
    multiplier = sp.exp(sp.I * charge * phase)
    checks.check(
        "compact multiplication vertex has unit pointwise modulus",
        sp.simplify(sp.conjugate(multiplier) * multiplier - 1) == 0,
    )
    checks.check(
        "compact multiplication vertex translates Fourier labels",
        sp.simplify(
            multiplier * sp.exp(sp.I * n * phase)
            - sp.exp(sp.I * (n + charge) * phase)
        )
        == 0,
    )
    checks.check(
        "periodicity is independent of coherent displacement intensity",
        sp.simplify(
            sp.exp(sp.I * (phase + 2 * sp.pi)) - sp.exp(sp.I * phase)
        )
        == 0
        and numeric_alpha not in multiplier.free_symbols,
    )

    probability_doc = " ".join(
        coherent_state_number_probability.__doc__.split()
    )
    ledger_doc = " ".join(coherent_state_ledger.__doc__.split())
    checks.check(
        "canonical probability semantics exclude material event probability",
        "not a probability that a material event" in probability_doc,
    )
    checks.check(
        "canonical support semantics exclude classical amplitude inference",
        "does not imply an unbounded classical excursion" in ledger_doc,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
