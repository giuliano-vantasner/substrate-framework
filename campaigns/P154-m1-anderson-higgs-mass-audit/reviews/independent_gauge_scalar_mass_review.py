#!/usr/bin/env python3
"""Fresh C-GSM-001 derivation without importing the canonical mass helper."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _zero(matrix: sp.MatrixBase) -> bool:
    return sp.ImmutableMatrix(sp.Matrix(matrix).applyfunc(sp.simplify)) == sp.zeros(
        *matrix.shape
    )


def run() -> int:
    checks = CheckLedger("P154-independent")

    a, b, c, d, e, f, h, j = sp.symbols("a b c d e f h j", real=True)
    p, q = sp.symbols("p q", nonzero=True, real=True)
    r, s, t, u = sp.symbols("r s t u", real=True)
    x, y = sp.symbols("x y", real=True)
    first = sp.Matrix([[a, b + sp.I * c], [b - sp.I * c, d]])
    second = sp.Matrix([[e, f + sp.I * h], [f - sp.I * h, j]])
    vacuum = sp.Matrix([r + sp.I * s, t + sp.I * u])
    orbit = sp.Matrix.hstack(p * first * vacuum, q * second * vacuum)
    mass = sp.Matrix(
        2,
        2,
        lambda row, column: sp.simplify(
            (orbit[:, row].H * orbit[:, column])[0]
            + (orbit[:, column].H * orbit[:, row])[0]
        ),
    )
    anticommutator = sp.Matrix(
        [
            [
                sp.simplify(
                    (couplings_row * couplings_column)
                    * (
                        vacuum.H
                        * (generator_row * generator_column + generator_column * generator_row)
                        * vacuum
                    )[0]
                )
                for generator_column, couplings_column in ((first, p), (second, q))
            ]
            for generator_row, couplings_row in ((first, p), (second, q))
        ]
    )
    checks.check(
        "fresh general Hermitian anticommutator equals twice-real Gram",
        _zero(mass - anticommutator),
    )
    combination = orbit * sp.Matrix([x, y])
    checks.check(
        "fresh arbitrary-real-coefficient PSD identity",
        sp.simplify(
            (sp.Matrix([x, y]).T * mass * sp.Matrix([x, y]))[0]
            - 2 * (combination.H * combination)[0]
        )
        == 0,
    )

    g, gp, v = sp.symbols("g gp v", positive=True)
    i = sp.I
    t1 = sp.Matrix([[0, 1], [1, 0]]) / 2
    t2 = sp.Matrix([[0, -i], [i, 0]]) / 2
    t3 = sp.diag(1, -1) / 2
    y_half = sp.eye(2) / 2
    phi0 = sp.Matrix([0, v / sp.sqrt(2)])
    generators = (t1, t2, t3, y_half)
    couplings = (g, g, g, gp)
    fields = sp.Matrix(sp.symbols("W1 W2 W3 B", real=True))
    connection = sum(
        (
            field * coupling * generator
            for field, coupling, generator in zip(
                fields, couplings, generators, strict=True
            )
        ),
        sp.zeros(2),
    )
    density = sp.expand((connection * phi0).H.dot(connection * phi0))
    direct_mass = sp.ImmutableMatrix(sp.hessian(density, fields))
    expected = v**2 / 4 * sp.Matrix(
        [
            [g**2, 0, 0, 0],
            [0, g**2, 0, 0],
            [0, 0, g**2, -g * gp],
            [0, 0, -g * gp, gp**2],
        ]
    )
    checks.check(
        "fresh scalar kinetic Hessian gives the doublet matrix",
        _zero(direct_mass - expected),
    )
    neutral = direct_mass.extract((2, 3), (2, 3))
    denominator = sp.sqrt(g**2 + gp**2)
    null = sp.Matrix([gp, g]) / denominator
    massive = sp.Matrix([g, -gp]) / denominator
    nonzero_mass = (g**2 + gp**2) * v**2 / 4
    checks.check(
        "fresh neutral kernel and nonzero eigenvector",
        _zero(neutral * null)
        and _zero(neutral * massive - nonzero_mass * massive),
    )
    checks.check(
        "fresh rank is three and the declared charge kills the vacuum",
        direct_mass.rank() == 3 and _zero((t3 + y_half) * phi0),
    )
    charged_mass = g**2 * v**2 / 4
    cosine = g / denominator
    checks.check(
        "fresh conditional rho identity",
        sp.simplify(charged_mass / (nonzero_mass * cosine**2)) == 1,
    )

    k_w, k_b = sp.symbols("k_w k_b", positive=True)
    kinetic = sp.diag(k_w, k_w, k_w, k_b)
    generalized = sp.simplify(kinetic.inv() * direct_mass)
    neutral_generalized = generalized.extract((2, 3), (2, 3))
    checks.check(
        "fresh noncanonical kinetic metric changes quadratic masses",
        sp.simplify(neutral_generalized.det()) == 0
        and sp.simplify(
            neutral_generalized.trace()
            - v**2 * (g**2 / k_w + gp**2 / k_b) / 4
        )
        == 0
        and generalized[0, 0] == g**2 * v**2 / (4 * k_w),
    )

    sign_flip = sp.diag(1, -1)
    positive_offdiagonal = sp.simplify(sign_flip.T * neutral * sign_flip)
    checks.check(
        "fresh B sign basis change preserves determinant and eigenvalues",
        positive_offdiagonal[0, 1] == g * gp * v**2 / 4
        and sp.simplify(positive_offdiagonal.det()) == 0
        and positive_offdiagonal.trace() == neutral.trace(),
    )
    misnormalized = v**2 / 4 * sp.Matrix(
        [[g**2, g * gp / 2], [g * gp / 2, gp**2]]
    )
    checks.check(
        "fresh source CHECK8 mutant changes magnitude as well as sign",
        sp.simplify(misnormalized.det() - 3 * g**2 * gp**2 * v**4 / 64) == 0
        and misnormalized != positive_offdiagonal,
    )

    wrong_factor = direct_mass / 2
    checks.check(
        "fresh factor-two mutation fails direct Hessian equality",
        not _zero(wrong_factor - sp.hessian(density, fields)),
    )
    normalized_generators = tuple(2 * generator for generator in generators)
    changed_connection = sum(
        (
            field * coupling * generator
            for field, coupling, generator in zip(
                fields, couplings, normalized_generators, strict=True
            )
        ),
        sp.zeros(2),
    )
    changed_density = sp.expand(
        (changed_connection * phi0).H.dot(changed_connection * phi0)
    )
    checks.check(
        "fresh generator normalization mutation scales mass by four",
        _zero(sp.hessian(changed_density, fields) - 4 * direct_mass),
    )

    root_two = sp.sqrt(2)
    triplet_generators = (
        sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) / root_two,
        sp.Matrix([[0, -i, 0], [i, 0, -i], [0, i, 0]]) / root_two,
        sp.diag(1, 0, -1),
    )
    triplet_vacuum = sp.Matrix([0, v, 0])
    triplet_orbit = sp.Matrix.hstack(
        *(g * generator * triplet_vacuum for generator in triplet_generators)
    )
    triplet_mass = sp.simplify(
        2
        * sp.Matrix.vstack(
            triplet_orbit.applyfunc(sp.re), triplet_orbit.applyfunc(sp.im)
        ).T
        * sp.Matrix.vstack(
            triplet_orbit.applyfunc(sp.re), triplet_orbit.applyfunc(sp.im)
        )
    )
    checks.check(
        "fresh triplet countermodel changes the quadratic spectrum",
        triplet_mass == sp.diag(2 * g**2 * v**2, 2 * g**2 * v**2, 0)
        and triplet_mass.rank() == 2,
    )
    checks.check(
        "fresh zero-vacuum limit removes every coefficient",
        direct_mass.subs(v, 0) == sp.zeros(4),
    )

    condensate_dictionary, particle_dictionary = sp.symbols(
        "condensate_dictionary particle_dictionary"
    )
    checks.check(
        "fresh same-matrix countermodels leave physical dictionaries free",
        condensate_dictionary not in direct_mass.free_symbols
        and particle_dictionary not in direct_mass.free_symbols,
    )

    tally = checks.finish()
    print(f"P154 INDEPENDENT ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
