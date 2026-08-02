"""Independent exact P078 derivation without the confrontation API."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-22/"
    "bridge_AS7_gravity_confrontation_planck_granularity.py"
)
SOURCE_SHA256 = "710635ddf323b8995dc4a1481aeb8232938d6db14c37bd95a537b26d17df3e0f"


def main() -> int:
    checks = CheckLedger("P078-INDEPENDENT")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    checks.check(
        "review reads immutable AS7 source",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )

    newton, speed, action = sp.symbols("G c hbar", positive=True)
    s_lower, s_upper = sp.Integer(1), sp.Integer(100)
    a_lower = sp.sqrt(s_lower * action * newton / speed**3)
    a_upper = sp.sqrt(s_upper * action * newton / speed**3)
    checks.check(
        "fresh interval image is exact",
        a_upper == 10 * a_lower,
    )
    mutated_upper = sp.sqrt(121 * action * newton / speed**3)
    checks.check(
        "fresh endpoint mutation changes the interval image",
        mutated_upper == 11 * a_lower and mutated_upper != a_upper,
    )

    target = sp.symbols("a_target", positive=True)
    target_coefficient = sp.simplify(target**2 * speed**3 / (action * newton))
    reconstructed_newton = sp.simplify(
        target**2 * speed**3 / (target_coefficient * action)
    )
    checks.check(
        "fresh arbitrary-target coefficient construction round trips",
        reconstructed_newton == newton,
    )
    checks.check(
        "fresh target construction exposes target dependence",
        sp.diff(target_coefficient, target) != 0,
    )

    coefficient = sp.symbols("s", nonzero=True, real=True)
    shift = coefficient * action / (target**2 * speed**3)
    baseline = sp.simplify(1 / newton - shift)
    checks.check(
        "fresh additive baseline restores supplied total",
        sp.simplify(baseline + shift - 1 / newton) == 0,
    )
    checks.check(
        "fresh zero-baseline mutation is generically unequal",
        sp.simplify(shift - 1 / newton) != 0,
    )

    b0 = sp.symbols("b0", positive=True)
    exponent = 8 * sp.pi**2 / b0
    design = sp.Matrix([[2, -1, 0], [1, 0, exponent]])
    checks.check(
        "fresh joint matrix has rank two",
        design.rank() == 2,
    )
    nullspace = design.nullspace()
    expected_null = sp.Matrix([-exponent, -2 * exponent, 1])
    checks.check(
        "fresh joint null direction is exact",
        nullspace == [expected_null] and design * expected_null == sp.zeros(2, 1),
    )
    checks.check(
        "fresh two-row system has one free coordinate",
        design.cols - design.rank() == 1,
    )

    gravity_log, length_log, conversion_log, coefficient_log = sp.symbols(
        "g l k v", real=True
    )
    full_design = design.col_join(sp.Matrix([[0, 1, 0]]))
    full_rhs = sp.Matrix(
        [gravity_log, length_log - conversion_log, coefficient_log]
    )
    solution = sp.simplify(full_design.inv() * full_rhs)
    expected_u = (gravity_log + coefficient_log) / 2
    expected_y = (length_log - conversion_log - expected_u) / exponent
    checks.check(
        "fresh supplied coefficient row raises rank to three",
        full_design.rank() == 3,
    )
    checks.check(
        "fresh unique solve retains every supplied input",
        solution
        == sp.Matrix(
            [sp.simplify(expected_u), coefficient_log, sp.simplify(expected_y)]
        ),
    )
    checks.check(
        "fresh unique solution has zero exact residual",
        sp.simplify(full_design * solution - full_rhs) == sp.zeros(3, 1),
    )
    checks.check(
        "fresh coupling coordinate depends on length target",
        sp.diff(expected_y, length_log) != 0,
    )
    checks.check(
        "fresh coupling coordinate depends on conversion and coefficient",
        sp.diff(expected_y, conversion_log) != 0
        and sp.diff(expected_y, coefficient_log) != 0,
    )
    checks.check(
        "fresh coupling coordinate depends on beta coefficient",
        sp.diff(expected_y, b0) != 0,
    )

    numeric_design = design.subs(b0, 8 * sp.pi**2)
    positive_solution = numeric_design.col_join(sp.Matrix([[0, 1, 0]])).inv() * sp.Matrix(
        [2, 4, 0]
    )
    reversed_solution = numeric_design.col_join(sp.Matrix([[0, 1, 0]])).inv() * sp.Matrix(
        [2, -4, 0]
    )
    checks.check(
        "fresh admissible example reconstructs positive coupling",
        positive_solution == sp.Matrix([1, 0, 3])
        and 1 / positive_solution[2] == sp.Rational(1, 3),
    )
    checks.check(
        "fresh orientation mutation yields nonphysical negative coupling square",
        reversed_solution == sp.Matrix([1, 0, -5])
        and 1 / reversed_solution[2] == -sp.Rational(1, 5),
    )

    checks.check(
        "fresh source audit finds imported observations",
        "G_obs = 6.674e-11" in source_text
        and "xi_hadron = 1.4e-15" in source_text,
    )
    checks.check(
        "fresh source audit finds selected coefficient prior",
        "s_G ~ O(1..100)" in source_text
        and "for s_G in (1, 12, 60)" in source_text,
    )
    checks.check(
        "fresh source audit finds solve-back equality",
        "b2_star, _ = beta2_from_gravity(s_G_test)" in source_text
        and "a_had = xi_hadron / math.exp" in source_text,
    )
    checks.check(
        "fresh source audit finds hard-coded comparison coupling",
        "b2_phys = sp.Rational(245, 1000)" in source_text,
    )
    checks.check(
        "fresh source audit finds no additive baseline",
        "baseline_inverse_newton" not in source_text,
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
