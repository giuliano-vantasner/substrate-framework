#!/usr/bin/env python3
"""Independent exact rederivation of P210's common-phase matrix claim."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-42/"
    "bridge_GC3_cp_needs_relative_phases.py"
)
SOURCE_SHA256 = "0e44cc80e118cd38366c033c508774bf9a7cab981e8ea3cf054998958426dad8"
RELEASE_SHA256 = "d4a34703c842ced4804bf3ad87378529f753cd75a532c7ef559dcef46627d6a5"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def statement(claim_id: str) -> str:
    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())
    return next(
        str(claim["statement"])
        for claim in registry["claims"]
        if claim["id"] == claim_id
    )


def main() -> int:
    checks = CheckLedger("P210-INDEPENDENT-COMMON-PHASE")
    checks.check("independent source hash is pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "independent release snapshot is pinned",
        digest(ROOT / "governance/releases/v0.151.0.yaml") == RELEASE_SHA256,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    checks.check(
        "independent AST inventory finds nine checks and one assertion",
        sum(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            for node in ast.walk(tree)
        )
        == 9
        and sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check(
        "independent compatibility audit finds no quadrature name",
        compatibility.legacy_references
        == compatibility.current_references
        == compatibility.eager_legacy_default_fallbacks
        == 0,
    )

    theta = sp.symbols("theta", real=True)
    r = sp.Matrix(2, 3, sp.symbols("r0:6", real=True))
    y = sp.exp(sp.I * theta) * r
    checks.check(
        "fresh conjugate-transpose multiplication cancels the left phase",
        zero(sp.simplify(y * y.H - r * r.T)),
    )
    checks.check(
        "fresh conjugate-transpose multiplication cancels the right phase",
        zero(sp.simplify(y.H * y - r.T * r)),
    )
    checks.check(
        "fresh quadratic form proves positive semidefiniteness conditionally",
        sp.simplify(
            (sp.Matrix(sp.symbols("z0:2", real=True)).T * (r * r.T)
             * sp.Matrix(sp.symbols("z0:2", real=True)))[0]
            - sum(
                value**2
                for value in r.T * sp.Matrix(sp.symbols("z0:2", real=True))
            )
        )
        == 0,
    )

    rotation12 = sp.Matrix(
        [[sp.Rational(3, 5), sp.Rational(4, 5), 0],
         [-sp.Rational(4, 5), sp.Rational(3, 5), 0],
         [0, 0, 1]]
    )
    rotation23 = sp.Matrix(
        [[1, 0, 0],
         [0, sp.Rational(5, 13), sp.Rational(12, 13)],
         [0, -sp.Rational(12, 13), sp.Rational(5, 13)]]
    )
    orthogonal = rotation23 * rotation12
    first_diagonal = sp.diag(1, 4, 9)
    second_diagonal = sp.diag(2, 5, 11)
    first_gram = first_diagonal
    second_gram = sp.simplify(orthogonal * second_diagonal * orthogonal.T)
    checks.check(
        "fresh rational relative basis is exactly orthogonal",
        zero(orthogonal.T * orthogonal - sp.eye(3)),
    )
    checks.check(
        "fresh rational basis exactly diagonalizes its constructed Gram",
        zero(orthogonal.T * second_gram * orthogonal - second_diagonal),
    )
    checks.check(
        "fresh rational relative-basis quartets are all real",
        all(
            sp.im(
                orthogonal[i, j]
                * orthogonal[k, ell]
                * sp.conjugate(orthogonal[i, ell])
                * sp.conjugate(orthogonal[k, j])
            )
            == 0
            for i in range(3)
            for k in range(3)
            for j in range(3)
            for ell in range(3)
        ),
    )

    commutator = first_gram * second_gram - second_gram * first_gram
    checks.check(
        "fresh rational Gram commutator is exactly antisymmetric",
        zero(commutator + commutator.T),
    )
    checks.check(
        "fresh rational odd commutator traces vanish",
        sp.trace(commutator) == 0
        and sp.simplify(sp.trace(commutator**3)) == 0
        and sp.simplify(sp.trace(commutator**5)) == 0,
    )
    checks.check(
        "fresh rational odd-dimensional commutator determinant vanishes",
        sp.simplify(commutator.det()) == 0,
    )

    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    fourier = sp.Matrix(
        [[1, 1, 1], [1, omega, omega**2], [1, omega**2, omega]]
    ) / sp.sqrt(3)
    checks.check(
        "fresh complex Fourier matrix is exactly unitary",
        zero(sp.simplify(fourier.H * fourier - sp.eye(3))),
    )
    quartet = sp.simplify(
        fourier[0, 1]
        * fourier[1, 2]
        * sp.conjugate(fourier[0, 2])
        * sp.conjugate(fourier[1, 1])
    )
    checks.check(
        "fresh complex Fourier quartet is exactly nonreal",
        sp.simplify(sp.im(quartet)) != 0,
    )

    complex_symmetric = sp.simplify(fourier * sp.diag(1, 2, 3) * fourier.T)
    source_zero = complex_symmetric.applyfunc(lambda value: sp.simplify(sp.re(value)))
    source_quarter = complex_symmetric.applyfunc(lambda value: sp.simplify(sp.im(value)))
    checks.check(
        "fresh two-phase decomposition uses two real symmetric matrices",
        zero(complex_symmetric - source_zero - sp.I * source_quarter)
        and zero(source_zero - source_zero.T)
        and zero(source_quarter - source_quarter.T),
    )
    complex_gram = sp.simplify(complex_symmetric * complex_symmetric.H)
    checks.check(
        "fresh two-source construction produces the nonreal Fourier Gram",
        zero(complex_gram - fourier * sp.diag(1, 4, 9) * fourier.H)
        and any(sp.simplify(sp.im(entry)) != 0 for entry in complex_gram),
    )

    global_phase = sp.exp(sp.I * sp.symbols("alpha", real=True))
    checks.check(
        "fresh one-factor countermodel retains an independent complex coupling Gram",
        zero(
            sp.simplify(
                (global_phase * complex_symmetric)
                * (global_phase * complex_symmetric).H
                - complex_gram
            )
        ),
    )
    checks.check(
        "fresh countermodel disproves inference from one scalar factor to a real matrix",
        any(sp.simplify(sp.im(entry)) != 0 for entry in complex_symmetric)
        and any(sp.simplify(sp.im(entry)) != 0 for entry in complex_gram),
    )

    checks.check(
        "fresh degeneracy mutation preserves the identity Gram in a complex basis",
        zero(sp.simplify(fourier.H * sp.eye(3) * fourier - sp.eye(3)))
        and sp.simplify(sp.im(quartet)) != 0,
    )
    checks.check(
        "fresh degeneracy invariant remains zero despite the coordinate quartet",
        zero(sp.eye(3) * sp.eye(3) - sp.eye(3) * sp.eye(3)),
    )

    checks.check(
        "fresh phase budget separates source count K and matrix dimension N",
        (1 - 1) < ((3 - 1) * (3 - 2) // 2)
        and (2 - 1) == ((3 - 1) * (3 - 2) // 2)
        and (4 - 1) == ((4 - 1) * (4 - 2) // 2),
    )
    checks.check(
        "source phase budget reuses one symbol for the two independent counts",
        "supply = Nsym - 1" in source_text
        and "demand = (Nsym - 1) * (Nsym - 2) / 2" in source_text,
    )
    checks.check(
        "source nonzero ensemble gate is not a mathematical lower bound",
        "float(np.min(J_three)) > 0.0" in source_text
        and "med_three > 1e-6" in source_text,
    )
    checks.check(
        "source solved-mode route has no coexisting field equation",
        "eigh_tridiagonal" in source_text
        and "solve_ivp" not in source_text
        and "solve_bvp" not in source_text,
    )

    checks.check(
        "accepted predecessor ceilings independently reject the physical imports",
        "forced complex ontology" in statement("C-QBL-001")
        and "Yukawa interaction" in statement("C-OVL-001")
        and "physical CP operation or violation" in statement("C-MIX-002"),
    )
    canonical_source = (
        ROOT / "src/substrate_framework/common_phase_matrices.py"
    ).read_text(encoding="utf-8")
    checks.check(
        "new canonical surface has no NumPy quadrature dependency",
        "np." + "trapz" not in canonical_source
        and "np." + "trapezoid" not in canonical_source,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
