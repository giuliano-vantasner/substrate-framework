#!/usr/bin/env python3
"""Primary exact verifier for C-DOS-001 and the P196 MD1 disposition."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.mode_counting import (
    isotropic_continuum_dos_on_band,
    isotropic_continuum_mode_count,
    isotropic_continuum_target_cutoff,
    isotropic_gapped_angular_frequency,
    unit_sphere_surface,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
PROPOSAL = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-38/"
    "bridge_MD1_mode_count_is_a_counting_theorem.py"
)
SOURCE_SHA256 = "e7408667dbb6644e4c88a0a1523b6eb5f9058c628b5650ff0bf72cfa3238e5ba"
RELEASE_SHA256 = "b995916d6e708d29f0f493562741d7ba35bc202ce2784f4aaed7d1dfd5232a0a"
FORMULA_FREEZE_SHA256 = "de520bd631c3e244b2e538a92dbc65f92e26301a4d927b7b8b48280423b94540"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P196-MD1-PRIMARY")
    checks.check("MD1 source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        digest(ROOT / "governance/releases/v0.144.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "general-d formula freeze remains pinned",
        digest(PROPOSAL / "evidence/formula-freeze.yaml") == FORMULA_FREEZE_SHA256,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    check_calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source inventory separates 19 check sites from 27 executions",
        len(check_calls) == 19
        and not any(isinstance(node, ast.Assert) for node in ast.walk(source_tree)),
    )
    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check(
        "MD1 has no NumPy integration compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    omega, omega_0, k, c, V, K = sp.symbols(
        "omega omega_0 k c V K", positive=True
    )
    branches = 3
    dispersion = isotropic_gapped_angular_frequency(k, c, omega_0)
    checks.check(
        "canonical dispersion has the exact gap speed and radial wave number",
        sp.simplify(dispersion**2 - omega_0**2 - c**2 * k**2) == 0,
    )
    inverse = sp.sqrt(omega**2 - omega_0**2) / c
    jacobian = sp.diff(inverse, omega)
    checks.check(
        "inverse dispersion Jacobian is derived rather than copied",
        sp.simplify(jacobian - omega / (c * sp.sqrt(omega**2 - omega_0**2))) == 0,
    )

    for dimension in (1, 2, 3, 4, 5):
        shell_density = sp.simplify(
            branches
            * V
            * unit_sphere_surface(dimension)
            * inverse ** (dimension - 1)
            * jacobian
            / (2 * sp.pi) ** dimension
        )
        canonical = isotropic_continuum_dos_on_band(
            omega,
            V,
            c,
            omega_0,
            dimension,
            branches=branches,
        )
        checks.check(
            f"radial shell and Jacobian derive the d={dimension} DOS",
            sp.simplify(shell_density - canonical) == 0,
        )

    checks.check(
        "first three unit-sphere normalizations are exact",
        tuple(unit_sphere_surface(dimension) for dimension in (1, 2, 3))
        == (2, 2 * sp.pi, 4 * sp.pi),
    )
    d3_per_branch = isotropic_continuum_dos_on_band(
        omega, V, c, omega_0, 3
    )
    checks.check(
        "MD1 per-branch d3 DOS is the canonical specialization",
        d3_per_branch
        == V
        * omega
        * sp.sqrt(omega**2 - omega_0**2)
        / (2 * sp.pi**2 * c**3),
    )
    checks.check(
        "gapless limits retain dimension-dependent frequency powers",
        all(
            sp.simplify(
                isotropic_continuum_dos_on_band(
                    omega, V, c, omega_0, dimension
                ).subs(omega_0, 0)
                - V
                * unit_sphere_surface(dimension)
                * omega ** (dimension - 1)
                / ((2 * sp.pi) ** dimension * c**dimension)
            )
            == 0
            for dimension in (1, 2, 3, 4)
        ),
    )

    upper = isotropic_gapped_angular_frequency(K, c, omega_0)
    for dimension in (1, 2, 3, 4):
        density = isotropic_continuum_dos_on_band(
            omega,
            V,
            c,
            omega_0,
            dimension,
            branches=branches,
        )
        direct_integral = sp.simplify(sp.integrate(density, (omega, omega_0, upper)))
        ball_count = isotropic_continuum_mode_count(
            K,
            V,
            dimension,
            branches=branches,
        )
        checks.check(
            f"d={dimension} frequency integral equals the radial ball count",
            sp.simplify(direct_integral - ball_count) == 0,
        )
        checks.check(
            f"d={dimension} fixed-K count is gap independent",
            sp.simplify(sp.diff(direct_integral, omega_0)) == 0,
        )

    target = sp.Symbol("N_target", positive=True)
    for dimension in (1, 2, 3, 4):
        cutoff = isotropic_continuum_target_cutoff(
            target,
            V,
            dimension,
            branches=branches,
        )
        checks.check(
            f"d={dimension} target cutoff inverts only the supplied count",
            sp.simplify(
                isotropic_continuum_mode_count(
                    cutoff,
                    V,
                    dimension,
                    branches=branches,
                )
                - target
            )
            == 0,
        )

    a = sp.Symbol("a", positive=True)
    md1_target = 3 * V / a**3
    md1_cutoff = isotropic_continuum_target_cutoff(
        md1_target, V, 3, branches=3
    )
    checks.check(
        "MD1 cutoff survives only after three branches and target are supplied",
        sp.simplify(md1_cutoff - (6 * sp.pi**2) ** sp.Rational(1, 3) / a) == 0,
    )
    checks.check(
        "one and three branches at fixed d3 differ by exactly three",
        sp.simplify(
            isotropic_continuum_mode_count(K, V, 3, branches=3)
            / isotropic_continuum_mode_count(K, V, 3, branches=1)
        )
        == 3,
    )

    expected_d3 = isotropic_continuum_mode_count(K, V, 3, branches=2)
    checks.mutation_sensitive(
        "sphere normalization and Fourier denominator are load bearing",
        lambda candidate: sp.simplify(candidate - expected_d3) == 0,
        2 * V * 4 * sp.pi * K**3 / (3 * (2 * sp.pi) ** 3),
        (
            2 * V * 2 * sp.pi * K**3 / (3 * (2 * sp.pi) ** 3),
            2 * V * 4 * sp.pi * K**3 / (3 * (2 * sp.pi) ** 2),
            V * 4 * sp.pi * K**3 / (3 * (2 * sp.pi) ** 3),
        ),
    )

    continuum_1d = isotropic_continuum_mode_count(1, 2 * sp.pi, 1)
    finite_periodic_count = len(tuple(index for index in range(-1, 2) if abs(index) <= 1))
    checks.check(
        "finite periodic lattice points counterexample continuum exact rank",
        continuum_1d == 2 and finite_periodic_count == 3,
    )
    sites = 5
    checks.check(
        "same three-dimensional space permits scalar and vector site ranks",
        1 * sites == 5 and 3 * sites == 15 and 1 * sites != 3 * sites,
    )
    couplings_sparse = (1, 0, 0, 0, 0)
    couplings_dense = (1, 1, 1, 1, 1)
    checks.check(
        "same total mode count permits different participating-mode counts",
        len(couplings_sparse) == len(couplings_dense) == 5
        and sum(value != 0 for value in couplings_sparse) == 1
        and sum(value != 0 for value in couplings_dense) == 5,
    )

    registry_text = (ROOT / "governance/claims.yaml").read_text(encoding="utf-8")
    checks.check(
        "accepted scalar spectrum explicitly leaves DOS cutoff and finite boxes separate",
        "finite-box mode, nonlinear existence theorem" in registry_text
        and "density of states, cutoff, lifetime" in registry_text,
    )
    checks.check(
        "source visibly conflates d3 and three mechanical degrees",
        "M_count = 3*N_cells" in source_text
        and "number of mechanical" in source_text
        and "d = 3" in source_text,
    )
    checks.check(
        "source WN6 verdict tests gap independence rather than participation",
        "WN6's premise is FALSE" in source_text
        and "sp.diff(integrated, omega0)" in source_text
        and "coupling" not in source_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())

