"""Primary exact and regression verifier for P074 / C-GRV-001."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.induced_gravity import (
    cutoff_length_from_pure_induced_newton,
    effective_newton_from_inverse,
    gravity_source_normalization_ledger,
    induced_inverse_newton_ledger,
    induced_scaling_log_constraint,
    induced_scaling_null_rescaling,
    newton_dimension_ledger,
    normalized_gravity_source_coupling,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-21/"
    "bridge_AS3_sakharov_kappa_reduce.py"
)
SOURCE_SHA256 = "f88cc85a3fb64d1b8aabdf53ced29168d78fce9470e586dc19564288a120903b"


def main() -> int:
    checks = CheckLedger("P074")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    checks.check(
        "source hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "source has eight executed checks and terminal tally",
        source_text.count("check(") == 9
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source uses no numerical quadrature alias",
        "np.trapz" not in source_text and "np.trapezoid" not in source_text,
    )
    checks.check(
        "source admits induced form and cutoff map are imported",
        "IMPORTED (cited, FORM not magnitude" in source_text
        and "the cutoff = hbar c0/a granularity identification" in source_text,
    )

    dimensions = newton_dimension_ledger()
    checks.check(
        "canonical MLT rows and a c hbar columns",
        dimensions.dimension_matrix
        == sp.Matrix([[0, 0, 1], [1, 1, 2], [0, -1, -1]]),
    )
    checks.check(
        "primitive dimension matrix is full rank",
        dimensions.dimension_matrix.rank() == 3,
    )
    checks.check(
        "Newton monomial powers derived",
        dimensions.newton_exponents == sp.Matrix([2, 3, -1])
        and dimensions.dimension_matrix * dimensions.newton_exponents
        == dimensions.newton_dimension,
    )
    checks.check(
        "inverse Newton monomial powers derived",
        dimensions.inverse_newton_exponents == sp.Matrix([-2, -3, 1])
        and dimensions.dimension_matrix * dimensions.inverse_newton_exponents
        == dimensions.inverse_newton_dimension,
    )
    checks.check(
        "wrong cutoff powers fail in the declared complete basis",
        dimensions.dimension_matrix * sp.Matrix([-1, -3, 1])
        != dimensions.inverse_newton_dimension
        and dimensions.dimension_matrix * sp.Matrix([-4, -3, 1])
        != dimensions.inverse_newton_dimension,
    )
    checks.check(
        "G over a squared is not dimensionless in MLT units",
        dimensions.newton_dimension - sp.Matrix([0, 2, 0])
        == sp.Matrix([-1, 1, -2]),
    )

    a, s, c, hbar = sp.symbols("a s c hbar", positive=True)
    pure = induced_inverse_newton_ledger(a, s, c, hbar)
    checks.check(
        "declared cutoff energy derived",
        pure.cutoff_energy == hbar * c / a,
    )
    checks.check(
        "declared leading inverse Newton shift derived",
        pure.induced_inverse_newton == s * hbar / (a**2 * c**3),
    )
    checks.check(
        "cutoff energy and length forms agree",
        sp.simplify(
            pure.induced_inverse_newton
            - s * pure.cutoff_energy**2 / (hbar * c**5)
        )
        == 0,
    )
    checks.check(
        "pure induced reciprocal is conditional",
        pure.pure_induced_newton == a**2 * c**3 / (s * hbar),
    )
    checks.check(
        "dimensionless coefficient remains load bearing",
        pure.pure_induced_newton.has(s)
        and sp.diff(pure.pure_induced_newton, s) != 0,
    )
    negative = induced_inverse_newton_ledger(a, -s, c, hbar)
    checks.check(
        "coefficient sign is not selected by dimensions",
        negative.induced_inverse_newton == -pure.induced_inverse_newton,
    )

    baseline, target = sp.symbols("baseline target", positive=True)
    shifted = induced_inverse_newton_ledger(
        a,
        s,
        c,
        hbar,
        baseline_inverse_newton=baseline,
    )
    checks.check(
        "independent baseline adds in inverse space",
        shifted.total_inverse_newton
        == baseline + s * hbar / (a**2 * c**3),
    )
    arbitrary = induced_inverse_newton_ledger(
        a,
        s,
        c,
        hbar,
        baseline_inverse_newton=target - pure.induced_inverse_newton,
    )
    checks.check(
        "baseline counterfamily reaches arbitrary supplied inverse",
        arbitrary.total_inverse_newton == target,
    )
    cancellation = induced_inverse_newton_ledger(
        a,
        s,
        c,
        hbar,
        baseline_inverse_newton=-pure.induced_inverse_newton,
    )
    checks.check(
        "baseline cancellation makes inverse singular",
        cancellation.total_inverse_newton == 0,
    )
    try:
        effective_newton_from_inverse(cancellation.total_inverse_newton)
    except ValueError:
        cancellation_rejected = True
    else:
        cancellation_rejected = False
    checks.check(
        "positive effective Newton gate rejects cancellation",
        cancellation_rejected,
    )
    checks.check(
        "removed cutoff leaves baseline rather than pure scaling",
        sp.limit(shifted.total_inverse_newton, a, sp.oo) == baseline,
    )
    checks.check(
        "source omits baseline and finite inverse terms",
        "G_0" not in source_text
        and "baseline" not in source_text
        and "UV finite" not in source_text,
    )

    ratio = sp.symbols("R", positive=True)
    constraint = induced_scaling_log_constraint(
        ratio,
        provenance="declared pure induced ratio",
    )
    checks.check(
        "pure scaling gives exact two-coordinate log row",
        constraint.design == sp.Matrix([[2, -1]])
        and constraint.rhs == sp.Matrix([sp.log(ratio)]),
    )
    checks.check(
        "log row leaves one null direction",
        constraint.linear.coefficient_rank == 1
        and constraint.linear.solution_dimension == 1
        and len(constraint.nullspace) == 1
        and constraint.design * constraint.nullspace[0] == sp.zeros(1, 1),
    )
    checks.check(
        "nullspace spans simultaneous a and s change",
        2 * constraint.nullspace[0] == sp.Matrix([1, 2]),
    )
    checks.check(
        "neither a nor s coordinate is identified",
        constraint.coordinate_identifiable == (False, False),
    )
    a_ratio, s_ratio, rho = sp.symbols("a_ratio s_ratio rho", positive=True)
    changed_a, changed_s, invariant = induced_scaling_null_rescaling(
        a_ratio,
        s_ratio,
        rho,
    )
    checks.check(
        "null rescaling preserves pure Newton ratio",
        invariant == a_ratio**2 / s_ratio
        and sp.simplify(changed_a**2 / changed_s - invariant) == 0,
    )
    supplied_newton = sp.symbols("G_supplied", positive=True)
    inferred_a = cutoff_length_from_pure_induced_newton(
        supplied_newton,
        s,
        c,
        hbar,
    )
    checks.check(
        "a inverse is inference from supplied G and s",
        inferred_a.has(supplied_newton, s)
        and inferred_a == sp.sqrt(s * hbar * supplied_newton / c**3),
    )
    checks.check(
        "source calls a pinned while retaining s",
        "PINS the ONE length" in source_text
        and "a = sqrt(s_G hbar G_eff/c0^3)" in source_text,
    )
    checks.check(
        "source performs no joint identifiability rank test",
        "nullspace" not in source_text and "coefficient_rank" not in source_text,
    )
    checks.check(
        "source branch filter is verifier insensitive",
        "if s.is_positive or True" in source_text,
    )

    operator_dimension = [0, -2, 0]
    mass_density = gravity_source_normalization_ledger(
        operator_dimension,
        [1, -3, 0],
    )
    checks.check(
        "mass-density source coupling requires c inverse squared dimensions",
        mass_density.required_coupling_dimension == sp.Matrix([-1, 1, 0])
        and mass_density.normalization_dimension == sp.Matrix([0, -2, 2]),
    )
    energy_density = gravity_source_normalization_ledger(
        operator_dimension,
        [1, -1, -2],
    )
    checks.check(
        "energy-density source coupling requires c inverse fourth dimensions",
        energy_density.required_coupling_dimension == sp.Matrix([-1, -1, 2])
        and energy_density.normalization_dimension == sp.Matrix([0, -4, 4]),
    )
    compatible_source = sp.Matrix(operator_dimension) - dimensions.newton_dimension
    compatible = gravity_source_normalization_ledger(
        operator_dimension,
        compatible_source,
    )
    checks.check(
        "numeric normalization allowed only for matching source units",
        compatible.dimensionless_normalization_allowed
        and not mass_density.dimensionless_normalization_allowed
        and not energy_density.dimensionless_normalization_allowed,
    )
    normalized = normalized_gravity_source_coupling(
        supplied_newton,
        8 * sp.pi / c**2,
    )
    checks.check(
        "source normalization retains dimensioned factor",
        normalized == 8 * sp.pi * supplied_newton / c**2,
    )
    checks.check(
        "source imports bare 8 pi Newton map",
        "kappa = 8 * sp.pi * G_eff" in source_text
        and "note-13 Node F, reused" in source_text,
    )

    kappa = 8 * sp.pi * pure.pure_induced_newton
    eps0_mu0 = 1 / c**2
    checks.check(
        "G5 source cross-check is substitution identity",
        sp.simplify(
            pure.pure_induced_newton / c**2
            - kappa * eps0_mu0 / (8 * sp.pi)
        )
        == 0,
    )
    checks.check(
        "free coefficient can absorb every cutoff rescaling",
        sp.simplify(
            pure.pure_induced_newton.subs({a: rho * a, s: rho**2 * s})
            - pure.pure_induced_newton
        )
        == 0,
    )
    checks.check(
        "pure ultraviolet and coefficient limits remain conditional",
        sp.limit(pure.pure_induced_newton, a, 0, dir="+") == 0
        and sp.limit(pure.pure_induced_newton, s, 0, dir="+") == sp.oo,
    )
    checks.check(
        "no comparator or physical scale enters canonical result",
        all(
            token not in Path("src/substrate_framework/induced_gravity.py").read_text()
            for token in ("G_Newton", "ell_Planck", "Skyrmion", "3.62")
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
