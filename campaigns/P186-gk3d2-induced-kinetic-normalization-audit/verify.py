#!/usr/bin/env python3
"""Primary exact verifier for GK3D2 adjudication and C-VAC-003."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

import substrate_framework.vacuum_polarization as scalar_module
from substrate_framework.dirac_vacuum_polarization import (
    dirac_qed4_zero_momentum_renormalization,
)
from substrate_framework.gauge_beta import (
    GaugeFactor,
    ProductMultiplet,
    product_gauge_coefficients,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.vacuum_polarization import (
    matter_induced_kinetic_evidence,
    scalar_qed4_zero_momentum_renormalization,
    scalar_vacuum_polarization_master,
    scalar_ward_integrand_evidence,
)
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-41/"
    "bridge_GK3D2_induced_kinetic_normalization.py"
)
RUNG25 = Path(
    "/home/dan/substrate/pulson-backreaction-bridge/sympy/imported/"
    "pulson-clock-qm/rung25_gauge_clock_holonomy_no_go.py"
)
SOURCE_SHA256 = "856096aba38812dc17fb07ce5cf7c0fa13eb2623665ccf871810734ac3ca0886"
RUNG25_SHA256 = "a69197cd1925560af122f268edb71738ecc896df3a61f557ef9daf26d4bbd2fa"
RELEASE_SHA256 = "874abae995ffc0ad883255bee7f754383b0aa183cf88aa44fa77ce9712b9a55e"
FORMULA_FREEZE_SHA256 = (
    "70ee71c81829f880ee770ee7efafeee0fb03889ff026c00e934b7b16e3183022"
)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P186-GK3D2-C-VAC-003")
    campaign = ROOT / "campaigns/P186-gk3d2-induced-kinetic-normalization-audit"
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check("rung25 hash remains pinned", _digest(RUNG25) == RUNG25_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.137.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "corrected formula freeze remains pinned",
        _digest(campaign / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    lexical_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source predicate inventory remains exact",
        len(lexical_checks) == 17 and len(assertions) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "GK3D2 has no NumPy trapezoidal compatibility surface",
        compatibility.current_references == 0
        and compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "source scalar helper omits the load-bearing quantum derivation",
        "def log_slope(numerator, prefactor_const):" in source_text
        and "seagull" not in source_text.lower()
        and "tr log" not in source_text.lower()
        and "epsilon" not in source_text.lower(),
    )

    rung25_text = RUNG25.read_text(encoding="utf-8")
    checks.check(
        "rung25 contains no kinetic matching datum",
        all(
            token not in rung25_text
            for token in ("Z_bare", "counterterm", "matching scale", "Lambda")
        ),
    )
    checks.check(
        "source promotes rung25 beyond its actual surface",
        "Z_bare(Lambda)" in source_text
        and "rung25 SUPPLIES" in source_text
        and "Z = sp.Function(\"Z\")" in source_text,
    )

    ward = scalar_ward_integrand_evidence()
    checks.check(
        "scalar bubble and seagull close the Ward contraction",
        ward.denominator_difference_residual == 0
        and ward.shifted_bubble_numerator_difference
        == 2 * ward.transfer_component
        and ward.integrated_ward_residual == 0
        and ward.integrated_cancellation_requires_shift_invariance,
    )
    wrong_seagull = sp.simplify(
        ward.shifted_bubble_contraction - ward.seagull_contraction
    )
    checks.check(
        "seagull-sign mutation breaks rather than preserves transversality",
        wrong_seagull != 0,
    )

    dimension = sp.Symbol("d", positive=True)
    momentum2, mass2, charge = sp.symbols("Q M2 e", positive=True)
    master = scalar_vacuum_polarization_master(
        dimension,
        momentum2,
        mass2,
        charge,
        species_count=3,
    )
    x = master.parameter
    expected_prefactor = (
        -3
        * charge**2
        * sp.gamma(2 - dimension / 2)
        / (4 * sp.pi) ** (dimension / 2)
    )
    checks.check(
        "general scalar master has the frozen bubble-seagull weight",
        sp.simplify(master.parameter_weight - (1 - 2 * x) ** 2) == 0
        and sp.simplify(master.prefactor - expected_prefactor) == 0
        and sp.simplify(
            master.delta - (mass2 + x * (1 - x) * momentum2)
        )
        == 0,
    )
    checks.check(
        "general scalar master is dimensionless in the declared convention",
        master.charge_squared_mass_dimension == 4 - dimension
        and master.delta_power_mass_dimension == dimension - 4
        and master.transverse_form_factor_mass_dimension == 0,
    )

    scale2 = sp.Symbol("mu2", positive=True)
    finite = sp.Symbol("c_fin", real=True)
    epsilon = sp.Symbol("epsilon", positive=True)
    scalar = scalar_qed4_zero_momentum_renormalization(
        charge,
        mass2,
        scale2,
        finite,
        species_count=2,
        regulator=epsilon,
    )
    common = charge**2 / (24 * sp.pi**2)
    checks.check(
        "complex-scalar D4 bare form and Laurent residue are exact",
        scalar.parameter_weight_integral == sp.Rational(1, 3)
        and sp.simplify(
            scalar.bare_form_factor
            + common
            * sp.gamma(epsilon)
            * (4 * sp.pi * scale2 / mass2) ** epsilon
        )
        == 0
        and scalar.laurent_pole_residue == -common,
    )
    checks.check(
        "MS-bar subtraction leaves the finite local family",
        scalar.renormalization_residual == 0
        and sp.simplify(
            scalar.expected_renormalized_form_factor
            - common * sp.log(mass2 / scale2)
            - finite
        )
        == 0,
    )
    checks.check(
        "scalar logarithmic slopes and beta coefficient have frozen signs",
        scalar.mass_squared_log_slope == common
        and scalar.mass_log_slope == 2 * common
        and scalar.scale_squared_log_slope == -common
        and scalar.scale_log_slope == -2 * common
        and scalar.beta_coupling == charge**3 / (24 * sp.pi**2),
    )
    shifted_scalar = scalar_qed4_zero_momentum_renormalization(
        charge,
        mass2,
        scale2,
        finite + 7,
        species_count=2,
        regulator=epsilon,
    )
    checks.check(
        "finite-counterterm mutation changes the total but not universal data",
        sp.simplify(
            shifted_scalar.expected_renormalized_form_factor
            - scalar.expected_renormalized_form_factor
        )
        == 7
        and shifted_scalar.laurent_pole_residue == scalar.laurent_pole_residue
        and shifted_scalar.mass_squared_log_slope
        == scalar.mass_squared_log_slope,
    )

    one_scalar = scalar_qed4_zero_momentum_renormalization(
        charge,
        mass2,
        scale2,
    )
    one_dirac = dirac_qed4_zero_momentum_renormalization(
        charge,
        mass2,
        scale2,
    )
    checks.check(
        "Dirac and complex-scalar slopes have exact factor four",
        sp.simplify(
            one_dirac.mass_squared_log_slope
            / one_scalar.mass_squared_log_slope
        )
        == 4
        and sp.simplify(one_dirac.scale_log_slope / one_scalar.scale_log_slope)
        == 4,
    )

    scalar_weight, dirac_weight = sp.symbols("W_s W_f", nonnegative=True)
    beta_ledger = product_gauge_coefficients(
        [GaugeFactor("u1", 0, is_abelian=True)],
        [
            ProductMultiplet(
                "scalar",
                "complex_scalar",
                1,
                (scalar_weight,),
                (0,),
            ),
            ProductMultiplet(
                "dirac_as_two_weyl",
                "weyl_fermion",
                2,
                (dirac_weight,),
                (0,),
            ),
        ],
    )
    family = matter_induced_kinetic_evidence(
        1,
        2,
        0,
        0,
        scalar_weight,
        dirac_weight,
    )
    checks.check(
        "derived matter weights match the accepted generic beta ledger",
        beta_ledger.one_loop_gauge == (0,)
        and beta_ledger.one_loop[0] == family.one_loop_coefficient
        and family.scalar_coefficient == scalar_weight / 3
        and family.dirac_coefficient == 4 * dirac_weight / 3,
    )
    checks.mutation_sensitive(
        "matter coefficient normalization",
        lambda candidate: sp.simplify(
            candidate - (scalar_weight / 3 + 4 * dirac_weight / 3)
        )
        == 0,
        family.one_loop_coefficient,
        [
            scalar_weight / 3 + dirac_weight / 3,
            4 * scalar_weight / 3 + dirac_weight / 3,
            -(scalar_weight / 3 + 4 * dirac_weight / 3),
        ],
    )

    scale, reference = sp.symbols("mu mu_ref", positive=True)
    local, matching = sp.symbols("Z_local c_matching", real=True)
    affine = matter_induced_kinetic_evidence(
        scale,
        reference,
        local,
        matching,
        scalar_weight,
        dirac_weight,
    )
    expected_b = scalar_weight / 3 + 4 * dirac_weight / 3
    checks.check(
        "affine solution retains its independent reference value",
        affine.reference_value == local + matching
        and sp.simplify(
            affine.kinetic_coefficient
            - local
            - matching
            - expected_b * sp.log(reference / scale) / (8 * sp.pi**2)
        )
        == 0
        and affine.flow_residual == 0,
    )
    checks.check(
        "same one-loop slope admits unequal boundary values",
        affine.boundary_mutation_residual == 0
        and sp.simplify(
            affine.boundary_mutated_kinetic_coefficient
            - affine.kinetic_coefficient
        )
        == affine.boundary_mutation,
    )
    checks.check(
        "scheme and reference coordinate changes preserve the total function",
        affine.scheme_decomposition_residual == 0
        and affine.reference_covariance_residual == 0
        and affine.transformed_reference_value != affine.reference_value,
    )

    zero_uv_above = matter_induced_kinetic_evidence(1, 2, 0, 0, 1, 0)
    zero_uv_below = matter_induced_kinetic_evidence(2, 1, 0, 0, 1, 0)
    positive_offset = matter_induced_kinetic_evidence(2, 1, 10, 0, 1, 0)
    negative_offset = matter_induced_kinetic_evidence(1, 2, -10, 0, 1, 0)
    checks.check(
        "zero matching has the conditional scale-ordering sign",
        zero_uv_above.zero_matching_kinetic_coefficient.is_positive is True
        and zero_uv_below.zero_matching_kinetic_coefficient.is_negative is True
        and zero_uv_above.zero_matching_is_separate_premise,
    )
    checks.check(
        "general positivity is not selected by scale ordering",
        positive_offset.kinetic_coefficient.is_positive is True
        and negative_offset.kinetic_coefficient.is_negative is True,
    )

    rejected_domains = 0
    for args in (
        (0, 1, 1, 0, 1),
        (1, 0, 1, 0, 1),
        (1, 1, 1, 0, 0),
    ):
        try:
            scalar_qed4_zero_momentum_renormalization(
                args[0],
                args[1],
                args[2],
                args[3],
                species_count=args[4],
            )
        except (TypeError, ValueError):
            rejected_domains += 1
    try:
        matter_induced_kinetic_evidence(1, 1, sp.Float(1), 0, 1, 0)
    except ValueError:
        rejected_domains += 1
    checks.check(
        "domain mutations and hidden floating coordinates are rejected",
        rejected_domains == 4,
    )

    module_scope = " ".join((scalar_module.__doc__ or "").lower().split())
    checks.check(
        "canonical module preserves its conditional scientific scope",
        all(
            phrase in module_scope
            for phrase in (
                "separately declared euclidean scalar-qed functional determinant",
                "does not quantize the framework's accepted classical complex field",
                "derive a physical gauge sector",
                "massive complex scalar",
                "scalar bubble and seagull",
            )
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
