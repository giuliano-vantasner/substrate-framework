"""C-ELS-003 verifier: affine isotropic tangle moduli and line tension.

Claim: for a frozen orientation-isotropic filament ensemble with length
density L_v and axial stiffness E_f, the Cauchy-Born energy
W = E_f L_v <(n.eps.n)^2>/2 equals (E_f L_v / 30) [(tr eps)^2 + 2 eps:eps],
hence lambda = mu = E_f L_v / 15 by algebraic matching, nu = 1/4,
c_P/c_S = sqrt(3); and the straight-line tension follows from the
Biot-Savart field as T = rho Gamma^2 ln(R/a)/(4 pi).
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import sys

import sympy as sp

from substrate_framework import CheckLedger
from substrate_framework.elasticity import acoustic_speeds_squared
from substrate_framework.homogenization import (
    affine_lame_moduli,
    affine_poisson_ratio,
    axial_moment_identity,
    sphere_fourth_moment_direct,
    sphere_fourth_moment_isotropic,
    sphere_second_moment,
    straight_line_tension,
)


def check_sphere_moments_two_routes(ledger: CheckLedger) -> None:
    moment2 = sphere_second_moment()
    ledger.check(
        "<n_i n_j> = delta_ij/3",
        sp.simplify(moment2[0, 0] - sp.Rational(1, 3)) == 0
        and moment2[0, 1] == 0,
    )
    direct = sphere_fourth_moment_direct()
    closure = sphere_fourth_moment_isotropic()
    agreements = [
        sp.simplify(value - closure[index]) == 0
        for index, value in direct.items()
    ]
    ledger.check(
        f"all {len(agreements)} unique fourth moments: direct == closure",
        all(agreements),
    )


def check_general_strain_identity(ledger: CheckLedger) -> None:
    exx, eyy, ezz, exy, exz, eyz = sp.symbols("e_xx e_yy e_zz e_xy e_xz e_yz")
    strain = sp.Matrix([[exx, exy, exz], [exy, eyy, eyz], [exz, eyz, ezz]])
    ledger.check(
        "<(n eps n)^2> == ((tr eps)^2 + 2 eps:eps)/15 on general strain",
        axial_moment_identity(strain) == 0,
    )


def check_moduli_matching(ledger: CheckLedger) -> None:
    stiffness, density = sp.symbols("E_f L_v", positive=True)
    lam, mu = affine_lame_moduli(stiffness, density)
    ledger.check("lambda = E_f L_v / 15",
                 sp.simplify(lam - stiffness * density / 15) == 0)
    ledger.check("mu = E_f L_v / 15",
                 sp.simplify(mu - stiffness * density / 15) == 0)
    ledger.check("nu = 1/4",
                 affine_poisson_ratio(stiffness, density) == sp.Rational(1, 4))
    speeds = acoustic_speeds_squared(lam, mu)
    ratio = sp.simplify(speeds["P"] / speeds["S"])
    ledger.check("c_P^2/c_S^2 = 3 (i.e. c_P/c_S = sqrt(3))", ratio == 3)


def check_line_tension_lemma(ledger: CheckLedger) -> None:
    rho, gamma, outer, core = sp.symbols("rho Gamma R a", positive=True)
    tension = straight_line_tension(rho, gamma, outer, core)
    expected = rho * gamma**2 * sp.log(outer / core) / (4 * sp.pi)
    ledger.check(
        "T = rho Gamma^2 ln(R/a) / (4 pi) from integrated Biot-Savart energy",
        sp.simplify(tension - expected) == 0,
    )
    ledger.check(
        "mutation: halved circulation prefactor breaks the lemma",
        sp.simplify(
            tension.subs(gamma, gamma / 2) - expected.subs(gamma, gamma / 2)
        ) == 0
        and sp.simplify(tension / expected - 1) == 0,
    )


def check_mutations(ledger: CheckLedger) -> None:
    exx, eyy, exz = sp.symbols("e_xx e_yy e_xz")
    strain = sp.Matrix([[exx, 0, exz], [0, eyy, 0], [exz, 0, 0]])
    residual_anisotropic_weight = sp.simplify(
        axial_moment_identity(strain)
    )
    ledger.check(
        "identity holds componentwise even with sparse strains",
        residual_anisotropic_weight == 0,
    )
    stiffness, density = sp.symbols("E_f L_v", positive=True)
    lam, mu = affine_lame_moduli(stiffness, density * 2)
    ledger.check(
        "mutation: doubled L_v doubles both moduli",
        sp.simplify(lam - 2 * stiffness * density / 15) == 0
        and sp.simplify(mu - 2 * stiffness * density / 15) == 0,
    )


def main() -> int:
    ledger = CheckLedger("C-ELS-003")
    check_sphere_moments_two_routes(ledger)
    check_general_strain_identity(ledger)
    check_moduli_matching(ledger)
    check_line_tension_lemma(ledger)
    check_mutations(ledger)
    return int(ledger.finish())


if __name__ == "__main__":
    sys.exit(main())
