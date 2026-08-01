#!/usr/bin/env python3
"""Verify P038's TT image/basis theorem and audit GW3's scope."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

import sympy as sp

from substrate_framework.tt_angular import (
    circular_tt_polarizations,
    frobenius_inner_product,
    rotated_tt_polarizations,
    transverse_projector,
    tt_basis_reconstruct,
    tt_operator_matrix,
    tt_polarization_basis,
    tt_project_symmetric,
)
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "3b941debf6933729b693b928579d4a7f1d73d906911c2fcedb9316ad08038326"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P038-GW3")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    ledger.check(
        "the audited GW3 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    reproduction = subprocess.run(
        [sys.executable, str(args.source_file)],
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    ledger.check("GW3 exits cleanly", reproduction.returncode == 0)
    ledger.check(
        "GW3's declared fifteen-check tally reproduces",
        "ALL 15 CHECKS PASS" in reproduction.stdout,
    )
    ledger.check(
        "GW3 itself marks the physical TT and graviton map as imported",
        "IMPORTED:  the TT-gauge / TT-projector construction" in source_text
        and 'map "TT count = propagating graviton polarizations"' in source_text,
    )

    direction = sp.Matrix([1, 2, 2])
    projector = transverse_projector(direction)
    ledger.check(
        "the transverse projector has exact rank two",
        projector.rank() == 2
        and sp.trace(projector) == 2
        and sp.simplify(projector**2 - projector) == sp.zeros(3),
    )
    operator = tt_operator_matrix(direction)
    ledger.check(
        "the TT operator is an exact self-adjoint projector on symmetric tensors",
        sp.simplify(operator - operator.T) == sp.zeros(6)
        and sp.simplify(operator**2 - operator) == sp.zeros(6),
    )
    ledger.check(
        "the TT image has exact dimension two rather than a displayed-pair count",
        operator.rank() == 2
        and sp.trace(operator) == 2
        and operator.eigenvals() == {sp.Integer(1): 2, sp.Integer(0): 4},
    )

    basis = tt_polarization_basis(direction, reference=[1, -1, 0])
    ledger.check(
        "the transverse frame is orthonormal and positively oriented",
        sp.simplify(basis.first_transverse.dot(basis.direction)) == 0
        and sp.simplify(basis.second_transverse.dot(basis.direction)) == 0
        and sp.simplify(
            basis.first_transverse.dot(basis.second_transverse)
        )
        == 0
        and sp.simplify(basis.first_transverse.cross(basis.second_transverse) - basis.direction)
        == sp.zeros(3, 1),
    )
    ledger.check(
        "plus and cross are individually symmetric transverse and traceless",
        all(
            tensor == tensor.T
            and sp.trace(tensor) == 0
            and sp.simplify(tensor * basis.direction) == sp.zeros(3, 1)
            for tensor in (basis.plus, basis.cross)
        ),
    )
    ledger.check(
        "plus and cross are Frobenius-orthonormal in the accepted convention",
        frobenius_inner_product(basis.plus, basis.plus) == 1
        and frobenius_inner_product(basis.cross, basis.cross) == 1
        and frobenius_inner_product(basis.plus, basis.cross) == 0,
    )

    arbitrary = sp.Matrix([[3, 2, 1], [2, -1, 4], [1, 4, 5]])
    ledger.check(
        "basis dyadic completeness equals the accepted TT projector",
        sp.simplify(
            tt_basis_reconstruct(arbitrary, basis)
            - tt_project_symmetric(arbitrary, direction)
        )
        == sp.zeros(3),
    )
    ledger.check(
        "the normalized basis fixes exactly two coefficient coordinates",
        sp.simplify(
            tt_basis_reconstruct(basis.plus, basis) - basis.plus
        )
        == sp.zeros(3)
        and sp.simplify(
            tt_basis_reconstruct(basis.cross, basis) - basis.cross
        )
        == sp.zeros(3),
    )

    source_plus = sp.diag(1, -1, 0)
    source_cross = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    ledger.check(
        "GW3's displayed tensors are orthogonal but not orthonormal",
        frobenius_inner_product(source_plus, source_plus) == 2
        and frobenius_inner_product(source_cross, source_cross) == 2
        and frobenius_inner_product(source_plus, source_cross) == 0,
    )
    axis_basis = tt_polarization_basis([0, 0, 1], reference=[1, 0, 0])
    ledger.check(
        "division by square root two repairs GW3's normalization",
        source_plus == sp.sqrt(2) * axis_basis.plus
        and source_cross == sp.sqrt(2) * axis_basis.cross,
    )

    def normalization_complete(candidate: object) -> bool:
        scale = sp.sympify(candidate)
        plus = scale * source_plus
        cross = scale * source_cross
        reconstructed = sp.simplify(
            frobenius_inner_product(arbitrary, plus) * plus
            + frobenius_inner_product(arbitrary, cross) * cross
        )
        return (
            frobenius_inner_product(plus, plus) == 1
            and frobenius_inner_product(cross, cross) == 1
            and sp.simplify(
                reconstructed - tt_project_symmetric(arbitrary, [0, 0, 1])
            )
            == sp.zeros(3)
        )

    ledger.mutation_sensitive(
        "polarization normalization and completeness",
        normalization_complete,
        1 / sp.sqrt(2),
        [sp.Integer(1), sp.Rational(1, 2), sp.sqrt(2)],
    )

    for coordinate_direction in ([1, 0, 0], [0, 1, 0], [0, 0, 1]):
        coordinate_basis = tt_polarization_basis(coordinate_direction)
        ledger.check(
            f"the piecewise frame covers coordinate direction {coordinate_direction}",
            coordinate_basis.first_transverse.dot(coordinate_basis.direction) == 0
            and coordinate_basis.second_transverse.dot(coordinate_basis.direction) == 0,
        )

    angle = sp.symbols("psi", real=True)
    rotated_plus, rotated_cross = rotated_tt_polarizations(axis_basis, angle)
    first = (
        sp.cos(angle) * axis_basis.first_transverse
        + sp.sin(angle) * axis_basis.second_transverse
    )
    second = (
        -sp.sin(angle) * axis_basis.first_transverse
        + sp.cos(angle) * axis_basis.second_transverse
    )
    direct_plus = sp.simplify((first * first.T - second * second.T) / sp.sqrt(2))
    direct_cross = sp.simplify((first * second.T + second * first.T) / sp.sqrt(2))
    ledger.check(
        "direct transverse-frame rotation gives the exact double-angle tensor law",
        sp.simplify(rotated_plus - direct_plus) == sp.zeros(3)
        and sp.simplify(rotated_cross - direct_cross) == sp.zeros(3),
    )

    def rotation_weight_matches(candidate: object) -> bool:
        weight = sp.sympify(candidate)
        plus = sp.cos(weight * angle) * axis_basis.plus + sp.sin(weight * angle) * axis_basis.cross
        cross = -sp.sin(weight * angle) * axis_basis.plus + sp.cos(weight * angle) * axis_basis.cross
        return sp.simplify(plus - direct_plus) == sp.zeros(3) and sp.simplify(
            cross - direct_cross
        ) == sp.zeros(3)

    ledger.mutation_sensitive(
        "transverse-frame rotation weight",
        rotation_weight_matches,
        sp.Integer(2),
        [sp.Integer(1), sp.Integer(3), sp.Integer(-2)],
    )

    right, left = circular_tt_polarizations(axis_basis)
    rotated_right = sp.simplify((rotated_plus + sp.I * rotated_cross) / sp.sqrt(2))
    rotated_left = sp.simplify((rotated_plus - sp.I * rotated_cross) / sp.sqrt(2))
    ledger.check(
        "the circular algebra has opposite weight-two frame phases",
        sp.simplify(
            rotated_right
            - (sp.cos(2 * angle) - sp.I * sp.sin(2 * angle)) * right
        )
        == sp.zeros(3)
        and sp.simplify(
            rotated_left
            - (sp.cos(2 * angle) + sp.I * sp.sin(2 * angle)) * left
        )
        == sp.zeros(3),
    )
    ledger.check(
        "cross-sign reversal is a basis convention that preserves the projector span",
        sp.simplify(
            frobenius_inner_product(arbitrary, axis_basis.plus) * axis_basis.plus
            + frobenius_inner_product(arbitrary, -axis_basis.cross) * (-axis_basis.cross)
            - tt_project_symmetric(arbitrary, [0, 0, 1])
        )
        == sp.zeros(3),
    )

    plane_trace = transverse_projector([0, 0, 1])
    ledger.check(
        "omitting trace removal leaves a third transverse-symmetric direction",
        sp.trace(plane_trace) == 2
        and tt_project_symmetric(plane_trace, [0, 0, 1]) == sp.zeros(3)
        and plane_trace != sp.zeros(3),
    )
    ledger.check(
        "GW3's provenance narrative misreports its own guard trace as four",
        "guard Tr(Lambda_wrong)=4" in source_text
        and "Tr(Lambda_wrong) = 3" in reproduction.stdout,
    )
    ledger.check(
        "rank-two spatial algebra does not establish propagating gravitational modes",
        "the 'TT count = graviton DOF' map (G6 input)" in source_text,
    )

    count = ledger.finish()
    print(f"P038 GW3 TT POLARIZATION-BASIS AUDIT ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
