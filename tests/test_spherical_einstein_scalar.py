from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.spherical_einstein_scalar import (
    regular_origin_sine_gordon_data,
    sine_gordon_gravity_scaling,
    static_spherical_sine_gordon_reduction,
)


def _symbolic_reduction():
    x = sp.symbols("x", positive=True)
    omega, alpha = sp.symbols("Omega alpha", positive=True)
    amplitude = sp.Function("a", real=True)(x)
    mass = sp.Function("m", real=True)(x)
    lapse_exponent = sp.Function("Phi", real=True)(x)
    return x, static_spherical_sine_gordon_reduction(
        x, amplitude, mass, lapse_exponent, omega, alpha
    )


def test_nondimensionalization_has_declared_physical_scales_and_dimensions() -> None:
    kappa, field_scale, mu = sp.symbols("kappa F mu", positive=True)
    u, radius, time, mass = sp.symbols("u r t M", real=True)
    result = sine_gordon_gravity_scaling(
        kappa, field_scale, mu, u, radius, time, mass
    )
    assert result.physical_field == field_scale * u
    assert result.physical_potential == field_scale**2 * mu**2 * (1 - sp.cos(u))
    assert result.dimensionless_radius == mu * radius
    assert result.dimensionless_time == mu * time
    assert result.dimensionless_mass == mu * mass
    assert result.dimensionless_coupling == field_scale**2 * kappa
    dimensions = dict(result.mass_dimensions)
    assert dimensions["physical_potential"] == 4
    assert all(
        dimensions[name] == 0
        for name in (
            "dimensionless_radius",
            "dimensionless_time",
            "dimensionless_mass",
            "dimensionless_coupling",
        )
    )


def test_averaged_stress_and_areal_constraints_match_canonical_reduction() -> None:
    x, result = _symbolic_reduction()
    a = result.amplitude
    omega = result.frequency
    lapse = result.lapse
    f = result.radial_metric_function
    derivative = sp.diff(a, x)
    assert result.stress.energy_density == sp.simplify(
        omega**2 * a**2 / (4 * lapse**2)
        + f * derivative**2 / 4
        + 1
        - sp.besselj(0, a)
    )
    assert result.stress.radial_pressure == sp.simplify(
        f * derivative**2 / 4
        + omega**2 * a**2 / (4 * lapse**2)
        - (1 - sp.besselj(0, a))
    )
    assert result.mass_constraint_residual == sp.simplify(
        sp.diff(result.mass, x)
        - result.dimensionless_coupling * x**2 * result.stress.energy_density / 2
    )
    assert result.lapse_constraint_residual == sp.simplify(
        sp.diff(result.lapse_exponent, x)
        - (
            result.mass
            + result.dimensionless_coupling
            * x**3
            * result.stress.radial_pressure
            / 2
        )
        / (x * (x - 2 * result.mass))
    )


def test_averaged_conservation_is_exactly_the_projected_scalar_equation() -> None:
    _x, result = _symbolic_reduction()
    assert result.conservation_identity_residual == 0
    assert sp.simplify(result.conservation_residual - result.conservation_factor) == 0


def test_conservation_factor_is_sensitive_to_load_bearing_mutations() -> None:
    x, result = _symbolic_reduction()
    a = result.amplitude
    f = result.radial_metric_function
    correct = result.scalar_equation_residual
    wrong_bessel_sign = sp.simplify(correct + 4 * sp.besselj(1, a) / f)
    wrong_radial_factor = sp.simplify(correct - sp.diff(a, x) / x)
    assert sp.simplify(
        result.conservation_residual - f * sp.diff(a, x) * wrong_bessel_sign / 2
    ) != 0
    assert sp.simplify(
        result.conservation_residual - f * sp.diff(a, x) * wrong_radial_factor / 2
    ) != 0


def test_discarded_harmonics_prevent_pointwise_full_pde_promotion() -> None:
    x, result = _symbolic_reduction()
    a = result.amplitude
    assert result.discarded_scalar_third_harmonic == 2 * sp.besselj(3, a)
    amplitude_symbol = sp.symbols("A", real=True)
    assert sp.series(2 * sp.besselj(3, amplitude_symbol), amplitude_symbol, 0, 5) == (
        amplitude_symbol**3 / 24 + sp.Order(amplitude_symbol**5)
    )
    expected_stress_harmonic = (
        -result.frequency**2 * a**2 / (4 * result.lapse**2)
        + result.radial_metric_function * sp.diff(a, x) ** 2 / 4
        + 2 * sp.besselj(2, a)
    )
    assert result.pointwise_energy_density_second_harmonic == sp.simplify(
        expected_stress_harmonic
    )
    assert result.pointwise_energy_density_second_harmonic != 0


def test_flat_and_vacuum_limits_are_explicit() -> None:
    x = sp.symbols("x", positive=True)
    omega = sp.symbols("Omega", positive=True)
    a = sp.Function("a", real=True)(x)
    flat = static_spherical_sine_gordon_reduction(x, a, 0, 0, omega, 0)
    assert flat.radial_metric_function == 1
    assert flat.mass_constraint_residual == 0
    assert flat.lapse_constraint_residual == 0
    assert flat.scalar_equation_residual == sp.simplify(
        sp.diff(a, x, 2)
        + 2 * sp.diff(a, x) / x
        + omega**2 * a
        - 2 * sp.besselj(1, a)
    )
    vacuum = static_spherical_sine_gordon_reduction(x, 0, 0, 0, omega, 0)
    assert vacuum.stress.energy_density == 0
    assert vacuum.scalar_equation_residual == 0
    assert vacuum.discarded_scalar_third_harmonic == 0
    assert vacuum.pointwise_energy_density_second_harmonic == 0


def test_regular_origin_coefficients_cancel_singular_limits() -> None:
    amplitude, phi_zero, omega, alpha = sp.symbols(
        "A Phi0 Omega alpha", real=True, positive=True
    )
    result = regular_origin_sine_gordon_data(amplitude, phi_zero, omega, alpha)
    expected_second = (
        2 * sp.besselj(1, amplitude)
        - omega**2 * amplitude * sp.exp(-2 * phi_zero)
    ) / 3
    assert result.amplitude_second_derivative == expected_second
    assert sp.simplify(
        result.mass_cubic_coefficient - alpha * result.central_energy_density / 6
    ) == 0
    assert sp.simplify(
        result.lapse_second_derivative
        - alpha
        * (result.central_energy_density / 6 + result.central_radial_pressure / 2)
    ) == 0
    radial_limit = sp.simplify(
        3 * result.amplitude_second_derivative
        + omega**2 * amplitude * sp.exp(-2 * phi_zero)
        - 2 * sp.besselj(1, amplitude)
    )
    assert radial_limit == 0


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: sine_gordon_gravity_scaling(1.0, 1, 1, 0, 0, 0, 0),
            "gravitational_coupling",
        ),
        (
            lambda: static_spherical_sine_gordon_reduction(
                sp.Symbol("x", real=True), 0, 0, 0, 1, 0
            ),
            "radius",
        ),
        (
            lambda: static_spherical_sine_gordon_reduction(
                sp.Symbol("x", positive=True), 0, 0, 0, 0, 0
            ),
            "frequency",
        ),
        (
            lambda: regular_origin_sine_gordon_data(1, 0, 1, -1),
            "dimensionless_coupling",
        ),
    ],
)
def test_exact_input_guards(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
