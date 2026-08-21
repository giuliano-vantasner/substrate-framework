"""Direct variational Skyrme one-body oracle for P240 attempt 0012.

The clock inertia is the symbolically selected axis-weighted timelike Skyrme
current. Descent is only a root-basin warm start; verdicts come from the
Euler-Lagrange residual, independent first variations, and Hessian modes.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass

import numpy as np
import torch
from scipy.optimize import minimize, root
from scipy.sparse.linalg import ArpackNoConvergence, LinearOperator, eigsh


torch.set_default_dtype(torch.float64)
ETA = torch.diag(torch.tensor([-1.0, 1.0, 1.0, 1.0]))
P0 = torch.diag(torch.tensor([1.0, 0.0, 0.0, 0.0]))
AZIMUTH_GENERATOR = torch.zeros((4, 4))
AZIMUTH_GENERATOR[1, 2], AZIMUTH_GENERATOR[2, 1] = -1.0, 1.0
PARITY = torch.diag(torch.tensor([1.0, -1.0, -1.0, 1.0]))


@dataclass(frozen=True)
class Parameters:
    spacing: float = 0.5
    rho_cells: int = 8
    z_cells: int = 16
    g: float = 8.0
    curvature_c2: float = 1.0
    beta: float = 1.0
    potential_scale: float = 1.0
    projector_stiffness: float = 1.0
    scalar_stiffness: float = 1.0
    scalar_coupling: float = 0.1
    l2_strength: float = 1.0
    angular_momentum: float = 1.0
    core_radius: float = 1.0
    adam_steps: int = 1800
    adam_learning_rate: float = 0.008
    lbfgsb_iterations: int = 12000
    lbfgsb_gtol: float = 1.0e-10


def coordinates(parameters: Parameters) -> tuple[torch.Tensor, torch.Tensor]:
    rho = (torch.arange(parameters.rho_cells) + 0.5) * parameters.spacing
    z = (
        torch.arange(parameters.z_cells) - parameters.z_cells / 2 + 0.5
    ) * parameters.spacing
    return torch.meshgrid(rho, z, indexing="ij")


def decode_spatial(field: torch.Tensor) -> tuple[torch.Tensor, ...]:
    return tuple(field[..., index] for index in range(4))


def physical_components(
    field: torch.Tensor, parameters: Parameters
) -> tuple[torch.Tensor, ...]:
    anisotropy, common, split, angle_control = decode_spatial(field)
    rho, z = coordinates(parameters)
    radius_squared = rho**2 + z**2
    core_squared = parameters.core_radius**2
    q_radius = radius_squared / (radius_squared + core_squared)
    q_axis = rho**2 / (rho**2 + core_squared)
    q_vector = rho / torch.sqrt(rho**2 + core_squared)
    director = common + q_radius * anisotropy
    tangent = common + q_axis * split
    azimuthal = common - q_axis * split
    angle = torch.atan2(z, rho) + q_vector * angle_control
    boost_rho = q_vector * field[..., 4]
    boost_z = field[..., 5]
    return director, tangent, azimuthal, angle, boost_rho, boost_z


def initial_field(parameters: Parameters, split_sign: float) -> torch.Tensor:
    rho, z = coordinates(parameters)
    radius_squared = rho**2 + z**2
    radius = torch.sqrt(radius_squared)
    core_squared = parameters.core_radius**2
    q_radius = radius_squared / (radius_squared + core_squared)
    amplitude = 1 - torch.exp(-radius_squared / core_squared)
    field = torch.zeros(
        parameters.rho_cells, parameters.z_cells, 7, dtype=torch.float64
    )
    field[..., 0] = amplitude / q_radius
    field[..., 2] = (
        split_sign
        * 0.15
        * amplitude
        * torch.exp(-((radius / (1.5 * parameters.core_radius)) ** 2))
    )
    field[..., 6] = -parameters.scalar_coupling * torch.exp(
        -((radius / (2 * parameters.core_radius)) ** 2)
    )
    boundary = torch.zeros_like(field)
    boundary[..., 0] = 1 / q_radius
    field[-1] = boundary[-1]
    field[:, 0] = boundary[:, 0]
    field[:, -1] = boundary[:, -1]
    return field

def _boost_matrix(
    rapidity_rho: torch.Tensor, rapidity_z: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
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
    boost = torch.zeros(rapidity.shape[:-1] + (4, 4))
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
    return boost, inverse, rapidity


def matrix_fields(field: torch.Tensor, parameters: Parameters) -> tuple[torch.Tensor, ...]:
    (
        director_value,
        tangent_value,
        azimuthal_value,
        angle,
        boost_rho,
        boost_z,
    ) = physical_components(field, parameters)
    cosine, sine = torch.cos(angle), torch.sin(angle)
    director = torch.stack((cosine, torch.zeros_like(cosine), sine), dim=-1)
    tangent = torch.stack((-sine, torch.zeros_like(sine), cosine), dim=-1)
    azimuthal = torch.zeros_like(director)
    azimuthal[..., 1] = 1
    spatial = (
        director_value[..., None, None] * director[..., :, None] * director[..., None, :]
        + tangent_value[..., None, None] * tangent[..., :, None] * tangent[..., None, :]
        + azimuthal_value[..., None, None]
        * azimuthal[..., :, None]
        * azimuthal[..., None, :]
    )
    rest = torch.zeros(field.shape[:-1] + (4, 4))
    rest[..., 0, 0] = -(parameters.g + field[..., 6])
    rest[..., 1:4, 1:4] = spatial
    boost, inverse_boost, rapidity = _boost_matrix(boost_rho, boost_z)
    order_parameter = boost @ rest @ boost.transpose(-1, -2)
    projector_t = inverse_boost @ P0 @ boost
    inverse_cartan = ETA - 2 * projector_t @ ETA
    axis_rest = torch.zeros_like(rest)
    axis_rest[..., 1:4, 1:4] = director[..., :, None] * director[..., None, :]
    projector_n = boost @ axis_rest @ inverse_boost
    return (
        spatial,
        rest,
        boost,
        order_parameter,
        projector_t,
        projector_n,
        inverse_cartan,
        rapidity,
    )


def matrix_derivatives(
    matrices: torch.Tensor, *, mixed: bool, parameters: Parameters
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    ghost = PARITY @ matrices[0] @ PARITY
    minus = torch.cat((ghost[None], matrices[:-2]), dim=0)
    derivative_rho = (matrices[1:] - minus)[:, 1:-1] / (2 * parameters.spacing)
    derivative_z = (matrices[:-1, 2:] - matrices[:-1, :-2]) / (
        2 * parameters.spacing
    )
    centre = matrices[:-1, 1:-1]
    angular = (
        AZIMUTH_GENERATOR @ centre - centre @ AZIMUTH_GENERATOR
        if mixed
        else AZIMUTH_GENERATOR @ centre + centre @ AZIMUTH_GENERATOR.T
    )
    rho, _ = coordinates(parameters)
    angular = angular / rho[:-1, 1:-1][..., None, None]
    return derivative_rho, angular, derivative_z


def scalar_derivatives(
    scalar: torch.Tensor, parameters: Parameters
) -> tuple[torch.Tensor, torch.Tensor]:
    minus = torch.cat((scalar[0:1], scalar[:-2]), dim=0)
    return (
        (scalar[1:] - minus)[:, 1:-1] / (2 * parameters.spacing),
        (scalar[:-1, 2:] - scalar[:-1, :-2]) / (2 * parameters.spacing),
    )


def eta_commutator(left: torch.Tensor, right: torch.Tensor) -> torch.Tensor:
    return left @ ETA @ right - right @ ETA @ left


def cartan_norm(curvature: torch.Tensor, cartan: torch.Tensor) -> torch.Tensor:
    return torch.einsum(
        "...ab,...cd,...ac,...bd->...", curvature, curvature, cartan, cartan
    )


def projector_norm(derivative: torch.Tensor) -> torch.Tensor:
    return -0.5 * torch.einsum("...ab,...ba->...", derivative, derivative)


def rest_clock_derivative(
    angle: torch.Tensor, rest: torch.Tensor
) -> torch.Tensor:
    angle_centre = angle[:-1, 1:-1]
    n_rho, n_z = torch.cos(angle_centre), torch.sin(angle_centre)
    generator = torch.zeros(rest[:-1, 1:-1].shape)
    generator[..., 1, 2] = -n_z
    generator[..., 2, 1] = n_z
    generator[..., 2, 3] = -n_rho
    generator[..., 3, 2] = n_rho
    rest_centre = rest[:-1, 1:-1]
    return generator @ rest_centre + rest_centre @ generator.transpose(-1, -2)


def densities(
    field: torch.Tensor, parameters: Parameters, *, unweighted_axis: bool = False
) -> dict[str, torch.Tensor | tuple[tuple[torch.Tensor, ...], ...]]:
    (
        spatial,
        rest,
        boost,
        order_parameter,
        projector_t,
        projector_n,
        inverse_cartan,
        _,
    ) = matrix_fields(field, parameters)
    physical = physical_components(field, parameters)
    derivatives = matrix_derivatives(order_parameter, mixed=False, parameters=parameters)
    projector_derivatives = matrix_derivatives(
        projector_t, mixed=True, parameters=parameters
    )
    cartan = inverse_cartan[:-1, 1:-1]
    static_curvatures = (
        eta_commutator(derivatives[0], derivatives[1]),
        eta_commutator(derivatives[0], derivatives[2]),
        eta_commutator(derivatives[1], derivatives[2]),
    )
    curvature_energy = 4 * parameters.curvature_c2 * sum(
        cartan_norm(value, cartan) for value in static_curvatures
    )
    projector_energy = parameters.projector_stiffness * sum(
        projector_norm(value) for value in projector_derivatives
    )
    spatial_centre = spatial[:-1, 1:-1]
    spatial_two = spatial_centre @ spatial_centre
    trace_two = torch.einsum("...aa->...", spatial_two)
    trace_three = torch.einsum("...aa->...", spatial_two @ spatial_centre)
    c_value = parameters.potential_scale
    b_value = parameters.beta * c_value
    a_value = 0.5 * (3 * b_value - 4 * c_value)
    potential = (
        a_value * trace_two
        - b_value * trace_three
        + c_value * trace_two**2
        - (a_value - b_value + c_value)
    )
    clock = rest_clock_derivative(physical[3], rest)
    spatial_mixed = torch.zeros_like(clock)
    spatial_mixed[..., 1:4, 1:4] = spatial_centre
    skyrme_current = spatial_mixed @ clock - clock @ spatial_mixed
    skyrme_commutator = -0.5 * torch.einsum(
        "...ab,...ba->...", skyrme_current, skyrme_current
    )
    skyrme_trace = torch.einsum(
        "...aa->...",
        spatial_mixed @ spatial_mixed @ clock @ clock
        - spatial_mixed @ clock @ spatial_mixed @ clock,
    )
    director = physical[0][:-1, 1:-1]
    axis_weight = torch.ones_like(director) if unweighted_axis else director**2
    inertia_density = parameters.l2_strength * axis_weight * skyrme_commutator
    scalar_rho, scalar_z = scalar_derivatives(field[..., 6], parameters)
    scalar_energy = parameters.scalar_stiffness * (scalar_rho**2 + scalar_z**2) / 2
    matter_factor = torch.exp(2 * parameters.scalar_coupling * field[:-1, 1:-1, 6])
    return {
        "curvature": matter_factor * curvature_energy,
        "projector": matter_factor * projector_energy,
        "potential": matter_factor * potential,
        "scalar": scalar_energy,
        "inertia": matter_factor * inertia_density,
        "skyrme_commutator": skyrme_commutator,
        "skyrme_trace": skyrme_trace,
    }


def observables(
    field: torch.Tensor, parameters: Parameters, *, unweighted_axis: bool = False
) -> dict[str, torch.Tensor]:
    values = densities(field, parameters, unweighted_axis=unweighted_axis)
    rho, _ = coordinates(parameters)
    weights = 2 * np.pi * rho[:-1, 1:-1] * parameters.spacing**2
    components = {
        name: torch.sum(weights * values[name])
        for name in ("curvature", "projector", "potential", "scalar", "inertia")
    }
    components["static"] = sum(
        components[name] for name in ("curvature", "projector", "potential", "scalar")
    )
    components["rotational"] = parameters.angular_momentum**2 / (
        4 * components["inertia"]
    )
    components["total"] = components["static"] + components["rotational"]
    components["frequency"] = parameters.angular_momentum / (
        2 * components["inertia"]
    )
    return components


def assemble(interior: torch.Tensor, boundary_seed: torch.Tensor) -> torch.Tensor:
    field = boundary_seed.clone()
    field[:-1, 1:-1] = interior.reshape(field.shape[0] - 1, field.shape[1] - 2, 7)
    return field


def independent_skyrme_trace_error(
    field: torch.Tensor, parameters: Parameters
) -> float:
    evaluated = densities(field, parameters)
    commutator = evaluated["skyrme_commutator"].detach().numpy()
    trace = evaluated["skyrme_trace"].detach().numpy()
    return float(
        np.max(np.abs(commutator - trace))
        / max(1.0, np.max(np.abs(commutator)), np.max(np.abs(trace)))
    )

def axis_regularity(field: torch.Tensor, parameters: Parameters) -> float:
    spatial = matrix_fields(field, parameters)[0]
    axis_row = spatial[0, 1:-1]
    commutator = AZIMUTH_GENERATOR[1:4, 1:4] @ axis_row - axis_row @ AZIMUTH_GENERATOR[1:4, 1:4]
    return float(torch.max(torch.linalg.matrix_norm(commutator, ord="fro")) / parameters.spacing)


def _energy_and_gradient(
    values: np.ndarray,
    shape: tuple[int, ...],
    seed: torch.Tensor,
    parameters: Parameters,
) -> tuple[float, np.ndarray]:
    variable = torch.tensor(values.reshape(shape), requires_grad=True)
    total = observables(assemble(variable, seed), parameters)["total"]
    if not torch.isfinite(total):
        raise FloatingPointError("variational objective became non-finite")
    gradient = torch.autograd.grad(total, variable)[0]
    return float(total.detach()), gradient.detach().numpy().ravel()


def _energy_value(
    values: np.ndarray,
    shape: tuple[int, ...],
    seed: torch.Tensor,
    parameters: Parameters,
) -> float:
    variable = torch.tensor(values.reshape(shape))
    total = observables(assemble(variable, seed), parameters)["total"]
    if not torch.isfinite(total):
        raise FloatingPointError("directional energy became non-finite")
    return float(total.detach())


def _hessian_vector(
    values: np.ndarray,
    vector: np.ndarray,
    shape: tuple[int, ...],
    seed: torch.Tensor,
    parameters: Parameters,
) -> np.ndarray:
    variable = torch.tensor(values.reshape(shape), requires_grad=True)
    total = observables(assemble(variable, seed), parameters)["total"]
    gradient = torch.autograd.grad(total, variable, create_graph=True)[0]
    direction = torch.tensor(vector.reshape(shape))
    product = torch.sum(gradient * direction)
    result = torch.autograd.grad(product, variable)[0]
    return result.detach().numpy().ravel()


def _deterministic_directions(size: int, count: int = 3) -> list[np.ndarray]:
    index = np.arange(1, size + 1, dtype=np.float64)
    directions: list[np.ndarray] = []
    for mode in range(1, count + 1):
        vector = np.sin(index * (0.37 + 0.11 * mode)) + np.cos(
            index * (0.19 + 0.07 * mode)
        )
        for prior in directions:
            vector -= np.dot(vector, prior) * prior
        vector /= np.linalg.norm(vector)
        directions.append(vector)
    return directions


def solve_branch(
    parameters: Parameters, split_sign: float, root_iterations: int
) -> dict:
    seed = initial_field(parameters, split_sign)
    interior = torch.nn.Parameter(seed[:-1, 1:-1].clone())
    optimizer = torch.optim.Adam([interior], lr=parameters.adam_learning_rate)
    progress_stride = max(parameters.adam_steps // 2, 1)
    for iteration in range(parameters.adam_steps):
        optimizer.zero_grad()
        total = observables(assemble(interior, seed), parameters)["total"]
        if not torch.isfinite(total):
            raise FloatingPointError("warm-start Adam objective became non-finite")
        total.backward()
        optimizer.step()
        if iteration % progress_stride == 0:
            print(
                json.dumps(
                    {
                        "stage": "warm_adam",
                        "split_sign": split_sign,
                        "iteration": iteration,
                        "energy": float(total.detach()),
                        "gradient_inf": float(torch.max(torch.abs(interior.grad))),
                    }
                ),
                flush=True,
            )

    shape = tuple(interior.shape)
    initial = interior.detach().numpy().ravel()
    warm_evaluations = 0

    def objective(values: np.ndarray) -> tuple[float, np.ndarray]:
        nonlocal warm_evaluations
        warm_evaluations += 1
        return _energy_and_gradient(values, shape, seed, parameters)

    warm = minimize(
        objective,
        initial,
        jac=True,
        method="L-BFGS-B",
        bounds=None,
        options={
            "maxiter": parameters.lbfgsb_iterations,
            "ftol": 1.0e-15,
            "gtol": parameters.lbfgsb_gtol,
            "maxls": 40,
            "maxcor": 50,
        },
    )
    reference_scale = max(1.0, abs(float(warm.fun)))
    root_evaluations = 0

    def residual(values: np.ndarray) -> np.ndarray:
        nonlocal root_evaluations
        root_evaluations += 1
        return _energy_and_gradient(values, shape, seed, parameters)[1] / reference_scale

    try:
        solved = root(
            residual,
            warm.x,
            method="krylov",
            options={
                "fatol": 1.0e-10,
                "maxiter": root_iterations,
                "line_search": "armijo",
            },
        )
        values = np.asarray(solved.x, dtype=np.float64)
        root_success = bool(solved.success)
        root_message = str(solved.message)
        root_outer_iterations = int(getattr(solved, "nit", -1))
    except Exception as error:
        values = np.asarray(warm.x, dtype=np.float64)
        root_success = False
        root_message = f"{type(error).__name__}: {error}"
        root_outer_iterations = -1

    energy, gradient = _energy_and_gradient(values, shape, seed, parameters)
    residual_inf_relative = float(
        np.max(np.abs(gradient)) / max(1.0, abs(energy))
    )
    directions = _deterministic_directions(values.size)
    difference_step = 2.0e-5
    probe_offset = 1.0e-4
    root_directional = []
    probe_errors = []
    for direction in directions:
        plus = _energy_value(
            values + difference_step * direction, shape, seed, parameters
        )
        minus = _energy_value(
            values - difference_step * direction, shape, seed, parameters
        )
        root_directional.append(
            abs((plus - minus) / (2 * difference_step))
            / max(1.0, abs(energy))
        )
        probe = values + probe_offset * direction
        _, probe_gradient = _energy_and_gradient(probe, shape, seed, parameters)
        ad_value = float(np.dot(probe_gradient, direction))
        fd_value = (
            _energy_value(
                probe + difference_step * direction, shape, seed, parameters
            )
            - _energy_value(
                probe - difference_step * direction, shape, seed, parameters
            )
        ) / (2 * difference_step)
        probe_errors.append(
            abs(ad_value - fd_value) / max(1.0, abs(ad_value), abs(fd_value))
        )

    hessian_calls = 0

    def matvec(vector: np.ndarray) -> np.ndarray:
        nonlocal hessian_calls
        hessian_calls += 1
        return _hessian_vector(values, vector, shape, seed, parameters)

    operator = LinearOperator(
        (values.size, values.size), matvec=matvec, dtype=np.float64
    )
    left, right = directions[:2]
    left_h_right = float(np.dot(left, matvec(right)))
    right_h_left = float(np.dot(right, matvec(left)))
    hessian_symmetry_error = abs(left_h_right - right_h_left) / max(
        1.0, abs(left_h_right), abs(right_h_left)
    )
    eigensolver_success = True
    try:
        eigenvalues, _ = eigsh(
            operator,
            k=6,
            which="SA",
            tol=1.0e-7,
            maxiter=2000,
        )
        eigenvalues = np.sort(eigenvalues)
    except ArpackNoConvergence as error:
        eigensolver_success = False
        eigenvalues = np.sort(error.eigenvalues)
    except Exception:
        eigensolver_success = False
        eigenvalues = np.empty(0, dtype=np.float64)

    variable = torch.tensor(values.reshape(shape), requires_grad=True)
    field = assemble(variable, seed)
    final_observables = observables(field, parameters)
    wrong_variable = torch.tensor(values.reshape(shape), requires_grad=True)
    wrong_total = observables(
        assemble(wrong_variable, seed), parameters, unweighted_axis=True
    )["total"]
    wrong_gradient = torch.autograd.grad(wrong_total, wrong_variable)[0]
    field_values = field.detach().numpy()
    boundary_residual = max(
        float(np.max(np.abs(field_values[-1] - seed[-1].detach().numpy()))),
        float(np.max(np.abs(field_values[:, 0] - seed[:, 0].detach().numpy()))),
        float(np.max(np.abs(field_values[:, -1] - seed[:, -1].detach().numpy()))),
    )
    director, tangent, azimuthal, _, boost_rho, boost_z = physical_components(
        field, parameters
    )
    eigenvalue_fields = torch.stack((director, tangent, azimuthal), dim=-1)
    timelike_gap = torch.min(
        torch.abs(parameters.g + field[..., 6, None] - eigenvalue_fields)
    )
    rho_extent = parameters.rho_cells * parameters.spacing
    z_extent = parameters.z_cells * parameters.spacing
    volume_scale = np.pi * rho_extent**2 * z_extent
    inertia_floor = np.sqrt(np.finfo(np.float64).eps) * volume_scale
    return {
        "split_sign": split_sign,
        "warm_optimizer_success": bool(warm.success),
        "warm_optimizer_message": str(warm.message),
        "warm_iterations": int(warm.nit),
        "warm_evaluations": warm_evaluations,
        "root_success": root_success,
        "root_message": root_message,
        "root_outer_iterations": root_outer_iterations,
        "root_evaluations": root_evaluations,
        "euler_lagrange_gradient_inf": float(np.max(np.abs(gradient))),
        "euler_lagrange_residual_inf_relative": residual_inf_relative,
        "root_directional_derivative_relative_max": float(max(root_directional)),
        "probe_ad_vs_fd_relative_error_max": float(max(probe_errors)),
        "hessian_bilinear_symmetry_relative_error": float(hessian_symmetry_error),
        "hessian_eigensolver_success": eigensolver_success,
        "hessian_vector_calls": hessian_calls,
        "six_smallest_hessian_eigenvalues": [float(value) for value in eigenvalues],
        "minimum_hessian_eigenvalue": (
            float(eigenvalues[0]) if eigenvalues.size else None
        ),
        "unweighted_axis_mutation_relative_gradient": float(
            torch.max(torch.abs(wrong_gradient)).detach()
            / max(1.0, abs(float(wrong_total.detach())))
        ),
        "boundary_residual": boundary_residual,
        "timelike_gap": float(timelike_gap.detach()),
        "min_tau_minus_g": float(torch.min(field[..., 6]).detach()),
        "max_tau_minus_g": float(torch.max(field[..., 6]).detach()),
        "max_abs_boost": float(
            torch.max(torch.abs(torch.stack((boost_rho, boost_z), dim=-1))).detach()
        ),
        "axis_connection_over_spacing": axis_regularity(field, parameters),
        "transverse_split_over_rho_squared": float(
            torch.max(
                torch.abs(tangent - azimuthal) / coordinates(parameters)[0] ** 2
            ).detach()
        ),
        "independent_skyrme_trace_relative_error": independent_skyrme_trace_error(
            field, parameters
        ),
        "inertia_scale_floor": float(inertia_floor),
        "observables": {
            name: float(value.detach()) for name, value in final_observables.items()
        },
    }

def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(1.0, abs(left), abs(right))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spacing", type=float, default=0.5)
    parser.add_argument("--rho-cells", type=int, default=8)
    parser.add_argument("--z-cells", type=int, default=16)
    parser.add_argument("--adam-steps", type=int, default=1800)
    parser.add_argument("--adam-learning-rate", type=float, default=0.008)
    parser.add_argument("--lbfgsb-iterations", type=int, default=6000)
    parser.add_argument("--lbfgsb-gtol", type=float, default=1.0e-10)
    parser.add_argument("--root-iterations", type=int, default=120)
    parser.add_argument("--split-signs", nargs="+", type=float, default=(1.0, -1.0))
    args = parser.parse_args()
    parameters = Parameters(
        spacing=args.spacing,
        rho_cells=args.rho_cells,
        z_cells=args.z_cells,
        adam_steps=args.adam_steps,
        adam_learning_rate=args.adam_learning_rate,
        lbfgsb_iterations=args.lbfgsb_iterations,
        lbfgsb_gtol=args.lbfgsb_gtol,
    )
    starts = [
        solve_branch(parameters, sign, args.root_iterations)
        for sign in args.split_signs
    ]
    selected = min(starts, key=lambda row: row["observables"]["total"])
    comparison = None
    if len(starts) >= 2:
        comparison = {
            "total_energy_relative_difference": relative_difference(
                starts[0]["observables"]["total"], starts[1]["observables"]["total"]
            ),
            "frequency_relative_difference": relative_difference(
                starts[0]["observables"]["frequency"], starts[1]["observables"]["frequency"]
            ),
        }
    payload = {
        "campaign": "P240",
        "attempt": "0012",
        "candidate": "L2_sextic_axis_weighted_timelike_skyrme_current",
        "environment": {
            "numpy": np.__version__,
            "scipy": __import__("scipy").__version__,
            "torch": torch.__version__,
            "dtype": "float64",
        },
        "parameters": asdict(parameters),
        "starts": starts,
        "opposite_start_comparison": comparison,
        "selected": selected,
    }
    print("P240_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
