"""Independent exact P079 derivation without the fixation API."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-22/"
    "bridge_AS8_superborn_quantum_face_of_granularity.py"
)
SOURCE_SHA256 = "47fda3732d8901b6949b2859952123be675eef2bb28bad0ac0d241948fe3ea73"


def main() -> int:
    checks = CheckLedger("P079-INDEPENDENT")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "review reads immutable AS8 source",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )

    x = sp.symbols("x", real=True)
    selection = sp.symbols("S", real=True, nonzero=True)
    probability = (1 - sp.exp(-selection * x)) / (1 - sp.exp(-selection))
    neutral = sp.symbols("epsilon", real=True)
    neutral_probability = (
        1 - sp.exp(-neutral * x)
    ) / (1 - sp.exp(-neutral))
    checks.check(
        "fresh neutral limit is x",
        sp.limit(neutral_probability, neutral, 0) == x,
    )
    checks.check(
        "fresh absorbing endpoints are zero and one",
        sp.simplify(probability.subs(x, 0)) == 0
        and sp.simplify(probability.subs(x, 1)) == 1,
    )
    checks.check(
        "fresh backward-equation residual vanishes",
        sp.simplify(
            sp.diff(probability, x, 2)
            + selection * sp.diff(probability, x)
        )
        == 0,
    )
    checks.check(
        "fresh generator mutation produces nonzero residual",
        sp.simplify(
            sp.diff(probability, x, 2)
            + 2 * selection * sp.diff(probability, x)
        )
        != 0,
    )

    boundary_matrix = sp.Matrix([[1, 1], [1, sp.exp(-selection)]])
    boundary_values = sp.Matrix([0, 1])
    constants = sp.simplify(boundary_matrix.inv() * boundary_values)
    reconstructed = sp.simplify(constants[0] + constants[1] * sp.exp(-selection * x))
    checks.check(
        "fresh boundary matrix is nonsingular for nonzero real selection",
        boundary_matrix.det() == sp.exp(-selection) - 1
        and boundary_matrix.det() != 0,
    )
    checks.check(
        "fresh boundary solve reconstructs branch",
        sp.simplify(reconstructed - probability) == 0,
    )

    complement = (
        1 - sp.exp(selection * (1 - x))
    ) / (1 - sp.exp(selection))
    checks.check(
        "fresh complement symmetry is exact",
        sp.simplify(probability + complement - 1) == 0,
    )
    frequency_derivative = sp.simplify(sp.diff(probability, x))
    checks.check(
        "fresh frequency derivative has same-sign numerator and denominator",
        sp.simplify(
            frequency_derivative
            - selection * sp.exp(-selection * x) / (1 - sp.exp(-selection))
        )
        == 0,
    )
    selection_derivative = sp.factor(sp.diff(probability, selection))
    convexity_gap = (1 - x) + x * sp.exp(selection) - sp.exp(selection * x)
    factorized_derivative = sp.simplify(
        convexity_gap
        * sp.exp(selection)
        * sp.exp(-selection * x)
        / (sp.exp(selection) - 1) ** 2
    )
    checks.check(
        "fresh selection derivative has strict-convexity gap",
        sp.simplify(selection_derivative - factorized_derivative) == 0,
    )
    checks.check(
        "fresh midpoint gap is a nonzero square",
        sp.simplify(
            convexity_gap.subs(x, sp.Rational(1, 2))
            - (sp.exp(selection / 2) - 1) ** 2 / 2
        )
        == 0,
    )
    series = sp.series(neutral_probability, neutral, 0, 4).removeO()
    expected_series = sp.simplify(
        x
        + neutral * x * (1 - x) / 2
        + neutral**2 * x * (1 - x) * (1 - 2 * x) / 12
        - neutral**3 * x**2 * (1 - x) ** 2 / 24
    )
    checks.check(
        "fresh cubic neutral series is exact",
        sp.simplify(series - expected_series) == 0,
    )

    interior = sp.Rational(2, 5)
    positive = probability.subs({x: interior, selection: 3})
    negative = probability.subs({x: interior, selection: -3})
    checks.check(
        "fresh sign counterexample moves bias in opposite directions",
        0 < negative < interior < positive < 1,
    )
    limit_branch = (
        1 - sp.exp(-neutral * interior)
    ) / (1 - sp.exp(-neutral))
    checks.check(
        "fresh selection extremes span zero to one",
        sp.limit(limit_branch, neutral, -sp.oo) == 0
        and sp.limit(limit_branch, neutral, sp.oo) == 1,
    )

    first, second, coefficient, scale = sp.symbols(
        "I1 I2 kappa lambda", positive=True
    )
    total = first + second
    frequency = first / total
    contrast = first - second
    normalized_contrast = contrast / total
    selection_coordinate = coefficient * contrast
    checks.check(
        "fresh intensity parameterization is invertible",
        sp.simplify(contrast - total * (2 * frequency - 1)) == 0
        and sp.simplify(normalized_contrast - (2 * frequency - 1)) == 0,
    )
    scaled_first = scale**2 * first
    scaled_second = scale**2 * second
    checks.check(
        "fresh common amplitude scaling preserves normalized frequency",
        sp.simplify(
            scaled_first / (scaled_first + scaled_second) - frequency
        )
        == 0,
    )
    scaled_selection = coefficient * (scaled_first - scaled_second)
    checks.check(
        "fresh fixed coefficient makes selection scale quadratically",
        sp.simplify(scaled_selection - scale**2 * selection_coordinate) == 0,
    )
    covariant_coefficient = coefficient / scale**2
    checks.check(
        "fresh compensating coefficient preserves selection coordinate",
        sp.simplify(
            covariant_coefficient * (scaled_first - scaled_second)
            - selection_coordinate
        )
        == 0,
    )
    normalized_first = first / total
    normalized_second = second / total
    normalized_coefficient = coefficient * total
    checks.check(
        "fresh unit normalization preserves selection with transformed coefficient",
        sp.simplify(normalized_first + normalized_second - 1) == 0
        and sp.simplify(
            normalized_coefficient * (normalized_first - normalized_second)
            - selection_coordinate
        )
        == 0,
    )

    checks.check(
        "fresh source examples have norms five and one hundred twenty five",
        2**2 + 1**2 == 5 and 10**2 + 5**2 == 125,
    )
    checks.check(
        "fresh source examples have identical unit-normalized intensities",
        sp.Rational(2**2, 2**2 + 1**2)
        == sp.Rational(10**2, 10**2 + 5**2)
        == sp.Rational(4, 5),
    )
    selection_expression_load_lines = tuple(
        sorted(
            node.lineno
            for node in ast.walk(source_tree)
            if isinstance(node, ast.Name)
            and node.id == "S_expr"
            and isinstance(node.ctx, ast.Load)
        )
    )
    checks.check(
        "fresh source audit finds inserted rather than derived S examples",
        "u_S3" in source_text
        and "u_S75" in source_text
        and selection_expression_load_lines == (111, 112),
    )
    theta_loads = sum(
        isinstance(node, ast.Name)
        and node.id == "Theta_eff"
        and isinstance(node.ctx, ast.Load)
        for node in ast.walk(source_tree)
    )
    cutoff_loads = sum(
        isinstance(node, ast.Name)
        and node.id == "a"
        and isinstance(node.ctx, ast.Load)
        for node in ast.walk(source_tree)
    )
    checks.check(
        "fresh source audit finds no executable Theta_eff or cutoff use",
        theta_loads == 0 and cutoff_loads == 0,
    )
    checks.check(
        "fresh source audit finds tautological hbar substitution",
        "Theta_form.subs(hbar_med, hbar) == hbar * omega" in source_text,
    )
    checks.check(
        "fresh source audit finds no generator derivation",
        "u_xx" not in source_text and "absorbing" not in source_text.lower(),
    )
    checks.check(
        "fresh source audit finds positive-only symbolic selection",
        'sp.symbols("A1 A2 lambda S x0", positive=True)' in source_text,
    )
    checks.check(
        "fresh exact routes use no NumPy integration",
        "import numpy" not in source_text
        and "np." + "trapz" not in source_text
        and "np." + "trapezoid" not in source_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
