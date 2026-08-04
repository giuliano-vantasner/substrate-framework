#!/usr/bin/env python3
"""Exact source-aware verifier for the QCD1 claim delta."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.nonabelian_gauge import nonabelian_field_strength
from substrate_framework.nonabelian_vacuum_polarization import (
    finite_lie_scalar_qed2_vacuum_polarization,
    su2_scalar_qed2_vacuum_polarization,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.su3 import (
    fundamental_generators,
    structure_constant,
    symmetric_structure_constant,
    symmetric_tensor_evidence,
)
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P160-qcd1-su3-kinetic-induction-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-8/"
    "bridge_QCD1_su3_kinetic_induction.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_AUDIT = CAMPAIGN / "evidence/source-audit.yaml"
CHECK_ADJUDICATION = CAMPAIGN / "evidence/check-adjudication.yaml"
SOURCE_SHA256 = "b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed"
FROZEN_SHA256 = "2a2913f5249bce276edd71921b8c5706c2702be067b896d0bd8b33e4ecdfba43"
REVISION_SHA256 = "c65a96bceebdb9f800e758563ce6d83f6bbcea952553858f2197bc139dbb0ac0"
REPRODUCTION_SHA256 = "6d0f6d61a40dbbce93cdd262d854d412e98227c4e45e26603168fe0d7953a2c6"
SOURCE_AUDIT_SHA256 = "edac8a50e958a7dd786a9e912fabd439231f66d396264b790e0a4dc3c8e56d47"
CHECK_ADJUDICATION_SHA256 = (
    "405d1942a4375487d8e09fb2fec0eb6adb4c6f712ce18c5d1cbb7ecf14f2b87c"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _su2_generators() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return (
        sp.Matrix([[0, 1], [1, 0]]) / 2,
        sp.Matrix([[0, -sp.I], [sp.I, 0]]) / 2,
        sp.diag(1, -1) / 2,
    )


def _su3_constants() -> sp.ImmutableDenseNDimArray:
    return sp.ImmutableDenseNDimArray(
        [
            structure_constant(a, b, c)
            for a in range(8)
            for b in range(8)
            for c in range(8)
        ],
        (8, 8, 8),
    )


def run() -> int:
    checks = CheckLedger("P160/QCD1")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned QCD1 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("initial frozen proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    checks.check("source-aware revision hash", _sha256(REVISION) == REVISION_SHA256)
    checks.check("source reproduction hash", _sha256(REPRODUCTION) == REPRODUCTION_SHA256)
    checks.check("source audit hash", _sha256(SOURCE_AUDIT) == SOURCE_AUDIT_SHA256)
    checks.check(
        "predicate adjudication hash",
        _sha256(CHECK_ADJUDICATION) == CHECK_ADJUDICATION_SHA256,
    )

    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    assigned_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store)
    }
    integration_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "integrate"
    ]
    checks.check("eleven source predicates", len(source_checks) == 11)
    checks.check("one source assertion", len(source_assertions) == 1)

    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check(
        "QCD1 has no NumPy integration compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    native = subprocess.run(
        [sys.executable, str(SOURCE)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    native_lines = [line.strip() for line in native.stdout.splitlines() if line.strip()]
    checks.check("native QCD1 exits cleanly", native.returncode == 0)
    checks.check(
        "native QCD1 terminal tally is exact",
        native_lines.count("ALL 11 CHECKS PASS") == 1,
    )

    symmetric = symmetric_tensor_evidence()
    checks.check(
        "canonical SU3 d tensor is fully symmetric",
        symmetric.fully_symmetric and symmetric.tensor.shape == (8, 8, 8),
    )
    checks.check(
        "canonical SU3 d tensor standard values are exact",
        symmetric_structure_constant(0, 0, 7) == 1 / sp.sqrt(3)
        and symmetric_structure_constant(7, 7, 7) == -1 / sp.sqrt(3)
        and symmetric_structure_constant(0, 3, 5) == sp.Rational(1, 2),
    )
    checks.check(
        "all fundamental anticommutators reconstruct",
        all(residual == sp.zeros(3) for residual in symmetric.anticommutator_residuals),
    )
    checks.check(
        "d vanishes on the standard embedded SU2 only",
        symmetric.embedded_su2_all_zero
        and symmetric.outside_nonzero_witness == (0, 0, 7, 1 / sp.sqrt(3)),
    )
    generators = fundamental_generators()
    missing_identity = sp.simplify(
        generators[0] * generators[0]
        + generators[0] * generators[0]
        - sum(
            (symmetric.tensor[0, 0, c] * generators[c] for c in range(8)),
            sp.zeros(3),
        )
    )
    checks.check(
        "anticommutator identity term is load bearing",
        missing_identity == sp.eye(3) / 3 and missing_identity != sp.zeros(3),
    )
    doubled_generators = tuple(2 * generator for generator in generators)
    doubled_d118 = sp.simplify(
        2
        * sp.trace(
            (
                doubled_generators[0] * doubled_generators[0]
                + doubled_generators[0] * doubled_generators[0]
            )
            * doubled_generators[7]
        )
    )
    checks.check(
        "generator normalization mutation changes d cubically",
        doubled_d118 == 8 / sp.sqrt(3)
        and doubled_d118 != symmetric.tensor[0, 0, 7],
    )
    pauli = _su2_generators()
    pauli_d = [
        sp.simplify(
            2
            * sp.trace(
                (pauli[a] * pauli[b] + pauli[b] * pauli[a]) * pauli[c]
            )
        )
        for a in range(3)
        for b in range(3)
        for c in range(3)
    ]
    checks.check(
        "fresh Pauli comparison has no symmetric rank-three tensor",
        all(value == 0 for value in pauli_d),
    )

    q2, mass, coupling = sp.symbols("Q m g", positive=True)
    constants = _su3_constants()
    loop = finite_lie_scalar_qed2_vacuum_polarization(
        generators, constants, q2, mass, coupling, species_count=2
    )
    checks.check(
        "generic finite-Lie API validates fundamental SU3",
        loop.generator_count == 8
        and loop.carrier_dimension == 3
        and loop.trace_metric == sp.eye(8) / 2
        and loop.dynkin_index == sp.Rational(1, 2)
        and all(residual == sp.zeros(3) for residual in loop.commutator_residuals),
    )
    checks.check(
        "SU3 color kernel is the accepted scalar kernel times its trace metric",
        loop.color_projector_coefficient
        == sp.eye(8) * loop.abelian_ledger.projector_coefficient / 2,
    )
    checks.check(
        "bubble and seagull derive the color Ward cancellation",
        loop.bubble_ward_tadpole_coefficient == 2 * coupling**2 * sp.eye(8)
        and loop.seagull_ward_tadpole_coefficient == -2 * coupling**2 * sp.eye(8)
        and loop.ward_tadpole_residual == sp.zeros(8),
    )
    checks.check(
        "deleted or sign-flipped seagull breaks the Ward contraction",
        loop.bubble_ward_tadpole_coefficient != sp.zeros(8)
        and (
            loop.bubble_ward_tadpole_coefficient
            - loop.seagull_ward_tadpole_coefficient
        )
        != sp.zeros(8),
    )
    checks.check(
        "generic SU3 local component and trace coefficients are typed",
        loop.local_trace_fmunu_squared_coefficient
        == coupling**2 / (24 * sp.pi * mass**2)
        and loop.local_component_fmunu_squared_coefficient
        == coupling**2 / (48 * sp.pi * mass**2),
    )
    checks.check(
        "proper-time background coefficient closes the trace density",
        loop.heat_kernel_curvature_weight == sp.Rational(1, 12)
        and loop.heat_kernel_free_factor == 1 / (4 * sp.pi)
        and loop.proper_time_mass_integral == 1 / mass**2
        and loop.covariant_completion_residual == 0,
    )
    direct_sum = finite_lie_scalar_qed2_vacuum_polarization(
        tuple(sp.diag(generator, generator) for generator in generators),
        constants,
        q2,
        mass,
        coupling,
        species_count=2,
    )
    checks.check(
        "direct-sum representation mutation doubles the trace index",
        direct_sum.carrier_dimension == 6
        and direct_sum.dynkin_index == 1
        and sp.simplify(
            direct_sum.local_component_fmunu_squared_coefficient
            / loop.local_component_fmunu_squared_coefficient
        )
        == 2,
    )
    su2 = su2_scalar_qed2_vacuum_polarization(pauli, q2, mass, coupling)
    su2_constants = sp.ImmutableDenseNDimArray(
        [sp.LeviCivita(a, b, c) for a in range(3) for b in range(3) for c in range(3)],
        (3, 3, 3),
    )
    generic_su2 = finite_lie_scalar_qed2_vacuum_polarization(
        pauli, su2_constants, q2, mass, coupling
    )
    checks.check(
        "backward-compatible SU2 wrapper is an exact specialization",
        su2.trace_metric == generic_su2.trace_metric
        and su2.color_projector_coefficient
        == generic_su2.color_projector_coefficient
        and su2.covariant_completion_residual == 0,
    )

    x, y = sp.symbols("x y", real=True)
    full_curvature = nonabelian_field_strength(
        (generators[0], generators[1]), (x, y), coupling
    )
    checks.check(
        "noncommuting SU3 background exercises the nonlinear completion",
        full_curvature == coupling * generators[2]
        and sp.trace(full_curvature * full_curvature) == coupling**2 / 2,
    )
    checks.check(
        "curl-only mutation misses the constant noncommuting background",
        generators[1].diff(x) - generators[0].diff(y) == sp.zeros(3)
        and full_curvature != sp.zeros(3),
    )

    u = sp.Symbol("u", real=True)
    source_integrand = sp.simplify(
        u * (1 - u) * q2 / (mass**2 + u * (1 - u) * q2)
    )
    scalar_parameter = loop.abelian_ledger.parameter
    scalar_integrand = sp.factor(loop.abelian_ledger.projector_parameter_integrand)
    checks.check(
        "QCD1 numerator is not the declared complex-scalar numerator",
        sp.simplify(u * (1 - u) * q2 - (1 - 2 * u) ** 2) != 0
        and scalar_integrand.has((2 * scalar_parameter - 1) ** 2)
        and sp.simplify(
            source_integrand
            - scalar_integrand.subs(scalar_parameter, u)
        )
        != 0,
    )
    checks.check(
        "correct scalar fixed-Q massless limit diverges",
        loop.abelian_ledger.massless_projector_limit == sp.oo
        and loop.abelian_ledger.heavy_mass_projector_limit == 0,
    )
    source_projector_coefficient = coupling**2 / sp.pi
    source_curvature_form_factor = source_projector_coefficient / q2
    checks.check(
        "QCD1 constant projector coefficient is nonlocal in curvature variables",
        sp.limit(source_curvature_form_factor, q2, 0, dir="+") == sp.oo
        and sp.limit(loop.abelian_ledger.transverse_form_factor, q2, 0)
        == coupling**2 / (6 * sp.pi * mass**2),
    )
    absent_construction_names = {
        "bubble",
        "seagull",
        "functional_determinant",
        "field_strength",
        "curvature",
    }
    checks.check(
        "QCD1 executable constructs only a postulated projector loop",
        assigned_names.isdisjoint(absent_construction_names)
        and len(integration_calls) == 1
        and isinstance(integration_calls[0].args[0], ast.Name)
        and integration_calls[0].args[0].id == "integrand_m0"
        and "Pi_abelian = Pi_q2 * P" in source_text
        and "integrand_general = u * (1 - u) * q2s" in source_text,
    )
    checks.check(
        "QCD1 Abelian guard changes normalization manually",
        "single generator (colour factor -> 1)" in source_text
        and "abelian = {f_self: 0}" in source_text
        and "Pi_abelian_limit = (e**2 / sp.pi)" in source_text,
    )
    t8_trace = sp.trace(generators[7] * generators[7])
    checks.check(
        "fixed standard Cartan generator retains trace one half",
        t8_trace == sp.Rational(1, 2) and t8_trace != 1,
    )

    bare, counterterm = sp.symbols("c_bare c_ct", real=True)
    total = bare + counterterm + loop.local_component_fmunu_squared_coefficient
    checks.check(
        "bare and counterterm family defeats unique induction",
        sp.diff(total, bare) == 1
        and sp.diff(total, counterterm) == 1
        and total.subs(bare, 1) != total.subs(bare, 2),
    )
    checks.check(
        "source code uses Euclidean momentum despite mostly-plus prose",
        "Q2 = q0**2 + q1**2" in source_text and "1+1D metric (+,-)" in source_text,
    )

    mutable_audits = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        for path in (
            ROOT / "src/substrate_framework/nonabelian_vacuum_polarization.py",
            ROOT / "src/substrate_framework/su3.py",
            *CAMPAIGN.rglob("*.py"),
        )
    ]
    checks.check(
        "mutable P160 and canonical code have no legacy integration access",
        all(item.legacy_references == 0 for item in mutable_audits),
    )
    checks.check(
        "mutable P160 and canonical code have no eager legacy fallback",
        all(item.eager_legacy_default_fallbacks == 0 for item in mutable_audits),
    )

    tally = checks.finish()
    print(f"P160 PRIMARY ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
