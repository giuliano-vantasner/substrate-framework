from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.gauge_u1 import u1_field_strength
from substrate_framework.maxwell import (
    maxwell_euler_lagrange,
    static_maxwell_point_source,
)
from substrate_framework.momentum_kernels import riesz_green_kernel
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "1c674bae211322b24a4504ff5aafc04424eb6a4bfe7813f63e5ec4337f783fc9"


def _source_inventory(source: Path) -> tuple[str, ast.Module, list[ast.Call], set[str]]:
    text = source.read_text(encoding="utf-8")
    tree = ast.parse(text)
    checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    numpy_calls = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "np"
    }
    return text, tree, checks, numpy_calls


def _static_action_residuals() -> tuple[sp.Expr, sp.Expr]:
    time, x = sp.symbols("t x", real=True)
    temporal = sp.Function("A0")(time, x)
    spatial = sp.Function("A1")(time, x)
    phi = sp.Function("phi")(x)
    rho = sp.Function("rho")(x)
    kappa = sp.Symbol("kappa", positive=True)
    action = maxwell_euler_lagrange(
        (temporal, spatial),
        (rho, 0),
        (time, x),
        sp.diag(1, -1),
        kappa,
    )
    component = action.expected_field_equation_residuals[0].subs(spatial, 0)
    correct = sp.simplify(component.subs(temporal, phi).doit())
    source_sign = sp.simplify(component.subs(temporal, -phi).doit())
    return correct, source_sign


def main(source_file: str) -> int:
    ledger = CheckLedger("P134/C-MAX-001/EM3")
    source = Path(source_file).resolve()
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    text, tree, checks, numpy_calls = _source_inventory(source)

    ledger.check("pinned EM3 hash", digest == SOURCE_SHA256)
    ledger.check("eleven source predicates", len(checks) == 11)
    ledger.check(
        "single source assertion belongs to the local check helper",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    ledger.check(
        "source uses NumPy but imports no SciPy",
        "import numpy as np" in text
        and "import scipy" not in text
        and "from scipy" not in text,
    )
    ledger.check(
        "no numerical-integration compatibility event",
        "trapz" not in numpy_calls
        and "trapezoid" not in numpy_calls
        and "np.trapz" not in text,
    )

    time, x, y = sp.symbols("t x y", real=True)
    coordinates = (time, x, y)
    potentials = tuple(
        sp.Function(f"A{index}")(*coordinates) for index in range(3)
    )
    currents = tuple(
        sp.Function(f"j{index}")(*coordinates) for index in range(3)
    )
    kappa = sp.Symbol("kappa", positive=True)
    action = maxwell_euler_lagrange(
        potentials,
        currents,
        coordinates,
        sp.diag(1, -1, -1),
        kappa,
    )
    ledger.check(
        "field strength is antisymmetric",
        action.field_strength == -action.field_strength.T,
    )
    ledger.check(
        "declared action varies to kappa divergence F equals current",
        all(residual == 0 for residual in action.derivation_residuals),
    )
    ledger.check(
        "Bianchi identities follow from d squared zero",
        all(residual == 0 for residual in action.bianchi_residuals),
    )
    ledger.check(
        "double divergence is identically zero",
        action.continuity_identity == 0,
    )
    ledger.check(
        "removing the kinetic term yields only minus current",
        action.source_only_euler_residuals == tuple(-entry for entry in currents),
    )

    correct_static, source_sign_static = _static_action_residuals()
    # Compare by structure through fresh symbols to avoid depending on function names.
    kappa_s = next(symbol for symbol in correct_static.free_symbols if symbol.name == "kappa")
    x_s = next(symbol for symbol in correct_static.free_symbols if symbol.name == "x")
    rho_term = next(
        function for function in correct_static.atoms(sp.Function) if function.func.__name__ == "rho"
    )
    phi_term = next(
        function for function in correct_static.atoms(sp.Function) if function.func.__name__ == "phi"
    )
    correct_expected = -kappa_s * sp.diff(phi_term, x_s, 2) - rho_term
    wrong_expected = kappa_s * sp.diff(phi_term, x_s, 2) - rho_term
    ledger.check(
        "A0 equals phi gives the frozen Poisson sign",
        sp.simplify(correct_static - correct_expected) == 0,
    )
    ledger.check(
        "EM3 A0 equals minus phi flips the action-derived Laplacian sign",
        sp.simplify(source_sign_static - wrong_expected) == 0
        and sp.simplify(source_sign_static - correct_static) != 0,
    )
    ledger.check(
        "source Poisson check is disconnected from its declared A0 sign",
        "A_0=-phi" in text
        and "E_vec = [-sp.diff(phi, v)" in text
        and "L_EM3 = L_kin + L_src" in text,
    )

    radius = sp.Symbol("r", positive=True)
    source_charge, test_charge = sp.symbols("Q q", real=True)
    point3 = static_maxwell_point_source(
        3, radius, source_charge, test_charge, kappa
    )
    ledger.check(
        "three-dimensional point source normalization",
        point3.unit_sphere_area == 4 * sp.pi
        and point3.potential == source_charge / (4 * sp.pi * kappa * radius)
        and point3.normalized_source_flux == source_charge,
    )
    ledger.check(
        "three-dimensional endpoint reuses the accepted Riesz kernel",
        sp.simplify(
            point3.potential
            - source_charge
            * riesz_green_kernel(3, 1, radius, kappa).green_kernel
        )
        == 0,
    )
    ledger.check(
        "point-source field is harmonic away from the source",
        point3.radial_harmonic_residual == 0,
    )
    ledger.check(
        "test-charge energy gradient equals charge times field",
        sp.simplify(-sp.diff(point3.potential_energy, radius) - point3.radial_force)
        == 0
        and sp.simplify(
            point3.radial_force - test_charge * point3.radial_electric_field
        )
        == 0,
    )

    point4 = static_maxwell_point_source(4, radius, source_charge, test_charge, kappa)
    point5 = static_maxwell_point_source(5, radius, source_charge, test_charge, kappa)
    ledger.check(
        "d greater than three supplies decaying counterexamples",
        point4.decays_at_infinity
        and point5.decays_at_infinity
        and not point4.inverse_square_force
        and point4.potential == source_charge / (4 * sp.pi**2 * kappa * radius**2)
        and sp.limit(point4.potential, radius, sp.oo) == 0
        and sp.limit(point5.potential, radius, sp.oo) == 0,
    )
    ledger.check(
        "inverse-square force selects d three only within the declared family",
        point3.inverse_square_force
        and point3.field_radial_power == -2
        and point4.field_radial_power == -3
        and point5.field_radial_power == -4,
    )

    reference = sp.Symbol("r0", positive=True)
    point2 = static_maxwell_point_source(
        2,
        radius,
        source_charge,
        test_charge,
        kappa,
        reference_radius=reference,
    )
    point1 = static_maxwell_point_source(
        1, radius, source_charge, test_charge, kappa
    )
    ledger.check(
        "d two keeps logarithmic reference data",
        sp.simplify(
            point2.potential
            + source_charge * sp.log(radius / reference) / (2 * sp.pi * kappa)
        )
        == 0
        and point2.normalized_source_flux == source_charge
        and not point2.decays_at_infinity,
    )
    ledger.check(
        "d one keeps the linear nondecaying branch",
        point1.potential == -source_charge * radius / (2 * kappa)
        and point1.normalized_source_flux == source_charge
        and not point1.decays_at_infinity,
    )

    baseline = static_maxwell_point_source(3, radius, 2, 3, 5)
    ledger.check(
        "kinetic source and probe mutations remain distinguishable",
        static_maxwell_point_source(3, radius, 2, 3, 10).radial_force
        == baseline.radial_force / 2
        and static_maxwell_point_source(3, radius, -2, 3, 5).radial_force
        == -baseline.radial_force
        and static_maxwell_point_source(3, radius, 2, -3, 5).radial_force
        == -baseline.radial_force,
    )
    ledger.check(
        "zero source and zero probe are different limits",
        static_maxwell_point_source(3, radius, 0, 3, 5).radial_electric_field == 0
        and static_maxwell_point_source(3, radius, 2, 0, 5).radial_electric_field
        == baseline.radial_electric_field
        and static_maxwell_point_source(3, radius, 2, 0, 5).radial_force == 0,
    )

    separation, observation = sp.symbols("a X", positive=True)
    neutral_dipole = (
        1 / (observation - separation) - 1 / (observation + separation)
    ) / (4 * sp.pi * kappa)
    ledger.check(
        "zero net charge does not imply zero source density or field",
        sp.simplify(neutral_dipole) != 0
        and sp.limit(neutral_dipole, observation, sp.oo) == 0
        and sp.simplify(-sp.diff(neutral_dipole, observation)) != 0,
    )
    ledger.check(
        "source neutral guard checks only the zeroed Coulomb ansatz",
        "phi_coulomb.subs(Q, 0)" in text
        and "neutral source Q=0 gives rho=0" in text,
    )

    nonpure_curvature = u1_field_strength(0, x, x, y)
    ledger.check(
        "zero source-only action leaves non-pure connections unconstrained",
        nonpure_curvature == 1
        and all(residual.subs({entry: 0 for entry in currents}) == 0
                for residual in action.source_only_euler_residuals),
    )
    ledger.check(
        "source no-kinetic guard contradicts its own source-only Euler result",
        "EL_nokin" in text
        and "nokin_is_just_source" in text
        and "gauge EOM leave A pure-gauge" in text,
    )

    mass, length, duration, charge_dimension = sp.symbols("M L T C")
    epsilon_dimension = charge_dimension**2 * duration**2 / (mass * length**3)
    hbar_dimension = mass * length**2 / duration
    speed_dimension = length / duration
    alpha_dimension = sp.simplify(
        charge_dimension**2
        / (epsilon_dimension * hbar_dimension * speed_dimension)
    )
    epsilon, mu, speed, elementary, hbar = sp.symbols(
        "epsilon mu c e hbar", positive=True
    )
    alpha = elementary**2 / (4 * sp.pi * epsilon * hbar * speed)
    ledger.check("fine-structure combination is conditionally dimensionless", alpha_dimension == 1)
    ledger.check(
        "constitutive substitution is an exact conditional identity",
        sp.simplify(
            alpha.subs(epsilon, 1 / (mu * speed**2))
            - elementary**2 * mu * speed / (4 * sp.pi * hbar)
        )
        == 0,
    )
    ledger.check(
        "source alpha magnitude is an embedded imported comparator",
        "1.602176634e-19" in text
        and "8.8541878128e-12" in text
        and "137.036" in text
        and "no real data consulted" in text,
    )
    ledger.check(
        "numeric Coulomb leg regresses its own hard-coded formula",
        "phi_num = Q_num / (4.0 * np.pi * eps0_num * r_num)" in text
        and {"polyfit", "gradient", "linspace"}.issubset(numpy_calls),
    )
    return int(ledger.finish())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", required=True)
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_file))
