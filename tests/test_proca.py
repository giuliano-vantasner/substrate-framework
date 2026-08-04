from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.proca import (
    mostly_plus_proca_momentum_evidence,
    normalized_proca_mode_evidence,
    transverse_half_line_proca_evidence,
)


def test_full_momentum_kernel_derives_constraint_and_dispersion() -> None:
    m, omega, kx, ky, kz = sp.symbols(
        "m omega kx ky kz",
        positive=True,
    )
    evidence = mostly_plus_proca_momentum_evidence(m, omega, (kx, ky, kz))

    assert evidence.metric == sp.diag(-1, 1, 1, 1)
    assert evidence.momentum_norm_squared == -omega**2 + kx**2 + ky**2 + kz**2
    assert evidence.divergence_constraint_certified
    assert evidence.divergence_contraction == -m**2 * evidence.momentum_covector.T
    assert evidence.transverse_kernel_factor == omega**2 - kx**2 - ky**2 - kz**2 - m**2
    assert evidence.dispersion_frequency_squared == kx**2 + ky**2 + kz**2 + m**2
    assert evidence.dispersion_residual == 0


def test_transverse_polarization_solves_on_shell_but_longitudinal_does_not() -> None:
    m, k = sp.symbols("m k", positive=True)
    omega = sp.sqrt(k**2 + m**2)
    evidence = mostly_plus_proca_momentum_evidence(m, omega, (k, 0, 0))

    transverse = (0, 0, 1, 0)
    longitudinal = (0, 1, 0, 0)
    assert evidence.transversality_residual(transverse) == 0
    assert evidence.euler_residual(transverse) == sp.zeros(4, 1)
    assert evidence.transversality_residual(longitudinal) == k
    assert evidence.euler_residual(longitudinal) != sp.zeros(4, 1)


def test_half_line_boundary_and_decay_select_one_branch() -> None:
    m = sp.Symbol("m", positive=True)
    amplitude = sp.Symbol("A0", real=True, nonzero=True)
    x = sp.Symbol("x", real=True)
    evidence = transverse_half_line_proca_evidence(m, amplitude, coordinate=x)

    rate = evidence.characteristic_variable
    assert evidence.characteristic_polynomial == (-m + rate) * (m + rate)
    assert evidence.characteristic_roots == (-m, m)
    assert evidence.general_solution.has(sp.exp(-m * x))
    assert evidence.general_solution.has(sp.exp(m * x))
    assert evidence.decaying_profile == amplitude * sp.exp(-m * x)
    assert evidence.bvp_certified
    assert evidence.decaying_basis_limit == 0
    assert evidence.growing_basis_absolute_limit == sp.oo
    assert evidence.selected_general_solution_residual == 0
    assert evidence.longitudinal_divergence == -amplitude * m * sp.exp(-m * x)
    assert evidence.longitudinal_divergence != 0
    assert evidence.inverse_length == m
    assert evidence.penetration_length == 1 / m


def test_growing_branch_and_missing_decay_data_do_not_satisfy_the_bvp() -> None:
    m = sp.Symbol("m", positive=True)
    x = sp.Symbol("x", real=True)
    evidence = transverse_half_line_proca_evidence(m, 1, coordinate=x)

    residual = sp.diff(evidence.growing_profile, x, 2) - m**2 * evidence.growing_profile
    assert residual == 0
    assert sp.limit(evidence.growing_profile, x, sp.oo) == sp.oo
    assert evidence.general_solution.subs(
        {
            evidence.decay_coefficient: 0,
            evidence.growing_coefficient: 1,
        }
    ) == sp.exp(m * x)


def test_kinetic_normalization_changes_mass_and_cgsm_composition_is_conditional() -> None:
    g, v = sp.symbols("g v", positive=True)
    coefficient = g**2 * v**2 / 4
    canonical = normalized_proca_mode_evidence(1, coefficient)
    rescaled = normalized_proca_mode_evidence(4, coefficient)

    assert canonical.mass_squared == coefficient
    assert canonical.mass == g * v / 2
    assert canonical.penetration_length == 2 / (g * v)
    assert rescaled.mass_squared == coefficient / 4
    assert rescaled.mass == g * v / 4
    assert rescaled.penetration_length == 4 / (g * v)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: mostly_plus_proca_momentum_evidence(0, 1, (0, 0, 0)),
            "mass must be explicitly positive",
        ),
        (
            lambda: mostly_plus_proca_momentum_evidence(1.0, 1, (0, 0, 0)),
            "mass must be exact",
        ),
        (
            lambda: mostly_plus_proca_momentum_evidence(1, sp.I, (0, 0, 0)),
            "frequency must be explicitly real",
        ),
        (
            lambda: mostly_plus_proca_momentum_evidence(1, 1, (0, 0)),
            "spatial_momentum must contain exactly 3 entries",
        ),
        (
            lambda: transverse_half_line_proca_evidence(-1, 1),
            "mass must be explicitly positive",
        ),
        (
            lambda: transverse_half_line_proca_evidence(1, sp.I),
            "boundary_amplitude must be explicitly real",
        ),
        (
            lambda: normalized_proca_mode_evidence(0, 1),
            "kinetic_coefficient must be explicitly positive",
        ),
        (
            lambda: normalized_proca_mode_evidence(1, -1),
            "quadratic_coefficient must be explicitly positive",
        ),
    ],
)
def test_exact_positive_input_contracts(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
