#!/usr/bin/env python3
"""Exact source-aware verifier for the YM2 accepted-composition decision."""

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
    su2_scalar_qed2_vacuum_polarization,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P159-ym2-yang-mills-lift-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-7/"
    "bridge_YM2_yang_mills_3plus1_lift.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_AUDIT = CAMPAIGN / "evidence/source-audit.yaml"
CHECK_ADJUDICATION = CAMPAIGN / "evidence/check-adjudication.yaml"
SOURCE_SHA256 = "19c8708ea9b81eff719362ee713dd3d933b5422788759ae6e8933c705863b11c"
FROZEN_SHA256 = "5faa25f9cfb4ae07256f507ef707a4ed954062b721b35c55f133a1c0deadb60c"
REVISION_SHA256 = "da156bed216e4fb1a5a27524b5f5e4807382b26a0805244a5d6536d03bbece8d"
REPRODUCTION_SHA256 = "9a8e6762394632f3b10cdad8158d1a406162634d9156da57e6306a39dc09b84f"
SOURCE_AUDIT_SHA256 = "d0526f4b40b45a60bd73d64ac9d197df4309d6ea6ebe2844168c3e1e239f6795"
CHECK_ADJUDICATION_SHA256 = (
    "96f5801aef4fb974c8429250cceb5f544e9475ddf9d5e167c1bbb33fd610d4a6"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fundamental_generators() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return (
        sp.Matrix([[0, 1], [1, 0]]) / 2,
        sp.Matrix([[0, -sp.I], [sp.I, 0]]) / 2,
        sp.diag(1, -1) / 2,
    )


def run() -> int:
    checks = CheckLedger("P159/YM2")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned YM2 source hash", _sha256(SOURCE) == SOURCE_SHA256)
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
    checks.check("ten source predicates", len(source_checks) == 10)
    checks.check("one source assertion", len(source_assertions) == 1)

    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "YM2 eager legacy compatibility shape is exact",
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
        "native YM2 abort is compatibility-only",
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
    checks.check("alias-only YM2 exits cleanly", alias.returncode == 0)
    checks.check(
        "alias-only YM2 terminal tally is exact",
        alias_lines.count("ALL 10 CHECKS PASS") == 1,
    )

    q2, mass, coupling = sp.symbols("Q m g", positive=True)
    loop = su2_scalar_qed2_vacuum_polarization(
        _fundamental_generators(), q2, mass, coupling
    )
    checks.check(
        "accepted fundamental trace metric is one half",
        loop.dynkin_index == sp.Rational(1, 2)
        and loop.trace_metric == sp.eye(3) / 2,
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
        "YM2 defined product is exactly one eighth pi r",
        source_defined_product == 1 / (8 * sp.pi * radius),
    )

    fixed_source_inverse = riesz_green_kernel(3, 1, radius, tau)
    checks.check(
        "color-weighted quadratic kernel inverts with reciprocal trace index",
        fixed_source_inverse.green_kernel == 1 / (2 * sp.pi * radius)
        and sp.simplify(fixed_source_inverse.green_kernel - source_defined_product)
        != 0,
    )
    trace_index, coefficient, momentum2 = sp.symbols(
        "T_R A k2", positive=True
    )
    color_kernel = coefficient * trace_index * momentum2 * sp.eye(3)
    color_inverse = color_kernel.inv()
    source_ansatz = trace_index * sp.eye(3) / (coefficient * momentum2)
    checks.check(
        "general color inverse differs from the source ansatz",
        color_inverse == sp.eye(3) / (coefficient * trace_index * momentum2)
        and sp.simplify((color_inverse - source_ansatz)[0, 0])
        == (1 - trace_index**2) / (coefficient * momentum2 * trace_index),
    )
    checks.check(
        "representation mutation changes inverse and product oppositely",
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

    fundamental_t3 = _fundamental_generators()[2]
    checks.check(
        "source abelian guard changes carrier normalization",
        sp.trace(fundamental_t3 * fundamental_t3) == sp.Rational(1, 2)
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
        and "YM2 supplies the static" in source_text,
    )
    checks.check(
        "source also prints the contradictory closure claim",
        "THE YM1 CEILING IS CLOSED" in source_text
        and "fractional-Laplacian / Riesz family lifts the kinetic term" in source_text,
    )

    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        for path in CAMPAIGN.rglob("*.py")
    ]
    checks.check(
        "mutable P159 has no executable legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )
    checks.check(
        "mutable P159 has no eager legacy fallback",
        all(item.eager_legacy_default_fallbacks == 0 for item in mutable_compatibility),
    )
    return checks.finish()


if __name__ == "__main__":
    result = run()
    print(f"P159 PRIMARY ALL {result} CHECKS PASS")
