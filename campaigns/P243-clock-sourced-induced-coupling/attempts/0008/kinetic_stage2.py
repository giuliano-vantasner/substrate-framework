"""Attempt 0008 stage 2 -- fluctuation kinetic metric about the window root.

PREREGISTRATION (declared before any stage-2 number was computed):

CONSTRUCTION
  On the frozen R=12 order-16 S-family window root, the quadratic kinetic
  Lagrangian of fluctuation velocities is built from the same algebraic
  channel the committed reduction uses for the static curvature density and
  the clock inertia: velocity fields enter as commutators with the
  background spatial gradients,

      T(v) = sum_grid w(r,mu) * 4 * sum_i || [Vdot(r,mu), d_i S_bg] ||_F^2 ,

  with Vdot built from velocity modals through the SAME shape factors as
  coefficient modals, and director frames held fixed (their time variation
  is second order).  M = d^2T/dv^2 is exact: T is quadratic, so
  grad T(v) = M v and the Jacobian of grad T equals M identically.
  Background gradients are formed with coordinate grids requiring grad
  BEFORE the spatial matrix is built (the solve_radial_1d pattern); a
  first implementation that detached them produced M == 0 exactly, which
  is recorded in stdout-stage2-run1.txt as a verifier defect.

DECLARED NORMALIZATION AND EXCLUSIONS
  - Frobenius inner product throughout, matching the committed static
    reduction.  Any overall action normalization cancels from generalized
    eigenvalues because H and M carry it equally.
  - The kappa projector-current term is EXCLUDED (hedgehog reduction not
    established in canon).  Bias direction: omitted positive-semidefinite
    contribution can only move classifications TOWARD "static".

CLASSIFICATION RULES (pre-declared)
  - M gates: symmetry defect < 1e-12 relative; PSD defect < 1e-11.
  - Kinetic floor: Rayleigh quotient below 1e-10 * max-eig(M) => mode is
    CONSTRAINED/STATIC; otherwise PROPAGATING with omega^2 from the
    whitened generalized problem reported.
  - Grid-mode interplay: PROPAGATING weakens (does not kill) the
    grid-artifact suspicion; CONSTRAINED strengthens it.  Full adjudication
    belongs to the independent-discretization route.

GATES (pre-declared)
  G1 symmetry/PSD gates pass.
  G2 omega^2 stability under quadrature refinement <= 5% relative to the
     block scale.
  G3 mutations: R10-root M differs > 10% relative Frobenius; unit q/t/d
     channel Rayleigh quotients pairwise distinct (> 1%).
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "proposals/P240-m5-kinetic-axis/attempts/0041"))

from cpu_energy import (  # noqa: E402
    chebyshev_stack,
    commutator,
    elementwise_derivative,
    frobenius_squared,
    gauss_grid,
)
from solve_radial_1d import Oracle  # noqa: E402

torch.set_num_threads(1)

DTYPE = torch.float64
RADIUS = 12.0
ORDER = 16
BLOCK = 8
BASE_QUAD = (48, 24)
REFINE_QUAD = (64, 32)
KIN_FLOOR_REL = 1e-10
SYMMETRY_TOL = 1e-12
PSD_TOL = 1e-11
STIFF_IDENTITY_RTOL = 0.25
ENERGY_ANOMALY_RTOL = 1e-2


def build_cache(values: np.ndarray, radial_nodes: int, angular_nodes: int):
    """Field construction mirroring solve_radial_1d.energy_radial: the
    coordinate grids require grad BEFORE the spatial matrix forms."""
    coefficients = torch.tensor(values.reshape(3, ORDER), dtype=DTYPE)
    radial, radial_weight, mu, angular_weight = gauss_grid(
        radial_nodes, angular_nodes, RADIUS)
    radius_grid = radial[:, None].repeat(1, angular_nodes).clone()
    radius_grid.requires_grad_(True)
    mu_grid = mu[None, :].repeat(radial_nodes, 1).clone()
    mu_grid.requires_grad_(True)
    x = radius_grid / RADIUS
    basis = chebyshev_stack(2 * x**2 - 1, tuple(range(ORDER)))
    modal = torch.einsum("...i,ci->...c", basis, coefficients)

    q = x**2 + x**2 * (1 - x**2) * modal[..., 0]
    tangent = (1 - x**2) * (
        torch.tensor(1 / 3, dtype=DTYPE) + modal[..., 1])
    delta_amp = x**4 * (1 - x**2) * modal[..., 2]
    sine = torch.sqrt(torch.clamp(1 - mu_grid**2, min=0.0))
    delta = delta_amp * sine**2
    zero = torch.zeros_like(sine)
    director = torch.stack((sine, zero, mu_grid), dim=-1)
    polar = torch.stack((mu_grid, zero, -sine), dim=-1)
    azimuthal = torch.stack((zero, torch.ones_like(zero), zero), dim=-1)

    def outer(vector):
        return vector[..., :, None] * vector[..., None, :]

    lam_n = tangent + q
    spatial = (
        lam_n[..., None, None] * outer(director)
        + (tangent + delta)[..., None, None] * outer(polar)
        + (tangent - delta)[..., None, None] * outer(azimuthal)
    )

    def velocity_matrix(modal_v):
        qd = x**2 * (1 - x**2) * modal_v[..., 0]
        td = (1 - x**2) * modal_v[..., 1]
        dd = x**4 * (1 - x**2) * modal_v[..., 2]
        lam_d = qd + td
        return (
            lam_d[..., None, None] * outer(director)
            + (td + dd)[..., None, None] * outer(polar)
            + (td - dd)[..., None, None] * outer(azimuthal)
        )

    d_r = elementwise_derivative(spatial, radius_grid)
    d_mu = elementwise_derivative(spatial, mu_grid)
    d_theta = (-sine[..., None, None] * d_mu
               / radius_grid[..., None, None])
    rot_z = torch.tensor([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0]], dtype=DTYPE)
    d_phi = ((rot_z @ spatial + spatial @ rot_z.T)
             / (radius_grid * sine)[..., None, None])
    weights = (2 * torch.pi * radius_grid**2
               * radial_weight[:, None] * angular_weight[None, :])
    cache = {
        "radius_grid": radius_grid,
        "velocity_matrix": velocity_matrix,
        "weights": weights,
        "gradients": [g.detach() for g in (d_r, d_theta, d_phi)],
        "grad_norms": [float(g.norm()) for g in (d_r, d_theta, d_phi)],
    }
    return cache


def kinetic_functional(v_flat: torch.Tensor, cache: dict) -> torch.Tensor:
    basis = chebyshev_stack(
        2 * (cache["radius_grid"] / RADIUS)**2 - 1, tuple(range(ORDER)))
    modal_v = torch.einsum("...i,ci->...c",
                           basis, v_flat.reshape(3, ORDER))
    vdot = cache["velocity_matrix"](modal_v)
    total = torch.zeros((), dtype=DTYPE)
    for deriv in cache["gradients"]:
        total = total + frobenius_squared(commutator(vdot, deriv)).sum()
    return 4.0 * (cache["weights"] * total).sum()


def kinetic_hessian(cache: dict) -> np.ndarray:
    def grad_t(v_vector: torch.Tensor):
        x_in = v_vector.clone().requires_grad_(True)
        value = kinetic_functional(x_in, cache)
        return torch.autograd.grad(value, x_in, create_graph=True)[0]

    jac = torch.autograd.functional.jacobian(
        grad_t, torch.zeros(3 * ORDER, dtype=DTYPE))
    return np.asarray(jac.detach().numpy(), dtype=float)


def main():
    started = time.time()
    roots = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                        "attempts/0042/largeR-roots.json").read_text())
    background = np.asarray(roots["R12"]["values"], dtype=float)
    r10 = np.asarray(roots["R10"]["values"], dtype=float)
    checks = []
    report = {
        "attempt": "0008-stage2",
        "preregistration": "module docstring (pre-computation)",
        "excluded_surface": ("kappa projector-current term (bias toward "
                             "STATIC classification)"),
        "checks": checks,
    }

    oracle = Oracle(dict(radial_order=ORDER, radial_nodes=BASE_QUAD[0],
                         angular_nodes=BASE_QUAD[1], radius=RADIUS))
    _, _, hess_bg, _ = oracle.evaluate(background)
    sym_h = (np.asarray(hess_bg) + np.asarray(hess_bg).T) / 2
    lam_h, vec_h = np.linalg.eigh(sym_h)
    lambdas, vectors = lam_h[:BLOCK], vec_h[:, :BLOCK]

    cache = build_cache(background, *BASE_QUAD)
    print(f"[gradients] norms r/theta/phi = "
          f"{['%.3e' % g for g in cache['grad_norms']]}",
          flush=True)
    assert all(g > 0.0 for g in cache["grad_norms"]), \
        "background gradients vanished -- construction bug"
    m_mat = kinetic_hessian(cache)
    asym = float(np.max(np.abs(m_mat - m_mat.T))
                 / max(1.0, np.max(np.abs(m_mat))))
    m_evals, m_evecs = np.linalg.eigh((m_mat + m_mat.T) / 2)
    psd_defect = float(max(0.0, -m_evals.min())
                       / max(1.0, m_evals.max()))
    g1_pass = bool(asym < SYMMETRY_TOL and psd_defect < PSD_TOL)
    checks.append({"name": "M_symmetry_psd", "asymmetry": asym,
                   "psd_defect": psd_defect, "passed": g1_pass})
    print(f"[M] asym={asym:.2e} psd_defect={psd_defect:.2e} "
          f"max_eig={m_evals.max():.6e} "
          f"floor={KIN_FLOOR_REL * m_evals.max():.3e}", flush=True)

    kin_floor = KIN_FLOOR_REL * float(m_evals.max())
    keep = m_evals > kin_floor
    transform = m_evecs[:, keep] / np.sqrt(m_evals[keep])
    h_proj = transform.T @ sym_h @ transform
    omega_sq = np.linalg.eigvalsh((h_proj + h_proj.T) / 2)

    rows = []
    classifications = []
    for idx in range(BLOCK):
        v = vectors[:, idx]
        rayleigh = float(v @ m_mat @ v)
        cls = ("PROPAGATING" if rayleigh > kin_floor
               else "CONSTRAINED/STATIC")
        classifications.append(cls)
        rows.append({
            "mode": idx,
            "stiffness": float(lambdas[idx]),
            "kinetic_rayleigh": rayleigh,
            "classification": cls,
        })
        print(f"[mode {idx}] lam={lambdas[idx]:+.6e} "
              f"m_ray={rayleigh:.6e} -> {cls}", flush=True)
    report["generalized_omega_sq_low"] = \
        [float(w) for w in omega_sq[:min(BLOCK, len(omega_sq))]]
    report["modes"] = rows
    print(f"[omega^2] lowest: "
          f"{['%.4e' % w for w in omega_sq[:5]]}", flush=True)

    cache_r = build_cache(background, *REFINE_QUAD)
    m_ref = kinetic_hessian(cache_r)
    ev_r = np.linalg.eigh((m_ref + m_ref.T) / 2)
    m_evals_r, m_evecs_r = ev_r
    keep_r = m_evals_r > KIN_FLOOR_REL * float(m_evals_r.max())
    tr = m_evecs_r[:, keep_r] / np.sqrt(m_evals_r[keep_r])
    h_pr = tr.T @ sym_h @ tr
    omega_r = np.linalg.eigvalsh((h_pr + h_pr.T) / 2)
    n_cmp = min(len(omega_sq), len(omega_r))
    if n_cmp == 0:
        g2_pass = False
        max_drift = float("nan")
        note = "no propagating subspace at base quadrature"
    else:
        drift = np.abs(omega_r[:n_cmp] - omega_sq[:n_cmp])
        scale_w = max(1.0, float(np.max(np.abs(omega_sq[:n_cmp]))))
        max_drift = float(np.max(drift / scale_w))
        g2_pass = bool(max_drift <= 5e-2)
        note = ""
    checks.append({"name": "omega_sq_refinement_stability",
                   "max_rel_drift": max_drift, "gate": 5e-2,
                   "note": note, "passed": g2_pass})
    print(f"[G2] max_rel_drift={max_drift:.3e} pass={g2_pass}", flush=True)

    cache_m = build_cache(r10, *BASE_QUAD)
    m_r10 = kinetic_hessian(cache_m)
    frob_rel = float(np.linalg.norm(m_r10 - m_mat)
                     / max(1.0, np.linalg.norm(m_mat)))
    rays = {}
    for name, ch in (("q", 0), ("t", 1), ("d", 2)):
        u = np.zeros(3 * ORDER)
        u[ch * ORDER] = 1.0
        rays[name] = float(u @ m_mat @ u)
    vals = sorted(rays.values())
    distinct = bool(min(vals[1] / max(vals[0], 1e-30),
                        vals[2] / max(vals[1], 1e-30)) > 1.01)
    g3_pass = bool(frob_rel > 0.10 and distinct)
    checks.append({"name": "mutations",
                   "r10_frob_rel_diff": frob_rel, "gate_a": 0.10,
                   "channel_rayleigh_q_t_d": rays,
                   "channels_distinct": distinct, "passed": g3_pass})
    print(f"[G3] R10_frob_rel={frob_rel:.3f} rays={rays} pass={g3_pass}",
          flush=True)

    tally = sum(1 for c in checks if c["passed"])
    report["checks"] = checks
    report["tally"] = f"{tally}/{len(checks)} CHECKS PASS"
    report["runtime_seconds"] = round(time.time() - started, 1)
    report["thread_pin"] = "torch.set_num_threads(1)"
    (HERE / "kinetic-stage2.json").write_text(json.dumps(report, indent=1))
    print(report["tally"], flush=True)
    print("[DONE] kinetic-stage2.json written", flush=True)


if __name__ == "__main__":
    main()
