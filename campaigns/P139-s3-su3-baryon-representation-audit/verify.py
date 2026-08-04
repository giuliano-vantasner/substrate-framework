from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.su3 import invariants, triality_phase
from substrate_framework.su3_representations import (
    SU3Irrep,
    irreps_containing_hypercharge,
    minimal_dimension_hypercharge_matches,
    su3_gelfand_tsetlin_states,
    su3_irrep_dimension,
    su3_irrep_quadratic_casimir,
    su3_irrep_triality,
    su3_weight_multiplicities,
)
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "44d8cd1f3a3b3d0a316d0984db92d5e47e13cac9dcf3d476e2d996bf09f13b9a"
DOSSIER_SHA256 = "4467a11ac07ac9ffe97826722f28887a28f729f275ca81bbae9ea237346181b2"
FROZEN_PROPOSAL_SHA256 = "e2039d4f0cff2b28f9887107af5750141106372f7078b5652752cdcd9a95b1af"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _distinct_hypercharges(p: int, q: int) -> set[sp.Rational]:
    return {state.hypercharge for state in su3_gelfand_tsetlin_states(p, q)}


def main(source_file: str, dossier_file: str) -> int:
    source_path = Path(source_file)
    dossier_path = Path(dossier_file)
    frozen_path = Path(__file__).parent / "evidence" / "frozen-proposal.yaml"
    source_text = source_path.read_text(encoding="utf-8")
    dossier_text = dossier_path.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(source_path))
    checks = CheckLedger("P139/S3")

    checks.check("pinned S3 source hash", _sha256(source_path) == SOURCE_SHA256)
    checks.check("pinned S3 dossier hash", _sha256(dossier_path) == DOSSIER_SHA256)
    checks.check(
        "frozen proposal hash",
        _sha256(frozen_path) == FROZEN_PROPOSAL_SHA256,
    )

    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("ten source predicates", len(source_checks) == 10)
    checks.check("two source assertions", len(source_assertions) == 2)

    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(source_path),
    )
    checks.check(
        "S3 has no NumPy trapezoid compatibility event",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    accepted = invariants()
    checks.check(
        "general Casimir normalization composes with accepted fundamental matrices",
        su3_irrep_quadratic_casimir(1, 0) == accepted.fundamental_casimir
        and su3_irrep_quadratic_casimir(1, 1) == accepted.adjoint_casimir,
    )
    checks.check(
        "general center character composes with accepted abstract triality",
        all(
            triality_phase(su3_irrep_triality(p, q))
            == triality_phase(p + 2 * q)
            for p in range(7)
            for q in range(7)
        ),
    )

    labels = tuple((p, q) for p in range(8) for q in range(8))
    checks.check(
        "complete Gelfand-Tsetlin state count equals Weyl dimension",
        all(
            len(su3_gelfand_tsetlin_states(p, q))
            == su3_irrep_dimension(p, q)
            for p, q in labels
        ),
    )
    checks.check(
        "aggregated weight multiplicities preserve every state",
        all(
            sum(weight.multiplicity for weight in su3_weight_multiplicities(p, q))
            == su3_irrep_dimension(p, q)
            for p, q in labels
        ),
    )

    fundamental = SU3Irrep(1, 0)
    antifundamental = SU3Irrep(0, 1)
    checks.check(
        "p-q conjugation negates the fundamental weights",
        {
            (-weight.isospin_projection, -weight.hypercharge, weight.multiplicity)
            for weight in fundamental.weights
        }
        == {
            (weight.isospin_projection, weight.hypercharge, weight.multiplicity)
            for weight in antifundamental.weights
        },
    )
    checks.check(
        "the standard-convention sextet repairs the source table",
        _distinct_hypercharges(2, 0)
        == {sp.Rational(2, 3), sp.Rational(-1, 3), sp.Rational(-4, 3)}
        and "(2, 0): {Fraction(4, 3), Fraction(1, 3), Fraction(-2, 3)}"
        in source_text,
    )

    low_dimension_irreps = sorted(
        (
            su3_irrep_dimension(p, q),
            p,
            q,
        )
        for p in range(4)
        for q in range(4)
        if su3_irrep_dimension(p, q) <= 10
    )
    checks.check(
        "all irreps through dimension ten have a finite global certificate",
        low_dimension_irreps
        == [
            (1, 0, 0),
            (3, 0, 1),
            (3, 1, 0),
            (6, 0, 2),
            (6, 2, 0),
            (8, 1, 1),
            (10, 0, 3),
            (10, 3, 0),
        ]
        and su3_irrep_dimension(4, 0) > 10
        and su3_irrep_dimension(0, 4) > 10
        and su3_irrep_dimension(1, 2) > 10
        and su3_irrep_dimension(2, 1) > 10,
    )

    y_one_matches = irreps_containing_hypercharge(1, max_p=6, max_q=6)
    checks.check(
        "Y=1 has a unique minimum-dimension octet in the declared domain",
        [(match.p, match.q, match.dimension, match.isospins) for match in minimal_dimension_hypercharge_matches(
            1, max_p=6, max_q=6
        )]
        == [(1, 1, 8, (sp.Rational(1, 2),))],
    )
    checks.check(
        "the next distinct dimension is a visible conjugate tie",
        [
            (match.p, match.q, match.dimension, match.isospins)
            for match in y_one_matches
            if match.dimension == 10
        ]
        == [
            (0, 3, 10, (sp.Rational(1, 2),)),
            (3, 0, 10, (sp.Rational(3, 2),)),
        ],
    )
    checks.check(
        "source finite dictionary cannot certify complete selection",
        "for pq in Y_PHYSICAL" in source_text
        and "(0,3)=10bar also contains Y=1" in source_text
        and "the ANTI-decuplet (B=+1 baryons use (3,0))" in source_text,
    )

    y_two_thirds = irreps_containing_hypercharge(
        sp.Rational(2, 3), max_p=4, max_q=4
    )
    checks.check(
        "complete two-thirds guard selects antitriplet first and admits sextet",
        [(match.p, match.q, match.dimension) for match in y_two_thirds[:2]]
        == [(0, 1, 3), (2, 0, 6)],
    )
    checks.check(
        "source and dossier disagree on the two-color guard",
        "the 3bar (0,1), dim 3" in source_text
        and "N_c=2 would admit the 3, not the 8" in dossier_text
        and "the SEXTET (6) would be the lowest rep" in dossier_text,
    )

    checks.check(
        "source WZW iff is a finite sample rather than a quantified derivation",
        "for Nc in [1, 2, 3, 10]" in source_text
        and "for n in [1, 2, 5]" in source_text
        and "Nc_half = sp.Rational(3, 2)" in source_text,
    )
    checks.check(
        "right-hypercharge formula is evaluated after insertion",
        "Y_R_required = Fraction(Nc * B, 3)" in source_text
        and "Guadagnini-Witten WZW constraint" in source_text
        and not any(
            isinstance(node, ast.FunctionDef) and "collective" in node.name.lower()
            for node in ast.walk(tree)
        ),
    )

    angular_velocity, inertia = sp.symbols("Omega I", real=True)
    level, winding, coefficient, orientation = sp.symbols(
        "k B c sigma", real=True
    )
    declared_lagrangian = (
        inertia * angular_velocity**2 / 2
        + orientation * coefficient * level * winding * angular_velocity
    )
    momentum_shift = sp.simplify(
        sp.diff(declared_lagrangian, angular_velocity)
        - inertia * angular_velocity
    )
    checks.check(
        "a declared collective linear term is sensitive to all missing inputs",
        momentum_shift == orientation * coefficient * level * winding
        and momentum_shift.subs(level, 0) == 0
        and momentum_shift.subs(winding, 0) == 0
        and sp.simplify(
            momentum_shift.subs(orientation, -orientation) + momentum_shift
        )
        == 0
        and sp.diff(momentum_shift, coefficient) != 0,
    )

    inertia_one, inertia_two = sp.symbols("I1 I2", positive=True)
    octet_spin = sp.Rational(1, 2)
    decuplet_spin = sp.Rational(3, 2)

    def conditional_energy(p: int, q: int, spin: sp.Rational) -> sp.Expr:
        return sp.simplify(
            su3_irrep_quadratic_casimir(p, q) / (2 * inertia_two)
            + (1 / (2 * inertia_one) - 1 / (2 * inertia_two))
            * spin
            * (spin + 1)
        )

    octet_energy = conditional_energy(1, 1, octet_spin)
    decuplet_energy = conditional_energy(3, 0, decuplet_spin)
    antidecuplet_energy = conditional_energy(0, 3, octet_spin)
    checks.check(
        "source displayed Hamiltonian gives the decuplet-octet gap through I1",
        sp.simplify(decuplet_energy - octet_energy)
        == sp.Rational(3, 2) / inertia_one
        and sp.simplify(decuplet_energy - octet_energy)
        != sp.Rational(3, 2) / inertia_two,
    )
    checks.check(
        "the claimed I2 gap instead belongs to the same-spin conjugate",
        sp.simplify(antidecuplet_energy - octet_energy)
        == sp.Rational(3, 2) / inertia_two,
    )

    fundamental_rows = {
        (row.isospin, row.hypercharge) for row in fundamental.isospin_multiplets
    }
    checks.check(
        "fundamental branching refutes the source universal spin range",
        fundamental_rows
        == {
            (sp.Rational(1, 2), sp.Rational(1, 3)),
            (sp.Integer(0), sp.Rational(-2, 3)),
        }
        and "J ranges from |p-q|/2 to (p+q)/2" in source_text,
    )
    checks.check(
        "right-row isospin derives the three relevant conditional spins",
        SU3Irrep(1, 1).multiplets_at_hypercharge(1)[0].isospin
        == sp.Rational(1, 2)
        and SU3Irrep(3, 0).multiplets_at_hypercharge(1)[0].isospin
        == sp.Rational(3, 2)
        and SU3Irrep(0, 3).multiplets_at_hypercharge(1)[0].isospin
        == sp.Rational(1, 2),
    )

    checks.check(
        "source ceiling inserts rather than derives both periods",
        "wzw_period = sp.Integer(1)" in source_text
        and "exact_period = sp.Integer(0)" in source_text,
    )

    missing_state_mutation = su3_gelfand_tsetlin_states(2, 2)[:-1]
    checks.check(
        "state omission mutation breaks the dimension gate",
        len(missing_state_mutation) != su3_irrep_dimension(2, 2),
    )
    wrong_hypercharge_scale = {
        state.hypercharge / 2 for state in su3_gelfand_tsetlin_states(1, 0)
    }
    checks.check(
        "hypercharge normalization mutation breaks the fundamental fixture",
        wrong_hypercharge_scale != {sp.Rational(1, 3), sp.Rational(-2, 3)},
    )

    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file")
    parser.add_argument("dossier_file")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_file, arguments.dossier_file))
