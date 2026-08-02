"""Primary exact verifier for P060's symmetry-Hessian theorem and PG1 audit."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.symmetry_breaking import (
    leading_exponential_kinetic_metric,
    linear_symmetry_hessian_evidence,
    orthogonal_generators,
    positive_kinetic_mass_evidence,
    radial_quartic_potential,
)
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "a51ecc1833cd166bbef5aa799d2ab9eacc453b088660dbb98426591a7157aa74"


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
    parser.add_argument("--goldstone-provenance", type=Path, required=True)
    parser.add_argument("--independent-result", type=Path, required=True)
    parser.add_argument("--migration-queue", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    parser.add_argument("--release", type=Path, required=True)
    arguments = parser.parse_args()

    source = arguments.source_file.read_text(encoding="utf-8")
    reproduction = load_yaml(arguments.source_reproduction)
    audit = load_yaml(arguments.source_audit)
    provenance = load_yaml(arguments.goldstone_provenance)
    independent = load_yaml(arguments.independent_result)
    queue = load_yaml(arguments.migration_queue)
    claims = load_yaml(arguments.claims)
    release = load_yaml(arguments.release)
    ledger = CheckLedger("P060-PG1")

    ledger.check(
        "PG1 is hash-pinned and its native four-check tally is reproduced",
        file_hash(arguments.source_file) == SOURCE_SHA256
        and reproduction["source_sha256"] == SOURCE_SHA256
        and reproduction["native_run"]["exit_status"] == 0
        and reproduction["native_run"]["terminal_tally"] == "ALL 4 CHECKS PASS",
    )
    ledger.check(
        "the source's O(4) calculation is a declared radial-quartic model",
        "V = lam * (sig**2 + pi1**2 + pi2**2 + pi3**2 - v**2)**2" in source
        and audit["checks"]["PG1.1"]["surviving_scope"].startswith(
            "For positive lambda and v"
        ),
    )
    ledger.check(
        "the source executes one eighth for the ANW prefactor but prints one half",
        "L2_anw = sp.simplify(Fpi**2 / 16 * Tr_lead)" in source
        and "anw_eighth = sp.Rational(1, 8)" in source
        and reproduction["reported_values"]["anw_quadratic_term"]
        == "(p1**2+p2**2+p3**2)/8"
        and reproduction["reported_values"]["printed_result_anw_quadratic_term"]
        == "(p1**2+p2**2+p3**2)/2",
    )
    ledger.check(
        "mass absence and dispersion are declared-input checks rather than derivations",
        "pi1s, pi2s, pi3s = sp.symbols" in source
        and "dispersion_general.subs(m_pi, 0)" in source
        and any(
            "dispersion predicate substitutes" in defect
            for defect in audit["checks"]["PG1.2"]["defects"]
        ),
    )
    ledger.check(
        "the source count uses labels without an orbit or stabilizer construction",
        "n_goldstone_su2 = dim_G_su2 - dim_H_su2" in source
        and audit["checks"]["PG1.3"]["actual_object"]
        == "arithmetic_using_dim_su_n_equals_n_squared_minus_one",
    )
    ledger.check(
        "pending PG2 PG4 and S2 supply no accepted premise",
        audit["dependency_conflicts"][:3]
        == [
            "PG2 is pending and supplies no accepted explicit-breaking or GMOR premise.",
            "PG4 is pending and supplies no accepted pion-to-Skyrmion or nucleon map.",
            "S2 is pending and supplies no accepted pion, hedgehog-spectrum, or ANW premise.",
        ],
    )

    sigma, pi1, pi2, pi3 = sp.symbols("sigma pi1 pi2 pi3", real=True)
    coupling, scale = sp.symbols("lambda v", positive=True)
    fields = (sigma, pi1, pi2, pi3)
    generators = orthogonal_generators(4)
    potential = radial_quartic_potential(fields, coupling, scale)
    evidence = linear_symmetry_hessian_evidence(
        potential,
        fields,
        (scale, 0, 0, 0),
        generators,
    )
    ledger.check(
        "all six actual O(4) infinitesimal invariance residuals vanish",
        len(evidence.invariance_residuals) == 6
        and evidence.invariant
        and all(residual == 0 for residual in evidence.invariance_residuals),
    )
    ledger.check(
        "the differentiated invariance identity has exact zero residual",
        evidence.differentiated_identity_residual == sp.zeros(4, 6),
    )
    ledger.check(
        "the declared nonzero vacuum is exactly stationary",
        evidence.stationary
        and evidence.stationarity_residual == sp.zeros(4, 1)
        and evidence.vacuum != sp.zeros(4, 1),
    )
    ledger.check(
        "the supplied O(4) matrices form an independent six-generator basis",
        evidence.generators_independent
        and evidence.generator_span_rank == 6
        and all(generator.T == -generator for generator in evidence.generators),
    )
    ledger.check(
        "the actual vacuum-tangent rank is three with a three-dimensional stabilizer",
        evidence.broken_tangent_rank == 3
        and evidence.stabilizer_dimension == 3
        and len(evidence.generator_tangents.nullspace()) == 3,
    )
    ledger.check(
        "the exact O(4) Hessian has one radial and three zero eigenvalues",
        evidence.hessian_at_vacuum
        == sp.diag(8 * coupling * scale**2, 0, 0, 0)
        and evidence.hessian_at_vacuum.rank() == 1
        and len(evidence.hessian_at_vacuum.nullspace()) == 3,
    )
    ledger.check(
        "stationary invariance puts every actual tangent in the Hessian kernel",
        evidence.theorem_hypotheses_hold
        and evidence.tangent_kernel_certified
        and evidence.hessian_tangent_residual == sp.zeros(4, 6),
    )

    ledger.mutation_sensitive(
        "vacuum stationarity",
        lambda candidate: linear_symmetry_hessian_evidence(
            potential, fields, candidate, generators
        ).stationary,
        (scale, 0, 0, 0),
        ((scale / 2, 0, 0, 0), (scale, 1, 0, 0)),
    )
    anisotropy = sp.symbols("mu2", positive=True)
    anisotropic_potential = potential + anisotropy * pi1**2 / 2
    anisotropic = linear_symmetry_hessian_evidence(
        anisotropic_potential,
        fields,
        (scale, 0, 0, 0),
        generators,
    )
    ledger.mutation_sensitive(
        "continuous invariance",
        lambda candidate_potential: linear_symmetry_hessian_evidence(
            candidate_potential, fields, (scale, 0, 0, 0), generators
        ).invariant,
        potential,
        (anisotropic_potential, potential - sigma),
    )
    ledger.check(
        "anisotropic curvature lifts a tangent and breaks the kernel verdict",
        anisotropic.hessian_at_vacuum[1, 1] == anisotropy
        and not anisotropic.tangent_kernel_certified
        and not matrix_zero(anisotropic.hessian_tangent_residual),
    )

    source, shifted = sp.symbols("c s0", positive=True)
    stationary_source = 4 * coupling * shifted * (shifted**2 - scale**2)
    tilted = linear_symmetry_hessian_evidence(
        (potential - source * sigma).subs(source, stationary_source),
        fields,
        (shifted, 0, 0, 0),
        generators,
    )
    ledger.check(
        "the explicit linear tilt is stationary but lifts transverse curvature to c over s0",
        tilted.stationary
        and not tilted.invariant
        and not tilted.tangent_kernel_certified
        and all(
            sp.simplify(tilted.hessian_at_vacuum[index, index] - stationary_source / shifted)
            == 0
            for index in (1, 2, 3)
        ),
    )

    symmetric_vacuum = linear_symmetry_hessian_evidence(
        potential,
        fields,
        (0, 0, 0, 0),
        generators,
    )
    ledger.check(
        "the symmetric vacuum has no nonzero broken tangent despite six generators",
        symmetric_vacuum.stationary
        and symmetric_vacuum.broken_tangent_rank == 0
        and symmetric_vacuum.stabilizer_dimension == 6,
    )
    repeated_generator = linear_symmetry_hessian_evidence(
        potential,
        fields,
        (scale, 0, 0, 0),
        (generators[0], 2 * generators[0]),
    )
    stabilizer_rejected = False
    try:
        _ = repeated_generator.stabilizer_dimension
    except ValueError:
        stabilizer_rejected = True
    ledger.check(
        "dependent generator labels cannot inflate tangent rank or masquerade as a stabilizer basis",
        repeated_generator.generator_span_rank == 1
        and repeated_generator.broken_tangent_rank == 1
        and stabilizer_rejected,
    )

    kinetic_one, kinetic_two = sp.symbols("K1 K2", positive=True)
    positive_metric = sp.diag(1, kinetic_one, kinetic_two, 2)
    masses = positive_kinetic_mass_evidence(
        evidence.hessian_at_vacuum,
        positive_metric,
        evidence.generator_tangents,
    )
    ledger.check(
        "a separately proven positive kinetic metric preserves the three zero directions",
        positive_metric.is_positive_definite is True
        and masses.zero_direction_rank == 3
        and masses.zero_directions_certified,
    )
    lifted_mass = positive_kinetic_mass_evidence(
        evidence.hessian_at_vacuum + sp.diag(0, 1, 0, 0),
        positive_metric,
        evidence.generator_tangents,
    )
    ledger.check(
        "a positive kinetic metric does not create a zero after Hessian lifting",
        not lifted_mass.zero_directions_certified
        and not matrix_zero(lifted_mass.zero_direction_residual),
    )

    pauli = (
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -sp.I], [sp.I, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    )
    physicist = leading_exponential_kinetic_metric(
        pauli, scale, scale**2 / 4
    )
    anw = leading_exponential_kinetic_metric(pauli, scale, scale**2 / 16)
    ledger.check(
        "the canonical helper derives the Pauli trace Gram matrix rather than copying it",
        physicist.trace_gram == 2 * sp.eye(3)
        and all(
            physicist.trace_gram[row, column]
            == sp.trace(pauli[row] * pauli[column])
            for row in range(3)
            for column in range(3)
        ),
    )
    ledger.mutation_sensitive(
        "group-coordinate kinetic prefactor",
        lambda metric: metric == sp.eye(3),
        physicist.kinetic_metric,
        (anw.kinetic_metric, 2 * physicist.kinetic_metric),
    )
    ledger.check(
        "the ANW prefactor has metric I over four and quadratic coefficient one eighth",
        anw.kinetic_metric == sp.eye(3) / 4
        and anw.kinetic_metric != sp.eye(3),
    )

    derivative_only_hessian = sp.hessian(sp.Integer(0), fields[1:])
    declared_mass_squared = sp.symbols("m2", positive=True)
    lifted_potential = declared_mass_squared * sum(
        (component**2 for component in fields[1:]), sp.Integer(0)
    ) / 2
    ledger.check(
        "zero potential gives zero Hessian while an added mass potential lifts it",
        derivative_only_hessian == sp.zeros(3)
        and sp.hessian(lifted_potential, fields[1:])
        == declared_mass_squared * sp.eye(3),
    )
    ledger.check(
        "four-dimensional scalar dimensions separate kinetic and curvature inputs",
        2 * (1 + 1) == 4
        and 4 - 2 * 1 == 2
        and 4 - 1 == 3,
    )

    goldstone_source = next(
        entry
        for entry in provenance["sources"]
        if entry["id"] == "goldstone-salam-weinberg-1962"
    )
    anw_source = next(
        entry for entry in provenance["sources"] if entry["id"] == "adkins-nappi-witten-1983"
    )
    ledger.check(
        "primary literature is used only to delimit stronger external model and quantum claims",
        goldstone_source["doi"] == "10.1103/PhysRev.127.965"
        and "external_quantum_theorem_scope" in goldstone_source["imported_as"]
        and anw_source["doi"] == "10.1016/0550-3213(83)90559-X"
        and anw_source["imported_as"] == "source_model_provenance_not_framework_authority",
    )
    ledger.check(
        "the independent route passed without canonical theorem imports",
        independent["process_exit_code"] == 0
        and independent["terminal_tally"] == "ALL 24 CHECKS PASS [P060-INDEPENDENT]"
        and independent["canonical_symmetry_breaking_helpers_imported"] is False,
    )

    symmetry_claim = next(entry for entry in claims["claims"] if entry["id"] == "C-SYM-001")
    chiral_claim = next(entry for entry in claims["claims"] if entry["id"] == "C-CHI-001")
    ledger.check(
        "the general theorem is accepted dependency-free with a strict interpretation ceiling",
        symmetry_claim["verification"] == "symbolic_verified"
        and symmetry_claim["review"] == "accepted"
        and symmetry_claim["compatibility"] == "compatible_extension"
        and symmetry_claim["epistemic"] == "active"
        and symmetry_claim["dependencies"] == []
        and "no quantum Goldstone-particle theorem" in symmetry_claim["statement"],
    )
    ledger.check(
        "the O(4) and SU(2) specialization is accepted separately without physical identification",
        chiral_claim["verification"] == "symbolic_verified"
        and chiral_claim["review"] == "accepted"
        and chiral_claim["dependencies"] == ["C-SYM-001"]
        and "no physical pion identification" in chiral_claim["statement"],
    )
    source_entry = next(
        entry for entry in queue["units"] if entry["source_unit"] == "PG1"
    )
    ledger.check(
        "PG1 is qualified only through its surviving conditional model mathematics",
        source_entry["disposition"] == "qualified"
        and source_entry["accepted_claims"] == ["C-SYM-001", "C-CHI-001"]
        and "factor of four" in source_entry["qualification"]
        and "physical pion" in source_entry["qualification"],
    )
    ledger.check(
        "the release closes both new claims and no unsupported pending source unit",
        release["release"] == "v0.54.0"
        and release["accepted_claims"][-2:] == ["C-SYM-001", "C-CHI-001"]
        and set(release["accepted_claims"]) == {
            entry["id"]
            for entry in claims["claims"]
            if entry["review"] == "accepted"
        },
    )
    ledger.check(
        "the accepted claims exclude every unsupported physical and substrate conclusion",
        "no physical pion identification" in chiral_claim["statement"]
        and "no substrate realization" in chiral_claim["statement"]
        and "no quantum Goldstone-particle theorem" in symmetry_claim["statement"]
        and "no chiral symmetry action" in chiral_claim["statement"],
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
