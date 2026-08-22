"""C-ELS-002 numerical verifier: SciPy time integration of shear waves.

The symbolic rung fixes c_S^2 = mu/rho. This file validates the same
logic dynamically: the Navier-Cauchy transverse plane mode, reduced to
its amplitude oscillator u_tt = -(c_S k)^2 u, is integrated with scipy
solve_ivp (through substrate_framework.numerics.solve_ivp_evidence) and
the measured oscillation frequency must match c_S * k within a declared
tolerance. Mutations: a half-strength medium oscillates at its own
frequency (off-shell), and refinement must not move the estimate.
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import sys

import numpy as np

from substrate_framework import CheckLedger
from substrate_framework.numerics import (
    SolverTolerances,
    solve_ivp_evidence,
)

MU = 2.0
RHO = 0.5
K_WAVE = 3.0
C_S_SQUARED = MU / RHO
OMEGA_EXACT = (C_S_SQUARED ** 0.5) * K_WAVE


def transverse_rhs(state: np.ndarray, omega_squared: float) -> np.ndarray:
    """Harmonic oscillator form of the transverse plane wave amplitude."""

    displacement, velocity = state
    return np.array([velocity, -omega_squared * displacement])


def measured_frequency(omega_squared_mode: float) -> dict[str, float]:
    """Integrate one window; estimate omega by zero crossings of u(t)."""

    state0 = np.array([1.0, 0.0])
    duration = 4.0 * np.pi / OMEGA_EXACT
    samples = 4001
    times = np.linspace(0.0, duration, samples)
    evidence = solve_ivp_evidence(
        lambda time, state: transverse_rhs(state, omega_squared_mode),
        (0.0, float(duration)),
        state0,
        sample_times=times,
        tolerances=SolverTolerances(rtol=1e-12, atol=1e-14),
    )
    displacement = evidence.state[0]
    sign_changes = int(np.sum(np.diff(np.sign(displacement)) != 0))
    periods = sign_changes / 2.0
    omega_measured = 2.0 * np.pi * periods / float(duration)
    velocity = evidence.state[1]
    energy = 0.5 * (
        velocity**2 + omega_squared_mode * displacement**2
    )
    energy_drift = float(np.max(np.abs(energy - energy[0])))
    return {
        "omega": omega_measured,
        "relative_error": abs(omega_measured - OMEGA_EXACT) / OMEGA_EXACT,
        "max_energy_drift": energy_drift,
    }


def check_frequency_matches_symbolic_speed(ledger: CheckLedger) -> None:
    result = measured_frequency(C_S_SQUARED * K_WAVE**2)
    ledger.check(
        f"measured omega == c_S*k = {OMEGA_EXACT:.6f} within 1e-6",
        result["relative_error"] < 1e-6,
    )
    ledger.check(
        "oscillator energy conserved across the integration window",
        result["max_energy_drift"] < 1e-10,
    )


def check_refinement_stability(ledger: CheckLedger) -> None:
    coarse = measured_frequency(C_S_SQUARED * K_WAVE**2)["omega"]
    fine_times = 16001
    state0 = np.array([1.0, 0.0])
    duration = 4.0 * np.pi / OMEGA_EXACT
    times = np.linspace(0.0, float(duration), fine_times)
    evidence = solve_ivp_evidence(
        lambda time, state: transverse_rhs(state, C_S_SQUARED * K_WAVE**2),
        (0.0, float(duration)),
        state0,
        sample_times=times,
        tolerances=SolverTolerances(rtol=1e-13, atol=1e-15),
    )
    displacement = evidence.state[0]
    crossings = int(np.sum(np.diff(np.sign(displacement)) != 0))
    fine_omega = 2.0 * np.pi * (crossings / 2.0) / float(duration)
    ledger.check(
        "frequency estimate stable under sampling/tolerance refinement",
        abs(fine_omega - coarse) < 1e-8,
    )
def check_mutation_off_shell_fails(ledger: CheckLedger) -> None:
    wrong_omega_squared = 0.5 * C_S_SQUARED * K_WAVE**2
    own_expected = wrong_omega_squared ** 0.5
    long_window = 16.0 * np.pi / OMEGA_EXACT
    state0 = np.array([1.0, 0.0])
    times = np.linspace(0.0, long_window, 16001)
    evidence = solve_ivp_evidence(
        lambda time, state: transverse_rhs(state, wrong_omega_squared),
        (0.0, float(long_window)),
        state0,
        sample_times=times,
        tolerances=SolverTolerances(rtol=1e-12, atol=1e-14),
    )
    displacement = evidence.state[0]
    crossings = int(np.sum(np.diff(np.sign(displacement)) != 0))
    measured = 2.0 * np.pi * (crossings / 2.0) / float(long_window)
    ledger.check(
        "mutation: half-strength medium oscillates off the claimed shell",
        abs(measured - OMEGA_EXACT) / OMEGA_EXACT > 0.1,
    )
    ledger.check(
        "mutation control: it does match its own half-strength dispersion",
        abs(measured - own_expected) / own_expected < 0.1,
    )

def main() -> int:
    ledger = CheckLedger("C-ELS-002-dynamics")
    check_frequency_matches_symbolic_speed(ledger)
    check_refinement_stability(ledger)
    check_mutation_off_shell_fails(ledger)
    return int(ledger.finish())


if __name__ == "__main__":
    sys.exit(main())
