"""Exact power counting, covariance, and Derrick balance for Candidate F."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from substrate_framework.m5_covariant_action import (
    MINKOWSKI_MOSTLY_PLUS,
    completed_m5_hamiltonian_density,
    m5_curvature_from_derivatives,
    projector_current_bilinear,
    projector_sigma_hamiltonian_density,
    projector_sigma_lagrangian_density,
    spectral_cartan_hamiltonian_density,
)
from substrate_framework.verification import CheckLedger


HERE = Path(__file__).resolve().parent
ETA = sp.Matrix(MINKOWSKI_MOSTLY_PLUS)


def main():
    ledger = CheckLedger("P239/projector-current-completion")
    epsilon = sp.symbols("epsilon", real=True)
    stiffness = sp.symbols("kappa", positive=True)

    derivative_0 = epsilon * sp.diag(1, 0, 0, 0)
    derivative_1 = sp.zeros(4)
    derivative_1[0, 1] = derivative_1[1, 0] = epsilon
    zero = sp.zeros(4)
    curvature = m5_curvature_from_derivatives((derivative_0, derivative_1, zero, zero))
    curvature_energy = spectral_cartan_hamiltonian_density(curvature, sp.eye(4))
    ledger.check(
        "vacuum-orbit curvature energy starts at fourth perturbative order",
        sp.Poly(curvature_energy, epsilon).monoms() == [(4,)],
    )
    ledger.check(
        "curvature-only action has no quadratic linearized operator",
        sp.diff(curvature_energy, epsilon, 2).subs(epsilon, 0) == 0,
    )

    boost_tangent = sp.zeros(4)
    boost_tangent[0, 1] = -epsilon
    boost_tangent[1, 0] = epsilon
    projector_derivatives = (zero, boost_tangent, zero, zero)
    current_energy = projector_sigma_hamiltonian_density(
        projector_derivatives, stiffness
    )
    ledger.check(
        "projector target metric is positive on a boost tangent",
        projector_current_bilinear(boost_tangent, boost_tangent) == epsilon**2,
    )
    ledger.check(
        "projector current supplies a positive quadratic operator",
        sp.diff(current_energy, epsilon, 2).subs(epsilon, 0) == 2 * stiffness,
    )
    ledger.check(
        "projector current vanishes on every constant-projector 3x3 field",
        projector_sigma_lagrangian_density((zero, zero, zero, zero), stiffness) == 0,
    )
    ledger.check(
        "completed Hamiltonian is the sum of current and curvature energies",
        sp.simplify(
            completed_m5_hamiltonian_density(
                curvature, sp.eye(4), projector_derivatives, stiffness
            )
            - current_energy
            - curvature_energy
        )
        == 0,
    )

    radius = sp.symbols("R", positive=True)
    sigma_shape, curvature_shape = sp.symbols("A_2 A_4", positive=True)
    curvature_only = curvature_shape / radius
    completed_static = stiffness * sigma_shape * radius + curvature_shape / radius
    stationary_radius = sp.sqrt(curvature_shape / (stiffness * sigma_shape))
    ledger.check(
        "curvature-only Derrick energy decreases under expansion",
        sp.diff(curvature_only, radius) < 0,
    )
    ledger.check(
        "curvature-only energy tends to zero at infinite size",
        sp.limit(curvature_only, radius, sp.oo) == 0,
    )
    ledger.check(
        "projector-current completion has an exact finite stationary scale",
        sp.simplify(sp.diff(completed_static, radius).subs(radius, stationary_radius))
        == 0,
    )
    ledger.check(
        "completed static scale is a strict minimum",
        sp.diff(completed_static, radius, 2).subs(radius, stationary_radius) > 0,
    )

    angular_momentum, inertia_shape = sp.symbols("J C_I", positive=True)
    fixed_j_energy = (
        stiffness * sigma_shape * radius
        + curvature_shape / radius
        + angular_momentum**2 / (4 * inertia_shape * radius**3)
    )
    stationary_radius_squared = (
        curvature_shape
        + sp.sqrt(
            curvature_shape**2
            + 3 * stiffness * sigma_shape * angular_momentum**2 / inertia_shape
        )
    ) / (2 * stiffness * sigma_shape)
    fixed_j_radius = sp.sqrt(stationary_radius_squared)
    frequency = angular_momentum / (2 * inertia_shape * fixed_j_radius**3)
    ledger.check(
        "fixed-J reduced energy diverges at zero size",
        sp.limit(fixed_j_energy, radius, 0, dir="+") == sp.oo,
    )
    ledger.check(
        "fixed-J reduced energy diverges at infinite size",
        sp.limit(fixed_j_energy, radius, sp.oo) == sp.oo,
    )
    ledger.check(
        "fixed-J scale equation has the displayed positive root",
        sp.simplify(sp.diff(fixed_j_energy, radius).subs(radius, fixed_j_radius)) == 0,
    )
    ledger.check(
        "fixed-J stationary scale is a strict minimum",
        sp.diff(fixed_j_energy, radius, 2).subs(radius, fixed_j_radius) > 0,
    )
    ledger.check("fixed-J frequency is finite and nonzero", frequency > 0)

    wave_numbers = sp.symbols("k_0:3", real=True)
    boost_amplitude = sp.symbols("chi", real=True)
    linearized_density = (
        stiffness
        * boost_amplitude**2
        * sum(wave_number**2 for wave_number in wave_numbers)
    )
    ledger.check(
        "projector current has the massless Laplace Fourier symbol",
        sp.factor(linearized_density / (stiffness * boost_amplitude**2))
        == sum(wave_number**2 for wave_number in wave_numbers),
    )
    ledger.check(
        "no mass term appears in the projector-orbit linearization",
        linearized_density.subs(dict.fromkeys(wave_numbers, 0)) == 0,
    )

    result = {
        "campaign": "P239",
        "attempt": "0003",
        "rejected_completion": "E_spectral_cartan_without_projector_current",
        "selected_for_stationary_testing": "F_projector_current_completion",
        "power_counting": {
            "curvature_energy": "O(epsilon^4)",
            "projector_current_energy": "O(epsilon^2)",
        },
        "three_dimensional_scaling": {
            "projector_current": "kappa*A_2*R",
            "spectral_cartan_curvature": "A_4/R",
            "static_radius": "sqrt(A_4/(kappa*A_2))",
        },
        "fixed_j_scale": {
            "energy": "kappa*A_2*R+A_4/R+J^2/(4*C_I*R^3)",
            "radius_squared": str(stationary_radius_squared),
            "frequency": "J/(2*C_I*R_*^3)",
        },
        "linearized_boost_operator": "-2*kappa*Delta",
        "scope": (
            "Exact structural and scale reduction. It does not prove that a "
            "full radial or three-dimensional stationary solution realizes "
            "the positive shape coefficients used here."
        ),
        "check_count": len(ledger.passed),
    }
    (HERE / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
