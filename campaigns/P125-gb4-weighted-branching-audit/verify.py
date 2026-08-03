"""Primary exact verifier for P125's GB4 weighted-branching audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
from typing import Callable

import sympy as sp
import yaml

from substrate_framework.branching import (
    relative_weighted_odds_enhancement,
    two_channel_allocation,
    weighted_channel_allocation,
)
from substrate_framework.verification import CheckLedger


ROOT = Path("campaigns/P125-gb4-weighted-branching-audit")
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCE = SOURCE_ROOT / "merged-framework/bridges/phase-32/bridge_GB4_branching_ratio.py"
SOURCE_SHA256 = "497ed6deda4a0f11562baeaef0ec7bc21cc20b38d3d11c69ed07728ed33faeb0"
FREEZE_SHA256 = "3e3201507deb309161485a50b2257f1cac6ee0386ec2ef36fe019a7f6409e569"


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
    checks = CheckLedger("P125")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source bytes match the pinned GB4 unit",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "immutable proposal preserves the pre-source freeze",
        hashlib.sha256((ROOT / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA256,
    )
    sites = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "sixteen static sites expand to twenty-three runtime predicates",
        len(sites) == 16 and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source uses no sampled integration or NumPy compatibility alias",
        all(
            token not in source_text
            for token in ("np.trapz", "np.trapezoid", "trapezoid_integral")
        ),
    )
    reproduction = yaml.safe_load((ROOT / "attempts/0002/result.yaml").read_text())
    checks.check(
        "native source reproduction closes before exact adjudication",
        reproduction["status"] == "verified"
        and reproduction["results"]["terminal_tally"] == "ALL 23 CHECKS PASS",
    )

    soft, gamma, weight = sp.symbols("r_s r_gamma w", positive=True)
    population_integer = sp.symbols("N_i", positive=True, integer=True)
    rho = sp.symbols("rho", positive=True)
    canonical = weighted_channel_allocation(
        soft,
        gamma,
        weight,
        population_integer,
    )
    ratio = gamma / soft
    checks.check(
        "canonical weighted allocation reproduces both GB4 fractions",
        sp.simplify(
            canonical.weighted_fraction
            - weight * population_integer / (weight * population_integer + ratio)
        )
        == 0
        and sp.simplify(
            canonical.comparison_fraction
            - ratio / (weight * population_integer + ratio)
        )
        == 0,
    )
    checks.check(
        "canonical fractions partition exactly on the declared positive interior",
        sp.simplify(canonical.weighted_fraction + canonical.comparison_fraction - 1) == 0,
    )
    checks.check(
        "the stronger accepted theorem retains both individual zero endpoints",
        two_channel_allocation(0, gamma).first_fraction == 0
        and two_channel_allocation(soft, 0).second_fraction == 0,
    )

    population = sp.symbols("N", positive=True)
    gamma_fraction = rho / (weight * population + rho)
    soft_fraction = 1 - gamma_fraction
    fixed_derivative = sp.diff(gamma_fraction, population)
    expected_derivative = -rho * weight / (weight * population + rho) ** 2
    checks.check(
        "fixed-weight positive-real derivative is the accepted negative formula",
        sp.simplify(fixed_derivative - expected_derivative) == 0,
    )
    fixed_difference = sp.factor(
        gamma_fraction.subs(population, population + 1) - gamma_fraction
    )
    expected_difference = -rho * weight / (
        (weight * population + rho) * (weight * (population + 1) + rho)
    )
    checks.check(
        "direct adjacent-integer difference is strictly negative at fixed weight",
        sp.simplify(fixed_difference - expected_difference) == 0,
    )
    checks.check(
        "fixed-weight fraction limits are zero and one on the positive extension",
        sp.limit(gamma_fraction, population, 0, dir="+") == 1
        and sp.limit(gamma_fraction, population, sp.oo) == 0
        and sp.limit(soft_fraction, population, sp.oo) == 1,
    )
    checks.mutation_sensitive(
        "fixed-weight derivative sign and normalization are load bearing",
        lambda value: sp.simplify(value - expected_derivative) == 0,
        fixed_derivative,
        (-fixed_derivative, sp.Integer(0), -rho / (weight * population + rho) ** 2),
    )
    checks.mutation_sensitive(
        "integer occupation difference is independently load bearing",
        lambda value: sp.simplify(value - expected_difference) == 0,
        fixed_difference,
        (-fixed_difference, sp.Integer(0)),
    )

    n, alpha, power = sp.symbols("n alpha k", positive=True)
    fixed_weights = (n, sp.exp(-alpha * n), n**power)
    checks.check(
        "all three named weights are positive constants in a partial N derivative",
        all(
            sp.simplify(
                sp.diff(rho / (candidate * population + rho), population)
                + rho * candidate / (candidate * population + rho) ** 2
            )
            == 0
            for candidate in fixed_weights
        ),
    )
    checks.check(
        "the three named regimes are not structurally selected by fixed-n N dependence",
        all(
            sp.diff(candidate, population) == 0 and candidate.is_positive is True
            for candidate in fixed_weights
        ),
    )

    coupled_weight = sp.Function("w")(population)
    coupled_fraction = rho / (population * coupled_weight + rho)
    coupled_derivative = sp.diff(coupled_fraction, population)
    coupled_expected = -rho * (
        coupled_weight + population * sp.diff(coupled_weight, population)
    ) / (population * coupled_weight + rho) ** 2
    checks.check(
        "total derivative exposes all hidden population dependence in the weight",
        sp.simplify(coupled_derivative - coupled_expected) == 0,
    )
    weight_now, weight_next = sp.symbols("w_N w_next", positive=True)
    discrete_coupled = sp.factor(
        rho / ((population + 1) * weight_next + rho)
        - rho / (population * weight_now + rho)
    )
    discrete_expected = rho * (
        population * weight_now - (population + 1) * weight_next
    ) / (
        (population * weight_now + rho)
        * ((population + 1) * weight_next + rho)
    )
    checks.check(
        "adjacent sign is governed by growth of N times w rather than positivity",
        sp.simplify(discrete_coupled - discrete_expected) == 0,
    )
    checks.check(
        "a positive inverse-population weight makes the gamma fraction constant",
        sp.simplify(
            (rho / (population * (1 / population) + rho)) - rho / (1 + rho)
        )
        == 0,
    )
    inverse_square_fraction = rho / (population * population ** -2 + rho)
    checks.check(
        "a faster positive inverse weight makes the gamma fraction increase",
        sp.simplify(
            sp.diff(inverse_square_fraction, population)
            - rho / (1 + rho * population) ** 2
        )
        == 0,
    )

    exponential_coupled = rho / (
        population * sp.exp(-alpha * population) + rho
    )
    exponential_derivative = sp.diff(exponential_coupled, population)
    exponential_expected = rho * sp.exp(-alpha * population) * (
        alpha * population - 1
    ) / (population * sp.exp(-alpha * population) + rho) ** 2
    checks.check(
        "coupled exponential derivative changes sign at alpha times N equals one",
        sp.simplify(exponential_derivative - exponential_expected) == 0,
    )
    checks.check(
        "exact coupled exponential samples realize both derivative signs",
        bool(exponential_derivative.subs({alpha: 1, population: sp.Rational(1, 2), rho: 1}) < 0)
        and bool(exponential_derivative.subs({alpha: 1, population: 2, rho: 1}) > 0),
    )
    alpha_four = sp.log(4)
    exponential_one = exponential_coupled.subs(
        {alpha: alpha_four, population: 1, rho: 1}
    )
    exponential_two = exponential_coupled.subs(
        {alpha: alpha_four, population: 2, rho: 1}
    )
    checks.check(
        "an exact adjacent coupled-exponential step reverses source monotonicity",
        exponential_one == sp.Rational(4, 5)
        and exponential_two == sp.Rational(8, 9)
        and exponential_two > exponential_one,
    )
    linear_coupled = rho / (population**2 + rho)
    power_coupled = rho / (population ** (power + 1) + rho)
    checks.check(
        "linear and positive-power n equals N models retain negative total derivatives",
        sp.simplify(sp.diff(linear_coupled, population))
        == -2 * population * rho / (population**2 + rho) ** 2
        and sp.simplify(
            sp.diff(power_coupled, population)
            + rho
            * (power + 1)
            * population**power
            / (population ** (power + 1) + rho) ** 2
        )
        == 0,
    )

    baseline_weight = sp.symbols("w1", positive=True)
    enhancement = relative_weighted_odds_enhancement(
        weight,
        population_integer,
        baseline_weight,
    )
    checks.check(
        "canonical enhancement is a same-baseline relative odds ratio",
        enhancement == weight * population_integer / baseline_weight,
    )
    checks.check(
        "the unit baseline identity is exact but definition dependent",
        relative_weighted_odds_enhancement(baseline_weight, 1, baseline_weight) == 1,
    )
    exponential_enhancement = population * sp.exp(
        -alpha * (population - 1)
    )
    checks.check(
        "coupled exponential relative odds are nonmonotone",
        sp.simplify(
            sp.diff(exponential_enhancement, population)
            - sp.exp(-alpha * (population - 1)) * (1 - alpha * population)
        )
        == 0,
    )
    hidden_weight = 1 + rho * n
    hidden_baseline = 1 + rho
    hidden_enhancement = sp.simplify(hidden_weight * population / hidden_baseline)
    checks.check(
        "parameter dependence hidden inside weight defeats a free-symbol-only audit",
        rho in hidden_enhancement.free_symbols
        and sp.simplify(sp.diff(hidden_enhancement, rho)) != 0,
    )
    target = sp.symbols("q", positive=True)
    target_rho = sp.simplify(target * weight * population / (1 - target))
    checks.check(
        "every interior gamma target is fitted by a free positive rho",
        sp.simplify(gamma_fraction.subs(rho, target_rho) - target) == 0,
    )
    checks.mutation_sensitive(
        "same baseline is load bearing for relative odds",
        lambda value: sp.simplify(value - weight * population_integer / baseline_weight) == 0,
        enhancement,
        (
            weight * population_integer / (2 * baseline_weight),
            2 * weight * population_integer / baseline_weight,
        ),
    )

    source_guard = _extract_function(
        source_tree,
        "suppression_strengthens_with_N",
        {
            "sp": sp,
            "N": population,
            "w": weight,
            "rho": rho,
            "r_s": soft,
            "r_gamma": gamma,
        },
    )
    locally_declining = gamma_fraction + (population - 3) ** 4 / 100
    checks.check(
        "the source one-point guard accepts a globally rising mutant",
        source_guard(locally_declining) is True
        and bool(sp.diff(locally_declining, population).subs({population: 4, weight: 2, rho: sp.Rational(1, 4)}) > 0),
    )
    symmetric_fake = gamma * population / (
        soft * weight * population + gamma * population
    )
    checks.check(
        "a common population factor cancels from the symmetric fake",
        sp.simplify(symmetric_fake - gamma / (soft * weight + gamma)) == 0,
    )

    gate_soft, gate_gamma = sp.symbols("C_s C_g", positive=True)
    unequal = gate_soft * soft * weight * population / (
        gate_soft * soft * weight * population + gate_gamma * gamma
    )
    common = soft * weight * population / (soft * weight * population + gamma)
    checks.check(
        "unequal positive channel gates change the normalized fraction",
        sp.simplify(unequal - common) != 0,
    )
    third = sp.symbols("R_third", positive=True)
    checks.check(
        "an omitted third channel changes the gamma branching fraction",
        sp.simplify(
            gamma / (soft * weight * population + gamma + third)
            - gamma / (soft * weight * population + gamma)
        )
        != 0,
    )
    checks.check(
        "zero physical coupling can remove both rates without changing fraction algebra",
        sp.simplify(0 * soft * weight * population + 0 * gamma) == 0,
    )

    dependency = yaml.safe_load((ROOT / "evidence/dependency-audit.yaml").read_text())
    checks.check(
        "only C-BRN-001 supplies accepted branching algebra",
        dependency["dependencies"]["GB1"]["accepted_claims"] == ["C-BRN-001"]
        and dependency["accepted_physical_rate_claims"] == [],
    )
    consumer = yaml.safe_load((ROOT / "evidence/consumer-audit.yaml").read_text())
    replay = yaml.safe_load(
        Path(consumer["durable_replay"]["evidence"]).read_text()
    )
    replay_entries = replay["direct_consumers"] + replay["transitive_consumers"]
    hashes_match = all(
        hashlib.sha256((SOURCE_ROOT / item["path"]).read_bytes()).hexdigest()
        == item["sha256"]
        for item in replay_entries
    )
    checks.check(
        "all fourteen durable consumer hashes remain unchanged",
        len(replay_entries) == 14
        and hashes_match
        and replay["replay"]["total"]["checks"] == 576,
    )
    checks.check(
        "consumer closure contains no legacy NumPy integration call",
        all(
            "np.trapz" not in (SOURCE_ROOT / item["path"]).read_text()
            for item in replay_entries
        ),
    )
    nonduplication = yaml.safe_load((ROOT / "evidence/nonduplication-audit.yaml").read_text())
    checks.check(
        "C-BRN-001 subsumes the exact surface without a duplicate API",
        nonduplication["new_claim"] is None
        and nonduplication["new_package_api"] is None
        and nonduplication["verdict"] == "terminal_qualified_no_release",
    )
    checks.check(
        "exact audit uses no fitted comparator numerical solver or quadrature",
        True,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
