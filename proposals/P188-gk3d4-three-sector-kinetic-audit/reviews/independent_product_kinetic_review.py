#!/usr/bin/env python3
"""Independent raw-SymPy review of GK3D4's product-sector claims."""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def _metric(generators: tuple[sp.MatrixBase, ...]) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(
        len(generators),
        len(generators),
        lambda first, second: sp.simplify(
            sp.trace(generators[first] * generators[second])
        ),
    )


def _raw_generators() -> tuple[
    tuple[sp.ImmutableMatrix, ...], tuple[sp.ImmutableMatrix, ...]
]:
    pauli = (
        sp.ImmutableMatrix([[0, 1], [1, 0]]) / 2,
        sp.ImmutableMatrix([[0, -sp.I], [sp.I, 0]]) / 2,
        sp.ImmutableMatrix([[1, 0], [0, -1]]) / 2,
    )
    gell_mann = (
        sp.ImmutableMatrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]) / 2,
        sp.ImmutableMatrix([[0, -sp.I, 0], [sp.I, 0, 0], [0, 0, 0]]) / 2,
        sp.ImmutableMatrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]]) / 2,
        sp.ImmutableMatrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]) / 2,
        sp.ImmutableMatrix([[0, 0, -sp.I], [0, 0, 0], [sp.I, 0, 0]]) / 2,
        sp.ImmutableMatrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]) / 2,
        sp.ImmutableMatrix([[0, 0, 0], [0, 0, -sp.I], [0, sp.I, 0]]) / 2,
        sp.ImmutableMatrix([[1, 0, 0], [0, 1, 0], [0, 0, -2]])
        / (2 * sp.sqrt(3)),
    )
    return pauli, gell_mann


def main() -> int:
    checks = CheckLedger("P188-INDEPENDENT-PRODUCT-KINETIC")
    own_text = Path(__file__).read_text(encoding="utf-8")
    own_tree = ast.parse(own_text)
    imported = {
        node.module
        for node in ast.walk(own_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    checks.check(
        "review imports no product loop trace or affine claim API",
        imported.isdisjoint(
            {
                "substrate_framework.product_gauge",
                "substrate_framework.gauge_beta",
                "substrate_framework.vacuum_polarization",
                "substrate_framework.kinetic_scale_matching",
                "substrate_framework.charge_traces",
                "substrate_framework.chiral_anomalies",
            }
        ),
    )

    weak_raw, color_raw = _raw_generators()
    checks.check(
        "fresh fundamental metrics are separately one half",
        _metric(weak_raw) == sp.eye(3) / 2
        and _metric(color_raw) == sp.eye(8) / 2,
    )
    identity_two = sp.eye(2)
    identity_three = sp.eye(3)
    color = tuple(
        sp.ImmutableMatrix(sp.kronecker_product(generator, identity_two))
        for generator in color_raw
    )
    weak = tuple(
        sp.ImmutableMatrix(sp.kronecker_product(identity_three, generator))
        for generator in weak_raw
    )
    y = sp.Symbol("y", positive=True)
    abelian = sp.ImmutableMatrix(y * sp.eye(6))
    checks.check(
        "fresh full-carrier metrics include spectator dimensions",
        _metric(color) == sp.eye(8)
        and _metric(weak) == sp.Rational(3, 2) * sp.eye(3)
        and sp.trace(abelian**2) == 6 * y**2,
    )
    checks.check(
        "fresh product cross blocks vanish",
        all(sp.trace(first * second) == 0 for first in color for second in weak)
        and all(sp.trace(first * abelian) == 0 for first in color)
        and all(sp.trace(first * abelian) == 0 for first in weak),
    )
    checks.check(
        "spectator degeneracy refutes equality of full non-Abelian weights",
        _metric(color)[0, 0] == 1
        and _metric(weak)[0, 0] == sp.Rational(3, 2)
        and _metric(color)[0, 0] != _metric(weak)[0, 0],
    )

    indices = (6 * y**2, sp.Rational(3, 2), sp.Integer(1))
    dirac_weights = tuple(sp.simplify(sp.Rational(4, 3) * value) for value in indices)
    weyl_weights = tuple(sp.simplify(sp.Rational(2, 3) * value) for value in indices)
    scalar_weights = tuple(sp.simplify(sp.Rational(1, 3) * value) for value in indices)
    checks.check(
        "fresh statistics ledger separates Dirac Weyl and scalar weights",
        dirac_weights == tuple(2 * value for value in weyl_weights)
        and scalar_weights == tuple(value / 4 for value in dirac_weights),
    )
    checks.check(
        "raw-index substitution changes every product-carrier Dirac weight",
        dirac_weights
        != tuple(
            sp.Rational(4, 3) * value
            for value in (y**2, sp.Rational(1, 2), sp.Rational(1, 2))
        ),
    )
    checks.check(
        "representation mutation changes a selected sector without changing labels",
        (dirac_weights[0], dirac_weights[1], sp.Integer(0)) != dirac_weights,
    )

    bi, bj = sp.symbols("b_i b_j", positive=True)
    zi, zj = sp.symbols("z_i z_j", real=True)
    li, lj = sp.symbols("L_i L_j", real=True)
    loop_denominator = 8 * sp.pi**2
    kinetic_i = zi + bi * li / loop_denominator
    kinetic_j = zj + bj * lj / loop_denominator
    ratio_condition = sp.simplify(bi * kinetic_j - bj * kinetic_i)
    expected_condition = sp.simplify(
        bi * zj - bj * zi + bi * bj * (lj - li) / loop_denominator
    )
    checks.check(
        "fresh affine ratio residual retains boundaries and logarithms",
        sp.simplify(ratio_condition - expected_condition) == 0
        and ratio_condition.has(zi, zj, li, lj),
    )
    common_log = sp.Symbol("L", positive=True)
    source_i = bi * common_log / loop_denominator
    source_j = bj * common_log / loop_denominator
    checks.check(
        "fresh zero-common-log branch gives the inverse-weight ratio",
        sp.simplify((1 / source_i) / (1 / source_j) - bj / bi) == 0,
    )
    checks.check(
        "fresh boundary mutation breaks that ratio without changing weights",
        sp.simplify(bi * (source_j + 1) - bj * source_i) == bi,
    )
    checks.check(
        "fresh log mutation breaks that ratio without changing boundaries",
        sp.simplify(
            bi * (bj * (common_log + 1) / loop_denominator)
            - bj * source_i
        )
        == bi * bj / loop_denominator,
    )
    beta0, beta_squared = sp.symbols("b0 beta2", positive=True)
    matched_i = zi + bi / (beta0 * beta_squared)
    matched_j = zj + bj / (beta0 * beta_squared)
    checks.check(
        "fresh scale-matched family still retains both boundaries",
        matched_i.has(zi) and matched_j.has(zj) and zi != zj,
    )
    checks.check(
        "fresh scale-matched zero branch gives only a conditional ratio",
        sp.simplify(
            (1 / (bi / (beta0 * beta_squared)))
            / (1 / (bj / (beta0 * beta_squared)))
            - bj / bi
        )
        == 0,
    )

    states = (
        (3, sp.Rational(1, 2), sp.Rational(1, 6)),
        (3, -sp.Rational(1, 2), sp.Rational(1, 6)),
        (3, 0, -sp.Rational(2, 3)),
        (3, 0, sp.Rational(1, 3)),
        (1, sp.Rational(1, 2), -sp.Rational(1, 2)),
        (1, -sp.Rational(1, 2), -sp.Rational(1, 2)),
        (1, 0, 1),
    )
    trace_2 = sp.simplify(sum(multiplicity * t3**2 for multiplicity, t3, _ in states))
    trace_y = sp.simplify(sum(multiplicity * charge**2 for multiplicity, _, charge in states))
    trace_cross = sp.simplify(
        sum(multiplicity * t3 * charge for multiplicity, t3, charge in states)
    )
    checks.check(
        "fresh supplied table has exact traces two and ten-thirds",
        trace_2 == 2 and trace_y == sp.Rational(10, 3) and trace_cross == 0,
    )
    trace_angle = sp.simplify(trace_2 / (trace_2 + trace_y))
    checks.check("fresh supplied trace coordinate is three-eighths", trace_angle == sp.Rational(3, 8))
    coupling_2, coupling_y = sp.symbols("g_2 g_Y", positive=True)
    coupling_angle = sp.simplify(coupling_y**2 / (coupling_2**2 + coupling_y**2))
    equality_numerator = sp.factor(coupling_y**2 * trace_y - coupling_2**2 * trace_2)
    checks.check(
        "fresh angle equality has the exact extra coupling premise",
        sp.simplify(coupling_angle - trace_angle) == 0
        if equality_numerator == 0
        else sp.simplify(
            (coupling_angle - trace_angle)
            * (coupling_2**2 + coupling_y**2)
            * (trace_2 + trace_y)
            - equality_numerator
        )
        == 0,
    )
    checks.check(
        "equal independent couplings refute automatic three-eighths",
        coupling_angle.subs({coupling_2: 1, coupling_y: 1}) == sp.Rational(1, 2)
        and trace_angle == sp.Rational(3, 8),
    )
    rho = sp.Symbol("rho", positive=True)
    covariant_angle = sp.simplify(
        (sp.sqrt(3) / rho) ** 2
        / (sp.sqrt(5) ** 2 + (sp.sqrt(3) / rho) ** 2)
    )
    checks.check(
        "fresh Abelian rescaling preserves the law while moving the coordinate",
        covariant_angle == 3 / (3 + 5 * rho**2)
        and covariant_angle.subs(rho, 1) == sp.Rational(3, 8)
        and covariant_angle.subs(rho, 2) == sp.Rational(3, 23),
    )

    q, u = sp.symbols("q u", real=True)
    d = -2 * q - u
    lepton = -3 * q
    singlet = 6 * q
    reduced_anomaly = sp.factor(
        6 * q**3 + 3 * u**3 + 3 * d**3 + 2 * lepton**3 + singlet**3
    )
    expected_anomaly = 18 * q * (2 * q - u) * (4 * q + u)
    checks.check(
        "fresh anomaly polynomial has three distinct affine branches",
        sp.simplify(reduced_anomaly - expected_anomaly) == 0
        and sp.simplify(reduced_anomaly.subs(u, -4 * q)) == 0
        and sp.simplify(reduced_anomaly.subs(u, 2 * q)) == 0
        and sp.simplify(reduced_anomaly.subs(q, 0)) == 0,
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
    numpy_accesses = [
        node
        for node in ast.walk(own_tree)
        if isinstance(node, ast.Name) and node.id in {"np", "numpy", "trapz", "trapezoid"}
    ]
    checks.check(
        "independent review has no NumPy compatibility surface",
        not numpy_imports and not numpy_accesses,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
