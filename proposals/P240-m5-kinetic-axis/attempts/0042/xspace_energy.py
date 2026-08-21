"""Fixed-quadrature x-space evaluator for attempt 0042.

Rewrites cpu_energy.energy with the radial quadrature placed on x in [0, 1]
ONCE, so that the radius R enters only through exact algebraic factors:

    E(R)[c] = R^3 V[c] + (C[c] + Phi[c]) / R,
    Phi[c] = 1 / (4 I[c]),   I[c] = x-space inertia integral,

with V, C, I computed on fixed nodes (no R anywhere).  The decomposition is
then exact at the discrete level and Hessians can be combined across radii.

Validation obligation: energy_x must converge to cpu_energy.energy under
node refinement (checked in validate_against_cpu()).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / ".." / "0041"))

from cpu_energy import (  # noqa: E402
    DEVICE, DTYPE, chebyshev_stack, commutator, frobenius_squared,
)
def xspace_components(flat, radial_order, radial_nodes, angular_nodes,
                      angular_modes=1):
    coefficients = flat.reshape(3, radial_order, 1)
    xs, wx = np.polynomial.legendre.leggauss(radial_nodes)
    xs = (xs + 1) / 2                      # map to [0, 1]
    wx = wx / 2
    mus, wmu = np.polynomial.legendre.leggauss(angular_nodes)
    xg = torch.tensor(np.tile(xs[:, None], (1, angular_nodes)),
                      dtype=DTYPE, device=DEVICE).requires_grad_(True)
    mg = torch.tensor(np.tile(mus[None, :], (radial_nodes, 1)),
                      dtype=DTYPE, device=DEVICE).requires_grad_(True)
    radial_basis = chebyshev_stack(2 * xg**2 - 1, tuple(range(radial_order)))
    angular_basis = chebyshev_stack(mg, tuple(2 * i for i in range(angular_modes)))
    modal = torch.einsum("...i,cij,...j->...c", radial_basis, coefficients,
                         angular_basis)

    q = xg**2 + xg**2 * (1 - xg**2) * modal[..., 0]
    tangent = (1 - xg**2) * (torch.tensor(1 / 3, dtype=DTYPE, device=DEVICE)
                             + modal[..., 1])
    split_amplitude = xg**4 * (1 - xg**2) * modal[..., 2]
    sine = torch.sqrt(torch.clamp(1 - mg**2, min=0.0))
    zero = torch.zeros_like(sine)
    director = torch.stack((sine, zero, mg), dim=-1)
    polar = torch.stack((mg, zero, -sine), dim=-1)
    azimuthal = torch.stack((zero, torch.ones_like(zero), zero), dim=-1)

    def outer(vector):
        return vector[..., :, None] * vector[..., None, :]

    lambda_n = tangent + q
    # cpu_energy couples the anisotropy through delta = split * sin(mu)^2
    delta = split_amplitude * sine**2
    spatial = (
        lambda_n[..., None, None] * outer(director)
        + (tangent + delta)[..., None, None] * outer(polar)
        + (tangent - delta)[..., None, None] * outer(azimuthal)
    )
    dx = elementwise_derivative_x(spatial, xg)
    # d/dr = (1/R) d/dx ; assemble the x-derivative, apply 1/R later
    dmu = elementwise_derivative_x(spatial, mg)
    dtheta = -sine[..., None, None] * dmu / xg[..., None, None]
    rotation_z = torch.tensor([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0],
                               [0.0, 0.0, 0.0]], dtype=DTYPE, device=DEVICE)
    dphi = (rotation_z @ spatial + spatial @ rotation_z.T) / (xg * sine)[..., None, None]

    static_density = 4 * sum(
        frobenius_squared(commutator(a, b))
        for a, b in ((dx, dtheta), (dx, dphi), (dtheta, dphi)))
    spatial_two = spatial @ spatial
    trace_two = torch.diagonal(spatial_two, dim1=-2, dim2=-1).sum(-1)
    trace_three = torch.diagonal(spatial_two @ spatial, dim1=-2, dim2=-1).sum(-1)
    potential = (-0.5 * trace_two - trace_three + trace_two**2 + 0.5)

    nx, ny, nz = director.unbind(-1)
    clock_generator = torch.stack(
        (torch.stack((zero, -nz, ny), dim=-1),
         torch.stack((nz, zero, -nx), dim=-1),
         torch.stack((-ny, nx, zero), dim=-1)), dim=-2)
    clock_response = (clock_generator @ spatial
                      + spatial @ clock_generator.transpose(-1, -2))
    inertia_density = 4 * sum(
        frobenius_squared(commutator(clock_response, d))
        for d in (dx, dtheta, dphi))

    # measure: r^2 dr = R^3 x^2 dx  -> keep only the x-part
    weights = (2 * torch.pi * xg**2 * torch.tensor(wx, dtype=DTYPE,
                                                   device=DEVICE)[:, None]
               * torch.tensor(wmu, dtype=DTYPE, device=DEVICE)[None, :])
    C = torch.sum(weights * static_density)          # multiplies 1/R
    V = torch.sum(weights * potential)               # multiplies R^3
    I = torch.sum(weights * inertia_density)         # multiplies R^1
    return C, V, I


def elementwise_derivative_x(matrix: torch.Tensor, coordinate: torch.Tensor):
    rows = []
    for left in range(3):
        columns = []
        for right in range(3):
            derivative = torch.autograd.grad(
                matrix[..., left, right].sum(),
                coordinate,
                create_graph=True,
                retain_graph=True,
                allow_unused=True,
            )[0]
            if derivative is None:
                derivative = torch.zeros_like(coordinate)
            columns.append(derivative)
        rows.append(torch.stack(columns, dim=-1))
    return torch.stack(rows, dim=-2)


class XOracle:
    """Value and exact Hessian of E(R) = R^3 V + (C + 1/(4I))/R."""

    def __init__(self, flat, radial_order, radial_nodes, angular_nodes):
        self.flat = np.asarray(flat, dtype=np.float64)
        self.radial_order = radial_order
        self.radial_nodes = radial_nodes
        self.angular_nodes = angular_nodes

    def _components_with_grad(self):
        flat = torch.tensor(self.flat, dtype=DTYPE, device=DEVICE)
        flat.requires_grad_(True)
        C, V, I = xspace_components(flat, self.radial_order,
                                    self.radial_nodes, self.angular_nodes)
        phi = 1 / (4 * I)
        return flat, C, V, phi

    def value_at(self, radius):
        _, C, V, phi = self._components_with_grad()
        return radius**3 * V + (C + phi) / radius

    def parts(self):
        flat, C, V, phi = self._components_with_grad()
        return flat, C, V, phi

    def hessian_at(self, radius):
        flat, C, V, phi = self._components_with_grad()
        target = radius**3 * V + (C + phi) / radius
        grad = torch.autograd.grad(target, flat, create_graph=True)[0]
        n = flat.numel()
        rows = [torch.autograd.grad(grad[i], flat,
                                    retain_graph=(i < n - 1))[0]
                .detach().numpy() for i in range(n)]
        return float(target.detach()), np.asarray(rows)
