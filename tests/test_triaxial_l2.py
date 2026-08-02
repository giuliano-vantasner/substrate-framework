import numpy as np
import pytest
import sympy as sp

from substrate_framework.triaxial_l2 import (
    averaged_mode_equation_defect,
    linearized_l_mode_residual,
    real_l2_triple_stf_tensor,
    real_l2_tt_readout,
    regular_l_mode_origin_mismatch,
    temporal_coefficient_rank,
)


def test_real_m2_cosine_gives_exact_triaxial_triple_stf_tensor() -> None:
    scale = sp.symbols("H", real=True)
    tensor = real_l2_triple_stf_tensor(m2_cosine=scale)
    assert tensor == sp.diag(2 * scale / 5, -2 * scale / 5, 0)
    assert sp.trace(tensor) == 0
    assert tensor.eigenvals() == {2 * scale / 5: 1, -2 * scale / 5: 1, 0: 1}


def test_m2_cosine_angular_normalization_is_independently_integrated() -> None:
    mu, phi = sp.symbols("mu phi", real=True)
    nx = sp.sqrt(1 - mu**2) * sp.cos(phi)
    ny = sp.sqrt(1 - mu**2) * sp.sin(phi)
    nz = mu
    harmonic = nx**2 - ny**2
    diagonal = [
        sp.integrate(sp.integrate(component**2 * harmonic, (phi, 0, 2 * sp.pi)), (mu, -1, 1))
        for component in (nx, ny, nz)
    ]
    assert diagonal == [8 * sp.pi / 15, -8 * sp.pi / 15, 0]


def test_natural_axis_tt_readout_separates_real_m2_components() -> None:
    cosine, sine = sp.symbols("H_c H_s", real=True)
    tensor = real_l2_triple_stf_tensor(m2_cosine=cosine, m2_sine=sine)
    readout = real_l2_tt_readout(tensor, [0, 0, 1], [1, 0, 0])
    assert sp.simplify(readout.conventional_plus_readout - 2 * cosine / 5) == 0
    assert sp.simplify(readout.conventional_cross_readout - 2 * sine / 5) == 0
    assert sp.simplify(readout.normalized_plus_coordinate - 2 * sp.sqrt(2) * cosine / 5) == 0
    assert sp.simplify(readout.normalized_cross_coordinate - 2 * sp.sqrt(2) * sine / 5) == 0


def test_temporal_rank_distinguishes_coordinates_from_independent_traces() -> None:
    time = np.linspace(0.0, 2.0 * np.pi, 257, endpoint=False)
    fixed_orientation = np.column_stack((np.cos(time), 3.0 * np.cos(time)))
    circular = np.column_stack((np.cos(time), np.sin(time)))
    assert temporal_coefficient_rank(fixed_orientation) == 1
    assert temporal_coefficient_rank(circular) == 2
    assert temporal_coefficient_rank(np.zeros((8, 2))) == 0
    assert temporal_coefficient_rank(np.column_stack((np.cos(time), np.cos(time)))) == 1


def test_time_average_defect_is_nonzero_for_a_harmonic_background() -> None:
    time = np.linspace(0.0, 2.0 * np.pi, 1025, endpoint=False)
    amplitude = 1.3
    averaged = float(sp.N(sp.besselj(0, amplitude), 17))
    defect = np.cos(amplitude * np.cos(time)) - averaged
    assert np.sqrt(np.mean(defect**2)) > 0.1
    tau, mode = sp.symbols("tau mode", real=True)
    exact = averaged_mode_equation_defect(0, 1, mode * sp.cos(tau))
    assert exact == 0


def test_linearized_residual_and_angular_mutation_are_sensitive() -> None:
    radius = sp.symbols("r", positive=True)
    mode = radius**2
    correct = linearized_l_mode_residual(-mode, 2, 2 * radius, mode, 0, radius, 2)
    mutated = linearized_l_mode_residual(-mode, 2, 2 * radius, mode, 0, radius, 1)
    assert sp.simplify(correct) == 0
    assert sp.simplify(mutated) == -4


def test_regular_origin_oracle_rejects_qb3_starting_pair() -> None:
    radius, coefficient = sp.symbols("r C", nonzero=True)
    assert regular_l_mode_origin_mismatch(coefficient * radius**2, 2 * coefficient * radius, radius, 2) == 0
    assert regular_l_mode_origin_mismatch(0, sp.Rational(1, 10_000), sp.Rational(1, 100), 2) == sp.Rational(1, 1_000_000)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: real_l2_tt_readout(sp.eye(2), [0, 0, 1]), "3 by 3"),
        (lambda: real_l2_tt_readout([[0, 1, 0], [0, 0, 0], [0, 0, 0]], [0, 0, 1]), "symmetric"),
        (lambda: temporal_coefficient_rank([1.0, 2.0]), "two-dimensional"),
        (lambda: temporal_coefficient_rank([[np.nan]]), "finite"),
        (lambda: temporal_coefficient_rank([[1.0]], -1.0), "nonnegative"),
        (lambda: linearized_l_mode_residual(0, 0, 0, 0, 0, 1, sp.Rational(1, 2)), "nonnegative integer"),
    ],
)
def test_invalid_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
