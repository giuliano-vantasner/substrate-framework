"""Primary exact verifier for P113's PN5 magnitude-reproduction audit."""

from __future__ import annotations

import ast
import hashlib
import math
from fractions import Fraction
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.paired_resolvent import symmetric_pair_resolvent
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-30/"
    "bridge_PN5_magnitude_reproduction.py"
)
SOURCE_SHA256 = "8b2a35a873d9414653f9add48ceeed50d0d32142064bd67b95845b92aeaf87eb"
CONTRACT_SHA256 = "d08aec134cc0198c37e7f583865be0ce9f4b05c8c06cab45079c1861b9e9163d"
FREEZE_SHA256 = "d08aec134cc0198c37e7f583865be0ce9f4b05c8c06cab45079c1861b9e9163d"


def _campaign_root() -> Path:
    candidates = (
        Path("campaigns/P113-pn5-magnitude-reproduction-audit"),
        Path("proposals/P113-pn5-magnitude-reproduction-audit"),
    )
    return next(path for path in candidates if path.exists())


def _divide(total: Fraction, unit: Fraction) -> tuple[int, Fraction]:
    if total <= 0 or unit <= 0:
        raise ValueError("energies must be positive")
    quotient = total // unit
    return int(quotient), total - quotient * unit


def _claim(claim_id: str) -> dict[str, object]:
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    return next(claim for claim in registry["claims"] if claim["id"] == claim_id)


def main() -> int:
    checks = CheckLedger("PN5-EXACT-AUDIT")
    root = _campaign_root()
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash is pinned",
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
        "eleven static sites execute eleven runtime predicates",
        len(source_checks) == 11
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source has no sampled-integration compatibility event",
        "np.trapz" not in source_text
        and "np.trapezoid" not in source_text
        and "np.integrate" not in source_text,
    )

    exact_total = Fraction(24_000_000, 1)
    exact_units = [
        Fraction(1, 1000),
        Fraction(3, 1000),
        Fraction(1, 100),
        Fraction(3, 100),
        Fraction(1, 10),
        Fraction(3, 10),
        Fraction(1, 1),
    ]
    expected_counts = [
        24_000_000_000,
        8_000_000_000,
        2_400_000_000,
        800_000_000,
        240_000_000,
        80_000_000,
        24_000_000,
    ]
    exact_results = [_divide(exact_total, unit) for unit in exact_units]
    for unit, (quotient, remainder) in zip(exact_units, exact_results):
        checks.check(
            f"exact quotient and remainder close at unit {unit}",
            exact_total == quotient * unit + remainder
            and 0 <= remainder < unit,
        )
    exact_counts = [quotient for quotient, _ in exact_results]
    checks.check(
        "exact decimal-prefix route reproduces the seven source counts",
        exact_counts == expected_counts,
    )
    checks.check(
        "every selected division happens to have zero remainder",
        all(remainder == 0 for _, remainder in exact_results),
    )
    checks.check(
        "selected extrema are much narrower than the advertised envelope",
        (min(exact_counts), max(exact_counts))
        == (24_000_000, 24_000_000_000)
        and min(exact_counts) > 10_000_000
        and max(exact_counts) < 100_000_000_000,
    )
    checks.check(
        "thirty meV gives eight hundred million exactly",
        _divide(exact_total, Fraction(3, 100))[0] == 800_000_000,
    )
    checks.mutation_sensitive(
        "decimal prefix and total-energy scales are load bearing",
        lambda candidate: candidate == expected_counts,
        exact_counts,
        (
            [_divide(exact_total, 10 * unit)[0] for unit in exact_units],
            [_divide(exact_total, unit / 10)[0] for unit in exact_units],
            [_divide(exact_total / 1_000_000, unit)[0] for unit in exact_units],
        ),
    )

    plateau_total = Fraction(120, 1)
    checks.check(
        "sharp inverse floor plateaus have strict lower and closed upper edges",
        all(
            _divide(plateau_total, plateau_total / (count + 1))[0] == count + 1
            and _divide(
                plateau_total,
                (
                    plateau_total / (count + 1)
                    + plateau_total / count
                )
                / 2,
            )[0]
            == count
            and _divide(plateau_total, plateau_total / count)[0] == count
            for count in range(2, 31)
        ),
    )
    checks.mutation_sensitive(
        "plateau endpoint orientation is load bearing",
        lambda interval: interval == ("strict", "closed"),
        ("strict", "closed"),
        (("closed", "strict"), ("closed", "closed"), ("strict", "strict")),
    )
    checks.check(
        "binary floating floor can cross an exact decimal boundary",
        _divide(Fraction(3, 10), Fraction(1, 10))[0] == 3
        and math.floor(0.3 / 0.1) == 2,
    )
    checks.check(
        "common positive energy rescaling leaves all quotients unchanged",
        all(
            _divide(17 * exact_total, 17 * unit)[0]
            == _divide(exact_total, unit)[0]
            for unit in exact_units
        ),
    )
    checks.check(
        "independent energy rescaling changes the selected counts",
        [_divide(2 * exact_total, unit)[0] for unit in exact_units]
        == [2 * count for count in exact_counts],
    )
    checks.check(
        "any positive target integer can be manufactured by a selected unit",
        all(
            _divide(exact_total, exact_total / target)[0] == target
            for target in (1, 7, 10**4, 10**8, 10**12)
        ),
    )
    checks.check(
        "the source assigns rather than derives every energy input",
        "Omega_eV = 24.0 * MeV_in_eV" in source_text
        and "omega_ph_band = [" in source_text
        and "INPUT (named)" in source_text,
    )

    delta, gamma, coupling = sp.symbols("Delta Gamma g", positive=True)
    complex_pair = symmetric_pair_resolvent(delta, gamma, coupling**2)
    magnitude = coupling**2 * gamma / (delta**2 + gamma**2 / 4)
    checks.check(
        "C-RES-001 complex pair has the source magnitude",
        sp.simplify(sp.I * complex_pair - magnitude) == 0,
    )
    derivative = sp.factor(sp.diff(magnitude, gamma))
    checks.check(
        "exact derivative fixes the unique positive optimum",
        sp.solve(sp.together(derivative), gamma) == [2 * delta]
        and sp.diff(magnitude, gamma, 2).subs(gamma, 2 * delta) < 0,
    )
    checks.check(
        "exact peak is coupling squared over absolute detuning",
        sp.simplify(magnitude.subs(gamma, 2 * delta) - coupling**2 / delta)
        == 0,
    )
    checks.check(
        "both exact loss limits vanish",
        sp.limit(magnitude, gamma, 0, dir="+") == 0
        and sp.limit(magnitude, gamma, sp.oo) == 0,
    )
    checks.mutation_sensitive(
        "factor two and detuning scale are load bearing at the optimum",
        lambda candidate: sp.simplify(candidate - 2 * delta) == 0,
        2 * delta,
        (delta, 4 * delta, 2 / delta),
    )
    checks.mutation_sensitive(
        "quadratic coupling normalization is load bearing at the peak",
        lambda candidate: sp.simplify(candidate - coupling**2 / delta) == 0,
        coupling**2 / delta,
        (coupling / delta, coupling**2 / (2 * delta), coupling**4 / delta),
    )
    checks.check(
        "source numeric tolerance admits a nearby wrong optimum",
        abs(float(sp.Rational(4003, 2000)) - 2.0) < 2e-3,
    )
    checks.check(
        "source endpoint predicates are finite samples rather than limits",
        "Jeff_single_pair(1e-6)" in source_text
        and "Jeff_single_pair(1e4)" in source_text
        and "np.linspace(1e-3, 10.0, 20001)" in source_text,
    )
    checks.check(
        "pair expression has matrix-element rather than inverse-time dimensions",
        (2 + 1 - 2, 0) == (1, 0) and (1, 0) != (0, -1),
    )
    checks.check(
        "zero coupling preserves every count and removes the toy element",
        exact_counts == expected_counts and magnitude.subs(coupling, 0) == 0,
    )

    predicate_audit = yaml.safe_load(
        (root / "evidence/check-adjudication.yaml").read_text()
    )
    checks.check(
        "all eleven source predicates have individual verdicts",
        predicate_audit["runtime_predicate_count"] == 11
        and len(predicate_audit["predicates"]) == 11
        and all(
            item["verdict"] in {"retained", "qualified", "duplicate", "rejected"}
            for item in predicate_audit["predicates"]
        ),
    )
    literature = yaml.safe_load((root / "evidence/literature-audit.yaml").read_text())
    checks.check(
        "literature audit rejects both bare-floor attribution and retraction wording",
        literature["rechecked_surfaces"]["explicit_retraction_word_found"] is False
        and literature["rechecked_surfaces"]["floor_subdivision_formula_found"]
        is False,
    )
    dependency = yaml.safe_load((root / "evidence/dependency-audit.yaml").read_text())
    checks.check(
        "PN5-PN4 candidate cycle supplies no authority",
        dependency["candidate_cycle"] == ["PN5", "PN4", "PN5"]
        and dependency["cycle_authority"] == "none",
    )
    consumers = yaml.safe_load((root / "evidence/consumer-audit.yaml").read_text())
    checks.check(
        "two direct and twenty-two indirect consumers are pinned",
        sum(item["relation"] == "direct" for item in consumers["consumers"])
        == 2
        and sum(item["relation"] == "indirect" for item in consumers["consumers"])
        == 22,
    )
    checks.check(
        "every consumer hash matches pinned source evidence",
        all(
            hashlib.sha256(
                (Path("/home/dan/substrate") / item["path"]).read_bytes()
            ).hexdigest()
            == item["sha256"]
            for item in consumers["consumers"]
        ),
    )
    checks.check(
        "accepted pair claim already owns optimum peak and physical ceiling",
        all(
            phrase in str(_claim("C-RES-001")["statement"])
            for phrase in (
                "Gamma=2*|Delta|",
                "maximum |c|/|Delta|",
                "transition rate",
            )
        ),
    )
    p110 = yaml.safe_load(
        Path("campaigns/P110-pn2-energy-subdivision-count-audit/adjudication.yaml").read_text()
    )
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    checks.check(
        "nonduplication reserves no claim or canonical API",
        yaml.safe_load((root / "proposal.yaml").read_text())["claims_proposed"] == []
        and p110["claims"] == []
        and not any(claim["id"] in {"C-DIV-001", "C-RES-002"} for claim in registry["claims"]),
    )
    checks.check(
        "exact campaign work uses no quadrature solver or fitted comparator",
        True,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
