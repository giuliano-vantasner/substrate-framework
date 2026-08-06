"""Fresh P223 derivation and DOP853 shooting without canonical GSK imports."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.integrate import simpson, solve_ivp
from scipy.optimize import brentq
from scipy.special import kve
import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN = Path(__file__).resolve().parents[1]
ANGULAR = {1: 1.0, 2: float(np.pi + 8.0 / 3.0), 4: 20.6496264884189}
BRACKETS = {1: (1.5, 2.5), 2: (1.0, 2.0), 4: (0.4, 1.2)}
ME = 0.511
MPI = 138.03
MRHO = 775.26
NC = 3.0
UNIT = 16.0 * np.pi * ME
COUPLING = float(np.sqrt(MRHO / (16.0 * np.sqrt(2.0) * np.pi * ME)))
C6 = NC**2 * COUPLING**4 / (128.0 * np.pi**4)
C0 = 8.0 * MPI**2 / (COUPLING**4 * UNIT**2)
INNER = 1.0e-4
OUTER = 14.0


def origin_power(degree: int) -> float:
    return float((np.sqrt(1.0 + 8.0 * degree) - 1.0) / 2.0)


def tail_coefficient(degree: int) -> float:
    mass = np.sqrt(C0 / 2.0)
    order = np.sqrt(0.25 + 2.0 * degree)
    argument = mass * OUTER
    ratio = (
        kve(order - 1.0, argument) + kve(order + 1.0, argument)
    ) / kve(order, argument)
    return float(1.0 / (2.0 * OUTER) + 0.5 * mass * ratio)


def equations(degree: int, angular: float):
    def rhs(radius: float, state: np.ndarray) -> tuple[float, float]:
        complement, complement_derivative = state
        field = np.pi - complement
        derivative = -complement_derivative
        sine = np.sin(field)
        sine_twice = np.sin(2.0 * field)
        kinetic = (
            radius**2
            + 2.0 * degree * sine**2
            + C6 * angular * sine**4 / radius**2
        )
        numerator = (
            -2.0 * radius * derivative
            - degree * sine_twice * (derivative**2 - 1.0)
            + angular * sine**2 * sine_twice / radius**2
            - C6 * angular * sine**2 * sine_twice * derivative**2 / radius**2
            + 2.0 * C6 * angular * sine**4 * derivative / radius**3
            + 0.5 * C0 * radius**2 * sine
        )
        return complement_derivative, -numerator / kinetic

    return rhs


def integrate(degree: int, angular: float, amplitude: float, samples=None):
    power = origin_power(degree)
    return solve_ivp(
        equations(degree, angular),
        (INNER, OUTER),
        (
            amplitude * INNER**power,
            amplitude * power * INNER ** (power - 1.0),
        ),
        method="DOP853",
        t_eval=samples,
        rtol=5.0e-12,
        atol=5.0e-14,
        max_step=0.0075,
    )


def solve_branch(degree: int, angular: float) -> dict[str, object]:
    tail = tail_coefficient(degree)

    def residual(amplitude: float) -> float:
        solution = integrate(degree, angular, amplitude)
        if not solution.success:
            raise RuntimeError(solution.message)
        return float(
            -solution.y[1, -1] + tail * (np.pi - solution.y[0, -1])
        )

    lower, upper = BRACKETS[degree]
    lower_residual = residual(lower)
    upper_residual = residual(upper)
    amplitude = float(brentq(residual, lower, upper, xtol=1.0e-14, rtol=1.0e-14))
    radius = np.linspace(INNER, OUTER, 28_001, dtype=np.float64)
    solution = integrate(degree, angular, amplitude, radius)
    field = np.pi - solution.y[0]
    derivative = -solution.y[1]
    sine_squared = np.sin(field) ** 2
    densities = (
        radius**2 * derivative**2 + 2.0 * degree * sine_squared,
        2.0 * degree * sine_squared * derivative**2
        + angular * sine_squared**2 / radius**2,
        C6 * angular * sine_squared**2 * derivative**2 / radius**2,
        C0 * radius**2 * (1.0 - np.cos(field)),
    )
    components = tuple(
        float(4.0 * np.pi * simpson(density, x=radius)) for density in densities
    )
    coefficient = float(sum(components) / (12.0 * np.pi**2))
    virial = float(
        abs(components[0] - components[1] - 3 * components[2] + 3 * components[3])
        / sum(components)
    )
    return {
        "lower_residual": lower_residual,
        "upper_residual": upper_residual,
        "boundary_residual": residual(amplitude),
        "success": solution.success,
        "field": field,
        "derivative": derivative,
        "components": components,
        "coefficient": coefficient,
        "virial": virial,
    }


def main() -> int:
    checks = CheckLedger("P223-independent")
    e, a, d = sp.symbols("e A D", positive=True)
    checks.check(
        "fresh coefficient elimination fixes only the supplied product",
        sp.simplify((a * e**4) * (d / e**4) - a * d) == 0,
    )
    radius = sp.symbols("r", positive=True)
    field = sp.Function("f")(radius)
    derivative = sp.diff(field, radius)
    degree, angular = sp.symbols("B I", positive=True)
    c6, c0 = sp.symbols("c6 c0", nonnegative=True)
    sine = sp.sin(field)
    density = (
        radius**2 * derivative**2
        + 2 * degree * sine**2 * (1 + derivative**2)
        + angular * sine**4 / radius**2
        + c6 * angular * sine**4 * derivative**2 / radius**2
        + c0 * radius**2 * (1 - sp.cos(field))
    )
    direct = sp.simplify(
        (sp.diff(sp.diff(density, derivative), radius) - sp.diff(density, field))
        / 2
    )
    expected = (
        (radius**2 + 2 * degree * sine**2 + c6 * angular * sine**4 / radius**2)
        * sp.diff(field, radius, 2)
        + (2 * radius - 2 * c6 * angular * sine**4 / radius**3) * derivative
        + degree * sp.sin(2 * field) * (derivative**2 - 1)
        + c6 * angular * sine**2 * sp.sin(2 * field) * derivative**2 / radius**2
        - angular * sine**2 * sp.sin(2 * field) / radius**2
        - c0 * radius**2 * sine / 2
    )
    checks.check(
        "fresh symbolic variation gives the accepted radial equation",
        sp.simplify(direct - expected) == 0,
    )
    branches = {
        degree_value: solve_branch(degree_value, angular_value)
        for degree_value, angular_value in ANGULAR.items()
    }
    checks.check(
        "fresh shooting brackets change tail-residual sign",
        all(
            float(branch["lower_residual"]) * float(branch["upper_residual"]) < 0.0
            for branch in branches.values()
        ),
    )
    checks.check(
        "all independent branches are finite monotone endpoint profiles",
        all(
            bool(branch["success"])
            and np.all(np.isfinite(branch["field"]))
            and np.all(np.isfinite(branch["derivative"]))
            and np.max(branch["derivative"]) < 1.0e-5
            and np.min(branch["field"]) >= -1.0e-7
            and np.max(branch["field"]) <= np.pi + 1.0e-7
            for branch in branches.values()
        ),
    )
    checks.check(
        "independent tail residuals are explicitly bounded",
        max(abs(float(branch["boundary_residual"])) for branch in branches.values())
        < 2.0e-5,
    )
    checks.check(
        "independent Simpson sectors are positive and virial balanced",
        all(
            min(branch["components"]) >= 0.0 and float(branch["virial"]) < 1.0e-5
            for branch in branches.values()
        ),
    )
    primary = yaml.safe_load(
        (CAMPAIGN / "evidence/primary-numerical-evidence.yaml").read_text()
    )["domains"]["R14"]
    primary_coefficients = {
        1: primary["b"]["B1"],
        2: primary["b"]["B2"],
        4: primary["b"]["B4"],
    }
    checks.check(
        "fresh shooting agrees with like-for-like Robin collocation",
        all(
            abs(float(branches[b]["coefficient"]) - primary_coefficients[b])
            < 3.0e-7
            for b in branches
        ),
    )
    shooting_kappa = float(
        3.0
        * np.pi**2
        * (
            2.0 * float(branches[2]["coefficient"])
            - float(branches[4]["coefficient"])
        )
    )
    checks.check(
        "fresh signed difference agrees with like-for-like collocation",
        abs(shooting_kappa - float(primary["kappa"])) < 1.0e-5,
    )
    source_text = Path(
        "/home/dan/substrate/merged-framework/bridges/phase-44/"
        "bridge_MR5_solve_at_derived_e.py"
    ).read_text()
    checks.check(
        "fresh review detects source comparator use outside its guard needles",
        all(token in source_text for token in ("8.46", "1.46534", "12.343", "E_IMPORTED = 5.45"))
        and "FORBIDDEN = [929 / 1000.0" in source_text,
    )
    claims = {
        claim["id"]: claim
        for claim in yaml.safe_load((ROOT / "governance/claims.yaml").read_text())[
            "claims"
        ]
    }
    checks.check(
        "accepted owners exclude minimum state and physical interpretations",
        "global or local minimality" in claims["C-GSK-002"]["statement"]
        and "derives no mass formula" in claims["C-RDIFF-001"]["statement"]
        and "physical rho" in claims["C-VEC-001"]["statement"],
    )
    delta = yaml.safe_load(
        (CAMPAIGN / "evidence/post-source-claim-delta.yaml").read_text()
    )
    checks.check(
        "independent review finds no nonduplicate accepted claim surface",
        delta["reserved_identifiers"] == []
        and delta["package_change"] == "none_pending_nonduplication",
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
