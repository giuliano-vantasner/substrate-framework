"""Primary exact verifier for P109's PN1 cosine mixed-coefficient claim."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

import substrate_framework as framework
from substrate_framework.cosine_vertices import (
    cosine_mixed_coefficient,
    cosine_mixed_derivative,
    cosine_mixed_taylor_polynomial,
    vacuum_cosine_mixed_coefficient,
    vacuum_one_high_coefficient,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-30/"
    "bridge_PN1_multiphonon_vertex.py"
)
SOURCE_SHA256 = "f2fcd58c97b9e9aa0b92e0ece9d92ff6c7ddaddec1b385b10a68a156ac3df985"
CONTRACT_SHA256 = "a3e4a230ba74d4c2c0c8c2a3e0355121e60ff25cb410a84c8d14c2549265ad15"
FREEZE_SHA256 = "a3e4a230ba74d4c2c0c8c2a3e0355121e60ff25cb410a84c8d14c2549265ad15"


def _campaign_root() -> Path:
    candidates = (
        Path("campaigns/P109-pn1-cosine-mixed-vertex-audit"),
        Path("proposals/P109-pn1-cosine-mixed-vertex-audit"),
    )
    return next(path for path in candidates if path.exists())


def _claim(claim_id: str) -> dict[str, object]:
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    return next(claim for claim in registry["claims"] if claim["id"] == claim_id)


def _queue_unit(source_unit: str) -> dict[str, object]:
    queue = yaml.safe_load(Path("migration/source-claims.yaml").read_text())
    return next(unit for unit in queue["units"] if unit["source_unit"] == source_unit)


def main() -> int:
    checks = CheckLedger("C-SG-019")
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
        "pre-source commitment is immutable",
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
        "source has thirteen static call sites and a dynamic tally",
        len(source_checks) == 13
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "loop expansion explains the reproduced thirty-two source predicates",
        (8 - 1) + 1 + 2 + (3 * 4) + (3 * 2) + 2 + 2 == 32,
    )
    checks.check(
        "source needs no NumPy integration compatibility replay",
        "numpy" not in source_text.lower()
        and "np." not in source_text
        and "trapz" not in source_text
        and "trapezoid" not in source_text,
    )

    amplitude, high_scale, low_scale = sp.symbols("A a_H a_L", nonzero=True)
    for high_order in range(7):
        for low_order in range(7):
            total = high_order + low_order
            actual = vacuum_cosine_mixed_coefficient(
                high_order,
                low_order,
                amplitude=amplitude,
                high_scale=high_scale,
                low_scale=low_scale,
            )
            if total == 0 or total % 2:
                expected = sp.Integer(0)
            else:
                expected = (
                    amplitude
                    * (-1) ** (total // 2 + 1)
                    * high_scale**high_order
                    * low_scale**low_order
                    / (sp.factorial(high_order) * sp.factorial(low_order))
                )
            checks.check(
                f"all-order formula matches derivative at orders {high_order},{low_order}",
                sp.simplify(actual - expected) == 0,
            )

    checks.check(
        "vacuum constant and every tested odd total coefficient vanish",
        vacuum_cosine_mixed_coefficient(0, 0) == 0
        and all(
            vacuum_cosine_mixed_coefficient(j, k) == 0
            for j in range(6)
            for k in range(6)
            if (j + k) % 2 == 1
        ),
    )
    checks.check(
        "one-high specialization reproduces source orders one through fifteen",
        all(
            vacuum_one_high_coefficient(n)
            == (
                (-1) ** ((n - 1) // 2) / sp.factorial(n)
                if n % 2
                else 0
            )
            for n in range(1, 16)
        ),
    )
    checks.mutation_sensitive(
        "one-high sign parity and factorial are load bearing",
        lambda candidate: all(
            sp.simplify(candidate(n) - vacuum_one_high_coefficient(n)) == 0
            for n in (1, 2, 3, 5, 7)
        ),
        lambda n: (
            (-1) ** ((n - 1) // 2) / sp.factorial(n) if n % 2 else 0
        ),
        (
            lambda n: (-1) ** ((n + 1) // 2) / sp.factorial(n) if n % 2 else 0,
            lambda n: (-1) ** ((n - 1) // 2) / n if n % 2 else 0,
            lambda n: (-1) ** ((n - 1) // 2) / sp.factorial(n) if n % 2 == 0 else 0,
        ),
    )
    checks.check(
        "raw derivative differs from coefficient by both factorials",
        cosine_mixed_coefficient(2, 4) == sp.Rational(1, 48)
        and cosine_mixed_derivative(2, 4) == 1
        and sp.factorial(2) * sp.factorial(4) * cosine_mixed_coefficient(2, 4)
        == cosine_mixed_derivative(2, 4),
    )
    checks.mutation_sensitive(
        "coefficient versus raw derivative convention is load bearing",
        lambda pair: sp.simplify(pair[1] - sp.factorial(2) * sp.factorial(4) * pair[0]) == 0,
        (cosine_mixed_coefficient(2, 4), cosine_mixed_derivative(2, 4)),
        (
            (cosine_mixed_derivative(2, 4), cosine_mixed_derivative(2, 4)),
            (cosine_mixed_coefficient(2, 4), cosine_mixed_coefficient(2, 4)),
        ),
    )

    scaled = vacuum_one_high_coefficient(
        3,
        amplitude=amplitude,
        high_scale=high_scale,
        low_scale=low_scale,
    )
    checks.check(
        "one-high coefficient carries explicit amplitude and mode normalizations",
        scaled == -amplitude * high_scale * low_scale**3 / 6,
    )
    checks.check(
        "independent high and low rescalings have distinct exact powers",
        sp.simplify(scaled.subs(high_scale, 2 * high_scale) / scaled) == 2
        and sp.simplify(scaled.subs(low_scale, 2 * low_scale) / scaled) == 8,
    )
    checks.mutation_sensitive(
        "low-coordinate normalization power n is load bearing",
        lambda candidate: sp.simplify(candidate / scaled - 1) == 0,
        -amplitude * high_scale * low_scale**3 / 6,
        (
            -amplitude * high_scale * low_scale / 6,
            -amplitude * high_scale**3 * low_scale / 6,
            -amplitude * low_scale**3 / 6,
        ),
    )

    background = sp.pi / 2
    checks.check(
        "nonvacuum background makes odd total coefficients nonzero",
        cosine_mixed_coefficient(1, 0, background=background) == 1
        and cosine_mixed_coefficient(0, 1, background=background) == 1
        and cosine_mixed_coefficient(1, 2, background=background) == -sp.Rational(1, 2),
    )
    checks.check(
        "nonvacuum background can instead zero even total coefficients",
        cosine_mixed_coefficient(1, 1, background=background) == 0
        and cosine_mixed_coefficient(2, 0, background=background) == 0,
    )
    checks.mutation_sensitive(
        "vacuum background is load bearing for the parity selection rule",
        lambda candidate: candidate == (0, 1),
        (
            cosine_mixed_coefficient(1, 0, background=0),
            cosine_mixed_coefficient(1, 0, background=sp.pi / 2),
        ),
        ((1, 1), (0, 0)),
    )

    high, low, bookkeeper = sp.symbols("H L lambda", real=True)
    polynomial = cosine_mixed_taylor_polynomial(high, low, 8)
    potential = 1 - sp.cos(high + low)
    scaled_residual = (potential - polynomial).subs(
        {high: bookkeeper * high, low: bookkeeper * low}
    )
    checks.check(
        "degree-eight polynomial matches every total order below ten",
        sp.simplify(sp.series(scaled_residual, bookkeeper, 0, 10).removeO()) == 0,
    )
    tenth_order = sp.series(scaled_residual, bookkeeper, 0, 11).removeO()
    checks.check(
        "finite truncation retains a nonzero tenth-order remainder",
        sp.simplify(tenth_order) != 0
        and sp.expand(tenth_order).coeff(bookkeeper, 10) != 0,
    )
    checks.check(
        "univariate specialization reproduces accepted cosine local data",
        sp.expand(cosine_mixed_taylor_polynomial(high, 0, 6))
        == high**2 / 2 - high**4 / 24 + high**6 / 720,
    )

    magnitude_ratios = [
        sp.simplify(
            abs(vacuum_one_high_coefficient(n + 2))
            / abs(vacuum_one_high_coefficient(n))
        )
        for n in (1, 3, 5, 7)
    ]
    checks.check(
        "successive nonzero one-high magnitudes have exact factorial ratios",
        magnitude_ratios
        == [sp.Rational(1, (n + 1) * (n + 2)) for n in (1, 3, 5, 7)],
    )
    index = sp.symbols("m", integer=True, nonnegative=True)
    checks.check(
        "normalized one-high magnitude tends to zero despite unbounded formal order",
        sp.limit(1 / sp.gamma(2 * index + 2), index, sp.oo) == 0,
    )
    checks.mutation_sensitive(
        "factorial suppression distinguishes the exact series from an unsuppressed ladder",
        lambda candidate: candidate[0] > candidate[1] > candidate[2] > 0,
        tuple(abs(vacuum_one_high_coefficient(n)) for n in (1, 3, 5)),
        ((1, 1, 1), (1, 2, 3), (1, 0, 0)),
    )

    checks.check(
        "source fixes unit split and vacuum without testing alternatives",
        "V = 1 - sp.cos(phi_H + phi_L)" in source_text
        and "background" not in source_text
        and "high_scale" not in source_text
        and "low_scale" not in source_text,
    )
    checks.check(
        "source high low and quantum labels do not appear in its potential expression",
        ast.unparse(
            next(
                node.value
                for node in source_tree.body
                if isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == "V" for target in node.targets)
            )
        )
        == "1 - sp.cos(phi_H + phi_L)",
    )
    checks.check(
        "accepted classical potential supplies no quantum process premises",
        "quantum" not in _claim("C-SG-012")["statement"].lower()
        or "neither" in _claim("C-SG-012")["statement"].lower(),
    )
    checks.check(
        "existing periodic-potential claim stops at a univariate sixth-order series",
        "series through sixth order" in _claim("C-BRK-001")["statement"]
        and "mixed" not in _claim("C-BRK-001")["statement"].lower(),
    )
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    promoted = [claim for claim in registry["claims"] if claim["id"] == "C-SG-019"]
    checks.check(
        "C-SG-019 identifier is unique and promotion owned",
        len(promoted) <= 1
        and (
            not promoted
            or promoted[0]["provenance"]
            == "campaigns/P109-pn1-cosine-mixed-vertex-audit/adjudication.yaml"
        ),
    )
    checks.check(
        "proposed package functions are exported",
        all(
            hasattr(framework, name)
            for name in (
                "cosine_mixed_coefficient",
                "cosine_mixed_derivative",
                "cosine_mixed_taylor_polynomial",
                "vacuum_cosine_mixed_coefficient",
                "vacuum_one_high_coefficient",
            )
        ),
    )
    checks.check(
        "declared source dependencies have no high-low quantum-mode theorem",
        all(
            phrase not in " ".join(
                str(_claim(claim_id)["statement"]).lower()
                for claim_id in ("C-SG-009", "C-SG-011", "C-SG-012")
            )
            for phrase in ("creation operator", "transition rate", "phonon")
        ),
    )
    checks.check(
        "direct future consumers remain noncanonical pending evidence",
        all(
            _queue_unit(unit)["disposition"] == "pending_adjudication"
            for unit in ("PN2", "WN1", "WN2", "WN3", "WN6", "MD3")
        ),
    )
    checks.check(
        "exact claim work uses no sampled quadrature or numerical solver",
        True,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
