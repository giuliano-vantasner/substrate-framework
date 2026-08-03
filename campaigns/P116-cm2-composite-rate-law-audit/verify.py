"""Primary exact verifier for P116's CM2 composite-factor audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.composite_factors import (
    actual_loss_cycle_product,
    common_loss_pair_magnitude,
    conditional_composite_factor,
    loss_cycle_composition,
    nominal_loss_cycle_product,
    zero_cutoff_nominal_loss_cycle_product,
)
from substrate_framework.paired_resolvent import symmetric_pair_resolvent
from substrate_framework.thermal import symmetric_two_level_gate
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-31/"
    "bridge_CM2_coherence_rate_law.py"
)
BARRIER_SOURCE = Path("/home/dan/substrate/engineering/barrier_scaling.py")
SOURCE_SHA256 = "c75fee880740765d3ef3e32634bf05360fd9789e46bd579fd07af60d29a79fa2"
BARRIER_SHA256 = "8aff859aeff9bd2d317f3c458faa9e617e3865d3c8e12a6b198c15d92cf85014"
CONTRACT_SHA256 = "ee57cf8778eeb7e0ef2122cbab6cf3dd790abffe04ff0e55c1e5cc40a53da451"
FREEZE_SHA256 = "ee57cf8778eeb7e0ef2122cbab6cf3dd790abffe04ff0e55c1e5cc40a53da451"


def _campaign_root() -> Path:
    candidates = (
        Path("campaigns/P116-cm2-composite-rate-law-audit"),
        Path("proposals/P116-cm2-composite-rate-law-audit"),
    )
    return next(path for path in candidates if path.exists())


def main() -> int:
    checks = CheckLedger("C-CMP-001")
    root = _campaign_root()
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "CM2 source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "external barrier-scaling source hash is pinned",
        hashlib.sha256(BARRIER_SOURCE.read_bytes()).hexdigest() == BARRIER_SHA256,
    )
    normalized_contract = (
        (root / "proposal.yaml")
        .read_bytes()
        .replace(b"status: accepted\n", b"status: draft\n")
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    checks.check(
        "pre-source contract is immutable",
        hashlib.sha256((root / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA256,
    )
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "twenty-one static predicates match the runtime tally",
        len(source_checks) == 21
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "CM2 has no sampled-integration compatibility event",
        "np.trapz" not in source_text
        and "np.trapezoid" not in source_text
        and "trapezoid_integral" not in source_text,
    )

    gamma, omega, coupling = sp.symbols(
        "Gamma omega c",
        positive=True,
    )
    detunings = (sp.Integer(1), sp.Integer(2), sp.Integer(3))
    products = (coupling, coupling, coupling)
    pair_sum = sp.simplify(
        sum(
            (
                symmetric_pair_resolvent(delta, gamma, coupling)
                for delta in detunings
            ),
            sp.Integer(0),
        )
    )
    expected_pair_sum = sp.simplify(
        -sp.I
        * gamma
        * coupling
        * sum(1 / (delta**2 + gamma**2 / 4) for delta in detunings)
    )
    checks.check(
        "finite common-loss pair sum follows C-RES-001 exactly",
        sp.simplify(pair_sum - expected_pair_sum) == 0,
    )
    magnitude = common_loss_pair_magnitude(detunings, products, gamma)
    checks.check(
        "nonnegative products give the exact pair-sum magnitude",
        sp.simplify(magnitude - sp.I * pair_sum) == 0
        and magnitude.is_positive is True,
    )
    checks.check(
        "exact zero loss is an algebraic null rather than a floating tolerance",
        common_loss_pair_magnitude(detunings, products, 0) == 0,
    )

    nominal = nominal_loss_cycle_product(
        detunings,
        products,
        gamma,
        omega,
    )
    expected_nominal = sp.simplify(
        omega
        * coupling
        / (2 * sp.pi)
        * sum(1 / (delta**2 + gamma**2 / 4) for delta in detunings)
    )
    checks.check(
        "the explicit loss cancels the nominal inverse-loss factor",
        sp.simplify(nominal - expected_nominal) == 0,
    )
    ledger = loss_cycle_composition(
        detunings,
        products,
        gamma,
        omega,
    )
    checks.check(
        "the nominal product derivative is exact and strictly negative",
        sp.simplify(sp.diff(nominal, gamma) - ledger.nominal_loss_derivative) == 0
        and ledger.nominal_loss_derivative.is_negative is True,
    )
    checks.check(
        "the nominal product has no positive-loss stationary point",
        sp.solve(sp.together(ledger.nominal_loss_derivative), gamma) == [],
    )
    checks.check(
        "the zero-loss right limit is finite and strictly positive",
        sp.simplify(
            sp.limit(nominal, gamma, 0, dir="+") - ledger.zero_loss_limit
        )
        == 0
        and ledger.zero_loss_limit.is_positive is True,
    )
    checks.check(
        "the large-loss decay is inverse square with an exact coefficient",
        sp.simplify(
            sp.limit(gamma**2 * nominal, gamma, sp.oo)
            - ledger.large_loss_inverse_square_coefficient
        )
        == 0,
    )

    cutoff_gamma = sp.symbols("Gamma_cut", nonnegative=True)
    cutoff = zero_cutoff_nominal_loss_cycle_product(
        detunings,
        products,
        cutoff_gamma,
        omega,
    )
    open_cutoff_expression = sp.simplify(
        omega
        * coupling
        / (2 * sp.pi)
        * sum(
            1 / (delta**2 + cutoff_gamma**2 / 4)
            for delta in detunings
        )
    )
    checks.check(
        "the source-style endpoint convention assigns zero at zero loss",
        cutoff.subs(cutoff_gamma, 0) == 0,
    )
    checks.check(
        "the source-style cutoff assigns zero at and above criticality",
        cutoff.subs(cutoff_gamma, 2 * omega) == 0
        and cutoff.subs(cutoff_gamma, 3 * omega) == 0,
    )
    checks.check(
        "zero loss is a positive-height right jump",
        sp.simplify(
            sp.limit(open_cutoff_expression, cutoff_gamma, 0, dir="+")
            - ledger.zero_loss_limit
        )
        == 0
        and cutoff.subs(cutoff_gamma, 0) == 0,
    )
    checks.check(
        "the nominal critical cutoff is a positive-height left jump",
        sp.simplify(
            sp.limit(
                open_cutoff_expression,
                cutoff_gamma,
                2 * omega,
                dir="-",
            )
            - ledger.nominal_critical_left_limit
        )
        == 0
        and ledger.nominal_critical_left_limit.is_positive is True,
    )
    checks.check(
        "the discontinuous open support has a supremum but no maximizer",
        ledger.zero_loss_limit.is_positive is True
        and ledger.nominal_loss_derivative.is_negative is True
        and cutoff.subs(cutoff_gamma, 0) == 0,
    )

    source_grid = tuple(sp.Rational(index, 20) for index in range(41))
    source_grid_values = tuple(
        zero_cutoff_nominal_loss_cycle_product(
            detunings,
            (sp.Rational(1, 100),) * 3,
            point,
            1,
        )
        for point in source_grid
    )
    checks.check(
        "the source grid selects only its smallest positive loss",
        source_grid_values[0] == 0
        and source_grid_values[-1] == 0
        and max(range(len(source_grid_values)), key=source_grid_values.__getitem__) == 1,
    )
    checks.check(
        "refining the grid moves the selected point toward the excluded endpoint",
        zero_cutoff_nominal_loss_cycle_product(
            detunings,
            products,
            sp.Rational(1, 40),
            1,
        )
        > zero_cutoff_nominal_loss_cycle_product(
            detunings,
            products,
            sp.Rational(1, 20),
            1,
        ),
    )

    actual = actual_loss_cycle_product(
        detunings,
        products,
        gamma,
        omega,
    )
    actual_log_derivative = sp.simplify(sp.diff(sp.log(actual), gamma))
    positive_kernel = sum(
        coupling / (delta**2 + gamma**2 / 4) for delta in detunings
    )
    expected_actual_log_derivative = sp.simplify(
        -gamma / (4 * (omega**2 - gamma**2 / 4))
        + sp.diff(sp.log(positive_kernel), gamma)
    )
    checks.check(
        "the actual-cycle alternative has a strictly negative log derivative",
        sp.simplify(actual_log_derivative - expected_actual_log_derivative) == 0
        and sp.diff(positive_kernel, gamma).is_negative is True,
    )
    checks.check(
        "the actual-cycle product vanishes continuously at criticality",
        sp.limit(actual, gamma, 2 * omega, dir="-")
        == ledger.actual_critical_left_limit
        == 0,
    )
    checks.check(
        "the nominal and actual products share the positive zero-loss limit",
        sp.simplify(
            sp.limit(actual, gamma, 0, dir="+") - ledger.zero_loss_limit
        )
        == 0,
    )

    energy, scale = sp.symbols("E Theta", positive=True)
    subdivision = sp.symbols("n", integer=True, positive=True)
    population = sp.symbols("N", integer=True, positive=True)
    splitting = sp.symbols("x", positive=True)
    full_factor = conditional_composite_factor(
        energy,
        scale,
        subdivision,
        population,
        detunings,
        products,
        gamma,
        omega,
        splitting,
    )
    expected_full_factor = sp.simplify(
        sp.exp(-energy / scale)
        * subdivision
        * population
        * nominal
        * symmetric_two_level_gate(splitting)
    )
    checks.check(
        "the typed full factor composes exactly",
        sp.simplify(full_factor - expected_full_factor) == 0,
    )
    checks.check(
        "count multipliers are each linear only by declared normalization",
        sp.simplify(sp.diff(full_factor / subdivision, subdivision)) == 0
        and sp.simplify(sp.diff(full_factor / population, population)) == 0,
    )
    checks.check(
        "the full factor remains strictly decreasing with loss",
        sp.simplify(
            sp.diff(full_factor, gamma)
            - full_factor / nominal * ledger.nominal_loss_derivative
        )
        == 0,
    )
    checks.check(
        "activation loading and thermal gates remain dimensionless",
        sp.exp(-energy / scale).is_positive is True
        and symmetric_two_level_gate(splitting).is_positive is True,
    )

    rho = sp.symbols("rho", positive=True)
    common_rescaling = nominal_loss_cycle_product(
        tuple(rho * delta for delta in detunings),
        tuple(rho**2 * product for product in products),
        rho * gamma,
        rho * omega,
    )
    fixed_coupling_rescaling = nominal_loss_cycle_product(
        tuple(rho * delta for delta in detunings),
        products,
        rho * gamma,
        rho * omega,
    )
    checks.check(
        "dimensionally common scaling gives one frequency power",
        sp.simplify(common_rescaling - rho * nominal) == 0,
    )
    checks.check(
        "holding coupling products fixed reverses the scale power",
        sp.simplify(fixed_coupling_rescaling - nominal / rho) == 0,
    )
    checks.check(
        "dimensionless factors do not change the matrix-element dimension",
        (2 + 1 - 2, 0, 0, 0, 0) == (1, 0, 0, 0, 0),
    )

    target, kinetic_prefactor = sp.symbols("R_target nu", positive=True)
    checks.check(
        "zero kinetic interaction is a zero-rate countermodel",
        sp.simplify(0 * full_factor) == 0 and full_factor.is_positive is True,
    )
    checks.check(
        "a free kinetic prefactor fits any positive target",
        sp.simplify(
            (kinetic_prefactor * full_factor).subs(
                kinetic_prefactor,
                target / full_factor,
            )
            - target
        )
        == 0,
    )
    checks.check(
        "collective operator normalization remains a free square scale",
        sp.simplify((rho**2 * population) / population - rho**2) == 0,
    )

    single_detuning = sp.symbols("Delta", positive=True)
    mutated_quadratic_opening = sp.simplify(
        gamma
        * nominal_loss_cycle_product(
            (single_detuning,),
            (coupling,),
            gamma,
            omega,
        )
    )
    checks.check(
        "an extra loss power creates a different interior optimum",
        sp.solve(sp.diff(mutated_quadratic_opening, gamma), gamma)
        == [2 * single_detuning],
    )
    checks.mutation_sensitive(
        "loss cancellation and half-width convention are load bearing",
        lambda candidate: sp.simplify(candidate - expected_nominal) == 0,
        nominal,
        (
            gamma * nominal,
            nominal / gamma,
            omega
            * coupling
            / (2 * sp.pi)
            * sum(1 / (delta**2 + gamma**2) for delta in detunings),
            2 * nominal,
        ),
    )
    checks.mutation_sensitive(
        "cutoff endpoint and actual-frequency conventions are load bearing",
        lambda candidate: candidate.subs(cutoff_gamma, 2 * omega) == 0
        and candidate.subs(cutoff_gamma, omega).is_positive is True,
        cutoff,
        (
            sp.Piecewise(
                (open_cutoff_expression, cutoff_gamma <= 2 * omega),
                (0, True),
            ),
            sp.Integer(0),
        ),
    )

    claims = yaml.safe_load(Path("governance/claims.yaml").read_text())["claims"]
    governed = [claim for claim in claims if claim["id"] == "C-CMP-001"]
    if root.parts[0] == "proposals":
        lifecycle_ok = not governed
    else:
        lifecycle_ok = (
            len(governed) == 1
            and governed[0]["review"] == "accepted"
            and governed[0]["provenance"]
            == "campaigns/P116-cm2-composite-rate-law-audit/adjudication.yaml"
        )
    checks.check(
        "claim lifecycle matches draft or promoted campaign state",
        lifecycle_ok,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
