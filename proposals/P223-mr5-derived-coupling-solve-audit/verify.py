"""Primary exact and numerical audit for P223 MR5."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
import sympy as sp
import yaml

from substrate_framework.generalized_skyrme_radial import (
    generalized_skyrme_energy_components,
    generalized_skyrme_radial_energy_density,
    generalized_skyrme_radial_euler_lagrange_residual,
    solve_generalized_skyrme_radial_profile,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-44/"
    "bridge_MR5_solve_at_derived_e.py"
)
SOURCE_SHA = "0da10adafe3badb7f3eab225543bc601996df45b142f2d59b5d0ddd6dd9117d7"
FREEZE_SHA = "781ef83b2a5128bcde4c1d2803accd02098d9cf11cb616827e39bb6fa64d824b"
ANGULAR = {1: 1.0, 2: float(np.pi + 8.0 / 3.0), 4: 20.6496264884189}
ME = 0.511
MPI = 138.03
MRHO = 775.26
NC = 3.0
U = 16.0 * np.pi * ME
E_SOURCE = float(np.sqrt(MRHO / (16.0 * np.sqrt(2.0) * np.pi * ME)))
C6_PREFACTOR = NC**2 / (128.0 * np.pi**4)
C0_PREFACTOR = 8.0 * MPI**2 / U**2


def coefficients(coupling: float, *, c6_scale: float = 1.0) -> tuple[float, float]:
    return (
        c6_scale * C6_PREFACTOR * coupling**4,
        C0_PREFACTOR / coupling**4,
    )


def solve_set(outer: float, *, samples: int = 8001):
    c6, c0 = coefficients(E_SOURCE)
    return {
        degree: solve_generalized_skyrme_radial_profile(
            degree,
            angular,
            c6,
            c0,
            outer_radius=outer,
            initial_points=401,
            sample_points=samples,
            continuation_steps=8,
            tolerance=1.0e-6,
            max_nodes=200_000,
        )
        for degree, angular in ANGULAR.items()
    }


def kappa(profiles) -> float:
    return float(
        3.0
        * np.pi**2
        * (2.0 * profiles[2].energy_coefficient - profiles[4].energy_coefficient)
    )


def branch_value(log_coupling: float, *, c6_scale: float = 1.0) -> float:
    coupling = float(np.exp(log_coupling))
    c6, c0 = coefficients(coupling, c6_scale=c6_scale)
    profile = solve_generalized_skyrme_radial_profile(
        1,
        1.0,
        c6,
        c0,
        outer_radius=20.0,
        initial_points=301,
        sample_points=4001,
        continuation_steps=8,
        tolerance=2.0e-6,
        max_nodes=200_000,
    )
    return profile.energy_coefficient


def interval_minimum(*, c6_scale: float = 1.0):
    return minimize_scalar(
        lambda value: branch_value(value, c6_scale=c6_scale),
        bounds=(float(np.log(3.0)), float(np.log(7.0))),
        method="bounded",
        options={"xatol": 2.0e-4, "maxiter": 20},
    )


def main() -> int:
    checks = CheckLedger("P223")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    tree = ast.parse(source_text)
    checks.check(
        "source and preregistered formula freeze are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA
        and hashlib.sha256(
            (CAMPAIGN / "evidence/formula-freeze.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source inventory separates six predicates from one assertion",
        len(calls) == 6 and len(assertions) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "MR5 uses current SciPy trapezoid without legacy NumPy access",
        compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0
        and "from scipy.integrate import solve_bvp, trapezoid" in source_text,
    )
    reproduction = yaml.safe_load(
        (CAMPAIGN / "evidence/source-reproduction.yaml").read_text()
    )
    native = reproduction["native_execution"]
    checks.check(
        "hash-identical clean native execution reaches all source checks",
        native["execution_classification"] == "fresh_clean"
        and native["runtime_checks"] == 6
        and native["assertions"] == 1
        and native["exit_status"] == 0,
    )

    numeric_literals = {
        float(node.value)
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
    }
    checks.check(
        "the claimed comparator guard is falsified by executable comparators",
        all(value in numeric_literals for value in (8.46, 1.46534, 12.343, 5.45))
        and "FORBIDDEN = [929 / 1000.0" in source_text
        and yaml.safe_load(
            (CAMPAIGN / "evidence/check-adjudication.yaml").read_text()
        )["checks"]["MR5.6"]["verification"]
        == "refuted_by_AST_audit",
    )

    radius = sp.symbols("r", positive=True)
    q, p = sp.symbols("q p", real=True)
    degree, angular = sp.symbols("B I", positive=True)
    c6_symbol, c0_symbol = sp.symbols("c6 c0", nonnegative=True)
    profile = sp.Function("f")(radius)
    density = generalized_skyrme_radial_energy_density(
        q, p, radius, degree, angular, c6_symbol, c0_symbol
    )
    substitutions = {q: profile, p: sp.diff(profile, radius)}
    direct = sp.simplify(
        (
            sp.diff(sp.diff(density, p).subs(substitutions), radius)
            - sp.diff(density, q).subs(substitutions)
        )
        / 2
    )
    checks.check(
        "fresh variation maps the source model to C-GSK-001 exactly",
        sp.simplify(
            direct
            - generalized_skyrme_radial_euler_lagrange_residual(
                profile, radius, degree, angular, c6_symbol, c0_symbol
            )
        )
        == 0,
    )

    e, a, d = sp.symbols("e A D", positive=True)
    symbolic_c6 = a * e**4
    symbolic_c0 = d / e**4
    checks.check(
        "coefficient product is coupling independent but premise dependent",
        sp.simplify(symbolic_c6 * symbolic_c0 - a * d) == 0
        and sp.diff(symbolic_c6, e) != 0
        and sp.diff(symbolic_c0, e) != 0
        and sp.diff(a * d, a) != 0
        and sp.diff(a * d, d) != 0,
    )
    c6_value, c0_value = coefficients(E_SOURCE)
    checks.check(
        "source parameter arithmetic is reproduced without accepting its labels",
        abs(E_SOURCE - 4.619774866381011) < 2.0e-15
        and abs(c6_value - 0.32878825565855035) < 2.0e-15
        and abs(c0_value - 0.5071917782762795) < 2.0e-15,
    )
    claims = {
        claim["id"]: claim
        for claim in yaml.safe_load((ROOT / "governance/claims.yaml").read_text())[
            "claims"
        ]
    }
    checks.check(
        "accepted owners preserve supplied-input and nonphysical ceilings",
        "separately supplied" in claims["C-GSK-001"]["statement"]
        and "proves no" in claims["C-GSK-002"]["statement"]
        and "derives no mass formula" in claims["C-RDIFF-001"]["statement"]
        and "physical rho" in claims["C-VEC-001"]["statement"],
    )

    reference = solve_set(20.0, samples=8001)
    checks.check(
        "canonical branches pass status residual boundary and monotonicity gates",
        all(
            item.max_rms_residual < 1.1e-6
            and abs(item.inner_boundary_residual) < 2.0e-11
            and abs(item.outer_boundary_residual) < 2.0e-11
            and np.all(np.isfinite(item.field))
            and np.all(np.isfinite(item.radial_derivative))
            and np.max(item.radial_derivative) < 2.0e-6
            for item in reference.values()
        ),
    )
    checks.check(
        "canonical branches have nonnegative sectors and controlled Derrick residuals",
        all(
            min(
                item.two_derivative_energy,
                item.four_derivative_energy,
                item.sextic_energy,
                item.potential_energy,
            )
            >= 0.0
            and item.virial_relative_residual < 2.0e-6
            for item in reference.values()
        ),
    )
    expected = {1: 1.435998787155452, 2: 2.812806050268519, 4: 5.23598337140261}
    checks.check(
        "canonical coefficients reproduce the frozen supplied-point evidence",
        all(
            abs(reference[degree].energy_coefficient - value) < 3.0e-8
            for degree, value in expected.items()
        ),
    )
    reference_kappa = kappa(reference)
    checks.check(
        "accepted angular and boundary conventions materially repair source kappa",
        abs(reference_kappa - 11.536444259568) < 3.0e-7
        and abs(reference_kappa - 11.490) > 0.04,
    )

    coarse = solve_set(14.0, samples=6001)
    fine = solve_set(26.0, samples=10001)
    checks.check(
        "individual coefficients and signed difference converge by outer domain",
        all(
            abs(reference[b].energy_coefficient - fine[b].energy_coefficient)
            < abs(coarse[b].energy_coefficient - fine[b].energy_coefficient)
            and abs(reference[b].energy_coefficient - fine[b].energy_coefficient)
            < 5.0e-7
            for b in ANGULAR
        )
        and abs(reference_kappa - kappa(fine)) < 1.0e-7,
    )
    tolerance_profiles = [
        solve_generalized_skyrme_radial_profile(
            2,
            ANGULAR[2],
            c6_value,
            c0_value,
            outer_radius=20.0,
            initial_points=401,
            sample_points=4001,
            continuation_steps=8,
            tolerance=tolerance,
            max_nodes=200_000,
        )
        for tolerance in (2.0e-6, 1.0e-6, 5.0e-7)
    ]
    checks.check(
        "isolated tolerance refinement decreases the solver residual",
        all(
            fine_item.max_rms_residual < coarse_item.max_rms_residual
            for coarse_item, fine_item in zip(
                tolerance_profiles, tolerance_profiles[1:]
            )
        )
        and max(item.energy_coefficient for item in tolerance_profiles)
        - min(item.energy_coefficient for item in tolerance_profiles)
        < 3.0e-10,
    )
    middle = reference[2]
    quadrature = []
    for stride in (4, 2, 1):
        components = generalized_skyrme_energy_components(
            middle.radius[::stride],
            middle.field[::stride],
            middle.radial_derivative[::stride],
            2,
            ANGULAR[2],
            c6_value,
            c0_value,
        )
        quadrature.append(sum(components) / (12.0 * np.pi**2))
    checks.check(
        "output quadrature converges independently of the adaptive mesh",
        abs(quadrature[1] - quadrature[2]) < abs(quadrature[0] - quadrature[2])
        and abs(quadrature[1] - quadrature[2]) < 5.0e-8,
    )

    minimum = interval_minimum()
    mutated_minimum = interval_minimum(c6_scale=1.25)
    checks.check(
        "bounded interval optimization reproduces the branch minimum",
        minimum.success
        and 4.30 < np.exp(minimum.x) < 4.35
        and abs(minimum.fun - 1.4333949534606327) < 3.0e-7,
    )
    checks.check(
        "load-bearing coefficient mutation moves both branch optimum and value",
        mutated_minimum.success
        and abs(np.exp(mutated_minimum.x) - np.exp(minimum.x)) > 0.1
        and abs(mutated_minimum.fun - minimum.fun) > 0.02,
    )
    source_optimizers = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and node.id in {"minimize", "minimize_scalar"}
    ]
    checks.check(
        "source finite scan cannot establish its universal every-e floor",
        not source_optimizers
        and "e_grid = [3.0, 3.5, 4.0, 4.3" in source_text
        and "for ev in sorted(e_grid)" in source_text
        and "for EVERY e" in source_text,
    )

    b1, electron_mass = sp.symbols("b1 m_e", positive=True)
    mass = 3 * sp.pi**2 * b1 * (16 * sp.pi * electron_mass)
    checks.check(
        "mass-ratio cancellation is exact but its physical normalization is imported",
        sp.simplify(mass / electron_mass - 48 * sp.pi**3 * b1) == 0
        and "M_E = 0.511" in source_text
        and "M_RHO = 775.26" in source_text
        and "M_PI = 138.03" in source_text,
    )
    delta = yaml.safe_load(
        (CAMPAIGN / "evidence/post-source-claim-delta.yaml").read_text()
    )
    checks.check(
        "new point remains regression evidence with no claim or package delta",
        delta["reserved_identifiers"] == []
        and delta["package_change"] == "none_pending_nonduplication"
        and yaml.safe_load(
            (CAMPAIGN / "evidence/primary-numerical-evidence.yaml").read_text()
        )["interpretation"]["accepted_claim_delta"]
        == "none",
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
