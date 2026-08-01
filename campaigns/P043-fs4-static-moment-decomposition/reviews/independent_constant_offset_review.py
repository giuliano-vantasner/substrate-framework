#!/usr/bin/env python3
"""Independent calculus, tensor, and identifiability review for FS4."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P043-INDEPENDENT")
    time = sp.symbols("t", real=True)
    constant, transverse = sp.symbols("c I_perp", real=True)
    longitudinal = sp.Function("mu")(time)

    raw = sp.diag(longitudinal + constant, transverse, transverse)
    trace_free = sp.simplify(raw - sp.eye(3) * sp.trace(raw) / 3)
    modulation_raw = sp.diag(longitudinal, transverse, transverse)
    modulation_trace_free = sp.simplify(
        modulation_raw - sp.eye(3) * sp.trace(modulation_raw) / 3
    )
    ledger.check(
        "direct trace subtraction leaves only a constant STF offset",
        sp.diff(trace_free - modulation_trace_free, time) == sp.zeros(3)
        and trace_free - modulation_trace_free
        == sp.diag(2 * constant / 3, -constant / 3, -constant / 3),
    )
    for order in (1, 2, 3):
        ledger.check(
            f"direct normalized and triple derivatives of order {order} ignore the constant",
            sp.simplify(
                trace_free.diff(time, order)
                - modulation_trace_free.diff(time, order)
            )
            == sp.zeros(3)
            and sp.simplify(
                (3 * trace_free).diff(time, order)
                - (3 * modulation_trace_free).diff(time, order)
            )
            == sp.zeros(3),
        )

    third = sp.diff(longitudinal, time, 3)
    normalized_contraction = sp.simplify(
        sum(
            modulation_trace_free.diff(time, 3)[row, column] ** 2
            for row in range(3)
            for column in range(3)
        )
    )
    triple_contraction = sp.simplify(9 * normalized_contraction)
    coupling = sp.symbols("G", positive=True, real=True)
    ledger.check(
        "direct contractions and convention coefficients give identical conditional power",
        sp.simplify(normalized_contraction - 2 * third**2 / 3) == 0
        and sp.simplify(triple_contraction - 6 * third**2) == 0
        and sp.simplify(
            coupling * normalized_contraction / 5
            - coupling * triple_contraction / 45
        )
        == 0,
    )

    epsilon = sp.symbols("epsilon", nonzero=True, real=True)
    ledger.check(
        "quadratic and cubic time-dependent offsets defeat waveform and power invariance",
        sp.diff(longitudinal + epsilon * time**2, time, 2)
        - sp.diff(longitudinal, time, 2)
        == 2 * epsilon
        and sp.diff(longitudinal + epsilon * time**3, time, 3)
        - third
        == 6 * epsilon,
    )

    mean, first_piece, second_piece = sp.symbols("m a b", real=True)
    ledger.check(
        "constant differentiation supplies no unique two-piece decomposition",
        sp.diff(first_piece + (mean - first_piece), time, 3) == 0
        and sp.diff(second_piece + (mean - second_piece), time, 3) == 0
        and first_piece != second_piece,
    )
    ledger.check(
        "a nonzero static scalar cannot become a radiating amplitude without a new time law",
        sp.diff(first_piece, time, 3) == 0
        and sp.diff(first_piece * sp.cos(time), time, 3) != 0,
    )

    count = ledger.finish()
    print(f"P043 INDEPENDENT CONSTANT-OFFSET REVIEW ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
