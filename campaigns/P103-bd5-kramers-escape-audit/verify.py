"""Primary exact, numeric, stochastic, and source verifier for P103 BD5."""

from __future__ import annotations

import ast
import hashlib
import math
from pathlib import Path

import numpy as np
import sympy as sp
import yaml

from substrate_framework.coherence_gates import population_activation_scale
from substrate_framework.first_passage import (
    free_reflected_absorbing_mfpt,
    linear_potential_reflected_absorbing_mfpt,
    quadratic_barrier_gradient,
    quadratic_barrier_potential,
    reflected_absorbing_mfpt,
    simulate_reflected_euler_maruyama,
    summarize_censored_first_passage,
    thresholded_completed_only_rate,
)
from substrate_framework.thermal import declared_coth_effective_scale
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-28/"
    "bridge_BD5_kramers_escape_pde.py"
)
SOURCE_SHA256 = "fd1fd9e54990bbac4a60bc669a37f1c15a89ebd2595203aef7d2bddb88b99cf9"
CONTRACT_SHA256 = "48fff634b6d54c15309bff60767e1515a4b545c50d585895234e1645f610e39a"
FREEZE_SHA256 = "1382d45961ef4965bce86dfb95c6823203a1beb2c617aa96d9207c4cf4e55145"


def _campaign_path() -> Path:
    candidates = (
        Path("campaigns/P103-bd5-kramers-escape-audit"),
        Path("proposals/P103-bd5-kramers-escape-audit"),
    )
    return next(path for path in candidates if path.exists())


def _claims() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text(encoding="utf-8"))
    return {claim["id"]: claim for claim in registry["claims"]}


def _quadratic_mfpt(
    barrier_energy: float,
    ratio: float,
    *,
    absorbing: float = 1.6,
    epsabs: float = 1.0e-11,
    epsrel: float = 1.0e-11,
) -> float:
    return reflected_absorbing_mfpt(
        lambda coordinate: quadratic_barrier_potential(coordinate, barrier_energy),
        0.0,
        0.0,
        absorbing,
        barrier_energy / ratio,
        1.0,
        epsabs=epsabs,
        epsrel=epsrel,
    ).mean_first_passage_time


def _mean_and_standard_error(event_times: np.ndarray) -> tuple[float, float]:
    sample = np.asarray(event_times, dtype=np.float64)
    return float(np.mean(sample)), float(np.std(sample, ddof=1) / np.sqrt(sample.size))


def main() -> int:
    checks = CheckLedger("C-FPT-001")
    campaign = _campaign_path()
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash and pinned BD5 body are unchanged",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    normalized_contract = (campaign / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n",
        b"status: active\n",
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    checks.check(
        "pre-source commitment is immutable",
        hashlib.sha256((campaign / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA256,
    )
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source has thirteen literal checks and a dynamic terminal tally",
        len(source_checks) == 13
        and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source needs no trapezoidal compatibility repair",
        "import numpy as np" in source_text
        and all(
            alias not in source_text
            for alias in ("np." + "trapz", "np." + "trapezoid")
        ),
    )
    escape_function = next(
        node
        for node in source_tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "escape_rate"
    )
    escape_names = {
        node.id for node in ast.walk(escape_function) if isinstance(node, ast.Name)
    }
    checks.check(
        "executable escape model is overdamped and contains no BD4 inertia",
        "gamma" in escape_names
        and "Theta" in escape_names
        and not {"m_R", "lambda", "omega_R"}.intersection(escape_names),
    )

    x, y, z, a, b = sp.symbols("x y z a b", real=True)
    theta, gamma = sp.symbols("Theta gamma", positive=True)
    potential = sp.Function("U", real=True)
    inner = sp.Integral(sp.exp(-potential(z) / theta), (z, a, y))
    mean_time = gamma / theta * sp.Integral(
        sp.exp(potential(y) / theta) * inner,
        (y, x, b),
    )
    first = sp.diff(mean_time, x)
    second = sp.diff(mean_time, x, 2)
    backward_residual = sp.simplify(
        theta * second - sp.diff(potential(x), x) * first + gamma
    )
    checks.check(
        "direct FTC differentiation solves the backward generator equation",
        backward_residual == 0,
    )
    checks.check(
        "integral solution satisfies reflecting and absorbing boundary data",
        sp.simplify(first.subs(x, a)) == 0
        and sp.simplify(mean_time.subs(x, b).doit()) == 0,
    )
    constant = sp.symbols("C", real=True)
    shifted = mean_time.xreplace({potential(y): potential(y) + constant, potential(z): potential(z) + constant})
    checks.check(
        "additive potential constants cancel exactly in the integral",
        sp.simplify(shifted - mean_time) == 0,
    )
    integration_constant = sp.symbols("A", real=True)
    homogeneous_derivative = integration_constant * sp.exp(potential(x) / theta)
    checks.check(
        "reflecting data and absorbing data make the backward solution unique",
        homogeneous_derivative.subs(x, a) == integration_constant * sp.exp(potential(a) / theta)
        and sp.exp(potential(a) / theta).is_zero is False,
    )
    checks.mutation_sensitive(
        "backward drift diffusion and source coefficients are load bearing",
        lambda coefficients: sp.simplify(
            coefficients[0] * theta * second
            - coefficients[1] * sp.diff(potential(x), x) * first
            + coefficients[2] * gamma
        )
        == 0,
        (1, 1, 1),
        ((2, 1, 1), (1, -1, 1), (1, 1, 2)),
    )

    force, length = sp.symbols("F L", positive=True)
    scaled_force = force * length / theta
    linear_exact = gamma * theta * (sp.exp(scaled_force) - 1 - scaled_force) / force**2
    checks.check(
        "linear-force soluble control has the exact zero-force limit",
        sp.limit(linear_exact, force, 0, dir="+") == gamma * length**2 / (2 * theta),
    )
    checks.check(
        "numeric linear controls agree with the adaptive integral",
        all(
            math.isclose(
                reflected_absorbing_mfpt(
                    lambda coordinate, slope=slope: slope * coordinate,
                    0.0,
                    0.0,
                    1.4,
                    0.8,
                    1.3,
                    epsabs=1.0e-12,
                    epsrel=1.0e-12,
                ).mean_first_passage_time,
                linear_potential_reflected_absorbing_mfpt(slope, 1.4, 0.8, 1.3),
                rel_tol=2.0e-9,
                abs_tol=1.0e-11,
            )
            for slope in (-1.2, 0.0, 0.7, 2.0)
        ),
    )
    checks.check(
        "free reflected diffusion control is positive and dimensionally timed",
        free_reflected_absorbing_mfpt(2.0, 0.5, 3.0) == 12.0,
    )
    dimension_energy, dimension_length, dimension_time = sp.eye(3).columnspace()
    potential_dimension = dimension_energy
    thermal_dimension = dimension_energy
    friction_dimension = dimension_energy - 2 * dimension_length + dimension_time
    integral_dimension = 2 * dimension_length
    checks.check(
        "friction over thermal scale times the double coordinate integral has time dimension",
        friction_dimension - thermal_dimension + integral_dimension == dimension_time
        and potential_dimension - thermal_dimension == sp.zeros(3, 1),
    )

    tolerance_values = [
        _quadratic_mfpt(3.0, 5.0, epsabs=tolerance, epsrel=tolerance)
        for tolerance in (1.0e-8, 1.0e-10, 1.0e-12)
    ]
    checks.check(
        "adaptive quadrature is stable through the frozen tolerance sequence",
        max(tolerance_values) - min(tolerance_values)
        < 1.0e-10 * tolerance_values[-1],
    )
    barrier_ratios = np.array([2.0, 3.0, 4.0, 5.0])
    exact_times = np.array([_quadratic_mfpt(3.0, ratio) for ratio in barrier_ratios])
    exact_rates = 1.0 / exact_times
    exact_slope, exact_intercept = np.polyfit(barrier_ratios, np.log(exact_rates), 1)
    checks.check(
        "exact source-family inverse MFPT decreases over ratios two through five",
        np.all(np.diff(exact_rates) < 0.0),
    )
    checks.check(
        "moderate-window log-rate slope contains a boundary-prefactor correction",
        -0.90 < exact_slope < -0.83
        and abs(exact_slope + 1.0) > 0.10
        and np.isfinite(exact_intercept),
        f"exact slope={exact_slope}",
    )
    deep_ratios = np.array([8.0, 12.0, 16.0, 20.0])
    deep_times = np.array([_quadratic_mfpt(3.0, ratio) for ratio in deep_ratios])
    boundary_asymptotic = np.array(
        [
            math.sqrt(math.pi / ratio) * math.exp(ratio) / (2.0 * 3.0)
            for ratio in deep_ratios
        ]
    )
    asymptotic_relative_errors = np.abs(deep_times / boundary_asymptotic - 1.0)
    checks.check(
        "boundary-well Laplace asymptotic converges to the exact MFPT",
        np.all(np.diff(asymptotic_relative_errors) < 0.0)
        and asymptotic_relative_errors[-1] < 0.03,
    )
    checks.check(
        "finite absorbing location is load bearing",
        _quadratic_mfpt(3.0, 3.0, absorbing=1.6)
        > 1.8 * _quadratic_mfpt(3.0, 3.0, absorbing=1.0),
    )
    reversed_drift_time = reflected_absorbing_mfpt(
        lambda coordinate: -quadratic_barrier_potential(coordinate, 3.0),
        0.0,
        0.0,
        1.6,
        1.0,
        1.0,
    ).mean_first_passage_time
    checks.check(
        "drift-sign mutation changes the first-passage observable",
        reversed_drift_time < _quadratic_mfpt(3.0, 3.0) / 3.0,
    )

    completion_probability, completed_mean, survivor_mean, cutoff = sp.symbols(
        "p m_c m_s c", positive=True
    )
    full_population_mean = (
        completion_probability * completed_mean
        + (1 - completion_probability) * survivor_mean
    )
    restricted_population_mean = (
        completion_probability * completed_mean
        + (1 - completion_probability) * cutoff
    )
    checks.check(
        "population decomposition exposes completed-only censoring bias",
        sp.simplify(
            full_population_mean
            - completed_mean
            - (completion_probability - 1) * (completed_mean - survivor_mean)
        )
        == 0
        and sp.simplify(
            restricted_population_mean
            - completed_mean
            - (completion_probability - 1) * (completed_mean - cutoff)
        )
        == 0,
    )
    synthetic = summarize_censored_first_passage(
        [1.0, 2.0, np.nan, np.nan],
        [True, True, False, False],
        10.0,
    )
    checks.check(
        "synthetic administrative censoring separates both reported means",
        synthetic.completed_only_mean == 1.5
        and synthetic.restricted_mean == 5.75
        and synthetic.inverse_completed_only_mean is not None
        and synthetic.inverse_completed_only_mean > synthetic.inverse_restricted_mean,
    )
    checks.check(
        "five-percent rule is an operational zero despite positive exact inverse MFPT",
        thresholded_completed_only_rate(
            summarize_censored_first_passage(
                [np.nan] * 100,
                [False] * 100,
                300.0,
            )
        )
        == 0.0
        and 1.0 / _quadratic_mfpt(20.0, 20.0) > 0.0,
    )

    exact_moderate_time = _quadratic_mfpt(3.0, 3.0)
    timestep_results: list[tuple[float, float, float]] = []
    for time_step in (0.008, 0.004, 0.002):
        ensemble = simulate_reflected_euler_maruyama(
            lambda coordinates: 6.0 * (1.0 - coordinates),
            0.0,
            0.0,
            1.6,
            1.0,
            1.0,
            trajectory_count=12_000,
            time_step=time_step,
            horizon=40.0,
            seed=31_003,
        )
        completed_times = ensemble.event_times[ensemble.completed]
        mean, standard_error = _mean_and_standard_error(completed_times)
        timestep_results.append((ensemble.summary.completion_fraction, mean, standard_error))
    checks.check(
        "three-timestep ensemble study has effectively uncensored moderate paths",
        all(fraction > 0.999 for fraction, _mean, _error in timestep_results),
    )
    checks.check(
        "two finest Euler means are statistically compatible with backward MFPT",
        all(
            abs(mean - exact_moderate_time) < 2.0 * standard_error
            for _fraction, mean, standard_error in timestep_results[-2:]
        ),
    )
    checks.check(
        "halving the fine timestep changes the mean by less than combined uncertainty",
        abs(timestep_results[-1][1] - timestep_results[-2][1])
        < 2.0
        * math.hypot(timestep_results[-1][2], timestep_results[-2][2]),
    )
    ensemble_results: list[tuple[int, float, float]] = []
    for count in (2_000, 4_000, 8_000):
        ensemble = simulate_reflected_euler_maruyama(
            lambda coordinates: 6.0 * (1.0 - coordinates),
            0.0,
            0.0,
            1.6,
            1.0,
            1.0,
            trajectory_count=count,
            time_step=0.004,
            horizon=40.0,
            seed=100 + count,
        )
        mean, standard_error = _mean_and_standard_error(
            ensemble.event_times[ensemble.completed]
        )
        ensemble_results.append((count, mean, standard_error))
    checks.check(
        "three ensemble sizes separately resolve Monte Carlo uncertainty",
        all(
            abs(mean - exact_moderate_time) < 2.0 * standard_error
            for _count, mean, standard_error in ensemble_results
        )
        and ensemble_results[-1][2] < ensemble_results[0][2],
    )

    thermal_coordinate = sp.symbols("vartheta", positive=True)
    energy_quantum = sp.symbols("q", positive=True)
    coth_scale = declared_coth_effective_scale(energy_quantum, thermal_coordinate)
    checks.check(
        "declared coth scale is strictly increasing and has its exact low-coordinate floor",
        sp.simplify(
            sp.diff(coth_scale, thermal_coordinate)
            - energy_quantum**2
            / (
                4
                * thermal_coordinate**2
                * sp.sinh(energy_quantum / (2 * thermal_coordinate)) ** 2
            )
        )
        == 0
        and sp.diff(coth_scale, thermal_coordinate).is_positive is True
        and sp.limit(coth_scale, thermal_coordinate, 0, dir="+") == energy_quantum / 2,
    )
    exact_temperature_points = (
        sp.Rational(2, 5),
        sp.Rational(3, 5),
        sp.Rational(9, 10),
        sp.Rational(13, 10),
    )
    effective_scales = np.array(
        [
            float(declared_coth_effective_scale(sp.sqrt(2) / 2, value))
            for value in exact_temperature_points
        ]
    )
    temperature_rates = np.array(
        [
            1.0
            / reflected_absorbing_mfpt(
                lambda coordinate: quadratic_barrier_potential(coordinate, 2.5),
                0.0,
                0.0,
                1.6,
                scale,
                1.0,
            ).mean_first_passage_time
            for scale in effective_scales
        ]
    )
    checks.check(
        "source temperature points show monotonic response rather than a finite optimum",
        np.all(np.diff(effective_scales) > 0.0)
        and np.all(np.diff(temperature_rates) > 0.0)
        and "kT_onset = hbar*omega_b/2.0" in source_text
        and "0.3 < kT_onset/(hbar*omega_b) < 0.7" in source_text,
    )
    checks.check(
        "population guard is accepted algebra but is not coupled to escape dynamics",
        population_activation_scale(10, sp.Rational(1, 20), 0) == sp.Rational(1, 2)
        and population_activation_scale(10, sp.Rational(1, 20), 1) == 5
        and "Theta_pop" not in escape_names,
    )

    claims = _claims()
    proposed = claims.get("C-FPT-001")
    checks.check(
        "claim identifier is either reserved only or accepted with the exact campaign provenance",
        proposed is None
        or (
            proposed["review"] == "accepted"
            and proposed["provenance"]
            == "campaigns/P103-bd5-kramers-escape-audit/adjudication.yaml"
        ),
    )
    checks.check(
        "accepted interpretation ceilings remain explicit",
        all(
            claim_id in claims
            for claim_id in (
                "C-RG-001",
                "C-RG-002",
                "C-TH-002",
                "C-COH-001",
                "C-COL-001",
                "C-PRB-001",
            )
        )
        and "stochastic escape" in claims["C-COL-001"]["statement"]
        and "not by itself a stochastic rate" in claims["C-TH-002"]["statement"],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
