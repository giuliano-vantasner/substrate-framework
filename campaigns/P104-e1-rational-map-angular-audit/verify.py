"""Primary exact, numeric, source, and interpretation verifier for P104 E1."""

from __future__ import annotations

import ast
import hashlib
import math
from pathlib import Path

import numpy as np
import sympy as sp
import yaml

from substrate_framework.rational_maps import (
    axial_rational_map_angular_integral,
    exact_rational_map_degree,
    rational_map_angular_lower_bound,
    rational_map_sphere_integrals,
    rotate_rational_map_about_axis,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-29/"
    "bridge_E1_rational_map_integrals.py"
)
SOURCE_SHA256 = "1afa9ba8ade88912e7361bbbd6f59a9fce5cc114c75ddf604a6439bc066ae2d1"
CONTRACT_SHA256 = "8fea2a864993960cb837bc26ae61fe97a5701a474edceaeb0a35de77c5b1bd4e"
FREEZE_SHA256 = "2c1c30f2a03e037f88514fb950ed2980ee0262fc759e19f4daa4b5e0a1aea69e"


def _campaign_path() -> Path:
    candidates = (
        Path("campaigns/P104-e1-rational-map-angular-audit"),
        Path("proposals/P104-e1-rational-map-angular-audit"),
    )
    return next(path for path in candidates if path.exists())


def _accepted_claims() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text(encoding="utf-8"))
    return {claim["id"]: claim for claim in registry["claims"]}


def _cubic_coefficients(scale: float = 2.0 * math.sqrt(3.0)) -> tuple[np.ndarray, np.ndarray]:
    return (
        np.array([1.0, 0.0, 1j * scale, 0.0, 1.0]),
        np.array([1.0, 0.0, -1j * scale, 0.0, 1.0]),
    )


def main() -> int:
    checks = CheckLedger("C-RMAP-001/002")
    campaign = _campaign_path()
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash and pinned E1 body are unchanged",
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
        "source quadrature applies trapezoids to midpoint nodes without endpoints",
        "(np.arange(n_th) + 0.5)" in source_text
        and "(np.arange(n_ph) + 0.5)" in source_text
        and "trapezoid(trapezoid(integrand * weight" in source_text,
    )

    z = sp.Symbol("z")
    identity_degree = exact_rational_map_degree([1, 0], [1])
    checks.check(
        "identity map is exactly coprime and degree one",
        identity_degree.is_coprime and identity_degree.degree == 1,
    )
    common_factor = exact_rational_map_degree([1, 1, 0], [1, 1])
    checks.check(
        "common-factor cancellation changes apparent degree without changing the map",
        common_factor.numerator_degree == 2
        and common_factor.common_factor_degree == 1
        and common_factor.degree == 1
        and sp.simplify(
            common_factor.reduced_numerator / common_factor.reduced_denominator - z
        )
        == 0,
    )
    cubic_exact_coefficient = 2 * sp.I * sp.sqrt(3)
    cubic_degree = exact_rational_map_degree(
        [1, 0, cubic_exact_coefficient, 0, 1],
        [1, 0, -cubic_exact_coefficient, 0, 1],
    )
    checks.check(
        "declared cubic map is exactly coprime and degree four",
        cubic_degree.is_coprime and cubic_degree.degree == 4,
    )

    degree = sp.Symbol("B", positive=True)
    inverse_degree = 1 / degree
    radial_variable = sp.Symbol("x", positive=True)
    gamma_product = sp.gamma(2 - inverse_degree) * sp.gamma(2 + inverse_degree)
    transformed_radial_integrand = (
        degree**3
        * radial_variable ** (1 - inverse_degree)
        * (1 + radial_variable**inverse_degree) ** 2
        / (1 + radial_variable) ** 4
    )
    expanded_radial_integrand = degree**3 * (
        radial_variable ** (1 - inverse_degree)
        + 2 * radial_variable
        + radial_variable ** (1 + inverse_degree)
    ) / (1 + radial_variable) ** 4
    checks.check(
        "the axial radial substitution expands into three Euler-beta kernels",
        sp.simplify(transformed_radial_integrand - expanded_radial_integrand) == 0,
    )
    beta_reduction = degree**3 * (
        sp.beta(2 - inverse_degree, 2 + inverse_degree)
        + 2 * sp.beta(2, 2)
        + sp.beta(2 + inverse_degree, 2 - inverse_degree)
    )
    preregistered = degree**3 * (1 + gamma_product) / 3
    checks.check(
        "the three Euler-beta integrals give the preregistered gamma formula",
        sp.simplify(sp.expand_func(beta_reduction) - preregistered) == 0,
    )
    reflection_form = (
        (1 - inverse_degree**2)
        * sp.pi
        * inverse_degree
        / sp.sin(sp.pi * inverse_degree)
    )
    checks.check(
        "gamma reflection independently simplifies the axial correction",
        sp.simplify(sp.expand_func(gamma_product) - reflection_form) == 0,
    )
    t = sp.Symbol("t", positive=True)
    checks.check(
        "axial pullback area normalizes exactly to degree B",
        sp.integrate(degree / (1 + t) ** 2, (t, 0, sp.oo)) == degree,
    )
    checks.check(
        "identity and degree-two axial angular values are exact",
        axial_rational_map_angular_integral(1) == 1
        and sp.simplify(
            axial_rational_map_angular_integral(2)
            - sp.pi
            - sp.Rational(8, 3)
        )
        == 0,
    )
    checks.check(
        "axial maps obey the Cauchy lower bound and are strict above degree one",
        all(
            axial_rational_map_angular_integral(value)
            > rational_map_angular_lower_bound(value)
            for value in range(2, 9)
        )
        and axial_rational_map_angular_integral(1)
        == rational_map_angular_lower_bound(1),
    )
    angular_value = sp.Symbol("I", real=True)
    total_measure = 4 * sp.pi
    area_integral = total_measure * degree
    square_integral = total_measure * angular_value
    normalized_square_deficit = sp.expand(
        (
            square_integral
            - 2 * degree * area_integral
            + degree**2 * total_measure
        )
        / total_measure
    )
    real_jacobian = sp.Symbol("J", real=True)
    checks.check(
        "the degree identity makes I minus B squared a normalized square integral",
        sp.simplify(normalized_square_deficit - (angular_value - degree**2)) == 0
        and sp.ask(sp.Q.nonnegative((real_jacobian - degree) ** 2)) is True,
    )
    checks.mutation_sensitive(
        "axial normalization derivative and measure factors are load bearing",
        lambda factors: sp.simplify(
            factors[0]
            * factors[1]
            * sp.integrate(1 / (1 + t) ** 2, (t, 0, sp.oo))
            - factors[2]
        )
        == 0,
        (1, 2, 2),
        ((2, 2, 2), (1, 1, 2), (1, 2, 4)),
    )

    identity = rational_map_sphere_integrals(
        [1.0, 0.0],
        [1.0],
        declared_degree=1,
        polar_order=16,
        azimuthal_order=32,
    )
    checks.check(
        "compact sphere cubature integrates the identity map to roundoff",
        abs(identity.normalized_area - 1.0) < 2.0e-14
        and abs(identity.angular_integral - 1.0) < 2.0e-14,
    )
    exact_degree_two = float(axial_rational_map_angular_integral(2))
    axial_orders = (16, 24, 32, 48)
    axial_values = [
        rational_map_sphere_integrals(
            [1.0, 0.0, 0.0],
            [1.0],
            declared_degree=2,
            polar_order=order,
            azimuthal_order=2 * order,
        )
        for order in axial_orders
    ]
    axial_errors = [
        abs(value.angular_integral - exact_degree_two) / exact_degree_two
        for value in axial_values
    ]
    checks.check(
        "degree-two cubature converges to the exact axial value",
        axial_errors[1] < axial_errors[0]
        and max(axial_errors[1:]) < 2.0e-13
        and axial_values[-1].degree_area_relative_error < 2.0e-13,
    )

    cubic_numerator, cubic_denominator = _cubic_coefficients()
    cubic_orders = (16, 24, 32, 48)
    cubic_values = [
        rational_map_sphere_integrals(
            cubic_numerator,
            cubic_denominator,
            declared_degree=4,
            polar_order=order,
            azimuthal_order=2 * order,
        )
        for order in cubic_orders
    ]
    cubic_area_errors = [value.degree_area_relative_error for value in cubic_values]
    cubic_successive = [
        abs(right.angular_integral - left.angular_integral) / right.angular_integral
        for left, right in zip(cubic_values, cubic_values[1:])
    ]
    checks.check(
        "cubic pullback area converges monotonically to degree four",
        all(right < left for left, right in zip(cubic_area_errors, cubic_area_errors[1:]))
        and cubic_area_errors[-1] < 2.0e-13,
    )
    checks.check(
        "cubic angular integral converges across four tensor orders",
        all(right < left for left, right in zip(cubic_successive, cubic_successive[1:]))
        and cubic_successive[-1] < 1.0e-9,
    )
    cubic_final = cubic_values[-1].angular_integral
    checks.check(
        "refined cubic value is finite positive and above the degree bound",
        math.isfinite(cubic_final)
        and cubic_final > float(rational_map_angular_lower_bound(4))
        and 20.64 < cubic_final < 20.66,
        f"I4={cubic_final}",
    )
    rotated_numerator, rotated_denominator = rotate_rational_map_about_axis(
        cubic_numerator,
        cubic_denominator,
        domain_angle=0.37,
        target_angle=-0.52,
    )
    rotated = rational_map_sphere_integrals(
        rotated_numerator,
        rotated_denominator,
        declared_degree=4,
        polar_order=48,
        azimuthal_order=96,
    )
    checks.check(
        "domain and target axis rotations preserve cubic degree area and I",
        math.isclose(rotated.normalized_area, cubic_values[-1].normalized_area, rel_tol=2.0e-13)
        and math.isclose(rotated.angular_integral, cubic_final, rel_tol=2.0e-13),
    )
    mutated_numerator, mutated_denominator = _cubic_coefficients(3.2)
    mutated = rational_map_sphere_integrals(
        mutated_numerator,
        mutated_denominator,
        declared_degree=4,
        polar_order=40,
        azimuthal_order=80,
    )
    checks.check(
        "cubic coefficient is load bearing while degree remains four",
        abs(mutated.normalized_area - 4.0) < 2.0e-10
        and mutated.angular_integral > cubic_final + 0.1,
    )
    shifted = rational_map_sphere_integrals(
        [1.0, 0.0, 0.6],
        [1.0],
        declared_degree=2,
        polar_order=48,
        azimuthal_order=96,
    )
    checks.check(
        "one shifted degree-two map costs more without proving global minimality",
        abs(shifted.normalized_area - 2.0) < 2.0e-12
        and shifted.angular_integral > exact_degree_two,
    )

    reproduction = yaml.safe_load(
        (campaign / "attempts/0001/result.yaml").read_text(encoding="utf-8")
    )
    source_results = reproduction["source_results"]
    source_i1 = float(source_results["coarse_identity"])
    source_i2 = float(source_results["coarse_degree_two"])
    source_i4 = float(source_results["coarse_degree_four"])
    checks.check(
        "source identity error exposes endpoint-domain loss despite its loose pass band",
        abs(source_i1 - 1.0) > 1.0e-3
        and abs(source_i1 - 1.0) < 5.0e-3,
    )
    checks.check(
        "source degree-two decimal is biased relative to the exact theorem",
        abs(source_i2 - exact_degree_two) / exact_degree_two > 1.0e-3
        and axial_errors[-1] < 2.0e-13,
    )
    checks.check(
        "source cubic decimal is biased beyond the refined method uncertainty",
        abs(source_i4 - cubic_final) / cubic_final > 5.0e-4
        and cubic_successive[-1] < 1.0e-9,
    )
    checks.check(
        "small source coarse-to-fine change does not bound its remaining exact error",
        float(source_results["degree_two_relative_change"])
        < abs(float(source_results["fine_degree_two"]) - exact_degree_two) / exact_degree_two
        and float(source_results["degree_four_relative_change"])
        < abs(float(source_results["fine_degree_four"]) - cubic_final) / cubic_final,
    )

    claims = _accepted_claims()
    proposed = {"C-RMAP-001", "C-RMAP-002"}
    accepted_proposed = proposed.intersection(claims)
    checks.check(
        "claim identifiers are either reserved only or accepted with exact P104 provenance",
        not accepted_proposed
        or all(
            claims[claim_id]["provenance"]
            == "campaigns/P104-e1-rational-map-angular-audit/adjudication.yaml"
            for claim_id in accepted_proposed
        ),
    )
    checks.check(
        "accepted interpretation ceilings remain explicit",
        all(claim_id in claims for claim_id in ("C-DIM-002", "C-SK-001", "C-TOP-002", "C-MOD-001", "C-MOD-002"))
        and "pending B1/E2/E4/S2" in claims["C-MOD-002"]["assumptions"][-1]
        and "physical Skyrme action" in claims["C-MOD-001"]["statement"],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
