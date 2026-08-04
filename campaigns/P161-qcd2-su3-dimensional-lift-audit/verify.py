#!/usr/bin/env python3
"""Exact source-aware verifier for the QCD2 accepted-composition decision."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.momentum_kernels import (
    riesz_green_kernel,
    riesz_radial_force_law,
)
from substrate_framework.nonabelian_vacuum_polarization import (
    finite_lie_scalar_qed2_vacuum_polarization,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.su3 import fundamental_generators, structure_constant
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P161-qcd2-su3-dimensional-lift-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-8/"
    "bridge_QCD2_su3_3plus1_lift.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_AUDIT = CAMPAIGN / "evidence/source-audit.yaml"
CHECK_ADJUDICATION = CAMPAIGN / "evidence/check-adjudication.yaml"
SOURCE_SHA256 = "64f8125a5c0ef194e23569711036ce6ec46f3ffef2b6eb94a7b5c97ed8bb566f"
FROZEN_SHA256 = "68bd4a2c1e66ff9e328c34b86dc71b6d011467000b026b9fe901fe89599bc2b4"
REVISION_SHA256 = "f91f92deca79a26e793945de24e14a4e8e2e9904b24f7dbaec564f967a5c34fe"
REPRODUCTION_SHA256 = "a32ef2512feabef33dfce34053509e6d51f6dfc08a881952cd5f0d0c49fb9cff"
SOURCE_AUDIT_SHA256 = "601dcf45611cf05b989147d4680eb1a013eee6a266a8b0de854eb2e0967f2768"
CHECK_ADJUDICATION_SHA256 = (
    "29b9e7468cc7fd2aa63cc0a6a939c12a1d0913eba438b5870522309fdb2bae93"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _su3_structure_constants() -> sp.ImmutableDenseNDimArray:
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
    checks = CheckLedger("P161/QCD2")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned QCD2 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("initial frozen proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    checks.check("source-aware revision hash", _sha256(REVISION) == REVISION_SHA256)
    checks.check(
        "source reproduction hash", _sha256(REPRODUCTION) == REPRODUCTION_SHA256
    )
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
    loaded_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    checks.check("ten source predicates", len(source_checks) == 10)
    checks.check("one source assertion", len(source_assertions) == 1)

    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "QCD2 eager legacy compatibility shape is exact",
        compatibility.dynamic_legacy_getattrs == 1
        and compatibility.dynamic_current_getattrs == 1
        and compatibility.direct_legacy_attributes == 0
        and compatibility.imported_legacy_names == 0
        and compatibility.eager_legacy_default_fallbacks == 1,
    )
    native = subprocess.run(
        [sys.executable, str(SOURCE)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    checks.check(
        "native QCD2 abort is compatibility-only",
        native.returncode == 1
        and "numpy' has no attribute 'trapz'" in native.stderr
        and "ALL 10 CHECKS PASS" not in native.stdout,
    )
    alias_code = (
        "import runpy; import numpy as np; "
        "np.trapz = np.trapezoid; "
        f"runpy.run_path({str(SOURCE)!r}, run_name='__main__')"
    )
    alias = subprocess.run(
        [sys.executable, "-c", alias_code],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    alias_lines = [line.strip() for line in alias.stdout.splitlines() if line.strip()]
    checks.check("alias-only QCD2 exits cleanly", alias.returncode == 0)
    checks.check(
        "alias-only QCD2 terminal tally is exact",
        alias_lines.count("ALL 10 CHECKS PASS") == 1,
    )

    q2, mass, coupling = sp.symbols("Q m g", positive=True)
    loop = finite_lie_scalar_qed2_vacuum_polarization(
        fundamental_generators(),
        _su3_structure_constants(),
        q2,
        mass,
        coupling,
    )
    checks.check(
        "accepted fundamental SU3 trace metric is one half",
        loop.generator_count == 8
        and loop.dynkin_index == sp.Rational(1, 2)
        and loop.trace_metric == sp.eye(8) / 2,
    )
    checks.check(
        "accepted SU3 loop remains Euclidean two dimensional and conditional",
        loop.ward_tadpole_residual == sp.zeros(8)
        and loop.abelian_ledger.massless_projector_limit == sp.oo,
    )

    radius = sp.symbols("r", positive=True)
    scalar = riesz_green_kernel(3, 1, radius)
    checks.check(
        "accepted supplied d3 s1 scalar inverse is Coulomb",
        scalar.green_kernel == 1 / (4 * sp.pi * radius)
        and scalar.radial_power == -1,
    )
    tau = loop.dynkin_index
    source_defined_product = sp.simplify(tau * scalar.green_kernel)
    checks.check(
        "QCD2 defined product is exactly one eighth pi r",
        source_defined_product == 1 / (8 * sp.pi * radius),
    )

    fixed_source_inverse = riesz_green_kernel(3, 1, radius, tau)
    checks.check(
        "color-weighted quadratic kernel inverts with reciprocal trace index",
        fixed_source_inverse.green_kernel == 1 / (2 * sp.pi * radius)
        and sp.simplify(fixed_source_inverse.green_kernel - source_defined_product)
        != 0,
    )
    trace_index, coefficient, momentum2 = sp.symbols("T_R A k2", positive=True)
    color_kernel = coefficient * trace_index * momentum2 * sp.eye(8)
    color_inverse = color_kernel.inv()
    source_ansatz = trace_index * sp.eye(8) / (coefficient * momentum2)
    checks.check(
        "general eight-color inverse differs from the source ansatz",
        color_inverse == sp.eye(8) / (coefficient * trace_index * momentum2)
        and sp.simplify((color_inverse - source_ansatz)[0, 0])
        == (1 - trace_index**2) / (coefficient * momentum2 * trace_index),
    )
    checks.check(
        "representation-index mutation changes inverse and product oppositely",
        sp.simplify(color_inverse[0, 0].subs(trace_index, 2))
        == 1 / (2 * coefficient * momentum2)
        and sp.simplify(source_ansatz[0, 0].subs(trace_index, 2))
        == 2 / (coefficient * momentum2),
    )

    source_strength, probe_strength = sp.symbols("Q_s q_p", real=True)
    force = riesz_radial_force_law(
        3, 1, radius, source_strength, probe_strength, tau
    )
    checks.check(
        "a force requires the accepted source-probe dictionary",
        force.potential_energy
        == source_strength * probe_strength / (2 * sp.pi * radius)
        and force.radial_force
        == source_strength * probe_strength / (2 * sp.pi * radius**2),
    )
    checks.check(
        "zero source or probe removes the force",
        force.radial_force.subs(source_strength, 0) == 0
        and force.radial_force.subs(probe_strength, 0) == 0,
    )

    generator_eight = fundamental_generators()[7]
    checks.check(
        "source abelian guard changes carrier normalization",
        sp.trace(generator_eight * generator_eight) == sp.Rational(1, 2)
        and "abelian_color_factor = sp.Integer(1)" in source_text
        and "G_abelian_limit = abelian_color_factor" in source_text,
    )
    checks.check(
        "the self-coupling switch never enters the abelian kernel",
        "G_abelian_limit = abelian_color_factor * riesz_G" in source_text
        and "abelian = {eps_self: 0}" in source_text,
    )

    fractional = riesz_radial_force_law(
        sp.Rational(14, 5),
        sp.Rational(9, 10),
        radius,
        source_strength,
        probe_strength,
    )
    checks.check(
        "inverse-square behavior does not select d3 s1",
        fractional.force_radial_power == -2
        and fractional.inverse_square_residual == 0
        and fractional.inverse_square_dimension_family == sp.Rational(14, 5),
    )
    dimension_four = riesz_green_kernel(4, 1, radius)
    checks.check(
        "dimension-blind color does not select a spatial kernel",
        dimension_four.green_kernel == 1 / (4 * sp.pi**2 * radius**2)
        and sp.simplify(tau * dimension_four.green_kernel - source_defined_product)
        != 0,
    )

    frequency, spatial_k2 = sp.symbols("omega k_spatial2", real=True)
    spacetime_symbol = spatial_k2 - frequency**2
    checks.check(
        "static agreement does not construct a spacetime operator",
        spacetime_symbol.subs(frequency, 0) == spatial_k2
        and spacetime_symbol.subs(frequency, 1) != spatial_k2,
    )
    checks.check(
        "source contains no executable dimension-changing map",
        "intertwiner" not in loaded_names
        and "pushforward" not in loaded_names
        and "pullback" not in loaded_names,
    )
    gauge_parameter, kinetic = sp.symbols("xi kappa", positive=True)
    transverse_eigenvalue = kinetic * momentum2
    longitudinal_eigenvalue = kinetic * momentum2 / gauge_parameter
    checks.check(
        "gauge-fixed operator has an independent longitudinal sector",
        transverse_eigenvalue.subs(gauge_parameter, 2) == kinetic * momentum2
        and longitudinal_eigenvalue.subs(gauge_parameter, 2)
        == kinetic * momentum2 / 2,
    )

    bare, loop_coefficient = sp.symbols("kappa_bare kappa_loop", positive=True)
    total_propagator = 1 / ((bare + loop_coefficient) * momentum2)
    checks.check(
        "bare coefficient counterfamily defeats unique propagation",
        sp.simplify(
            total_propagator.subs(bare, 1)
            - total_propagator.subs(bare, 2)
        )
        != 0,
    )
    checks.check(
        "source admits its static-shape-only ceiling",
        "THE 3+1D KINETIC-TERM CEILING IS NOT CLOSED HERE" in source_text
        and "QCD2 supplies the static" in source_text,
    )
    checks.check(
        "source also prints the contradictory closure claim",
        "THE QCD1 CEILING IS CLOSED" in source_text
        and "lifts the kinetic term PER COLOR" in source_text,
    )

    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        for path in CAMPAIGN.rglob("*.py")
    ]
    checks.check(
        "mutable P161 has no executable legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )
    checks.check(
        "mutable P161 has no eager legacy fallback",
        all(item.eager_legacy_default_fallbacks == 0 for item in mutable_compatibility),
    )
    return checks.finish()


if __name__ == "__main__":
    result = run()
    print(f"P161 PRIMARY ALL {result} CHECKS PASS")
