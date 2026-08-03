"""Independent exact reconstruction of P096 without importing its new APIs."""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P096-INDEPENDENT")

    lam, tension, mu = sp.symbols("lambda T mu", positive=True, real=True)
    x, time = sp.symbols("x t", real=True)
    epsilon = sp.symbols("epsilon", real=True)
    vacuum_index = sp.symbols("n", integer=True)
    perturbation = sp.Function("v")(x, time)
    nonlinear = (
        lam * sp.diff(epsilon * perturbation, time, 2)
        - tension * sp.diff(epsilon * perturbation, x, 2)
        + mu * sp.sin(2 * sp.pi * vacuum_index + epsilon * perturbation)
    )
    linear = sp.diff(nonlinear, epsilon).subs(epsilon, 0)
    expected_linear = (
        lam * sp.diff(perturbation, time, 2)
        - tension * sp.diff(perturbation, x, 2)
        + mu * perturbation
    )
    checks.check(
        "fresh vacuum derivative gives the massive linear equation",
        sp.simplify(linear - expected_linear) == 0,
    )
    checks.mutation_sensitive(
        "fresh linearization rejects sign and coefficient mutations",
        lambda candidate: sp.simplify(candidate - linear) == 0,
        expected_linear,
        (
            lam * sp.diff(perturbation, time, 2)
            + tension * sp.diff(perturbation, x, 2)
            + mu * perturbation,
            lam * sp.diff(perturbation, time, 2)
            - tension * sp.diff(perturbation, x, 2)
            - mu * perturbation,
        ),
    )

    k, angular = sp.symbols("k Omega", real=True)
    plane_wave = sp.exp(sp.I * (k * x - angular * time))
    characteristic = sp.simplify(
        (
            lam * sp.diff(plane_wave, time, 2)
            - tension * sp.diff(plane_wave, x, 2)
            + mu * plane_wave
        )
        / (lam * plane_wave)
    )
    speed = sp.sqrt(tension / lam)
    gap = sp.sqrt(mu / lam)
    dispersion_squared = gap**2 + speed**2 * k**2
    checks.check(
        "fresh Fourier substitution gives Omega squared equals gap squared plus c squared k squared",
        sp.simplify(characteristic - (-angular**2 + dispersion_squared)) == 0,
    )

    positive_k = sp.symbols("q", positive=True, real=True)
    positive_branch = sp.sqrt(gap**2 + speed**2 * positive_k**2)
    group_velocity = sp.simplify(sp.diff(positive_branch, positive_k))
    phase_velocity = sp.simplify(positive_branch / positive_k)
    checks.check(
        "fresh differentiation fixes phase and group velocities",
        group_velocity
        == tension * positive_k / (sp.sqrt(lam) * sp.sqrt(mu + tension * positive_k**2))
        and phase_velocity
        == sp.sqrt(mu + tension * positive_k**2) / (sp.sqrt(lam) * positive_k)
        and sp.simplify(group_velocity * phase_velocity - speed**2) == 0,
    )
    checks.check(
        "fresh limiting analysis fixes the band floor and velocity asymptotes",
        sp.limit(positive_branch, positive_k, 0, dir="+") == gap
        and sp.limit(group_velocity, positive_k, 0, dir="+") == 0
        and sp.limit(phase_velocity, positive_k, 0, dir="+") == sp.oo
        and sp.limit(group_velocity, positive_k, sp.oo) == speed
        and sp.limit(phase_velocity, positive_k, sp.oo) == speed,
    )

    amplitude = sp.Function("a")(x)
    separated = amplitude * sp.exp(-sp.I * angular * time)
    separated_residual = sp.simplify(
        (
            lam * sp.diff(separated, time, 2)
            - tension * sp.diff(separated, x, 2)
            + mu * separated
        )
        / (-tension * sp.exp(-sp.I * angular * time))
    )
    tail_coefficient = sp.simplify((gap**2 - angular**2) / speed**2)
    checks.check(
        "fresh time separation gives a double-prime equals tail coefficient times a",
        sp.simplify(
            separated_residual
            - (sp.diff(amplitude, x, 2) - tail_coefficient * amplitude)
        )
        == 0,
    )

    rate = sp.symbols("kappa", positive=True, real=True)
    right_amplitude, left_amplitude = sp.symbols("A B", real=True)
    continuity = right_amplitude - left_amplitude
    derivative_continuity = -rate * right_amplitude - rate * left_amplitude
    matching = sp.linear_eq_to_matrix(
        [continuity, derivative_continuity],
        [right_amplitude, left_amplitude],
    )[0]
    checks.check(
        "fresh origin matching eliminates the two sub-gap decay amplitudes",
        matching == sp.Matrix([[1, -1], [-rate, -rate]])
        and matching.det() == -2 * rate
        and sp.linsolve(
            [continuity, derivative_continuity],
            [right_amplitude, left_amplitude],
        )
        == {(0, 0)},
    )
    checks.check(
        "the narrated absolute-value exponential has the unmatched derivative jump",
        sp.limit(sp.diff(sp.exp(-rate * sp.Abs(x)), x), x, 0, dir="+") == -rate
        and sp.limit(sp.diff(sp.exp(-rate * sp.Abs(x)), x), x, 0, dir="-") == rate,
    )

    affine_a, affine_b = sp.symbols("a_0 a_1", real=True, nonzero=True)
    cutoff = sp.symbols("R", positive=True, real=True)
    constant_norm = sp.integrate(affine_a**2, (x, 0, cutoff))
    affine_norm = sp.integrate(
        (affine_a + affine_b * x) ** 2,
        (x, 0, cutoff),
    )
    checks.check(
        "a threshold affine branch is half-line L2 only when both coefficients vanish",
        sp.limit(constant_norm, cutoff, sp.oo) == sp.oo
        and sp.limit(affine_norm, cutoff, sp.oo) == sp.oo,
    )
    oscillatory_a, oscillatory_b, wave_number = sp.symbols(
        "C D q_o",
        real=True,
        nonzero=True,
    )
    wave_number_positive = sp.symbols("q_o_pos", positive=True, real=True)
    oscillatory = (
        oscillatory_a * sp.cos(wave_number_positive * x)
        + oscillatory_b * sp.sin(wave_number_positive * x)
    )
    norm_per_period = sp.simplify(
        sp.integrate(
            oscillatory**2,
            (x, 0, 2 * sp.pi / wave_number_positive),
        )
    )
    checks.check(
        "every nonzero oscillatory branch has positive repeated L2 mass per period",
        norm_per_period
        == sp.pi * (oscillatory_a**2 + oscillatory_b**2) / wave_number_positive,
    )
    checks.check(
        "all real-frequency homogeneous whole-line separated branches are non-L2 or zero",
        matching.rank() == 2
        and norm_per_period.is_positive is True
        and sp.limit((1 + x) ** 2, x, sp.oo) == sp.oo,
    )

    normalized_frequency = sp.symbols("w", positive=True, real=True)
    eta = sp.sqrt(1 - normalized_frequency**2)
    length = speed / gap
    physical_frequency = normalized_frequency * gap
    breather_tail_squared = sp.simplify(eta**2 / length**2)
    linear_tail_squared = sp.simplify(
        (gap**2 - physical_frequency**2) / speed**2
    )
    checks.check(
        "fresh scale substitution matches the nonlinear breather and linear exterior rates",
        sp.simplify(breather_tail_squared - linear_tail_squared) == 0,
    )
    checks.mutation_sensitive(
        "breather tail matching rejects missing length and frequency factors",
        lambda candidate: sp.simplify(candidate - linear_tail_squared) == 0,
        breather_tail_squared,
        (eta**2, eta**2 / length, normalized_frequency**2 / length**2),
    )

    wave_angular = sp.sqrt(gap**2 + speed**2 * positive_k**2)
    standing = sp.cos(positive_k * x) * sp.cos(wave_angular * time)
    outgoing = sp.cos(positive_k * x - wave_angular * time)
    period = 2 * sp.pi / wave_angular

    def mean_flux(field: sp.Expr) -> sp.Expr:
        flux = -tension * sp.diff(field, time) * sp.diff(field, x)
        return sp.simplify(sp.integrate(flux, (time, 0, period)) / period)

    checks.check(
        "fresh flux calculation separates standing oscillation from directed propagation",
        mean_flux(standing) == 0
        and sp.simplify(
            mean_flux(outgoing) - tension * wave_angular * positive_k / 2
        )
        == 0,
    )

    profile_argument = x - speed * time
    gapless_packet = sp.sech(profile_argument)
    gapless_residual = sp.simplify(
        sp.diff(gapless_packet, time, 2)
        - speed**2 * sp.diff(gapless_packet, x, 2)
    )
    packet_energy_density_at_zero = sp.simplify(
        (
            lam * sp.diff(gapless_packet, time) ** 2 / 2
            + tension * sp.diff(gapless_packet, x) ** 2 / 2
        ).subs(time, 0)
    )
    packet_antiderivative = tension * sp.tanh(x) ** 3 / 3
    checks.check(
        "fresh d'Alembert packet is localized exact and finite energy",
        gapless_residual == 0
        and sp.simplify(
            packet_energy_density_at_zero
            - tension * sp.sech(x) ** 2 * sp.tanh(x) ** 2
        )
        == 0
        and sp.simplify(
            sp.diff(packet_antiderivative, x) - packet_energy_density_at_zero
        )
        == 0
        and sp.limit(packet_antiderivative, x, sp.oo)
        - sp.limit(packet_antiderivative, x, -sp.oo)
        == 2 * tension / 3,
    )
    checks.check(
        "the traveling packet is not a real-frequency separated L2 eigenmode",
        sp.simplify(
            gapless_packet.subs(time, time + 1) / gapless_packet
        ).has(x),
    )

    review_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    direct_alias_calls = [
        node
        for node in ast.walk(review_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "np"
        and node.func.attr in {"trapz", "trapezoid"}
    ]
    checks.check(
        "independent exact review uses no direct NumPy trapezoidal alias",
        direct_alias_calls == [],
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
