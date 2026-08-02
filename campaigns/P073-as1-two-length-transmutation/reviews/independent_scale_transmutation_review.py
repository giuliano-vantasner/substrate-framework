"""Independent exact rederivation for P073 without canonical API imports."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-21/"
    "bridge_AS1_two_length_transmutation.py"
)
SOURCE_SHA256 = "baca25e9b2b999088c1dc2969f9979cd341c582b3bdcfd009432db0eae9ea6cf"


def main() -> int:
    ledger = CheckLedger("P073-INDEPENDENT")
    source_bytes = SOURCE.read_bytes()
    ledger.check(
        "review reads immutable AS1 source",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )

    dimension_matrix = sp.Matrix([[1, 1, 1], [0, 0, -1]])
    kernel = dimension_matrix.nullspace()
    ledger.check(
        "fresh dimension matrix has rank two",
        dimension_matrix.rank() == 2,
    )
    ledger.check(
        "fresh Buckingham count is one",
        dimension_matrix.cols - dimension_matrix.rank() == 1,
    )
    ledger.check(
        "fresh kernel derives ell1 over ell0",
        kernel == [sp.Matrix([-1, 1, 0])],
    )
    ledger.check(
        "fresh reciprocal generator is equally valid",
        dimension_matrix * (-kernel[0]) == sp.zeros(2, 1),
    )

    mu0, g2, b0, k0, k1 = sp.symbols("mu0 g2 b0 K0 K1", positive=True)
    exponent = 8 * sp.pi**2 / (b0 * g2)
    transmuted_energy = mu0 * sp.exp(-exponent)
    energy_ratio = sp.simplify(transmuted_energy / mu0)
    ell0 = k0 / mu0
    ell1 = k1 / transmuted_energy
    length_ratio = sp.simplify(ell1 / ell0)
    ledger.check(
        "fresh positive one-loop exponent separates formal energies",
        exponent.is_positive and energy_ratio == sp.exp(-exponent),
    )
    ledger.check(
        "fresh inverse-energy conversion gives oriented length ratio",
        length_ratio == k1 * sp.exp(exponent) / k0,
    )
    ledger.check(
        "fresh equal-conversion energy and length ratios are reciprocal",
        sp.simplify((energy_ratio * length_ratio).subs(k1, k0) - 1) == 0,
    )
    ledger.check(
        "fresh unequal-conversion countermodel retains prefactor",
        sp.simplify(energy_ratio * length_ratio - k1 / k0) == 0,
    )
    ledger.check(
        "fresh ratio cancels reference energy but absolute lengths do not",
        not length_ratio.has(mu0) and ell0.has(mu0) and ell1.has(mu0),
    )
    ledger.check(
        "fresh b0 and coupling sensitivities are nonzero",
        sp.diff(length_ratio, b0) != 0 and sp.diff(length_ratio, g2) != 0,
    )

    design = sp.Matrix([[-1, 1]])
    ratio = sp.symbols("R", positive=True)
    rhs = sp.Matrix([sp.log(ratio)])
    ledger.check(
        "fresh relative-log system has one equation and rank one",
        design.rank() == design.row_join(rhs).rank() == 1,
    )
    ledger.check(
        "fresh relative-log system leaves common rescaling",
        design.nullspace() == [sp.Matrix([1, 1])],
    )
    ledger.check(
        "fresh common rescaling changes both absolute coordinates",
        design * sp.Matrix([1, 1]) == sp.zeros(1, 1),
    )
    first_covector = sp.Matrix([[1, 0]])
    second_covector = sp.Matrix([[0, 1]])
    ledger.check(
        "fresh rowspace contains neither absolute coordinate covector",
        design.col_join(first_covector).rank() > design.rank()
        and design.col_join(second_covector).rank() > design.rank(),
    )

    inferred = sp.simplify(8 * sp.pi**2 / (b0 * sp.log(ratio * k0 / k1)))
    ledger.check(
        "fresh coupling inverse round trips on valid ratio",
        sp.simplify(inferred.subs(ratio, length_ratio) - g2) == 0,
    )
    ledger.check(
        "fresh inverse needs ratio above conversion prefactor",
        bool(
            inferred.subs({ratio: 2, k0: 1, k1: 1, b0: 7}) > 0
        )
        and bool(
            inferred.subs({ratio: sp.Rational(1, 2), k0: 1, k1: 1, b0: 7})
            < 0
        ),
    )
    ledger.check(
        "fresh weak and large coupling limits",
        sp.limit(length_ratio, g2, 0, dir="+") == sp.oo
        and sp.limit(length_ratio, g2, sp.oo) == k1 / k0,
    )

    source_text = source_bytes.decode("utf-8")
    ledger.check(
        "fresh source audit finds reciprocal naming conflict",
        "group is xi/a" in source_text
        and "a_over_xi = sp.simplify(a_from_Lam / xi_from_mu0)" in source_text
        and "exactly the Buckingham group xi/a" in source_text,
    )
    ledger.check(
        "fresh source audit finds swapped physical assignments",
        "UV lattice length a" in source_text
        and "IR soliton length xi" in source_text
        and "xi_UV = hbar c0 / mu0" in source_text
        and "a_IR  = hbar c0 / Lambda" in source_text,
    )
    ledger.check(
        "fresh source audit finds omitted b0 in named parameter set",
        "xi_reduced.free_symbols == {a_len, beta2, b0}" in source_text
        and "{a, beta^2}" in source_text,
    )
    ledger.check(
        "fresh source audit distinguishes inverse inference from prediction",
        "ratio_sym" in source_text and "sp.solve" in source_text,
    )
    ledger.check(
        "fresh dependency audit finds unaccepted physical narratives",
        all(label in source_text for label in ("S5", "AS4", "AS6", "AS7")),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
