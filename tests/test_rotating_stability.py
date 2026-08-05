import pytest
import sympy as sp

import substrate_framework as sf
from substrate_framework.rotating_stability import (
    axisymmetric_density_inertia_relation,
    axisymmetric_transverse_rotor_evidence,
    co_rotating_linear_system_evidence,
    finite_matrix_power_evidence,
)


def test_rotating_stability_public_api_is_exported():
    assert sf.axisymmetric_transverse_rotor_evidence is axisymmetric_transverse_rotor_evidence
    assert sf.co_rotating_linear_system_evidence is co_rotating_linear_system_evidence
    assert sf.finite_matrix_power_evidence is finite_matrix_power_evidence


def test_periodic_rotating_frame_gives_exact_static_monodromy_but_not_stability():
    omega = sp.Symbol("omega", positive=True)
    frame = sp.Matrix([[0, -omega], [omega, 0]])
    jordan = sp.Matrix([[0, 1], [0, 0]])
    period = 2 * sp.pi / omega
    evidence = co_rotating_linear_system_evidence(frame + jordan, frame, period)
    assert evidence.frame_periodic
    assert evidence.generator_identity_residual == sp.zeros(2)
    assert evidence.transformed_generator == jordan
    assert evidence.transformed_monodromy == sp.eye(2) + period * jordan
    assert evidence.laboratory_monodromy == evidence.transformed_monodromy
    assert evidence.transformed_power_evidence.modulus_squared == (1,)
    assert evidence.transformed_power_evidence.unit_circle_eigenvalues_semisimple is False
    assert evidence.transformed_power_evidence.powers_bounded is False


def test_unit_multiplier_jordan_counterexample_and_growth_mutation_are_detected():
    jordan = finite_matrix_power_evidence(sp.Matrix([[1, 1], [0, 1]]))
    assert jordan.all_inside_closed_unit_disk
    assert jordan.unit_circle_eigenvalues_semisimple is False
    assert jordan.powers_bounded is False

    growth = sp.Symbol("growth", positive=True)
    unstable = finite_matrix_power_evidence(sp.diag(sp.exp(growth), 1))
    assert unstable.all_inside_closed_unit_disk is False
    assert unstable.powers_bounded is False

    bounded = finite_matrix_power_evidence(sp.diag(-1, 1))
    assert bounded.powers_bounded is True


def test_axisymmetric_transverse_rotor_has_unbounded_linearization_but_stable_set():
    inertia = sp.Symbol("A", positive=True)
    excess = sp.Symbol("Delta", positive=True)
    omega = sp.Symbol("Omega", positive=True)
    time = sp.Symbol("t", real=True)
    evidence = axisymmetric_transverse_rotor_evidence(
        inertia,
        inertia + excess,
        omega,
        time,
    )
    assert evidence.linearized_generator != sp.zeros(3)
    assert evidence.linearized_generator**2 == sp.zeros(3)
    assert evidence.fundamental_matrix == sp.eye(3) + time * evidence.linearized_generator
    assert evidence.monodromy_power_evidence.modulus_squared == (1,)
    assert evidence.monodromy_power_evidence.unit_circle_eigenvalues_semisimple is False
    assert evidence.monodromy_power_evidence.powers_bounded is False
    assert evidence.invariant_derivatives == (0, 0)
    assert evidence.exact_solution_residual == sp.zeros(3, 1)

    symbols = {
        item.name: item for item in evidence.exact_perturbed_solution.free_symbols
    }
    radius = symbols["transverse_radius"]
    epsilon = symbols["axial_perturbation"]
    assert evidence.equilibrium_circle_distance_squared.has(radius, epsilon)
    assert evidence.fixed_equilibrium_initial_distance_squared == epsilon**2
    assert evidence.fixed_equilibrium_witness_distance_squared == 2 * omega**2 + epsilon**2


def test_fixed_rotor_equilibrium_instability_is_not_removed_by_bounded_invariants():
    inertia = sp.Integer(2)
    symmetry_inertia = sp.Integer(3)
    omega = sp.Integer(5)
    time = sp.Symbol("t", real=True)
    evidence = axisymmetric_transverse_rotor_evidence(
        inertia, symmetry_inertia, omega, time
    )
    epsilon = sp.Symbol("axial_perturbation", positive=True)
    assert sp.limit(
        evidence.fixed_equilibrium_initial_distance_squared,
        epsilon,
        0,
        dir="+",
    ) == 0
    assert sp.limit(
        evidence.fixed_equilibrium_witness_distance_squared,
        epsilon,
        0,
        dir="+",
    ) == 2 * omega**2


def test_axisymmetric_density_inertia_relation_keeps_collective_metric_separate():
    radial, axial = sp.symbols("R2 Z", real=True)
    relation = axisymmetric_density_inertia_relation(radial, axial)
    assert relation.symmetry_axis_inertia == radial - axial
    assert relation.transverse_axis_inertia == (radial + axial) / 2
    assert relation.normalized_stf_zz == axial - radial / 3
    assert relation.relation_residual == 0


@pytest.mark.parametrize(
    "call, message",
    [
        (
            lambda: finite_matrix_power_evidence(sp.Matrix([[1, 2, 3]])),
            "non-empty square",
        ),
        (
            lambda: co_rotating_linear_system_evidence(sp.eye(2), sp.eye(3), 1),
            "equal shape",
        ),
        (
            lambda: co_rotating_linear_system_evidence(sp.eye(2), sp.eye(2), 0),
            "period",
        ),
        (
            lambda: axisymmetric_transverse_rotor_evidence(2, 1, 1, sp.Symbol("t")),
            "provably greater",
        ),
    ],
)
def test_rotating_stability_invalid_inputs_are_rejected(call, message):
    with pytest.raises(ValueError, match=message):
        call()
