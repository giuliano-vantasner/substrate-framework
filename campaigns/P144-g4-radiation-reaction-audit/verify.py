from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.generalized_dissipation import (
    energy_rate_with_external_work,
    metric_power_balance,
    power_balance_residual,
    rayleigh_dissipation,
    scalar_power_balance_force,
)
from substrate_framework.retarded_wave import retarded_point_source_radiation
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "308c8d82aff062fb0f0254498fb2bdb19fe6bdc207036cb0fa73643d3608c799"
DOSSIER_SHA256 = "e88a3bdc12599f72c4092f374fa73ebf3c7632c6ae7e70f5b6c238c38337a39b"
FROZEN_PROPOSAL_SHA256 = "718af2ae0f1fce5b54df312c446e9e4df92a278eafaddaa4c98d47f4a65c25c2"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_file: str, dossier_file: str) -> int:
    source_path = Path(source_file)
    dossier_path = Path(dossier_file)
    frozen_path = Path(__file__).parent / "evidence" / "frozen-proposal.yaml"
    source_text = source_path.read_text(encoding="utf-8")
    dossier_text = dossier_path.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(source_path))
    checks = CheckLedger("P144/C-RR-001")

    checks.check("pinned G4 source hash", _sha256(source_path) == SOURCE_SHA256)
    checks.check("pinned G4 dossier hash", _sha256(dossier_path) == DOSSIER_SHA256)
    checks.check("frozen proposal hash", _sha256(frozen_path) == FROZEN_PROPOSAL_SHA256)

    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("ten source predicates", len(source_checks) == 10)
    checks.check("one source assertion", len(source_assertions) == 1)

    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(source_path),
    )
    checks.check(
        "G4 compatibility event is one direct immutable legacy access",
        compatibility.direct_legacy_attributes == 1
        and compatibility.dynamic_legacy_getattrs == 0
        and compatibility.imported_legacy_names == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    loaded_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    checks.check(
        "source contains no executable self-field or momentum-flux route",
        not loaded_names.intersection(
            {"h_ret", "h_adv", "h_rad", "dp_rad", "schott_energy", "source_equation"}
        ),
    )
    checks.check(
        "source force is the scalar power quotient in closed form",
        "F_self.v = -P_rad  =>  F_self = -P_rad / v" in source_text
        and "F_self = -sp.Rational(1, 8) * kappa * gamma_expr**6" in source_text,
    )
    checks.check(
        "dossier itself identifies the quotient as non-independent",
        "not an\nindependent derivation" in dossier_text
        and "If the builder uses F_self = −P_rad/v as a definition, the check is vacuous"
        in dossier_text,
    )

    power, first_rate, second_rate = sp.symbols("P u w", positive=True)
    gx, gy = sp.symbols("g_x g_y", positive=True)
    metric_balance = metric_power_balance(
        power,
        (first_rate, second_rate),
        sp.diag(gx, gy),
    )
    denominator = gx * first_rate**2 + gy * second_rate**2
    checks.check(
        "declared metric gives an exact particular balanced force",
        metric_balance.particular_force
        == sp.ImmutableMatrix(
            [
                -power * gx * first_rate / denominator,
                -power * gy * second_rate / denominator,
            ]
        )
        and metric_balance.balance_residual == 0,
    )

    alpha = sp.symbols("alpha", real=True)
    work_free = sp.ImmutableMatrix([alpha * second_rate, -alpha * first_rate])
    alternate = metric_balance.particular_force + work_free
    checks.check(
        "one scalar balance leaves an affine force family",
        power_balance_residual(power, (first_rate, second_rate), alternate) == 0
        and alternate != metric_balance.particular_force,
    )

    inverse_metric = metric_balance.coordinate_metric.inv()
    objective_gap = sp.simplify(
        (alternate.T * inverse_metric * alternate)[0]
        - (
            metric_balance.particular_force.T
            * inverse_metric
            * metric_balance.particular_force
        )[0]
    )
    expected_gap = sp.simplify((work_free.T * inverse_metric * work_free)[0])
    checks.check(
        "particular force is the declared-metric minimum",
        sp.simplify(objective_gap - expected_gap) == 0,
    )

    euclidean = metric_power_balance(power, (first_rate, second_rate))
    weighted = metric_power_balance(
        power,
        (first_rate, second_rate),
        sp.diag(gx, 1),
    )
    checks.check(
        "allocation changes with additional coordinate metric data",
        euclidean.balance_residual == weighted.balance_residual == 0
        and sp.simplify(
            euclidean.particular_force[0] - weighted.particular_force[0]
        )
        != 0,
    )

    rate = sp.symbols("v", positive=True)
    checks.check(
        "single nonzero rate has the conditional quotient force",
        scalar_power_balance_force(power, rate) == -power / rate,
    )
    arbitrary_force = sp.symbols("F", real=True)
    checks.check(
        "zero rate separates inconsistency from underdetermination",
        power_balance_residual(power, (0,), (arbitrary_force,)) == power
        and power_balance_residual(0, (0,), (arbitrary_force,)) == 0,
    )

    kappa, energy, gamma, acceleration = sp.symbols(
        "kappa E0 gamma a",
        positive=True,
    )
    g4_power = kappa * energy**2 * gamma**6 * rate**2 * acceleration**2 / 8
    g4_force = scalar_power_balance_force(g4_power, rate)
    checks.check(
        "G4 force follows conditionally from its supplied power and nothing more",
        g4_force == -kappa * energy**2 * gamma**6 * rate * acceleration**2 / 8,
    )
    checks.mutation_sensitive(
        "supplied power coefficient controls the quotient",
        lambda coefficient: sp.simplify(
            (-coefficient * kappa * energy**2 * gamma**6 * rate * acceleration**2)
            * rate
            + coefficient * kappa * energy**2 * gamma**6 * rate**2 * acceleration**2
        )
        == 0
        and sp.simplify(
            (-coefficient * kappa * energy**2 * gamma**6 * rate * acceleration**2)
            - g4_force
        )
        == 0,
        sp.Rational(1, 8),
        [sp.Rational(1, 4), sp.Rational(1, 16), sp.Integer(0)],
    )

    edot = sp.symbols("Edot", positive=True)
    accepted_scalar = retarded_point_source_radiation(1 / kappa, 1, 1, edot)
    source_power = kappa * edot**2 / 8
    checks.check(
        "accepted scalar-action normalization contradicts inherited G1 coefficient",
        accepted_scalar.total_outward_power == kappa * edot**2 / 2
        and sp.simplify(accepted_scalar.total_outward_power / source_power) == 4,
    )

    damping_first, damping_second = sp.symbols("d_1 d_2", positive=True)
    rayleigh = rayleigh_dissipation(
        (first_rate, second_rate),
        sp.diag(damping_first, damping_second),
    )
    expected_dissipation = (
        damping_first * first_rate**2 + damping_second * second_rate**2
    )
    checks.check(
        "declared Rayleigh matrix closes force power and energy loss",
        rayleigh.rayleigh_function == expected_dissipation / 2
        and rayleigh.generalized_force
        == sp.ImmutableMatrix(
            [-damping_first * first_rate, -damping_second * second_rate]
        )
        and rayleigh.dissipated_power == expected_dissipation
        and rayleigh.energy_rate_without_external_work == -expected_dissipation,
    )

    external_first, external_second = sp.symbols("F_x F_y", real=True)
    checks.check(
        "external work remains a separate reservoir term",
        sp.simplify(
            energy_rate_with_external_work(
                rayleigh,
                (external_first, external_second),
            )
            - (
                external_first * first_rate
                + external_second * second_rate
                - expected_dissipation
            )
        )
        == 0,
    )

    checks.check(
        "wrong-sign damping matrix is rejected",
        _rejects_wrong_sign_damping(first_rate, second_rate, damping_first),
    )

    time = sp.symbols("t", positive=True)
    v_profile = sp.Rational(3, 5) * sp.tanh(sp.Rational(4, 5) * time)
    prescribed_energy = energy / sp.sqrt(1 - v_profile**2)
    checks.check(
        "G4 numeric profile increases prescribed kinetic energy",
        sp.diff(prescribed_energy, time).subs(time, 1).is_positive is True
        and "Here E(t)=gamma E0 is INCREASING because v rises" in source_text,
    )

    omega, period_time = sp.symbols("omega tau", positive=True)
    period = 2 * sp.pi / omega
    averaged_kernel_harmonic = sp.simplify(
        sp.integrate(sp.cos(2 * omega * period_time), (period_time, 0, period))
        / period
    )
    checks.check(
        "time-averaged kernel carries no nonzero temporal harmonic by itself",
        averaged_kernel_harmonic == 0
        and "time-averaged coupling kernel" in source_text,
    )
    checks.check(
        "internal source amplitude is absent from assigned power",
        "P_internal = (kappa_h / 4.0) * WB**2 * w_krad**2" in source_text
        and "internal_amplitude" not in loaded_names,
    )
    checks.check(
        "source numerical leg lacks evolved damping and solver-success gate",
        "solve_ivp(energy_rhs" in source_text
        and "sol.success" not in source_text
        and "Fself" not in source_text[source_text.index("def energy_rhs") : source_text.index("sol = solve_ivp")],
    )

    return checks.finish()


def _rejects_wrong_sign_damping(
    first_rate: sp.Expr,
    second_rate: sp.Expr,
    damping: sp.Expr,
) -> bool:
    try:
        rayleigh_dissipation(
            (first_rate, second_rate),
            sp.diag(damping, -damping),
        )
    except ValueError:
        return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", required=True)
    parser.add_argument("--dossier-file", required=True)
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_file, arguments.dossier_file))
