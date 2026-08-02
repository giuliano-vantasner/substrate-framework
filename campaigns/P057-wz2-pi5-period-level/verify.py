"""Primary exact verifier for P057's SU(3) sphere-period theorem."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger
from substrate_framework.wzw import (
    alternating_trace,
    sphere_extension_coefficient,
    sphere_extension_phase_ratio,
    su3_pi5_generator,
    su3_pi5_generator_differential,
    su3_pi5_period_evidence,
    su3_sphere_trace_five_period,
)


SOURCE_SHA256 = "f991e222f038268077d3f50e759beeec95ac65f06a8369011ecc0e0ad79ce3ff"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    parser.add_argument("--source-audit", type=Path, required=True)
    parser.add_argument("--topology-provenance", type=Path, required=True)
    parser.add_argument("--independent-result", type=Path, required=True)
    parser.add_argument("--migration-queue", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    parser.add_argument("--release", type=Path, required=True)
    arguments = parser.parse_args()

    source = arguments.source_file.read_text(encoding="utf-8")
    reproduction = load_yaml(arguments.source_reproduction)
    audit = load_yaml(arguments.source_audit)
    provenance = load_yaml(arguments.topology_provenance)
    independent = load_yaml(arguments.independent_result)
    queue = load_yaml(arguments.migration_queue)
    claims = load_yaml(arguments.claims)
    release = load_yaml(arguments.release)
    ledger = CheckLedger("P057-WZ2")

    ledger.check(
        "WZ2 is hash-pinned and its clean terminal tally is preserved",
        file_hash(arguments.source_file) == SOURCE_SHA256
        and reproduction["sha256"] == SOURCE_SHA256
        and reproduction["exit_code"] == 0
        and reproduction["terminal_tally"] == "ALL 8 CHECKS PASS",
    )
    ledger.check(
        "the source map is unitary but fails the SU3 determinant condition",
        "return EYE3 + (np.exp(1j * F)" in source
        and audit["map"]["exact_determinant"] == "exp(iF)"
        and audit["map"]["unitary"] is True
        and audit["map"]["special_unitary_for_generic_F"] is False,
    )
    ledger.check(
        "the claimed suspension domain is separated from S5",
        audit["domain"]["actual_reduced_homology"]["H3"] == "Z"
        and audit["domain"]["S5_reduced_H3"] == 0
        and audit["domain"]["smooth_manifold_at_suspension_poles"] is False,
    )
    ledger.check(
        "source rounding, doubling, and generator labels are not promoted as oracles",
        "round(n)" in source
        and "F_integral = nwind * 3 * np.pi / 4" in source
        and audit["generator"]["independent_of_period_under_review"] is False
        and audit["doubling"]["recomputes_doubled_map"] is False,
    )

    z1, z2, z3, w1, w2, w3 = sp.symbols("z1 z2 z3 w1 w2 w3")
    eta = su3_pi5_generator((z1, z2, z3)).xreplace(
        {sp.conjugate(z1): w1, sp.conjugate(z2): w2, sp.conjugate(z3): w3}
    )
    eta_adjoint = eta.T.xreplace(
        {z1: w1, z2: w2, z3: w3, w1: z1, w2: z2, w3: z3}
    )
    norm_squared = w1 * z1 + w2 * z2 + w3 * z3
    gram_residual = sp.expand(eta_adjoint * eta - sp.eye(3))
    expected_residual = sp.expand(
        (norm_squared - 1)
        * (sp.eye(3) + sp.Matrix([w1, w2, w3]) * sp.Matrix([z1, z2, z3]).T)
    )
    ledger.check(
        "the replacement map has exact determinant one and unitarity on S5",
        sp.factor(eta.det()) == norm_squared**2
        and gram_residual == expected_residual,
    )

    evidence = su3_pi5_period_evidence()
    ledger.check(
        "two independently oriented regular preimages derive projection degree plus two",
        evidence.positive_preimage_jacobian == 8
        and evidence.negative_preimage_jacobian == 8
        and evidence.projection_degree == 2,
    )
    primary = provenance["sources"][0]
    ledger.check(
        "the generator criterion is a precise primary-source import",
        primary["doi"] == "10.1007/s00014-003-0770-0"
        and 653 in primary["audited_pages"]
        and any("Theorem 2.1" in item for item in primary["imported_statements"]),
    )

    ledger.check(
        "the exact oriented tangent density derives the primitive period",
        evidence.raw_trace_density == -480 * sp.I
        and evidence.real_trace_density == -480
        and evidence.sphere_volume == sp.pi**3
        and evidence.raw_trace_period == -480 * sp.I * sp.pi**3
        and evidence.real_trace_period == -480 * sp.pi**3,
    )
    ledger.mutation_sensitive(
        "the unnormalized alternating convention detects tangent rescaling",
        lambda scale: sp.simplify(
            alternating_trace(
                tuple(
                    su3_pi5_generator((1, 0, 0)).H
                    * su3_pi5_generator_differential((1, 0, 0), tangent)
                    for tangent in (
                        (scale * sp.I, 0, 0),
                        (0, 1, 0),
                        (0, sp.I, 0),
                        (0, 0, 1),
                        (0, 0, sp.I),
                    )
                )
            )
            + 480 * sp.I
        )
        == 0,
        sp.Integer(1),
        [sp.Integer(2), sp.Integer(-1), sp.Rational(1, 120)],
    )
    ledger.check(
        "orientation reversal and multiple winding change the period correctly",
        su3_sphere_trace_five_period(-1) == 480 * sp.pi**3
        and su3_sphere_trace_five_period(2) == -960 * sp.pi**3,
    )

    level = sp.Symbol("level", integer=True)
    winding = sp.Symbol("winding", integer=True)
    ledger.check(
        "the exact sphere-extension coefficient lattice is derived from the period",
        evidence.coefficient_lattice_step == 1 / (240 * sp.pi**2)
        and sphere_extension_coefficient(level) == level / (240 * sp.pi**2)
        and sphere_extension_phase_ratio(level, winding) == 1,
    )
    ledger.mutation_sensitive(
        "noninteger level mutations fail on the primitive sphere",
        lambda candidate: sphere_extension_phase_ratio(candidate, 1) == 1,
        sp.Integer(1),
        [sp.Rational(1, 2), sp.Rational(3, 2), sp.sqrt(2)],
    )
    ledger.check(
        "the independent finite-difference and five-dimensional cubature review passed",
        independent["process_exit_code"] == 0
        and independent["terminal_tally"] == "ALL 9 CHECKS PASS [P057-INDEPENDENT]"
        and independent["cubature"]["relative_errors"][-1] < 6e-4,
    )
    ledger.check(
        "the external matching normalization remained a blinded comparator",
        provenance["sources"][2]["role"] == "independent_comparator_only"
        and provenance["sources"][2]["statements_not_used_as_derivation_inputs"],
    )

    source_entry = next(
        entry for entry in queue["units"] if entry["source_unit"] == "WZ2"
    )
    claim_entry = next(
        entry for entry in claims["claims"] if entry["id"] == "C-WZW-002"
    )
    ledger.check(
        "the accepted claim has minimal dependency closure and four reviewed axes",
        claim_entry["verification"] == "symbolic_verified"
        and claim_entry["review"] == "accepted"
        and claim_entry["compatibility"] == "compatible_extension"
        and claim_entry["epistemic"] == "active"
        and claim_entry["dependencies"] == ["C-WZW-001"],
    )
    ledger.check(
        "WZ2 is qualified and maps only to the surviving mathematical theorem",
        source_entry["disposition"] == "qualified"
        and source_entry["accepted_claims"] == ["C-WZW-002"]
        and "not an SU(3) map" in source_entry["qualification"],
    )
    ledger.check(
        "the promoted theorem explicitly excludes unsupported physical scope",
        "arbitrary closed five-manifolds" in claim_entry["statement"]
        and "identify k with N_c" in claim_entry["statement"]
        and "gauge anomaly" in claim_entry["statement"]
        and "physical realization" in claim_entry["statement"],
    )
    ledger.check(
        "the campaign release pins both exact WZW claims",
        release["release"] == "v0.51.0"
        and release["accepted_claims"][-2:] == ["C-WZW-001", "C-WZW-002"],
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
