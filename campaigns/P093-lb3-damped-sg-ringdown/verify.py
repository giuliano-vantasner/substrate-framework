"""Primary audit verifier for the P093 LB3 ring-down adjudication."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.damped_oscillator import damped_oscillator_regime
from substrate_framework.sine_gordon import (
    breather_damping_form_factor,
    phase_averaged_damped_breather_energy,
    phase_averaged_damped_breather_frequency,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-26/"
    "bridge_LB3_damped_sg_ringdown.py"
)
SOURCE_SHA256 = "1b54ef5704fce1502464f44bd675c01824cfa48b6b98688b1df8f000d1030a2b"
CONTRACT_SHA256 = "edd362c2de354142924f0c3ccbce311d87feca4bf0a6a832b473a385dfae3461"
FREEZE_SHA256 = "6464965ad5471502f9db64df6227566736340034f92726794ce8943fcf38632b"


def _campaign_dir() -> Path:
    candidates = (
        Path("campaigns/P093-lb3-damped-sg-ringdown"),
        Path("proposals/P093-lb3-damped-sg-ringdown"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_fit_times(spatial_step: float = 0.05) -> np.ndarray:
    time_step = 0.4 * spatial_step
    step_count = int(320.0 / time_step)
    times = np.arange(4, step_count + 1, 4, dtype=np.float64) * time_step
    return np.asarray(times[(times >= 40.0) & (times <= 120.0)])


def _reduced_log_slope(omega_initial: float, gamma: float) -> float:
    times = _source_fit_times()
    time_symbol = sp.symbols("t", real=True)
    expression = phase_averaged_damped_breather_energy(
        sp.Float(omega_initial),
        sp.Float(gamma),
        time_symbol,
    )
    evaluator = sp.lambdify(time_symbol, expression, "numpy")
    energy = np.asarray(evaluator(times), dtype=np.float64)
    centered_time = times - np.mean(times)
    centered_log_energy = np.log(energy) - np.mean(np.log(energy))
    return float(
        -np.sum(centered_time * centered_log_energy)
        / np.sum(np.square(centered_time))
    )


def main() -> int:
    checks = CheckLedger("P093")
    campaign_dir = _campaign_dir()
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("LB3 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
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

    literal_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source has eight check-call sites and one terminal tally",
        len(literal_checks) == 8
        and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
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
        "source redefines its full numerical stack without framework imports",
        imported_modules == {"sys", "numpy", "mpmath"}
        and not any(isinstance(node, ast.ImportFrom) for node in source_tree.body)
        and {
            "check",
            "lap1d",
            "grad1d",
            "breather_ic",
            "evolve",
            "fit_decay_rate",
            "core_frequency",
            "D_formfactor",
            "measure",
        }
        <= local_functions,
    )
    checks.check(
        "immutable source chooses the current NumPy integral before its legacy fallback",
        'trapz = np.trapezoid if hasattr(np, "trapezoid") else np.trapz'
        in source_text,
    )

    old, current, acceleration = sp.symbols("old current acceleration", real=True)
    gamma, dt = sp.symbols("Gamma dt", positive=True, real=True)
    source_update = (
        2 * current
        - (1 - gamma * dt / 2) * old
        + dt**2 * acceleration
    ) / (1 + gamma * dt / 2)
    canonical_update = (
        2 * current
        - (1 - sp.Rational(1, 2) * gamma * dt) * old
        + dt**2 * acceleration
    ) / (1 + sp.Rational(1, 2) * gamma * dt)
    checks.check(
        "source recurrence is the existing centered-damping leapfrog update",
        sp.simplify(source_update - canonical_update) == 0,
    )
    checks.check(
        "Gamma zero gives the exact lossless centered recurrence",
        sp.simplify(
            source_update.subs(gamma, 0)
            - (2 * current - old + dt**2 * acceleration)
        )
        == 0,
    )
    checks.mutation_sensitive(
        "damping-centering factor is load bearing",
        lambda factor: sp.simplify(
            (
                2 * current
                - (1 - factor * gamma * dt) * old
                + dt**2 * acceleration
            )
            / (1 + factor * gamma * dt)
            - canonical_update
        )
        == 0,
        sp.Rational(1, 2),
        (0, 1),
    )
    checks.check(
        "source adds a separate sponge update after the centered recurrence",
        "phi_new = phi_new - sp * dt * (phi_new - phi_cur)" in source_text,
    )

    field_t_left, field_x_left, field_t_right, field_x_right = sp.symbols(
        "phi_t_left phi_x_left phi_t_right phi_x_right",
        real=True,
    )
    core_kinetic = sp.symbols("K_R", nonnegative=True, real=True)
    core_flux = field_t_right * field_x_right - field_t_left * field_x_left
    core_energy_rate = core_flux - gamma * core_kinetic
    checks.check(
        "finite-core energy rate contains boundary flux and bulk loss",
        sp.diff(core_energy_rate, core_kinetic) == -gamma
        and sp.diff(core_energy_rate, field_t_right) == field_x_right
        and sp.diff(core_energy_rate, field_t_left) == -field_x_left,
    )
    checks.mutation_sensitive(
        "core-boundary flux is load bearing",
        lambda flux: sp.simplify(flux - gamma * core_kinetic - core_energy_rate)
        == 0,
        core_flux,
        (0, -core_flux),
    )
    checks.check(
        "source records core energy without a core-flux or full energy ledger",
        "rec_Ecore.append" in source_text
        and "Ecore" in source_text
        and "core_flux" not in source_text
        and "energy_balance_residual" not in source_text,
    )

    source_cases = (
        (0.7, 0.010, 0.9425, 0.00954640),
        (0.5, 0.010, 0.8639, 0.00919841),
        (0.7, 0.005, 0.8639, 0.00451065),
        (0.7, 0.015, 0.9425, 0.0148707),
    )
    reduced_slopes = tuple(
        _reduced_log_slope(omega_initial, damping)
        for omega_initial, damping, _fft_frequency, _measured in source_cases
    )
    pointwise_predictions = tuple(
        damping * float(breather_damping_form_factor(sp.Float(fft_frequency)))
        for _omega_initial, damping, fft_frequency, _measured in source_cases
    )
    checks.check(
        "accepted reduced law predicts every reported finite-window slope",
        all(
            abs(measured - reduced) / reduced < 0.015
            for (*_unused, measured), reduced in zip(source_cases, reduced_slopes)
        ),
    )
    checks.check(
        "window-law regression is closer than the selected FFT-bin point rate",
        all(
            abs(measured - reduced) < abs(measured - pointwise)
            for (*_unused, measured), reduced, pointwise in zip(
                source_cases,
                reduced_slopes,
                pointwise_predictions,
            )
        ),
    )
    checks.mutation_sensitive(
        "initial family frequency is load bearing in the window slope",
        lambda omega_initial: abs(
            _reduced_log_slope(float(omega_initial), 0.01)
            - reduced_slopes[0]
        )
        < 1.0e-12,
        0.7,
        (0.5, 0.9),
    )

    sample_times = _source_fit_times()
    sample_spacing = float(np.mean(np.diff(sample_times)))
    fft_bin = 2.0 * np.pi / (sample_times.size * sample_spacing)
    checks.check(
        "reported FFT frequencies are exact bins of the finite source window",
        abs(fft_bin - np.pi / 40.0) < 1.0e-12
        and abs(12 * fft_bin - 0.9424777960769379) < 1.0e-12
        and abs(11 * fft_bin - 0.8639379797371932) < 1.0e-12,
    )
    checks.check(
        "source frequency estimator is an unwindowed single-bin argmax",
        "F = np.abs(np.fft.rfft(cm))" in source_text
        and "kpk = np.argmax(F[1:]) + 1" in source_text
        and "return fr[kpk]" in source_text,
    )
    frequency_drifts: list[float] = []
    time_symbol = sp.symbols("t", real=True)
    for omega_initial, damping, _fft_frequency, _measured in source_cases:
        trajectory = phase_averaged_damped_breather_frequency(
            sp.Float(omega_initial),
            sp.Float(damping),
            time_symbol,
        )
        frequency_drifts.append(
            float(trajectory.subs(time_symbol, sample_times[-1]))
            - float(trajectory.subs(time_symbol, sample_times[0]))
        )
    checks.check(
        "accepted family frequency drifts by more than one FFT bin in every fit",
        all(drift > fft_bin for drift in frequency_drifts),
    )

    checks.check(
        "source high-damping label conflicts with the normalized field mode",
        damped_oscillator_regime(1, 1.75) == "underdamped"
        and damped_oscillator_regime(0.7, 1.75) == "overdamped",
    )
    checks.mutation_sensitive(
        "natural-frequency identification changes the high-damping verdict",
        lambda natural_frequency: damped_oscillator_regime(
            natural_frequency,
            1.75,
        )
        == "underdamped",
        1,
        (0.7, 0.5),
    )
    checks.check(
        "high-damping predicate is finite-time and threshold-defined",
        "tO > T_int" in source_text
        and "np.abs(core_after) > 1e-4" in source_text
        and "surviving_frac < 0.1" in source_text,
    )

    new_code = Path(__file__).read_text(encoding="utf-8")
    new_tree = ast.parse(new_code)
    direct_numpy_integrals = [
        node
        for node in ast.walk(new_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "np"
        and node.func.attr in {"trapz", "trapezoid"}
    ]
    checks.check(
        "P093 verifier introduces no direct version-specific trapezoidal alias",
        not direct_numpy_integrals,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
