"""Independent P077 derivation without importing the canonical duality API."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-22/"
    "bridge_AS6_beta_self_dual_pin.py"
)
SOURCE_SHA256 = "2f6c76d8aedde25b343f85cb54b2618cd03c816a29553fa70a523909265dd7f0"


def main() -> int:
    checks = CheckLedger("P077-INDEPENDENT")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    checks.check(
        "review reads immutable AS6 source",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )

    x, coefficient = sp.symbols("x A", positive=True)
    dual = coefficient / x
    checks.check(
        "fresh double application is identity",
        sp.simplify(coefficient / dual - x) == 0,
    )
    checks.check(
        "fresh orbit product retains coefficient",
        sp.simplify(x * dual - coefficient) == 0,
    )
    fixed_solutions = sp.solve(sp.Eq(x, coefficient / x), x)
    checks.check(
        "fresh positive fixed solve is square root coefficient",
        fixed_solutions == [sp.sqrt(coefficient)],
    )
    unrestricted_x = sp.symbols("x_unrestricted", real=True)
    unrestricted_roots = sp.solve(
        sp.Eq(unrestricted_x, coefficient / unrestricted_x),
        unrestricted_x,
    )
    checks.check(
        "fresh omitted positivity mutation restores two real roots",
        unrestricted_roots
        == [-sp.sqrt(coefficient), sp.sqrt(coefficient)],
    )
    checks.check(
        "fresh source specialization is four pi",
        sp.sqrt(16 * sp.pi**2) == 4 * sp.pi,
    )
    checks.check(
        "fresh coefficient mutation moves fixed coordinate",
        sp.sqrt(25 * sp.pi**2) == 5 * sp.pi,
    )

    target = sp.symbols("target", positive=True)
    target_coefficient = target**2
    checks.check(
        "fresh arbitrary-target construction round trips",
        sp.simplify(target_coefficient / target - target) == 0,
    )
    checks.check(
        "fresh arbitrary-target construction is inverse inference",
        target_coefficient.has(target)
        and sp.diff(target_coefficient, target) != 0,
    )

    rho = sp.symbols("rho", positive=True)
    rescaled_x = rho * x
    rescaled_coefficient = rho**2 * coefficient
    rescaled_dual = sp.simplify(rescaled_coefficient / rescaled_x)
    checks.check(
        "fresh coordinate conjugation commutes",
        rescaled_dual == sp.simplify(rho * dual),
    )
    checks.check(
        "fresh fixed coordinate covariance",
        sp.sqrt(rescaled_coefficient) == rho * sp.sqrt(coefficient),
    )
    checks.check(
        "fresh wrong coefficient transformation fails",
        sp.simplify(coefficient / rescaled_x - rho * dual) != 0,
    )

    off_fixed_x = sp.Integer(2)
    off_fixed_coefficient = sp.Integer(9)
    off_fixed_dual = off_fixed_coefficient / off_fixed_x
    checks.check(
        "fresh off-fixed dual pair is constructive counterexample",
        off_fixed_dual == sp.Rational(9, 2)
        and off_fixed_coefficient / off_fixed_dual == off_fixed_x
        and off_fixed_x != sp.sqrt(off_fixed_coefficient),
    )

    checks.check(
        "fresh phase counterexample defeats unique phase selection",
        sp.exp(sp.I * 4 * sp.pi / 4) == -1
        and sp.exp(sp.I * 12 * sp.pi / 4) == -1,
    )

    b0, g2 = sp.symbols("b0 g2", positive=True)
    exponent = 8 * sp.pi**2 / (b0 * g2)
    transmuted_energy_ratio = sp.exp(-exponent)
    inverse_energy_length_ratio = sp.exp(exponent)
    checks.check(
        "fresh four-pi seven substitution is exact",
        sp.simplify(exponent.subs({b0: 7, g2: 4 * sp.pi}))
        == 2 * sp.pi / 7,
    )
    checks.check(
        "fresh energy and inverse-length orientations are reciprocal",
        sp.simplify(
            transmuted_energy_ratio * inverse_energy_length_ratio
        )
        == 1,
    )
    checks.check(
        "fresh AS6 audit finds reversed inverse-length label",
        "a_over_xi = sp.exp(-exponent_simpl)" in source_text,
    )
    checks.check(
        "fresh beta-coefficient audit finds hard-coded seven",
        "b0_val = 7" in source_text
        and sp.diff(exponent, b0) != 0,
    )

    checks.check(
        "fresh source audit finds no action-level construction",
        "lagrangian" not in source_text.lower()
        and "hamiltonian" not in source_text.lower()
        and "partition function" not in source_text.lower(),
    )
    checks.check(
        "fresh source audit finds imposed reciprocal coefficient",
        "dual_partner = 16 * sp.pi**2 / beta2" in source_text,
    )
    checks.check(
        "fresh source audit finds unsupported WZ3 physical analogy",
        "WZ3 topological=baryon" in source_text,
    )
    checks.check(
        "fresh source audit finds later self-correction",
        "framework does NOT sit there" in source_text,
    )
    checks.check(
        "fresh exact routes use no numpy integration",
        "import numpy" not in source_text
        and "np." + "trapz" not in source_text
        and "np." + "trapezoid" not in source_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
