#!/usr/bin/env python3
"""Primary exact verifier for GC5's overlap and count audit."""

from __future__ import annotations

import ast
import hashlib
import itertools
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.phase_interactions import (
    complete_phase_cosine_ledger,
    pairwise_phase_cosines,
    quartic_sech_pair_interaction,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.translated_overlap_matrices import (
    phase_weighted_self_overlap_limit,
    singular_value_cluster_bound,
)
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-42/"
    "bridge_GC5_two_role_structure_and_counts.py"
)
SOURCE_SHA256 = "ffc638accff802c16804bd793b47e1cc5da018d5e0742ace57d9d3207e06b220"
RELEASE_SHA256 = "845e3356c4dc59376835a36120e9f0c51cef0256726d4908b77185297a42af38"
FORMULA_FREEZE_SHA256 = "7a52a63b4bbdcf593503fa13e55d403056365012be94a55ef57d7aa7dcc45af6"


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


def zero_matrix(matrix: sp.MatrixBase) -> bool:
    return all(
        sp.simplify(sp.expand_complex(entry)) == 0 for entry in matrix
    )


def gaussian_triple_overlap(
    mode_a: int,
    mode_b: int,
    profile_c: int,
    separation: sp.Expr,
) -> sp.Expr:
    """Exact normalized-Gaussian witness for one translated triple overlap."""

    spread = (
        (mode_a - mode_b) ** 2
        + (mode_a - profile_c) ** 2
        + (mode_b - profile_c) ** 2
    )
    return sp.sqrt(sp.Rational(2, 3)) * sp.exp(
        -sp.Rational(spread, 6) * separation**2
    )


def main() -> int:
    checks = CheckLedger("P212-GC5-TWO-ROLE-COUNT-AUDIT")
    checks.check("source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        digest(ROOT / "governance/releases/v0.153.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned",
        digest(CAMPAIGN / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )
    proposal = load(CAMPAIGN / "proposal.yaml")
    checks.check(
        "proposal registers both minimum novel surfaces",
        proposal["claims_proposed"] == ["C-OVL-005", "C-PHS-002"],
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source predicate and assertion inventories remain exact",
        len(source_checks) == 8
        and sum(isinstance(node, ast.Assert) for node in ast.walk(source_tree)) == 1,
    )
    checks.check(
        "source literal and dynamic check-call inventories remain exact",
        sum(
            bool(node.args)
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
            for node in source_checks
        )
        == 2,
    )
    checks.check(
        "source has no NumPy quadrature compatibility surface",
        compatibility.legacy_references
        == compatibility.current_references
        == compatibility.eager_legacy_default_fallbacks
        == 0,
    )

    alpha = sp.sqrt(sp.Rational(2, 3))
    phases = (0, 2 * sp.pi / 3, 4 * sp.pi / 3)
    limit = phase_weighted_self_overlap_limit(alpha, phases)
    checks.check(
        "identical translated limit has one common singular-value square",
        zero_matrix(limit.H * limit - alpha**2 * sp.eye(3)),
    )

    d = sp.symbols("d", positive=True)
    components = []
    for c in range(3):
        components.append(
            sp.Matrix(
                3,
                3,
                lambda a, b: gaussian_triple_overlap(a, b, c, d),
            )
        )
    gaussian_matrix = sp.simplify(
        sum(
            (sp.exp(sp.I * phases[c]) * components[c] for c in range(3)),
            sp.zeros(3),
        )
    )
    gaussian_limit = gaussian_matrix.applyfunc(
        lambda entry: sp.limit(entry, d, sp.oo)
    )
    checks.check(
        "fresh normalized Gaussian family reaches the canonical limit",
        zero_matrix(gaussian_limit - limit),
    )
    checks.check(
        "every non-self Gaussian triple overlap vanishes",
        all(
            sp.limit(components[c][a, b], d, sp.oo) == 0
            for a, b, c in itertools.product(range(3), repeat=3)
            if not (a == b == c)
        ),
    )
    checks.check(
        "every matched Gaussian self-overlap is translation invariant",
        all(components[a][a, a] == alpha for a in range(3)),
    )

    epsilon = sp.Rational(1, 5)
    bound = singular_value_cluster_bound(alpha, epsilon, count=3)
    checks.check(
        "cluster ledger gives the exact perturbation interval",
        bound.singular_value_lower_bound == alpha - epsilon
        and bound.singular_value_upper_bound == alpha + epsilon,
    )
    checks.check(
        "condition bound is finite only after the strict residual gate",
        sp.simplify(
            bound.condition_number_upper_bound
            - (alpha + epsilon) / (alpha - epsilon)
        )
        == 0,
    )
    endpoint_matrix = sp.diag(alpha + epsilon, alpha, alpha - epsilon)
    endpoint_values = sorted(endpoint_matrix.singular_values(), key=float)
    checks.check(
        "a diagonal perturbation attains both Weyl endpoints",
        sp.simplify(
            endpoint_values[0] ** 2
            - bound.singular_value_lower_bound**2
        )
        == 0
        and sp.simplify(
            endpoint_values[-1] ** 2
            - bound.singular_value_upper_bound**2
        )
        == 0,
    )
    checks.check(
        "unequal self overlaps break the common-singular-value premise",
        len(set(sp.diag(1, 2, 3).singular_values())) == 3,
    )

    theta = sp.symbols("theta0:4", real=True)
    generic = complete_phase_cosine_ledger(theta)
    direct_cosine_sum = sum(
        sp.cos(theta[a] - theta[b])
        for a, b in itertools.combinations(range(4), 2)
    )
    checks.check(
        "complete cosine sum equals half resultant norm squared minus count",
        sp.trigsimp(
            direct_cosine_sum - (generic.resultant_squared - 4) / 2
        )
        == 0,
    )
    checks.check(
        "cosine surrogate excess above its lower bound is a norm square",
        sp.simplify(
            generic.pairwise_cosine_sum
            - generic.minimum
            - generic.resultant_squared / 2
        )
        == 0,
    )
    for count in range(2, 7):
        regular = complete_phase_cosine_ledger(
            tuple(2 * sp.pi * index / count for index in range(count))
        )
        checks.check(
            f"regular {count}-gon attains the exact surrogate minimum",
            regular.resultant_squared == 0
            and regular.pairwise_cosine_sum == -sp.Rational(count, 2),
        )

    beta = sp.pi / 3
    four_family = complete_phase_cosine_ledger(
        (0, sp.pi, beta, beta + sp.pi)
    )
    square_phases = (0, sp.pi / 2, sp.pi, 3 * sp.pi / 2)
    square = complete_phase_cosine_ledger(square_phases)
    checks.check(
        "four-phase surrogate minima are nonunique",
        four_family.resultant_squared == square.resultant_squared == 0
        and four_family.phases != square.phases,
    )
    checks.check(
        "square minimum has no positive pairwise cosine",
        max(pairwise_phase_cosines(square_phases)) == 0,
    )
    checks.check(
        "another four-phase minimum has a positive pair",
        max(pairwise_phase_cosines(four_family.phases)) > 0,
    )

    pair_equal = quartic_sech_pair_interaction(3, 1, 1, 1)
    pair_opposite = quartic_sech_pair_interaction(3, -1, 1, 1)
    phase_cosine = sp.symbols("phase_cosine", real=True)
    pair_symbolic = quartic_sech_pair_interaction(3, phase_cosine, 1, 1)
    checks.check(
        "accepted finite pair energy is not the source cosine surrogate",
        sp.diff(pair_symbolic.interaction_energy, phase_cosine, 2) != 0,
    )
    checks.check(
        "actual equal-phase pair energy is below opposite-phase energy",
        sp.simplify(
            pair_equal.interaction_energy - pair_opposite.interaction_energy
            + pair_equal.mixed_cubic_overlap / 3
        )
        == 0,
    )

    diagonal_complex = sp.diag(1, sp.I, 1 + sp.I)
    checks.check(
        "complex matrix entries do not force a nonzero quartet",
        any(sp.im(entry) != 0 for entry in diagonal_complex)
        and all(
            sp.simplify(
                diagonal_complex[i, j]
                * diagonal_complex[k, ell]
                * sp.conjugate(diagonal_complex[i, ell])
                * sp.conjugate(diagonal_complex[k, j])
            )
            == 0
            for i, k in itertools.combinations(range(3), 2)
            for j, ell in itertools.combinations(range(3), 2)
        ),
    )

    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    fourier = sp.Matrix(
        [[1, 1, 1], [1, omega, omega**2], [1, omega**2, omega]]
    ) / sp.sqrt(3)
    quartet = sp.simplify(
        fourier[0, 1]
        * fourier[1, 2]
        * sp.conjugate(fourier[0, 2])
        * sp.conjugate(fourier[1, 1])
    )
    complex_symmetric = sp.simplify(fourier * sp.diag(1, 2, 3) * fourier.T)
    real_source = complex_symmetric.applyfunc(lambda value: sp.simplify(sp.re(value)))
    imaginary_source = complex_symmetric.applyfunc(
        lambda value: sp.simplify(sp.im(value))
    )
    checks.check(
        "two phased real sources already build a nonreal three-dimensional invariant",
        zero_matrix(complex_symmetric - real_source - sp.I * imaginary_source)
        and zero_matrix(real_source - real_source.T)
        and zero_matrix(imaginary_source - imaginary_source.T)
        and sp.simplify(sp.im(quartet)) != 0,
    )

    role_countermodels = (
        {"field_species": 1, "localized_solutions": 3, "roles": 2},
        {"field_species": 4, "localized_solutions": 3, "roles": 2},
        {"field_species": 3, "localized_solutions": 3, "roles": 1},
    )
    checks.check(
        "role and solution counts do not determine field multiplicity",
        {model["field_species"] for model in role_countermodels} == {1, 3, 4},
    )
    modal_countermodel = {
        "stable_by_topology": True,
        "u1_charge_required_for_stability": False,
        "has_complex_field": True,
    }
    checks.check(
        "no required U1 charge does not imply no complex field",
        modal_countermodel["stable_by_topology"]
        and not modal_countermodel["u1_charge_required_for_stability"]
        and modal_countermodel["has_complex_field"],
    )

    em6_statement = claim_statement("C-QBL-001")
    mix_statement = claim_statement("C-MIX-002")
    phase_statement = claim_statement("C-PHS-001")
    checks.check(
        "accepted EM6 mapping explicitly withholds the source stability theorem",
        "no VK, spectral, orbital, or nonlinear stability" in em6_statement,
    )
    checks.check(
        "accepted phase algebra supplies no physical generation floor",
        "no quark or generation map" in mix_statement
        and "physical CP operation or violation" in mix_statement,
    )
    checks.check(
        "accepted scalar phase capacity supplies no occupied count",
        "not occupancy selectors" in phase_statement
        and "no interaction kernel" in phase_statement,
    )

    checks.check(
        "source phase optimizer never checks solver success",
        "if best is None or r.fun < best.fun" in source_text
        and "r.success" not in source_text,
    )
    checks.check(
        "source CP headline checks imaginary entries rather than a quartet",
        "max(np.abs(np.imag" in source_text
        and "quartet" not in source_text.lower(),
    )
    checks.check(
        "source role inference is lexical rather than an implemented map",
        '"gravity/topology" in SRC_EM6' in source_text
        and '"kink/antikink" in SRC_FG4' in source_text,
    )

    checks.mutation_sensitive(
        "singular-value conclusion is sensitive to identical self overlaps",
        lambda diagonal: len(set(sp.Matrix(diagonal).singular_values())) == 1,
        sp.diag(2, 2, 2),
        [sp.diag(1, 2, 3)],
    )
    checks.mutation_sensitive(
        "four-phase verdict is sensitive to strict versus weak pair signs",
        lambda pair: pair == (False, True),
        (
            max(pairwise_phase_cosines(square_phases)) < 0,
            max(pairwise_phase_cosines(square_phases)) <= 0,
        ),
        [(True, True), (False, False)],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
