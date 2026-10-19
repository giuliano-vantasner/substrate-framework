"""Compare independently decoded native XML spectra with every raw q-star matrix."""

from pathlib import Path
import json
import xml.etree.ElementTree as ET
import numpy as np

from substrate_framework import material_modes as modes
from substrate_framework import material_force_lattice as lattice


def xml_numbers(node):
    return np.array([float(x.replace("D","E")) for x in node.text.split()])


def xml_force(node, nat):
    """Independent entrywise decode: Fortran Cartesian column index is outermost."""
    force = np.empty((nat,3,nat,3),dtype=complex)
    for i in range(nat):
        for j in range(nat):
            pairs = xml_numbers(node.find(f"PHI.{i+1}.{j+1}")).reshape(9,2)
            for b in range(3):
                for a in range(3):
                    force[i,a,j,b] = complex(*pairs[3*b+a])
    return force


def spectral_budget(matrix, reference_lambda):
    """Absolute eigenvalue budget for serialized float64 matrices and eigensolves.

    256*n*eps*||D||_2 is a conservative engineering roundoff allowance, not a
    certified LAPACK enclosure and not a physical/numerical-convergence error.
    Weyl propagation is absolute, including at zero and in degenerate clusters.
    """
    n = len(reference_lambda)
    scale = max(np.linalg.norm(matrix,2),np.max(np.abs(reference_lambda)))
    return float(256*n*np.finfo(float).eps*scale)


def frequency_budget(values, reference, lambda_budget):
    """Propagate signed-sqrt absolute errors, avoiding relative acoustic tests."""
    same_sign = values*reference > 0
    denominator = np.sqrt(np.abs(values)) + np.sqrt(np.abs(reference))
    budget = np.full(values.shape,np.sqrt(2*lambda_budget))
    budget[same_sign] = lambda_budget/denominator[same_sign]
    return budget*modes.RY_TO_THZ


def degeneracy_clusters(values, absolute_budget):
    clusters = [[0]]
    for index in range(1,len(values)):
        if values[index]-values[index-1] <= 2*absolute_budget:
            clusters[-1].append(index)
        else:
            clusters.append([index])
    return clusters


def native_pilot_block(ledger, result_path, native_directory):
    native_directory = Path(native_directory)
    envelope = json.loads(Path(result_path).read_text())
    ledger.check("native pilot published complete", envelope["status"] == "complete")
    data = envelope["data"]
    rows = []
    for record in data["dynamical_matrices"]:
        native = ET.parse(native_directory/Path(record["artifact"]).name).getroot()
        nat = record["geometry"]["number_of_atoms"]
        masses = modes.atom_masses_amu(record["geometry"])
        reported = np.sort([xml_numbers(native.find(f"FREQUENCIES_THZ_CMM1/OMEGA.{i+1}"))[0]
                            for i in range(3*nat)])
        reference_lambda = np.sign(reported)*(reported/modes.RY_TO_THZ)**2
        xml_stars = [node for node in native if node.tag.startswith("DYNAMICAL_MAT_.")]
        ledger.check(f"q{record['q_index']} complete XML star count", len(xml_stars) == len(record["q_star"]))
        for member_index,(member,node) in enumerate(zip(record["q_star"],xml_stars),start=1):
            label = f"q{record['q_index']}/star{member_index}"
            raw = xml_force(node,nat)
            ledger.check(f"{label} independent XML force ordering", np.array_equal(raw,modes.force_tensor(member["force_matrix_ry_per_bohr2"])))
            ledger.check(f"{label} independent XML q vector", np.array_equal(xml_numbers(node.find("Q_POINT")),member["q_cartesian_2pi_alat"]))
            operator = modes.mass_weighted_operator(raw,masses,units="qe_ry")
            raw_residual = modes.operator_residuals(operator,masses)
            # Explicitly reproduce only QE's named Hermitian step, never ASR.
            hermitian = modes.project_hermitian(operator)
            spectrum = modes.signed_modes(hermitian,units="qe_ry")
            bound = spectral_budget(hermitian,reference_lambda)
            frequency_bound = frequency_budget(spectrum.eigenvalues,reference_lambda,bound)
            frequency_bound += 32*np.finfo(float).eps*np.abs(reported)
            absolute_errors = np.abs(spectrum.frequency_thz-reported)
            ledger.check(f"{label} native signed squared spectrum", np.max(np.abs(spectrum.eigenvalues-reference_lambda)) <= bound)
            ledger.check(f"{label} absolute THz spectrum including acoustic residuals", np.all(absolute_errors <= frequency_bound))
            ledger.check(f"{label} eigensolver residual", spectrum.eigenpair_residual <= bound*np.sqrt(3*nat))
            ledger.check(f"{label} factor-two force-unit mutation exposed", np.max(np.abs(2*spectrum.eigenvalues-reference_lambda)) > bound)
            rows.append({"q_index":record["q_index"],"star_index":member_index,
                         "q_cartesian_2pi_alat":member["q_cartesian_2pi_alat"],
                         "matrix_derived_signed_thz":spectrum.frequency_thz.tolist(),
                         "native_xml_signed_thz":reported.tolist(),
                         "absolute_error_thz":absolute_errors.tolist(),
                         "absolute_budget_thz":frequency_bound.tolist(),
                         "absolute_eigenvalue_budget_qe":bound,
                         "degenerate_index_clusters":degeneracy_clusters(reference_lambda,bound),
                         "raw_residuals_qe_units":raw_residual,
                         "explicit_hermitian_change_frobenius":float(np.linalg.norm(hermitian-operator)),
                         "eigenpair_residual_qe":spectrum.eigenpair_residual,
                         "orthogonality_residual":spectrum.orthogonality_residual})
    grid = lattice.complete_native_q_grid(data["dynamical_matrices"],data["q_manifest"]["grid"],grid_atol=1e-12)
    force_r = lattice.q_grid_to_force_lattice(grid)
    reconstruction = float(np.linalg.norm(lattice.force_lattice_to_q_grid(force_r)-grid))
    bound = 256*np.finfo(float).eps*np.linalg.norm(grid)
    ledger.check("raw pilot complete-grid transform reconstruction", reconstruction <= bound)
    return {"all_q_star_spectra":rows,"q_count":int(np.prod(grid.shape[:3])),
            "raw_lattice_residuals_ry_per_bohr2":lattice.lattice_residuals(force_r),
            "raw_grid_reconstruction_error":reconstruction,
            "native_frequency_scope":"Each XML contains one representative spectrum; compare every symmetry-related star member as a signed eigenvalue multiset, not as separately reported native modes.",
            "degeneracy_scope":"Sorted spectra and absolute-budget clusters; no individual eigenvector comparison inside degenerate subspaces.",
            "physical_scope":"Unconverged Ni1 native engineering/unit fixture only. Gamma acoustic residuals remain raw, with no ASR, zero assignment, stability or material interpretation."}
