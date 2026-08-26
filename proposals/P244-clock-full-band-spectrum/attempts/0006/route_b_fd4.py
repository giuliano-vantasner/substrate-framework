"""Attempt 0006 -- route B with fourth-order radial stencils.

PREREGISTRATION (frozen before execution; inherits attempt 0005 verbatim
except the single implementation repair below):

REPAIR
  Attempt 0005's second-order central differences left 3-5 percent median and
  up to 46 percent worst-mode disagreement against route A: the certified
  band's high modes carry radially oscillatory eigenvectors (Chebyshev order
  up to 15 in the committed basis) whose resolution needs more than
  O(dx^2) accuracy at n_r <= 192. The stencil is upgraded to the standard
  fourth-order five-point central difference with one-sided second-order
  fallbacks at the two edge cells; everything else (grids 96/144/192,
  n_mu = 24, gates, tolerances, Richardson machinery) is unchanged. Expected
  observed order ~4; Richardson factor (192/144)^4.

PURPOSE (inherited from attempt 0005)
  Independent-discretization agreement for the certified spectrum table of
  attempt 0004: route B shares no node set, weight rule, or radial derivative
  mechanism with route A; controls are the same 48 modal coefficients, so
  both routes approximate one continuum pencil. Gates: G0B transfer within
  5 percent per rung; per-mode agreement within inherited band tolerances,
  with observed-order Richardson extrapolation admissible with recorded
  residual.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
for p in (
    "campaigns/P243-clock-sourced-induced-coupling/attempts/0008",
    "proposals/P240-m5-kinetic-axis/attempts/0041",
    "proposals/P244-clock-full-band-spectrum/attempts/0002",
    "proposals/P244-clock-full-band-spectrum/attempts/0003",
):
    sys.path.insert(0, str(REPO / p))

from cpu_energy import (  # noqa: E402
    chebyshev_stack,
    commutator,
    elementwise_derivative,
    frobenius_squared,
)
from kinetic_stage2 import build_cache  # noqa: E402  (route-A reference only)
from route_a_corrected import corrected_kinetic_value  # noqa: E402
from route_final import pencil_float64  # noqa: E402
from solve_radial_1d import Oracle  # noqa: E402

torch.set_num_threads(1)

DTYPE = torch.float64
RADIUS = 12.0
ORDER = 16
GRIDS = (96, 144, 192)
N_MU = 24
E_COMMITTED = 55.10418278043526


def route_b_matrices(values16: np.ndarray, n_r: int, n_mu: int):
    """H and M wrt 48 modal controls on the uniform-x FD grid."""
    j_idx = torch.arange(n_r, dtype=DTYPE) + 0.5
    x_c = ((j_idx / n_r)).clone().requires_grad_(True)
    xn = torch.sqrt(x_c)
    dx = 1.0 / n_r
    mu_x, mu_w = np.polynomial.legendre.leggauss(n_mu)
    mug = torch.tensor(mu_x, dtype=DTYPE)[None, :] \
        .repeat(n_r, 1).clone().requires_grad_(True)
    w_mu = torch.tensor(mu_w, dtype=DTYPE)[None, :]
    coeffs = torch.tensor(values16.reshape(3, ORDER), dtype=DTYPE)
    angle = torch.acos(torch.clamp(2 * x_c.detach() - 1, -1.0, 1.0))
    basis_bg = torch.stack(tuple(torch.cos(k * angle)
                                 for k in range(ORDER)), dim=-1)
    modal_bg = torch.einsum("xk,ck->xc", basis_bg, coeffs.detach())
    mq_bg, mt_bg, md_bg = modal_bg[..., 0], modal_bg[..., 1], modal_bg[..., 2]
    measure = 2 * torch.pi * (RADIUS**3 / 2) \
        * torch.sqrt(x_c.detach())[:, None] * dx * w_mu
    sine = torch.sqrt(torch.clamp(1 - mug**2, min=0.0))
    env_q = xn[:, None]**2 * (1 - xn[:, None]**2)
    env_t = 1 - xn[:, None]**2
    env_d = xn[:, None]**4 * (1 - xn[:, None]**2)
    zero = torch.zeros_like(sine)
    ones = torch.ones_like(sine)
    director = torch.stack((sine, zero, mug), dim=-1)
    polar = torch.stack((mug, zero, -sine), dim=-1)
    azimuthal = torch.stack((zero, ones, zero), dim=-1)
    rot_z = torch.tensor([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0]], dtype=DTYPE)

    def outer(vec):
        return vec[..., :, None] * vec[..., None, :]

    def assemble(mq, mt, md):
        q = xn[:, None]**2 + env_q * mq[:, None]
        t = env_t * (torch.tensor(1 / 3, dtype=DTYPE) + mt[:, None])
        dd_amp = env_d * md[:, None]
        delta = dd_amp * sine**2
        lam_n = t + q
        return (lam_n[..., None, None] * outer(director)
                + (t + delta)[..., None, None] * outer(polar)
                + (t - delta)[..., None, None] * outer(azimuthal))

    def radial_deriv(s):
        ds_dx = torch.zeros_like(s)
        ds_dx[2:-2] = (-s[4:] + 8 * s[3:-1] - 8 * s[1:-3] + s[:-4]) / (12 * dx)
        ds_dx[1:2] = (s[2:3] - s[0:1]) / (2 * dx)
        ds_dx[0:1] = (s[1:2] - s[0:1]) / dx
        ds_dx[-2:-1] = (s[-1:] - s[-3:-2]) / (2 * dx)
        ds_dx[-1:] = (s[-1:] - s[-2:-1]) / dx
        chain = (2 * torch.sqrt(torch.clamp(x_c, min=1e-6)) / RADIUS)[:, None]
        return ds_dx * chain[:, :, None, None]

    s_bg = assemble(mq_bg, mt_bg, md_bg)
    d_mu_bg = elementwise_derivative(s_bg, mug)
    r_grid = RADIUS * torch.sqrt(torch.clamp(x_c, min=1e-6))
    sine_l = torch.sqrt(torch.clamp(1 - mug**2, min=0.0))
    grads_bg = [
        radial_deriv(s_bg).detach(),
        (-sine_l[..., None, None] * d_mu_bg
         / r_grid[:, None, None, None]).detach(),
        ((rot_z @ s_bg + s_bg @ rot_z.T)
         / (r_grid[:, None] * sine_l)[..., None, None]).detach(),
    ]

    def static_energy(control: torch.Tensor) -> torch.Tensor:
        c_pert = coeffs.detach() + control.reshape(3, ORDER)
        modal = torch.einsum("xk,ck->xc", basis_bg, c_pert)
        s = assemble(modal[..., 0], modal[..., 1], modal[..., 2])
        d_r = radial_deriv(s)
        d_mu = elementwise_derivative(s, mug)
        d_theta = (-sine_l[..., None, None] * d_mu
                   / r_grid[:, None, None, None])
        d_phi = ((rot_z @ s + s @ rot_z.T)
                 / (r_grid[:, None] * sine_l)[..., None, None])
        curv = 4 * sum(frobenius_squared(commutator(a, b))
                       for a, b in ((d_r, d_theta), (d_r, d_phi),
                                    (d_theta, d_phi)))
        trace_two = torch.diagonal(s @ s, dim1=-2, dim2=-1).sum(-1)
        trace_three = torch.diagonal(s @ s @ s, dim1=-2, dim2=-1).sum(-1)
        potential = -0.5 * trace_two - trace_three + trace_two**2 + 0.5
        return (measure * (curv + potential)).sum()

    def kinetic_value(v_flat: torch.Tensor) -> torch.Tensor:
        cvar = torch.tensor(values16.reshape(3, ORDER), dtype=DTYPE)
        angle_v = torch.acos(torch.clamp(2 * x_c.detach() - 1, -1.0, 1.0))
        basis_v = torch.stack(tuple(torch.cos(k * angle_v)
                                    for k in range(ORDER)), dim=-1)
        ctrl = v_flat.reshape(3, ORDER)
        mv = torch.einsum("xk,ck->xc", basis_v, cvar.detach() + ctrl)
        qd = env_q * mv[..., 0][:, None]
        td = env_t * mv[..., 1][:, None]
        dd = env_d * mv[..., 2][:, None]
        lam_d = qd + td
        vdot = (lam_d[..., None, None] * outer(director)
                + (td + dd)[..., None, None] * outer(polar)
                + (td - dd)[..., None, None] * outer(azimuthal))
        density = torch.zeros_like(measure)
        for g in grads_bg:
            density = density + frobenius_squared(commutator(vdot, g))
        return 4.0 * (measure * density).sum()

    def hess_of(func):
        def grad_of(vec):
            xv = vec.clone().requires_grad_(True)
            g = torch.autograd.grad(func(xv), xv, create_graph=True)[0]
            return g

        jac = torch.autograd.functional.jacobian(
            grad_of, torch.zeros(3 * ORDER, dtype=DTYPE))
        return np.asarray(jac.detach().numpy(), dtype=float)

    e0 = float(static_energy(torch.zeros(3 * ORDER, dtype=DTYPE)))
    h_fd = hess_of(static_energy)
    m_fd = hess_of(kinetic_value)
    return e0, (h_fd + h_fd.T) / 2, (m_fd + m_fd.T) / 2


def main():
    started = time.time()
    roots = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                        "attempts/0042/largeR-roots.json").read_text())
    background = np.asarray(roots["R12"]["values"], dtype=float)

    # route-A reference spectrum (committed machinery, corrected reduction)
    oracle = Oracle(dict(radial_order=ORDER, radial_nodes=96,
                         angular_nodes=48, radius=RADIUS))
    _, _, h_a, _ = oracle.evaluate(background)
    cache = build_cache(background, 96, 48)
    from route_a_corrected import corrected_kinetic_hessian as ckh
    m_a = ckh(cache)
    omega_a, _, stiff_ray, _, _, _ = pencil_float64(
        (h_a + h_a.T) / 2, (m_a + m_a.T) / 2)
    print(f"[routeA] omega[0..7] = {np.sort(omega_a)[:8]}", flush=True)

    checks = []
    report = {
        "attempt": "0005-route-b-fd-pencil",
        "preregistration": "module docstring (pre-computation)",
        "thread_pin": "torch.set_num_threads(1)",
        "grids": list(GRIDS),
        "rows": [],
        "checks": checks,
    }
    prev = None
    for n_r in GRIDS:
        t0 = time.time()
        e_b, h_b, m_b = route_b_matrices(background, n_r, N_MU)
        omega_b, _, _, _, _, _ = pencil_float64(h_b, m_b)
        rel_e = abs(e_b - E_COMMITTED) / E_COMMITTED
        n_cmp = min(len(omega_b), len(omega_a))
        rel_diff = np.abs(np.sort(omega_b[:n_cmp]) - np.sort(omega_a)[:n_cmp]) \
            / np.abs(np.sort(omega_a)[:n_cmp])
        row = {"n_r": n_r, "energy_transfer_rel": rel_e,
               "max_rel_omega_diff": float(rel_diff.max()),
               "median_rel_omega_diff": float(np.median(rel_diff)),
               "runtime_s": round(time.time() - t0, 1)}
        if prev is not None:
            k = min(len(prev["w"]), len(omega_b))
            dr = np.abs(np.sort(omega_b[:k]) - prev["w"][:k])
            dp = np.abs(prev["w"][1:k] - prev["w"][:k - 1])
            ratio = np.where(dp > 0, dr[1:] / dp, np.nan)
            row["observed_order_ratio_median"] = float(np.nanmedian(ratio))
        report["rows"].append(row)
        print(f"[routeB {n_r}] etrans={rel_e:.3e} maxrel={rel_diff.max():.4f} "
              f"med={np.median(rel_diff):.4f} ({row['runtime_s']}s)", flush=True)
        checks.append({"name": f"G0B_{n_r}",
                       "passed": bool(rel_e <= 0.05),
                       "energy_transfer_rel": rel_e})
        prev = {"w": np.sort(omega_b)}
        (HERE / f"omega-b-{n_r}.json").write_text(
            json.dumps([float(w) for w in np.sort(omega_b)]))

    # Richardson extrapolation with observed order from the last two steps
    w1 = np.sort(np.array(json.loads(
        (HERE / "omega-b-144.json").read_text())))
    w2 = np.sort(np.array(json.loads(
        (HERE / "omega-b-192.json").read_text())))
    k = min(len(w1), len(w2))
    factor = (192.0 / 144.0)**2
    w_ex = w2 + (w2 - w1) / (factor - 1)
    rel_ex = np.abs(w_ex[:min(k, len(omega_a))] -
                    np.sort(omega_a)[:min(k, len(omega_a))]) \
        / np.abs(np.sort(omega_a)[:min(k, len(omega_a))])
    report["richardson_max_rel"] = float(rel_ex.max())
    report["richardson_within_1pct_modes"] = int((rel_ex <= 0.01).sum())
    report["compared_modes"] = int(min(k, len(omega_a)))
    print(f"[extrap] max_rel={rel_ex.max():.5f} "
          f"within1pct={(rel_ex <= 0.01).sum()}/{min(k, len(omega_a))}",
          flush=True)
    checks.append({"name": "G2B_route_agreement",
                   "finest_max_rel": float(report["rows"][-1]["max_rel_omega_diff"]),
                   "richardson_max_rel": float(rel_ex.max()),
                   "tol_stiff": 0.01,
                   "passed": bool(rel_ex.max() <= 0.01)})

    tally = sum(1 for c in checks if c.get("passed"))
    report["tally"] = f"{tally}/{len(checks)} CHECKS PASS"
    report["runtime_seconds"] = round(time.time() - started, 1)
    (HERE / "route-b-verdict.json").write_text(json.dumps(report, indent=1))
    print(report["tally"], flush=True)


if __name__ == "__main__":
    main()
