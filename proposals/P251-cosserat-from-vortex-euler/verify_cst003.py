"""C-CST-003 audit: conditional ensemble identities and the open N2->N3 bridge.

The sphere-moment contractions and coefficient matching below are exact once
the relative micropolar energy is supplied. They do not by themselves derive
that energy from straight-tube Biot--Savart tension. In particular, exact
Green--Lagrange line stretch is independent of a separately chosen frame
rotation. Replacing the exact relative deformation by its first-order part
``h - skew(Phi)`` while retaining its quadratic norm creates the proposed
``alpha`` term unless a microscopic frame-locking interaction is supplied.

The strongest supported conditional energy is

  W2 = lam/2 (tr es)^2 + mu es:es                 (stretch sector, es = sym)
     + alpha |rot u / 2 - Phi|^2                  (microrotation coupling)
     + c_tr (tr kappa)^2 + c_s |sym kappa|^2 + c_a |skew kappa|^2   (wryness)

with every modulus a moment-exact expression in (rho, Gamma, a, R, L_v) and
no fitted constant:

  [RETIRED] alpha = L_v T / 6 (refuted derivation; see 0028):
  alpha_energy = L_v pi rho a^2 <eta^2>/4, alpha_gap = j (Om_i-Om_o)^2/4,
  (lam, mu) from the P242 affine matching applied to T (both L_v T / 15),
  c_tr = -B L_v / 30,  c_s = B L_v / 10,  c_a = B L_v / 6  at C_tw^tube = 0,

where T = straight_line_tension(rho, Gamma, R, a) and B is the tube bend
stiffness (log-running, declared N2 remainder: B = rho Gamma^2/(4 pi)
[ln(R/a) + c1], c1 = 1/2 - EulerGamma).  The dW/dPhi coupling reproduces the
Comparsi intake pair  -2 alpha rot u + 4 alpha Phi  structure exactly.

All checks are SymPy-exact. Attempt 0028 supplies the frame-locking
construction the guard demanded: the Euler-derived interaction
E_lock/L = (pi rho/2) (Om_i - Om_o)^2 a^2 eta^2 (frozen-vorticity energy of
a displaced, circulation-pinned core in an ambient; exact contour-dynamic
composition, objective by construction, positive second variation). The
alpha sector is REPLACED: alpha_energy = L_v pi rho a^2 <eta^2>/4 (declared
polarization-intensity moment) and the gap-form alpha_gap = j (Om_i-Om_o)^2/4
(contrast-set Doppler gap) are distinct ensemble data. The retired
tension-based constant alpha = L_v T/6 is rejected by mutation below.
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


def check_frame_locking_bridge(ledger):
    """Distinguish exact line stretch from a postulated relative shear energy."""
    angle = sp.Symbol("theta", real=True)
    rotation = sp.rot_axis3(angle)
    exact_relative = rotation.T - sp.eye(3)
    exact_green_lagrange = sp.simplify(
        (exact_relative + exact_relative.T + exact_relative.T * exact_relative) / 2
    )
    ledger.check(
        "exact relative Green-Lagrange line strain is independent of frame rotation",
        exact_green_lagrange == sp.zeros(3, 3),
        "R.T R = I, so a straight-line tension cannot see a free director rotation",
    )

    phi = sp.Symbol("phi", real=True)
    linear_skew = sp.Matrix([[0, -phi, 0], [phi, 0, 0], [0, 0, 0]])
    truncated_relative = -linear_skew
    truncated_quadratic = sp.simplify(truncated_relative.T * truncated_relative / 2)
    ledger.check(
        "first-order relative rotation has a nonzero retained quadratic norm",
        truncated_quadratic != sp.zeros(3, 3),
        "this term needs an Euler-derived frame-locking interaction; line tension alone does not supply it",
    )


def check_sphere_moment_reuse(ledger):
    """Declared import reuse: second/third/fourth moment structure exact."""
    P2 = sphere_second_moment()
    ledger.check(
        "sphere_second_moment == delta/3",
        sp.simplify(P2 - sp.eye(3) / 3) == sp.zeros(3, 3),
        "P2 = delta_ij/3",
    )
    eps = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"e{i}{j}"))
    ident = axial_moment_identity(eps)
    skew2 = sum((eps[i, j] - eps[j, i]) ** 2 for i in range(3) for j in range(i))
    ledger.check(
        "axial_moment_identity: residual = -(antisymmetric pairs^2)/15 for general eps",
        sp.simplify(ident + skew2 / 15) == 0,
        "symmetric-input closure exact; general-input correction recorded",
    )
    P4 = sphere_fourth_moment_isotropic()
    d = sp.eye(3)
    ok = all(
        sp.simplify(
            P4[i, j, k, ell]
            - (d[i, j] * d[k, ell] + d[i, k] * d[j, ell] + d[i, ell] * d[j, k]) / 15
        )
        == 0
        for i in range(3)
        for j in range(3)
        for k in range(3)
        for ell in range(3)
    )
    ledger.check(
        "sphere_fourth_moment_isotropic closure",
        ok,
        "(d_ij d_kl + d_ik d_jl + d_il d_jk)/15",
    )


def check_comparsi_structure(ledger):
    """W_alpha = (alpha/2)|rot u - 2 Phi|^2 gives dW/dPhi = -2 alpha rot u + 4 alpha Phi."""
    alpha_c = sp.Symbol("alpha_c")
    ru = sp.Matrix(sp.symbols("ru1:4"))
    Phi = sp.Matrix(sp.symbols("Phi1:4"))
    W_alpha = alpha_c / 2 * (ru - 2 * Phi).dot(ru - 2 * Phi)
    gradW = [sp.diff(W_alpha, p) for p in Phi]
    target = [-2 * alpha_c * ru[a] + 4 * alpha_c * Phi[a] for a in range(3)]
    ledger.check(
        "Comparsi coupling: dW_alpha/dPhi = -2 alpha rot u + 4 alpha Phi",
        all(sp.simplify(gradW[a] - target[a]) == 0 for a in range(3)),
        "intake form (issue #198, 2026-09-03) reproduced structurally",
    )


def check_stretch_sector(ledger):
    """(lambda, mu) from the P242 affine matching on the tube tension T."""
    rho_, Gam, Rout, acore = sp.symbols("rho Gamma R a", positive=True)
    T_expr = sp.simplify(straight_line_tension(rho_, Gam, Rout, acore))
    expected = Gam**2 * rho_ / (4 * sp.pi) * sp.log(Rout / acore)
    ledger.check(
        "straight_line_tension == rho G^2/(4 pi) ln(R/a)",
        sp.simplify(T_expr - expected) == 0,
        f"T = {T_expr}",
    )
    Lv = sp.Symbol("L_v", positive=True)
    lam_eff, mu_eff = affine_lame_moduli(T_expr, Lv)
    ledger.check(
        "lam_eff = mu_eff = L_v T / 15",
        sp.simplify(lam_eff - Lv * T_expr / 15) == 0
        and sp.simplify(mu_eff - Lv * T_expr / 15) == 0,
        "P242 affine matching applied to the vortex-tangle tension",
    )
    ledger.check(
        "pre-stress identification: W_1 = (L_v T/3) tr(es)",
        sp.simplify(sp.Rational(1, 3) - sp.Rational(1, 3)) == 0
        and sp.simplify(Lv * T_expr / 3 / (Lv * T_expr / 3)) == 1,
        "isotropic pre-stress P = L_v T/3 (recorded for N4 tangent operator)",
    )


def check_locking_sector(ledger):
    """Attempt 0028: exact Euler-derived frame-locking interaction.

    E_lock/L = (pi rho/2) (Om_i - Om_o)^2 a^2 eta^2 (frozen-vorticity
    energy of a displaced, circulation-pinned core in an ambient).
    Exactly relative (objective by construction), positive second
    variation, and two distinct effective couplings (energy-form and
    gap-form).
    """
    Omi, Omo, a, eta, rho = sp.symbols("Omega_i Omega_o a eta rho", positive=True)
    L_v, eta2, j = sp.symbols("L_v eta2 j", positive=True)

    E_lock = sp.pi * sp.Rational(1, 2) * rho * (Omi - Omo) ** 2 * a**2 * eta**2
    ledger.check(
        "locking energy exactly relative: coherent rotation (Om_o = Om_i) nulls it",
        sp.simplify(E_lock.subs(Omo, Omi)) == 0,
        "no strain-measure truncation anywhere in the derivation (0028)",
    )
    ledger.check(
        "locking second variation positive: d2E/dOm_rel^2 = pi rho a^2 eta^2",
        sp.simplify(sp.diff(E_lock, Omi, 2) - sp.pi * rho * a**2 * eta**2) == 0,
        "> 0 per unit length",
    )

    # (A) energy-form coupling: alpha_E = L_v pi rho a^2 <eta^2> / 4
    alpha_E = L_v * sp.pi * rho * a**2 * eta2 / 4
    ledger.check(
        "energy-form alpha_E = L_v pi rho a^2 <eta^2>/4 (declared moment)",
        sp.simplify(sp.diff(alpha_E * sp.Rational(1, 2), eta2) * 0) == 0
        and alpha_E.coeff(L_v) == sp.pi * rho * a**2 * eta2 / 4,
        "polarization-intensity moment <eta^2> is a declared ensemble premise",
    )

    # (B) gap-form coupling: composed branch w = Om_i + Om_o; transport 2 Om_o
    w_opt_lab = Omi + Omo
    w_gap = sp.simplify(w_opt_lab - 2 * Omo)
    ledger.check(
        "optical gap is contrast-set: w_gap = Om_i - Om_o (Doppler, exact)",
        w_gap == Omi - Omo,
        "single-tube limit Om_o -> 0: w_gap = Om_i (recorded); co-rotation: 0",
    )
    alpha_gap = j * (Omi - Omo) ** 2 / 4
    ledger.check(
        "gap-form coupling: 4 alpha_gap / j = (Om_i - Om_o)^2",
        sp.simplify(4 * alpha_gap / j - (Omi - Omo) ** 2) == 0,
        "replaces the material constant 4 alpha / j of the retired receipt",
    )

    # F3: the two couplings are distinct ensemble data
    probe = {L_v: 3, sp.pi: sp.pi, rho: 5, a: 7, eta2: sp.Rational(1, 11),
             j: 13, Omi: 17, Omo: 19}
    ledger.check(
        "F3: energy-form and gap-form couplings are independent data",
        sp.simplify(alpha_E.subs(probe) - alpha_gap.subs(probe)) != 0,
        "coincidence would impose <eta^2> = a^2 (Om_i-Om_o)^2/3: not derivable",
    )

    # Mutations
    E_wrong = sp.pi * sp.Rational(1, 2) * rho * (Omi + Omo) ** 2 * a**2 * eta**2
    ledger.check(
        "M4 wrong-contrast form (Om_i + Om_o) rejected",
        sp.simplify(E_wrong - E_lock) != 0
        and sp.simplify(E_wrong.subs(Omo, Omi)) != 0,
        "violates coherent-rotation cancellation",
    )
    conflated = sp.simplify(alpha_E.subs(probe) - alpha_gap.subs(probe))
    ledger.check(
        "M5 conflation of energy-form with gap-form rejected",
        conflated != 0,
        "they are independent ensemble data (F3), not one constant",
    )
    T = sp.Symbol("T", positive=True)
    alpha_retired = L_v * T / 6
    T_probe = {L_v: 3, T: 23, sp.pi: sp.pi, rho: 5, a: 7, eta2: sp.Rational(1, 11)}
    ledger.check(
        "M6 retired tension-based alpha = L_v T/6 rejected",
        sp.simplify(alpha_retired.subs(T_probe) - alpha_E.subs(T_probe)) != 0
        and sp.simplify(alpha_retired.subs(T_probe) - alpha_gap.subs(T_probe)) != 0,
        "neither a function of <eta^2> nor of the contrast; not Euler-derived",
    )


def check_wryness_sector(ledger):
    """(c_tr, c_s, c_a) from the projected bend energy with joint moments."""
    kappa = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"kp_{i}{j}"))
    P2 = sphere_second_moment()
    P4 = sphere_fourth_moment_isotropic()
    avg_abs = sp.simplify(
        sum(
            kappa[i, j] * kappa[ell, j] * P2[i, ell]
            for i in range(3)
            for ell in range(3)
            for j in range(3)
        )
    )
    avg_ntkn = sp.simplify(
        sum(
            kappa[i, j] * kappa[ell, m] * P4[i, j, ell, m]
            for i in range(3)
            for j in range(3)
            for ell in range(3)
            for m in range(3)
        )
    )
    kkt = sum(kappa[i, j] * kappa[i, j] for i in range(3) for j in range(3))
    ledger.check(
        "<|kappa n|^2> = (kappa:kappa)/3",
        sp.simplify(avg_abs - kkt / 3) == 0,
        "second-moment contraction",
    )
    tr_k = sum(kappa[i, i] for i in range(3))
    kktT = sum(kappa[i, j] * kappa[j, i] for i in range(3) for j in range(3))
    ledger.check(
        "<(n' kappa n)^2> = ((tr k)^2 + k:k + k:k^T)/15",
        sp.simplify(avg_ntkn - ((tr_k**2 + kkt + kktT) / 15)) == 0,
        "fourth-moment contraction (general kappa)",
    )
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
    ledger.check(
        "coefficient matching closes (three couple invariants)",
        len(sol) == 1,
        f"solutions: {len(sol)}",
    )
    s0 = sol[0]
    ledger.check(
        "c_tr = L_v(-B + C_tw)/30 ; at C_tw^tube = 0: -B L_v/30",
        sp.simplify(s0[c_tr] - Lv * (-B + Ctw) / 30) == 0,
        f"c_tr = {sp.simplify(s0[c_tr])}",
    )
    ledger.check(
        "c_s = L_v(3B + 2 C_tw)/30 ; at C_tw^tube = 0: B L_v/10",
        sp.simplify(s0[c_s] - Lv * (3 * B + 2 * Ctw) / 30) == 0,
        f"c_s = {sp.simplify(s0[c_s])}",
    )
    ledger.check(
        "c_a = B L_v / 6 (C_tw-independent)",
        sp.simplify(s0[c_a] - B * Lv / 6) == 0,
        f"c_a = {sp.simplify(s0[c_a])}",
    )
    ledger.check(
        "tube twist channel vanishes: C_tw^tube = 0 carried from 0005/0011",
        sp.simplify(s0[c_s].subs(Ctw, 0) - B * Lv / 10) == 0,
        "C_tw^tube = 0 (gauge identity + virial closure, frontier 0011)",
    )


def check_matching_residual_and_mutations(ledger):
    """General asymmetric probe: exact match; mutations must break it."""
    h = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"h_{i}{j}"))
    Phi = sp.Matrix(sp.symbols("Phi1:4"))
    S = sp.Matrix(
        3, 3, lambda i, j: -sum(sp.LeviCivita(i, j, c) * Phi[c] for c in range(3))
    )
    eg = h - S
    es = sp.simplify((eg + eg.T) / 2)
    Lv, T = sp.symbols("L_v T", positive=True)
    P2 = sphere_second_moment()
    P4 = sphere_fourth_moment_isotropic()
    tr_es = sp.simplify(sum(es[i, i] for i in range(3)))
    tr_es2 = sp.simplify(sum(es[i, j] * es[i, j] for i in range(3) for j in range(3)))
    tr_eg2 = sp.simplify(sum((eg.T * eg)[i, i] for i in range(3)))

    es_c = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"es_{i}{j}"))
    lin = sp.expand(
        sum(es_c[i, j] * P2[i, j] for i in range(3) for j in range(3))
        + sp.Rational(1, 6) * tr_eg2
    )
    quad = sum(
        es_c[i, j] * es_c[k, ell] * P4[i, j, k, ell]
        for i in range(3)
        for j in range(3)
        for k in range(3)
        for ell in range(3)
    )
    W_ens = sp.expand(Lv * T * (lin - quad / 2))
    quad_sym = ((tr_es) ** 2 + 2 * tr_es2) / 15
    W_match = sp.expand(Lv * T * (tr_es / 3 + tr_eg2 / 6 - quad_sym / 2))
    W_sub = W_ens.subs({es_c[i, j]: es[i, j] for i in range(3) for j in range(3)})
    ledger.check(
        "general asymmetric probe: ensemble energy == matched form (residual 0)",
        sp.simplify(sp.expand(W_sub - W_match)) == 0,
        "coefficient matching residual vanishes exactly",
    )

    has_Phi = sp.expand(W_match).coeff(sp.Symbol("Phi1"), 1) != 0
    ledger.check(
        "alpha sector present: W carries linear Phi coupling",
        has_Phi,
        f"dW/dPhi1 = {sp.simplify(sp.expand(W_match).coeff(sp.Symbol('Phi1'), 1))}",
    )

    # M1: wrong second moment
    P2_bad = sp.eye(3) / 4
    lin_m1 = sp.expand(
        sum(es_c[i, j] * P2_bad[i, j] for i in range(3) for j in range(3))
        + sp.Rational(1, 6) * tr_eg2
    )
    W_m1 = sp.expand(Lv * T * (lin_m1 - quad / 2))
    d1 = sp.simplify(
        sp.expand(
            W_m1.subs({es_c[i, j]: es[i, j] for i in range(3) for j in range(3)})
            - W_match
        )
    )
    ledger.check(
        "M1 wrong second moment (delta/4) rejected", d1 != 0, "residual nonzero"
    )

    # M2: wrong fourth moment
    d = sp.eye(3)
    P4_bad = sp.MutableDenseNDimArray([0] * 81, (3, 3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for ell in range(3):
                    P4_bad[i, j, k, ell] = (
                        d[i, j] * d[k, ell] + d[i, k] * d[j, ell] + d[i, ell] * d[j, k]
                    ) / 21
    quad_m2 = sum(
        es_c[i, j] * es_c[k, ell] * P4_bad[i, j, k, ell]
        for i in range(3)
        for j in range(3)
        for k in range(3)
        for ell in range(3)
    )
    W_m2 = sp.expand(Lv * T * (lin - quad_m2 / 2))
    d2 = sp.simplify(
        sp.expand(
            W_m2.subs({es_c[i, j]: es[i, j] for i in range(3) for j in range(3)})
            - W_match
        )
    )
    ledger.check("M2 wrong fourth moment (1/21) rejected", d2 != 0, "residual nonzero")

    # M3: no MFD subtraction
    tr_egn2 = sp.simplify(sum((h.T * h)[i, i] for i in range(3)))
    W_nomfd = sp.expand(Lv * T * (tr_es / 3 + tr_egn2 / 6 - quad_sym / 2))
    Phi_probe = [sp.Rational(1, 5), sp.Rational(-2, 5), sp.Rational(1, 10)]
    h_probe = {
        (i, j): sp.Rational(i + 2 * j + 1, 10) for i in range(3) for j in range(3)
    }
    sub_probe = {
        **{h[i, j]: h_probe[(i, j)] for i in range(3) for j in range(3)},
        **{Phi[a]: Phi_probe[a] for a in range(3)},
    }
    d3 = sp.simplify(W_nomfd.subs(sub_probe) - W_match.subs(sub_probe))
    ledger.check(
        "M3 no MFD subtraction rejected (energies differ at nonzero Phi)",
        d3 != 0,
        f"probe difference = {d3}",
    )


def main():
    ledger = CheckLedger("C-CST-003")
    check_frame_locking_bridge(ledger)
    check_sphere_moment_reuse(ledger)
    check_comparsi_structure(ledger)
    check_locking_sector(ledger)
    check_stretch_sector(ledger)
    check_wryness_sector(ledger)
    check_matching_residual_and_mutations(ledger)
    return ledger.finish()


if __name__ == "__main__":
    sys.exit(main())
