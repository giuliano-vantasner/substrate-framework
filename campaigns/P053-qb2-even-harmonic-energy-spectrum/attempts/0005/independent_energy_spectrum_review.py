from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import yaml
from scipy.integrate import simpson
from scipy.special import jv, roots_legendre

from substrate_framework.radial_harmonic_balance import solve_radial_harmonic_balance
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "f7ff064a708d4b3072b247088bee532eda6b14ef4a9d9f5480ea80743a22bbff"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def solve_branch():
    current = None
    for maximum in (1, 3, 5, 7, 9):
        current = solve_radial_harmonic_balance(
            tuple(range(1, maximum + 1, 2)),
            central_fundamental=2.5,
            outer_radius=40.0,
            frequency_guess=0.9769 if current is None else current.frequency,
            radial_points=320,
            temporal_samples=384,
            tolerance=5.0e-9,
            initial_solution=current,
        )
    return current


def interpolated_coefficients(solution, radius):
    amplitudes = np.vstack(
        [np.interp(radius, solution.radius, row) for row in solution.amplitudes]
    )
    derivatives = np.vstack(
        [np.interp(radius, solution.radius, row) for row in solution.radial_derivatives]
    )
    return amplitudes, derivatives


def gauss_moment_coefficients(
    solution,
    *,
    time_derivative_factor: float = 1.0,
    radial_measure_power: int = 4,
    fourier_factor: float = 1.0,
):
    radius = np.linspace(solution.origin_epsilon, 12.0, 4801)
    amplitudes, derivatives = interpolated_coefficients(solution, radius)
    nodes, weights = roots_legendre(192)
    phase = np.pi * (nodes + 1.0)
    modes = np.asarray(solution.harmonics, dtype=np.float64)
    angle = np.outer(modes, phase)
    field = np.cos(angle).T @ amplitudes
    time_derivative = (
        -(time_derivative_factor * solution.frequency * modes[:, None] * np.sin(angle)).T
        @ amplitudes
    )
    radial_derivative = np.cos(angle).T @ derivatives
    density = (
        0.5 * np.square(time_derivative)
        + 0.5 * np.square(radial_derivative)
        + 1.0
        - np.cos(field)
    )
    moment = 4.0 * np.pi * simpson(
        density * np.power(radius, radial_measure_power)[None, :],
        x=radius,
        axis=1,
    )
    coefficients = np.asarray(
        [
            fourier_factor
            * np.sum(weights * moment * np.cos(harmonic * phase))
            for harmonic in range(21)
        ]
    )
    coefficients[0] *= 0.5
    return coefficients


def arbitrary_non_solution_audit():
    radius = np.linspace(0.0, 12.0, 2401)
    phase = 2.0 * np.pi * np.arange(512) / 512
    width = 4.0
    omega = 0.93
    amplitude = 2.5 * np.exp(-np.square(radius / width))
    derivative = -2.0 * radius * amplitude / width**2
    radial_laplacian = (4.0 * radius**2 / width**4 - 6.0 / width**2) * amplitude
    field = np.cos(phase)[:, None] * amplitude[None, :]
    time_derivative = (
        -omega * np.sin(phase)[:, None] * amplitude[None, :]
    )
    radial_derivative = np.cos(phase)[:, None] * derivative[None, :]
    density = (
        0.5 * np.square(time_derivative)
        + 0.5 * np.square(radial_derivative)
        + 1.0
        - np.cos(field)
    )
    moment = 4.0 * np.pi * simpson(
        density * radius[None, :] ** 4, x=radius, axis=1
    )
    transform = np.fft.rfft(moment - np.mean(moment))
    power = np.square(np.abs(transform))
    purity = float(np.sum(power[1::2]) / np.sum(power[2::2]))
    residual = (
        -omega**2 * field
        - radial_laplacian[None, :] * np.cos(phase)[:, None]
        + np.sin(field)
    )
    return purity, float(np.sqrt(np.mean(np.square(residual))))


def local_cancellation_coefficients():
    phase = 2.0 * np.pi * np.arange(4096) / 4096
    amplitude = 1.0
    omega = 0.97
    derivative_squared = omega**2 - 8.0 * jv(2, amplitude)
    derivative = np.sqrt(derivative_squared)
    density = (
        0.5 * omega**2 * amplitude**2 * np.square(np.sin(phase))
        + 0.5 * derivative**2 * np.square(np.cos(phase))
        + 1.0
        - np.cos(amplitude * np.cos(phase))
    )
    coefficient = np.asarray(
        [2.0 * np.mean(density * np.cos(k * phase)) for k in range(9)]
    )
    coefficient[0] *= 0.5
    return coefficient


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--primary-evidence", type=Path, required=True)
    arguments = parser.parse_args()
    primary = yaml.safe_load(arguments.primary_evidence.read_text())
    source = arguments.source_file.read_text()
    target = float(primary["baseline"]["second_cos2"])
    ledger = CheckLedger("P053-INDEPENDENT")

    ledger.check(
        "the reviewed QB2 source is hash pinned",
        file_hash(arguments.source_file) == SOURCE_SHA256,
    )
    solution = solve_branch()
    ledger.check(
        "the independently sampled dependency branch resolves with a sub-gap frequency",
        solution.completed
        and solution.max_collocation_rms_residual < 6.0e-9
        and 0.97 < solution.frequency < 0.98,
    )
    coefficients = gauss_moment_coefficients(solution)
    ledger.check(
        "Gauss phase and Simpson radius integration reproduce the primary twice-frequency coefficient",
        abs(coefficients[2] - target) < 0.03,
    )
    ledger.check(
        "the independent twice-frequency coefficient dominates the resolved even comb",
        coefficients[2] ** 2 / np.sum(np.square(coefficients[2::2])) > 0.9998,
    )
    ledger.check(
        "Gauss integration independently annihilates every resolved odd coefficient",
        np.max(np.abs(coefficients[1::2])) < 2.0e-10,
    )

    ledger.mutation_sensitive(
        "the physical time-derivative omega factor",
        lambda factor: abs(
            gauss_moment_coefficients(
                solution, time_derivative_factor=float(factor)
            )[2]
            - target
        )
        < 0.03,
        1.0,
        [0.0, 2.0],
    )
    ledger.mutation_sensitive(
        "the real Fourier coefficient normalization",
        lambda factor: abs(
            gauss_moment_coefficients(solution, fourier_factor=float(factor))[2]
            - target
        )
        < 0.03,
        1.0,
        [0.5, -1.0],
    )
    ledger.check(
        "replacing the radial second-moment measure by total-energy measure changes the claim",
        abs(
            gauss_moment_coefficients(solution, radial_measure_power=2)[2]
            - target
        )
        > 100.0,
    )

    purity, residual = arbitrary_non_solution_audit()
    ledger.check(
        "an arbitrary odd-harmonic non-solution retains exact even spectral purity",
        purity < 1.0e-26,
    )
    ledger.check(
        "the same spectrally pure fabricated field fails the radial sine-Gordon equation",
        residual > 0.1,
    )
    cancellation = local_cancellation_coefficients()
    ledger.check(
        "even selection does not force a nonzero twice-frequency coefficient",
        abs(cancellation[2]) < 2.0e-14 and abs(cancellation[4]) > 1.0e-3,
    )

    moment_tensor = coefficients[2] * np.eye(3) / 3.0
    stf = moment_tensor - np.eye(3) * np.trace(moment_tensor) / 3.0
    ledger.check(
        "the spherical twice-frequency second moment has an exact STF null",
        np.max(np.abs(stf)) < 1.0e-14,
    )
    anisotropic = np.diag([coefficients[2], 0.0, 0.0])
    anisotropic_stf = anisotropic - np.eye(3) * np.trace(anisotropic) / 3.0
    ledger.check(
        "a declared anisotropic mutation is nonzero but is different source data",
        np.max(np.abs(anisotropic_stf)) > 100.0,
    )
    ledger.check(
        "QB2 calls a radial scalar moment a radiating line without a nonspherical source",
        "S[k] = trapz(T00 * r**2 * 4.0 * np.pi * r**2, r)" in source
        and "radiating line" in source,
    )
    ledger.check(
        "QB2's leakage guard changes temporal closure rather than the field equation",
        "1.37 * ph" in source and "residual" not in source,
    )

    print(
        "independent coefficients: "
        f"cos2={coefficients[2]:.12f} cos4={coefficients[4]:.12f} "
        f"max_odd={np.max(np.abs(coefficients[1::2])):.3e}"
    )
    print(
        f"fabricated odd/even={purity:.3e} residual_rms={residual:.6f}; "
        f"local_cancel_cos2={cancellation[2]:.3e} cos4={cancellation[4]:.6f}"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
