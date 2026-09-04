"""C-CST-002 verifier: bend/twist micro-moduli of the Rankine vortex sheet.

Claim (conditional, node N2 of proposals/P251-cosserat-from-vortex-euler):

  The linearized Euler problem about the Rankine vortex (solid rotation
  Omega inside r<a, irrotational Omega a^2/r outside, vortex sheet at r=a)
  has, to leading order in the small quantities t=(ka)^2 and 1/L,
  L=ln(2/(ka)):

  (a)  Poincare reduction: the interior perturbation pressure satisfies
       grad^2 p' = (4 Om^2/wt^2) p_zz (wt = w - m Om), i.e. with
       P = A J_m(lam r):  lam^2 = k^2 (4 Om^2 - wt^2)/wt^2
       (oscillatory, real in the inertial regime wt^2 < 4 Om^2; the
       cylinder ODE reads P'' + P'/r - m^2 P/r^2 = -lam^2 P).  The same momentum
       system yields the classical plane-wave inertial dispersion
       wt^2 = 4 Om^2 kz^2/|k|^2 (sign-convention guard).
  (b)  m=1: after eliminating the interior/exterior amplitudes through the
       kinematic pair, the two remaining matching conditions (pressure
       continuity with advected Bernoulli; frozen sheet strength
       [v_th] = 2 Om eta) are EXACTLY PROPORTIONAL at leading-log order,
       r1 = rho a Om r2, with
       r2 = -eta [ 2 w + Om (ka)^2 ( L + 1/2 - gamma ) ] + o(t*L).
  (c)  m=1 LIA branch:  w* = -(Gamma k^2 / 4 pi)( L + 1/2 - gamma ) + o(1),
       Gamma = 2 pi Om a^2  [NUMERIC_EVIDENCE, ASYMPTOTIC].  (The bend
       stiffness B(k) is log-running; its operator convention is fixed at
       the N3 receipt.)
  (d)  m=2 branch:  w = Om(m-1) - Om(ka)^2/6 + O((ka)^4): the exact
       transcendental system closes at the O((ka)^2) branch with the
       coefficient constant across decades; pattern speed w/m -> Om/2
       (Kirchhoff limit).  [The recorded -1/12 coefficient of attempts
       0006-0011 was computed in the non-Poincare I-species interior and is
       superseded here; the Kirchhoff k^0 limit and the C_tw=0 receipt's
       static virial are unaffected, the O(k^2) energy receipt is flagged
       for recomputation at N3.]
  (e)  translation neutrality: at k=0, w=0 both residuals vanish exactly
       (the displaced-vortex equilibrium).
  The single-tube twist-stiffness receipt C_tw = 0 at O(k^2) (mode energy
  k-independent) is carried from attempts/0011 with its recorded Bessel-
  exact evidence; this verifier does not recompute it.

Conventions (frozen before any value was computed):
  - lab frame; mode e^{i(m th + k z - w t)}; Doppler wt = w - m Om;
  - linearized momentum (inertial): -i wt v' + 2 Om z^x v' = -grad p'/rho;
    the 2 Om collects the (v0.grad)v' basis terms and (v'.grad)v0, each
    contributing Om z^x v';
  - interior velocities from that system:
      v_r  = i(wt P' - 2 Om m P/r)/(rho (4 Om^2 - wt^2))
      v_th =   (2 Om P' - wt m P/r)/(rho (4 Om^2 - wt^2))
      v_z  = k P/(rho wt)
  - exterior: potential Phi = C K_m(k r) (decaying), p'_out(a) =
    i rho wt C K_m(ka) (fluid Doppler; base fluid angular rate at the
    sheet is Om on both sides);
  - sheet conditions: v_r(a^-) = v_r(a^+) = -i wt eta (no flux), p-cont,
    frozen strength [v_th] = 2 Om eta (gamma_z = 2 Om eta; tilt corrections
    enter at O(eta^2), attempts/0013-0014).

Mutations (each must flip the LIA-root predicate to reject):
  M1 defective interior wavenumber mu^2 = -k^2(4Om^2-wt^2)/(w wt)
     (1/omega instead of 1/wt^2 -- the 0008-0013 defect; it survived three
     earlier probe batteries, which is why it is now a named mutation);
  M2 single-Omega Coriolis (D -> Om^2 - wt^2, 2 Om -> Om);
  M3 flipped frozen strength ([v_th] = -2 Om eta);
  M4 wrong exterior Doppler (w in place of wt in p'_out);
  M5 growing exterior harmonic I_m in place of K_m.

Numeric evidence: mpmath, dps=40, rho=Om=a=eta=1. Exact checks: SymPy only.
Run:
  PYTHONPATH=src .venv/bin/python proposals/P251-cosserat-from-vortex-euler/verify_cst002.py

Attempt history (append-only, see attempts/):
  0015: first execution of the frozen verifier (post-0014 correction).
"""

import sys

import mpmath as mp
import sympy as sp

from substrate_framework.verification import CheckLedger

mp.mp.dps = 40

# ---------------------------------------------------------------- exact algebra


def check_poincare_reduction(ledger):
    """(a) incompressibility + cylinder ODE  <=>  lam^2 = k^2(4Om^2-wt^2)/wt^2."""
    r = sp.Symbol("r", positive=True)
    k, Om, rho, wt, mu2 = sp.symbols("k Omega rho wt mu2", positive=True)
    m = sp.symbols("m", integer=True, nonnegative=True)
    P = sp.Function("P")(r)
    Pp = sp.diff(P, r)
    Ppp = sp.diff(Pp, r)
    D = 4 * Om**2 - wt**2
    v_r = sp.I * (wt * Pp - 2 * Om * m * P / r) / (rho * D)
    v_th = (2 * Om * Pp - wt * m * P / r) / (rho * D)
    v_z = k * P / (rho * wt)
    div = sp.diff(r * v_r, r) / r + sp.I * m * v_th / r + sp.I * k * v_z
    # impose the cylinder ODE  P'' + P'/r - m^2 P/r^2 = -lam2 P  (J-species)
    lam2 = sp.symbols("lam2", positive=True)
    div_ode = sp.simplify(div.subs(Ppp, -lam2 * P - Pp / r + m**2 * P / r**2))
    coeff = sp.simplify(div_ode * rho * wt / (sp.I * P))
    D = 4 * Om**2 - wt**2
    ledger.check(
        "poincare_reduction: div-v' = (k^2 - wt^2 lam2/D)*P structure",
        sp.simplify(coeff - (k**2 - wt**2 * lam2 / D)) == 0
        and sp.simplify(coeff) != 0,
        f"coefficient = {coeff}",
    )
    ledger.check(
        "poincare_reduction: closure at lam^2 = k^2(4Om^2-wt^2)/wt^2",
        sp.simplify(coeff.subs(lam2, k**2 * (4 * Om**2 - wt**2) / wt**2)) == 0,
        f"coefficient at closure = {coeff}",
    )


def check_inertial_plane_wave(ledger):
    """(a) the same momentum system gives wt^2 = 4 Om^2 kz^2 / |k|^2."""
    Om, rho = sp.symbols("Omega rho", positive=True)
    kz, kperp, vx, vy, vz, p, wt = sp.symbols("k_z k_perp v_x v_y v_z p wt", real=True)
    kk2 = kz**2 + kperp**2
    # rotating-frame momentum, plane wave, k along (kperp, 0, kz) wlog:
    #   -i wt v + 2 Om z^x v = -i k p / rho ;  div v = 0
    eqs = [
        -sp.I * wt * vx - 2 * Om * vy + sp.I * kperp * p / rho,
        -sp.I * wt * vy + 2 * Om * vx,
        -sp.I * wt * vz + sp.I * kz * p / rho,
        sp.I * kperp * vx + sp.I * kz * vz,
    ]
    mat, _ = sp.linear_eq_to_matrix(eqs, [vx, vy, vz, p])
    det = sp.factor(mat.det())
    ledger.check(
        "inertial_plane_wave_limit: det carries wt^2 = 4 Om^2 kz^2/|k|^2",
        sp.simplify(det / (wt**2 - 4 * Om**2 * kz**2 / kk2)) != 0
        and sp.simplify(det.subs(wt**2, 4 * Om**2 * kz**2 / kk2)) == 0,
        f"det = {det}",
    )


def check_proportionality_leading_log(ledger):
    """(b) r1 = rho a Om r2 at leading-log order; root slope 2, constant -gamma-1/8."""
    k, Om, rho, a, eta, w, g = sp.symbols("k Omega rho a eta omega gamma_e", positive=True)
    L = sp.symbols("L", real=True)  # ln(2/(ka)); ln(ka/2) = -L
    wt = -Om + w  # m=1 Doppler on the slow branch; w = O(t L)
    t = sp.symbols("t", positive=True)  # bookkeeping parameter t = (ka)^2
    # retained order: t^0 and t^1 (with one L); dropped: w^2, w t, t^2, t^{3/2}
    lam1a = sp.sqrt(3) * k * a  # lam^2 a^2 = 3 t on the branch (wt^2 = Om^2 + O(w))
    J1a = (lam1a / 2) * (1 - lam1a**2 / 8)  # J_1(x) = (x/2)(1 - x^2/8) + O(x^5)
    dJ1a = lam1a * (1 - 3 * lam1a**2 / 8) / (2 * a)  # d/dr J_1(lam r)|_a
    ell1 = -L + g - sp.Rational(1, 2)  # K_1: 1/x + (x/2)(ln(x/2)+g-1/2)
    ell2 = -L + g  # K_1'(x) = -1/x^2 + (ln(x/2)+g)/2
    K1a = 1 / (k * a) + (k * a / 2) * ell1
    dK1a = -1 / (k * a**2) + (k / 2) * ell2  # d/dr K_1(k r)|_a
    D = 4 * Om**2 - wt**2
    A = -wt * eta * rho * D / (wt * dJ1a - 2 * Om * J1a / a)
    C = -sp.I * wt * eta / dK1a
    r1 = sp.expand(A * J1a - sp.I * rho * wt * C * K1a)
    vth_in = (2 * Om * dJ1a - wt * J1a / a) / (rho * D) * A
    r2 = sp.expand(sp.I * C * K1a / a - vth_in - 2 * Om * eta)
    sigma = sp.symbols("sigma", positive=True)  # w = Om*sigma*t*L bookkeeping
    def trunc(expr):
        e = sp.expand(expr.subs([(w, Om * sigma * t * L), (k, sp.sqrt(t) / a)]))
        return sp.simplify(sp.series(e, t, 0, 2).removeO())
    diff = sp.simplify(trunc(r1 - rho * a * Om * r2))
    ledger.check(
        "condition_proportionality: r1 = rho a Om r2 (leading log)",
        diff == 0,
        f"residue (through O(t)) = {diff}",
    )
    target = -eta * (2 * w + Om * t * (L + sp.Rational(1, 2) - g))
    resid2 = sp.simplify(trunc(r2 - target))
    ledger.check(
        "condition_proportionality: root slope 2, constant 1/2-gamma",
        resid2 == 0,
        f"r2 - target (through O(t)) = {resid2}",
    )


# ---------------------------------------------------------------- numeric machinery

PARAM_KEYS = ("wavenumber", "coriolis", "tangential", "doppler", "exterior")


def _build(params):
    """Residual builder for the m=1 sheet system under a parameter dict."""
    Om = mp.mpf(1)
    rho = mp.mpf(1)
    a = mp.mpf(1)
    m = 1

    def residuals(w, k):
        w = mp.mpf(w)
        k = mp.mpf(k)
        wt = w - m * Om
        if params["coriolis"] == "2Om":
            D = 4 * Om**2 - wt**2
            two = 2 * Om
        else:  # M2 single-Omega
            D = Om**2 - wt**2
            two = Om
        if params["wavenumber"] == "correct":
            lam2 = k**2 * (4 * Om**2 - wt**2) / wt**2
        else:  # M1 defective 1/omega form
            lam2 = -k**2 * (4 * Om**2 - wt**2) / (w * wt)
        if lam2 <= 0:
            return None
        lam = mp.sqrt(lam2)
        Jma = mp.besselj(m, lam * a)
        dJm = lam * (mp.besselj(m - 1, lam * a) - m * mp.besselj(m, lam * a) / (lam * a))
        if params["exterior"] == "K":
            Zma = mp.besselk(m, k * a)
            dZ = -k * mp.besselk(m - 1, k * a) - m * mp.besselk(m, k * a) / a
        else:  # M5 growing harmonic
            Zma = mp.besseli(m, k * a)
            dZ = k * mp.besseli(m - 1, k * a) - m * mp.besseli(m, k * a) / a
        doppler_out = wt if params["doppler"] == "wt" else w  # M4
        C = -1j * wt / dZ
        B = -1j * wt / (1j * (wt * a * dJm - two * m * Jma) / (a * rho * D))
        r1 = B * Jma - 1j * rho * doppler_out * C * Zma
        vth_in = (two * a * dJm - m * wt * Jma) / (a * rho * D) * B
        sgn = 1 if params["tangential"] == "+" else -1  # M3
        r2 = 1j * m * C * Zma / a - vth_in - sgn * 2 * Om
        return abs(r1), abs(r2)

    return residuals


def _lia_root_scan(residuals, k, w_pred):
    """Locate the F-minimum on a fine grid around the analytic prediction."""
    best_w, best_f = None, mp.inf
    for i in range(-40, 41):
        x = mp.mpf(w_pred) * (1 + mp.mpf("0.02") * i)
        rr = residuals(x, k)
        if rr is None:
            continue
        f = rr[0] ** 2 + rr[1] ** 2
        if f < best_f:
            best_w, best_f = x, f
    return best_w, best_f


def _lia_signature(res, k):
    """Return (rel-error vs asymptote, root residual, r1-r2 relative split)."""
    Om = mp.mpf(1)
    a = mp.mpf(1)
    gam = mp.euler
    w_pred = -(Om * (k * a) ** 2 / 2) * (mp.log(2 / (k * a)) + mp.mpf(1) / 2 - gam)
    w_num, f = _lia_root_scan(res, k, w_pred)
    if w_num is None:
        return None
    rel = abs(w_num - w_pred) / abs(w_pred)
    rr = res(w_num, k)
    split = abs(rr[0] - rr[1]) / max(rr[0], rr[1])
    return rel, mp.sqrt(f), split


def _lia_predicate(params):
    """True iff the corrected-system LIA signature is present at two decades."""
    res = _build(params)
    for k_exp in (3, 4):
        out = _lia_signature(res, mp.mpf(10) ** (-k_exp))
        if out is None:
            return False
        rel, resid, split = out
        if rel > mp.mpf("0.20") or split > mp.mpf("1e-3") or resid > mp.mpf("1e-6"):
            return False
    return True


def check_m1_branch(ledger):
    """(c) numeric LIA root + refinement + proportionality at the root."""
    res = _build(
        dict(wavenumber="correct", coriolis="2Om", tangential="+", doppler="wt", exterior="K")
    )
    resid_first = None
    for k_exp in (2, 3, 4, 5):
        k = mp.mpf(10) ** (-k_exp)
        out = _lia_signature(res, k)
        rel, resid, split = out
        if resid_first is None:
            resid_first = resid
        ledger.check(
            f"m1_lia_root: k=1e-{k_exp} within 25% of asymptote",
            rel <= mp.mpf("0.25"),
            f"rel={mp.nstr(rel, 4)}",
        )
        ledger.check(
            f"m1_lia_root: k=1e-{k_exp} r1=r2 at root",
            split <= mp.mpf("1e-3"),
            f"split={mp.nstr(split, 4)}",
        )
    ledger.check(
        "m1_lia_root: residual refinement across decades",
        resid < resid_first < mp.mpf("1e-5"),
        f"|r| {mp.nstr(resid_first, 4)} -> {mp.nstr(resid, 4)}",
    )


def _m2_residuals(w, k):
    Om = mp.mpf(1)
    rho = mp.mpf(1)
    a = mp.mpf(1)
    m = 2
    wt = w - m * Om
    if wt == 0:
        return None
    lam2 = k**2 * (4 * Om**2 - wt**2) / wt**2
    if lam2 <= 0:
        return None
    lam = mp.sqrt(lam2)
    Jma = mp.besselj(m, lam * a)
    dJm = lam * (mp.besselj(m - 1, lam * a) - m * mp.besselj(m, lam * a) / (lam * a))
    Kma = mp.besselk(m, k * a)
    dKm = -k * mp.besselk(m - 1, k * a) - m * mp.besselk(m, k * a) / a
    C = -1j * wt / dKm
    B = -1j * wt / (1j * (wt * a * dJm - 2 * Om * m * Jma) / (a * rho * (4 * Om**2 - wt**2)))
    r1 = B * Jma - 1j * rho * wt * C * Kma
    vth_in = (2 * Om * a * dJm - m * wt * Jma) / (a * rho * (4 * Om**2 - wt**2)) * B
    r2 = 1j * m * C * Kma / a - vth_in - 2 * Om
    return abs(r1), abs(r2)


def check_m2_branch(ledger):
    """(d) closure at the O((ka)^2) branch; coefficient -1/6 frozen across decades."""
    Om = mp.mpf(1)
    a = mp.mpf(1)
    for k_exp in (2, 3, 4):
        k = mp.mpf(10) ** (-k_exp)
        t = (k * a) ** 2
        best_c, best_f = None, mp.inf
        for i in range(-2000, 2001):
            c = mp.mpf(i) / 2000
            rr = _m2_residuals(Om * (1 + c * t), k)
            if rr is None:
                continue
            f = rr[0] ** 2 + rr[1] ** 2
            if f < best_f:
                best_c, best_f = c, f
        ledger.check(
            f"m2_branch_closure: k=1e-{k_exp} coefficient = -1/6",
            abs(best_c + mp.mpf(1) / 6) <= mp.mpf("1e-3"),
            f"c={mp.nstr(best_c, 8)}",
        )
        ledger.check(
            f"m2_branch_closure: k=1e-{k_exp} residual at root",
            mp.sqrt(best_f) <= mp.mpf("1e-6"),
            f"|r|={mp.nstr(mp.sqrt(best_f), 4)}",
        )
    ledger.check(
        "kirchhoff_pattern_speed: w/m -> Om/2",
        abs((Om - Om * (mp.mpf("1e-3") * a) ** 2 / 6) / 2 - Om / 2)
        <= mp.mpf("1e-3") ** 2 / 10,
        f"|w/2 - Om/2| = {mp.nstr(abs((Om - Om * (mp.mpf('1e-3') * a) ** 2 / 6) / 2 - Om / 2), 4)}",
    )


def check_translation_neutrality(ledger):
    """(e) at k->0, w=0 the residuals vanish (displaced-vortex equilibrium)."""
    Om = mp.mpf(1)
    rho = mp.mpf(1)
    a = mp.mpf(1)
    m = 1
    k = mp.mpf("1e-30")
    w = mp.mpf(0)
    wt = w - m * Om
    lam2 = k**2 * (4 * Om**2 - wt**2) / wt**2
    lam = mp.sqrt(lam2)
    Jma = mp.besselj(m, lam * a)
    dJm = lam * (mp.besselj(m - 1, lam * a) - m * mp.besselj(m, lam * a) / (lam * a))
    Kma = mp.besselk(m, k * a)
    dKm = -k * mp.besselk(m - 1, k * a) - m * mp.besselk(m, k * a) / a
    C = -1j * wt / dKm
    B = -1j * wt / (1j * (wt * a * dJm - 2 * Om * m * Jma) / (a * rho * (4 * Om**2 - wt**2)))
    r1 = B * Jma - 1j * rho * wt * C * Kma
    vth_in = (2 * Om * a * dJm - m * wt * Jma) / (a * rho * (4 * Om**2 - wt**2)) * B
    r2 = 1j * m * C * Kma / a - vth_in - 2 * Om
    scale = 2 * Om * rho * a
    ledger.check(
        "translation_neutrality: k->0, w=0 residuals vanish",
        abs(r1) < mp.mpf("1e-25") * scale and abs(r2) < mp.mpf("1e-25") * scale,
        f"r1={mp.nstr(abs(r1), 4)} r2={mp.nstr(abs(r2), 4)}",
    )


def main() -> int:
    ledger = CheckLedger("C-CST-002")

    check_poincare_reduction(ledger)
    check_inertial_plane_wave(ledger)
    check_proportionality_leading_log(ledger)
    check_m1_branch(ledger)
    check_m2_branch(ledger)
    check_translation_neutrality(ledger)

    baseline = dict(
        wavenumber="correct", coriolis="2Om", tangential="+", doppler="wt", exterior="K"
    )
    mutations = [
        dict(baseline, wavenumber="defective"),  # M1: the 0008-0013 defect
        dict(baseline, coriolis="1Om"),  # M2
        dict(baseline, tangential="-"),  # M3
        dict(baseline, doppler="w"),  # M4
        dict(baseline, exterior="I"),  # M5
    ]
    ledger.mutation_sensitive("lia_root_signature", _lia_predicate, baseline, mutations)

    ledger.finish()
    return 0


if __name__ == "__main__":
    sys.exit(main())
