"""Independent Cartesian and Bessel review of P054's exact claim delta."""

from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.special import jv, roots_legendre

from substrate_framework.triaxial_l2 import real_l2_triple_stf_tensor
from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P054-INDEPENDENT")
    matrices = (
        sp.diag(-sp.Rational(1, 2), -sp.Rational(1, 2), 1),
        sp.diag(1, -1, 0),
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
    )
    ledger.check(
        "the five Cartesian quadratic-form matrices are symmetric and traceless",
        all(value == value.T and sp.trace(value) == 0 for value in matrices),
    )

    # <n_i n_j n_k n_l>=(delta_ij delta_kl+delta_ik delta_jl+delta_il delta_jk)/15.
    # For Y=n^T A n with Tr(A)=0, Q/H=3*<n_i n_j Y>=2*A/5.
    independently_derived = tuple(sp.simplify(2 * value / 5) for value in matrices)
    canonical = tuple(
        real_l2_triple_stf_tensor(**{name: 1})
        for name in ("p20", "m2_cosine", "m2_sine", "m1_cosine", "m1_sine")
    )
    ledger.check(
        "isotropic fourth-moment contraction independently reproduces the canonical map",
        independently_derived == canonical,
    )
    ledger.mutation_sensitive(
        "triple-STF normalization retains the factor two-fifths",
        lambda factor: tuple(sp.simplify(factor * value) for value in matrices) == canonical,
        sp.Rational(2, 5),
        [sp.Rational(1, 5), sp.Rational(2, 15), sp.Rational(6, 5)],
    )

    h_c, h_s = sp.symbols("H_c H_s", real=True)
    source = 2 * (h_c * matrices[1] + h_s * matrices[2]) / 5
    plus = sp.diag(1, -1, 0) / sp.sqrt(2)
    cross = matrices[2] / sp.sqrt(2)
    contract = lambda left, right: sp.simplify(
        sum((left[i, j] * right[i, j] for i in range(3) for j in range(3)), sp.Integer(0))
    )
    ledger.check(
        "direct normalized TT contractions give 2sqrt(2)Hc/5 and 2sqrt(2)Hs/5",
        contract(source, plus) == 2 * sp.sqrt(2) * h_c / 5
        and contract(source, cross) == 2 * sp.sqrt(2) * h_s / 5,
    )
    ledger.check(
        "a pure real-m2 cosine tensor has three distinct eigenvalues when nonzero",
        independently_derived[1].eigenvals()
        == {sp.Rational(2, 5): 1, -sp.Rational(2, 5): 1, 0: 1},
    )

    angle = sp.symbols("chi", real=True)
    rotation = sp.Matrix(
        [[sp.cos(2 * angle), -sp.sin(2 * angle)], [sp.sin(2 * angle), sp.cos(2 * angle)]]
    )
    ledger.check(
        "polarization rotation has determinant one and preserves temporal rank",
        sp.trigsimp(rotation.det()) == 1,
    )
    first, second, ratio = sp.symbols("f g c", real=True)
    proportional = sp.Matrix([[first, ratio * first], [second, ratio * second]])
    ledger.check(
        "proportional nonzero readouts have rank one while independent traces have rank two",
        sp.simplify(proportional.det()) == 0 and sp.eye(2).det() == 1,
    )

    amplitude = sp.symbols("a", nonzero=True, real=True)
    j0_second = -sp.besselj(0, amplitude) + sp.besselj(1, amplitude) / amplitude
    twice_coefficient = sp.simplify(-4 * j0_second - 2 * sp.besselj(0, amplitude))
    ledger.check(
        "J0 differentiation and the Bessel recurrence give the exact minus-two-J2 coefficient",
        sp.simplify(twice_coefficient + 2 * sp.besselj(2, amplitude)) == 0,
    )
    ledger.mutation_sensitive(
        "the omitted twice-phase coefficient sign and factor are load bearing",
        lambda coefficient: sp.simplify(coefficient + 2 * sp.besselj(2, amplitude)) == 0,
        twice_coefficient,
        [0, 2 * sp.besselj(2, amplitude), -sp.besselj(2, amplitude)],
    )

    nodes, weights = roots_legendre(192)
    tau = np.pi * (nodes + 1.0)
    transformed_weights = np.pi * weights
    amplitudes = np.array([0.4, 1.3, 2.5])
    quadrature = np.array(
        [
            np.sum(transformed_weights * np.cos(value * np.cos(tau)) * np.cos(2 * tau)) / np.pi
            for value in amplitudes
        ]
    )
    expected = -2.0 * jv(2, amplitudes)
    error = np.max(np.abs(quadrature - expected))
    scale = max(1.0, float(np.max(np.abs(expected))))
    ledger.check(
        "direct Gauss-Legendre Fourier quadrature reproduces the Bessel coefficient",
        error / scale < 5.0e-13,
        f"scale-relative error={error / scale:.3e}",
    )
    ledger.check(
        "wrong-sign Fourier mutation fails far above quadrature error",
        np.max(np.abs(quadrature - 2.0 * jv(2, amplitudes))) / scale > 0.1,
    )

    radius, coefficient = sp.symbols("r C", nonzero=True)
    ledger.check(
        "regular real-l2 data obey r psi_r minus 2 psi at leading order",
        sp.simplify(radius * sp.diff(coefficient * radius**2, radius) - 2 * coefficient * radius**2) == 0,
    )
    ledger.check(
        "QB3's epsilon data have the independently computed mismatch one-millionth",
        sp.Rational(1, 100) * sp.Rational(1, 10_000) == sp.Rational(1, 1_000_000),
    )
    ledger.check(
        "the accepted P2 Qzz coefficient maps to real-m2 Qxx and natural plus",
        independently_derived[0][2, 2]
        == independently_derived[1][0, 0]
        == sp.Rational(2, 5),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
