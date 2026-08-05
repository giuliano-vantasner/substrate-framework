#!/usr/bin/env python3
"""Primary exact verifier for GK3D3 adjudication and C-VAC-004."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

import substrate_framework.kinetic_scale_matching as matching_module
from substrate_framework.kinetic_scale_matching import (
    inverse_length_scale_kinetic_evidence,
    one_loop_scale_matched_kinetic_evidence,
)
from substrate_framework.scale_transmutation import two_length_log_constraint
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-41/"
    "bridge_GK3D3_transmutation_closes_the_log.py"
)
SOURCE_SHA256 = "1c3f81d15ace3ec2c6326c89659596f5b9ff84ac23ef7f0143a53ad92b23b211"
RELEASE_SHA256 = "55916c2f626ebcd2afdb6461de485d35c850e22fbf439c78d9cbccea08004591"
FORMULA_FREEZE_SHA256 = (
    "7210ca6ac4b8b9ae06d72f2fd4ed68c3d149c57527f383cb734f685a3f6d3838"
)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P187-GK3D3-C-VAC-004")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.138.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "corrected formula freeze remains pinned",
        _digest(CAMPAIGN / "evidence/formula-freeze.yaml")
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
        len(lexical_checks) == 14 and len(assertions) == 1,
    )
    source_compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "immutable source has no NumPy compatibility surface",
        source_compatibility.legacy_references == 0
        and source_compatibility.current_references == 0
        and source_compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "source exposes its load-bearing overclaims",
        all(
            token in source_text
            for token in (
                "p = 0 IS the logarithm",
                "No free parameter.",
                "Z(Lambda) = 0 -- rung25",
                "sp.Rational(245, 1000)",
            )
        ),
    )

    ell0, ell1, k0, k1 = sp.symbols("ell0 ell1 K0 K1", positive=True)
    local, finite = sp.symbols("Z_local c_fin", real=True)
    scalar, dirac = sp.symbols("W_s W_f", nonnegative=True)
    generic = inverse_length_scale_kinetic_evidence(
        ell0,
        ell1,
        k0,
        k1,
        local,
        finite,
        scalar,
        dirac,
    )
    coefficient = sp.simplify(scalar / 3 + 4 * dirac / 3)
    expected_ratio = sp.simplify(k0 * ell1 / (k1 * ell0))
    checks.check(
        "independent inverse-length energy maps are exact",
        generic.reference_energy == k0 / ell0
        and generic.evaluation_energy == k1 / ell1
        and generic.energy_length_ratio_residual == 0
        and generic.reference_to_evaluation_energy_ratio == expected_ratio,
    )
    checks.check(
        "generic logarithm retains the conversion ratio",
        generic.scale_logarithm == sp.log(expected_ratio)
        and generic.scale_logarithm.has(k0, k1, ell0, ell1),
    )
    checks.check(
        "generic affine composition retains the reference value",
        generic.kinetic.reference_value == local + finite
        and generic.kinetic.one_loop_coefficient == coefficient
        and generic.affine_composition_residual == 0
        and sp.simplify(
            generic.kinetic.kinetic_coefficient
            - local
            - finite
            - coefficient * sp.log(expected_ratio) / (8 * sp.pi**2)
        )
        == 0,
    )
    checks.mutation_sensitive(
        "generic scale-log formula",
        lambda candidate: sp.simplify(candidate - sp.log(expected_ratio)) == 0,
        generic.scale_logarithm,
        [
            sp.log(ell1 / ell0),
            sp.log(k1 * ell1 / (k0 * ell0)),
            sp.log(k0 * ell0 / (k1 * ell1)),
        ],
    )

    fixed_lengths = inverse_length_scale_kinetic_evidence(
        2,
        10,
        3,
        5,
        1,
        0,
        1,
        0,
    )
    conversion_mutation = inverse_length_scale_kinetic_evidence(
        2,
        10,
        6,
        5,
        1,
        0,
        1,
        0,
    )
    checks.check(
        "fixed-length conversion mutation changes the logarithm and total",
        sp.simplify(
            conversion_mutation.scale_logarithm - fixed_lengths.scale_logarithm
        )
        == sp.log(2)
        and conversion_mutation.kinetic.kinetic_coefficient
        != fixed_lengths.kinetic.kinetic_coefficient,
    )
    checks.check(
        "common length rescaling preserves only relative data",
        generic.common_rescaling_log_residual == 0
        and generic.rescaled_reference_energy
        == generic.reference_energy / generic.common_length_rescaling
        and generic.rescaled_evaluation_energy
        == generic.evaluation_energy / generic.common_length_rescaling
        and generic.rescaled_reference_energy != generic.reference_energy,
    )
    boundary_mutation = inverse_length_scale_kinetic_evidence(
        ell0,
        ell1,
        k0,
        k1,
        local + 7,
        finite,
        scalar,
        dirac,
    )
    checks.check(
        "affine boundary mutation changes total without changing scale data",
        boundary_mutation.scale_logarithm == generic.scale_logarithm
        and boundary_mutation.kinetic.one_loop_coefficient
        == generic.kinetic.one_loop_coefficient
        and sp.simplify(
            boundary_mutation.kinetic.kinetic_coefficient
            - generic.kinetic.kinetic_coefficient
        )
        == 7,
    )

    mu0, g2, b0 = sp.symbols("mu0 g2 b0", positive=True)
    positive_scalar, positive_dirac = sp.symbols("Wsp Wfp", positive=True)
    one_loop = one_loop_scale_matched_kinetic_evidence(
        mu0,
        g2,
        b0,
        reference_conversion=k0,
        transmuted_conversion=k1,
        renormalized_local_coefficient=local,
        finite_matching_offset=finite,
        scalar_weight=positive_scalar,
        dirac_weight=positive_dirac,
    )
    positive_coefficient = sp.simplify(positive_scalar / 3 + 4 * positive_dirac / 3)
    checks.check(
        "formal one-loop energy and length relations remain explicit",
        one_loop.transmutation.transmuted_energy
        == mu0 * sp.exp(-8 * sp.pi**2 / (b0 * g2))
        and one_loop.transmutation.transmuted_to_reference_length_ratio
        == k1 * sp.exp(8 * sp.pi**2 / (b0 * g2)) / k0,
    )
    checks.check(
        "unequal paired conversions cancel from the one-loop logarithm",
        one_loop.matched.reference_conversion == k0
        and one_loop.matched.evaluation_conversion == k1
        and k0 != k1
        and one_loop.matched.scale_logarithm == 8 * sp.pi**2 / (b0 * g2)
        and one_loop.scale_log_cancellation_residual == 0
        and one_loop.conversion_factors_need_not_be_equal,
    )
    checks.check(
        "general one-loop kinetic family retains Z_ref",
        sp.simplify(
            one_loop.general_kinetic_coefficient
            - local
            - finite
            - positive_coefficient / (b0 * g2)
        )
        == 0
        and one_loop.general_kinetic_residual == 0,
    )
    checks.check(
        "zero matching is a separate exact specialization",
        one_loop.zero_matching_is_separate_premise
        and sp.simplify(
            one_loop.zero_matching_kinetic_coefficient
            - positive_coefficient / (b0 * g2)
        )
        == 0
        and one_loop.zero_matching_residual == 0,
    )
    checks.check(
        "positive zero branch has the conditional inverse coordinate",
        sp.simplify(
            one_loop.zero_matching_inverse_kinetic_coordinate
            - b0 * g2 / positive_coefficient
        )
        == 0
        and one_loop.zero_matching_inverse_residual == 0
        and one_loop.physical_coupling_interpretation_is_separate_premise,
    )

    paired_first = one_loop_scale_matched_kinetic_evidence(
        13,
        2,
        3,
        reference_conversion=5,
        transmuted_conversion=7,
        renormalized_local_coefficient=0,
        finite_matching_offset=0,
        scalar_weight=1,
        dirac_weight=0,
    )
    paired_second = one_loop_scale_matched_kinetic_evidence(
        13,
        2,
        3,
        reference_conversion=11,
        transmuted_conversion=17,
        renormalized_local_coefficient=0,
        finite_matching_offset=0,
        scalar_weight=1,
        dirac_weight=0,
    )
    checks.check(
        "paired conversion mutation preserves energy ratio but changes lengths",
        paired_first.matched.scale_logarithm == paired_second.matched.scale_logarithm
        and paired_first.zero_matching_kinetic_coefficient
        == paired_second.zero_matching_kinetic_coefficient
        and paired_first.transmutation.reference_length
        != paired_second.transmutation.reference_length
        and paired_first.transmutation.transmuted_length
        != paired_second.transmutation.transmuted_length,
    )
    reversed_lengths = inverse_length_scale_kinetic_evidence(
        ell1,
        ell0,
        k0,
        k1,
        local,
        finite,
        scalar,
        dirac,
    )
    checks.check(
        "unpaired orientation mutation changes the generic logarithm",
        sp.simplify(reversed_lengths.scale_logarithm - generic.scale_logarithm)
        != 0,
    )

    constraint = two_length_log_constraint(
        one_loop.transmutation.transmuted_to_reference_length_ratio,
        provenance="C-RGE-003 paired length ratio",
    )
    checks.check(
        "one scale ratio leaves the common absolute direction free",
        constraint.linear.coefficient_rank == 1
        and constraint.linear.solution_dimension == 1
        and constraint.nullspace == (sp.ImmutableMatrix([1, 1]),)
        and constraint.coordinate_identifiable == (False, False),
    )

    zero_matter = inverse_length_scale_kinetic_evidence(1, 2, 1, 1, 3, 5, 0, 0)
    rejected_zero_inverse = False
    try:
        one_loop_scale_matched_kinetic_evidence(
            1,
            2,
            3,
            reference_conversion=1,
            transmuted_conversion=1,
            renormalized_local_coefficient=0,
            finite_matching_offset=0,
            scalar_weight=0,
            dirac_weight=0,
        )
    except ValueError:
        rejected_zero_inverse = True
    checks.check(
        "zero matter leaves the affine boundary and has no inverse zero branch",
        zero_matter.kinetic.kinetic_coefficient == 8
        and zero_matter.kinetic.zero_matching_kinetic_coefficient == 0
        and rejected_zero_inverse,
    )

    x = sp.Symbol("X", positive=True)
    y = sp.exp(x)
    checks.check(
        "power zero is a constant rather than a logarithm",
        sp.simplify(y**0 - 1) == 0 and sp.simplify(y**0 - sp.log(y)) != 0,
    )
    checks.check(
        "logarithm is not uniquely rational after transmutation",
        sp.simplify(sp.log(y) - x) == 0
        and sp.simplify(sp.log(y) ** 2 - x**2) == 0
        and sp.simplify(1 / sp.log(y) - 1 / x) == 0,
    )

    rejected_domains = 0
    invalid_calls = (
        lambda: inverse_length_scale_kinetic_evidence(0, 1, 1, 1, 0, 0, 1, 0),
        lambda: inverse_length_scale_kinetic_evidence(1, 1, 1, -1, 0, 0, 1, 0),
        lambda: one_loop_scale_matched_kinetic_evidence(
            sp.Float(1),
            2,
            3,
            reference_conversion=1,
            transmuted_conversion=1,
            renormalized_local_coefficient=0,
            finite_matching_offset=0,
            scalar_weight=1,
            dirac_weight=0,
        ),
    )
    for call in invalid_calls:
        try:
            call()
        except ValueError:
            rejected_domains += 1
    checks.check(
        "invalid domains and hidden floating inputs are rejected",
        rejected_domains == len(invalid_calls),
    )

    module_source = Path(matching_module.__file__).read_text(encoding="utf-8")
    module_compatibility = audit_numpy_trapezoid_compatibility(
        module_source,
        filename=str(matching_module.__file__),
    )
    module_scope = " ".join((matching_module.__doc__ or "").lower().split())
    checks.check(
        "canonical module preserves conditional scientific scope",
        all(
            phrase in module_scope
            for phrase in (
                "do not identify either length",
                "select a conversion factor or matching boundary",
                "physical gauge coupling",
            )
        ),
    )
    checks.check(
        "canonical module has no NumPy trapezoidal compatibility surface",
        module_compatibility.legacy_references == 0
        and module_compatibility.current_references == 0
        and module_compatibility.eager_legacy_default_fallbacks == 0,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
