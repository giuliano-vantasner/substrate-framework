#!/usr/bin/env python3
"""Exact and refinement-bounded CF1 Abelian-Higgs vortex verifier."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.abelian_higgs_vortex import (
    VortexParameters,
    angular_log_coefficient,
    asymptotic_masses,
    euler_lagrange_residuals,
    quantized_flux,
    radial_energy_lagrangian,
    solve_vortex_bvp,
    vortex_boundary_residual,
    vortex_energy_density,
    vortex_tension,
)
from substrate_framework.verification import CheckLedger


CF1_SHA256 = "a4ec97923804f1b7c624b7619bc6b6a1cbb62f42d659897799545b257ca33f5d"


@dataclass(frozen=True)
class EquationCandidate:
    scalar_friction: sp.Expr
    angular_sign: sp.Expr
    gauge_friction: sp.Expr
    gauge_sign: sp.Expr
    gauge_power: sp.Expr


def run(source_file: Path) -> int:
    checks = CheckLedger("C-VTX-001/C-VTX-002")
    checks.check(
        "the audited CF1 source is the hash-pinned candidate unit",
        hashlib.sha256(source_file.read_bytes()).hexdigest() == CF1_SHA256,
    )

    radius = sp.symbols("r", positive=True)
    winding = sp.symbols("n", integer=True, positive=True)
    lam, vacuum, coupling = sp.symbols("lambda v g", positive=True)
    scalar = sp.Function("f")(radius)
    gauge = sp.Function("a")(radius)
    lagrangian = radial_energy_lagrangian(
        radius, scalar, gauge, winding, lam, vacuum, coupling
    )
    expected_scalar, expected_gauge = euler_lagrange_residuals(
        radius, scalar, gauge, winding, lam, vacuum, coupling
    )
    varied_scalar = sp.simplify(
        (
            sp.diff(sp.diff(lagrangian, sp.diff(scalar, radius)), radius)
            - sp.diff(lagrangian, scalar)
        )
        / radius
    )
    varied_gauge = sp.simplify(
        coupling**2
        * radius
        * (
            sp.diff(sp.diff(lagrangian, sp.diff(gauge, radius)), radius)
            - sp.diff(lagrangian, gauge)
        )
    )
    checks.check(
        "the declared radial functional varies to both canonical equations",
        sp.simplify(varied_scalar - expected_scalar) == 0
        and sp.simplify(varied_gauge - expected_gauge) == 0,
    )
    checks.check(
        "the source equations are the gauge-coupling-one specialization",
        sp.simplify(
            expected_gauge.subs(coupling, 1)
            - (
                sp.diff(gauge, radius, 2)
                - sp.diff(gauge, radius) / radius
                + (winding - gauge) * scalar**2
            )
        )
        == 0,
    )

    def equations_match(candidate: EquationCandidate) -> bool:
        scalar_candidate = (
            sp.diff(scalar, radius, 2)
            + candidate.scalar_friction * sp.diff(scalar, radius) / radius
            + candidate.angular_sign
            * scalar
            * (winding - gauge) ** 2
            / radius**2
            - lam * scalar * (scalar**2 - vacuum**2)
        )
        gauge_candidate = (
            sp.diff(gauge, radius, 2)
            + candidate.gauge_friction * sp.diff(gauge, radius) / radius
            + candidate.gauge_sign
            * coupling**candidate.gauge_power
            * (winding - gauge)
            * scalar**2
        )
        return (
            sp.simplify(scalar_candidate - expected_scalar) == 0
            and sp.simplify(gauge_candidate - expected_gauge) == 0
        )

    checks.mutation_sensitive(
        "radial friction signs angular sign and gauge normalization",
        equations_match,
        EquationCandidate(1, -1, -1, 1, 2),
        [
            EquationCandidate(0, -1, -1, 1, 2),
            EquationCandidate(1, 1, -1, 1, 2),
            EquationCandidate(1, -1, 1, 1, 2),
            EquationCandidate(1, -1, -1, -1, 2),
            EquationCandidate(1, -1, -1, 1, 0),
        ],
    )

    asymptotic_gauge = sp.symbols("a_infinity", real=True)
    log_coefficient = angular_log_coefficient(
        vacuum, winding, asymptotic_gauge
    )
    checks.check(
        "finite angular energy uniquely forces the asymptotic gauge profile to winding",
        sp.solve(sp.Eq(log_coefficient, 0), asymptotic_gauge) == [winding],
    )
    checks.check(
        "the ungauged positive-winding profile retains a nonzero logarithmic divergence",
        angular_log_coefficient(vacuum, winding, 0) == vacuum**2 * winding**2,
    )
    checks.mutation_sensitive(
        "finite-energy asymptotic boundary",
        lambda value: angular_log_coefficient(vacuum, winding, value) == 0,
        winding,
        [winding + 1, winding - 1],
    )
    checks.check(
        "the frozen A_theta convention gives the exact flux quantum",
        quantized_flux(winding, coupling) == 2 * sp.pi * winding / coupling,
    )
    checks.check(
        "dropping the gauge coupling changes the flux except at the demo normalization",
        sp.simplify(quantized_flux(winding, coupling) - 2 * sp.pi * winding) != 0
        and quantized_flux(winding, 1) == 2 * sp.pi * winding,
    )

    epsilon = sp.symbols("epsilon")
    scalar_deviation = sp.Function("delta")(radius)
    gauge_deviation = sp.Function("chi")(radius)
    linear_scalar = sp.expand(
        euler_lagrange_residuals(
            radius,
            vacuum - epsilon * scalar_deviation,
            sp.sympify(winding),
            winding,
            lam,
            vacuum,
            coupling,
        )[0]
    ).coeff(epsilon, 1)
    linear_gauge = sp.expand(
        euler_lagrange_residuals(
            radius,
            sp.sympify(vacuum),
            winding - epsilon * gauge_deviation,
            winding,
            lam,
            vacuum,
            coupling,
        )[1]
    ).coeff(epsilon, 1)
    checks.check(
        "independent vacuum linearization gives the scalar and vector inverse lengths",
        sp.simplify(
            linear_scalar
            + sp.diff(scalar_deviation, radius, 2)
            + sp.diff(scalar_deviation, radius) / radius
            - 2 * lam * vacuum**2 * scalar_deviation
        )
        == 0
        and sp.simplify(
            linear_gauge
            + sp.diff(gauge_deviation, radius, 2)
            - sp.diff(gauge_deviation, radius) / radius
            - coupling**2 * vacuum**2 * gauge_deviation
        )
        == 0
        and asymptotic_masses(vacuum, lam, coupling)
        == (coupling * vacuum, vacuum * sp.sqrt(2 * lam)),
    )
    vector_mass, scalar_mass = asymptotic_masses(vacuum, lam, coupling)
    checks.check(
        "the unbroken vacuum-scale limit removes both inverse screening lengths",
        sp.limit(vector_mass, vacuum, 0, dir="+") == 0
        and sp.limit(scalar_mass, vacuum, 0, dir="+") == 0,
    )

    parameters = VortexParameters(
        vacuum_scale=1.0, winding=1, self_coupling=2.0, gauge_coupling=1.0
    )
    reference = solve_vortex_bvp(
        parameters,
        inner_radius=1.0e-4,
        outer_radius=20.0,
        initial_points=120,
        tolerance=1.0e-8,
    )
    reference_tension = vortex_tension(reference)
    boundary = vortex_boundary_residual(
        reference.evidence.state[:, 0],
        reference.evidence.state[:, -1],
        parameters,
    )
    checks.check(
        "the reference BVP reports success residuals and boundary closure",
        reference.evidence.max_rms_residual < 1.1e-8
        and np.max(np.abs(boundary)) < 1.0e-10
        and reference.evidence.iterations > 0,
    )
    sample_radius = np.linspace(0.01, 15.0, 3000)
    sample_state = reference.state_at(sample_radius)
    checks.check(
        "the nontrivial scalar and gauge profiles are monotone on the audited interior",
        np.min(sample_state[1]) > -1.0e-9
        and np.min(sample_state[3]) > -1.0e-9
        and sample_state[0, 0] < 0.02
        and sample_state[0, -1] > 0.999
        and sample_state[2, 0] < 1.0e-3
        and sample_state[2, -1] > 0.999,
    )
    density = vortex_energy_density(
        reference.evidence.coordinate,
        reference.evidence.state,
        parameters,
    )
    checks.check(
        "the declared energy density and integrated tension are finite and positive",
        np.all(np.isfinite(density))
        and np.all(density >= 0.0)
        and 4.20 < reference_tension < 4.23,
    )

    tolerance_solutions = [
        solve_vortex_bvp(
            parameters,
            inner_radius=1.0e-4,
            outer_radius=20.0,
            initial_points=120,
            tolerance=tolerance,
        )
        for tolerance in (1.0e-4, 1.0e-6)
    ]
    tolerance_tensions = [vortex_tension(solution) for solution in tolerance_solutions]
    tolerance_errors = [
        abs(value - reference_tension) for value in tolerance_tensions
    ]
    checks.check(
        "collocation tolerance refinement reduces residuals and tension error",
        tolerance_solutions[0].evidence.max_rms_residual < 1.1e-4
        and tolerance_solutions[1].evidence.max_rms_residual < 1.1e-6
        and tolerance_errors[1] < tolerance_errors[0] / 20,
    )

    domain_tensions = []
    for outer_radius in (10.0, 15.0, 25.0):
        solution = solve_vortex_bvp(
            parameters,
            inner_radius=1.0e-4,
            outer_radius=outer_radius,
            initial_points=120,
            tolerance=1.0e-8,
        )
        domain_tensions.append(vortex_tension(solution))
    checks.check(
        "outer-domain refinement bounds the tension tail",
        max(abs(value - reference_tension) for value in domain_tensions) < 1.0e-5,
    )

    cutoff_tensions = []
    for inner_radius in (1.0e-2, 3.0e-3, 1.0e-3, 3.0e-4):
        solution = solve_vortex_bvp(
            parameters,
            inner_radius=inner_radius,
            outer_radius=20.0,
            initial_points=120,
            tolerance=1.0e-8,
        )
        cutoff_tensions.append(vortex_tension(solution))
    cutoff_errors = [abs(value - reference_tension) for value in cutoff_tensions]
    checks.check(
        "inner-cutoff refinement monotonically reduces the tension error",
        all(
            fine < coarse
            for coarse, fine in zip(cutoff_errors, cutoff_errors[1:])
        )
        and cutoff_errors[-1] < 2.0e-6,
    )

    guess_solutions = [
        solve_vortex_bvp(
            parameters,
            inner_radius=1.0e-4,
            outer_radius=20.0,
            initial_points=80,
            tolerance=1.0e-7,
            guess_family=family,
        )
        for family in ("exponential", "rational")
    ]
    common_radius = np.linspace(1.0e-4, 20.0, 2001)
    checks.check(
        "two structurally different initial guesses converge to the same branch",
        np.max(
            np.abs(
                guess_solutions[0].state_at(common_radius)
                - guess_solutions[1].state_at(common_radius)
            )
        )
        < 1.0e-8
        and abs(
            vortex_tension(guess_solutions[0])
            - vortex_tension(guess_solutions[1])
        )
        < 1.0e-8,
    )

    doubled = solve_vortex_bvp(
        VortexParameters(
            vacuum_scale=2.0,
            winding=1,
            self_coupling=2.0,
            gauge_coupling=1.0,
        ),
        inner_radius=5.0e-5,
        outer_radius=10.0,
        initial_points=120,
        tolerance=1.0e-8,
    )
    checks.check(
        "matched dimensionless domains verify the exact vacuum-scale-square law",
        abs(vortex_tension(doubled) / reference_tension - 4.0) < 1.0e-5,
    )

    fit_radius = np.linspace(4.0, 10.0, 3001)
    fit_scalar, _, _, fit_gauge_prime = reference.state_at(fit_radius)
    magnetic_field = fit_gauge_prime / fit_radius
    scalar_tail = 1.0 - fit_scalar
    vector_fit = -np.polyfit(
        fit_radius, np.log(np.abs(magnetic_field) * np.sqrt(fit_radius)), 1
    )[0]
    scalar_fit = -np.polyfit(
        fit_radius, np.log(np.abs(scalar_tail) * np.sqrt(fit_radius)), 1
    )[0]
    checks.check(
        "profile tails regress against the independently exact linearized masses",
        abs(vector_fit - 1.0) < 0.01 and abs(scalar_fit - 2.0) < 0.08,
    )
    checks.check(
        "a wrong asymptotic gauge boundary fails the finite-energy verdict",
        angular_log_coefficient(vacuum, winding, winding + 1) != 0,
    )
    checks.check(
        "none of the accepted equations contains a physical dual or confinement map",
        all(
            token not in str(expression)
            for expression in (lagrangian, expected_scalar, expected_gauge)
            for token in ("QCD", "chromo", "confin")
        ),
    )

    total = checks.finish()
    print(f"P026 CF1 CONDITIONAL VORTEX AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
