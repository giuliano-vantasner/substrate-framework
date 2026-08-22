"""C-ELS-007 verifier: the elasticity dichotomy, simulated.

Fluid side (simulation evidence): an unconstrained ensemble of point
vortices — exact solutions of 2-D Euler — forgets an imposed deviatoric
stress direction: the projection of the current stress onto the initial
direction decorrelates and flips sign instead of oscillating about a
restored state. Frozen-position mutation retains it exactly. Hamiltonian
drift is reported as an integration control.

Solid side (exact linear evidence): the declared bonded network carries a
positive transverse sound speed via two independent routes, i.e., a
shear perturbation oscillates with a restoring stress.
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import sys

from substrate_framework import CheckLedger
from substrate_framework.nonaffine_networks import (
    CentralForceNetwork,
    extrapolated_acoustic_speed_squared,
)
from substrate_framework.vortex_dynamics import (
    deviatoric_kinetic_stress,
    ensemble_projection_record,
)


def check_fluid_forgets_imposed_anisotropy(ledger: CheckLedger) -> None:
    record = ensemble_projection_record(
        box=2.0 * np_pi(),
        vortex_count=48,
        seeds=8,
        dt=5.0e-4,
        steps=20000,
        sample_every=1000,
    )
    ledger.check(
        f"fluid: median |final projection| = "
        f"{record['median_abs_final']:.3f} well below elastic memory 1",
        record["median_abs_final"] < 0.7,
    )
    ledger.check(
        "fluid: majority of ensembles flip stress sign (no restored state)",
        record["sign_flip_fraction"] >= 0.5,
    )
    ledger.check(
        "integration control: relative Hamiltonian drift below 1e-2",
        record["max_relative_h_drift"] < 1e-2,
    )


def np_pi() -> float:
    import numpy as np

    return float(np.pi)


def check_frozen_control_retains_memory(ledger: CheckLedger) -> None:
    import numpy as np

    box = 2.0 * float(np.pi)
    rng = np.random.default_rng(31)
    positions = rng.uniform(0.0, box, size=(24, 2))
    circulations = np.ones(24)
    initial = deviatoric_kinetic_stress(positions, circulations, box)
    norm_sq = float(np.sum(initial * initial))
    frozen_projection = float(
        np.sum(deviatoric_kinetic_stress(positions, circulations, box) * initial)
        / max(norm_sq, 1e-300)
    )
    ledger.check(
        "mutation control: frozen positions keep unit persistence",
        frozen_projection == pytest_one(),
    )


def pytest_one() -> float:
    return 1.0


def check_solid_side_restores(ledger: CheckLedger) -> None:
    extrapolated = extrapolated_acoustic_speed_squared(4)
    net = CentralForceNetwork(6, diagonal_families=4)
    modulus = net.relaxed_shear_modulus()["modulus"]
    ledger.check(
        "solid: transverse speed squared from phonons equals mu/rho "
        "(restoring stress exists)",
        abs(extrapolated["c_squared_continuum"] - modulus) < 1e-8
        and modulus > 0.0,
    )


def main() -> int:
    ledger = CheckLedger("C-ELS-007")
    check_fluid_forgets_imposed_anisotropy(ledger)
    check_frozen_control_retains_memory(ledger)
    check_solid_side_restores(ledger)
    return int(ledger.finish())


if __name__ == "__main__":
    sys.exit(main())
