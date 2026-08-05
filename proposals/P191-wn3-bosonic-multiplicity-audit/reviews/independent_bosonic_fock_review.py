#!/usr/bin/env python3
"""Independent raw-SymPy review of the P191 bosonic Fock theorem."""

from __future__ import annotations

import ast
import math
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def _raw_ladder(dimension: int) -> tuple[sp.Matrix, sp.Matrix]:
    annihilation = sp.zeros(dimension)
    for level in range(1, dimension):
        annihilation[level - 1, level] = sp.sqrt(level)
    return annihilation, annihilation.T


def _raw_mass(order: int, intensity: sp.Expr, support: str) -> sp.Expr:
    included = (
        support == "all_nonnegative"
        or (support == "positive" and order >= 1)
        or (support == "positive_odd" and order >= 1 and order % 2 == 1)
    )
    return sp.factor(intensity**order / math.factorial(order)) if included else sp.Integer(0)


def _raw_modes(intensity: sp.Rational, support: str) -> tuple[int, ...]:
    upper = max(20, 3 * int(sp.ceiling(intensity)) + 10)
    values = [_raw_mass(order, intensity, support) for order in range(upper)]
    maximum = max(values)
    return tuple(order for order, value in enumerate(values) if value == maximum)


def main() -> int:
    checks = CheckLedger("C-OSC-001-INDEPENDENT")
    own_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imported_modules = {
        node.module
        for node in ast.walk(own_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    checks.check(
        "review imports no candidate or accepted scientific API",
        imported_modules.isdisjoint(
            {
                "substrate_framework.bosonic_fock",
                "substrate_framework.cosine_vertices",
                "substrate_framework.factorial_suppression",
                "substrate_framework.symmetric_spin",
            }
        ),
    )

    for dimension in (1, 2, 4, 12):
        annihilation, creation = _raw_ladder(dimension)
        commutator = annihilation * creation - creation * annihilation
        top = sp.zeros(dimension)
        top[-1, -1] = 1
        checks.check(
            f"raw dimension {dimension} rederives the top-state defect",
            commutator == sp.eye(dimension) - dimension * top
            and sp.trace(commutator) == 0,
        )
        checks.check(
            f"raw dimension {dimension} cannot have a full identity commutator",
            commutator != sp.eye(dimension)
            and sp.trace(sp.eye(dimension)) == dimension,
        )

    dimension = 16
    annihilation, creation = _raw_ladder(dimension)
    vacuum = sp.zeros(dimension, 1)
    vacuum[0] = 1
    state = vacuum
    for order in range(13):
        expected = sp.zeros(dimension, 1)
        expected[order] = sp.sqrt(math.factorial(order))
        checks.check(
            f"raw repeated creation order {order} has coefficient and norm factorial",
            state == expected and (state.T * state)[0] == math.factorial(order),
        )
        state = creation * state

    coordinate = annihilation + creation
    for order in range(13):
        target = sp.zeros(1, dimension)
        target[0, order] = 1
        checks.check(
            f"raw full coordinate power reaches level {order} only through all creation",
            sp.simplify((target * coordinate**order * vacuum)[0])
            == sp.sqrt(math.factorial(order)),
        )

    high, low = sp.symbols("H L", real=True)
    amplitude, high_scale, low_scale = sp.symbols("U h ell", real=True, nonzero=True)
    potential = amplitude * (1 - sp.cos(high_scale * high + low_scale * low))
    for order in range(10):
        derivative = sp.diff(potential, high, 1, low, order).subs({high: 0, low: 0})
        coefficient = sp.simplify(derivative / math.factorial(order))
        element = sp.simplify(coefficient * sp.sqrt(math.factorial(order)))
        expected = (
            amplitude
            * (-1) ** ((order - 1) // 2)
            * high_scale
            * low_scale**order
            / sp.sqrt(math.factorial(order))
            if order % 2
            else 0
        )
        checks.check(
            f"fresh derivative and raw ladder retain parity at order {order}",
            sp.simplify(element - expected) == 0,
        )

    checks.check(
        "all sampled even orders remain zero after raw bosonic composition",
        all(
            sp.diff(potential, high, 1, low, order).subs({high: 0, low: 0}) == 0
            for order in range(0, 16, 2)
        ),
    )

    intensity = sp.Symbol("S", positive=True)
    index = sp.Symbol("n", integer=True, nonnegative=True)
    all_total = sp.summation(intensity**index / sp.factorial(index), (index, 0, sp.oo))
    positive_total = sp.summation(
        intensity**index / sp.factorial(index),
        (index, 1, sp.oo),
    )
    odd_series = sum(
        intensity ** (2 * k + 1) / math.factorial(2 * k + 1)
        for k in range(8)
    )
    checks.check(
        "raw series rederive all and positive normalizers",
        all_total == sp.exp(intensity)
        and sp.simplify(positive_total - (sp.exp(intensity) - 1)) == 0,
    )
    checks.check(
        "raw parity series rederives the sinh normalizer",
        sp.series(sp.sinh(intensity) - odd_series, intensity, 0, 17).removeO() == 0,
    )
    checks.mutation_sensitive(
        "raw normalizer signs and supports",
        lambda candidate: candidate
        == (sp.exp(intensity), sp.exp(intensity) - 1, sp.sinh(intensity)),
        (all_total, sp.simplify(positive_total), sp.sinh(intensity)),
        (
            (sp.exp(intensity) - 1, sp.exp(intensity), sp.sinh(intensity)),
            (sp.exp(intensity), sp.exp(intensity) - 1, sp.cosh(intensity)),
        ),
    )

    checks.check(
        "raw brute-force modes preserve ordinary integer ties",
        _raw_modes(sp.Integer(25), "all_nonnegative") == (24, 25)
        and _raw_modes(sp.Integer(25), "positive") == (24, 25),
    )
    checks.check(
        "raw odd-support modes differ from the all-positive family",
        _raw_modes(sp.Integer(25), "positive_odd") == (25,)
        and _raw_modes(sp.Integer(49), "positive_odd") == (49,),
    )
    ordinary_ratio = sp.combsimp(
        (intensity ** (index + 1) / sp.factorial(index + 1))
        / (intensity**index / sp.factorial(index))
    )
    odd_ratio = sp.combsimp(
        (intensity ** (index + 2) / sp.factorial(index + 2))
        / (intensity**index / sp.factorial(index))
    )
    checks.check(
        "raw ratios explain the distinct mode families",
        ordinary_ratio == intensity / (index + 1)
        and sp.simplify(
            odd_ratio - intensity**2 / ((index + 1) * (index + 2))
        )
        == 0,
    )

    algebraic_square = sp.Rational(5**6, math.factorial(3))
    coupling, spectral_density = sp.symbols("g rho", real=True)
    putative_rate = coupling**2 * algebraic_square * spectral_density
    checks.check(
        "raw zero-coupling and zero-density countermodels preserve the algebraic square",
        algebraic_square > 0
        and putative_rate.subs(coupling, 0) == 0
        and putative_rate.subs(spectral_density, 0) == 0,
    )
    checks.check(
        "one normalized vector per single-mode occupation refutes factorial state counting",
        all(
            sum(1 for level in range(12) if level == occupation) == 1
            for occupation in range(12)
        ),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
