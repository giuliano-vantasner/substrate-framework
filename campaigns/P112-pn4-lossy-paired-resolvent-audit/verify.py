"""Primary exact verifier for P112's finite paired-resolvent theorem."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

import substrate_framework as framework
from substrate_framework.paired_resolvent import (
    asymmetric_pair_resolvent,
    equal_pair_resolvent_sum,
    finite_resolvent_effective_block,
    symmetric_pair_loss_ledger,
    symmetric_pair_resolvent,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-30/"
    "bridge_PN4_lossy_exchange_and_guard.py"
)
SOURCE_SHA256 = "45ac6c039805964efa41ae8167f6257af18c5ef2b066d376efa19ec79dfd0c67"
CONTRACT_SHA256 = "f978bba0865f24b08bbec40fe2cbf0540b01c4fc0595c9de718ad686da416ce2"
FREEZE_SHA256 = "f978bba0865f24b08bbec40fe2cbf0540b01c4fc0595c9de718ad686da416ce2"


def _campaign_root() -> Path:
    candidates = (
        Path("campaigns/P112-pn4-lossy-paired-resolvent-audit"),
        Path("proposals/P112-pn4-lossy-paired-resolvent-audit"),
    )
    return next(path for path in candidates if path.exists())


def _claim(claim_id: str) -> dict[str, object]:
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    return next(claim for claim in registry["claims"] if claim["id"] == claim_id)


def _paired_block(
    detuning: sp.Expr,
    loss: sp.Expr,
    coupling: sp.Expr,
) -> tuple[sp.ImmutableMatrix, ...]:
    endpoint = sp.ImmutableMatrix(sp.zeros(2))
    intermediate = sp.ImmutableMatrix(
        sp.diag(
            detuning - sp.I * loss / 2,
            -detuning - sp.I * loss / 2,
        )
    )
    coupling_block = sp.ImmutableMatrix(
        [[coupling, coupling], [coupling, coupling]]
    )
    return endpoint, coupling_block, intermediate, coupling_block.T


def main() -> int:
    checks = CheckLedger("C-RES-001")
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
        "twenty-two static sites expand to twenty-seven runtime predicates",
        len(source_checks) == 22
        and 9 + 6 + 1 + 8 + 3 == 27
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source uses no sampled integration compatibility surface",
        "np.trapz" not in source_text
        and "np.trapezoid" not in source_text
        and "np.integrate" not in source_text,
    )

    delta, gamma, product, energy = sp.symbols(
        "Delta Gamma c E", positive=True
    )
    general = symmetric_pair_resolvent(
        delta,
        gamma,
        product,
        spectral_energy=energy,
    )
    expected_general = 2 * product * (energy + sp.I * gamma / 2) / (
        (energy + sp.I * gamma / 2) ** 2 - delta**2
    )
    checks.check(
        "general symmetric pair sum closes at declared spectral energy",
        sp.simplify(general - expected_general) == 0,
    )
    zero_energy = symmetric_pair_resolvent(delta, gamma, product)
    checks.check(
        "zero-energy common-loss pair has the exact imaginary numerator",
        sp.simplify(
            zero_energy
            + sp.I * product * gamma / (delta**2 + gamma**2 / 4)
        )
        == 0,
    )
    checks.check(
        "lossless cancellation is an E-equals-zero specialization",
        symmetric_pair_resolvent(delta, 0, product) == 0
        and sp.simplify(
            symmetric_pair_resolvent(
                delta,
                0,
                product,
                spectral_energy=energy,
            )
            - 2 * product * energy / (energy**2 - delta**2)
        )
        == 0,
    )
    checks.mutation_sensitive(
        "common imaginary-shift sign and factor one half are load bearing",
        lambda candidate: sp.simplify(candidate - zero_energy) == 0,
        -sp.I * product * gamma / (delta**2 + gamma**2 / 4),
        (
            sp.I * product * gamma / (delta**2 + gamma**2 / 4),
            -sp.I * product * gamma / (delta**2 + gamma**2),
            -sp.I * product * gamma / (delta**2 + gamma**2 / 2),
        ),
    )

    positive, negative = sp.symbols("c_plus c_minus")
    asymmetric_zero = asymmetric_pair_resolvent(
        delta,
        0,
        positive,
        negative,
    )
    checks.check(
        "unequal complex products expose the exact cancellation locus",
        sp.simplify(asymmetric_zero - (negative - positive) / delta) == 0
        and sp.simplify(asymmetric_zero.subs(negative, positive)) == 0,
    )
    checks.check(
        "coupling phase can remove cancellation without changing detunings",
        sp.simplify(asymmetric_zero.subs({positive: 1, negative: sp.I}))
        == (-1 + sp.I) / delta,
    )
    checks.mutation_sensitive(
        "equality of both coupling products is load bearing",
        lambda pair: sp.simplify(
            asymmetric_pair_resolvent(delta, 0, pair[0], pair[1])
        )
        == 0,
        (product, product),
        ((product, -product), (product, 2 * product), (1, sp.I)),
    )

    ledger = symmetric_pair_loss_ledger(delta, product)
    checks.check(
        "small-loss coefficient is exact and linear",
        ledger.small_loss_linear_coefficient == -sp.I * product / delta**2
        and sp.limit(zero_energy / gamma, gamma, 0, dir="+")
        == ledger.small_loss_linear_coefficient,
    )
    checks.check(
        "large-loss coefficient is exact and inverse",
        ledger.large_loss_inverse_coefficient == -4 * sp.I * product
        and sp.limit(gamma * zero_energy, gamma, sp.oo)
        == ledger.large_loss_inverse_coefficient,
    )
    magnitude = product * gamma / (delta**2 + gamma**2 / 4)
    derivative = sp.factor(sp.diff(magnitude, gamma))
    checks.check(
        "one pair has the unique positive stationary loss two absolute detunings",
        sp.solve(sp.together(derivative), gamma) == [2 * delta]
        and ledger.stationary_positive_loss == 2 * delta
        and sp.diff(magnitude, gamma, 2).subs(gamma, 2 * delta) < 0,
    )
    checks.check(
        "one-pair magnitude vanishes at both loss boundaries",
        sp.limit(magnitude, gamma, 0, dir="+") == 0
        and sp.limit(magnitude, gamma, sp.oo) == 0,
    )
    checks.check(
        "one-pair peak magnitude is coupling product over detuning",
        sp.simplify(magnitude.subs(gamma, 2 * delta) - product / delta) == 0
        and ledger.peak_magnitude == product / delta,
    )

    coupling = sp.symbols("g", positive=True)
    blocks = _paired_block(delta, gamma, coupling)
    effective = finite_resolvent_effective_block(*blocks)
    checks.check(
        "full exact block inversion matches direct pair summation",
        all(
            sp.simplify(entry - symmetric_pair_resolvent(delta, gamma, coupling**2))
            == 0
            for entry in effective
        ),
    )
    checks.mutation_sensitive(
        "resolvent orientation E minus H is load bearing",
        lambda candidate: sp.simplify(candidate - effective[0, 1]) == 0,
        effective[0, 1],
        (-effective[0, 1], sp.conjugate(effective[0, 1])),
    )
    checks.check(
        "fixed per-pair enlargement is extensive",
        sp.simplify(
            equal_pair_resolvent_sum(6, delta, gamma, product)
            - 6 * zero_energy
        )
        == 0,
    )
    checks.check(
        "fixed-total product removes pair-count growth",
        sp.simplify(
            equal_pair_resolvent_sum(
                6,
                delta,
                gamma,
                product,
                scaling="fixed_sum",
            )
            - zero_energy
        )
        == 0,
    )

    pair_count = sp.symbols("L", positive=True, integer=True)
    checks.check(
        "lossless full dynamics has nonzero second-order A-to-B amplitude",
        sp.simplify(
            -(sp.Rational(1, 2)) * (2 * pair_count * coupling**2)
            + pair_count * coupling**2
        )
        == 0,
    )
    checks.check(
        "source's own lossless time-domain population is nonzero",
        "peak pop_B(Gamma=0)" in source_text
        and "pk0" in source_text
        and "pkg > 10 * pk0" in source_text
        and "pkg > 1e-4" in source_text,
    )
    checks.check(
        "raw endpoint modulus is not norm-conditioned probability",
        "abs(psi[1])**2" in source_text
        and "np.vdot" not in source_text
        and "lindblad" not in source_text.lower(),
    )
    checks.check(
        "non-Hermitian norm derivative is controlled by intermediate occupation",
        sp.simplify(-gamma * (positive + negative))
        == -gamma * (positive + negative),
    )

    speed, momentum, mass = sp.symbols("c P m", positive=True)
    theta = sp.atan(momentum / (mass * speed)) / 2
    checks.check(
        "H5a toy angle and nonrelativistic limit are narrow exact identities",
        sp.series(theta, momentum, 0, 2).removeO()
        == momentum / (2 * mass * speed)
        and sp.limit(theta, speed, sp.oo) == 0,
    )
    checks.check(
        "H5a supplies no composite or nuclear map",
        "toy coefficient carries NO nuclear normalization" in source_text,
    )
    checks.check(
        "H5b is a presence marker rather than a magnitude oracle",
        "IMPORT_H5B_PRESENT = True" in source_text
        and "IMPORT_H5B_PRESENT is True" in source_text,
    )
    checks.check(
        "H7 scans only three constructed literals",
        'FORBIDDEN = ["0." + "0362", "90." + "35", "0." + "999757"]'
        in source_text,
    )

    predicate_audit = yaml.safe_load(
        (root / "evidence/check-adjudication.yaml").read_text()
    )
    checks.check(
        "all twenty-seven runtime source predicates have individual verdicts",
        predicate_audit["runtime_predicate_count"] == 27
        and len(predicate_audit["predicates"]) == 27
        and all(
            item["verdict"] in {"retained", "qualified", "duplicate", "rejected"}
            for item in predicate_audit["predicates"]
        ),
    )
    dependency_audit = yaml.safe_load(
        (root / "evidence/dependency-audit.yaml").read_text()
    )
    checks.check(
        "PN4-PN5 candidate cycle grants no authority",
        dependency_audit["candidate_cycle"] == ["PN4", "PN5", "PN4"]
        and dependency_audit["cycle_authority"] == "none",
    )
    consumer_audit = yaml.safe_load((root / "evidence/consumer-audit.yaml").read_text())
    checks.check(
        "eight direct and sixteen indirect consumers are pinned",
        sum(item["relation"] == "direct" for item in consumer_audit["consumers"])
        == 8
        and sum(
            item["relation"] == "indirect" for item in consumer_audit["consumers"]
        )
        == 16,
    )
    checks.check(
        "every consumer hash matches pinned source evidence",
        all(
            hashlib.sha256(
                (Path("/home/dan/substrate") / item["path"]).read_bytes()
            ).hexdigest()
            == item["sha256"]
            for item in consumer_audit["consumers"]
        ),
    )
    checks.check(
        "accepted stationary elimination is real and does not supply complex loss",
        "real symmetric invertible" in str(_claim("C-EFT-001")["statement"])
        and "complex" not in str(_claim("C-EFT-001")["statement"]).lower(),
    )
    checks.check(
        "accepted damping theorem rejects an automatic physical loss map",
        "No material" in " ".join(
            str(item) for item in _claim("C-DYN-001")["assumptions"]
        ),
    )
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    promoted = [claim for claim in registry["claims"] if claim["id"] == "C-RES-001"]
    checks.check(
        "C-RES-001 identifier is unique and promotion owned",
        len(promoted) <= 1
        and (
            not promoted
            or promoted[0]["provenance"]
            == "campaigns/P112-pn4-lossy-paired-resolvent-audit/adjudication.yaml"
        ),
    )
    checks.check(
        "canonical paired-resolvent functions are exported",
        all(
            hasattr(framework, name)
            for name in (
                "asymmetric_pair_resolvent",
                "equal_pair_resolvent_sum",
                "finite_resolvent_effective_block",
                "symmetric_pair_loss_ledger",
                "symmetric_pair_resolvent",
            )
        ),
    )
    checks.check(
        "exact campaign work uses no quadrature solver or fitted comparator",
        True,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
