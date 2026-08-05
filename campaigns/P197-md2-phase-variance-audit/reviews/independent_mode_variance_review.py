#!/usr/bin/env python3
"""Independent raw-SymPy review of the P197 conditional variance claim."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-38/"
    "bridge_MD2_phase_variance_and_the_overparametrization.py"
)
SOURCE_SHA256 = "7dee2e731cc957c97ee151d3fd3349080460f2dc5781be8d4fd7869a589d2df0"
RELEASE_SHA256 = "0b549525847c57f4e246a2bd56331389ce6a8352468823b126b7f16e27b3a329"
FREEZE_SHA256 = "412bc390cf5268549240c1d708d79463a58fe96f037bd76795f0ba96100f416d"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P197-MD2-INDEPENDENT")
    checks.check("MD2 bytes are independently pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release is independently pinned",
        digest(ROOT / "governance/releases/v0.145.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze is independently pinned",
        digest(ROOT / "campaigns/P197-md2-phase-variance-audit/evidence/formula-freeze.yaml")
        == FREEZE_SHA256,
    )

    q = sp.symbols("q", real=True)
    hbar, mass, omega = sp.symbols("hbar mass omega", positive=True)
    psi = (mass * omega / (sp.pi * hbar)) ** sp.Rational(1, 4) * sp.exp(
        -mass * omega * q**2 / (2 * hbar)
    )
    norm = sp.integrate(psi**2, (q, -sp.oo, sp.oo))
    raw_variance = sp.integrate(q**2 * psi**2, (q, -sp.oo, sp.oo))
    checks.check("raw Gaussian ground state normalizes to one", sp.simplify(norm) == 1)
    checks.check(
        "raw Gaussian moment derives hbar over two m omega",
        sp.simplify(raw_variance - hbar / (2 * mass * omega)) == 0,
    )

    V, kappa, c = sp.symbols("V kappa c", positive=True)
    effective_mass = V * kappa / c**2
    raw_mode_variance = sp.simplify(raw_variance.subs(mass, effective_mass))
    checks.check(
        "raw effective-mass substitution gives the frozen one-mode variance",
        raw_mode_variance == hbar * c**2 / (2 * V * kappa * omega),
    )
    checks.check(
        "removing the Gaussian half changes the one-mode moment",
        sp.simplify(2 * raw_mode_variance - raw_mode_variance) != 0,
    )

    K, k, omega_0 = sp.symbols("K k omega_0", positive=True)
    omega_k = sp.sqrt(omega_0**2 + c**2 * k**2)
    raw_integrand = sp.simplify(
        V * 4 * sp.pi * k**2 / (2 * sp.pi) ** 3
        * raw_mode_variance.subs(omega, omega_k)
    )
    expected_integrand = hbar * c**2 * k**2 / (
        4 * sp.pi**2 * kappa * omega_k
    )
    checks.check(
        "raw volume and radial shell normalization reduce exactly",
        sp.simplify(raw_integrand - expected_integrand) == 0,
    )
    raw_integral = sp.simplify(sp.integrate(raw_integrand, (k, 0, K)))
    antiderivative_result = hbar / (8 * sp.pi**2 * kappa) * (
        K * sp.sqrt(omega_0**2 + c**2 * K**2)
        - omega_0**2 * sp.asinh(c * K / omega_0) / c
    )
    checks.check(
        "raw radial integration yields the frozen positive-gap form",
        sp.simplify(raw_integral - antiderivative_result) == 0,
    )
    checks.check(
        "independent differentiation recovers the radial integrand",
        sp.simplify(sp.diff(antiderivative_result, K) - expected_integrand.subs(k, K))
        == 0,
    )

    ell = c / omega_0
    X = sp.symbols("X", positive=True)
    raw_J = (X * sp.sqrt(1 + X**2) - sp.asinh(X)) / 2
    beta_squared = hbar * c / (kappa * ell**2)
    checks.check(
        "raw beta and length substitution is the same integral coordinate",
        sp.simplify(
            raw_integral
            - beta_squared * raw_J.subs(X, K * ell) / (4 * sp.pi**2)
        )
        == 0,
    )
    checks.check(
        "raw J derivative is positive and reconstructs its integrand",
        sp.simplify(sp.diff(raw_J, X) - X**2 / sp.sqrt(1 + X**2)) == 0
        and (X**2 / sp.sqrt(1 + X**2)).is_positive is True,
    )
    checks.check(
        "raw J has the exact leading large-cutoff ratio",
        sp.limit(raw_J / (X**2 / 2), X, sp.oo) == 1,
    )
    ratio = X / sp.sqrt(1 + X**2)
    upper_gap_derivative = sp.simplify(sp.diff(X**2 / 2 - raw_J, X))
    checks.check(
        "raw J upper-envelope gap has a positive derivative certificate",
        sp.simplify(upper_gap_derivative - X * (1 - ratio)) == 0
        and sp.simplify((1 - ratio) * (1 + ratio) - 1 / (1 + X**2)) == 0
        and (1 / (1 + X**2)).is_positive is True
        and (1 + ratio).is_positive is True,
    )
    gapless = hbar * c * K**2 / (8 * sp.pi**2 * kappa)
    checks.check(
        "raw positive-gap expression has the gapless limit",
        sp.simplify(sp.limit(raw_integral, omega_0, 0, dir="+") - gapless) == 0,
    )
    small = hbar * c**2 * K**3 / (12 * sp.pi**2 * kappa * omega_0)
    checks.check("raw small-cutoff leading ratio is one", sp.limit(raw_integral / small, K, 0, dir="+") == 1)
    checks.check(
        "raw result is UV-cutoff dependent",
        sp.simplify(sp.diff(raw_integral, K)) != 0,
    )
    checks.check(
        "raw result changes under branch multiplication",
        sp.simplify(3 * raw_integral - raw_integral) != 0,
    )
    checks.check(
        "raw result changes if Fourier normalization is removed",
        sp.simplify((2 * sp.pi) ** 3 * raw_integral - raw_integral) != 0,
    )

    fixed = (sp.Integer(1), sp.Integer(3))
    fixed_total = sum(fixed)
    fixed_mean = sp.Rational(fixed_total, len(fixed))
    checks.check("raw fixed-set factorization is exact", len(fixed) * fixed_mean == fixed_total)
    zero_added = fixed + (sp.Integer(0),)
    positive_added = fixed + (sp.Integer(5),)
    checks.check(
        "raw zero-mode extension changes count but not total",
        len(zero_added) != len(fixed) and sum(zero_added) == fixed_total,
    )
    checks.check(
        "raw positive extension changes count and total",
        len(positive_added) != len(fixed) and sum(positive_added) != fixed_total,
    )
    checks.check(
        "raw equal-mean families can have different totals",
        sp.Rational(sum((2, 2)), 2) == sp.Rational(sum((2, 2, 2)), 3)
        and sum((2, 2)) != sum((2, 2, 2)),
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)
    assigned = {
        node.id
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store)
    }
    checks.check(
        "source declares rather than derives hbar stiffness volume and cell scale",
        {"hbar", "K", "V", "a"} <= assigned,
    )
    checks.check(
        "source's M derivative acts after defining mean as S over M",
        "A2_mean = Ssym/Msym" in source_text
        and "sp.diff(growth_gap, Msym)" in source_text,
    )
    checks.check(
        "source's alleged two routes are one substitution chain",
        "S_asym_claim - S_at_a" in source_text
        and "beta2 = hbar*c/(K*ell**2)" in source_text,
    )
    review_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imported_modules = {
        node.module
        for node in ast.walk(review_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    imported_modules.update(
        alias.name
        for node in ast.walk(review_tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    )
    checks.check(
        "independent review imports no canonical variance implementation",
        "substrate_framework.quantum_mode_variance" not in imported_modules,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
