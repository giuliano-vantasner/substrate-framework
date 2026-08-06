"""Fresh exact rederivation of the MK1 matching and identifiability ceiling."""

from __future__ import annotations

from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    checks = CheckLedger("P214-INDEPENDENT")

    pion, F, q, K, mass, mu = sp.symbols(
        "pi F q K m mu",
        positive=True,
    )
    potential = mu**2 * (1 - sp.cos(q * pion / F))
    curvature = sp.diff(potential, pion, 2).subs(pion, 0)
    generalized_mass = sp.simplify(curvature / K)
    solution = sp.solve(sp.Eq(generalized_mass, mass**2), mu)
    checks.check(
        "direct Hessian derivation gives the positive covariant matching relation",
        generalized_mass == mu**2 * q**2 / (F**2 * K)
        and solution == [F * sp.sqrt(K) * mass / q],
    )
    checks.check(
        "the source coordinate specialization is conditional rather than absolute",
        sp.simplify(solution[0].subs({q: 2, K: 1}) - mass * F / 2) == 0
        and sp.simplify(solution[0].subs({q: 1, K: sp.Rational(1, 4)}) - mass * F / 2)
        == 0,
    )

    alpha, derivative = sp.symbols("alpha dpi", positive=True)
    sigma3 = sp.diag(1, -1)
    angle = sp.Symbol("theta", real=True)
    identity = sp.eye(2)
    dU_dangle = -sp.sin(angle) * identity + sp.I * sp.cos(angle) * sigma3
    trace_metric = sp.simplify(sp.trace(dU_dangle * dU_dangle.conjugate().T))
    anw_density = sp.simplify(F**2 * trace_metric * (alpha * derivative / F) ** 2 / 16)
    scalar_K = sp.simplify(2 * anw_density / derivative**2)
    checks.check(
        "fresh ANW trace computation gives K=alpha squared over four",
        trace_metric == 2 and scalar_K == alpha**2 / 4,
    )
    checks.check(
        "canonical target K=1 selects positive alpha=2 only after that target is declared",
        sp.solve(sp.Eq(scalar_K, 1), alpha) == [2],
    )

    trace_prefactor = mass**2 * F**2 / 8
    trace_potential = 2 * trace_prefactor * (1 - sp.cos(alpha * pion / F))
    trace_curvature = sp.diff(trace_potential, pion, 2).subs(pion, 0)
    trace_mass = sp.simplify(trace_curvature / scalar_K.subs(derivative, 1))
    checks.check(
        "matched trace potential and kinetic metric cancel coordinate normalization",
        sp.simplify(trace_mass - mass**2) == 0,
    )

    y = sp.Symbol("y", nonnegative=True)
    beta_integral = sp.integrate(sp.sin(y) ** 3 * sp.cos(y) ** 2, (y, 0, sp.pi / 2))
    target_integral = sp.simplify(32 * sp.pi * sp.sqrt(2) * beta_integral)
    target_average = sp.simplify(target_integral / (2 * sp.pi**2))
    checks.check(
        "half-angle beta route independently gives the one-cosine target average",
        beta_integral == sp.Rational(2, 15)
        and target_average == 32 * sp.sqrt(2) / (15 * sp.pi),
    )

    e = sp.Symbol("e", positive=True)
    length = 2 / (e * F)
    coefficient = 4 * e * mu**2 * length**3 / F
    tail = sp.simplify(sp.sqrt(coefficient / 2) / length)
    checks.check(
        "fresh radial simplification makes the alleged independent route explicit",
        tail == 2 * mu / F,
    )
    checks.check(
        "tail equality and curvature equality have identical positive solution sets",
        sp.solve(sp.Eq(tail, mass), mu)
        == sp.solve(sp.Eq(generalized_mass.subs({q: 2, K: 1}), mass**2), mu),
    )

    medium_inertia, medium_onsite, rho = sp.symbols(
        "lambda_medium mu_medium rho",
        positive=True,
    )
    gap = sp.sqrt(medium_onsite / medium_inertia)
    scaled_gap = sp.sqrt((rho * medium_onsite) / (rho * medium_inertia))
    checks.check(
        "medium common-scale orbit preserves the exact gap ratio",
        sp.simplify(scaled_gap - gap) == 0,
    )
    F_a = sp.Symbol("F_a", positive=True)
    two_candidate_couplings = (gap * F_a / 2, gap * (3 * F_a) / 2)
    checks.check(
        "the same accepted medium gap permits distinct BPS matches without a decay-scale map",
        sp.simplify(two_candidate_couplings[1] - 3 * two_candidate_couplings[0]) == 0
        and sp.simplify(two_candidate_couplings[1] - two_candidate_couplings[0]) != 0,
    )

    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())
    claims = {claim["id"]: claim for claim in registry["claims"]}
    checks.check(
        "accepted authority keeps every cross-sector identification conditional or absent",
        "No accepted physical map" in " ".join(claims["C-BRK-001"]["assumptions"])
        and "not a coefficient derived" in " ".join(claims["C-CHI-002"]["assumptions"])
        and "does not establish" in claims["C-BPS-001"]["statement"]
        and "does not derive a material" in claims["C-MED-003"]["statement"],
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
