#!/usr/bin/env python3
"""Independent raw master-equation rederivation for C-MKV-001."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P199-MD4-INDEPENDENT")
    S, r = sp.symbols("S r", positive=True)
    n = sp.symbols("n", integer=True, nonnegative=True)

    def stationary(state: int) -> sp.Expr:
        return sp.exp(-S) * S**state / sp.factorial(state)

    checks.check(
        "raw stationary series normalizes",
        sp.simplify(
            sp.summation(
                sp.exp(-S) * S**n / sp.factorial(n),
                (n, 0, sp.oo),
            )
            - 1
        )
        == 0,
    )
    for state in range(8):
        left_current = stationary(state) * r * S
        right_current = stationary(state + 1) * r * (state + 1)
        checks.check(
            f"raw edge current cancels at {state}",
            sp.simplify(left_current - right_current) == 0,
        )

    z, t = sp.symbols("z t", nonnegative=True)
    q = sp.exp(-r * t)
    initial_state = 4
    raw_pgf = (1 + (z - 1) * q) ** initial_state * sp.exp(
        S * (z - 1) * (1 - q)
    )
    forward_residual = sp.diff(raw_pgf, t) - r * (z - 1) * (
        S * raw_pgf - sp.diff(raw_pgf, z)
    )
    checks.check("raw PGF solves the forward PDE", sp.simplify(forward_residual) == 0)
    checks.check("raw PGF is normalized", sp.simplify(raw_pgf.subs(z, 1) - 1) == 0)
    checks.check(
        "raw PGF has deterministic initial state",
        sp.simplify(raw_pgf.subs(t, 0) - z**initial_state) == 0,
    )
    checks.check(
        "raw PGF converges to Poisson stationary law",
        sp.simplify(sp.limit(raw_pgf, t, sp.oo) - sp.exp(S * (z - 1))) == 0,
    )

    raw_mean = sp.diff(raw_pgf, z).subs(z, 1)
    raw_variance = (
        sp.diff(raw_pgf, z, 2).subs(z, 1) + raw_mean - raw_mean**2
    )
    checks.check(
        "raw mean has binomial survivor plus immigrant form",
        sp.simplify(raw_mean - (initial_state * q + S * (1 - q))) == 0,
    )
    checks.check(
        "raw variance has binomial survivor plus immigrant form",
        sp.simplify(
            raw_variance
            - (initial_state * q * (1 - q) + S * (1 - q))
        )
        == 0,
    )
    checks.check(
        "raw mean solves the restoring equation",
        sp.simplify(sp.diff(raw_mean, t) - r * (S - raw_mean)) == 0,
    )

    for final_state in range(6):
        coefficient = sp.diff(raw_pgf, z, final_state).subs(z, 0) / sp.factorial(
            final_state
        )
        survivor_convolution = sp.Integer(0)
        for survivors in range(min(initial_state, final_state) + 1):
            immigrant_order = final_state - survivors
            survivor_convolution += (
                sp.binomial(initial_state, survivors)
                * q**survivors
                * (1 - q) ** (initial_state - survivors)
                * sp.exp(-S * (1 - q))
                * (S * (1 - q)) ** immigrant_order
                / sp.factorial(immigrant_order)
            )
        checks.check(
            f"raw transition convolution coefficient {final_state}",
            sp.simplify(coefficient - survivor_convolution) == 0,
        )

    for state in range(6):
        primary_ratio = (r * S) / (r * (state + 1))
        alternative_ratio = (r * S / (state + 1)) / r
        checks.check(
            f"two raw generators share edge ratio at {state}",
            sp.simplify(primary_ratio - alternative_ratio) == 0,
        )
    primary_drift = r * S - 2 * r
    alternative_drift = r * S / 3 - r
    checks.check(
        "same stationary ratio does not fix local drift",
        sp.simplify(primary_drift - alternative_drift) != 0,
    )
    checks.check(
        "same stationary ratio does not fix holding rate",
        sp.simplify((r * S + 2 * r) - (r * S / 3 + r)) != 0,
    )

    wrong_index_current = stationary(3) * r * S - stationary(4) * r * 3
    checks.check(
        "wrong detailed-balance index leaves nonzero current",
        sp.simplify(wrong_index_current) != 0,
    )
    mutated_boundary_outflow = stationary(0) * r
    checks.check(
        "nonzero boundary death creates uncompensated probability outflow",
        mutated_boundary_outflow.is_positive is True
        and sp.simplify(mutated_boundary_outflow) != 0,
    )
    checks.check(
        "positive restoring drift coexists with a death jump",
        sp.simplify((r * (S - 2)).subs(S, 5)) > 0 and 2 * r > 0,
    )

    static_ratio = S / 3
    local_drift = r * (S - 2)
    checks.check(
        "static ratio cannot equal a rate-scale-independent drift",
        r in local_drift.free_symbols and r not in static_ratio.free_symbols,
    )

    slow_mean = S * (1 - sp.exp(-t))
    fast_mean = S * (1 - sp.exp(-2 * t))
    checks.check(
        "stationary mean does not select a time scale",
        sp.simplify(slow_mean - fast_mean) != 0
        and sp.limit(slow_mean, t, sp.oo) == S
        and sp.limit(fast_mean, t, sp.oo) == S,
    )

    pure_birth_pgf = sp.exp(r * t * (z - 1))
    checks.check(
        "competing pure-birth PGF is normalized",
        pure_birth_pgf.subs(z, 1) == 1,
    )
    checks.check(
        "competing pure-birth mean grows without finite stationary target",
        sp.diff(pure_birth_pgf, z).subs(z, 1) == r * t,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
