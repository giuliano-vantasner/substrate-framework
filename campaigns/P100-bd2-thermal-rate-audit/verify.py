"""Primary exact verifier for the P100 BD2 thermal-rate adjudication."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.radial_energy import capillary_barrier_height
from substrate_framework.thermal import (
    activated_barrier_log_elasticity,
    conditional_coth_gated_capillary_rate,
    coth_gated_log_stationarity_residual,
    coth_gated_reduced_shape,
    coth_gated_response_shape,
    coth_gated_stationary_coordinate_upper_bound,
    declared_coth_effective_scale,
    inverse_power_input_log_elasticity,
    symmetric_two_level_gate,
    two_level_upper_occupation,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-28/"
    "bridge_BD2_scaling_law_thermal_optimum.py"
)
SOURCE_SHA256 = "91f2344bd59618b5915d018e1ee7d728b86f59a29e42e1a0a60cd833747f7a65"
CONTRACT_SHA256 = "4926b46554871d50e27c4a4ff00a173dc2556aa564bc4fda34820e8cdd5f303a"
FREEZE_SHA256 = "91f4ba60818652258a75a593e8ae6a75de459730bb0aa1e68cb490f207f81842"


def _campaign_dir() -> Path:
    candidates = (
        Path("campaigns/P100-bd2-thermal-rate-audit"),
        Path("proposals/P100-bd2-thermal-rate-audit"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _imports_module(tree: ast.AST, module: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(
            alias.name.split(".", 1)[0] == module for alias in node.names
        ):
            return True
        if (
            isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.module.split(".", 1)[0] == module
        ):
            return True
    return False


def main() -> int:
    checks = CheckLedger("C-TH-002")
    campaign_dir = _campaign_dir()
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("BD2 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
    normalized_contract = (campaign_dir / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n",
        b"status: draft\n",
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    checks.check(
        "pre-exposure freeze record remains immutable",
        _sha256(campaign_dir / "evidence/frozen-proposal.yaml") == FREEZE_SHA256,
    )

    literal_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    imported_modules = {
        alias.name
        for node in source_tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "source has sixteen literal checks and a local tally",
        len(literal_checks) == 16
        and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source imports no accepted framework API or stochastic solver",
        imported_modules == {"sys", "math", "sympy"}
        and not any(isinstance(node, ast.ImportFrom) for node in source_tree.body),
    )

    splitting = sp.symbols("x", real=True)
    occupation = two_level_upper_occupation(splitting)
    gate = symmetric_two_level_gate(splitting)
    checks.check(
        "normalized occupation and gate are exactly C-TH-001",
        occupation == 1 / (1 + sp.exp(splitting))
        and sp.simplify((gate - sp.sech(splitting / 2) ** 2 / 2).rewrite(sp.exp))
        == 0,
    )
    checks.mutation_sensitive(
        "one-half gate normalization is load bearing",
        lambda coefficient: sp.simplify(
            (
                gate
                - coefficient * sp.sech(splitting / 2) ** 2
            ).rewrite(sp.exp)
        )
        == 0,
        sp.Rational(1, 2),
        (1, 2, sp.Rational(1, 4)),
    )
    bare = sp.exp(-splitting)
    checks.check(
        "bare Boltzmann weight is an exact wrong-occupation counterexample",
        sp.simplify(
            (
                2 * bare * (1 - bare)
                - sp.sech(splitting / 2) ** 2 / 2
            ).rewrite(sp.exp)
        )
        != 0,
    )

    quantum, thermal = sp.symbols("q vartheta", positive=True)
    scale = declared_coth_effective_scale(quantum, thermal)
    checks.check(
        "declared coth scale has exact thermal and floor limits",
        sp.limit(scale / thermal, thermal, sp.oo) == 1
        and sp.limit(scale, thermal, 0, dir="+") == quantum / 2,
    )

    tension, drive, frequency = sp.symbols("tau p nu", positive=True)
    barrier = capillary_barrier_height(tension, drive)
    reduced_rate = conditional_coth_gated_capillary_rate(
        frequency,
        barrier,
        quantum,
        thermal,
    )
    source_rate = (
        frequency
        * tension
        / sp.sqrt(drive * scale)
        * sp.exp(-barrier / scale)
        * symmetric_two_level_gate(quantum / thermal)
    )
    checks.check(
        "capillary elimination exactly reproduces the displayed conditional rate",
        sp.simplify(reduced_rate - source_rate) == 0,
    )
    energy_dimension = sp.Matrix([1, 0, 0])
    length_dimension = sp.Matrix([0, 1, 0])
    inverse_time_dimension = sp.Matrix([0, 0, -1])
    tension_dimension = energy_dimension - length_dimension
    drive_dimension = energy_dimension - 2 * length_dimension
    prefactor_dimension = (
        tension_dimension
        - drive_dimension / 2
        - energy_dimension / 2
    )
    checks.check(
        "line-drive-scale prefactor is dimensionless and frequency supplies rate units",
        prefactor_dimension == sp.zeros(3, 1)
        and prefactor_dimension + inverse_time_dimension == inverse_time_dimension,
    )
    checks.mutation_sensitive(
        "capillary pi normalization is load bearing",
        lambda divisor: sp.simplify(
            frequency
            * coth_gated_response_shape(barrier, quantum, thermal)
            / sp.sqrt(divisor)
            - reduced_rate
        )
        == 0,
        sp.pi,
        (1, 2 * sp.pi, sp.pi / 2),
    )

    coordinate, ratio = sp.symbols("u b", positive=True)
    reduced_shape = coth_gated_reduced_shape(coordinate, ratio)
    log_residual = coth_gated_log_stationarity_residual(coordinate, ratio)
    expected_shape = (
        sp.sqrt(coordinate)
        * (1 - coordinate**2)
        * sp.exp(-2 * ratio * coordinate)
    )
    checks.check(
        "coth substitution gives the exact reduced temperature shape",
        reduced_shape == expected_shape
        and sp.simplify(sp.diff(sp.log(reduced_shape), coordinate) - log_residual)
        == 0,
    )
    stationary_numerator = sp.factor(
        2 * coordinate * (1 - coordinate**2) * log_residual
    )
    expected_numerator = sp.factor(
        1
        - 5 * coordinate**2
        - 4 * ratio * coordinate * (1 - coordinate**2)
    )
    checks.check(
        "source-prefactor stationary equation is the exact frozen cubic",
        stationary_numerator == expected_numerator,
    )
    checks.mutation_sensitive(
        "stationary barrier coefficient is load bearing",
        lambda coefficient: sp.factor(
            1
            - 5 * coordinate**2
            - coefficient * ratio * coordinate * (1 - coordinate**2)
            - expected_numerator
        )
        == 0,
        4,
        (2, 8, -4),
    )

    residual_derivative = sp.diff(log_residual, coordinate)
    manifest_negative_derivative = (
        -sp.Rational(1, 2) / coordinate**2
        - 2 * (1 + coordinate**2) / (1 - coordinate**2) ** 2
    )
    positive_domain_coordinate = sp.symbols("y_domain", positive=True)
    physical_derivative = sp.simplify(
        residual_derivative.subs(
            coordinate,
            sp.tanh(positive_domain_coordinate),
        )
    )
    physical_negative_terms = (
        -sp.Rational(1, 2) / sp.tanh(positive_domain_coordinate) ** 2
        - 2
        * (1 + sp.tanh(positive_domain_coordinate) ** 2)
        / sp.sech(positive_domain_coordinate) ** 4
    )
    upper_coordinate = coth_gated_stationary_coordinate_upper_bound()
    checks.check(
        "strictly decreasing residual brackets one unique stationary point",
        sp.simplify(residual_derivative - manifest_negative_derivative) == 0
        and sp.simplify(physical_derivative - physical_negative_terms) == 0
        and (sp.Rational(1, 2) / sp.tanh(positive_domain_coordinate) ** 2).is_positive
        is True
        and (
            2
            * (1 + sp.tanh(positive_domain_coordinate) ** 2)
            / sp.sech(positive_domain_coordinate) ** 4
        ).is_positive
        is True
        and sp.limit(log_residual, coordinate, 0, dir="+") == sp.oo
        and sp.simplify(log_residual.subs(coordinate, upper_coordinate) + 2 * ratio)
        == 0,
    )
    checks.check(
        "the unique stationary point is a global interior maximum",
        sp.limit(reduced_shape, coordinate, 0, dir="+") == 0
        and sp.limit(reduced_shape, coordinate, 1, dir="-") == 0
        and reduced_shape.subs(coordinate, sp.Rational(1, 2)).is_positive is True,
    )

    y_bound = sp.atanh(1 / sp.sqrt(5))
    thermal_lower_bound = quantum / (2 * y_bound)
    checks.check(
        "stationary bound excludes the advertised vartheta equals q over two point",
        upper_coordinate == 1 / sp.sqrt(5)
        and float(sp.N(y_bound, 30)) < 1
        and float(sp.N(thermal_lower_bound / quantum, 30)) > 1.039,
    )
    checks.check(
        "declared y equals one onset is not a stationary point of the rate",
        float(sp.N(log_residual.subs({coordinate: sp.tanh(1), ratio: 1}), 30)) < 0
        and float(sp.N(sp.tanh(1) - upper_coordinate, 30)) > 0,
    )

    general_exponent = sp.symbols("a", positive=True)
    general_residual = coth_gated_log_stationarity_residual(
        coordinate,
        ratio,
        prefactor_exponent=general_exponent,
    )
    general_upper = coth_gated_stationary_coordinate_upper_bound(general_exponent)
    checks.check(
        "every positive prefactor exponent has one model-dependent root",
        sp.simplify(
            sp.diff(general_residual, coordinate)
            - (
                -general_exponent / coordinate**2
                - 2 * (1 + coordinate**2) / (1 - coordinate**2) ** 2
            )
        )
        == 0
        and sp.limit(general_residual, coordinate, 0, dir="+") == sp.oo
        and sp.simplify(
            general_residual.subs(coordinate, general_upper) + 2 * ratio
        )
        == 0,
    )
    constant_shape = coth_gated_reduced_shape(
        coordinate,
        ratio,
        prefactor_exponent=0,
    )
    constant_residual = coth_gated_log_stationarity_residual(
        coordinate,
        ratio,
        prefactor_exponent=0,
    )
    checks.check(
        "constant prefactor is an admissible no-finite-optimum countermodel",
        constant_residual == -2 * coordinate / (1 - coordinate**2) - 2 * ratio
        and sp.limit(constant_shape, coordinate, 0, dir="+") == 1
        and sp.limit(constant_shape, coordinate, 1, dir="-") == 0,
    )

    activation_scale, energy_barrier = sp.symbols("Theta E", positive=True)
    response_in_barrier = (
        (energy_barrier / activation_scale) ** sp.Rational(1, 2)
        * sp.exp(-energy_barrier / activation_scale)
    )
    direct_barrier_elasticity = sp.simplify(
        energy_barrier
        * sp.diff(sp.log(response_in_barrier), energy_barrier)
    )
    expected_barrier_elasticity = (
        sp.Rational(1, 2) - energy_barrier / activation_scale
    )
    checks.check(
        "barrier response changes monotonicity at E over Theta equals one half",
        sp.simplify(direct_barrier_elasticity - expected_barrier_elasticity)
        == 0
        and sp.simplify(
            activated_barrier_log_elasticity(
                energy_barrier,
                activation_scale,
            )
            - expected_barrier_elasticity
        )
        == 0,
    )
    source_input_elasticity = inverse_power_input_log_elasticity(
        energy_barrier,
        activation_scale,
        2,
    )
    checks.check(
        "loading and fixed-q wavenumber elasticities reverse sign",
        source_input_elasticity == 2 * energy_barrier / activation_scale - 1
        and source_input_elasticity.subs(energy_barrier, activation_scale) == 1
        and source_input_elasticity.subs(energy_barrier, activation_scale / 4)
        == -sp.Rational(1, 2)
        and source_input_elasticity.subs(energy_barrier, activation_scale / 2)
        == 0,
    )
    checks.check(
        "constant prefactor changes the loading conclusion",
        inverse_power_input_log_elasticity(
            energy_barrier,
            activation_scale,
            2,
            prefactor_exponent=0,
        )
        == 2 * energy_barrier / activation_scale,
    )

    wave = sp.symbols("k", positive=True)
    fixed_quantum_rate = conditional_coth_gated_capillary_rate(
        1,
        wave**-2,
        1,
        1,
    )
    linked_quantum_rate = conditional_coth_gated_capillary_rate(
        1,
        wave**-2,
        wave**4,
        1,
    )
    fixed_derivative = sp.diff(fixed_quantum_rate, wave).subs(wave, 1)
    linked_derivative = sp.diff(linked_quantum_rate, wave).subs(wave, 1)
    checks.check(
        "undeclared q of k maps can reverse the total drive derivative",
        float(sp.N(fixed_derivative, 50)) > 0
        and float(sp.N(linked_derivative, 50)) < 0,
    )

    y = sp.symbols("y", positive=True)
    gate_y = sp.sech(y) ** 2 / 2
    log_temperature_sensitivity = -y * sp.diff(gate_y, y)
    ordinary_temperature_scaled_sensitivity = y * log_temperature_sensitivity
    checks.check(
        "source sensitivity scan is logarithmic rather than ordinary temperature sensitivity",
        sp.simplify(
            log_temperature_sensitivity
            - y * sp.sech(y) ** 2 * sp.tanh(y)
        )
        == 0
        and sp.simplify(
            ordinary_temperature_scaled_sensitivity
            - y**2 * sp.sech(y) ** 2 * sp.tanh(y)
        )
        == 0,
    )

    rho = sp.symbols("rho", positive=True)
    checks.check(
        "common energy rescaling leaves the entire dimensionless response invariant",
        sp.simplify(
            coth_gated_response_shape(
                rho * barrier,
                rho * quantum,
                rho * thermal,
            )
            - coth_gated_response_shape(barrier, quantum, thermal)
        )
        == 0,
    )
    target = sp.symbols("R_target", positive=True)
    unit_rate = conditional_coth_gated_capillary_rate(
        1,
        barrier,
        quantum,
        thermal,
    )
    fitted_frequency = target / unit_rate
    checks.check(
        "free attempt frequency fits any positive rate target",
        sp.simplify(
            conditional_coth_gated_capillary_rate(
                fitted_frequency,
                barrier,
                quantum,
                thermal,
            )
            - target
        )
        == 0,
    )
    checks.check(
        "exact campaign and canonical paths import no NumPy integration stack",
        not _imports_module(
            ast.parse(Path(__file__).read_text(encoding="utf-8")),
            "numpy",
        )
        and not _imports_module(
            ast.parse(
                Path("src/substrate_framework/thermal.py").read_text(
                    encoding="utf-8"
                )
            ),
            "numpy",
        ),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
