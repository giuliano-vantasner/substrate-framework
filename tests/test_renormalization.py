from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.renormalization import (
    affine_unification_scale,
    diagnose_affine_unification,
    one_loop_inverse_coupling_squared,
    one_loop_transmutation_scale,
    pairwise_affine_crossing,
    reconstruct_electroweak_unification,
    rescale_abelian_inverse_coordinate,
    shift_affine_reference,
    single_scale_tension,
    transmuted_mass_coordinate,
)


def test_one_loop_inverse_coupling_has_boundary_and_flow() -> None:
    scale, reference, coupling, coefficient = sp.symbols(
        "mu mu0 g0 b0", positive=True
    )
    inverse = one_loop_inverse_coupling_squared(
        scale, reference, coupling, coefficient
    )
    assert inverse.subs(scale, reference) == 1 / coupling**2
    assert sp.simplify(scale * sp.diff(inverse, scale)) == coefficient / (
        8 * sp.pi**2
    )


def test_transmutation_scale_is_inverse_coupling_zero() -> None:
    reference, coupling, coefficient = sp.symbols("mu0 g0 b0", positive=True)
    invariant = one_loop_transmutation_scale(reference, coupling, coefficient)
    assert (
        sp.simplify(
            one_loop_inverse_coupling_squared(
                invariant, reference, coupling, coefficient
            )
        )
        == 0
    )


def test_single_scale_tension_retains_free_dimensionless_ratio() -> None:
    scale, ratio = sp.symbols("Lambda k", positive=True)
    tension = single_scale_tension(scale, ratio)
    assert tension == ratio * scale**2
    assert sp.simplify(tension / scale**2) == ratio
    assert sp.diff(tension, ratio) == scale**2
    assert sp.diff(tension, scale) == 2 * ratio * scale


def test_transmuted_mass_coordinate_retains_all_dimensionless_inputs() -> None:
    coupling_squared, coefficient, ratio = sp.symbols("beta2 b0 q", positive=True)
    coordinate = transmuted_mass_coordinate(
        coupling_squared, coefficient, ratio
    )
    assert coordinate == ratio * sp.exp(
        -8 * sp.pi**2 / (coefficient * coupling_squared)
    )
    assert sp.diff(coordinate, ratio) != 0
    assert sp.diff(coordinate, coupling_squared) != 0
    assert sp.diff(coordinate, coefficient) != 0


def test_pairwise_affine_crossing_classifies_all_exact_branches() -> None:
    unique = pairwise_affine_crossing(5, 2, 2, -1, left="one", right="two")
    coincident = pairwise_affine_crossing(5, 2, 5, 2)
    disjoint = pairwise_affine_crossing(5, 2, 4, 2)
    assert unique.status == "unique"
    assert unique.coordinate == 1
    assert (unique.left, unique.right) == ("one", "two")
    assert coincident.status == "coincident" and coincident.coordinate is None
    assert disjoint.status == "parallel_disjoint" and disjoint.coordinate is None


def test_affine_unification_requires_augmented_consistency() -> None:
    compatible = diagnose_affine_unification(
        [5, 2, -1], [2, -1, -4], provenance=("one", "two", "three")
    )
    inconsistent = diagnose_affine_unification(
        [5, 2, 0], [2, -1, -4], provenance=("one", "two", "three")
    )
    assert compatible.linear.unique
    assert compatible.common_inverse_coupling == 3
    assert compatible.running_coordinate == 1
    assert all(crossing.coordinate == 1 for crossing in compatible.pairwise_crossings)
    assert compatible.compatibility_residuals == (0,)
    assert not inconsistent.linear.consistent
    assert inconsistent.common_inverse_coupling is None
    assert len(set(crossing.coordinate for crossing in inconsistent.pairwise_crossings)) > 1
    assert inconsistent.compatibility_residuals != (0,)


def test_reference_shift_preserves_common_inverse_and_shifts_crossings() -> None:
    shifted = shift_affine_reference([5, 2, -1], [2, -1, -4], sp.Rational(1, 3))
    diagnosis = diagnose_affine_unification(
        shifted, [2, -1, -4], provenance=("one", "two", "three")
    )
    assert diagnosis.common_inverse_coupling == 3
    assert diagnosis.running_coordinate == sp.Rational(2, 3)


def test_wm3_inverse_reconstruction_is_exact_and_input_dependent() -> None:
    reconstruction = reconstruct_electroweak_unification(
        sp.Rational(1279, 10),
        sp.Rational(500, 59),
        sp.Rational(41, 10),
        sp.Rational(-19, 6),
        -7,
        sp.Rational(5, 3),
    )
    assert reconstruction.denominator == sp.Rational(67, 3)
    assert reconstruction.running_coordinate == sp.Rational(186383, 39530)
    assert reconstruction.common_inverse_coupling == sp.Rational(1639681, 39530)
    assert reconstruction.weak_angle_coordinate == sp.Rational(6296809, 30335322)
    assert reconstruction.boundary_weak_angle_coordinate == sp.Rational(3, 8)
    assert reconstruction.inverse_couplings[2] == sp.Rational(500, 59)
    assert (
        reconstruction.inverse_couplings[1]
        + sp.Rational(5, 3) * reconstruction.inverse_couplings[0]
        == sp.Rational(1279, 10)
    )
    mutated = reconstruct_electroweak_unification(
        sp.Rational(1280, 10),
        sp.Rational(500, 59),
        sp.Rational(41, 10),
        sp.Rational(-19, 6),
        -7,
        sp.Rational(5, 3),
    )
    assert mutated.weak_angle_coordinate != reconstruction.weak_angle_coordinate


def test_abelian_coordinate_rescaling_preserves_em_term_not_unification_equality() -> None:
    inverse, beta, weight = rescale_abelian_inverse_coordinate(
        30, sp.Rational(41, 10), sp.Rational(5, 3), 2
    )
    assert (inverse, beta, weight) == (15, sp.Rational(41, 20), sp.Rational(10, 3))
    assert weight * inverse == sp.Rational(5, 3) * 30
    assert inverse != 30


def test_affine_unification_scale_uses_declared_dimensionless_coordinate() -> None:
    reference = sp.Symbol("mu0", positive=True)
    coordinate = sp.Symbol("B", real=True)
    assert affine_unification_scale(reference, coordinate) == reference * sp.exp(
        2 * sp.pi * coordinate
    )


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: one_loop_inverse_coupling_squared(0, 1, 1, 1), "scale"),
        (
            lambda: one_loop_inverse_coupling_squared(1, 0, 1, 1),
            "reference_scale",
        ),
        (
            lambda: one_loop_inverse_coupling_squared(1, 1, 0, 1),
            "reference_coupling",
        ),
        (
            lambda: one_loop_inverse_coupling_squared(1, 1, 1, 0),
            "beta_coefficient",
        ),
        (lambda: one_loop_transmutation_scale(0, 1, 1), "reference_scale"),
        (lambda: one_loop_transmutation_scale(1, 0, 1), "reference_coupling"),
        (lambda: one_loop_transmutation_scale(1, 1, 0), "beta_coefficient"),
        (lambda: single_scale_tension(0, 1), "scale"),
        (lambda: single_scale_tension(1, 0), "dimensionless_ratio"),
        (lambda: transmuted_mass_coordinate(0, 1, 1), "coupling_squared"),
        (lambda: transmuted_mass_coordinate(1, 0, 1), "beta_coefficient"),
        (lambda: transmuted_mass_coordinate(1, 1, 0), "mass_energy_ratio"),
        (
            lambda: reconstruct_electroweak_unification(0, 1, 1, 2, 3, 1),
            "electromagnetic_inverse",
        ),
        (
            lambda: reconstruct_electroweak_unification(1, 0, 1, 2, 3, 1),
            "strong_inverse",
        ),
        (
            lambda: reconstruct_electroweak_unification(1, 1, 1, 2, 3, 0),
            "hypercharge_weight",
        ),
        (
            lambda: reconstruct_electroweak_unification(1, 1, 1, 1, 1, 1),
            "denominator",
        ),
        (
            lambda: rescale_abelian_inverse_coordinate(1, 1, 1, 0),
            "coordinate_factor",
        ),
        (lambda: affine_unification_scale(0, 1), "reference_scale"),
    ],
)
def test_positive_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()


@pytest.mark.parametrize(
    "call",
    [
        lambda: pairwise_affine_crossing(sp.Float(1), 1, 2, 2),
        lambda: diagnose_affine_unification([1], [2], provenance=("one",)),
        lambda: diagnose_affine_unification([1, 2], [3], provenance=("one", "two")),
        lambda: diagnose_affine_unification([1, 2], [3, 4], provenance=("one",)),
    ],
)
def test_affine_ledgers_reject_inexact_or_malformed_inputs(call) -> None:
    with pytest.raises(ValueError):
        call()
