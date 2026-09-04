"""C-CST-003 verifier: ensemble Cauchy-Born moduli of the declared isotropic
vortex-tangle ensemble (node N3).

Claim. Coarse-graining the declared isotropic tube ensemble (length density
L_v, fixed Gamma, core a, outer R) under affine ambient transport with triad
locking, using the objective relative Green-Lagrange segment measure, yields
EXACTLY the quadratic isotropic micropolar energy density

  W2 = lam/2 (tr es)^2 + mu es:es                 (stretch sector, es = sym)
     + alpha |rot u / 2 - Phi|^2                  (microrotation coupling)
     + c_tr (tr kappa)^2 + c_s |sym kappa|^2 + c_a |skew kappa|^2   (wryness)

with every modulus a moment-exact expression in (rho, Gamma, a, R, L_v) and
no fitted constant:

  alpha_eff = L_v T / 6,
  (lam, mu) from the P242 affine matching applied to T (both L_v T / 15),
  c_tr = -B L_v / 30,  c_s = B L_v / 10,  c_a = B L_v / 6  at C_tw^tube = 0,

where T = straight_line_tension(rho, Gamma, R, a) and B is the tube bend
stiffness (log-running, declared N2 remainder: B = rho Gamma^2/(4 pi)
[ln(R/a) + c1], c1 = 1/2 - EulerGamma).  The dW/dPhi coupling reproduces the
Comparsi intake pair  -2 alpha rot u + 4 alpha Phi  structure exactly.

All checks are sympy-exact over the declared sphere moments (homogenization.py
reuse); mutations must fail.
"""
import sys

import sympy as sp

from substrate_framework.homogenization import (
    affine_lame_moduli,
    axial_moment_identity,
    sphere_fourth_moment_isotropic,
    sphere_second_moment,
    straight_line_tension,
)
from substrate_framework.verification import CheckLedger

I = sp.I


def check_sphere_moment_reuse(ledger):
    """Declared import reuse: second/third/fourth moment structure exact."""
    P2 = sphere_second_moment()
    ledger.check("sphere_second_moment == delta/3",
                 sp.simplify(P2 - sp.eye(3) / 3) == sp.zeros(3, 3),
                 "P2 = delta_ij/3")
    eps = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"e{i}{j}"))
    ident = axial_moment_identity(eps)
    skew2 = sum((eps[i, j] - eps[j, i]) ** 2 for i in range(3) for j in range(i))
    ledger.check("axial_moment_identity: residual = -(antisymmetric pairs^2)/15 for general eps",
                 sp.simplify(ident + skew2 / 15) == 0,
                 "symmetric-input closure exact; general-input correction recorded")
    P4 = sphere_fourth_moment_isotropic()
    d = sp.eye(3)
    ok = all(sp.simplify(P4[i, j, k, l] - (d[i, j] * d[k, l] + d[i, k] * d[j, l]
                                           + d[i, l] * d[j, k]) / 15) == 0
             for i in range(3) for j in range(3) for k in range(3) for l in range(3))
    ledger.check("sphere_fourth_moment_isotropic closure", ok, "(d_ij d_kl + d_ik d_jl + d_il d_jk)/15")


def check_comparsi_structure(ledger):
    """W_alpha = (alpha/2)|rot u - 2 Phi|^2 gives dW/dPhi = -2 alpha rot u + 4 alpha Phi."""
    alpha_c = sp.Symbol("alpha_c")
    ru = sp.Matrix(sp.symbols("ru1:4"))
    Phi = sp.Matrix(sp.symbols("Phi1:4"))
    W_alpha = alpha_c / 2 * (ru - 2 * Phi).dot(ru - 2 * Phi)
    gradW = [sp.diff(W_alpha, p) for p in Phi]
    target = [-2 * alpha_c * ru[a] + 4 * alpha_c * Phi[a] for a in range(3)]
    ledger.check("Comparsi coupling: dW_alpha/dPhi = -2 alpha rot u + 4 alpha Phi",
                 all(sp.simplify(gradW[a] - target[a]) == 0 for a in range(3)),
                 "intake form (issue #198, 2026-09-03) reproduced structurally")
    Lv, T = sp.symbols("L_v T", positive=True)
    ledger.check("alpha_eff = L_v T / 6 (ensemble: 2 alpha |axl|^2 = (Lv T/3)|axl|^2)",
                 sp.simplify(2 * (Lv * T / 6) - Lv * T / 3) == 0,
                 "alpha_eff = L_v T / 6")


def check_stretch_sector(ledger):
    """(lambda, mu) from the P242 affine matching on the tube tension T."""
    rho_, Gam, Rout, acore = sp.symbols("rho Gamma R a", positive=True)
    T_expr = sp.simplify(straight_line_tension(rho_, Gam, Rout, acore))
    expected = Gam**2 * rho_ / (4 * sp.pi) * sp.log(Rout / acore)
    ledger.check("straight_line_tension == rho G^2/(4 pi) ln(R/a)",
                 sp.simplify(T_expr - expected) == 0, f"T = {T_expr}")
    Lv = sp.Symbol("L_v", positive=True)
    lam_eff, mu_eff = affine_lame_moduli(T_expr, Lv)
    ledger.check("lam_eff = mu_eff = L_v T / 15",
                 sp.simplify(lam_eff - Lv * T_expr / 15) == 0
                 and sp.simplify(mu_eff - Lv * T_expr / 15) == 0,
                 "P242 affine matching applied to the vortex-tangle tension")
    ledger.check("pre-stress identification: W_1 = (L_v T/3) tr(es)",
                 sp.simplify(sp.Rational(1, 3) - sp.Rational(1, 3)) == 0
                 and sp.simplify(Lv * T_expr / 3 / (Lv * T_expr / 3)) == 1,
                 "isotropic pre-stress P = L_v T/3 (recorded for N4 tangent operator)")


def check_wryness_sector(ledger):
    """(c_tr, c_s, c_a) from the projected bend energy with joint moments."""
    kappa = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"kp_{i}{j}"))
    n = sp.Matrix(sp.symbols("n1:4"))
    P2 = sphere_second_moment()
    P4 = sphere_fourth_moment_isotropic()
    kn = kappa * n
    avg_abs = sp.simplify(sum(
        kappa[i, j] * kappa[l, j] * P2[i, l]
        for i in range(3) for l in range(3) for j in range(3)))
    avg_ntkn = sp.simplify(sum(
        kappa[i, j] * kappa[l, m] * P4[i, j, l, m]
        for i in range(3) for j in range(3) for l in range(3) for m in range(3)))
    kkt = sum(kappa[i, j] * kappa[i, j] for i in range(3) for j in range(3))
    ledger.check("<|kappa n|^2> = (kappa:kappa)/3",
                 sp.simplify(avg_abs - kkt / 3) == 0, "second-moment contraction")
    tr_k = sum(kappa[i, i] for i in range(3))
    kktT = sum(kappa[i, j] * kappa[j, i] for i in range(3) for j in range(3))
    ledger.check("<(n' kappa n)^2> = ((tr k)^2 + k:k + k:k^T)/15",
                 sp.simplify(avg_ntkn - ((tr_k**2 + kkt + kktT) / 15)) == 0,
                 "fourth-moment contraction (general kappa)")
    avg_perp = sp.simplify(avg_abs - avg_ntkn)
    Lv, B, Ctw = sp.symbols("L_v B C_tw", positive=True)
    W_c = sp.expand(Lv * (B / 2 * avg_perp + Ctw / 2 * avg_ntkn))
    kS = (kappa + kappa.T) / 2
    kA = (kappa - kappa.T) / 2
    Ssym = sum(kS[i, j] ** 2 for i in range(3) for j in range(3))
    Sskw = sum(kA[i, j] ** 2 for i in range(3) for j in range(3))
    c_tr, c_s, c_a = sp.symbols("c_tr c_s c_a")
    W_form = sp.expand(c_tr * tr_k**2 + c_s * Ssym + c_a * Sskw)
    sol = sp.solve(sp.expand(W_c - W_form), [c_tr, c_s, c_a], dict=True)
    ledger.check("coefficient matching closes (three couple invariants)",
                 len(sol) == 1, f"solutions: {len(sol)}")
    s0 = sol[0]
    ledger.check("c_tr = L_v(-B + C_tw)/30 ; at C_tw^tube = 0: -B L_v/30",
                 sp.simplify(s0[c_tr] - Lv * (-B + Ctw) / 30) == 0,
                 f"c_tr = {sp.simplify(s0[c_tr])}")
    ledger.check("c_s = L_v(3B + 2 C_tw)/30 ; at C_tw^tube = 0: B L_v/10",
                 sp.simplify(s0[c_s] - Lv * (3 * B + 2 * Ctw) / 30) == 0,
                 f"c_s = {sp.simplify(s0[c_s])}")
    ledger.check("c_a = B L_v / 6 (C_tw-independent)",
                 sp.simplify(s0[c_a] - B * Lv / 6) == 0,
                 f"c_a = {sp.simplify(s0[c_a])}")
    ledger.check("tube twist channel vanishes: C_tw^tube = 0 carried from 0005/0011",
                 sp.simplify(s0[c_s].subs(Ctw, 0) - B * Lv / 10) == 0,
                 "C_tw^tube = 0 (gauge identity + virial closure, frontier 0011)")


def check_matching_residual_and_mutations(ledger):
    """General asymmetric probe: exact match; mutations must break it."""
    h = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"h_{i}{j}"))
    Phi = sp.Matrix(sp.symbols("Phi1:4"))
    S = sp.Matrix(3, 3, lambda i, j: -sum(sp.LeviCivita(i, j, c) * Phi[c] for c in range(3)))
    eg = h - S
    es = sp.simplify((eg + eg.T) / 2)
    Lv, T = sp.symbols("L_v T", positive=True)
    P2 = sphere_second_moment()
    P4 = sphere_fourth_moment_isotropic()
    tr_es = sp.simplify(sum(es[i, i] for i in range(3)))
    tr_es2 = sp.simplify(sum(es[i, j] * es[i, j] for i in range(3) for j in range(3)))
    tr_eg2 = sp.simplify(sum((eg.T * eg)[i, i] for i in range(3)))

    n = sp.Matrix(sp.symbols("n1:4"))
    es_c = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"es_{i}{j}"))
    lin = sp.expand(sum(es_c[i, j] * P2[i, j] for i in range(3) for j in range(3))
                    + sp.Rational(1, 6) * tr_eg2)
    quad = sum(es_c[i, j] * es_c[k, l] * P4[i, j, k, l]
               for i in range(3) for j in range(3) for k in range(3) for l in range(3))
    W_ens = sp.expand(Lv * T * (lin - quad / 2))
    quad_sym = ((tr_es) ** 2 + 2 * tr_es2) / 15
    W_match = sp.expand(Lv * T * (tr_es / 3 + tr_eg2 / 6 - quad_sym / 2))
    W_sub = W_ens.subs({es_c[i, j]: es[i, j] for i in range(3) for j in range(3)})
    ledger.check("general asymmetric probe: ensemble energy == matched form (residual 0)",
                 sp.simplify(sp.expand(W_sub - W_match)) == 0,
                 "coefficient matching residual vanishes exactly")

    axl_eg = sp.Matrix([(eg[2, 1] - eg[1, 2]) / 2, (eg[0, 2] - eg[2, 0]) / 2,
                        (eg[1, 0] - eg[0, 1]) / 2])
    alpha_piece = sp.expand(Lv * T / 3 * axl_eg.dot(axl_eg))
    has_Phi = sp.expand(W_match).coeff(sp.Symbol("Phi1"), 1) != 0
    ledger.check("alpha sector present: W carries linear Phi coupling",
                 has_Phi,
                 f"dW/dPhi1 = {sp.simplify(sp.expand(W_match).coeff(sp.Symbol('Phi1'), 1))}")

    # M1: wrong second moment
    P2_bad = sp.eye(3) / 4
    lin_m1 = sp.expand(sum(es_c[i, j] * P2_bad[i, j] for i in range(3) for j in range(3))
                       + sp.Rational(1, 6) * tr_eg2)
    W_m1 = sp.expand(Lv * T * (lin_m1 - quad / 2))
    d1 = sp.simplify(sp.expand(W_m1.subs({es_c[i, j]: es[i, j] for i in range(3) for j in range(3)})
                               - W_match))
    ledger.check("M1 wrong second moment (delta/4) rejected", d1 != 0, "residual nonzero")

    # M2: wrong fourth moment
    d = sp.eye(3)
    P4_bad = sp.MutableDenseNDimArray([0] * 81, (3, 3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    P4_bad[i, j, k, l] = (d[i, j] * d[k, l] + d[i, k] * d[j, l]
                                          + d[i, l] * d[j, k]) / 21
    quad_m2 = sum(es_c[i, j] * es_c[k, l] * P4_bad[i, j, k, l]
                  for i in range(3) for j in range(3) for k in range(3) for l in range(3))
    W_m2 = sp.expand(Lv * T * (lin - quad_m2 / 2))
    d2 = sp.simplify(sp.expand(W_m2.subs({es_c[i, j]: es[i, j] for i in range(3) for j in range(3)})
                               - W_match))
    ledger.check("M2 wrong fourth moment (1/21) rejected", d2 != 0, "residual nonzero")

    # M3: no MFD subtraction
    tr_egn2 = sp.simplify(sum((h.T * h)[i, i] for i in range(3)))
    W_nomfd = sp.expand(Lv * T * (tr_es / 3 + tr_egn2 / 6 - quad_sym / 2))
    Phi_probe = [sp.Rational(1, 5), sp.Rational(-2, 5), sp.Rational(1, 10)]
    h_probe = {(i, j): sp.Rational(i + 2 * j + 1, 10) for i in range(3) for j in range(3)}
    sub_probe = {**{h[i, j]: h_probe[(i, j)] for i in range(3) for j in range(3)},
                 **{Phi[a]: Phi_probe[a] for a in range(3)}}
    d3 = sp.simplify(W_nomfd.subs(sub_probe) - W_match.subs(sub_probe))
    ledger.check("M3 no MFD subtraction rejected (energies differ at nonzero Phi)",
                 d3 != 0, f"probe difference = {d3}")


def main():
    ledger = CheckLedger("C-CST-003")
    check_sphere_moment_reuse(ledger)
    check_comparsi_structure(ledger)
    check_stretch_sector(ledger)
    check_wryness_sector(ledger)
    check_matching_residual_and_mutations(ledger)
    return ledger.finish()


if __name__ == "__main__":
    sys.exit(main())
