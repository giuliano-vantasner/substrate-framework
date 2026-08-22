"""C-ELS-006 verifier: non-affine correction and rigidity threshold.

Claims (numeric evidence, float64, threads pinned):
- the isostatic-counted nearest-neighbour cubic network (z = 6) has exactly
  zero shear modulus and no transverse acoustic branch: Maxwell counting is
  necessary, not sufficient;
- every centrosymmetric Bravais network here has zero non-affine
  correction, so the relaxed modulus equals the affine modulus exactly;
- the static second-variation route and the Bloch phonon route agree to
  1e-8 relative on the isotropic (four-diagonal) network;
- mutations: halving the stiffness halves the modulus; a sign-flipped
  stiffness produces a Hessian with a negative eigenvalue (detected).
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import sys

import numpy as np

from substrate_framework import CheckLedger
from substrate_framework.nonaffine_networks import (
    CentralForceNetwork,
    acoustic_speed_squared,
    bloch_matrix,
    extrapolated_acoustic_speed_squared,
    threshold_record,
)


def check_threshold_structure(ledger: CheckLedger) -> None:
    records = threshold_record(n=4, max_families=4)
    floppy = records[0]
    ledger.check(
        "f=0 network (z=6): relaxed modulus exactly zero",
        floppy["modulus"] == 0.0 and floppy["mu_affine"] == 0.0,
    )
    floppy_sound = acoustic_speed_squared(CentralForceNetwork(4, 0))
    ledger.check(
        "f=0 network: no propagating transverse branch (soft modes)",
        not floppy_sound["transverse_branch_found"]
        or floppy_sound["c_squared_finite_q"] == 0.0,
    )
    moduli = [record["modulus"] for record in records]
    ledger.check(
        "relaxed modulus strictly increases with connectivity above threshold",
        all(b > a for a, b in zip(moduli, moduli[1:])),
    )
    counted = CentralForceNetwork(3, diagonal_families=0)
    ledger.check(
        "Maxwell count z=6 satisfied while mu = 0: necessary, not sufficient",
        counted.mean_coordination == 6.0
        and counted.affine_shear_modulus() == 0.0,
    )

def check_centrosymmetric_exactness(ledger: CheckLedger) -> None:
    net = CentralForceNetwork(4, diagonal_families=4)
    relaxed = net.relaxed_shear_modulus()
    ledger.check(
        "centrosymmetric Bravais network: non-affine correction vanishes",
        abs(relaxed["nonaffine_correction"]) < 1e-20,
    )
    ledger.check(
        "relaxed == affine == 4/3 for the isotropic network",
        abs(relaxed["modulus"] - 4.0 / 3.0) < 1e-12,
    )


def check_two_route_agreement(ledger: CheckLedger) -> None:
    extrapolated = extrapolated_acoustic_speed_squared(4)
    ledger.check(
        "static and phonon routes agree to 1e-8 (isotropic network)",
        abs(extrapolated["c_squared_continuum"] - 4.0 / 3.0) < 1e-8,
    )
    matrix = bloch_matrix(CentralForceNetwork(4, 4), np.array([0.1, 0.0, 0.0]))
    ledger.check(
        "Bloch matrix is symmetric positive semidefinite at small q",
        np.allclose(matrix, matrix.T, atol=1e-14)
        and float(np.linalg.eigvalsh(matrix).min()) >= -1e-14,
    )


def check_mutations(ledger: CheckLedger) -> None:
    net = CentralForceNetwork(4, diagonal_families=4)
    doubled = CentralForceNetwork(4, diagonal_families=4, stiffness=2.0)
    ledger.check(
        "mutation: doubled stiffness doubles the modulus (linear springs)",
        abs(doubled.affine_shear_modulus() - 2.0 * net.affine_shear_modulus())
        < 1e-12,
    )
    unstable = CentralForceNetwork(3, diagonal_families=2, stiffness=-1.0)
    negative_present = bool(
        (np.linalg.eigvalsh(unstable.hessian()) < -1e-10).any()
    )
    ledger.check(
        "mutation: sign-flipped stiffness yields a detected negative mode",
        negative_present,
    )


def main() -> int:
    ledger = CheckLedger("C-ELS-006")
    check_threshold_structure(ledger)
    check_centrosymmetric_exactness(ledger)
    check_two_route_agreement(ledger)
    check_mutations(ledger)
    return int(ledger.finish())


if __name__ == "__main__":
    sys.exit(main())
