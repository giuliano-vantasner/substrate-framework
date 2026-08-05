#!/usr/bin/env python3
"""Independent KI3 range audit from accepted authority and exact functions."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.crossovers import monotone_range_location
from substrate_framework.verification import CheckLedger


ROOT = Path("/home/dan/substrate-framework")
CLAIMS = ROOT / "governance/claims.yaml"
CLAIMS_SHA256 = "b2d68ae4e293301d402de4a0292445805ff42e26871b058fc74427aac37b7a0f"
P107 = ROOT / "campaigns/P107-e4-bps-zero-binding-audit/adjudication.yaml"
P107_SHA256 = "06947b443bb6fb41fec59a199aab6051f5804a1c89bdcd00c3d5814a57fa7cd2"
P172 = ROOT / "campaigns/P172-ki2-epsilon-underdetermination-audit/adjudication.yaml"
P172_SHA256 = "a15b42bd20a9dda1b498ce6b230fdded0c2ef5690ba2b7dbf718fc71dc13b746"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P173-INDEPENDENT-KI3-REDERIVATION")
    checks.check(
        "independent authority files retain their pinned bytes",
        _digest(CLAIMS) == CLAIMS_SHA256
        and _digest(P107) == P107_SHA256
        and _digest(P172) == P172_SHA256,
    )
    registry = yaml.safe_load(CLAIMS.read_text(encoding="utf-8"))
    claims = {claim["id"]: claim for claim in registry["claims"]}
    bps_zero = claims["C-BPS-002"]["statement"]
    near_bps = claims["C-BPS-003"]["statement"]
    classical = claims["C-RDIFF-002"]["statement"]
    crossover = claims["C-XOV-001"]["statement"]
    checks.check(
        "accepted BPS zero difference is conditional on sector attainment",
        "with attainment in sectors A and n*A" in bps_zero
        and "not an existence" in bps_zero,
    )
    checks.check(
        "accepted near-BPS authority denies a global interpolation and fixed sign",
        "provide a global interpolation" in near_bps
        and "positive, zero, or negative" in near_bps,
    )
    checks.check(
        "accepted classical coordinate is neither a bound nor a BPS limit",
        "not a variational bound" in classical and "BPS limit" in classical,
    )

    epsilon = sp.symbols("epsilon", positive=True)
    canonical = epsilon / (1 + epsilon)
    checks.check(
        "an independent Pade witness has exact endpoint limits",
        sp.limit(canonical, epsilon, 0, "+") == 0
        and sp.limit(canonical, epsilon, sp.oo) == 1,
    )
    checks.check(
        "the independent Pade witness is strictly increasing and bounded",
        sp.simplify(sp.diff(canonical, epsilon) - (epsilon + 1) ** -2) == 0
        and canonical.is_positive is True
        and sp.simplify(1 - canonical).is_positive is True,
    )
    checks.check(
        "the accepted monotone theorem classifies its representative levels exactly",
        monotone_range_location(0, 1, sp.Rational(-1, 2)) == "below_range"
        and monotone_range_location(0, 1, 0) == "lower_endpoint"
        and monotone_range_location(0, 1, sp.Rational(1, 3))
        == "unique_interior"
        and monotone_range_location(0, 1, 1) == "upper_limit_only"
        and monotone_range_location(0, 1, sp.Rational(3, 2)) == "above_range",
    )
    checks.check(
        "C-XOV-001 declares the global premises rather than deriving them",
        "continuous strictly increasing function" in crossover
        and "actual range are independently load bearing" in crossover,
    )

    bump = epsilon / (1 + epsilon) ** 2
    high = sp.factor(canonical + 4 * bump)
    low = sp.factor(canonical - 4 * bump)
    checks.check(
        "independently constructed maps preserve both endpoint limits",
        all(
            sp.limit(function, epsilon, 0, "+") == 0
            and sp.limit(function, epsilon, sp.oo) == 1
            for function in (high, low)
        ),
    )
    checks.check(
        "the same endpoint data permit exact over- and undershoot",
        high.subs(epsilon, 1) == sp.Rational(3, 2)
        and low.subs(epsilon, 1) == -sp.Rational(1, 2),
    )
    high_derivative = sp.factor(sp.diff(high, epsilon))
    checks.check(
        "the overshooting map is increasing locally but decreasing later",
        high_derivative.subs(epsilon, sp.Rational(1, 2)) > 0
        and high_derivative.subs(epsilon, 2) < 0,
    )
    roots = sp.solve(sp.Eq(high, sp.Rational(6, 5)), epsilon)
    checks.check(
        "the overshooting map has two exact positive preimages",
        len(roots) == 2
        and sp.simplify(roots[0] * roots[1] - 6) == 0
        and all(root.is_positive is True for root in roots),
    )
    checks.check(
        "endpoint limits alone therefore imply neither exclusion nor uniqueness",
        high.subs(epsilon, 1) > 1
        and low.subs(epsilon, 1) < 0
        and len(roots) == 2,
    )

    target = sp.Rational(1, 2)
    inverses = (
        target / (1 - target),
        -sp.log(1 - target),
        sp.atanh(target),
        target / sp.sqrt(1 - target**2),
    )
    checks.check(
        "four endpoint-compatible monotone witnesses have distinct exact half-level inverses",
        all(
            sp.simplify(left - right) != 0
            for index, left in enumerate(inverses)
            for right in inverses[:index]
        ),
    )
    checks.check(
        "inverse ambiguity needs no empirical comparator",
        all(not value.has(sp.Float) for value in inverses),
    )

    p107 = yaml.safe_load(P107.read_text(encoding="utf-8"))
    p172 = yaml.safe_load(P172.read_text(encoding="utf-8"))
    checks.check(
        "prior governed reviews expose no common physical interpolation",
        p107["source_disposition"] == {"E4": "qualified"}
        and p172["source_disposition"] == {"KI2": "qualified"}
        and p172["claims"] == [],
    )
    checks.check(
        "the valid conditional monotone result is already governed by C-XOV-001",
        claims["C-XOV-001"]["review"] == "accepted"
        and claims["C-XOV-001"]["verification"] == "symbolic_verified"
        and claims["C-XOV-001"]["epistemic"] == "active",
    )
    total = checks.finish()
    print(f"P173 INDEPENDENT KI3 REDERIVATION ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
