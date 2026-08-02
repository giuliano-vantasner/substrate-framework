"""Independent exact rederivation for P072 without canonical API imports."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-20/"
    "bridge_MH3_overlap_feeds_mixing.py"
)
SOURCE_SHA256 = "f33ab10dadee8ae4f747328f1fc593733942d18ccdb280ca6f21c3961e03c425"


def main() -> int:
    ledger = CheckLedger("P072-INDEPENDENT")
    source_bytes = SOURCE.read_bytes()
    ledger.check(
        "review reads immutable MH3 source",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )

    x = sp.symbols("x", real=True)
    left_i, left_j, profile = sp.symbols("eta_i eta_j Phi", complex=True)
    swapped_conjugate = sp.conjugate(sp.conjugate(left_i) * profile * left_j)
    ledger.check(
        "fresh sesquilinear conjugation gives Hermitian entry for real profile",
        swapped_conjugate.subs(sp.conjugate(profile), profile)
        == sp.conjugate(left_j) * profile * left_i,
    )

    c, s = sp.symbols("c s", real=True)
    unitary = sp.Matrix([[c, s], [-s, c]])
    y00, y01, y11 = sp.symbols("y00 y01 y11", real=True)
    matrix = sp.Matrix([[y00, y01], [y01, y11]])
    transformed = sp.expand(unitary.T * matrix * unitary)
    ledger.check(
        "fresh common-basis bilinear expansion is similarity covariance",
        transformed[0, 0]
        == sp.expand(c**2 * y00 - 2 * c * s * y01 + s**2 * y11)
        and transformed[0, 1]
        == sp.expand(c * s * y00 + (c**2 - s**2) * y01 - c * s * y11),
    )
    ledger.check(
        "fresh trace covariance closes under orthogonality",
        sp.simplify(sp.trace(transformed).subs(c**2, 1 - s**2) - sp.trace(matrix))
        == 0,
    )

    kappa, amplitude, asymmetry = sp.symbols("kappa A b", positive=True)
    integral = lambda power: sp.sqrt(sp.pi) * sp.gamma(sp.Rational(power, 2)) / (
        kappa * sp.gamma(sp.Rational(power + 1, 2))
    )
    i2, i3, i4, i5, i6 = (sp.simplify(integral(power)) for power in range(2, 7))
    even_norm = i4
    odd_norm = sp.simplify(i2 - i4)
    even_diagonal = sp.simplify(amplitude * i5 / even_norm)
    odd_diagonal = sp.simplify(amplitude * (i3 - i5) / odd_norm)
    cross_raw = sp.simplify(i4 - i6)
    cross = sp.simplify(
        amplitude * asymmetry * cross_raw / sp.sqrt(even_norm * odd_norm)
    )
    ledger.check(
        "fresh gamma route derives actual mode norms",
        even_norm == 4 / (3 * kappa) and odd_norm == 2 / (3 * kappa),
    )
    ledger.check(
        "fresh gamma route derives actual diagonal entries",
        even_diagonal == 9 * sp.pi * amplitude / 32
        and odd_diagonal == 3 * sp.pi * amplitude / 16,
    )
    ledger.check(
        "fresh tanh-squared reduction derives asymmetric cross entry",
        cross_raw == 4 / (15 * kappa)
        and cross == sp.sqrt(2) * amplitude * asymmetry / 5,
    )
    fresh_actual = sp.Matrix([[even_diagonal, cross], [cross, odd_diagonal]])
    ledger.check(
        "fresh actual compression is independent of common width",
        fresh_actual.applyfunc(lambda entry: sp.diff(entry, kappa)) == sp.zeros(2),
    )
    ledger.check(
        "fresh parity mutation removes the cross entry",
        fresh_actual.subs(asymmetry, 0)[0, 1] == 0,
    )
    ledger.check(
        "fresh odd-profile sign mutation reverses the cross entry",
        fresh_actual.subs(asymmetry, -asymmetry)[0, 1] == -fresh_actual[0, 1],
    )

    source_even_norm = i2
    source_odd_norm = sp.simplify(i2 - i4)
    source_even = sp.simplify(amplitude * i3 / source_even_norm)
    source_odd = sp.simplify(amplitude * (i3 - i5) / source_odd_norm)
    source_cross = sp.simplify(
        amplitude
        * asymmetry
        * (i3 - i5)
        / sp.sqrt(source_even_norm * source_odd_norm)
    )
    fresh_source = sp.Matrix(
        [[source_even, source_cross], [source_cross, source_odd]]
    )
    ledger.check(
        "fresh source-mode reduction reproduces MH3 matrix",
        fresh_source
        == sp.pi
        * amplitude
        * sp.Matrix([[4, sp.sqrt(3) * asymmetry], [sp.sqrt(3) * asymmetry, 3]])
        / 16,
    )
    ledger.check(
        "fresh source matrix width derivative vanishes",
        fresh_source.applyfunc(lambda entry: sp.diff(entry, kappa)) == sp.zeros(2),
    )
    ledger.check(
        "fresh accepted-mode calculation differs from source proxy",
        fresh_actual[0, 0] != fresh_source[0, 0],
    )

    a, b, d, e, f, h = sp.symbols("a b d e f h", real=True)
    first = sp.Matrix([[a, b], [b, d]])
    second = sp.Matrix([[e, f], [f, h]])
    commutator = sp.simplify(first * second - second * first)
    scalar = sp.expand(f * (a - d) + b * (h - e))
    ledger.check(
        "fresh two-by-two commutator has one load-bearing scalar",
        commutator == sp.Matrix([[0, scalar], [-scalar, 0]]),
    )
    ledger.check(
        "fresh different diagonal matrices commute",
        sp.diag(1, 2) * sp.diag(3, 5) - sp.diag(3, 5) * sp.diag(1, 2)
        == sp.zeros(2),
    )

    b_up, b_down = sp.symbols("b_u b_d", real=True)
    actual_up = fresh_actual.subs(asymmetry, b_up)
    actual_down = fresh_actual.subs(asymmetry, b_down)
    actual_commutator = sp.simplify(actual_up * actual_down - actual_down * actual_up)
    ledger.check(
        "fresh actual commutator is proportional only to asymmetry difference",
        sp.factor(actual_commutator[0, 1])
        == 3 * sp.sqrt(2) * sp.pi * amplitude**2 * (b_down - b_up) / 160,
    )
    ledger.check(
        "fresh width-only source explanation is impossible",
        not fresh_source.has(kappa) and not fresh_actual.has(kappa),
    )

    phase = sp.diag(1, sp.I)
    permutation = sp.Matrix([[0, 1], [1, 0]])
    rotation = sp.Matrix([[0, 1], [-1, 0]])
    ledger.check(
        "fresh phase representative is unitary and nonidentity",
        phase.H * phase == sp.eye(2) and phase != sp.eye(2),
    )
    ledger.check(
        "fresh ordering representative is unitary and nonidentity",
        permutation.H * permutation == sp.eye(2) and permutation != sp.eye(2),
    )
    ledger.check(
        "fresh degenerate block admits arbitrary unitary basis",
        rotation.T * sp.eye(2) * rotation == sp.eye(2),
    )
    ledger.check(
        "nonidentity relative representative does not imply unequal operators",
        phase != sp.eye(2) and phase.H * sp.eye(2) * phase == sp.eye(2),
    )

    source_text = source_bytes.decode("utf-8")
    ledger.check(
        "fresh data-flow audit identifies independent odd-profile inputs",
        "b_u = sp.Rational(1, 3)" in source_text
        and "b_d = sp.Rational(1, 4)" in source_text,
    )
    ledger.check(
        "fresh dependency audit finds no physical interaction operator",
        "L_yukawa" not in source_text and "charged_current" not in source_text,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
