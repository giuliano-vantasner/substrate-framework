"""Direct smooth fixed-J spectral-Cartan hedgehog solve on PyTorch 2.4 CUDA."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import root
import torch


HERE = Path(__file__).resolve().parent
DEVICE = torch.device("cuda")
DTYPE = torch.float64


def gauss_grid(radial_nodes: int, angular_nodes: int, radius: float):
    radial_x, radial_w = np.polynomial.legendre.leggauss(radial_nodes)
    angular_x, angular_w = np.polynomial.legendre.leggauss(angular_nodes)
    radial = radius * (radial_x + 1.0) / 2.0
    radial_weight = radius * radial_w / 2.0
    return tuple(
        torch.tensor(value, dtype=DTYPE, device=DEVICE)
        for value in (radial, radial_weight, angular_x, angular_w)
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
        torch.cuda.synchronize()
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


def initial_values(radial_order: int, angular_modes: int):
    values = np.zeros((3, radial_order, angular_modes), dtype=np.float64)
    values[2, 0, 0] = 0.5
    return values.ravel()


def pad_values(values: np.ndarray, old_shape, new_shape):
    old = values.reshape(3, *old_shape)
    new = np.zeros((3, *new_shape), dtype=np.float64)
    new[:, : old_shape[0], : old_shape[1]] = old
    return new.ravel()


def deterministic_directions(size: int):
    indices = np.arange(size, dtype=np.float64) + 1
    rows = []
    for frequency in (0.37, 0.71, 1.13):
        row = np.sin(frequency * indices) + 0.4 * np.cos((frequency + 0.23) * indices)
        rows.append(row / np.linalg.norm(row))
    return rows


def energy_value(values: np.ndarray, settings):
    variable = torch.tensor(values, dtype=DTYPE, device=DEVICE)
    total, _ = energy(variable, **settings)
    torch.cuda.synchronize()
    return float(total.detach())


def main() -> int:
    if torch.__version__ < "2.4":
        raise RuntimeError("PyTorch 2.4 or newer is required")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for this frozen run")
    settings = {
        "radial_order": 4,
        "angular_modes": 3,
        "radial_nodes": 24,
        "angular_nodes": 20,
        "radius": 6.0,
    }
    initial = initial_values(settings["radial_order"], settings["angular_modes"])
    oracle = ExactOracle(settings)
    initial_energy, initial_gradient, _, initial_components = oracle.evaluate(initial)
    residual_scale = max(1.0, abs(initial_energy))

    def residual(values):
        return oracle.evaluate(values)[1] / residual_scale

    def jacobian(values):
        return oracle.evaluate(values)[2] / residual_scale

    solved = root(
        residual,
        initial,
        jac=jacobian,
        method="hybr",
        options={"xtol": 1.0e-11, "maxfev": 120},
    )
    values = np.asarray(solved.x, dtype=np.float64)
    total, gradient, hessian, components = oracle.evaluate(values)
    gradient_relative = float(np.max(np.abs(gradient)) / max(1.0, abs(total)))
    hessian_symmetry = float(
        np.max(np.abs(hessian - hessian.T))
        / max(1.0, np.max(np.abs(hessian)))
    )
    eigenvalues = np.linalg.eigvalsh((hessian + hessian.T) / 2)
    step = 2.0e-5
    directional = []
    for direction in deterministic_directions(values.size):
        plus = energy_value(values + step * direction, settings)
        minus = energy_value(values - step * direction, settings)
        directional.append(abs((plus - minus) / (2 * step)) / max(1.0, abs(total)))

    withheld_settings = dict(settings, radial_order=5, angular_modes=4)
    withheld_values = pad_values(values, (4, 3), (5, 4))
    withheld_oracle = ExactOracle(withheld_settings)
    withheld_total, withheld_gradient, _, withheld_components = withheld_oracle.evaluate(
        withheld_values
    )
    withheld_gradient_relative = float(
        np.max(np.abs(withheld_gradient)) / max(1.0, abs(withheld_total))
    )

    quadrature_settings = dict(settings, radial_nodes=32, angular_nodes=28)
    quadrature_oracle = ExactOracle(quadrature_settings)
    quadrature_total, quadrature_gradient, _, quadrature_components = quadrature_oracle.evaluate(values)
    quadrature_energy_change = abs(quadrature_total - total) / max(
        1.0, abs(total), abs(quadrature_total)
    )
    quadrature_gradient_relative = float(
        np.max(np.abs(quadrature_gradient)) / max(1.0, abs(quadrature_total))
    )

    output = HERE / "coefficients-order4x3.npz"
    np.savez_compressed(
        output,
        coefficients=values.reshape(3, 4, 3),
        radius=np.array(settings["radius"]),
    )
    payload = {
        "campaign": "P240",
        "attempt": "0036",
        "candidate": "D_fixed_j_two_clock_spectral_cartan_one_body",
        "environment": {
            "torch": torch.__version__,
            "cuda_runtime": torch.version.cuda,
            "device": torch.cuda.get_device_name(0),
            "dtype": "float64",
        },
        "settings": settings,
        "initial": {
            "energy": initial_energy,
            "gradient_inf_relative": float(np.max(np.abs(initial_gradient)) / max(1.0, abs(initial_energy))),
            "components": initial_components,
        },
        "solver": {
            "success": bool(solved.success),
            "status": int(solved.status),
            "message": str(solved.message),
            "function_evaluations": int(solved.nfev),
            "jacobian_evaluations": int(solved.njev),
            "exact_oracle_evaluations": oracle.evaluations,
        },
        "stationary": {
            "energy": total,
            "gradient_inf_relative": gradient_relative,
            "independent_directional_relative_max": float(max(directional)),
            "hessian_symmetry_relative_max": hessian_symmetry,
            "minimum_restricted_hessian_eigenvalue": float(eigenvalues[0]),
            "components": components,
        },
        "withheld_order_5x4": {
            "energy": withheld_total,
            "gradient_inf_relative": withheld_gradient_relative,
            "components": withheld_components,
        },
        "higher_quadrature_32x28": {
            "energy": quadrature_total,
            "energy_relative_change": float(quadrature_energy_change),
            "gradient_inf_relative": quadrature_gradient_relative,
            "components": quadrature_components,
        },
        "output_coefficients": str(output),
    }
    payload["restricted_stationary_gate_pass"] = bool(
        solved.success
        and gradient_relative <= 1.0e-9
        and max(directional) <= 2.0e-8
        and hessian_symmetry <= 1.0e-10
        and eigenvalues[0] >= -1.0e-8
        and components["inertia"] > 0
        and np.isfinite(components["frequency"])
        and components["frequency"] > 0
        and withheld_gradient_relative <= 1.0e-6
        and quadrature_energy_change <= 1.0e-6
        and quadrature_gradient_relative <= 2.0e-7
    )
    print("P240_SPECTRAL_CARTAN_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
    return 0 if payload["restricted_stationary_gate_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
