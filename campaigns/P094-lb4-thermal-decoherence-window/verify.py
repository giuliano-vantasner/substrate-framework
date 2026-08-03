"""Primary exact audit for the P094 LB4 stochastic-coherence campaign."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.coherence_gates import (
    brownian_mean_phasor_window_average,
    brownian_pair_coherence_window_average,
    brownian_phase_characteristic,
    brownian_phase_pair_coherence,
    damped_brownian_coherent_mean_factor,
    damped_brownian_coherent_quadratic_factor,
    gaussian_phase_pair_coherence,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-26/"
    "bridge_LB4_thermal_decoherence_gwindow.py"
)
RUNG047 = Path(
    "/home/dan/substrate/pulson-backreaction-bridge/sympy/rungs/"
    "rung047_intrinsic_mode_noise_sector.py"
)
RUNG056 = Path(
    "/home/dan/substrate/pulson-backreaction-bridge/sympy/rungs/"
    "rung056_theta_eff_concrete_dispersion.py"
)
SOURCE_SHA256 = "e33361e6985002e76342203716fd00ca72c22f905590825a6c064fe472b0d103"
RUNG047_SHA256 = "0b18c568b902bc036ebafcacf5d45f60ad2f3d0768ec6cd19a6ef080bd64bb64"
RUNG056_SHA256 = "ec52262567b1fb9466bae6b632057f62ceef995e7104a2a4f90c78fe11dc8d34"
CONTRACT_SHA256 = "89b384e018b2a485b8483a5c6295469a8248c2183e501e0748c5318ddcac0d09"
FREEZE_SHA256 = "4f5c18bf9dfc48de28a56f5b9a9e309a54541504a1f3f9c38cbdde1ad98fef87"


def _campaign_dir() -> Path:
    candidates = (
        Path("campaigns/P094-lb4-thermal-decoherence-window"),
        Path("proposals/P094-lb4-thermal-decoherence-window"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P094")
    campaign_dir = _campaign_dir()
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("LB4 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
    normalized_contract = (campaign_dir / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n",
        b"status: draft\n",
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    checks.check(
        "partial-exposure freeze record remains immutable",
        _sha256(campaign_dir / "evidence/frozen-proposal.yaml") == FREEZE_SHA256,
    )
    checks.check(
        "supporting predecessor rungs are hash pinned",
        _sha256(RUNG047) == RUNG047_SHA256
        and _sha256(RUNG056) == RUNG056_SHA256,
    )

    check_calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    imported_modules = {
        alias.name
        for node in source_tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    local_functions = {
        node.name for node in source_tree.body if isinstance(node, ast.FunctionDef)
    }
    checks.check(
        "source has forty literal checks and a forty-check terminal path",
        len(check_calls) == 40
        and all(
            node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
            for node in check_calls
        )
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source imports no accepted stochastic or framework implementation",
        imported_modules == {"sys", "math", "sympy", "itertools"}
        and not any(isinstance(node, ast.ImportFrom) for node in source_tree.body)
        and local_functions == {"check", "A_acc"},
    )
    checks.check(
        "source FDT predicate is a self-equality rather than a derivation",
        "sp.simplify(S_xi - 2 * Gamma * Theta_eff) == 0" in source_text
        and "S_xi = 2 * Gamma * Theta_eff" in source_text,
    )
    checks.check(
        "source admits an unfixed order-one phase coefficient",
        "up to an O(1) constant absorbed into the" in source_text
        and "we do NOT claim a hidden O(1) prefactor" in source_text,
    )

    eta, probe_frequency, hbar, thermal_energy, mode_frequency = sp.symbols(
        "eta nu hbar Theta omega_b",
        positive=True,
        real=True,
    )
    quantum_psd = (
        eta
        * probe_frequency
        * hbar
        * sp.coth(hbar * probe_frequency / (2 * thermal_energy))
    )
    low_frequency_psd = sp.limit(quantum_psd, probe_frequency, 0, dir="+")
    zero_temperature_psd = sp.limit(
        quantum_psd,
        thermal_energy,
        0,
        dir="+",
    )
    checks.check(
        "cited Ohmic spectrum has distinct classical and zero-temperature routes",
        sp.simplify(low_frequency_psd - 2 * eta * thermal_energy) == 0
        and sp.simplify(zero_temperature_psd - eta * hbar * probe_frequency)
        == 0,
    )
    checks.check(
        "zero-point spectrum is not a nonzero white low-frequency floor",
        sp.limit(zero_temperature_psd, probe_frequency, 0, dir="+") == 0,
    )
    theta_effective = (
        hbar
        * mode_frequency
        / 2
        * sp.coth(hbar * mode_frequency / (2 * thermal_energy))
    )
    lb4_white_psd = 2 * eta * theta_effective
    checks.check(
        "LB4 white-noise substitution is not the cited low-frequency result",
        sp.simplify(lb4_white_psd - low_frequency_psd) != 0
        and sp.limit(lb4_white_psd, thermal_energy, 0, dir="+")
        == eta * hbar * mode_frequency
        and sp.limit(low_frequency_psd, thermal_energy, 0, dir="+") == 0,
    )
    checks.mutation_sensitive(
        "mode-scale substitution is load bearing",
        lambda scale: sp.simplify(
            2 * eta * scale - 2 * eta * theta_effective
        )
        == 0,
        theta_effective,
        (thermal_energy, hbar * mode_frequency / 2),
    )
    checks.check(
        "coth scale has only its conditional algebraic limits",
        sp.limit(theta_effective / thermal_energy, thermal_energy, sp.oo) == 1
        and sp.limit(theta_effective, thermal_energy, 0, dir="+")
        == hbar * mode_frequency / 2,
    )

    diffusion, time = sp.symbols(
        "D t",
        positive=True,
        real=True,
    )
    harmonic = sp.symbols("n", integer=True)
    variance = 2 * diffusion * time
    characteristic = sp.exp(-(harmonic**2) * diffusion * time)
    checks.check(
        "Brownian phase characteristic solves the Fourier heat equation",
        sp.simplify(
            sp.diff(characteristic, time)
            + diffusion * harmonic**2 * characteristic
        )
        == 0
        and sp.limit(characteristic, time, 0, dir="+") == 1,
    )
    checks.check(
        "canonical Brownian characteristic matches the exact derivation",
        brownian_phase_characteristic(diffusion, time, harmonic)
        == characteristic,
    )
    mean_phasor = characteristic.subs(harmonic, 1)
    pair_coherence = sp.simplify(mean_phasor**2)
    checks.check(
        "mean phasor and pair coherence retain their factor-two distinction",
        mean_phasor == sp.exp(-diffusion * time)
        and pair_coherence == sp.exp(-2 * diffusion * time)
        and mean_phasor != pair_coherence,
    )
    checks.check(
        "accepted Gaussian ensemble maps Brownian variance to pair coherence",
        gaussian_phase_pair_coherence(variance) == pair_coherence,
    )
    checks.check(
        "canonical Brownian pair coherence uses the full variance",
        brownian_phase_pair_coherence(diffusion, time) == pair_coherence,
    )
    checks.mutation_sensitive(
        "Brownian variance factor is load bearing",
        lambda factor: gaussian_phase_pair_coherence(
            factor * diffusion * time
        )
        == pair_coherence,
        2,
        (1, 4),
    )
    checks.check(
        "source renames half the actual variance as phase_rms squared",
        "delta2 = 2 * Gamma_phi * tt" in source_text
        and "phase_rms_sq = Gamma_phi * tt" in source_text,
    )

    damping = sp.symbols("Gamma", positive=True, real=True)
    deterministic_amplitude = sp.exp(-damping * time / 2)
    coherent_mean_factor = sp.simplify(deterministic_amplitude * mean_phasor)
    coherent_quadratic_factor = sp.simplify(
        deterministic_amplitude**2 * pair_coherence
    )
    checks.check(
        "combined source exponent is a coherent mean-field factor",
        sp.simplify(
            coherent_mean_factor
            - sp.exp(-(damping / 2 + diffusion) * time)
        )
        == 0,
    )
    checks.check(
        "the associated coherent quadratic factor is the square, not the same value",
        sp.simplify(
            coherent_quadratic_factor
            - sp.exp(-(damping + 2 * diffusion) * time)
        )
        == 0
        and sp.simplify(coherent_quadratic_factor - coherent_mean_factor**2)
        == 0,
    )
    checks.check(
        "canonical damped Brownian factors preserve observable type",
        sp.simplify(
            damped_brownian_coherent_mean_factor(damping, diffusion, time)
            - coherent_mean_factor
        )
        == 0
        and sp.simplify(
            damped_brownian_coherent_quadratic_factor(
                damping,
                diffusion,
                time,
            )
            - coherent_quadratic_factor
        )
        == 0,
    )
    checks.mutation_sensitive(
        "coherence observable factor is load bearing",
        lambda phase_rate: sp.exp(-(damping + phase_rate) * time)
        == coherent_quadratic_factor,
        2 * diffusion,
        (diffusion, 4 * diffusion),
    )

    window = sp.symbols("T_w", positive=True, real=True)
    endpoint_mean = sp.exp(-diffusion * window)
    window_mean = (1 - sp.exp(-diffusion * window)) / (diffusion * window)
    endpoint_pair = sp.exp(-2 * diffusion * window)
    window_pair = (1 - sp.exp(-2 * diffusion * window)) / (
        2 * diffusion * window
    )
    checks.check(
        "endpoint factors differ from uniform window averages",
        sp.simplify(endpoint_mean - window_mean) != 0
        and sp.simplify(endpoint_pair - window_pair) != 0,
    )
    checks.check(
        "window averages have correct short and long limits",
        sp.limit(window_mean, window, 0, dir="+") == 1
        and sp.limit(window_pair, window, 0, dir="+") == 1
        and sp.limit(window_mean, window, sp.oo) == 0
        and sp.limit(window_pair, window, sp.oo) == 0,
    )
    checks.check(
        "canonical window APIs match direct integration",
        sp.simplify(
            brownian_mean_phasor_window_average(diffusion, window)
            - window_mean
        )
        == 0
        and sp.simplify(
            brownian_pair_coherence_window_average(diffusion, window)
            - window_pair
        )
        == 0,
    )

    coordinate_scaled, momentum = sp.symbols("x y", real=True)
    oscillator_frequency, temperature_scale = sp.symbols(
        "omega Theta",
        positive=True,
        real=True,
    )
    radius_squared = coordinate_scaled**2 + momentum**2
    sigma_squared = 2 * damping * temperature_scale
    phase_x = -momentum / radius_squared
    phase_y = coordinate_scaled / radius_squared
    phase_yy = -2 * coordinate_scaled * momentum / radius_squared**2
    phase_drift = sp.simplify(
        phase_x * oscillator_frequency * momentum
        + phase_y
        * (-oscillator_frequency * coordinate_scaled - damping * momentum)
        + sp.Rational(1, 2) * phase_yy * sigma_squared
    )
    expected_phase_drift = (
        -oscillator_frequency
        - damping * coordinate_scaled * momentum / radius_squared
        - 2
        * damping
        * temperature_scale
        * coordinate_scaled
        * momentum
        / radius_squared**2
    )
    phase_qv_rate = sp.simplify(sigma_squared * phase_y**2)
    checks.check(
        "one-coordinate Langevin phase projection has exact Ito drift",
        sp.simplify(phase_drift - expected_phase_drift) == 0,
    )
    checks.check(
        "one-coordinate Langevin phase diffusion is angle dependent",
        phase_qv_rate.subs(coordinate_scaled, 0) == 0
        and sp.simplify(
            phase_qv_rate.subs(momentum, 0)
            - 2 * damping * temperature_scale / coordinate_scaled**2
        )
        == 0,
    )
    energy = sp.symbols("E", positive=True, real=True)
    averaged_qv_rate = sp.simplify(
        sigma_squared * sp.Rational(1, 2) / (2 * energy)
    )
    averaged_diffusion = sp.simplify(averaged_qv_rate / 2)
    checks.check(
        "fast-phase average gives D=Gamma*Theta/(4E) for the declared SDE",
        averaged_diffusion == damping * temperature_scale / (4 * energy),
    )
    checks.mutation_sensitive(
        "phase-projection normalization is load bearing",
        lambda coefficient: coefficient * damping * temperature_scale / energy
        == averaged_diffusion,
        sp.Rational(1, 4),
        (sp.Rational(1, 2), 1),
    )
    energy_drift = sp.simplify(
        coordinate_scaled * oscillator_frequency * momentum
        + momentum
        * (-oscillator_frequency * coordinate_scaled - damping * momentum)
        + sp.Rational(1, 2) * sigma_squared
    )
    checks.check(
        "same Langevin SDE makes energy stochastic rather than fixed stiffness",
        energy_drift == damping * (temperature_scale - momentum**2),
    )
    initial_energy = sp.symbols("E_0", positive=True, real=True)
    decaying_energy = initial_energy * sp.exp(-damping * time)
    evolving_diffusion = damping * temperature_scale / (4 * decaying_energy)
    integrated_diffusion = sp.integrate(evolving_diffusion, (time, 0, window))
    checks.check(
        "decaying energy makes the projected phase exponent nonconstant",
        sp.simplify(
            integrated_diffusion
            - temperature_scale
            * (sp.exp(damping * window) - 1)
            / (4 * initial_energy)
        )
        == 0
        and sp.simplify(
            integrated_diffusion
            - damping * temperature_scale * window / (4 * initial_energy)
        )
        != 0,
    )

    angular_window = sp.symbols("omega_t", positive=True, real=True)
    cycle_count = angular_window / (2 * sp.pi)
    checks.check(
        "omega times window is angular phase advance rather than cycle count",
        sp.simplify(angular_window / cycle_count - 2 * sp.pi) == 0
        and "n_w = omega_b t_w in [5, 30] cycles" in source_text,
    )
    checks.mutation_sensitive(
        "cycle conversion is load bearing",
        lambda divisor: sp.simplify(angular_window / divisor - cycle_count)
        == 0,
        2 * sp.pi,
        (1, sp.pi),
    )

    target = sp.Rational(1, 8)
    grid_minimum = sp.exp(-sp.Rational(33, 5))
    grid_maximum = sp.exp(-sp.Rational(11, 200))
    grid_central = sp.exp(-sp.Rational(36, 25))
    checks.check(
        "source grid extrema and central point are exact supplied exponents",
        grid_minimum < target < grid_maximum
        and abs(float(grid_central) - 0.23692775868212176) < 1.0e-15,
    )
    checks.check(
        "declared grid nearly spans the entire unit interval",
        float(grid_maximum - grid_minimum) > 0.94,
    )
    ratio, delta, theta = sp.symbols(
        "g delta theta",
        positive=True,
        real=True,
    )
    inverse_window = -sp.log(ratio) / (delta * (sp.Rational(1, 2) + theta))
    checks.check(
        "every target in the unit interval defines a free parameter surface",
        sp.simplify(
            sp.exp(-delta * (sp.Rational(1, 2) + theta) * inverse_window)
            - ratio
        )
        == 0,
    )
    checks.mutation_sensitive(
        "target bracketing depends on the declared window range",
        lambda largest_window: sp.exp(
            -sp.Rational(1, 5)
            * sp.Rational(11, 10)
            * largest_window
        )
        < target
        < grid_maximum,
        30,
        (5,),
    )
    checks.check(
        "source declares rather than derives every grid range and central point",
        "Physical ranges (stated, not fitted to 0.125)" in source_text
        and "delta_c, theta_c, nw_c = 0.10, 0.30, 18.0" in source_text,
    )

    theta_ratio = sp.symbols("theta_ratio", nonnegative=True, real=True)
    source_factor_at_wall = sp.exp(
        -2
        * mode_frequency
        * (sp.Rational(1, 2) + theta_ratio)
        * window
    )
    checks.check(
        "continuous source formula stays positive at its alleged overdamped wall",
        source_factor_at_wall.is_positive
        and "Gamma->inf => g_window->0" in source_text,
    )
    checks.check(
        "source accumulation examples are selected scalar inputs, not dynamics",
        "A_dbd  = A_acc(0.5, delta_rep)" in source_text
        and "A_spark= A_acc(0.01, delta_rep)" in source_text
        and "population" not in local_functions,
    )

    verifier_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    direct_numpy_integrals = [
        node
        for node in ast.walk(verifier_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "np"
        and node.func.attr in {"trapz", "trapezoid"}
    ]
    checks.check(
        "P094 verifier uses no direct version-specific trapezoidal alias",
        not direct_numpy_integrals,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
