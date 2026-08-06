"""Primary exact and refined numerical verifier for P218 MK5."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
import yaml

from substrate_framework.generalized_skyrme_radial import (
    generalized_skyrme_endpoint_data,
    generalized_skyrme_energy_components,
    generalized_skyrme_radial_energy_density,
    generalized_skyrme_radial_euler_lagrange_residual,
    generalized_skyrme_reduced_coefficients,
    generalized_skyrme_scaling_residual,
    generalized_skyrme_tail_robin_coefficient,
    solve_generalized_skyrme_radial_profile,
)
from substrate_framework.rational_map_radial import (
    rational_map_radial_energy_density,
    rational_map_radial_euler_lagrange_residual,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-43/"
    "bridge_MK5_generalized_solve_kappa.py"
)
SOURCE_SHA = "a5ecb5d0d2ba96cf8083a9cfb32ddb44c2a4f4841bf776ebbccb91bc12b246f8"
FREEZE_SHA = "c5bddf4683c993fc6297a1dca046d9398746d3c66d24772f911ea48e548fd273"
ANGULAR = {1: 1.0, 2: float(np.pi + 8.0 / 3.0), 4: 20.6496264884189}
REFERENCE = {
    1: 1.4326169552,
    2: 2.7988849886,
    4: 5.1973886988,
}


def _solve_set(outer: float, *, sample_points: int = 8001):
    return {
        degree: solve_generalized_skyrme_radial_profile(
            degree,
            angular,
            0.5,
            0.25,
            outer_radius=outer,
            initial_points=401,
            sample_points=sample_points,
            continuation_steps=8,
            tolerance=1.0e-6,
        )
        for degree, angular in ANGULAR.items()
    }


def _kappa(profiles) -> float:
    return float(
        3.0
        * np.pi**2
        * (
            2.0 * profiles[2].energy_coefficient
            - profiles[4].energy_coefficient
        )
    )


def main() -> int:
    checks = CheckLedger("P218")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source and formula freeze hashes are pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA
        and hashlib.sha256(
            (CAMPAIGN / "evidence/formula-freeze.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(source_tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source inventory separates eight predicates and one assertion",
        len(calls) == 8 and len(assertions) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "MK5 uses current SciPy trapezoid with no legacy NumPy access",
        compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0
        and "from scipy.integrate import solve_bvp, trapezoid" in source_text,
    )
    reproduction = yaml.safe_load(
        (CAMPAIGN / "evidence/source-reproduction.yaml").read_text()
    )
    checks.check(
        "single native execution reached all eight checks without rerun",
        reproduction["native"]["exit_code"] == 0
        and reproduction["native"]["runtime_checks"] == 8
        and reproduction["terminal_tally"] == "ALL_8_CHECKS_PASS",
    )

    radius = sp.symbols("r", positive=True)
    field_symbol, derivative_symbol = sp.symbols("q p", real=True)
    degree, angular = sp.symbols("B I", positive=True)
    c6, c0 = sp.symbols("c6 c0", nonnegative=True)
    profile = sp.Function("f")(radius)
    density = generalized_skyrme_radial_energy_density(
        field_symbol,
        derivative_symbol,
        radius,
        degree,
        angular,
        c6,
        c0,
    )
    substitutions = {
        field_symbol: profile,
        derivative_symbol: sp.diff(profile, radius),
    }
    direct_residual = sp.simplify(
        (
            sp.diff(sp.diff(density, derivative_symbol).subs(substitutions), radius)
            - sp.diff(density, field_symbol).subs(substitutions)
        )
        / 2
    )
    canonical_residual = generalized_skyrme_radial_euler_lagrange_residual(
        profile,
        radius,
        degree,
        angular,
        c6,
        c0,
    )
    checks.check(
        "independent symbolic variation gives the canonical extended equation",
        sp.simplify(direct_residual - canonical_residual) == 0,
    )
    checks.check(
        "zero extra coefficients exactly recover C-RPROF-001",
        sp.simplify(
            density.subs({c6: 0, c0: 0})
            - rational_map_radial_energy_density(
                field_symbol,
                derivative_symbol,
                radius,
                degree,
                angular,
            )
        )
        == 0
        and sp.simplify(
            canonical_residual.subs({c6: 0, c0: 0})
            - rational_map_radial_euler_lagrange_residual(
                profile,
                radius,
                degree,
                angular,
            )
        )
        == 0,
    )
    checks.check(
        "declared density is nonnegative and coefficient mutations are load bearing",
        generalized_skyrme_radial_energy_density(
            sp.pi / 3,
            sp.Rational(-2, 5),
            2,
            4,
            7,
            sp.Rational(1, 2),
            sp.Rational(1, 4),
        ).is_positive
        is True
        and sp.simplify(sp.diff(density, c6)) != 0
        and sp.simplify(sp.diff(density, c0)) != 0,
    )

    lam, mu, coupling, scale = sp.symbols("lambda mu e F", positive=True)
    reduced_c6, reduced_c0 = generalized_skyrme_reduced_coefficients(
        lam,
        mu,
        coupling,
        scale,
    )
    lambda_a = sp.pi**2 * lam
    epsilon_bps = scale / (coupling * lam * mu)
    checks.check(
        "accepted lambda convention gives both reduced coefficient forms",
        sp.simplify(
            reduced_c6
            - lambda_a**2 * coupling**4 * scale**2 / (8 * sp.pi**4)
        )
        == 0
        and reduced_c0 == 32 * mu**2 / (coupling**2 * scale**4),
    )
    checks.check(
        "coefficient product is four over accepted epsilon squared only conditionally",
        sp.simplify(reduced_c6 * reduced_c0 - 4 / epsilon_bps**2) == 0,
    )
    e2, e4, e6, e0, dilation = sp.symbols("E2 E4 E6 E0 s", positive=True)
    scaled = dilation * e2 + e4 / dilation + e6 / dilation**3 + dilation**3 * e0
    checks.check(
        "Derrick scaling has weights one minus one minus three plus three",
        sp.simplify(
            sp.diff(scaled, dilation).subs(dilation, 1)
            - generalized_skyrme_scaling_residual(e2, e4, e6, e0)
        )
        == 0,
    )
    endpoint_ok = True
    for b in ANGULAR:
        endpoint = generalized_skyrme_endpoint_data(b, 0.25)
        endpoint_ok &= abs(
            endpoint.origin_power * (endpoint.origin_power + 1.0) - 2.0 * b
        ) < 2.0e-14
        endpoint_ok &= abs(
            endpoint.tail_power * (endpoint.tail_power - 1.0) - 2.0 * b
        ) < 2.0e-14
    checks.check(
        "regular-origin and massive-tail data solve their linearized equations",
        endpoint_ok
        and all(
            generalized_skyrme_tail_robin_coefficient(20.0, b, 0.25)
            > generalized_skyrme_tail_robin_coefficient(20.0, b, 0.0)
            for b in ANGULAR
        ),
    )

    reference = _solve_set(20.0)
    checks.check(
        "all three checked collocation solves meet status residual and boundary gates",
        all(
            item.max_rms_residual < 1.1e-6
            and abs(item.inner_boundary_residual) < 2.0e-11
            and abs(item.outer_boundary_residual) < 2.0e-11
            for item in reference.values()
        ),
    )
    checks.check(
        "all three branches are finite monotone and stay within their endpoint range",
        all(
            np.all(np.isfinite(item.field))
            and np.all(np.isfinite(item.radial_derivative))
            and np.max(item.radial_derivative) < 2.0e-6
            and np.min(item.field) >= -2.0e-8
            and np.max(item.field) <= np.pi + 2.0e-8
            for item in reference.values()
        ),
    )
    checks.check(
        "every energy sector is nonnegative and the scaling residual is small",
        all(
            min(
                item.two_derivative_energy,
                item.four_derivative_energy,
                item.sextic_energy,
                item.potential_energy,
            )
            >= 0.0
            and item.virial_relative_residual < 2.0e-6
            for item in reference.values()
        ),
    )
    checks.check(
        "reference energy coefficients reproduce the frozen conditional claim",
        all(
            abs(reference[b].energy_coefficient - REFERENCE[b]) < 3.0e-8
            for b in REFERENCE
        ),
    )
    reference_kappa = _kappa(reference)
    checks.check(
        "reference signed difference is derived rather than hard coded",
        abs(reference_kappa - 11.85481448) < 3.0e-7,
    )

    coarse_domain = _solve_set(14.0, sample_points=6001)
    fine_domain = _solve_set(26.0, sample_points=10001)
    checks.check(
        "individual energy coefficients converge under outer-domain refinement",
        all(
            abs(reference[b].energy_coefficient - fine_domain[b].energy_coefficient)
            < abs(coarse_domain[b].energy_coefficient - fine_domain[b].energy_coefficient)
            and abs(reference[b].energy_coefficient - fine_domain[b].energy_coefficient)
            < 5.0e-6
            for b in REFERENCE
        ),
    )
    checks.check(
        "signed difference converges without hiding individual domain errors",
        abs(reference_kappa - _kappa(fine_domain))
        < abs(_kappa(coarse_domain) - _kappa(fine_domain))
        and abs(reference_kappa - _kappa(fine_domain)) < 5.0e-6,
    )

    middle = reference[2]
    sampled_coefficients = []
    for stride in (4, 2, 1):
        components = generalized_skyrme_energy_components(
            middle.radius[::stride],
            middle.field[::stride],
            middle.radial_derivative[::stride],
            2,
            ANGULAR[2],
            0.5,
            0.25,
        )
        sampled_coefficients.append(sum(components) / (12.0 * np.pi**2))
    checks.check(
        "output quadrature converges independently of the adaptive solver mesh",
        abs(sampled_coefficients[1] - sampled_coefficients[2])
        < abs(sampled_coefficients[0] - sampled_coefficients[2])
        and abs(sampled_coefficients[1] - sampled_coefficients[2]) < 2.0e-7,
    )

    tolerance_profiles = [
        solve_generalized_skyrme_radial_profile(
            2,
            ANGULAR[2],
            0.5,
            0.25,
            outer_radius=20.0,
            initial_points=401,
            sample_points=4001,
            continuation_steps=8,
            tolerance=tolerance,
        )
        for tolerance in (2.0e-6, 1.0e-6, 5.0e-7)
    ]
    checks.check(
        "solver residual decreases under isolated tolerance refinement",
        all(
            fine.max_rms_residual < coarse.max_rms_residual
            for coarse, fine in zip(tolerance_profiles, tolerance_profiles[1:])
        )
        and max(item.energy_coefficient for item in tolerance_profiles)
        - min(item.energy_coefficient for item in tolerance_profiles)
        < 3.0e-10,
    )
    cutoff_profiles = [
        solve_generalized_skyrme_radial_profile(
            4,
            ANGULAR[4],
            0.5,
            0.25,
            inner_radius=inner,
            outer_radius=20.0,
            initial_points=401,
            sample_points=4001,
            continuation_steps=8,
            tolerance=1.0e-6,
        )
        for inner in (2.0e-4, 1.0e-4, 5.0e-5)
    ]
    checks.check(
        "inner-cutoff refinement leaves the degree-four coefficient stable",
        max(item.energy_coefficient for item in cutoff_profiles)
        - min(item.energy_coefficient for item in cutoff_profiles)
        < 3.0e-10,
    )

    mutated_angular = {
        b: solve_generalized_skyrme_radial_profile(
            b,
            float(b**2),
            0.5,
            0.25,
            outer_radius=20.0,
            initial_points=401,
            sample_points=4001,
            continuation_steps=8,
            tolerance=1.0e-6,
        )
        for b in (2, 4)
    }
    mutated_angular_kappa = float(
        3.0
        * np.pi**2
        * (
            2.0 * mutated_angular[2].energy_coefficient
            - mutated_angular[4].energy_coefficient
        )
    )
    checks.check(
        "replacing squared-Jacobian averages by degree squared changes the verdict",
        abs(reference_kappa - mutated_angular_kappa) > 3.0,
    )
    zero_sextic = {
        b: solve_generalized_skyrme_radial_profile(
            b,
            ANGULAR[b],
            0.0,
            0.25,
            outer_radius=20.0,
            initial_points=401,
            sample_points=4001,
            continuation_steps=8,
            tolerance=1.0e-6,
        )
        for b in (2, 4)
    }
    zero_sextic_kappa = float(
        3.0
        * np.pi**2
        * (
            2.0 * zero_sextic[2].energy_coefficient
            - zero_sextic[4].energy_coefficient
        )
    )
    checks.check(
        "removing the sextic coefficient materially changes the signed difference",
        abs(reference_kappa - zero_sextic_kappa) > 2.5,
    )
    wrong_tail_residual = abs(
        reference[2].radial_derivative[-1]
        + generalized_skyrme_tail_robin_coefficient(20.0, 2, 0.0)
        * reference[2].field[-1]
    )
    checks.check(
        "massless-tail mutation fails on the massive reference branch",
        wrong_tail_residual > 1.0e-7,
    )

    dispositions = yaml.safe_load((ROOT / "migration/dispositions.yaml").read_text())[
        "units"
    ]
    checks.check(
        "MK1 through MK4 grant no physical coupling or full-model closure",
        all(
            dispositions[label]["disposition"] == "qualified"
            and "physical" in dispositions[label]["qualification"]
            for label in ("MK1", "MK2", "MK3", "MK4")
        ),
    )
    source_guard = "FORBIDDEN = [929 / 1000.0" in source_text and "guard_clean" in source_text
    checks.check(
        "source honesty guard reconstructs and reads the forbidden comparator",
        source_guard,
    )
    candidate = yaml.safe_load(
        (CAMPAIGN / "evidence/candidate-claim.yaml").read_text()
    )
    checks.check(
        "proposed claims remain conditional and exclude physical overreach",
        candidate["numeric_candidate"]["supplied_parameters"] == {"c6": 0.5, "c0": 0.25}
        and "physical_baryon" in candidate["numeric_candidate"]["excluded"]
        and "minimum" in candidate["numeric_candidate"]["excluded"],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
