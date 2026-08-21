"""P240 attempt 0044: de-boxing the certified hedgehog (issue #151 Phase 3).

Questions (preregistered in manifest.yaml):
  D2  Does the pinned-wall branch converge, as R grows, to a finite-energy
      de-boxed limit?  Track E(R), I(R), omega(R) along chained roots.
  D3  Is the limit stable?  For each background c(R) extract
      A[c] = nabla^2 V[c]  from the exact identity H(R) = R^3 A + R^-1 D
      (validated two-radius extraction, third-radius reconstruction check)
      and track lambda_min(A[c(R)]).
  T   Tail laws: fit each profile channel's far-field behavior (exponential
      with derived masses sqrt(5), sqrt(3) vs power law).  The derivation
      (derive_vacuum_curvature.py) proved the np/na shear channels are exactly
      potential-flat around the projector background, so only the diagonal
      channels are expected to be exponential.
  G4  Boundary-condition variation at R=8: free wall value for the leading
      profile, q = x^2 (a + (1-x^2) m0(x)), a variational.  With a=1 this is
      EXACTLY the certified family (certification check); the converged a
      measures whether pinning the wall to the rank-1 vacuum value is benign.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch
from scipy.optimize import root

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / ".." / "0041"))
sys.path.insert(0, str(HERE / ".." / "0042"))

from cpu_energy import DTYPE, chebyshev_stack, commutator, elementwise_derivative, gauss_grid  # noqa: E402
from solve_radial_1d import Oracle, analyze_mode, energy_radial  # noqa: E402
from xspace_energy import XOracle  # noqa: E402

RESULTS = HERE / "debox-results.json"
ATTEMPTS = HERE.parent


def extract_A(oracle_x, r1, r2, r_check):
    """Validated two-radius extraction of A from H(R) = R^3 A + R^-1 D."""
    _, H1 = oracle_x.hessian_at(r1)
    _, H2 = oracle_x.hessian_at(r2)
    A = (r2**-1 * np.asarray(H1) - r1**-1 * np.asarray(H2)) / (r1**3 / r2 - r2**3 / r1)
    _, Hc = oracle_x.hessian_at(r_check)
    recon = float(np.abs((r_check**3 * A + r_check**-1 * (np.asarray(H1) - r1**3 * A) * r1) - np.asarray(Hc)).max())
    return (A + A.T) / 2, recon



def project_root(values, order_from, order_to, n_x=4001):
    """Reproject modal coefficients m_k(x) = sum_i c_ki T_i(2x^2-1) to order_to."""
    c = np.asarray(values).reshape(3, order_from)
    x = np.linspace(0.0, 1.0, n_x)
    angle = np.arccos(np.clip(2 * x**2 - 1, -1.0, 1.0))
    b_old = np.cos(np.multiply.outer(angle, np.arange(order_from)))
    b_new = np.cos(np.multiply.outer(angle, np.arange(order_to)))
    m = b_old @ c.T                      # (n_x, 3) profile functions
    c_new, *_ = np.linalg.lstsq(b_new, m, rcond=None)
    return c_new.T.ravel()


def solve_radius(order, seed, radius, radial_nodes=32, angular_nodes=16):
    settings = dict(radial_nodes=radial_nodes, angular_nodes=angular_nodes,
                    radius=radius, radial_order=order)
    oracle = Oracle(settings)
    # fixed normalisation: the SEED energy, not the running energy
    e_seed = float(
        energy_radial(torch.tensor(np.asarray(seed, dtype=np.float64)), **settings)[0]
    )
    scale = max(1.0, min(abs(e_seed), 1e4)) if np.isfinite(e_seed) else 1e2

    def residual(v):
        total, grad, _, _ = oracle.evaluate(v)
        return grad / scale

    def jacobian(v):
        _, _, hess, _ = oracle.evaluate(v)
        return hess / scale

    sol = root(residual, seed, jac=jacobian, method="hybr", options=dict(xtol=1e-13, maxfev=300))
    values = np.asarray(sol.x, dtype=np.float64)
    total, grad, hess, comp = oracle.evaluate(values)
    rel_grad = float(np.max(np.abs(grad)) / max(1.0, abs(total)))
    sym = (hess + hess.T) / 2
    eigs = np.linalg.eigvalsh(sym)
    return {
        "radius": radius, "order": order, "success": bool(sol.success),
        "rel_grad": rel_grad, "energy": total,
        "inertia": comp["inertia"], "omega": comp["frequency"], "curvature": comp["curvature"], "potential": comp["potential"],
        "lambda_min_branch": float(eigs[0]),
        "values": values,
    }


def profile_arrays(values, order, n_x=4001):
    c = np.asarray(values).reshape(3, order)
    x = np.linspace(1e-6, 1 - 1e-6, n_x)
    angle = np.arccos(np.clip(2 * x**2 - 1, -1.0, 1.0))
    basis = np.cos(np.multiply.outer(angle, np.arange(order)))
    modal = basis @ c.T
    q = x**2 + x**2 * (1 - x**2) * modal[:, 0]
    tangent = (1 - x**2) * (1 / 3 + modal[:, 1])
    split = x**4 * (1 - x**2) * modal[:, 2]
    return x, q, tangent, split


def fit_tail(x, y, asymptote, r, window=(0.75, 0.985)):
    """Fit exponential A e^{-m r} + asym and power B r^-alpha + asym on the tail."""
    m = (x >= window[0]) & (x <= window[1])
    rr, yy = r[m], y[m] - asymptote

    def resid_exp(p):
        A, mm = p
        return A * np.exp(-mm * rr) - yy

    def resid_pow(p):
        B, al = p
        return B * rr**(-al) - yy

    from scipy.optimize import least_squares
    se = least_squares(resid_exp, [yy[0], 2.0], method="lm", max_nfev=20000)
    sp_ = least_squares(resid_pow, [yy[0] * rr[0]**2, 2.0], method="lm", max_nfev=20000)
    re = float(np.abs(se.fun).max())
    rp = float(np.abs(sp_.fun).max())
    return {
        "exp": {"A": float(se.x[0]), "mass": float(se.x[1]), "max_resid": re},
        "pow": {"B": float(sp_.x[0]), "alpha": float(sp_.x[1]), "max_resid": rp},
        "exponential_wins": bool(re < rp),
        "residual_ratio_pow_over_exp": float(rp / max(re, 1e-300)),
    }


def free_wall_energy(flat, *, radial_order, radial_nodes, angular_nodes, radius):
    """Certified evaluator with ONE change: the wall value of q is free.

    q = x^2 * (a + (1 - x^2) m0(x)),  a = flat[-1].
    With a = 1 this spans exactly the certified family (G4 certification).
    """
    coefficients = flat[:-1].reshape(3, radial_order)
    wall_a = flat[-1]
    radial, radial_weight, mu, angular_weight = gauss_grid(radial_nodes, angular_nodes, radius)
    radius_grid = radial[:, None].repeat(1, angular_nodes).clone().requires_grad_(True)
    mu_grid = mu[None, :].repeat(radial_nodes, 1).clone().requires_grad_(True)
    normalized = radius_grid / radius
    radial_coordinate = 2 * normalized**2 - 1
    radial_basis = chebyshev_stack(radial_coordinate, tuple(range(radial_order)))
    modal = torch.einsum("...i,ci->...c", radial_basis, coefficients)

    q = normalized**2 * (wall_a + (1 - normalized**2) * modal[..., 0])
    tangent = (1 - normalized**2) * (
        torch.tensor(1 / 3, dtype=DTYPE, device="cpu") + modal[..., 1]
    )
    split_amplitude = normalized**4 * (1 - normalized**2) * modal[..., 2]
    sine = torch.sqrt(torch.clamp(1 - mu_grid**2, min=0.0))
    delta = split_amplitude * sine**2
    zero = torch.zeros_like(sine)
    director = torch.stack((sine, zero, mu_grid), dim=-1)
    polar = torch.stack((mu_grid, zero, -sine), dim=-1)
    azimuthal = torch.stack((zero, torch.ones_like(zero), zero), dim=-1)
    outer = lambda v: v[..., :, None] * v[..., None, :]
    lambda_n = tangent + q
    spatial = (
        lambda_n[..., None, None] * outer(director)
        + (tangent + delta)[..., None, None] * outer(polar)
        + (tangent - delta)[..., None, None] * outer(azimuthal)
    )
    derivative_r = elementwise_derivative(spatial, radius_grid)
    derivative_mu = elementwise_derivative(spatial, mu_grid)
    derivative_theta = -sine[..., None, None] * derivative_mu / radius_grid[..., None, None]
    rotation_z = torch.tensor(
        [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]], dtype=DTYPE
    )
    derivative_phi = (rotation_z @ spatial + spatial @ rotation_z.T) / (
        radius_grid * sine
    )[..., None, None]
    derivatives = (derivative_r, derivative_theta, derivative_phi)
    static_density = 4 * sum(
        commutator_sq(derivatives[l], derivatives[r])
        for l in range(3) for r in range(l + 1, 3)
    )
    spatial_two = spatial @ spatial
    trace_two = torch.diagonal(spatial_two, dim1=-2, dim2=-1).sum(-1)
    trace_three = torch.diagonal(spatial_two @ spatial, dim1=-2, dim2=-1).sum(-1)
    potential = -0.5 * trace_two - trace_three + trace_two**2 + 0.5
    nx, ny, nz = director.unbind(-1)
    clock_generator = torch.stack(
        (
            torch.stack((zero, -nz, ny), dim=-1),
            torch.stack((nz, zero, -nx), dim=-1),
            torch.stack((-ny, nx, zero), dim=-1),
        ),
        dim=-2,
    )
    clock_response = clock_generator @ spatial + spatial @ clock_generator.transpose(-1, -2)
    inertia_density = 4 * sum(
        commutator_sq(clock_response, d) for d in derivatives
    )
    weights = 2 * torch.pi * radius_grid**2 * radial_weight[:, None] * angular_weight[None, :]
    curvature = torch.sum(weights * static_density)
    potential_energy = torch.sum(weights * potential)
    inertia = torch.sum(weights * inertia_density)
    static = curvature + potential_energy
    fixed_j = 1 / (4 * inertia)
    total = static + fixed_j
    return total, {
        "curvature": curvature, "potential": potential_energy, "static": static,
        "inertia": inertia, "fixed_j": fixed_j, "frequency": 1 / (2 * inertia),
    }


def commutator_sq(a, b):
    from cpu_energy import frobenius_squared
    return frobenius_squared(commutator(a, b))


def main():
    results = {}

    # ---- D2/D3: chained large-R ladder ---------------------------------
    rows = json.loads((ATTEMPTS / "0042" / "largeR-roots.json").read_text())
    seed14 = np.asarray(rows["R14"]["values"])
    # physical-resolution schedule: Chebyshev cutoff 2*pi*R/order must stay
    # ~2.5 core units as in the certified R=8/order-20 chart.
    schedule = ((14.0, seed14, 32), (16.0, None, 38), (20.0, None, 46), (24.0, None, 54))
    ladder = []
    previous = (seed14, seed14.size // 3)
    for radius, seed_override, order in schedule:
        values_prev, order_prev = previous
        seed = (project_root(values_prev, order_prev, order)
                if seed_override is None else project_root(seed_override, order // 2, order))
        row = solve_radius(order, seed, radius)
        ladder.append(row)
        previous = (row["values"], row["order"])
        print(f"R={radius:5.1f} order={row['order']} E={row['energy']:.10f} "
              f"I={row['inertia']:.8f} omega={row['omega']:.8f} "
              f"lam_branch={row['lambda_min_branch']:+.3e} relgrad={row['rel_grad']:.1e}",
              flush=True)
    results["ladder"] = [
        {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in r.items()}
        for r in ladder
    ]

    # resolution gate: recompute the largest-radius background at +8 order
    big_row = ladder[-1]
    order_hi = big_row["order"] + 8
    seed_hi = project_root(ladder[-2]["values"], ladder[-2]["order"], order_hi)
    row_hi = solve_radius(order_hi, seed_hi, big_row["radius"])
    dE = abs(row_hi["energy"] - big_row["energy"]) / abs(big_row["energy"])
    ox_a = XOracle(big_row["values"], big_row["order"], 48, 16)
    ox_b = XOracle(row_hi["values"], order_hi, 48, 16)
    la = float(np.linalg.eigvalsh(extract_A(ox_a, big_row["radius"], 2*big_row["radius"], 1.5*big_row["radius"])[0])[0])
    lb = float(np.linalg.eigvalsh(extract_A(ox_b, big_row["radius"], 2*big_row["radius"], 1.5*big_row["radius"])[0])[0])
    results["resolution_gate_R24"] = {
        "order_base": big_row["order"], "order_hi": order_hi,
        "energy_rel_diff": float(dE),
        "lambda_min_A_base": la, "lambda_min_A_hi": lb,
        "passed": bool(dE < 1e-6),
    }
    print(f"resolution gate R=24: dE/E={dE:.2e} lamA {la:+.3e} vs {lb:+.3e}", flush=True)

    # ---- A-spectrum per background --------------------------------------
    a_rows = []
    for row in ladder:
        ox = XOracle(row["values"], row["order"], 48, 16)
        R = row["radius"]
        A, recon = extract_A(ox, R, 2.0 * R, 1.5 * R)
        eigs = np.linalg.eigvalsh(A)
        vecs = np.linalg.eigh(A)[1][:, 0]
        fr, nodes = analyze_mode(vecs)
        a_rows.append({
            "radius": R, "lambda_min_A": float(eigs[0]),
            "reconstruction_maxdiff": recon,
            "negative_direction_fractions": [float(f) for f in fr],
            "negative_direction_split_nodes": nodes,
        })
        print(f"A[c(R={R})]: lambda_min={eigs[0]:+.6e} recon={recon:.1e} "
              f"fractions={np.round(fr, 5).tolist()}", flush=True)
    results["A_spectrum"] = a_rows

    # quadrature independence at the largest radius (gate G3)
    big = ladder[-1]
    ox2 = XOracle(big["values"], big["order"], 72, 24)
    A2, _ = extract_A(ox2, big["radius"], 2.0 * big["radius"], 1.5 * big["radius"])
    ox1 = XOracle(big["values"], big["order"], 48, 16)
    A1, _ = extract_A(ox1, big["radius"], 2.0 * big["radius"], 1.5 * big["radius"])
    l1 = float(np.linalg.eigvalsh(A1)[0])
    l2 = float(np.linalg.eigvalsh(A2)[0])
    results["quadrature_check"] = {"48x16": l1, "72x24": l2, "absdiff": abs(l1 - l2)}
    print(f"G3 quadrature: {l1:+.8e} vs {l2:+.8e} (diff {abs(l1-l2):.1e})", flush=True)

    # ---- tail laws -------------------------------------------------------
    tails = {}
    for row in ladder[-2:]:
        key = f"R{int(row['radius'])}"
        x, q, t, s = profile_arrays(row["values"], row["order"])
        r = x * row["radius"]
        tails[key] = {
            "lambda_minus_1": fit_tail(x, q, 1.0, r),
            "tangent": fit_tail(x, t, 0.0, r),
            "split": fit_tail(x, s, 0.0, r),
        }
        print(f"tails {key}: lam-1 mass={tails[key]['lambda_minus_1']['exp']['mass']:.3f} "
              f"tan mass={tails[key]['tangent']['exp']['mass']:.3f}", flush=True)
    results["tail_fits"] = tails

    # ---- G4: free-wall variant at R=8 ------------------------------------
    cert = json.loads((ATTEMPTS / "0041" / "radial-results.json").read_text())
    cert_root = np.asarray([r for r in cert if r["radial_order"] == 20][0]["values"])
    # certification: a=1 must reproduce the certified chart exactly
    flat_cert = np.concatenate([cert_root, [1.0]])
    var = torch.tensor(flat_cert, dtype=DTYPE, requires_grad=True)
    total_fw, _ = free_wall_energy(var, radial_order=20, radial_nodes=32,
                                   angular_nodes=16, radius=8.0)
    total_ref, _ = energy_radial(torch.tensor(cert_root, dtype=DTYPE),
                                 radial_order=20, radial_nodes=32,
                                 angular_nodes=16, radius=8.0)
    cert_err = float(abs(total_fw - total_ref) / abs(total_ref))
    print(f"G4 certification (a=1 reproduces certified chart): rel err {cert_err:.2e}",
          flush=True)

    # now free the wall value and relax
    settings = dict(radial_order=20, radial_nodes=32, angular_nodes=16, radius=8.0)

    class FWOracle:
        def __init__(self):
            self.cached_values = None
            self.cached_result = None

        def evaluate(self, values):
            if self.cached_values is not None and np.array_equal(values, self.cached_values):
                return self.cached_result
            variable = torch.tensor(values, dtype=DTYPE, requires_grad=True)
            total, components = free_wall_energy(variable, **settings)
            gradient = torch.autograd.grad(total, variable, create_graph=True)[0]
            hessian = torch.stack(tuple(
                torch.autograd.grad(gradient[i], variable, retain_graph=True)[0]
                for i in range(variable.numel())
            ))
            result = (float(total.detach()), gradient.detach().numpy(),
                      hessian.detach().numpy(),
                      {k: float(v.detach()) for k, v in components.items()})
            self.cached_values = np.array(values, copy=True)
            self.cached_result = result
            return result

    fw = FWOracle()

    def residual(v):
        total, grad, _, _ = fw.evaluate(v)
        return grad / max(1.0, abs(total))

    def jacobian_fw(v):
        _, _, hess, _ = fw.evaluate(v)
        return hess / max(1.0, abs(fw.cached_result[0]))

    sol = root(residual, flat_cert, jac=jacobian_fw, method="hybr",
               options=dict(xtol=1e-13, maxfev=300))
    values_fw = np.asarray(sol.x)
    total, grad, _, comp = fw.evaluate(values_fw)
    rel_grad = float(np.max(np.abs(grad)) / max(1.0, abs(total)))
    results["free_wall_R8"] = {
        "certification_rel_err": cert_err,
        "converged": bool(sol.success),
        "wall_value_a": float(values_fw[-1]),
        "energy": total,
        "inertia": comp["inertia"],
        "omega": comp["frequency"],
        "rel_grad": rel_grad,
        "pinned_reference_energy": float(total_ref),
    }
    print(f"free-wall R=8: a* = {values_fw[-1]:.8f}  E = {total:.8f} "
          f"(pinned {float(total_ref):.8f})  relgrad {rel_grad:.1e}", flush=True)

    RESULTS.write_text(json.dumps(results, indent=2))
    print("wrote debox-results.json")


if __name__ == "__main__":
    main()
