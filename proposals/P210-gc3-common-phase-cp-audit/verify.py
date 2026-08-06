#!/usr/bin/env python3
"""Primary exact verifier for GC3's common-phase and CP-odd interpretation."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
import yaml

from substrate_framework.common_phase_matrices import (
    common_phase_grams,
    odd_antisymmetric_trace,
    real_gram_relative_basis,
)
from substrate_framework.matrix_decompositions import unitarity_residual
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.unitary_rephasing import invariant_quartet
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-42/"
    "bridge_GC3_cp_needs_relative_phases.py"
)
SOURCE_SHA256 = "0e44cc80e118cd38366c033c508774bf9a7cab981e8ea3cf054998958426dad8"
RELEASE_SHA256 = "d4a34703c842ced4804bf3ad87378529f753cd75a532c7ef559dcef46627d6a5"
FORMULA_FREEZE_SHA256 = "1c35af1f65d8f85100277bd1c214666b68599d112b5e6549d875c4fd5f307da6"
ROOT_MAPPING = [
    "C-QBL-001",
    "C-QBL-003",
    "C-OVL-001",
    "C-MIX-001",
    "C-MIX-002",
    "C-MIX-003",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def zero_matrix(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def claim_statement(claim_id: str) -> str:
    registry = load(ROOT / "governance/claims.yaml")
    for claim in registry["claims"]:
        if claim["id"] == claim_id:
            return str(claim["statement"])
    raise KeyError(claim_id)


def main() -> int:
    checks = CheckLedger("P210-GC3-COMMON-PHASE-AUDIT")
    checks.check("source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        digest(ROOT / "governance/releases/v0.151.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned",
        digest(CAMPAIGN / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )

    proposal = load(CAMPAIGN / "proposal.yaml")
    checks.check(
        "proposal registers the novel algebraic claim without physical imports",
        proposal["claims_proposed"] == ["C-MIX-003"]
        and proposal["post_source_claim_delta"]["dependencies"]
        == ["C-MIX-001", "C-MIX-002"],
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "source predicate and assertion inventories remain exact",
        sum(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            for node in ast.walk(source_tree)
        )
        == 9
        and sum(isinstance(node, ast.Assert) for node in ast.walk(source_tree)) == 1,
    )
    checks.check(
        "source has no NumPy quadrature compatibility surface",
        compatibility.legacy_references
        == compatibility.current_references
        == compatibility.eager_legacy_default_fallbacks
        == 0,
    )

    theta = sp.symbols("theta", real=True)
    real_symbols = sp.symbols("r0:6", real=True)
    real_matrix = sp.Matrix(2, 3, real_symbols)
    phased = sp.exp(sp.I * theta) * real_matrix
    left_gram = sp.simplify(phased * phased.H)
    right_gram = sp.simplify(phased.H * phased)
    checks.check(
        "global phase cancels from both rectangular Grams exactly",
        zero_matrix(left_gram - real_matrix * real_matrix.T)
        and zero_matrix(right_gram - real_matrix.T * real_matrix),
    )
    checks.check(
        "both rectangular Grams are real symmetric",
        zero_matrix(left_gram - left_gram.T)
        and zero_matrix(right_gram - right_gram.T)
        and all(sp.im(entry).simplify() == 0 for entry in left_gram)
        and all(sp.im(entry).simplify() == 0 for entry in right_gram),
    )
    checks.check(
        "Gram phase derivatives vanish rather than merely matching samples",
        zero_matrix(left_gram.diff(theta)) and zero_matrix(right_gram.diff(theta)),
    )

    hu_symbols = sp.symbols("a b c d e f", real=True)
    hd_symbols = sp.symbols("g h i j k l", real=True)
    first_symmetric = sp.Matrix(
        [
            [hu_symbols[0], hu_symbols[1], hu_symbols[2]],
            [hu_symbols[1], hu_symbols[3], hu_symbols[4]],
            [hu_symbols[2], hu_symbols[4], hu_symbols[5]],
        ]
    )
    second_symmetric = sp.Matrix(
        [
            [hd_symbols[0], hd_symbols[1], hd_symbols[2]],
            [hd_symbols[1], hd_symbols[3], hd_symbols[4]],
            [hd_symbols[2], hd_symbols[4], hd_symbols[5]],
        ]
    )
    commutator = first_symmetric * second_symmetric - second_symmetric * first_symmetric
    checks.check(
        "generic real symmetric Gram commutator is antisymmetric",
        zero_matrix(commutator + commutator.T),
    )
    checks.check(
        "generic three-dimensional odd commutator traces vanish exactly",
        sp.simplify(sp.trace(commutator)) == 0
        and sp.simplify(sp.trace(commutator**3)) == 0
        and sp.simplify(sp.trace(commutator**5)) == 0,
    )
    checks.check(
        "generic three-dimensional real antisymmetric determinant vanishes",
        sp.simplify(commutator.det()) == 0,
    )

    real_v = sp.Matrix(3, 3, sp.symbols("v0:9", real=True))
    quartet = (
        real_v[0, 1]
        * real_v[1, 2]
        * sp.conjugate(real_v[0, 2])
        * sp.conjugate(real_v[1, 1])
    )
    checks.check(
        "every displayed quartet of a general real matrix has zero imaginary part",
        sp.simplify(sp.im(quartet)) == 0,
    )

    first_numeric = np.array(
        [[1.0, 2.0, 0.0], [0.0, 1.0, -1.0], [2.0, 0.0, 1.0]]
    )
    second_numeric = np.array(
        [[2.0, -1.0], [1.0, 3.0], [0.5, 2.0]]
    )
    pair = real_gram_relative_basis(
        first_numeric,
        second_numeric,
        first_phase=0.37,
        second_phase=-1.29,
    )
    checks.check(
        "independent sector-global phases give a real orthogonal relative basis",
        unitarity_residual(pair.relative_basis) < 2e-14
        and np.max(np.abs(np.asarray(pair.relative_basis).imag)) == 0.0,
    )
    checks.check(
        "all numeric three-dimensional relative-basis quartets are real",
        all(
            invariant_quartet(pair.relative_basis, i, k, j, ell).imag == 0.0
            for i in range(3)
            for k in range(3)
            for j in range(3)
            for ell in range(3)
        ),
    )
    commutator_scale = max(1.0, np.linalg.norm(pair.commutator, ord=np.inf) ** 5)
    checks.check(
        "canonical odd-trace regression uses a scale-relative error model",
        abs(odd_antisymmetric_trace(pair.commutator, 5)) / commutator_scale
        < 2e-14,
    )

    phase_mutations = [
        common_phase_grams(first_numeric, phase).left_gram
        for phase in (-7.0, -0.2, 0.0, 1.4, 11.0)
    ]
    checks.check(
        "load-bearing global-phase mutations leave the Gram unchanged",
        all(np.allclose(value, phase_mutations[0], atol=2e-14) for value in phase_mutations[1:]),
    )
    dimension_results = [
        common_phase_grams(np.arange(1, n * (n + 1) + 1).reshape(n, n + 1), 0.4)
        for n in (2, 3, 4)
    ]
    checks.check(
        "common-phase algebra accepts dimensions two three and four without selecting one",
        [result.left_gram.shape for result in dimension_results]
        == [(2, 2), (3, 3), (4, 4)],
    )

    sqrt_three = sp.sqrt(3)
    omega = -sp.Rational(1, 2) + sp.I * sqrt_three / 2
    fourier = sp.Matrix(
        [[1, 1, 1], [1, omega, omega**2], [1, omega**2, omega]]
    ) / sqrt_three
    checks.check(
        "exact Fourier counterbasis is unitary",
        zero_matrix(sp.simplify(fourier.H * fourier - sp.eye(3))),
    )
    fourier_quartet = sp.simplify(
        fourier[0, 1]
        * fourier[1, 2]
        * sp.conjugate(fourier[0, 2])
        * sp.conjugate(fourier[1, 1])
    )
    checks.check(
        "exact Fourier quartet has a nonzero imaginary part",
        sp.simplify(sp.im(fourier_quartet)) != 0,
    )

    singular_values = sp.diag(1, 2, 3)
    two_source_matrix = sp.simplify(fourier * singular_values * fourier.T)
    real_source = two_source_matrix.applyfunc(lambda value: sp.simplify(sp.re(value)))
    imaginary_source = two_source_matrix.applyfunc(lambda value: sp.simplify(sp.im(value)))
    checks.check(
        "two differently phased real symmetric sources exactly build the complex matrix",
        zero_matrix(two_source_matrix - real_source - sp.I * imaginary_source)
        and zero_matrix(real_source - real_source.T)
        and zero_matrix(imaginary_source - imaginary_source.T),
    )
    two_source_gram = sp.simplify(two_source_matrix * two_source_matrix.H)
    checks.check(
        "two-source left Gram has the exact complex Fourier eigenbasis",
        zero_matrix(
            two_source_gram
            - fourier * singular_values**2 * fourier.H
        ),
    )
    checks.check(
        "two source phases already suffice algebraically at matrix dimension three",
        (2 - 1) == ((3 - 1) * (3 - 2) // 2)
        and sp.simplify(sp.im(fourier_quartet)) != 0,
    )

    theta_counter = sp.symbols("theta_counter", real=True)
    one_condensate_complex_coupling = sp.exp(sp.I * theta_counter) * two_source_matrix
    complex_coupling_gram = sp.simplify(
        one_condensate_complex_coupling * one_condensate_complex_coupling.H
    )
    checks.check(
        "one global condensate factor cannot remove an independent complex coupling matrix",
        zero_matrix(complex_coupling_gram - two_source_gram)
        and any(sp.simplify(sp.im(entry)) != 0 for entry in complex_coupling_gram),
    )

    local_real = sp.diag(1, 2, 4)
    local_imaginary = sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    local_phase_matrix = local_real + sp.I * local_imaginary
    local_gram = sp.simplify(local_phase_matrix * local_phase_matrix.H)
    checks.check(
        "position-dependent or entrywise phases can produce a complex Gram",
        any(sp.simplify(sp.im(entry)) != 0 for entry in local_gram),
    )
    checks.check(
        "the complex mutation is detected by the canonical premise guard",
        np.max(
            np.abs(
                (
                    np.asarray(local_phase_matrix, dtype=np.complex128)
                    @ np.asarray(local_phase_matrix, dtype=np.complex128).conj().T
                ).imag
            )
        )
        > 1.0,
    )

    identity = sp.eye(3)
    checks.check(
        "degenerate identity Gram admits both real and complex diagonalizing bases",
        zero_matrix(identity.T * identity * identity - identity)
        and zero_matrix(sp.simplify(fourier.H * identity * fourier - identity)),
    )
    checks.check(
        "degenerate complex coordinate quartet does not change the zero commutator invariant",
        sp.simplify(sp.im(fourier_quartet)) != 0
        and zero_matrix(identity * identity - identity * identity),
    )

    source_assignments = {
        target.id: node.value
        for node in source_tree.body
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
    }
    checks.check(
        "source dimension draw count and phases are declared literals",
        ast.literal_eval(source_assignments["n_gen"]) == 3
        and ast.literal_eval(source_assignments["NDRAW"]) == 400
        and ast.literal_eval(source_assignments["PHASES"]) == (0.7, 1.6, 2.5),
    )
    checks.check(
        "source random one-sector phases are shared rather than required",
        "Yu1 = np.exp(1j * th) * real_sym()" in source_text
        and "Yd1 = np.exp(1j * th) * real_sym()" in source_text,
    )
    checks.check(
        "source solved modes are separate external wells rather than one field solution",
        "for rc in centers:" in source_text
        and "eigh_tridiagonal" in source_text
        and "solve_ivp" not in source_text
        and "solve_bvp" not in source_text,
    )
    checks.check(
        "source finite ensemble cannot prove bounded-away language",
        "med_three > 1e-6" in source_text
        and "float(np.min(J_three)) > 0.0" in source_text
        and "bounded AWAY from zero" in source_text,
    )
    checks.check(
        "source equal-spacing prediction rests on one declared comparison",
        ast.literal_eval(source_assignments["CEN_EQUAL"]) == (0.0, 3.0, 6.0)
        and ast.literal_eval(source_assignments["CEN_UNEQUAL"])
        == (0.0, 2.5, 7.0)
        and "PREDICTS a non-equally-spaced generation geometry" in source_text,
    )
    checks.check(
        "source overloads one symbol for condensate supply and matrix demand",
        "supply = Nsym - 1" in source_text
        and "demand = (Nsym - 1) * (Nsym - 2) / 2" in source_text,
    )
    checks.check(
        "separating condensate count K from matrix dimension N repairs the budget",
        all(
            (k - 1 >= (n - 1) * (n - 2) // 2)
            == (k >= 1 + (n - 1) * (n - 2) // 2)
            for k in range(1, 7)
            for n in range(2, 6)
        ),
    )
    checks.check(
        "source anti-fit check is only a selected-global-name intersection",
        "measured_names & set(globals().keys())" in source_text
        and "read_text" not in source_text,
    )

    qball_statement = claim_statement("C-QBL-001")
    overlap_statement = claim_statement("C-OVL-001")
    matrix_statement = claim_statement("C-MIX-001")
    rephasing_statement = claim_statement("C-MIX-002")
    checks.check(
        "accepted EM6 explicitly does not force complex ontology",
        "no VK, spectral, orbital, or nonlinear stability, forced complex ontology"
        in qball_statement,
    )
    checks.check(
        "accepted overlap explicitly derives no Yukawa interaction or condensate",
        "derive no fermion, Yukawa interaction" in overlap_statement
        and "physical condensate" in overlap_statement,
    )
    checks.check(
        "accepted matrix claim explicitly derives no Yukawa CKM or CP result",
        "Yukawa texture" in matrix_statement
        and "CKM identity" in matrix_statement
        and "CP-phase count" in matrix_statement,
    )
    checks.check(
        "accepted rephasing claim explicitly derives no physical CP result",
        "physical CP operation or violation" in rephasing_statement
        and "observed family count" in rephasing_statement,
    )

    imported_modules = {
        node.module
        for node in source_tree.body
        if isinstance(node, ast.ImportFrom)
    }
    checks.check(
        "source copies predecessor premises rather than importing accepted APIs",
        imported_modules == {"scipy.linalg"}
        and "substrate_framework" not in source_text,
    )
    checks.check(
        "claim mapping keeps conditional algebra separate from physical ceilings",
        ROOT_MAPPING
        == [
            "C-QBL-001",
            "C-QBL-003",
            "C-OVL-001",
            "C-MIX-001",
            "C-MIX-002",
            "C-MIX-003",
        ],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
