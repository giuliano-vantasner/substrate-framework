from __future__ import annotations

import numpy as np
import pytest
import sympy as sp
import substrate_framework as framework

from substrate_framework.conditional_triaxial_radiation import (
    conditional_real_m2_natural_axis_waveform,
    conditional_real_m2_power,
    conditional_scaled_stf_power,
    conditional_scaled_stf_waveform,
    real_m2_triple_stf_tensor,
)
from substrate_framework.triaxial_l2 import (
    real_l2_tt_readout,
    temporal_coefficient_rank,
)


def test_scaled_waveform_is_convention_invariant() -> None:
    amplitude, coupling, distance = sp.symbols("q G R", nonzero=True, real=True)
    normalized = sp.diag(amplitude, -amplitude, 0)
    triple = 3 * normalized
    normalized_wave = conditional_scaled_stf_waveform(
        normalized, [0, 0, 1], coupling, distance, 1, [1, 0, 0]
    )
    triple_wave = conditional_scaled_stf_waveform(
        triple, [0, 0, 1], coupling, distance, 3, [1, 0, 0]
    )
    assert triple_wave.waveform_tensor == normalized_wave.waveform_tensor
    assert triple_wave.conventional_plus == normalized_wave.conventional_plus
    assert normalized_wave.conventional_plus == 2 * coupling * amplitude / distance
    assert normalized_wave.conventional_cross == 0


def test_conditional_triaxial_public_api_is_exported() -> None:
    assert framework.ConditionalScaledSTFWaveform is not None
    assert framework.conditional_scaled_stf_waveform is conditional_scaled_stf_waveform
    assert framework.conditional_scaled_stf_power is conditional_scaled_stf_power
    assert framework.conditional_real_m2_power is conditional_real_m2_power
    assert framework.real_m2_triple_stf_tensor is real_m2_triple_stf_tensor


def test_scaled_power_is_convention_invariant_and_rejects_factor_nine_error() -> None:
    amplitude, coupling = sp.symbols("q3 G", nonzero=True, real=True)
    normalized = sp.diag(amplitude, -amplitude, 0)
    triple = 3 * normalized
    normalized_power = conditional_scaled_stf_power(normalized, coupling, 1)
    triple_power = conditional_scaled_stf_power(triple, coupling, 3)
    wrong_power = conditional_scaled_stf_power(triple, coupling, 1)
    assert normalized_power == 2 * coupling * amplitude**2 / 5
    assert triple_power == normalized_power
    assert wrong_power == 9 * triple_power


def test_real_m2_natural_axis_has_exact_triple_waveform_and_power() -> None:
    cosine2, sine2, cosine3, sine3, coupling, distance = sp.symbols(
        "q_c2 q_s2 q_c3 q_s3 G R", nonzero=True, real=True
    )
    waveform = conditional_real_m2_natural_axis_waveform(
        cosine2, sine2, coupling, distance
    )
    assert waveform.conventional_plus == 2 * coupling * cosine2 / (3 * distance)
    assert waveform.conventional_cross == 2 * coupling * sine2 / (3 * distance)
    assert conditional_real_m2_power(cosine3, sine3, coupling) == (
        2 * coupling * (cosine3**2 + sine3**2) / 45
    )


def test_fixed_orientation_can_have_two_nonzero_coordinates_but_rank_one() -> None:
    tensor = sp.diag(2, -1, -1)
    readout = real_l2_tt_readout(tensor, [1, 1, 1], [0, 0, 1])
    plus = readout.conventional_plus_readout
    cross = readout.conventional_cross_readout
    assert plus != 0 and cross != 0
    magnitude = sp.sqrt(plus**2 + cross**2)
    cosine_two_angle = sp.simplify(plus / magnitude)
    sine_two_angle = sp.simplify(cross / magnitude)
    rotated_cross = sp.simplify(
        -sine_two_angle * plus + cosine_two_angle * cross
    )
    assert rotated_cross == 0

    time = np.linspace(0.0, 2.0 * np.pi, 257, endpoint=False)
    fixed = np.column_stack(
        (float(plus) * np.cos(time), float(cross) * np.cos(time))
    )
    assert temporal_coefficient_rank(fixed) == 1


def test_two_real_m2_traces_separate_rank_one_and_circular_rank_two() -> None:
    time = np.linspace(0.0, 2.0 * np.pi, 257, endpoint=False)
    proportional = np.column_stack((np.cos(time), -2.0 * np.cos(time)))
    quadrature = np.column_stack((np.cos(time), np.sin(time)))
    assert temporal_coefficient_rank(proportional) == 1
    assert temporal_coefficient_rank(quadrature) == 2
    assert np.allclose(np.sum(quadrature**2, axis=1), 1.0)


def test_real_m2_tensor_is_symmetric_trace_free_with_exact_norm() -> None:
    cosine, sine = sp.symbols("q_c q_s", real=True)
    tensor = real_m2_triple_stf_tensor(cosine, sine)
    assert tensor == tensor.T
    assert sp.trace(tensor) == 0
    assert sum(tensor[i, j] ** 2 for i in range(3) for j in range(3)) == (
        2 * (cosine**2 + sine**2)
    )


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: conditional_scaled_stf_waveform(
                sp.eye(3), [0, 0, 1], 1, 1
            ),
            "trace free",
        ),
        (
            lambda: conditional_scaled_stf_waveform(
                sp.zeros(3), [0, 0, 1], 1, 0
            ),
            "distance",
        ),
        (
            lambda: conditional_scaled_stf_waveform(
                sp.zeros(3), [0, 0, 1], 1, 1, 0
            ),
            "quadrupole_scale",
        ),
        (
            lambda: conditional_scaled_stf_power(sp.zeros(3), 0, 3),
            "gravitational_coupling",
        ),
    ],
)
def test_invalid_conditional_triaxial_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
