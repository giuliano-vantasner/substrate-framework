from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from itertools import combinations_with_replacement
from pathlib import Path

import sympy as sp

from substrate_framework.su3_representations import (
    irreps_containing_hypercharge,
    su3_irrep_dimension,
    su3_irrep_quadratic_casimir,
    su3_weight_multiplicities,
)
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "44d8cd1f3a3b3d0a316d0984db92d5e47e13cac9dcf3d476e2d996bf09f13b9a"
DOSSIER_SHA256 = "4467a11ac07ac9ffe97826722f28887a28f729f275ca81bbae9ea237346181b2"
FROZEN_PROPOSAL_SHA256 = "e2039d4f0cff2b28f9887107af5750141106372f7078b5652752cdcd9a95b1af"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tableau_contents(p: int, q: int) -> tuple[tuple[int, int, int], ...]:
    """Enumerate SSYT contents for shape ``(p+q,q)`` over entries 1,2,3."""

    contents: list[tuple[int, int, int]] = []
    for first_row in combinations_with_replacement((1, 2, 3), p + q):
        for second_row in combinations_with_replacement((1, 2, 3), q):
            if all(first_row[column] < second_row[column] for column in range(q)):
                entries = first_row + second_row
                contents.append(tuple(entries.count(value) for value in (1, 2, 3)))
    return tuple(contents)


def _tableau_weights(
    p: int, q: int
) -> Counter[tuple[sp.Rational, sp.Rational]]:
    weights: Counter[tuple[sp.Rational, sp.Rational]] = Counter()
    for first, second, third in _tableau_contents(p, q):
        isospin_projection = sp.Rational(first - second, 2)
        hypercharge = sp.Rational(first + second - 2 * third, 3)
        weights[(isospin_projection, hypercharge)] += 1
    return weights


def _isospins_at_hypercharge(
    weights: Counter[tuple[sp.Rational, sp.Rational]],
    hypercharge: sp.Rational,
) -> tuple[sp.Rational, ...]:
    remaining = Counter(
        {
            projection: multiplicity
            for (projection, value), multiplicity in weights.items()
            if value == hypercharge
        }
    )
    multiplets: list[sp.Rational] = []
    while any(multiplicity for multiplicity in remaining.values()):
        isospin = max(
            projection
            for projection, multiplicity in remaining.items()
            if multiplicity
        )
        if isospin < 0:
            raise AssertionError("incomplete SU(2) multiplet in tableau weights")
        multiplets.append(isospin)
        projection = -isospin
        while projection <= isospin:
            if remaining[projection] <= 0:
                raise AssertionError("nonintegral SU(2) branching multiplicity")
            remaining[projection] -= 1
            projection += 1
    return tuple(sorted(multiplets))


def _weyl_product_dimension(p: int, q: int) -> sp.Integer:
    positive_root_pairing_ratios = (
        sp.Integer(p + 1),
        sp.Integer(q + 1),
        sp.Rational(p + q + 2, 2),
    )
    return sp.prod(positive_root_pairing_ratios)


def _highest_weight_casimir(p: int, q: int) -> sp.Expr:
    inverse_cartan = sp.Matrix(
        [[sp.Rational(2, 3), sp.Rational(1, 3)],
         [sp.Rational(1, 3), sp.Rational(2, 3)]]
    )
    highest_weight = sp.Matrix([p, q])
    weyl_vector = sp.Matrix([1, 1])
    return sp.simplify(
        (highest_weight.T * inverse_cartan * (highest_weight + 2 * weyl_vector))[0]
        / 2
    )


def _canonical_weights(
    p: int, q: int
) -> Counter[tuple[sp.Rational, sp.Rational]]:
    return Counter(
        {
            (weight.isospin_projection, weight.hypercharge): weight.multiplicity
            for weight in su3_weight_multiplicities(p, q)
        }
    )


def _weak_column_tableau_count(p: int, q: int) -> int:
    return sum(
        1
        for first_row in combinations_with_replacement((1, 2, 3), p + q)
        for second_row in combinations_with_replacement((1, 2, 3), q)
        if all(first_row[column] <= second_row[column] for column in range(q))
    )


def main(source_file: str, dossier_file: str) -> int:
    source_path = Path(source_file)
    dossier_path = Path(dossier_file)
    frozen_path = Path(__file__).parents[1] / "evidence" / "frozen-proposal.yaml"
    checks = CheckLedger("P139-INDEPENDENT-SU3-TABLEAUX")

    checks.check("fresh source hash", _sha256(source_path) == SOURCE_SHA256)
    checks.check("fresh dossier hash", _sha256(dossier_path) == DOSSIER_SHA256)
    checks.check(
        "fresh frozen proposal hash",
        _sha256(frozen_path) == FROZEN_PROPOSAL_SHA256,
    )

    labels = tuple((p, q) for p in range(6) for q in range(6))
    checks.check(
        "independent Weyl positive-root product matches every canonical dimension",
        all(_weyl_product_dimension(p, q) == su3_irrep_dimension(p, q) for p, q in labels),
    )
    checks.check(
        "independent highest-weight inner product matches every canonical Casimir",
        all(
            _highest_weight_casimir(p, q)
            == su3_irrep_quadratic_casimir(p, q)
            for p, q in labels
        ),
    )
    checks.check(
        "independent semistandard tableaux count every state",
        all(len(_tableau_contents(p, q)) == su3_irrep_dimension(p, q) for p, q in labels),
    )
    checks.check(
        "independent tableau weights match every canonical multiplicity",
        all(_tableau_weights(p, q) == _canonical_weights(p, q) for p, q in labels),
    )

    fundamental = _tableau_weights(1, 0)
    sextet_hypercharges = {value for _, value in _tableau_weights(2, 0)}
    checks.check(
        "fresh fundamental sums fix the hypercharge normalization",
        set(fundamental) == {
            (sp.Rational(1, 2), sp.Rational(1, 3)),
            (sp.Rational(-1, 2), sp.Rational(1, 3)),
            (sp.Integer(0), sp.Rational(-2, 3)),
        }
        and sextet_hypercharges
        == {sp.Rational(2, 3), sp.Rational(-1, 3), sp.Rational(-4, 3)},
    )

    for p, q in labels:
        conjugate = Counter(
            {(-i3, -hypercharge): multiplicity for (i3, hypercharge), multiplicity in _tableau_weights(p, q).items()}
        )
        if conjugate != _tableau_weights(q, p):
            raise AssertionError(f"conjugation failed for {(p, q)}")
    checks.check("fresh tableaux satisfy p-q conjugation", True)

    y_one = sp.Integer(1)
    independent_matches = sorted(
        (
            su3_irrep_dimension(p, q),
            p,
            q,
            _isospins_at_hypercharge(_tableau_weights(p, q), y_one),
        )
        for p, q in labels
        if any(value == y_one for _, value in _tableau_weights(p, q))
    )
    canonical_matches = [
        (match.dimension, match.p, match.q, tuple(sorted(match.isospins)))
        for match in irreps_containing_hypercharge(1, max_p=5, max_q=5)
    ]
    checks.check(
        "fresh supplied-hypercharge filter matches the canonical declared domain",
        independent_matches == canonical_matches,
    )
    checks.check(
        "fresh filter exposes the complete first two dimension layers",
        independent_matches[:3]
        == [
            (8, 1, 1, (sp.Rational(1, 2),)),
            (10, 0, 3, (sp.Rational(1, 2),)),
            (10, 3, 0, (sp.Rational(3, 2),)),
        ],
    )

    inertia_one, inertia_two = sp.symbols("I1 I2", positive=True)
    octet_spin = sp.Rational(1, 2)
    decuplet_spin = sp.Rational(3, 2)
    antidecuplet_spin = sp.Rational(1, 2)

    def rotor(casimir: sp.Expr, spin: sp.Rational) -> sp.Expr:
        return sp.simplify(
            casimir / (2 * inertia_two)
            + (1 / (2 * inertia_one) - 1 / (2 * inertia_two))
            * spin
            * (spin + 1)
        )

    octet_energy = rotor(_highest_weight_casimir(1, 1), octet_spin)
    decuplet_energy = rotor(_highest_weight_casimir(3, 0), decuplet_spin)
    antidecuplet_energy = rotor(
        _highest_weight_casimir(0, 3), antidecuplet_spin
    )
    checks.check(
        "fresh displayed-Hamiltonian algebra assigns the decuplet gap to I1",
        sp.simplify(decuplet_energy - octet_energy)
        == sp.Rational(3, 2) / inertia_one,
    )
    checks.check(
        "fresh displayed-Hamiltonian algebra assigns the same-spin conjugate gap to I2",
        sp.simplify(antidecuplet_energy - octet_energy)
        == sp.Rational(3, 2) / inertia_two,
    )

    checks.check(
        "strict column mutation is load bearing",
        _weak_column_tableau_count(1, 1) != su3_irrep_dimension(1, 1),
    )
    wrong_sextet = {
        sp.Rational(4, 3),
        sp.Rational(1, 3),
        sp.Rational(-2, 3),
    }
    checks.check(
        "source hypercharge mutation is detected",
        wrong_sextet != sextet_hypercharges
        and sp.Rational(2, 3) not in wrong_sextet
        and sp.Rational(2, 3) in sextet_hypercharges,
    )
    checks.check(
        "omitting the conjugate dimension tie changes the verdict",
        (10, 0, 3, (sp.Rational(1, 2),)) in independent_matches
        and [item for item in independent_matches if item[0] == 10]
        != [(10, 3, 0, (sp.Rational(3, 2),))],
    )

    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file")
    parser.add_argument("dossier_file")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_file, arguments.dossier_file))
