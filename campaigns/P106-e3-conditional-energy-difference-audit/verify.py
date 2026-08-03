"""Primary exact and resolution-ledger verifier for the P106 E3 audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
import yaml

from substrate_framework.energy_differences import (
    linear_difference_coefficient,
    linear_difference_interval,
    normalized_linear_difference,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-29/"
    "bridge_E3_yield_coefficient_overbinding.py"
)
SOURCE_SHA256 = "aa76b9e675d4fbb45594e9d3df5107af175e927a24840260ca71ffda1bad3315"
INITIAL_CONTRACT_SHA256 = "c4c1b535a2a4254544635d43667f671c52384e68fe9059b63713947743de1673"
REVISED_CONTRACT_SHA256 = "c5a0f09005ad8c6716814e85c374b8e21dacd94ef8efb80a647b30db8784c1a2"
FREEZE_SHA256 = "21e54dd267cfca015bdc99fa6be24d30decbf0a8dca460fa22e176f5729664aa"
REVISION_SHA256 = "d8ddc173aa2951a24eb285ad1898bb11c4280e22c4898d9ddf0bf71b58272a93"
P105_CANONICAL_SHA256 = "33e58ec644a0181c9395b20fe171dbd5a612b533b9e24f696f99cb859be375f6"
P105_INDEPENDENT_SHA256 = "28f7d2b3e85c0d32bb869c3af69d8603c2b2c022b485aa01b70e7767490de2d3"


def _campaign_root() -> Path:
    return Path(__file__).resolve().parent


def _repository_root() -> Path:
    return _campaign_root().parents[1]


def _load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text())


def _exact_decimal(value: object) -> sp.Rational:
    return sp.Rational(str(value))


def _normalized_contract_bytes() -> bytes:
    return (
        (_campaign_root() / "proposal.yaml")
        .read_bytes()
        .replace(b"status: accepted\n", b"status: draft\n")
    )


def _profile_snapshots() -> tuple[dict[str, object], dict[str, object]]:
    root = _repository_root()
    canonical_path = (
        root
        / "campaigns/P105-e2-rational-map-radial-profiles/attempts/0006/result.yaml"
    )
    independent_path = (
        root
        / "campaigns/P105-e2-rational-map-radial-profiles/attempts/0005/result.yaml"
    )
    if hashlib.sha256(canonical_path.read_bytes()).hexdigest() != P105_CANONICAL_SHA256:
        raise AssertionError("P105 canonical snapshot hash changed")
    if hashlib.sha256(independent_path.read_bytes()).hexdigest() != P105_INDEPENDENT_SHA256:
        raise AssertionError("P105 independent snapshot hash changed")
    return _load_yaml(canonical_path), _load_yaml(independent_path)


def main() -> int:
    checks = CheckLedger("P106")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "recorded claim-delta revision is the only contract change",
        hashlib.sha256(_normalized_contract_bytes()).hexdigest()
        == REVISED_CONTRACT_SHA256
        and hashlib.sha256(
            (_campaign_root() / "proposal-revision-0001.yaml").read_bytes()
        ).hexdigest()
        == REVISION_SHA256,
    )
    checks.check(
        "pre-source contract commitment is immutable",
        hashlib.sha256((_campaign_root() / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA256
        and INITIAL_CONTRACT_SHA256
        in (_campaign_root() / "evidence/frozen-proposal.yaml").read_text(),
    )
    literal_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source has five literal predicates and a dynamic terminal tally",
        len(literal_checks) == 5
        and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source selects current NumPy trapezoid before its immutable legacy fallback",
        'np.trapezoid if hasattr(np, "trapezoid") else np.trapz' in source_text
        and hasattr(np, "trapezoid"),
    )
    checks.check(
        "source profile route lacks a solver-status gate",
        "sol = solve_bvp" in source_text
        and "sol.success" not in source_text
        and "sol.status" not in source_text,
    )
    checks.check(
        "source repeats midpoint arrays with trapezoidal reduction",
        "(np.arange(n_th) + 0.5)" in source_text
        and "(np.arange(n_ph) + 0.5)" in source_text
        and "return trapezoid(trapezoid" in source_text,
    )

    n, alpha, b_initial, b_final, scale = sp.symbols(
        "n alpha b_i b_f U", positive=True
    )
    mass_initial = alpha * b_initial * scale
    mass_final = alpha * b_final * scale
    release = sp.expand(n * mass_initial - mass_final)
    coefficient = sp.factor(release / scale)
    checks.check(
        "direct declared-mass algebra retains every load-bearing coordinate",
        coefficient == alpha * (n * b_initial - b_final)
        and coefficient.free_symbols == {alpha, n, b_initial, b_final},
    )
    checks.check(
        "scale cancels only after the mass normalization is declared",
        sp.simplify(sp.diff(release, scale) - coefficient) == 0
        and sp.simplify(release - coefficient * scale) == 0,
    )

    one_body, degree_initial = sp.symbols("M_1 A_i", real=True)
    degree_final = n * degree_initial
    binding_initial = degree_initial * one_body - mass_initial
    binding_final = degree_final * one_body - mass_final
    release_from_bindings = sp.expand(binding_final - n * binding_initial)
    checks.check(
        "fresh binding ledger cancels the one-body term exactly",
        sp.simplify(release_from_bindings - release) == 0
        and one_body not in release_from_bindings.free_symbols,
    )
    checks.check(
        "binding and direct-mass routes agree only with conserved multiplicity",
        sp.simplify(degree_final - n * degree_initial) == 0
        and sp.simplify(release_from_bindings / scale - coefficient) == 0,
    )
    kappa = sp.Symbol("kappa", real=True)
    solved_final = sp.solve(sp.Eq(kappa, coefficient), b_final)
    checks.check(
        "coefficient inverse and zero surface are exact",
        solved_final == [n * b_initial - kappa / alpha]
        and coefficient.subs(b_final, n * b_initial) == 0,
    )
    checks.check(
        "positive normalization preserves all three possible signs",
        coefficient.subs({alpha: 3, n: 2, b_initial: 2, b_final: 3}) > 0
        and coefficient.subs({alpha: 3, n: 2, b_initial: 2, b_final: 4}) == 0
        and coefficient.subs({alpha: 3, n: 2, b_initial: 2, b_final: 5}) < 0,
    )
    baseline = 3 * sp.pi**2 * (2 * b_initial - b_final)
    checks.mutation_sensitive(
        "normalization multiplicity and subtraction are load bearing",
        lambda candidate: sp.simplify(candidate - baseline) == 0,
        baseline,
        (
            12 * sp.pi**2 * (2 * b_initial - b_final),
            3 * sp.pi**2 * (b_initial - b_final),
            3 * sp.pi**2 * (2 * b_initial + b_final),
        ),
    )

    canonical, independent = _profile_snapshots()
    canonical_values = canonical["corrected_2401_sample_results"]
    independent_values = independent["independent_results"]
    b2_c = _exact_decimal(canonical_values["B2"]["energy_coefficient"])
    b4_c = _exact_decimal(canonical_values["B4"]["energy_coefficient"])
    b2_i = _exact_decimal(independent_values["B2"]["energy_coefficient"])
    b4_i = _exact_decimal(independent_values["B4"]["energy_coefficient"])
    kappa_c = sp.N(3 * sp.pi**2 * (2 * b2_c - b4_c), 40)
    kappa_i = sp.N(3 * sp.pi**2 * (2 * b2_i - b4_i), 40)
    checks.check(
        "accepted P105 snapshots supply total rather than per-degree coefficients",
        b2_c == 2 * _exact_decimal(canonical_values["B2"]["per_degree"])
        and b4_c == 4 * _exact_decimal(canonical_values["B4"]["per_degree"]),
    )
    checks.check(
        "accepted-value coefficient is derived from the pinned P105 snapshot",
        sp.N(2 * b2_c - b4_c, 20) > 0
        and sp.N(kappa_c, 20) > 8
        and sp.N(kappa_c, 20) < 9,
    )
    checks.check(
        "independent P105 route gives the same positive combination",
        sp.N(2 * b2_i - b4_i, 20) > 0
        and abs(float(kappa_c - kappa_i)) < 3e-6,
    )

    b2_lo, b2_hi = min(b2_c, b2_i), max(b2_c, b2_i)
    b4_lo, b4_hi = min(b4_c, b4_i), max(b4_c, b4_i)
    rectangular_lo = sp.N(3 * sp.pi**2 * (2 * b2_lo - b4_hi), 40)
    rectangular_hi = sp.N(3 * sp.pi**2 * (2 * b2_hi - b4_lo), 40)
    checks.check(
        "rectangular method-spread envelope follows monotonic endpoint propagation",
        rectangular_lo <= kappa_c <= rectangular_hi
        and rectangular_lo <= kappa_i <= rectangular_hi
        and rectangular_lo > 0,
    )
    checks.check(
        "method spread is sensitivity evidence rather than exact status",
        0 < float(rectangular_hi - rectangular_lo) < 3e-6
        and canonical["status"] == "record_correction_passed"
        and independent["status"] == "focused_scientific_gate_passed",
    )
    api_coefficient = linear_difference_coefficient(
        float(b2_c),
        float(b4_c),
        multiplicity=2,
        normalization=3.0 * np.pi**2,
    )
    api_interval = linear_difference_interval(
        (float(b2_lo), float(b2_hi)),
        (float(b4_lo), float(b4_hi)),
        multiplicity=2,
        normalization=3.0 * np.pi**2,
    )
    checks.check(
        "canonical API regresses the independently derived exact and interval formulas",
        abs(
            normalized_linear_difference(float(b2_c), float(b4_c), multiplicity=2)
            - float(2 * b2_c - b4_c)
        )
        <= np.spacing(abs(float(2 * b2_c - b4_c)))
        and abs(api_coefficient - float(kappa_c)) < 2e-15
        and api_interval.contains(float(kappa_c))
        and api_interval.contains(float(kappa_i)),
    )
    print(
        "P106 accepted-input ledger: "
        f"delta={float(2 * b2_c - b4_c):.12f}, "
        f"kappa={float(kappa_c):.12f}, "
        f"method envelope=[{float(rectangular_lo):.12f}, "
        f"{float(rectangular_hi):.12f}]"
    )

    source_band = lambda value: sp.Rational(15, 2) < value < sp.Rational(19, 2)
    checks.check(
        "source band admits incompatible ten-percent normalization mutations",
        source_band(kappa_c)
        and source_band(sp.Rational(9, 10) * kappa_c)
        and source_band(sp.Rational(11, 10) * kappa_c),
    )
    checks.check(
        "source broad-band predicate cannot establish accepted numeric provenance",
        "7.5 < kappa_classical < 9.5" in source_text
        and "I_OF_B = {1: I_integral" in source_text
        and "b = {B: b_of_B" in source_text,
    )

    true_x, true_y, upper_x, upper_y = sp.symbols("x y X Y", real=True)
    slack_x, slack_y = sp.symbols("delta_x delta_y", nonnegative=True)
    difference_with_slack = sp.expand(
        (upper_x - slack_x) - (upper_y - slack_y)
    )
    checks.check(
        "difference of separate upper bounds retains an uncontrolled slack difference",
        sp.simplify(
            difference_with_slack
            - ((upper_x - upper_y) - (slack_x - slack_y))
        )
        == 0,
    )
    checks.check(
        "explicit valid upper-bound counterexamples reverse either comparison",
        2 <= 2
        and 0 <= 2
        and (2 - 0) > (2 - 2)
        and 0 <= 2
        and 2 <= 2
        and (0 - 2) < (2 - 2),
    )
    checks.check(
        "zero-slack limit recovers the bound difference without generalizing it",
        sp.simplify(difference_with_slack.subs({slack_x: 0, slack_y: 0}) - (upper_x - upper_y))
        == 0,
    )

    checks.check(
        "source imports rather than derives its physical mass and scale premises",
        "IMPORTED (cite): the NY1 mass map" in source_text
        and "F_PI_OVER_E = float(16 * sp.pi * 0.51099895)" in source_text,
    )
    checks.check(
        "source empirical and BPS comparisons are separate inputs",
        "B_HE4, B_D = 28.30, 2.22" in source_text
        and "kappa_BPS = 0" in source_text
        and "DEFERRED to E4" in source_text,
    )
    checks.check(
        "removing empirical literals leaves the conditional coefficient unchanged",
        coefficient.free_symbols == {alpha, n, b_initial, b_final}
        and scale not in coefficient.free_symbols,
    )
    checks.check(
        "no new numerical solve or quadrature is needed for the E3 composition",
        not any(expression.has(sp.Integral) for expression in (
            coefficient,
            release_from_bindings,
            difference_with_slack,
        )),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
