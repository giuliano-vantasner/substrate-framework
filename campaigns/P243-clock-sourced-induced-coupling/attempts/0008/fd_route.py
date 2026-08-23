"""Attempt 0008 fd_route -- independent-discretization adjudication.

PREREGISTRATION (declared before any FD number was computed):

PURPOSE
  Decide, per low-lying mode, PHYSICAL vs GRID ARTIFACT vs INCONCLUSIVE
  using a radial discretization sharing nothing with the Chebyshev-modal
  route: profiles live on a uniform x-grid, the radial derivative is a
  CENTRAL FINITE DIFFERENCE of grid values, while the angular mu-direction
  stays exactly as committed (elementwise_derivative autograd pattern).

EXACT MEASURES AND CHAIN RULE
  x = (r/R)^2 in (0,1); r = R sqrt(x); r^2 dr = (R^3/2) sqrt(x) dx;
  dS/dr = (2 sqrt(x)/R) dS/dx with dS/dx from 2nd-order central
  differences along the grid index (one-sided at the two edge cells).
  Cell-centered nodes x_j = (j+1/2)/N_r, dx = 1/N_r.
  E = sum_{j,k} 2 pi (R^3/2) sqrt(x_j) dx w_k *
      [4 sum_{pairs a<b in (r,theta,phi)} ||[d_a S, d_b S]||_F^2 + V(S)],
  V(S) = -0.5 tr S^2 - tr S^3 + (tr S^2)^2 + 0.5   (as committed).

CONTROLS AND BACKGROUND
  Controls delta m_q/t/d(x_j) enter through the inherited envelope factors
  x^2(1-x^2), (1-x^2), x^4(1-x^2).  Background = R12 order-16 modal root
  sampled onto the grid (constant offset).  Hessian of E wrt the control
  vector at zero = FD second variation; residual gradient reported as a
  diagnostic (sampled point is stationary for the MODAL functional, not
  exactly for the FD one).

LADDER AND DECISION RULE (fixed now)
  N_r in (48, 72, 96), N_mu = 12; bottom block k = 6.
  * PHYSICAL    : last-step eigenvalue change <= 25% AND dominant-channel
    nodal count stable within +-2 across the last step;
  * GRID ARTIFACT: dominant-channel nodal count grows >= 3 per step OR
    eigenvalue grows by >= 4x per step;
  * INCONCLUSIVE: neither signature dominates.
  Gate G0 (transfer sanity): |E_FD(background, N_r=48)/55.1041827804 - 1|
  <= 5%, else NOTHING downstream is read.
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
sys.path.insert(0, str(HERE))

from cpu_energy import (  # noqa: E402
    chebyshev_stack,
    commutator,
    elementwise_derivative,
    frobenius_squared,
)

torch.set_num_threads(1)

DTYPE = torch.float64
RADIUS = 12.0
N_MU = 12
GRIDS = (48, 72, 96)
BLOCK = 6
MODAL_ENERGY = 55.1041827804
G0_TRANSFER_TOL = 0.05


def fd_energy(values16: np.ndarray, n_r: int):
    """Return scalar energy(control_vector) plus a zero-control evaluator."""
    j_idx = torch.arange(n_r, dtype=DTYPE) + 0.5
    x_c = ((j_idx / n_r).clone().requires_grad_(True))
    mu_x, mu_w = np.polynomial.legendre.leggauss(N_MU)
    mug = torch.tensor(mu_x, dtype=DTYPE)[None, :] \
        .repeat(n_r, 1).clone().requires_grad_(True)
    w_mu = torch.tensor(mu_w, dtype=DTYPE)[None, :]
    coeffs = torch.tensor(values16.reshape(3, 16), dtype=DTYPE)
    angle = torch.acos(torch.clamp(2 * x_c.detach()**2 - 1, -1.0, 1.0))
    basis = torch.stack(tuple(torch.cos(k * angle)
                              for k in range(16)), dim=-1)
    modal = torch.einsum("xi,ci->xc", basis, coeffs)
    mq_bg, mt_bg, md_bg = modal[..., 0], modal[..., 1], modal[..., 2]
    w_mu = torch.tensor(mu_w, dtype=DTYPE)[None, :]
    dx = 1.0 / n_r
    measure = 2 * torch.pi * (RADIUS**3 / 2) \
        * torch.sqrt(x_c.detach())[:, None] * dx * w_mu
    sine = torch.sqrt(torch.clamp(1 - mug**2, min=0.0))
    env_q = x_c[:, None]**2 * (1 - x_c[:, None]**2)
    env_t = 1 - x_c[:, None]**2
    env_d = x_c[:, None]**4 * (1 - x_c[:, None]**2)
    zero = torch.zeros_like(sine)
    ones = torch.ones_like(sine)
    director = torch.stack((sine, zero, mug), dim=-1)
    polar = torch.stack((mug, zero, -sine), dim=-1)
    azimuthal = torch.stack((zero, ones, zero), dim=-1)
    rot_z = torch.tensor([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0]], dtype=DTYPE)

    def outer(vec):
        return vec[..., :, None] * vec[..., None, :]

    def spatial_from(mq, mt, md):
        q = x_c[:, None]**2 + env_q * mq
        t = (1 - x_c[:, None]**2) * (torch.tensor(1 / 3, dtype=DTYPE)
                                     + mt)
        dd_amp = x_c[:, None]**4 * (1 - x_c[:, None]**2) * md
        delta = dd_amp * sine**2
        lam_n = t + q
        return (lam_n[..., None, None] * outer(director)
                + (t + delta)[..., None, None] * outer(polar)
                + (t - delta)[..., None, None] * outer(azimuthal))

    def energy(control: torch.Tensor) -> torch.Tensor:
        mq = mq_bg.detach() + control[0:n_r]
        mt = mt_bg.detach() + control[n_r:2 * n_r]
        md = md_bg.detach() + control[2 * n_r:3 * n_r]
        s = assemble(mq, mt, md)
        ds_dx = torch.zeros_like(s)
        ds_dx[1:-1] = (s[2:] - s[:-2]) / (2 * dx)
        ds_dx[0:1] = (s[1:2] - s[0:1]) / dx
        ds_dx[-1:] = (s[-1:] - s[-2:-1]) / dx
        chain = (2 * torch.sqrt(torch.clamp(x_c, min=1e-6))
                 / RADIUS)[:, None]
        d_r = ds_dx * chain[:, :, None, None]
        d_mu = elementwise_derivative(s, mug)
        r_grid = RADIUS * torch.sqrt(torch.clamp(x_c, min=1e-6))
        sine_l = torch.sqrt(torch.clamp(1 - mug**2, min=0.0))
        d_theta = (-sine_l[..., None, None] * d_mu
                   / r_grid[:, None, None, None])
        d_phi = ((rot_z @ s + s @ rot_z.T)
                 / (r_grid[:, None] * sine_l)[..., None, None])
        curv = 4 * sum(
            frobenius_squared(commutator(a, b))
            for a, b in ((d_r, d_theta), (d_r, d_phi),
                         (d_theta, d_phi)))
        trace_two = torch.diagonal(s @ s, dim1=-2, dim2=-1).sum(-1)
        trace_three = torch.diagonal(
            s @ s @ s, dim1=-2, dim2=-1).sum(-1)
        potential = -0.5 * trace_two - trace_three \
            + trace_two**2 + 0.5
        return (measure * (curv + potential)).sum()

    # assemble must close over the SAME graph objects as energy uses:
    def assemble(mq, mt, md):
        q = x_c[:, None]**2 + env_q * mq[:, None]
        t = ((1 - x_c[:, None]**2)
             * (torch.tensor(1 / 3, dtype=DTYPE) + mt[:, None]))
        dd_amp = env_d * md[:, None]
        delta = dd_amp * sine**2
        lam_n = t + q
        return (lam_n[..., None, None] * outer(director)
                + (t + delta)[..., None, None] * outer(polar)
                + (t - delta)[..., None, None] * outer(azimuthal))

    return energy


def analyze(hess: np.ndarray, n_r: int):
    sym = (hess + hess.T) / 2
    values, vectors = np.linalg.eigh(sym)
    block_vals = values[:BLOCK]
    nodes = []
    for idx in range(BLOCK):
        v = vectors[:, idx].reshape(3, n_r)
        counts = [int(np.sum(np.abs(np.diff(np.sign(v[c]))) > 0))
                  for c in range(3)]
        nodes.append(counts)
    return block_vals, vectors[:, :BLOCK], nodes


def run_ladder(values16: np.ndarray):
    rows = []
    prev = None
    for n_r in GRIDS:
        energy = fd_energy(values16, n_r)
        zeros = torch.zeros(3 * n_r, dtype=DTYPE)
        e0 = float(energy(zeros))

        def grad_of(v_vec):
            xv = v_vec.clone().requires_grad_(True)
            val = energy(xv)
            g = torch.autograd.grad(val, xv, create_graph=True)[0]
            return g

        jac = torch.autograd.functional.jacobian(
            grad_of, torch.zeros(3 * n_r, dtype=DTYPE))
        relgrad = float((jac.detach().norm()
                         / max(1.0, abs(e0))).item())
        hess = np.asarray(jac.detach().numpy(), dtype=float)
        vals, vecs, nodes = analyze(hess, n_r)
        row = {"n_r": n_r, "e_fd": e0,
               "relgrad_fd": float(jac.detach().norm().item()) /
               max(1.0, abs(e0)),
               "bottom": [float(v) for v in vals],
               "nodes_per_mode_qtd": nodes}
        if prev is not None:
            la = np.asarray(prev["bottom"])
            lb = np.asarray(row["bottom"])
            row["last_step_rel_change"] = [
                float(abs(b - a) / max(abs(a), 1e-12))
                for a, b in zip(la, lb)]
        rows.append(row)
        print(f"[grid {n_r}] E={e0:.6f} bottom={vals[0]:+.4e} "
              f"relgrad={row['relgrad_fd']:.2e}", flush=True)
        prev = row
    return rows


def main():
    started = time.time()
    roots = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                        "attempts/0042/largeR-roots.json").read_text())
    background = np.asarray(roots["R12"]["values"], dtype=float)

    energy48 = fd_energy(background, GRIDS[0])
    transfer = abs(float(energy48(torch.zeros(3 * GRIDS[0],
                                                dtype=DTYPE)))
                   / MODAL_ENERGY - 1.0)
    g0_pass = bool(transfer <= G0_TRANSFER_TOL)
    print(f"[G0] transfer={transfer:.4f} tol={G0_TRANSFER_TOL} "
          f"pass={g0_pass}", flush=True)
    report = {
        "attempt": "0008-fd-route",
        "preregistration": "module docstring (pre-computation)",
        "g0_transfer_rel": transfer,
        "g0_passed": g0_pass,
        "rows": [],
        "verdicts": {},
        "runtime_seconds": None,
        "thread_pin": "torch.set_num_threads(1)",
    }
    if not g0_pass:
        report["verdicts"]["all"] = \
            "INCONCLUSIVE -- G0 transfer gate failed"
        (HERE / "fd-verdict.json").write_text(json.dumps(report, indent=1))
        print("[STOP] G0 failed; nothing downstream read", flush=True)
        return

    rows = run_ladder(background)
    report["rows"] = rows
    verdicts = {}
    if len(rows) >= 2:
        last = rows[-1]
        changes = last.get("last_step_rel_change", [])
        for idx in range(BLOCK):
            ch = changes[idx] if idx < len(changes) else None
            nd_now = last["nodes_per_mode_qtd"][idx]
            nd_prev = rows[-2]["nodes_per_mode_qtd"][idx]
            d_nodes = max(abs(n - p) for n, p in zip(nd_now, nd_prev))
            grew = any(n - p >= 3 for n, p in zip(nd_now, nd_prev))
            if ch is not None and ch >= 4.0 or grew:
                verdicts[f"mode_{idx}"] = "GRID ARTIFACT"
            elif ch is not None and ch <= 0.25 and d_nodes <= 2:
                verdicts[f"mode_{idx}"] = "PHYSICAL"
            else:
                verdicts[f"mode_{idx}"] = (
                    f"INCONCLUSIVE (change={ch}, d_nodes={d_nodes})")
    report["verdicts"] = verdicts
    report["runtime_seconds"] = round(time.time() - started, 1)
    (HERE / "fd-verdict.json").write_text(json.dumps(report, indent=1))
    for k, v in verdicts.items():
        print(f"[VERDICT {k}] {v}", flush=True)
    print("[DONE] fd-verdict.json written", flush=True)


if __name__ == "__main__":
    main()
