"""Coupled Candidate-H fixed-J hedgehog preflight.

This proposal-only solver uses a labeled principal-director chart, exact
axisymmetric derivative channels, and automatic derivatives.  It writes every
diagnostic needed to decide whether the branch merits an independent
dependency-light implementation.
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
_GAP_SMOOTHING = 1.0e-8


@dataclass(frozen=True)
class Parameters:
    spacing: float = 0.5
    rho_cells: int = 8
    z_cells: int = 16
    g: float = 8.0
    curvature_c2: float = 1.0
    beta: float = 1.0
    cscale: float = 0.0037705544498939964
    projector_stiffness: float = 1.0
    scalar_stiffness: float = 1.0
    scalar_coupling: float = 0.05
    guard_strength: float = 0.0
    auxiliary_clock_axis: bool = False
    axis_lock_strength: float = 0.0
    angular_momentum: float = 20.0
    core_radius: float = 1.5
    adam_steps: int = 4000
    adam_learning_rate: float = 0.01
    lbfgsb_iterations: int = 1200


def coordinates(parameters: Parameters) -> tuple[torch.Tensor, torch.Tensor]:
    rho = (torch.arange(parameters.rho_cells) + 0.5) * parameters.spacing
    z = (
        torch.arange(parameters.z_cells) - parameters.z_cells / 2 + 0.5
    ) * parameters.spacing
    return torch.meshgrid(rho, z, indexing="ij")


def _inverse_softplus(value: torch.Tensor) -> torch.Tensor:
    return torch.log(torch.expm1(torch.clamp(value, min=1.0e-8)))


def decode_spatial(
    field: torch.Tensor, *, auxiliary_clock_axis: bool = False
) -> tuple[torch.Tensor, ...]:
    gap_coordinate, tangent, azimuthal, angle = (
        field[..., index] for index in range(4)
    )
    if auxiliary_clock_axis:
        director = gap_coordinate
    else:
        smooth_maximum = (tangent + azimuthal) / 2 + torch.sqrt(
            ((tangent - azimuthal) / 2) ** 2 + _GAP_SMOOTHING
        )
        director = smooth_maximum + torch.nn.functional.softplus(gap_coordinate)
    return director, tangent, azimuthal, angle


def initial_field(parameters: Parameters) -> torch.Tensor:
    rho, z = coordinates(parameters)
    radius = torch.sqrt(rho**2 + z**2)
    amplitude = 1 - torch.exp(-((radius / parameters.core_radius) ** 2))
    splitting = (
        0.1
        * amplitude
        * rho**2
        / (radius**2 + parameters.core_radius**2)
        * torch.exp(-((radius / (1.5 * parameters.core_radius)) ** 2))
    )
    smooth_maximum = torch.sqrt(splitting**2 + _GAP_SMOOTHING)
    gap = torch.clamp(amplitude - smooth_maximum, min=1.0e-5)

    field = torch.zeros(
        parameters.rho_cells, parameters.z_cells, 7, dtype=torch.float64
    )
    field[..., 0] = (
        amplitude if parameters.auxiliary_clock_axis else _inverse_softplus(gap)
    )
    field[..., 1] = splitting
    field[..., 2] = -splitting
    field[..., 3] = torch.atan2(z, rho)
    field[..., 6] = -parameters.scalar_coupling * torch.exp(
        -((radius / (2 * parameters.core_radius)) ** 2)
    )

    vacuum_gap_coordinate = float(
        _inverse_softplus(torch.tensor(1 - np.sqrt(_GAP_SMOOTHING)))
    )
    boundary = torch.zeros_like(field)
    boundary[..., 0] = 1.0 if parameters.auxiliary_clock_axis else vacuum_gap_coordinate
    boundary[..., 3] = torch.atan2(z, rho)
    field[-1] = boundary[-1]
    field[:, 0] = boundary[:, 0]
    field[:, -1] = boundary[:, -1]
    return field


def _boost_matrix(
    rapidity_rho: torch.Tensor, rapidity_z: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    rapidity = torch.stack(
        (rapidity_rho, torch.zeros_like(rapidity_rho), rapidity_z), dim=-1
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
    boost = torch.zeros(rapidity.shape[:-1] + (4, 4), dtype=rapidity.dtype)
    boost[..., 0, 0] = cosine
    boost[..., 0, 1:4] = sinh_over_radius[..., None] * rapidity
    boost[..., 1:4, 0] = sinh_over_radius[..., None] * rapidity
    boost[..., 1:4, 1:4] = torch.eye(3) + (
        cosh_minus_one_over_radius_squared[..., None, None]
        * rapidity[..., :, None]
        * rapidity[..., None, :]
    )
    inverse = boost.clone()
    inverse[..., 0, 1:4] *= -1
    inverse[..., 1:4, 0] *= -1
    return boost, inverse


def matrix_fields(
    field: torch.Tensor, parameters: Parameters
) -> tuple[torch.Tensor, ...]:
    director_value, tangent_value, azimuthal_value, angle = decode_spatial(
        field, auxiliary_clock_axis=parameters.auxiliary_clock_axis
    )
    cosine, sine = torch.cos(angle), torch.sin(angle)
    director = torch.stack((cosine, torch.zeros_like(cosine), sine), dim=-1)
    tangent = torch.stack((-sine, torch.zeros_like(sine), cosine), dim=-1)
    azimuthal = torch.zeros_like(director)
    azimuthal[..., 1] = 1
    spatial = (
        director_value[..., None, None]
        * director[..., :, None]
        * director[..., None, :]
        + tangent_value[..., None, None] * tangent[..., :, None] * tangent[..., None, :]
        + azimuthal_value[..., None, None]
        * azimuthal[..., :, None]
        * azimuthal[..., None, :]
    )
    rest = torch.zeros(field.shape[:-1] + (4, 4), dtype=field.dtype)
    rest[..., 0, 0] = -(parameters.g + field[..., 6])
    rest[..., 1:4, 1:4] = spatial
    boost, inverse_boost = _boost_matrix(field[..., 4], field[..., 5])
    order_parameter = boost @ rest @ boost.transpose(-1, -2)
    p0 = torch.diag(torch.tensor([1.0, 0.0, 0.0, 0.0]))
    projector = inverse_boost @ p0 @ boost
    eta = torch.diag(torch.tensor([-1.0, 1.0, 1.0, 1.0]))
    inverse_cartan = eta - 2 * projector @ eta
    return spatial, rest, boost, order_parameter, projector, inverse_cartan


def _matrix_derivatives(
    matrices: torch.Tensor, *, mixed: bool, parameters: Parameters
) -> tuple[torch.Tensor, ...]:
    parity = torch.diag(torch.tensor([1.0, -1.0, -1.0, 1.0]))
    ghost = parity @ matrices[0] @ parity
    minus = torch.cat((ghost[None], matrices[:-2]), dim=0)
    derivative_rho = (matrices[1:] - minus)[:, 1:-1] / (2 * parameters.spacing)
    derivative_z = (matrices[:-1, 2:] - matrices[:-1, :-2]) / (2 * parameters.spacing)
    centre = matrices[:-1, 1:-1]
    generator = torch.zeros((4, 4))
    generator[1, 2], generator[2, 1] = -1, 1
    angular = (
        generator @ centre - centre @ generator
        if mixed
        else generator @ centre + centre @ generator.T
    )
    rho, _ = coordinates(parameters)
    angular = angular / rho[:-1, 1:-1][..., None, None]
    return derivative_rho, angular, derivative_z


def _scalar_derivatives(
    scalar: torch.Tensor, parameters: Parameters
) -> tuple[torch.Tensor, torch.Tensor]:
    minus = torch.cat((scalar[0:1], scalar[:-2]), dim=0)
    derivative_rho = (scalar[1:] - minus)[:, 1:-1] / (2 * parameters.spacing)
    derivative_z = (scalar[:-1, 2:] - scalar[:-1, :-2]) / (2 * parameters.spacing)
    return derivative_rho, derivative_z


def _eta_commutator(left: torch.Tensor, right: torch.Tensor) -> torch.Tensor:
    eta = torch.diag(torch.tensor([-1.0, 1.0, 1.0, 1.0]))
    return left @ eta @ right - right @ eta @ left


def _cartan_norm(curvature: torch.Tensor, cartan: torch.Tensor) -> torch.Tensor:
    return torch.einsum(
        "...ab,...cd,...ac,...bd->...", curvature, curvature, cartan, cartan
    )


def _projector_norm(derivative: torch.Tensor) -> torch.Tensor:
    return -0.5 * torch.einsum("...ab,...ba->...", derivative, derivative)


def _clock_derivative(
    field: torch.Tensor, rest: torch.Tensor, boost: torch.Tensor
) -> torch.Tensor:
    angle = field[:-1, 1:-1, 3]
    n_rho, n_z = torch.cos(angle), torch.sin(angle)
    generator = torch.zeros(rest[:-1, 1:-1].shape)
    generator[..., 1, 2] = -n_z
    generator[..., 2, 1] = n_z
    generator[..., 2, 3] = -n_rho
    generator[..., 3, 2] = n_rho
    rest_centre = rest[:-1, 1:-1]
    rest_clock = generator @ rest_centre + rest_centre @ generator.transpose(-1, -2)
    boost_centre = boost[:-1, 1:-1]
    return boost_centre @ rest_clock @ boost_centre.transpose(-1, -2)


def observables(field: torch.Tensor, parameters: Parameters) -> dict[str, torch.Tensor]:
    spatial, rest, boost, order_parameter, projector, inverse_cartan = matrix_fields(
        field, parameters
    )
    derivatives = _matrix_derivatives(
        order_parameter, mixed=False, parameters=parameters
    )
    projector_derivatives = _matrix_derivatives(
        projector, mixed=True, parameters=parameters
    )
    cartan = inverse_cartan[:-1, 1:-1]
    curvature = torch.zeros(cartan.shape[:-2])
    for left in range(3):
        for right in range(left + 1, 3):
            curvature = curvature + _cartan_norm(
                _eta_commutator(derivatives[left], derivatives[right]), cartan
            )
    curvature = 4 * parameters.curvature_c2 * curvature
    projector_energy = parameters.projector_stiffness * sum(
        _projector_norm(derivative) for derivative in projector_derivatives
    )

    spatial_centre = spatial[:-1, 1:-1]
    spatial_two = spatial_centre @ spatial_centre
    trace_two = torch.einsum("...aa->...", spatial_two)
    trace_three = torch.einsum("...aa->...", spatial_two @ spatial_centre)
    c_value = parameters.cscale
    b_value = parameters.beta * c_value
    a_value = 0.5 * (3 * b_value - 4 * c_value)
    potential = (
        a_value * trace_two
        - b_value * trace_three
        + c_value * trace_two**2
        - (a_value - b_value + c_value)
    )
    director_centre, tangent_centre, azimuthal_centre, _ = (
        value[:-1, 1:-1]
        for value in decode_spatial(
            field, auxiliary_clock_axis=parameters.auxiliary_clock_axis
        )
    )
    if parameters.guard_strength == 0:
        guard = torch.zeros_like(potential)
    else:
        guard = (
            parameters.guard_strength
            * (tangent_centre - azimuthal_centre) ** 4
            / (
                (director_centre - tangent_centre) ** 2
                * (director_centre - azimuthal_centre) ** 2
            )
        )
    matter_factor = torch.exp(2 * parameters.scalar_coupling * field[:-1, 1:-1, 6])
    axis_lock = parameters.axis_lock_strength * (
        tangent_centre**2 + azimuthal_centre**2
    )

    clock = _clock_derivative(field, rest, boost)
    inertia = torch.zeros_like(curvature)
    for derivative in derivatives:
        inertia = inertia + _cartan_norm(_eta_commutator(clock, derivative), cartan)
    inertia = 4 * parameters.curvature_c2 * inertia

    scalar_rho, scalar_z = _scalar_derivatives(field[..., 6], parameters)
    scalar_energy = parameters.scalar_stiffness * (scalar_rho**2 + scalar_z**2) / 2
    rho, _ = coordinates(parameters)
    weights = 2 * np.pi * rho[:-1, 1:-1] * parameters.spacing**2
    components = {
        "curvature": torch.sum(weights * matter_factor * curvature),
        "projector": torch.sum(weights * matter_factor * projector_energy),
        "potential": torch.sum(weights * matter_factor * potential),
        "guard": torch.sum(weights * matter_factor * guard),
        "axis_lock": torch.sum(weights * matter_factor * axis_lock),
        "scalar": torch.sum(weights * scalar_energy),
        "inertia": torch.sum(weights * matter_factor * inertia),
    }
    components["static"] = sum(
        components[name]
        for name in (
            "curvature",
            "projector",
            "potential",
            "guard",
            "axis_lock",
            "scalar",
        )
    )
    components["rotational"] = parameters.angular_momentum**2 / (
        4 * components["inertia"] + 1.0e-30
    )
    components["total"] = components["static"] + components["rotational"]
    components["frequency"] = parameters.angular_momentum / (
        2 * components["inertia"] + 1.0e-30
    )
    return components


def assemble(interior: torch.Tensor, seed: torch.Tensor) -> torch.Tensor:
    field = seed.clone()
    field[:-1, 1:-1] = interior.reshape(field.shape[0] - 1, field.shape[1] - 2, 7)
    return field


def _clamp(interior: torch.Tensor, parameters: Parameters) -> None:
    with torch.no_grad():
        if parameters.auxiliary_clock_axis:
            interior[..., 0].clamp_(-2, 2)
        else:
            interior[..., 0].clamp_(-12, 3)
        interior[..., 1:3].clamp_(-2, 2)
        interior[..., 3].clamp_(-np.pi, np.pi)
        interior[..., 4:6].clamp_(-1.25, 1.25)
        interior[..., 6].clamp_(-2, 2)


def relax(
    parameters: Parameters, initial_solution: Path | None = None
) -> tuple[dict, np.ndarray]:
    seed = initial_field(parameters)
    if initial_solution is None:
        initial_values = seed
    else:
        initial_array = np.load(initial_solution)["field"]
        if initial_array.shape != tuple(seed.shape):
            raise ValueError("initial solution grid does not match requested grid")
        initial_values = torch.tensor(initial_array)
        initial_values[-1] = seed[-1]
        initial_values[:, 0] = seed[:, 0]
        initial_values[:, -1] = seed[:, -1]
    interior = torch.nn.Parameter(initial_values[:-1, 1:-1].clone())
    optimizer = torch.optim.Adam([interior], lr=parameters.adam_learning_rate)
    for iteration in range(parameters.adam_steps):
        optimizer.zero_grad()
        total = observables(assemble(interior, seed), parameters)["total"]
        total.backward()
        optimizer.step()
        _clamp(interior, parameters)
        if iteration % 500 == 0:
            print(
                json.dumps(
                    {
                        "stage": "adam",
                        "iteration": iteration,
                        "energy": float(total.detach()),
                        "gradient_inf": float(torch.max(torch.abs(interior.grad))),
                    }
                ),
                flush=True,
            )

    shape = interior.shape
    initial = interior.detach().numpy().ravel()
    bounds = []
    for _ in range(int(np.prod(shape[:-1]))):
        bounds.extend(
            [
                (-2, 2) if parameters.auxiliary_clock_axis else (-12, 3),
                (-2, 2),
                (-2, 2),
                (-np.pi, np.pi),
            ]
            + [(-1.25, 1.25)] * 2
            + [(-2, 2)]
        )

    evaluations = 0

    def objective(values: np.ndarray) -> tuple[float, np.ndarray]:
        nonlocal evaluations
        variable = torch.tensor(values.reshape(shape), requires_grad=True)
        total = observables(assemble(variable, seed), parameters)["total"]
        total.backward()
        evaluations += 1
        return float(total.detach()), variable.grad.detach().numpy().ravel()

    result = minimize(
        objective,
        initial,
        jac=True,
        method="L-BFGS-B",
        bounds=bounds,
        options={
            "maxiter": parameters.lbfgsb_iterations,
            "ftol": 1.0e-13,
            "gtol": 1.0e-8,
            "maxls": 40,
        },
    )
    variable = torch.tensor(result.x.reshape(shape), requires_grad=True)
    final_field = assemble(variable, seed)
    final_observables = observables(final_field, parameters)
    final_observables["total"].backward()
    gradient_inf = float(torch.max(torch.abs(variable.grad)))
    scale = max(1.0, abs(float(final_observables["total"].detach())))
    values = final_field.detach().numpy()
    director, tangent, azimuthal, _ = decode_spatial(
        final_field, auxiliary_clock_axis=parameters.auxiliary_clock_axis
    )
    rho, z = coordinates(parameters)
    radius = torch.sqrt(rho**2 + z**2)
    outside_core = radius > 2 * parameters.spacing
    principal_gap = torch.minimum(director - tangent, director - azimuthal)
    eigenvalues = torch.stack((director, tangent, azimuthal), dim=-1)
    timelike_gap = torch.min(
        torch.abs(parameters.g + final_field[..., 6, None] - eigenvalues)
    )
    summary = {
        "optimizer_success": bool(result.success),
        "optimizer_message": str(result.message),
        "lbfgsb_iterations": int(result.nit),
        "lbfgsb_evaluations": evaluations,
        "gradient_inf_norm": gradient_inf,
        "stationarity_relative_inf_norm": gradient_inf / scale,
        "principal_gap_outside_core": float(torch.min(principal_gap[outside_core])),
        "timelike_gap": float(timelike_gap),
        "max_abs_boost": float(np.max(np.abs(values[..., 4:6]))),
        "min_phi": float(np.min(values[..., 6])),
        "max_phi": float(np.max(values[..., 6])),
        "observables": {
            name: float(value.detach()) for name, value in final_observables.items()
        },
    }
    return summary, values


def tail_diagnostics(field: np.ndarray, parameters: Parameters) -> dict:
    rho = (np.arange(parameters.rho_cells) + 0.5) * parameters.spacing
    z = (
        np.arange(parameters.z_cells) - parameters.z_cells / 2 + 0.5
    ) * parameters.spacing
    rr, zz = np.meshgrid(rho, z, indexing="ij")
    radius = np.sqrt(rr**2 + zz**2)
    domain = min(rho[-1], max(abs(z[0]), abs(z[-1])))
    mask = (
        (radius > 0.42 * domain)
        & (radius < 0.75 * domain)
        & (np.arange(parameters.rho_cells)[:, None] < parameters.rho_cells - 1)
        & (np.arange(parameters.z_cells)[None, :] > 0)
        & (np.arange(parameters.z_cells)[None, :] < parameters.z_cells - 1)
    )
    basis = (1 / radius[mask] - 1 / domain)[:, None]
    target = field[..., 6][mask]
    coefficient, *_ = np.linalg.lstsq(basis, target, rcond=None)
    residual = target - basis[:, 0] * coefficient[0]
    return {
        "fit_point_count": int(target.size),
        "one_over_r_coefficient": float(coefficient[0]),
        "relative_rms_residual": float(
            np.sqrt(np.mean(residual**2)) / max(np.sqrt(np.mean(target**2)), 1.0e-15)
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spacing", type=float, default=0.5)
    parser.add_argument("--rho-cells", type=int, default=8)
    parser.add_argument("--z-cells", type=int, default=16)
    parser.add_argument("--adam-steps", type=int, default=4000)
    parser.add_argument("--adam-learning-rate", type=float, default=0.01)
    parser.add_argument("--lbfgsb-iterations", type=int, default=1200)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--angular-momentum", type=float, default=20.0)
    parser.add_argument("--guard-strength", type=float, default=0.0)
    parser.add_argument("--auxiliary-clock-axis", action="store_true")
    parser.add_argument("--axis-lock-strength", type=float, default=0.0)
    parser.add_argument("--output", type=Path, default=HERE / "result.json")
    parser.add_argument("--initial-solution", type=Path)
    args = parser.parse_args()
    parameters = Parameters(
        spacing=args.spacing,
        rho_cells=args.rho_cells,
        z_cells=args.z_cells,
        adam_steps=args.adam_steps,
        adam_learning_rate=args.adam_learning_rate,
        lbfgsb_iterations=args.lbfgsb_iterations,
        scalar_coupling=args.alpha,
        angular_momentum=args.angular_momentum,
        guard_strength=args.guard_strength,
        auxiliary_clock_axis=args.auxiliary_clock_axis,
        axis_lock_strength=args.axis_lock_strength,
    )
    summary, field = relax(parameters, args.initial_solution)
    tail = tail_diagnostics(field, parameters)
    payload = {
        "campaign": "P239",
        "attempt": "0008",
        "status": "preflight",
        "parameters": asdict(parameters),
        "solution": summary,
        "scalar_tail": tail,
    }
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    np.savez_compressed(args.output.with_suffix(".npz"), field=field)
    print(json.dumps(payload, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
