#!/usr/bin/env python3
"""Exact source-aware verifier for proposed C-GSM-001 and M1."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.gauge_scalar_mass import (
    gauge_scalar_mass_evidence,
    positive_gauge_kinetic_mass_evidence,
    su2_u1_lower_doublet_mass_evidence,
    transform_gauge_quadratic_forms,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P154-m1-anderson-higgs-mass-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-7/"
    "bridge_M1_anderson_higgs_mass_matrix.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_AUDIT = CAMPAIGN / "evidence/source-audit.yaml"
SOURCE_SHA256 = "6e4a60d5c895fc6ce045ffebb9f9676710e86c9f553a0428292acbc9f78bc80f"
FROZEN_SHA256 = "95c0ebbbf3b9058183efcc878d8369fe74b389a73df522a58f07ae6067739089"
REVISION_SHA256 = "aa97d2b43db9878650592590215a6783adfb530309302f3ca6494512e040e582"
REPRODUCTION_SHA256 = "3fcb362d48b87f56a8ea260e791517151faa4086ef0bfaef1fd3b89eba02f643"
SOURCE_AUDIT_SHA256 = "c5135756a8a88c5687e33d4e7bba0734d95e499a6b3b124b024e54b251622bba"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _zero(matrix: sp.MatrixBase) -> bool:
    return sp.ImmutableMatrix(sp.Matrix(matrix).applyfunc(sp.simplify)) == sp.zeros(
        *matrix.shape
    )


def run() -> int:
    checks = CheckLedger("P154/C-GSM-001")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned M1 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("initial proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    checks.check("proposal revision hash", _sha256(REVISION) == REVISION_SHA256)
    checks.check("source reproduction hash", _sha256(REPRODUCTION) == REPRODUCTION_SHA256)
    checks.check("source audit hash", _sha256(SOURCE_AUDIT) == SOURCE_AUDIT_SHA256)
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check("nine source predicates", len(source_checks) == 9)
    checks.check(
        "one source assertion",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    source_compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "M1 has no numerical integration compatibility surface",
        source_compatibility.numpy_aliases == ()
        and source_compatibility.legacy_references == 0
        and source_compatibility.current_references == 0,
    )
    checks.check(
        "source CHECK8 changes sign and magnitude rather than sign alone",
        "g * gp / 2" in source_text
        and "same magnitude off-diagonal gives det 0" in source_text,
    )

    g, gp, v = sp.symbols("g gp v", positive=True)
    doublet = su2_u1_lower_doublet_mass_evidence(g, gp, v)
    evidence = doublet.general_evidence
    expected = v**2 / 4 * sp.Matrix(
        [
            [g**2, 0, 0, 0],
            [0, g**2, 0, 0],
            [0, 0, g**2, -g * gp],
            [0, 0, -g * gp, gp**2],
        ]
    )
    checks.check(
        "generic anticommutator and twice-real-Gram routes agree",
        evidence.gram_identity_certified,
    )
    checks.check(
        "canonical doublet mass matrix has the one-half real-field normalization",
        evidence.mass_matrix == expected,
    )

    gauge_fields = sp.symbols("W1 W2 W3 B", real=True)
    connection_on_vacuum = sum(
        (
            field * coupling * generator * evidence.vacuum
            for field, coupling, generator in zip(
                gauge_fields, evidence.couplings, evidence.generators, strict=True
            )
        ),
        sp.zeros(2, 1),
    )
    direct_density = sp.simplify(
        (connection_on_vacuum.H * connection_on_vacuum)[0]
    )
    direct_hessian = sp.ImmutableMatrix(sp.hessian(direct_density, gauge_fields))
    checks.check(
        "direct scalar kinetic expansion independently gives the API Hessian",
        _zero(direct_hessian - evidence.mass_matrix),
    )
    checks.check(
        "quadratic-density helper reproduces the direct scalar kinetic term",
        sp.simplify(evidence.quadratic_density(gauge_fields) - direct_density) == 0,
    )

    coefficients = sp.Matrix(sp.symbols("x0:4", real=True))
    combined_orbit = evidence.coupled_orbit_vectors * coefficients
    checks.check(
        "PSD identity evaluates the claimed object for arbitrary real coefficients",
        sp.simplify(
            (coefficients.T * evidence.mass_matrix * coefficients)[0]
            - 2 * (combined_orbit.H * combined_orbit)[0]
        )
        == 0,
    )
    checks.check(
        "real stabilizer kernel is certified by orbit and mass maps",
        evidence.stabilizer_kernel_certified
        and evidence.orbit_rank == evidence.mass_rank == 3
        and evidence.stabilizer_dimension == 1,
    )
    checks.check(
        "charge generator annihilates only the declared lower vacuum direction",
        _zero(doublet.charge_vacuum_residual),
    )
    checks.check(
        "neutral null and massive vectors satisfy exact eigen-equations",
        _zero(doublet.neutral_mass_matrix * doublet.neutral_null_vector)
        and _zero(
            doublet.neutral_mass_matrix * doublet.neutral_massive_vector
            - doublet.neutral_mass_squared * doublet.neutral_massive_vector
        ),
    )
    checks.check(
        "charged coefficient and conditional rho identity are exact",
        doublet.charged_mass_squared == g**2 * v**2 / 4
        and doublet.rho == 1,
    )

    sigma_x = sp.Matrix([[0, 1], [1, 0]])
    sigma_y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    complex_columns = gauge_scalar_mass_evidence(
        (sigma_x, sigma_y),
        (sp.Integer(1), sp.Integer(1)),
        sp.Matrix([1, 0]),
    )
    checks.check(
        "realification rejects a complex-only coefficient relation",
        complex_columns.coupled_orbit_vectors[:, 1]
        == sp.I * complex_columns.coupled_orbit_vectors[:, 0]
        and complex_columns.real_orbit_map.rank() == 2
        and complex_columns.coefficient_kernel_dimension == 0,
    )

    k_su2, k_u1 = sp.symbols("K_W K_B", positive=True)
    kinetic = sp.diag(k_su2, k_su2, k_su2, k_u1)
    kinetic_evidence = positive_gauge_kinetic_mass_evidence(
        evidence.mass_matrix,
        kinetic,
    )
    neutral_operator = kinetic_evidence.generalized_mass_operator.extract(
        (2, 3), (2, 3)
    )
    generalized_neutral_mass = sp.simplify(
        v**2 * (g**2 / k_su2 + gp**2 / k_u1) / 4
    )
    checks.check(
        "positive kinetic metric produces the generalized mass operator",
        sp.simplify(
            kinetic * kinetic_evidence.generalized_mass_operator
            - evidence.mass_matrix
        )
        == sp.zeros(4),
    )
    checks.check(
        "noncanonical neutral generalized spectrum differs from raw M2",
        sp.simplify(neutral_operator.det()) == 0
        and sp.simplify(neutral_operator.trace() - generalized_neutral_mass) == 0
        and sp.simplify(
            kinetic_evidence.generalized_mass_operator[0, 0]
            - g**2 * v**2 / (4 * k_su2)
        )
        == 0,
    )
    checks.check(
        "mass null remains null for every accepted positive kinetic metric",
        kinetic_evidence.kernel_certified,
    )

    neutral = doublet.neutral_mass_matrix
    sign_flip = sp.diag(1, -1)
    congruence = transform_gauge_quadratic_forms(neutral, sp.eye(2), sign_flip)
    checks.check(
        "B sign congruence flips the off-diagonal and preserves the paired forms",
        congruence.transformed_mass_matrix[0, 1] == g * gp * v**2 / 4
        and congruence.transformed_kinetic_metric == sp.eye(2)
        and congruence.generalized_spectrum_covariant
        and congruence.original_nullity == congruence.transformed_nullity == 1,
    )
    sign_only_bad = v**2 / 4 * sp.Matrix(
        [[g**2, g * gp], [g * gp, gp**2]]
    )
    source_bad = v**2 / 4 * sp.Matrix(
        [[g**2, g * gp / 2], [g * gp / 2, gp**2]]
    )
    checks.check(
        "pure sign mutation falsifies the source guard description",
        sp.simplify(sign_only_bad.det()) == 0
        and sp.simplify(source_bad.det() - 3 * g**2 * gp**2 * v**4 / 64) == 0,
    )

    half_hessian = direct_hessian / 2
    checks.check(
        "factor-two mutation fails the scalar quadratic Hessian",
        not _zero(half_hessian - evidence.mass_matrix),
    )
    doubled_generators = gauge_scalar_mass_evidence(
        tuple(2 * generator for generator in evidence.generators),
        evidence.couplings,
        evidence.vacuum,
    )
    checks.check(
        "generator-normalization mutation changes the entire mass matrix",
        doubled_generators.mass_matrix == 4 * evidence.mass_matrix,
    )
    upper_vacuum = gauge_scalar_mass_evidence(
        evidence.generators,
        evidence.couplings,
        sp.Matrix([v / sp.sqrt(2), 0]),
    )
    checks.check(
        "vacuum-direction mutation flips the fixed-basis neutral sign",
        upper_vacuum.mass_matrix[2, 3] == g * gp * v**2 / 4
        and upper_vacuum.mass_matrix[2, 3] == -evidence.mass_matrix[2, 3],
    )
    doubled_u1 = gauge_scalar_mass_evidence(
        (*evidence.generators[:3], 2 * evidence.generators[3]),
        evidence.couplings,
        evidence.vacuum,
    )
    checks.check(
        "Abelian-generator normalization mutation changes mixing and diagonal",
        doubled_u1.mass_matrix[2, 3] == 2 * evidence.mass_matrix[2, 3]
        and doubled_u1.mass_matrix[3, 3] == 4 * evidence.mass_matrix[3, 3],
    )
    zero_vacuum = gauge_scalar_mass_evidence(
        evidence.generators,
        evidence.couplings,
        sp.zeros(2, 1),
    )
    checks.check(
        "zero-vacuum limit removes the complete quadratic matrix",
        zero_vacuum.mass_matrix == sp.zeros(4)
        and zero_vacuum.mass_rank == 0,
    )
    zero_coupling = gauge_scalar_mass_evidence(
        evidence.generators,
        (g, g, g, sp.Integer(0)),
        evidence.vacuum,
    )
    checks.check(
        "zero-coupling mutation invalidates the generator-stabilizer premise",
        not zero_coupling.all_couplings_nonzero
        and zero_coupling.coefficient_kernel_dimension == 1,
    )

    root_two = sp.sqrt(2)
    triplet = gauge_scalar_mass_evidence(
        (
            sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) / root_two,
            sp.Matrix(
                [[0, -sp.I, 0], [sp.I, 0, -sp.I], [0, sp.I, 0]]
            )
            / root_two,
            sp.diag(1, 0, -1),
        ),
        (g, g, g),
        sp.Matrix([0, v, 0]),
    )
    checks.check(
        "alternative triplet representation changes rank and coefficients",
        triplet.mass_matrix
        == sp.diag(2 * g**2 * v**2, 2 * g**2 * v**2, 0)
        and triplet.mass_rank == 2,
    )

    condensate_label, photon_label, standard_model_label = sp.symbols(
        "condensate_label photon_label standard_model_label"
    )
    checks.check(
        "identical mass matrix leaves physical dictionaries free",
        all(
            label not in evidence.mass_matrix.free_symbols
            for label in (condensate_label, photon_label, standard_model_label)
        ),
    )

    mutable_python = sorted(CAMPAIGN.rglob("*.py")) + [
        ROOT / "src/substrate_framework/gauge_scalar_mass.py",
        ROOT / "tests/test_gauge_scalar_mass.py",
    ]
    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        for path in mutable_python
    ]
    checks.check(
        "mutable P154 and canonical code has no executable legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )

    tally = checks.finish()
    print(f"P154 PRIMARY ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
