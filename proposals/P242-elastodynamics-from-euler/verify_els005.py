"""C-ELS-005 verifier: the conditional emergence theorem, assembled.

Claim: for a declared frozen isotropic filament ensemble (line density L_v,
axial stiffness E_f > 0) satisfying the campaign premises, the long-
wavelength effective dynamics obtained through the ladder is exactly
isotropic elastodynamics with computed moduli lambda = mu = E_f L_v / 15
(compressible branch) or transverse-only c_S^2 = E_f L_v / (15 rho)
(incompressible branch). The chain runs end-to-end on canonical APIs:
ensemble premises -> affine homogenization -> Navier-Cauchy operator ->
acoustic speeds -> stability gates.
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
    strong_elliptic,
)
from substrate_framework.homogenization import (
    affine_lame_moduli,
    straight_line_tension,
)


def run_chain(ledger: CheckLedger, stiffness, density) -> tuple:
    lam, mu = affine_lame_moduli(stiffness, density)
    ledger.check(
        "chain output: positive computed moduli for positive premises",
        sp.simplify(lam - stiffness * density / 15) == 0
        and sp.simplify(mu - stiffness * density / 15) == 0,
    )
    return lam, mu


def check_end_to_end_symbolic(ledger: CheckLedger) -> None:
    stiffness, density = sp.symbols("E_f L_v", positive=True)
    rho = sp.Symbol("rho", positive=True)
    lam, mu = run_chain(ledger, stiffness, density)
    speeds = acoustic_speeds_squared(lam, mu, rho)
    ledger.check(
        "P speed squared = E_f L_v / (5 rho)",
        sp.simplify(speeds["P"] - stiffness * density / (5 * rho)) == 0,
    )
    ledger.check(
        "S speed squared = E_f L_v / (15 rho)",
        sp.simplify(speeds["S"] - stiffness * density / (15 * rho)) == 0,
    )


def check_numeric_instance_on_shell(ledger: CheckLedger) -> None:
    x, y, z, t = sp.symbols("x y z t")
    k = sp.Rational(3, 2)
    omega_p = sp.sqrt(sp.Rational(27, 10))
    displacement = [
        sp.exp(sp.I * (k * x - omega_p * t)),
        sp.Integer(0),
        sp.Integer(0),
    ]
    residual = navier_cauchy_operator(displacement, (x, y, z), t,
                                      sp.Rational(2, 5), sp.Rational(2, 5),
                                      sp.Integer(1))
    ledger.check(
        "numeric instance: longitudinal wave is exactly on shell",
        all(sp.simplify(component) == 0 for component in residual),
    )


def check_degenerate_limits(ledger: CheckLedger) -> None:
    stiffness, density = sp.symbols("E_f L_v", positive=True)
    zero_density_lam, zero_density_mu = affine_lame_moduli(stiffness, 0)
    ledger.check(
        "mutation: L_v = 0 collapses the medium (no elasticity)",
        zero_density_lam == 0 and zero_density_mu == 0
        and not strong_elliptic(zero_density_lam, zero_density_mu),
    )
    try:
        run_chain(ledger, sp.Integer(-2), sp.Integer(3))
        rejected = False
    except ValueError:
        rejected = True
    ledger.check(
        "mutation: negative axial stiffness cannot define a stable medium",
        rejected,
    )


def check_interpretive_layer_boundary(ledger: CheckLedger) -> None:
    rho, gamma, outer, core = sp.symbols("rho Gamma R a", positive=True)
    tension = straight_line_tension(rho, gamma, outer, core)
    ledger.check(
        "line-tension scale available as declared input to the premises",
        sp.simplify(tension - rho * gamma**2 * sp.log(outer / core) / (4 * sp.pi))
        == 0,
    )


def main() -> int:
    ledger = CheckLedger("C-ELS-005")
    check_end_to_end_symbolic(ledger)
    check_numeric_instance_on_shell(ledger)
    check_degenerate_limits(ledger)
    check_interpretive_layer_boundary(ledger)
    return int(ledger.finish())


if __name__ == "__main__":
    sys.exit(main())
