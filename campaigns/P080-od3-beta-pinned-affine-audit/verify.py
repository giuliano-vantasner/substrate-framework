"""Primary exact verifier for the P080 OD3 affine-pinning audit."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.coupling_duality import (
    reciprocal_coordinate_change_ledger,
    reciprocal_coupling_ledger,
)
from substrate_framework.scale_constraints import (
    diagnose_log_constraints,
    generalized_least_squares,
    shift_log_references,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-22/"
    "bridge_OD3_beta_pinned.py"
)
SOURCE_SHA256 = "af96fa76a30c9ebb863e0a50b605ade5003a7595f28188ce7ca4d0884d67910c"
CONTRACT_SHA256 = "b12fabe8549ad427d18af52f4d7ee5e84f2b0474ed748542c1ecf885b30111c4"
FREEZE_SHA256 = "18ce3a34617f909e1c3e1822eb39cc2078b83710210a9b21c7bf1ee8f069bb49"
PROVENANCE = ("gravity", "medium", "hadronic", "confinement")


def _contract_path() -> Path:
    candidates = (
        Path("campaigns/P080-od3-beta-pinned-affine-audit/proposal.yaml"),
        Path("proposals/P080-od3-beta-pinned-affine-audit/proposal.yaml"),
    )
    return next(path for path in candidates if path.exists())


def _zero(value: object) -> bool:
    return sp.simplify(sp.sympify(value)) == 0


def _source_rank_predicate(matrix: sp.Matrix) -> bool:
    """Reproduce OD3.2's coefficient-only verdict."""

    rank = int(matrix.rank())
    return bool(
        rank == matrix.cols
        and matrix.rows > matrix.cols
        and matrix.cols - rank == 0
    )


def _source_prediction_predicate(
    matrix: sp.Matrix,
    rhs: sp.Matrix,
    coordinate: sp.Symbol,
    gravity_symbol: sp.Symbol,
) -> bool:
    """Reproduce the load-bearing Boolean in OD3.5."""

    solution = sp.solve(sp.Eq(matrix[0, 0] * coordinate, rhs[0]), coordinate)[0]
    predictions = tuple(
        sp.simplify(matrix[index, 0] * solution) for index in range(1, 4)
    )
    no_literal_y = not any(
        prediction.has(sp.Symbol("y")) for prediction in predictions
    )
    return bool(
        all(prediction.has(gravity_symbol) for prediction in predictions)
        and solution.is_number is not True
        and no_literal_y
    )


def main() -> int:
    checks = CheckLedger("P080")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    checks.check(
        "source hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
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
        "source has eight literal checks and a dynamic terminal tally",
        source_text.count("check(") == 9
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source and audit require no NumPy quadrature alias",
        all(alias not in source_text for alias in ("np." + "trapz", "np." + "trapezoid")),
    )

    x, x_star = sp.symbols("x x_star", real=True)
    k, y_pin = sp.symbols("k y_pin", positive=True)
    gravity, medium, hadronic, confine = sp.symbols(
        "g m h s", real=True
    )
    raw_rhs = sp.Matrix([gravity, medium, hadronic, confine])
    two_coordinate = sp.Matrix(
        [[2, 0], [-4, 0], [-1, k], [-2, 2 * k]]
    )
    free_column = two_coordinate[:, 0]
    pinned_column = two_coordinate[:, 1]
    pinned_contribution = pinned_column * y_pin
    pinned_rhs = raw_rhs - pinned_contribution

    checks.check(
        "pinning is exact affine substitution rather than a new row",
        free_column == sp.Matrix([2, -4, -1, -2])
        and pinned_contribution == sp.Matrix([0, 0, k * y_pin, 2 * k * y_pin])
        and pinned_rhs
        == sp.Matrix(
            [gravity, medium, hadronic - k * y_pin, confine - 2 * k * y_pin]
        ),
    )
    checks.check(
        "affine substitution round trips the original two-coordinate system",
        free_column * x + pinned_contribution
        == two_coordinate * sp.Matrix([x, y_pin]),
    )
    checks.check(
        "column removal is value independent",
        free_column.rank() == 1
        and not free_column.has(y_pin)
        and pinned_rhs.diff(y_pin) == -pinned_column,
    )

    original = diagnose_log_constraints(
        two_coordinate, raw_rhs, provenance=PROVENANCE
    )
    checks.check(
        "unpinned AS4 system has two directions and two compatibility conditions",
        original.linear.coefficient_rank == 2
        and original.linear.coefficient_row_dependencies == 2
        and len(original.left_nullspace) == 2
        and set(original.compatibility_residuals)
        == {2 * gravity + medium, -2 * hadronic + confine},
    )

    generic = diagnose_log_constraints(
        free_column, pinned_rhs, provenance=PROVENANCE
    )
    checks.check(
        "pinned coefficient column has one direction and three row dependencies",
        generic.linear.equations == 4
        and generic.linear.unknowns == 1
        and generic.linear.coefficient_rank == 1
        and generic.linear.coefficient_row_dependencies == 3
        and len(generic.left_nullspace) == 3
        and generic.nullspace == (),
    )
    expected_residuals = {
        2 * gravity + medium,
        gravity / 2 + hadronic - k * y_pin,
        gravity + confine - 2 * k * y_pin,
    }
    checks.check(
        "complete left-nullspace derives all three pinned compatibility residuals",
        set(generic.compatibility_residuals) == expected_residuals
        and all(
            vector.T * free_column == sp.zeros(1, 1)
            for vector in generic.left_nullspace
        ),
    )
    checks.check(
        "generic symbolic OD3 right-hand sides are inconsistent",
        generic.linear.augmented_rank == 2
        and not generic.linear.consistent
        and not generic.linear.unique
        and generic.linear.solution_dimension is None
        and generic.coordinate_identifiable is None,
    )

    compatible_raw_rhs = two_coordinate * sp.Matrix([x_star, y_pin])
    compatible_pinned_rhs = sp.simplify(
        compatible_raw_rhs - pinned_contribution
    )
    compatible = diagnose_log_constraints(
        free_column, compatible_pinned_rhs, provenance=PROVENANCE
    )
    checks.check(
        "compatible supplied rows conditionally identify the remaining coordinate",
        compatible_pinned_rhs == free_column * x_star
        and compatible.linear.coefficient_rank
        == compatible.linear.augmented_rank
        == 1
        and compatible.linear.unique
        and compatible.coordinate_identifiable == (True,)
        and compatible.compatibility_residuals == (0, 0, 0)
        and sp.linsolve((free_column, compatible_pinned_rhs)) == {(x_star,)},
    )

    def pin_compatible(values: object) -> bool:
        return diagnose_log_constraints(
            free_column,
            sp.Matrix(values) - pinned_contribution,
            provenance=PROVENANCE,
        ).linear.consistent

    checks.mutation_sensitive(
        "every supplied row is load bearing for pinned compatibility",
        pin_compatible,
        compatible_raw_rhs,
        [
            compatible_raw_rhs + sp.eye(4)[:, index]
            for index in range(4)
        ],
    )
    checks.check(
        "same coefficient rank admits both compatible and inconsistent data",
        _source_rank_predicate(free_column)
        and compatible.linear.consistent
        and not generic.linear.consistent
        and compatible.linear.coefficient_rank
        == generic.linear.coefficient_rank
        == 1,
    )
    checks.check(
        "OD3.2's source predicate cannot distinguish those data branches",
        _source_rank_predicate(free_column)
        and _source_rank_predicate(free_column)
        and generic.rhs != compatible.rhs,
    )
    checks.check(
        "OD3.5 never compares its three forced values with their supplied rows",
        _source_prediction_predicate(
            free_column, compatible_pinned_rhs, x, x_star
        )
        and _source_prediction_predicate(
            free_column,
            sp.Matrix(
                [
                    compatible_pinned_rhs[0],
                    compatible_pinned_rhs[1] + 17,
                    compatible_pinned_rhs[2] - 9,
                    compatible_pinned_rhs[3] + 5,
                ]
            ),
            x,
            x_star,
        ),
    )

    different_pin = y_pin + 1
    wrong_pin_rhs = compatible_raw_rhs - pinned_column * different_pin
    wrong_pin = diagnose_log_constraints(
        free_column, wrong_pin_rhs, provenance=PROVENANCE
    )
    checks.check(
        "a different supplied pin preserves coefficient rank but breaks the prior branch",
        wrong_pin.linear.coefficient_rank == 1
        and wrong_pin.linear.augmented_rank == 2
        and not wrong_pin.linear.consistent,
    )
    inferred_y = sp.simplify((gravity / 2 + hadronic) / k)
    pin_residual = gravity / 2 + hadronic - k * y_pin
    checks.check(
        "pin compatibility is inverse selection of the unpinned solution",
        not _zero(pin_residual)
        and sp.simplify(inferred_y - y_pin)
        == pin_residual / k,
    )

    delta = sp.Symbol("delta", real=True)
    shifted_generic = shift_log_references(generic, [delta])
    shifted_compatible = shift_log_references(compatible, [delta])
    checks.check(
        "reference shifts preserve every left-null compatibility residual",
        shifted_generic.compatibility_residuals == generic.compatibility_residuals
        and shifted_compatible.compatibility_residuals == (0, 0, 0),
    )
    checks.check(
        "reference shifts move the numeric solution without selecting a scale",
        shifted_compatible.rhs == compatible.rhs - free_column * delta
        and sp.linsolve((free_column, shifted_compatible.rhs))
        == {(x_star - delta,)},
    )

    nuisance_design = free_column.row_join(sp.eye(4))
    nuisance = diagnose_log_constraints(
        nuisance_design, raw_rhs, provenance=PROVENANCE
    )
    checks.check(
        "restoring four undeclared row offsets makes arbitrary right-hand sides feasible",
        nuisance_design.shape == (4, 5)
        and nuisance.linear.coefficient_rank
        == nuisance.linear.augmented_rank
        == 4
        and nuisance.linear.solution_dimension == 1
        and nuisance.coordinate_identifiable[0] is False,
    )
    relabeled = diagnose_log_constraints(
        free_column,
        compatible_pinned_rhs,
        provenance=("fabricated-a", "fabricated-b", "fabricated-c", "fabricated-d"),
    )
    checks.check(
        "unchanged algebra under fabricated labels proves provenance is external",
        relabeled.design == compatible.design
        and relabeled.rhs == compatible.rhs
        and relabeled.linear == compatible.linear
        and relabeled.provenance != compatible.provenance,
    )

    baseline, induced = sp.symbols("B S_ind", positive=True)
    total_gravity = 1 / (baseline + induced * sp.exp(-2 * x))
    gravity_slope = sp.simplify(sp.diff(sp.log(total_gravity), x))
    checks.check(
        "accepted additive inverse-gravity baseline destroys the constant gravity row",
        _zero(gravity_slope.subs(baseline, 0) - 2)
        and not _zero(gravity_slope - 2),
    )

    b0 = sp.Symbol("b0", positive=True)
    source_k = 8 * sp.pi**2 / b0
    source_y = 1 / (4 * sp.pi)
    checks.check(
        "source four-pi substitution retains the free beta-function coefficient",
        sp.simplify(source_k * source_y) == 2 * sp.pi / b0
        and sp.diff(source_k * source_y, b0) != 0
        and "b0 = sp.Symbol" in source_text,
    )
    checks.check(
        "source exact-pin guards are assignments rather than a selection oracle",
        _zero(4 * sp.pi - 4 * sp.pi)
        and _zero(5 * sp.pi - 5 * sp.pi)
        and "beta2.subs(beta2, 4 * sp.pi) - 4 * sp.pi" in source_text
        and "(4 * sp.pi) - 4 * sp.pi" in source_text,
    )
    checks.check(
        "source prose and executable disagree on the advertised physical pin",
        "AS6's self-dual 4pi" in source_text
        and "AS7: emergent gravity over-determines beta^2~0.245" in source_text
        and "y0 = 1 / (4 * sp.pi)" in source_text,
    )

    rho = sp.Symbol("rho", positive=True)
    coordinate_change = reciprocal_coordinate_change_ledger(
        4 * sp.pi, 16 * sp.pi**2, rho
    )
    checks.check(
        "coupling-coordinate normalization changes the numeric fixed coordinate",
        coordinate_change.rescaled_duality_coefficient
        == 16 * sp.pi**2 * rho**2
        and coordinate_change.rescaled_positive_fixed_point == 4 * sp.pi * rho
        and coordinate_change.fixed_point_rescaling_ratio == rho,
    )
    alternate = reciprocal_coupling_ledger(5 * sp.pi, 25 * sp.pi**2)
    checks.check(
        "an alternate reciprocal coefficient has an equally exact fixed coordinate",
        alternate.positive_fixed_point == 5 * sp.pi
        and alternate.fixed_point_residual == 0,
    )

    observations = sp.Matrix([2, -3, 1, 5])
    identity_gls = generalized_least_squares(
        free_column,
        observations,
        sp.eye(4),
        provenance=PROVENANCE,
        covariance_provenance="declared identity audit covariance",
    )
    unequal_gls = generalized_least_squares(
        free_column,
        observations,
        sp.diag(1, 4, 9, 16),
        provenance=PROVENANCE,
        covariance_provenance="declared unequal audit covariance",
    )
    checks.check(
        "residual scoring requires a declared covariance absent from OD3",
        identity_gls.degrees_of_freedom == unequal_gls.degrees_of_freedom == 3
        and identity_gls.chi_squared > 0
        and unequal_gls.chi_squared > 0
        and identity_gls.chi_squared != unequal_gls.chi_squared,
    )
    checks.check(
        "source imports no accepted physical row or covariance implementation",
        source_text.count("import ") == 1
        and "import sympy as sp" in source_text
        and "covariance" not in source_text.lower(),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
