#!/usr/bin/env python3
"""Exact source-aware verifier for proposed C-PRC-001 and M2."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.gauge_scalar_mass import (
    su2_u1_lower_doublet_mass_evidence,
)
from substrate_framework.proca import (
    mostly_plus_proca_momentum_evidence,
    normalized_proca_mode_evidence,
    transverse_half_line_proca_evidence,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P155-m2-meissner-proca-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-7/"
    "bridge_M2_meissner_proca_W_mass.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_AUDIT = CAMPAIGN / "evidence/source-audit.yaml"
SOURCE_SHA256 = "4ae3e5cb06e7c0bce6387ac7b84f555de65f12cce4be42d620405bb2b5c5b59f"
FROZEN_SHA256 = "eaf1f33bdc364be4cea2f583c2d408c24aa809289a2a8c06cce870f3f68d165f"
REVISION_SHA256 = "eacdffe9281468e2d0a6833c3abec9be6929c5bcee4450d0c4b5703515c1efda"
REPRODUCTION_SHA256 = "e0801c64553a034ad721e62bd497c5d3e82df776febc3e021e3b7def9685b568"
SOURCE_AUDIT_SHA256 = "0a97ce61c30129803aaaa177c37fb07e814d6621000e5c3dba70ad4e54885307"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> int:
    checks = CheckLedger("P155/C-PRC-001")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned M2 source hash", _sha256(SOURCE) == SOURCE_SHA256)
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
    checks.check("seven source predicates", len(source_checks) == 7)
    checks.check(
        "one source assertion",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    source_compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "M2 has no numerical integration compatibility surface",
        source_compatibility.numpy_aliases == ()
        and source_compatibility.legacy_references == 0
        and source_compatibility.current_references == 0,
    )
    checks.check(
        "source branch guard accepts either exponential sign",
        "ode_sol.rhs.has(sp.exp(-M_W * x)) or ode_sol.rhs.has(sp.exp(M_W * x))"
        in source_text,
    )
    loaded_names = [
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    ]
    checks.check(
        "source superconductor mass-squared assignment is unused",
        loaded_names.count("m_sc2") == 0,
    )

    m, omega, kx, ky, kz = sp.symbols(
        "m omega kx ky kz",
        positive=True,
    )
    momentum = mostly_plus_proca_momentum_evidence(
        m,
        omega,
        (kx, ky, kz),
    )
    checks.check(
        "full mixed-index kernel uses the frozen mostly-plus convention",
        momentum.metric == sp.diag(-1, 1, 1, 1)
        and momentum.momentum_norm_squared
        == -omega**2 + kx**2 + ky**2 + kz**2,
    )
    checks.check(
        "kernel contraction derives the massive divergence constraint",
        momentum.divergence_constraint_certified
        and momentum.divergence_contraction
        == -m**2 * momentum.momentum_covector.T,
    )
    checks.check(
        "transverse kernel derives the positive massive dispersion",
        momentum.transverse_kernel_factor
        == omega**2 - kx**2 - ky**2 - kz**2 - m**2
        and momentum.dispersion_frequency_squared
        == kx**2 + ky**2 + kz**2 + m**2
        and momentum.dispersion_residual == 0,
    )

    k = sp.Symbol("k", positive=True)
    on_shell = mostly_plus_proca_momentum_evidence(
        m,
        sp.sqrt(k**2 + m**2),
        (k, 0, 0),
    )
    transverse = (0, 0, 1, 0)
    longitudinal = (0, 1, 0, 0)
    checks.check(
        "on-shell transverse polarization solves the full vector equation",
        on_shell.transversality_residual(transverse) == 0
        and on_shell.euler_residual(transverse) == sp.zeros(4, 1),
    )
    checks.check(
        "scalar component equation falsely admits a longitudinal polarization",
        on_shell.transverse_kernel_factor == 0
        and on_shell.transversality_residual(longitudinal) == k
        and on_shell.euler_residual(longitudinal) != sp.zeros(4, 1),
    )

    amplitude = sp.Symbol("A0", real=True, nonzero=True)
    x = sp.Symbol("x", real=True)
    half_line = transverse_half_line_proca_evidence(
        m,
        amplitude,
        coordinate=x,
    )
    checks.check(
        "static characteristic equation contains both exact branches",
        half_line.characteristic_roots == (-m, m)
        and half_line.general_solution.has(sp.exp(-m * x))
        and half_line.general_solution.has(sp.exp(m * x)),
    )
    checks.check(
        "boundary and decay data certify the unique decaying profile",
        half_line.bvp_certified
        and half_line.decaying_profile == amplitude * sp.exp(-m * x)
        and half_line.decaying_basis_limit == 0
        and half_line.growing_basis_absolute_limit == sp.oo
        and half_line.selected_general_solution_residual == 0
        and half_line.penetration_length == 1 / m,
    )
    checks.check(
        "tangential profile satisfies the constraint while longitudinal copy fails",
        half_line.tangential_divergence_residual == 0
        and half_line.longitudinal_divergence
        == -amplitude * m * sp.exp(-m * x)
        and half_line.longitudinal_divergence != 0,
    )
    growing_only = sp.exp(m * x)
    source_or_guard = growing_only.has(sp.exp(-m * x)) or growing_only.has(
        sp.exp(m * x)
    )
    checks.check(
        "source OR guard accepts a growing-only counterexample",
        source_or_guard and sp.limit(growing_only, x, sp.oo) == sp.oo,
    )

    g, gp, v = sp.symbols("g gp v", positive=True)
    doublet = su2_u1_lower_doublet_mass_evidence(g, gp, v)
    coefficient = doublet.charged_mass_squared
    canonical = normalized_proca_mode_evidence(1, coefficient)
    noncanonical = normalized_proca_mode_evidence(4, coefficient)
    checks.check(
        "canonical C-GSM composition gives the conditional source formulas",
        coefficient == g**2 * v**2 / 4
        and canonical.mass == g * v / 2
        and canonical.penetration_length == 2 / (g * v),
    )
    checks.check(
        "positive kinetic normalization changes mass and penetration length",
        noncanonical.mass_squared == coefficient / 4
        and noncanonical.mass == g * v / 4
        and noncanonical.penetration_length == 4 / (g * v),
    )

    massless_contraction = momentum.divergence_contraction.subs(m, 0)
    checks.check(
        "zero mass removes the algebraic transversality implication",
        massless_contraction == sp.zeros(1, 4)
        and momentum.momentum_covector.T != sp.zeros(1, 4),
    )
    tachyonic_frequency_squared = sp.simplify(k**2 - m**2)
    checks.check(
        "wrong mass-sign mutation loses the positive rest gap",
        tachyonic_frequency_squared.subs(k, 0) == -m**2
        and tachyonic_frequency_squared
        != on_shell.dispersion_frequency_squared,
    )
    doubled_coefficient = normalized_proca_mode_evidence(1, 2 * coefficient)
    checks.check(
        "quadratic factor mutation changes the normalized inverse length",
        sp.simplify(doubled_coefficient.mass / canonical.mass - sp.sqrt(2)) == 0,
    )
    london_label, weak_label, substrate_label = sp.symbols(
        "london_label weak_label substrate_label"
    )
    checks.check(
        "identical Proca BVP leaves physical dictionaries free",
        all(
            label not in half_line.decaying_profile.free_symbols
            for label in (london_label, weak_label, substrate_label)
        ),
    )

    mutable_python = sorted(CAMPAIGN.rglob("*.py")) + [
        ROOT / "src/substrate_framework/proca.py",
        ROOT / "tests/test_proca.py",
    ]
    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
        for path in mutable_python
    ]
    checks.check(
        "mutable P155 and canonical code has no executable legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )

    tally = checks.finish()
    print(f"P155 PRIMARY ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
