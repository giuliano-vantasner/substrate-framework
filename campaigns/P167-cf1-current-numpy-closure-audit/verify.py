#!/usr/bin/env python3
"""Current-environment CF1 reproduction and accepted-claim closure audit."""

from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys

import numpy as np
import sympy as sp
import yaml

from substrate_framework.abelian_higgs_vortex import (
    VortexParameters,
    angular_log_coefficient,
    asymptotic_masses,
    euler_lagrange_residuals,
    quantized_flux,
    radial_energy_lagrangian,
    solve_vortex_bvp,
    vortex_boundary_residual,
    vortex_tension,
)
from substrate_framework.numerics import trapezoid_integral
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path("/home/dan/substrate-framework")
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-10/"
    "bridge_CF1_dual_superconductor_flux_tube.py"
)
DOSSIER = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-10/dossiers/CF1-dossier.md"
)

PINNED_HASHES = {
    SOURCE: "a4ec97923804f1b7c624b7619bc6b6a1cbb62f42d659897799545b257ca33f5d",
    DOSSIER: "b0f1d6abc6d37410a6258a1411061c3fe9889c68b2f0314dc3fdd38c19ebadcc",
    ROOT / "campaigns/P026-abelian-higgs-vortex/verify.py":
        "b4d06baaeb3a196185f58c526b1b423a191a8d1f3a8c973feea9357d90291ed1",
    ROOT / "campaigns/P026-abelian-higgs-vortex/reviews/independent_finite_difference_review.py":
        "eea4cebeb7493383369cfcf38f2e338cf1fe1899a7a7444b1d3244801143f359",
    ROOT / "campaigns/P026-abelian-higgs-vortex/attempts/0004/result.yaml":
        "2e823dca1e0adbccb6866ccea21076aeea603a5cffd733314b7fd581d4b7b1af",
    ROOT / "tests/test_abelian_higgs_vortex.py":
        "534af58c5e007de4a526027f2d7f3496526645edc82273794e520d070ab2ce46",
    ROOT / "src/substrate_framework/abelian_higgs_vortex.py":
        "d816938fc091ee4641bec7f193e4b9e083131f6d5193c4870b910ee3d1e93d99",
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_source(*, compatibility_alias: bool) -> subprocess.CompletedProcess[str]:
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    if not compatibility_alias:
        return subprocess.run(
            [sys.executable, str(SOURCE)],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )
    code = (
        "import runpy; import numpy as np; "
        "setattr(np, 'trapz', np.trapezoid); "
        f"runpy.run_path({str(SOURCE)!r}, run_name='__main__')"
    )
    return subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )


def main() -> int:
    checks = CheckLedger("P167-CF1-CURRENT-NUMPY-CLOSURE")

    for path, expected in PINNED_HASHES.items():
        checks.check(f"pinned artifact {path.name} retains its audited bytes", _digest(path) == expected)

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    check_calls = sorted(
        (
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
        ),
        key=lambda node: node.lineno,
    )
    check_labels = [
        re.match(r"(CF1\.[0-9]+b?)", ast.literal_eval(node.args[0])).group(1)
        for node in check_calls
    ]
    checks.check(
        "CF1 has exactly the advertised eight lexical scientific predicates",
        check_labels == ["CF1.1", "CF1.1b", "CF1.2", "CF1.3", "CF1.3b", "CF1.4", "CF1.5", "CF1.6"],
    )
    checks.check(
        "CF1 has exactly two assertion nodes with distinct ledger and solver roles",
        sorted(node.lineno for node in ast.walk(tree) if isinstance(node, ast.Assert)) == [110, 219],
    )
    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check(
        "immutable CF1 has three legacy and zero current integration references",
        compatibility.legacy_references == 3 and compatibility.current_references == 0,
    )
    mutable_text = (ROOT / "src/substrate_framework/abelian_higgs_vortex.py").read_text()
    mutable_compatibility = audit_numpy_trapezoid_compatibility(
        mutable_text,
        filename="src/substrate_framework/abelian_higgs_vortex.py",
    )
    checks.check(
        "the canonical vortex module has no executable legacy integration access",
        mutable_compatibility.legacy_references == 0
        and "trapezoid_integral" in mutable_text,
    )

    native = _run_source(compatibility_alias=False)
    native_combined = native.stdout + native.stderr
    if hasattr(np, "trapz"):
        native_shape = native.returncode == 0 and "ALL 8 CHECKS PASS" in native.stdout
    else:
        native_shape = (
            native.returncode == 1
            and native.stdout.count("  PASS\n") == 2
            and "module 'numpy' has no attribute 'trapz'" in native_combined
            and "sigma_of" in native_combined
        )
    checks.check(
        "native CF1 outcome is exactly explained by installed NumPy name availability",
        native_shape,
    )

    aliased = _run_source(compatibility_alias=True)
    checks.check(
        "an isolated legacy-name alias backed only by np.trapezoid restores clean execution",
        aliased.returncode == 0
        and aliased.stderr == ""
        and "ALL 8 CHECKS PASS" in aliased.stdout
        and aliased.stdout.count("  PASS\n") == 8,
    )
    tension_match = re.search(
        r"sigma N=400: ([0-9.]+)\s+N=800: ([0-9.]+)\s+\|diff\|=([0-9.e+-]+)",
        aliased.stdout,
    )
    checks.check(
        "the alias replay retains the source BVP and mesh-difference evidence",
        tension_match is not None
        and 4.20 < float(tension_match.group(1)) < 4.23
        and 4.20 < float(tension_match.group(2)) < 4.23
        and float(tension_match.group(3)) < 1.0e-9,
    )
    tail_match = re.search(r"tail diff ([0-9.e+-]+)", aliased.stdout)
    scale_match = re.search(r"sigma\(v=2\)/sigma\(v=1\) = ([0-9.]+)", aliased.stdout)
    vector_match = re.search(
        r"vector mass m_V: measured ([0-9.]+)\s+predicted g v = ([0-9.]+)",
        aliased.stdout,
    )
    scalar_match = re.search(
        r"scalar mass m_H: measured ([0-9.]+)\s+predicted v\*sqrt\(2 lambda\) = ([0-9.]+)",
        aliased.stdout,
    )
    zero_match = re.search(r"v=0:.*max\|f\|=([0-9.e+-]+)", aliased.stdout)
    checks.check(
        "the alias replay retains finite-tail scaling screening and zero-vacuum diagnostics",
        all(
            match is not None
            for match in (tail_match, scale_match, vector_match, scalar_match, zero_match)
        )
        and float(tail_match.group(1)) < 1.0e-4
        and 3.5 < float(scale_match.group(1)) < 4.5
        and abs(float(vector_match.group(1)) - float(vector_match.group(2)))
        / float(vector_match.group(2))
        < 0.05
        and abs(float(scalar_match.group(1)) - float(scalar_match.group(2)))
        / float(scalar_match.group(2))
        < 0.06
        and float(zero_match.group(1)) < 1.0e-6,
    )

    radius = sp.symbols("r", positive=True)
    winding = sp.symbols("n", integer=True, positive=True)
    lam, vacuum, coupling = sp.symbols("lambda v g", positive=True)
    scalar = sp.Function("f")(radius)
    gauge = sp.Function("a")(radius)
    lagrangian = radial_energy_lagrangian(
        radius, scalar, gauge, winding, lam, vacuum, coupling
    )
    expected_scalar, expected_gauge = euler_lagrange_residuals(
        radius, scalar, gauge, winding, lam, vacuum, coupling
    )
    varied_scalar = sp.simplify(
        (
            sp.diff(sp.diff(lagrangian, sp.diff(scalar, radius)), radius)
            - sp.diff(lagrangian, scalar)
        )
        / radius
    )
    varied_gauge = sp.simplify(
        coupling**2
        * radius
        * (
            sp.diff(sp.diff(lagrangian, sp.diff(gauge, radius)), radius)
            - sp.diff(lagrangian, gauge)
        )
    )
    checks.check(
        "canonical exact variation closes CF1.1 in one general coupling convention",
        sp.simplify(varied_scalar - expected_scalar) == 0
        and sp.simplify(varied_gauge - expected_gauge) == 0,
    )
    checks.check(
        "dropping scalar friction or gauge-coupling normalization breaks exact closure",
        sp.simplify(varied_scalar - (expected_scalar - sp.diff(scalar, radius) / radius)) != 0
        and sp.simplify(
            expected_gauge
            - expected_gauge.xreplace({coupling**2: sp.Integer(1)})
        )
        != 0,
    )
    asymptotic = sp.symbols("a_infinity", real=True)
    checks.check(
        "canonical finite-energy and flux APIs close CF1.3 and its ungauged guard",
        sp.solve(
            sp.Eq(angular_log_coefficient(vacuum, winding, asymptotic), 0),
            asymptotic,
        )
        == [winding]
        and angular_log_coefficient(vacuum, winding, 0) == vacuum**2 * winding**2
        and quantized_flux(winding, coupling) == 2 * sp.pi * winding / coupling,
    )
    vector_mass, scalar_mass = asymptotic_masses(vacuum, lam, coupling)
    checks.check(
        "canonical inverse lengths close the mathematical part of CF1.5 and CF1.6 exactly",
        vector_mass == coupling * vacuum
        and scalar_mass == vacuum * sp.sqrt(2 * lam)
        and sp.limit(vector_mass, vacuum, 0, dir="+") == 0
        and sp.limit(scalar_mass, vacuum, 0, dir="+") == 0,
    )

    parameters = VortexParameters()
    solution = solve_vortex_bvp(
        parameters,
        inner_radius=1.0e-4,
        outer_radius=20.0,
        initial_points=120,
        tolerance=1.0e-8,
    )
    boundary = vortex_boundary_residual(
        solution.evidence.state[:, 0], solution.evidence.state[:, -1], parameters
    )
    canonical_tension = vortex_tension(solution)
    checks.check(
        "current canonical BVP retains status residual boundary and bounded tension evidence",
        solution.evidence.max_rms_residual < 1.1e-8
        and np.max(np.abs(boundary)) < 1.0e-10
        and 4.20 < canonical_tension < 4.23,
    )
    samples = np.asarray([0.0, 1.0, 4.0], dtype=float)
    checks.check(
        "canonical trapezoid dispatch equals the current NumPy quadrature",
        trapezoid_integral(samples**2, samples)
        == float(np.trapezoid(samples**2, samples)),
    )

    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())["claims"]
    claims = {entry["id"]: entry for entry in registry}
    release = yaml.safe_load((ROOT / "governance/releases/current.yaml").read_text())
    checks.check(
        "both accepted CF1 claims remain pinned in current release v0.127.0",
        release["release"] == "v0.127.0"
        and {"C-VTX-001", "C-VTX-002"}.issubset(release["accepted_claims"])
        and all(claims[name]["review"] == "accepted" for name in ("C-VTX-001", "C-VTX-002")),
    )
    checks.check(
        "the numeric claim depends only on the exact conditional model claim",
        claims["C-VTX-001"]["dependencies"] == []
        and claims["C-VTX-002"]["dependencies"] == ["C-VTX-001"],
    )
    checks.check(
        "accepted statements explicitly exclude physical and continuum overreach",
        "no substrate, dual, chromoelectric, QCD, or confinement" in claims["C-VTX-001"]["statement"]
        and "not a continuum existence or uniqueness theorem" in claims["C-VTX-002"]["statement"]
        and "absolute tension" in claims["C-VTX-002"]["statement"]
        and "The dimensionless demo tension is not an absolute physical string tension."
        in claims["C-VTX-002"]["assumptions"],
    )
    checks.check(
        "the fixed-area flux theorem remains a separately scoped construction",
        claims["C-FLX-001"]["dependencies"] == []
        and "no physical charge, flux tube, vortex-tension identity" in claims["C-FLX-001"]["statement"],
    )
    checks.check(
        "P026's immutable passing record retains exact and numeric status separation",
        yaml.safe_load(
            (ROOT / "campaigns/P026-abelian-higgs-vortex/attempts/0004/result.yaml").read_text()
        )["verdict"]
        == {"C-VTX-001": "symbolic_verified", "C-VTX-002": "numeric_evidence"},
    )

    total = checks.finish()
    print(f"P167 CF1 CURRENT-NUMPY CLOSURE ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
