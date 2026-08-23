"""Attempt 0003 driver: multi-species composition and massless collapse."""

from __future__ import annotations

import json
import sys

import sympy as sp

from substrate_framework.m5_induced_coupling import (
    massless_substrate_coupling,
    species_additivity_identity,
)
from substrate_framework.total_gravitational_coupling import (
    scheme_spread_ratio,
)
from substrate_framework.verification import CheckLedger


LAMBDA = sp.Symbol("Lambda", positive=True)


def main() -> int:
    ledger = CheckLedger("P243-attempt-0003")

    # Additivity of per-species shifts at equal mass.
    ledger.check(
        "species_additivity_identity",
        species_additivity_identity(
            field_counts=(2, 3),
            mass_squared=(sp.Rational(3, 2), sp.Rational(3, 2)),
            non_minimal_coupling=0,
            cutoff=LAMBDA,
        ),
        "shift(N1+N2) = shift(N1)+shift(N2) exactly",
    )

    # Massless collapse with the census multiplicity.
    xi_zero = massless_substrate_coupling(
        massless_count=3, non_minimal_coupling=0, cutoff=LAMBDA
    )
    expected_shift = 3 * LAMBDA**2 / (12 * sp.pi)
    ledger.check(
        "massless_delta_closed_form",
        sp.simplify(xi_zero.induced_shift - expected_shift) == 0,
        f"Delta={xi_zero.induced_shift}",
    )
    ledger.check(
        "scheme_values_equal_at_z0",
        xi_zero.scheme_values_equal,
        "sharp and smooth agree exactly",
    )
    spread = scheme_spread_ratio(cutoff=LAMBDA, mass_squared=0)
    ledger.check(
        "spread_ratio_exactly_one_at_z0",
        sp.simplify(spread.ratio - 1) == 0,
        f"R(0)={sp.simplify(spread.ratio)}",
    )

    # Purely-induced declared reading: G_total = 4*pi/Lambda^2 at N=3, xi=0.
    ledger.check(
        "purely_induced_newton_constant",
        sp.simplify(xi_zero.newton_constant - 4 * sp.pi / LAMBDA**2) == 0,
        f"G={xi_zero.newton_constant}",
    )

    # Mutation A: conformal coupling nulls the shift identically.
    conformal = massless_substrate_coupling(
        massless_count=3, non_minimal_coupling=sp.Rational(1, 6),
        cutoff=LAMBDA,
    )
    ledger.check(
        "conformal_coupling_nulls_shift",
        sp.simplify(conformal.induced_shift) == 0,
        "Delta(xi=1/6)=0",
    )

    # Mutation B: a fourth species must move the shift.
    four = massless_substrate_coupling(
        massless_count=4, non_minimal_coupling=0, cutoff=LAMBDA
    )
    ledger.check(
        "species_count_moves_shift",
        sp.simplify(four.induced_shift - xi_zero.induced_shift) != 0,
        f"Delta(N=4)={four.induced_shift}",
    )

    # Mutation C: positive baseline enters additively and keeps attraction.
    based = massless_substrate_coupling(
        massless_count=3, non_minimal_coupling=0, cutoff=LAMBDA,
        baseline=sp.Symbol("B", positive=True),
    )
    expected_total = sp.Symbol("B", positive=True) + expected_shift
    ledger.check(
        "baseline_enters_additively",
        sp.simplify(based.total_inverse_newton - expected_total) == 0,
        f"total={based.total_inverse_newton}",
    )
    ledger.check(
        "positive_xi_below_conformal_is_attractive",
        based.total_inverse_newton.is_positive is True,
        "B>0, Delta>0 implies 1/G_total>0 (C-GRV-002)",
    )

    # Sign sensitivity: flipping below/above conformal flips the induced sign.
    superconformal = massless_substrate_coupling(
        massless_count=3, non_minimal_coupling=sp.Rational(1, 3),
        cutoff=LAMBDA,
    )
    ledger.check(
        "induced_sign_follows_weight",
        superconformal.induced_shift.is_negative is True
        and xi_zero.induced_shift.is_positive is True,
        "sign(Delta)=sign(1-6*xi)",
    )

    print(
        json.dumps(
            {
                "induced_symbolic": str(xi_zero.induced_shift),
                "newton_purely_induced": str(xi_zero.newton_constant),
                "schemes": ["sharp", "smooth"],
                "numeric_evaluation": "blinded until Lambda selection",
            },
            indent=2,
        )
    )
    ledger.finish()
    return 0


if __name__ == "__main__":
    sys.exit(main())
