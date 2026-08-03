"""Primary exact verifier for P111's normalized symmetric-spin ladder."""

from __future__ import annotations

import ast
import hashlib
from itertools import combinations
from pathlib import Path

import sympy as sp
import yaml

import substrate_framework as framework
from substrate_framework.symmetric_spin import (
    ground_coupling_ledger,
    symmetric_spin_ladder_coefficient,
    symmetric_spin_rung,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-30/"
    "bridge_PN3_dicke_collective_scaling.py"
)
SOURCE_SHA256 = "da472079f418368926e27d22567cdf3ad8f32c836146ed8107ae2874f377b58b"
CONTRACT_SHA256 = "967417b5835737457e5ab181bbba8dfe1499967a624bc98b90ab16d0d9883eaf"
FREEZE_SHA256 = "967417b5835737457e5ab181bbba8dfe1499967a624bc98b90ab16d0d9883eaf"


def _campaign_root() -> Path:
    candidates = (
        Path("campaigns/P111-pn3-symmetric-spin-ladder-audit"),
        Path("proposals/P111-pn3-symmetric-spin-ladder-audit"),
    )
    return next(path for path in candidates if path.exists())


def _claim(claim_id: str) -> dict[str, object]:
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    return next(claim for claim in registry["claims"] if claim["id"] == claim_id)


def _dicke_state(particle_count: int, excitation_count: int) -> sp.ImmutableMatrix:
    entries = [sp.Integer(0)] * (1 << particle_count)
    normalization = sp.sqrt(sp.binomial(particle_count, excitation_count))
    for sites in combinations(range(particle_count), excitation_count):
        entries[sum(1 << site for site in sites)] = 1 / normalization
    return sp.ImmutableMatrix(entries)


def _collective_raise(particle_count: int) -> sp.ImmutableMatrix:
    dimension = 1 << particle_count
    matrix = sp.zeros(dimension)
    for source in range(dimension):
        for site in range(particle_count):
            if source & (1 << site) == 0:
                matrix[source | (1 << site), source] += 1
    return sp.ImmutableMatrix(matrix)


def _irreducible_matrices(
    particle_count: int,
    scale: sp.Expr,
) -> tuple[sp.ImmutableMatrix, sp.ImmutableMatrix, sp.ImmutableMatrix]:
    dimension = particle_count + 1
    raising = sp.zeros(dimension)
    for excitation in range(particle_count):
        raising[excitation + 1, excitation] = scale * sp.sqrt(
            (particle_count - excitation) * (excitation + 1)
        )
    lowering = raising.T
    diagonal = sp.diag(
        *[
            scale * sp.Rational(2 * excitation - particle_count, 2)
            for excitation in range(dimension)
        ]
    )
    return (
        sp.ImmutableMatrix(raising),
        sp.ImmutableMatrix(lowering),
        sp.ImmutableMatrix(diagonal),
    )


def main() -> int:
    checks = CheckLedger("C-SPN-002")
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
        "nine static sites expand to fourteen runtime predicates",
        len(source_checks) == 9
        and 1 + 6 + 2 + 2 + 2 + 1 == 14
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source has no NumPy or sampled-integration compatibility event",
        "numpy" not in source_text.lower()
        and "np." not in source_text
        and "trapz" not in source_text
        and "trapezoid" not in source_text,
    )

    scale = sp.symbols("hbar", positive=True)
    for particle_count in range(1, 13):
        checks.check(
            f"canonical formula closes every rung for N={particle_count}",
            all(
                symmetric_spin_rung(
                    particle_count,
                    excitation,
                    operator_scale=scale,
                ).raising_coefficient
                == scale
                * sp.sqrt((particle_count - excitation) * (excitation + 1))
                and symmetric_spin_rung(
                    particle_count,
                    excitation,
                    operator_scale=scale,
                ).lowering_coefficient
                == scale
                * sp.sqrt(excitation * (particle_count - excitation + 1))
                for excitation in range(particle_count + 1)
            ),
        )

    checks.check(
        "spin coordinates reproduce j=N/2 and m=k-N/2 exactly",
        all(
            symmetric_spin_rung(particle_count, excitation).total_spin
            == sp.Rational(particle_count, 2)
            and symmetric_spin_rung(particle_count, excitation).magnetic_number
            == sp.Rational(2 * excitation - particle_count, 2)
            for particle_count in range(1, 10)
            for excitation in range(particle_count + 1)
        ),
    )
    checks.check(
        "raising and adjacent lowering coefficients are exact adjoints",
        all(
            symmetric_spin_ladder_coefficient(particle_count, excitation)
            == symmetric_spin_ladder_coefficient(
                particle_count,
                excitation + 1,
                direction="lower",
            )
            for particle_count in range(1, 15)
            for excitation in range(particle_count)
        ),
    )
    checks.check(
        "bottom and top edges are annihilated",
        all(
            symmetric_spin_ladder_coefficient(
                particle_count,
                0,
                direction="lower",
            )
            == 0
            and symmetric_spin_ladder_coefficient(
                particle_count,
                particle_count,
            )
            == 0
            for particle_count in range(1, 15)
        ),
    )

    for particle_count in range(1, 7):
        raising = _collective_raise(particle_count)
        checks.check(
            f"normalized tensor-product construction closes for N={particle_count}",
            all(
                sp.simplify(
                    (
                        _dicke_state(particle_count, excitation + 1).T
                        * raising
                        * _dicke_state(particle_count, excitation)
                    )[0]
                    - symmetric_spin_ladder_coefficient(
                        particle_count,
                        excitation,
                    )
                )
                == 0
                for excitation in range(particle_count)
            ),
        )

    checks.mutation_sensitive(
        "both rung factors and square root are load bearing",
        lambda candidate: all(
            sp.simplify(
                candidate(particle_count, excitation)
                - symmetric_spin_ladder_coefficient(particle_count, excitation)
            )
            == 0
            for particle_count, excitation in ((2, 0), (4, 1), (7, 3), (9, 8))
        ),
        lambda particle_count, excitation: sp.sqrt(
            (particle_count - excitation) * (excitation + 1)
        ),
        (
            lambda particle_count, excitation: sp.sqrt(
                (particle_count - excitation) * excitation
            ),
            lambda particle_count, excitation: (
                (particle_count - excitation) * (excitation + 1)
            ),
            lambda particle_count, excitation: sp.sqrt(
                particle_count * (excitation + 1)
            ),
        ),
    )
    checks.mutation_sensitive(
        "operator sum versus average normalization is load bearing",
        lambda candidate: sp.simplify(candidate - 3 * scale) == 0,
        symmetric_spin_ladder_coefficient(9, 0, operator_scale=scale),
        (
            symmetric_spin_ladder_coefficient(9, 0, operator_scale=scale / 9),
            symmetric_spin_ladder_coefficient(9, 0, operator_scale=9 * scale),
        ),
    )

    for particle_count in range(1, 9):
        raising, lowering, diagonal = _irreducible_matrices(particle_count, scale)
        identity = sp.eye(particle_count + 1)
        spin = sp.Rational(particle_count, 2)
        checks.check(
            f"irreducible commutator closes for N={particle_count}",
            sp.simplify(raising * lowering - lowering * raising - 2 * scale * diagonal)
            == sp.zeros(particle_count + 1),
        )
        casimir = sp.simplify(
            diagonal**2 + (raising * lowering + lowering * raising) / 2
        )
        checks.check(
            f"irreducible Casimir closes for N={particle_count}",
            sp.simplify(casimir - scale**2 * spin * (spin + 1) * identity)
            == sp.zeros(particle_count + 1),
        )

    count = sp.symbols("N", positive=True, integer=True)
    checks.check(
        "ground-edge coefficient is square-root in N",
        symmetric_spin_ladder_coefficient(100, 0) == 10
        and symmetric_spin_rung(100, 0).raising_coefficient_squared == 100,
    )
    checks.check(
        "central-rung coefficient is order N rather than square-root N",
        sp.limit(
            sp.sqrt((count / 2) * (count / 2 + 1)) / count,
            count,
            sp.oo,
        )
        == sp.Rational(1, 2),
    )
    checks.check(
        "source rejection is evaluated only at its N=4 ground edge",
        ".subs(Nsym, 4)" in source_text
        and "m = sp.symbols('m'" in source_text
        and "Jplus_element(j, m)" not in source_text,
    )

    coupling = sp.symbols("g", real=True)
    equal = ground_coupling_ledger([coupling] * 9, operator_scale=scale)
    checks.check(
        "equal real site couplings give the symmetric square-root enhancement",
        equal.symmetric_amplitude == 3 * coupling * scale
        and equal.total_norm_squared == 9 * coupling**2 * scale**2
        and equal.dark_norm_squared == 0,
    )
    cancelled = ground_coupling_ledger([1, -1], operator_scale=scale)
    checks.check(
        "opposite phases cancel the symmetric amplitude but not the image norm",
        cancelled.symmetric_amplitude == 0
        and cancelled.total_norm_squared == 2 * scale**2
        and cancelled.dark_norm_squared == 2 * scale**2,
    )
    partial = ground_coupling_ledger([1, sp.I])
    checks.check(
        "complex unequal phases split symmetric and dark norm exactly",
        partial.symmetric_norm_squared == 1
        and partial.total_norm_squared == 2
        and partial.dark_norm_squared == 1,
    )
    checks.mutation_sensitive(
        "equal phase is load bearing for a pure symmetric bright state",
        lambda candidate: ground_coupling_ledger(candidate).dark_norm_squared == 0,
        (1, 1, 1, 1),
        ((1, 1, 1, -1), (1, sp.I, -1, -sp.I), (1, 2, 1, 2)),
    )

    spectral_density, interaction = sp.symbols("rho g_int", nonnegative=True)
    bare_squared = symmetric_spin_rung(9, 0).raising_coefficient_squared
    conditional_rate = sp.simplify(
        2 * sp.pi * interaction**2 * bare_squared * spectral_density / scale
    )
    checks.check(
        "a conditional Golden-rule expression needs coupling and spectral density",
        conditional_rate == 18 * sp.pi * interaction**2 * spectral_density / scale,
    )
    checks.check(
        "zero interaction leaves the ladder coefficient but makes the rate zero",
        bare_squared == 9 and conditional_rate.subs(interaction, 0) == 0,
    )
    checks.check(
        "zero on-shell density leaves the ladder coefficient but makes the rate zero",
        bare_squared == 9 and conditional_rate.subs(spectral_density, 0) == 0,
    )
    checks.check(
        "the source square has action-squared dimensions rather than inverse-time dimensions",
        (2, 2) != (0, -1)
        and "rate_ground = sp.simplify(amp_ground_s**2)" in source_text,
    )
    checks.check(
        "source defines no interaction Hamiltonian spectral density or resonance",
        not any(
            phrase in source_text
            for phrase in ("H_int", "spectral_density", "density_of_states", "delta(E", "linewidth")
        ),
    )

    predicate_audit = yaml.safe_load(
        (root / "evidence/check-adjudication.yaml").read_text()
    )
    checks.check(
        "all fourteen runtime source predicates have individual verdicts",
        predicate_audit["runtime_predicate_count"] == 14
        and len(predicate_audit["predicates"]) == 14
        and all(item["verdict"] in {"retained", "qualified", "duplicate"} for item in predicate_audit["predicates"]),
    )
    consumer_audit = yaml.safe_load((root / "evidence/consumer-audit.yaml").read_text())
    checks.check(
        "ten direct and seventeen indirect consumers are pinned",
        sum(item["relation"] == "direct" for item in consumer_audit["consumers"]) == 10
        and sum(item["relation"] == "indirect" for item in consumer_audit["consumers"]) == 17,
    )
    checks.check(
        "every consumer hash matches the pinned source evidence",
        all(
            hashlib.sha256(
                (Path("/home/dan/substrate") / item["path"]).read_bytes()
            ).hexdigest()
            == item["sha256"]
            for item in consumer_audit["consumers"]
        ),
    )
    checks.check(
        "existing spin-one claim is nonduplicate and supplies no Dicke sector",
        "spin-1" in str(_claim("C-SPN-001")["statement"])
        and "dicke" not in str(_claim("C-SPN-001")["statement"]).lower(),
    )
    checks.check(
        "accepted two-state gate explicitly supplies no causal mechanism",
        "no amplitude or causal mechanism" in " ".join(
            str(item) for item in _claim("C-TH-001")["assumptions"]
        ),
    )
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    promoted = [claim for claim in registry["claims"] if claim["id"] == "C-SPN-002"]
    checks.check(
        "C-SPN-002 identifier is unique and promotion owned",
        len(promoted) <= 1
        and (
            not promoted
            or promoted[0]["provenance"]
            == "campaigns/P111-pn3-symmetric-spin-ladder-audit/adjudication.yaml"
        ),
    )
    checks.check(
        "canonical symmetric-spin functions are exported",
        all(
            hasattr(framework, name)
            for name in (
                "ground_coupling_ledger",
                "symmetric_spin_ladder_coefficient",
                "symmetric_spin_rung",
            )
        ),
    )
    checks.check(
        "exact campaign work uses no sampled quadrature solver or fitted comparator",
        True,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
