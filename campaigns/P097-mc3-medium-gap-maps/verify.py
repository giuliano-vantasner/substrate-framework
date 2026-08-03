"""Primary exact verifier for the P097 MC3 medium-gap audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.lattice_scalar import (
    mass_scale_phase_gap_ratio,
    periodic_physical_phase_chain_eom_residual,
    periodic_physical_phase_chain_lagrangian,
    phase_inertia_from_mass_scale,
    physical_phase_chain_coefficients,
    physical_phase_chain_dimension_matrix,
    physical_phase_chain_dispersion_squared,
    physical_phase_chain_scales,
)
from substrate_framework.mixed_sine_gordon import (
    mixed_coefficient_from_absorption_rate,
    mixed_sine_gordon_dimension_matrix,
    mixed_sine_gordon_hyperbolic_coordinates,
    mixed_sine_gordon_linear_spectrum,
    mixed_sine_gordon_linearized_residual,
    mixed_sine_gordon_log_scale_jacobian,
    mixed_sine_gordon_residual,
    mixed_sine_gordon_scale_choice,
    normalized_hyperbolic_sine_gordon_residual,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-27/"
    "bridge_MC3_per_medium_omega0.py"
)
SOURCE_SHA256 = "74fbddc086781a0d61d5dd22effabf48d7ff37f47c6d97ebde0b2fb6186464a5"
CONTRACT_SHA256 = "de6b8fae8c205288895af43f4336f7bc04797553923cb2a036c3bc2bfdb73ad9"
FREEZE_SHA256 = "79a5d912685a1cfe01b518cff7a7f5f94964d83c0b5ded502dc4979b8ad44efb"
IMPORT_HASHES = {
    Path(
        "/home/dan/substrate/pulson-backreaction-bridge/sympy/rungs/"
        "rung165_c030_isotope_shift_prediction.py"
    ): "0a825e893439a87c143fb73524624ab523ff6467acd205698d8ce8456ca9909b",
    Path(
        "/home/dan/substrate/pulson-backreaction-bridge/sympy/rungs/"
        "rung176_c035_gas_type_collisional_rate.py"
    ): "54c9c63a91a63bdab93d5c297db0c0c7052de8925fbc7c36a592c244fd4537ee",
    Path(
        "/home/dan/substrate/merged-framework/bridges/phase-20/"
        "bridge_ME3_lattice_continuum.py"
    ): "8b5f888708b2edc202cb1acba37780aa62e7d71d002dc5042fd92e8afefbb0d0",
}


def _campaign_dir() -> Path:
    candidates = (
        Path("campaigns/P097-mc3-medium-gap-maps"),
        Path("proposals/P097-mc3-medium-gap-maps"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P097")
    campaign_dir = _campaign_dir()
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("MC3 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
    normalized_contract = (campaign_dir / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n", b"status: draft\n"
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
        "all runtime imports remain hash pinned",
        all(_sha256(path) == digest for path, digest in IMPORT_HASHES.items()),
    )

    check_calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    literal_calls = [
        node
        for node in check_calls
        if node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ]
    imports = {
        alias.name
        for node in source_tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "source has twenty-nine calls with twenty-six literal names",
        len(check_calls) == 29
        and len(literal_calls) == 26
        and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source imports no accepted framework implementation",
        imports
        == {"os", "io", "sys", "importlib.util", "contextlib", "sympy"}
        and not any(isinstance(node, ast.ImportFrom) for node in source_tree.body),
    )
    checks.check(
        "source divides an energy curvature by a bare mass without a phase scale",
        "omega0_A_sq = Vpp.subs(u, 0) / m_eff" in source_text
        and "m_eff*b" not in source_text
        and "m_eff * b" not in source_text,
    )
    checks.check(
        "source static kink does not evaluate its declared mixed equation",
        "theta_zz - sp.sin(theta_kink)" in source_text
        and "theta_{x tau}" in source_text
        and "sp.diff(theta_kink, x, t)" not in source_text,
    )
    checks.check(
        "source consumer guards include pass counts literals and string searches",
        "len(r165.PASS) >= 12" in source_text
        and "len(me3.PASS) >= 4" in source_text
        and "len(r176.PASS) >= 11" in source_text
        and "abs(N_OP_H2_bar - 0.05) < 1e-12" in source_text
        and '"sqrt(N d^2)" in DELIVERABLE' in source_text,
    )

    inertia, coupling, onsite, spacing = sp.symbols("I K V0 a", positive=True)
    q = sp.symbols("q0:3", real=True)
    velocity = sp.symbols("v0:3", real=True)
    acceleration = sp.symbols("b0:3", real=True)
    model = physical_phase_chain_coefficients(
        inertia, coupling, onsite, spacing
    )
    lagrangian = periodic_physical_phase_chain_lagrangian(q, velocity, model)
    residuals = periodic_physical_phase_chain_eom_residual(q, acceleration, model)
    checks.check(
        "sitewise variation derives the physical phase-chain equation",
        all(
            sp.simplify(
                inertia * acceleration[index]
                - sp.diff(lagrangian, q[index])
                - residuals[index]
            )
            == 0
            for index in range(3)
        ),
    )

    k, angular = sp.symbols("k Omega", real=True)
    dispersion = physical_phase_chain_dispersion_squared(k, model)
    expected_dispersion = (
        onsite + 4 * coupling * sp.sin(k * spacing / 2) ** 2
    ) / inertia
    checks.check(
        "Fourier substitution gives the exact physical lattice spectrum",
        sp.simplify(dispersion - expected_dispersion) == 0,
    )
    checks.mutation_sensitive(
        "lattice inertia curvature coupling and stencil factor are load bearing",
        lambda candidate: sp.simplify(candidate - expected_dispersion) == 0,
        dispersion,
        (
            (onsite + 4 * coupling * sp.sin(k * spacing / 2) ** 2),
            (2 * onsite + 4 * coupling * sp.sin(k * spacing / 2) ** 2)
            / inertia,
            (onsite - 4 * coupling * sp.sin(k * spacing / 2) ** 2) / inertia,
            (onsite + coupling * sp.sin(k * spacing / 2) ** 2) / inertia,
        ),
    )
    scales = physical_phase_chain_scales(model)
    checks.check(
        "gap band edge and long-wave speed follow from the same spectrum",
        physical_phase_chain_dispersion_squared(0, model)
        == scales.gap_frequency**2
        and physical_phase_chain_dispersion_squared(sp.pi / spacing, model)
        == scales.band_edge_frequency**2
        and sp.limit(
            sp.sqrt(
                (physical_phase_chain_dispersion_squared(k, model) - onsite / inertia)
                / k**2
            ),
            k,
            0,
            dir="+",
        )
        == scales.long_wave_speed,
    )

    dimension_matrix = physical_phase_chain_dimension_matrix()
    bare_formula_dimensions = sp.Matrix([1, 2, -2]) - sp.Matrix([1, 0, 0])
    lifted_formula_dimensions = (
        sp.Matrix([1, 2, -2]) - sp.Matrix([1, 2, 0])
    )
    checks.check(
        "dimension ledger distinguishes bare mass from phase inertia",
        dimension_matrix
        == sp.ImmutableMatrix(
            [[1, 1, 1, 0, 1, 0], [2, 2, 2, 1, 0, 1], [0, -2, -2, 0, 0, 0]]
        )
        and bare_formula_dimensions / 2 == sp.Matrix([0, 1, -1])
        and lifted_formula_dimensions / 2 == sp.Matrix([0, 0, -1]),
    )
    mass, displacement_scale = sp.symbols("m b", positive=True)
    checks.check(
        "declared displacement q=b*u derives I=m*b squared",
        phase_inertia_from_mass_scale(mass, displacement_scale)
        == mass * displacement_scale**2,
    )
    checks.mutation_sensitive(
        "the displacement scale is load bearing in the gap",
        lambda candidate: sp.simplify(
            candidate - sp.sqrt(onsite / (mass * displacement_scale**2))
        )
        == 0,
        sp.sqrt(onsite / phase_inertia_from_mass_scale(mass, displacement_scale)),
        (
            sp.sqrt(onsite / mass),
            sp.sqrt(onsite / (mass * displacement_scale)),
            displacement_scale * sp.sqrt(onsite / mass),
        ),
    )

    mass_h, mass_d = sp.symbols("m_H m_D", positive=True)
    scale_h, scale_d = sp.symbols("b_H b_D", positive=True)
    onsite_h, onsite_d = sp.symbols("V_H V_D", positive=True)
    ratio = mass_scale_phase_gap_ratio(
        mass_h, scale_h, onsite_h, mass_d, scale_d, onsite_d
    )
    expected_ratio = sp.sqrt(
        onsite_h * mass_d * scale_d**2
        / (onsite_d * mass_h * scale_h**2)
    )
    checks.check(
        "general host ratio retains both curvatures masses and phase scales",
        sp.simplify(ratio - expected_ratio) == 0,
    )
    sqrt_two_assumptions = {
        onsite_d: onsite_h,
        scale_d: scale_h,
        mass_d: 2 * mass_h,
    }
    checks.check(
        "sqrt two follows only under all exact equality premises",
        sp.simplify(ratio.subs(sqrt_two_assumptions) - sp.sqrt(2)) == 0
        and sp.simplify(
            ratio.subs({**sqrt_two_assumptions, onsite_d: 2 * onsite_h}) - 1
        )
        == 0
        and sp.simplify(
            ratio.subs({**sqrt_two_assumptions, scale_d: scale_h / sp.sqrt(2)})
            - 1
        )
        == 0,
    )
    checks.check(
        "zero onsite closes the linear gap without proving nonlinear existence",
        sp.limit(scales.gap_frequency, onsite, 0, dir="+") == 0
        and scales.gap_frequency.is_positive is True,
    )

    z, tau, epsilon, g = sp.symbols("z tau epsilon g", positive=True)
    psi = sp.Function("psi")(z, tau)
    direct_linearization = sp.diff(
        mixed_sine_gordon_residual(epsilon * psi, z, tau, g), epsilon
    ).subs(epsilon, 0)
    canonical_linearization = mixed_sine_gordon_linearized_residual(
        psi, z, tau, g
    )
    checks.check(
        "direct mixed-equation linearization preserves the cross derivative",
        sp.simplify(direct_linearization - canonical_linearization) == 0,
    )
    wave = sp.exp(sp.I * (k * z - angular * tau))
    characteristic = sp.simplify(
        mixed_sine_gordon_linearized_residual(wave, z, tau, g) / wave
    )
    checks.check(
        "mixed-coordinate plane wave gives k times Omega equals g",
        characteristic == k * angular - g,
    )
    checks.mutation_sensitive(
        "mixed derivative coefficient and characteristic signs are load bearing",
        lambda candidate: sp.simplify(characteristic - candidate) == 0,
        k * angular - g,
        (k * angular + g, angular**2 - g, k**2 + g, k * angular - 2 * g),
    )

    mixed_dimensions = mixed_sine_gordon_dimension_matrix()
    checks.check(
        "mixed coefficient absorption rate and frequency squared have distinct units",
        mixed_dimensions
        == sp.ImmutableMatrix([[-1, -1, 0, 0], [-1, 0, -1, -2]])
        and mixed_dimensions[:, 0] != mixed_dimensions[:, 1]
        and mixed_dimensions[:, 1] != mixed_dimensions[:, 3],
    )
    alpha, rate = sp.symbols("alpha gamma", positive=True)
    checks.check(
        "absorption requires an inverse-time factor to form the mixed coefficient",
        mixed_coefficient_from_absorption_rate(
            alpha, rate, sp.Rational(1, 2)
        )
        == alpha * rate / 2,
    )

    length = sp.symbols("L", positive=True)
    choice = mixed_sine_gordon_scale_choice(g, length)
    second_choice = mixed_sine_gordon_scale_choice(g, 2 * length)
    jacobian = mixed_sine_gordon_log_scale_jacobian()
    checks.check(
        "normalization leaves one reciprocal coordinate-scale direction",
        g * choice.length_scale * choice.time_scale == 1
        and second_choice.time_scale == choice.time_scale / 2
        and second_choice.inverse_time_scale == 2 * choice.inverse_time_scale
        and jacobian.rank() == 1
        and jacobian.nullspace() == [sp.Matrix([-1, 1])],
    )

    hyperbolic_space, hyperbolic_time = sp.symbols("X S", real=True)
    trial = hyperbolic_space**2 + 3 * hyperbolic_time**2 + hyperbolic_space * hyperbolic_time
    mapped_space, mapped_time = mixed_sine_gordon_hyperbolic_coordinates(
        z, tau, choice.length_scale, choice.time_scale
    )
    pulled = trial.subs(
        {hyperbolic_space: mapped_space, hyperbolic_time: mapped_time}
    )
    mixed_residual = mixed_sine_gordon_residual(pulled, z, tau, g)
    hyperbolic_residual = normalized_hyperbolic_sine_gordon_residual(
        trial, hyperbolic_space, hyperbolic_time
    ).subs({hyperbolic_space: mapped_space, hyperbolic_time: mapped_time})
    checks.check(
        "explicit light-cone map derives the hyperbolic sign and normalization",
        sp.trigsimp(mixed_residual + g * hyperbolic_residual) == 0,
    )

    positive_k = sp.symbols("k_pos", positive=True)
    spectrum = mixed_sine_gordon_linear_spectrum(positive_k, g)
    checks.check(
        "mixed spectrum has no finite k-independent laboratory floor",
        spectrum.angular_frequency == g / positive_k
        and sp.limit(spectrum.angular_frequency, positive_k, sp.oo) == 0
        and sp.limit(spectrum.angular_frequency, positive_k, 0, dir="+") == sp.oo,
    )
    kink = 4 * sp.atan(sp.exp(hyperbolic_space))
    kink_residual = normalized_hyperbolic_sine_gordon_residual(
        kink, hyperbolic_space, hyperbolic_time
    )
    checks.check(
        "exact kink is a coordinate-map cross-check not a coefficient derivation",
        sp.simplify(sp.expand_trig(kink_residual)) == 0,
    )

    exact_sources = (
        Path("src/substrate_framework/lattice_scalar.py"),
        Path("src/substrate_framework/mixed_sine_gordon.py"),
        Path("tests/test_lattice_scalar.py"),
        Path("tests/test_mixed_sine_gordon.py"),
    )
    checks.check(
        "exact P097 surfaces use no NumPy quadrature alias",
        all(
            "np." + "trapz" not in path.read_text(encoding="utf-8")
            and "np." + "trapezoid" not in path.read_text(encoding="utf-8")
            for path in exact_sources
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
