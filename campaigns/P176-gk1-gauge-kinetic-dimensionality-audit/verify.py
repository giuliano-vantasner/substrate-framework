#!/usr/bin/env python3
"""Exact source-aware verifier for GK1 and proposed C-DIM-009."""

from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys

import sympy as sp
import yaml

from substrate_framework.gauge_dimensions import (
    canonical_gauge_dimensions,
    connection_gauge_dimensions,
    four_dimensional_form_factor_examples,
    gauge_convention_translation,
    polarization_dimensions,
    representation_rescaling,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.su2_doublets import su2_fundamental_ledger
from substrate_framework.su3 import fundamental_generators
from substrate_framework.vacuum_polarization import (
    scalar_qed2_vacuum_polarization,
)
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P176-gk1-gauge-kinetic-dimensionality-audit"
BASE_RELEASE = ROOT / "governance/releases/v0.127.0.yaml"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-35/"
    "bridge_GK1_gauge_kinetic_dimensionality_boundary.py"
)
PINNED_HASHES = {
    SOURCE: "c142538897e9168769483aeb978ea86587fa9a073e606aa204316238dfa24d74",
    CAMPAIGN / "evidence/frozen-proposal.yaml": (
        "291c21f5ce0fe61a427ec1e6037626f5131ce2d7e8b5129cedbf951953ca0c4f"
    ),
    CAMPAIGN / "evidence/proposal-revision-0001.yaml": (
        "10e122e32527c608c0ad05daf962bc6eda7e49473638ad82504d0252b1f487c6"
    ),
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_source() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SOURCE)],
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def _pure_coupling_dimension(candidate: object) -> bool:
    ledger = polarization_dimensions(sp.sympify(candidate))
    return ledger.pure_coupling_residual == 0


def _mass_completion_power(candidate: object) -> bool:
    dimension = sp.Symbol("D", positive=True)
    exponent = sp.sympify(candidate)
    return sp.simplify((4 - dimension) + exponent - 2) == 0


def _connection_coefficient_power(candidate: object) -> bool:
    coupling, coefficient, curvature = sp.symbols("g kappa F", positive=True)
    power = sp.sympify(candidate)
    canonical_density = coefficient * curvature**2 / 4
    connection_density = coefficient / coupling**power * (coupling * curvature) ** 2 / 4
    return sp.simplify(connection_density - canonical_density) == 0


def _generator_coupling_power(candidate: object) -> bool:
    coupling, trace_index, scale = sp.symbols("g T_R rho", positive=True)
    power = sp.sympify(candidate)
    original = coupling**2 * trace_index
    transformed = (coupling / scale**power) ** 2 * scale**2 * trace_index
    return sp.simplify(transformed - original) == 0


def main() -> int:
    checks = CheckLedger("P176-GK1-C-DIM-009")
    for path, expected in PINNED_HASHES.items():
        checks.check(
            f"pinned artifact {path.name} retains its audited bytes",
            _digest(path) == expected,
        )

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    source_calls = sorted(
        (
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
        ),
        key=lambda node: node.lineno,
    )
    labels = [
        re.match(r"GK1\.(\d+)", ast.literal_eval(node.args[0])).group(0)
        for node in source_calls
    ]
    checks.check(
        "GK1 has exactly eleven advertised predicates in order",
        labels == [f"GK1.{index}" for index in range(1, 12)],
    )
    checks.check(
        "GK1 has one assertion and only os and SymPy imports",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1
        and {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        == {"os", "sympy"},
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "GK1 has no NumPy integration compatibility surface",
        compatibility.numpy_aliases == ()
        and compatibility.current_references == 0
        and compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    native = _run_source()
    checks.check(
        "native GK1 executes eleven predicates and its terminal tally",
        native.returncode == 0
        and native.stderr == ""
        and len(re.findall(r"  PASS$", native.stdout, flags=re.MULTILINE)) == 11
        and native.stdout.count("ALL 11 CHECKS PASS") == 1,
        native.stderr[-500:],
    )

    su2 = su2_fundamental_ledger().generators
    su3 = fundamental_generators()
    su2_trace = sp.Matrix(
        3, 3, lambda first, second: sp.trace(su2[first] * su2[second])
    )
    su3_trace = sp.Matrix(
        8, 8, lambda first, second: sp.trace(su3[first] * su3[second])
    )
    checks.check(
        "accepted standard SU2 and SU3 bases have the displayed trace indices",
        su2_trace == sp.eye(3) / 2 and su3_trace == sp.eye(8) / 2,
    )

    dimension = sp.Symbol("D", positive=True)
    canonical = canonical_gauge_dimensions(dimension)
    connection = connection_gauge_dimensions(dimension)
    checks.check(
        "canonical field coupling curvature and projector dimensions close",
        canonical.potential == (dimension - 2) / 2
        and canonical.coupling == (4 - dimension) / 2
        and canonical.coupling_squared == 4 - dimension
        and canonical.curvature == dimension / 2
        and canonical.curvature_squared == dimension
        and canonical.projector_coefficient == 2,
    )
    checks.check(
        "connection field curvature and kinetic coefficient dimensions close",
        connection.connection_potential == 1
        and connection.connection_curvature == 2
        and connection.connection_curvature_squared == 4
        and connection.kinetic_coefficient == dimension - 4,
    )
    checks.mutation_sensitive(
        "the pure-coupling dimension-two projector selects D equals two",
        _pure_coupling_dimension,
        2,
        [3, 4],
    )

    polarization = polarization_dimensions(dimension)
    checks.check(
        "the pure-coupling result is narrow and the mass-scale family is general",
        polarization.pure_coupling_residual == 2 - dimension
        and polarization.unique_pure_coupling_dimension == 2
        and polarization.scale_completion_mass_power == dimension - 2
        and polarization.scale_completed_dimension == 2
        and polarization.scale_completed_residual == 0,
    )
    checks.mutation_sensitive(
        "the completing mass power is load bearing",
        _mass_completion_power,
        dimension - 2,
        [dimension - 3, dimension - 1],
    )

    coupling, coefficient = sp.symbols("g kappa", positive=True)
    translation = gauge_convention_translation(
        dimension, coupling, coefficient
    )
    checks.check(
        "canonical and connection densities are exactly identical",
        translation.connection_potential
        == coupling * translation.canonical_potential
        and translation.connection_curvature
        == coupling * translation.canonical_curvature
        and translation.connection_coefficient == coefficient / coupling**2
        and translation.density_residual == 0,
    )
    checks.mutation_sensitive(
        "the inverse coupling-squared coefficient is load bearing",
        _connection_coefficient_power,
        2,
        [0, 1, 3],
    )

    trace_index, generator_scale = sp.symbols("T_R rho", positive=True)
    rescaling = representation_rescaling(
        trace_index, coupling, generator_scale
    )
    checks.check(
        "generator and inverse-coupling rescaling preserves the loop weight",
        rescaling.rescaled_trace_index == generator_scale**2 * trace_index
        and rescaling.rescaled_coupling == coupling / generator_scale
        and rescaling.rescaled_weight == coupling**2 * trace_index
        and rescaling.invariant_residual == 0,
    )
    checks.mutation_sensitive(
        "the inverse generator-scale power is load bearing",
        _generator_coupling_power,
        1,
        [0, 2],
    )

    q2, mass = sp.symbols("Q M", positive=True)
    form_factors = four_dimensional_form_factor_examples(q2, mass)
    checks.check(
        "constant rational and logarithmic form factors are all scale invariant",
        all(value == 0 for value in form_factors.form_factor_scale_residuals)
        and all(value == 0 for value in form_factors.projector_scale_residuals),
    )
    checks.check(
        "four-dimensional homogeneity does not uniquely select a logarithm",
        sp.simplify(
            form_factors.constant_form_factor
            - form_factors.rational_form_factor
        )
        != 0
        and sp.simplify(
            form_factors.rational_form_factor
            - form_factors.logarithmic_form_factor
        )
        != 0,
    )

    scalar_loop = scalar_qed2_vacuum_polarization(
        q2, mass, coupling, species_count=2
    )
    scalar_translation = gauge_convention_translation(
        2,
        coupling,
        scalar_loop.local_fmunu_squared_coefficient,
    )
    checks.check(
        "the accepted scalar-QED2 local coefficient maps between conventions",
        scalar_loop.local_fmunu_squared_coefficient
        == coupling**2 / (24 * sp.pi * mass**2)
        and scalar_translation.connection_coefficient
        == 1 / (24 * sp.pi * mass**2)
        and scalar_translation.density_residual == 0,
    )
    checks.check(
        "the accepted scalar loop rejects GK1's massless fermion-shaped value",
        scalar_loop.massless_projector_limit == sp.oo
        and "integrand = u * (1 - u)" in source_text
        and "integrand_m0 == 1 and I_m0 == 1" in source_text,
    )

    check_five_condition = ast.unparse(source_calls[4].args[1])
    checks.check(
        "GK1's claimed Abelian limit is division by its own trace value",
        "Pi_group(Tr_su3, 0, 0) / Tr_su3[0, 0]" in source_text
        and "abelian_limit_exact and same_integral" == check_five_condition,
    )
    checks.check(
        "a convention-preserving rescaling changes trace and coupling together",
        rescaling.rescaled_trace_index != trace_index
        and rescaling.rescaled_coupling != coupling
        and rescaling.invariant_residual == 0,
    )

    check_seven_condition = ast.unparse(source_calls[6].args[1])
    checks.check(
        "GK1.7 verifies only the pure-coupling dimension ansatz",
        "dim_e2" in check_seven_condition
        and "D_solutions" in check_seven_condition
        and "m_mass" not in check_seven_condition
        and "q2s" not in check_seven_condition,
    )
    checks.check(
        "the mass-scale counterfamily defeats the universal constant no-go",
        polarization.scale_completed_residual == 0
        and polarization.pure_coupling_residual.subs(dimension, 4) == -2,
    )
    checks.check(
        "the form-factor counterfamily defeats logarithm selection by dimensions",
        form_factors.constant_form_factor == 1
        and form_factors.rational_form_factor == q2 / (mass**2 + q2)
        and form_factors.logarithmic_form_factor == sp.log(1 + q2 / mass**2),
    )

    d, s, radius, effective_coupling = sp.symbols(
        "d s r g_eff", positive=True
    )
    normalized_riesz = (
        sp.gamma(d / 2 - s)
        / (sp.pi ** (d / 2) * 4**s * sp.gamma(s))
        * radius ** (2 * s - d)
    )
    checks.check(
        "GK1's normalized Riesz expression omits kinetic normalization by construction",
        effective_coupling not in normalized_riesz.free_symbols
        and sp.diff(normalized_riesz, effective_coupling) == 0
        and "G_riesz = c_ds * r**(2 * s_par - d_par)" in source_text,
    )
    source_amplitude = sp.Symbol("source_amplitude", positive=True)
    checks.check(
        "an independently supplied Riesz amplitude remains free and load bearing",
        sp.diff(source_amplitude * normalized_riesz, source_amplitude)
        == normalized_riesz
        and source_amplitude
        in (source_amplitude * normalized_riesz).free_symbols,
    )

    component_count = dimension * (dimension - 1) / 2
    magnetic_count = (dimension - 1) * (dimension - 2) / 2
    checks.check(
        "the antisymmetric component census is exact at D two and four",
        component_count.subs(dimension, 2) == 1
        and component_count.subs(dimension, 4) == 6
        and magnetic_count.subs(dimension, 2) == 0
        and magnetic_count.subs(dimension, 4) == 3,
    )
    checks.check(
        "GK1's two-by-two projector is evidence only for its supplied D two object",
        "projector_dim = P.shape[0]" in source_text
        and "P = sp.Matrix([[1 - q0**2 / Q2" in source_text,
    )

    claims_data = yaml.safe_load(
        (ROOT / "governance/claims.yaml").read_text(encoding="utf-8")
    )
    claims = {claim["id"]: claim for claim in claims_data["claims"]}
    base_release = yaml.safe_load(BASE_RELEASE.read_text(encoding="utf-8"))
    checks.check(
        "accepted U1 and non-Abelian covariance leave kinetic dynamics open",
        "leaves every F^2 coefficient unconstrained"
        in claims["C-GAU-001"]["statement"]
        and "does not derive an action coefficient or equation of motion"
        in claims["C-NAG-001"]["statement"],
    )
    checks.check(
        "accepted loop claims already own the corrected two-dimensional construction",
        "Euclidean two dimensions" in claims["C-VAC-001"]["statement"]
        and "two-dimensional Euclidean space" in claims["C-NVP-001"]["statement"]
        and "two-dimensional Euclidean space" in claims["C-NVP-002"]["statement"],
    )
    checks.check(
        "accepted loop claims reject unique coupling propagation and dimensional lift",
        "no bare Maxwell coefficient" in claims["C-VAC-001"]["statement"]
        and "propagating photon" in claims["C-VAC-001"]["statement"]
        and "no unique total gauge coupling" in claims["C-NVP-001"]["statement"]
        and "dimensional lift" in claims["C-NVP-002"]["statement"],
    )
    checks.check(
        "C-MAX-001 imports rather than derives the action and dimension",
        "declared action density" in claims["C-MAX-001"]["statement"]
        and "imports the action" in claims["C-MAX-001"]["statement"]
        and "preferred dimension" in claims["C-MAX-001"]["statement"],
    )
    checks.check(
        "C-DIM-009 was collision free at the frozen v0.127.0 base",
        "C-DIM-009" not in base_release["accepted_claims"],
    )

    checks.check(
        "GK1's live-file census is documentation regression not physics derivation",
        "read from the LIVE files at runtime" in source_text
        and "def read(relpath):" in source_text
        and all(
            name in source_text
            for name in ("em5", "ym1", "qcd1", "em7", "ym2", "qcd2")
        ),
    )
    checks.check(
        "GK1 result prose exceeds accepted physical authority",
        "a propagating gauge boson" in source_text
        and "canonically normalized gauge kinetic term with" in source_text
        and "a COMPUTED coupling" in source_text
        and "emergent-gauge-sector result" in source_text,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
