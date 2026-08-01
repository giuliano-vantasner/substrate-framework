from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.tt_angular import (
    axisymmetric_stf_readout,
    axisymmetric_stf_tensor,
    conditional_axisymmetric_stf_power,
    conditional_tt_power,
    frobenius_norm_squared,
    harmonic_stf_third_derivative_average,
    integrated_tt_norm_squared,
    transverse_projector,
    tt_project_symmetric,
    waveform_prefactor_for_quadrupole_convention,
)


def test_arbitrary_axis_axisymmetric_stf_tensor_has_exact_eigenstructure() -> None:
    amplitude = sp.symbols("alpha", real=True)
    axis = sp.Matrix([1, 2, 2])
    normalized = axisymmetric_stf_tensor(amplitude, axis)
    triple = axisymmetric_stf_tensor(amplitude, axis, 3)
    unit_axis = axis / 3
    assert sp.trace(normalized) == 0
    assert sp.simplify(
        normalized * unit_axis - 2 * amplitude * unit_axis / 3
    ) == sp.zeros(3, 1)
    assert sp.simplify(
        frobenius_norm_squared(normalized) - 2 * amplitude**2 / 3
    ) == 0
    assert triple == 3 * normalized
    assert sp.simplify(frobenius_norm_squared(triple) - 6 * amplitude**2) == 0


def test_arbitrary_axis_natural_readout_has_sine_squared_plus_and_zero_cross() -> None:
    amplitude = sp.symbols("alpha", real=True)
    axis = sp.Matrix([1, 2, 2])
    direction = sp.Matrix([2, -1, 2])
    readout = axisymmetric_stf_readout(amplitude, axis, direction, 3)
    expected_sine_squared = sp.Rational(65, 81)
    assert readout.inclination_sine_squared == expected_sine_squared
    assert sp.simplify(
        readout.normalized_plus_coordinate
        - 3 * amplitude * expected_sine_squared / sp.sqrt(2)
    ) == 0
    assert readout.normalized_cross_coordinate == 0
    assert sp.simplify(
        readout.conventional_plus_readout
        - 3 * amplitude * expected_sine_squared / 2
    ) == 0
    assert readout.conventional_cross_readout == 0


def test_arbitrary_axis_readout_has_exact_axis_null_and_rotation_covariance() -> None:
    amplitude = sp.symbols("alpha", real=True)
    axis = sp.Matrix([1, 2, 2])
    null = axisymmetric_stf_readout(amplitude, axis, 2 * axis)
    assert null.inclination_sine_squared == 0
    assert null.projected_tensor == sp.zeros(3)
    rotated = axisymmetric_stf_readout(amplitude, [0, 0, 1], [1, 0, 0])
    assert rotated.projected_tensor == sp.diag(0, -amplitude / 2, amplitude / 2)
    assert rotated.normalized_cross_coordinate == 0


def test_axisymmetric_conditional_power_is_convention_invariant() -> None:
    derivative, coupling = sp.symbols("alpha3 G", nonzero=True, real=True)
    normalized = conditional_axisymmetric_stf_power(derivative, coupling, 1)
    triple = conditional_axisymmetric_stf_power(derivative, coupling, 3)
    assert sp.simplify(normalized - 2 * coupling * derivative**2 / 15) == 0
    assert triple == normalized


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: axisymmetric_stf_tensor(1, [0, 0, 0]), "symmetry_axis"),
        (lambda: axisymmetric_stf_tensor(1, [1, 0, 0], 0), "quadrupole_scale"),
        (
            lambda: axisymmetric_stf_readout(1, [1, 0, 0], [0, 0, 0]),
            "direction",
        ),
        (
            lambda: conditional_axisymmetric_stf_power(1, 0),
            "gravitational_coupling",
        ),
    ],
)
def test_invalid_axisymmetric_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()


def test_transverse_projector_and_tt_projection_have_exact_properties() -> None:
    direction = sp.Matrix([2, 3, 6])
    tensor = sp.Matrix([[3, 2, 1], [2, -1, 4], [1, 4, 5]])
    projector = transverse_projector(direction)
    projected = tt_project_symmetric(tensor, direction)
    assert sp.simplify(projector**2 - projector) == sp.zeros(3)
    assert sp.simplify(projector * direction) == sp.zeros(3, 1)
    assert projected == projected.T
    assert sp.trace(projected) == 0
    assert sp.simplify(projected * direction) == sp.zeros(3, 1)


def test_tt_projection_and_angular_integral_kill_pure_trace() -> None:
    tensor = sp.Matrix([[2, 1, 0], [1, -3, 4], [0, 4, 5]])
    shifted = tensor + 7 * sp.eye(3)
    assert tt_project_symmetric(shifted, [1, 2, 2]) == tt_project_symmetric(
        tensor, [1, 2, 2]
    )
    assert integrated_tt_norm_squared(shifted) == integrated_tt_norm_squared(tensor)
    assert integrated_tt_norm_squared(11 * sp.eye(3)) == 0


def test_integrated_tt_contraction_has_eight_pi_over_five_coefficient() -> None:
    tensor = sp.diag(1, -1, 0)
    assert frobenius_norm_squared(tensor) == 2
    assert integrated_tt_norm_squared(tensor) == sp.Rational(16, 5) * sp.pi


def test_conditional_power_keeps_waveform_and_flux_inputs_explicit() -> None:
    gravitational_coupling = sp.symbols("G", positive=True)
    third_derivative = sp.diag(1, -1, 0)
    normalized = conditional_tt_power(
        third_derivative,
        2 * gravitational_coupling,
        1 / (32 * sp.pi * gravitational_coupling),
    )
    assert normalized == gravitational_coupling / 5 * frobenius_norm_squared(
        third_derivative
    )


def test_triple_normalized_quadrupole_requires_factor_nine_power_conversion() -> None:
    gravitational_coupling = sp.symbols("G", positive=True)
    normalized_third = sp.diag(1, -1, 0)
    triple_third = 3 * normalized_third
    normalized_wave = 2 * gravitational_coupling
    triple_wave = waveform_prefactor_for_quadrupole_convention(normalized_wave, 3)
    flux = 1 / (32 * sp.pi * gravitational_coupling)
    normalized_power = conditional_tt_power(normalized_third, normalized_wave, flux)
    triple_power = conditional_tt_power(triple_third, triple_wave, flux)
    source_power = conditional_tt_power(triple_third, normalized_wave, flux)
    assert triple_wave == 2 * gravitational_coupling / 3
    assert triple_power == normalized_power
    assert source_power == 9 * normalized_power
    assert triple_power == gravitational_coupling / 45 * frobenius_norm_squared(
        triple_third
    )


def test_harmonic_average_matches_direct_cycle_integration() -> None:
    time, frequency = sp.symbols("t omega", positive=True, real=True)
    cosine = sp.diag(2, -2, 0)
    sine = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    harmonic = cosine * sp.cos(frequency * time) + sine * sp.sin(frequency * time)
    third = harmonic.diff(time, 3)
    direct = sp.simplify(
        frequency
        / (2 * sp.pi)
        * sp.integrate(
            frobenius_norm_squared(third),
            (time, 0, 2 * sp.pi / frequency),
        )
    )
    exact = harmonic_stf_third_derivative_average(cosine, sine, frequency)
    assert sp.simplify(direct - exact) == 0


def test_circular_binary_convention_invariance() -> None:
    time = sp.symbols("t", real=True)
    mass, radius, frequency, gravitational_coupling = sp.symbols(
        "mu a omega G", positive=True, real=True
    )
    separation = sp.Matrix(
        [radius * sp.cos(frequency * time), radius * sp.sin(frequency * time), 0]
    )
    normalized = sp.simplify(
        mass * (separation * separation.T - radius**2 * sp.eye(3) / 3)
    )
    normalized_third = sp.simplify(normalized.diff(time, 3))
    assert sp.trigsimp(frobenius_norm_squared(normalized_third)) == (
        32 * mass**2 * radius**4 * frequency**6
    )
    normalized_power = conditional_tt_power(
        normalized_third,
        2 * gravitational_coupling,
        1 / (32 * sp.pi * gravitational_coupling),
    )
    triple_power = conditional_tt_power(
        3 * normalized_third,
        2 * gravitational_coupling / 3,
        1 / (32 * sp.pi * gravitational_coupling),
    )
    expected = (
        sp.Rational(32, 5)
        * gravitational_coupling
        * mass**2
        * radius**4
        * frequency**6
    )
    assert sp.trigsimp(normalized_power) == expected
    assert sp.trigsimp(triple_power) == expected


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: transverse_projector([0, 0, 0]), "nonzero"),
        (lambda: transverse_projector([1, 2]), "three components"),
        (lambda: tt_project_symmetric(sp.eye(2), [1, 0, 0]), "3 by 3"),
        (
            lambda: tt_project_symmetric(
                [[1, 1, 0], [0, 1, 0], [0, 0, 1]], [1, 0, 0]
            ),
            "symmetric",
        ),
        (
            lambda: waveform_prefactor_for_quadrupole_convention(1, 0),
            "nonzero",
        ),
    ],
)
def test_invalid_tt_inputs_are_rejected(call, message) -> None:
    with pytest.raises(ValueError, match=message):
        call()
