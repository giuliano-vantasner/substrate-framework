#!/usr/bin/env python3
"""Independent time-integrator and frequency review for P045."""

from __future__ import annotations

import numpy as np
from scipy.signal import find_peaks

from substrate_framework.radial_sine_gordon import (
    evolve_radial_sine_gordon_leapfrog,
    evolve_radial_sine_gordon_mol,
)
from substrate_framework.verification import CheckLedger


def quadratic_fft_omega(time: np.ndarray, trace: np.ndarray, start: float) -> float:
    selected = time >= start
    tw = time[selected]
    values = np.array(trace[selected], copy=True)
    values -= np.polyval(np.polyfit(tw, values, 1), tw)
    spectrum = np.abs(np.fft.rfft(values * np.hanning(values.size)))
    bins = 2.0 * np.pi * np.fft.rfftfreq(values.size, tw[1] - tw[0])
    peak = int(np.argmax(spectrum[1:]) + 1)
    left, middle, right = np.log(np.maximum(spectrum[peak - 1 : peak + 2], 1.0e-300))
    offset = 0.5 * (left - right) / (left - 2.0 * middle + right)
    return float((peak + offset) * bins[1])


def peak_omega(time: np.ndarray, trace: np.ndarray, start: float, distance: float) -> float:
    selected = time >= start
    tw = time[selected]
    values = np.array(trace[selected], copy=True)
    values -= np.polyval(np.polyfit(tw, values, 1), tw)
    sample_step = tw[1] - tw[0]
    peaks, _ = find_peaks(
        values,
        distance=int(np.floor(distance / sample_step)),
        prominence=0.1 * np.ptp(values),
    )
    if peaks.size < 3:
        raise RuntimeError("independent peak route resolved fewer than two periods")
    peak_times: list[float] = []
    for peak in peaks:
        curvature = values[peak - 1] - 2.0 * values[peak] + values[peak + 1]
        offset = 0.5 * (values[peak - 1] - values[peak + 1]) / curvature
        peak_times.append(float(tw[peak] + offset * sample_step))
    return float(2.0 * np.pi / np.mean(np.diff(peak_times)))


def main() -> int:
    ledger = CheckLedger("P045-INDEPENDENT")
    common = dict(
        amplitude=3.0,
        width=4.0,
        spacing=0.2,
        outer_radius=200.0,
        final_time=300.0,
        core_radius=25.0,
        sample_interval=0.2,
    )
    adaptive = evolve_radial_sine_gordon_mol(**common)
    leapfrog = evolve_radial_sine_gordon_leapfrog(**common, courant=0.4)
    ledger.check(
        "adaptive DOP853 method-of-lines evolution completes with finite moment data",
        adaptive.completed
        and adaptive.function_evaluations is not None
        and adaptive.function_evaluations > 0
        and np.all(np.isfinite(adaptive.core_energy_radius_moment)),
    )
    ledger.check(
        "the independently integrated core moment is nonconstant",
        np.ptp(adaptive.core_energy_radius_moment[adaptive.time >= 140.0])
        / np.mean(adaptive.core_energy_radius_moment[adaptive.time >= 140.0])
        > 0.4,
    )

    ratios: dict[str, float] = {}
    for start in (140.0, 180.0):
        field_fft = quadratic_fft_omega(adaptive.time, adaptive.center, start)
        moment_fft = quadratic_fft_omega(
            adaptive.time, adaptive.core_energy_radius_moment, start
        )
        field_peaks = peak_omega(adaptive.time, adaptive.center, start, 5.0)
        moment_peaks = peak_omega(
            adaptive.time, adaptive.core_energy_radius_moment, start, 2.5
        )
        ratios[f"fft_{int(start)}"] = moment_fft / field_fft
        ratios[f"peaks_{int(start)}"] = moment_peaks / field_peaks
    ledger.check(
        "independent detrended FFT interpolation resolves the twice-frequency relation",
        max(abs(ratios[key] - 2.0) for key in ("fft_140", "fft_180")) < 0.004,
    )
    ledger.check(
        "independent prominent-maximum periods resolve the twice-frequency relation",
        max(abs(ratios[key] - 2.0) for key in ("peaks_140", "peaks_180"))
        < 0.004,
    )

    overlap = (
        (adaptive.time >= leapfrog.time[0])
        & (adaptive.time <= leapfrog.time[-1])
    )
    comparison_time = adaptive.time[overlap]
    interpolated_moment = np.interp(
        comparison_time,
        leapfrog.time,
        leapfrog.core_energy_radius_moment,
    )
    relative_moment_rms = float(
        np.sqrt(
            np.mean(
                np.square(
                    interpolated_moment
                    - adaptive.core_energy_radius_moment[overlap]
                )
            )
        )
        / np.std(adaptive.core_energy_radius_moment[overlap])
    )
    ledger.check(
        "adaptive and leapfrog moment traces agree on their common finite-time window",
        relative_moment_rms < 0.016,
        f"relative RMS={relative_moment_rms:.6g}",
    )

    leapfrog_ratios: list[float] = []
    for start in (140.0, 180.0):
        leapfrog_ratios.append(
            quadratic_fft_omega(
                leapfrog.time, leapfrog.core_energy_radius_moment, start
            )
            / quadratic_fft_omega(leapfrog.time, leapfrog.center, start)
        )
    ledger.check(
        "the independent integrator and leapfrog give the same frequency verdict",
        max(abs(value - 2.0) for value in leapfrog_ratios) < 0.004
        and max(
            abs(ratios[f"fft_{start}"] - value)
            for start, value in zip((140, 180), leapfrog_ratios)
        )
        < 5.0e-4,
    )
    print(
        "P045 independent metrics: "
        f"nfev={adaptive.function_evaluations}, ratios={ratios}, "
        f"leapfrog_fft_ratios={leapfrog_ratios}, "
        f"moment_relative_rms={relative_moment_rms:.9e}"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
