"""Primary exact verifier for P114's PN6 finite-pair-sum audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.paired_resolvent import (
    asymmetric_pair_resolvent,
    equal_pair_resolvent_sum,
    finite_resolvent_effective_block,
    symmetric_pair_resolvent,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-30/"
    "bridge_PN6_general_L_lossless_null.py"
)
SOURCE_SHA256 = "50ebbf97568fef13e69fc926db3e57457aba4685f3140ac8786bed525e71289f"
CONTRACT_SHA256 = "539ba98bb24b64c3a918a273632a0ef94948a7c5a69360a93aeda7d320016659"
FREEZE_SHA256 = "539ba98bb24b64c3a918a273632a0ef94948a7c5a69360a93aeda7d320016659"


def _campaign_root() -> Path:
    candidates = (
        Path("campaigns/P114-pn6-general-finite-pair-sum-audit"),
        Path("proposals/P114-pn6-general-finite-pair-sum-audit"),
    )
    return next(path for path in candidates if path.exists())


def _claim(claim_id: str) -> dict[str, object]:
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    return next(claim for claim in registry["claims"] if claim["id"] == claim_id)


def _direct_effective_entry(
    detunings: list[sp.Expr],
    losses: list[sp.Expr],
    products: list[sp.Expr],
) -> sp.Expr:
    energies: list[sp.Expr] = []
    expanded_products: list[sp.Expr] = []
    for delta, gamma, product in zip(detunings, losses, products):
        energies.extend((delta - sp.I * gamma / 2, -delta - sp.I * gamma / 2))
        expanded_products.extend((product, product))
    count = len(energies)
    to_intermediate = sp.Matrix([[1] * count, [0] * count])
    from_intermediate = sp.Matrix([[0, product] for product in expanded_products])
    effective = finite_resolvent_effective_block(
        sp.zeros(2),
        to_intermediate,
        sp.diag(*energies),
        from_intermediate,
    )
    return sp.factor(effective[0, 1])


def main() -> int:
    checks = CheckLedger("PN6-EXACT-AUDIT")
    root = _campaign_root()
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
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
        "thirty static sites execute thirty runtime predicates",
        len(source_checks) == 30
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source has no sampled-integration compatibility event",
        "np.trapz" not in source_text
        and "np.trapezoid" not in source_text
        and "np.integrate" not in source_text,
    )

    gamma = sp.symbols("Gamma", positive=True)
    detunings = [sp.Integer(1), sp.Integer(2), sp.Integer(5)]
    products = [sp.Integer(2), sp.Integer(3), sp.Integer(7)]
    exact_sum = sp.factor(
        sum(
            symmetric_pair_resolvent(delta, gamma, product)
            for delta, product in zip(detunings, products)
        )
    )
    expected_sum = sp.factor(
        -sp.I
        * gamma
        * sum(
            product / (delta**2 + gamma**2 / 4)
            for delta, product in zip(detunings, products)
        )
    )
    checks.check(
        "arbitrary finite equal-product pairs sum exactly",
        sp.simplify(exact_sum - expected_sum) == 0,
    )
    block_entry = _direct_effective_entry(
        detunings,
        [gamma] * len(detunings),
        products,
    )
    checks.check(
        "complete finite block inversion agrees with pairwise summation",
        sp.simplify(block_entry - exact_sum) == 0,
    )
    checks.mutation_sensitive(
        "resolvent orientation and common half-width are load bearing",
        lambda candidate: sp.simplify(candidate - exact_sum) == 0,
        block_entry,
        (-block_entry, block_entry.subs(gamma, 2 * gamma), sp.conjugate(block_entry)),
    )

    positive, negative, delta = sp.symbols("c_plus c_minus Delta")
    lossless_pair = asymmetric_pair_resolvent(
        sp.Integer(3), 0, positive, negative
    )
    checks.check(
        "lossless pair cancellation is exactly a matching-product condition",
        sp.simplify(lossless_pair - (negative - positive) / 3) == 0
        and sp.solve(sp.Eq(lossless_pair, 0), negative) == [positive],
    )
    pair_one = asymmetric_pair_resolvent(1, 0, 0, 1)
    pair_two = asymmetric_pair_resolvent(2, 0, 2, 0)
    checks.check(
        "full lossless cancellation need not occur pairwise",
        pair_one != 0 and pair_two != 0 and sp.simplify(pair_one + pair_two) == 0,
    )
    checks.check(
        "one unequal-product pair gives a nonzero lossless countermodel",
        asymmetric_pair_resolvent(3, 0, 2, 5) == 1,
    )

    c1, c2, c3 = sp.symbols("c1 c2 c3", nonnegative=True)
    denominators = [
        sp.Integer(1) + gamma**2 / 4,
        sp.Integer(4) + gamma**2 / 4,
        sp.Integer(25) + gamma**2 / 4,
    ]
    strict_sum = sum(
        product / denominator
        for product, denominator in zip((c1, c2, c3), denominators)
    )
    numerator = sp.cancel(strict_sum).as_numer_denom()[0]
    coefficient_ledger = sp.Poly(numerator, c1, c2, c3).coeffs()
    checks.check(
        "nonnegative-product strictness has necessary nontriviality",
        all(coefficient.is_positive is True for coefficient in coefficient_ledger)
        and sp.simplify(strict_sum.subs({c1: 0, c2: 0, c3: 0})) == 0,
    )
    checks.check(
        "at least one positive product makes the common-loss sum negative imaginary",
        sp.im(expected_sum).is_negative is True and sp.re(expected_sum) == 0,
    )
    checks.check(
        "all-zero couplings refute unrestricted strict nonvanishing",
        sp.simplify(
            sum(symmetric_pair_resolvent(d, gamma, 0) for d in detunings)
        )
        == 0,
    )
    checks.check(
        "negative real couplings remain nonnegative after squaring",
        (-sp.Integer(3)) ** 2 == 9
        and symmetric_pair_resolvent(2, gamma, (-sp.Integer(3)) ** 2)
        == symmetric_pair_resolvent(2, gamma, 9),
    )
    checks.check(
        "signed equal-detuning products can cancel at positive loss",
        sp.simplify(
            symmetric_pair_resolvent(2, gamma, 1)
            + symmetric_pair_resolvent(2, gamma, -1)
        )
        == 0,
    )
    complex_coupling = sp.I
    checks.check(
        "complex g squared can cancel while a Hermitian product cannot",
        sp.simplify(
            symmetric_pair_resolvent(2, gamma, 1**2)
            + symmetric_pair_resolvent(2, gamma, complex_coupling**2)
        )
        == 0
        and sp.simplify(
            symmetric_pair_resolvent(2, gamma, 1)
            + symmetric_pair_resolvent(
                2, gamma, sp.conjugate(complex_coupling) * complex_coupling
            )
        )
        != 0,
    )

    pair_losses = [sp.Rational(1, 2), sp.Rational(3, 2), sp.Integer(4)]
    nonuniform_sum = sum(
        symmetric_pair_resolvent(d, loss, product)
        for d, loss, product in zip(detunings, pair_losses, products)
    )
    checks.check(
        "pairwise shared nonuniform positive losses preserve the common sign",
        sp.re(nonuniform_sum) == 0 and sp.im(nonuniform_sum) < 0,
    )
    unequal_member_shifts = sp.factor(
        1 / (-1 + sp.I / 2) + 1 / (1 + 3 * sp.I / 2)
    )
    checks.check(
        "unequal shifts inside one pair break the pure-imaginary formula",
        sp.re(unequal_member_shifts) != 0,
    )
    checks.mutation_sensitive(
        "equal products within each lossless pair are load bearing",
        lambda pair_products: sp.simplify(
            asymmetric_pair_resolvent(2, 0, pair_products[0], pair_products[1])
        )
        == 0,
        (3, 3),
        ((3, 2), (0, 3), (3, sp.I)),
    )

    small_coefficient = sp.limit(exact_sum / gamma, gamma, 0, dir="+")
    large_coefficient = sp.limit(gamma * exact_sum, gamma, sp.oo)
    checks.check(
        "finite-sum small-loss coefficient is exact",
        sp.simplify(
            small_coefficient
            + sp.I * sum(c / d**2 for d, c in zip(detunings, products))
        )
        == 0,
    )
    checks.check(
        "finite-sum large-loss coefficient is exact",
        sp.simplify(large_coefficient + 4 * sp.I * sum(products)) == 0,
    )
    magnitude_sum = gamma * (
        1 / (1 + gamma**2 / 4) + 1 / (9 + gamma**2 / 4)
    )
    stationary = sp.factor(sp.diff(magnitude_sum, gamma))
    expected_stationary = sp.factor(
        (1 - gamma**2 / 4) / (1 + gamma**2 / 4) ** 2
        + (9 - gamma**2 / 4) / (9 + gamma**2 / 4) ** 2
    )
    checks.check(
        "finite-sum stationary equation is the sum of pair derivatives",
        sp.simplify(stationary - expected_stationary) == 0,
    )
    checks.check(
        "unequal detunings do not inherit either one-pair optimum",
        stationary.subs(gamma, 2) > 0
        and stationary.subs(gamma, 6) < 0,
    )

    one_pair = symmetric_pair_resolvent(2, gamma, 5)
    checks.check(
        "fixed-per-pair and fixed-total size conventions separate",
        sp.simplify(
            equal_pair_resolvent_sum(4, 2, gamma, 5, scaling="fixed_per_pair")
            - 4 * one_pair
        )
        == 0
        and sp.simplify(
            equal_pair_resolvent_sum(4, 2, gamma, 5, scaling="fixed_sum")
            - one_pair
        )
        == 0,
    )
    build_model = next(
        node
        for node in source_tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "build_model_re"
    )
    build_model_text = ast.get_source_segment(source_text, build_model) or ""
    checks.check(
        "source changes finite model size rather than numerical resolution",
        "dim = 2 + 2 * Lv" in build_model_text
        and "np.zeros((dim, dim)" in build_model_text
        and "for Lv in L_LIST" in source_text
        and "np.linalg.inv" in source_text
        and not any(
            isinstance(node, ast.Name) and node.id in {"dx", "dt", "mesh", "timestep"}
            for node in ast.walk(source_tree)
        ),
    )

    ladder_scale = sp.symbols("Delta0", positive=True)
    ladder_loss = sp.symbols("Gamma_p", positive=True)
    ladder_count = sp.symbols("L", integer=True, positive=True)
    x = sp.I * ladder_loss / (2 * ladder_scale)

    def ladder_closed(count: sp.Expr) -> sp.Expr:
        return (
            sp.digamma(count + 1 - x)
            - sp.digamma(1 - x)
            - sp.digamma(count + 1 + x)
            + sp.digamma(1 + x)
        ) / (2 * x * ladder_scale**2)

    ladder_term = lambda count: 1 / (
        ladder_scale**2 * count**2 + ladder_loss**2 / 4
    )
    checks.check(
        "uniform-ladder digamma base and recurrence are exact",
        sp.simplify(sp.expand_func(ladder_closed(1)) - ladder_term(1)) == 0
        and sp.simplify(
            sp.expand_func(ladder_closed(ladder_count + 1) - ladder_closed(ladder_count))
            - ladder_term(ladder_count + 1)
        )
        == 0,
    )
    checks.check(
        "digamma route is a uniform-ladder specialization",
        "Delta_j = Delta0*j" in source_text and "G[j]: gr" in source_text,
    )
    checks.check(
        "source strictness proof narrows arbitrary couplings to positive symbols",
        "Delta, gc = sp.symbols('Delta g', positive=True)" in source_text
        and "Dr, gr = sp.symbols('Delta_r g_r', positive=True)" in source_text
        and "Gp * gc**2 * term_u(1)" in source_text,
    )
    checks.check(
        "seven source block sizes are regression rather than independent proof",
        "L_LIST = (1, 2, 3, 4, 6, 8, 11)" in source_text
        and "rtol 1e-12" in source_text,
    )

    predicate_audit = yaml.safe_load(
        (root / "evidence/check-adjudication.yaml").read_text()
    )
    checks.check(
        "all thirty source predicates have individual verdicts",
        predicate_audit["runtime_predicate_count"] == 30
        and len(predicate_audit["predicates"]) == 30
        and all(
            item["verdict"] in {"retained", "qualified", "duplicate", "rejected"}
            for item in predicate_audit["predicates"]
        ),
    )
    dependency = yaml.safe_load((root / "evidence/dependency-audit.yaml").read_text())
    checks.check(
        "pending source dependencies supply no premise",
        dependency["dependency_closure"]
        == "existing_C_RES_001_finite_block_ceiling_only"
        and all(
            item["authority"] == "none"
            for item in dependency["source_dependencies"]
            if item["id"] in {"LB2", "S1", "S2", "S3", "S4", "S5"}
        ),
    )
    consumers = yaml.safe_load((root / "evidence/consumer-audit.yaml").read_text())
    checks.check(
        "source dependency graph has an empty PN6 consumer closure",
        consumers["consumers"] == []
        and consumers["closure"]["direct_count"] == 0
        and consumers["closure"]["indirect_count"] == 0,
    )
    claim_statement = str(_claim("C-RES-001")["statement"])
    normalized_claim_statement = claim_statement.lower()
    checks.check(
        "accepted finite-block claim already owns PN6's exact algebra and ceiling",
        all(
            phrase in normalized_claim_statement
            for phrase in (
                "finite square complex intermediate block",
                "c_plus=c_minus",
                "changing l is model enlargement",
                "transition rate",
            )
        ),
    )
    checks.check(
        "nonduplication reserves no claim or canonical API",
        yaml.safe_load((root / "proposal.yaml").read_text())["claims_proposed"] == []
        and not any(
            claim["id"] == "C-RES-002"
            for claim in yaml.safe_load(Path("governance/claims.yaml").read_text())["claims"]
        ),
    )
    checks.check(
        "exact campaign work uses no quadrature solver fitted comparator or np.trapz",
        not exact_sum.has(sp.Float, sp.Integral),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
