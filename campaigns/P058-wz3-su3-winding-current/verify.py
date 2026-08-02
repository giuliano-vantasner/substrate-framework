"""Primary exact verifier for P058's SU(3) winding-current theorem."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger
from substrate_framework.wzw import (
    chevalley_eilenberg_differential,
    cochain_basis,
    hedgehog_winding_charge,
    hedgehog_winding_density,
    hedgehog_winding_radial_density,
    maurer_cartan_power_derivative_multiplier,
    su2_quaternion_embedding,
    su2_quaternion_embedding_differential,
    su2_quaternion_trace_three_period,
    su3_trace_power_cochain,
    su3_winding_current,
    su3_winding_current_coefficient,
    su3_winding_three_evidence,
    trace_power_cyclic_shift_sign,
    trace_power_derivative_multiplier,
)


SOURCE_SHA256 = "30da2ac41a0d46c48bd4e1b9733c3712d0b6c1c9b4838f1a1df3c4db22cc3569"


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
    ledger = CheckLedger("P058-WZ3")

    ledger.check(
        "WZ3 is hash-pinned and its version-specific native failure is preserved",
        file_hash(arguments.source_file) == SOURCE_SHA256
        and reproduction["sha256"] == SOURCE_SHA256
        and reproduction["native_run"]["exit_code"] == 1
        and reproduction["native_run"]["terminal_tally"] is None
        and "no attribute trapz" in reproduction["native_run"]["failure"],
    )
    ledger.check(
        "the immutable source reaches its tally only through the explicit current-API shim",
        "np.trapz" in source
        and reproduction["compatibility_replay"]["shim"] == "np.trapz=np.trapezoid"
        and reproduction["compatibility_replay"]["source_file_modified"] is False
        and reproduction["compatibility_replay"]["exit_code"] == 0
        and reproduction["compatibility_replay"]["terminal_tally"]
        == "ALL 7 CHECKS PASS",
    )
    ledger.check(
        "the source flips its derived trace orientation only in the numerical integrand",
        "NUMERIC_SIGN = -ORIENT" in source
        and audit["current_convention"]["exact_trace_radial_integrand"]
        == "+(2/pi)*sin(F)^2*Fprime"
        and audit["current_convention"]["charge_for_F_pi_to_zero_under_headline_sign"]
        == -1
        and audit["current_convention"]["numerical_charge_for_F_pi_to_zero"] == 1,
    )
    ledger.check(
        "the source linkage and anomaly checks are structural stand-ins rather than derivations",
        "pi3_baryon = round(B_unit)" in source
        and "n_value = 3" in source
        and audit["degree_and_baryon_link"]["gauged_WZW_functional_constructed"] is False
        and audit["degree_and_baryon_link"]["local_U1_variation_computed"] is False
        and audit["anomaly_and_color"]["measured_width_loaded_or_compared"] is False
        and audit["anomaly_and_color"]["equality_of_level_and_Nc_derived"] is False,
    )

    a0, a1, a2, a3 = sp.symbols("a0 a1 a2 a3", real=True)
    norm_squared = a0**2 + a1**2 + a2**2 + a3**2
    quaternion = su2_quaternion_embedding((a0, a1, a2, a3))
    ledger.check(
        "the quaternion block has exact SU3 membership on the unit sphere",
        sp.factor(quaternion.det()) == norm_squared
        and sp.simplify(quaternion.H * quaternion)
        == sp.diag(norm_squared, norm_squared, 1),
    )
    first_column = quaternion[:, 0]
    projected = sp.Matrix(
        [
            sp.re(first_column[0]),
            sp.im(first_column[0]),
            sp.re(first_column[1]),
            sp.im(first_column[1]),
        ]
    )
    ledger.check(
        "the generator witness is independent of the trace integral",
        projected.jacobian((a0, a1, a2, a3)).det() == 1
        and su3_winding_three_evidence().column_projection_jacobian == 1
        and su3_winding_three_evidence().column_projection_degree == 1,
    )
    topology_source = provenance["sources"][0]
    ledger.check(
        "the degree-one generator criterion is a precise primary-source import",
        topology_source["doi"] == "10.1007/s00014-003-0770-0"
        and 652 in topology_source["audited_pages"]
        and "n=2" in topology_source["imported_statement"],
    )

    d2 = chevalley_eilenberg_differential(2)
    d3 = chevalley_eilenberg_differential(3)
    trace_three = su3_trace_power_cochain(3)
    evidence = su3_winding_three_evidence()
    ledger.check(
        "the exact CE complex derives one-dimensional third cohomology",
        d3 * d2 == sp.zeros(70, 28)
        and evidence.d2_rank == 20
        and evidence.d3_rank == 35
        and evidence.three_cocycle_dimension == 21
        and evidence.third_cohomology_dimension == 1,
    )
    ledger.check(
        "the actual trace-three cochain is closed and nonexact",
        d3 * trace_three == sp.zeros(70, 1)
        and evidence.trace_nonzero_components == 9
        and evidence.trace_norm_squared == 9
        and evidence.augmented_d2_trace_rank == 21
        and evidence.trace_is_closed
        and not evidence.trace_is_exact,
    )
    ledger.check(
        "the full graded derivative and cyclic-even kernel imply off-shell closure",
        trace_power_derivative_multiplier(3) == 3
        and maurer_cartan_power_derivative_multiplier(3) == -1
        and trace_power_cyclic_shift_sign(4) == -1
        and su3_trace_power_cochain(4) == sp.zeros(len(cochain_basis(4)), 1),
    )

    ledger.check(
        "the explicit oriented generator derives the normalization without a copied unit charge",
        evidence.raw_generator_density == 12
        and evidence.sphere_volume == 2 * sp.pi**2
        and evidence.raw_generator_period == 24 * sp.pi**2
        and su2_quaternion_trace_three_period() == 24 * sp.pi**2
        and evidence.current_coefficient == -1 / (24 * sp.pi**2)
        and su3_winding_current_coefficient() == -1 / (24 * sp.pi**2)
        and evidence.normalized_generator_period == -1,
    )
    zero = sp.zeros(3)
    spatial = tuple(
        su2_quaternion_embedding_differential(tangent)
        for tangent in ((0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    )
    positive_orientation = su3_winding_current((zero, *spatial))
    negative_orientation = su3_winding_current((zero, *spatial), orientation=-1)
    ledger.check(
        "orientation reverses charge but does not masquerade as a conservation mutation",
        positive_orientation == (-1 / (2 * sp.pi**2), 0, 0, 0)
        and negative_orientation == tuple(-value for value in positive_orientation),
    )

    radius = sp.symbols("r", positive=True)
    profile = sp.Function("F", real=True)(radius)
    local_density = hedgehog_winding_density(profile, radius)
    radial_density = hedgehog_winding_radial_density(profile, radius)
    expected_local = -sp.sin(profile) ** 2 * sp.diff(profile, radius) / (
        2 * sp.pi**2 * radius**2
    )
    ledger.check(
        "the canonical hedgehog local and radial densities retain the fixed sign",
        local_density == expected_local
        and radial_density
        == -2 * sp.sin(profile) ** 2 * sp.diff(profile, radius) / sp.pi,
    )
    endpoint = sp.symbols("f", real=True)
    primitive = (endpoint - sp.sin(endpoint) * sp.cos(endpoint)) / sp.pi
    winding = sp.symbols("n", integer=True)
    ledger.check(
        "the charge is an exact boundary functional and integer on winding endpoints",
        sp.simplify(sp.diff(primitive, endpoint) - 2 * sp.sin(endpoint) ** 2 / sp.pi)
        == 0
        and hedgehog_winding_charge(winding * sp.pi, 0) == winding
        and hedgehog_winding_charge(sp.pi, 0) == 1
        and hedgehog_winding_charge(2 * sp.pi, 0) == 2
        and hedgehog_winding_charge(0, 0) == 0,
    )
    ledger.mutation_sensitive(
        "endpoint and orientation mutations cannot retain the unit charge",
        lambda inner: hedgehog_winding_charge(inner, 0) == 1,
        sp.pi,
        [sp.Integer(0), sp.pi / 2, 2 * sp.pi, -sp.pi],
    )

    ledger.check(
        "the independent exact and current-API regression review passed",
        independent["process_exit_code"] == 0
        and independent["terminal_tally"] == "ALL 10 CHECKS PASS [P058-INDEPENDENT]"
        and independent["numeric_regression"]["api"] == "numpy.trapezoid"
        and independent["numeric_regression"]["absolute_errors"][-1] < 5.0e-7,
    )
    color_count = sp.symbols("N_c", positive=True)
    consistent_up = (1 + 1 / color_count) / 2
    consistent_down = (1 / color_count - 1) / 2
    fixed_charge_expression = color_count * (
        sp.Rational(2, 3) ** 2 - sp.Rational(-1, 3) ** 2
    )
    ledger.check(
        "anomaly-consistent charge dependence defeats the source color-count oracle",
        sp.simplify(color_count * (consistent_up**2 - consistent_down**2)) == 1
        and sp.simplify(fixed_charge_expression) == color_count / 3
        and sp.solve(sp.Eq(fixed_charge_expression, 1), color_count) == [3]
        and provenance["sources"][3]["arxiv"] == "hep-ph/0105258",
    )

    source_entry = next(
        entry for entry in queue["units"] if entry["source_unit"] == "WZ3"
    )
    claim_entry = next(
        entry for entry in claims["claims"] if entry["id"] == "C-TOP-002"
    )
    ledger.check(
        "the accepted claim has minimal dependency closure and four reviewed axes",
        claim_entry["verification"] == "symbolic_verified"
        and claim_entry["review"] == "accepted"
        and claim_entry["compatibility"] == "compatible_extension"
        and claim_entry["epistemic"] == "active"
        and claim_entry["dependencies"] == ["C-LIE-001"],
    )
    ledger.check(
        "WZ3 is qualified and maps only to the surviving mathematical theorem",
        source_entry["disposition"] == "qualified"
        and source_entry["accepted_claims"] == ["C-TOP-002"]
        and "sign" in source_entry["qualification"]
        and "n=N_c=3" in source_entry["qualification"],
    )
    ledger.check(
        "the promoted theorem explicitly excludes unsupported physical scope",
        "not by itself a Noether" in claim_entry["statement"]
        and "gauged-WZW-response" in claim_entry["statement"]
        and "physical baryon" in claim_entry["statement"]
        and "N_c" in claim_entry["statement"]
        and "substrate realization" in claim_entry["statement"],
    )
    ledger.check(
        "the campaign release pins the new topological claim after both WZW claims",
        release["release"] == "v0.52.0"
        and release["accepted_claims"][-3:]
        == ["C-WZW-001", "C-WZW-002", "C-TOP-002"],
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
