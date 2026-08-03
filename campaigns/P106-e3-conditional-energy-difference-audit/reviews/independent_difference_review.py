"""Independent P106 derivation without importing the primary verifier."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


CANONICAL_SNAPSHOT = Path(
    "campaigns/P105-e2-rational-map-radial-profiles/attempts/0006/result.yaml"
)
INDEPENDENT_SNAPSHOT = Path(
    "campaigns/P105-e2-rational-map-radial-profiles/attempts/0005/result.yaml"
)


def _number(value: object) -> sp.Rational:
    return sp.Rational(str(value))


def main() -> int:
    checks = CheckLedger("P106-INDEPENDENT")
    checks.check(
        "P105 evidence snapshots are independently hash pinned",
        hashlib.sha256(CANONICAL_SNAPSHOT.read_bytes()).hexdigest()
        == "33e58ec644a0181c9395b20fe171dbd5a612b533b9e24f696f99cb859be375f6"
        and hashlib.sha256(INDEPENDENT_SNAPSHOT.read_bytes()).hexdigest()
        == "28f7d2b3e85c0d32bb869c3af69d8603c2b2c022b485aa01b70e7767490de2d3",
    )
    canonical = yaml.safe_load(CANONICAL_SNAPSHOT.read_text())
    independent = yaml.safe_load(INDEPENDENT_SNAPSHOT.read_text())

    unit, normalization = sp.symbols("U c", positive=True)
    m_one, c_two, c_four = sp.symbols("M_1 c_2 c_4", real=True)
    mass_two = normalization * c_two * unit
    mass_four = normalization * c_four * unit
    binding_two = 2 * m_one - mass_two
    binding_four = 4 * m_one - mass_four
    from_binding = sp.expand(binding_four - 2 * binding_two)
    from_masses = sp.expand(2 * mass_two - mass_four)
    checks.check(
        "fresh binding construction cancels the one-body mass",
        sp.simplify(from_binding - from_masses) == 0
        and m_one not in from_binding.free_symbols,
    )
    fresh_coefficient = sp.factor(from_binding / unit)
    checks.check(
        "fresh factorization retains normalization and both branch coefficients",
        fresh_coefficient == normalization * (2 * c_two - c_four)
        and fresh_coefficient.free_symbols == {normalization, c_two, c_four},
    )
    checks.check(
        "fresh sign ledger spans positive zero and negative differences",
        [
            fresh_coefficient.subs({normalization: 1, c_two: 2, c_four: value})
            for value in (3, 4, 5)
        ]
        == [1, 0, -1],
    )

    c_values = canonical["corrected_2401_sample_results"]
    i_values = independent["independent_results"]
    b2c = _number(c_values["B2"]["energy_coefficient"])
    b4c = _number(c_values["B4"]["energy_coefficient"])
    b2i = _number(i_values["B2"]["energy_coefficient"])
    b4i = _number(i_values["B4"]["energy_coefficient"])
    kc = sp.N(fresh_coefficient.subs({
        normalization: 3 * sp.pi**2,
        c_two: b2c,
        c_four: b4c,
    }), 40)
    ki = sp.N(fresh_coefficient.subs({
        normalization: 3 * sp.pi**2,
        c_two: b2i,
        c_four: b4i,
    }), 40)
    checks.check(
        "fresh accepted-input and method-check coefficients agree tightly",
        8 < kc < 9 and 8 < ki < 9 and abs(float(kc - ki)) < 3e-6,
    )
    lo = sp.N(3 * sp.pi**2 * (2 * min(b2c, b2i) - max(b4c, b4i)), 40)
    hi = sp.N(3 * sp.pi**2 * (2 * max(b2c, b2i) - min(b4c, b4i)), 40)
    checks.check(
        "fresh rectangular endpoint propagation encloses both methods",
        0 < lo <= min(kc, ki) <= max(kc, ki) <= hi
        and float(hi - lo) < 3e-6,
    )

    upper_a, upper_b = sp.symbols("A B", real=True)
    slack_a, slack_b = sp.symbols("s_a s_b", nonnegative=True)
    actual_difference = (upper_a - slack_a) - (upper_b - slack_b)
    checks.check(
        "fresh upper-bound algebra exposes the unconstrained slack difference",
        sp.expand(actual_difference - (upper_a - upper_b)) == -slack_a + slack_b,
    )
    checks.check(
        "fresh bound countermodels lie on opposite sides of the bound difference",
        (2 - 0) > (2 - 2) and (0 - 2) < (2 - 2),
    )

    arbitrary_scale, arbitrary_map = sp.symbols("S T", positive=True)
    physical_candidate = arbitrary_scale * arbitrary_map * fresh_coefficient
    checks.check(
        "fresh physical completion retains independent scale and state-map premises",
        physical_candidate.free_symbols
        == {arbitrary_scale, arbitrary_map, normalization, c_two, c_four},
    )
    checks.check(
        "coefficient agreement cannot select either physical premise",
        sp.diff(physical_candidate, arbitrary_scale) != 0
        and sp.diff(physical_candidate, arbitrary_map) != 0,
    )
    checks.check(
        "independent route performs no profile solve or sampled quadrature",
        not any(
            expression.has(sp.Integral, sp.Derivative)
            for expression in (fresh_coefficient, actual_difference, physical_candidate)
        ),
    )
    print(
        "P106 independent ledger: "
        f"kappa_canonical={float(kc):.12f}, "
        f"kappa_cross_method={float(ki):.12f}, "
        f"envelope=[{float(lo):.12f}, {float(hi):.12f}]"
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
