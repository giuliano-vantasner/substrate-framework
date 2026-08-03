"""Primary exact verifier for P117's CM3 monotone-crossover audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.composite_factors import nominal_loss_cycle_product
from substrate_framework.crossovers import (
    exponential_crossover_energy,
    exponential_crossover_ledger,
    exponential_saturation,
    monotone_range_location,
    shifted_barrier_crossover_energy,
    shifted_barrier_crossover_ledger,
    shifted_barrier_crossover_residual,
    shifted_barrier_zero_energy_floor,
)
from substrate_framework.screened_barrier import (
    shifted_inverse_sqrt_barrier_factor,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-31/"
    "bridge_CM3_crossover.py"
)
SOURCE_SHA256 = "d62d8deadbba30c4d240ed57c204149ffe0d6b2ec49ed0e200206a4b4a8eccdb"
CONTRACT_SHA256 = "faa958c93d9a7478bd6abd2f8cc10cea58267d217b3b0b6f04e0f8b8b3efa1d1"
FREEZE_SHA256 = "faa958c93d9a7478bd6abd2f8cc10cea58267d217b3b0b6f04e0f8b8b3efa1d1"


def _campaign_root() -> Path:
    candidates = (
        Path("campaigns/P117-cm3-monotone-crossover-audit"),
        Path("proposals/P117-cm3-monotone-crossover-audit"),
    )
    return next(path for path in candidates if path.exists())


def main() -> int:
    checks = CheckLedger("C-XOV-001")
    root = _campaign_root()
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "CM3 source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    normalized_contract = (
        (root / "proposal.yaml")
        .read_bytes()
        .replace(b"status: accepted\n", b"status: draft\n")
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    checks.check(
        "pre-source contract is immutable",
        hashlib.sha256((root / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA256,
    )
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "ten static predicates match the runtime tally",
        len(source_checks) == 10
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "CM3 has no sampled-integration compatibility event",
        "np.trapz" not in source_text
        and "np.trapezoid" not in source_text
        and "trapezoid_integral" not in source_text,
    )

    checks.check(
        "range classifier separates lower endpoint interior and upper limit",
        monotone_range_location(0, 1, 0) == "lower_endpoint"
        and monotone_range_location(0, 1, sp.Rational(1, 2))
        == "unique_interior"
        and monotone_range_location(0, 1, 1) == "upper_limit_only",
    )
    checks.check(
        "out-of-range levels have no finite crossing",
        monotone_range_location(0, 1, -1) == "below_range"
        and monotone_range_location(0, 1, 2) == "above_range",
    )

    energy, scale, odds = sp.symbols("E E0 u", positive=True)
    level = sp.simplify(odds / (1 + odds))
    response = exponential_saturation(energy, scale)
    crossing = exponential_crossover_energy(scale, level)
    expected_crossing = sp.simplify(scale * sp.log(1 + odds))
    checks.check(
        "the exponential level parameter lies strictly between zero and one",
        level.is_positive is True and (1 - level).is_positive is True,
    )
    checks.check(
        "the exponential crossover inverse is exact for every positive odds",
        sp.simplify(crossing - expected_crossing) == 0,
    )
    checks.check(
        "substitution of the exact inverse has zero residual",
        sp.simplify(response.subs(energy, crossing) - level) == 0,
    )
    checks.check(
        "the exponential response is continuous and strictly increasing",
        sp.diff(response, energy).is_positive is True
        and sp.limit(response, energy, 0, dir="+") == 0
        and sp.limit(response, energy, sp.oo) == 1,
    )
    below_residual = sp.simplify(
        exponential_saturation(crossing / 2, scale) - level
    )
    above_residual = sp.simplify(
        exponential_saturation(2 * crossing, scale) - level
    )
    odds_root = sp.sqrt(1 + odds)
    checks.check(
        "strict increase gives below and above ordering globally",
        sp.simplify(
            below_residual * (1 + odds) * odds_root
            + odds_root * (odds_root - 1)
        )
        == 0
        and sp.simplify((odds_root - 1) * (odds_root + 1) - odds) == 0
        and odds.is_positive is True
        and (odds_root + 1).is_positive is True
        and sp.simplify(above_residual - odds / (1 + odds) ** 2) == 0
        and (odds / (1 + odds) ** 2).is_positive is True,
    )

    rational_level = sp.Rational(2, 5)
    ledger = exponential_crossover_ledger(scale, rational_level)
    checks.check(
        "level sensitivity and convexity are strictly positive",
        ledger.level_derivative.is_positive is True
        and ledger.level_second_derivative.is_positive is True,
    )
    checks.check(
        "scale sensitivity is positive and equals the reduced crossing",
        sp.simplify(
            ledger.scale_derivative - ledger.crossover_energy / scale
        )
        == 0
        and ledger.scale_derivative.is_positive is True,
    )
    checks.check(
        "zero level is the finite lower-endpoint crossing",
        exponential_crossover_energy(scale, 0) == 0,
    )
    checks.check(
        "the crossover diverges as the level approaches the unattained upper limit",
        sp.limit(crossing, odds, sp.oo) == sp.oo
        and sp.limit(level, odds, sp.oo) == 1,
    )
    rho = sp.symbols("rho", positive=True)
    checks.check(
        "common energy rescaling is covariant",
        sp.simplify(
            exponential_crossover_energy(rho * scale, rational_level)
            - rho * exponential_crossover_energy(scale, rational_level)
        )
        == 0,
    )
    checks.check(
        "the reported half-level specialization is exactly log two",
        exponential_crossover_energy(1, sp.Rational(1, 2)) == sp.log(2),
    )

    barrier, shift, exponent = sp.symbols("G U q", positive=True)
    screened_level = sp.exp(-exponent)
    screened_crossing = shifted_barrier_crossover_energy(
        barrier,
        shift,
        screened_level,
    )
    checks.check(
        "the actual shifted-factor inverse is exact algebraically",
        sp.simplify(screened_crossing - (barrier / exponent**2 - shift)) == 0,
    )
    positive_crossing = sp.symbols("X", positive=True)
    parameterized_barrier = sp.simplify((positive_crossing + shift) * exponent**2)
    checks.check(
        "the shifted inverse satisfies the canonical factor on its interior domain",
        shifted_barrier_crossover_residual(
            parameterized_barrier,
            shift,
            screened_level,
        )
        == 0,
    )
    floor = shifted_barrier_zero_energy_floor(barrier, shift)
    checks.check(
        "positive screening shift gives a finite positive floor rather than zero",
        floor.is_positive is True
        and sp.simplify(
            sp.limit(
                shifted_inverse_sqrt_barrier_factor(
                    energy,
                    barrier,
                    shift,
                ),
                energy,
                0,
                dir="+",
            )
            - floor
        )
        == 0,
    )
    checks.check(
        "the surrogate and actual shifted factor disagree at zero input",
        exponential_saturation(0, scale) == 0 and floor.is_positive is True,
    )
    floor_margin = sp.symbols("r", positive=True)
    floor_parameterized_barrier = shift * (exponent + floor_margin) ** 2
    floor_ratio = sp.simplify(
        screened_level
        / floor.subs(barrier, floor_parameterized_barrier)
    )
    positive_parameterized_crossing = sp.factor(
        screened_crossing.subs(barrier, floor_parameterized_barrier)
    )
    checks.check(
        "the shifted crossing is positive exactly above the floor",
        floor_ratio.is_positive is True
        and sp.simplify(sp.log(floor_ratio) - floor_margin) == 0
        and floor_margin.is_positive is True
        and sp.simplify(
            positive_parameterized_crossing
            - shift * floor_margin * (2 * exponent + floor_margin) / exponent**2
        )
        == 0
        and positive_parameterized_crossing.is_positive is True,
    )
    screened_ledger = shifted_barrier_crossover_ledger(
        barrier,
        shift,
        screened_level,
    )
    checks.check(
        "shifted crossing sensitivities have exact global signs",
        screened_ledger.level_derivative.is_positive is True
        and screened_ledger.barrier_derivative.is_positive is True
        and screened_ledger.shift_derivative == -1,
    )
    checks.check(
        "zero shift recovers a zero floor and positive inverse",
        shifted_barrier_zero_energy_floor(barrier, 0) == 0
        and shifted_barrier_crossover_energy(barrier, 0, screened_level)
        == barrier / exponent**2,
    )
    checks.check(
        "shifted crossing is covariant under common energy rescaling",
        sp.simplify(
            shifted_barrier_crossover_energy(
                rho * barrier,
                rho * shift,
                screened_level,
            )
            - rho * screened_crossing
        )
        == 0,
    )

    gamma, omega, coupling = sp.symbols("Gamma omega c_pair", positive=True)
    cm2_factor = nominal_loss_cycle_product((1,), (coupling,), gamma, omega)
    checks.check(
        "C-CMP-001's accepted CM2 factor is not flat in loss",
        sp.diff(cm2_factor, gamma).is_negative is True,
    )
    target_energy = sp.symbols("E_target", positive=True)
    fitted_scale = sp.simplify(target_energy / sp.log(1 + odds))
    checks.check(
        "free level or scale fits any positive crossover target",
        sp.simplify(
            exponential_crossover_energy(fitted_scale, level) - target_energy
        )
        == 0,
    )
    rate_prefactor, rate_target = sp.symbols("nu R_target", positive=True)
    checks.check(
        "zero physical normalization is a zero-channel countermodel",
        0 * response == 0
        and exponential_saturation(scale, scale) == 1 - sp.exp(-1)
        and (1 - sp.exp(-1)).is_positive is True,
    )
    checks.check(
        "a free physical normalization fits any positive channel target",
        sp.simplify(
            (rate_prefactor * response).subs(
                rate_prefactor,
                rate_target / response,
            )
            - rate_target
        )
        == 0,
    )

    x = sp.symbols("x", real=True)
    plateau = sp.Piecewise((x, x < 1), (1, True))
    discontinuous = sp.Piecewise((0, x < 0), (1, True))
    nonmonotone = x**2
    checks.check(
        "loss of strictness permits a plateau of crossings",
        plateau.subs(x, 1) == 1 and plateau.subs(x, 2) == 1,
    )
    checks.check(
        "loss of continuity can skip every interior level",
        discontinuous.subs(x, -1) == 0
        and discontinuous.subs(x, 1) == 1
        and sp.solve(sp.Eq(discontinuous, sp.Rational(1, 2)), x) == [],
    )
    checks.check(
        "loss of monotonicity permits multiple crossings",
        sp.solve(sp.Eq(nonmonotone, 1), x) == [-1, 1],
    )

    checks.mutation_sensitive(
        "exponential inverse sign complement and scale are load bearing",
        lambda candidate: sp.simplify(
            (1 - sp.exp(-candidate / scale)) - level
        )
        == 0,
        crossing,
        (
            2 * scale * sp.log(1 + odds),
            -scale * sp.log(level),
            -2 * scale * sp.log(1 - level),
            scale * sp.log(1 - level),
        ),
    )
    checks.mutation_sensitive(
        "shift floor and inverse conventions are load bearing",
        lambda candidate: sp.simplify(
            candidate - (barrier / exponent**2 - shift)
        )
        == 0,
        screened_crossing,
        (
            barrier / exponent**2 + shift,
            barrier / exponent - shift,
            barrier * exponent**2 - shift,
        ),
    )

    claims = yaml.safe_load(Path("governance/claims.yaml").read_text())["claims"]
    governed = [claim for claim in claims if claim["id"] == "C-XOV-001"]
    if root.parts[0] == "proposals":
        lifecycle_ok = not governed
    else:
        lifecycle_ok = (
            len(governed) == 1
            and governed[0]["review"] == "accepted"
            and governed[0]["provenance"]
            == "campaigns/P117-cm3-monotone-crossover-audit/adjudication.yaml"
        )
    checks.check("claim lifecycle matches draft or promoted state", lifecycle_ok)
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
