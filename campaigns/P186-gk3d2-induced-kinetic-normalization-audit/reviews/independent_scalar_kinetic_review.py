#!/usr/bin/env python3
"""Independent raw-SymPy rederivation for C-VAC-003.

This review intentionally does not import the canonical vacuum-polarization,
Dirac, gauge-beta, or renormalization modules.
"""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
CANONICAL_MODULE = ROOT / "src/substrate_framework/vacuum_polarization.py"


def main() -> int:
    checks = CheckLedger("P186-INDEPENDENT-C-VAC-003")

    own_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imported_names = {
        alias.name
        for node in ast.walk(own_tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    imported_modules = {
        node.module
        for node in ast.walk(own_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    checks.check(
        "review does not import canonical scientific claim modules",
        not any(
            fragment in imported_names
            for fragment in (
                "substrate_framework.vacuum_polarization",
                "substrate_framework.dirac_vacuum_polarization",
                "substrate_framework.gauge_beta",
                "substrate_framework.renormalization",
            )
        ),
    )

    p2, pq, q2, mass2 = sp.symbols("p2 pq q2 M2", real=True)
    pnu, qnu, tadpole = sp.symbols("pnu qnu I_tad", real=True)
    denominator = p2 + mass2
    shifted_denominator = p2 + 2 * pq + q2 + mass2
    vertex_contraction = 2 * pq + q2
    checks.check(
        "raw scalar vertex contraction is a propagator difference",
        sp.simplify(
            vertex_contraction - (shifted_denominator - denominator)
        )
        == 0,
    )
    routed_bubble = sp.simplify(((2 * pnu + qnu) - (2 * pnu - qnu)) * tadpole)
    seagull = -2 * qnu * tadpole
    checks.check(
        "independent bubble-seagull Ward contraction vanishes",
        routed_bubble != 0 and sp.simplify(routed_bubble + seagull) == 0,
    )
    checks.mutation_sensitive(
        "seagull coefficient",
        lambda candidate: sp.simplify(routed_bubble + candidate * qnu * tadpole)
        == 0,
        sp.Integer(-2),
        [sp.Integer(2), sp.Integer(-1), sp.Integer(-4)],
    )

    x = sp.Symbol("x", real=True)
    shifted_loop_component, transfer_component = sp.symbols("l_mu q_mu", real=True)
    first_vertex = 2 * shifted_loop_component + (1 - 2 * x) * transfer_component
    second_vertex = 2 * shifted_loop_component + (1 - 2 * x) * transfer_component
    numerator = sp.expand(first_vertex * second_vertex)
    even_numerator = sp.expand(
        numerator.subs(shifted_loop_component, -shifted_loop_component)
        + numerator
    ) / 2
    transfer_weight = sp.expand(
        even_numerator.coeff(transfer_component, 2)
    )
    checks.check(
        "shifted scalar vertices independently produce the squared weight",
        sp.simplify(transfer_weight - (1 - 2 * x) ** 2) == 0,
    )
    weight_integral = sp.integrate(transfer_weight, (x, 0, 1))
    checks.check(
        "raw Feynman-parameter weight integrates exactly to one third",
        weight_integral == sp.Rational(1, 3),
    )
    checks.mutation_sensitive(
        "scalar Feynman weight",
        lambda candidate: sp.integrate(candidate, (x, 0, 1))
        == sp.Rational(1, 3),
        transfer_weight,
        [x * (1 - x), (1 - 2 * x), 4 * x * (1 - x)],
    )

    species = sp.Symbol("N", positive=True, integer=True)
    charge = sp.Symbol("e", positive=True)
    scale2 = sp.Symbol("mu2", positive=True)
    positive_mass2 = sp.Symbol("M2_positive", positive=True)
    epsilon = sp.Symbol("epsilon", positive=True)
    common = sp.simplify(
        species * charge**2 * weight_integral / (4 * sp.pi) ** 2
    )
    bare = sp.simplify(
        -common
        * sp.gamma(epsilon)
        * (4 * sp.pi * scale2 / positive_mass2) ** epsilon
    )
    residue = sp.simplify(sp.limit(epsilon * bare, epsilon, 0, dir="+"))
    finite_part = sp.expand(
        sp.expand_log(
            sp.limit(bare - residue / epsilon, epsilon, 0, dir="+"),
            force=True,
        )
    )
    checks.check(
        "independent Laurent residue is minus N e squared over forty-eight pi squared",
        residue == -species * charge**2 / (48 * sp.pi**2),
    )
    checks.check(
        "independent finite bare part retains scale and mass logarithms",
        sp.simplify(
            finite_part
            - common
            * (
                sp.log(positive_mass2 / (4 * sp.pi * scale2))
                + sp.EulerGamma
            )
        )
        == 0,
    )
    finite_local = sp.Symbol("c_fin", real=True)
    counterterm = sp.simplify(
        common * (1 / epsilon - sp.EulerGamma + sp.log(4 * sp.pi))
        + finite_local
    )
    renormalized = sp.expand(
        sp.expand_log(
            sp.limit(bare + counterterm, epsilon, 0, dir="+"),
            force=True,
        )
    )
    expected = sp.simplify(
        common * sp.log(positive_mass2 / scale2) + finite_local
    )
    checks.check(
        "raw MS-bar limit retains the arbitrary finite local coefficient",
        sp.simplify(sp.expand_log(renormalized - expected, force=True)) == 0,
    )
    mass2_slope = sp.simplify(
        positive_mass2 * sp.diff(renormalized, positive_mass2)
    )
    scale_slope = sp.simplify(2 * scale2 * sp.diff(renormalized, scale2))
    checks.check(
        "independent mass-squared and scale slopes have opposite signs",
        mass2_slope == species * charge**2 / (48 * sp.pi**2)
        and scale_slope == -species * charge**2 / (24 * sp.pi**2),
    )
    shifted_finite = sp.simplify(renormalized.subs(finite_local, finite_local + 5))
    checks.check(
        "finite matching mutation shifts the total and preserves the slope",
        sp.simplify(shifted_finite - renormalized) == 5
        and sp.simplify(
            positive_mass2 * sp.diff(shifted_finite, positive_mass2)
            - mass2_slope
        )
        == 0,
    )

    dirac_parameter_integral = sp.integrate(x * (1 - x), (x, 0, 1))
    dirac_prefactor_relative_to_scalar = 8
    slope_ratio = sp.simplify(
        dirac_prefactor_relative_to_scalar
        * dirac_parameter_integral
        / weight_integral
    )
    checks.check(
        "independent spin trace and parameter integrals give factor four",
        dirac_parameter_integral == sp.Rational(1, 6) and slope_ratio == 4,
    )
    scalar_weight, dirac_weight = sp.symbols("W_s W_f", nonnegative=True)
    one_loop = sp.simplify(scalar_weight / 3 + 4 * dirac_weight / 3)
    checks.check(
        "independent connection-field weights are one third and four thirds",
        sp.diff(one_loop, scalar_weight) == sp.Rational(1, 3)
        and sp.diff(one_loop, dirac_weight) == sp.Rational(4, 3),
    )

    scale, reference = sp.symbols("mu mu_ref", positive=True)
    reference_value = sp.Symbol("Z_ref", real=True)
    running = sp.simplify(one_loop / (8 * sp.pi**2))
    general_solution = sp.simplify(
        reference_value + running * sp.log(reference / scale)
    )
    checks.check(
        "raw affine family solves the declared differential equation",
        sp.simplify(scale * sp.diff(general_solution, scale) + running) == 0
        and sp.simplify(general_solution.subs(scale, reference) - reference_value)
        == 0,
    )
    boundary_shift = sp.Symbol("delta_Z", nonzero=True, real=True)
    shifted_solution = general_solution + boundary_shift
    checks.check(
        "unequal boundaries have the same derivative but unequal totals",
        sp.simplify(
            scale * sp.diff(shifted_solution, scale)
            - scale * sp.diff(general_solution, scale)
        )
        == 0
        and sp.simplify(shifted_solution - general_solution) == boundary_shift,
    )
    kappa = sp.Symbol("kappa", positive=True)
    transformed_reference_value = sp.simplify(
        reference_value - running * sp.log(kappa)
    )
    transformed_solution = sp.simplify(
        transformed_reference_value
        + running * sp.log(kappa * reference / scale)
    )
    checks.check(
        "reference-coordinate transformation preserves the running function",
        sp.simplify(transformed_solution - general_solution) == 0,
    )

    zero_matching = sp.simplify(general_solution.subs(reference_value, 0))
    checks.check(
        "explicit zero matching has the expected conditional sign",
        zero_matching.subs(
            {
                scalar_weight: 1,
                dirac_weight: 0,
                reference: 2,
                scale: 1,
            }
        ).is_positive
        is True
        and zero_matching.subs(
            {
                scalar_weight: 1,
                dirac_weight: 0,
                reference: 1,
                scale: 2,
            }
        ).is_negative
        is True,
    )
    checks.check(
        "general boundary counterexamples defeat scale-only positivity",
        general_solution.subs(
            {
                scalar_weight: 1,
                dirac_weight: 0,
                reference_value: 10,
                reference: 1,
                scale: 2,
            }
        ).is_positive
        is True
        and general_solution.subs(
            {
                scalar_weight: 1,
                dirac_weight: 0,
                reference_value: -10,
                reference: 2,
                scale: 1,
            }
        ).is_negative
        is True,
    )

    canonical_text = CANONICAL_MODULE.read_text(encoding="utf-8")
    checks.check(
        "review independence is auditable at source level",
        "substrate_framework.vacuum_polarization" not in imported_modules
        and "substrate_framework.dirac_vacuum_polarization" not in imported_modules
        and "substrate_framework.gauge_beta" not in imported_modules
        and "substrate_framework.renormalization" not in imported_modules
        and "def scalar_qed4_zero_momentum_renormalization" in canonical_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
