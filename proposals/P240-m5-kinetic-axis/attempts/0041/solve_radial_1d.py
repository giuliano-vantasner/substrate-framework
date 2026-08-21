"""Kelvin-method validation of the P240 hedgehog: 1D radial reduction + Morse index.

Independent validation for the request in issue #146 comment 5359719475, following
the method proposed by @mlops-kelvin in comment 5360116141: reduce the hedgehog to
spherically symmetric (mu-independent) profiles q(r), t(r), d(r) so the 2D
mesh-transfer/interpolation channel disappears, then certify the Morse index of the
continuum second variation instead of re-estimating it in float64 on a 2D basis.

The angular integration is kept as quadrature; the modals carry radial Chebyshev
structure only.  Stationary points of this 1D functional are exactly the radial ODE
solutions of the continuum problem restricted to the spherically symmetric sector.

For each radial order N we report:
  - convergence of the stationary root,
  - lambda_min of the exact Hessian (discrete Morse index count),
  - centered-energy curvature along the lowest mode (independent corroboration),
  - nodal count of the lowest eigenfunction along r (Sturm oscillation census),
  - field fractions of the lowest mode.
"""

from __future__ import annotations


import json
import sys
from pathlib import Path

import numpy as np
import torch
from scipy.optimize import root

HERE = Path(__file__).resolve().parent
ATTEMPTS = HERE.parent
sys.path.insert(0, str(HERE))

from cpu_energy import (  # noqa: E402
    chebyshev_stack,
    commutator,
    elementwise_derivative,
    frobenius_squared,
    gauss_grid,
)

DTYPE = torch.float64
DEVICE = torch.device("cpu")


def energy_radial(
    flat: torch.Tensor,
    *,
    radial_order: int,
    radial_nodes: int,
    angular_nodes: int,
    radius: float,
):
    coefficients = flat.reshape(3, radial_order)
    radial, radial_weight, mu, angular_weight = gauss_grid(
        radial_nodes, angular_nodes, radius
    )
    radius_grid = radial[:, None].repeat(1, angular_nodes).clone().requires_grad_(True)
    mu_grid = mu[None, :].repeat(radial_nodes, 1).clone().requires_grad_(True)
    normalized = radius_grid / radius
    radial_coordinate = 2 * normalized**2 - 1
    radial_basis = chebyshev_stack(radial_coordinate, tuple(range(radial_order)))
    modal = torch.einsum("...i,ci->...c", radial_basis, coefficients)

    q = normalized**2 + normalized**2 * (1 - normalized**2) * modal[..., 0]
    tangent = (1 - normalized**2) * (
        torch.tensor(1 / 3, dtype=DTYPE, device=DEVICE) + modal[..., 1]
    )
    split_amplitude = normalized**4 * (1 - normalized**2) * modal[..., 2]
    sine = torch.sqrt(torch.clamp(1 - mu_grid**2, min=0.0))
    delta = split_amplitude * sine**2
    zero = torch.zeros_like(sine)
    director = torch.stack((sine, zero, mu_grid), dim=-1)
    polar = torch.stack((mu_grid, zero, -sine), dim=-1)
    azimuthal = torch.stack((zero, torch.ones_like(zero), zero), dim=-1)

    def outer(vector: torch.Tensor):
        return vector[..., :, None] * vector[..., None, :]

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
        [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        dtype=DTYPE,
        device=DEVICE,
    )
    derivative_phi = (
        rotation_z @ spatial + spatial @ rotation_z.T
    ) / (radius_grid * sine)[..., None, None]
    derivatives = (derivative_r, derivative_theta, derivative_phi)
    static_density = 4 * sum(
        frobenius_squared(commutator(derivatives[left], derivatives[right]))
        for left in range(3)
        for right in range(left + 1, 3)
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
        frobenius_squared(commutator(clock_response, derivative))
        for derivative in derivatives
    )

    weights = (
        2
        * torch.pi
        * radius_grid**2
        * radial_weight[:, None]
        * angular_weight[None, :]
    )
    curvature = torch.sum(weights * static_density)
    potential_energy = torch.sum(weights * potential)
    inertia = torch.sum(weights * inertia_density)
    static = curvature + potential_energy
    fixed_j = 1 / (4 * inertia)
    total = static + fixed_j
    return total, {
        "curvature": curvature,
        "potential": potential_energy,
        "static": static,
        "inertia": inertia,
        "fixed_j": fixed_j,
        "frequency": 1 / (2 * inertia),
    }


class Oracle:
    def __init__(self, settings):
        self.settings = settings
        self.cached_values = None
        self.cached_result = None

    def evaluate(self, values: np.ndarray):
        if self.cached_values is not None and np.array_equal(values, self.cached_values):
            return self.cached_result
        variable = torch.tensor(values, dtype=DTYPE, requires_grad=True)
        total, components = energy_radial(variable, **self.settings)
        gradient = torch.autograd.grad(total, variable, create_graph=True)[0]
        hessian = torch.stack(
            tuple(
                torch.autograd.grad(gradient[i], variable, retain_graph=True)[0]
                for i in range(variable.numel())
            )
        )
        result = (
            float(total.detach()),
            gradient.detach().numpy(),
            hessian.detach().numpy(),
            {k: float(v.detach()) for k, v in components.items()},
        )
        self.cached_values = np.array(values, copy=True)
        self.cached_result = result
        return result


def project_seed(radial_order: int):
    """Seed from the angular-degree-0 column of the saved 6x5 P240 root."""
    with np.load(ATTEMPTS / "0040" / "coefficients-order6x5.npz") as z:
        full = z["coefficients"]
    seed = np.zeros((3, radial_order), dtype=np.float64)
    take = min(6, radial_order)
    seed[:, :take] = full[:, :take, 0]
    return seed.ravel()


def analyze_mode(eigenvector: np.ndarray):
    """Field fractions + radial nodal count of an eigenmode at mu=0.5."""
    order = eigenvector.size // 3
    m3 = eigenvector.reshape(3, order)
    fractions = np.linalg.norm(m3, axis=1) ** 2 / np.linalg.norm(eigenvector) ** 2

    x = np.linspace(1e-4, 1.0 - 1e-4, 2001)
    radial_coordinate = 2 * x**2 - 1
    angle = np.arccos(np.clip(radial_coordinate, -1, 1))
    basis = np.cos(np.multiply.outer(angle, np.arange(order)))  # (nx, order)
    profiles = np.einsum("xi,ci->xc", basis, m3)  # perturbation of (q, tangent, split)
    nodes = int(np.sum(np.abs(np.diff(np.sign(profiles[:, 2]))) > 0))
    return fractions, nodes


def centered_curvature(oracle: Oracle, values: np.ndarray, direction: np.ndarray, step: float):
    total0 = oracle.evaluate(values)[0]
    plus = oracle.evaluate(values + step * direction)[0]
    minus = oracle.evaluate(values - step * direction)[0]
    scale = max(1.0, abs(total0))
    return (plus - 2 * total0 + minus) / step**2 / scale


def solve_order(order: int, seed: np.ndarray, settings_base: dict):
    settings = dict(settings_base, radial_order=order)
    oracle = Oracle(settings)

    def residual(v):
        total, grad, _, _ = oracle.evaluate(v)
        return grad / max(1.0, abs(total))

    def jacobian(v):
        _, _, hess, _ = oracle.evaluate(v)
        return hess / max(1.0, abs(oracle.cached_result[0]))

    sol = root(residual, seed, jac=jacobian, method="hybr", options=dict(xtol=1e-14, maxfev=400))
    values = np.asarray(sol.x, dtype=np.float64)
    total, grad, hess, comp = oracle.evaluate(values)
    rel_grad = float(np.max(np.abs(grad)) / max(1.0, abs(total)))
    sym = (hess + hess.T) / 2
    symmetry = float(np.max(np.abs(hess - sym)) / max(1.0, np.max(np.abs(hess))))
    eigenvalues, eigenvectors = np.linalg.eigh(sym)
    lam_min = float(eigenvalues[0])
    index = int(np.sum(eigenvalues < -1e-8 * max(1.0, float(np.max(np.abs(eigenvalues))))))
    fractions, nodes = analyze_mode(eigenvectors[:, 0])
    cc = centered_curvature(oracle, values, eigenvectors[:, 0], 1e-4)
    return {
        "radial_order": order,
        "success": bool(sol.success),
        "energy": total,
        "relative_gradient": rel_grad,
        "hessian_symmetry": symmetry,
        "lambda_min": lam_min,
        "morse_index": index,
        "centered_curvature_scaled": cc,
        "mode_fractions": [float(f) for f in fractions],
        "mode_radial_nodes_split": nodes,
        "components": comp,
        "values": values.tolist(),
    }


def main():
    settings_base = dict(radial_nodes=32, angular_nodes=16, radius=6.0)
    results = []
    previous = None
    for order in (8, 10, 12, 14, 16, 18, 20):
        seed = previous if previous is not None else project_seed(order)
        if seed.size != 3 * order:
            padded = np.zeros(3 * order)
            old = np.asarray(seed).reshape(3, -1)
            padded.reshape(3, order)[:, : old.shape[1]] = old
            seed = padded
        row = solve_order(order, seed, settings_base)
        previous = np.asarray(row["values"])
        results.append(row)
        print(
            f"N={order:2d}  conv={row['success']}  |g|/|E|={row['relative_gradient']:.2e}  "
            f"E={row['energy']:.8f}  inertia={row['components']['inertia']:.6f}  "
            f"omega={row['components']['frequency']:.6f}  "
            f"lambda_min={row['lambda_min']:.6f}  index={row['morse_index']}  "
            f"cc={row['centered_curvature_scaled']:.4f}  nodes={row['mode_radial_nodes_split']}  "
            f"fractions={np.round(row['mode_fractions'], 4).tolist()}",
            flush=True,
        )
    out = HERE / "radial-results.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
