from __future__ import annotations

import pytest
import sympy as sp
import substrate_framework as framework

from substrate_framework.conditional_triaxial_radiation import (
    conditional_scaled_stf_power,
    conditional_scaled_stf_waveform,
)
from substrate_framework.rigid_quadrupole_rotation import (
    axisymmetric_stf_from_transverse_eigenvalue,
    rigid_axisymmetric_stf_rotation,
    rodrigues_rotation_matrix,
    symmetric_tensor_characteristic_polynomial,
    tilted_axisymmetric_stf_rotation_about_z,
)
from substrate_framework.tt_angular import frobenius_norm_squared


def test_rigid_rotation_public_api_is_exported() -> None:
    assert framework.RigidAxisymmetricSTFRotation is not None
    assert framework.rigid_axisymmetric_stf_rotation is rigid_axisymmetric_stf_rotation
    assert framework.rodrigues_rotation_matrix is rodrigues_rotation_matrix
    assert (
        framework.symmetric_tensor_characteristic_polynomial
        is symmetric_tensor_characteristic_polynomial
    )


def test_rodrigues_x_convention_matches_the_source_implementation() -> None:
    angle = sp.symbols("a", real=True)
    expected = sp.Matrix(
        [
            [1, 0, 0],
            [0, sp.cos(angle), -sp.sin(angle)],
            [0, sp.sin(angle), sp.cos(angle)],
        ]
    )
    rotation = rodrigues_rotation_matrix([1, 0, 0], angle)
    assert rotation == expected
    assert sp.simplify(rotation.T * rotation) == sp.eye(3)
    assert sp.simplify(rotation.det()) == 1


def test_rotated_full_tensor_remains_axisymmetric_with_repeated_eigenvalue() -> None:
    time = sp.symbols("t", real=True)
    q, omega, scale, spectral = sp.symbols(
        "q Omega s lambda", nonzero=True, real=True
    )
    result = rigid_axisymmetric_stf_rotation(
        q,
        omega,
        time,
        rotation_axis=[1, 0, 0],
        body_symmetry_axis=[0, 0, 1],
        quadrupole_scale=scale,
    )
    expected_polynomial = (spectral - scale * q) ** 2 * (
        spectral + 2 * scale * q
    )
    assert sp.trigsimp(
        sp.expand(
            symmetric_tensor_characteristic_polynomial(result.tensor, spectral)
            - expected_polynomial
        )
    ) == 0
    assert sp.simplify(
        result.tensor * result.instantaneous_symmetry_axis
        + 2 * scale * q * result.instantaneous_symmetry_axis
    ) == sp.zeros(3, 1)
    assert sp.simplify(sp.trace(result.tensor)) == 0


def test_perpendicular_source_components_have_positive_implemented_yz_sign() -> None:
    time = sp.symbols("t", real=True)
    q, omega, scale = sp.symbols("q Omega s", real=True)
    angle = omega * time
    result = rigid_axisymmetric_stf_rotation(
        q,
        omega,
        time,
        rotation_axis=[1, 0, 0],
        body_symmetry_axis=[0, 0, 1],
        quadrupole_scale=scale,
    )
    expected = scale * q * sp.Matrix(
        [
            [1, 0, 0],
            [0, 1 - 3 * sp.sin(angle) ** 2, 3 * sp.sin(angle) * sp.cos(angle)],
            [0, 3 * sp.sin(angle) * sp.cos(angle), -2 + 3 * sp.sin(angle) ** 2],
        ]
    )
    assert sp.simplify(result.tensor - expected) == sp.zeros(3)
    assert sp.simplify(result.tensor[1, 2] - 3 * scale * q * sp.sin(2 * angle) / 2) == 0


def test_aligned_rotation_is_constant_and_perpendicular_is_exactly_twice_frequency() -> None:
    time = sp.symbols("t", real=True)
    q, omega, scale = sp.symbols("q Omega s", nonzero=True, real=True)
    aligned = rigid_axisymmetric_stf_rotation(
        q,
        omega,
        time,
        rotation_axis=[0, 0, 1],
        body_symmetry_axis=[0, 0, 1],
        quadrupole_scale=scale,
    )
    perpendicular = rigid_axisymmetric_stf_rotation(
        q,
        omega,
        time,
        rotation_axis=[1, 0, 0],
        body_symmetry_axis=[0, 0, 1],
        quadrupole_scale=scale,
    )
    assert aligned.tensor == aligned.body_tensor
    assert aligned.third_derivative == sp.zeros(3)
    assert sp.simplify(
        perpendicular.tensor.subs(time, time + sp.pi / omega)
        - perpendicular.tensor
    ) == sp.zeros(3)
    assert sp.simplify(
        perpendicular.tensor.subs(time, time + sp.pi / (2 * omega))
        - perpendicular.tensor
    ) != sp.zeros(3)
    assert sp.simplify(perpendicular.third_derivative) != sp.zeros(3)


def test_perpendicular_derivative_norms_eigenvalues_and_power_are_exact() -> None:
    time = sp.symbols("t", real=True)
    q, omega, scale, coupling, spectral = sp.symbols(
        "q Omega s G lambda", nonzero=True, real=True
    )
    result = rigid_axisymmetric_stf_rotation(
        q,
        omega,
        time,
        rotation_axis=[1, 0, 0],
        body_symmetry_axis=[0, 0, 1],
        quadrupole_scale=scale,
    )
    assert sp.trigsimp(frobenius_norm_squared(result.second_derivative)) == (
        72 * scale**2 * q**2 * omega**4
    )
    assert sp.trigsimp(frobenius_norm_squared(result.third_derivative)) == (
        288 * scale**2 * q**2 * omega**6
    )
    derivative_polynomial = symmetric_tensor_characteristic_polynomial(
        result.third_derivative, spectral
    )
    assert sp.simplify(
        sp.expand(
            sp.trigsimp(derivative_polynomial)
            - spectral * (spectral**2 - 144 * scale**2 * q**2 * omega**6)
        )
    ) == 0
    assert conditional_scaled_stf_power(
        result.third_derivative, coupling, scale
    ) == 288 * coupling * q**2 * omega**6 / 5


def test_rotation_axis_readout_is_circular_but_conditional() -> None:
    time = sp.symbols("t", real=True)
    q, omega, scale, coupling, distance = sp.symbols(
        "q Omega s G R", nonzero=True, real=True
    )
    result = rigid_axisymmetric_stf_rotation(
        q,
        omega,
        time,
        rotation_axis=[1, 0, 0],
        body_symmetry_axis=[0, 0, 1],
        quadrupole_scale=scale,
    )
    waveform = conditional_scaled_stf_waveform(
        result.second_derivative,
        [1, 0, 0],
        coupling,
        distance,
        scale,
        [0, 1, 0],
    )
    angle = 2 * omega * time
    assert sp.simplify(
        waveform.conventional_plus
        + 12 * coupling * q * omega**2 * sp.cos(angle) / distance
    ) == 0
    assert sp.simplify(
        waveform.conventional_cross
        + 12 * coupling * q * omega**2 * sp.sin(angle) / distance
    ) == 0
    radius_squared = sp.trigsimp(
        waveform.conventional_plus**2 + waveform.conventional_cross**2
    )
    assert radius_squared == 144 * coupling**2 * q**2 * omega**4 / distance**2


def test_generic_tilt_contains_fundamental_and_twice_frequency_channels() -> None:
    time = sp.symbols("t", real=True)
    q, omega, scale, tilt = sp.symbols("q Omega s beta", nonzero=True, real=True)
    result = tilted_axisymmetric_stf_rotation_about_z(
        q, omega, time, tilt, scale
    )
    angle = omega * time
    assert sp.simplify(
        result.tensor[0, 2]
        + 3 * scale * q * sp.sin(tilt) * sp.cos(tilt) * sp.cos(angle)
    ) == 0
    assert sp.simplify(
        result.tensor[0, 1]
        + 3 * scale * q * sp.sin(tilt) ** 2 * sp.sin(2 * angle) / 2
    ) == 0
    expected_norm = (
        18
        * scale**2
        * q**2
        * omega**6
        * sp.sin(tilt) ** 2
        * (sp.cos(tilt) ** 2 + 16 * sp.sin(tilt) ** 2)
    )
    assert sp.trigsimp(
        frobenius_norm_squared(result.third_derivative) - expected_norm
    ) == 0
    assert result.third_derivative.subs(tilt, 0) == sp.zeros(3)
    assert sp.trigsimp(
        frobenius_norm_squared(result.third_derivative).subs(tilt, sp.pi / 2)
    ) == 288 * scale**2 * q**2 * omega**6


def test_zero_anisotropy_or_speed_breaks_the_nonzero_derivative_verdict() -> None:
    time = sp.symbols("t", real=True)
    q, omega = sp.symbols("q Omega", real=True)
    result = rigid_axisymmetric_stf_rotation(
        q,
        omega,
        time,
        rotation_axis=[1, 0, 0],
        body_symmetry_axis=[0, 0, 1],
    )
    assert result.third_derivative.subs(q, 0) == sp.zeros(3)
    assert result.third_derivative.subs(omega, 0) == sp.zeros(3)
    triaxial_body = sp.diag(q, 0, -q)
    spectral = sp.symbols("lambda")
    assert sp.simplify(
        symmetric_tensor_characteristic_polynomial(triaxial_body, spectral)
        - spectral * (spectral - q) * (spectral + q)
    ) == 0


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: rodrigues_rotation_matrix([0, 0, 0], 1), "axis"),
        (
            lambda: axisymmetric_stf_from_transverse_eigenvalue(1, [0, 0, 1], 0),
            "quadrupole_scale",
        ),
        (
            lambda: rigid_axisymmetric_stf_rotation(
                1,
                1,
                sp.Symbol("t") + 1,
                rotation_axis=[1, 0, 0],
                body_symmetry_axis=[0, 0, 1],
            ),
            "time",
        ),
        (
            lambda: symmetric_tensor_characteristic_polynomial(sp.eye(2), sp.Symbol("x")),
            "3 by 3",
        ),
    ],
)
def test_invalid_rigid_rotation_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
