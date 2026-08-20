"""Corrected fixed-J projector-current plus alternating-Skyrme coefficient map.

The clock inertia is the symbolically selected axis-weighted spatial norm of
the alternating three-current. Descent is only a root-basin warm start;
verdicts come from the Euler-Lagrange residual, independent first variations,
and Hessian modes.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass, replace
from itertools import permutations

import numpy as np
import torch
from scipy.optimize import minimize, root
from scipy.linalg import eigh as dense_eigh
from scipy.sparse.linalg import ArpackNoConvergence, LinearOperator, eigsh


torch.set_default_dtype(torch.float64)
DEVICE = torch.device("cpu")
ETA = torch.diag(torch.tensor([-1.0, 1.0, 1.0, 1.0]))
P0 = torch.diag(torch.tensor([1.0, 0.0, 0.0, 0.0]))
AZIMUTH_GENERATOR = torch.zeros((4, 4))
AZIMUTH_GENERATOR[1, 2], AZIMUTH_GENERATOR[2, 1] = -1.0, 1.0
PARITY = torch.diag(torch.tensor([1.0, -1.0, -1.0, 1.0]))


def configure_device(name: str) -> None:
    global DEVICE, ETA, P0, AZIMUTH_GENERATOR, PARITY
    DEVICE = torch.device(name)
    if DEVICE.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    ETA = ETA.to(DEVICE)
    P0 = P0.to(DEVICE)
    AZIMUTH_GENERATOR = AZIMUTH_GENERATOR.to(DEVICE)
    PARITY = PARITY.to(DEVICE)


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
    rho = (
        torch.arange(parameters.rho_cells, device=DEVICE) + 0.5
    ) * parameters.spacing
    z = (
        torch.arange(parameters.z_cells, device=DEVICE)
        - parameters.z_cells / 2
        + 0.5
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
        parameters.rho_cells,
        parameters.z_cells,
        7,
        dtype=torch.float64,
        device=DEVICE,
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
    boost = torch.zeros(
        rapidity.shape[:-1] + (4, 4), device=rapidity.device
    )
    boost[..., 0, 0] = cosine
    boost[..., 0, 1:4] = sinh_over_radius[..., None] * rapidity
    boost[..., 1:4, 0] = sinh_over_radius[..., None] * rapidity
    boost[..., 1:4, 1:4] = torch.eye(3, device=rapidity.device) + (
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
    rest = torch.zeros(field.shape[:-1] + (4, 4), device=field.device)
    rest[..., 0, 0] = -(parameters.g + field[..., 6])
    rest[..., 1:4, 1:4] = spatial
    boost, inverse_boost, rapidity = _boost_matrix(boost_rho, boost_z)
    order_parameter = boost @ rest @ boost.transpose(-1, -2)
    projector_t = inverse_boost @ P0 @ boost
    inverse_cartan = ETA - 2 * projector_t @ ETA
    axis_rest = torch.zeros_like(rest)
    axis_rest[..., 1:4, 1:4] = director[..., :, None] * director[..., None, :]
    projector_n = inverse_boost @ axis_rest @ boost
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
    generator = torch.zeros_like(rest[:-1, 1:-1])
    generator[..., 1, 2] = -n_z
    generator[..., 2, 1] = n_z
    generator[..., 2, 3] = -n_rho
    generator[..., 3, 2] = n_rho
    rest_centre = rest[:-1, 1:-1]
    return generator @ rest_centre + rest_centre @ generator.transpose(-1, -2)


def axial_vector(current: torch.Tensor) -> torch.Tensor:
    """Return v for a spatial antisymmetric block current=C(v)."""

    return torch.stack(
        (-current[..., 2, 3], current[..., 1, 3], -current[..., 1, 2]),
        dim=-1,
    )


def alternating_current_from_axial(
    currents: tuple[torch.Tensor, ...]
) -> torch.Tensor:
    """Closed determinant form of epsilon Tr(K K K)/6."""

    vectors = tuple(axial_vector(current) for current in currents)

    def determinant(first: int, second: int, third: int) -> torch.Tensor:
        return torch.sum(
            vectors[first]
            * torch.linalg.cross(vectors[second], vectors[third], dim=-1),
            dim=-1,
        )

    return torch.stack(
        (
            -determinant(1, 2, 3),
            determinant(0, 2, 3),
            -determinant(0, 1, 3),
            determinant(0, 1, 2),
        ),
        dim=-1,
    )


def _permutation_sign(indices: tuple[int, ...]) -> int:
    inversions = sum(
        indices[left] > indices[right]
        for left in range(len(indices))
        for right in range(left + 1, len(indices))
    )
    return -1 if inversions % 2 else 1


def alternating_current_from_epsilon(
    currents: tuple[torch.Tensor, ...]
) -> torch.Tensor:
    """Independent literal epsilon-trace implementation of the current."""

    components = []
    for mu in range(4):
        others = tuple(index for index in range(4) if index != mu)
        value = torch.zeros_like(currents[0][..., 0, 0])
        for spatial_order in permutations(others):
            order = (mu, *spatial_order)
            product = (
                currents[spatial_order[0]]
                @ currents[spatial_order[1]]
                @ currents[spatial_order[2]]
            )
            value = value + _permutation_sign(order) * torch.einsum(
                "...aa->...", product
            )
        components.append(value / 6)
    return torch.stack(components, dim=-1)


def densities(
    field: torch.Tensor,
    parameters: Parameters,
    *,
    unweighted_axis: bool = False,
    omit_spatial_current: int | None = None,
    rest_only_spatial_metric: bool = False,
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
    spatial_mixed_full = torch.zeros_like(rest)
    spatial_mixed_full[..., 1:4, 1:4] = spatial
    spatial_derivatives = matrix_derivatives(
        spatial_mixed_full, mixed=False, parameters=parameters
    )
    spatial_mixed = spatial_mixed_full[:-1, 1:-1]
    z_derivatives = (
        rest_clock_derivative(physical[3], rest),
        *spatial_derivatives,
    )
    currents = tuple(
        spatial_mixed @ derivative - derivative @ spatial_mixed
        for derivative in z_derivatives
    )
    if omit_spatial_current is not None:
        if omit_spatial_current not in (1, 2, 3):
            raise ValueError("omit_spatial_current must be one of 1, 2, 3")
        currents = tuple(
            torch.zeros_like(current) if index == omit_spatial_current else current
            for index, current in enumerate(currents)
        )
    alternating = alternating_current_from_axial(currents)
    director = physical[0][:-1, 1:-1]
    axis_weight = torch.ones_like(director) if unweighted_axis else director**2
    projector_centre = projector_t[:-1, 1:-1]
    if rest_only_spatial_metric:
        spatial_metric = torch.zeros_like(projector_centre)
        spatial_metric[..., 1:4, 1:4] = torch.eye(3, device=DEVICE)
    else:
        spatial_metric = ETA - ETA @ projector_centre
    clock_static_density = (
        parameters.l2_strength
        * axis_weight
        * spatial_metric[..., 0, 0]
        * alternating[..., 0] ** 2
    )
    clock_linear_density = (
        parameters.l2_strength
        * axis_weight
        * alternating[..., 0]
        * torch.einsum(
            "...i,...i->...", spatial_metric[..., 0, 1:4], alternating[..., 1:4]
        )
    )
    inertia_density = parameters.l2_strength * axis_weight * torch.einsum(
        "...i,...ij,...j->...",
        alternating[..., 1:4],
        spatial_metric[..., 1:4, 1:4],
        alternating[..., 1:4],
    )
    scalar_rho, scalar_z = scalar_derivatives(field[..., 6], parameters)
    scalar_energy = parameters.scalar_stiffness * (scalar_rho**2 + scalar_z**2) / 2
    matter_factor = torch.exp(2 * parameters.scalar_coupling * field[:-1, 1:-1, 6])
    return {
        "curvature": matter_factor * curvature_energy,
        "projector": matter_factor * projector_energy,
        "potential": matter_factor * potential,
        "scalar": scalar_energy,
        "clock_static": matter_factor * clock_static_density,
        "clock_linear": matter_factor * clock_linear_density,
        "inertia": matter_factor * inertia_density,
        "alternating_current": alternating,
        "constituent_currents": currents,
        "spatial_metric": spatial_metric,
    }


def observables(
    field: torch.Tensor,
    parameters: Parameters,
    *,
    unweighted_axis: bool = False,
    omit_spatial_current: int | None = None,
    rest_only_spatial_metric: bool = False,
) -> dict[str, torch.Tensor]:
    values = densities(
        field,
        parameters,
        unweighted_axis=unweighted_axis,
        omit_spatial_current=omit_spatial_current,
        rest_only_spatial_metric=rest_only_spatial_metric,
    )
    rho, _ = coordinates(parameters)
    weights = 2 * np.pi * rho[:-1, 1:-1] * parameters.spacing**2
    components = {
        name: torch.sum(weights * values[name])
        for name in (
            "curvature",
            "projector",
            "potential",
            "scalar",
            "clock_static",
            "clock_linear",
            "inertia",
        )
    }
    components["static"] = sum(
        components[name] for name in ("curvature", "projector", "potential", "scalar")
    )
    components["fixed_j_clock"] = (
        parameters.angular_momentum - 2 * components["clock_linear"]
    ) ** 2 / (4 * components["inertia"]) - components["clock_static"]
    components["rotational"] = components["fixed_j_clock"]
    components["total"] = components["static"] + components["fixed_j_clock"]
    components["frequency"] = (
        parameters.angular_momentum - 2 * components["clock_linear"]
    ) / (
        2 * components["inertia"]
    )
    return components


def assemble(interior: torch.Tensor, boundary_seed: torch.Tensor) -> torch.Tensor:
    field = boundary_seed.clone()
    field[:-1, 1:-1] = interior.reshape(field.shape[0] - 1, field.shape[1] - 2, 7)
    return field


def independent_alternating_current_error(
    field: torch.Tensor, parameters: Parameters
) -> float:
    evaluated = densities(field, parameters)
    determinant = evaluated["alternating_current"].detach().cpu().numpy()
    epsilon = alternating_current_from_epsilon(
        evaluated["constituent_currents"]
    ).detach().cpu().numpy()
    return float(
        np.max(np.abs(determinant - epsilon))
        / max(1.0, np.max(np.abs(determinant)), np.max(np.abs(epsilon)))
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
    variable = torch.tensor(
        values.reshape(shape), device=DEVICE, requires_grad=True
    )
    total = observables(assemble(variable, seed), parameters)["total"]
    if not torch.isfinite(total):
        raise FloatingPointError("variational objective became non-finite")
    gradient = torch.autograd.grad(total, variable)[0]
    return float(total.detach()), gradient.detach().cpu().numpy().ravel()


def _energy_value(
    values: np.ndarray,
    shape: tuple[int, ...],
    seed: torch.Tensor,
    parameters: Parameters,
) -> float:
    variable = torch.tensor(values.reshape(shape), device=DEVICE)
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
    variable = torch.tensor(
        values.reshape(shape), device=DEVICE, requires_grad=True
    )
    total = observables(assemble(variable, seed), parameters)["total"]
    gradient = torch.autograd.grad(total, variable, create_graph=True)[0]
    direction = torch.tensor(vector.reshape(shape), device=DEVICE)
    product = torch.sum(gradient * direction)
    result = torch.autograd.grad(product, variable)[0]
    return result.detach().cpu().numpy().ravel()


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
    parameters: Parameters,
    split_sign: float,
    root_iterations: int,
    coefficient_ladder: tuple[float, ...] | None = None,
    dense_single_hessian: bool = False,
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
    initial = interior.detach().cpu().numpy().ravel()
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
                "fatol": 1.0e-8,
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
    eigenvectors = np.empty((values.size, 0), dtype=np.float64)
    dense_coefficient_map = None
    if dense_single_hessian:
        current_hessian = np.empty((values.size, values.size), dtype=np.float64)
        basis = np.zeros(values.size, dtype=np.float64)
        for column in range(values.size):
            basis[column] = 1.0
            current_hessian[:, column] = _hessian_vector(
                values, basis, shape, seed, parameters
            )
            basis[column] = 0.0
            if column % 100 == 0:
                print(
                    json.dumps(
                        {
                            "stage": "dense_single_hessian",
                            "column": column,
                            "columns": values.size,
                        }
                    ),
                    flush=True,
                )
        dense_symmetry = float(
            np.max(np.abs(current_hessian - current_hessian.T))
            / max(1.0, np.max(np.abs(current_hessian)))
        )
        eigenvalues, eigenvectors = dense_eigh(
            current_hessian,
            subset_by_index=(0, 5),
            driver="evr",
        )
        dense_coefficient_map = {
            "dense_single_hessian_symmetry_relative_max": dense_symmetry,
            "dimension": values.size,
        }
    elif coefficient_ladder is not None:
        zero_parameters = replace(parameters, projector_stiffness=0.0)
        unit_parameters = replace(parameters, projector_stiffness=1.0)
        hessian_zero = np.empty((values.size, values.size), dtype=np.float64)
        hessian_unit = np.empty_like(hessian_zero)
        basis = np.zeros(values.size, dtype=np.float64)
        for column in range(values.size):
            basis[column] = 1.0
            hessian_zero[:, column] = _hessian_vector(
                values, basis, shape, seed, zero_parameters
            )
            hessian_unit[:, column] = _hessian_vector(
                values, basis, shape, seed, unit_parameters
            )
            basis[column] = 0.0
            if column % 100 == 0:
                print(
                    json.dumps(
                        {
                            "stage": "dense_hessian",
                            "column": column,
                            "columns": values.size,
                        }
                    ),
                    flush=True,
                )
        projector_hessian = hessian_unit - hessian_zero
        hessian_zero_symmetry = float(
            np.max(np.abs(hessian_zero - hessian_zero.T))
            / max(1.0, np.max(np.abs(hessian_zero)))
        )
        projector_hessian_symmetry = float(
            np.max(np.abs(projector_hessian - projector_hessian.T))
            / max(1.0, np.max(np.abs(projector_hessian)))
        )
        rows = []
        selected_values = None
        selected_vectors = None
        component_names = (
            "anisotropy",
            "common",
            "split",
            "angle_control",
            "boost_rho",
            "boost_z",
            "scalar",
        )
        for stiffness in coefficient_ladder:
            current_parameters = replace(
                parameters, projector_stiffness=stiffness
            )
            current_hessian = hessian_zero + stiffness * projector_hessian
            current_values, current_vectors = dense_eigh(
                current_hessian,
                subset_by_index=(0, 5),
                driver="evr",
            )
            _, current_gradient = _energy_and_gradient(
                values, shape, seed, current_parameters
            )
            current_energy = _energy_value(
                values, shape, seed, current_parameters
            )
            mode = current_vectors[:, 0]
            mode /= np.linalg.norm(mode)
            mode_shape = mode.reshape(shape)
            component_power = np.sum(mode_shape**2, axis=(0, 1))
            curvatures = {}
            relative_errors = {}
            for step in (0.005, 0.0025, 0.00125):
                curvature = (
                    _energy_value(
                        values + step * mode,
                        shape,
                        seed,
                        current_parameters,
                    )
                    - 2 * current_energy
                    + _energy_value(
                        values - step * mode,
                        shape,
                        seed,
                        current_parameters,
                    )
                ) / step**2
                curvatures[str(step)] = float(curvature)
                relative_errors[str(step)] = float(
                    abs(curvature - current_values[0])
                    / max(1.0, abs(curvature), abs(current_values[0]))
                )
            rows.append(
                {
                    "projector_stiffness": stiffness,
                    "root_gradient_inf_relative": float(
                        np.max(np.abs(current_gradient))
                        / max(1.0, abs(current_energy))
                    ),
                    "six_smallest_eigenvalues": [
                        float(value) for value in current_values
                    ],
                    "minimum_mode_component_squared_norm_fractions": {
                        name: float(value)
                        for name, value in zip(component_names, component_power)
                    },
                    "minimum_mode_projector_rayleigh_contribution": float(
                        mode @ projector_hessian @ mode
                    ),
                    "energy_only_centered_curvature": curvatures,
                    "energy_curvature_relative_error": relative_errors,
                }
            )
            if stiffness == parameters.projector_stiffness:
                selected_values = current_values
                selected_vectors = current_vectors
        if selected_values is None:
            raise ValueError(
                "parameters.projector_stiffness must occur in coefficient_ladder"
            )
        eigenvalues = selected_values
        eigenvectors = selected_vectors
        dense_coefficient_map = {
            "hessian_zero_symmetry_relative_max": hessian_zero_symmetry,
            "projector_hessian_symmetry_relative_max": (
                projector_hessian_symmetry
            ),
            "rows": rows,
        }
    else:
        try:
            eigenvalues, eigenvectors = eigsh(
                operator,
                k=1,
                which="SA",
                tol=1.0e-8,
                maxiter=3000,
            )
            order = np.argsort(eigenvalues)
            eigenvalues = eigenvalues[order]
            eigenvectors = eigenvectors[:, order]
        except ArpackNoConvergence as error:
            eigensolver_success = False
            order = np.argsort(error.eigenvalues)
            eigenvalues = error.eigenvalues[order]
            eigenvectors = error.eigenvectors[:, order]
        except Exception:
            eigensolver_success = False
            eigenvalues = np.empty(0, dtype=np.float64)

    negative_mode_audit = None
    if eigenvalues.size and eigenvectors.shape[1]:
        mode = eigenvectors[:, 0]
        mode = mode / np.linalg.norm(mode)
        hessian_mode = matvec(mode)
        rayleigh = float(np.dot(mode, hessian_mode))
        eigen_residual = float(
            np.linalg.norm(hessian_mode - rayleigh * mode)
            / max(1.0, abs(rayleigh))
        )
        mode_shape = mode.reshape(shape)
        component_names = (
            "anisotropy",
            "common",
            "split",
            "angle_control",
            "boost_rho",
            "boost_z",
            "scalar",
        )
        component_power = np.sum(mode_shape**2, axis=(0, 1))
        full_mode = np.zeros(tuple(seed.shape), dtype=np.float64)
        full_mode[:-1, 1:-1] = mode_shape
        outer_mask = np.zeros(shape[:2], dtype=bool)
        outer_mask[-1, :] = True
        outer_mask[:, 0] = True
        outer_mask[:, -1] = True
        energy_curvature = {}
        curvature_relative_error = {}
        perturbed_minimum_inertia = np.inf
        perturbed_minimum_timelike_gap = np.inf
        perturbations_finite = True
        for step in (0.04, 0.02, 0.01, 0.005, 0.0025, 0.00125):
            plus_values = values + step * mode
            minus_values = values - step * mode
            plus_energy = _energy_value(plus_values, shape, seed, parameters)
            minus_energy = _energy_value(minus_values, shape, seed, parameters)
            curvature = (plus_energy - 2 * energy + minus_energy) / step**2
            energy_curvature[str(step)] = float(curvature)
            curvature_relative_error[str(step)] = float(
                abs(curvature - rayleigh)
                / max(1.0, abs(curvature), abs(rayleigh))
            )
            for perturbed_values in (plus_values, minus_values):
                perturbed_field = assemble(
                    torch.tensor(perturbed_values.reshape(shape), device=DEVICE),
                    seed,
                )
                perturbed_observables = observables(perturbed_field, parameters)
                inertia = float(perturbed_observables["inertia"].detach())
                physical_perturbed = physical_components(perturbed_field, parameters)
                perturbed_eigenvalues = torch.stack(
                    physical_perturbed[:3], dim=-1
                )
                gap = float(
                    torch.min(
                        torch.abs(
                            parameters.g
                            + perturbed_field[..., 6, None]
                            - perturbed_eigenvalues
                        )
                    ).detach()
                )
                perturbed_minimum_inertia = min(
                    perturbed_minimum_inertia, inertia
                )
                perturbed_minimum_timelike_gap = min(
                    perturbed_minimum_timelike_gap, gap
                )
                perturbations_finite = perturbations_finite and bool(
                    torch.isfinite(perturbed_observables["total"])
                )
        gradient_hvp_error = {}
        for step in (0.01, 0.005, 0.0025, 0.00125, 0.000625, 0.0003125):
            _, plus_gradient = _energy_and_gradient(
                values + step * mode, shape, seed, parameters
            )
            _, minus_gradient = _energy_and_gradient(
                values - step * mode, shape, seed, parameters
            )
            finite_difference_hvp = (plus_gradient - minus_gradient) / (2 * step)
            gradient_hvp_error[str(step)] = float(
                np.linalg.norm(finite_difference_hvp - hessian_mode)
                / max(
                    1.0,
                    np.linalg.norm(finite_difference_hvp),
                    np.linalg.norm(hessian_mode),
                )
            )
        smallest_steps = ("0.005", "0.0025", "0.00125")
        no_projector_parameters = replace(parameters, projector_stiffness=0.0)
        no_projector_hessian_mode = _hessian_vector(
            values, mode, shape, seed, no_projector_parameters
        )
        projector_hessian_rayleigh_contribution = float(
            np.dot(mode, hessian_mode - no_projector_hessian_mode)
        )
        negative_mode_audit = {
            "ad_rayleigh_quotient": rayleigh,
            "ad_eigen_residual_relative": eigen_residual,
            "energy_only_centered_curvature": energy_curvature,
            "energy_curvature_relative_error": curvature_relative_error,
            "gradient_fd_hvp_relative_error": gradient_hvp_error,
            "all_energy_curvatures_negative": all(
                value < 0 for value in energy_curvature.values()
            ),
            "three_smallest_energy_curvatures_within_two_percent": all(
                curvature_relative_error[key] <= 0.02 for key in smallest_steps
            ),
            "smallest_gradient_hvp_error_within_1e_4": (
                gradient_hvp_error["0.0003125"] <= 1.0e-4
            ),
            "projector_hessian_rayleigh_contribution": (
                projector_hessian_rayleigh_contribution
            ),
            "component_squared_norm_fractions": {
                name: float(value)
                for name, value in zip(component_names, component_power)
            },
            "axis_row_squared_norm_fraction": float(np.sum(mode_shape[0] ** 2)),
            "outer_interior_shell_squared_norm_fraction": float(
                np.sum(mode_shape[outer_mask] ** 2)
            ),
            "reconstructed_boundary_mode_max_abs": float(
                max(
                    np.max(np.abs(full_mode[-1])),
                    np.max(np.abs(full_mode[:, 0])),
                    np.max(np.abs(full_mode[:, -1])),
                )
            ),
            "perturbations_finite": perturbations_finite,
            "perturbed_minimum_inertia": float(perturbed_minimum_inertia),
            "perturbed_minimum_timelike_gap": float(
                perturbed_minimum_timelike_gap
            ),
        }

    variable = torch.tensor(
        values.reshape(shape), device=DEVICE, requires_grad=True
    )
    field = assemble(variable, seed)
    final_observables = observables(field, parameters)
    wrong_variable = torch.tensor(
        values.reshape(shape), device=DEVICE, requires_grad=True
    )
    wrong_total = observables(
        assemble(wrong_variable, seed), parameters, unweighted_axis=True
    )["total"]
    wrong_gradient = torch.autograd.grad(wrong_total, wrong_variable)[0]
    rest_metric_variable = torch.tensor(
        values.reshape(shape), device=DEVICE, requires_grad=True
    )
    rest_metric_total = observables(
        assemble(rest_metric_variable, seed),
        parameters,
        rest_only_spatial_metric=True,
    )["total"]
    rest_metric_gradient = torch.autograd.grad(
        rest_metric_total, rest_metric_variable
    )[0]
    rho_extent = parameters.rho_cells * parameters.spacing
    z_extent = parameters.z_cells * parameters.spacing
    volume_scale = np.pi * rho_extent**2 * z_extent
    inertia_floor = np.sqrt(np.finfo(np.float64).eps) * volume_scale
    omitted_variable = torch.tensor(
        values.reshape(shape), device=DEVICE, requires_grad=True
    )
    omitted_observables = observables(
        assemble(omitted_variable, seed),
        parameters,
        omit_spatial_current=2,
    )
    omitted_total = omitted_observables["total"]
    omitted_inertia = float(omitted_observables["inertia"].detach())
    omitted_gradient_change = None
    if torch.isfinite(omitted_total) and omitted_inertia > inertia_floor:
        omitted_gradient = torch.autograd.grad(omitted_total, omitted_variable)[0]
        omitted_gradient_change = float(
            np.max(
                np.abs(
                    omitted_gradient.detach().cpu().numpy().ravel() - gradient
                )
            )
            / max(1.0, abs(float(omitted_total.detach())), abs(energy))
        )
    field_values = field.detach().cpu().numpy()
    boundary_residual = max(
        float(
            np.max(np.abs(field_values[-1] - seed[-1].detach().cpu().numpy()))
        ),
        float(
            np.max(
                np.abs(field_values[:, 0] - seed[:, 0].detach().cpu().numpy())
            )
        ),
        float(
            np.max(
                np.abs(field_values[:, -1] - seed[:, -1].detach().cpu().numpy())
            )
        ),
    )
    director, tangent, azimuthal, _, boost_rho, boost_z = physical_components(
        field, parameters
    )
    eigenvalue_fields = torch.stack((director, tangent, azimuthal), dim=-1)
    timelike_gap = torch.min(
        torch.abs(parameters.g + field[..., 6, None] - eigenvalue_fields)
    )
    evaluated_densities = densities(field, parameters)
    spatial_metric = evaluated_densities["spatial_metric"]
    spatial_metric_symmetry_error = torch.max(
        torch.abs(spatial_metric - spatial_metric.transpose(-1, -2))
    )
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
        "smallest_hessian_eigenvalues": [float(value) for value in eigenvalues],
        "minimum_hessian_eigenvalue": (
            float(eigenvalues[0]) if eigenvalues.size else None
        ),
        "negative_mode_audit": negative_mode_audit,
        "dense_coefficient_map": dense_coefficient_map,
        "unweighted_axis_mutation_relative_gradient": float(
            torch.max(torch.abs(wrong_gradient)).detach()
            / max(1.0, abs(float(wrong_total.detach())))
        ),
        "rest_only_metric_mutation_relative_gradient_change": float(
            torch.max(
                torch.abs(
                    rest_metric_gradient
                    - torch.tensor(
                        gradient.reshape(shape), device=DEVICE
                    )
                )
            ).detach()
            / max(1.0, abs(float(rest_metric_total.detach())), abs(energy))
        ),
        "omitted_spatial_current_inertia": omitted_inertia,
        "omitted_spatial_current_below_inertia_floor": bool(
            omitted_inertia <= inertia_floor
        ),
        "omitted_spatial_current_mutation_relative_gradient_change": (
            omitted_gradient_change
        ),
        "boundary_residual": boundary_residual,
        "timelike_gap": float(timelike_gap.detach()),
        "spatial_metric_symmetry_max_abs": float(
            spatial_metric_symmetry_error.detach()
        ),
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
        "independent_alternating_current_relative_error": (
            independent_alternating_current_error(field, parameters)
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
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--benchmark-evaluations", type=int, default=0)
    parser.add_argument("--spacing", type=float, default=0.5)
    parser.add_argument("--rho-cells", type=int, default=8)
    parser.add_argument("--z-cells", type=int, default=16)
    parser.add_argument("--adam-steps", type=int, default=1800)
    parser.add_argument("--adam-learning-rate", type=float, default=0.008)
    parser.add_argument("--lbfgsb-iterations", type=int, default=6000)
    parser.add_argument("--lbfgsb-gtol", type=float, default=1.0e-10)
    parser.add_argument("--projector-stiffness", type=float, default=1.0)
    parser.add_argument("--dense-coefficient-map", action="store_true")
    parser.add_argument("--dense-single-hessian", action="store_true")
    parser.add_argument("--root-iterations", type=int, default=240)
    parser.add_argument("--split-signs", nargs="+", type=float, default=(1.0,))
    args = parser.parse_args()
    configure_device(args.device)
    parameters = Parameters(
        spacing=args.spacing,
        rho_cells=args.rho_cells,
        z_cells=args.z_cells,
        adam_steps=args.adam_steps,
        adam_learning_rate=args.adam_learning_rate,
        lbfgsb_iterations=args.lbfgsb_iterations,
        lbfgsb_gtol=args.lbfgsb_gtol,
        projector_stiffness=args.projector_stiffness,
    )
    if args.benchmark_evaluations:
        seed = initial_field(parameters, 1.0)
        interior = seed[:-1, 1:-1].detach().cpu().numpy()
        shape = tuple(interior.shape)
        values = interior.ravel()
        for _ in range(2):
            _energy_and_gradient(values, shape, seed, parameters)
        if DEVICE.type == "cuda":
            torch.cuda.synchronize()
        start = time.perf_counter()
        for _ in range(args.benchmark_evaluations):
            _energy_and_gradient(values, shape, seed, parameters)
        if DEVICE.type == "cuda":
            torch.cuda.synchronize()
        gradient_elapsed = time.perf_counter() - start
        direction = _deterministic_directions(values.size, count=1)[0]
        for _ in range(2):
            _hessian_vector(values, direction, shape, seed, parameters)
        if DEVICE.type == "cuda":
            torch.cuda.synchronize()
        start = time.perf_counter()
        for _ in range(args.benchmark_evaluations):
            _hessian_vector(values, direction, shape, seed, parameters)
        if DEVICE.type == "cuda":
            torch.cuda.synchronize()
        hvp_elapsed = time.perf_counter() - start
        print(
            "P240_BENCHMARK "
            + json.dumps(
                {
                    "attempt": "0021",
                    "device": args.device,
                    "evaluations": args.benchmark_evaluations,
                    "energy_gradient_elapsed_seconds": gradient_elapsed,
                    "seconds_per_energy_gradient": (
                        gradient_elapsed / args.benchmark_evaluations
                    ),
                    "hvp_elapsed_seconds": hvp_elapsed,
                    "seconds_per_hvp": hvp_elapsed / args.benchmark_evaluations,
                    "dtype": "float64",
                },
                sort_keys=True,
            )
        )
        return 0
    starts = [
        solve_branch(
            parameters,
            sign,
            args.root_iterations,
            (
                (1.0, 2.0, 4.0, 8.0, 16.0, 32.0)
                if args.dense_coefficient_map
                else None
            ),
            args.dense_single_hessian,
        )
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
        "attempt": "0021",
        "candidate": "projector_current_plus_alternating_skyrme",
        "environment": {
            "numpy": np.__version__,
            "scipy": __import__("scipy").__version__,
            "torch": torch.__version__,
            "dtype": "float64",
            "device": str(DEVICE),
            "device_name": (
                torch.cuda.get_device_name(DEVICE)
                if DEVICE.type == "cuda"
                else "CPU"
            ),
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
