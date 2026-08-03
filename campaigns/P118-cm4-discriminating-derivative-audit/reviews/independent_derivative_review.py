"""Implementation-independent exact review of P118's CM4 derivative ledger."""

from __future__ import annotations

from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("CM4-INDEPENDENT")

    n, a2, numerator, theta, normalization = sp.symbols(
        "n A2 B Theta kappa",
        positive=True,
    )
    barrier_energy = numerator / a2
    activation = sp.exp(-barrier_energy / theta)
    response = sp.factor(normalization * n * activation)

    checks.check(
        "fresh composition gives the displayed conditional response",
        sp.simplify(
            response
            - normalization * n * sp.exp(-numerator / (a2 * theta))
        )
        == 0,
    )
    checks.check(
        "fresh continuous count derivative is positive and count independent",
        sp.diff(response, n).is_positive is True
        and sp.diff(response, n, 2) == 0
        and sp.diff(sp.diff(response, n), n) == 0,
    )
    integer_n = sp.symbols("m", integer=True, positive=True)
    discrete_step = sp.simplify(
        response.subs(n, integer_n + 1) - response.subs(n, integer_n)
    )
    checks.check(
        "fresh integer forward difference equals the continuous extension slope",
        sp.simplify(discrete_step - sp.diff(response, n)) == 0
        and discrete_step.is_positive is True,
    )
    checks.check(
        "the chosen count-one comparison is exact but has no state semantics",
        sp.simplify(
            response
            - response.subs(n, 1)
            - normalization * activation * (n - 1)
        )
        == 0,
    )

    a2_derivative = sp.factor(sp.diff(response, a2))
    checks.check(
        "fresh A-squared derivative is exact and positive",
        sp.simplify(
            a2_derivative
            - response * numerator / (a2**2 * theta)
        )
        == 0
        and a2_derivative.is_positive is True,
    )
    checks.check(
        "fresh barrier and temperature derivatives have opposite signs",
        sp.diff(response, numerator).is_negative is True
        and sp.diff(response, theta).is_positive is True,
    )
    dimensionless_barrier = sp.simplify(numerator / (a2 * theta))
    checks.check(
        "fresh log elasticities reproduce the full conditional ledger",
        sp.simplify(n * sp.diff(sp.log(response), n)) == 1
        and sp.simplify(
            a2 * sp.diff(sp.log(response), a2) - dimensionless_barrier
        )
        == 0
        and sp.simplify(
            theta * sp.diff(sp.log(response), theta) - dimensionless_barrier
        )
        == 0
        and sp.simplify(
            numerator * sp.diff(sp.log(response), numerator)
            + dimensionless_barrier
        )
        == 0,
    )
    checks.check(
        "fresh loading limits have zero floor and finite saturation",
        sp.limit(response, a2, 0, dir="+") == 0
        and sp.limit(response, a2, sp.oo) == normalization * n,
    )
    second_derivative = sp.factor(sp.diff(response, a2, 2))
    checks.check(
        "fresh curvature changes sign at dimensionless barrier two",
        sp.simplify(
            second_derivative
            - response
            * dimensionless_barrier
            * (dimensionless_barrier - 2)
            / a2**2
        )
        == 0,
    )
    checks.check(
        "the curvature change refutes unrestricted convex loading response",
        second_derivative.subs(
            {normalization: 1, n: 1, numerator: 1, a2: 1, theta: 1}
        ).is_negative
        is True
        and second_derivative.subs(
            {normalization: 1, n: 1, numerator: 4, a2: 1, theta: 1}
        ).is_positive
        is True,
    )

    tension, coupling, wavenumber, thickness = sp.symbols(
        "T g k ell",
        positive=True,
    )
    accepted_capillary_barrier = sp.simplify(
        2 * sp.pi * tension**2 / (coupling * a2 * wavenumber**2 * thickness)
    )
    accepted_composition = sp.simplify(
        normalization * n * sp.exp(-accepted_capillary_barrier / theta)
    )
    checks.check(
        "fresh C-RG-002 composition is exactly the source family",
        sp.simplify(
            accepted_composition
            - response.subs(
                numerator,
                2 * sp.pi * tension**2 / (coupling * wavenumber**2 * thickness),
            )
        )
        == 0,
    )
    checks.check(
        "accepted capillary composition already fixes the positive A-squared sign",
        sp.diff(accepted_composition, a2).is_positive is True,
    )

    scale = sp.symbols("rho", positive=True)
    checks.check(
        "common numerator-temperature rescaling is invariant",
        sp.simplify(
            response.subs(
                {numerator: scale * numerator, theta: scale * theta},
                simultaneous=True,
            )
            - response
        )
        == 0,
    )
    target = sp.symbols("Y", positive=True)
    checks.check(
        "free normalization fits any positive magnitude",
        sp.simplify(
            response.subs(normalization, target / (n * activation)) - target
        )
        == 0,
    )
    checks.check(
        "zero physical coupling removes a rate without changing formal controls",
        0 * response == 0 and response.is_positive is True,
    )

    control_reversed = (sp.Integer(4), sp.Integer(3), sp.Integer(2))
    values_increasing = (sp.Integer(1), sp.Integer(2), sp.Integer(3))
    reversed_slopes = tuple(
        sp.simplify((y1 - y0) / (x1 - x0))
        for x0, x1, y0, y1 in zip(
            control_reversed[:-1],
            control_reversed[1:],
            values_increasing[:-1],
            values_increasing[1:],
        )
    )
    checks.check(
        "increasing values under reversed controls have negative quotient slopes",
        reversed_slopes == (-1, -1),
    )
    checks.check(
        "duplicate controls make a derivative quotient undefined",
        sp.zoo == (sp.Integer(2) - 1) / (sp.Integer(2) - 2),
    )
    checks.check(
        "unequal control and response lengths define no paired derivative ledger",
        len((2, 3)) != len((1, 2, 3)),
    )

    intercept, slope = sp.symbols("alpha beta", positive=True)
    unrelated_affine = intercept + slope * n
    checks.check(
        "an unrelated affine response has the same positive count derivative",
        sp.diff(unrelated_affine, n).is_positive is True,
    )
    count_power, loading_power = sp.symbols("p q", positive=True)
    alternative_family = sp.simplify(
        normalization
        * n**count_power
        * sp.exp(-numerator / (a2**loading_power * theta))
    )
    checks.check(
        "infinitely many alternative monomial mechanisms share both derivative signs",
        sp.diff(alternative_family, n).is_positive is True
        and sp.diff(alternative_family, a2).is_positive is True,
    )
    nonmonotone = -(n - 3) ** 2 + 10
    checks.check(
        "a nonmonotone response can pass on a selected rising sub-sweep",
        nonmonotone.subs(n, 2) < nonmonotone.subs(n, 3)
        and nonmonotone.subs(n, 3) > nonmonotone.subs(n, 4),
    )

    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())["claims"]
    claims = {claim["id"]: claim for claim in registry}
    checks.check(
        "C-RG-002 already governs the inverse-A-squared conditional barrier",
        claims["C-RG-002"]["review"] == "accepted"
        and "2*pi*T^2/(g*A^2*k^2*l_m)"
        in claims["C-RG-002"]["statement"],
    )
    checks.check(
        "C-SPN-002 already withholds a rate from the squared count coefficient",
        claims["C-SPN-002"]["review"] == "accepted"
        and "A squared ladder coefficient is not a rate"
        in claims["C-SPN-002"]["statement"],
    )
    checks.check(
        "C-CMP-001 already withholds a transition-rate interpretation",
        claims["C-CMP-001"]["review"] == "accepted"
        and "not a phase-coherence" in claims["C-CMP-001"]["statement"]
        and "transition-rate" in claims["C-CMP-001"]["statement"],
    )

    checks.mutation_sensitive(
        "fresh inverse-loading and count powers are load bearing",
        lambda candidate: sp.simplify(sp.diff(candidate, n) - sp.diff(response, n))
        == 0
        and sp.simplify(sp.diff(candidate, a2) - sp.diff(response, a2)) == 0,
        response,
        (
            normalization * n**2 * activation,
            normalization * n * sp.exp(numerator / (a2 * theta)),
            normalization * n * sp.exp(-numerator * a2 / theta),
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
