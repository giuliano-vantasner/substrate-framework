"""Primary exact verifier for P077 / provisional C-SYM-002."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.coupling_duality import (
    reciprocal_coefficient_for_fixed_target,
    reciprocal_coordinate_change_ledger,
    reciprocal_coupling_ledger,
)
from substrate_framework.scale_transmutation import (
    one_loop_inverse_energy_length_ledger,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-22/"
    "bridge_AS6_beta_self_dual_pin.py"
)
SOURCE_SHA256 = "2f6c76d8aedde25b343f85cb54b2618cd03c816a29553fa70a523909265dd7f0"
CONTRACT = Path(
    "campaigns/P077-as6-self-dual-coupling-audit/evidence/frozen-proposal.yaml"
)
CONTRACT_SHA256 = "56ae5926509fc4cf496ba1e153509d633cc9232d2b6d88bb5e3c8eac5779ec27"


def main() -> int:
    checks = CheckLedger("P077")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    checks.check(
        "source hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "candidate contract was frozen before source opening",
        hashlib.sha256(CONTRACT.read_bytes()).hexdigest() == CONTRACT_SHA256,
    )
    checks.check(
        "source has nine literal checks and a dynamic terminal tally",
        source_text.count("check(") == 10
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    canonical_text = Path(
        "src/substrate_framework/coupling_duality.py"
    ).read_text(encoding="utf-8")
    checks.check(
        "exact source and canonical route use no numpy quadrature alias",
        all(
            alias not in source_text and alias not in canonical_text
            for alias in ("np." + "trapz", "np." + "trapezoid")
        ),
    )

    x, coefficient = sp.symbols("x A", positive=True)
    generic = reciprocal_coupling_ledger(x, coefficient)
    checks.check(
        "general reciprocal map is exact",
        generic.dual_coordinate == coefficient / x,
    )
    checks.check(
        "general reciprocal map is an involution",
        generic.double_dual_coordinate == x,
    )
    checks.check(
        "general orbit product retains supplied coefficient",
        generic.orbit_product == coefficient,
    )
    checks.check(
        "general positive fixed coordinate is square root of coefficient",
        generic.positive_fixed_point == sp.sqrt(coefficient)
        and generic.fixed_point_residual == 0,
    )
    try:
        reciprocal_coupling_ledger(sp.Symbol("unassessed"), coefficient)
        positivity_rejected = False
    except ValueError:
        positivity_rejected = True
    checks.check(
        "omitting positive-domain evidence is rejected",
        positivity_rejected,
    )

    source_map = reciprocal_coupling_ledger(x, 16 * sp.pi**2)
    checks.check(
        "AS6 coefficient conditionally gives four pi",
        source_map.positive_fixed_point == 4 * sp.pi,
    )
    coefficient_mutation = reciprocal_coupling_ledger(x, 25 * sp.pi**2)
    checks.check(
        "coefficient mutation changes the fixed coordinate",
        coefficient_mutation.positive_fixed_point == 5 * sp.pi
        and coefficient_mutation.positive_fixed_point
        != source_map.positive_fixed_point,
    )

    target = sp.symbols("target", positive=True)
    target_coefficient = reciprocal_coefficient_for_fixed_target(target)
    target_map = reciprocal_coupling_ledger(target, target_coefficient)
    checks.check(
        "any positive target can be encoded as fixed",
        target_coefficient == target**2
        and target_map.dual_coordinate == target
        and target_map.positive_fixed_point == target,
    )
    checks.check(
        "arbitrary target remains a load-bearing inverse input",
        target_coefficient.has(target)
        and sp.diff(target_coefficient, target) == 2 * target,
    )

    off_fixed = reciprocal_coupling_ledger(2, 9)
    checks.check(
        "generic off-fixed point still has a valid dual orbit",
        off_fixed.dual_coordinate == sp.Rational(9, 2)
        and off_fixed.double_dual_coordinate == 2
        and off_fixed.orbit_product == 9,
    )
    checks.check(
        "duality orbit does not impose self-dual restriction",
        off_fixed.coupling_coordinate != off_fixed.positive_fixed_point
        and off_fixed.dual_coordinate != off_fixed.positive_fixed_point,
    )

    rho = sp.symbols("rho", positive=True)
    changed = reciprocal_coordinate_change_ledger(x, coefficient, rho)
    checks.check(
        "coordinate conjugation rescales map coefficient quadratically",
        changed.rescaled_coordinate == rho * x
        and changed.rescaled_duality_coefficient == rho**2 * coefficient
        and changed.coefficient_rescaling_ratio == rho**2,
    )
    checks.check(
        "coordinate conjugation commutes with the dual map",
        changed.rescaled_dual_coordinate
        == changed.conjugated_dual_coordinate
        == rho * coefficient / x,
    )
    checks.check(
        "numeric fixed coordinate rescales linearly",
        changed.rescaled_positive_fixed_point
        == changed.conjugated_positive_fixed_point
        and changed.fixed_point_rescaling_ratio == rho,
    )
    wrong_dual = sp.simplify(coefficient / changed.rescaled_coordinate)
    checks.check(
        "holding coefficient fixed fails generic coordinate conjugation",
        sp.simplify(wrong_dual - changed.conjugated_dual_coordinate) != 0,
    )

    phase_at_four_pi = sp.simplify(sp.exp(sp.I * 4 * sp.pi / 4))
    phase_at_twelve_pi = sp.simplify(sp.exp(sp.I * 12 * sp.pi / 4))
    checks.check(
        "source exchange phase evaluates to minus one at four pi",
        phase_at_four_pi == -1,
    )
    checks.check(
        "exchange phase does not uniquely select four pi",
        phase_at_twelve_pi == -1 and 12 * sp.pi != 4 * sp.pi,
    )

    mu0, conversion = sp.symbols("mu0 K", positive=True)
    length_map = one_loop_inverse_energy_length_ledger(
        mu0,
        4 * sp.pi,
        7,
        reference_conversion=conversion,
        transmuted_conversion=conversion,
    )
    checks.check(
        "conditional exponent substitution gives two pi over seven",
        length_map.exponent == 2 * sp.pi / 7,
    )
    checks.check(
        "accepted inverse-energy length orientation has positive exponent",
        length_map.transmuted_to_reference_length_ratio
        == sp.exp(2 * sp.pi / 7),
    )
    checks.check(
        "AS6 labels the opposite exponent as a over xi",
        "a_over_xi = sp.exp(-exponent_simpl)" in source_text
        and "a/xi = exp(-2pi/7)" in source_text,
    )
    b0 = sp.symbols("b0", positive=True)
    exponent = 8 * sp.pi**2 / (b0 * 4 * sp.pi)
    checks.check(
        "beta coefficient remains load bearing",
        sp.diff(exponent, b0) != 0
        and "b0_val = 7" in source_text,
    )

    checks.check(
        "AS6 provides no action or observable duality map",
        not any(
            token in source_text.lower()
            for token in (
                "lagrangian",
                "hamiltonian",
                "partition function",
                "observable map",
                "solution family",
            )
        ),
    )
    sine_gordon_text = Path(
        "src/substrate_framework/sine_gordon.py"
    ).read_text(encoding="utf-8")
    checks.check(
        "accepted sine-Gordon module declares beta one normalization",
        "c = m = beta = 1" in sine_gordon_text,
    )
    checks.check(
        "source imports physical duality by prose rather than a dependency",
        "SG / 2D-Coulomb-gas electric-magnetic (KT) duality" in source_text
        and "dual_partner = 16 * sp.pi**2 / beta2" in source_text,
    )
    checks.check(
        "source baryon analogy conflicts with accepted interpretation ceiling",
        "WZ3 topological=baryon" in source_text,
    )
    checks.check(
        "source itself records that fixed-point occupancy was later withdrawn",
        "NOTE (CORRECTION by AS7" in source_text
        and "framework does NOT sit there" in source_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
