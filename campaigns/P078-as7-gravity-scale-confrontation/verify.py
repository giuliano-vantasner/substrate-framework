"""Primary exact verifier for P078 / provisional C-IDN-002."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.gravity_scale_confrontation import (
    induced_coefficient_for_target_cutoff,
    inverse_newton_baseline_for_target,
    joint_gravity_transmutation_log_ledger,
    pure_gravity_cutoff_interval,
    solve_joint_with_fixed_coefficient_ratio,
)
from substrate_framework.induced_gravity import induced_inverse_newton_ledger
from substrate_framework.scale_constraints import diagnose_log_constraints
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-22/"
    "bridge_AS7_gravity_confrontation_planck_granularity.py"
)
SOURCE_SHA256 = "710635ddf323b8995dc4a1481aeb8232938d6db14c37bd95a537b26d17df3e0f"
CONTRACT_SHA256 = "8c7913e7d628145b9322fc2949931522b68a82943c93d70113eb5483c77fb522"
FREEZE_SHA256 = "04199cc725f4dba93a6bcea77a90a9da84436b144840426d5af8968850936b82"


def _contract_path() -> Path:
    candidates = (
        Path("campaigns/P078-as7-gravity-scale-confrontation/proposal.yaml"),
        Path("proposals/P078-as7-gravity-scale-confrontation/proposal.yaml"),
    )
    return next(path for path in candidates if path.exists())


def main() -> int:
    checks = CheckLedger("P078")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    checks.check(
        "source hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "candidate contract hash remains frozen apart from terminal status",
        hashlib.sha256(
            _contract_path()
            .read_bytes()
            .replace(b"status: accepted\n", b"status: draft\n")
        ).hexdigest()
        == CONTRACT_SHA256,
    )
    freeze_path = _contract_path().parent / "evidence/frozen-proposal.yaml"
    checks.check(
        "pre-source contract commitment is immutable",
        hashlib.sha256(freeze_path.read_bytes()).hexdigest() == FREEZE_SHA256,
    )
    checks.check(
        "source has six literal checks and a dynamic terminal tally",
        source_text.count("check(") == 7
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    canonical_text = Path(
        "src/substrate_framework/gravity_scale_confrontation.py"
    ).read_text(encoding="utf-8")
    checks.check(
        "source and canonical exact routes use no NumPy quadrature alias",
        all(
            alias not in source_text and alias not in canonical_text
            for alias in ("np." + "trapz", "np." + "trapezoid")
        ),
    )

    newton, speed, action = sp.symbols("G c hbar", positive=True)
    interval = pure_gravity_cutoff_interval(newton, 1, 100, speed, action)
    unit_cutoff = sp.sqrt(action * newton / speed**3)
    checks.check(
        "supplied coefficient interval has exact endpoint image",
        interval.cutoff_lower == unit_cutoff
        and interval.cutoff_upper == 10 * unit_cutoff,
    )
    widened = pure_gravity_cutoff_interval(newton, 1, 121, speed, action)
    checks.check(
        "coefficient endpoint mutation changes the cutoff endpoint",
        widened.cutoff_lower == interval.cutoff_lower
        and widened.cutoff_upper == 11 * unit_cutoff
        and widened.cutoff_upper != interval.cutoff_upper,
    )
    checks.check(
        "interval width remains a supplied premise",
        interval.coefficient_interval_width == 99
        and widened.coefficient_interval_width == 120,
    )

    target = sp.symbols("a_target", positive=True)
    coefficient = induced_coefficient_for_target_cutoff(
        target, newton, speed, action
    )
    checks.check(
        "every positive target cutoff has a pure-branch coefficient preimage",
        coefficient == target**2 * speed**3 / (action * newton),
    )
    target_roundtrip = induced_inverse_newton_ledger(
        target, coefficient, speed, action
    )
    checks.check(
        "target coefficient round trips to supplied Newton total",
        sp.simplify(target_roundtrip.pure_induced_newton - newton) == 0,
    )
    checks.check(
        "target remains load bearing in the inverse construction",
        coefficient.has(target) and sp.diff(coefficient, target) != 0,
    )

    free_coefficient = sp.symbols("s", nonzero=True, real=True)
    baseline = inverse_newton_baseline_for_target(
        newton, target, free_coefficient, speed, action
    )
    general = induced_inverse_newton_ledger(
        target,
        free_coefficient,
        speed,
        action,
        baseline_inverse_newton=baseline,
    )
    checks.check(
        "additive baseline realizes any supplied positive Newton total",
        sp.simplify(general.total_inverse_newton - 1 / newton) == 0,
    )
    checks.check(
        "baseline retains cutoff and coefficient dependence",
        sp.diff(baseline, target) != 0
        and sp.diff(baseline, free_coefficient) != 0,
    )
    wrong_zero_baseline = induced_inverse_newton_ledger(
        2 * target, free_coefficient, speed, action
    )
    checks.check(
        "restoring zero baseline after a cutoff mutation changes the total",
        sp.simplify(
            wrong_zero_baseline.total_inverse_newton - 1 / newton
        )
        != 0,
    )

    g_log, length_log = sp.symbols("g_log length_log", real=True)
    b0 = sp.symbols("b0", positive=True)
    joint = joint_gravity_transmutation_log_ledger(
        sp.exp(g_log),
        sp.exp(length_log),
        b0,
        gravity_provenance="supplied pure-gravity ratio",
        length_provenance="supplied inverse-energy length ratio",
    )
    exponent = 8 * sp.pi**2 / b0
    checks.check(
        "joint row matrix retains all three free coordinates",
        joint.system.design
        == sp.ImmutableMatrix([[2, -1, 0], [1, 0, exponent]]),
    )
    checks.check(
        "two rows on three coordinates are rank two and underdetermined",
        joint.system.linear.coefficient_rank == 2
        and joint.system.linear.solution_dimension == 1
        and joint.system.linear.underdetermined,
    )
    expected_null = sp.ImmutableMatrix([-exponent, -2 * exponent, 1])
    checks.check(
        "joint nullspace is the cutoff-coefficient-coupling tradeoff",
        len(joint.system.nullspace) == 1
        and joint.system.nullspace[0] == expected_null
        and joint.system.design * expected_null == sp.zeros(2, 1),
    )
    checks.check(
        "no joint coordinate is identifiable from the two rows",
        joint.system.coordinate_identifiable == (False, False, False),
    )
    gravity_only = diagnose_log_constraints(
        [[2, -1, 0]],
        [g_log],
        provenance=["supplied pure-gravity ratio"],
    )
    checks.check(
        "removing the length row reduces rank rather than preserving a verdict",
        gravity_only.linear.coefficient_rank == 1
        and joint.system.linear.coefficient_rank == 2,
    )

    coefficient_log, conversion_log = sp.symbols(
        "coefficient_log conversion_log", real=True
    )
    solved = solve_joint_with_fixed_coefficient_ratio(
        sp.exp(g_log),
        sp.exp(length_log),
        sp.exp(coefficient_log),
        b0,
        conversion_ratio=sp.exp(conversion_log),
        gravity_provenance="G row",
        length_provenance="L row",
        coefficient_provenance="supplied s row",
    )
    expected_u = sp.simplify((g_log + coefficient_log) / 2)
    expected_y = sp.simplify(
        (length_log - conversion_log - expected_u) / exponent
    )
    checks.check(
        "supplied coefficient row makes the exact system unique",
        solved.system.linear.unique
        and solved.system.coordinate_identifiable == (True, True, True),
    )
    checks.check(
        "unique log solution is derived from all supplied rows",
        sp.simplify(
            solved.log_solution
            - sp.ImmutableMatrix([expected_u, coefficient_log, expected_y])
        )
        == sp.zeros(3, 1),
    )
    checks.check(
        "unique solve satisfies every row exactly",
        solved.residuals == (0, 0, 0),
    )
    checks.check(
        "inferred inverse coupling depends on the target length row",
        sp.diff(expected_y, length_log) != 0,
    )
    checks.check(
        "inferred inverse coupling depends on conversion and coefficient inputs",
        sp.diff(expected_y, conversion_log) != 0
        and sp.diff(expected_y, coefficient_log) != 0,
    )
    checks.check(
        "beta coefficient remains load bearing",
        sp.diff(expected_y, b0) != 0,
    )

    admissible = solve_joint_with_fixed_coefficient_ratio(
        sp.exp(2),
        sp.exp(4),
        1,
        8 * sp.pi**2,
        gravity_provenance="G",
        length_provenance="L",
        coefficient_provenance="s",
    )
    checks.check(
        "an explicit admissible inverse solve gives positive coupling",
        admissible.log_solution == sp.ImmutableMatrix([1, 0, 3])
        and admissible.inferred_coupling_squared == sp.Rational(1, 3)
        and admissible.positive_coupling_admissible is True,
    )
    reversed_length = solve_joint_with_fixed_coefficient_ratio(
        sp.exp(2),
        sp.exp(-4),
        1,
        8 * sp.pi**2,
        gravity_provenance="G",
        length_provenance="reciprocal L mutation",
        coefficient_provenance="s",
    )
    checks.check(
        "length-orientation mutation breaks positive-coupling admissibility",
        reversed_length.inverse_coupling_squared == -5
        and reversed_length.positive_coupling_admissible is False,
    )

    checks.check(
        "source explicitly imports observed dimensionful quantities",
        all(
            token in source_text
            for token in (
                "hbar = 1.054571817e-34",
                "c0 = 2.99792458e8",
                "G_obs = 6.674e-11",
                "xi_hadron = 1.4e-15",
            )
        ),
    )
    checks.check(
        "source hard-codes beta coefficient and coefficient samples",
        "b0 = 7" in source_text
        and "for s_G in (1, 12, 60)" in source_text,
    )
    checks.check(
        "source Planck-band predicate is a supplied numerical interval",
        "1e-36 < a_planck(s_G) < 1e-33" in source_text,
    )
    checks.check(
        "source equality reuses coupling solved from gravity target",
        "b2_star, _ = beta2_from_gravity(s_G_test)" in source_text
        and "a_had = xi_hadron / math.exp" in source_text,
    )
    checks.check(
        "source comparison coupling is hard-coded rather than derived",
        "b2_phys = sp.Rational(245, 1000)" in source_text,
    )
    checks.check(
        "source omits an additive inverse-coupling baseline",
        "baseline_inverse_newton" not in source_text
        and "bare_inverse_newton" not in source_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
