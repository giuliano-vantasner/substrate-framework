#!/usr/bin/env python3
"""Primary exact verifier for the GK3D4 accepted-composition audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.charge_traces import (
    WeightedChargeState,
    charge_coupling_angle_ledger,
    common_trace_normalized_coupling_angle,
    finite_charge_trace_ledger,
)
from substrate_framework.chiral_anomalies import (
    five_row_local_anomaly_solution_variety,
)
from substrate_framework.gauge_beta import (
    GaugeFactor,
    ProductMultiplet,
    product_gauge_coefficients,
)
from substrate_framework.kinetic_scale_matching import (
    one_loop_scale_matched_kinetic_evidence,
)
from substrate_framework.product_gauge import standard_product_gauge_algebra
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.vacuum_polarization import matter_induced_kinetic_evidence
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
PROPOSAL = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-41/"
    "bridge_GK3D4_three_sectors_one_construction.py"
)
SOURCE_SHA256 = "046273d9a06f92ddbe9cd666d3b6de0f321b9709c371aeee8103394dd2a2ad35"
RELEASE_SHA256 = "0617c10955594b30c6d0d122476e360494d9e1b065efdf4f5c67728583388bb8"
FORMULA_FREEZE_SHA256 = (
    "673cb2d1766c9c503868fddd1ed687df23783fac392714c4acddb7cabe5b8688"
)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _trace_metric(generators: tuple[sp.MatrixBase, ...]) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(
        len(generators),
        len(generators),
        lambda first, second: sp.simplify(
            sp.trace(generators[first] * generators[second])
        ),
    )


def _declared_generation() -> tuple[WeightedChargeState, ...]:
    """Return WM1's supplied fifteen-state table, without a physical label claim."""

    return (
        WeightedChargeState("Q_L_up", 3, sp.Rational(1, 2), sp.Rational(1, 6)),
        WeightedChargeState("Q_L_down", 3, -sp.Rational(1, 2), sp.Rational(1, 6)),
        WeightedChargeState("u_R_conj", 3, 0, -sp.Rational(2, 3)),
        WeightedChargeState("d_R_conj", 3, 0, sp.Rational(1, 3)),
        WeightedChargeState("L_neutrino", 1, sp.Rational(1, 2), -sp.Rational(1, 2)),
        WeightedChargeState("L_electron", 1, -sp.Rational(1, 2), -sp.Rational(1, 2)),
        WeightedChargeState("e_R_conj", 1, 0, 1),
    )


def main() -> int:
    checks = CheckLedger("P188-GK3D4-ACCEPTED-COMPOSITION")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.139.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned",
        _digest(PROPOSAL / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    lexical_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(source_tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source predicate inventory remains exact",
        len(lexical_checks) == 11 and len(assertions) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "immutable source has no NumPy compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "source exposes the universal premises it later calls derived",
        all(
            token in source_text
            for token in (
                '"U(1)_Y": sp.Symbol("TrY2", positive=True)',
                '"SU(2)_L": sp.Symbol("TrT2", positive=True)',
                '"SU(3)_c": sp.Symbol("TrG2", positive=True)',
                "TrYsq = sp.Rational(5, 3) * TrT3sq",
                "Z_i = {k: sp.simplify(v / (b0 * beta2))",
            )
        ),
    )
    checks.check(
        "source has no loop action representation or matching construction",
        not any(
            token in source_text
            for token in (
                "Tr log(",
                "bubble",
                "seagull",
                "counterterm",
                "Z_ref",
                "ProductMultiplet",
            )
        ),
    )

    y = sp.Symbol("y", positive=True)
    product = standard_product_gauge_algebra(y)
    raw_color = _trace_metric(product.color_generators)
    raw_isospin = _trace_metric(product.isospin_generators)
    color = _trace_metric(product.color_embeddings)
    isospin = _trace_metric(product.isospin_embeddings)
    abelian = sp.simplify(sp.trace(product.abelian_generator**2))
    checks.check(
        "raw fundamental trace indices are both one half",
        raw_color == sp.eye(8) / 2 and raw_isospin == sp.eye(3) / 2,
    )
    checks.check(
        "one common product carrier supplies spectator-degenerate blocks",
        color == sp.eye(8)
        and isospin == sp.Rational(3, 2) * sp.eye(3)
        and abelian == 6 * y**2,
    )
    checks.check(
        "equal raw indices do not imply equal full matter weights",
        color[0, 0] != isospin[0, 0]
        and color[0, 0] != abelian
        and isospin[0, 0] != abelian,
    )
    cross_color_isospin = sp.ImmutableMatrix(
        8,
        3,
        lambda first, second: sp.simplify(
            sp.trace(
                product.color_embeddings[first]
                * product.isospin_embeddings[second]
            )
        ),
    )
    cross_color_abelian = tuple(
        sp.simplify(sp.trace(generator * product.abelian_generator))
        for generator in product.color_embeddings
    )
    cross_isospin_abelian = tuple(
        sp.simplify(sp.trace(generator * product.abelian_generator))
        for generator in product.isospin_embeddings
    )
    checks.check(
        "cross-factor trace blocks vanish for the actual standard carrier",
        cross_color_isospin == sp.zeros(8, 3)
        and cross_color_abelian == (0,) * 8
        and cross_isospin_abelian == (0,) * 3,
    )

    factors = (
        GaugeFactor("U1", 0, is_abelian=True),
        GaugeFactor("SU2", 2),
        GaugeFactor("SU3", 3),
    )
    full_indices = (6 * y**2, sp.Rational(3, 2), sp.Integer(1))
    dirac_as_two_weyl = ProductMultiplet(
        "declared_product_carrier",
        "weyl_fermion",
        2,
        full_indices,
        (y**2, sp.Rational(3, 4), sp.Rational(4, 3)),
    )
    weights = product_gauge_coefficients(factors, (dirac_as_two_weyl,))
    expected_dirac = tuple(sp.simplify(sp.Rational(4, 3) * value) for value in full_indices)
    checks.check(
        "accepted factor ledger reproduces Dirac four-thirds weights",
        weights.one_loop_weyl_fermions == expected_dirac,
    )
    raw_index_mutation = product_gauge_coefficients(
        factors,
        (
            ProductMultiplet(
                "raw_index_mutation",
                "weyl_fermion",
                2,
                (y**2, sp.Rational(1, 2), sp.Rational(1, 2)),
                (y**2, sp.Rational(3, 4), sp.Rational(4, 3)),
            ),
        ),
    )
    scalar_mutation = product_gauge_coefficients(
        factors,
        (
            ProductMultiplet(
                "statistics_mutation",
                "complex_scalar",
                1,
                full_indices,
                (y**2, sp.Rational(3, 4), sp.Rational(4, 3)),
            ),
        ),
    )
    checks.mutation_sensitive(
        "full product matter weights",
        lambda candidate: candidate == expected_dirac,
        weights.one_loop_weyl_fermions,
        [
            raw_index_mutation.one_loop_weyl_fermions,
            scalar_mutation.one_loop_complex_scalars,
            (expected_dirac[0], expected_dirac[1], sp.Integer(0)),
        ],
    )

    mus = sp.symbols("mu_Y mu_2 mu_3", positive=True)
    references = sp.symbols("M_Y M_2 M_3", positive=True)
    boundaries = sp.symbols("z_Y z_2 z_3", real=True)
    flows = tuple(
        matter_induced_kinetic_evidence(
            mus[index],
            references[index],
            boundaries[index],
            0,
            0,
            full_indices[index],
        )
        for index in range(3)
    )
    coefficients = tuple(flow.one_loop_coefficient for flow in flows)
    logarithms = tuple(
        sp.log(references[index] / mus[index]) for index in range(3)
    )
    totals = tuple(flow.kinetic_coefficient for flow in flows)
    checks.check(
        "factorwise accepted composition retains every boundary and logarithm",
        all(
            sp.simplify(
                totals[index]
                - boundaries[index]
                - coefficients[index] * logarithms[index] / (8 * sp.pi**2)
            )
            == 0
            for index in range(3)
        )
        and len(set(boundaries)) == 3
        and len(set(logarithms)) == 3,
    )
    ratio_residual = sp.simplify(
        coefficients[0] * totals[1] - coefficients[1] * totals[0]
    )
    expected_ratio_residual = sp.simplify(
        coefficients[0] * boundaries[1]
        - coefficients[1] * boundaries[0]
        + coefficients[0]
        * coefficients[1]
        * (logarithms[1] - logarithms[0])
        / (8 * sp.pi**2)
    )
    checks.check(
        "inverse-weight coupling ratio has an exact necessary and sufficient residual",
        sp.simplify(ratio_residual - expected_ratio_residual) == 0
        and ratio_residual != 0,
    )
    common_log = sp.Symbol("L", positive=True)
    zero_common_totals = tuple(
        sp.simplify(coefficient * common_log / (8 * sp.pi**2))
        for coefficient in coefficients
    )
    checks.check(
        "zero boundary and common logarithm recover the source ratio conditionally",
        sp.simplify(
            (1 / zero_common_totals[0])
            / (1 / zero_common_totals[1])
            - coefficients[1] / coefficients[0]
        )
        == 0,
    )
    checks.check(
        "independent boundary mutation breaks the source ratio",
        sp.simplify(
            coefficients[0] * (zero_common_totals[1] + 1)
            - coefficients[1] * zero_common_totals[0]
        )
        == coefficients[0]
        and coefficients[0] != 0,
    )

    mu0, beta_squared, b0 = sp.symbols("mu0 beta_squared b0", positive=True)
    matched = tuple(
        one_loop_scale_matched_kinetic_evidence(
            mu0,
            beta_squared,
            b0,
            reference_conversion=1,
            transmuted_conversion=1,
            renormalized_local_coefficient=boundaries[index],
            finite_matching_offset=0,
            scalar_weight=0,
            dirac_weight=full_indices[index],
        )
        for index in range(2)
    )
    checks.check(
        "scale-matched factors retain separate affine reference values",
        all(
            sp.simplify(
                matched[index].general_kinetic_coefficient
                - boundaries[index]
                - coefficients[index] / (b0 * beta_squared)
            )
            == 0
            for index in range(2)
        ),
    )
    checks.check(
        "source scale-matched ratio is an explicit zero-boundary specialization",
        sp.simplify(
            matched[0].zero_matching_inverse_kinetic_coordinate
            / matched[1].zero_matching_inverse_kinetic_coordinate
            - coefficients[1] / coefficients[0]
        )
        == 0
        and all(item.zero_matching_is_separate_premise for item in matched),
    )

    generation = finite_charge_trace_ledger(_declared_generation())
    checks.check(
        "supplied fifteen-state table has the exact three-eighths trace coordinate",
        generation.state_count == 15
        and generation.trace_t3_squared == 2
        and generation.trace_abelian_squared == sp.Rational(10, 3)
        and generation.trace_ratio == sp.Rational(3, 8),
    )
    common = sp.Symbol("C", positive=True)
    conditional_angle = common_trace_normalized_coupling_angle(
        generation.trace_t3_squared,
        generation.trace_abelian_squared,
        common,
    )
    checks.check(
        "three-eighths coupling angle requires the common inverse-trace law",
        conditional_angle.coupling_angle == sp.Rational(3, 8)
        and conditional_angle.angle_residual == 0
        and conditional_angle.common_coefficient_residual == 0,
    )
    unequal_angle = charge_coupling_angle_ledger(
        generation.trace_t3_squared,
        generation.trace_abelian_squared,
        1,
        1,
    )
    checks.check(
        "independent coupling coordinates preserve traces but break three-eighths",
        unequal_angle.trace_angle == sp.Rational(3, 8)
        and unequal_angle.coupling_angle == sp.Rational(1, 2)
        and unequal_angle.angle_residual != 0,
    )
    rho = sp.Symbol("rho", positive=True)
    normalized_angle = charge_coupling_angle_ledger(
        generation.trace_t3_squared,
        rho**2 * generation.trace_abelian_squared,
        sp.sqrt(5),
        sp.sqrt(3) / rho,
    )
    checks.check(
        "Abelian coordinate covariance preserves the conditional law not the number",
        normalized_angle.angle_residual == 0
        and normalized_angle.coupling_angle == 3 / (3 + 5 * rho**2)
        and normalized_angle.coupling_angle.subs(rho, 1) == sp.Rational(3, 8)
        and normalized_angle.coupling_angle.subs(rho, 2) == sp.Rational(3, 23),
    )
    anomaly_variety = five_row_local_anomaly_solution_variety()
    checks.check(
        "anomaly cancellation does not select the source charge assignment",
        len(anomaly_variety.branches) == 3
        and {branch.name for branch in anomaly_variety.branches}
        == {"displayed_line", "row_exchanged_line", "vectorlike_line"},
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
