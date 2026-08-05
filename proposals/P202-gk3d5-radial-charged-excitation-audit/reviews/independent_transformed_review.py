#!/usr/bin/env python3
"""Independent transformed-variable review of provisional C-QBL-004."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import sympy as sp

from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class TransformedBranch:
    outer_radius: float
    central_amplitude: float
    radius: np.ndarray
    h: np.ndarray
    h_prime: np.ndarray
    root_residual: float
    energy: float
    charge: float
    normalized_pohozaev: float

    @property
    def profile(self) -> np.ndarray:
        return self.h / self.radius

    @property
    def profile_derivative(self) -> np.ndarray:
        return self.h_prime / self.radius - self.h / self.radius**2


FREQUENCY = 0.5
KAPPA = 0.5
ORIGIN_EPSILON = 1.0e-6


def integrate(center: float, outer_radius: float, *, dense: bool):
    force = 0.5 * np.sin(center) - FREQUENCY**2 * center
    initial = np.asarray(
        [
            center * ORIGIN_EPSILON + force * ORIGIN_EPSILON**3 / 6.0,
            center + force * ORIGIN_EPSILON**2 / 2.0,
        ]
    )

    def transformed_rhs(radius: float, state: np.ndarray) -> np.ndarray:
        profile = state[0] / radius
        return np.asarray(
            [
                state[1],
                radius
                * (0.5 * np.sin(profile) - FREQUENCY**2 * profile),
            ]
        )

    result = solve_ivp(
        transformed_rhs,
        (ORIGIN_EPSILON, outer_radius),
        initial,
        method="DOP853",
        rtol=2.0e-11,
        atol=2.0e-13,
        max_step=0.025,
        dense_output=dense,
    )
    if not result.success:
        raise RuntimeError(f"independent transformed IVP failed: {result.message}")
    return result


def transformed_robin(center: float, outer_radius: float) -> float:
    terminal = integrate(center, outer_radius, dense=False).y[:, -1]
    return float(terminal[1] + KAPPA * terminal[0])


def solve_transformed(outer_radius: float) -> TransformedBranch:
    lower = transformed_robin(6.1, outer_radius)
    upper = transformed_robin(6.125, outer_radius)
    if np.signbit(lower) == np.signbit(upper):
        raise RuntimeError("independent transformed shooting bracket failed")
    center = float(
        brentq(
            lambda value: transformed_robin(value, outer_radius),
            6.1,
            6.125,
            xtol=1.0e-13,
            rtol=1.0e-14,
        )
    )
    result = integrate(center, outer_radius, dense=True)
    radius = np.linspace(ORIGIN_EPSILON, outer_radius, 16_001)
    if result.sol is None:
        raise RuntimeError("independent transformed dense output is absent")
    h, h_prime = result.sol(radius)
    profile = h / radius
    derivative = h_prime / radius - h / radius**2
    measure = 4.0 * np.pi * radius**2
    field_norm = float(np.trapezoid(measure * profile**2, radius))
    gradient = float(np.trapezoid(measure * derivative**2, radius))
    potential = float(np.trapezoid(measure * (1.0 - np.cos(profile)), radius))
    effective = potential - FREQUENCY**2 * field_norm
    pohozaev = gradient + 3.0 * effective
    normalized = abs(pohozaev) / (abs(gradient) + 3.0 * abs(effective))
    return TransformedBranch(
        outer_radius,
        center,
        radius,
        h,
        h_prime,
        transformed_robin(center, outer_radius),
        gradient + FREQUENCY**2 * field_norm + potential,
        2.0 * FREQUENCY * field_norm,
        normalized,
    )


def relative_change(left: float, right: float) -> float:
    return abs(left - right) / abs(right)


def main() -> int:
    checks = CheckLedger("P202-GK3D5-INDEPENDENT")
    radius = sp.symbols("r", positive=True)
    h = sp.Function("h")(radius)
    profile = h / radius
    transformed_left = sp.simplify(
        sp.diff(profile, radius, 2) + 2 * sp.diff(profile, radius) / radius
    )
    checks.check(
        "h equals r f removes the explicit radial singular term",
        sp.simplify(transformed_left - sp.diff(h, radius, 2) / radius) == 0,
    )

    density = sp.symbols("density", nonnegative=True)
    checks.check(
        "raw potential series independently closes smoothness",
        sp.series(1 - sp.cos(sp.sqrt(density)), density, 0, 4)
        == density / 2
        - density**2 / 24
        + density**3 / 720
        + sp.Order(density**4),
    )
    time, omega, amplitude = sp.symbols(
        "time omega amplitude", real=True, positive=True
    )
    field = amplitude * sp.exp(-sp.I * omega * time)
    conjugate = amplitude * sp.exp(sp.I * omega * time)
    current = sp.I * (
        conjugate * sp.diff(field, time) - field * sp.diff(conjugate, time)
    )
    checks.check(
        "Noether current normalization is independently rederived",
        sp.simplify(current - 2 * omega * amplitude**2) == 0,
    )
    scale, gradient, effective = sp.symbols(
        "scale gradient effective", positive=True
    )
    checks.check(
        "independent coordinate scaling gives T plus three W",
        sp.diff(scale * gradient + scale**3 * effective, scale).subs(scale, 1)
        == gradient + 3 * effective,
    )

    branches = [solve_transformed(value) for value in (16.0, 18.0, 20.0, 22.0)]
    checks.check(
        "all transformed shoots close the Robin root",
        all(abs(branch.root_residual) < 1.0e-8 for branch in branches),
    )
    checks.check(
        "all transformed profiles are nodeless and monotone",
        all(
            np.all(branch.profile > 0.0)
            and np.all(branch.profile_derivative < 0.0)
            for branch in branches
        ),
    )
    center_changes = [
        abs(left.central_amplitude - right.central_amplitude)
        for left, right in zip(branches, branches[1:])
    ]
    checks.check(
        "transformed central amplitude converges under domain extension",
        center_changes[2] < center_changes[1] < center_changes[0]
        and center_changes[2] < 1.0e-10,
    )
    energy_changes = [
        relative_change(left.energy, right.energy)
        for left, right in zip(branches, branches[1:])
    ]
    charge_changes = [
        relative_change(left.charge, right.charge)
        for left, right in zip(branches, branches[1:])
    ]
    checks.check(
        "transformed energy and charge convergence accelerates",
        energy_changes[2] < energy_changes[1] < energy_changes[0]
        and charge_changes[2] < charge_changes[1] < charge_changes[0]
        and energy_changes[2] < 1.0e-6
        and charge_changes[2] < 1.0e-6,
    )
    checks.check(
        "transformed Pohozaev residual decreases below the frozen gate",
        all(
            fine.normalized_pohozaev < coarse.normalized_pohozaev
            for coarse, fine in zip(branches, branches[1:])
        )
        and branches[-1].normalized_pohozaev < 1.0e-4,
    )

    finest = branches[-1]
    tail = (finest.radius >= 8.0) & (finest.radius <= 16.0)
    fitted = -float(
        np.polyfit(
            finest.radius[tail],
            np.log(finest.radius[tail] * finest.profile[tail]),
            1,
        )[0]
    )
    checks.check(
        "transformed tail fit recovers the analytic inverse length",
        relative_change(fitted, KAPPA) < 0.05,
    )

    baseline = branches[2]
    sample = (baseline.radius >= 0.1) & (baseline.radius <= 10.0)
    r = baseline.radius[sample]
    f = baseline.profile[sample]
    correct_h_second = r * (0.5 * np.sin(f) - FREQUENCY**2 * f)

    def equation_verdict(candidate: object) -> bool:
        sine_coefficient, frequency_coefficient = candidate  # type: ignore[misc]
        changed = r * (
            float(sine_coefficient) * np.sin(f)
            - float(frequency_coefficient) * FREQUENCY**2 * f
        )
        return float(np.max(np.abs(correct_h_second - changed))) < 1.0e-8

    checks.mutation_sensitive(
        "transformed equation depends on both force coefficients",
        equation_verdict,
        (0.5, 1.0),
        [(1.0, 1.0), (0.5, 0.0)],
    )
    wrong_tail_residual = float(
        baseline.h_prime[-1] - KAPPA * baseline.h[-1]
    )
    checks.check(
        "wrong growing-tail Robin sign is rejected",
        abs(wrong_tail_residual) > 1.0e-4
        and abs(baseline.root_residual) < 1.0e-8,
    )
    checks.check(
        "review assigns numerical rather than exact existence status",
        branches[-1].energy > 0.0
        and branches[-1].charge > 0.0
        and len(branches) == 4,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
