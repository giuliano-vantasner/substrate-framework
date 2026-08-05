#!/usr/bin/env python3
"""Primary exact verifier for C-QFL-001 and the P197 MD2 disposition."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.mode_counting import (
    isotropic_continuum_dos_on_band,
    isotropic_gapped_angular_frequency,
)
from substrate_framework.quantum_mode_variance import (
    gapped_vacuum_kernel,
    mode_variance_ledger,
    scalar_continuum_vacuum_variance_3d,
    scalar_mode_ground_state_variance,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-38/"
    "bridge_MD2_phase_variance_and_the_overparametrization.py"
)
SOURCE_SHA256 = "7dee2e731cc957c97ee151d3fd3349080460f2dc5781be8d4fd7869a589d2df0"
RELEASE_SHA256 = "0b549525847c57f4e246a2bd56331389ce6a8352468823b126b7f16e27b3a329"
FREEZE_SHA256 = "412bc390cf5268549240c1d708d79463a58fe96f037bd76795f0ba96100f416d"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def main() -> int:
    checks = CheckLedger("P197-MD2-PRIMARY")
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("MD2 source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        digest(ROOT / "governance/releases/v0.145.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned",
        digest(ROOT / "campaigns/P197-md2-phase-variance-audit/evidence/formula-freeze.yaml")
        == FREEZE_SHA256,
    )

    call_sites = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    literal_sites = [
        node
        for node in call_sites
        if node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ]
    checks.check(
        "source inventory separates 23 check sites from 26 executions",
        len(call_sites) == 23
        and len(literal_sites) == 22
        and len(call_sites) - len(literal_sites) == 1
        and sum(isinstance(node, ast.Assert) for node in ast.walk(source_tree)) == 0,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "MD2 has no NumPy integration compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    hbar, volume, kappa, c, omega, omega_0, K, k = sp.symbols(
        "hbar V kappa c omega omega_0 K k", positive=True
    )
    variance_k = scalar_mode_ground_state_variance(
        hbar, volume, kappa, c, omega
    )
    checks.check(
        "one-mode variance retains the ground-state half",
        sp.simplify(variance_k - hbar * c**2 / (2 * volume * kappa * omega)) == 0,
    )
    checks.check(
        "one-mode effective-mass normalization is reconstructed",
        sp.simplify(variance_k * (volume * kappa / c**2) * omega - hbar / 2)
        == 0,
    )

    dimensions = {
        "hbar": sp.Matrix([1, 2, -1]),
        "c": sp.Matrix([0, 1, -1]),
        "ell": sp.Matrix([0, 1, 0]),
        "kappa": sp.Matrix([1, 1, -2]),
    }
    beta_dimension = (
        dimensions["hbar"]
        + dimensions["c"]
        - dimensions["kappa"]
        - 2 * dimensions["ell"]
    )
    checks.check("declared d3 stiffness gives an action", dimensions["kappa"] + sp.Matrix([0, 1, 1]) == dimensions["hbar"])
    checks.check("the beta-squared coordinate is dimensionless", beta_dimension == sp.zeros(3, 1))

    frequency = isotropic_gapped_angular_frequency(k, c, omega_0)
    checks.check(
        "accepted typed dispersion is reused without a dimensional lift",
        sp.simplify(frequency**2 - omega_0**2 - c**2 * k**2) == 0,
    )
    density = isotropic_continuum_dos_on_band(
        omega, volume, c, omega_0, 3, branches=1
    )
    checks.check(
        "C-DOS-001 scalar d3 density retains one independent branch",
        density == volume * omega * sp.sqrt(omega**2 - omega_0**2) / (2 * sp.pi**2 * c**3),
    )

    X, x = sp.symbols("X x", positive=True)
    kernel = gapped_vacuum_kernel(X)
    checks.check(
        "J derivative reconstructs its radial inverse-frequency integrand",
        sp.simplify(sp.diff(kernel, X) - X**2 / sp.sqrt(1 + X**2)) == 0,
    )
    checks.check(
        "J closed form reconstructs its definite integral",
        sp.simplify(
            kernel - sp.integrate(x**2 / sp.sqrt(1 + x**2), (x, 0, X))
        )
        == 0,
    )
    checks.check(
        "J is strictly increasing on the positive domain",
        sp.simplify(sp.diff(kernel, X) - X**2 / sp.sqrt(1 + X**2)) == 0
        and (X**2 / sp.sqrt(1 + X**2)).is_positive is True,
    )

    canonical = scalar_continuum_vacuum_variance_3d(
        hbar, kappa, c, omega_0, K
    )
    direct = sp.integrate(
        hbar * c**2 * k**2 / (4 * sp.pi**2 * kappa * frequency),
        (k, 0, K),
    )
    checks.check(
        "canonical d3 variance equals the directly derived radial integral",
        sp.simplify(canonical - direct) == 0,
    )
    ell = c / omega_0
    beta_squared = hbar * c / (kappa * ell**2)
    checks.check(
        "MD2 beta-kernel form is an exact reparameterization",
        sp.simplify(
            canonical
            - beta_squared * gapped_vacuum_kernel(K * ell) / (4 * sp.pi**2)
        )
        == 0,
    )
    checks.check(
        "quantization volume cancels only after the declared continuum measure",
        volume not in canonical.free_symbols
        and sp.simplify(variance_k.subs(omega, frequency) * volume - hbar * c**2 / (2 * kappa * frequency)) == 0,
    )
    checks.check(
        "three identical branches multiply rather than emerge from d3",
        scalar_continuum_vacuum_variance_3d(
            hbar, kappa, c, omega_0, K, branches=3
        )
        == 3 * canonical,
    )

    gapless = scalar_continuum_vacuum_variance_3d(hbar, kappa, c, 0, K)
    checks.check(
        "positive-gap formula has the exact gapless cutoff limit",
        sp.simplify(sp.limit(canonical, omega_0, 0, dir="+") - gapless) == 0,
    )
    checks.check(
        "gapless scalar variance is quadratically cutoff dependent",
        gapless == hbar * c * K**2 / (8 * sp.pi**2 * kappa),
    )
    small_leading = hbar * c**2 * K**3 / (12 * sp.pi**2 * kappa * omega_0)
    checks.check(
        "small-cutoff limit retains cubic phase volume and the gap",
        sp.limit(canonical / small_leading, K, 0, dir="+") == 1,
    )
    checks.check(
        "large-X kernel leading term is one half X squared",
        sp.limit(kernel / (X**2 / 2), X, sp.oo) == 1,
    )
    upper_gap_derivative = sp.simplify(sp.diff(X**2 / 2 - kernel, X))
    ratio = X / sp.sqrt(1 + X**2)
    checks.check(
        "J upper-envelope derivative has an explicit positive certificate",
        sp.simplify(upper_gap_derivative - X * (1 - X / sp.sqrt(1 + X**2))) == 0
        and sp.simplify((1 - ratio) * (1 + ratio) - 1 / (1 + X**2)) == 0
        and (1 / (1 + X**2)).is_positive is True
        and (1 + ratio).is_positive is True,
    )
    expected_cutoff_derivative = hbar * c**2 * K**2 / (
        4 * sp.pi**2 * kappa * sp.sqrt(omega_0**2 + c**2 * K**2)
    )
    checks.check(
        "cutoff derivative recovers the load-bearing shell",
        sp.simplify(sp.diff(canonical, K) - expected_cutoff_derivative) == 0,
    )
    checks.check(
        "variance is linear in action scale and inverse in stiffness",
        sp.simplify(hbar * sp.diff(canonical, hbar) - canonical) == 0
        and sp.simplify(kappa * sp.diff(canonical, kappa) + canonical) == 0,
    )

    mutations = {
        "ground_state_half": 2 * canonical,
        "fourier_cube": (2 * sp.pi) ** 3 * canonical,
        "branch_factor": 3 * canonical,
        "cutoff": canonical.subs(K, 2 * K),
    }
    checks.check("normalization mutations are registered", len(mutations) == 4)
    for name, mutant in mutations.items():
        checks.check(
            f"load-bearing mutation {name} changes the claimed variance",
            sp.simplify(mutant - canonical) != 0,
        )

    fixed = mode_variance_ledger((sp.Integer(1), sp.Integer(3)))
    zero_added = mode_variance_ledger((sp.Integer(1), sp.Integer(3), sp.Integer(0)))
    positive_added = mode_variance_ledger((sp.Integer(1), sp.Integer(3), sp.Integer(5)))
    checks.check(
        "heterogeneous fixed modes have an exact arithmetic mean",
        fixed.count == 2 and fixed.total == 4 and fixed.arithmetic_mean == 2,
    )
    checks.check("fixed-set M-times-mean factorization is exact", fixed.factorization_residual == 0)
    checks.check(
        "adding a zero-variance mode changes count without changing total",
        zero_added.count == 3 and zero_added.total == fixed.total,
    )
    checks.check(
        "adding a positive-variance mode changes count and total",
        positive_added.count == 3 and positive_added.total == 9,
    )
    equal_two = mode_variance_ledger((2, 2))
    equal_three = mode_variance_ledger((2, 2, 2))
    checks.check(
        "holding the mean fixed while adding a mode changes total variance",
        equal_two.arithmetic_mean == equal_three.arithmetic_mean == 2
        and equal_two.total != equal_three.total,
    )

    queue = load(ROOT / "migration/source-claims.yaml")
    units = {row["source_unit"]: row for row in queue["units"]}
    checks.check(
        "AS6 and AS7 accepted mappings contain no MD2 beta or granularity premise",
        "C-QFL-001" not in units["AS6"]["accepted_claims"]
        and "C-QFL-001" not in units["AS7"]["accepted_claims"]
        and "C-DOS-001" not in units["AS7"]["accepted_claims"],
    )
    registry = load(ROOT / "governance/claims.yaml")
    claims = {claim["id"]: claim for claim in registry["claims"]}
    checks.check(
        "accepted classical medium explicitly remains one-dimensional",
        "energy-per-length" in claims["C-MED-003"]["statement"]
        and "psi_xx" in claims["C-SG-018"]["statement"]
        and "psi_yy" not in claims["C-SG-018"]["statement"],
    )
    checks.check(
        "accepted DOS explicitly supplies no state or occupation",
        "state" in claims["C-DOS-001"]["statement"]
        and "participating-mode" in claims["C-DOS-001"]["assumptions"][-1],
    )
    checks.check(
        "source visibly claims overdetermination from a substitution identity",
        "both forms agree => S is over-determined" in source_text,
    )
    checks.check(
        "source visibly differentiates a discrete count while fixing total S",
        "d/dM (n - M A^2) = 0" in source_text
        and "A2_mean = Ssym/Msym" in source_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
