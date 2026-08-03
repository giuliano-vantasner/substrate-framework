"""Primary exact audit for the P095 MC1 dimensional sine-Gordon campaign."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.dimensional_sine_gordon import (
    dimensional_breather_field,
    dimensional_breather_observables,
    dimensional_sine_gordon_coefficient_dimension_matrix,
    dimensional_sine_gordon_coefficients,
    dimensional_sine_gordon_coefficients_from_speed_gap,
    dimensional_sine_gordon_log_ratio_jacobian,
    dimensional_sine_gordon_normalized_coordinates,
    dimensional_sine_gordon_physical_coordinates,
    dimensional_sine_gordon_residual,
    dimensional_sine_gordon_scales,
    rescale_dimensional_sine_gordon_coefficients,
)
from substrate_framework.sine_gordon import (
    breather_action,
    breather_energy,
    breather_field,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-27/"
    "bridge_MC1_constitutive_reduction.py"
)
FULCERI = Path(
    "/home/dan/substrate/vantasner-framework/tf-paper/scripts/"
    "verify_fulceri_drift.py"
)
RUNG147 = Path(
    "/home/dan/substrate/pulson-backreaction-bridge/sympy/rungs/"
    "rung147_c024_breather_energy_amplitude.py"
)
SOURCE_SHA256 = "32ed770bb753a9d1f0e67620a66fa29355e84c430c150694ffdfdb3003a8d3f3"
FULCERI_SHA256 = "69ba1e218e7b49816282181117b02d7022ba9035f11d9aec4fa1c34534d7f1a7"
RUNG147_SHA256 = "50c64e77738751de8412c380ca0a3b99bd1e0d149af02b77287f3935e3065c51"
CONTRACT_SHA256 = "499f703f8d90b613b2ed0dfd9c5edb2ac73116466e956eaf2b42bfbc42cbb5af"
FREEZE_SHA256 = "eb03b7043bacae316a26a2e1c65d66a795539dcc30cd91bf52a2e7c0cd625ddf"


def _campaign_dir() -> Path:
    candidates = (
        Path("campaigns/P095-mc1-dimensional-sine-gordon"),
        Path("proposals/P095-mc1-dimensional-sine-gordon"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P095")
    campaign_dir = _campaign_dir()
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("MC1 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
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
        "supporting predecessor files are hash pinned",
        _sha256(FULCERI) == FULCERI_SHA256
        and _sha256(RUNG147) == RUNG147_SHA256,
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
        "source has twenty-four literal checks and a dynamic terminal tally",
        len(check_calls) == 24
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
        and local_functions == {"check", "phys_eom", "linear_eom"},
    )
    checks.check(
        "source interval iff is only one sampled point",
        "w.subs({omega_b: sp.Rational(1, 2), omega0: 1})" in source_text,
    )
    checks.check(
        "source absolute-scale guard checks only a symbol name",
        "not any(str(s) == 'a' for s in smuggled)" in source_text,
    )
    checks.check(
        "source omits the physical energy and canonical action transforms",
        "E_b_dimless = 16 * eta_dimless" in source_text
        and "E_b_phys" not in source_text
        and "J_scale" not in source_text,
    )

    lam, tension, mu = sp.symbols("lambda T mu", positive=True, real=True)
    field_value, field_t, field_x = sp.symbols("u u_t u_x", real=True)
    density = (
        lam * field_t**2 / 2
        - tension * field_x**2 / 2
        - mu * (1 - sp.cos(field_value))
    )
    checks.check(
        "declared density has the exact three partial derivatives",
        sp.diff(density, field_t) == lam * field_t
        and sp.diff(density, field_x) == -tension * field_x
        and sp.diff(density, field_value) == -mu * sp.sin(field_value),
    )

    x, t = sp.symbols("x t", real=True)
    u = sp.Function("u")(x, t)
    coefficients = dimensional_sine_gordon_coefficients(lam, tension, mu)
    expected_residual = (
        lam * sp.diff(u, t, 2)
        - tension * sp.diff(u, x, 2)
        + mu * sp.sin(u)
    )
    checks.check(
        "canonical field residual is the direct Euler-Lagrange equation",
        sp.simplify(
            dimensional_sine_gordon_residual(u, x, t, coefficients)
            - expected_residual
        )
        == 0,
    )
    checks.mutation_sensitive(
        "field-equation coefficients and signs are load bearing",
        lambda candidate: sp.simplify(candidate - expected_residual) == 0,
        expected_residual,
        (
            lam * sp.diff(u, t, 2) + tension * sp.diff(u, x, 2) + mu * sp.sin(u),
            lam * sp.diff(u, t, 2) - tension * sp.diff(u, x, 2) - mu * sp.sin(u),
            2 * lam * sp.diff(u, t, 2) - tension * sp.diff(u, x, 2) + mu * sp.sin(u),
        ),
    )

    scales = dimensional_sine_gordon_scales(coefficients)
    checks.check(
        "coefficient ratios define speed gap and length with positive roots",
        scales.signal_speed == sp.sqrt(tension / lam)
        and scales.gap_frequency == sp.sqrt(mu / lam)
        and scales.length == sp.sqrt(tension / mu),
    )
    checks.check(
        "length speed and gap obey one exact relation",
        sp.simplify(scales.length - scales.signal_speed / scales.gap_frequency)
        == 0,
    )
    checks.check(
        "energy and action scales are distinct and satisfy E_scale=omega_0*J_scale",
        scales.energy == sp.sqrt(tension * mu)
        and scales.action == sp.sqrt(lam * tension)
        and sp.simplify(scales.energy - scales.gap_frequency * scales.action)
        == 0,
    )

    dimension_matrix = dimensional_sine_gordon_coefficient_dimension_matrix()
    checks.check(
        "coefficient dimensions are full rank in the declared density convention",
        dimension_matrix == sp.Matrix([[1, 1, 1], [-1, 1, -1], [2, 0, 0]])
        and dimension_matrix.det() == -4
        and dimension_matrix.rank() == 3,
    )
    scale_exponents = {
        "speed": sp.Matrix([-sp.Rational(1, 2), sp.Rational(1, 2), 0]),
        "gap": sp.Matrix([-sp.Rational(1, 2), 0, sp.Rational(1, 2)]),
        "length": sp.Matrix([0, sp.Rational(1, 2), -sp.Rational(1, 2)]),
        "energy": sp.Matrix([0, sp.Rational(1, 2), sp.Rational(1, 2)]),
        "action": sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2), 0]),
    }
    expected_dimensions = {
        "speed": sp.Matrix([0, 1, -1]),
        "gap": sp.Matrix([0, 0, -1]),
        "length": sp.Matrix([0, 1, 0]),
        "energy": sp.Matrix([1, 0, 0]),
        "action": sp.Matrix([1, 0, 1]),
    }
    checks.check(
        "every derived scale has the exact declared dimension",
        all(
            dimension_matrix * exponent == expected_dimensions[name]
            for name, exponent in scale_exponents.items()
        ),
    )

    log_jacobian = dimensional_sine_gordon_log_ratio_jacobian()
    checks.check(
        "ratio map has rank two and one common-multiplier null direction",
        log_jacobian.rank() == 2
        and log_jacobian.nullspace() == [sp.ones(3, 1)]
        and log_jacobian.T.nullspace() == [sp.Matrix([-1, 1, 1])],
    )
    inertia_scale, speed, gap = sp.symbols("s c omega_0", positive=True, real=True)
    inverse_coefficients = dimensional_sine_gordon_coefficients_from_speed_gap(
        inertia_scale,
        speed,
        gap,
    )
    inverse_scales = dimensional_sine_gordon_scales(inverse_coefficients)
    checks.check(
        "inverse coefficient family retains one arbitrary positive scale",
        inverse_coefficients.inertia == inertia_scale
        and inverse_coefficients.gradient == inertia_scale * speed**2
        and inverse_coefficients.onsite == inertia_scale * gap**2
        and inverse_scales.signal_speed == speed
        and inverse_scales.gap_frequency == gap
        and sp.simplify(inverse_scales.length - speed / gap) == 0,
    )

    alpha = sp.symbols("alpha", positive=True, real=True)
    scaled_coefficients = rescale_dimensional_sine_gordon_coefficients(
        coefficients,
        alpha,
    )
    scaled_scales = dimensional_sine_gordon_scales(scaled_coefficients)
    checks.check(
        "common coefficient multiplier preserves ratios and rescales energy and action",
        sp.simplify(scaled_scales.signal_speed - scales.signal_speed) == 0
        and sp.simplify(scaled_scales.gap_frequency - scales.gap_frequency) == 0
        and sp.simplify(scaled_scales.length - scales.length) == 0
        and sp.simplify(scaled_scales.energy - alpha * scales.energy) == 0
        and sp.simplify(scaled_scales.action - alpha * scales.action) == 0,
    )
    checks.mutation_sensitive(
        "common multiplier must scale all three coefficients together",
        lambda candidate: dimensional_sine_gordon_scales(candidate).signal_speed
        == scales.signal_speed
        and dimensional_sine_gordon_scales(candidate).gap_frequency
        == scales.gap_frequency,
        scaled_coefficients,
        (
            dimensional_sine_gordon_coefficients(alpha * lam, tension, mu),
            dimensional_sine_gordon_coefficients(lam, alpha * tension, mu),
            dimensional_sine_gordon_coefficients(lam, tension, alpha * mu),
        ),
    )

    X, tau = sp.symbols("X tau", real=True)
    normalized = dimensional_sine_gordon_normalized_coordinates(x, t, coefficients)
    physical = dimensional_sine_gordon_physical_coordinates(*normalized, coefficients)
    reverse = dimensional_sine_gordon_normalized_coordinates(
        *dimensional_sine_gordon_physical_coordinates(X, tau, coefficients),
        coefficients,
    )
    checks.check(
        "physical and normalized coordinate maps are exact inverses",
        all(sp.simplify(a - b) == 0 for a, b in zip(physical, (x, t), strict=True))
        and all(sp.simplify(a - b) == 0 for a, b in zip(reverse, (X, tau), strict=True)),
    )

    U = sp.Function("U")
    composed = U(*normalized)
    normalized_operator = (
        sp.diff(U(X, tau), tau, 2)
        - sp.diff(U(X, tau), X, 2)
        + sp.sin(U(X, tau))
    ).subs({X: normalized[0], tau: normalized[1]})
    checks.check(
        "chain rule maps the dimensional residual to mu times the normalized operator",
        sp.simplify(
            dimensional_sine_gordon_residual(composed, x, t, coefficients)
            - mu * normalized_operator
        )
        == 0,
    )

    rational_coefficients = dimensional_sine_gordon_coefficients(2, 8, 18)
    normalized_frequency = sp.Rational(1, 2)
    physical_field = dimensional_breather_field(
        x,
        t,
        normalized_frequency,
        rational_coefficients,
    )
    rational_normalized = dimensional_sine_gordon_normalized_coordinates(
        x,
        t,
        rational_coefficients,
    )
    checks.check(
        "canonical physical field is exactly the accepted normalized pullback",
        physical_field
        == breather_field(*rational_normalized, normalized_frequency),
    )
    checks.check(
        "pulled-back breather solves the declared dimensional field equation",
        sp.simplify(
            dimensional_sine_gordon_residual(
                physical_field,
                x,
                t,
                rational_coefficients,
            )
        )
        == 0,
    )
    observations = dimensional_breather_observables(
        normalized_frequency,
        rational_coefficients,
    )
    checks.check(
        "physical angular frequency and period retain the omega_0 conversion",
        observations.angular_frequency == sp.Rational(3, 2)
        and observations.period == 4 * sp.pi / 3,
    )
    checks.check(
        "profile length and inverse width are reciprocal physical scales",
        observations.inverse_width == 3 * sp.sqrt(3) / 4
        and sp.simplify(observations.profile_length * observations.inverse_width - 1)
        == 0,
    )
    checks.check(
        "profile scale is an asymptotic tail length rather than the core one-over-e point",
        sp.acosh(sp.E) != 1
        and sp.simplify(
            sp.acosh(sp.E) * observations.profile_length
            - observations.profile_length
        )
        != 0,
    )
    checks.check(
        "physical energy and canonical action include their distinct coefficient scales",
        observations.energy == 96 * sp.sqrt(3)
        and observations.action == 64 * sp.pi / 3
        and observations.energy != breather_energy(normalized_frequency)
        and observations.action != breather_action(normalized_frequency),
    )

    eta = sp.symbols("eta", positive=True, real=True)
    direct_energy = sp.simplify(
        8
        * mu
        * eta**2
        * sp.integrate(
            1 / sp.cosh(eta * x / scales.length) ** 2,
            (x, -sp.oo, sp.oo),
        )
    )
    checks.check(
        "direct physical kinetic slice gives E_scale times normalized energy",
        sp.simplify(direct_energy - 16 * scales.energy * eta) == 0,
    )
    checks.check(
        "canonical phase-space measure gives J_scale=sqrt(lambda*T)",
        sp.simplify(lam * scales.gap_frequency * scales.length - scales.action)
        == 0,
    )

    omega = sp.symbols("omega", positive=True, real=True)
    physical_energy = scales.energy * 16 * sp.sqrt(1 - omega**2)
    physical_action = scales.action * 16 * sp.acos(omega)
    checks.check(
        "physical action derivative reproduces physical angular frequency",
        sp.simplify(
            sp.diff(physical_energy, omega) / sp.diff(physical_action, omega)
            - omega * scales.gap_frequency
        )
        == 0,
    )
    checks.mutation_sensitive(
        "energy and action Jacobian factors are load bearing",
        lambda candidate: sp.simplify(
            candidate[0] / candidate[1] - scales.gap_frequency
        )
        == 0,
        (scales.energy, scales.action),
        (
            (sp.Integer(1), scales.action),
            (scales.energy, sp.Integer(1)),
            (sp.sqrt(lam * mu), scales.action),
        ),
    )

    gap_mu = sp.sqrt(mu / lam)
    length_mu = sp.sqrt(tension / mu)
    fixed_normalized_frequency = sp.Rational(1, 2)
    checks.check(
        "zero-onsite limit at fixed normalized frequency softens and delocalizes",
        sp.limit(fixed_normalized_frequency * gap_mu, mu, 0, dir="+") == 0
        and sp.limit(
            length_mu / sp.sqrt(1 - fixed_normalized_frequency**2),
            mu,
            0,
            dir="+",
        )
        == sp.oo
        and sp.limit(
            sp.sqrt(tension * mu)
            * breather_energy(fixed_normalized_frequency),
            mu,
            0,
            dir="+",
        )
        == 0,
    )
    omega_b = sp.symbols("omega_b", positive=True, real=True)
    checks.check(
        "fixed positive physical frequency leaves the breather domain before mu reaches zero",
        sp.limit(omega_b / gap_mu, mu, 0, dir="+") == sp.oo,
    )

    epsilon = sp.symbols("epsilon", positive=True, real=True)
    probe_value = physical_field.subs({x: 0, t: sp.pi / 9})
    alternative_force = sp.sin(probe_value) + 2 * epsilon * sp.sin(2 * probe_value)
    checks.check(
        "periodicity alone does not preserve the sine-Gordon breather",
        sp.simplify(alternative_force - sp.sin(probe_value)) != 0,
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
        "exact P095 implementation uses no direct NumPy trapezoidal alias",
        direct_alias_calls == [],
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
