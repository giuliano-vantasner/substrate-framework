"""Attempt 0001 driver: exact vacuum fluctuation census (P243).

Runs the canonical census at the certified default targets, the independent
projector-variation probe, and preregistered mutations.  Captured stdout is
the attempt record; run with PYTHONPATH=src.
"""

from __future__ import annotations

import json
import sys

import sympy as sp

from substrate_framework.m5_fluctuation_spectrum import (
    certify_projector_variation,
    classify_census,
)
from substrate_framework.verification import CheckLedger


TARGETS = (sp.Integer(4), sp.Integer(1), sp.Rational(3, 10), sp.Integer(0))


def main() -> int:
    ledger = CheckLedger("P243-attempt-0001")

    census = classify_census(targets=TARGETS)

    ledger.check(
        "basis_dimension_is_sym4",
        census.basis_dimension == 10,
        f"dim={census.basis_dimension}",
    )
    ledger.check(
        "massless_species_count_is_three",
        census.massless_count == 3,
        f"count={census.massless_count}",
    )
    ledger.check(
        "stiff_static_directions_are_four",
        len(census.massive_stiff_gaps) == 4,
        f"gaps={census.massive_stiff_gaps}",
    )
    ledger.check(
        "inert_directions_are_three",
        census.inert_count == 3,
        f"count={census.inert_count}",
    )

    expected_kinetic = [sp.Rational(1, 9), sp.Rational(100, 1369),
                        sp.Rational(1, 16)]
    got = sorted(sp.nsimplify(value) for value in census.kinetic_coefficients)
    ledger.check(
        "kinetic_coefficients_exact",
        got == sorted(expected_kinetic),
        f"got={got}",
    )

    expected_gaps = {
        sp.Integer(67905),
        sp.Integer(30),
        sp.Rational(361141, 250000),
        sp.Integer(1),
    }
    ledger.check(
        "stiff_gaps_exact",
        set(census.massive_stiff_gaps) == expected_gaps,
        f"got={census.massive_stiff_gaps}",
    )

    # Independent route: the analytic first variation must satisfy the
    # affine projector defining system exactly, and its kernel must be
    # trivial (distinct eigenvalues make the branch solution unique).
    nullities = certify_projector_variation(targets=TARGETS)
    ledger.check(
        "projector_variation_certified_unique",
        len(nullities) == 10 and all(dim == 0 for dim in nullities),
        f"certification per direction={nullities}",
    )

    # Mutation 1: degenerate timelike target must be rejected outright.
    try:
        classify_census(targets=(sp.Integer(1), sp.Integer(1),
                                 sp.Rational(3, 10), sp.Integer(0)))
        degenerate_rejected = False
    except Exception:
        degenerate_rejected = True
    ledger.check(
        "degenerate_target_rejected",
        degenerate_rejected,
        "non-simple timelike branch raises",
    )

    # Mutation 2: a wrong kinetic metric must break the exact coefficients.
    tampered = classify_census(targets=TARGETS, projector_stiffness=7)
    ledger.check(
        "kinetic_rescaling_moves_coefficients",
        all(
            sp.nsimplify(value) != sp.nsimplify(expected)
            for value, expected in zip(
                sorted(tampered.kinetic_coefficients),
                sorted(census.kinetic_coefficients),
            )
        ),
        f"kappa=7 gives {tampered.kinetic_coefficients}",
    )

    # Mutation 3: dropping a potential weight must move the stiff gaps.
    light = classify_census(
        targets=TARGETS,
        weights=(sp.Integer(1), sp.Integer(1), sp.Integer(1),
                 sp.Integer(0)),
    )
    ledger.check(
        "weight_mutation_moves_stiff_gaps",
        set(light.massive_stiff_gaps) != set(census.massive_stiff_gaps),
        f"weights=(1,1,1,0): {light.massive_stiff_gaps}",
    )

    record = {
        "targets": [str(value) for value in census.targets],
        "massless_count": census.massless_count,
        "inert_count": census.inert_count,
        "massive_stiff_gaps": [str(sp.nsimplify(g))
                               for g in census.massive_stiff_gaps],
        "kinetic_coefficients": [str(sp.nsimplify(k))
                                 for k in census.kinetic_coefficients],
        "stiffness_rank": census.stiffness_rank,
        "kinetic_rank": census.kinetic_rank,
    }
    print(json.dumps(record, indent=2, sort_keys=True))
    ledger.finish()
    return 0


if __name__ == "__main__":
    sys.exit(main())
