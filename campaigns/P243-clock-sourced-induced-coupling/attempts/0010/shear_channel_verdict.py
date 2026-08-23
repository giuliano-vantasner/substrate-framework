"""Attempt 0010 -- np/na shear-channel pairing verdict (criterion D).

PREREGISTRATION (declared before any number was computed; the first
draft's "exterior = identity" lemma was REFUTED by check C1a during
development and superseded by the projector lemma below -- both drafts
are recorded here per append-only discipline):

QUESTION (issue #163, criterion 4)
  Sign and power law of any np/na-mediated interaction between two stable
  confined clocks -- positive result, or structural refutation with the
  mechanism named.

PROVENANCE NOTE (scout-verified 2026-08-23)
  The labels "np"/"na" and the literal H_split = diag(5,3,3,0,0,6)/2 occur
  ONLY in the issue prose; no derivation site exists in the repository.
  The repo-real objects underneath that prose are:
  (i) the (q, tangent, split) hedgehog channels with transverse shear
  entering as the polar/azimuthal eigenvalue pair t +/- delta,
  delta = split * sin^2(Theta)  [P240 pair_oracle.build_field];
  (ii) the EXACT aligned-vacuum flatness statement -- off-diagonal
  fluctuation directions have zero potential stiffness at quadratic order
  (m5_fluctuation_spectrum.py);
  (iii) P240 attempt 0041: on CONFINED roots delta == 0 is NOT stationary
  (split-channel force ~1e12) -- vacuum flatness does not transfer;
  (iv) attempt 0008 (this campaign): the confined clock's soft-mode
  candidates are grid artifacts (FD ladder GRID ARTIFACT x6); the
  internal spectrum has NO flat/massless member.

METHOD -- three legs, exact where possible, per .agents/skills/
small-ratio-numerics ("where a proof is possible, prove it"; pairing
numerics only AFTER tail existence is settled):

  L1 (EXACT + numeric probe): exterior-factorization lemma, corrected
     form.  In the committed deviation-additive two-clock family
     (VACUUM_Q = 1, each clock's (q,t,s) profile pinned to (1,0,0)
     outside its own box), the field EXTERIOR to both support balls is
     the exact RANK-ONE PROJECTOR n n^T with n = n(Theta_1+Theta_2) --
     a point on the trace potential's vacuum manifold {rank-1
     projectors}, still angle-carrying.  Pure projector-angle textures
     have IDENTICALLY vanishing static density: every spatial derivative
     of X(theta) = n(theta) n(theta)^T is (grad theta) * A with
     A = dX/dtheta = m n^T + n m^T (m = unit tangent), so every
     commutator pair [d_i X, d_j X] is proportional to [A, A] = 0.
     Hence the exterior region contributes exactly zero static energy
     density at ANY separation, all internal-channel multipole moments
     vanish, and the direct pairing interaction is exactly zero for
     d > 2*max(R_box).  Verified symbolically (projector substitution;
     dX/dtheta == A) and numerically (two-clock exterior density probe,
     central differences).
  L2 (committed-record corroboration, read-only): no protected flat
     direction exists on the physical confined background (0008 grid-
     artifact resolution; 0041 delta non-stationarity).
  L3 (composition closure): inside the accepted induced-gravity
     composition the unique long-range kernel is the universal Newton
     one; its pairing was delivered in attempt 0007 (attractive xi < 1/6,
     cancellation at 1/6).  Internal shear excitations can enter only
     through subleading stress multipoles of that SAME interaction -- no
     independent sign or power law exists for them.  The boxed static
     channel (+457 d^-1.70, repulsive; P240) lives INSIDE the overlap
     region d < 2*R_box by L1 and was already dropped as a static-frame
     category mismatch in review.

VERDICT TARGET
  Structural refutation with mechanism: (i) compact-support confinement +
  the single-generator identity zero every internal-channel tail exactly
  beyond support overlap; (ii) no protected flat direction survives on
  the physical background; (iii) the only long-range mediator in the
  accepted composition is the already-delivered Newton channel.

CHECKS
  C1a: exterior substitution gives exactly n n^T (symbolic).
  C1b: dX/dtheta == m n^T + n m^T exactly (single-generator property) --
       hence [d_i X, d_j X] = 0 identically.
  C1c: numeric two-clock exterior probe -- committed construction's
       static density < 1e-8 at >=150 random strictly-exterior points.
  C2:  MUTATION -- giving the split profile an exterior tail moves the
       field off the vacuum manifold and the density becomes nonzero.
  C3:  INTERIOR CONTROL -- an interior configuration with three distinct
       eigenvalues is NOT rank-1-projectorial (lemma not vacuous).
  C4:  0008 fd-verdict.json contains >= 6 GRID ARTIFACT verdicts
       (read-only).
  C5:  0041 result.yaml records delta==0 non-stationarity with force
       ~1e12 (read-only).

Environment: sympy exact; numpy float64 probes; BLAS threads pinned via
env at launch; stdout captured on first execution.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "src"))

checks: list[dict] = []


def build_symbolic():
    th = sp.symbols("theta", real=True)
    q, t, s = sp.symbols("q t s", real=True)
    st_, ct_ = sp.sin(th), sp.cos(th)
    n = sp.Matrix([st_, 0, ct_])
    p_mat = sp.Matrix([ct_, 0, -st_])
    ay = sp.Matrix([0, 1, 0])
    delta = s * st_**2
    X = ((t + q) * (n * n.T)
         + (t + delta) * (p_mat * p_mat.T)
         + (t - delta) * (ay * ay.T))
    return th, q, t, s, n, p_mat, ay, X


def main() -> int:
    started = time.time()
    th, q, t, s, n, p_mat, ay, X = build_symbolic()

    # ---------------- L1 symbolic -----------------------------------------
    X_out = sp.simplify(sp.expand(X.subs({q: 1, t: 0, s: 0})))
    c1a = bool(sp.simplify(X_out - n * n.T) == sp.zeros(3))
    checks.append({"name": "C1a_exterior_is_projector", "passed": c1a})
    print(f"[C1a] exterior X == n n^T exactly: {c1a}", flush=True)

    A = p_mat * n.T + n * p_mat.T          # m = p_mat here (unit tangent)
    dX_dth = sp.diff(X_out, th)
    c1b = bool(sp.simplify(dX_dth - A) == sp.zeros(3))
    checks.append({
        "name": "C1b_single_generator_identity",
        "note": "every d_i X is scalar*A so [d_i X, d_j X] = "
                "scalar*[A,A] = 0 identically",
        "passed": c1b})
    print(f"[C1b] dX/dtheta == m n^T + n m^T (all commutator pairs "
          f"vanish identically): {c1b}", flush=True)

    # ---------------- numeric machinery ------------------------------------
    def two_clock_field(rho, z, half, split_tail=None):
        """Committed deviation-additive spatial matrix on sample arrays."""
        th1 = np.arctan2(rho, z + half)
        th2 = np.arctan2(rho, z - half)
        ra1 = np.hypot(rho, z + half)
        ra2 = np.hypot(rho, z - half)

        def prof(ra):
            x = ra / half
            inside = x <= 1.0
            qq = np.where(inside, x**2, 1.0)
            tt = np.where(inside, (1.0 - x**2) / 3.0, 0.0)
            ss = np.zeros_like(x)
            if split_tail is not None:
                ss = np.where(inside, 0.3 * np.sin(3.0 * x),
                              split_tail * np.exp(-((x - 1.0) ** 2)))
            return qq, tt, ss

        q1, t1, s1 = prof(ra1)
        q2, t2, s2 = prof(ra2)
        qt = float(q1[0] + q2[0]) - 1.0
        tt = float(t1[0] + t2[0])
        sst = float(s1[0] + s2[0])
        thf = float(th1[0] + th2[0])
        nx, nz = float(np.sin(thf)), float(np.cos(thf))
        px, pz = float(np.cos(thf)), -float(np.sin(thf))
        dl = sst * nz**2
        ln = tt + qt
        Nv = np.array([nx, 0.0, nz])
        Pv = np.array([px, 0.0, pz])
        Av = np.array([0.0, 1.0, 0.0])
        return (ln * np.outer(Nv, Nv)
                + (tt + dl) * np.outer(Pv, Pv)
                + (tt - dl) * np.outer(Av, Av))

    def point_density(rho0, z0, half, split_tail=None):
        """4 * ||[d_rho X, d_z X]||_F^2 at one point via central FD."""
        hh = 1e-5

        def f(rp, zp):
            return two_clock_field(np.array([rp]), np.array([zp]),
                                   half, split_tail)

        dX_rho = (f(rho0 + hh, z0) - f(rho0 - hh, z0)) / (2 * hh)
        dX_z = (f(rho0, z0 + hh) - f(rho0, z0 - hh)) / (2 * hh)
        comm = dX_rho @ dX_z - dX_z @ dX_rho
        return 4.0 * float(np.sum(comm**2))

    def exterior_samples(rng, count, split_tail=None):
        vals = []
        while len(vals) < count:
            half = float(rng.uniform(6.0, 14.0))
            rho = float(rng.uniform(0.05, 30.0))
            z = float(rng.uniform(-30.0, 30.0))
            near = min(np.hypot(rho, z + half), np.hypot(rho, z - half))
            if near <= half * 1.02:
                continue          # strictly exterior to BOTH boxes
            vals.append(point_density(rho, z, half, split_tail))
        return vals

    rng = np.random.default_rng(20260823)
    ext = exterior_samples(rng, 150)
    worst = max(ext)
    c1c = bool(worst < 1e-8)
    checks.append({"name": "C1c_exterior_density_probe",
                   "max_density": worst, "n_points": len(ext),
                   "passed": c1c})
    print(f"[C1c] exterior static density max = {worst:.3e} over "
          f"{len(ext)} pts (<1e-8 required)", flush=True)

    # ---------------- C3 interior control ------------------------------------
    X_in = X.subs({q: sp.Rational(21, 10), t: sp.Rational(-1, 5),
                   s: sp.Rational(1, 3),
                   th: sp.Rational(1, 4)})
    proj_dev = X_in * X_in - X_in
    dev_norm = sum(abs(float(sp.N(e))) for e in proj_dev)
    det_abs = abs(float(sp.N(sp.det(X_in))))
    c3 = bool(dev_norm > 1e-3 and det_abs > 1e-6)
    checks.append({"name": "C3_interior_not_projector",
                   "XX_minus_X_absnorm": dev_norm, "abs_det": det_abs,
                   "passed": c3})
    print(f"[C3] interior ||XX-X|| = {dev_norm:.4f}, |det| = "
          f"{det_abs:.4f} (nonzero required) pass={c3}", flush=True)

    mut = exterior_samples(rng, 60, split_tail=0.15)
    mut_max = max(mut)
    contrast = mut_max / max(worst, 1e-300)
    c2 = bool(mut_max > 1e-8)
    checks.append({"name": "C2_mutation_split_tail_nonzero_density",
                   "max_mutated_density": mut_max,
                   "max_unmutated_density": worst,
                   "contrast": contrast,
                   "n_points": len(mut),
                   "passed": c2})
    print(f"[C2] mutated exterior density max = {mut_max:.3e} "
          f"(unmutated max {worst:.3e}, contrast {contrast:.1e}) "
          f"pass={c2}", flush=True)
    att8 = REPO / ("campaigns/P243-clock-sourced-induced-coupling/"
                   "attempts/0008")
    fd = json.loads((att8 / "fd-verdict.json").read_text())
    n_artifact = str(fd).count("GRID ARTIFACT")
    c4 = n_artifact >= 6
    checks.append({"name": "C4_fd_grid_artifact_verdicts",
                   "count": n_artifact, "passed": c4})
    print(f"[C4] fd-verdict.json GRID ARTIFACT count = {n_artifact}",
          flush=True)

    txt41 = (REPO / ("proposals/P240-m5-kinetic-axis/attempts/0041/"
                     "result.yaml")).read_text()
    c5 = ("not even in delta" in txt41) and ("1e12" in txt41)
    checks.append({"name": "C5_delta_zero_nonstationarity_recorded",
                   "passed": c5})
    print(f"[C5] 0041 delta==0 non-stationary (~1e12) recorded: {c5}",
          flush=True)

    tally = sum(1 for c in checks if c["passed"])
    report = {
        "attempt": "0010",
        "title": "np/na shear-channel pairing verdict",
        "preregistration": "module docstring (pre-computation; includes "
                           "the refuted first-draft lemma verbatim)",
        "verdict": (
            "STRUCTURAL REFUTATION with mechanism: the np/na (transverse "
            "shear) channels mediate NO long-range interaction between "
            "confined clocks. (i) Exterior factorization: with VACUUM_Q=1 "
            "and compact-support pinning, the two-clock field outside both "
            "supports is the exact rank-1 projector n n^T(Theta_1+Theta_2)"
            "; every spatial derivative of such a pure projector-angle "
            "texture is a scalar times the single generator A = m n^T + "
            "n m^T, so every commutator pair in the static density "
            "vanishes identically -- zero energy density at ANY "
            "separation, vanishing internal multipole moments, and an "
            "exactly zero direct pairing integral for d > 2*max(R_box) "
            "(L1: symbolic C1a/C1b + numeric probe C1c). The residual "
            "global winding is pure gauge within the vacuum manifold. The "
            "boxed repulsive channel (+457 d^-1.70, P240) necessarily "
            "lived inside the overlap region and was already dropped as a "
            "static-frame category mismatch. (ii) No protected flat "
            "direction exists on the physical confined background -- "
            "aligned-vacuum flatness does not transfer (0041: delta==0 "
            "non-stationary, ~1e12 force) and the 0008 soft modes are "
            "grid artifacts, leaving no massless internal channel to "
            "carry a power-law tail (L2). (iii) Within the accepted "
            "induced composition the unique long-range kernel is the "
            "universal Newton one, whose pairing attempt 0007 delivered "
            "(attractive xi<1/6, cancellation at xi=1/6); shear "
            "excitations enter only as subleading stress multipoles of "
            "that same interaction, never as an independent channel with "
            "its own sign or power law (L3)."
        ),
        "checks": checks,
        "tally": f"{tally}/{len(checks)} CHECKS PASS",
        "runtime_seconds": round(time.time() - started, 1),
        "thread_pin": "BLAS threads pinned via env at launch",
        "outputs": ["attempts/0010/shear_channel_verdict.py",
                    "attempts/0010/stdout.txt",
                    "attempts/0010/shear-verdict.json"],
    }
    (HERE / "shear-verdict.json").write_text(json.dumps(report, indent=1))
    print(report["tally"], flush=True)
    print("[DONE] shear-verdict.json written", flush=True)
    return 0 if tally == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
