from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.axial_ward import (
    analytic_gt_discrepancy_evidence,
    axial_form_factor_dimension_ledger,
    generalized_axial_ward_evidence,
    gt_relation_ledger,
    on_shell_axial_divergence,
    pcac_limit_order_evidence,
    pion_pole_remainder_evidence,
)


def test_dimension_ledger_rejects_source_mixed_induced_convention() -> None:
    standard = axial_form_factor_dimension_ledger()
    source_like = axial_form_factor_dimension_ledger(induced_scale_mass_dimension=0)
    assert standard.convention_is_dimensionally_consistent
    assert standard.dimension_residual == 0
    assert not source_like.convention_is_dimensionally_consistent
    assert source_like.dimension_residual == 1


def test_on_shell_divergence_keeps_the_two_mass_scale() -> None:
    mass, q2, axial, induced = sp.symbols("M Q2 G_A G_P", positive=True)
    evidence = on_shell_axial_divergence(mass, q2, axial, induced)
    assert evidence.induced_scale == 2 * mass
    assert evidence.unnormalized_divergence_coefficient == (
        2 * mass * axial - q2 * induced / (2 * mass)
    )
    assert evidence.normalized_divergence_coefficient == (
        axial - q2 * induced / (4 * mass**2)
    )
    source_like = on_shell_axial_divergence(
        mass,
        q2,
        axial,
        induced,
        induced_scale=1,
    )
    assert sp.simplify(
        source_like.unnormalized_divergence_coefficient
        - evidence.unnormalized_divergence_coefficient
    ) != 0


def test_explicit_gamma_matrices_give_the_on_shell_two_mass_identity() -> None:
    identity2 = sp.eye(2)
    zero2 = sp.zeros(2)
    sigma3 = sp.diag(1, -1)
    gamma0 = sp.diag(1, 1, -1, -1)
    gamma3 = sp.Matrix.vstack(
        sp.Matrix.hstack(zero2, sigma3),
        sp.Matrix.hstack(-sigma3, zero2),
    )
    gamma1 = sp.Matrix(
        [[0, 0, 0, 1], [0, 0, 1, 0], [0, -1, 0, 0], [-1, 0, 0, 0]]
    )
    gamma2 = sp.Matrix(
        [[0, 0, 0, -sp.I], [0, 0, sp.I, 0], [0, sp.I, 0, 0], [-sp.I, 0, 0, 0]]
    )
    gamma5 = sp.simplify(sp.I * gamma0 * gamma1 * gamma2 * gamma3)
    assert gamma5 * gamma5 == sp.eye(4)
    for gamma in (gamma0, gamma1, gamma2, gamma3):
        assert sp.simplify(gamma5 * gamma + gamma * gamma5) == sp.zeros(4)

    mass, momentum = sp.symbols("M k", positive=True)
    energy = sp.sqrt(mass**2 + momentum**2)
    normalization = sp.sqrt((energy + mass) / (2 * mass))
    spinor_initial = normalization * sp.Matrix(
        [1, 0, -momentum / (energy + mass), 0]
    )
    spinor_final = normalization * sp.Matrix(
        [1, 0, momentum / (energy + mass), 0]
    )
    bar_final = spinor_final.conjugate().T * gamma0
    q_slash = -2 * momentum * gamma3
    left = sp.simplify((bar_final * q_slash * gamma5 * spinor_initial)[0])
    pseudoscalar = sp.simplify((bar_final * gamma5 * spinor_initial)[0])
    right = sp.simplify(2 * mass * pseudoscalar)
    assert sp.simplify(left - right) == 0

    axial, induced = sp.symbols("G_A G_P", real=True)
    minkowski_q_squared = -4 * momentum**2
    contracted_current = sp.simplify(
        axial * left
        + minkowski_q_squared * induced * pseudoscalar / (2 * mass)
    )
    assert sp.simplify(
        contracted_current / (2 * mass * pseudoscalar)
        - (axial - 4 * momentum**2 * induced / (4 * mass**2))
    ) == 0


def test_generalized_pcac_identity_and_pole_dominance_are_separate() -> None:
    q2 = sp.symbols("Q2", real=True)
    mass, pion_mass2, scale = sp.symbols("M mu2 F", positive=True)
    g0, slope, axial0, axial_slope, induced0 = sp.symbols(
        "g0 s a0 a1 p0",
        real=True,
    )
    pion_nucleon = g0 + slope * q2
    axial = axial0 + axial_slope * q2
    evidence = generalized_axial_ward_evidence(
        q2,
        mass,
        pion_mass2,
        scale,
        axial,
        induced0,
        pion_nucleon,
    )
    assert evidence.normalized_divergence == axial - q2 * induced0 / (4 * mass**2)
    assert evidence.pcac_pion_pole_source == (
        scale * pion_mass2 * pion_nucleon / (mass * (pion_mass2 + q2))
    )
    assert sp.simplify(
        evidence.pole_dominance_reduced_residual
        - (axial - scale * pion_nucleon / mass)
    ) == 0
    assert evidence.generalized_identity_residual != evidence.pole_dominance_reduced_residual


def test_pion_pole_residue_and_coupling_evaluation_points_are_explicit() -> None:
    q2 = sp.symbols("Q2", real=True)
    mass, pion_mass2, scale = sp.symbols("M mu2 F", positive=True)
    g0, slope, axial = sp.symbols("g0 s G_A", positive=True)
    pion_nucleon = g0 + slope * q2
    evidence = generalized_axial_ward_evidence(
        q2,
        mass,
        pion_mass2,
        scale,
        axial,
        0,
        pion_nucleon,
    )
    assert evidence.coupling_at_zero_transfer == g0
    assert evidence.coupling_at_pion_pole == g0 - slope * pion_mass2
    assert evidence.pion_pole_residue == (
        4 * mass * scale * (g0 - slope * pion_mass2)
    )
    assert sp.simplify(
        evidence.zero_transfer_gt_residual - evidence.pion_pole_gt_residual
    ) != 0


def test_regular_induced_remainder_changes_off_zero_identity_not_residue() -> None:
    q2 = sp.symbols("Q2", real=True)
    mass, pion_mass2, scale = sp.symbols("M mu2 F", positive=True)
    axial, coupling, remainder0, remainder1 = sp.symbols(
        "G_A g R0 R1",
        real=True,
    )
    remainder = remainder0 + remainder1 * q2
    evidence = pion_pole_remainder_evidence(
        q2,
        mass,
        pion_mass2,
        scale,
        axial,
        coupling,
        remainder,
    )
    assert sp.simplify(
        evidence.generalized_identity_residual - evidence.reduced_residual
    ) == 0
    assert sp.simplify(
        evidence.reduced_residual
        - (axial - scale * coupling / mass - q2 * remainder / (4 * mass**2))
    ) == 0
    assert evidence.pion_pole_residue == 4 * mass * scale * coupling
    assert evidence.zero_transfer_residual == axial - scale * coupling / mass


def test_pcac_pole_kernel_limits_do_not_commute() -> None:
    q2, pion_mass2, ratio = sp.symbols("Q2 mu2 rho", positive=True)
    evidence = pcac_limit_order_evidence(q2, pion_mass2, ratio)
    assert evidence.zero_transfer_then_chiral == 1
    assert evidence.chiral_then_zero_transfer == 0
    assert evidence.fixed_ratio_path == 1 / (ratio + 1)


def test_mass_squared_discrepancy_requires_regular_coupling_expansion() -> None:
    pion_mass2 = sp.symbols("mu2", positive=True)
    coupling0 = sp.symbols("g0", positive=True)
    slope, remainder = sp.symbols("s R", real=True)
    evidence = analytic_gt_discrepancy_evidence(
        pion_mass2,
        coupling0,
        slope,
        remainder,
    )
    assert evidence.coupling_at_pion_pole == (
        coupling0 - slope * pion_mass2 + remainder * pion_mass2**2
    )
    assert sp.simplify(
        evidence.dimensionless_discrepancy
        - pion_mass2 * evidence.mass_squared_factor
    ) == 0
    assert evidence.leading_mass_squared_coefficient == -slope / coupling0
    assert evidence.chiral_limit == 0


def test_gt_equation_has_three_free_parameter_directions() -> None:
    coupling, scale, axial, mass, rho = sp.symbols(
        "g F g_A M rho",
        positive=True,
    )
    ledger = gt_relation_ledger(coupling, scale, axial, mass, rho)
    assert ledger.solved_axial_charge == coupling * scale / mass
    assert ledger.solved_pion_nucleon_coupling == axial * mass / scale
    assert ledger.monomial_exponent_row.rank() == 1
    assert ledger.independent_parameter_directions == 3
    assert ledger.monomial_exponent_row * ledger.exponent_nullspace == sp.zeros(1, 3)
    assert ledger.common_scale_covariance_residual == 0
    assert ledger.inverse_decay_coupling_residual == 0
    assert ledger.inverse_mass_axial_residual == 0


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: on_shell_axial_divergence(-1, 1, 1, 1),
            "nucleon mass",
        ),
        (
            lambda: pcac_limit_order_evidence(
                sp.symbols("Q2"),
                sp.Integer(1),
                1,
            ),
            "pion mass squared",
        ),
    ],
)
def test_invalid_axial_ward_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
