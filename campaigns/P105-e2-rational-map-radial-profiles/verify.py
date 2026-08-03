"""Primary exact, numeric, source, and interpretation verifier for P105 E2."""

from __future__ import annotations

import ast
import hashlib
import math
from pathlib import Path

import numpy as np
import sympy as sp
import yaml

from substrate_framework.numerics import SolverTolerances
from substrate_framework.radial_modes import (
    derrick_scaling_evidence,
    option_c_euler_lagrange_residual,
    option_c_radial_energy_density,
)
from substrate_framework.rational_map_radial import (
    massless_tail_boundary_residual,
    rational_map_radial_endpoint_exponents,
    rational_map_radial_energy_components,
    rational_map_radial_energy_density,
    rational_map_radial_euler_lagrange_residual,
    rational_map_radial_rhs,
    regular_origin_boundary_residual,
    solve_rational_map_radial_profile,
)
from substrate_framework.rational_maps import axial_rational_map_angular_integral
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-29/"
    "bridge_E2_multi_skyrmion_solutions.py"
)
SOURCE_SHA256 = "fdde30878eaf1f8dff7fce9c2d9d4234d1d6e14566be6d2ee56dd1926481c46f"
CONTRACT_SHA256 = "ab05676296c4396dfd60f5b82343a96f9046c9380d6dc381a3fbbdef5187fbd5"
FREEZE_SHA256 = "1f19fb7aa0bebd1052dab57655af8a2991d1f07bb7974fca26b363ac483824d8"
ACCEPTED_ANGULAR = {
    1: 1.0,
    2: float(axial_rational_map_angular_integral(2)),
    4: 20.6496264884189,
}
BASE_TOLERANCES = SolverTolerances(
    rtol=3.0e-10,
    atol=3.0e-12,
    max_step=0.05,
)


def _campaign_path() -> Path:
    candidates = (
        Path("campaigns/P105-e2-rational-map-radial-profiles"),
        Path("proposals/P105-e2-rational-map-radial-profiles"),
    )
    return next(path for path in candidates if path.exists())


def _accepted_claims() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text(encoding="utf-8"))
    return {claim["id"]: claim for claim in registry["claims"]}


def _coefficient_from_samples(profile: object, stride: int) -> float:
    radius = profile.radius[::stride]
    field = profile.field[::stride]
    derivative = profile.radial_derivative[::stride]
    if radius[-1] != profile.radius[-1]:
        raise AssertionError("sample stride omitted the outer endpoint")
    two, four = rational_map_radial_energy_components(
        radius,
        field,
        derivative,
        profile.degree,
        profile.angular_integral,
    )
    total = (
        two
        + four
        + profile.origin_two_derivative_estimate
        + profile.origin_four_derivative_estimate
        + profile.tail_two_derivative_estimate
        + profile.tail_four_derivative_estimate
    )
    return total / (12.0 * np.pi**2)


def main() -> int:
    checks = CheckLedger("C-RPROF-001/002")
    campaign = _campaign_path()
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash and pinned E2 body are unchanged",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    normalized_contract = (campaign / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n",
        b"status: active\n",
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    checks.check(
        "pre-source commitment is immutable",
        hashlib.sha256((campaign / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA256,
    )
    provenance = yaml.safe_load(
        (campaign / "evidence/primary-provenance.yaml").read_text(encoding="utf-8")
    )["implementation"]
    provenance_paths = {
        "package_exports_sha256": Path(provenance["package_exports"]),
        "module_sha256": Path(provenance["module"]),
        "tests_sha256": Path(provenance["tests"]),
        "primary_verifier_sha256": Path(provenance["primary_verifier"]),
        "independent_review_sha256": Path(provenance["independent_review"]),
    }
    checks.check(
        "canonical implementation test and verifier hashes match provenance",
        all(
            hashlib.sha256(path.read_bytes()).hexdigest() == provenance[key]
            for key, path in provenance_paths.items()
        ),
    )
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source has six literal checks and a dynamic terminal tally",
        len(source_checks) == 6
        and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source selects current trapezoid before its legacy fallback",
        'np.trapezoid if hasattr(np, "trapezoid") else np.trapz' in source_text,
    )
    checks.check(
        "source omits solver-status gates and imposes exact vacua at finite walls",
        "sol.success" not in source_text
        and "return sol" in source_text
        and "ya[0] - np.pi, yb[0]" in source_text,
    )
    checks.check(
        "source refinement changes domain mesh and tolerance together",
        "rmax=22.0, n0=5000, tol=3e-7" in source_text,
    )

    radius = sp.symbols("r", positive=True)
    value, slope = sp.symbols("q p", real=True)
    degree, angular = sp.symbols("B I", positive=True)
    profile_symbol = sp.Function("f")(radius)
    density = rational_map_radial_energy_density(
        value,
        slope,
        radius,
        degree,
        angular,
    )
    substitutions = {
        value: profile_symbol,
        slope: sp.diff(profile_symbol, radius),
    }
    direct_residual = sp.simplify(
        (
            sp.diff(sp.diff(density, slope).subs(substitutions), radius)
            - sp.diff(density, value).subs(substitutions)
        )
        / 2
    )
    generalized_residual = rational_map_radial_euler_lagrange_residual(
        profile_symbol,
        radius,
        degree,
        angular,
    )
    checks.check(
        "exact variation derives the generalized radial equation",
        sp.simplify(direct_residual - generalized_residual) == 0,
    )
    checks.check(
        "degree one and unit angular input reduce exactly to accepted Option C",
        sp.simplify(
            rational_map_radial_energy_density(value, slope, radius, 1, 1)
            - option_c_radial_energy_density(value, slope, radius)
        )
        == 0
        and sp.simplify(
            rational_map_radial_euler_lagrange_residual(
                profile_symbol,
                radius,
                1,
                1,
            )
            - option_c_euler_lagrange_residual(profile_symbol, radius)
        )
        == 0,
    )
    sine_squared = sp.sin(value) ** 2
    exact_two_density = radius**2 * slope**2 + 2 * degree * sine_squared
    exact_four_density = (
        2 * degree * sine_squared * slope**2
        + angular * sine_squared**2 / radius**2
    )
    checks.check(
        "the exact density separates into two- and four-derivative pieces",
        sp.simplify(density - exact_two_density - exact_four_density) == 0,
    )
    e2, e4, scale = sp.symbols("E2 E4 s", positive=True)
    scaling = derrick_scaling_evidence(e2, e4, scale)
    checks.check(
        "logarithmic scaling gives the stationary E2 equals E4 identity",
        scaling.scaled_energy == sp.exp(-scale) * e2 + sp.exp(scale) * e4
        and scaling.slope_at_origin == e4 - e2
        and scaling.curvature_at_origin == e2 + e4,
    )
    endpoint = rational_map_radial_endpoint_exponents(degree)
    checks.check(
        "regular-origin and massless-tail powers solve their indicial equations",
        sp.simplify(endpoint.origin_power * (endpoint.origin_power + 1) - 2 * degree)
        == 0
        and sp.simplify(endpoint.tail_power * (endpoint.tail_power - 1) - 2 * degree)
        == 0,
    )
    test_radius = 0.04
    test_sigma = 1.6
    test_amplitude = 0.7
    origin_field = np.pi - test_amplitude * test_radius**test_sigma
    origin_slope = -test_amplitude * test_sigma * test_radius ** (test_sigma - 1.0)
    checks.mutation_sensitive(
        "origin exponent is load bearing in the asymptotic boundary residual",
        lambda exponent: abs(
            regular_origin_boundary_residual(
                test_radius,
                origin_field,
                origin_slope,
                exponent,
            )
        )
        < 2.0e-14,
        test_sigma,
        (test_sigma - 0.2, test_sigma + 0.2),
    )
    tail_radius = 18.0
    test_tail = 2.7
    tail_field = 1.3 * tail_radius**-test_tail
    tail_slope = -test_tail * 1.3 * tail_radius ** (-test_tail - 1.0)
    checks.mutation_sensitive(
        "tail exponent is load bearing in the asymptotic boundary residual",
        lambda exponent: abs(
            massless_tail_boundary_residual(
                tail_radius,
                tail_field,
                tail_slope,
                exponent,
            )
        )
        < 2.0e-14,
        test_tail,
        (test_tail - 0.2, test_tail + 0.2),
    )

    cache: dict[tuple[object, ...], object] = {}

    def solve(
        b: int,
        angular_value: float,
        *,
        inner: float = 1.0e-4,
        outer: float = 24.0,
        points: int = 1201,
        tolerances: SolverTolerances = BASE_TOLERANCES,
        bracket: tuple[float, float] = (0.5, 4.0),
    ) -> object:
        key = (
            b,
            angular_value,
            inner,
            outer,
            points,
            tolerances.rtol,
            tolerances.atol,
            tolerances.max_step,
            bracket,
        )
        if key not in cache:
            cache[key] = solve_rational_map_radial_profile(
                b,
                angular_value,
                inner_radius=inner,
                outer_radius=outer,
                sample_points=points,
                tolerances=tolerances,
                amplitude_bracket=bracket,
            )
        return cache[key]

    base_profiles = {
        b: solve(b, angular_value, points=2401)
        for b, angular_value in ACCEPTED_ANGULAR.items()
    }
    checks.check(
        "corrected-input shooting branches are finite monotone and bounded",
        all(
            np.all(np.isfinite(result.field))
            and np.all(np.isfinite(result.radial_derivative))
            and np.min(result.field) >= -2.0e-8
            and np.max(result.field) <= np.pi + 2.0e-8
            and np.max(result.radial_derivative) < 2.0e-8
            for result in base_profiles.values()
        ),
    )
    checks.check(
        "all shooting branches satisfy both asymptotic boundary residuals",
        all(
            abs(result.inner_boundary_residual) < 2.0e-12
            and abs(result.outer_boundary_residual) < 2.0e-7
            for result in base_profiles.values()
        ),
    )
    checks.check(
        "all corrected endpoint energy estimates are finite and nonnegative",
        all(
            all(
                math.isfinite(value) and value >= 0.0
                for value in (
                    result.origin_two_derivative_estimate,
                    result.origin_four_derivative_estimate,
                    result.tail_two_derivative_estimate,
                    result.tail_four_derivative_estimate,
                )
            )
            for result in base_profiles.values()
        ),
    )
    checks.check(
        "corrected-input branches satisfy the stationary virial identity",
        max(result.virial_relative_imbalance for result in base_profiles.values())
        < 3.0e-6,
    )
    per_degree = [
        base_profiles[b].per_degree_energy_coefficient
        for b in (1, 2, 4)
    ]
    checks.check(
        "the three declared stationary branches have decreasing conditional per-degree energy",
        per_degree[0] > per_degree[1] > per_degree[2],
        f"per_degree={per_degree}",
    )

    degree_four = base_profiles[4]
    rhs_second = np.asarray(
        [
            rational_map_radial_rhs(
                coordinate,
                state,
                4,
                ACCEPTED_ANGULAR[4],
            )[1]
            for coordinate, state in zip(
                degree_four.radius,
                np.column_stack(
                    (degree_four.field, degree_four.radial_derivative)
                ),
                strict=True,
            )
        ]
    )
    finite_difference_second = np.gradient(
        degree_four.radial_derivative,
        degree_four.radius,
        edge_order=2,
    )
    interior = slice(5, -5)
    relative_fd_residual = np.abs(
        finite_difference_second[interior] - rhs_second[interior]
    ) / (1.0 + np.abs(rhs_second[interior]))
    checks.check(
        "an independent centered finite difference resolves the degree-four ODE",
        np.max(relative_fd_residual) < 1.0e-3
        and np.sqrt(np.mean(relative_fd_residual**2)) < 5.0e-5,
    )
    mutated_rhs_second = np.asarray(
        [
            rational_map_radial_rhs(coordinate, state, 4, 16.0)[1]
            for coordinate, state in zip(
                degree_four.radius,
                np.column_stack(
                    (degree_four.field, degree_four.radial_derivative)
                ),
                strict=True,
            )
        ]
    )
    mutated_residual = np.abs(
        finite_difference_second[interior] - mutated_rhs_second[interior]
    ) / (1.0 + np.abs(mutated_rhs_second[interior]))
    checks.check(
        "mutating the angular coefficient breaks the resolved degree-four equation",
        np.sqrt(np.mean(mutated_residual**2))
        > 20.0 * np.sqrt(np.mean(relative_fd_residual**2)),
    )

    quadrature_coefficients = [
        _coefficient_from_samples(degree_four, stride)
        for stride in (4, 2, 1)
    ]
    quadrature_errors = [
        abs(value - quadrature_coefficients[-1])
        for value in quadrature_coefficients[:-1]
    ]
    checks.check(
        "sampled energy quadrature refines toward the finest degree-four value",
        quadrature_errors[1] < quadrature_errors[0]
        and quadrature_errors[1] / quadrature_coefficients[-1] < 2.0e-7,
    )

    domain_profiles = [
        solve(4, ACCEPTED_ANGULAR[4], outer=outer, points=int(50 * outer) + 1)
        for outer in (16.0, 24.0, 32.0)
    ]
    domain_values = [result.energy_coefficient for result in domain_profiles]
    domain_changes = [
        abs(right - left) / right
        for left, right in zip(domain_values, domain_values[1:])
    ]
    checks.check(
        "outer-domain refinement stabilizes corrected degree-four energy",
        domain_changes[-1] < domain_changes[0]
        and domain_changes[-1] < 2.0e-7,
    )
    checks.check(
        "the explicit degree-four tail estimate decreases with outer radius",
        all(
            right.tail_two_derivative_estimate < left.tail_two_derivative_estimate
            for left, right in zip(domain_profiles, domain_profiles[1:])
        ),
    )

    cutoff_profiles = [
        solve(4, ACCEPTED_ANGULAR[4], inner=inner)
        for inner in (1.0e-3, 3.0e-4, 1.0e-4)
    ]
    cutoff_values = [result.energy_coefficient for result in cutoff_profiles]
    cutoff_spread = max(cutoff_values) - min(cutoff_values)
    checks.check(
        "origin-cutoff refinement stabilizes corrected degree-four energy",
        cutoff_spread / cutoff_values[-1] < 3.0e-7,
    )
    checks.check(
        "explicit degree-four origin estimates decrease with the cutoff",
        all(
            right.origin_two_derivative_estimate
            < left.origin_two_derivative_estimate
            for left, right in zip(cutoff_profiles, cutoff_profiles[1:])
        ),
    )

    tolerance_settings = (
        SolverTolerances(rtol=1.0e-7, atol=1.0e-9, max_step=0.05),
        SolverTolerances(rtol=1.0e-9, atol=1.0e-11, max_step=0.05),
        SolverTolerances(rtol=1.0e-11, atol=1.0e-13, max_step=0.05),
    )
    tolerance_profiles = [
        solve(4, ACCEPTED_ANGULAR[4], tolerances=tolerances)
        for tolerances in tolerance_settings
    ]
    tolerance_values = [result.energy_coefficient for result in tolerance_profiles]
    checks.check(
        "isolated IVP tolerance refinement stabilizes degree-four energy",
        (max(tolerance_values) - min(tolerance_values)) / tolerance_values[-1]
        < 3.0e-6
        and abs(tolerance_values[-1] - degree_four.energy_coefficient)
        / degree_four.energy_coefficient
        < 3.0e-6,
    )

    step_settings = (
        SolverTolerances(rtol=3.0e-10, atol=3.0e-12, max_step=0.10),
        BASE_TOLERANCES,
        SolverTolerances(rtol=3.0e-10, atol=3.0e-12, max_step=0.025),
    )
    step_profiles = [
        solve(4, ACCEPTED_ANGULAR[4], tolerances=tolerances)
        for tolerances in step_settings
    ]
    step_values = [result.energy_coefficient for result in step_profiles]
    checks.check(
        "isolated maximum-step refinement stabilizes degree-four energy",
        (max(step_values) - min(step_values)) / step_values[-1] < 2.0e-7,
    )

    i_equals_b = {
        2: solve(2, 2.0, bracket=(40.0, 120.0)),
        4: solve(4, 4.0, bracket=(40.0, 120.0)),
    }
    i_equals_b_squared = {
        2: solve(2, 4.0),
        4: solve(4, 16.0),
    }
    source_biased = {
        2: solve(2, 5.794),
        4: solve(4, 20.625),
    }
    checks.check(
        "I equals B and I equals B squared are distinct solved mutations",
        all(
            result.virial_relative_imbalance < 3.0e-6
            for result in (
                *i_equals_b.values(),
                *i_equals_b_squared.values(),
            )
        )
        and all(
            abs(
                i_equals_b[b].per_degree_energy_coefficient
                - i_equals_b_squared[b].per_degree_energy_coefficient
            )
            > 0.03
            for b in (2, 4)
        ),
    )
    checks.check(
        "accepted angular inputs change energy materially relative to both simple mutations",
        all(
            abs(
                base_profiles[b].per_degree_energy_coefficient
                - mutated[b].per_degree_energy_coefficient
            )
            > 0.03
            for b in (2, 4)
            for mutated in (i_equals_b, i_equals_b_squared)
        ),
    )
    biased_shifts = [
        abs(
            base_profiles[b].per_degree_energy_coefficient
            - source_biased[b].per_degree_energy_coefficient
        )
        for b in (2, 4)
    ]
    numerical_uncertainty = max(
        quadrature_errors[1] / 4.0,
        domain_changes[-1] * degree_four.per_degree_energy_coefficient,
        cutoff_spread / 4.0,
        (max(tolerance_values) - min(tolerance_values)) / 4.0,
        (max(step_values) - min(step_values)) / 4.0,
    )
    checks.check(
        "source-biased angular values shift energies beyond numerical refinement scales",
        min(biased_shifts) > 20.0 * numerical_uncertainty,
        f"biased_shifts={biased_shifts}, uncertainty={numerical_uncertainty}",
    )
    checks.check(
        "the selected ordering survives simple-I mutations and is not their rejection oracle",
        all(
            1.231445654401988
            > mutated[2].per_degree_energy_coefficient
            > mutated[4].per_degree_energy_coefficient
            for mutated in (i_equals_b, i_equals_b_squared)
        ),
    )

    reproduction = yaml.safe_load(
        (campaign / "attempts/0001/result.yaml").read_text(encoding="utf-8")
    )
    source_results = reproduction["source_results"]
    checks.check(
        "source compatibility branch executed without a version-only abort",
        reproduction["numpy_compatibility"]["current_branch"] == "np.trapezoid"
        and reproduction["numpy_compatibility"]["compatibility_abort"] is False
        and reproduction["process"]["exit_status"] == 0,
    )
    checks.check(
        "source decimals reflect biased angular inputs and finite-wall profiles",
        abs(float(source_results["angular_degree_two_printed"]) - ACCEPTED_ANGULAR[2])
        > 1.0e-2
        and abs(float(source_results["angular_degree_four_printed"]) - ACCEPTED_ANGULAR[4])
        > 2.0e-2
        and abs(float(source_results["b2_per_degree"]) - per_degree[1]) > 3.0e-4
        and abs(float(source_results["b4_per_degree"]) - per_degree[2]) > 1.0e-4,
    )
    checks.check(
        "source I equals B guard preserves rather than destroys its reported ordering",
        float(source_results["b1"])
        > float(source_results["trivial_I_equals_B_b2_per_degree"])
        > float(source_results["trivial_I_equals_B_b4_per_degree"]),
    )

    module_text = Path(
        "src/substrate_framework/rational_map_radial.py"
    ).read_text(encoding="utf-8")
    checks.check(
        "canonical sampled integration uses only the shared compatibility helper",
        "trapezoid_integral" in module_text
        and "np.tr" + "apz" not in module_text
        and "np.tr" + "apezoid" not in module_text,
    )
    claims = _accepted_claims()
    proposed = {"C-RPROF-001", "C-RPROF-002"}
    accepted_proposed = proposed.intersection(claims)
    checks.check(
        "claim identifiers are either reserved or accepted with exact P105 provenance",
        not accepted_proposed
        or all(
            claims[claim_id]["provenance"]
            == "campaigns/P105-e2-rational-map-radial-profiles/adjudication.yaml"
            for claim_id in accepted_proposed
        ),
    )
    checks.check(
        "accepted angular and degree-one compatibility dependencies remain explicit",
        all(
            claim_id in claims
            for claim_id in (
                "C-RMAP-001",
                "C-RMAP-002",
                "C-MOD-001",
                "C-MOD-002",
            )
        )
        and "global" in claims["C-RMAP-002"]["statement"]
        and "physical Skyrme action" in claims["C-MOD-001"]["statement"],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
