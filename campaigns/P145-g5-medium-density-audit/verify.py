#!/usr/bin/env python3
"""Exact, source-aware verifier for proposed C-MED-005 and the G5 audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.constitutive import (
    mechanical_medium_conversion,
    si_constitutive_dimension_ledger,
)
from substrate_framework.induced_gravity import gravity_source_normalization_ledger
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-5/"
    "bridge_G5_Geff_medium_density.py"
)
DOSSIER = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-5/dossiers/"
    "G5-dossier.md"
)
FROZEN = ROOT / "campaigns/P145-g5-medium-density-audit/evidence/frozen-proposal.yaml"
REVISION = (
    ROOT
    / "campaigns/P145-g5-medium-density-audit/evidence/"
    "proposal-revision-0001.yaml"
)
SOURCE_SHA256 = "38a28bb452b055e7aa7894e1c31e3fcc98bfc5c6a8cbee2040aa003c62a4071a"
DOSSIER_SHA256 = "972605f48b9941c6a8d054c4bd7ca173d7cf6d05d370d92ac59db18d2a61e427"
FROZEN_SHA256 = "5ddab6e0f0d7d9eb84473289077e9dacdb4603bdbcea143329450a537ec17504"
REVISION_SHA256 = "d34c5a5a626670b6ac2c151805d82564b0fecdcf2a345a51a62d59375464d1b1"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> int:
    checks = CheckLedger("P145/C-MED-005")
    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned G5 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("pinned G5 dossier hash", _sha256(DOSSIER) == DOSSIER_SHA256)
    checks.check("initial proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    checks.check("proposal revision hash", _sha256(REVISION) == REVISION_SHA256)

    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [
        node for node in ast.walk(source_tree) if isinstance(node, ast.Assert)
    ]
    checks.check("fifteen source predicates", len(source_checks) == 15)
    checks.check("one source assertion", len(source_assertions) == 1)

    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "G5 has no NumPy integration compatibility event",
        compatibility.numpy_aliases == ()
        and compatibility.direct_legacy_attributes == 0
        and compatibility.dynamic_legacy_getattrs == 0
        and compatibility.imported_legacy_names == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    reproduction = subprocess.run(
        [sys.executable, str(SOURCE)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    checks.check("native G5 process exits cleanly", reproduction.returncode == 0)
    checks.check(
        "native G5 terminal tally is exact",
        reproduction.stdout.rstrip().endswith(
            "=============================================================================="
        )
        and "ALL 15 CHECKS PASS" in reproduction.stdout.splitlines()[-2],
    )

    dimensions = si_constitutive_dimension_ledger()
    checks.check(
        "SI dimension order is M L T I",
        dimensions.base_dimensions == ("M", "L", "T", "I"),
    )
    checks.check(
        "SI permittivity and inverse permeability columns are exact",
        dimensions.permittivity == sp.ImmutableMatrix([-1, -3, 4, 2])
        and dimensions.inverse_permeability
        == sp.ImmutableMatrix([-1, -1, 2, 2]),
    )
    checks.check(
        "mechanical density stiffness and energy columns are exact",
        dimensions.mass_density == sp.ImmutableMatrix([1, -3, 0, 0])
        and dimensions.stiffness
        == dimensions.energy_density
        == sp.ImmutableMatrix([1, -1, -2, 0]),
    )
    checks.check(
        "both mechanical maps require one common dimension column",
        dimensions.mass_density - dimensions.permittivity
        == dimensions.mechanical_conversion
        and dimensions.stiffness - dimensions.inverse_permeability
        == dimensions.mechanical_conversion
        == sp.ImmutableMatrix([2, 0, -4, -2]),
    )
    checks.check(
        "bare epsilon over two is not an SI mass density",
        dimensions.permittivity != dimensions.mass_density,
    )
    checks.check(
        "bare inverse mu over two is not an SI energy density",
        dimensions.inverse_permeability != dimensions.energy_density,
    )
    checks.check(
        "electromagnetic wave ratio has speed-squared dimension",
        dimensions.inverse_permeability - dimensions.permittivity
        == 2 * dimensions.speed,
    )

    epsilon, inverse_mu, a, b, xi, scale = sp.symbols(
        "epsilon mu_inv a b xi s",
        positive=True,
    )
    general = mechanical_medium_conversion(
        epsilon,
        inverse_mu,
        a,
        stiffness_conversion=b,
        strain_amplitude=xi,
    )
    checks.check(
        "general mechanical dictionary retains both conversion factors",
        general.mass_density == a * epsilon
        and general.stiffness == b * inverse_mu,
    )
    checks.check(
        "mechanical speed retains the conversion ratio",
        general.mechanical_speed_squared
        == b * inverse_mu / (a * epsilon)
        and general.speed_squared_ratio == b / a,
    )
    speed_solution = sp.solve(
        sp.Eq(
            general.mechanical_speed_squared,
            general.electromagnetic_speed_squared,
        ),
        b,
    )
    checks.check(
        "positive speed equality selects equal conversion factors",
        speed_solution == [a],
    )

    common = mechanical_medium_conversion(
        epsilon,
        inverse_mu,
        a,
        strain_amplitude=xi,
    )
    rescaled = mechanical_medium_conversion(
        epsilon,
        inverse_mu,
        scale * a,
        strain_amplitude=xi,
    )
    checks.check(
        "common conversion preserves electromagnetic speed",
        common.mechanical_speed_squared
        == common.electromagnetic_speed_squared
        == inverse_mu / epsilon,
    )
    checks.check(
        "common conversion remains an arbitrary scale orbit",
        rescaled.mechanical_speed_squared == common.mechanical_speed_squared
        and rescaled.mass_density == scale * common.mass_density
        and rescaled.stiffness == scale * common.stiffness,
    )
    checks.check(
        "strain energy requires both calibration and amplitude",
        common.strain_energy_density == a * inverse_mu * xi**2 / 2,
    )
    checks.check(
        "mass-equivalent strain energy is not inertial density at unit strain",
        common.mass_equivalent_density == a * epsilon * xi**2 / 2
        and common.mass_equivalent_density.subs(xi, 1)
        == common.mass_density / 2,
    )
    checks.check(
        "strain mutation changes energy without changing wave speed",
        sp.simplify(
            common.strain_energy_density.subs(xi, 2)
            / common.strain_energy_density.subs(xi, 1)
        )
        == 4
        and sp.diff(common.mechanical_speed_squared, xi) == 0,
    )
    checks.check(
        "unequal conversion mutation breaks the source wave-speed claim",
        mechanical_medium_conversion(
            epsilon,
            inverse_mu,
            a,
            stiffness_conversion=2 * a,
        ).mechanical_speed_squared
        == 2 * inverse_mu / epsilon,
    )

    output_rows = sp.Matrix(
        [
            [-1, -1, 0],
            [1, 0, 0],
            [0, -1, 0],
            [1, 1, 1],
        ]
    )
    checks.check(
        "source L1 L2 L3 have rank two rather than three",
        output_rows[:3, :].rank() == 2,
    )
    checks.check(
        "L3 is exactly the L1 plus L2 log consequence",
        output_rows[2, :] == output_rows[0, :] + output_rows[1, :],
    )
    checks.check(
        "adding free-kappa L4 raises output rank only to input rank three",
        output_rows.rank() == 3
        and len(output_rows.T.nullspace()) == 1
        and output_rows.T.nullspace()[0][3] == 0,
    )
    checks.check(
        "shared symbol membership is not an independence oracle",
        "{eps0_s, mu0_s}" in source_text
        and "sum(eps0_s in s" in source_text
        and "rank(" not in source_text,
    )

    operator = (0, -2, 0)
    energy_density = (1, -1, -2)
    mass_density = (1, -3, 0)
    energy_coupling = gravity_source_normalization_ledger(
        operator,
        energy_density,
    )
    mass_coupling = gravity_source_normalization_ledger(
        operator,
        mass_density,
    )
    checks.check(
        "Einstein energy-density source requires G over c fourth dimensions",
        energy_coupling.required_coupling_dimension
        == sp.ImmutableMatrix([-1, -1, 2])
        and energy_coupling.normalization_dimension
        == sp.ImmutableMatrix([0, -4, 4]),
    )
    checks.check(
        "mass-density source requires G over c squared dimensions",
        mass_coupling.required_coupling_dimension
        == dimensions.newton_over_speed_squared[:3, :]
        and mass_coupling.normalization_dimension
        == sp.ImmutableMatrix([0, -2, 2]),
    )
    checks.check(
        "dimensionless eight-pi times G matches neither SI source coupling",
        not energy_coupling.dimensionless_normalization_allowed
        and not mass_coupling.dimensionless_normalization_allowed,
    )
    checks.check(
        "G5 defines kappa with G units rather than deriving a typed source map",
        "kappa_U = u.meter**3 / (u.kilogram * u.second**2)" in source_text
        and "kappa = 8*pi*G_eff" in source_text,
    )

    kappa, target = sp.symbols("kappa target", positive=True)
    gravity_ratio = kappa * epsilon / inverse_mu / (8 * sp.pi)
    checks.check(
        "G5 L4 remains freely targetable through kappa",
        sp.solve(sp.Eq(gravity_ratio, target), kappa)
        == [8 * sp.pi * inverse_mu * target / epsilon],
    )
    checks.check(
        "L4 dimension is conditionally correct only after assigning G units to kappa",
        dimensions.newton_constant
        + dimensions.permittivity
        + dimensions.permeability
        == dimensions.newton_over_speed_squared,
    )
    checks.check(
        "G5 unit guards omit its load-bearing L2 and L3 correct-form dimensions",
        "rho_a = EPS0 / 2.0" in source_text
        and "strain_rhs = 1.0 / (2.0 * MU0)" in source_text
        and "dim(rho_a)" not in source_text
        and "dim(strain_rhs)" not in source_text,
    )

    total = checks.finish()
    print(f"P145 PRIMARY ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(run())
