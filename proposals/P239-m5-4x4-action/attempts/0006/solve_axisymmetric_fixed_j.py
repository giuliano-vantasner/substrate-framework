"""Relax the regular axisymmetric Candidate-G fixed-J functional.

This is proposal evidence, not an accepted solver API.  It uses PyTorch only
for the analytic reverse-mode gradient supplied to SciPy's L-BFGS-B.  The
field representation, density, boundary conditions, and diagnostics are kept
explicit so a successful branch can be reimplemented independently without a
PyTorch dependency.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import torch
from scipy.optimize import minimize


HERE = Path(__file__).resolve().parent
torch.set_default_dtype(torch.float64)


@dataclass(frozen=True)
class RunParameters:
    spacing: float = 0.5
    rho_cells: int = 12
    z_cells: int = 24
    angular_momentum: float = 20.0
    projector_stiffness: float = 1.0
    g: float = 8.0
    curvature_c2: float = 1.0
    beta: float = 1.0
    cscale: float = 0.0037705544498939964
    core_radius: float = 1.5
    splitting_seed: float = 0.25
    boost_seed: float = 0.08
    max_iterations: int = 220


def _coordinates(parameters: RunParameters) -> tuple[torch.Tensor, torch.Tensor]:
    rho = (torch.arange(parameters.rho_cells) + 0.5) * parameters.spacing
    z = (
        torch.arange(parameters.z_cells) - parameters.z_cells / 2 + 0.5
    ) * parameters.spacing
    return torch.meshgrid(rho, z, indexing="ij")


def _initial_field(parameters: RunParameters, boost_sign: float) -> torch.Tensor:
    rho, z = _coordinates(parameters)
    radius = torch.sqrt(rho**2 + z**2)
    n_rho = rho / radius
    n_z = z / radius
    amplitude = 1 - torch.exp(-((radius / parameters.core_radius) ** 2))
    splitting = (
        parameters.splitting_seed
        * rho**2
        / (radius**2 + parameters.core_radius**2)
        * torch.exp(-((radius / (1.5 * parameters.core_radius)) ** 2))
    )

    field = torch.zeros(
        parameters.rho_cells, parameters.z_cells, 6, dtype=torch.float64
    )
    # Coordinates are (lambda_director, lambda_meridional_tangent,
    # lambda_azimuthal, director_angle, b_rho, b_z).  Keeping the director
    # label explicit makes the collective clock continuous through a melted
    # core where eigenvalues meet.
    field[..., 0] = amplitude
    field[..., 1] = splitting
    field[..., 2] = -splitting
    field[..., 3] = torch.atan2(z, rho)
    localized_boost = (
        boost_sign
        * parameters.boost_seed
        * torch.exp(-((radius / (1.8 * parameters.core_radius)) ** 2))
    )
    field[..., 4] = 0.0
    field[..., 5] = localized_boost

    # The three outer coordinate edges are the exact pure-director M5.17
    # boundary with zero boost.  rho=0 is represented by a parity ghost.
    boundary = torch.zeros_like(field)
    boundary[..., 0] = 1.0
    boundary[..., 3] = torch.atan2(z, rho)
    field[-1, :, :] = boundary[-1, :, :]
    field[:, 0, :] = boundary[:, 0, :]
    field[:, -1, :] = boundary[:, -1, :]
    return field


def _boost_matrix(
    rapidity_rho: torch.Tensor, rapidity_z: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    rapidity = torch.stack(
        (rapidity_rho, torch.zeros_like(rapidity_rho), rapidity_z), -1
    )
    radius_squared = torch.sum(rapidity**2, dim=-1)
    safe_radius = torch.sqrt(torch.clamp(radius_squared, min=1.0e-24))
    small = radius_squared < 1.0e-12
    sinh_over_radius = torch.where(
        small,
        1 + radius_squared / 6 + radius_squared**2 / 120,
        torch.sinh(safe_radius) / safe_radius,
    )
    cosh_minus_one_over_radius_squared = torch.where(
        small,
        0.5 + radius_squared / 24 + radius_squared**2 / 720,
        (torch.cosh(safe_radius) - 1) / torch.clamp(radius_squared, min=1.0e-24),
    )
    cosine = torch.cosh(
        torch.where(small, torch.sqrt(radius_squared + 1.0e-30), safe_radius)
    )
    shape = rapidity.shape[:-1] + (4, 4)
    boost = torch.zeros(shape, dtype=rapidity.dtype, device=rapidity.device)
    boost[..., 0, 0] = cosine
    boost[..., 0, 1:4] = sinh_over_radius[..., None] * rapidity
    boost[..., 1:4, 0] = sinh_over_radius[..., None] * rapidity
    identity_three = torch.eye(3, dtype=rapidity.dtype, device=rapidity.device)
    boost[..., 1:4, 1:4] = identity_three + (
        cosh_minus_one_over_radius_squared[..., None, None]
        * rapidity[..., :, None]
        * rapidity[..., None, :]
    )
    inverse = boost.clone()
    inverse[..., 0, 1:4] *= -1
    inverse[..., 1:4, 0] *= -1
    return boost, inverse


def _matrix_fields(
    field: torch.Tensor, parameters: RunParameters
) -> tuple[torch.Tensor, ...]:
    director_value, meridional_value, azimuthal_value, angle = (
        field[..., index] for index in range(4)
    )
    cosine, sine = torch.cos(angle), torch.sin(angle)
    director = torch.stack((cosine, torch.zeros_like(cosine), sine), dim=-1)
    tangent = torch.stack((-sine, torch.zeros_like(sine), cosine), dim=-1)
    azimuthal = torch.zeros_like(director)
    azimuthal[..., 1] = 1.0
    spatial = (
        director_value[..., None, None]
        * director[..., :, None]
        * director[..., None, :]
        + meridional_value[..., None, None]
        * tangent[..., :, None]
        * tangent[..., None, :]
        + azimuthal_value[..., None, None]
        * azimuthal[..., :, None]
        * azimuthal[..., None, :]
    )
    rest = torch.zeros(field.shape[:-1] + (4, 4), dtype=field.dtype)
    rest[..., 0, 0] = -parameters.g
    rest[..., 1:4, 1:4] = spatial
    boost, inverse_boost = _boost_matrix(field[..., 4], field[..., 5])
    order_parameter = boost @ rest @ boost.transpose(-1, -2)

    p0 = torch.diag(torch.tensor([1.0, 0.0, 0.0, 0.0], dtype=field.dtype))
    projector = inverse_boost @ p0 @ boost
    eta = torch.diag(torch.tensor([-1.0, 1.0, 1.0, 1.0], dtype=field.dtype))
    inverse_cartan = eta - 2 * projector @ eta
    return spatial, rest, boost, order_parameter, projector, inverse_cartan


def _equivariant_derivatives(
    matrices: torch.Tensor, *, mixed: bool, parameters: RunParameters
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    parity = torch.diag(torch.tensor([1.0, -1.0, -1.0, 1.0]))
    ghost = (
        parity @ matrices[0] @ parity if not mixed else parity @ matrices[0] @ parity
    )
    minus = torch.cat((ghost[None], matrices[:-2]), dim=0)
    derivative_rho = (matrices[1:] - minus) / (2 * parameters.spacing)
    derivative_rho = derivative_rho[:, 1:-1]
    derivative_z = (matrices[:-1, 2:] - matrices[:-1, :-2]) / (2 * parameters.spacing)
    centre = matrices[:-1, 1:-1]
    generator = torch.zeros((4, 4), dtype=matrices.dtype)
    generator[1, 2], generator[2, 1] = -1.0, 1.0
    if mixed:
        angular = generator @ centre - centre @ generator
    else:
        angular = generator @ centre + centre @ generator.T
    rho, _ = _coordinates(parameters)
    angular = angular / rho[:-1, 1:-1][..., None, None]
    return derivative_rho, angular, derivative_z


def _eta_commutator(left: torch.Tensor, right: torch.Tensor) -> torch.Tensor:
    eta = torch.diag(torch.tensor([-1.0, 1.0, 1.0, 1.0], dtype=left.dtype))
    return left @ eta @ right - right @ eta @ left


def _cartan_norm(curvature: torch.Tensor, inverse_cartan: torch.Tensor) -> torch.Tensor:
    return torch.einsum(
        "...ab,...cd,...ac,...bd->...",
        curvature,
        curvature,
        inverse_cartan,
        inverse_cartan,
    )


def _projector_norm(derivative: torch.Tensor) -> torch.Tensor:
    return -0.5 * torch.einsum("...ab,...ba->...", derivative, derivative)


def _clock_derivative(
    field: torch.Tensor, rest: torch.Tensor, boost: torch.Tensor
) -> torch.Tensor:
    angle = field[:-1, 1:-1, 3]
    n_rho = torch.cos(angle)
    n_phi = torch.zeros_like(angle)
    n_z = torch.sin(angle)
    generator = torch.zeros(rest[:-1, 1:-1].shape, dtype=rest.dtype)
    generator[..., 1, 2] = -n_z
    generator[..., 1, 3] = n_phi
    generator[..., 2, 1] = n_z
    generator[..., 2, 3] = -n_rho
    generator[..., 3, 1] = -n_phi
    generator[..., 3, 2] = n_rho
    rest_centre = rest[:-1, 1:-1]
    rest_clock = generator @ rest_centre + rest_centre @ generator.transpose(-1, -2)
    boost_centre = boost[:-1, 1:-1]
    return boost_centre @ rest_clock @ boost_centre.transpose(-1, -2)


def _densities(
    field: torch.Tensor, parameters: RunParameters
) -> dict[str, torch.Tensor]:
    spatial, rest, boost, order_parameter, projector, inverse_cartan = _matrix_fields(
        field, parameters
    )
    field_derivatives = _equivariant_derivatives(
        order_parameter, mixed=False, parameters=parameters
    )
    projector_derivatives = _equivariant_derivatives(
        projector, mixed=True, parameters=parameters
    )
    cartan = inverse_cartan[:-1, 1:-1]
    curvature_density = torch.zeros(cartan.shape[:-2], dtype=field.dtype)
    for left in range(3):
        for right in range(left + 1, 3):
            curvature_density = curvature_density + _cartan_norm(
                _eta_commutator(field_derivatives[left], field_derivatives[right]),
                cartan,
            )
    curvature_density = 4 * parameters.curvature_c2 * curvature_density

    projector_density = parameters.projector_stiffness * sum(
        _projector_norm(derivative) for derivative in projector_derivatives
    )

    spatial_centre = spatial[:-1, 1:-1]
    spatial_two = spatial_centre @ spatial_centre
    trace_two = torch.einsum("...aa->...", spatial_two)
    trace_three = torch.einsum("...aa->...", spatial_two @ spatial_centre)
    c_value = parameters.cscale
    b_value = parameters.beta * c_value
    a_value = 0.5 * (3 * b_value - 4 * c_value)
    vacuum_value = a_value - b_value + c_value
    potential_density = (
        a_value * trace_two
        - b_value * trace_three
        + c_value * trace_two**2
        - vacuum_value
    )

    clock = _clock_derivative(field, rest, boost)
    inertia_density = torch.zeros_like(curvature_density)
    for derivative in field_derivatives:
        inertia_density = inertia_density + _cartan_norm(
            _eta_commutator(clock, derivative), cartan
        )
    inertia_density = 4 * parameters.curvature_c2 * inertia_density

    rho, _ = _coordinates(parameters)
    weights = 2 * np.pi * rho[:-1, 1:-1] * parameters.spacing**2
    return {
        "curvature": curvature_density,
        "projector": projector_density,
        "potential": potential_density,
        "inertia": inertia_density,
        "weights": weights,
    }


def _observables(
    field: torch.Tensor, parameters: RunParameters
) -> dict[str, torch.Tensor]:
    densities = _densities(field, parameters)
    weights = densities["weights"]
    integrated = {
        name: torch.sum(weights * densities[name])
        for name in ("curvature", "projector", "potential", "inertia")
    }
    static = integrated["curvature"] + integrated["projector"] + integrated["potential"]
    rotational = parameters.angular_momentum**2 / (4 * integrated["inertia"] + 1.0e-30)
    integrated["static"] = static
    integrated["rotational"] = rotational
    integrated["total"] = static + rotational
    integrated["frequency"] = parameters.angular_momentum / (
        2 * integrated["inertia"] + 1.0e-30
    )
    return integrated


def _assemble_field(
    interior: torch.Tensor, boundary_seed: torch.Tensor
) -> torch.Tensor:
    field = boundary_seed.clone()
    field[:-1, 1:-1] = interior.reshape(field.shape[0] - 1, field.shape[1] - 2, 6)
    return field


def _relax(parameters: RunParameters, boost_sign: float) -> tuple[dict, np.ndarray]:
    seed = _initial_field(parameters, boost_sign)
    initial = seed[:-1, 1:-1].detach().numpy().ravel()
    bounds = []
    for _ in range((parameters.rho_cells - 1) * (parameters.z_cells - 2)):
        bounds.extend([(-2.0, 2.0)] * 3 + [(-np.pi, np.pi)] + [(-1.25, 1.25)] * 2)

    evaluations = 0

    def objective(values: np.ndarray) -> tuple[float, np.ndarray]:
        nonlocal evaluations
        interior = torch.tensor(values, requires_grad=True)
        field = _assemble_field(interior, seed)
        total = _observables(field, parameters)["total"]
        total.backward()
        evaluations += 1
        return float(total.detach()), interior.grad.detach().numpy()

    result = minimize(
        objective,
        initial,
        jac=True,
        method="L-BFGS-B",
        bounds=bounds,
        options={
            "maxiter": parameters.max_iterations,
            "ftol": 1.0e-12,
            "gtol": 1.0e-7,
            "maxls": 30,
        },
    )
    final_interior = torch.tensor(result.x, requires_grad=True)
    final_field = _assemble_field(final_interior, seed)
    observables = _observables(final_field, parameters)
    observables["total"].backward()
    gradient = final_interior.grad.detach().numpy()
    field_numpy = final_field.detach().numpy()
    eigenvalues = field_numpy[..., :3]
    branch_gap = float(np.min(np.abs(parameters.g - eigenvalues)))
    director_gap = float(
        np.min(
            field_numpy[..., 0] - np.maximum(field_numpy[..., 1], field_numpy[..., 2])
        )
    )
    scale = max(1.0, abs(float(observables["total"].detach())))
    summary = {
        "boost_seed_sign": boost_sign,
        "success": bool(result.success),
        "message": str(result.message),
        "iterations": int(result.nit),
        "evaluations": evaluations,
        "objective": float(result.fun),
        "gradient_inf_norm": float(np.max(np.abs(gradient))),
        "stationarity_relative_inf_norm": float(np.max(np.abs(gradient)) / scale),
        "branch_gap": branch_gap,
        "meridional_director_gap": director_gap,
        "max_abs_b_rho": float(np.max(np.abs(field_numpy[..., 4]))),
        "max_abs_b_z": float(np.max(np.abs(field_numpy[..., 5]))),
        "observables": {
            name: float(value.detach()) for name, value in observables.items()
        },
    }
    return summary, field_numpy


def _tail_decomposition(field: np.ndarray, parameters: RunParameters) -> dict:
    rho = (np.arange(parameters.rho_cells) + 0.5) * parameters.spacing
    z = (
        np.arange(parameters.z_cells) - parameters.z_cells / 2 + 0.5
    ) * parameters.spacing
    rr, zz = np.meshgrid(rho, z, indexing="ij")
    radius = np.sqrt(rr**2 + zz**2)
    domain_scale = min(rho[-1], max(abs(z[0]), abs(z[-1])))
    mask = (
        (radius > 0.45 * domain_scale)
        & (radius < 0.78 * domain_scale)
        & (np.arange(parameters.rho_cells)[:, None] < parameters.rho_cells - 1)
        & (np.arange(parameters.z_cells)[None, :] > 0)
        & (np.arange(parameters.z_cells)[None, :] < parameters.z_cells - 1)
    )
    radial_basis_rho = rr[mask] / radius[mask] ** 3
    radial_basis_z = zz[mask] / radius[mask] ** 3
    monopole_basis = 1 / radius[mask] - 1 / domain_scale
    # One shared radial-vector coefficient and one fixed-z monopole coefficient.
    design = np.concatenate(
        (
            np.stack((radial_basis_rho, np.zeros_like(radial_basis_rho)), axis=1),
            np.stack((radial_basis_z, monopole_basis), axis=1),
        ),
        axis=0,
    )
    target = np.concatenate((field[..., 4][mask], field[..., 5][mask]))
    coefficients, *_ = np.linalg.lstsq(design, target, rcond=None)
    residual = target - design @ coefficients
    return {
        "fit_point_count": int(target.size),
        "radial_vector_r_minus_2_coefficient": float(coefficients[0]),
        "fixed_z_monopole_r_minus_1_coefficient": float(coefficients[1]),
        "relative_rms_residual": float(
            np.sqrt(np.mean(residual**2)) / max(np.sqrt(np.mean(target**2)), 1.0e-15)
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spacing", type=float, default=0.5)
    parser.add_argument("--rho-cells", type=int, default=12)
    parser.add_argument("--z-cells", type=int, default=24)
    parser.add_argument("--angular-momentum", type=float, default=20.0)
    parser.add_argument("--projector-stiffness", type=float, default=1.0)
    parser.add_argument("--max-iterations", type=int, default=220)
    parser.add_argument(
        "--boost-signs", type=float, nargs="+", default=(0.0, 1.0, -1.0)
    )
    parser.add_argument("--output", type=Path, default=HERE / "result.json")
    args = parser.parse_args()
    parameters = RunParameters(
        spacing=args.spacing,
        rho_cells=args.rho_cells,
        z_cells=args.z_cells,
        angular_momentum=args.angular_momentum,
        projector_stiffness=args.projector_stiffness,
        max_iterations=args.max_iterations,
    )
    starts = []
    best = None
    best_field = None
    for sign in args.boost_signs:
        summary, field = _relax(parameters, sign)
        starts.append(summary)
        print(json.dumps(summary, sort_keys=True), flush=True)
        if best is None or summary["objective"] < best["objective"]:
            best, best_field = summary, field
    assert best is not None and best_field is not None
    tail = _tail_decomposition(best_field, parameters)
    payload = {
        "campaign": "P239",
        "attempt": "0006",
        "parameters": asdict(parameters),
        "starts": starts,
        "selected": best,
        "tail_decomposition": tail,
        "status": "preflight",
    }
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    np.savez_compressed(args.output.with_suffix(".npz"), field=best_field)
    print(json.dumps({"selected": best, "tail": tail}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
