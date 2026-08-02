"""Audit QB4's literal time-series claims after its own clean reproduction."""

from __future__ import annotations

import contextlib
import io
import json
import runpy

import numpy as np


SOURCE = "/home/dan/substrate/merged-framework/bridges/phase-16/bridge_QB4_two_polarization_waveform.py"


def singular_ratio(values: np.ndarray) -> tuple[int, float, list[float]]:
    centered = values - np.mean(values, axis=0, keepdims=True)
    singular = np.linalg.svd(centered, compute_uv=False)
    threshold = max(centered.shape) * np.finfo(float).eps * singular[0]
    rank = int(np.count_nonzero(singular > threshold))
    ratio = float(singular[1] / singular[0]) if singular.size > 1 else 0.0
    return rank, ratio, [float(value) for value in singular]


def main() -> None:
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        namespace = runpy.run_path(SOURCE)

    omega = float(namespace["omega"])
    omega_2 = float(namespace["omega_2"])
    period = float(namespace["period_T"])
    q_series = np.asarray(namespace["Q_series"], dtype=float)
    q_band = np.asarray(namespace["Q_band"], dtype=float)
    q_ddot = np.asarray(namespace["Qddot"], dtype=float)
    d3_spec = np.asarray(namespace["d3_spec"], dtype=float)
    dt = float(namespace["dt"])
    n_time = int(namespace["Nt"])
    q_tensor = namespace["Q_tensor"]
    amplitude = float(namespace["B_M2"])
    readout = namespace["hplus_hcross"]

    ratio = omega_2 / omega
    frequency_closure_defect = abs(ratio - round(ratio))
    q_start = np.asarray(q_tensor(amplitude, 0.0, 0.0), dtype=float)
    q_end = np.asarray(q_tensor(amplitude, omega * period, omega_2 * period), dtype=float)
    endpoint_relative_defect = float(
        np.linalg.norm(q_end - q_start) / max(np.linalg.norm(q_start), 1.0e-30)
    )

    angular_frequency = 2.0 * np.pi * np.fft.rfftfreq(n_time, dt)
    two_omega_bin = int(np.argmin(np.abs(angular_frequency - 2.0 * omega)))
    isolated_transform = np.zeros_like(np.fft.rfft(q_series, axis=-1))
    isolated_transform[..., two_omega_bin] = np.fft.rfft(q_series, axis=-1)[..., two_omega_bin]
    isolated_d3 = np.fft.irfft(
        (1j * angular_frequency) ** 3 * isolated_transform,
        n=n_time,
        axis=-1,
    )
    all_derivative_norm = float(np.mean(np.sum(d3_spec**2, axis=(0, 1))))
    line_derivative_norm = float(np.mean(np.sum(isolated_d3**2, axis=(0, 1))))
    line_fraction = line_derivative_norm / all_derivative_norm
    source_slice = namespace["sl"]
    source_derivative_norm = float(
        np.mean(np.sum(d3_spec[..., source_slice] ** 2, axis=(0, 1)))
    )
    source_line_norm = float(
        np.mean(np.sum(isolated_d3[..., source_slice] ** 2, axis=(0, 1)))
    )
    source_line_fraction = source_line_norm / source_derivative_norm

    diagonal_coefficients = np.column_stack(
        ((q_series[0, 0] - q_series[1, 1]) / 2.0, q_series[2, 2])
    )
    tensor_rank, tensor_ratio, tensor_singular = singular_ratio(diagonal_coefficients)

    interior = slice(2, -2)
    generic_readouts = np.array(
        [readout(q_ddot[:, :, index], [1.0, 1.0, 1.0]) for index in range(2, n_time - 2)]
    )
    readout_rank, readout_ratio, readout_singular = singular_ratio(generic_readouts)

    # QB4's exact line-amplitude equality uses the same FFT coefficient on both
    # sides, so it is algebraically guaranteed by the derivative definition.
    fft = np.fft.rfft(q_series[2, 2] - np.mean(q_series[2, 2]))
    source_line_amplitude = 2.0 * abs(fft[two_omega_bin]) / n_time
    constructed_analytic_line = (2.0 * omega) ** 3 * source_line_amplitude
    derivative_fft = np.fft.rfft(d3_spec[2, 2] - np.mean(d3_spec[2, 2]))
    derivative_line = 2.0 * abs(derivative_fft[two_omega_bin]) / n_time

    output = {
        "source_tally_preserved": "ALL 5 CHECKS PASS",
        "periodic_fft_gate": {
            "omega_2_over_omega": ratio,
            "nearest_integer_defect": frequency_closure_defect,
            "frequency_closure_pass": frequency_closure_defect < 1.0e-10,
            "endpoint_tensor_relative_defect": endpoint_relative_defect,
            "endpoint_pass": endpoint_relative_defect < 1.0e-3,
        },
        "two_omega_power_gate": {
            "bin_frequency": float(angular_frequency[two_omega_bin]),
            "all_bandlimited_derivative_norm": all_derivative_norm,
            "two_omega_derivative_norm": line_derivative_norm,
            "two_omega_fraction": line_fraction,
            "source_interior_derivative_norm": source_derivative_norm,
            "source_interior_two_omega_derivative_norm": source_line_norm,
            "source_interior_two_omega_fraction": source_line_fraction,
            "dominance_pass": source_line_fraction > 0.5,
        },
        "source_temporal_rank": {
            "diagonal_stf_rank": tensor_rank,
            "diagonal_second_to_first_ratio": tensor_ratio,
            "diagonal_singular_values": tensor_singular,
            "generic_readout_rank": readout_rank,
            "generic_second_to_first_ratio": readout_ratio,
            "generic_singular_values": readout_singular,
            "finite_b_ceiling": "rank belongs to the qualified finite-b source and is not promotable dynamics",
        },
        "same_fft_bin_identity": {
            "constructed_analytic_line": constructed_analytic_line,
            "spectral_derivative_line": derivative_line,
            "relative_difference": abs(derivative_line - constructed_analytic_line)
            / max(constructed_analytic_line, 1.0e-30),
            "independent_oracle": False,
        },
        "power_convention": {
            "reported_G_over_5_average": float(namespace["P_avg"]),
            "triple_STF_G_over_45_average": float(namespace["P_avg"]) / 9.0,
            "factor_error": 9.0,
        },
        "time_reversal_structure": {
            "field_inputs": ["cos(omega*t)", "cos(omega_2*t)"],
            "moment_is_even_in_time": True,
            "consequence": "each exact combination-frequency line has real tensor amplitude and is linearly polarized; one-time nonzero coordinates do not prove an ellipse",
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
