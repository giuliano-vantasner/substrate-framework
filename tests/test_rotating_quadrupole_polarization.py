from __future__ import annotations

import pytest
import sympy as sp
import substrate_framework as framework

from substrate_framework.rigid_quadrupole_rotation import (
    rigid_axisymmetric_stf_rotation,
)
from substrate_framework.rotating_quadrupole_polarization import (
    PerpendicularRotationTTPolarization,
    conditional_perpendicular_rotation_polarization,
    perpendicular_axisymmetric_stf_second_derivative,
)


def _symbols() -> tuple[sp.Symbol, ...]:
    return sp.symbols("q Omega psi iota phi alpha G R", nonzero=True, real=True)


def test_rotating_polarization_public_api_is_exported() -> None:
    assert framework.PerpendicularRotationTTPolarization is PerpendicularRotationTTPolarization
    assert (
        framework.conditional_perpendicular_rotation_polarization
        is conditional_perpendicular_rotation_polarization
    )
    assert (
        framework.perpendicular_axisymmetric_stf_second_derivative
        is perpendicular_axisymmetric_stf_second_derivative
    )


def test_phase_derivative_matches_the_time_differentiated_rotation() -> None:
    time = sp.Symbol("t", real=True)
    q, omega, _, _, _, _, _, _ = _symbols()
    scale = sp.Symbol("s", nonzero=True, real=True)
    rotated = rigid_axisymmetric_stf_rotation(
        q,
        omega,
        time,
        rotation_axis=[1, 0, 0],
        body_symmetry_axis=[0, 0, 1],
        quadrupole_scale=scale,
    )
    phase_route = perpendicular_axisymmetric_stf_second_derivative(
        q,
        omega,
        omega * time,
        scale,
    )
    assert sp.simplify(phase_route - rotated.second_derivative) == sp.zeros(3)


def test_natural_meridian_readout_has_exact_inclination_ellipse() -> None:
    q, omega, phase, inclination, azimuth, _, coupling, distance = _symbols()
    result = conditional_perpendicular_rotation_polarization(
        q,
        omega,
        phase,
        inclination,
        coupling,
        distance,
        observer_azimuth=azimuth,
    )
    harmonic = 2 * (phase - azimuth)
    common = 12 * coupling * q * omega**2 / distance
    expected_plus = -common * (1 + sp.cos(inclination) ** 2) * sp.cos(harmonic) / 2
    expected_cross = -common * sp.cos(inclination) * sp.sin(harmonic)
    assert sp.trigsimp(result.waveform.conventional_plus - expected_plus) == 0
    assert sp.trigsimp(result.waveform.conventional_cross - expected_cross) == 0
    assert result.common_waveform_scale == common


def test_coefficient_matrix_derives_temporal_rank_and_ellipse_axes() -> None:
    q, omega, phase, inclination, azimuth, _, coupling, distance = _symbols()
    result = conditional_perpendicular_rotation_polarization(
        q,
        omega,
        phase,
        inclination,
        coupling,
        distance,
        observer_azimuth=azimuth,
    )
    common = result.common_waveform_scale
    cosine = sp.cos(inclination)
    expected = sp.diag(-common * (1 + cosine**2) / 2, -common * cosine)
    assert sp.trigsimp(result.coefficient_matrix - expected) == sp.zeros(2)
    expected_gram = sp.diag(
        common**2 * (1 + cosine**2) ** 2 / 4,
        common**2 * cosine**2,
    )
    assert sp.trigsimp(result.phase_gram_matrix - expected_gram) == sp.zeros(2)
    assert sp.trigsimp(sp.expand_trig(
        result.coefficient_determinant
        - common**2 * cosine * (1 + cosine**2) / 2
    )) == 0


def test_transverse_frame_rotation_preserves_ellipse_singular_values() -> None:
    q, omega, phase, inclination, azimuth, frame, coupling, distance = _symbols()
    base = conditional_perpendicular_rotation_polarization(
        q,
        omega,
        phase,
        inclination,
        coupling,
        distance,
        observer_azimuth=azimuth,
    )
    rotated = conditional_perpendicular_rotation_polarization(
        q,
        omega,
        phase,
        inclination,
        coupling,
        distance,
        observer_azimuth=azimuth,
        transverse_frame_angle=frame,
    )
    coordinate_rotation = sp.Matrix(
        [
            [sp.cos(2 * frame), sp.sin(2 * frame)],
            [-sp.sin(2 * frame), sp.cos(2 * frame)],
        ]
    )
    assert rotated.coefficient_matrix == coordinate_rotation * base.coefficient_matrix
    assert rotated.phase_gram_matrix == base.phase_gram_matrix
    assert rotated.coefficient_determinant == base.coefficient_determinant


def test_axis_edge_and_generic_views_are_circular_linear_and_elliptical() -> None:
    q, omega, phase, _, _, _, coupling, distance = _symbols()
    axis = conditional_perpendicular_rotation_polarization(
        q, omega, phase, 0, coupling, distance
    )
    edge = conditional_perpendicular_rotation_polarization(
        q, omega, phase, sp.pi / 2, coupling, distance
    )
    generic = conditional_perpendicular_rotation_polarization(
        q, omega, phase, sp.pi / 3, coupling, distance
    )
    assert sp.simplify(axis.phase_gram_matrix[0, 0] - axis.phase_gram_matrix[1, 1]) == 0
    assert sp.simplify(axis.coefficient_determinant) != 0
    assert sp.simplify(edge.coefficient_determinant) == 0
    assert sp.simplify(edge.coefficient_matrix[0, 0]) != 0
    assert sp.simplify(edge.coefficient_matrix[1, 1]) == 0
    assert sp.simplify(generic.coefficient_determinant) != 0
    assert sp.simplify(
        generic.phase_gram_matrix[0, 0] - generic.phase_gram_matrix[1, 1]
    ) != 0


def test_source_sample_direction_is_rank_two_but_not_circular() -> None:
    q, omega, phase, _, _, _, coupling, distance = _symbols()
    inclination = sp.acos(1 / sp.sqrt(3))
    result = conditional_perpendicular_rotation_polarization(
        q,
        omega,
        phase,
        inclination,
        coupling,
        distance,
        observer_azimuth=sp.pi / 4,
    )
    common = result.common_waveform_scale
    assert sp.simplify(result.coefficient_determinant - 2 * common**2 / (3 * sp.sqrt(3))) == 0
    major = sp.simplify(result.phase_gram_matrix[0, 0])
    minor = sp.simplify(result.phase_gram_matrix[1, 1])
    assert sp.simplify(minor / major - sp.Rational(3, 4)) == 0


def test_fixed_phase_ratio_cancels_scale_but_fixed_time_ratio_depends_on_speed() -> None:
    q, omega, phase, inclination, _, _, coupling, distance = _symbols()
    result = conditional_perpendicular_rotation_polarization(
        q,
        omega,
        phase,
        inclination,
        coupling,
        distance,
    )
    ratio = sp.simplify(
        result.waveform.conventional_cross / result.waveform.conventional_plus
    )
    assert not ({q, omega, coupling, distance} & ratio.free_symbols)
    time = sp.Symbol("t", nonzero=True, real=True)
    fixed_time_ratio = ratio.subs(phase, omega * time)
    assert sp.simplify(sp.diff(fixed_time_ratio, omega)) != 0
    assert ratio.has(sp.tan(2 * phase))
    pole_phase = sp.pi / 4
    assert sp.simplify(
        result.waveform.conventional_plus.subs(phase, pole_phase)
    ) == 0
    assert sp.simplify(
        result.waveform.conventional_cross.subs(phase, pole_phase)
    ) != 0


def test_quadrupole_convention_scale_cancels_from_conditional_waveform() -> None:
    q, omega, phase, inclination, azimuth, _, coupling, distance = _symbols()
    normalized = conditional_perpendicular_rotation_polarization(
        q,
        omega,
        phase,
        inclination,
        coupling,
        distance,
        observer_azimuth=azimuth,
        quadrupole_scale=1,
    )
    triple = conditional_perpendicular_rotation_polarization(
        q,
        omega,
        phase,
        inclination,
        coupling,
        distance,
        observer_azimuth=azimuth,
        quadrupole_scale=3,
    )
    assert triple.source_second_derivative == 3 * normalized.source_second_derivative
    assert triple.waveform.waveform_tensor == normalized.waveform.waveform_tensor
    assert triple.coefficient_matrix == normalized.coefficient_matrix


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: perpendicular_axisymmetric_stf_second_derivative(1, 1, 0, 0),
            "quadrupole_scale",
        ),
        (
            lambda: conditional_perpendicular_rotation_polarization(
                1, 1, 0, 0, 1, 0
            ),
            "distance",
        ),
    ],
)
def test_invalid_rotating_polarization_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
