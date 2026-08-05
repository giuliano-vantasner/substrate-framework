#!/usr/bin/env python3
"""Exact source-aware verifier for BX1 and proposed C-PDE-012."""

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

from substrate_framework.radial_modes import solve_radial_finite_box_spectrum
from substrate_framework.radial_spectral_classification import (
    bracketed_spherical_bessel_zero,
    central_radial_liouville_evidence,
    endpoint_decay_evidence,
    hard_zero_endpoint_counterexample,
    radial_threshold_form_evidence,
    vacuum_dirichlet_ball_evidence,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P177-bx1-l2-box-artifact-audit"
BASE_RELEASE = ROOT / "governance/releases/v0.128.0.yaml"
PRIOR_NUMERIC_AUDIT = (
    ROOT
    / "campaigns/P054-qb3-triaxial-l2-polarizations/evidence/numerical-audit.yaml"
)
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-36/"
    "bridge_BX1_l2_mode_box_artifact.py"
)
PINNED_HASHES = {
    SOURCE: "a80364df834f23b5ad006b54e7097e0a38d846405ba40408e558a8773aa74fb3",
    CAMPAIGN / "evidence/frozen-proposal.yaml": (
        "a7ad333c3f04907d9e27721d39e17eb592b2167b62c7582cd025cd9b310bfa4b"
    ),
    CAMPAIGN / "evidence/proposal-revision-0001.yaml": (
        "9c16e8c1c5b232b65eb8dab27c70f3b16a6ac3bcae2e6fac61a452765a174cfc"
    ),
    PRIOR_NUMERIC_AUDIT: (
        "392d26bd1735d53d0ca7b8d1af2ffc8970c3d26cf4eb07e52323ebc80038ac7b"
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
        timeout=180,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def _liouville_power_closes(candidate: object) -> bool:
    radius = sp.symbols("r", positive=True)
    chi = sp.Function("chi")(radius)
    power = sp.sympify(candidate)
    radial = chi / radius**power
    original = (
        -sp.diff(radial, radius, 2)
        - 2 * sp.diff(radial, radius) / radius
        + 6 * radial / radius**2
    )
    transformed = -sp.diff(chi, radius, 2) + 6 * chi / radius**2
    return sp.simplify(radius * original - transformed) == 0


def _centrifugal_coefficient_closes(candidate: object) -> bool:
    coordinate = sp.symbols("r", positive=True)
    radius, zero = sp.symbols("R z", positive=True)
    vacuum = vacuum_dirichlet_ball_evidence(radius, 1, zero, coordinate, 2)
    coefficient = sp.sympify(candidate)
    residual = sp.simplify(
        -sp.diff(vacuum.radial_mode, coordinate, 2)
        - 2 * sp.diff(vacuum.radial_mode, coordinate) / coordinate
        + coefficient * vacuum.radial_mode / coordinate**2
        - vacuum.wavenumber**2 * vacuum.radial_mode
    )
    return residual == 0


def _wall_gap_power_closes(candidate: object) -> bool:
    exponent = sp.sympify(candidate)
    radius, scale = sp.symbols("R z", positive=True)
    gap = scale**2 / radius**exponent
    return sp.simplify(gap / gap.subs(radius, 2 * radius) - 4) == 0


def _vacuum_fem(radius_value: float, points: int):
    radius = np.linspace(1.0e-3, radius_value, points, dtype=np.float64)
    ones = np.ones_like(radius)
    return solve_radial_finite_box_spectrum(
        radius,
        ones,
        1.0 + 6.0 / radius**2,
        ones,
        mode_count=1,
        continuum_threshold=1.0,
    )


def main() -> int:
    checks = CheckLedger("P177-BX1-C-PDE-012")
    for path, expected in PINNED_HASHES.items():
        checks.check(
            f"pinned artifact {path.name} retains its audited bytes",
            _digest(path) == expected,
        )

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "BX1 has eight advertised predicates and one local assertion helper",
        len(source_checks) == 8
        and sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "BX1 has no NumPy integration compatibility surface",
        compatibility.current_references == 0
        and compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    native = _run_source()
    checks.check(
        "native BX1 executes eight predicates and exits with its terminal tally",
        native.returncode == 0
        and native.stderr == ""
        and len(re.findall(r"  PASS$", native.stdout, flags=re.MULTILINE)) == 8
        and native.stdout.count("ALL 8 CHECKS PASS") == 1,
        native.stderr[-500:],
    )
    checks.check(
        "native output exposes the finite-wall and vacuum-counterexample values",
        "80.0   1.087681" in native.stdout
        and "R = 320 -> 640" in native.stdout
        and "PURE VACUUM" in native.stdout
        and "localized = True" in native.stdout,
    )

    radius = sp.symbols("r", positive=True)
    energy = sp.symbols("E", real=True)
    potential = sp.Function("V")(radius)
    chi = sp.Function("chi")(radius)
    liouville = central_radial_liouville_evidence(
        chi, potential, energy, radius, 2
    )
    checks.check(
        "chi equals r times g closes the exact l2 transformed operator",
        liouville.scaled_residual_difference == 0
        and sp.simplify(
            liouville.transformed_residual
            - (
                -sp.diff(chi, radius, 2)
                + (6 / radius**2 + potential - energy) * chi
            )
        )
        == 0,
    )
    checks.check(
        "the transform preserves the real radial norm and regular origin power",
        liouville.norm_density_difference == 0
        and liouville.regular_radial_power == 2
        and liouville.regular_transformed_power == 3,
    )
    checks.mutation_sensitive(
        "the Liouville power is load bearing",
        _liouville_power_closes,
        1,
        [0, 2],
    )

    threshold = sp.symbols("mu2", real=True)
    form = radial_threshold_form_evidence(chi, threshold, threshold, radius, 2)
    checks.check(
        "the threshold quadratic form retains derivative and centrifugal terms",
        form.excess_potential == 6 / radius**2
        and sp.simplify(
            form.quadratic_form_density
            - sp.diff(chi, radius) ** 2
            - 6 * chi**2 / radius**2
        )
        == 0,
    )
    negative_mutation = radial_threshold_form_evidence(
        chi, threshold - 7 / radius**2, threshold, radius, 2
    )
    checks.check(
        "an attractive mutation invalidates rather than passes the form premise",
        negative_mutation.excess_potential == -1 / radius**2,
    )

    root = bracketed_spherical_bessel_zero(2, (5.0, 6.5))
    checks.check(
        "the first l2 spherical-Bessel zero is independently bracketed",
        abs(root.zero - 5.76345919689455) < 2.0e-13
        and root.absolute_residual < 2.0e-16,
    )
    coordinate = sp.symbols("rho", positive=True)
    ball_radius, zero = sp.symbols("R z", positive=True)
    vacuum = vacuum_dirichlet_ball_evidence(
        ball_radius, threshold, zero, coordinate, 2
    )
    checks.check(
        "the exact regular vacuum ball mode solves the l2 equation",
        vacuum.differential_residual == 0
        and vacuum.spectral_value == threshold + zero**2 / ball_radius**2,
    )
    checks.mutation_sensitive(
        "the centrifugal coefficient is load bearing",
        _centrifugal_coefficient_closes,
        6,
        [5, 7],
    )
    checks.mutation_sensitive(
        "the vacuum wall gap has exact inverse-square scaling",
        _wall_gap_power_closes,
        2,
        [1, 3],
    )
    numeric_vacuum = vacuum_dirichlet_ball_evidence(
        40.0, 1.0, root.zero, coordinate, 2
    )
    checks.check(
        "the independently derived R40 vacuum level and boundary close",
        abs(float(numeric_vacuum.spectral_value) - 1.020760913696417) < 2.0e-13
        and abs(float(sp.N(numeric_vacuum.outer_boundary_value, 17))) < 2.0e-16,
    )

    coarse = _vacuum_fem(20.0, 251)
    fine = _vacuum_fem(20.0, 501)
    exact_level = 1.0 + (root.zero / 20.0) ** 2
    coarse_error = abs(coarse.eigenvalues[0] - exact_level)
    fine_error = abs(fine.eigenvalues[0] - exact_level)
    checks.check(
        "the existing canonical FEM converges to the soluble l2 ball level",
        coarse_error / fine_error > 3.8
        and fine_error / exact_level < 1.1e-6
        and fine.node_counts == (0,)
        and max(fine.relative_residuals) < 2.0e-10
        and not any(fine.below_continuum),
    )

    hard_zero = hard_zero_endpoint_counterexample(0.2)
    unforced = endpoint_decay_evidence(0.2, 0.02)
    checks.check(
        "forced zero passes the arithmetic endpoint test without discrimination",
        hard_zero.passes
        and hard_zero.endpoint_forced
        and not hard_zero.endpoint_value_is_discriminating,
    )
    checks.check(
        "a load-bearing unforced endpoint mutation fails the same tolerance",
        not unforced.passes
        and not unforced.endpoint_forced
        and unforced.endpoint_value_is_discriminating,
    )
    checks.check(
        "BX1's vacuum predicate applies only after imposed outer zeros",
        "g_vac[rc > R_mode_qb3] = 0.0" in source_text
        and "abs(g_vac[-1]) < 1e-3 * np.max(np.abs(g_vac))" in source_text,
    )

    prior = yaml.safe_load(PRIOR_NUMERIC_AUDIT.read_text(encoding="utf-8"))
    averaged = prior["converged_averaged_operator"]
    soluble = prior["soluble_limit"]
    checks.check(
        "hash-reused P054 evidence types the accepted-background averaged level",
        averaged["lowest_eigenvalue_at_wall_40"] > averaged["continuum_threshold"]
        and averaged["outer_quarter_v_norm_fraction"] > 0.24
        and averaged["wall_30_to_40_eigenvalue_difference"] > 0.015
        and averaged["relative_eigenpair_residual"] < 2.0e-10,
    )
    checks.check(
        "P054 independently calibrated the same vacuum box level",
        abs(
            soluble["exact_vacuum_spherical_j2_box_eigenvalue"]
            - (1.0 + (exact_level - 1.0) / 4.0)
        )
        < 2.0e-15
        and soluble["absolute_error"] < 3.0e-9,
    )
    checks.check(
        "BX1 promotes finite sampling to an exact premise and fits tolerances post hoc",
        "rw = np.linspace(0.05, 60.0, 8000)" in source_text
        and "positive_everywhere = minW >= 0.0" in source_text
        and "thresholds are stated to the MEASURED data" in source_text,
    )
    checks.check(
        "BX1 node and l0 prose disagree with its pinned execution",
        "5 -> 42" in source_text
        and "0.4015 for A = 1..5" in source_text
        and "node count 5 -> 41" in native.stdout
        and "0.459073" in native.stdout,
    )

    claims_data = yaml.safe_load(
        (ROOT / "governance/claims.yaml").read_text(encoding="utf-8")
    )
    claims = {claim["id"]: claim for claim in claims_data["claims"]}
    checks.check(
        "accepted l2 transform and unit far threshold are the only imported physics",
        "For v=r*psi" in claims["C-PDE-003"]["statement"]
        and "((n*omega)^2-1)" in claims["C-PDE-005"]["statement"]
        and "n*omega=1 is threshold" in claims["C-PDE-005"]["statement"],
    )
    checks.check(
        "accepted phase averaging remains distinct from the full perturbation equation",
        "defines a different equation" in claims["C-PDE-009"]["statement"]
        and "pointwise defect vanishes" in claims["C-PDE-009"]["statement"]
        and "separate Floquet argument" in claims["C-PDE-009"]["statement"],
    )
    base_release = yaml.safe_load(BASE_RELEASE.read_text(encoding="utf-8"))
    checks.check(
        "C-PDE-012 was collision free at the frozen v0.128.0 base",
        "C-PDE-012" not in base_release["accepted_claims"],
    )
    checks.check(
        "BX1 result prose exceeds the averaged finite-wall authority",
        "its only genuine internal mode is the l=0 breathing mode" in source_text
        and "from a single SELF-CONSISTENT soliton" in source_text
        and "a CONTINUUM (radiative) fluctuation" in source_text,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
