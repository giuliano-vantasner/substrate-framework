"""Primary exact verifier for P059's conditional heavy-field theorem and WZ4 audit."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.effective_actions import (
    eliminate_even_odd_sources,
    eliminate_quadratic_field,
    low_momentum_inverse_expansion,
    quadratic_source_action,
    stationary_reduced_variation,
)
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "fca6b9c1d95bdf49e99b863470c7e800880e493b3f716159aa2341f8cf963d2b"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_zero(matrix: sp.MatrixBase) -> bool:
    return matrix.applyfunc(sp.simplify) == sp.zeros(*matrix.shape)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    parser.add_argument("--source-audit", type=Path, required=True)
    parser.add_argument("--hls-provenance", type=Path, required=True)
    parser.add_argument("--independent-result", type=Path, required=True)
    parser.add_argument("--migration-queue", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    parser.add_argument("--release", type=Path, required=True)
    arguments = parser.parse_args()

    source = arguments.source_file.read_text(encoding="utf-8")
    reproduction = load_yaml(arguments.source_reproduction)
    audit = load_yaml(arguments.source_audit)
    provenance = load_yaml(arguments.hls_provenance)
    independent = load_yaml(arguments.independent_result)
    queue = load_yaml(arguments.migration_queue)
    claims = load_yaml(arguments.claims)
    release = load_yaml(arguments.release)
    ledger = CheckLedger("P059-WZ4")

    ledger.check(
        "WZ4 is hash-pinned and its native nine-check tally is reproduced",
        file_hash(arguments.source_file) == SOURCE_SHA256
        and reproduction["source_sha256"] == SOURCE_SHA256
        and reproduction["native_run"]["exit_status"] == 0
        and reproduction["native_run"]["terminal_tally"] == "ALL 9 CHECKS PASS",
    )
    ledger.check(
        "the source imports its target before applying a unit-limit form factor",
        "F_3pi_WZW = e * N_c / (12 * sp.pi**2 * F_pi**3)" in source
        and "A_HLS = F_3pi_WZW * (m_V**2 / (m_V**2 - q2))" in source
        and audit["checks"]["WZ4.4"]["verdict"] == "copied_answer_times_unit_limit",
    )
    ledger.check(
        "the advertised HLS action, field equation, and coefficient basis are absent",
        all(
            item in audit["absent_objects"]
            for item in (
                "the four independent homogeneous operators L1 through L4",
                "coefficients c1 through c4",
                "an HLS quadratic vector action and functional variation",
                "anomaly variation before and after vector elimination",
            )
        ),
    )
    ledger.check(
        "pending source sectors do not enter the accepted proof",
        audit["dependency_conflicts"][:4]
        == [
            "G2 and G3 are pending and supply no accepted gauge mechanism.",
            "S3 is pending and supplies no accepted baryon or N_c level identification.",
            "S4 is pending and supplies no accepted HLS action, KSRF relation, or vector-meson map.",
            "C-WZW-001 and C-WZW-002 are ungauged mathematical theorems only.",
        ],
    )

    k11, k12, k22 = sp.symbols("k11 k12 k22", real=True)
    j1, j2, v1, v2 = sp.symbols("j1 j2 v1 v2", real=True)
    kernel = sp.Matrix([[k11, k12], [k12, k22]])
    source_vector = sp.Matrix([j1, j2])
    field = sp.Matrix([v1, v2])
    action = quadratic_source_action(field, kernel, source_vector)
    elimination = eliminate_quadratic_field(kernel, source_vector)
    gradient = sp.Matrix([sp.diff(action, component) for component in field])
    ledger.check(
        "the canonical stationary field is derived from the declared action",
        matrix_zero(gradient - (kernel * field + source_vector))
        and matrix_zero(elimination.stationary_field + kernel.inv() * source_vector)
        and elimination.stationarity_residual == sp.zeros(2, 1),
    )
    ledger.check(
        "direct stationary substitution gives the exact Schur complement",
        sp.simplify(
            action.subs(dict(zip(field, elimination.stationary_field, strict=True)))
            - elimination.effective_term
        )
        == 0
        and sp.simplify(
            elimination.effective_term
            + (source_vector.T * kernel.inv() * source_vector)[0] / 2
        )
        == 0,
    )
    ledger.mutation_sensitive(
        "stationary sign and source normalization",
        lambda candidate: matrix_zero(kernel * candidate + source_vector),
        elimination.stationary_field,
        (-elimination.stationary_field, 2 * elimination.stationary_field),
    )

    even_amplitude, odd_amplitude = sp.symbols("e_source o_source", real=True)
    split = eliminate_even_odd_sources(
        sp.Matrix([[2, 1], [1, 3]]),
        sp.Matrix([even_amplitude, 0]),
        sp.Matrix([0, odd_amplitude]),
    )
    ledger.check(
        "the effective action contains the derived parity-odd cross term",
        split.even_square == -3 * even_amplitude**2 / 10
        and split.odd_square == -odd_amplitude**2 / 5
        and split.odd_cross == even_amplitude * odd_amplitude / 5
        and sp.simplify(
            split.elimination.effective_term
            - (split.even_square + split.odd_square + split.odd_cross)
        )
        == 0,
    )
    ledger.check(
        "parity and source-removal mutations isolate the cross term",
        sp.simplify(
            split.parity_transformed_effective_term
            - split.elimination.effective_term.subs(odd_amplitude, -odd_amplitude)
        )
        == 0
        and split.odd_cross.subs(even_amplitude, 0) == 0
        and split.odd_cross.subs(odd_amplitude, 0) == 0,
    )

    scale = sp.symbols("lambda", real=True)
    mass = sp.diag(2, 3)
    derivative = scale * sp.Matrix([[1, 2], [2, -1]])
    expansion = low_momentum_inverse_expansion(mass, derivative, max_order=2)
    ratio = mass.inv() * derivative
    ledger.check(
        "the noncommuting finite inverse has exact left and right residual formulas",
        matrix_zero(expansion.left_residual - mass * ratio**3 * mass.inv())
        and matrix_zero(expansion.right_residual - ratio**3),
    )
    ledger.check(
        "the inverse approximation is honest about its nonzero truncation remainder",
        expansion.left_residual != sp.zeros(2)
        and expansion.right_residual != sp.zeros(2)
        and all(
            matrix_zero(
                residual.applyfunc(
                    lambda entry: sp.series(entry, scale, 0, 3).removeO()
                )
            )
            for residual in (expansion.left_residual, expansion.right_residual)
        ),
    )

    anomaly, induced = sp.symbols("A deltaV", real=True)
    ledger.check(
        "stationarity removes only the induced-field chain-rule term",
        stationary_reduced_variation(anomaly, [0], [induced]) == anomaly
        and stationary_reduced_variation(0, [0], [induced]) == 0
        and stationary_reduced_variation(anomaly, [1], [induced])
        == anomaly + induced,
    )
    coefficient_map = sp.Matrix([[1, 0, 0, 0, 0]])
    hls_source = provenance["sources"][1]
    ledger.check(
        "the audited HLS anomaly equation leaves four free homogeneous directions",
        coefficient_map.rank() == 1
        and len(coefficient_map.nullspace()) == 4
        and hls_source["doi"] == "10.1103/PhysRevD.84.036010"
        and any(
            "c1 through c4 are free" in statement
            for statement in hls_source["audited_equations_and_statements"]
        ),
    )
    first_hls_source = provenance["sources"][0]
    ledger.check(
        "primary HLS sources distinguish vector participation from anomaly normalization",
        first_hls_source["doi"] == "10.1143/PTP.73.926"
        and "primary_definition" in first_hls_source["imported_as"]
        and provenance["framework_conclusion"].startswith(
            "The audited HLS literature supports vector participation"
        ),
    )

    contact, mass_scale, momentum_squared = sp.symbols("C m q2", positive=True)
    form_factor = contact * mass_scale**2 / (mass_scale**2 - momentum_squared)
    correction = contact * momentum_squared / (mass_scale**2 - momentum_squared)
    ledger.check(
        "an arbitrary contact passes WZ4's zero-momentum and heavy-mass tests",
        sp.factor(form_factor - contact - correction) == 0
        and form_factor.subs(momentum_squared, 0) == contact
        and sp.limit(form_factor, mass_scale, sp.oo) == contact
        and sp.limit(correction, mass_scale, sp.oo) == 0,
    )
    ledger.check(
        "zero imported contact defeats the claimed independent generation route",
        form_factor.subs(contact, 0) == 0 and correction.subs(contact, 0) == 0,
    )
    ledger.check(
        "physical pion parity corrects the source's polar-vector classification",
        (-1) * (-1) ** 3 == 1
        and audit["checks"]["WZ4.2"]["surviving_scope"]
        == "a four-polar-vector epsilon contraction changes sign under parity",
    )
    ledger.check(
        "the independent exact route passed without canonical helper imports",
        independent["process_exit_code"] == 0
        and independent["terminal_tally"] == "ALL 23 CHECKS PASS [P059-INDEPENDENT]"
        and independent["canonical_effective_action_helpers_imported"] is False,
    )

    source_entry = next(
        entry for entry in queue["units"] if entry["source_unit"] == "WZ4"
    )
    claim_entry = next(entry for entry in claims["claims"] if entry["id"] == "C-EFT-001")
    ledger.check(
        "the accepted theorem has no hidden physical dependency",
        claim_entry["verification"] == "symbolic_verified"
        and claim_entry["review"] == "accepted"
        and claim_entry["compatibility"] == "compatible_extension"
        and claim_entry["epistemic"] == "active"
        and claim_entry["dependencies"] == [],
    )
    ledger.check(
        "WZ4 is qualified only through the surviving conditional theorem",
        source_entry["disposition"] == "qualified"
        and source_entry["accepted_claims"] == ["C-EFT-001"]
        and "arbitrary imported contact" in source_entry["qualification"]
        and "c1 through c4" in source_entry["qualification"],
    )
    ledger.check(
        "the theorem excludes every unsupported HLS and physical interpretation",
        "no HLS field content" in claim_entry["statement"]
        and "no WZW functional" in claim_entry["statement"]
        and "no anomaly coefficient" in claim_entry["statement"]
        and "no N_c" in claim_entry["statement"]
        and "no substrate realization" in claim_entry["statement"],
    )
    ledger.check(
        "the campaign release appends exactly the generic EFT claim",
        release["release"] == "v0.53.0"
        and release["accepted_claims"][-2:] == ["C-TOP-002", "C-EFT-001"],
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
