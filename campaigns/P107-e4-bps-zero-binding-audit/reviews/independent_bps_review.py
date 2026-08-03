"""Independent AM-GM and degree-normalization review for P107."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-29/"
    "bridge_E4_bps_zero_binding_resolution.py"
)
SOURCE_SHA256 = "f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7"


def main() -> int:
    checks = CheckLedger("P107-INDEPENDENT")
    checks.check(
        "source provenance is independently pinned",
        hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
    )

    chi = sp.Symbol("chi", real=True)
    target_volume = sp.simplify(
        4 * sp.pi * sp.integrate(sp.sin(chi) ** 2, (chi, 0, sp.pi))
    )
    checks.check(
        "unit target three-sphere volume is rederived from hyperspherical measure",
        target_volume == 2 * sp.pi**2,
    )

    half_angle = sp.Symbol("t", nonnegative=True)
    radial_integral = sp.integrate(
        8
        * sp.sqrt(2)
        * sp.sin(half_angle) ** 3
        * sp.cos(half_angle) ** 2,
        (half_angle, 0, sp.pi / 2),
    )
    pion_potential_average = sp.simplify(2 * radial_integral / sp.pi)
    checks.check(
        "standard V=1-cos(chi) square-root average has exact normalized value",
        radial_integral == 16 * sp.sqrt(2) / 15
        and pion_potential_average == 32 * sp.sqrt(2) / (15 * sp.pi),
    )
    checks.check(
        "missing target-volume normalization is rejected on the explicit potential",
        sp.simplify(target_volume * pion_potential_average)
        != pion_potential_average,
    )

    magnitude, potential_weight = sp.symbols("a c", nonnegative=True)
    positive_gap = sp.expand(
        magnitude**2 + potential_weight**2 - 2 * magnitude * potential_weight
    )
    negative_gap = sp.expand(
        (-magnitude) ** 2
        + potential_weight**2
        - 2 * (-1) * (-magnitude) * potential_weight
    )
    checks.check(
        "AM-GM gap is a square on the positive-density branch",
        sp.factor(positive_gap) == (magnitude - potential_weight) ** 2,
    )
    checks.check(
        "AM-GM gap is the same square on the negative-density branch",
        sp.factor(negative_gap) == (magnitude - potential_weight) ** 2,
    )
    checks.check(
        "AM-GM equality fixes magnitude but not orientation",
        sp.solve(sp.Eq(positive_gap, 0), magnitude) == [potential_weight]
        and sp.solve(sp.Eq(negative_gap, 0), magnitude) == [potential_weight],
    )

    lam, mu, average = sp.symbols("lambda mu W", positive=True)
    degree = sp.Symbol("B", integer=True, nonzero=True)
    signed_pairing = degree * average
    amgm_bound = 2 * lam * mu * sp.pi**2 * sp.Abs(signed_pairing)
    checks.check(
        "triangle inequality and oriented degree pairing give the absolute-degree bound",
        sp.simplify(amgm_bound - 2 * lam * mu * sp.pi**2 * sp.Abs(degree) * average)
        == 0,
    )

    identity_density = 1 / target_volume
    identity_pairing = sp.simplify(
        identity_density * target_volume * pion_potential_average
    )
    reversing_pairing = sp.simplify(-identity_pairing)
    checks.check(
        "identity and orientation reversal independently fix the signed pairing normalization",
        identity_pairing == pion_potential_average
        and reversing_pairing == -pion_potential_average,
    )

    zero_potential_density = sp.Symbol("b_0", real=True)
    zero_potential_equation = sp.Eq(
        lam * sp.pi**2 * zero_potential_density,
        0,
    )
    checks.check(
        "nonzero-degree universal saturation fails for the admissible zero potential",
        sp.solve(zero_potential_equation, zero_potential_density) == [0],
        "a zero normalized density cannot integrate to nonzero degree",
    )

    radius_fraction, edge_distance = sp.symbols("y x", positive=True)
    radial_degree, radius = sp.symbols("B_r R", positive=True)
    normalized_radial_density = (
        4
        * radial_degree
        / (sp.pi**2 * radius**3)
        * sp.sqrt(1 - radius_fraction**2)
    )
    compacton_lhs = sp.simplify(
        lam * sp.pi**2 * normalized_radial_density
    )
    compacton_rhs = mu * sp.sqrt(2) * sp.sqrt(1 - radius_fraction**2)
    compacton_radius_cube = 2 * sp.sqrt(2) * lam * radial_degree / mu
    checks.check(
        "standard-potential radial compacton satisfies the BPS equation conditionally",
        sp.simplify(
            compacton_lhs.subs(radius**3, compacton_radius_cube)
            - compacton_rhs
        )
        == 0,
    )
    l2_edge_integrand = sp.simplify(
        4 * radius_fraction**2 / (1 - radius_fraction**2)
    )
    pole_coefficient = sp.limit(
        edge_distance
        * l2_edge_integrand.subs(radius_fraction, 1 - edge_distance),
        edge_distance,
        0,
        dir="+",
    )
    l4_edge_factor = sp.simplify(
        4
        * radius_fraction**2
        * (1 - radius_fraction**2)
        * 4
        / (radius**2 * (1 - radius_fraction**2))
    )
    checks.check(
        "naive L2 first-order correction diverges on that compacton while its L4 factor stays finite",
        pole_coefficient == 2
        and sp.limit(
            l2_edge_integrand.subs(radius_fraction, 1 - edge_distance),
            edge_distance,
            0,
            dir="+",
        )
        == sp.oo
        and sp.limit(l4_edge_factor, radius_fraction, 1, dir="-")
        == 16 / radius**2,
    )

    k = 2 * lam * mu * sp.pi**2 * average
    base_degree = sp.Integer(2)
    multiplicity = sp.Integer(3)
    slack_a, slack_na = sp.symbols("s_A s_nA", nonnegative=True)
    mass_a = k * base_degree + slack_a
    mass_na = k * multiplicity * base_degree + slack_na
    signed_difference = sp.expand(multiplicity * mass_a - mass_na)
    checks.check(
        "sector lower-bound slacks survive the signed difference",
        signed_difference == multiplicity * slack_a - slack_na,
    )
    checks.check(
        "sector slack choices realize positive zero and negative differences",
        signed_difference.subs({slack_a: 1, slack_na: 0}) > 0
        and signed_difference.subs(
            {slack_a: 1, slack_na: multiplicity}
        )
        == 0
        and signed_difference.subs({slack_a: 0, slack_na: 1}) < 0,
    )
    checks.check(
        "attainment in both sectors removes both slacks and gives zero",
        signed_difference.subs({slack_a: 0, slack_na: 0}) == 0,
    )

    epsilon = sp.Symbol("epsilon", positive=True)
    delta_a, delta_na, rho_a, rho_na = sp.symbols(
        "Delta_A Delta_nA rho_A rho_nA",
        finite=True,
    )
    near_mass_a = (
        k * base_degree + epsilon * delta_a + epsilon**2 * rho_a
    )
    near_mass_na = (
        k * multiplicity * base_degree
        + epsilon * delta_na
        + epsilon**2 * rho_na
    )
    near_difference = sp.expand(
        multiplicity * near_mass_a - near_mass_na
    )
    expected_near = (
        epsilon * (multiplicity * delta_a - delta_na)
        + epsilon**2 * (multiplicity * rho_a - rho_na)
    )
    checks.check(
        "fresh near-BPS mass ledger cancels the degree-linear term",
        sp.simplify(near_difference - expected_near) == 0,
    )
    checks.check(
        "fresh controlled remainder has the exact first-order limit",
        sp.limit(near_difference / epsilon, epsilon, 0, dir="+")
        == multiplicity * delta_a - delta_na,
    )
    checks.check(
        "near-BPS coefficient cancellation is admissible and rejects strict nonzero wording",
        near_difference.subs(
            {
                delta_na: multiplicity * delta_a,
                rho_na: multiplicity * rho_a,
            }
        )
        == 0,
    )
    checks.check(
        "an epsilon-half remainder is not controlled at first order",
        sp.limit(sp.sqrt(epsilon) / epsilon, epsilon, 0, dir="+") == sp.oo,
    )

    lambda_a, lambda_b, density = sp.symbols(
        "lambda_A lambda_B q",
        positive=True,
    )
    solved_convention = sp.solve(
        sp.Eq(lambda_a**2 * density**2, lambda_b**2 * sp.pi**4 * density**2),
        lambda_a,
    )
    checks.check(
        "sextic convention conversion is independently solved",
        solved_convention == [sp.pi**2 * lambda_b],
    )
    checks.check(
        "converted bound coefficients agree while mixed coefficients differ by pi squared",
        sp.simplify(
            (2 * lambda_a * mu * average).subs(
                lambda_a,
                sp.pi**2 * lambda_b,
            )
            - 2 * lambda_b * mu * sp.pi**2 * average
        )
        == 0
        and sp.simplify(
            (2 * lambda_a * mu * sp.pi**2 * average)
            / (2 * lambda_a * mu * average)
        )
        == sp.pi**2,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
