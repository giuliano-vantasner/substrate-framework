"""Primary exact verifier for P055 Candidates B, C, and D."""

from __future__ import annotations

import numpy as np
import sympy as sp

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
from substrate_framework.tt_angular import frobenius_norm_squared
from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P055-EXACT")
    coupling, distance, scale = sp.symbols("G R s", nonzero=True, real=True)
    a, b, c, d, e = sp.symbols("a b c d e", real=True)
    general_stf = sp.Matrix([[a, b, c], [b, d, e], [c, e, -a - d]])
    general_power = conditional_scaled_stf_power(general_stf, coupling, scale)
    ledger.check(
        "scaled-STF power is G times the Frobenius norm over five scale squared",
        sp.simplify(
            general_power
            - coupling * frobenius_norm_squared(general_stf) / (5 * scale**2)
        )
        == 0,
    )

    normalized = sp.diag(a, -a, 0)
    triple = 3 * normalized
    normalized_wave = conditional_scaled_stf_waveform(
        normalized, [0, 0, 1], coupling, distance, 1, [1, 0, 0]
    )
    triple_wave = conditional_scaled_stf_waveform(
        triple, [0, 0, 1], coupling, distance, 3, [1, 0, 0]
    )
    ledger.check(
        "normalized and triple conventions produce the same waveform tensor",
        normalized_wave.waveform_tensor == triple_wave.waveform_tensor,
    )
    ledger.check(
        "natural-axis conventional waveform retains the two-G-over-scale-R coefficient",
        sp.simplify(
            triple_wave.conventional_plus - 2 * coupling * a / distance
        )
        == 0
        and triple_wave.conventional_cross == 0,
    )
    expected_triple_power = coupling * frobenius_norm_squared(triple) / 45
    ledger.mutation_sensitive(
        "triple-STF power requires the scale-three coefficient",
        lambda candidate: sp.simplify(
            conditional_scaled_stf_power(triple, coupling, candidate)
            - expected_triple_power
        )
        == 0,
        3,
        [1, sp.Rational(3, 2), 9],
    )

    cosine2, sine2, cosine3, sine3 = sp.symbols(
        "q_c2 q_s2 q_c3 q_s3", real=True
    )
    real_m2 = real_m2_triple_stf_tensor(cosine3, sine3)
    ledger.check(
        "real-m2 Cartesian tensor is symmetric trace free with both off-diagonal terms",
        real_m2 == real_m2.T
        and sp.trace(real_m2) == 0
        and frobenius_norm_squared(real_m2)
        == 2 * (cosine3**2 + sine3**2),
    )
    natural = conditional_real_m2_natural_axis_waveform(
        cosine2, sine2, coupling, distance
    )
    ledger.check(
        "triple real-m2 natural-axis plus and cross waveforms are two-G-over-three-R",
        sp.simplify(
            natural.conventional_plus - 2 * coupling * cosine2 / (3 * distance)
        )
        == 0
        and sp.simplify(
            natural.conventional_cross - 2 * coupling * sine2 / (3 * distance)
        )
        == 0,
    )
    ledger.check(
        "triple real-m2 conditional power has the exact two-G-over-forty-five coefficient",
        sp.simplify(
            conditional_real_m2_power(cosine3, sine3, coupling)
            - 2 * coupling * (cosine3**2 + sine3**2) / 45
        )
        == 0,
    )

    fixed_tensor = sp.diag(2, -1, -1)
    fixed_readout = real_l2_tt_readout(
        fixed_tensor, [1, 1, 1], [0, 0, 1]
    )
    plus = fixed_readout.conventional_plus_readout
    cross = fixed_readout.conventional_cross_readout
    ledger.check(
        "one fixed STF tensor can have two nonzero generic-frame coordinates",
        plus != 0 and cross != 0,
    )
    magnitude = sp.sqrt(plus**2 + cross**2)
    cosine_two_angle = sp.simplify(plus / magnitude)
    sine_two_angle = sp.simplify(cross / magnitude)
    ledger.check(
        "a spin-two transverse-frame rotation sets the fixed-tensor cross coordinate to zero",
        sp.simplify(-sine_two_angle * plus + cosine_two_angle * cross) == 0
        and sp.simplify(cosine_two_angle**2 + sine_two_angle**2) == 1,
    )

    time = np.linspace(0.0, 2.0 * np.pi, 513, endpoint=False)
    trace = np.cos(time)
    fixed_coefficients = np.column_stack(
        (float(plus) * trace, float(cross) * trace)
    )
    independent_coefficients = np.column_stack((np.cos(time), np.sin(time)))
    ledger.mutation_sensitive(
        "two temporal source modes require nonproportional coefficient traces",
        lambda candidate: temporal_coefficient_rank(candidate) == 2,
        independent_coefficients,
        [fixed_coefficients, np.column_stack((trace, -2.0 * trace))],
    )
    frame_angle = 0.413
    frame_rotation = np.array(
        [
            [np.cos(2 * frame_angle), -np.sin(2 * frame_angle)],
            [np.sin(2 * frame_angle), np.cos(2 * frame_angle)],
        ]
    )
    ledger.check(
        "polarization-frame rotation preserves rank one and rank two",
        temporal_coefficient_rank(fixed_coefficients @ frame_rotation) == 1
        and temporal_coefficient_rank(independent_coefficients @ frame_rotation)
        == 2,
    )

    phase, amplitude, frequency = sp.symbols(
        "tau A omega", real=True, nonzero=True
    )
    circular_plus = -2 * coupling * amplitude * frequency**2 * sp.cos(phase) / (
        3 * distance
    )
    circular_cross = -2 * coupling * amplitude * frequency**2 * sp.sin(phase) / (
        3 * distance
    )
    ledger.check(
        "equal quadrature real-m2 traces give a constant-radius circular waveform",
        sp.trigsimp(
            circular_plus**2
            + circular_cross**2
            - (2 * coupling * amplitude * frequency**2 / (3 * distance)) ** 2
        )
        == 0,
    )
    ledger.check(
        "the corresponding circular real-m2 conditional power is constant",
        sp.trigsimp(
            conditional_real_m2_power(
                amplitude * frequency**3 * sp.sin(phase),
                -amplitude * frequency**3 * sp.cos(phase),
                coupling,
            )
            - 2 * coupling * amplitude**2 * frequency**6 / 45
        )
        == 0,
    )
    ledger.check(
        "removing the sine trace collapses the natural-axis waveform to linear polarization",
        conditional_real_m2_natural_axis_waveform(
            cosine2, 0, coupling, distance
        ).conventional_cross
        == 0,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
