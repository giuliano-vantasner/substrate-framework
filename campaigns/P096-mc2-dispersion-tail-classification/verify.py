"""Primary exact audit for the P096 MC2 dispersion and tail campaign."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.dimensional_sine_gordon import (
    dimensional_breather_observables,
    dimensional_sine_gordon_coefficients,
    dimensional_sine_gordon_linear_spectrum,
    dimensional_sine_gordon_linearized_residual,
    dimensional_sine_gordon_scales,
    dimensional_sine_gordon_tail_coefficient,
    dimensional_sine_gordon_time_harmonic_ledger,
    evanescent_half_line_matching_matrix,
    linear_wave_energy_density,
    linear_wave_residual,
    linear_wave_traveling_field,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-27/"
    "bridge_MC2_dispersion_gap_rejection.py"
)
SOURCE_SHA256 = "b73b5a623ae645b1232b09a3f144eb6429f89fbb0cb130a3d223f42129bacef0"
CONTRACT_SHA256 = "6f62689a8d3c6b32f73f3c8bd4d82dfd1d28d503c5535ae9c5cd648934a48ae9"
FREEZE_SHA256 = "2d6743ec2786828447d6d9abd05a4748595652fee374e3e92bf3cf0207d4a58a"


def _campaign_dir() -> Path:
    candidates = (
        Path("campaigns/P096-mc2-dispersion-tail-classification"),
        Path("proposals/P096-mc2-dispersion-tail-classification"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P096")
    campaign_dir = _campaign_dir()
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("MC2 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
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

    check_calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    imports = {
        alias.name
        for node in source_tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    local_functions = {
        node.name for node in source_tree.body if isinstance(node, ast.FunctionDef)
    }
    checks.check(
        "source has twenty-one literal checks and a dynamic terminal tally",
        len(check_calls) == 21
        and all(
            node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
            for node in check_calls
        )
        and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source imports no accepted framework implementation",
        imports == {"sys", "sympy"}
        and not any(isinstance(node, ast.ImportFrom) for node in source_tree.body)
        and local_functions == {"check"},
    )
    checks.check(
        "source gap iff is evaluated only at c equals ell equals one",
        "bool(omega0.subs({c: 1, ell: 1}) > 0)" in source_text,
    )
    checks.check(
        "source regime signs can fall back to finite samples",
        "(sub_pos is True) or sub_pos_num" in source_text
        and "(neg is True) or neg_num" in source_text
        and "(above_neg is True) or above_neg_num" in source_text,
    )
    checks.check(
        "source checks only the positive half-line exponential",
        "env = sp.exp(-kap * sp.Abs(x))" in source_text
        and "sp.diff(env_pos, x, 2)" in source_text
        and "sp.diff(env, x, 2)" not in source_text,
    )
    checks.check(
        "source neither tests global matching nor distinguishes outgoing flux",
        "matching" not in source_text
        and "nullspace" not in source_text
        and "flux" not in source_text,
    )
    checks.check(
        "source's named breather bound predicate checks positivity only",
        "omega_b.is_Symbol and omega_b.is_positive" in source_text,
    )

    lam, tension, mu = sp.symbols("lambda T mu", positive=True, real=True)
    x, time = sp.symbols("x t", real=True)
    epsilon = sp.symbols("epsilon", real=True)
    vacuum_index = sp.symbols("n", integer=True)
    perturbation = sp.Function("psi")(x, time)
    varied_field = 2 * sp.pi * vacuum_index + epsilon * perturbation
    nonlinear_residual = (
        lam * sp.diff(varied_field, time, 2)
        - tension * sp.diff(varied_field, x, 2)
        + mu * sp.sin(varied_field)
    )
    direct_linearization = sp.diff(nonlinear_residual, epsilon).subs(epsilon, 0)
    coefficients = dimensional_sine_gordon_coefficients(lam, tension, mu)
    canonical_linearization = dimensional_sine_gordon_linearized_residual(
        perturbation,
        x,
        time,
        coefficients,
    )
    checks.check(
        "direct vacuum derivative gives the canonical linearized residual",
        sp.simplify(direct_linearization - canonical_linearization) == 0,
    )
    checks.mutation_sensitive(
        "linearized mass speed and signs are load bearing",
        lambda candidate: sp.simplify(candidate - direct_linearization) == 0,
        canonical_linearization,
        (
            lam * sp.diff(perturbation, time, 2)
            + tension * sp.diff(perturbation, x, 2)
            + mu * perturbation,
            lam * sp.diff(perturbation, time, 2)
            - tension * sp.diff(perturbation, x, 2)
            - mu * perturbation,
            2 * lam * sp.diff(perturbation, time, 2)
            - tension * sp.diff(perturbation, x, 2)
            + mu * perturbation,
        ),
    )

    k, angular = sp.symbols("k Omega", real=True)
    plane_wave = sp.exp(sp.I * (k * x - angular * time))
    characteristic = sp.simplify(
        dimensional_sine_gordon_linearized_residual(
            plane_wave,
            x,
            time,
            coefficients,
        )
        / (lam * plane_wave)
    )
    scales = dimensional_sine_gordon_scales(coefficients)
    expected_characteristic = (
        -angular**2
        + scales.gap_frequency**2
        + scales.signal_speed**2 * k**2
    )
    checks.check(
        "plane-wave substitution derives the physical dispersion",
        sp.simplify(characteristic - expected_characteristic) == 0,
    )
    checks.mutation_sensitive(
        "dispersion coefficients and band term are load bearing",
        lambda candidate: sp.simplify(characteristic - candidate) == 0,
        expected_characteristic,
        (
            -angular**2 - scales.gap_frequency**2 + scales.signal_speed**2 * k**2,
            -angular**2 + scales.gap_frequency**2 - scales.signal_speed**2 * k**2,
            -angular**2 + 2 * scales.gap_frequency**2 + scales.signal_speed**2 * k**2,
        ),
    )

    positive_k = sp.symbols("k_pos", positive=True, real=True)
    spectrum = dimensional_sine_gordon_linear_spectrum(positive_k, coefficients)
    expected_squared = scales.gap_frequency**2 + scales.signal_speed**2 * positive_k**2
    checks.check(
        "positive spectrum has the exact nonzero band floor",
        sp.simplify(spectrum.angular_frequency_squared - expected_squared) == 0
        and sp.limit(spectrum.angular_frequency, positive_k, 0, dir="+")
        == scales.gap_frequency
        and sp.simplify(expected_squared - scales.gap_frequency**2)
        == scales.signal_speed**2 * positive_k**2,
    )
    checks.check(
        "phase and group velocities have the exact product and ordering",
        spectrum.phase_velocity is not None
        and sp.simplify(spectrum.phase_velocity * spectrum.group_velocity)
        == scales.signal_speed**2
        and sp.simplify(spectrum.phase_velocity**2 - scales.signal_speed**2)
        == scales.gap_frequency**2 / positive_k**2
        and sp.simplify(
            scales.signal_speed**2 - spectrum.group_velocity**2
        )
        == sp.simplify(
            scales.signal_speed**2
            * scales.gap_frequency**2
            / expected_squared
        ),
    )
    checks.check(
        "velocity limits recover zero group speed and the signal-speed asymptote",
        sp.limit(spectrum.group_velocity, positive_k, 0, dir="+") == 0
        and sp.limit(spectrum.phase_velocity, positive_k, 0, dir="+") == sp.oo
        and sp.limit(spectrum.group_velocity, positive_k, sp.oo)
        == scales.signal_speed
        and sp.limit(spectrum.phase_velocity, positive_k, sp.oo)
        == scales.signal_speed,
    )
    normalized = dimensional_sine_gordon_linear_spectrum(
        positive_k,
        dimensional_sine_gordon_coefficients(1, 1, 1),
    )
    checks.check(
        "unit coefficients recover the accepted normalized dispersion",
        normalized.angular_frequency_squared == 1 + positive_k**2,
    )

    exact_coefficients = dimensional_sine_gordon_coefficients(2, 8, 18)
    subgap = dimensional_sine_gordon_time_harmonic_ledger(1, exact_coefficients)
    threshold = dimensional_sine_gordon_time_harmonic_ledger(3, exact_coefficients)
    above_gap = dimensional_sine_gordon_time_harmonic_ledger(5, exact_coefficients)
    checks.check(
        "tail coefficient classifies sub-gap threshold and above-gap branches",
        subgap.spatial_coefficient == 2
        and subgap.behavior == "evanescent"
        and threshold.spatial_coefficient == 0
        and threshold.behavior == "threshold"
        and above_gap.spatial_coefficient == -4
        and above_gap.behavior == "oscillatory",
    )
    checks.mutation_sensitive(
        "tail coefficient frequency mass and speed factors are load bearing",
        lambda candidate: sp.simplify(
            candidate
            - dimensional_sine_gordon_tail_coefficient(1, exact_coefficients)
        )
        == 0,
        sp.Integer(2),
        (sp.Integer(-2), sp.Integer(8), sp.Rational(1, 2)),
    )

    rate = sp.symbols("kappa", positive=True, real=True)
    matching = evanescent_half_line_matching_matrix(rate)
    checks.check(
        "two decaying half-line branches have a full-rank smooth matching matrix",
        matching == sp.Matrix([[1, -1], [-rate, -rate]])
        and matching.det() == -2 * rate
        and matching.rank() == 2
        and matching.nullspace() == [],
    )
    checks.mutation_sensitive(
        "derivative matching sign is load bearing",
        lambda candidate: candidate.det() == -2 * rate,
        matching,
        (
            sp.Matrix([[1, -1], [-rate, rate]]),
            sp.Matrix([[1, 1], [-rate, -rate]]),
        ),
    )
    right_derivative = -rate
    left_derivative = rate
    checks.check(
        "the exp-minus-kappa-abs-x cusp carries a derivative jump",
        sp.simplify(right_derivative - left_derivative) == -2 * rate,
    )
    checks.check(
        "the homogeneous whole line has no nonzero L2 separated mode in any branch",
        subgap.right_half_line_l2_dimension == 1
        and subgap.left_half_line_l2_dimension == 1
        and subgap.whole_line_l2_dimension == 0
        and threshold.right_half_line_l2_dimension == 0
        and threshold.whole_line_l2_dimension == 0
        and above_gap.right_half_line_l2_dimension == 0
        and above_gap.whole_line_l2_dimension == 0,
    )

    normalized_frequency = sp.Rational(1, 2)
    observables = dimensional_breather_observables(
        normalized_frequency,
        exact_coefficients,
    )
    tail_coefficient = dimensional_sine_gordon_tail_coefficient(
        observables.angular_frequency,
        exact_coefficients,
    )
    checks.check(
        "the exact nonlinear breather tail matches the independent linear exponent",
        sp.simplify(tail_coefficient - observables.inverse_width**2) == 0,
    )

    speed, wave_number = sp.symbols("c q", positive=True, real=True)
    wave_angular = sp.sqrt(9 + speed**2 * wave_number**2)
    standing = sp.cos(wave_number * x) * sp.cos(wave_angular * time)
    traveling = sp.cos(wave_number * x - wave_angular * time)
    standing_flux = -sp.diff(standing, time) * sp.diff(standing, x)
    traveling_flux = -sp.diff(traveling, time) * sp.diff(traveling, x)
    period = 2 * sp.pi / wave_angular
    standing_average = sp.simplify(
        sp.integrate(standing_flux, (time, 0, period)) / period
    )
    traveling_average = sp.simplify(
        sp.integrate(traveling_flux, (time, 0, period)) / period
    )
    checks.check(
        "oscillatory dispersion alone does not impose outgoing radiation",
        standing_average == 0
        and sp.simplify(traveling_average - wave_angular * wave_number / 2) == 0,
    )

    profile = sp.Function("F")
    gapless_field = linear_wave_traveling_field(profile, x, time, speed)
    checks.check(
        "the gapless equation admits every differentiable traveling profile",
        sp.simplify(linear_wave_residual(gapless_field, x, time, speed)) == 0,
    )
    sech_field = linear_wave_traveling_field(sp.sech, x, time, speed)
    energy_density = linear_wave_energy_density(
        sech_field,
        x,
        time,
        1,
        speed**2,
    ).subs(time, 0)
    antiderivative = speed**2 * sp.tanh(x) ** 3 / 3
    checks.check(
        "a localized gapless traveling packet has finite exact energy",
        sp.simplify(energy_density - speed**2 * sp.sech(x) ** 2 * sp.tanh(x) ** 2)
        == 0
        and sp.simplify(sp.diff(antiderivative, x) - energy_density) == 0
        and sp.limit(antiderivative, x, sp.oo)
        - sp.limit(antiderivative, x, -sp.oo)
        == 2 * speed**2 / 3,
    )
    checks.check(
        "gapless traveling packets do not create an L2 time-harmonic eigenmode",
        linear_wave_traveling_field(sp.sech, x, time, speed).has(time)
        and sp.simplify(
            linear_wave_traveling_field(sp.sech, x, time + 1, speed)
            - linear_wave_traveling_field(sp.sech, x, time, speed)
        )
        != 0,
    )

    verifier_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    canonical_tree = ast.parse(
        Path("src/substrate_framework/dimensional_sine_gordon.py").read_text(
            encoding="utf-8"
        )
    )
    direct_alias_calls = [
        node
        for tree in (verifier_tree, canonical_tree)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "np"
        and node.func.attr in {"trapz", "trapezoid"}
    ]
    checks.check(
        "exact P096 implementation uses no direct NumPy trapezoidal alias",
        direct_alias_calls == [],
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
