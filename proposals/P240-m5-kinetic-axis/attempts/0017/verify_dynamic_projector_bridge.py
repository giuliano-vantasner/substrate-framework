"""Exact dynamic-projector bridge for the P240 alternating sextic."""

from __future__ import annotations

import sympy as sp

from substrate_framework.m5_kinetic_axis import (
    alternating_sextic_lagrangian_density,
    alternating_three_current,
    spatial_covariant_metric_from_timelike_projector,
)
from substrate_framework.verification import CheckLedger


ETA = sp.diag(-1, 1, 1, 1)
P_T = sp.diag(1, 0, 0, 0)
ZERO = sp.zeros(4)


def _generator(left: int, right: int) -> sp.Matrix:
    result = sp.zeros(4)
    result[left, right] = -1
    result[right, left] = 1
    return result


def _preimage(spatial: sp.Matrix, current: sp.Matrix) -> sp.Matrix:
    result = sp.zeros(4)
    for left in range(4):
        for right in range(left + 1, 4):
            if current[left, right] != 0:
                result[left, right] = result[right, left] = (
                    current[left, right]
                    / (spatial[left, left] - spatial[right, right])
                )
    return result


def _axial(current: sp.Matrix) -> sp.Matrix:
    return sp.Matrix((-current[2, 3], current[1, 3], -current[1, 2]))


def _determinant_current(currents: tuple[sp.Matrix, ...]) -> sp.Matrix:
    vectors = tuple(_axial(current) for current in currents)
    determinant = lambda left, middle, right: sp.det(
        sp.Matrix.hstack(vectors[left], vectors[middle], vectors[right]).T
    )
    return sp.Matrix(
        (
            -determinant(1, 2, 3),
            determinant(0, 2, 3),
            -determinant(0, 1, 3),
            determinant(0, 1, 2),
        )
    )


def main() -> int:
    ledger = CheckLedger("P240/dynamic-projector-bridge")
    rapidity = sp.symbols("rapidity", real=True)
    kappa = sp.symbols("kappa", positive=True)
    spatial = sp.diag(0, 1, 2, 4)
    axis = sp.diag(0, 0, 0, 1)
    target_currents = (
        _generator(2, 3),
        _generator(3, 1),
        _generator(1, 2),
        ZERO,
    )
    derivatives = tuple(_preimage(spatial, current) for current in target_currents)
    generated = tuple(
        spatial * derivative - derivative * spatial
        for derivative in derivatives
    )
    ledger.check(
        "one spatial Y and symmetric derivatives generate the witness",
        generated == target_currents
        and all(derivative == derivative.T for derivative in derivatives),
    )
    alternating = alternating_three_current(generated)
    ledger.check(
        "literal epsilon current equals the independent determinant current",
        alternating == _determinant_current(generated),
    )
    ledger.check(
        "witness has only the spatial component aligned with the boost",
        alternating[:3, 0] == sp.zeros(3, 1) and alternating[3] != 0,
    )
    baseline = alternating_sextic_lagrangian_density(
        P_T, axis, spatial, derivatives, kappa
    )

    boost = sp.eye(4)
    boost[0, 0] = boost[3, 3] = sp.cosh(rapidity)
    boost[0, 3] = boost[3, 0] = sp.sinh(rapidity)
    inverse = boost.inv()
    projector_t = inverse * P_T * boost
    spatial_metric = spatial_covariant_metric_from_timelike_projector(projector_t)
    time_vector = inverse * sp.Matrix((1, 0, 0, 0))
    ledger.check(
        "dynamic q is symmetric and annihilates the selected timelike line",
        sp.simplify(spatial_metric - spatial_metric.T) == ZERO
        and sp.simplify(spatial_metric * time_vector) == sp.zeros(4, 1)
        and spatial_covariant_metric_from_timelike_projector(P_T)
        == sp.diag(0, 1, 1, 1),
    )
    transformed_axis = inverse * axis * boost
    transformed_spatial = inverse * spatial * boost
    transformed_derivatives = tuple(
        inverse * derivative * boost for derivative in derivatives
    )
    transformed = alternating_sextic_lagrangian_density(
        projector_t,
        transformed_axis,
        transformed_spatial,
        transformed_derivatives,
        kappa,
    )
    ledger.check(
        "full coordinate-frame density retains the load-bearing dynamic q",
        sp.simplify(transformed - baseline * sp.cosh(rapidity) ** 2) == 0,
    )
    ledger.check(
        "the aligned zero-boost second variation is strictly positive",
        sp.simplify(sp.diff(transformed, rapidity, 2).subs(rapidity, 0))
        == 2 * baseline
        and baseline.is_positive is True,
    )
    rest_only = baseline
    ledger.check(
        "the old bare spatial sum is not equivalent off the rest slice",
        sp.diff(rest_only, rapidity) == 0
        and sp.simplify(transformed - rest_only) != 0,
    )
    correct_axis_value = sp.trace(transformed_axis * transformed_spatial)
    wrong_axis = boost * axis * inverse
    wrong_axis_value = sp.trace(wrong_axis * transformed_spatial)
    ledger.check(
        "P_N must use the same mixed similarity as Y",
        sp.simplify(correct_axis_value - sp.trace(axis * spatial)) == 0
        and sp.simplify(wrong_axis_value - sp.trace(axis * spatial)) != 0,
    )

    static_currents = (
        ZERO,
        _generator(2, 3),
        _generator(3, 1),
        _generator(1, 2),
    )
    static_derivatives = tuple(
        _preimage(spatial, current) for current in static_currents
    )
    static_alternating = alternating_three_current(static_currents)
    ledger.check(
        "arbitrary static-current witness remains rest-slice null",
        static_alternating[0] != 0
        and static_alternating[1:, 0] == sp.zeros(3, 1)
        and alternating_sextic_lagrangian_density(
            P_T, axis, spatial, static_derivatives, kappa
        )
        == 0,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
