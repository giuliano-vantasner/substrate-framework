"""Fresh P218 derivation and DOP853 shooting without canonical GSK imports."""

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
BRACKETS = {1: (1.5, 1.6), 2: (1.3, 1.4), 4: (0.6, 0.7)}
C6 = 0.5
C0 = 0.25
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
        # Evolve the vacuum complement g=pi-f so the degree-four origin
        # perturbation is not subtracted from pi in binary64.
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
        rtol=2.0e-11,
        atol=2.0e-13,
        max_step=0.015,
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
    amplitude = float(
        brentq(
            residual,
            lower,
            upper,
            xtol=1.0e-13,
            rtol=1.0e-13,
        )
    )
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
        "amplitude": amplitude,
        "lower_residual": lower_residual,
        "upper_residual": upper_residual,
        "boundary_residual": residual(amplitude),
        "success": solution.success,
        "field": field,
        "derivative": derivative,
        "components": components,
        "coefficient": coefficient,
        "virial": virial,
        "function_evaluations": solution.nfev,
    }


def main() -> int:
    checks = CheckLedger("P218-independent")
    r = sp.symbols("r", positive=True)
    f = sp.Function("f")(r)
    fp = sp.diff(f, r)
    degree, angular = sp.symbols("B I", positive=True)
    c6, c0 = sp.symbols("c6 c0", nonnegative=True)
    sine = sp.sin(f)
    density = (
        r**2 * fp**2
        + 2 * degree * sine**2 * (1 + fp**2)
        + angular * sine**4 / r**2
        + c6 * angular * sine**4 * fp**2 / r**2
        + c0 * r**2 * (1 - sp.cos(f))
    )
    direct = sp.simplify(
        (
            sp.diff(sp.diff(density, fp), r)
            - sp.diff(density, f)
        )
        / 2
    )
    expected = (
        (r**2 + 2 * degree * sine**2 + c6 * angular * sine**4 / r**2)
        * sp.diff(f, r, 2)
        + (2 * r - 2 * c6 * angular * sine**4 / r**3) * fp
        + degree * sp.sin(2 * f) * (fp**2 - 1)
        + c6 * angular * sine**2 * sp.sin(2 * f) * fp**2 / r**2
        - angular * sine**2 * sp.sin(2 * f) / r**2
        - c0 * r**2 * sine / 2
    )
    checks.check(
        "fresh symbolic variation gives the extended radial equation",
        sp.simplify(direct - expected) == 0,
    )
    e2, e4, e6, e0, scale = sp.symbols("E2 E4 E6 E0 s", positive=True)
    scaled = scale * e2 + e4 / scale + e6 / scale**3 + scale**3 * e0
    checks.check(
        "fresh dilation gives the four Derrick weights",
        sp.simplify(
            sp.diff(scaled, scale).subs(scale, 1)
            - (e2 - e4 - 3 * e6 + 3 * e0)
        )
        == 0,
    )
    checks.check(
        "accepted angular inputs obey the squared-Jacobian lower bound",
        ANGULAR[1] == 1.0
        and ANGULAR[2] > 4.0
        and ANGULAR[4] > 16.0,
    )

    branches = {
        degree: solve_branch(degree, angular)
        for degree, angular in ANGULAR.items()
    }
    checks.check(
        "fresh shooting brackets change tail-residual sign",
        all(
            float(branch["lower_residual"]) * float(branch["upper_residual"]) < 0.0
            for branch in branches.values()
        ),
    )
    checks.check(
        "all DOP853 branches are finite monotone endpoint profiles",
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
        "shooting tail residuals are resolution limited but explicitly bounded",
        max(abs(float(branch["boundary_residual"])) for branch in branches.values())
        < 2.0e-5,
    )
    checks.check(
        "independent Simpson components are positive and virial balanced",
        all(
            min(branch["components"]) >= 0.0
            and float(branch["virial"]) < 1.0e-5
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
        "fresh shooting agrees with like-for-like collocation energies",
        all(
            abs(float(branches[degree]["coefficient"]) - primary_coefficients[degree])
            < 3.0e-7
            for degree in branches
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
    checks.check(
        "conditional benchmark is distinct from the source physical-premise number",
        abs(shooting_kappa - 12.3434) > 0.4,
    )

    claims = {
        claim["id"]: claim
        for claim in yaml.safe_load((ROOT / "governance/claims.yaml").read_text())[
            "claims"
        ]
    }
    checks.check(
        "accepted predecessors keep radial and BPS scope conditional",
        claims["C-RPROF-001"]["review"] == "accepted"
        and claims["C-RPROF-002"]["verification"] == "numeric_evidence"
        and claims["C-RPROF-002"]["epistemic"] == "qualified"
        and "separately declared dimensionless radial functional"
        in claims["C-RPROF-001"]["statement"]
        and "proves no half-line existence or uniqueness theorem"
        in claims["C-RPROF-002"]["statement"]
        and "physical baryon" in claims["C-RPROF-002"]["statement"]
        and "does not establish that an equality configuration exists"
        in claims["C-BPS-001"]["statement"],
    )
    candidate = yaml.safe_load(
        (CAMPAIGN / "evidence/candidate-claim.yaml").read_text()
    )["numeric_candidate"]
    checks.check(
        "fresh review preserves the numerical claim exclusions",
        all(
            item in candidate["excluded"]
            for item in ("half_line_existence", "minimum", "full_3d_solution", "physical_baryon")
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
