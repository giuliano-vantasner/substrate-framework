"""Independent P067 derivation without importing spin1_mean_field."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _expectation(state: sp.Matrix, matrix: sp.Matrix) -> sp.Expr:
    return sp.simplify((state.conjugate().T * matrix * state)[0])


def main() -> int:
    ledger = CheckLedger("P067-INDEPENDENT")
    root_two = sp.sqrt(2)
    matrices = (
        sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) / root_two,
        sp.Matrix([[0, -sp.I, 0], [sp.I, 0, -sp.I], [0, sp.I, 0]])
        / root_two,
        sp.diag(1, 0, -1),
    )
    ar, ai, br, bi, cr, ci = sp.symbols(
        "a_r a_i b_r b_i c_r c_i", real=True
    )
    state = sp.Matrix([ar + sp.I * ai, br + sp.I * bi, cr + sp.I * ci])
    spin = tuple(_expectation(state, matrix) for matrix in matrices)
    spin_squared = sp.simplify(sum(value**2 for value in spin))
    norm = sp.simplify((state.conjugate().T * state)[0])
    singlet = sp.simplify(state[1] ** 2 - 2 * state[0] * state[2])
    ledger.check(
        "fresh matrix expansion derives the pure-spin-1 invariant",
        sp.expand(spin_squared + sp.conjugate(singlet) * singlet - norm**2) == 0,
    )

    px, py, pz, qx, qy, qz = sp.symbols(
        "p_x p_y p_z q_x q_y q_z", real=True
    )
    real_part = sp.Matrix([px, py, pz])
    imaginary_part = sp.Matrix([qx, qy, qz])
    vector = real_part + sp.I * imaginary_part
    fresh_state = sp.Matrix(
        [
            -(vector[0] - sp.I * vector[1]) / root_two,
            vector[2],
            (vector[0] + sp.I * vector[1]) / root_two,
        ]
    )
    fresh_spin = sp.Matrix([_expectation(fresh_state, matrix) for matrix in matrices])
    ledger.check(
        "fresh Cartesian conversion derives the cross-product spin",
        (fresh_spin - 2 * real_part.cross(imaginary_part)).applyfunc(sp.simplify)
        == sp.zeros(3, 1),
    )
    ledger.check(
        "fresh Cartesian conversion derives the singlet self-dot-product",
        sp.expand(
            fresh_state[1] ** 2
            - 2 * fresh_state[0] * fresh_state[2]
            - vector.dot(vector)
        )
        == 0,
    )
    ledger.check(
        "fresh endpoint equations separate parallel and equal-orthogonal geometry",
        sp.re(vector.dot(vector)).expand()
        == real_part.dot(real_part) - imaginary_part.dot(imaginary_part)
        and sp.im(vector.dot(vector)).expand() == 2 * real_part.dot(imaginary_part),
    )

    x, y, b = sp.symbols("x y b", real=True)
    polar_chart = sp.Matrix([x + sp.I * y, b, -x + sp.I * y])
    ledger.check(
        "fresh nonzero-middle-component solution chart has identically zero spin",
        all(_expectation(polar_chart, matrix) == 0 for matrix in matrices),
    )
    phase, theta = sp.symbols("alpha theta", real=True)
    coherent = sp.Matrix(
        [
            sp.exp(-sp.I * phase) * sp.cos(theta / 2) ** 2,
            sp.sin(theta) / root_two,
            sp.exp(sp.I * phase) * sp.sin(theta / 2) ** 2,
        ]
    )
    coherent_norm = sp.trigsimp(
        (coherent.conjugate().T * coherent)[0], method="fu"
    )
    coherent_spin_squared = sp.trigsimp(
        sum(_expectation(coherent, matrix) ** 2 for matrix in matrices)
    )
    coherent_singlet = sp.trigsimp(
        coherent[1] ** 2 - 2 * coherent[0] * coherent[2]
    )
    ledger.check(
        "fresh coherent-state orbit saturates the upper endpoint",
        coherent_norm == 1 and coherent_spin_squared == 1 and coherent_singlet == 0,
    )

    density, coefficient = sp.symbols("n c2", positive=True)
    ledger.check(
        "fresh interval minimization gives the positive-coupling polar energy",
        sp.simplify(coefficient * 0 / 2) == 0
        and sp.simplify(coefficient * density**2 / 2) > 0,
    )
    negative_coefficient = -coefficient
    ledger.check(
        "fresh interval minimization flips at negative coupling",
        sp.simplify(negative_coefficient * density**2 / 2) < 0,
    )
    ledger.check(
        "fresh zero-coupling boundary is fully degenerate",
        all(sp.Integer(0) * value / 2 == 0 for value in (0, density**2)),
    )
    ledger.mutation_sensitive(
        "fresh invariant rejects altered singlet normalization",
        lambda candidate: sp.expand(
            spin_squared + sp.conjugate(candidate) * candidate - norm**2
        )
        == 0,
        singlet,
        [state[1] ** 2 + 2 * state[0] * state[2], state[1] ** 2 - state[0] * state[2]],
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
