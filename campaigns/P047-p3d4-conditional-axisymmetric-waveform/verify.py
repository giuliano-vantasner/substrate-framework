#!/usr/bin/env python3
"""Verify P047's axisymmetric STF map and audit P3D4."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.axisymmetric_radiation import (
    conditional_axisymmetric_radiation_coefficients,
)
from substrate_framework.governance import load_yaml
from substrate_framework.numerics import (
    interpolating_spline_time_derivative,
    local_polynomial_time_derivative,
)
from substrate_framework.radial_sine_gordon import gaussian_radial_seed
from substrate_framework.sine_gordon_l_modes import (
    LinearizedAngularModeEvolution,
    evolve_radial_background_with_linearized_mode,
    multiplicative_p2_residual,
    regular_l_mode_gaussian_seed,
)
from substrate_framework.tt_angular import (
    axisymmetric_stf_readout,
    axisymmetric_stf_tensor,
    conditional_axisymmetric_stf_power,
    frobenius_norm_squared,
)
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "055c001288217998406b73026bf9f1402e044c5b4b26aa1929241a31402b827f"
)


def run_branch(
    spacing: float,
    *,
    outer_radius: float = 80.0,
    final_time: float = 40.0,
    courant: float = 0.4,
    mode_amplitude: float = 0.2,
) -> LinearizedAngularModeEvolution:
    """Run the accepted P046 IVP with P047's aligned dense sampling."""

    radius = spacing * np.arange(int(round(outer_radius / spacing)) + 1)
    return evolve_radial_background_with_linearized_mode(
        gaussian_radial_seed(radius, 3.0, 4.0),
        regular_l_mode_gaussian_seed(
            radius,
            ell=2,
            amplitude=mode_amplitude,
            width=4.0,
        ),
        spacing=spacing,
        final_time=final_time,
        ell=2,
        courant=courant,
        sample_interval=0.16,
    )


def sampled(
    result: LinearizedAngularModeEvolution,
    stride: int,
) -> tuple[np.ndarray, np.ndarray]:
    return (
        result.time[::stride],
        result.p2_triple_stf_zz_coefficient[::stride],
    )


def derivatives(
    time: np.ndarray,
    trace: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    interval = float(time[1] - time[0])
    local_second = local_polynomial_time_derivative(
        time,
        trace,
        2,
        window_duration=8.0 * interval,
        polynomial_order=5,
    )
    local_third = local_polynomial_time_derivative(
        time,
        trace,
        3,
        window_duration=8.0 * interval,
        polynomial_order=5,
    )
    spline_second = interpolating_spline_time_derivative(
        time,
        trace,
        2,
        spline_degree=5,
    )
    spline_third = interpolating_spline_time_derivative(
        time,
        trace,
        3,
        spline_degree=5,
    )
    return local_second, local_third, spline_second, spline_third


def interpreted_mask(time: np.ndarray) -> np.ndarray:
    return (time >= 5.0) & (time <= 35.0)


def rms(values: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(values))))


def symmetric_relative_rms(first: np.ndarray, second: np.ndarray) -> float:
    denominator = 0.5 * (rms(first) + rms(second))
    if denominator <= 1.0e-14:
        if np.array_equal(first, second):
            return 0.0
        raise RuntimeError("near-zero derivative comparison has unequal traces")
    return rms(first - second) / denominator


def aligned_local(
    result: LinearizedAngularModeEvolution,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    time, trace = sampled(result, 2)
    second, third, _spline_second, _spline_third = derivatives(time, trace)
    interior = interpreted_mask(time)
    return time[interior], second[interior], third[interior]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P047-P3D4")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    reproduction = load_yaml(args.source_reproduction)
    ledger.check(
        "the audited P3D4 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    ledger.check(
        "the exact source reproduction exits with its four-check tally",
        reproduction.get("sha256") == EXPECTED_SOURCE_SHA256
        and reproduction.get("exit_code") == 0
        and "ALL 4 CHECKS PASS" in str(reproduction.get("terminal_tally", "")),
    )
    ledger.check(
        "P3D4 selects the current NumPy trapezoid API before its legacy fallback",
        'np.trapezoid if hasattr(np, "trapezoid") else np.trapz' in source_text,
    )

    alpha, coupling = sp.symbols("alpha G", nonzero=True, real=True)
    axis = sp.Matrix([1, 2, 2])
    normalized = axisymmetric_stf_tensor(alpha, axis)
    triple = axisymmetric_stf_tensor(alpha, axis, 3)
    unit_axis = axis / 3
    ledger.check(
        "the arbitrary-axis tensor is STF with the exact axial eigenvalue and norm",
        sp.trace(normalized) == 0
        and sp.simplify(
            normalized * unit_axis - 2 * alpha * unit_axis / 3
        )
        == sp.zeros(3, 1)
        and sp.simplify(frobenius_norm_squared(normalized) - 2 * alpha**2 / 3)
        == 0,
    )
    ledger.check(
        "the triple convention multiplies the tensor by three and its norm by nine",
        triple == 3 * normalized
        and sp.simplify(frobenius_norm_squared(triple) - 6 * alpha**2) == 0,
    )

    direction = sp.Matrix([2, -1, 2])
    readout = axisymmetric_stf_readout(alpha, axis, direction, 3)
    sine_squared = sp.Rational(65, 81)
    ledger.check(
        "the natural arbitrary-axis TT frame has sine-squared plus and zero cross",
        readout.inclination_sine_squared == sine_squared
        and sp.simplify(
            readout.normalized_plus_coordinate
            - 3 * alpha * sine_squared / sp.sqrt(2)
        )
        == 0
        and readout.normalized_cross_coordinate == 0
        and sp.simplify(
            readout.conventional_plus_readout
            - 3 * alpha * sine_squared / 2
        )
        == 0,
    )
    axis_null = axisymmetric_stf_readout(alpha, axis, axis)
    ledger.check(
        "an arbitrary-axis axisymmetric STF tensor has an exact symmetry-axis TT null",
        axis_null.inclination_sine_squared == 0
        and axis_null.projected_tensor == sp.zeros(3),
    )

    normalized_power = conditional_axisymmetric_stf_power(alpha, coupling, 1)
    triple_power = conditional_axisymmetric_stf_power(alpha, coupling, 3)
    ledger.check(
        "conditional axisymmetric power is convention invariant and keeps G explicit",
        sp.simplify(normalized_power - 2 * coupling * alpha**2 / 15) == 0
        and triple_power == normalized_power,
    )

    def convention_predicate(candidate: object) -> bool:
        scale = float(candidate)
        q_second = np.array([2.0, -4.0])
        q_third = np.array([3.0, 5.0])
        supplied = conditional_axisymmetric_radiation_coefficients(
            q_second,
            q_third,
            inclination=np.pi / 2.0,
            quadrupole_scale=scale,
        )
        normalized_equivalent = conditional_axisymmetric_radiation_coefficients(
            q_second / 3.0,
            q_third / 3.0,
            inclination=np.pi / 2.0,
            quadrupole_scale=1.0,
        )
        return bool(
            np.allclose(
                supplied.conventional_plus_R_over_G,
                normalized_equivalent.conventional_plus_R_over_G,
            )
            and np.allclose(supplied.power_over_G, normalized_equivalent.power_over_G)
        )

    ledger.mutation_sensitive(
        "triple quadrupole convention scale",
        convention_predicate,
        3,
        [1, 9],
    )

    triple_numeric = conditional_axisymmetric_radiation_coefficients(
        np.array([2.0, -4.0]),
        np.array([3.0, 5.0]),
        inclination=np.pi / 2.0,
        quadrupole_scale=3.0,
    )
    ledger.check(
        "a triple Qzz trace has hplus R/G=qddot/2 and P/G=qthird squared/30",
        np.allclose(
            triple_numeric.conventional_plus_R_over_G,
            np.array([1.0, -2.0]),
        )
        and np.allclose(
            triple_numeric.power_over_G,
            np.array([9.0, 25.0]) / 30.0,
        )
        and np.array_equal(
            triple_numeric.conventional_cross_R_over_G,
            np.zeros(2),
        ),
    )

    source_scale_error = conditional_axisymmetric_radiation_coefficients(
        np.array([2.0, -4.0]),
        np.array([3.0, 5.0]),
        inclination=np.pi / 2.0,
        quadrupole_scale=1.0,
    )
    ledger.check(
        "P3D4 applies the normalized G/5 coefficient to a triple tensor and is ninefold high",
        "return 3.0 * I - delta * np.trace(I)" in source_text
        and "P = (Geff / 5.0) * 1.5 * d3zz**2" in source_text
        and np.allclose(
            source_scale_error.power_over_G,
            9.0 * triple_numeric.power_over_G,
        ),
    )

    inherited_residual = multiplicative_p2_residual(
        np.array([0.8, 1.2]),
        np.array([1.0, 2.0]),
        0.3,
        np.array([0.2, 0.7]),
    )
    ledger.check(
        "P3D4 inherits P3D3's rejected multiplicative field construction",
        "fac = (1.0 + a * P2mu)" in source_text
        and "U = P[:, None] * fac[None, :]" in source_text
        and np.max(np.abs(inherited_residual)) > 0.1,
    )
    ledger.check(
        "the inherited source energy omits the nonradial angular-gradient term",
        "T00 = 0.5 * Ut**2 + 0.5 * Ur**2 + (1.0 - np.cos(U))" in source_text
        and "Utheta" not in source_text,
    )
    ledger.check(
        "P3D4's claimed refinement is only denser sampling of the same field evolution",
        "dt_fine = dt_leapfrog = dt_snap/2" in source_text
        and "dt = 0.4 * dr" in source_text
        and "dr=0.05" in source_text
        and "fQ.append(Qzz_from_profile(u_curr, Pt))" in source_text,
    )
    ledger.check(
        "P3D4 selects its FFT derivative cutoff from the observed source carrier",
        "W_BAND = 5.0 * omega_p" in source_text
        and "F[w > wmax] = 0.0" in source_text,
    )
    ledger.check(
        "P3D4 declares rather than derives its gravity law and effective coupling",
        "standard linearized GR" in source_text
        and "Geff = 1.0" in source_text
        and "DECLARED:      G_eff = c0 = 1" in source_text,
    )

    polynomial_time = np.linspace(-2.0, 2.0, 81)
    polynomial = polynomial_time**5 - 2.0 * polynomial_time**3
    polynomial_exact = 60.0 * polynomial_time**2 - 12.0
    polynomial_local = local_polynomial_time_derivative(
        polynomial_time,
        polynomial,
        3,
        window_duration=0.4,
        polynomial_order=5,
    )
    polynomial_spline = interpolating_spline_time_derivative(
        polynomial_time,
        polynomial,
        3,
        spline_degree=5,
    )
    polynomial_interior = np.abs(polynomial_time) <= 1.5
    ledger.check(
        "both derivative estimators recover an independently differentiated polynomial",
        np.allclose(
            polynomial_local[polynomial_interior],
            polynomial_exact[polynomial_interior],
            atol=3.0e-9,
        )
        and np.allclose(
            polynomial_spline[polynomial_interior],
            polynomial_exact[polynomial_interior],
            atol=3.0e-9,
        ),
    )
    constant_time = np.linspace(0.0, 8.0, 51)
    constant_trace = np.full_like(constant_time, 7.0)
    constant_third = local_polynomial_time_derivative(
        constant_time,
        constant_trace,
        3,
        window_duration=8.0 * (constant_time[1] - constant_time[0]),
        polynomial_order=5,
    )
    ledger.check(
        "the static nonzero trace guard has zero third derivative and conditional power",
        np.max(np.abs(constant_third[8:-8])) < 1.0e-10
        and np.max(
            conditional_axisymmetric_radiation_coefficients(
                np.zeros_like(constant_third[8:-8]),
                constant_third[8:-8],
                inclination=np.pi / 2.0,
                quadrupole_scale=3.0,
            ).power_over_G
        )
        < 1.0e-20,
    )

    coarse, baseline, fine = [run_branch(spacing) for spacing in (0.2, 0.1, 0.05)]
    timestep = run_branch(0.1, courant=0.2)
    domain = run_branch(0.1, outer_radius=100.0)
    half_amplitude = run_branch(0.1, mode_amplitude=0.1)
    zero_amplitude = run_branch(0.2, final_time=8.0, mode_amplitude=0.0)
    simulations = (coarse, baseline, fine, timestep, domain, half_amplitude)
    ledger.check(
        "all corrected regular-mode evolutions complete with finite moment traces",
        all(
            result.completed
            and np.all(np.isfinite(result.p2_triple_stf_zz_coefficient))
            for result in simulations
        ),
    )
    ledger.check(
        "the interpreted finite-time interval is quiet at the outer boundary",
        max(result.max_boundary_background for result in (coarse, baseline, fine))
        < 3.0e-19
        and max(result.max_boundary_mode for result in (coarse, baseline, fine))
        < 4.0e-19
        and fine.time[-1] < fine.outer_radius,
    )

    aligned = [aligned_local(result) for result in (coarse, baseline, fine)]
    ledger.check(
        "the three mesh derivative traces share the frozen interpreted time grid",
        all(np.array_equal(aligned[0][0], item[0]) for item in aligned[1:]),
    )
    mesh_second = [
        symmetric_relative_rms(aligned[0][1], aligned[1][1]),
        symmetric_relative_rms(aligned[1][1], aligned[2][1]),
    ]
    mesh_third = [
        symmetric_relative_rms(aligned[0][2], aligned[1][2]),
        symmetric_relative_rms(aligned[1][2], aligned[2][2]),
    ]
    ledger.check(
        "the second derivative self-converges and its fine difference is below five percent",
        mesh_second[1] < mesh_second[0] and mesh_second[1] < 0.05,
        f"successive relative RMS={mesh_second}",
    )
    ledger.check(
        "the third derivative self-converges and its fine difference is below five percent",
        mesh_third[1] < mesh_third[0] and mesh_third[1] < 0.05,
        f"successive relative RMS={mesh_third}",
    )

    base_time, base_second, base_third = aligned[1]
    timestep_time, timestep_second, timestep_third = aligned_local(timestep)
    domain_time, domain_second, domain_third = aligned_local(domain)
    half_time, half_second, half_third = aligned_local(half_amplitude)
    ledger.check(
        "timestep, domain, and amplitude mutations share the interpreted time grid",
        all(
            np.array_equal(base_time, comparison)
            for comparison in (timestep_time, domain_time, half_time)
        ),
    )
    timestep_errors = (
        symmetric_relative_rms(base_second, timestep_second),
        symmetric_relative_rms(base_third, timestep_third),
    )
    ledger.check(
        "halving the timestep changes both derivative RMS traces by below five percent",
        max(timestep_errors) < 0.05,
        f"second/third relative RMS={timestep_errors}",
    )
    domain_errors = (
        symmetric_relative_rms(base_second, domain_second),
        symmetric_relative_rms(base_third, domain_third),
    )
    ledger.check(
        "a causally disconnected domain extension preserves both derivative traces",
        max(domain_errors) < 0.05,
        f"second/third relative RMS={domain_errors}",
    )

    dense_time, dense_trace = sampled(baseline, 1)
    dense_second, dense_third, _dense_spline_second, _dense_spline_third = derivatives(
        dense_time,
        dense_trace,
    )
    dense_interior = interpreted_mask(dense_time)
    dense_time_interior = dense_time[dense_interior]
    dense_second_interior = dense_second[dense_interior]
    dense_third_interior = dense_third[dense_interior]
    dense_on_reported = np.searchsorted(dense_time_interior, base_time)
    ledger.check(
        "the dense and reported sampling grids align exactly in the interpreted window",
        np.array_equal(dense_time_interior[dense_on_reported], base_time),
    )
    sampling_errors = (
        symmetric_relative_rms(
            base_second,
            dense_second_interior[dense_on_reported],
        ),
        symmetric_relative_rms(
            base_third,
            dense_third_interior[dense_on_reported],
        ),
    )
    ledger.check(
        "halving the sampling interval changes both derivative traces by below five percent",
        max(sampling_errors) < 0.05,
        f"second/third relative RMS={sampling_errors}",
    )

    reported_time, reported_trace = sampled(baseline, 2)
    local_second, local_third, spline_second, spline_third = derivatives(
        reported_time,
        reported_trace,
    )
    reported_interior = interpreted_mask(reported_time)
    estimator_errors = (
        symmetric_relative_rms(
            local_second[reported_interior],
            spline_second[reported_interior],
        ),
        symmetric_relative_rms(
            local_third[reported_interior],
            spline_third[reported_interior],
        ),
    )
    ledger.check(
        "local-polynomial and independent spline derivatives agree below ten percent",
        max(estimator_errors) < 0.10,
        f"second/third relative RMS={estimator_errors}",
    )

    ledger.check(
        "halving the regular l=2 amplitude halves both derivative traces exactly",
        symmetric_relative_rms(half_second, 0.5 * base_second) < 1.0e-12
        and symmetric_relative_rms(half_third, 0.5 * base_third) < 1.0e-12,
    )
    ledger.check(
        "zero regular l=2 amplitude gives an exact zero moment trace",
        np.array_equal(
            zero_amplitude.p2_triple_stf_zz_coefficient,
            np.zeros_like(zero_amplitude.p2_triple_stf_zz_coefficient),
        ),
    )

    conditional = conditional_axisymmetric_radiation_coefficients(
        base_second,
        base_third,
        inclination=np.pi / 2.0,
        quadrupole_scale=3.0,
    )
    half_conditional = conditional_axisymmetric_radiation_coefficients(
        half_second,
        half_third,
        inclination=np.pi / 2.0,
        quadrupole_scale=3.0,
    )
    power_mean = float(np.mean(conditional.power_over_G))
    ledger.check(
        "the qualified q=Qzz/epsilon trace gives finite nonzero hplus R/(G epsilon) and nonnegative P/(G epsilon squared)",
        np.all(np.isfinite(conditional.conventional_plus_R_over_G))
        and np.all(np.isfinite(conditional.power_over_G))
        and rms(conditional.conventional_plus_R_over_G) > 1.0
        and power_mean > 1.0
        and np.min(conditional.power_over_G) >= 0.0
        and np.array_equal(
            conditional.conventional_cross_R_over_G,
            np.zeros_like(conditional.conventional_cross_R_over_G),
        ),
        f"plus RMS={rms(conditional.conventional_plus_R_over_G):.9g}, "
        f"power mean={power_mean:.9g}",
    )
    ledger.check(
        "half mode coefficient gives half conditional waveform coefficient and one-quarter power coefficient",
        symmetric_relative_rms(
            half_conditional.conventional_plus_R_over_G,
            0.5 * conditional.conventional_plus_R_over_G,
        )
        < 1.0e-12
        and symmetric_relative_rms(
            half_conditional.power_over_G,
            0.25 * conditional.power_over_G,
        )
        < 1.0e-12,
    )

    source_wrong_power = conditional_axisymmetric_radiation_coefficients(
        base_second,
        base_third,
        inclination=np.pi / 2.0,
        quadrupole_scale=1.0,
    ).power_over_G
    ledger.check(
        "the live corrected Qzz/epsilon coefficient exposes the source's factor-nine power mutation",
        np.allclose(source_wrong_power, 9.0 * conditional.power_over_G),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
