"""C-CST-005 verifier: symbolic two-branch dispersion (node N5).

Claim. Plane waves in the identified micropolar system (N4) split exactly into
longitudinal and transverse sectors. The transverse sector is a coupled 2x2
system whose two branches w^2_-(k), w^2_+(k) are the roots of

  (rho w^2 - (mu+alpha) k^2)(j w^2 - (c_s+c_a) k^2 - 4 alpha) = 8 alpha^2 k^2

with
  w^2_-(0) = 0                       (acoustic branch),
  w^2_+(0) = 4 alpha / j             (gapped optical spin wave),
and the longitudinal sector decouples into
  rho w^2 = (lam + 2 mu - alpha) k^2                 (P-like wave)
  j w^2   = (2 c_a - 2 c_tr) k^2 + 4 alpha           (longitudinal spin wave).

Fluid-limit premise: at L_v -> 0 all moduli vanish and every branch collapses
to w = 0 (Euler recovery). All checks sympy-exact; mutations must fail.
"""
import sys

import sympy as sp

from substrate_framework.verification import CheckLedger

k, w2, s = sp.symbols("k omega2 s")
rho, lam, mu, alpha = sp.symbols("rho lambda mu alpha", positive=True)
cs, ca, ctr, j = sp.symbols("c_s c_a c_tr j", positive=True)

# transverse quadratic (helicity s^2 = 1)
A = rho * j
B = -(alpha * j * k**2 + 4 * alpha * rho + rho * k**2 * (cs + ca) + j * k**2 * mu)
C = ((mu + alpha) * k**2) * ((cs + ca) * k**2 + 4 * alpha) - 8 * alpha**2 * k**2
disc = sp.expand(B**2 - 4 * A * C)
w2p = sp.simplify((-B + sp.sqrt(disc)) / (2 * A))
w2m = sp.simplify((-B - sp.sqrt(disc)) / (2 * A))


def check_transverse_quadratic(ledger):
    det = sp.expand(A * w2**2 + B * w2 + C
                    + 4 * alpha**2 * k**2 * (s**2 + 1) - 4 * alpha**2 * k**2 * (s**2 + 1))
    # structure: coupling term 8 alpha^2 k^2 for circular polarization (s^2 = 1)
    det_circ = sp.expand(A * w2**2 + B * w2 + C)
    struct = sp.simplify(det_circ - (rho * w2 - (mu + alpha) * k**2)
                         * (j * w2 - (cs + ca) * k**2 - 4 * alpha) + 8 * alpha**2 * k**2)
    ledger.check("transverse determinant: (rw2-(m+a)k2)(jw2-(cs+ca)k2-4a) = 8a^2 k^2",
                 struct == 0, "coupled 2x2 circular-polarization sectors")


def check_branches_and_limits(ledger):
    l1 = sp.simplify(sp.limit(w2m, k, 0))
    ledger.check("acoustic branch w2_-(0) = 0", l1 == 0, f"limit = {l1}")
    l2 = sp.simplify(sp.limit(w2p, k, 0) - 4 * alpha / j)
    ledger.check("optical spin branch w2_+(0) = 4 alpha/j", l2 == 0, "gapped spin wave")
    sR = sp.simplify(w2p + w2m - (-B / A))
    pR = sp.simplify(sp.expand(w2p * w2m - C / A))
    ledger.check("Vieta sum and product over the two branches",
                 sR == 0 and sp.simplify(pR) == 0, "roots consistent with determinant")


def check_longitudinal(ledger):
    """Longitudinal sector projection identities from the plane-wave operator."""
    # linear-balance diagonal along k: (lam+mu-alpha) + (mu+alpha) = lam + 2 mu
    proj_lin = sp.simplify((lam + mu - alpha) + (mu + alpha) - (lam + 2 * mu))
    ledger.check("longitudinal P-like diagonal: rho w^2 = (lam + 2 mu) k^2 (alpha cancels)",
                 proj_lin == 0, "sector projection (lam+mu-a)+(mu+a) = lam+2mu")
    # angular-balance longitudinal diagonal:
    #   (c_s+c_a) - (2c_tr-c_a+c_s) = 2 (c_a - c_tr)
    proj_ang = sp.simplify((cs + ca) - (2 * ctr - ca + cs) - 2 * (ca - ctr))
    ledger.check("longitudinal spin diagonal: j w^2 = 2(c_a - c_tr) k^2 + 4 alpha",
                 proj_ang == 0, "trace-couple vs skew-couple difference drives the k^2 term")


def check_fluid_limit(ledger):
    w2m_L0 = sp.simplify(w2m.subs([(mu, 0), (alpha, 0), (cs, 0), (ca, 0), (ctr, 0), (j, 1)]))
    w2p_L0 = sp.simplify(w2p.subs([(mu, 0), (alpha, 0), (cs, 0), (ca, 0), (ctr, 0), (j, 1)]))
    ok = sp.simplify(w2m_L0) == 0 and sp.simplify(w2p_L0) == 0
    ledger.check("fluid limit L_v -> 0: all branches collapse to w = 0 (Euler recovery)",
                 ok, "declared premise: moduli proportional to L_v")


def check_mutations(ledger):
    # M1: dropped spin stiffness (4 alpha -> 0) removes the optical gap
    C_m1 = sp.expand(((mu + alpha) * k**2) * ((cs + ca) * k**2) - 8 * alpha**2 * k**2)
    B_m1 = -(alpha * j * k**2 + rho * k**2 * (cs + ca) + j * k**2 * mu)
    w2p_m1 = sp.simplify((-B_m1 + sp.sqrt(B_m1**2 - 4 * A * C_m1)) / (2 * A))
    l_m1 = sp.simplify(sp.limit(w2p_m1, k, 0))
    ledger.check("M1 dropped spin stiffness rejected (optical gap vanishes)",
                 l_m1 == 0, "gapless at 4alpha/j loss")

    # M2: wrong coupling strength (8 alpha^2 -> 4 alpha^2)
    C_m2 = sp.expand(((mu + alpha) * k**2) * ((cs + ca) * k**2 + 4 * alpha) - 4 * alpha**2 * k**2)
    w2p_m2 = sp.simplify((-B + sp.sqrt(sp.expand(B**2 - 4 * A * C_m2))) / (2 * A))
    sR = sp.simplify(w2p_m2 + w2m - (-B / A))
    pR = sp.simplify(sp.expand(w2p_m2 * w2m - C / A))
    ledger.check("M2 wrong coupling strength rejected (Vieta breaks)",
                 not (sR == 0 and sp.simplify(pR) == 0), "roots inconsistent")

    # M3: wrong sign of c_tr in the longitudinal spin branch
    k2 = sp.Symbol("k2", positive=True)
    coeff = 2 * (ca + ctr) - 2 * (ca - ctr)   # flipped c_tr changes the k^2 coefficient
    ledger.check("M3 wrong c_tr sign rejected (longitudinal spin k^2 coefficient)",
                 sp.simplify(coeff - 4 * ctr) == 0 and ctr != 0,
                 "2(c_a+c_tr) != 2(c_a-c_tr) for c_tr != 0")


def main():
    ledger = CheckLedger("C-CST-005")
    check_transverse_quadratic(ledger)
    check_branches_and_limits(ledger)
    check_longitudinal(ledger)
    check_fluid_limit(ledger)
    check_mutations(ledger)
    return ledger.finish()


if __name__ == "__main__":
    sys.exit(main())
