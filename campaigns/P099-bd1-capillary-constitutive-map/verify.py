"""Primary exact verifier for the P099 BD1 constitutive adjudication."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.radial_energy import (
    capillary_barrier_height,
    capillary_critical_radius,
    capillary_energy,
    equivalent_quadratic_loading_parameters,
    frank_core_line_tension,
    frank_core_log_sensitivities,
    frank_quadratic_capillary_map,
    monomial_loading_dimension_ledger,
    quadratic_capillary_identifiability_ledger,
    quadratic_loading_area_drive,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-28/"
    "bridge_BD1_real_variable_barrier.py"
)
SOURCE_SHA256 = "42579012eda87243639248664c6f90945c454046aa66c8de166ad6d2e594abc7"
CONTRACT_SHA256 = "9b6f356ab1d152c5bdb6b3798fc5bab00c02fe48886074a9c1b9b698e6eee277"
FREEZE_SHA256 = "4ec2fcd4213735edcfdfbbbbf81ac0e08f104974c258e07b095b1b666a35c213"


def _campaign_dir() -> Path:
    candidates = (
        Path("campaigns/P099-bd1-capillary-constitutive-map"),
        Path("proposals/P099-bd1-capillary-constitutive-map"),
    )
    return next(path for path in candidates if path.exists())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _raises_value_error(callable_object: object) -> bool:
    try:
        callable_object()  # type: ignore[operator]
    except ValueError:
        return True
    return False


def main() -> int:
    checks = CheckLedger("C-RG-002")
    campaign_dir = _campaign_dir()
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)

    checks.check("BD1 source hash is pinned", _sha256(SOURCE) == SOURCE_SHA256)
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
        "source has exactly eighteen literal checks and its terminal tally",
        len(literal_checks) == 18
        and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source imports no accepted framework constitutive API",
        imported_modules == {"sys", "sympy"}
        and not any(isinstance(node, ast.ImportFrom) for node in source_tree.body),
    )

    radius, tension, drive, core_offset = sp.symbols(
        "R tau p E_0",
        positive=True,
    )
    energy = capillary_energy(radius, tension, drive, core_offset)
    critical = capillary_critical_radius(tension, drive)
    relative_barrier = sp.simplify(
        energy.subs(radius, critical) - energy.subs(radius, 0)
    )
    checks.check(
        "canonical capillary radius is the unique positive stationary point",
        critical == tension / drive
        and sp.simplify(sp.diff(energy, radius).subs(radius, critical)) == 0,
    )
    checks.check(
        "positive drive makes the stationary point a strict global maximum",
        sp.diff(energy, radius, 2) == -2 * sp.pi * drive
        and sp.limit(energy, radius, sp.oo) == -sp.oo,
    )
    checks.check(
        "relative barrier is pi*tau squared over p and cancels only the offset",
        relative_barrier == capillary_barrier_height(tension, drive)
        and relative_barrier == sp.pi * tension**2 / drive
        and energy.subs(radius, critical) == core_offset + relative_barrier,
    )
    checks.mutation_sensitive(
        "relative barrier pi coefficient is load bearing",
        lambda coefficient: sp.simplify(
            coefficient * tension**2 / drive
            - capillary_barrier_height(tension, drive)
        )
        == 0,
        sp.pi,
        (1, 2 * sp.pi, sp.pi / 2),
    )

    stiffness, strength, outer, cutoff, epsilon = sp.symbols(
        "K_F s R_o r_c epsilon_core",
        positive=True,
    )
    coupling, amplitude, wavenumber, thickness = sp.symbols(
        "g A k l_m",
        positive=True,
    )
    line_tension = frank_core_line_tension(
        stiffness,
        strength,
        outer,
        cutoff,
        epsilon,
    )
    area_drive = quadratic_loading_area_drive(
        coupling,
        amplitude,
        wavenumber,
        thickness,
    )
    composed = frank_quadratic_capillary_map(
        stiffness,
        strength,
        outer,
        cutoff,
        epsilon,
        coupling,
        amplitude,
        wavenumber,
        thickness,
    )
    expected_tension = sp.pi * stiffness * strength**2 * sp.log(outer / cutoff) + epsilon
    expected_drive = coupling * amplitude**2 * wavenumber**2 * thickness / 2
    checks.check(
        "declared Frank/core premise retains its additive core line energy",
        line_tension == expected_tension and line_tension.has(epsilon),
    )
    checks.check(
        "declared quadratic loading premise retains every free drive input",
        area_drive == expected_drive
        and area_drive.free_symbols == {coupling, amplitude, wavenumber, thickness},
    )
    checks.check(
        "canonical composition gives the exact radius and relative barrier",
        sp.simplify(composed.critical_radius - 2 * line_tension / (
            coupling * amplitude**2 * wavenumber**2 * thickness
        ))
        == 0
        and sp.simplify(composed.barrier_height - 2 * sp.pi * line_tension**2 / (
            coupling * amplitude**2 * wavenumber**2 * thickness
        ))
        == 0,
    )
    checks.check(
        "composition introduces neither thermodynamic temperature nor a k-omega law",
        "temperature" not in composed.__dataclass_fields__
        and all(symbol.name not in {"T_temp", "omega"} for symbol in composed.barrier_height.free_symbols),
    )
    checks.mutation_sensitive(
        "drive factor two is load bearing",
        lambda divisor: sp.simplify(
            coupling * amplitude**2 * wavenumber**2 * thickness / divisor
            - area_drive
        )
        == 0,
        2,
        (1, 4),
    )
    checks.mutation_sensitive(
        "quadratic amplitude power is load bearing once declared",
        lambda exponent: sp.simplify(
            coupling * amplitude**exponent * wavenumber**2 * thickness / 2
            - area_drive
        )
        == 0,
        2,
        (1, 3),
    )
    checks.mutation_sensitive(
        "quadratic wavenumber power is load bearing once declared",
        lambda exponent: sp.simplify(
            coupling * amplitude**2 * wavenumber**exponent * thickness / 2
            - area_drive
        )
        == 0,
        2,
        (1, 3),
    )
    checks.check(
        "numeric cutoff reversal and zero loading coordinates are rejected",
        _raises_value_error(lambda: frank_core_line_tension(1, 1, 1, 2, 1))
        and _raises_value_error(lambda: quadratic_loading_area_drive(1, 0, 1, 1))
        and _raises_value_error(lambda: quadratic_loading_area_drive(1, 1, 0, 1)),
    )

    alpha = sp.symbols("alpha", real=True)
    dimensions = monomial_loading_dimension_ledger(alpha)
    columns = {
        name: dimensions.dimension_matrix[:, index]
        for index, name in enumerate(dimensions.quantity_names)
    }
    checks.check(
        "quadratic loading closes dimensions for every amplitude convention",
        dimensions.coupling_length_exponent == -1 - 2 * alpha
        and columns["coupling"]
        + 2 * columns["amplitude"]
        + 2 * columns["wavenumber"]
        == columns["bulk_bias"]
        and columns["bulk_bias"] + columns["thickness"] == columns["area_drive"],
    )
    checks.check(
        "radius and barrier dimensions follow from line tension and area drive",
        columns["line_tension"] - columns["area_drive"] == columns["critical_radius"]
        and 2 * columns["line_tension"] - columns["area_drive"] == columns["barrier_height"],
    )
    alternative = monomial_loading_dimension_ledger(
        0,
        amplitude_power=1,
        wavenumber_power=2,
    )
    source_like = monomial_loading_dimension_ledger(0)
    checks.check(
        "dimensions do not select the quadratic amplitude law",
        alternative.amplitude_power == 1
        and source_like.amplitude_power == 2
        and alternative.coupling_length_exponent == source_like.coupling_length_exponent == -1,
    )

    drive_variables = (coupling, amplitude, wavenumber, thickness)
    expected_barrier_elasticities = (-1, -2, -2, -1)
    checks.check(
        "effective drive log elasticities are exact holding tension fixed",
        tuple(
            sp.simplify(
                variable
                * sp.diff(composed.barrier_height, variable)
                / composed.barrier_height
            )
            for variable in drive_variables
        )
        == expected_barrier_elasticities,
    )
    frank_sensitivities = frank_core_log_sensitivities(
        stiffness,
        strength,
        outer,
        cutoff,
        epsilon,
    )
    frank_parameters = (stiffness, strength, outer, cutoff, epsilon)
    checks.check(
        "Frank/core component elasticities are derived and state dependent",
        frank_sensitivities.line_tension_log_elasticities
        == tuple(
            sp.simplify(
                variable * sp.diff(line_tension, variable) / line_tension
            )
            for variable in frank_parameters
        )
        and any(value.has(epsilon) for value in frank_sensitivities.line_tension_log_elasticities),
    )
    checks.check(
        "barrier doubles every Frank/core line-tension elasticity",
        frank_sensitivities.barrier_height_log_elasticities
        == tuple(
            sp.simplify(2 * value)
            for value in frank_sensitivities.line_tension_log_elasticities
        ),
    )

    identifiability = quadratic_capillary_identifiability_ledger()
    checks.check(
        "barrier alone identifies no effective constituent",
        identifiability.barrier_only_rank == 1
        and len(identifiability.barrier_only_nullspace) == 4
        and identifiability.barrier_only_coordinate_identifiable == (False,) * 5,
    )
    checks.check(
        "radius plus barrier identifies tension but not drive constituents",
        identifiability.rank == 2
        and len(identifiability.nullspace) == 3
        and identifiability.coordinate_identifiable
        == (True, False, False, False, False),
    )
    rho_a, rho_k, rho_l = sp.symbols("rho_A rho_k rho_l", positive=True)
    changed = equivalent_quadratic_loading_parameters(
        coupling,
        amplitude,
        wavenumber,
        thickness,
        amplitude_factor=rho_a,
        wavenumber_factor=rho_k,
        thickness_factor=rho_l,
    )
    checks.check(
        "three-parameter constructive family preserves the entire capillary map",
        sp.simplify(quadratic_loading_area_drive(*changed) - area_drive) == 0
        and sp.simplify(capillary_critical_radius(line_tension, quadratic_loading_area_drive(*changed)) - composed.critical_radius) == 0
        and sp.simplify(capillary_barrier_height(line_tension, quadratic_loading_area_drive(*changed)) - composed.barrier_height) == 0,
    )

    positive_tension = sp.symbols("T_positive", positive=True)
    effective_barrier = (
        2
        * sp.pi
        * positive_tension**2
        / (coupling * amplitude**2 * wavenumber**2 * thickness)
    )
    checks.check(
        "no-loading and zero-coupling limits diverge inside the declared model",
        sp.limit(effective_barrier, amplitude, 0, dir="+") == sp.oo
        and sp.limit(effective_barrier, coupling, 0, dir="+") == sp.oo,
    )
    negative_drive = sp.symbols("q", positive=True)
    negative_energy = 2 * sp.pi * radius * tension + sp.pi * radius**2 * negative_drive
    zero_drive_derivative = 2 * sp.pi * tension
    negative_drive_derivative = sp.diff(negative_energy, radius)
    checks.check(
        "zero or negative area drive has no positive stationary barrier top",
        zero_drive_derivative.is_positive is True
        and negative_drive_derivative.is_positive is True
        and sp.solve(sp.Eq(negative_drive_derivative, 0), radius) == [],
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
