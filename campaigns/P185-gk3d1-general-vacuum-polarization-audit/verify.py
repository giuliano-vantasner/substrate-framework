#!/usr/bin/env python3
"""Primary exact verifier for GK3D1 adjudication and C-VAC-002."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

import substrate_framework.dirac_vacuum_polarization as dirac_module
from substrate_framework.dirac_vacuum_polarization import (
    dirac_qed4_subtracted_timelike_evidence,
    dirac_qed4_zero_momentum_renormalization,
    dirac_representation_weight_evidence,
    dirac_vacuum_polarization_master,
    dirac_ward_integrand_evidence,
    massless_dirac_qed2_evidence,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-41/"
    "bridge_GK3D1_master_polarization_general_D.py"
)
SOURCE_SHA256 = "9a25110ba53adfb439d0cfd0570bd311b0a43a20f13d1351f45c3fa4075aeacb"
RELEASE_SHA256 = "40cac131cd3b8a874e5b91449b69ee804214c987a15b63eea4f00b0dcba12374"
FORMULA_FREEZE_SHA256 = (
    "9fef0bde55313f9d436808d3ecd7301ecfcc384ee5fdd4bad379590417b2bdbe"
)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P185-GK3D1-C-VAC-002")
    campaign = ROOT / "campaigns/P185-gk3d1-general-vacuum-polarization-audit"
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.136.0.yaml") == RELEASE_SHA256,
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
        len(lexical_checks) == 19 and len(assertions) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "GK3D1 has no NumPy trapezoidal compatibility surface",
        compatibility.current_references == 0
        and compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "source imposes rather than derives its transverse tensor",
        "Pi_up = (qsq * g_up - q_up * q_up.T) * Pi_s" in source_text
        and "ward = sp.simplify(q_dn.T * Pi_up)" in source_text,
    )
    checks.check(
        "source uses a discontinuous integer-only trace prescription",
        "return 2 ** (Dval // 2)" in source_text,
    )

    a, b, c, d = sp.symbols("a b c d", real=True)
    e0, f, g, h = sp.symbols("e0 f g h", real=True)
    u, v, w0, z = sp.symbols("u v w0 z", real=True)
    left = sp.Matrix([[a, b], [c, d]])
    right = sp.Matrix([[e0, f], [g, h]])
    vertex = sp.Matrix([[u, v], [w0, z]])
    ward = dirac_ward_integrand_evidence(left, right, vertex)
    checks.check(
        "free-loop Ward contraction is an exact shifted trace difference",
        ward.trace_cyclicity_residual == 0
        and ward.contracted_integrand_trace
        == ward.shifted_integrand_difference,
    )
    numeric_left = sp.Matrix([[2, 1], [1, 1]])
    numeric_right = sp.Matrix([[3, 1], [2, 1]])
    numeric_vertex = sp.Matrix([[1, 2], [3, 5]])
    numeric_ward = dirac_ward_integrand_evidence(
        numeric_left,
        numeric_right,
        numeric_vertex,
    )
    wrong_sign = sp.trace(
        (numeric_right.inv() + numeric_left.inv())
        * numeric_right
        * numeric_vertex
        * numeric_left
    )
    checks.check(
        "inverse-propagator-sign mutation breaks the Ward identity",
        sp.simplify(wrong_sign - numeric_ward.shifted_integrand_difference)
        != 0,
    )

    dimension = sp.Symbol("d", positive=True)
    momentum2, mass2, charge = sp.symbols("Q M2 e", positive=True)
    master = dirac_vacuum_polarization_master(
        dimension,
        6,
        momentum2,
        mass2,
        charge,
    )
    expected_prefactor = (
        -12
        * charge**2
        * sp.gamma(2 - dimension / 2)
        / (4 * sp.pi) ** (dimension / 2)
    )
    checks.check(
        "general master has the frozen exact Feynman-parameter normalization",
        sp.simplify(master.prefactor - expected_prefactor) == 0
        and sp.simplify(
            master.delta
            - (mass2 + master.parameter * (1 - master.parameter) * momentum2)
        )
        == 0,
    )
    checks.check(
        "integration dimension and spinor trace remain independent inputs",
        master.integration_dimension == dimension
        and master.spinor_trace == 6
        and not master.prefactor.has(sp.floor(dimension / 2)),
    )
    checks.check(
        "form factor and projector coefficient dimensions remain distinct",
        master.charge_squared_mass_dimension == 4 - dimension
        and master.delta_power_mass_dimension == dimension - 4
        and master.transverse_form_factor_mass_dimension == 0
        and master.projector_coefficient_mass_dimension == 2,
    )

    qed2 = massless_dirac_qed2_evidence(momentum2, charge)
    checks.check(
        "declared massless Dirac D2 endpoint gives the Schwinger coefficient",
        qed2.transverse_form_factor == -charge**2 / (sp.pi * momentum2)
        and qed2.minkowski_projector_coefficient == charge**2 / sp.pi,
    )
    checks.check(
        "D2 endpoint is explicitly not the accepted scalar massless limit",
        qed2.scalar_comparator_is_inapplicable
        and qed2.master.spinor_trace == 2
        and qed2.master.mass_squared == 0,
    )
    trace_mutation = dirac_vacuum_polarization_master(
        2,
        4,
        momentum2,
        0,
        charge,
    )
    mutated_d2 = sp.simplify(
        trace_mutation.prefactor
        * sp.integrate(
            trace_mutation.parameter_integrand,
            (trace_mutation.parameter, 0, 1),
        )
    )
    checks.check(
        "spinor-trace mutation doubles rather than preserves the D2 result",
        sp.simplify(mutated_d2 - 2 * qed2.transverse_form_factor) == 0
        and mutated_d2 != qed2.transverse_form_factor,
    )

    scale2 = sp.Symbol("mu2", positive=True)
    finite = sp.Symbol("c_fin", real=True)
    epsilon = sp.Symbol("epsilon", positive=True)
    qed4 = dirac_qed4_zero_momentum_renormalization(
        charge,
        mass2,
        scale2,
        finite,
        regulator=epsilon,
    )
    common = charge**2 / (12 * sp.pi**2)
    checks.check(
        "fixed-four-spinor D4 regulator has the exact frozen bare form",
        sp.simplify(
            qed4.bare_form_factor
            + common
            * sp.gamma(epsilon)
            * (4 * sp.pi * scale2 / mass2) ** epsilon
        )
        == 0,
    )
    checks.check(
        "D4 Laurent pole and finite part are exact",
        qed4.laurent_pole_residue == -common
        and sp.simplify(
            qed4.laurent_finite_part
            - common
            * (sp.log(mass2 / (4 * sp.pi * scale2)) + sp.EulerGamma)
        )
        == 0,
    )
    checks.check(
        "MS-bar counterterm leaves the declared finite local family",
        qed4.renormalization_residual == 0
        and sp.simplify(
            qed4.expected_renormalized_form_factor
            - common * sp.log(mass2 / scale2)
            - finite
        )
        == 0,
    )
    checks.check(
        "mass and regulator-scale logarithmic slopes have frozen signs",
        qed4.mass_squared_log_slope == common
        and qed4.mass_log_slope == 2 * common
        and qed4.scale_squared_log_slope == -common
        and qed4.scale_log_slope == -2 * common,
    )
    shifted_counterterm = dirac_qed4_zero_momentum_renormalization(
        charge,
        mass2,
        scale2,
        finite + 7,
        regulator=epsilon,
    )
    checks.check(
        "finite-counterterm mutation changes the total but not universal data",
        sp.simplify(
            shifted_counterterm.expected_renormalized_form_factor
            - qed4.expected_renormalized_form_factor
            - 7
        )
        == 0
        and shifted_counterterm.laurent_pole_residue
        == qed4.laurent_pole_residue
        and shifted_counterterm.mass_squared_log_slope
        == qed4.mass_squared_log_slope,
    )

    ratio = sp.Symbol("w", nonnegative=True)
    subtracted = dirac_qed4_subtracted_timelike_evidence(charge, ratio)
    subtracted_common = charge**2 / (2 * sp.pi**2)
    checks.check(
        "below-threshold subtraction has all three frozen series coefficients",
        subtracted.linear_coefficient == -subtracted_common / 30
        and subtracted.quadratic_coefficient == -subtracted_common / 280
        and subtracted.cubic_coefficient == -subtracted_common / 1890,
    )
    beta_coefficients = [
        -subtracted_common
        * sp.factorial(n + 1) ** 2
        / (n * sp.factorial(2 * n + 3))
        for n in range(1, 4)
    ]
    checks.check(
        "independent beta-integral coefficient formula matches the series",
        beta_coefficients
        == [
            subtracted.linear_coefficient,
            subtracted.quadratic_coefficient,
            subtracted.cubic_coefficient,
        ],
    )
    checks.check(
        "real subtraction stops at the first pair-production branch point",
        subtracted.feynman_weight_maximum == sp.Rational(1, 4)
        and subtracted.first_branch_point == 4
        and subtracted.convergence_radius == 4
        and subtracted.above_threshold_requires_i0,
    )
    threshold_mutations_rejected = 0
    for bad_ratio in (-1, 4, 5):
        try:
            dirac_qed4_subtracted_timelike_evidence(charge, bad_ratio)
        except ValueError:
            threshold_mutations_rejected += 1
    checks.check(
        "real-domain mutations at and beyond threshold are rejected",
        threshold_mutations_rejected == 3,
    )

    gauge_coupling, trace, rescaling = sp.symbols("g T c", positive=True)
    representation = dirac_representation_weight_evidence(
        gauge_coupling,
        trace,
        rescaling,
    )
    checks.check(
        "paired generator and coupling convention changes preserve loop weight",
        representation.convention_residual == 0
        and representation.original_loop_weight == gauge_coupling**2 * trace,
    )
    checks.check(
        "unpaired generator mutation changes rather than selects the loop weight",
        sp.simplify(
            gauge_coupling**2 * representation.rescaled_generator_trace
            - representation.original_loop_weight
        )
        != 0,
    )
    module_scope = (dirac_module.__doc__ or "").lower()
    checks.check(
        "canonical module excludes physical matter group and normalization claims",
        all(
            phrase in module_scope
            for phrase in (
                "do not derive a physical charged excitation",
                "gauge group",
                "bare maxwell coefficient",
                "total kinetic",
                "dimensional lift",
            )
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
