#!/usr/bin/env python3
"""Primary exact verifier for provisional C-QBL-005 and GC1."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.normalized_overlaps import (
    quartic_bound_mode_overlap_ledger,
)
from substrate_framework.qball_fluctuations import (
    quartic_binding_coupling_ledger,
    quartic_curvature_deficit,
    quartic_fluctuation_bound_eigenvalues,
    quartic_fluctuation_continuum_threshold,
    quartic_fluctuation_potential,
)
from substrate_framework.quartic_qball import quartic_qball_profile
from substrate_framework.source_audit import (
    audit_numpy_trapezoid_compatibility,
)
from substrate_framework.translated_localization import (
    poschl_teller_ground_ledger,
)
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-42/"
    "bridge_GC1_overlap_binding_lock.py"
)
SOURCE_SHA256 = "3c9610d349b7fa0e47a4f122ea5ab84da3a03f6cd83686c3aa6f161bfccf4ebe"
RELEASE_SHA256 = "18dffeef5efd516018c918f65b45173c81ac0e1ba99fdd8a96274cc1df5c72db"
FORMULA_FREEZE_SHA256 = "e90af124bdc8d0d188dfe02470c71aeb6b40da6b95c4625c2969e39d893f9569"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def main() -> int:
    checks = CheckLedger("P208-GC1-OVERLAP-BINDING")
    checks.check("source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        digest(ROOT / "governance/releases/v0.150.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "post-source formula freeze remains pinned",
        digest(CAMPAIGN / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
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
        "source predicate and assertion inventories remain exact",
        len(source_checks) == 9
        and sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 2,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "source has no NumPy quadrature compatibility surface",
        compatibility.legacy_references
        == compatibility.current_references
        == compatibility.eager_legacy_default_fallbacks
        == 0,
    )

    field, frequency = sp.symbols("f omega", real=True)
    scale = sp.symbols("lambda", nonzero=True, real=True)
    ledger = quartic_binding_coupling_ledger(field, frequency, scale)
    checks.check(
        "quartic curvature deficit is derived from the potential",
        quartic_curvature_deficit(field, frequency) == field**2 / 4
        and ledger.vacuum_curvature
        == sp.Rational(1, 2) - frequency**2
        and ledger.field_curvature
        == sp.Rational(1, 2) - frequency**2 - field**2 / 4,
    )
    checks.check(
        "linear coupling lock retains the supplied normalization",
        ledger.local_coupling == scale * field
        and ledger.lock_coefficient == 1 / (4 * scale**2)
        and ledger.lock_residual == 0,
    )

    nonlinear_coupling = field**2
    nonlinear_residual = sp.simplify(
        ledger.curvature_deficit - nonlinear_coupling**2 / 4
    )
    independent_coupling = sp.symbols("c_independent", real=True)
    independent_residual = sp.simplify(
        ledger.curvature_deficit - independent_coupling**2 / 4
    )
    checks.check(
        "nonlinear and independent coupling maps break the source lock",
        nonlinear_residual != 0
        and independent_residual != 0
        and independent_residual.has(field, independent_coupling),
    )

    epsilon = sp.symbols("epsilon", nonzero=True, real=True)
    deformed = ledger.effective_potential + epsilon * field**6
    deformed_deficit = sp.simplify(
        sp.diff(deformed, field, 2).subs(field, 0)
        - sp.diff(deformed, field, 2)
    )
    checks.check(
        "sextic potential deformation changes the curvature relation",
        deformed_deficit == field**2 / 4 - 30 * epsilon * field**4
        and sp.simplify(deformed_deficit - ledger.curvature_deficit) != 0,
    )

    coordinate, center = sp.symbols("x x_0", real=True)
    positive_frequency = sp.symbols("omega_positive", positive=True)
    profile = quartic_qball_profile(coordinate, positive_frequency, center)
    kappa = sp.sqrt(sp.Rational(1, 2) - positive_frequency**2)
    profile_deficit = quartic_curvature_deficit(profile, positive_frequency)
    checks.check(
        "quartic profile substitution gives the exact sech-squared deficit",
        sp.simplify(
            profile_deficit
            - 6 * kappa**2 * sp.sech(kappa * (coordinate - center)) ** 2
        )
        == 0,
    )
    potential = quartic_fluctuation_potential(
        coordinate, positive_frequency, center
    )
    derivative = sp.factor(sp.diff(potential, coordinate))
    expected_derivative = (
        12
        * kappa**3
        * sp.sech(kappa * (coordinate - center)) ** 2
        * sp.tanh(kappa * (coordinate - center))
    )
    checks.check(
        "quartic fluctuation well has one exact center",
        sp.simplify(derivative - expected_derivative) == 0
        and sp.simplify(derivative.subs(coordinate, center)) == 0
        and sp.simplify(
            sp.diff(potential, coordinate, 2).subs(coordinate, center)
            - 12 * kappa**4
        )
        == 0,
    )

    positive_kappa = sp.symbols("kappa", positive=True)
    amplitude = sp.sqrt(24) * positive_kappa
    overlaps = quartic_bound_mode_overlap_ledger(amplitude, positive_kappa)
    checks.check(
        "quartic bound-mode overlap ratio is fixed but absolute overlaps scale to zero",
        sp.simplify(overlaps.odd_overlap / overlaps.even_overlap)
        == sp.Rational(2, 3)
        and sp.limit(overlaps.even_overlap, positive_kappa, 0, dir="+") == 0
        and sp.limit(overlaps.odd_overlap, positive_kappa, 0, dir="+") == 0,
    )
    eigenvalues = (-3 * positive_kappa**2, sp.Integer(0))
    threshold = positive_kappa**2
    checks.check(
        "small absolute overlaps coexist with bound quartic levels at every positive width",
        bool(eigenvalues[0] < threshold)
        and bool(eigenvalues[1] < threshold)
        and quartic_fluctuation_bound_eigenvalues(sp.Rational(1, 2))
        == (-sp.Rational(3, 4), 0)
        and quartic_fluctuation_continuum_threshold(sp.Rational(1, 2))
        == sp.Rational(1, 4),
    )

    depth, width = sp.symbols("D_0 w", positive=True)
    shallow = poschl_teller_ground_ledger(depth, width)
    checks.check(
        "every positive Poschl depth has an exact negative ground level",
        sp.simplify(shallow.index * (shallow.index + 1) - depth * width**2)
        == 0
        and sp.simplify(shallow.eigenvalue + shallow.index**2 / width**2)
        == 0
        and shallow.index
        == (sp.sqrt(1 + 4 * depth * width**2) - 1) / 2,
    )
    checks.check(
        "arbitrarily shallow numeric wells retain a negative ground level",
        all(
            float(poschl_teller_ground_ledger(value, 1).eigenvalue) < 0.0
            for value in (sp.Rational(1, 10), sp.Rational(1, 10**6))
        ),
    )

    probability, left, right = sp.symbols("p a b", real=True)
    mean = probability * left + (1 - probability) * right
    second = probability * left**2 + (1 - probability) * right**2
    variance_identity = sp.factor(second - mean**2)
    checks.check(
        "RMS versus mean-absolute ratio is the universal variance inequality",
        sp.simplify(
            variance_identity
            - probability * (1 - probability) * (left - right) ** 2
        )
        == 0,
    )
    displacement = sp.symbols("R", positive=True)
    point_mean_absolute = displacement
    point_rms = sp.sqrt(displacement**2)
    checks.check(
        "source RMS ratio cannot distinguish an exactly relocated point density",
        sp.simplify(point_rms / point_mean_absolute) == 1,
    )

    assignments = {
        node.targets[0].id: node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
    }
    sweep = ast.literal_eval(assignments["OMEGA_SWEEP"])
    checks.check(
        "source all-frequency conclusion is only an eight-point sweep",
        len(sweep) == 8
        and min(sweep) == 0.30
        and max(sweep) == 0.65
        and "bound_holds = min_yell > 0.1" in source_text,
    )
    checks.check(
        "source numeric model is exact-sine while the headline identity is quartic",
        "0.5 * np.sin(y[0]) - om**2 * y[0]" in source_text
        and "Vg = 0.5 * np.cos(f0f) - om**2" in source_text
        and "Uprime = kappa**2 * f_sym - f_sym**3 / 12" in source_text,
    )
    sine_deficit = sp.simplify((1 - sp.cos(field)) / 2)
    checks.check(
        "exact-sine curvature deficit differs beyond the quartic limit",
        sp.simplify(sine_deficit - field**2 / 4) != 0
        and sp.series(sine_deficit, field, 0, 7)
        == field**2 / 4 - field**4 / 48 + field**6 / 1440 + sp.Order(field**7),
    )

    claims = {
        claim["id"]: claim
        for claim in load(ROOT / "governance/claims.yaml")["claims"]
    }
    checks.check(
        "accepted quartic spectrum supplies two non-generation levels only",
        "exactly two simple levels" in claims["C-QBL-003"]["statement"]
        and "not positive particle masses or generations"
        in claims["C-QBL-003"]["statement"],
    )
    checks.check(
        "accepted exact-sine branch supplies no stability window",
        "no elementary closed form" in claims["C-QBL-002"]["statement"]
        and "VK or nonlinear stability" in claims["C-QBL-002"]["statement"],
    )
    checks.check(
        "accepted translated wells are separate isospectral declarations",
        "Translation changes R but not its spectrum"
        in claims["C-OVL-002"]["statement"]
        and "not an additional eigenlevel of one fixed operator"
        in " ".join(claims["C-OVL-002"]["assumptions"]),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
