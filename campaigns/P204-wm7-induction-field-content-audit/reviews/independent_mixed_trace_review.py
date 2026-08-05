#!/usr/bin/env python3
"""Independent raw-SymPy review of WM7's mixed-statistics trace claims."""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P204-INDEPENDENT-MIXED-TRACE")
    own_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imported = {
        node.module
        for node in ast.walk(own_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    checks.check(
        "review imports no beta trace affine or charge API",
        imported.isdisjoint(
            {
                "substrate_framework.gauge_beta",
                "substrate_framework.charge_traces",
                "substrate_framework.vacuum_polarization",
                "substrate_framework.multiplet_charges",
            }
        ),
    )

    R = sp.Rational
    # (multiplicity, color dimension, isospin dimension, hypercharge)
    rows = (
        (3, 3, 2, R(1, 6)),
        (3, 3, 1, -R(2, 3)),
        (3, 3, 1, R(1, 3)),
        (3, 1, 2, -R(1, 2)),
        (3, 1, 1, R(1)),
    )
    weyl_u1 = sp.simplify(
        sum(m * color * iso * R(3, 5) * y**2 for m, color, iso, y in rows)
    )
    weyl_su2 = sp.simplify(
        sum(m * color * R(1, 2) for m, color, iso, _ in rows if iso == 2)
    )
    weyl_su3 = sp.simplify(
        sum(m * iso * R(1, 2) for m, color, iso, _ in rows if color == 3)
    )
    checks.check(
        "fresh supplied Weyl invariant sums are six in all coordinates",
        (weyl_u1, weyl_su2, weyl_su3) == (6, 6, 6),
    )
    scalar_raw = (R(3, 10), R(1, 2), R(0))
    checks.check(
        "fresh supplied scalar invariant sums are exact",
        scalar_raw == (R(3, 10), R(1, 2), 0),
    )
    c_f, c_s = sp.symbols("c_F c_S", real=True)
    design = sp.Matrix(
        [
            [weyl_u1, scalar_raw[0]],
            [weyl_su2, scalar_raw[1]],
            [weyl_su3, scalar_raw[2]],
        ]
    )
    weights = sp.Matrix([R(2, 3), R(1, 3)])
    target = design * weights
    checks.check(
        "fresh weighted matter vector is forty-one-tenths twenty-five-sixths four",
        tuple(target) == (R(41, 10), R(25, 6), 4),
    )
    checks.check(
        "fresh inverse solve recovers the already inserted weights",
        sp.linsolve((design, target), (c_f, c_s)) == {(R(2, 3), R(1, 3))},
    )
    checks.check(
        "fresh design has one consistency relation",
        design.rank() == 2
        and len(design.T.nullspace()) == 1
        and (design.T.nullspace()[0].T * target)[0] == 0,
    )
    checks.check(
        "fresh target mutation breaks consistency",
        design.row_join(target + sp.Matrix([1, 0, 0])).rank() == 3,
    )
    checks.check(
        "fresh no-scalar design cannot identify a scalar weight",
        sp.Matrix.hstack(design[:, 0], sp.zeros(3, 1)).rank() == 1,
    )

    n_h = sp.Symbol("N_H", real=True)
    family = (4 + n_h / 10, 4 + n_h / 6, sp.Integer(4))
    checks.check(
        "fresh scalar-count family is concurrent only at zero",
        sp.solve([family[0] - family[2], family[1] - family[2]], n_h) == {n_h: 0},
    )
    checks.check(
        "fresh one-scalar vector has integer ratio 123 125 120",
        tuple(sp.simplify(30 * value.subs(n_h, 1)) for value in family)
        == (123, 125, 120),
    )
    checks.check(
        "fresh one-scalar spread is twenty-five over twenty-four",
        max(value.subs(n_h, 1) for value in family)
        / min(value.subs(n_h, 1) for value in family)
        == R(25, 24),
    )
    checks.check(
        "fresh three-scalar counterfactual gives twenty-seven over seventy",
        sp.simplify(
            family[1].subs(n_h, 3)
            / (family[1].subs(n_h, 3) + R(5, 3) * family[0].subs(n_h, 3))
        )
        == R(27, 70),
    )

    s1, s2, s3 = (value.subs(n_h, 1) for value in family)
    common = sp.Symbol("C", positive=True)
    checks.check(
        "fresh common zero-boundary inverse law gives the source coupling ratio",
        sp.simplify((1 / (common * s1)) / (1 / (common * s2))) == R(125, 123),
    )
    checks.check(
        "fresh one-boundary mutation breaks the source ratio",
        sp.simplify((1 / (1 + common * s1)) / (1 / (common * s2)) - R(125, 123))
        != 0,
    )
    checks.check(
        "fresh independent-coefficient mutation breaks the source ratio",
        sp.simplify((1 / (2 * common * s1)) / (1 / (common * s2)))
        != R(125, 123),
    )
    trace_coordinate = sp.simplify(s2 / (s2 + R(5, 3) * s1))
    checks.check("fresh conditional trace coordinate is twenty-five over sixty-six", trace_coordinate == R(25, 66))
    checks.check(
        "fresh equal independent couplings refute automatic trace interpretation",
        R(1, 2) != trace_coordinate,
    )
    rho = sp.Symbol("rho", positive=True)
    moved_coordinate = sp.simplify(s2 / (s2 + R(5, 3) * rho**2 * s1))
    checks.check(
        "fresh Abelian coordinate mutation moves the raw trace coordinate",
        moved_coordinate.subs(rho, 1) == R(25, 66)
        and moved_coordinate.subs(rho, 2) != R(25, 66),
    )

    beta = (R(41, 10), -R(19, 6), -7)
    boundaries = (1, 4, 8)
    checks.check(
        "fresh positive boundary offsets defeat the negative-total inference",
        tuple(boundaries[index] + beta[index] for index in range(3))
        == (R(51, 10), R(5, 6), 1),
    )
    checks.check(
        "fresh scalar-hypercharge mutation changes only its Abelian contribution",
        R(1, 3) * 2 * R(3, 5) * R(1, 3) ** 2 != R(1, 10),
    )
    numpy_imports = [
        node
        for node in ast.walk(own_tree)
        if (
            isinstance(node, ast.Import)
            and any(alias.name == "numpy" for alias in node.names)
        )
        or (isinstance(node, ast.ImportFrom) and node.module == "numpy")
    ]
    checks.check("independent review has no NumPy compatibility surface", not numpy_imports)
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
