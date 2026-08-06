#!/usr/bin/env python3
"""Primary exact verifier for GC4's interaction and phase-capacity audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.phase_interactions import (
    pairwise_phase_cosines,
    quartic_sech_pair_interaction,
    scalar_circle_packing,
    sech_pair_density_shape,
    sech_pair_mixed_cubic_shape,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-42/"
    "bridge_GC4_stability_forces_three.py"
)
SOURCE_SHA256 = "3292400544911dca74009a019b24b44f105f8aeb5c68a6172220903950f465bb"
RELEASE_SHA256 = "923444a67cb0c039b8c9c22dd1b8d4c8d9aa187d66caa282d739a794f19738b6"
FORMULA_FREEZE_SHA256 = "322955eff91f3861d544366b72b7a301954f36ba8eb06e6f3d573677cf0612bd"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def claim_statement(claim_id: str) -> str:
    registry = load(ROOT / "governance/claims.yaml")
    for claim in registry["claims"]:
        if claim["id"] == claim_id:
            return str(claim["statement"])
    raise KeyError(claim_id)


def main() -> int:
    checks = CheckLedger("P211-GC4-PHASE-CAPACITY-AUDIT")
    checks.check("source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        digest(ROOT / "governance/releases/v0.152.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned",
        digest(CAMPAIGN / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )
    proposal = load(CAMPAIGN / "proposal.yaml")
    checks.check(
        "proposal registers both minimum novel exact surfaces",
        proposal["claims_proposed"] == ["C-QBL-006", "C-PHS-001"],
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "source predicate and assertion inventories remain exact",
        sum(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            for node in ast.walk(source_tree)
        )
        == 8
        and sum(isinstance(node, ast.Assert) for node in ast.walk(source_tree)) == 1,
    )
    checks.check(
        "source has no NumPy quadrature compatibility surface",
        compatibility.legacy_references
        == compatibility.current_references
        == compatibility.eager_legacy_default_fallbacks
        == 0,
    )

    f, g, c = sp.symbols("f g c", real=True)
    modulus_squared = f**2 + g**2 + 2 * c * f * g
    quartic_cross = sp.expand(modulus_squared**2 - f**4 - g**4)
    expected_quartic_cross = (
        2 * f**2 * g**2
        + 4 * c * f * g * (f**2 + g**2)
        + 4 * c**2 * f**2 * g**2
    )
    checks.check(
        "direct quartic expansion retains constant linear and quadratic phase powers",
        sp.expand(quartic_cross - expected_quartic_cross) == 0,
    )

    i31, i22 = sp.symbols("I31 I22", positive=True)
    quadratic_cross_on_shell = i31 / 12
    reduced = sp.expand(
        2 * c * quadratic_cross_on_shell
        - (2 * i22 + 8 * c * i31 + 4 * c**2 * i22) / 24
    )
    expected_reduced = -c * i31 / 6 - (1 + 2 * c**2) * i22 / 12
    checks.check(
        "profile equation reduces the full cross energy exactly",
        sp.simplify(reduced - expected_reduced) == 0,
    )

    t = sp.symbols("t", real=True)
    source_separation = sp.log(3)
    ch = sp.cosh(source_separation)
    sh = sp.sinh(source_separation)
    fresh_31 = sp.integrate((1 - t**2) / (ch - sh * t), (t, -1, 1))
    fresh_22 = sp.integrate((1 - t**2) / (ch - sh * t) ** 2, (t, -1, 1))
    checks.check(
        "mixed cubic overlap shape has an independent rational-substitution integral",
        sp.simplify(
            fresh_31 - sech_pair_mixed_cubic_shape(source_separation)
        )
        == 0,
    )
    checks.check(
        "density overlap shape has an independent rational-substitution integral",
        sp.simplify(fresh_22 - sech_pair_density_shape(source_separation)) == 0,
    )

    s = sp.symbols("s", positive=True)
    j31 = sech_pair_mixed_cubic_shape(s)
    j22 = sech_pair_density_shape(s)
    checks.check(
        "coincident overlap limits recover the sech fourth-power integral",
        sp.limit(j31, s, 0, dir="+") == sp.Rational(4, 3)
        and sp.limit(j22, s, 0, dir="+") == sp.Rational(4, 3),
    )
    checks.check(
        "mixed cubic tail has exact leading four exp minus separation",
        sp.limit(sp.exp(s) * j31, s, sp.oo) == 4,
    )
    checks.check(
        "density tail has exact doubled-rate linear prefactor",
        sp.limit(j22 / (16 * (s - 1) * sp.exp(-2 * s)), s, sp.oo) == 1,
    )

    d, amplitude, kappa = sp.symbols("d A kappa", positive=True)
    interaction = quartic_sech_pair_interaction(d, c, amplitude, kappa)
    checks.check(
        "canonical interaction equals the independently reduced expression",
        sp.simplify(
            interaction.interaction_energy
            + c * interaction.mixed_cubic_overlap / 6
            + (1 + 2 * c**2) * interaction.density_overlap / 12
        )
        == 0,
    )
    checks.check(
        "finite-separation interaction is not a pure cosine",
        sp.simplify(sp.diff(interaction.interaction_energy, c, 2)) != 0,
    )
    perpendicular = quartic_sech_pair_interaction(d, 0, amplitude, kappa)
    checks.check(
        "perpendicular phase has an exact negative interaction rather than a numeric residue",
        sp.simplify(
            perpendicular.interaction_energy
            + perpendicular.density_overlap / 12
        )
        == 0,
    )

    omega = sp.Rational(45, 100)
    source_kappa = sp.sqrt(sp.Rational(1, 2) - omega**2)
    source_amplitude = 2 * sp.sqrt(6) * source_kappa
    source_cases = [
        (6, 1, -3.557102022641099),
        (10, -1, 0.23597506089536688),
        (12, 0, -0.0014269303147464918),
    ]
    checks.check(
        "exact formula reproduces source values without grid quadrature",
        all(
            abs(
                float(
                    quartic_sech_pair_interaction(
                        distance, cosine, source_amplitude, source_kappa
                    ).interaction_energy
                )
                - expected
            )
            < 2e-13
            for distance, cosine, expected in source_cases
        ),
    )

    distance = sp.symbols("distance", positive=True)
    anti_energy = quartic_sech_pair_interaction(distance, -1, 1, 1).interaction_energy
    z3_energy = quartic_sech_pair_interaction(
        distance, -sp.Rational(1, 2), 1, 1
    ).interaction_energy
    anti_force = -sp.diff(anti_energy, distance)
    z3_force = -sp.diff(z3_energy, distance)
    checks.check(
        "anti-phase generalized force changes sign outside the sampled tail regime",
        float(anti_force.subs(distance, 1)) < 0
        and float(anti_force.subs(distance, 6)) > 0,
    )
    checks.check(
        "Z3 pair generalized force also changes sign",
        float(z3_force.subs(distance, 1)) < 0
        and float(z3_force.subs(distance, 6)) > 0,
    )
    checks.check(
        "repulsive tail tends to zero and supplies no finite bound minimum",
        sp.limit(z3_energy, distance, sp.oo) == 0
        and float(z3_energy.subs(distance, 6)) > 0,
    )

    packings = {n: scalar_circle_packing(n) for n in range(2, 7)}
    checks.check(
        "nearest-gap obstruction is exact for counts two through six",
        all(
            item.nearest_gap_upper_bound == 2 * sp.pi / n
            for n, item in packings.items()
        ),
    )
    checks.check(
        "regular polygons attain the sharp worst-pair cosine",
        all(
            max(item.regular_pairwise_cosines)
            == item.optimal_worst_pairwise_cosine
            for item in packings.values()
        ),
    )
    checks.check(
        "strict scalar-circle capacity is three",
        [packings[n].strictly_negative_possible for n in range(2, 7)]
        == [True, True, False, False, False],
    )
    checks.check(
        "weak scalar-circle capacity is four",
        [packings[n].nonpositive_possible for n in range(2, 7)]
        == [True, True, True, False, False],
    )
    checks.check(
        "Z3 and quadrature witnesses have exact pairwise cosines",
        pairwise_phase_cosines((0, 2 * sp.pi / 3, 4 * sp.pi / 3))
        == (-sp.Rational(1, 2),) * 3
        and max(pairwise_phase_cosines((0, sp.pi / 2, sp.pi, 3 * sp.pi / 2)))
        == 0,
    )
    checks.check(
        "capacity cannot select exactly three because two also satisfies the strict rule",
        packings[2].strictly_negative_possible
        and packings[3].strictly_negative_possible,
    )

    sparse_phases = (0, sp.pi, 0, sp.pi)
    sparse_edges = ((0, 1), (1, 2), (2, 3), (3, 0))
    checks.check(
        "four-cycle countermodel makes every interacting edge negative",
        all(
            sp.cos(sparse_phases[i] - sparse_phases[j]) == -1
            for i, j in sparse_edges
        )
        and max(pairwise_phase_cosines(sparse_phases)) == 1,
    )
    tetrahedron = [
        sp.Matrix(vector) / sp.sqrt(3)
        for vector in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    ]
    checks.check(
        "higher internal orientation space admits four pairwise negative products",
        all(
            sp.simplify(tetrahedron[i].dot(tetrahedron[j]))
            == -sp.Rational(1, 3)
            for i in range(4)
            for j in range(i + 1, 4)
        ),
    )

    mix_statement = claim_statement("C-MIX-002")
    qball_statement = claim_statement("C-QBL-001")
    checks.check(
        "accepted phase-count claim denies the physical lower bound used by GC4",
        "no quark or generation map" in mix_statement
        and "physical CP operation or violation" in mix_statement,
    )
    checks.check(
        "accepted quartic profile denies the stability window used by GC4",
        "no VK, spectral, orbital, or nonlinear stability" in qball_statement,
    )

    imported_modules = {
        node.names[0].name
        for node in source_tree.body
        if isinstance(node, ast.Import)
    }
    checks.check(
        "static source imports expose no file network or measured-data loader",
        imported_modules == {"itertools", "numpy", "sympy"}
        and not any(isinstance(node, (ast.ImportFrom, ast.With)) for node in ast.walk(source_tree)),
    )
    checks.check(
        "source triple check calls only the two-profile E_int helper",
        "pair_ints[(i, j)] = E_int(10.0, dth)" in source_text
        and source_text.count("Ppair =") == 1,
    )

    checks.mutation_sensitive(
        "finite interaction rejects the source pure-cosine truncation",
        lambda expression: sp.simplify(
            expression.subs(c, 0) - perpendicular.interaction_energy
        )
        == 0,
        interaction.interaction_energy,
        [interaction.linear_phase_energy],
    )
    checks.mutation_sensitive(
        "capacity verdict is sensitive to strictness",
        lambda result: result == (3, 4),
        (
            max(n for n, item in packings.items() if item.strictly_negative_possible),
            max(n for n, item in packings.items() if item.nonpositive_possible),
        ),
        [(4, 4), (3, 3)],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
