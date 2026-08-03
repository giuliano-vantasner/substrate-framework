"""Independent P103 rederivation without the canonical first-passage API."""

from __future__ import annotations

import ast
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.integrate import solve_bvp
import sympy as sp

from substrate_framework.verification import CheckLedger


def _high_precision_quadratic_mfpt(ratio: int, *, absorbing: float = 1.6) -> float:
    mp.mp.dps = 45
    energy = mp.mpf(3)
    thermal = energy / ratio
    boundary = mp.mpf(str(absorbing))

    def potential(coordinate: mp.mpf) -> mp.mpf:
        return energy * (2 * coordinate - coordinate**2)

    integral = mp.quad(
        lambda outer: mp.exp(potential(outer) / thermal)
        * mp.quad(
            lambda inner: mp.exp(-potential(inner) / thermal),
            [0, outer],
        ),
        [0, boundary],
    )
    return float(integral / thermal)


def _backward_collocation(ratio: int, tolerance: float) -> tuple[float, float, int]:
    energy = 3.0
    thermal = energy / ratio
    absorbing = 1.6
    coordinate = np.linspace(0.0, absorbing, 21)
    guess = np.vstack(
        (
            (absorbing**2 - coordinate**2) / (2.0 * thermal),
            -coordinate / thermal,
        )
    )
    result = solve_bvp(
        lambda position, state: np.vstack(
            (
                state[1],
                (2.0 * energy * (1.0 - position) * state[1] - 1.0) / thermal,
            )
        ),
        lambda left, right: np.array([left[1], right[0]]),
        coordinate,
        guess,
        tol=tolerance,
        max_nodes=20_000,
    )
    if not result.success:
        raise RuntimeError(result.message)
    return (
        float(result.y[0, 0]),
        float(np.max(result.rms_residuals, initial=0.0)),
        int(result.x.size),
    )


def main() -> int:
    checks = CheckLedger("C-FPT-001-INDEPENDENT")
    x, y, z, left, right = sp.symbols("x y z a b", real=True)
    theta, gamma = sp.symbols("Theta gamma", positive=True)
    potential = sp.Function("V", real=True)
    inner = sp.Integral(sp.exp(-potential(z) / theta), (z, left, y))
    candidate = gamma / theta * sp.Integral(
        sp.exp(potential(y) / theta) * inner,
        (y, x, right),
    )
    candidate_prime = sp.diff(candidate, x)
    checks.check(
        "fresh integrating-factor candidate has reflecting data",
        sp.simplify(candidate_prime.subs(x, left)) == 0,
    )
    checks.check(
        "fresh integral has absorbing data",
        sp.simplify(candidate.subs(x, right).doit()) == 0,
    )
    checks.check(
        "fresh differentiation gives the backward equation",
        sp.simplify(
            theta * sp.diff(candidate, x, 2)
            - sp.diff(potential(x), x) * candidate_prime
            + gamma
        )
        == 0,
    )
    offset = sp.symbols("C", real=True)
    shifted_candidate = candidate.xreplace(
        {potential(y): potential(y) + offset, potential(z): potential(z) + offset}
    )
    checks.check(
        "fresh potential-offset substitution cancels",
        sp.simplify(shifted_candidate - candidate) == 0,
    )

    force, length = sp.symbols("F L", positive=True)
    direct_linear = sp.simplify(
        gamma
        / theta
        * sp.integrate(
            sp.exp(force * y / theta)
            * sp.integrate(sp.exp(-force * z / theta), (z, 0, y)),
            (y, 0, length),
        )
    )
    expected_linear = gamma * theta * (
        sp.exp(force * length / theta) - 1 - force * length / theta
    ) / force**2
    checks.check(
        "fresh direct linear-potential integration gives the closed form",
        sp.simplify(direct_linear - expected_linear) == 0,
    )
    checks.check(
        "fresh linear formula recovers reflected free diffusion",
        sp.limit(expected_linear, force, 0, dir="+")
        == gamma * length**2 / (2 * theta),
    )

    first_moment_at_reflection = gamma * length**2 / (2 * theta)
    second_moment_at_reflection = 5 * gamma**2 * length**4 / (12 * theta**2)
    checks.check(
        "fresh free-diffusion second moment is not exponential",
        sp.simplify(
            second_moment_at_reflection - 2 * first_moment_at_reflection**2
        )
        != 0
        and sp.simplify(
            (second_moment_at_reflection - first_moment_at_reflection**2)
            / first_moment_at_reflection**2
        )
        == sp.Rational(2, 3),
    )
    checks.check(
        "inverse MFPT therefore need not be a constant hazard",
        sp.Rational(2, 3) != 1,
    )

    ratios = (2, 3, 5, 8)
    references = {ratio: _high_precision_quadratic_mfpt(ratio) for ratio in ratios}
    checks.check(
        "fresh high-precision nested quadrature is positive across the source family",
        all(math.isfinite(value) and value > 0.0 for value in references.values()),
    )
    all_errors: dict[int, list[float]] = {}
    final_residuals: dict[int, float] = {}
    final_nodes: dict[int, int] = {}
    for ratio in ratios:
        errors: list[float] = []
        for tolerance in (1.0e-4, 1.0e-6, 1.0e-8):
            value, residual, nodes = _backward_collocation(ratio, tolerance)
            errors.append(abs(value - references[ratio]) / references[ratio])
            final_residuals[ratio] = residual
            final_nodes[ratio] = nodes
        all_errors[ratio] = errors
    checks.check(
        "fresh collocation solves report finite refined meshes",
        all(final_nodes[ratio] > 21 for ratio in ratios),
    )
    checks.check(
        "fresh collocation error decreases at every tolerance refinement",
        all(
            errors[2] < errors[1] < errors[0]
            for errors in all_errors.values()
        ),
    )
    checks.check(
        "fresh collocation residual reaches the frozen scale",
        max(final_residuals.values()) < 1.1e-8,
    )
    checks.check(
        "fresh collocation and high-precision quadrature agree beyond the frozen gate",
        max(errors[-1] for errors in all_errors.values()) < 2.0e-5,
    )

    source_window = np.array([references[ratio] for ratio in (2, 3, 5)])
    checks.check(
        "fresh source-family MFPT increases with barrier ratio",
        np.all(np.diff(source_window) > 0.0),
    )
    ratios_four = np.array([2.0, 3.0, 4.0, 5.0])
    times_four = np.array(
        [_high_precision_quadratic_mfpt(int(ratio)) for ratio in ratios_four]
    )
    slope = float(np.polyfit(ratios_four, np.log(1.0 / times_four), 1)[0])
    checks.check(
        "fresh four-point inverse-MFPT slope is not a pure minus-one law",
        -0.90 < slope < -0.83 and abs(slope + 1.0) > 0.10,
        f"slope={slope}",
    )
    deep_ratios = (8, 12, 16, 20)
    deep_exact = np.array([_high_precision_quadratic_mfpt(ratio) for ratio in deep_ratios])
    deep_asymptotic = np.array(
        [math.sqrt(math.pi / ratio) * math.exp(ratio) / 6.0 for ratio in deep_ratios]
    )
    asymptotic_errors = np.abs(deep_exact / deep_asymptotic - 1.0)
    checks.check(
        "fresh boundary-well asymptotic converges independently",
        np.all(np.diff(asymptotic_errors) < 0.0) and asymptotic_errors[-1] < 0.03,
    )

    top_absorption = _high_precision_quadratic_mfpt(3, absorbing=1.0)
    downhill_absorption = references[3]
    checks.check(
        "fresh absorbing-boundary mutation changes the observable by order one",
        downhill_absorption > 1.8 * top_absorption,
    )
    full_times = np.array([1.0, 2.0, 12.0, 20.0])
    horizon = 10.0
    completed = full_times <= horizon
    completed_mean = float(np.mean(full_times[completed]))
    restricted_mean = float(np.mean(np.minimum(full_times, horizon)))
    full_mean = float(np.mean(full_times))
    checks.check(
        "fresh censored counterexample orders completed restricted and full means",
        completed_mean < restricted_mean < full_mean,
    )
    checks.check(
        "fresh completed-only inverse mean overstates the full inverse mean",
        1.0 / completed_mean > 5.0 * (1.0 / full_mean),
    )
    checks.check(
        "fresh deep-barrier exact rate stays positive despite a zero-completion convention",
        1.0 / _high_precision_quadratic_mfpt(20) > 0.0,
    )
    checks.check(
        "independent review imports no canonical first-passage implementation",
        all(
            not isinstance(node, ast.ImportFrom)
            or node.module != "substrate_framework.first_passage"
            for node in ast.walk(
                ast.parse(Path(__file__).read_text(encoding="utf-8"))
            )
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
