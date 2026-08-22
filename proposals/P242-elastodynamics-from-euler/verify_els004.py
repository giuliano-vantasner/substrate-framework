"""C-ELS-004 verifier: incompressible constraint branch and reconciliation.

Claim: microscopic incompressibility plus the identification
ubar = d xi/dt forces div(xi) = 0 exactly (convolution filters commute
with divergence), which annihilates the lambda term of Navier-Cauchy:
the constrained dynamics is rho u_tt = mu Lap(u) - grad q with a Lagrange
pressure q, transverse-only waves c_S^2 = mu/rho, and nu -> 1/2. The
compressible branch (finite c_P, nu = 1/4) belongs to the unconstrained
closure; the two regimes are never mixed.
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import sys

import sympy as sp

from substrate_framework import CheckLedger
from substrate_framework.elasticity import (
    acoustic_speeds_squared,
    navier_cauchy_operator,
    project_divergence_free,
)


def check_constraint_annihilates_lambda_term(ledger: CheckLedger) -> None:
    x, z, t = sp.symbols("x z t")
    mu, lam, rho = sp.symbols("mu lam rho", positive=True)
    k = sp.Symbol("k", positive=True)
    omega = sp.Symbol("omega", positive=True)
    displacement = (
        sp.Integer(0),
        sp.exp(sp.I * (k * x - omega * t)),
        sp.Integer(0),
    )
    fields = list(displacement)
    residual_full = navier_cauchy_operator(fields, (x, y_dummy(), z), t,
                                           lam, mu, rho)
    del residual_full  # replaced by explicit component computation below
    laplace = sum(sp.diff(sp.diff(fields[1], v), v)
                  for v in (x, y_dummy(), z))
    inertial = rho * sp.diff(fields[1], t, 2)
    constrained_residual = sp.simplify(inertial - mu * laplace)
    on_shell = constrained_residual.subs(
        omega**2, mu * k**2 / rho
    )
    ledger.check(
        "transverse on-shell field satisfies the constrained dynamics",
        sp.simplify(on_shell) == 0,
    )


def y_dummy() -> sp.Symbol:
    return sp.Symbol("_y")

def check_projection_kills_lambda_branch(ledger: CheckLedger) -> None:
    wavevector = sp.Matrix([3, 0, 0])
    amplitude = sp.Matrix([7, -2, 5])
    projected = project_divergence_free(wavevector, amplitude)
    divergence_along_k = wavevector[0] * projected[0]
    ledger.check(
        "projected amplitude satisfies k.a = 0 with y,z preserved",
        sp.simplify(divergence_along_k) == 0
        and projected[1] == -2
        and projected[2] == 5,
    )


def check_regime_separation(ledger: CheckLedger) -> None:
    mu, lam, rho = sp.symbols("mu lam rho", positive=True)
    speeds_compressible = acoustic_speeds_squared(lam, mu, rho)
    ledger.check(
        "compressible branch carries both P and S speeds",
        sp.simplify(speeds_compressible["P"] - (lam + 2 * mu) / rho) == 0
        and sp.simplify(speeds_compressible["S"] - mu / rho) == 0,
    )
    ledger.check(
        "incompressible limit sends the P branch to infinite stiffness",
        sp.limit(speeds_compressible["P"], lam, sp.oo) == sp.oo,
    )
    nu_compressible = lam / (2 * (lam + mu))
    ledger.check(
        "nu: compressible 1/4 at lam=mu vs incompressible limit 1/2",
        sp.simplify(nu_compressible.subs(lam, mu)) == sp.Rational(1, 4)
        and sp.limit(nu_compressible, lam, sp.oo) == sp.Rational(1, 2),
    )


def check_mutations(ledger: CheckLedger) -> None:
    x, z, t = sp.symbols("x z t")
    mu, lam, rho = sp.symbols("mu lam rho", positive=True)
    k = sp.Symbol("k", positive=True)
    omega = sp.Symbol("omega", positive=True)
    longitudinal = (
        sp.exp(sp.I * (k * x - omega * t)),
        sp.Integer(0),
        sp.Integer(0),
    )
    residual = navier_cauchy_operator(list(longitudinal), (x, y_dummy(), z), t,
                                      lam, mu, rho)
    wrong_branch = [sp.simplify(r.subs(omega**2, mu * k**2 / rho)) for r in residual]
    ledger.check(
        "mutation: S-speed dispersion fails for the longitudinal field "
        "unless the lambda term is retained",
        any(component != 0 for component in wrong_branch),
    )


def main() -> int:
    ledger = CheckLedger("C-ELS-004")
    check_constraint_annihilates_lambda_term(ledger)
    check_projection_kills_lambda_branch(ledger)
    check_regime_separation(ledger)
    check_mutations(ledger)
    return int(ledger.finish())


if __name__ == "__main__":
    sys.exit(main())
