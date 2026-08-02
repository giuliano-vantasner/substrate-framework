"""Primary exact verifier for P056's SU(3) trace-five theorem."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger
from substrate_framework.wzw import (
    alternating_trace,
    antihermitian_generators,
    antihermitian_structure_constants,
    chevalley_eilenberg_differential,
    cochain_basis,
    extension_phase_ratio,
    glued_filling_period,
    maurer_cartan_power_derivative_multiplier,
    su3_real_trace_five_cochain,
    su3_trace_five_cohomology,
    su3_trace_power_cochain,
    trace_power_derivative_multiplier,
)


SOURCE_SHA256 = "87bab354a83a6edd05ed77ed0778e1cdf11cf402f92414664f7a3196df0551b9"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    parser.add_argument("--source-audit", type=Path, required=True)
    parser.add_argument("--independent-result", type=Path, required=True)
    parser.add_argument("--migration-queue", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    parser.add_argument("--release", type=Path, required=True)
    arguments = parser.parse_args()

    source = arguments.source_file.read_text()
    reproduction = load_yaml(arguments.source_reproduction)
    audit = load_yaml(arguments.source_audit)
    independent = load_yaml(arguments.independent_result)
    queue = load_yaml(arguments.migration_queue)
    claims = load_yaml(arguments.claims)
    release = load_yaml(arguments.release)
    ledger = CheckLedger("P056-WZ1")

    ledger.check(
        "WZ1 is the hash-pinned primary source",
        file_hash(arguments.source_file) == SOURCE_SHA256
        and reproduction["sha256"] == SOURCE_SHA256,
    )
    ledger.check(
        "the source process exit and complete tally are preserved",
        reproduction["exit_code"] == 0
        and reproduction["terminal_tally"] == "ALL 12 CHECKS PASS",
    )
    ledger.check(
        "the reported nonzero period is a literal assignment rather than an oracle",
        "wzw_period = sp.Integer(1)" in source
        and audit["global_non_exactness"]["source_period_oracle"] == "hard_coded",
    )
    ledger.check(
        "the metric and locality checks contain ceremonial stand-ins",
        "omega5_weyl = sp.Integer(1)" in source
        and "uses_first_derivs_only = True" in source
        and audit["metric_and_locality"]["sensitive_source_oracle"] is False,
    )

    generators = antihermitian_generators()
    gram = sp.Matrix(8, 8, lambda a, b: sp.trace(generators[a] * generators[b]))
    ledger.check(
        "accepted Hermitian generators convert to the exact anti-Hermitian convention",
        gram == -sp.eye(8) / 2
        and all(generator.H == -generator for generator in generators),
    )
    raw_trace = su3_trace_power_cochain(5)
    real_trace = su3_real_trace_five_cochain()
    ledger.check(
        "minus i converts the imaginary trace-five cochain to a real nonzero form",
        raw_trace == sp.I * real_trace
        and all(sp.im(value) == 0 for value in real_trace)
        and sum(value != 0 for value in real_trace) == 9,
    )
    ledger.mutation_sensitive(
        "the frozen trace normalization detects generator rescaling",
        lambda scale: sp.simplify(
            -sp.I
            * alternating_trace(tuple(scale * generators[index] for index in range(5)))
            + sp.Rational(15, 8)
        )
        == 0,
        sp.Integer(1),
        [sp.Integer(2), sp.Integer(-1)],
    )

    trace_four = su3_trace_power_cochain(4)
    ledger.check(
        "the source's even-power rejection guard is mathematically false",
        "d Tr(L^4) = -4 Tr(L^5)" in source
        and trace_four == sp.zeros(70, 1)
        and trace_power_derivative_multiplier(4) == 0
        and -4 * raw_trace != sp.zeros(56, 1)
        and audit["even_power_guard"]["verdict"] == "false",
    )
    ledger.check(
        "the correct odd closedness and boundary-variation coefficients survive",
        trace_power_derivative_multiplier(5) == 5
        and maurer_cartan_power_derivative_multiplier(4) == 0
        and audit["ungauged_variation"]["exact_boundary_identity"] is True,
    )

    d4 = chevalley_eilenberg_differential(4)
    d5 = chevalley_eilenberg_differential(5)
    evidence = su3_trace_five_cohomology()
    ledger.check(
        "the exact SU(3) Chevalley-Eilenberg operators form a complex",
        d5 * d4 == sp.zeros(28, 70) and evidence.differential_squares_to_zero,
    )
    ledger.check(
        "the real trace-five cochain is an exact nonzero cocycle",
        d5 * real_trace == sp.zeros(28, 1)
        and evidence.trace_is_closed
        and evidence.trace_nonzero_components == 9,
    )
    ledger.check(
        "exact ranks derive a one-dimensional fifth invariant cohomology",
        evidence.d4_rank == 35
        and evidence.d5_rank == 20
        and evidence.five_cocycle_dimension == 36
        and evidence.fifth_cohomology_dimension == 1,
    )
    ledger.check(
        "rank augmentation proves the trace cochain is not a coboundary",
        evidence.augmented_d4_trace_rank == evidence.d4_rank + 1
        and not evidence.trace_is_exact,
    )
    ledger.check(
        "a nonzero dual pairing independently separates it from every coboundary",
        real_trace.T * d4 == sp.zeros(1, 70)
        and evidence.trace_norm_squared == sp.Rational(75, 4)
        and evidence.trace_annihilates_coboundaries,
    )
    ledger.check(
        "Haar averaging closes the invariant-to-global non-exactness implication",
        audit["global_non_exactness"]["replacement_oracle"]
        == "exact_CE_nonimage_plus_compact_Haar_averaging",
    )

    constants = antihermitian_structure_constants()
    mutated = [[list(row) for row in plane] for plane in constants]
    mutated[0][1][2] = -mutated[0][1][2]
    mutated = tuple(tuple(tuple(row) for row in plane) for plane in mutated)
    mutated_d4 = chevalley_eilenberg_differential(4, mutated)
    mutated_d5 = chevalley_eilenberg_differential(5, mutated)
    ledger.check(
        "one accepted-bracket mutation destroys the cochain-complex oracle",
        mutated_d5 * mutated_d4 != sp.zeros(28, 70),
    )
    ledger.check(
        "dimension and commuting limits cannot fake a trace five-form",
        len(tuple(__import__("itertools").combinations(range(3), 5))) == 0
        and alternating_trace(
            tuple(sp.I * sp.diag(index, -index, 0) for index in (1, 2, 3, 4, 5))
        )
        == 0,
    )

    first, second, coefficient = sp.symbols("I_B I_Bprime k", real=True)
    ledger.check(
        "oriented filling gluing is subtraction and carries no hidden period value",
        glued_filling_period(first, second) == first - second
        and glued_filling_period(second, first) == second - first,
    )
    ledger.mutation_sensitive(
        "extension phase independence is conditional on coefficient times period",
        lambda candidate: extension_phase_ratio(candidate, 2 * sp.pi, 0) == 1,
        sp.Integer(1),
        [sp.Rational(1, 2), sp.sqrt(2)],
    )
    ledger.check(
        "ungauged boundary variation is not promoted as physical anomaly inflow",
        audit["ungauged_variation"]["physical_inflow_established"] is False
        and audit["ungauged_variation"]["missing_objects"]
        == ["gauge_connection", "anomaly_polynomial", "gauge_descent", "physical_current_map"],
    )
    ledger.check(
        "the independent exact review has a clean sensitive tally",
        independent["process_exit_code"] == 0
        and independent["terminal_tally"]
        == "ALL 26 CHECKS PASS [P056-INDEPENDENT]",
    )
    source_entry = next(
        entry for entry in queue["units"] if entry["source_unit"] == "WZ1"
    )
    claim_entry = next(
        entry for entry in claims["claims"] if entry["id"] == "C-WZW-001"
    )
    ledger.check(
        "the promoted claim has reviewed axes and minimal accepted dependency closure",
        claim_entry["verification"] == "symbolic_verified"
        and claim_entry["review"] == "accepted"
        and claim_entry["compatibility"] == "compatible_extension"
        and claim_entry["epistemic"] == "active"
        and claim_entry["dependencies"] == ["C-LIE-001"],
    )
    ledger.check(
        "the terminal WZ1 disposition maps only the exact accepted theorem",
        source_entry["disposition"] == "qualified"
        and source_entry["accepted_claims"] == ["C-WZW-001"],
    )
    pending_related = {
        entry["source_unit"]: entry["disposition"]
        for entry in queue["units"]
        if entry["source_unit"] in {"S3", "S4", "WZ2", "WZ3"}
    }
    ledger.check(
        "pending navigation units remain nonauthoritative",
        pending_related
        == {
            "S3": "pending_adjudication",
            "S4": "pending_adjudication",
            "WZ2": "pending_adjudication",
            "WZ3": "pending_adjudication",
        },
    )
    ledger.check(
        "the current release pins the exact claim and no unreviewed WZ claim",
        release["release"] == "v0.50.0"
        and "C-WZW-001" in release["accepted_claims"]
        and not any(
            claim.startswith("C-WZW-") and claim != "C-WZW-001"
            for claim in release["accepted_claims"]
        ),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
