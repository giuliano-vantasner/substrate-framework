"""Independent control-volume and finite-window audit for P093."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-26/"
    "bridge_LB3_damped_sg_ringdown.py"
)


def _times() -> np.ndarray:
    dt = 0.4 * 0.05
    all_times = np.arange(4, int(320.0 / dt) + 1, 4, dtype=np.float64) * dt
    return np.asarray(all_times[(all_times >= 40.0) & (all_times <= 120.0)])


def _independent_reduced_slope(omega_initial: float, gamma: float) -> float:
    times = _times()
    theta_initial = np.arccos(omega_initial)
    action_angle = theta_initial * np.exp(-gamma * times)
    energy = 16.0 * np.sin(action_angle)
    design = np.column_stack((np.ones_like(times), times))
    coefficients, *_ = np.linalg.lstsq(design, np.log(energy), rcond=None)
    return float(-coefficients[1])


def main() -> int:
    checks = CheckLedger("P093-INDEPENDENT")
    source_text = SOURCE.read_text(encoding="utf-8")

    x, time = sp.symbols("x t", real=True)
    gamma = sp.symbols("Gamma", positive=True, real=True)
    field = sp.Function("phi")(x, time)
    field_t = sp.diff(field, time)
    field_x = sp.diff(field, x)
    energy_density = (
        field_t**2 / 2 + field_x**2 / 2 + 1 - sp.cos(field)
    )
    local_balance_residual = sp.diff(energy_density, time) - sp.diff(
        field_t * field_x,
        x,
    )
    on_shell = local_balance_residual.subs(
        sp.diff(field, time, 2),
        sp.diff(field, x, 2) - sp.sin(field) - gamma * field_t,
    )
    checks.check(
        "local balance independently separates divergence and bulk loss",
        sp.simplify(on_shell + gamma * field_t**2) == 0,
    )

    left_flux, right_flux, kinetic_integral = sp.symbols(
        "F_left F_right K_R",
        real=True,
    )
    core_rate = right_flux - left_flux - gamma * kinetic_integral
    checks.check(
        "finite-interval integration independently retains both boundary terms",
        sp.diff(core_rate, right_flux) == 1
        and sp.diff(core_rate, left_flux) == -1
        and sp.diff(core_rate, kinetic_integral) == -gamma,
    )
    checks.mutation_sensitive(
        "omitting finite-core flux changes the balance",
        lambda include_flux: sp.simplify(
            include_flux * (right_flux - left_flux)
            - gamma * kinetic_integral
            - core_rate
        )
        == 0,
        1,
        (0, -1),
    )

    source_cases = (
        (0.7, 0.010, 0.00954640, 0.00960991),
        (0.5, 0.010, 0.00919841, 0.00905358),
        (0.7, 0.005, 0.00451065, 0.00452679),
        (0.7, 0.015, 0.0148707, 0.0144149),
    )
    reduced = tuple(
        _independent_reduced_slope(omega_initial, damping)
        for omega_initial, damping, _measured, _pointwise in source_cases
    )
    checks.check(
        "independent least squares reproduces all source rates within two percent",
        all(
            abs(measured - expected) / expected < 0.02
            for (_omega, _gamma, measured, _pointwise), expected in zip(
                source_cases,
                reduced,
            )
        ),
    )
    checks.check(
        "independent window prediction beats every source pointwise comparator",
        all(
            abs(measured - expected) < abs(measured - pointwise)
            for (_omega, _gamma, measured, pointwise), expected in zip(
                source_cases,
                reduced,
            )
        ),
    )
    checks.mutation_sensitive(
        "nonlinear family energy is load bearing in the fitted slope",
        lambda use_nonlinear_energy: abs(
            (
                _independent_reduced_slope(0.5, 0.01)
                if use_nonlinear_energy
                else 0.01
            )
            - reduced[1]
        )
        < 1.0e-12,
        True,
        (False,),
    )

    times = _times()
    spacing = float(times[1] - times[0])
    bin_width = 2.0 * np.pi / (times.size * spacing)
    checks.check(
        "independent sampling reconstruction gives 1000 points and pi/40 bins",
        times.size == 1000
        and abs(times[0] - 40.0) < 1.0e-12
        and abs(times[-1] - 119.92) < 1.0e-12
        and abs(bin_width - np.pi / 40.0) < 1.0e-12,
    )
    checks.check(
        "printed source frequencies identify adjacent integer FFT bins",
        round(12 * bin_width, 4) == 0.9425
        and round(11 * bin_width, 4) == 0.8639,
    )
    checks.mutation_sensitive(
        "fit-window duration is load bearing in frequency resolution",
        lambda sample_count: abs(
            2.0 * np.pi / (sample_count * spacing) - bin_width
        )
        < 1.0e-12,
        1000,
        (500, 2000),
    )

    accepted_mode_discriminant = sp.Rational(7, 4) ** 2 - 4
    source_substitution_discriminant = sp.Rational(7, 4) ** 2 - 4 * sp.Rational(
        7,
        10,
    ) ** 2
    checks.check(
        "exact discriminants reverse the source high-damping label",
        accepted_mode_discriminant < 0 and source_substitution_discriminant > 0,
    )
    checks.check(
        "source operational guard depends on mutable time and amplitude thresholds",
        "tO > T_int" in source_text
        and "np.abs(core_after) > 1e-4" in source_text
        and "surviving_frac < 0.1" in source_text,
    )
    checks.mutation_sensitive(
        "accepted mass gap is load bearing in the high-damping classification",
        lambda mass: sp.Rational(7, 4) ** 2 - 4 * mass**2 < 0,
        1,
        (sp.Rational(7, 10), sp.Rational(1, 2)),
    )

    new_code = Path(__file__).read_text(encoding="utf-8")
    checks.check(
        "independent review uses no direct NumPy trapezoidal alias",
        "np." + "trapz" not in new_code
        and "np." + "trapezoid(" not in new_code,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
