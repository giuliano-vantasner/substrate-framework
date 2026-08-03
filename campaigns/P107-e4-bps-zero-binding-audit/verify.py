"""Primary exact verifier for the P107 E4 BPS-bound audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.bps_energy import (
    bogomolny_density_decomposition,
    bps_bound_per_absolute_degree,
    bps_topological_lower_bound,
    conditional_attained_bps_sector_energy,
    degree_weighted_target_pairing,
    near_bps_mass_difference,
    normalized_sqrt_potential_average,
    target_three_sphere_volume,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-29/"
    "bridge_E4_bps_zero_binding_resolution.py"
)
SOURCE_SHA256 = "f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7"
FROZEN_CONTRACT_SHA256 = "57f050a8465716693667de333726986e7385b55c71e33b416934d3ecbe7706cd"


def _campaign_root() -> Path:
    return Path(__file__).resolve().parent


def _normalized_contract_bytes() -> bytes:
    return (
        (_campaign_root() / "proposal.yaml")
        .read_bytes()
        .replace(b"status: accepted\n", b"status: draft\n")
    )


def main() -> int:
    checks = CheckLedger("P107")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "pre-source proposal and frozen snapshot remain identical",
        hashlib.sha256(_normalized_contract_bytes()).hexdigest()
        == FROZEN_CONTRACT_SHA256
        and hashlib.sha256(
            (_campaign_root() / "evidence/frozen-proposal.yaml").read_bytes()
        ).hexdigest()
        == FROZEN_CONTRACT_SHA256,
    )
    literal_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source has five literal predicates and a dynamic terminal tally",
        len(literal_checks) == 5
        and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source has no NumPy quadrature compatibility surface",
        "import numpy" not in source_text
        and "np.trapz" not in source_text
        and "np.trapezoid" not in source_text,
    )
    checks.check(
        "source assumes positive density and degree rather than auditing orientation",
        'sp.symbols("lambda mu b0 V B W epsilon", positive=True)' in source_text
        and "sign(B)" not in source_text,
    )
    checks.check(
        "source hard-codes linear sector energy before its zero-binding check",
        "M_bps = lambda Bn: 2 * lam * mu * sp.pi ** 2 * W * Bn" in source_text
        and "zero_binding = all" in source_text,
    )
    checks.check(
        "source near-BPS check has no remainder or physical coefficient derivation",
        'dM = sp.Function("dM")' in source_text
        and "M_near = lambda Bn: Bn * M1_bps + eps * dM(Bn)" in source_text
        and "remainder" not in source_text,
    )

    lam, mu, potential = sp.symbols("lambda mu V", positive=True)
    density = sp.Symbol("b_0", real=True)
    branches = {
        orientation: bogomolny_density_decomposition(
            density,
            potential,
            lam,
            mu,
            orientation=orientation,
        )
        for orientation in (-1, 1)
    }
    checks.check(
        "both orientation branches reconstruct the declared energy exactly",
        all(result.identity_residual == 0 for result in branches.values()),
    )
    for orientation, result in branches.items():
        expected_density = orientation * mu * sp.sqrt(potential) / (
            lam * sp.pi**2
        )
        solved_density = sp.solve(
            sp.Eq(result.saturation_residual, 0),
            density,
        )
        checks.check(
            f"orientation {orientation:+d} equality condition is necessary and sufficient",
            solved_density == [expected_density]
            and sp.simplify(
                result.square_density.subs(density, expected_density)
            )
            == 0,
        )
    positive_saturation = mu * sp.sqrt(potential) / (lam * sp.pi**2)
    checks.check(
        "wrong orientation does not saturate a nonzero positive branch",
        sp.simplify(
            branches[-1].saturation_residual.subs(
                density,
                positive_saturation,
            )
        )
        == 2 * mu * sp.sqrt(potential),
    )

    target_integral, average = sp.symbols("I_sqrtV W", positive=True)
    checks.check(
        "target average retains the unit S3 volume normalization",
        target_three_sphere_volume() == 2 * sp.pi**2
        and normalized_sqrt_potential_average(target_integral)
        == target_integral / (2 * sp.pi**2),
    )
    checks.mutation_sensitive(
        "target volume factor is load bearing",
        lambda candidate: sp.simplify(
            candidate - target_integral / (2 * sp.pi**2)
        )
        == 0,
        normalized_sqrt_potential_average(target_integral),
        [target_integral, target_integral / (4 * sp.pi), target_integral / sp.pi**2],
    )
    checks.check(
        "oriented pairing flips sign while the lower bound uses absolute degree",
        degree_weighted_target_pairing(3, average) == 3 * average
        and degree_weighted_target_pairing(-3, average) == -3 * average
        and bps_topological_lower_bound(3, lam, mu, average)
        == bps_topological_lower_bound(-3, lam, mu, average),
    )
    bound_coefficient = bps_bound_per_absolute_degree(lam, mu, average)
    checks.check(
        "degree theorem and branch choice give the normalized cross-term bound",
        sp.simplify(
            2 * lam * mu * sp.pi**2 * degree_weighted_target_pairing(3, average)
            - 3 * bound_coefficient
        )
        == 0
        and bound_coefficient == 2 * sp.pi**2 * lam * mu * average,
    )
    checks.mutation_sensitive(
        "sextic convention pi-squared factor is load bearing",
        lambda candidate: sp.simplify(candidate - bound_coefficient) == 0,
        2 * sp.pi**2 * lam * mu * average,
        [
            2 * lam * mu * average,
            2 * sp.pi * lam * mu * average,
            2 * sp.pi**4 * lam * mu * average,
        ],
    )

    energy_unit, length_unit = sp.symbols("E L", positive=True)
    density_dimension = length_unit**-3
    lambda_dimension = sp.sqrt(energy_unit) * length_unit ** sp.Rational(3, 2)
    mu_dimension = sp.sqrt(energy_unit) * length_unit ** sp.Rational(-3, 2)
    sextic_integrated_dimension = sp.simplify(
        lambda_dimension**2 * density_dimension**2 * length_unit**3
    )
    potential_integrated_dimension = sp.simplify(
        mu_dimension**2 * length_unit**3
    )
    checks.check(
        "both declared energy terms and lambda-mu bound have energy dimension",
        sextic_integrated_dimension == energy_unit
        and potential_integrated_dimension == energy_unit
        and sp.simplify(lambda_dimension * mu_dimension) == energy_unit,
    )

    zero_potential = bogomolny_density_decomposition(
        density,
        0,
        lam,
        mu,
        orientation=1,
    )
    checks.check(
        "zero potential is a counterexample to universal nonzero-degree saturation",
        sp.solve(sp.Eq(zero_potential.saturation_residual, 0), density) == [0]
        and degree_weighted_target_pairing(1, 0) == 0,
        "saturation forces density zero, whose integral cannot be degree one",
    )

    base_degree, multiplicity = 2, 3
    bound_a = bps_topological_lower_bound(
        base_degree,
        lam,
        mu,
        average,
    )
    bound_na = bps_topological_lower_bound(
        base_degree * multiplicity,
        lam,
        mu,
        average,
    )
    slack_a, slack_na = sp.symbols("s_A s_nA", nonnegative=True)
    slack_difference = sp.expand(
        multiplicity * (bound_a + slack_a) - (bound_na + slack_na)
    )
    checks.check(
        "linear lower bounds alone leave the signed sector difference uncontrolled",
        sp.simplify(slack_difference - (multiplicity * slack_a - slack_na)) == 0
        and slack_difference.subs({slack_a: 1, slack_na: 0}) > 0
        and slack_difference.subs({slack_a: 0, slack_na: 1}) < 0
        and slack_difference.subs({slack_a: 1, slack_na: multiplicity}) == 0,
    )
    attained_a = conditional_attained_bps_sector_energy(
        base_degree,
        lam,
        mu,
        average,
    )
    attained_na = conditional_attained_bps_sector_energy(
        base_degree * multiplicity,
        lam,
        mu,
        average,
    )
    checks.check(
        "actual attainment in both compared sectors gives exact zero difference",
        sp.simplify(multiplicity * attained_a - attained_na) == 0,
    )

    epsilon = sp.Symbol("epsilon", positive=True)
    delta_a, delta_na, rho_a, rho_na, k = sp.symbols(
        "Delta_A Delta_nA rho_A rho_nA K",
        real=True,
    )
    expansion = near_bps_mass_difference(
        base_degree,
        base_degree * multiplicity,
        multiplicity=multiplicity,
        bps_energy_per_degree=k,
        epsilon=epsilon,
        base_correction=delta_a,
        composite_correction=delta_na,
        base_remainder=epsilon**2 * rho_a,
        composite_remainder=epsilon**2 * rho_na,
    )
    expected = (
        epsilon * (multiplicity * delta_a - delta_na)
        + epsilon**2 * (multiplicity * rho_a - rho_na)
    )
    checks.check(
        "balanced near-BPS ledger cancels only the degree-linear term",
        expansion.degree_balance == 0
        and expansion.bps_term == 0
        and sp.simplify(expansion.expression - expected) == 0,
    )
    checks.check(
        "controlled quadratic remainders give the declared first-order coefficient",
        sp.limit(expansion.expression / epsilon, epsilon, 0, dir="+")
        == multiplicity * delta_a - delta_na,
    )
    checks.check(
        "the first-order coefficient can be positive zero or negative",
        expansion.linear_coefficient.subs({delta_a: 1, delta_na: 2}) > 0
        and expansion.linear_coefficient.subs(
            {delta_a: 1, delta_na: multiplicity}
        )
        == 0
        and expansion.linear_coefficient.subs({delta_a: 1, delta_na: 4}) < 0,
    )
    uncontrolled = near_bps_mass_difference(
        base_degree,
        base_degree * multiplicity,
        multiplicity=multiplicity,
        bps_energy_per_degree=k,
        epsilon=epsilon,
        base_correction=0,
        composite_correction=0,
        base_remainder=sp.sqrt(epsilon),
        composite_remainder=0,
    )
    checks.check(
        "an uncontrolled remainder can invalidate an O-epsilon conclusion",
        sp.limit(uncontrolled.expression / epsilon, epsilon, 0, dir="+")
        == sp.oo,
    )
    unbalanced = near_bps_mass_difference(
        base_degree,
        base_degree * multiplicity - 1,
        multiplicity=multiplicity,
        bps_energy_per_degree=k,
        epsilon=epsilon,
        base_correction=delta_a,
        composite_correction=delta_na,
    )
    checks.check(
        "degree conservation is load bearing for zeroth-order cancellation",
        unbalanced.degree_balance == 1
        and unbalanced.expression.subs(epsilon, 0) == k,
    )

    lambda_b = sp.Symbol("lambda_B", positive=True)
    lambda_a = sp.Symbol("lambda_A", positive=True)
    convention_relation = {lambda_a: sp.pi**2 * lambda_b}
    density_symbol = sp.Symbol("q", real=True)
    checks.check(
        "sextic coupling conventions agree only after lambda_A=pi^2 lambda_B",
        sp.simplify(
            (lambda_a**2 * density_symbol**2).subs(convention_relation)
            - lambda_b**2 * sp.pi**4 * density_symbol**2
        )
        == 0
        and sp.simplify(
            (2 * lambda_a * mu * average).subs(convention_relation)
            - 2 * lambda_b * mu * sp.pi**2 * average
        )
        == 0,
    )
    checks.check(
        "mixing the two coupling conventions creates exactly one pi-squared error",
        sp.simplify(
            (2 * lambda_a * mu * sp.pi**2 * average).subs(convention_relation)
            / (2 * lambda_a * mu * average).subs(convention_relation)
        )
        == sp.pi**2,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
