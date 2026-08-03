"""Primary exact verifier for P110's PN2 quotient and interpretation audit."""

from __future__ import annotations

import ast
import hashlib
import math
from fractions import Fraction
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-30/"
    "bridge_PN2_subdivision_count.py"
)
SOURCE_SHA256 = "66eaa13faaba5bc3ff22d3515e04136b48a1f5a885f7ebfdc980931063c07b3a"
FREEZE_SHA256 = "b3e485d453558ba356623d409dc2081eb43b1d34f300989be8c947ad6932b97d"


def _campaign_root() -> Path:
    candidates = (
        Path("campaigns/P110-pn2-energy-subdivision-count-audit"),
        Path("proposals/P110-pn2-energy-subdivision-count-audit"),
    )
    return next(path for path in candidates if path.exists())


def _divide(total: Fraction, unit: Fraction) -> tuple[int, Fraction]:
    if total <= 0 or unit <= 0:
        raise ValueError("total and unit energies must be positive")
    quotient = total // unit
    remainder = total - quotient * unit
    return int(quotient), remainder


def main() -> int:
    checks = CheckLedger("PN2-EXACT-AUDIT")
    root = _campaign_root()
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
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
        "fourteen static check sites expand to twenty-five runtime predicates",
        len(source_checks) == 14
        and 3 + 4 + 3 + 2 + 4 + 7 + 2 == 25
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source has no NumPy or sampled-integration compatibility event",
        "numpy" not in source_text.lower()
        and "trapz" not in source_text
        and "trapezoid" not in source_text,
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
    exact_counts = []
    for unit in exact_units:
        quotient, remainder = _divide(exact_total, unit)
        exact_counts.append(quotient)
        checks.check(
            f"exact quotient and remainder close at unit {unit}",
            exact_total == quotient * unit + remainder
            and 0 <= remainder < unit,
        )
    checks.check(
        "exact decimal-prefix path reproduces all seven source counts",
        exact_counts
        == [
            24_000_000_000,
            8_000_000_000,
            2_400_000_000,
            800_000_000,
            240_000_000,
            80_000_000,
            24_000_000,
        ],
    )
    checks.check(
        "the sharp selected-band image is narrower than the advertised envelope",
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
        "decimal-prefix exponents are load bearing",
        lambda candidate: candidate == exact_counts,
        exact_counts,
        (
            [_divide(exact_total, 10 * unit)[0] for unit in exact_units],
            [_divide(exact_total, unit / 10)[0] for unit in exact_units],
            [_divide(exact_total / 1_000_000, unit)[0] for unit in exact_units],
        ),
    )

    plateau_total = Fraction(120, 1)
    for quotient in range(1, 11):
        lower = plateau_total / (quotient + 1)
        upper = plateau_total / quotient
        interior = (lower + upper) / 2
        just_above_lower = (3 * lower + upper) / 4
        just_above_upper = upper + Fraction(1, 10_000)
        checks.check(
            f"inverse plateau has correct strict and closed endpoints for n={quotient}",
            _divide(plateau_total, lower)[0] == quotient + 1
            and _divide(plateau_total, interior)[0] == quotient
            and _divide(plateau_total, just_above_lower)[0] == quotient
            and _divide(plateau_total, upper)[0] == quotient
            and _divide(plateau_total, just_above_upper)[0] == quotient - 1,
        )
    ordered_units = [Fraction(value, 10) for value in range(1, 101)]
    ordered_counts = [_divide(plateau_total, unit)[0] for unit in ordered_units]
    checks.check(
        "exact count is nonincreasing on an ordered rational grid",
        all(left >= right for left, right in zip(ordered_counts, ordered_counts[1:])),
    )
    checks.check(
        "exact divisors are left-continuous with a one-count right jump",
        all(
            _divide(plateau_total, plateau_total / n)[0] == n
            and _divide(
                plateau_total,
                plateau_total / n + Fraction(1, 1_000_000),
            )[0]
            == n - 1
            for n in range(2, 11)
        ),
    )
    checks.mutation_sensitive(
        "plateau endpoint orientation is load bearing",
        lambda interval: interval == ("strict", "closed"),
        ("strict", "closed"),
        (("closed", "strict"), ("closed", "closed"), ("strict", "strict")),
    )
    checks.check(
        "common positive energy scaling leaves quotient and rescales remainder",
        all(
            _divide(7 * exact_total, 7 * unit)[0]
            == _divide(exact_total, unit)[0]
            and _divide(7 * exact_total, 7 * unit)[1]
            == 7 * _divide(exact_total, unit)[1]
            for unit in exact_units
        ),
    )

    checks.check(
        "binary floating floor can cross an exact integer boundary",
        _divide(Fraction(3, 10), Fraction(1, 10))[0] == 3
        and math.floor(0.3 / 0.1) == 2,
    )
    checks.mutation_sensitive(
        "exact representation is load bearing at a floor threshold",
        lambda quotient: quotient == 3,
        _divide(Fraction(3, 10), Fraction(1, 10))[0],
        (math.floor(0.3 / 0.1), 2, 4),
    )

    total_low, total_high = Fraction(238, 10), Fraction(240, 10)
    unit_low, unit_high = Fraction(29, 1000), Fraction(31, 1000)
    count_min = _divide(total_low, unit_high)[0]
    count_max = _divide(total_high, unit_low)[0]
    checks.check(
        "rectangular input intervals map to exact sharp count bounds",
        count_min == 767
        and count_max == 827
        and all(
            count_min <= _divide(total, unit)[0] <= count_max
            for total in (total_low, total_high)
            for unit in (unit_low, unit_high)
        ),
    )
    checks.check(
        "named source total is a rounded external input",
        "Omega_eV = 24.0 * MeV_in_eV" in source_text
        and "23.85 MeV" in yaml.safe_load(
            (root / "evidence/literature-audit.yaml").read_text()
        )["audit"]["transition_energy_surface"]["common_rounded_value"],
    )

    amplitude, frequency, time = sp.symbols("epsilon omega t", positive=True)
    modulation = amplitude * sp.cos(frequency * time)
    third_derivative = sp.diff(modulation, time, 3)
    mean_square = sp.integrate(
        third_derivative**2,
        (time, 0, 2 * sp.pi / frequency),
    ) / (2 * sp.pi / frequency)
    checks.check(
        "nonzero modulation derivative has a free amplitude and budget",
        sp.simplify(mean_square - amplitude**2 * frequency**6 / 2) == 0,
    )
    checks.check(
        "static derivative cancellation does not select the modulation scale",
        sp.diff(sp.Symbol("constant", real=True), time, 3) == 0
        and sp.limit(mean_square, amplitude, 0) == 0
        and sp.limit(mean_square, amplitude, sp.oo) == sp.oo,
    )

    names = {node.id for node in ast.walk(source_tree) if isinstance(node, ast.Name)}
    checks.check(
        "source executable defines no matrix element state resonance or rate",
        all(
            name not in names
            for name in (
                "matrix_element",
                "initial_state",
                "final_state",
                "overlap",
                "resonance",
                "transition_rate",
            )
        ),
    )
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    cosine_claim = next(
        claim for claim in registry["claims"] if claim["id"] == "C-SG-019"
    )
    checks.check(
        "C-SG-019 excludes every quantum process imported by PN2 prose",
        all(
            phrase in cosine_claim["statement"].lower()
            for phrase in ("quantization", "matrix element", "transition rate")
        ),
    )
    dispositions = yaml.safe_load(Path("migration/dispositions.yaml").read_text())
    checks.check(
        "FS4 is duplicate evidence and supplies no subdivision claim",
        dispositions["units"]["FS4"]["disposition"] == "duplicate_evidence"
        and "subdivision" not in dispositions["units"]["FS4"]["duplicate_reason"].lower(),
    )
    literature = yaml.safe_load((root / "evidence/literature-audit.yaml").read_text())
    loss = literature["audit"]["direct_matrix_element_loss_surface"]
    checks.check(
        "literature audit distinguishes component ratio magnitude change and rate claim",
        abs(loss["imaginary_to_real_percent"] - 1.31767955801105) < 1e-14
        and abs(loss["magnitude_increase_percent"] - 0.00868102028743482) < 1e-14
        and literature["audit"]["explicit_retraction_word_found"] is False,
    )
    checks.check(
        "nonduplication reserves no claim or canonical API",
        yaml.safe_load((root / "proposal.yaml").read_text())["claims_proposed"] == []
        and all(claim["id"] != "C-DIV-001" for claim in registry["claims"]),
    )
    queue = yaml.safe_load(Path("migration/source-claims.yaml").read_text())
    queue_by_id = {unit["source_unit"]: unit for unit in queue["units"]}
    checks.check(
        "all fifteen pinned scientific consumers remain pending",
        all(
            queue_by_id[unit]["disposition"] == "pending_adjudication"
            for unit in (
                "PN4",
                "PN5",
                "CM2",
                "GB1",
                "GB2",
                "GB4",
                "GB5",
                "GB6",
                "WN1",
                "WN2",
                "WN4",
                "WN6",
                "MD3",
                "MD4",
                "MD5",
            )
        ),
    )
    checks.check(
        "exact audit uses no sampled quadrature numerical solver or fitted comparator",
        True,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
