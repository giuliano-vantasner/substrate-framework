#!/usr/bin/env python3
"""Primary exact verifier for C-MKV-001 and the P199 MD4 disposition."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.birth_death import (
    immigration_death_generator_action,
    immigration_death_ledger,
    immigration_death_local_drift,
    immigration_death_mean,
    immigration_death_probability_generating_function,
    immigration_death_rates,
    immigration_death_stationary_mass,
    immigration_death_transition_probability,
    reversible_factorial_one_rates,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN_ROOT = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-38/"
    "bridge_MD4_growth_threshold_and_the_rescue.py"
)
SOURCE_SHA256 = "269b275b2eabddc0f2539ecd22b672692de8790316b91c0f264d98e3582bc144"
RELEASE_SHA256 = "c13247bf582c463bf62f966b48250f4cc1a1e747a7c812f3fbe95b82eee20e2b"
FREEZE_SHA256 = "e8f7b8d1990476a835b63f0961cb8ec4d03ca240fb530adf7152f162c5cb3a4a"
MODULE_SHA256 = "25dc73269f3a5f5b9349cf2b61b46832e248138eeb1c514c7749beea352f1c6d"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P199-MD4-PRIMARY")
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("MD4 source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "immutable base release remains pinned",
        digest(ROOT / "governance/releases/v0.147.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned across proposal and campaign paths",
        digest(CAMPAIGN_ROOT / "evidence/formula-freeze.yaml") == FREEZE_SHA256,
    )
    checks.check(
        "canonical implementation remains pinned",
        digest(ROOT / "src/substrate_framework/birth_death.py") == MODULE_SHA256,
    )

    call_sites = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    literal_sites = [
        node
        for node in call_sites
        if node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ]
    unconditional = [
        node
        for node in call_sites
        if len(node.args) >= 2
        and isinstance(node.args[1], ast.Constant)
        and node.args[1].value is True
    ]
    checks.check(
        "source inventory separates 23 sites from 34 executions",
        len(call_sites) == 23
        and len(literal_sites) == 17
        and len(call_sites) - len(literal_sites) == 6
        and sum(isinstance(node, ast.Assert) for node in ast.walk(source_tree)) == 0,
    )
    checks.check(
        "source contains one unconditional headline predicate",
        len(unconditional) == 1
        and "threshold genuinely DISCRIMINATES" in ast.unparse(unconditional[0]),
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "MD4 has no NumPy quadrature compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    S, r = sp.symbols("S r", positive=True)
    for state in range(6):
        birth, death = immigration_death_rates(
            state,
            stationary_mean=S,
            rate=r,
        )
        checks.check(
            f"rates at state {state} are positive and boundary-correct",
            sp.simplify(birth - r * S) == 0
            and sp.simplify(death - r * state) == 0,
        )
    checks.check(
        "constant functions are annihilated at the boundary",
        immigration_death_generator_action(
            0,
            lower_value=73,
            current_value=1,
            upper_value=1,
            stationary_mean=S,
            rate=r,
        )
        == 0,
    )

    n = sp.symbols("n", integer=True, nonnegative=True)
    raw_mass = sp.exp(-S) * S**n / sp.factorial(n)
    checks.check(
        "stationary factorial-one mass normalizes exactly",
        sp.simplify(sp.summation(raw_mass, (n, 0, sp.oo)) - 1) == 0,
    )
    for state in range(6):
        current = immigration_death_stationary_mass(state, stationary_mean=S)
        following = immigration_death_stationary_mass(state + 1, stationary_mean=S)
        birth, _ = immigration_death_rates(state, stationary_mean=S, rate=r)
        _, following_death = immigration_death_rates(
            state + 1,
            stationary_mean=S,
            rate=r,
        )
        checks.check(
            f"detailed balance holds on edge {state} to {state + 1}",
            sp.simplify(current * birth - following * following_death) == 0,
        )

    checks.mutation_sensitive(
        "n plus one detailed-balance index is load bearing",
        lambda offset: sp.simplify(
            immigration_death_stationary_mass(3, stationary_mean=S) * r * S
            - immigration_death_stationary_mass(4, stationary_mean=S)
            * r
            * (3 + offset)
        )
        == 0,
        1,
        [0, 2],
    )
    checks.mutation_sensitive(
        "zero boundary death rate is load bearing",
        lambda boundary_death: sp.simplify(boundary_death) == 0,
        0,
        [r, r * S],
    )

    z, t = sp.symbols("z t", nonnegative=True)
    pgf = immigration_death_probability_generating_function(
        z,
        t,
        initial_generating_function=z**4,
        stationary_mean=S,
        rate=r,
    )
    pgf_pde_residual = sp.diff(pgf, t) - r * (z - 1) * (
        S * pgf - sp.diff(pgf, z)
    )
    checks.check("PGF solves the exact forward PDE", sp.simplify(pgf_pde_residual) == 0)
    checks.check("PGF preserves normalization", sp.simplify(pgf.subs(z, 1) - 1) == 0)
    checks.check("PGF has the declared initial law", sp.simplify(pgf.subs(t, 0) - z**4) == 0)
    checks.check(
        "PGF converges to the stationary law",
        sp.simplify(sp.limit(pgf, t, sp.oo) - sp.exp(S * (z - 1))) == 0,
    )
    mean_from_pgf = sp.diff(pgf, z).subs(z, 1)
    mean = immigration_death_mean(
        t,
        initial_mean=4,
        stationary_mean=S,
        rate=r,
    )
    checks.check("PGF mean equals the closed mean", sp.simplify(mean_from_pgf - mean) == 0)
    checks.check(
        "mean solves the restoring ODE",
        sp.simplify(sp.diff(mean, t) - r * (S - mean)) == 0,
    )

    for final_state in range(5):
        transition = immigration_death_transition_probability(
            final_state,
            initial_state=3,
            time=t,
            stationary_mean=S,
            rate=r,
        )
        coefficient = sp.diff(
            immigration_death_probability_generating_function(
                z,
                t,
                initial_generating_function=z**3,
                stationary_mean=S,
                rate=r,
            ),
            z,
            final_state,
        ).subs(z, 0) / sp.factorial(final_state)
        checks.check(
            f"transition coefficient {final_state} matches the PGF",
            sp.simplify(transition - coefficient) == 0,
        )

    for state in range(5):
        alternative_birth, _ = reversible_factorial_one_rates(
            state,
            stationary_mean=S,
            rate=r,
        )
        _, alternative_following_death = reversible_factorial_one_rates(
            state + 1,
            stationary_mean=S,
            rate=r,
        )
        checks.check(
            f"alternative chain has the same edge ratio at {state}",
            sp.simplify(
                alternative_birth / alternative_following_death
                - S / (state + 1)
            )
            == 0,
        )
    checks.check(
        "same stationary law permits different generators",
        immigration_death_rates(3, stationary_mean=5, rate=2)
        != reversible_factorial_one_rates(3, stationary_mean=5, rate=2),
    )

    slow = immigration_death_mean(t, initial_mean=0, stationary_mean=S, rate=1)
    fast = immigration_death_mean(t, initial_mean=0, stationary_mean=S, rate=2)
    checks.check(
        "rate scale changes transients without changing stationary mass",
        sp.simplify(slow - fast) != 0
        and immigration_death_stationary_mass(3, stationary_mean=S).free_symbols
        == {S},
    )
    ledger = immigration_death_ledger(2, stationary_mean=5, rate=3)
    checks.check(
        "positive local drift retains a positive death rate",
        ledger.local_drift > 0
        and ledger.death_rate > 0
        and not ledger.positive_drift_implies_monotone_sample_paths,
    )
    checks.check(
        "static adjacent ratio is not local time drift",
        ledger.adjacent_stationary_ratio == sp.Rational(5, 3)
        and ledger.local_drift == 9,
    )
    checks.check(
        "ledger preserves the physical interpretation ceiling",
        not ledger.static_mass_selects_unique_dynamics
        and ledger.material_process_is_separate_premise,
    )

    pure_birth_mass = sp.exp(-r * t) * (r * t) ** n / sp.factorial(n)
    pure_birth_mean = sp.summation(n * pure_birth_mass, (n, 0, sp.oo))
    checks.check(
        "competing pure-birth process has transient Poisson mean r t",
        sp.simplify(pure_birth_mean - r * t) == 0,
    )
    checks.check(
        "pure birth cannot satisfy factorial-one detailed balance",
        sp.simplify(
            immigration_death_stationary_mass(2, stationary_mean=S) * r
        )
        != 0,
    )

    generator_doc = " ".join(immigration_death_generator_action.__doc__.split())
    alternative_doc = " ".join(reversible_factorial_one_rates.__doc__.split())
    checks.check(
        "public API states the sample-path ceiling",
        "not monotone sample-path growth" in generator_doc,
    )
    checks.check(
        "public API states dynamical nonuniqueness",
        "nonuniqueness" in alternative_doc,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
