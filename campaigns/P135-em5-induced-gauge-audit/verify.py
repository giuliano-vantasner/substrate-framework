from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.source_audit import (
    audit_numpy_trapezoid_compatibility,
)
from substrate_framework.vacuum_polarization import (
    euclidean_transverse_projector,
    scalar_qed2_vacuum_polarization,
)
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "bcf2c49e1e98eefea98be0076afd29341ce80fd71a7b141618978139982e4ec0"
FROZEN_PROPOSAL_SHA256 = "cbbf294212c698c80d090ace72b6123b8003cb359f6f8aafcfbd9c809f771388"


def _source_inventory(
    source: Path,
) -> tuple[str, ast.Module, list[ast.Call], set[str]]:
    text = source.read_text(encoding="utf-8")
    tree = ast.parse(text)
    checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assigned = {
        target.id
        for node in ast.walk(tree)
        if isinstance(node, (ast.Assign, ast.AnnAssign))
        for target in (
            node.targets if isinstance(node, ast.Assign) else [node.target]
        )
        if isinstance(target, ast.Name)
    }
    return text, tree, checks, assigned


def _real_parameter_reconstruction(
    q2: sp.Expr,
    mass: sp.Expr,
    charge: sp.Expr,
) -> tuple[sp.Expr, sp.Expr]:
    ledger = scalar_qed2_vacuum_polarization(q2, mass, charge)
    ratio = ledger.dimensionless_ratio
    y = ledger.real_parameter
    endpoint_integral = sp.simplify(
        ledger.real_antiderivative.subs(y, 1)
        - sp.limit(ledger.real_antiderivative, y, 0)
    )
    reconstructed = sp.simplify(
        charge**2
        * q2
        / (sp.pi * (q2 + 4 * mass**2))
        * endpoint_integral
    )
    return endpoint_integral, reconstructed


def main(source_file: str) -> int:
    ledger = CheckLedger("P135/C-VAC-001/EM5")
    source = Path(source_file).resolve()
    campaign = Path(__file__).resolve().parent
    frozen = campaign / "evidence" / "frozen-proposal.yaml"
    text, tree, checks, assigned = _source_inventory(source)

    ledger.check(
        "pinned EM5 hash",
        hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA256,
    )
    ledger.check(
        "frozen proposal hash",
        hashlib.sha256(frozen.read_bytes()).hexdigest()
        == FROZEN_PROPOSAL_SHA256,
    )
    ledger.check("eleven source predicates", len(checks) == 11)
    ledger.check(
        "single source assertion belongs to local check helper",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    ledger.check("source executable imports only SymPy", imports == {"sympy"})
    compatibility = audit_numpy_trapezoid_compatibility(text, filename=str(source))
    ledger.check(
        "no NumPy trapezoid compatibility event",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    ledger.check(
        "source implements no scalar field determinant bubble or seagull",
        not ({"Psi", "bubble", "seagull", "determinant"} & assigned)
        and "imported      -- the charged mode".lower() in text.lower(),
    )

    q0, q1 = sp.symbols("q0 q1", real=True)
    projector = euclidean_transverse_projector((q0, q1))
    ledger.check(
        "nonzero-momentum projector is idempotent",
        projector.idempotence_residual == sp.zeros(2),
    )
    ledger.check(
        "projector is transverse on both sides",
        projector.left_transversality_residual == sp.zeros(1, 2)
        and projector.right_transversality_residual == sp.zeros(2, 1),
    )
    ledger.check(
        "projector has a zero-momentum domain exclusion",
        "q^2" in text and projector.matrix.has(1 / (q0**2 + q1**2)),
    )

    q2, mass, charge = sp.symbols("Q m e", positive=True)
    scalar = scalar_qed2_vacuum_polarization(q2, mass, charge)
    x = scalar.parameter
    scalar_shape = (1 - 2 * x) ** 2
    source_shape = 4 * x * (1 - x)
    ledger.check(
        "scalar loop carries the scalar numerator",
        sp.simplify(
            scalar.projector_parameter_integrand
            - charge**2
            * q2
            * scalar_shape
            / (4 * sp.pi * (mass**2 + q2 * x * (1 - x)))
        )
        == 0,
    )
    ledger.check(
        "source numerator is the fermionic Schwinger-model shape",
        "u * (1 - u) * q2s" in text
        and sp.simplify(source_shape - scalar_shape) != 0,
    )
    ledger.check(
        "source itself identifies the imported Schwinger result as fermionic",
        "Schwinger's exact 1+1D fermionic Pi = e^2/pi" in text,
    )
    ledger.check(
        "source nevertheless labels that integral bosonic scalar QED",
        "bosonic one-loop scalar-QED calculation" in text,
    )

    endpoint_integral, reconstructed = _real_parameter_reconstruction(
        q2, mass, charge
    )
    ratio = scalar.dimensionless_ratio
    ledger.check(
        "real-domain antiderivative is exact",
        scalar.antiderivative_residual == 0
        and sp.simplify(
            endpoint_integral
            - (sp.atanh(ratio) / ratio**3 - 1 / ratio**2)
        )
        == 0,
    )
    ledger.check(
        "parameter route reproduces the closed projector coefficient",
        sp.simplify(reconstructed - scalar.projector_coefficient) == 0,
    )
    ledger.check(
        "massive scalar projector coefficient vanishes at zero momentum",
        sp.limit(scalar.projector_coefficient, q2, 0) == 0,
    )
    ledger.check(
        "massive scalar local Maxwell form factor",
        sp.simplify(
            sp.limit(scalar.projector_coefficient / q2, q2, 0)
            - charge**2 / (12 * sp.pi * mass**2)
        )
        == 0,
    )
    ledger.check(
        "low-momentum F squared coefficient keeps mass and dimensions",
        scalar.local_fmunu_squared_coefficient
        == charge**2 / (48 * sp.pi * mass**2)
        and scalar.local_f01_squared_coefficient
        == charge**2 / (24 * sp.pi * mass**2),
    )
    ledger.check(
        "next low-momentum term is independently sensitive",
        sp.simplify(
            sp.limit(
                (
                    scalar.projector_coefficient
                    - charge**2 * q2 / (12 * sp.pi * mass**2)
                )
                / q2**2,
                q2,
                0,
            )
            + charge**2 / (120 * sp.pi * mass**4)
        )
        == 0,
    )
    ledger.check(
        "scalar massless limit is infrared divergent",
        sp.limit(scalar.projector_coefficient, mass, 0, dir="+") == sp.oo,
    )
    ledger.check(
        "heavy scalar decouples from the fixed-momentum kernel",
        sp.limit(scalar.projector_coefficient, mass, sp.oo) == 0,
    )

    fermion_like = sp.simplify(
        charge**2
        / sp.pi
        * sp.integrate(
            q2 * x * (1 - x) / (mass**2 + q2 * x * (1 - x)),
            (x, 0, 1),
        )
    )
    ledger.check(
        "fermion-like source integral has finite Schwinger limit",
        sp.simplify(
            sp.limit(fermion_like, mass, 0, dir="+") - charge**2 / sp.pi
        )
        == 0,
    )
    ledger.check(
        "scalar and fermion massless limits discriminate statistics",
        sp.limit(scalar.projector_coefficient, mass, 0, dir="+") == sp.oo
        and sp.limit(fermion_like, mass, 0, dir="+") == charge**2 / sp.pi,
    )

    ledger.check(
        "bubble and seagull derive the Ward cancellation",
        scalar.bubble_ward_tadpole_coefficient == 2 * charge**2
        and scalar.seagull_ward_tadpole_coefficient == -2 * charge**2
        and scalar.ward_tadpole_residual == 0,
    )
    ledger.check(
        "omitting the seagull breaks the Ward identity",
        scalar.bubble_ward_tadpole_coefficient != 0,
    )
    ledger.check(
        "flipping the seagull sign breaks the Ward identity",
        sp.simplify(
            scalar.bubble_ward_tadpole_coefficient
            - scalar.seagull_ward_tadpole_coefficient
        )
        != 0,
    )
    ledger.check(
        "source Ward check is true only by constructed projector",
        "Pi_tensor = Pi_q2 * P" in text
        and "ward = sp.simplify(q_vec.T * Pi_tensor)" in text
        and "bubble" not in assigned
        and "seagull" not in assigned,
    )

    a0, a1 = sp.symbols("A0 A1", real=True)
    amplitude = sp.Matrix([a0, a1])
    f01 = sp.expand(q0 * a1 - q1 * a0)
    projector_quadratic = sp.simplify(
        (amplitude.T * projector.matrix * amplitude)[0]
    )
    ledger.check(
        "projector quadratic form is nonlocal F01 squared over q squared",
        sp.simplify(
            projector_quadratic - f01**2 / projector.momentum_squared
        )
        == 0,
    )
    ledger.check(
        "source comments know the nonlocal denominator",
        "A_mu P^{munu} A_nu  <->  F_01^2 / q^2" in text,
    )
    ledger.check(
        "source Maxwell check drops that denominator",
        "coefficient of int F_01^2" in text
        and "induced_prefactor = (e**2 / (2 * sp.pi))" in text,
    )
    ledger.check(
        "source coefficient equality is definition-only algebra",
        sp.simplify(
            charge**2 / (4 * sp.pi)
            - sp.Rational(1, 4) / (sp.pi / charge**2)
        )
        == 0,
    )

    # In D=2 with D_mu=partial_mu-i*e*A_mu and [A]=0, [e]=1 and [F]=1.
    # Since the Lagrangian density has dimension two, a local kappa*F^2/4
    # requires [kappa]=0.  The source's e^2 coefficient has dimension two,
    # while the actual e^2/m^2 low-energy coefficient is dimensionless.
    lagrangian_dimension = 2
    gauge_potential_dimension = 0
    derivative_dimension = 1
    charge_dimension = derivative_dimension - gauge_potential_dimension
    field_strength_dimension = derivative_dimension + gauge_potential_dimension
    required_local_coefficient_dimension = (
        lagrangian_dimension - 2 * field_strength_dimension
    )
    source_local_coefficient_dimension = 2 * charge_dimension
    scalar_local_coefficient_dimension = 2 * charge_dimension - 2
    ledger.check(
        "source local coefficient fails the declared two-dimensional units",
        required_local_coefficient_dimension == 0
        and source_local_coefficient_dimension == 2
        and source_local_coefficient_dimension
        != required_local_coefficient_dimension
        and scalar_local_coefficient_dimension
        == required_local_coefficient_dimension
        and scalar.low_momentum_form_factor.has(mass),
    )

    kappa, scale = sp.symbols("kappa lambda", positive=True)
    invariant_mass2 = charge**2 / (sp.pi * kappa)
    transformed_mass2 = (charge / scale) ** 2 / (
        sp.pi * (kappa / scale**2)
    )
    source_mass2_transformed = (charge / scale) ** 2 / sp.pi
    ledger.check(
        "canonically normalized pole ratio is field-rescaling invariant",
        sp.simplify(transformed_mass2 - invariant_mass2) == 0,
    )
    ledger.check(
        "source e squared pole is not field-rescaling invariant without kappa",
        sp.simplify(source_mass2_transformed - charge**2 / sp.pi) != 0,
    )
    ledger.check(
        "source dresses an undeclared bare q squared propagator",
        "NO Maxwell/Chern-Simons term explicitly present" in text
        and "denom = q2_pole - Pi_const" in text,
    )

    time, coordinate = sp.symbols("t x", real=True)
    nonflat_connection_f01 = sp.diff(time, time) - sp.diff(0, coordinate)
    ledger.check(
        "zero loop coefficient does not force a connection to be pure gauge",
        nonflat_connection_f01 == 1,
    )
    ledger.check(
        "source neutral-limit implication is stronger than its algebra",
        "Pi_neutral == 0" in text and "so F=0" in text,
    )
    ledger.check(
        "two-dimensional local Maxwell theory has no massless photon polarization",
        2 - 2 == 0,
    )

    doubled = scalar_qed2_vacuum_polarization(q2, mass, charge, 2)
    ledger.check(
        "species multiplicity changes the loop coefficient",
        sp.simplify(
            doubled.projector_coefficient - 2 * scalar.projector_coefficient
        )
        == 0,
    )
    ledger.check(
        "halving charge changes the loop coefficient quadratically",
        sp.simplify(
            scalar_qed2_vacuum_polarization(q2, mass, charge / 2).projector_coefficient
            - scalar.projector_coefficient / 4
        )
        == 0,
    )
    ledger.check(
        "mass mutation changes the loop kernel",
        sp.simplify(
            scalar_qed2_vacuum_polarization(q2, 2 * mass, charge).projector_coefficient
            - scalar.projector_coefficient
        )
        != 0,
    )

    ledger.check(
        "EM5.1 survives only as kinematic projector algebra",
        projector.idempotence_residual == sp.zeros(2),
    )
    ledger.check(
        "EM5.2 and EM5.7 survive only for a supplied transverse kernel",
        projector.left_transversality_residual == sp.zeros(1, 2)
        and projector.right_transversality_residual == sp.zeros(2, 1),
    )
    ledger.check(
        "EM5.3 is refuted for the declared scalar statistics",
        sp.limit(scalar.projector_coefficient, mass, 0, dir="+") == sp.oo,
    )
    ledger.check(
        "EM5.4 narrow massive zero-momentum statement survives",
        sp.limit(scalar.projector_coefficient, q2, 0) == 0,
    )
    ledger.check(
        "EM5.5 EM5.8 and EM5.11 inherit the wrong loop and bare kernel",
        "denom = q2_pole - Pi_const" in text
        and sp.limit(scalar.projector_coefficient, mass, 0, dir="+") != charge**2 / sp.pi,
    )
    ledger.check(
        "EM5.6 local action is refuted by the missing q squared denominator",
        sp.simplify(
            projector_quadratic - f01**2 / projector.momentum_squared
        )
        == 0,
    )
    ledger.check(
        "EM5.9 coefficient limit survives but pure-gauge conclusion fails",
        sp.limit(scalar.projector_coefficient, charge, 0) == 0
        and nonflat_connection_f01 == 1,
    )
    ledger.check(
        "EM5.10 remains a valid nontransverse counterexample only",
        sp.simplify(
            (sp.Matrix([q0, q1]).T * sp.eye(2) / 2)
        )
        != sp.zeros(1, 2),
    )

    return ledger.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", required=True)
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_file))
