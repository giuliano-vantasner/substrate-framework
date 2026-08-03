"""Independent exact reconstruction of P094's stochastic obligations."""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P094-INDEPENDENT")

    phase, diffusion, time, mode = sp.symbols(
        "delta D t n",
        real=True,
        positive=True,
    )
    density = sp.exp(-phase**2 / (4 * diffusion * time)) / sp.sqrt(
        4 * sp.pi * diffusion * time
    )
    normalization = sp.integrate(density, (phase, -sp.oo, sp.oo))
    second_moment = sp.integrate(
        phase**2 * density,
        (phase, -sp.oo, sp.oo),
    )
    characteristic_integral = sp.integrate(
        sp.exp(sp.I * mode * phase) * density,
        (phase, -sp.oo, sp.oo),
    )
    characteristic = sp.exp(-diffusion * mode**2 * time)
    checks.check(
        "Gaussian heat kernel independently normalizes",
        sp.simplify(normalization - 1) == 0,
    )
    checks.check(
        "Gaussian heat kernel independently gives variance 2Dt",
        sp.simplify(second_moment - 2 * diffusion * time) == 0,
    )
    checks.check(
        "direct Gaussian integral gives the Brownian characteristic function",
        sp.simplify(characteristic_integral - characteristic) == 0,
    )

    mean_phasor = characteristic.subs(mode, 1)
    pair_coherence = sp.expand_power_base(mean_phasor**2, force=True)
    checks.check(
        "fresh characteristic route separates mean and pair observables",
        mean_phasor == sp.exp(-diffusion * time)
        and sp.simplify(pair_coherence - sp.exp(-2 * diffusion * time)) == 0,
    )
    checks.mutation_sensitive(
        "independent pair observable rejects the source half variance",
        lambda variance_factor: sp.exp(
            -variance_factor * diffusion * time
        )
        == sp.exp(-2 * diffusion * time),
        2,
        (1, 4),
    )

    window = sp.symbols("T", positive=True, real=True)
    direct_mean_average = sp.integrate(
        sp.exp(-diffusion * time),
        (time, 0, window),
    ) / window
    direct_pair_average = sp.integrate(
        sp.exp(-2 * diffusion * time),
        (time, 0, window),
    ) / window
    checks.check(
        "independent integration gives both uniform-window averages",
        sp.simplify(
            direct_mean_average
            - (1 - sp.exp(-diffusion * window)) / (diffusion * window)
        )
        == 0
        and sp.simplify(
            direct_pair_average
            - (1 - sp.exp(-2 * diffusion * window))
            / (2 * diffusion * window)
        )
        == 0,
    )
    checks.mutation_sensitive(
        "endpoint substitution is not a window average",
        lambda candidate: sp.simplify(candidate - direct_mean_average) == 0,
        direct_mean_average,
        (sp.exp(-diffusion * window), sp.exp(-2 * diffusion * window)),
    )

    coordinate, momentum, omega, damping, theta = sp.symbols(
        "q p omega Gamma Theta",
        real=True,
        positive=True,
    )
    energy = (momentum**2 + omega**2 * coordinate**2) / 2
    gibbs_density = sp.exp(-energy / theta)
    fpe_stationary_residual = sp.simplify(
        -sp.diff(momentum * gibbs_density, coordinate)
        - sp.diff(
            (-omega**2 * coordinate - damping * momentum) * gibbs_density,
            momentum,
        )
        + damping * theta * sp.diff(gibbs_density, momentum, 2)
    )
    checks.check(
        "declared one-coordinate FDT SDE has the Gibbs stationary density",
        fpe_stationary_residual == 0,
    )
    checks.mutation_sensitive(
        "FDT noise normalization is load bearing in stationarity",
        lambda noise_factor: sp.simplify(
            -sp.diff(momentum * gibbs_density, coordinate)
            - sp.diff(
                (-omega**2 * coordinate - damping * momentum)
                * gibbs_density,
                momentum,
            )
            + noise_factor
            * damping
            * theta
            * sp.diff(gibbs_density, momentum, 2)
        )
        == 0,
        1,
        (sp.Rational(1, 2), 2),
    )

    scaled_coordinate = sp.symbols("x", real=True)
    radius = sp.symbols("r", positive=True, real=True)
    angle = sp.symbols("alpha", real=True)
    sigma_squared = 2 * damping * theta
    radius_squared = scaled_coordinate**2 + momentum**2
    phase_gradient_momentum = scaled_coordinate / radius_squared
    quadratic_variation = sp.simplify(
        sigma_squared * phase_gradient_momentum**2
    )
    angular_qv = sp.simplify(
        quadratic_variation.subs(
            {
                scaled_coordinate: radius * sp.cos(angle),
                momentum: radius * sp.sin(angle),
            },
            simultaneous=True,
        )
    )
    angular_qv = sp.trigsimp(angular_qv)
    averaged_qv = sp.integrate(angular_qv, (angle, 0, 2 * sp.pi)) / (
        2 * sp.pi
    )
    energy_symbol = sp.symbols("E", positive=True, real=True)
    averaged_qv_energy = sp.simplify(
        averaged_qv.subs(radius**2, 2 * energy_symbol)
    )
    checks.check(
        "fresh angular integration gives averaged phase quadratic variation",
        averaged_qv_energy == damping * theta / (2 * energy_symbol),
    )
    independent_diffusion = sp.simplify(averaged_qv_energy / 2)
    checks.check(
        "Brownian convention halves quadratic variation to D=GammaTheta/(4E)",
        independent_diffusion == damping * theta / (4 * energy_symbol),
    )
    checks.mutation_sensitive(
        "independent phase projection rejects LB4 normalization",
        lambda coefficient: coefficient * damping * theta / energy_symbol
        == independent_diffusion,
        sp.Rational(1, 4),
        (sp.Rational(1, 2), 1),
    )

    energy_generator = sp.simplify(
        momentum * sp.diff(energy, coordinate)
        + (-omega**2 * coordinate - damping * momentum)
        * sp.diff(energy, momentum)
        + damping * theta * sp.diff(energy, momentum, 2)
    )
    checks.check(
        "independent generator makes energy an evolving stochastic coordinate",
        energy_generator == damping * (theta - momentum**2),
    )
    initial_energy = sp.symbols("E_0", positive=True, real=True)
    approximate_energy = initial_energy * sp.exp(-damping * time)
    accumulated_phase = sp.integrate(
        damping * theta / (4 * approximate_energy),
        (time, 0, window),
    )
    checks.check(
        "independent evolving-energy route rejects a global constant phase rate",
        sp.simplify(
            accumulated_phase
            - theta * (sp.exp(damping * window) - 1) / (4 * initial_energy)
        )
        == 0
        and sp.diff(accumulated_phase, window, 2) != 0,
    )

    angular_advance = sp.symbols("Omega_t", positive=True, real=True)
    checks.check(
        "independent phase-period count contains two pi",
        sp.simplify(
            angular_advance / (2 * sp.pi) * 2 * sp.pi - angular_advance
        )
        == 0,
    )
    checks.mutation_sensitive(
        "independent cycle count rejects angular advance as cycles",
        lambda divisor: sp.simplify(
            angular_advance / divisor - angular_advance / (2 * sp.pi)
        )
        == 0,
        2 * sp.pi,
        (1, sp.pi),
    )

    target, delta, ratio = sp.symbols(
        "g delta theta_ratio",
        positive=True,
        real=True,
    )
    inferred_window = -sp.log(target) / (
        delta * (sp.Rational(1, 2) + ratio)
    )
    checks.check(
        "fresh inversion exposes the comparator-fitting surface",
        sp.simplify(
            sp.exp(
                -delta
                * (sp.Rational(1, 2) + ratio)
                * inferred_window
            )
            - target
        )
        == 0,
    )
    checks.mutation_sensitive(
        "the 0.125 verdict depends on selected grid endpoints",
        lambda high_exponent: sp.exp(-high_exponent)
        < sp.Rational(1, 8)
        < sp.exp(-sp.Rational(11, 200)),
        sp.Rational(33, 5),
        (sp.Rational(11, 10),),
    )

    source_formula_at_wall = sp.exp(
        -2
        * omega
        * (sp.Rational(1, 2) + ratio)
        * window
    )
    checks.check(
        "finite continuous exponential does not create an overdamped hard zero",
        source_formula_at_wall.is_positive,
    )

    review_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    direct_numpy_integrals = [
        node
        for node in ast.walk(review_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "np"
        and node.func.attr in {"trapz", "trapezoid"}
    ]
    checks.check(
        "independent review uses no direct NumPy trapezoidal alias",
        not direct_numpy_integrals,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
