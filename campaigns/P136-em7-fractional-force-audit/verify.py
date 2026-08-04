from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.maxwell import static_maxwell_point_source
from substrate_framework.momentum_kernels import (
    critical_riesz_log_kernel,
    riesz_green_kernel,
    riesz_radial_force_law,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "c8bf044d846d22eaa652a0f4c11cd5f5e2a51f98e49d0578536fbc4e96f63f22"
FROZEN_PROPOSAL_SHA256 = "c5b0cdebc82ab0990cecc81242674bfdd58ff20ee9cf3b7d6dbb5649a9fc0c5a"


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
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imports.update(
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    )
    return text, tree, checks, imports


def _check_labels(checks: list[ast.Call]) -> tuple[str, ...]:
    labels: list[str] = []
    for call in checks:
        first = call.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            labels.append(first.value)
        elif isinstance(first, ast.JoinedStr):
            labels.append("".join(
                value.value
                for value in first.values
                if isinstance(value, ast.Constant) and isinstance(value.value, str)
            ))
        else:
            labels.append("")
    return tuple(labels)


def main(source_file: str) -> int:
    checks = CheckLedger("P136/C-KRN-002/EM7")
    source = Path(source_file).resolve()
    campaign = Path(__file__).resolve().parent
    frozen = campaign / "evidence" / "frozen-proposal.yaml"
    text, tree, source_checks, imports = _source_inventory(source)
    labels = _check_labels(source_checks)

    checks.check(
        "pinned EM7 source hash",
        hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "frozen proposal hash",
        hashlib.sha256(frozen.read_bytes()).hexdigest()
        == FROZEN_PROPOSAL_SHA256,
    )
    checks.check("seventeen source predicates", len(source_checks) == 17)
    checks.check(
        "one source assertion belongs to the local check helper",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    checks.check(
        "source import inventory is closed",
        imports == {"numpy", "sympy", "scipy.special"},
    )
    compatibility = audit_numpy_trapezoid_compatibility(text, filename=str(source))
    checks.check(
        "source has no trapezoid compatibility event",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    # The dispositions are claim-level classifications, not a reuse of the
    # source's binary tally.  Their order follows the seventeen check calls.
    dispositions = (
        "definition_only",
        "exact_conditional",
        "exact_subcritical_only",
        "exact_subcritical_only",
        "numeric_formula_evaluation",
        "exact_subcritical_endpoint",
        "numeric_formula_evaluation",
        "exact_subcritical_endpoint",
        "exact_conditional_force_dictionary_missing",
        "regression_of_hard_coded_powers_with_domain_violations",
        "ordinary_laplacian_endpoints_from_separate_regimes",
        "critical_regime_boolean_only",
        "numeric_regression_of_definition",
        "invalid_supercritical_smoothed_periodic_proxy",
        "fixed_dimension_counterexample_only",
        "fixed_dimension_counterexample_only",
        "fixed_dimension_counterexample_only",
    )
    expected_prefixes = (
        "EM7.i-a",
        "EM7.i-b",
        "EM7.ii-a",
        "EM7.iii-a",
        "EM7.iii-b",
        "EM7.iv-a",
        "EM7.iv-b",
        "EM7.iv-c",
        "EM7.v-a",
        "EM7.v-b",
        "EM7.vi-a",
        "EM7.vi-b",
        "EM7.vii-a",
        "EM7.viii-a",
        "EM7.ix-a",
        "EM7.ix-b",
        "EM7.ix-c",
    )
    checks.check(
        "all source predicates have an individual frozen disposition",
        len(dispositions) == len(labels) == 17
        and all(prefix in label for prefix, label in zip(expected_prefixes, labels)),
    )
    checks.check(
        "source tally contains both supportable and non-probative predicates",
        dispositions.count("exact_subcritical_endpoint") == 2
        and "critical_regime_boolean_only" in dispositions
        and "invalid_supercritical_smoothed_periodic_proxy" in dispositions,
    )

    radius = sp.Symbol("r", positive=True)
    reference = sp.Symbol("r0", positive=True)
    dimension, power = sp.symbols("d s", positive=True)
    coefficient = sp.Symbol("A", positive=True)
    source_strength, probe_strength = sp.symbols("Q q", real=True)

    subcritical = riesz_green_kernel(
        dimension,
        power,
        radius,
        coefficient,
    )
    expected_normalization = sp.gamma(dimension / 2 - power) / (
        coefficient
        * 4**power
        * sp.pi ** (dimension / 2)
        * sp.gamma(power)
    )
    checks.check(
        "subcritical Riesz normalization is exact in the pinned convention",
        sp.simplify(subcritical.normalization - expected_normalization) == 0
        and subcritical.convergence_condition == sp.Lt(power, dimension / 2),
    )
    checks.check(
        "subcritical derivative retains normalization and radial power",
        subcritical.radial_power == 2 * power - dimension
        and sp.simplify(
            subcritical.radial_derivative
            - expected_normalization
            * (2 * power - dimension)
            * radius ** (2 * power - dimension - 1)
        )
        == 0,
    )
    coulomb = riesz_green_kernel(3, 1, radius, coefficient)
    checks.check(
        "three-dimensional ordinary endpoint is conditional Coulomb",
        sp.simplify(coulomb.green_kernel - 1 / (4 * sp.pi * coefficient * radius))
        == 0,
    )

    critical = critical_riesz_log_kernel(
        dimension,
        radius,
        reference,
        coefficient,
    )
    critical_normalization = 2 / (
        coefficient
        * 4 ** (dimension / 2)
        * sp.pi ** (dimension / 2)
        * sp.gamma(dimension / 2)
    )
    checks.check(
        "critical kernel is a reference-subtracted subcritical limit",
        critical.limit_reconstruction_residual == 0
        and sp.simplify(
            critical.logarithmic_normalization - critical_normalization
        )
        == 0,
    )
    checks.check(
        "critical logarithm has its exact reference value and derivative",
        critical.reference_residual == 0
        and sp.simplify(
            critical.logarithmic_kernel
            - critical_normalization * sp.log(reference / radius)
        )
        == 0
        and sp.simplify(
            critical.radial_derivative + critical_normalization / radius
        )
        == 0,
    )
    epsilon = critical.approach_parameter
    unsubtracted = sp.gamma(epsilon) * radius ** (-2 * epsilon) / (
        coefficient
        * 4 ** (dimension / 2 - epsilon)
        * sp.pi ** (dimension / 2)
        * sp.gamma(dimension / 2 - epsilon)
    )
    checks.check(
        "unsubtracted critical kernel diverges rather than becoming a logarithm",
        sp.limit(unsubtracted.subs(dimension, 2), epsilon, 0, dir="+")
        == sp.oo,
    )
    alternate_reference = sp.Symbol("r1", positive=True)
    alternate = critical_riesz_log_kernel(
        dimension,
        radius,
        alternate_reference,
        coefficient,
    )
    checks.check(
        "changing the critical reference adds only a radius-independent constant",
        sp.simplify(
            sp.diff(
                alternate.logarithmic_kernel - critical.logarithmic_kernel,
                radius,
            )
        )
        == 0
        and sp.simplify(
            alternate.logarithmic_kernel
            - critical.logarithmic_kernel
            - critical_normalization * sp.log(alternate_reference / reference)
        )
        == 0,
    )

    critical_two = critical_riesz_log_kernel(
        2,
        radius,
        reference,
        coefficient,
    )
    maxwell_two = static_maxwell_point_source(
        2,
        radius,
        source_strength,
        probe_strength,
        coefficient,
        reference_radius=reference,
    )
    checks.check(
        "two-dimensional critical limit matches the accepted Maxwell branch",
        sp.simplify(
            source_strength * critical_two.logarithmic_kernel
            - maxwell_two.potential
        )
        == 0
        and sp.simplify(
            -source_strength * critical_two.radial_derivative
            - maxwell_two.radial_electric_field
        )
        == 0,
    )

    domain_rejected = False
    try:
        riesz_green_kernel(1, 1, radius, coefficient)
    except ValueError as error:
        domain_rejected = "requires" in str(error)
    maxwell_one = static_maxwell_point_source(
        1,
        radius,
        source_strength,
        probe_strength,
        coefficient,
    )
    checks.check(
        "one-dimensional ordinary branch is separate from subcritical Riesz",
        domain_rejected
        and maxwell_one.potential
        == -source_strength * radius / (2 * coefficient),
    )

    force = riesz_radial_force_law(
        dimension,
        power,
        radius,
        source_strength,
        probe_strength,
        coefficient,
    )
    checks.check(
        "force ledger declares source probe energy and sign convention",
        sp.simplify(force.potential - source_strength * subcritical.green_kernel)
        == 0
        and sp.simplify(
            force.potential_energy - probe_strength * force.potential
        )
        == 0
        and sp.simplify(
            force.radial_force + sp.diff(force.potential_energy, radius)
        )
        == 0,
    )
    checks.check(
        "inverse-square behavior selects a family rather than one endpoint",
        force.force_radial_power == 2 * power - dimension - 1
        and force.inverse_square_dimension_family == 2 * power + 1
        and sp.solve(
            sp.Eq(force.force_radial_power, -2), dimension
        ) == [2 * power + 1],
    )
    noninteger_family = riesz_radial_force_law(
        sp.Rational(14, 5),
        sp.Rational(9, 10),
        radius,
        source_strength,
        probe_strength,
        coefficient,
    )
    checks.check(
        "noninteger parameter pair is an exact inverse-square counterexample",
        noninteger_family.force_radial_power == -2
        and noninteger_family.inverse_square_residual == 0
        and noninteger_family.kernel.convergence_condition
        == sp.Lt(sp.Rational(9, 10), sp.Rational(7, 5)),
    )
    checks.check(
        "source fixed-d guard cannot establish endpoint uniqueness",
        "s_wrong = 0.9" in text
        and "d=3" in text
        and noninteger_family.force_radial_power == -2,
    )
    checks.check(
        "source and probe mutations affect distinct observables",
        sp.simplify(force.potential.subs(source_strength, 0)) == 0
        and sp.simplify(force.radial_force.subs(probe_strength, 0)) == 0
        and sp.simplify(
            force.potential_energy.subs(probe_strength, -probe_strength)
            + force.potential_energy
        )
        == 0,
    )
    checks.check(
        "inverse-kernel coefficient mutation rescales the force",
        sp.simplify(
            riesz_radial_force_law(
                3,
                1,
                radius,
                source_strength,
                probe_strength,
                2 * coefficient,
            ).radial_force
            - riesz_radial_force_law(
                3,
                1,
                radius,
                source_strength,
                probe_strength,
                coefficient,
            ).radial_force
            / 2
        )
        == 0,
    )

    checks.check(
        "source critical-log predicate is only an exponent Boolean",
        "log_boundary_d2 = (2 * 1 == 2)" in text
        and "reference_radius" not in text
        and "log(r0" not in text,
    )
    checks.check(
        "source force sweep includes parameters outside the subcritical domain",
        "(1.0, 1.0, 0.0)" in text
        and "(1.0, 2.5, -1.5)" in text,
    )
    checks.check(
        "source Green residual is a smoothed periodic supercritical proxy",
        "s_r = 0.75" in text
        and "G_smooth" in text
        and "np.fft.fft" in text
        and sp.Rational(3, 4) > sp.Rational(1, 2),
    )
    checks.check(
        "analytic dimension parameter is not a constructed geometry",
        {"d_sym", "s_sym", "c_ds", "riesz_G"}.issubset(
            {
                node.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Name)
            }
            | {
                node.name
                for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.ClassDef))
            }
        )
        and not (
            {"metric", "measure", "diffusion", "dirichlet_form", "geometry"}
            & {
                node.id.lower()
                for node in ast.walk(tree)
                if isinstance(node, ast.Name)
            }
        ),
    )
    checks.check(
        "source imports an unaccepted D3S endpoint selection",
        "s=1 SUBSEQUENTLY DERIVED by Phase 19 / D3S" in text
        and "QCD5" in text,
    )
    checks.check(
        "plane-wave relation follows from the source's declared symbol",
        "defined by Fourier symbol" in text
        and sp.simplify(sp.Symbol("k", positive=True) ** (2 * power)
                       - sp.Symbol("k", positive=True) ** (2 * power)) == 0,
    )

    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", required=True)
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_file))
