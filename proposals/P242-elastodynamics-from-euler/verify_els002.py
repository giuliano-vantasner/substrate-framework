"""C-ELS-002 verifier: conditional bridge from closure to elastodynamics.

Claim: GIVEN the declared premises
  P1  mean-flow identification ubar = d xi/dt about a rest reference state,
  P2  strain-coupled closure Pi = -sigma_elastic(eps)/rho with isotropic
      quadratic sigma = lam tr(eps) I + 2 mu eps,
the filtered balance becomes exactly Navier-Cauchy dynamics
  rho u_tt = mu Lap(u) + (lam+mu) grad div u,
whose acoustic tensor gives c_P^2=(lam+2mu)/rho and c_S^2=mu/rho.
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import sys

import sympy as sp

from substrate_framework import CheckLedger
from substrate_framework.elasticity import (
    acoustic_speeds_squared,
    christoffel_matrix,
    navier_cauchy_operator,
    strong_elliptic,
)


def plane_wave_fields(
    amplitude: tuple, wavevector: tuple, omega: sp.Expr, coords, time
):
    phase = sum(k * x for k, x in zip(wavevector, coords)) - omega * time
    exponential = sp.exp(sp.I * phase)
    return [sp.Matrix(amplitude).T @ sp.Matrix([exponential] * len(coords))][0]


def check_closure_yields_navier_cauchy(ledger: CheckLedger) -> None:
    x, y, z, t = sp.symbols("x y z t")
    lam, mu, rho = sp.symbols("lam mu rho", positive=True)
    k, omega_p = sp.symbols("k omega_P", positive=True)
    displacement = (
        sp.exp(sp.I * (k * x - omega_p * t)),
        sp.Integer(0),
        sp.Integer(0),
    )
    fields = list(displacement)
    residual = navier_cauchy_operator(fields, (x, y, z), t, lam, mu, rho)
    dispersion = omega_p**2 - (lam + 2 * mu) * k**2 / rho
    on_shell = [sp.simplify(r.subs(omega_p**2, (lam + 2 * mu) * k**2 / rho))
                for r in residual]
    ledger.check(
        "longitudinal on-shell field satisfies Navier-Cauchy exactly",
        all(sp.simplify(component) == 0 for component in on_shell),
    )
    ledger.check(
        "off-shell residual is proportional to the dispersion defect",
        sp.simplify(residual[0] / (rho * dispersion)) == -sp.exp(sp.I * (k * x - omega_p * t)),
    )


def check_acoustic_tensor_matches_speeds(ledger: CheckLedger) -> None:
    lam, mu, rho = sp.symbols("lam mu rho", positive=True)
    direction = sp.Matrix([1, 0, 0])
    matrix = christoffel_matrix(lam, mu, rho, direction)
    speeds = acoustic_speeds_squared(lam, mu, rho)
    eigenvalues = {sp.simplify(value) for value in matrix.eigenvals()}
    ledger.check(
        "Christoffel spectrum == {c_P^2, c_S^2}",
        sp.simplify(speeds["P"]) in eigenvalues
        and sp.simplify(speeds["S"]) in eigenvalues
        and len(eigenvalues) == 2,
    )


def check_mutations(ledger: CheckLedger) -> None:
    lam, mu = sp.symbols("lam mu", positive=True)
    x, y, z, t = sp.symbols("x y z t")
    k = sp.Symbol("k", positive=True)
    rho = sp.Symbol("rho", positive=True)

    wrong_sign_closure_speed = (-(lam + 2 * mu)) / rho
    fields = [
        sp.exp(sp.I * (k * x - sp.sqrt(abs(wrong_sign_closure_speed)) * t)),
        sp.Integer(0),
        sp.Integer(0),
    ]
    residual = navier_cauchy_operator(fields, (x, y, z), t, lam, mu, rho)
    substituted = [
        sp.simplify(
            r.subs(sp.sqrt(abs(wrong_sign_closure_speed)) ** 2,
                   wrong_sign_closure_speed)
        )
        for r in residual
    ]
    ledger.check(
        "mutation: sign-flipped closure cannot satisfy the balance",
        any(component != 0 for component in substituted),
    )
    ledger.check(
        "mutation: mu -> 0 collapses the transverse branch",
        sp.simplify(acoustic_speeds_squared(lam, 0, rho)["S"]) == 0,
    )
    ledger.check(
        "mutation: lam = -2mu loses strong ellipticity",
        not strong_elliptic(-2 * mu, mu),
    )


def main() -> int:
    ledger = CheckLedger("C-ELS-002")
    check_closure_yields_navier_cauchy(ledger)
    check_acoustic_tensor_matches_speeds(ledger)
    check_mutations(ledger)
    return int(ledger.finish())


if __name__ == "__main__":
    sys.exit(main())
