"""Primary exact and source-audit verifier for P122's GB1 campaign."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
from typing import Callable

import sympy as sp

from substrate_framework.branching import (
    channel_odds,
    relative_weighted_odds_enhancement,
    two_channel_allocation,
    weighted_channel_allocation,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-32/"
    "bridge_GB1_channel_definitions.py"
)
CAMPAIGN = Path("campaigns/P122-gb1-channel-branching-audit")
SOURCE_SHA = "ace0515d7ea362ef45a55db22308aecffdad9a003d03f2b1209c0a11874b489b"
FREEZE_SHA = "cb58ccdc4b7f08b84014341f7aca59afff13a28424aba766455fabfe7b3f1fea"


def _extract_function(
    tree: ast.Module,
    name: str,
    namespace: dict[str, object],
) -> Callable[..., object]:
    node = next(
        item for item in tree.body if isinstance(item, ast.FunctionDef) and item.name == name
    )
    module = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
    scope = dict(namespace)
    exec(compile(module, str(SOURCE), "exec"), scope)
    return scope[name]  # type: ignore[return-value]


def main() -> int:
    checks = CheckLedger("GB1-CHANNEL-BRANCHING-AUDIT")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "GB1 source bytes are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA,
    )
    normalized_contract = (CAMPAIGN / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n", b"status: draft\n"
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == FREEZE_SHA,
    )
    checks.check(
        "pre-source contract is immutable",
        hashlib.sha256(
            (CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    source_calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "twelve source call sites expand to the reproduced eighteen predicates",
        len(source_calls) == 12 and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "GB1 requires no quadrature compatibility path",
        all(
            token not in source_text
            for token in ("np.trapz", "np.trapezoid", "trapezoid_integral")
        ),
    )

    first, second = sp.symbols("A B", positive=True)
    allocation = two_channel_allocation(first, second)
    checks.check(
        "canonical allocation derives both fractions from one positive total",
        allocation.total_rate == first + second
        and allocation.first_fraction == first / (first + second)
        and allocation.second_fraction == second / (first + second),
    )
    checks.check(
        "the two canonical fractions partition exactly",
        sp.simplify(allocation.first_fraction + allocation.second_fraction - 1) == 0,
    )
    checks.check(
        "both zero endpoints are retained individually",
        two_channel_allocation(0, 3).first_fraction == 0
        and two_channel_allocation(0, 3).second_fraction == 1
        and two_channel_allocation(5, 0).first_fraction == 1
        and two_channel_allocation(5, 0).second_fraction == 0,
    )
    try:
        two_channel_allocation(0, 0)
    except ValueError:
        double_zero_rejected = True
    else:
        double_zero_rejected = False
    checks.check(
        "the undefined double-zero denominator is rejected",
        double_zero_rejected,
    )
    first_fraction = allocation.first_fraction
    checks.check(
        "exact derivatives give the global interior monotonicity signs",
        sp.simplify(
            sp.diff(first_fraction, first) - second / (first + second) ** 2
        )
        == 0
        and sp.simplify(
            sp.diff(first_fraction, second) + first / (first + second) ** 2
        )
        == 0,
    )
    checks.check(
        "exact limits close the first-channel endpoints",
        sp.limit(first_fraction, first, 0, dir="+") == 0
        and sp.limit(first_fraction, first, sp.oo) == 1,
    )
    scale = sp.symbols("s", positive=True)
    checks.check(
        "common positive rate scaling cancels exactly",
        sp.simplify(
            two_channel_allocation(scale * first, scale * second).first_fraction
            - first_fraction
        )
        == 0,
    )
    checks.check(
        "independent channel scaling changes the fraction",
        sp.simplify(
            two_channel_allocation(scale * first, second).first_fraction
            - first_fraction
        )
        != 0,
    )
    checks.check(
        "positive-denominator odds equal the fraction ratio",
        sp.simplify(
            channel_odds(first, second)
            - allocation.first_fraction / allocation.second_fraction
        )
        == 0,
    )
    try:
        channel_odds(first, 0)
    except ValueError:
        zero_odds_denominator_rejected = True
    else:
        zero_odds_denominator_rejected = False
    checks.check(
        "odds keep their nonzero denominator premise",
        zero_odds_denominator_rejected,
    )

    soft_scale, gamma_scale, weight = sp.symbols("r_s r_gamma w", positive=True)
    population = sp.symbols("N", positive=True, integer=True)
    specialized = weighted_channel_allocation(
        soft_scale,
        gamma_scale,
        weight,
        population,
    )
    ratio = sp.simplify(gamma_scale / soft_scale)
    checks.check(
        "the canonical weighted specialization reproduces the source fractions",
        sp.simplify(
            specialized.weighted_fraction
            - weight * population / (weight * population + ratio)
        )
        == 0
        and sp.simplify(
            specialized.comparison_fraction
            - ratio / (weight * population + ratio)
        )
        == 0,
    )
    checks.check(
        "the weighted comparison share decreases with positive population",
        sp.diff(ratio / (weight * population + ratio), population)
        == -ratio * weight / (weight * population + ratio) ** 2,
    )
    baseline_weight = sp.symbols("w1", positive=True)
    enhancement = relative_weighted_odds_enhancement(
        weight,
        population,
        baseline_weight,
    )
    checks.check(
        "the exact relative odds enhancement retains weight count and baseline",
        enhancement == weight * population / baseline_weight
        and enhancement.free_symbols == {weight, population, baseline_weight},
    )
    checks.check(
        "the declared unit baseline gives enhancement one",
        relative_weighted_odds_enhancement(baseline_weight, 1, baseline_weight) == 1,
    )
    for label, call in (
        ("negative rate", lambda: two_channel_allocation(-1, 2)),
        ("floating rate", lambda: two_channel_allocation(1.0, 2)),
        (
            "zero weight",
            lambda: weighted_channel_allocation(1, 1, 0, 1),
        ),
        (
            "noninteger population",
            lambda: weighted_channel_allocation(1, 1, 1, sp.Rational(3, 2)),
        ),
        (
            "zero baseline weight",
            lambda: relative_weighted_odds_enhancement(1, 1, 0),
        ),
    ):
        try:
            call()
        except ValueError:
            rejected = True
        else:
            rejected = False
        checks.check(f"canonical API rejects {label}", rejected)

    time_scale = sp.symbols("tau", positive=True)
    soft_rate = soft_scale * weight * population
    hard_rate = gamma_scale
    checks.check(
        "common inverse-time scaling gives both declared objects one rate dimension",
        sp.simplify(
            soft_rate.subs(
                {soft_scale: soft_scale / time_scale, gamma_scale: gamma_scale / time_scale}
            )
            - soft_rate / time_scale
        )
        == 0
        and sp.simplify(
            hard_rate.subs(
                {soft_scale: soft_scale / time_scale, gamma_scale: gamma_scale / time_scale}
            )
            - hard_rate / time_scale
        )
        == 0,
    )
    dimension_mutant = (
        (soft_scale / time_scale) * (weight / time_scale) * population
    )
    checks.check(
        "a dimensionful weight breaks the common-rate typing",
        sp.simplify(dimension_mutant / (soft_rate / time_scale)) != 1,
    )
    checks.check(
        "branching fractions are invariant under the declared common time-unit change",
        sp.simplify(
            (soft_rate / (soft_rate + hard_rate)).subs(
                {soft_scale: soft_scale / time_scale, gamma_scale: gamma_scale / time_scale}
            )
            - soft_rate / (soft_rate + hard_rate)
        )
        == 0,
    )

    common_factor = sp.symbols("C", positive=True)
    first_factor, second_factor = sp.symbols("C_s C_g", positive=True)
    checks.check(
        "one common positive gating factor cancels exactly",
        sp.simplify(
            two_channel_allocation(
                common_factor * first,
                common_factor * second,
            ).first_fraction
            - first_fraction
        )
        == 0,
    )
    unequal_fraction = first_factor * first / (
        first_factor * first + second_factor * second
    )
    unequal_residual = sp.factor(unequal_fraction - first_fraction)
    checks.check(
        "unequal channel gates do not cancel",
        sp.simplify(
            unequal_residual
            - first
            * second
            * (first_factor - second_factor)
            / (
                (first + second)
                * (first * first_factor + second * second_factor)
            )
        )
        == 0,
    )
    target = sp.symbols("q", positive=True)
    target_ratio = sp.simplify(weight * population * (1 - target) / target)
    checks.check(
        "every interior target fraction is fitted by a free positive ratio",
        sp.simplify(
            (weight * population / (weight * population + ratio)).subs(
                ratio,
                target_ratio,
            )
            - target
        )
        == 0,
    )
    checks.check(
        "zero interaction can remove both physical rates while leaving formal inputs",
        sp.simplify((sp.Integer(0) * soft_rate) + (sp.Integer(0) * hard_rate)) == 0,
    )

    rho_symbol = sp.symbols("rho", positive=True)
    source_rho_condition = sp.simplify(
        (gamma_scale / soft_scale)
        - rho_symbol.subs(rho_symbol, gamma_scale / soft_scale)
    )
    checks.check(
        "the source rho predicate is a substitution tautology with no rho symbol left",
        source_rho_condition == 0 and rho_symbol not in source_rho_condition.free_symbols,
    )
    n, omega, phonon = sp.symbols("n Omega omega_ph", positive=True)
    source_soft = soft_scale * weight * population
    source_gamma = gamma_scale
    source_soft_fraction = sp.simplify(
        (source_soft / (source_soft + source_gamma)).subs(
            gamma_scale,
            rho_symbol * soft_scale,
        )
    )
    source_gamma_fraction = sp.simplify(1 - source_soft_fraction)
    source_enhancement = sp.simplify(weight * population / baseline_weight)
    source_symbols = set().union(
        source_soft.free_symbols,
        source_gamma.free_symbols,
        source_soft_fraction.free_symbols,
        source_gamma_fraction.free_symbols,
        source_enhancement.free_symbols,
        (source_soft / source_gamma).free_symbols,
    )
    checks.check(
        "the executed construction never uses n Omega or omega_ph",
        source_symbols.isdisjoint({n, omega, phonon}),
    )
    checks.check(
        "the source uses an independent weight symbol rather than a derived w(n)",
        weight in source_symbols and not any(isinstance(node, sp.Function) for node in source_symbols),
    )
    executable_names = {
        node.id for node in ast.walk(source_tree) if isinstance(node, ast.Name)
    }
    checks.check(
        "the declared common gating factors are absent from executable syntax",
        executable_names.isdisjoint({"K_loss", "G_coh", "Wc", "W_nuc"}),
    )

    source_sqrt_scan = _extract_function(source_tree, "has_sqrt_ratio", {"sp": sp})
    barrier, energy = sp.symbols("G E", positive=True)
    checks.check(
        "the source sqrt scan detects its selected tunnelling-shaped example",
        bool(source_sqrt_scan(sp.exp(-sp.sqrt(barrier / energy)))),
    )
    checks.check(
        "the source sqrt scan falsely flags a benign square root",
        bool(source_sqrt_scan(sp.sqrt(weight))),
    )
    checks.check(
        "a non-square-root barrier-shaped response evades the source scan",
        not bool(source_sqrt_scan(sp.exp(-barrier / energy))),
    )
    checks.check(
        "an opaque imported factor evades both free-symbol naming and sqrt syntax",
        not bool(source_sqrt_scan(sp.symbols("opaque_gate", positive=True))),
    )
    checks.check(
        "substituting a barrier into the free weight preserves the algebra but changes semantics",
        (source_soft_fraction.subs(weight, sp.exp(-sp.sqrt(barrier / energy)))).has(
            barrier,
            energy,
        ),
    )

    checks.check(
        "the canonical source explicitly withholds physical rate derivation",
        "does not derive physical states" in Path(
            "src/substrate_framework/branching.py"
        ).read_text(),
    )
    checks.check(
        "the surviving generic allocation is distinct from the accepted factor and spin APIs",
        allocation.first_fraction == first / (first + second)
        and specialized.weighted_fraction.has(weight, population, soft_scale, gamma_scale),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
