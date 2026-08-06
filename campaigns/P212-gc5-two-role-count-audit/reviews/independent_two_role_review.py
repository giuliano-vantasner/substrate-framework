#!/usr/bin/env python3
"""Independent exact GC5 review without importing the P212 canonical APIs."""

from __future__ import annotations

import ast
import hashlib
import itertools
from pathlib import Path

import sympy as sp

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-42/"
    "bridge_GC5_two_role_structure_and_counts.py"
)
SOURCE_SHA256 = "ffc638accff802c16804bd793b47e1cc5da018d5e0742ace57d9d3207e06b220"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(sp.expand_complex(entry)) == 0 for entry in matrix)


def main() -> int:
    checks = CheckLedger("P212-GC5-INDEPENDENT-REVIEW")
    checks.check("source hash remains independently pinned", digest(SOURCE) == SOURCE_SHA256)
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    compatibility = audit_numpy_trapezoid_compatibility(source, filename=str(SOURCE))
    checks.check(
        "independent source inventory remains eight checks and one assertion",
        sum(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            for node in ast.walk(tree)
        )
        == 8
        and sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    checks.check(
        "independent compatibility audit finds no quadrature name",
        compatibility.legacy_references == compatibility.current_references == 0,
    )

    x, ra, rb, rc = sp.symbols("x r_a r_b r_c", real=True)
    exponent = sp.expand(
        ((x - ra) ** 2 + (x - rb) ** 2 + (x - rc) ** 2) / 2
    )
    center = sp.simplify((ra + rb + rc) / 3)
    remainder = sp.simplify(exponent - sp.Rational(3, 2) * (x - center) ** 2)
    expected_remainder = sp.simplify(
        ((ra - rb) ** 2 + (ra - rc) ** 2 + (rb - rc) ** 2) / 6
    )
    checks.check(
        "fresh Gaussian completion of the square has the exact separation exponent",
        sp.expand(remainder - expected_remainder) == 0,
    )
    alpha = sp.sqrt(sp.Rational(2, 3))
    checks.check(
        "fresh normalized Gaussian self overlap is exact",
        sp.pi ** (-sp.Rational(1, 2))
        * sp.sqrt(2 * sp.pi / 3)
        == alpha,
    )

    d = sp.symbols("d", positive=True)
    phases = (0, 2 * sp.pi / 3, 4 * sp.pi / 3)

    def triple(a: int, b: int, c: int) -> sp.Expr:
        spread = (a - b) ** 2 + (a - c) ** 2 + (b - c) ** 2
        return alpha * sp.exp(-sp.Rational(spread, 6) * d**2)

    matrix = sp.Matrix(
        3,
        3,
        lambda a, b: sum(
            sp.exp(sp.I * phases[c]) * triple(a, b, c) for c in range(3)
        ),
    )
    fresh_limit = matrix.applyfunc(lambda entry: sp.limit(entry, d, sp.oo))
    expected_limit = sp.diag(
        *(alpha * sp.exp(sp.I * phase) for phase in phases)
    )
    checks.check(
        "fresh translated Gaussian matrix has the phase-weighted diagonal limit",
        zero(fresh_limit - expected_limit),
    )
    checks.check(
        "fresh limit has three equal singular values",
        zero(fresh_limit.H * fresh_limit - alpha**2 * sp.eye(3)),
    )

    epsilon = sp.Rational(1, 4)
    endpoint = sp.diag(alpha + epsilon, alpha, alpha - epsilon)
    singular_values = sorted(endpoint.singular_values(), key=float)
    checks.check(
        "fresh perturbation witness attains the singular cluster endpoints",
        all(
            sp.simplify(actual**2 - expected**2) == 0
            for actual, expected in zip(
                singular_values, [alpha - epsilon, alpha, alpha + epsilon]
            )
        ),
    )
    checks.check(
        "fresh endpoint condition ratio equals the perturbation bound",
        sp.simplify(
            (singular_values[-1] / singular_values[0]) ** 2
            - ((alpha + epsilon) / (alpha - epsilon)) ** 2
        )
        == 0,
    )

    angles = sp.symbols("a0:5", real=True)
    resultant = sum(sp.exp(sp.I * angle) for angle in angles)
    resultant_squared = sp.trigsimp(
        sp.expand_complex(resultant * sp.conjugate(resultant))
    )
    direct = sum(
        sp.cos(angles[a] - angles[b])
        for a, b in itertools.combinations(range(5), 2)
    )
    checks.check(
        "fresh expansion proves the complete cosine resultant identity",
        sp.trigsimp(direct - (resultant_squared - 5) / 2) == 0,
    )
    for count in range(2, 7):
        roots = [sp.exp(2 * sp.pi * sp.I * index / count) for index in range(count)]
        root_sum = sp.trigsimp(sp.expand_complex(sum(roots)))
        pair_sum = sp.simplify(
            sum(
                sp.cos(2 * sp.pi * (a - b) / count)
                for a, b in itertools.combinations(range(count), 2)
            )
        )
        checks.check(
            f"fresh regular {count}-gon reaches minus count over two",
            root_sum == 0 and pair_sum == -sp.Rational(count, 2),
        )

    beta = sp.symbols("beta", real=True)
    antipodal = (0, sp.pi, beta, beta + sp.pi)
    antipodal_resultant = sp.trigsimp(
        sp.expand_complex(sum(sp.exp(sp.I * angle) for angle in antipodal))
    )
    checks.check(
        "fresh four-phase minimizer family has a continuous parameter",
        antipodal_resultant == 0,
    )
    square = (0, sp.pi / 2, sp.pi, 3 * sp.pi / 2)
    checks.check(
        "fresh square minimum has weak but no positive pair",
        max(
            sp.cos(square[a] - square[b])
            for a, b in itertools.combinations(range(4), 2)
        )
        == 0,
    )

    i31, i22, c = sp.symbols("I31 I22 c", positive=True)
    finite_pair = -c * i31 / 6 - (1 + 2 * c**2) * i22 / 12
    checks.check(
        "fresh finite quartic pair has a cosine-squared term",
        sp.diff(finite_pair, c, 2) == -i22 / 3,
    )
    checks.check(
        "fresh finite pair prefers equal over opposite phase",
        sp.simplify(finite_pair.subs(c, 1) - finite_pair.subs(c, -1))
        == -i31 / 3,
    )

    complex_diagonal = sp.diag(1, sp.I, 2 + sp.I)
    checks.check(
        "fresh imaginary-entry countermodel has zero off-diagonal quartets",
        any(sp.im(entry) != 0 for entry in complex_diagonal)
        and all(
            complex_diagonal[i, j]
            * complex_diagonal[k, ell]
            * sp.conjugate(complex_diagonal[i, ell])
            * sp.conjugate(complex_diagonal[k, j])
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
    real_part = complex_symmetric.applyfunc(lambda value: sp.simplify(sp.re(value)))
    imaginary_part = complex_symmetric.applyfunc(
        lambda value: sp.simplify(sp.im(value))
    )
    checks.check(
        "fresh two-real-source decomposition defeats a source-count phase budget",
        zero(complex_symmetric - real_part - sp.I * imaginary_part)
        and sp.simplify(sp.im(quartet)) != 0,
    )

    logical_models = {
        (1, 3, 2),
        (4, 3, 2),
        (3, 3, 1),
    }
    checks.check(
        "fresh finite role models separate species solutions and roles",
        len({model[0] for model in logical_models}) == 3
        and len({model[1] for model in logical_models}) == 1
        and len({model[2] for model in logical_models}) == 2,
    )
    checks.check(
        "source stability and role conclusions are prose-token checks",
        '"gravity/topology" in SRC_EM6' in source
        and '"kink/antikink" in SRC_FG4' in source,
    )
    checks.check(
        "source numerical minimization omits its success gate",
        "r.fun < best.fun" in source and "r.success" not in source,
    )
    checks.check(
        "source imaginary-entry test never computes its claimed invariant",
        "max(np.abs(np.imag" in source and "quartet" not in source.lower(),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
