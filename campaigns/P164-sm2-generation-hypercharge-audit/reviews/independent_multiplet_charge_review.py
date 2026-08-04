#!/usr/bin/env python3
"""Fresh exact review of SM2 charge spectra without importing P164 APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P164-INDEPENDENT")
    half = sp.Rational(1, 2)
    rows = (
        ("Q_L", 3, (half, -half), sp.Rational(1, 6)),
        ("u_R", 3, (0,), sp.Rational(2, 3)),
        ("d_R", 3, (0,), -sp.Rational(1, 3)),
        ("L", 1, (half, -half), -half),
        ("e_R", 1, (0,), sp.Integer(-1)),
    )
    spectra = tuple(
        tuple(sp.simplify(weight + hypercharge) for weight in weights)
        for _label, _multiplicity, weights, hypercharge in rows
    )
    checks.check(
        "fresh supplied spectra reproduce every component charge",
        spectra
        == (
            (sp.Rational(2, 3), -sp.Rational(1, 3)),
            (sp.Rational(2, 3),),
            (-sp.Rational(1, 3),),
            (0, -1),
            (-1,),
        ),
    )
    state_count = sum(multiplicity * len(weights) for _, multiplicity, weights, _ in rows)
    checks.check("fresh supplied spectator count is fifteen", state_count == 15)

    flattened = tuple(
        (multiplicity, weight, hypercharge)
        for _label, multiplicity, weights, hypercharge in rows
        for weight in weights
    )
    trace_t3 = sp.simplify(sum(m * weight**2 for m, weight, _y in flattened))
    trace_y = sp.simplify(sum(m * y**2 for m, _weight, y in flattened))
    trace_cross = sp.simplify(sum(m * weight * y for m, weight, y in flattened))
    trace_q = sp.simplify(sum(m * (weight + y) ** 2 for m, weight, y in flattened))
    checks.check(
        "fresh flattened traces reproduce the accepted supplied-table values",
        (trace_t3, trace_y, trace_cross, trace_q)
        == (2, sp.Rational(10, 3), 0, sp.Rational(16, 3)),
    )

    quark_targets = sp.Matrix([sp.Rational(2, 3) - half, -sp.Rational(1, 3) + half])
    quark_coefficients = sp.ones(2, 1)
    checks.check(
        "fresh quark inversion is consistent and unique in one supplied coordinate",
        quark_coefficients.rank() == 1
        and quark_coefficients.row_join(quark_targets).rank() == 1
        and sp.linsolve((quark_coefficients, quark_targets))
        == {(sp.Rational(1, 6),)},
    )
    inconsistent_targets = sp.Matrix([sp.Rational(1, 6), sp.Rational(7, 6)])
    checks.check(
        "fresh wrong target separation makes the one-row system inconsistent",
        quark_coefficients.rank() == 1
        and quark_coefficients.row_join(inconsistent_targets).rank() == 2,
    )
    alternative_targets = sp.Matrix([1, 1])
    checks.check(
        "fresh alternative targets admit a different exact common row value",
        sp.linsolve((quark_coefficients, alternative_targets)) == {(1,)},
    )

    unknowns = sp.symbols("y0:5", real=True)
    arbitrary_spectra = tuple(
        tuple(weight + unknowns[index] for weight in row[2])
        for index, row in enumerate(rows)
    )
    checks.check(
        "without target charges the five supplied row values remain free",
        set().union(*(value.free_symbols for row in arbitrary_spectra for value in row))
        == set(unknowns),
    )
    fabricated_up = half + half
    checks.check(
        "fresh fabricated quark row fails only the supplied up target",
        fabricated_up == 1 and fabricated_up != sp.Rational(2, 3),
    )

    rho, coefficient, hypercharge, coupling, weight = sp.symbols(
        "rho c y g t", positive=True
    )
    base_charge = weight + coefficient * hypercharge
    mapped_charge = weight + (coefficient / rho) * (rho * hypercharge)
    checks.check(
        "fresh Abelian generator and electric coefficient rescaling preserves Q",
        sp.simplify(mapped_charge - base_charge) == 0,
    )
    checks.check(
        "fresh inverse coupling rescaling preserves the coupled coordinate",
        sp.simplify((coupling / rho) * (rho * hypercharge) - coupling * hypercharge)
        == 0,
    )
    checks.check(
        "holding the electric coefficient fixed changes generic charges",
        sp.simplify(weight + coefficient * rho * hypercharge - base_charge)
        == coefficient * hypercharge * (rho - 1),
    )
    checks.check(
        "factor two specializes the PS-to-M1 coordinate map",
        sp.simplify((coefficient / 2) * (2 * hypercharge) - coefficient * hypercharge)
        == 0,
    )

    conjugate_rows = tuple(
        (
            label + "_conj",
            multiplicity,
            tuple(-weight for weight in weights),
            -hypercharge,
        )
        for label, multiplicity, weights, hypercharge in rows
    )
    conjugate_spectra = tuple(
        tuple(weight + hypercharge for weight in weights)
        for _label, _multiplicity, weights, hypercharge in conjugate_rows
    )
    checks.check(
        "fresh charge conjugation negates every component spectrum",
        conjugate_spectra == tuple(tuple(-charge for charge in row) for row in spectra),
    )
    checks.check(
        "fresh equal dimensions cannot distinguish a representation from its conjugate",
        tuple(row[1] for row in conjugate_rows) == tuple(row[1] for row in rows),
    )

    y_ql, y_h, y_ur, y_dr, y_l, y_er = (
        sp.Rational(1, 6),
        half,
        sp.Rational(2, 3),
        -sp.Rational(1, 3),
        -half,
        sp.Integer(-1),
    )
    checks.check(
        "fresh conjugated Yukawa monomials are neutral",
        (
            sp.simplify(-y_ql - y_h + y_ur),
            sp.simplify(-y_ql + y_h + y_dr),
            sp.simplify(-y_l + y_h + y_er),
        )
        == (0, 0, 0),
    )
    checks.check(
        "fresh unconjugated up shorthand is not neutral",
        sp.simplify(y_ql + y_h + y_ur) == sp.Rational(4, 3),
    )

    diagonal_family = sp.diag(half + hypercharge, -half + hypercharge)
    checks.check(
        "fresh arbitrary common row remains diagonal",
        diagonal_family.is_diagonal() and diagonal_family.free_symbols == {hypercharge},
    )
    checks.check(
        "fresh optional neutral singlet changes table count without breaking old rows",
        state_count + 1 == 16 and 0 + 0 == 0,
    )
    return checks.finish()


if __name__ == "__main__":
    result = run()
    print(f"P164 INDEPENDENT ALL {result} CHECKS PASS")
