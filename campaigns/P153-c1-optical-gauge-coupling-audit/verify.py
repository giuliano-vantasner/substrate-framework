#!/usr/bin/env python3
"""Exact source-aware verifier for proposed C-OG-005 and C1."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.optical_gauge_scalar import (
    affine_gauge_plane_wave,
    berry_one_form_to_u1_connection,
    charged_optical_scalar_euler_operator,
    charged_optical_scalar_lagrangian_density,
    circle_optical_gauge_mode,
    constant_optical_gauge_dispersion,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P153-c1-optical-gauge-coupling-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-7/"
    "bridge_C1_Aeff_optical_metric_coupling.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_AUDIT = CAMPAIGN / "evidence/source-audit.yaml"
SOURCE_SHA256 = "6c0b625cbfd8396104f185e4e3785956f66989a10d9fddf9d553fe433c39f0f5"
FROZEN_SHA256 = "85e16eafda92241b9c216e2289373ce25fa2ec063f1afc3c0bdb93d55937d79f"
REVISION_SHA256 = "5f490a295fb0944c4590206c514f597a8bb0c0ff0a4f109cce34e8e6e8cc123b"
REPRODUCTION_SHA256 = "2c2ab35bcdacf0f14bdfff49b1a31b12e22d744c7f73c332e27c7a558f85cdc3"
SOURCE_AUDIT_SHA256 = "7aa347a3e7f7df6d1ef6b47db335dd7cf38b4288986628d8c4ace73d3b9b4fd5"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> int:
    checks = CheckLedger("P153/C-OG-005")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned C1 source hash", _sha256(SOURCE) == SOURCE_SHA256)
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
        "C1 has no numerical integration compatibility surface",
        source_compatibility.numpy_aliases == ()
        and source_compatibility.legacy_references == 0
        and source_compatibility.current_references == 0,
    )
    assigned_names = {
        target.id
        for node in ast.walk(tree)
        if isinstance(node, (ast.Assign, ast.AnnAssign))
        for target in (
            node.targets if isinstance(node, ast.Assign) else [node.target]
        )
        if isinstance(target, ast.Name)
    }
    loaded_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    checks.check(
        "source declares but never uses eps0 in its SI curvature comparison",
        "eps0" in assigned_names and "eps0" not in loaded_names,
    )

    native = subprocess.run(
        [sys.executable, str(SOURCE)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    checks.check("native C1 exits cleanly", native.returncode == 0)
    checks.check(
        "native C1 reaches the exact terminal tally",
        native.stdout.rstrip().endswith("ALL 9 CHECKS PASS"),
    )

    t, x = sp.symbols("t x", real=True)
    n, c0, mass, charge = sp.symbols("n c0 m e", positive=True)
    omega, wave_number, a_t, a_x = sp.symbols(
        "omega k A_t A_x", real=True
    )
    field = sp.exp(sp.I * (wave_number * x - omega * t))
    field_bar = sp.exp(-sp.I * (wave_number * x - omega * t))
    dispersion = constant_optical_gauge_dispersion(
        n, c0, mass, charge, omega, wave_number, a_t, a_x
    )
    checks.check(
        "accepted optical metric inverse and volume are derived",
        dispersion.inverse_metric == sp.diag(-n, c0**2 / n)
        and dispersion.volume_density == 1 / c0,
    )
    checks.check(
        "constant optical mass shell uses both invariant momenta",
        dispersion.invariant_frequency == omega + charge * a_t
        and dispersion.invariant_wavenumber == wave_number - charge * a_x
        and sp.simplify(
            dispersion.mass_shell_lhs
            - n * (omega + charge * a_t) ** 2
            + c0**2 * (wave_number - charge * a_x) ** 2 / n
        )
        == 0,
    )
    euler = charged_optical_scalar_euler_operator(
        field, n, c0, mass, charge, (a_t, a_x), (t, x)
    )
    checks.check(
        "declared action Euler operator gives the mass shell",
        sp.simplify(euler / field - (dispersion.mass_shell_lhs - mass**2)) == 0,
    )

    alpha, beta = sp.symbols("alpha beta", real=True)
    phase = alpha * t + beta * x
    original_density = charged_optical_scalar_lagrangian_density(
        field, field_bar, n, c0, mass, charge, (a_t, a_x), (t, x)
    )
    transformed_density = charged_optical_scalar_lagrangian_density(
        sp.exp(sp.I * charge * phase) * field,
        sp.exp(-sp.I * charge * phase) * field_bar,
        n,
        c0,
        mass,
        charge,
        (a_t + alpha, a_x + beta),
        (t, x),
    )
    checks.check(
        "declared charged-scalar action density is gauge invariant",
        sp.simplify(transformed_density - original_density) == 0,
    )
    transformed_labels = affine_gauge_plane_wave(
        omega, wave_number, a_t, a_x, charge, alpha, beta
    )
    checks.check(
        "affine gauge transformation preserves the plane-wave invariants",
        transformed_labels.invariant_frequency == omega + charge * a_t
        and transformed_labels.invariant_wavenumber == wave_number - charge * a_x,
    )
    removed = affine_gauge_plane_wave(
        omega, wave_number, a_t, a_x, charge, -a_t, -a_x
    )
    checks.check(
        "constant line connection is removed without changing invariant labels",
        removed.temporal_connection == 0
        and removed.spatial_connection == 0
        and removed.frequency == omega + charge * a_t
        and removed.wavenumber == wave_number - charge * a_x,
    )

    wrong_spatial_sign = sp.simplify(
        n * (omega + charge * a_t) ** 2
        - c0**2 * (wave_number + charge * a_x) ** 2 / n
    )
    wrong_metric_factor = sp.simplify(
        n * (omega + charge * a_t) ** 2
        - c0**2 * n * (wave_number - charge * a_x) ** 2
    )
    checks.check(
        "connection-sign mutation changes the generic mass shell",
        sp.simplify(wrong_spatial_sign - dispersion.mass_shell_lhs) != 0,
    )
    checks.check(
        "optical inverse-metric mutation changes the generic mass shell",
        sp.simplify(wrong_metric_factor - dispersion.mass_shell_lhs) != 0,
    )
    checks.check(
        "mass-sign mutation changes the Euler verdict",
        sp.simplify(
            euler / field - (dispersion.mass_shell_lhs + mass**2)
        )
        != 0,
    )

    length = sp.symbols("L", positive=True)
    theta = sp.symbols("theta", real=True)
    mode, winding = sp.symbols("q ell", integer=True)
    circle = circle_optical_gauge_mode(
        n, c0, mass, charge, a_x, length, mode, theta
    )
    large_gauge = circle_optical_gauge_mode(
        n,
        c0,
        mass,
        charge,
        a_x + 2 * sp.pi * winding / (charge * length),
        length,
        mode + winding,
        theta,
    )
    checks.check(
        "circle spectrum and holonomy survive a large-gauge mode relabeling",
        sp.simplify(
            large_gauge.invariant_frequency_squared
            - circle.invariant_frequency_squared
        )
        == 0
        and sp.simplify(
            large_gauge.connection_holonomy - circle.connection_holonomy
        )
        == 0,
    )
    connection_only = circle_optical_gauge_mode(
        n,
        c0,
        mass,
        charge,
        a_x + 2 * sp.pi * winding / (charge * length),
        length,
        mode,
        theta,
    )
    checks.check(
        "connection-only large-gauge mutation changes a fixed mode label",
        sp.simplify(
            connection_only.invariant_frequency_squared
            - circle.invariant_frequency_squared
        )
        != 0,
    )

    varying_index = sp.Function("n", positive=True)(x)
    varying_connection = sp.Function("A_x", real=True)(x)
    generic_field = sp.Function("Psi")(t, x)
    exact_operator = charged_optical_scalar_euler_operator(
        generic_field,
        varying_index,
        c0,
        mass,
        charge,
        (0, varying_connection),
        (t, x),
    )
    d_x = (
        sp.diff(generic_field, x)
        - sp.I * charge * varying_connection * generic_field
    )
    d_x_twice = (
        sp.diff(d_x, x) - sp.I * charge * varying_connection * d_x
    )
    naive_operator = (
        -varying_index * sp.diff(generic_field, t, 2)
        + c0**2 * d_x_twice / varying_index
        - mass**2 * generic_field
    )
    checks.check(
        "variable-index divergence exposes the omitted C1 derivative term",
        sp.simplify(
            exact_operator
            - naive_operator
            + c0**2 * sp.diff(varying_index, x) * d_x / varying_index**2
        )
        == 0,
    )

    texture = 2 * sp.pi * x / length
    pulled_back = berry_one_form_to_u1_connection(
        sp.Rational(1, 2), texture, x, charge
    )
    checks.check(
        "same-phase Berry one-form uses the signed dimensioned pullback",
        pulled_back == -sp.pi / (charge * length)
        and sp.simplify(sp.exp(sp.I * charge * pulled_back * length)) == -1
        and pulled_back != sp.Rational(1, 2),
    )
    wrong_pullback = sp.pi / (charge * length)
    checks.check(
        "Berry pullback-sign mutation changes the local dispersion",
        sp.simplify(
            constant_optical_gauge_dispersion(
                n, c0, mass, charge, omega, wave_number, 0, wrong_pullback
            ).mass_shell_lhs
            - constant_optical_gauge_dispersion(
                n, c0, mass, charge, omega, wave_number, 0, pulled_back
            ).mass_shell_lhs
        )
        != 0,
    )

    material_label, gravity_label = sp.symbols("material_label gravity_label")
    checks.check(
        "identical mass shell leaves material and gravity dictionaries free",
        material_label not in dispersion.mass_shell_lhs.free_symbols
        and gravity_label not in dispersion.mass_shell_lhs.free_symbols,
    )
    checks.check(
        "source omits charge pullback topology and boundary premises",
        "A_eff = sp.symbols" in source_text
        and "eps0 =" in source_text
        and "partial_x" not in source_text
        and "boundary" not in source_text.lower()
        and "circumference" not in source_text.lower(),
    )

    mutable_python = sorted(CAMPAIGN.rglob("*.py")) + [
        ROOT / "src/substrate_framework/optical_gauge_scalar.py",
        ROOT / "tests/test_optical_gauge_scalar.py",
    ]
    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        for path in mutable_python
    ]
    checks.check(
        "mutable P153 and canonical code has no executable legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )

    tally = checks.finish()
    print(f"P153 PRIMARY ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
