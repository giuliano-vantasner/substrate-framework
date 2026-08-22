"""Tests for central-force network elasticity routes."""

from __future__ import annotations

import numpy as np
import pytest

from substrate_framework.nonaffine_networks import (
    CentralForceNetwork,
    acoustic_speed_squared,
    extrapolated_acoustic_speed_squared,
)


def test_affine_moduli_match_analytic_family_formula() -> None:
    for families in range(5):
        net = CentralForceNetwork(4, diagonal_families=families)
        assert net.affine_shear_modulus() == pytest.approx(families / 3.0, abs=1e-12)


def test_centrosymmetric_networks_have_zero_nonaffine_correction() -> None:
    net = CentralForceNetwork(4, diagonal_families=4)
    relaxed = net.relaxed_shear_modulus()
    assert relaxed["nonaffine_correction"] == pytest.approx(0.0, abs=1e-12)
    assert relaxed["modulus"] == pytest.approx(4.0 / 3.0)


def test_soft_mode_below_threshold_and_rigid_above() -> None:
    floppy = CentralForceNetwork(4, diagonal_families=0)
    rigid = CentralForceNetwork(4, diagonal_families=4)
    assert floppy.relaxed_shear_modulus()["modulus"] == 0.0
    floppy_sound = acoustic_speed_squared(floppy)
    assert not floppy_sound["transverse_branch_found"] or (
        floppy_sound["c_squared_finite_q"] == pytest.approx(0.0)
    )
    assert rigid.relaxed_shear_modulus()["modulus"] > 0.5


def test_two_routes_agree_on_isotropic_network() -> None:
    extrapolated = extrapolated_acoustic_speed_squared(4)
    static = CentralForceNetwork(6, diagonal_families=4)
    modulus = static.relaxed_shear_modulus()["modulus"]
    assert extrapolated["c_squared_continuum"] == pytest.approx(modulus, rel=1e-8)


def test_maxwell_count_is_not_sufficient() -> None:
    isostatic_counted = CentralForceNetwork(3, diagonal_families=0)
    assert isostatic_counted.mean_coordination == pytest.approx(6.0)
    assert isostatic_counted.affine_shear_modulus() == 0.0


def test_hessian_symmetric_psd_on_support() -> None:
    net = CentralForceNetwork(3, diagonal_families=2)
    matrix = net.hessian()
    assert np.allclose(matrix, matrix.T, atol=1e-14)
    eigenvalues = np.linalg.eigvalsh(matrix)
    assert float(eigenvalues.min()) == pytest.approx(0.0, abs=1e-10)
    assert float(eigenvalues.max()) > 0.0
