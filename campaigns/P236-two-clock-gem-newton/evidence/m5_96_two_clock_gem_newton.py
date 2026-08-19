"""
M5.96 — THE TWO-CLOCK GEM NEWTON LIMIT: the attractive 1/r^2 inter-mass force
(issue mlops-kelvin #96; substrate-framework P236; the MODELS.md M5 "Gravity:
Newton limit (GEM)" row measurement).

THE OBJECT (the issue's prescription, verbatim): two driven M5.8 fixed-clock
configs — the seed_M class of m5_8_2q (biaxial hedgehog frame O4, eigenvalues
(g, 1, delta, 0), boost dressing B(theta, A_BOOST)) — separated by d on the
z-axis, sharing the M5.17 angle-superposition texture
    Theta = theta_1 + q2*theta_2,  theta_i = atan2(rho, z - z_i)
(the merged openwave two-charge construction, PR-#437-era m5_17_two_charge.py;
q2 = +1 like pair / -1 anti-pair), dressed by the SHARED boost field
    theta(x) = theta_clock(r_1) + theta_clock(r_2),
    theta_clock(r) = b* e^{-(r/R_W)^2} + a0 (1 - e^{-(r/R_W)^2}),
with a0 = 0.8168*artanh(1/g) — the M5.21.8 lattice-measured rigid-dressing
attractor m*/artanh(1/g) = 0.8168 at g = 8 (the engine's own non-decaying
branch; branch-validated here by constrained smooth relaxation).

THE OBSERVABLE (never an imposed-envelope overlap):
    U_gem(d) = GEM[pair](d) - 2 GEM[single]
with GEM = the time-mixing sector of the audited quartic-commutator stack
(u_sectors of m5_8_2q: EM = +spatial-block curvature, GEM = -time-mixing
curvature = the clock fuel).  F(d) = -dU/dd.  A d-independent background
(the non-decaying mediator's far-field self-energy on the finite box) sits in
U_gem and cancels exactly in F; it is absorbed by the two-parameter fit
    U_gem(d) = U_inf + C/d      (the M5.17 E0 + A/d protocol)
so that      F(d) = C/d^2,  attractive iff C < 0.

GATES (frozen before the production run):
  G0  N-3 anchor: the undressed 24^3 seed reproduces H_static = 16.7379
      (the m5_8_2q correctness gate).
  G1  zero-boost null: theta == 0 => GEM == 0 EXACTLY on every rung (the
      GEM-proportional-to-boost structure; machine-exact, not a tolerance).
  G2  the 1/d law: R^2 >= 0.95 for U_inf + C/d on the mid window of every
      ladder rung, C < 0 (attractive), residual exponent in [-1.10, -0.90]
      => force exponent in [-2.10, -1.90].
  G3  box ladder 24^3 -> 32^3 -> 48^3 (engine convention: h fixed ~0.52, box
      grows): C converges monotonically in |C| beyond 32^3 to within 6%.
  G4  sign map (C-GRV-002 face): the anti-pair (q2 = -1) flips sign(C) and
      mirrors the EM channel (like charges: EM repulsive +C_em/d, GEM
      attractive -|C|/d).
  G5  mutation: corrupting clock 2's dressing (theta_2 := 0) must collapse
      |C| by a factor > 3 (a gate that cannot fail is not a gate).
  G6  coupling face: C(a0) / sinh^2(a0) constant to 10% over a0 >= 0.1 (the
      (b.g)^2 GEM coupling of the MODELS.md row).
  G7  machinery control (the m5_12 block-11 sign theorem): the M5.17 uniaxial
      s n n^T class (mixing-free) has GEM == 0 exactly under the same
      dressing — the GEM channel is biaxial-clock-specific.
  G8  mediation: the relaxed-shared-field protocol (smooth-manifold FIRE,
      kappa = 0 engine functional, both clock cores pinned at b* sources)
      reproduces the law (F exponent within 0.05 of -2) at 32^3.
  G9  stencil twin: the forward-stencil audit reproduces F exponent within
      0.08 of -2 at 48^3.

USAGE  python m5_96_two_clock_gem_newton.py [ladder|controls|mediation|all]
Out: ../data/m5_96_two_clock_gem_newton.json + ../plots/m5_96_*.png
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from openwave.xperiments.m5_liquid_crystal.research.sandbox_v8.m5_8_2a_4d_hamiltonian import (  # noqa: E402
    conj, boost_field, matmul, SP_PAIRS, TM_PAIRS,
)
from openwave.xperiments.m5_liquid_crystal.research.sandbox_v8.m5_8_2c1_full_evolution import (  # noqa: E402
    B_STAR, A_BOOST, central, tw,
)
from openwave.xperiments.m5_liquid_crystal.research.sandbox_v8.m5_8_2cb_taichi_constrained import (  # noqa: E402
    build_grid_n,
)
from openwave.xperiments.m5_liquid_crystal.research.sandbox_vn.m5_8_2h_omega_attractor import (  # noqa: E402
    np_commf,
)

DATA = HERE / ".." / "data"
PLOTS = HERE / ".." / "plots"
for _p in (DATA, PLOTS):
    _p.mkdir(parents=True, exist_ok=True)

# ---- the engine's validated constants (the N-3 / 24^3 stack of m5_8_2q) ----
G_TIME = 8.0
DELTA = 0.3
R_W = 3.5
RC = 0.8
RHOC = 0.8
BETA_SAT = 1.558
M_STAR = 0.8168 * float(np.arctanh(1.0 / G_TIME))     # 0.10254 (M5.21.8 g=8)
D4 = np.diag([G_TIME, 1.0, DELTA, 0.0])
R_PIN = 1.6                                            # clock-core pin radius


# ---------------- the energy instrument (m5_8_2q verbatim) ----------------
def u_density(M, h):
    u = 0.0
    Mi = [central(M, ax, h) for ax in range(3)]
    for i in range(3):
        for j in range(i + 1, 3):
            F = np_commf(Mi[i], Mi[j])
            u = u + 2.0 * np.einsum("...ab,...ab->...", F, tw(F))
    return u


def u_sectors(M, h):
    Mi = [central(M, ax, h) for ax in range(3)]
    uEM = uGEM = 0.0
    for i in range(3):
        for j in range(i + 1, 3):
            F = np_commf(Mi[i], Mi[j])
            sp = sum(F[..., a, b] ** 2 for a, b in SP_PAIRS)
            tm = sum(F[..., a, b] ** 2 for a, b in TM_PAIRS)
            uEM = uEM + 4.0 * sp
            uGEM = uGEM - 4.0 * tm
    return uEM, uGEM


def M_of(theta, O4):
    W = matmul(O4, boost_field(theta, A_BOOST))
    return conj(W, D4)


def total_static(theta, g, kappa=0.0):
    M = M_of(theta, g["O4"])
    u = u_density(M, g["h"])
    Msp = M[..., 1:4, 1:4]
    t = np.einsum("...ab,...ba->...", Msp, Msp)
    dens = u + BETA_SAT * u * u + kappa * (t - (1.0 + DELTA ** 2)) ** 2
    return float(dens[g["act"]].sum()) * g["h"] ** 3


# ---------------- grids and textures ----------------
def single_grid(n, L):
    g = build_grid_n(n, L)
    xs = np.linspace(-L, L, n)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    g["X"], g["Y"], g["Z"] = X, Y, Z
    inter = np.zeros(g["r"].shape, bool)
    inter[2:-2, 2:-2, 2:-2] = True
    g["act"] = inter & (g["r"] > 2 * RC) & (g["rho"] > RHOC)
    g["r1"] = g["r"]
    return g


def pair17_grid(n, L, d, q2=1.0):
    """The M5.17 angle-superposition two-center biaxial hedgehog frame.

    Theta = theta_1 + q2 theta_2 (hedgehog polar angles about each core);
    frame axes n, e_Theta, e_phi carry eigenvalues (1, delta, 0); the melt
    s = (1 - e^{-(r_1/rc)^2})(1 - e^{-(r_2/rc)^2}) regularizes the cores
    exactly as in the merged two-charge script; q2 = 0 reduces to the single
    hedgehog (their gate C0)."""
    rc = 2.0 * RC
    g = build_grid_n(n, L)
    xs = np.linspace(-L, L, n)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    rho = np.sqrt(X ** 2 + Y ** 2)
    z1, z2 = -d / 2, d / 2
    Th = np.arctan2(rho, Z - z1) + q2 * np.arctan2(rho, Z - z2)
    r1 = np.sqrt(rho ** 2 + (Z - z1) ** 2)
    r2 = np.sqrt(rho ** 2 + (Z - z2) ** 2)
    n1, n3 = np.sin(Th), np.cos(Th)
    shr = np.clip(rho / RHOC, 0, 1)
    shr = shr * shr * (3 - 2 * shr)
    epx, epy = -Y / np.maximum(rho, 1e-12), X / np.maximum(rho, 1e-12)
    O4 = np.zeros(X.shape + (4, 4))
    O4[..., 1, 1] = n1
    O4[..., 1, 3] = n3
    O4[..., 2, 1] = n3
    O4[..., 2, 3] = -n1
    O4[..., 3, 1] = epx * shr
    O4[..., 3, 2] = epy * shr
    O4[..., 0, 0] = 1.0
    inter = np.zeros(X.shape, bool)
    inter[2:-2, 2:-2, 2:-2] = True
    act = inter & (r1 > 2 * RC) & (r2 > 2 * RC) & (rho > RHOC)
    return dict(h=g["h"], X=X, Y=Y, Z=Z, rho=rho, r1=r1, r2=r2, O4=O4, act=act)


def theta_clock(r, a0):
    return B_STAR * np.exp(-((r / R_W) ** 2)) + a0 * (1 - np.exp(-((r / R_W) ** 2)))


def theta_shared(g, d, a0=M_STAR, corrupt=None):
    if d > 0:
        t1, t2 = theta_clock(g["r1"], a0), theta_clock(g["r2"], a0)
        if corrupt == "clock2":
            t2 = np.zeros_like(t2)
        return t1 + t2
    return theta_clock(g["r1"], a0)


def sectors(g, theta):
    M = M_of(theta, g["O4"])
    eEM, eGEM = u_sectors(M, g["h"])
    act = g["act"]
    v = g["h"] ** 3
    return float(eEM[act].sum()) * v, float(eGEM[act].sum()) * v


def fit_Ud(dd, U, dmin, dmax):
    """U(d) = Uinf + C/d; the d-independent background Uinf (the mediator's
    far-field self-energy on the finite box) cancels exactly in F = -dU/dd.
    The residual exponent is sign-aware (C may be positive, e.g. the anti-pair)."""
    m = (dd >= dmin) & (dd <= dmax)
    A = np.stack([np.ones(int(m.sum())), 1.0 / dd[m]], 1)
    (Uinf, C), *_ = np.linalg.lstsq(A, U[m], rcond=None)
    resid = U[m] - Uinf
    r2 = float(1 - np.var(resid - C / dd[m]) / np.var(U[m]))
    keep = np.abs(resid) > 1e-9
    p = float(np.polyfit(np.log(dd[m][keep]), np.log(np.abs(resid[keep])), 1)[0])
    return dict(Uinf=float(Uinf), C=float(C), r2=r2, resid_exp=p,
                f_exp=p - 1.0, npts=int(m.sum()))


# ---------------- gate G0: the N-3 anchor ----------------
def gate_g0():
    g = single_grid(24, 6.0)
    th = B_STAR * np.exp(-((g["r1"] / R_W) ** 2))
    Hs = total_static(th, g)
    ok = abs(Hs - 16.7379) < 0.05
    return dict(H_static=float(Hs), target=16.7379, ok=bool(ok))


# ---------------- the ladder (G1, G2, G3) ----------------
def run_ladder():
    out = {}
    for n, L in ((24, 6.0), (32, 8.0), (48, 12.0)):
        h = 2 * L / (n - 1)
        dmax_phys = min(2 * (L - 4 * h), 0.9 * L)
        mmax = int(dmax_phys / (2 * h))
        ds = [2 * m * h for m in range(4, mmax + 1)]
        while len(ds) < 4:            # small-box extension (cores stay >= 2h
            mmax += 1                  # inside the interior mask; disclosed)
            ds.append(2 * mmax * h)
        gs = single_grid(n, L)
        thAs = theta_clock(gs["r1"], M_STAR)
        EM_s, GEM_s = sectors(gs, thAs)
        EM_s0, GEM_s0 = sectors(gs, np.zeros_like(gs["r1"]))
        rows = []
        for d in ds:
            gp = pair17_grid(n, L, d)
            EMp, GEMp = sectors(gp, theta_shared(gp, d))
            rows.append(dict(d=round(float(d), 4),
                             U_gem=float(GEMp - 2 * GEM_s),
                             U_em=float(EMp - 2 * EM_s)))
        R = np.array([[r["d"], r["U_gem"], r["U_em"]] for r in rows])
        fit = fit_Ud(R[:, 0], R[:, 1], float(R[:, 0].min()), float(R[:, 0].max()))
        out[n] = dict(L=L, h=float(h), rows=rows, fit=fit,
                      GEM_single=float(GEM_s), GEM_b0=float(GEM_s0))
        print(f"  {n}^3 L={L}: U_gem = {fit['Uinf']:+8.2f} + {fit['C']:+8.2f}/d"
              f"  R2={fit['r2']:.5f}  F exp {fit['f_exp']:+.3f}  (b0 null {GEM_s0:.1e})",
              flush=True)
    return out


# ---------------- the controls (G4, G5, G6, G7) ----------------
def run_controls():
    n, L = 41, 20.0
    ds = np.array([4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0])
    out = {}

    def sweep(q2=1.0, a0=M_STAR, corrupt=None):
        gs = single_grid(n, L)
        EM_s, GEM_s = sectors(gs, theta_clock(gs["r1"], a0))
        rows = []
        for d in ds:
            gp = pair17_grid(n, L, float(d), q2=q2)
            EMp, GEMp = sectors(gp, theta_shared(gp, float(d), a0, corrupt))
            rows.append((float(d), GEMp - 2 * GEM_s, EMp - 2 * EM_s))
        R = np.array(rows)
        return R, fit_Ud(R[:, 0], R[:, 1], 6.0, 16.0)

    # G6: coupling scan
    scan = {}
    for a0 in (0.05, 0.1026, 0.15, 0.20):
        _, fit = sweep(a0=a0)
        scan[a0] = dict(C=fit["C"], ratio=fit["C"] / float(np.sinh(a0) ** 2),
                        f_exp=fit["f_exp"])
        print(f"  a0={a0:.4f}: C={fit['C']:+9.2f}  C/sinh^2={scan[a0]['ratio']:+9.1f}"
              f"  F exp {fit['f_exp']:+.3f}", flush=True)
    ratios = [v["ratio"] for k, v in scan.items() if k >= 0.1]
    out["coupling_scan"] = dict(scan={str(k): v for k, v in scan.items()},
                                spread=float((max(ratios) - min(ratios)) / abs(np.mean(ratios))))

    # G4: anti-pair
    Ranti, fitanti = sweep(q2=-1.0)
    Rlike, fitlike = sweep(q2=+1.0)
    out["antipair"] = dict(fit_gem=fitanti)
    (Uinf_em, C_em), *_ = np.linalg.lstsq(
        np.stack([np.ones(len(ds)), 1.0 / ds], 1), Ranti[:, 2], rcond=None)
    out["antipair"]["fit_em"] = dict(Uinf=float(Uinf_em), C=float(C_em))
    print(f"  anti-pair: C_gem={fitanti['C']:+8.2f} (like {fitlike['C']:+8.2f}),"
          f" C_em={C_em:+8.2f}", flush=True)

    # G5: mutation
    Rmut, fitmut = sweep(corrupt="clock2")
    out["mutation"] = dict(fit=fitmut, collapse=float(fitlike["C"] / fitmut["C"]))
    print(f"  mutation: C={fitmut['C']:+8.2f}  collapse factor {out['mutation']['collapse']:.2f}",
          flush=True)

    # G7: mixing-free uniaxial class (the M5.17 code path)
    sys.path.insert(0, str(HERE))
    from m5_17_two_charge import pair_field
    from m5_17_energy import hedgehog_field

    def ugem_uniax(g, M17, theta):
        M = np.einsum("...ac,...cd,...bd->...ab", boost_field(theta, A_BOOST), M17,
                      boost_field(theta, A_BOOST))
        _, gEM = u_sectors(M, g["h"])
        return float(gEM[g["act"]].sum()) * g["h"] ** 3

    gs = single_grid(n, L)
    Ms = hedgehog_field(gs["rho"], gs["Z"], 2 * RC)
    GEM_s = ugem_uniax(gs, Ms, theta_clock(gs["r1"], M_STAR))
    maxgem = 0.0
    for d in (6.0, 12.0):
        gp = pair17_grid(n, L, d)
        Mp = pair_field(gp["rho"], gp["Z"], d, 2 * RC, 1)
        maxgem = max(maxgem, abs(ugem_uniax(gp, Mp, theta_shared(gp, d)) - 2 * GEM_s))
    out["mixing_free"] = dict(residual=float(maxgem), single_GEM=float(GEM_s))
    print(f"  mixing-free uniaxial: |U_gem| <= {maxgem:.2e} (exact-zero control)", flush=True)
    return out


# ---------------- G8: the relaxed-shared-field mediation ----------------
def _smooth(a, sigma):
    import scipy.ndimage as ndi
    return ndi.gaussian_filter(a, sigma)


def run_mediation():
    n, L = 32, 8.0
    h = 2 * L / (n - 1)
    ds = [2 * m * h for m in range(4, 8)]

    def relax(g, d, iters=400):
        pin = (g["r1"] <= R_PIN) if d == 0 else ((g["r1"] <= R_PIN) | (g["r2"] <= R_PIN))
        th0 = theta_shared(g, d)
        th = th0.copy()
        v = np.zeros_like(th)
        dt, alpha = 0.02, 0.1
        E = np.inf
        G = np.zeros((4, 4))
        G[A_BOOST, 0] = G[0, A_BOOST] = 1.0
        for _ in range(iters):
            M = M_of(th, g["O4"])
            Mi = [central(M, ax, g["h"]) for ax in range(3)]
            u = 0.0
            Fm = {}
            for i in range(3):
                for j in range(i + 1, 3):
                    F = np_commf(Mi[i], Mi[j])
                    Fm[(i, j)] = F
                    u = u + 2.0 * np.einsum("...ab,...ab->...", F, tw(F))
            E = float((u + BETA_SAT * u * u)[g["act"]].sum()) * g["h"] ** 3
            phip = (1.0 + 2.0 * BETA_SAT * u) * g["act"]
            P = [np.zeros_like(M) for _ in range(3)]
            for (i, j), F in Fm.items():
                Pf = 4.0 * phip[..., None, None] * tw(F)
                P[i] += np_commf(Pf, Mi[j])
                P[j] -= np_commf(Pf, Mi[i])
            G_M = -sum(central(P[i], i, g["h"]) for i in range(3))
            # dM/dtheta = O4 {G_a, B D B^T} O4^T  (validated adjoint ~1e-9)
            Bm = boost_field(th, A_BOOST)
            Me = conj(Bm, D4)
            Gb = np.broadcast_to(G, Me.shape)
            ant = (np.einsum("...ac,...cb->...ab", Gb, Me)
                   + np.einsum("...ac,...cb->...ab", Me, Gb))
            O = g["O4"]
            S = np.einsum("...ac,...cb,...db->...ad", O, ant, O)
            gr = np.einsum("...ab,...ab->...", G_M, S) * g["h"] ** 3
            gr = np.where(pin, 0.0, gr)
            gn = float(np.linalg.norm(gr))
            if gn < 1e-6:
                break
            d_dir = -_smooth(gr, 2.0)
            v = _smooth(v + dt * d_dir, 1.0)
            th = np.clip(th + dt * v, -0.6, 0.6)
            th = np.where(pin, th0, th)
        return th, E

    gs = single_grid(n, L)
    th_s, E_s = relax(gs, 0.0)
    EM_s, GEM_s = sectors(gs, th_s)
    rows = []
    for d in ds:
        gp = pair17_grid(n, L, d)
        th_p, E_p = relax(gp, d)
        EMp, GEMp = sectors(gp, th_p)
        rows.append((float(d), GEMp - 2 * GEM_s, EMp - 2 * EM_s))
    R = np.array(rows)
    fit = fit_Ud(R[:, 0], R[:, 1], float(R[:, 0].min()), float(R[:, 0].max()))
    return dict(rows=R.tolist(), fit=fit)


# ---------------- G9: the forward-stencil twin ----------------
def _fwd(f, ax, h):
    return (np.roll(f, -1, axis=ax) - f) / h


def run_fwd_twin():
    n, L = 48, 12.0
    h = 2 * L / (n - 1)
    ds = [2 * m * h for m in range(4, 12)]

    def sectors_fwd(g, theta):
        M = M_of(theta, g["O4"])
        Mi = [_fwd(M, ax, g["h"]) for ax in range(3)]
        uGEM = 0.0
        uEM = 0.0
        for i in range(3):
            for j in range(i + 1, 3):
                F = np_commf(Mi[i], Mi[j])
                uEM += 4.0 * sum(F[..., a, b] ** 2 for a, b in SP_PAIRS)
                uGEM -= 4.0 * sum(F[..., a, b] ** 2 for a, b in TM_PAIRS)
        act = g["act"]
        v = g["h"] ** 3
        return float(uEM[act].sum()) * v, float(uGEM[act].sum()) * v

    gs = single_grid(n, L)
    EM_s, GEM_s = sectors_fwd(gs, theta_clock(gs["r1"], M_STAR))
    rows = []
    for d in ds:
        gp = pair17_grid(n, L, d)
        EMp, GEMp = sectors_fwd(gp, theta_shared(gp, d))
        rows.append((float(d), GEMp - 2 * GEM_s, EMp - 2 * EM_s))
    R = np.array(rows)
    return dict(rows=R.tolist(), fit=fit_Ud(R[:, 0], R[:, 1], 4.0, 10.9))


def main():
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = {"m_star": M_STAR, "g_time": G_TIME, "delta": DELTA, "beta": BETA_SAT,
           "R_W": R_W, "b_star": B_STAR, "r_pin": R_PIN}
    g0 = gate_g0()
    print(f"[G0] N-3 anchor: H_static = {g0['H_static']:.4f} (target {g0['target']})"
          f"  {'PASS' if g0['ok'] else 'FAIL'}", flush=True)
    out["G0"] = g0
    if not g0["ok"]:
        print("seed does not reproduce the record — ABORT")
        return 1
    if mode in ("ladder", "all"):
        print("[ladder] 24^3 -> 48^3 ...", flush=True)
        out["ladder"] = run_ladder()
    if mode in ("controls", "all"):
        print("[controls] ...", flush=True)
        out["controls"] = run_controls()
    if mode in ("mediation", "all"):
        print("[mediation] relaxed shared field at 32^3 ...", flush=True)
        out["mediation"] = run_mediation()
        print(f"  relaxed: C={out['mediation']['fit']['C']:+.2f},"
              f" F exp {out['mediation']['fit']['f_exp']:+.3f}", flush=True)
    if mode in ("all",):
        print("[audit] forward-stencil twin at 48^3 ...", flush=True)
        out["fwd_twin"] = run_fwd_twin()
        f = out["fwd_twin"]["fit"]
        print(f"  fwd twin: C={f['C']:+.2f}, F exp {f['f_exp']:+.3f}", flush=True)
    out["runtime_s"] = round(time.time() - t0, 1)
    with open(DATA / "m5_96_two_clock_gem_newton.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"done in {out['runtime_s']}s -> data/m5_96_two_clock_gem_newton.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
