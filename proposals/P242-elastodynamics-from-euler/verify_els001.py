"""C-ELS-001 verifier: exact filtered momentum balance.

Claim: for constant-density incompressible Euler, a homogeneous convolution
filter S commutes identically with every coordinate/time derivative; the
filtered balance

    d_t ubar_i + d_j(ubar_i ubar_j + Pi_ij) + (1/rho) d_i pbar - fbar_i = 0

closes exactly with Pi_ij := S(v_i v_j) - ubar_i ubar_j, and Pi is O(Delta^2)
in the field amplitude with exact coefficients on the polynomial class.
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import sys

import sympy as sp

from substrate_framework import CheckLedger
from substrate_framework.averaging import (
    commutation_residual,
    filter_direct_tophat,
    filter_polynomial,
    filtered_balance_residual,
    kernel_even_moments,
    microscopic_balance_residual,
    subfilter_flux,
)


def check_moment_conventions(ledger: CheckLedger) -> None:
    moments = kernel_even_moments("tophat", 2)
    ledger.check("tophat m_0 normalized", moments[0] == 1)
    ledger.check("tophat m_2 exact", moments[1] == sp.Rational(1, 12))
    ledger.check("tophat m_4 exact", moments[2] == sp.Rational(1, 80))


def check_series_equals_convolution(ledger: CheckLedger) -> None:
    x, width = sp.symbols("x Delta", positive=True)
    for polynomial in (x**2, x**3, x**4, 5 * x**3 - 2 * x):
        series = filter_polynomial(polynomial, x, width)
        direct = filter_direct_tophat(polynomial, x, width)
        degree = sp.degree(polynomial)
        ledger.check(
            f"moment series == direct integral (degree {degree})",
            sp.simplify(series - direct) == 0,
        )


def check_commutation_identity(ledger: CheckLedger) -> None:
    x, width = sp.symbols("x Delta", positive=True)
    residuals = [commutation_residual(x**d, x, width) for d in range(1, 6)]
    ledger.check(
        "[S, d/dx] == 0 on monomial basis degree 1..5",
        all(sp.simplify(residual) == 0 for residual in residuals),
    )


def build_rigid_rotation() -> dict:
    """Rigid rotation: an exact constant-density incompressible Euler flow."""

    x, y = sp.symbols("x y", positive=True)
    omega = sp.Symbol("omega_0", positive=True)
    rho = sp.Symbol("rho_0", positive=True)
    velocity = (omega * y, -omega * x)
    pressure = rho * omega**2 * (x**2 + y**2) / 2
    return {"velocity": velocity, "pressure": pressure, "rho": rho}


def check_exact_closure_on_euler_solution(ledger: CheckLedger) -> None:
    x, y, t, width = sp.symbols("x y t Delta", positive=True)
    fields = build_rigid_rotation()
    micro = microscopic_balance_residual(
        fields["velocity"], fields["pressure"], (0, 0),
        fields["rho"], (x, y), t,
    )
    ledger.check(
        "declared fields solve microscopic Euler exactly",
        all(sp.simplify(component) == 0 for component in micro),
    )
    filtered = filtered_balance_residual(
        fields["velocity"], fields["pressure"], (0, 0),
        fields["rho"], (x, y), t, width,
    )
    ledger.check(
        "filtered balance residual vanishes identically",
        all(sp.simplify(component) == 0 for component in filtered),
    )


def check_subfilter_flux_scaling(ledger: CheckLedger) -> None:
    x, y, t, width = sp.symbols("x y t Delta", positive=True)
    omega = sp.Symbol("omega_0", positive=True)
    flux = subfilter_flux((omega * y, -omega * x), (x, y), t, width)
    diagonal_exact = all(
        sp.simplify(flux[i, i] - omega**2 * width**2 / 12) == 0 for i in range(2)
    )
    ledger.check(
        "Pi quadratic in amplitude with exact Delta^2 coefficient",
        diagonal_exact,
    )
    ledger.check(
        "Pi off-diagonal vanishes for this symmetric class",
        sp.simplify(flux[0, 1]) == 0,
    )


def check_mutations(ledger: CheckLedger) -> None:
    x, y, t, width = sp.symbols("x y t Delta", positive=True)
    rho = sp.Symbol("rho_0", positive=True)

    def micro_residual(sign: int) -> list:
        omega = sp.Symbol("omega_0", positive=True)
        velocity = (omega * y, -omega * x)
        pressure = sign * rho * omega**2 * (x**2 + y**2) / 2
        return microscopic_balance_residual(
            velocity, pressure, (0, 0), rho, (x, y), t
        )

    mutated = micro_residual(-1)
    ledger.check(
        "mutation: flipped pressure sign breaks the Euler solution",
        any(sp.simplify(component) != 0 for component in mutated),
    )
    try:
        microscopic_balance_residual((x, 0), sp.Integer(0), (0, 0), rho, (x, y), t)
        raised = False
    except ValueError:
        raised = True
    ledger.check("mutation: divergent field rejected", raised)


def main() -> int:
    ledger = CheckLedger("C-ELS-001")
    check_moment_conventions(ledger)
    check_series_equals_convolution(ledger)
    check_commutation_identity(ledger)
    check_exact_closure_on_euler_solution(ledger)
    check_subfilter_flux_scaling(ledger)
    check_mutations(ledger)
    return int(ledger.finish())


if __name__ == "__main__":
    sys.exit(main())
