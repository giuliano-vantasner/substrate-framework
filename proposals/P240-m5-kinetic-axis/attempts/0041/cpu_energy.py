"""Independent CPU reimplementation of the P240 spectral-Cartan fixed-J hedgehog energy.

Verbatim port of attempts/0036/solve_spectral_cartan_hedgehog_gpu.py `energy()`
with device as a parameter, so the saved 6x5 root can be re-evaluated without CUDA.
Used to certify the reimplementation before the 1D radial reduction.
"""

from __future__ import annotations

import numpy as np
import torch

DTYPE = torch.float64
DEVICE = torch.device("cpu")


def gauss_grid(radial_nodes: int, angular_nodes: int, radius: float):
    radial_x, radial_w = np.polynomial.legendre.leggauss(radial_nodes)
    angular_x, angular_w = np.polynomial.legendre.leggauss(angular_nodes)
    radial = 0.5 * radius * (radial_x + 1.0)
    radial_weight = 0.5 * radius * radial_w
    return (
        torch.tensor(radial, dtype=DTYPE),
        torch.tensor(radial_weight, dtype=DTYPE),
        torch.tensor(angular_x, dtype=DTYPE),
        torch.tensor(angular_w, dtype=DTYPE),
    )


def chebyshev_stack(coordinate: torch.Tensor, degrees: tuple[int, ...]):
    angle = torch.acos(torch.clamp(coordinate, -1.0, 1.0))
    return torch.stack(tuple(torch.cos(degree * angle) for degree in degrees), dim=-1)

def elementwise_derivative(matrix: torch.Tensor, coordinate: torch.Tensor):
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


def commutator(left: torch.Tensor, right: torch.Tensor):
    return left @ right - right @ left


def frobenius_squared(matrix: torch.Tensor):
    return torch.sum(matrix**2, dim=(-2, -1))


def energy(
    flat: torch.Tensor,
    *,
    radial_order: int,
    angular_modes: int,
    radial_nodes: int,
    angular_nodes: int,
    radius: float,
):
    coefficients = flat.reshape(3, radial_order, angular_modes)
    radial, radial_weight, mu, angular_weight = gauss_grid(
        radial_nodes, angular_nodes, radius
    )
    radius_grid = radial[:, None].repeat(1, angular_nodes).clone().requires_grad_(True)
    mu_grid = mu[None, :].repeat(radial_nodes, 1).clone().requires_grad_(True)
    normalized = radius_grid / radius
    radial_coordinate = 2 * normalized**2 - 1
    radial_basis = chebyshev_stack(radial_coordinate, tuple(range(radial_order)))
    angular_basis = chebyshev_stack(
        mu_grid, tuple(2 * index for index in range(angular_modes))
    )
    modal = torch.einsum("...i,cij,...j->...c", radial_basis, coefficients, angular_basis)

    q = normalized**2 + normalized**2 * (1 - normalized**2) * modal[..., 0]
    tangent = (1 - normalized**2) * (torch.tensor(1 / 3, dtype=DTYPE, device=DEVICE) + modal[..., 1])
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


class ExactOracle:
    """Value / exact gradient / exact Hessian on CPU, mirroring attempt 0036."""

    def __init__(self, settings):
        self.settings = settings
        self.cached_values = None
        self.cached_result = None
        self.evaluations = 0

    def evaluate(self, values: np.ndarray):
        if self.cached_values is not None and np.array_equal(values, self.cached_values):
            return self.cached_result
        variable = torch.tensor(values, dtype=DTYPE, device=DEVICE, requires_grad=True)
        total, components = energy(variable, **self.settings)
        gradient = torch.autograd.grad(total, variable, create_graph=True)[0]
        hessian = torch.stack(
            tuple(
                torch.autograd.grad(
                    gradient[index], variable, retain_graph=True
                )[0]
                for index in range(variable.numel())
            )
        )
        result = (
            float(total.detach()),
            gradient.detach().cpu().numpy(),
            hessian.detach().cpu().numpy(),
            {name: float(value.detach()) for name, value in components.items()},
        )
        self.cached_values = np.array(values, copy=True)
        self.cached_result = result
        self.evaluations += 1
        return result


def pad_values(values: np.ndarray, old_shape, new_shape):
    old = values.reshape(3, *old_shape)
    new = np.zeros((3, *new_shape), dtype=np.float64)
    new[:, : old_shape[0], : old_shape[1]] = old
    return new.ravel()
