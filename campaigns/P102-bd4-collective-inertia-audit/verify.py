"""Primary exact verifier for the P102 BD4 collective-inertia audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.collective_coordinates import (
    capillary_barrier_top_linearization,
    collective_coordinate_dimension_ledger,
    collective_coordinate_metric,
    reduced_collective_euler_lagrange,
    stationary_collective_linearization,
    transform_collective_coordinate,
)
from substrate_framework.radial_energy import (
    capillary_critical_radius,
    capillary_energy,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-28/"
    "bridge_BD4_mR_inertia_ceiling_resolution.py"
)
SOURCE_SHA256 = "2f590473719f614f4ca641ad9443d6b4271429aba27337b94d5d064cc70c9929"
CONTRACT_SHA256 = "8b54bc0f8b3c8dc8dc7feca578621eee0f536d0eea6b51b7cbc80d72803c9144"
FREEZE_SHA256 = "55bf61e3cdef4492952be21410862a78517e9c72c64e166ea8c8a29781dbffc2"


def _contract_path() -> Path:
    candidates = (
        Path("campaigns/P102-bd4-collective-inertia-audit/proposal.yaml"),
        Path("proposals/P102-bd4-collective-inertia-audit/proposal.yaml"),
    )
    return next(path for path in candidates if path.exists())


def _claims() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    return {claim["id"]: claim for claim in registry["claims"]}


def main() -> int:
    checks = CheckLedger("C-COL-001")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash is pinned and BD4 remains outside the NumPy overlay",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    normalized_contract = _contract_path().read_bytes().replace(
        b"status: accepted\n",
        b"status: active\n",
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    freeze_path = _contract_path().parent / "evidence/frozen-proposal.yaml"
    checks.check(
        "pre-source commitment is immutable",
        hashlib.sha256(freeze_path.read_bytes()).hexdigest() == FREEZE_SHA256,
    )
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source has fourteen literal checks and a dynamic terminal tally",
        len(source_checks) == 14
        and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "exact source and campaign require no NumPy quadrature compatibility path",
        "import numpy" not in source_text
        and all(alias not in source_text for alias in ("np." + "trapz", "np." + "trapezoid")),
    )

    dimensions = collective_coordinate_dimension_ledger()
    columns = {
        name: dimensions.dimension_matrix[:, index]
        for index, name in enumerate(dimensions.quantity_names)
    }
    checks.check(
        "profile derivative squared times dx has inverse-length dimension",
        2 * columns["profile_derivative"] + columns["spatial_measure"]
        == columns["geometric_integral"]
        == sp.Matrix([0, -1, 0]),
    )
    checks.check(
        "lambda times the geometric integral has the required radius-inertia dimension",
        columns["inertia_density"] + columns["geometric_integral"]
        == columns["collective_inertia"]
        == sp.Matrix([1, -2, 2]),
    )
    checks.check(
        "curvature divided by collective inertia has inverse-time-squared dimension",
        columns["potential_curvature"] - columns["collective_inertia"]
        == columns["spectral_ratio"]
        == sp.Matrix([0, 0, -2])
        and 2 * columns["rate"] == columns["spectral_ratio"],
    )
    checks.mutation_sensitive(
        "profile-integral length exponent is load bearing",
        lambda candidate: columns["inertia_density"] + candidate
        == columns["collective_inertia"],
        columns["geometric_integral"],
        (
            sp.Matrix([0, 0, 0]),
            sp.Matrix([0, 1, 0]),
            sp.Matrix([0, -2, 0]),
        ),
    )

    x, q = sp.symbols("x q", real=True)
    length, inertia_density = sp.symbols("ell lambda", positive=True)
    gaussian = sp.exp(-(x - q) ** 2 / (2 * length**2))
    finite_metric = collective_coordinate_metric(
        inertia_density,
        gaussian,
        x,
        q,
    )
    checks.check(
        "a concrete Gaussian family has a finite positive exact pullback",
        sp.simplify(
            finite_metric.geometric_integral - sp.sqrt(sp.pi) / (2 * length)
        )
        == 0
        and sp.simplify(
            finite_metric.inertia
            - inertia_density * sp.sqrt(sp.pi) / (2 * length)
        )
        == 0,
    )
    zero_metric = collective_coordinate_metric(inertia_density, x**2, x, q)
    divergent_metric = collective_coordinate_metric(inertia_density, q * x, x, q)
    checks.check(
        "zero and divergent counterprofiles defeat dimensions-only existence",
        zero_metric.inertia == 0 and divergent_metric.geometric_integral is sp.oo,
    )
    checks.check(
        "BD4 supplies a dimension symbol rather than an admissible profile integral",
        "kappa_geom = geometric 1/length" in source_text
        and "sp.integrate" not in source_text
        and "sp.Integral" not in source_text
        and "Function(" not in source_text,
    )

    coordinate, velocity, acceleration = sp.symbols("q qdot qddot", real=True)
    mass_scale, stiffness = sp.symbols("M0 k", positive=True)
    metric = mass_scale * (1 + coordinate**2)
    potential = stiffness * coordinate**2 / 2
    canonical_equation = reduced_collective_euler_lagrange(
        metric,
        potential,
        coordinate,
        velocity,
        acceleration,
    )
    expected_equation = (
        metric * acceleration
        + mass_scale * coordinate * velocity**2
        + stiffness * coordinate
    )
    checks.check(
        "variable-metric reduction has the exact Euler-Lagrange connection term",
        sp.simplify(canonical_equation - expected_equation) == 0,
    )
    checks.mutation_sensitive(
        "the one-half metric-derivative coefficient is load bearing",
        lambda candidate: sp.simplify(candidate - canonical_equation) == 0,
        expected_equation,
        (
            expected_equation - mass_scale * coordinate * velocity**2,
            expected_equation + mass_scale * coordinate * velocity**2,
            expected_equation - stiffness * coordinate,
        ),
    )

    stable = stationary_collective_linearization(mass_scale, stiffness)
    neutral = stationary_collective_linearization(mass_scale, 0)
    unstable = stationary_collective_linearization(mass_scale, -stiffness)
    checks.check(
        "stationary curvature sign separates stable neutral and unstable branches",
        stable.stability == "stable"
        and neutral.stability == "neutral"
        and unstable.stability == "unstable",
    )
    checks.check(
        "stable and unstable scales occupy distinct result fields",
        stable.instability_rate is None
        and sp.simplify(stable.stable_angular_frequency**2 - stiffness / mass_scale) == 0
        and unstable.stable_angular_frequency is None
        and sp.simplify(unstable.instability_rate**2 - stiffness / mass_scale) == 0,
    )
    checks.mutation_sensitive(
        "curvature sign is load bearing for the physical classification",
        lambda candidate: stationary_collective_linearization(
            mass_scale,
            candidate,
        ).stability
        == "unstable",
        -stiffness,
        (stiffness, sp.Integer(0)),
    )

    radius, tension, pressure = sp.symbols("R T P", positive=True)
    capillary = capillary_energy(radius, tension, pressure)
    critical = capillary_critical_radius(tension, pressure)
    capillary_curvature = sp.diff(capillary, radius, 2).subs(radius, critical)
    barrier_top = capillary_barrier_top_linearization(pressure, mass_scale)
    checks.check(
        "accepted capillary stationary point is a strict maximum with negative curvature",
        critical == tension / pressure
        and capillary_curvature == -2 * sp.pi * pressure,
    )
    checks.check(
        "capillary-top scale is an exponential growth rate rather than a stable frequency",
        barrier_top.stability == "unstable"
        and barrier_top.stable_angular_frequency is None
        and sp.simplify(
            barrier_top.instability_rate**2 - 2 * sp.pi * pressure / mass_scale
        )
        == 0,
    )
    checks.check(
        "source discards the curvature sign before applying a mode-frequency label",
        "sqrt(|E''|/m_R)" in source_text
        and "barrier curvature becomes a frequency" in source_text
        and "unstable" not in source_text.lower(),
    )

    new_coordinate, scale = sp.symbols("Q a", positive=True)
    transformed = transform_collective_coordinate(
        mass_scale,
        stiffness * coordinate**2 / 2,
        coordinate,
        new_coordinate,
        new_coordinate / scale,
    )
    checks.check(
        "metric and stationary Hessian co-transform under coordinate rescaling",
        transformed.transformed_inertia == mass_scale / scale**2
        and transformed.stationary_hessian == stiffness / scale**2,
    )
    checks.check(
        "stationary curvature-to-inertia ratio is coordinate invariant",
        transformed.stationary_spectral_ratio == stiffness / mass_scale,
    )
    nonlinear = transform_collective_coordinate(
        1,
        coordinate**3,
        coordinate,
        new_coordinate,
        new_coordinate**2,
    )
    checks.check(
        "nonstationary Hessian carries the gradient chain term",
        nonlinear.hessian_chain_term == 6 * new_coordinate**4
        and nonlinear.transformed_hessian
        == sp.diff(new_coordinate**6, new_coordinate, 2)
        and nonlinear.transformed_hessian != nonlinear.stationary_hessian,
    )
    checks.mutation_sensitive(
        "coordinate Jacobian square is load bearing",
        lambda pair: sp.simplify(pair[1] / pair[0] - stiffness / mass_scale) == 0,
        (mass_scale / scale**2, stiffness / scale**2),
        (
            (mass_scale / scale, stiffness / scale**2),
            (mass_scale / scale**2, stiffness / scale),
        ),
    )

    common_scale = sp.Symbol("rho", positive=True)
    common = stationary_collective_linearization(
        common_scale * mass_scale,
        common_scale * stiffness,
    )
    inertia_only = stationary_collective_linearization(
        common_scale * mass_scale,
        stiffness,
    )
    checks.check(
        "common reduced-action scaling cancels from the stationary spectrum",
        common.spectral_ratio == stable.spectral_ratio,
    )
    checks.check(
        "inertia-only scaling changes the stationary spectrum",
        inertia_only.spectral_ratio == stable.spectral_ratio / common_scale,
    )

    geometric_factor, rate = sp.symbols("kappa w", positive=True)
    collective_inertia = inertia_density * geometric_factor
    barrier_energy = sp.pi * tension**2 / pressure
    rate_squared = 2 * sp.pi * pressure / collective_inertia
    pressure_from_rate = sp.solve(sp.Eq(rate**2, rate_squared), pressure)[0]
    eliminated_barrier = sp.simplify(barrier_energy.subs(pressure, pressure_from_rate))
    checks.check(
        "eliminating the shared drive leaves tension inertia and profile factors",
        eliminated_barrier
        == 2 * sp.pi**2 * tension**2 / (rate**2 * collective_inertia)
        and eliminated_barrier.free_symbols
        == {tension, rate, inertia_density, geometric_factor},
    )
    observation_matrix = sp.Matrix(
        [[2, -1, 0], [0, sp.Rational(1, 2), sp.Rational(-1, 2)]]
    )
    observation_nullspace = observation_matrix.nullspace()
    checks.check(
        "barrier and local rate leave a one-dimensional parameter orbit",
        observation_matrix.rank() == 2
        and len(observation_nullspace) == 1
        and observation_matrix * observation_nullspace[0] == sp.zeros(2, 1)
        and observation_nullspace[0] == sp.Matrix([sp.Rational(1, 2), 1, 1]),
    )
    checks.check(
        "constructive rescaling preserves both barrier and local rate",
        sp.simplify(
            (sp.pi * (common_scale * tension) ** 2 / (common_scale**2 * pressure))
            - barrier_energy
        )
        == 0
        and sp.simplify(
            2
            * sp.pi
            * (common_scale**2 * pressure)
            / (common_scale**2 * collective_inertia)
            - rate_squared
        )
        == 0,
    )

    claims = _claims()
    checks.check(
        "accepted continuum and capillary claims do not couple their coefficients or profiles",
        "does not derive a material" in claims["C-MED-003"]["statement"]
        and "k-omega dispersion" in claims["C-RG-002"]["statement"]
        and "capillary" not in claims["C-MED-003"]["statement"]
        and "C-MED-003" not in claims["C-RG-002"]["dependencies"]
        and "inertia" not in claims["C-RG-002"]["statement"],
    )
    proposed = claims.get("C-COL-001")
    checks.check(
        "claim identifier is either frozen-reserved or accepted with the exact ceiling",
        (
            proposed is None
            and "C-COL-001" in yaml.safe_load(_contract_path().read_text())["claims_proposed"]
        )
        or (
            proposed is not None
            and "unstable exponential rate" in proposed["statement"]
            and "do not supply" in proposed["statement"]
        ),
    )
    checks.check(
        "BD4 contains no hbar state thermal escape or observed-onset derivation",
        "hbar" in source_text
        and not any(
            token in source_text
            for token in (
                "Hamiltonian",
                "density_matrix",
                "solve_ivp",
                "Langevin",
                "first_passage",
                "cross_section",
                "measured",
            )
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
