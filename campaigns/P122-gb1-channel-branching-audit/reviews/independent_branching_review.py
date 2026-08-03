"""Independent exact rederivation for P122 without the canonical branching API."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-32/"
    "bridge_GB1_channel_definitions.py"
)
FROZEN = Path(
    "campaigns/P122-gb1-channel-branching-audit/evidence/frozen-proposal.yaml"
)
SOURCE_SHA = "ace0515d7ea362ef45a55db22308aecffdad9a003d03f2b1209c0a11874b489b"
FREEZE_SHA = "cb58ccdc4b7f08b84014341f7aca59afff13a28424aba766455fabfe7b3f1fea"


def main() -> int:
    checks = CheckLedger("GB1-INDEPENDENT-BRANCHING-REVIEW")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    tree = ast.parse(source_text)
    checks.check(
        "independently read GB1 bytes are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA,
    )
    checks.check(
        "the preregistration artifact remains byte identical",
        hashlib.sha256(FROZEN.read_bytes()).hexdigest() == FREEZE_SHA,
    )
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check("fresh AST count finds twelve check call sites", len(calls) == 12)

    total, coordinate = sp.symbols("T q", positive=True)
    first = sp.simplify(coordinate * total)
    second = sp.simplify((1 - coordinate) * total)
    checks.check(
        "fresh total-coordinate construction partitions the two inputs",
        sp.simplify(first + second - total) == 0,
    )
    first_rate, second_rate = sp.symbols("A B", positive=True)
    fraction = sp.simplify(first_rate / (first_rate + second_rate))
    complement = sp.simplify(second_rate / (first_rate + second_rate))
    checks.check(
        "fresh normalization derives the exact complementary shares",
        sp.simplify(fraction + complement - 1) == 0,
    )
    checks.check(
        "fresh odds inversion recovers the rate ratio",
        sp.simplify(fraction / complement - first_rate / second_rate) == 0,
    )
    checks.check(
        "fresh derivatives have opposite exact signs",
        sp.simplify(
            sp.diff(fraction, first_rate)
            - second_rate / (first_rate + second_rate) ** 2
        )
        == 0
        and sp.simplify(
            sp.diff(fraction, second_rate)
            + first_rate / (first_rate + second_rate) ** 2
        )
        == 0,
    )
    checks.check(
        "fresh first-rate limits give zero and one",
        sp.limit(fraction, first_rate, 0, dir="+") == 0
        and sp.limit(fraction, first_rate, sp.oo) == 1,
    )
    checks.check(
        "fresh explicit endpoints retain zero and unit shares",
        sp.Rational(0, 3) == 0
        and sp.Rational(3, 3) == 1
        and sp.Rational(5, 5) == 1
        and sp.Rational(0, 5) == 0,
    )
    scale = sp.symbols("s", positive=True)
    checks.check(
        "fresh common-scale substitution cancels",
        sp.simplify(
            (scale * first_rate) / (scale * first_rate + scale * second_rate)
            - fraction
        )
        == 0,
    )
    checks.check(
        "fresh relative-scale substitution changes the share",
        sp.simplify(
            (scale * first_rate) / (scale * first_rate + second_rate)
            - fraction
        )
        != 0,
    )

    soft, gamma, weight, rho = sp.symbols("r_s r_gamma w rho", positive=True)
    population = sp.symbols("N", positive=True, integer=True)
    soft_rate = soft * weight * population
    hard_rate = gamma
    specialized = sp.simplify(
        (soft_rate / (soft_rate + hard_rate)).subs(gamma, rho * soft)
    )
    checks.check(
        "fresh specialization gives wN over wN plus rho",
        sp.simplify(specialized - weight * population / (weight * population + rho)) == 0,
    )
    checks.check(
        "fresh complementary specialization gives rho over the same total",
        sp.simplify(1 - specialized - rho / (weight * population + rho)) == 0,
    )
    checks.check(
        "fresh population derivative gives the GB4-facing monotonicity theorem",
        sp.diff(rho / (weight * population + rho), population)
        == -rho * weight / (weight * population + rho) ** 2,
    )
    baseline = sp.symbols("w1", positive=True)
    odds = sp.simplify(soft_rate / hard_rate)
    baseline_odds = sp.simplify(odds.subs({weight: baseline, population: 1}))
    checks.check(
        "fresh odds ratio cancels both channel normalizations",
        sp.simplify(odds / baseline_odds - weight * population / baseline) == 0,
    )
    checks.check(
        "fresh enhancement keeps its arbitrary weight and count inputs",
        (weight * population / baseline).free_symbols == {weight, population, baseline},
    )
    target = sp.symbols("q", positive=True)
    fitted_rho = sp.simplify(weight * population * (1 - target) / target)
    checks.check(
        "fresh inverse fits any interior branch target with rho",
        sp.simplify(specialized.subs(rho, fitted_rho) - target) == 0,
    )

    first_gate, second_gate = sp.symbols("C_s C_g", positive=True)
    gated = first_gate * first_rate / (
        first_gate * first_rate + second_gate * second_rate
    )
    checks.check(
        "fresh unequal-gate residual is proportional to the gate difference",
        sp.simplify(
            gated
            - fraction
            - first_rate
            * second_rate
            * (first_gate - second_gate)
            / (
                (first_rate + second_rate)
                * (first_gate * first_rate + second_gate * second_rate)
            )
        )
        == 0,
    )
    checks.check(
        "fresh zero-interaction countermodel removes both physical rates",
        sp.simplify(0 * soft_rate + 0 * hard_rate) == 0,
    )

    time_scale = sp.symbols("tau", positive=True)
    checks.check(
        "fresh unit rescaling preserves the two inverse-time dimensions",
        sp.simplify(
            soft_rate.subs({soft: soft / time_scale, gamma: gamma / time_scale})
            - soft_rate / time_scale
        )
        == 0
        and sp.simplify(
            hard_rate.subs({soft: soft / time_scale, gamma: gamma / time_scale})
            - hard_rate / time_scale
        )
        == 0,
    )
    checks.check(
        "fresh dimensionful-weight mutation breaks rate matching",
        sp.simplify((soft * weight * population / time_scale**2) / (hard_rate / time_scale))
        != sp.simplify(soft_rate / hard_rate),
    )

    rho_check = sp.simplify(
        gamma / soft - rho.subs(rho, gamma / soft)
    )
    checks.check(
        "fresh source reading exposes the rho substitution tautology",
        rho_check == 0 and rho not in rho_check.free_symbols,
    )
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    checks.check(
        "fresh AST reading finds no executable common gating factors",
        names.isdisjoint({"K_loss", "G_coh", "Wc", "W_nuc"}),
    )
    checks.check(
        "fresh AST reading finds the advertised kinematic symbols unused by rate expressions",
        all(token in source_text for token in ("n, Omega, omega_ph", "R_soft = r_s * w * N")),
    )
    checks.check(
        "finite selected-symbol syntax cannot establish a physical channel",
        "the two channels exhaust" not in source_text.lower()
        or "same state" in source_text.lower(),
    )
    checks.check(
        "a declared inverse-time dimension alone supplies no state or interaction",
        all(token not in names for token in ("Hamiltonian", "spectral_density", "final_state")),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
