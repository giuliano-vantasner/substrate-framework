"""Primary exact and refined numerical verifier for P062."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.radial_modes import (
    apply_option_c_radial_hessian,
    classical_mode_scale_ledger,
    derrick_scale_tangent,
    derrick_scaling_evidence,
    option_c_continuum_threshold,
    option_c_euler_lagrange_residual,
    option_c_hedgehog_rhs,
    option_c_operator_coefficients,
    option_c_radial_energy_density,
    option_c_second_variation,
    radial_green_boundary_form,
    solve_option_c_hedgehog,
    solve_radial_finite_box_spectrum,
)
from substrate_framework.verification import CheckLedger

SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-18/"
    "bridge_PG3_roper_radial_excitation.py"
)
SOURCE_SHA256 = "4e3b56ab04977d254a291dd56d28e3285d72e86b3d640e0cfc322d5818cf007f"


def _finite_difference_stationarity(profile, stride: int) -> float:
    radius = profile.radius[::stride]
    field = profile.field[::stride]
    derivative = profile.radial_derivative[::stride]
    second = np.gradient(derivative, radius, edge_order=2)
    residual = (
        (radius**2 + 2.0 * np.sin(field) ** 2) * second
        + 2.0 * radius * derivative
        + np.sin(2.0 * field) * (derivative**2 - 1.0)
        - np.sin(2.0 * field) * np.sin(field) ** 2 / radius**2
    )
    interior = (radius >= 0.3) & (radius <= 10.0)
    return float(np.max(np.abs(residual[interior])))


def _profile_spectrum(profile):
    states = np.column_stack((profile.field, profile.radial_derivative))
    second = np.asarray(
        [
            option_c_hedgehog_rhs(radius, state)[1]
            for radius, state in zip(profile.radius, states, strict=True)
        ]
    )
    gradient, potential, weight, correction = option_c_operator_coefficients(
        profile.radius,
        profile.field,
        profile.radial_derivative,
        second,
    )
    spectrum = solve_radial_finite_box_spectrum(
        profile.radius,
        gradient,
        potential,
        weight,
        mode_count=4,
        continuum_threshold=float(option_c_continuum_threshold()),
    )
    return spectrum, gradient, potential, weight, correction


def main() -> int:
    ledger = CheckLedger("P062")
    ledger.check("hash-pinned PG3 source exists", SOURCE.is_file())
    ledger.check(
        "hash-pinned PG3 source integrity",
        hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
    )

    radius = sp.symbols("r", positive=True)
    field_symbol, derivative_symbol = sp.symbols("q p", real=True)
    profile = sp.Function("f")(radius)
    density = option_c_radial_energy_density(
        field_symbol,
        derivative_symbol,
        radius,
    )
    substitutions = {
        field_symbol: profile,
        derivative_symbol: sp.diff(profile, radius),
    }
    direct_el = sp.simplify(
        (
            sp.diff(sp.diff(density, derivative_symbol).subs(substitutions), radius)
            - sp.diff(density, field_symbol).subs(substitutions)
        )
        / 2
    )
    ledger.check(
        "declared energy derives the hedgehog equation",
        sp.simplify(direct_el - option_c_euler_lagrange_residual(profile, radius)) == 0,
    )

    variation = option_c_second_variation(profile, radius)
    mode = sp.Function("eta")(radius)
    epsilon = sp.symbols("epsilon", real=True)
    perturbed = profile + epsilon * mode
    expanded_density = option_c_radial_energy_density(
        perturbed,
        sp.diff(perturbed, radius),
        radius,
    )
    quadratic = sp.simplify(
        sp.diff(expanded_density, epsilon, 2).subs(epsilon, 0) / 2
    )
    self_adjoint = sp.simplify(
        variation.gradient_coefficient * sp.diff(mode, radius) ** 2
        + variation.potential_coefficient * mode**2
    )
    boundary_derivative = sp.diff(
        variation.mixed_coefficient * mode**2 / 2,
        radius,
    )
    ledger.check(
        "full epsilon expansion equals self-adjoint form plus boundary derivative",
        sp.simplify(quadratic - self_adjoint - boundary_derivative) == 0,
    )
    ledger.check(
        "mixed coefficient is load bearing",
        variation.mixed_coefficient != 0
        and variation.mixed_boundary_correction != 0,
    )
    ledger.check(
        "PG3 local half Hessian omits the mixed correction",
        sp.simplify(
            variation.potential_coefficient - variation.local_half_hessian
            - variation.mixed_boundary_correction
        )
        == 0,
    )

    first = sp.Function("u")(radius)
    second = sp.Function("v")(radius)
    green = radial_green_boundary_form(
        first,
        second,
        variation.gradient_coefficient,
        radius,
    )
    operator_difference = sp.simplify(
        first * apply_option_c_radial_hessian(second, profile, radius)
        - second * apply_option_c_radial_hessian(first, profile, radius)
    )
    ledger.check(
        "radial Hessian satisfies the Green identity",
        sp.simplify(operator_difference + sp.diff(green, radius)) == 0,
    )

    log_scale = sp.symbols("s", real=True)
    scaled_family = profile.subs(radius, sp.exp(log_scale) * radius)
    ledger.check(
        "Derrick tangent is r times the radial derivative",
        sp.simplify(
            sp.diff(scaled_family, log_scale).subs(log_scale, 0)
            - derrick_scale_tangent(profile, radius)
        )
        == 0,
    )
    e2, e4 = sp.symbols("E2 E4", positive=True)
    derrick = derrick_scaling_evidence(e2, e4, log_scale)
    ledger.check("Derrick slope is E4 minus E2", derrick.slope_at_origin == e4 - e2)
    ledger.check(
        "stationary Derrick direction is stiff rather than zero",
        derrick.curvature_at_origin.subs(e4, e2) == 2 * e2,
    )

    threshold = option_c_continuum_threshold()
    ledger.check("massless continuum threshold is exact zero", threshold == 0)
    ledger.check(
        "positive box level cannot lie below massless threshold",
        not (sp.Rational(1, 10) < threshold),
    )

    profiles = [
        solve_option_c_hedgehog(outer_radius=outer, sample_points=points)
        for outer, points in ((12.0, 801), (18.0, 1201), (24.0, 1601))
    ]
    slopes = np.asarray([item.shooting_slope for item in profiles])
    coefficients = np.asarray([item.energy_coefficient for item in profiles])
    virial_errors = np.asarray(
        [
            abs(item.two_derivative_energy - item.four_derivative_energy)
            / (item.two_derivative_energy + item.four_derivative_energy)
            for item in profiles
        ]
    )
    for item, virial_error in zip(profiles, virial_errors, strict=True):
        print(
            "PROFILE",
            f"R={item.radius[-1]:.0f}",
            f"slope={item.shooting_slope:.12f}",
            f"B1={item.energy_coefficient:.12f}",
            f"virial={virial_error:.6e}",
            f"tail={item.outer_tail_residual:.6e}",
        )
    ledger.check(
        "Robin-tail shooting slope is domain stable",
        abs(slopes[-1] - slopes[-2]) / slopes[-1] < 2.0e-8,
    )
    ledger.check(
        "energy coefficient converges without a fitted B1 target",
        np.all(np.diff(coefficients) > 0.0)
        and 1.231 < coefficients[-1] < 1.232,
    )
    ledger.check(
        "Derrick imbalance decreases with domain",
        np.all(np.diff(virial_errors) < 0.0) and virial_errors[-1] < 1.0e-4,
    )
    ledger.check(
        "Robin boundary residuals are scale small",
        max(abs(item.outer_tail_residual) for item in profiles) < 2.0e-7,
    )

    stationarity_errors = [
        _finite_difference_stationarity(profiles[-1], stride)
        for stride in (4, 2, 1)
    ]
    print(
        "FD_STATIONARITY",
        " ".join(f"{error:.6e}" for error in stationarity_errors),
    )
    ledger.check(
        "independent finite-difference EOM residual refines",
        stationarity_errors[1] < stationarity_errors[0] / 3.5
        and stationarity_errors[2] < stationarity_errors[1] / 3.5,
    )
    ledger.check(
        "independent finite-difference stationarity is resolved",
        stationarity_errors[-1] < 3.0e-4,
    )

    spectrum_data = [_profile_spectrum(item) for item in profiles]
    spectra = [item[0] for item in spectrum_data]
    lowest = np.asarray([item.eigenvalues[0] for item in spectra])
    for item in spectra:
        print(
            "BOX_SPECTRUM",
            f"R={item.upper_bound:.0f}",
            "eigenvalues=" + ",".join(f"{value:.9f}" for value in item.eigenvalues),
            "nodes=" + ",".join(str(value) for value in item.node_counts),
            f"max_residual={max(item.relative_residuals):.3e}",
        )
    ledger.check(
        "finite-box spectra have Sturm node ordering",
        all(item.node_counts == (0, 1, 2, 3) for item in spectra),
    )
    ledger.check(
        "generalized eigensolver residuals are resolved",
        max(max(item.relative_residuals) for item in spectra) < 2.0e-8,
    )
    ledger.check(
        "no positive box level is below the continuum",
        all(not any(item.below_continuum) for item in spectra),
    )
    ledger.check(
        "lowest box level collapses under domain expansion",
        np.all(np.diff(lowest) < 0.0) and lowest[-1] < 0.35 * lowest[0],
    )
    scaled_levels = lowest * np.asarray((12.0, 18.0, 24.0)) ** 2
    ledger.check(
        "lowest level has finite-wall inverse-square scaling",
        np.max(scaled_levels) / np.min(scaled_levels) < 1.08,
    )

    reference_spectrum, gradient, potential, weight, correction = spectrum_data[0]
    omitted = solve_radial_finite_box_spectrum(
        profiles[0].radius,
        gradient,
        potential - correction,
        weight,
        mode_count=4,
        continuum_threshold=0.0,
    )
    print(
        "MUTATION_LEVELS",
        f"correct={reference_spectrum.eigenvalues[0]:.9f}",
        f"mixed_omitted={omitted.eigenvalues[0]:.9f}",
    )
    ledger.check(
        "omitting the mixed correction changes the load-bearing level",
        abs(omitted.eigenvalues[0] - reference_spectrum.eigenvalues[0])
        / reference_spectrum.eigenvalues[0]
        > 0.05,
    )
    doubled_weight = solve_radial_finite_box_spectrum(
        profiles[0].radius,
        gradient,
        potential,
        2.0 * weight,
        mode_count=4,
        continuum_threshold=0.0,
    )
    ledger.check(
        "kinetic-weight mutation halves generalized eigenvalues",
        np.allclose(
            doubled_weight.eigenvalues,
            np.asarray(reference_spectrum.eigenvalues) / 2.0,
            rtol=2.0e-8,
        ),
    )
    tachyon = solve_radial_finite_box_spectrum(
        profiles[0].radius,
        gradient,
        potential - weight,
        weight,
        mode_count=4,
        continuum_threshold=0.0,
    )
    print(
        "MUTATION_LEVELS",
        f"double_weight={doubled_weight.eigenvalues[0]:.9f}",
        f"negative_shift={tachyon.eigenvalues[0]:.9f}",
    )
    ledger.check(
        "negative-potential mutation crosses the stability threshold",
        tachyon.eigenvalues[0] < 0.0
        and abs(tachyon.eigenvalues[0] - (reference_spectrum.eigenvalues[0] - 1.0))
        < 2.0e-8,
    )

    eigenvalue = sp.Rational(1, 10)
    time_scale, action_scale, energy_scale, background = sp.symbols(
        "nu S E0 epsilon",
        positive=True,
    )
    scale_ledger = classical_mode_scale_ledger(
        eigenvalue,
        time_scale,
        action_scale,
        energy_scale,
        background,
    )
    ledger.check(
        "classical frequency is square root of Hessian eigenvalue",
        scale_ledger.dimensionless_frequency == sp.sqrt(10) / 10,
    )
    ledger.check(
        "one-quantum gap keeps an explicit action scale",
        scale_ledger.one_quantum_gap
        == action_scale * time_scale * sp.sqrt(10) / 10,
    )
    rho = sp.symbols("rho", positive=True)
    ledger.check(
        "gap ratio remains free under time-scale mutation",
        sp.simplify(
            scale_ledger.gap_to_background_ratio.subs(time_scale, rho * time_scale)
            - rho * scale_ledger.gap_to_background_ratio
        )
        == 0,
    )
    ledger.check(
        "squared eigenvalue is not a harmonic gap",
        sp.simplify(eigenvalue - scale_ledger.dimensionless_frequency) != 0,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
