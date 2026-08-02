"""Independent exact P076 derivation without the canonical provenance API."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-22/"
    "bridge_AS5_scale_generated_not_imported.py"
)
SOURCE_SHA256 = "7b2399f5fb61dad1ac692fb8a809e8a0429359b2264ee1b8a3899de504ab3bea"


def main() -> int:
    ledger = CheckLedger("P076-INDEPENDENT")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    ledger.check(
        "review reads immutable AS5 source",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )

    matrix = sp.Matrix([[0, 1], [1, 2], [-1, -1]])
    length = sp.Matrix([0, 1, 0])
    augmented = matrix.row_join(length)
    ledger.check("fresh c hbar rank is two", matrix.rank() == 2)
    ledger.check(
        "fresh length target is outside span",
        augmented.rank() == 3 and matrix.rank() < augmented.rank(),
    )
    ledger.check(
        "fresh c hbar target equations have no solution",
        sp.linsolve((matrix, length)) is sp.EmptySet,
    )
    with_length = augmented
    solution = with_length.inv() * length
    ledger.check(
        "fresh adjoined-length system is full rank",
        with_length.rank() == 3 and with_length.det() != 0,
    )
    ledger.check(
        "fresh adjoined-length solution only returns supplied target",
        solution == sp.Matrix([0, 0, 1]),
    )
    g_dimension = sp.Matrix([-1, 3, -2])
    ledger.check(
        "fresh G-dimension solve remains in full MLT span",
        with_length.inv() * g_dimension == sp.Matrix([3, -1, 2]),
    )

    mu0, g2, b0, conversion, rho = sp.symbols(
        "mu0 g2 b0 K rho", positive=True
    )
    exponent = 8 * sp.pi**2 / (b0 * g2)
    transmuted = mu0 * sp.exp(-exponent)
    length_value = conversion / transmuted
    ledger.check(
        "fresh transmuted scale contains dimensionful reference",
        transmuted.has(mu0) and sp.diff(transmuted, mu0) == sp.exp(-exponent),
    )
    ledger.check(
        "fresh inverse length contains reference and conversion",
        length_value.has(mu0, conversion)
        and sp.diff(length_value, mu0) != 0
        and sp.diff(length_value, conversion) != 0,
    )
    ledger.check(
        "fresh finite reference rescaling covariance",
        sp.simplify(transmuted.subs(mu0, rho * mu0) / transmuted) == rho
        and sp.simplify(length_value.subs(mu0, rho * mu0) / length_value)
        == 1 / rho,
    )
    ledger.check(
        "fresh ratio alone cancels reference",
        sp.simplify(transmuted / mu0) == sp.exp(-exponent)
        and not sp.simplify(transmuted / mu0).has(mu0),
    )

    target_energy, target_length = sp.symbols(
        "Lambda_target a_target", positive=True
    )
    reference_for_energy = target_energy * sp.exp(exponent)
    reference_for_length = conversion * sp.exp(exponent) / target_length
    ledger.check(
        "fresh arbitrary energy target reconstruction",
        sp.simplify(
            transmuted.subs(mu0, reference_for_energy) - target_energy
        )
        == 0,
    )
    ledger.check(
        "fresh arbitrary length target reconstruction",
        sp.simplify(
            length_value.subs(mu0, reference_for_length) - target_length
        )
        == 0,
    )
    ledger.check(
        "fresh inverse constructions expose target circularity",
        reference_for_energy.has(target_energy)
        and reference_for_length.has(target_length),
    )

    quantity, unit = sp.symbols("Q u", positive=True)
    coordinate = quantity / unit
    changed_coordinate = quantity / (rho * unit)
    ledger.check(
        "fresh unit coordinate transforms inversely",
        sp.simplify(changed_coordinate / coordinate) == 1 / rho,
    )
    ledger.check(
        "fresh unit transformation preserves quantity",
        sp.simplify(coordinate * unit - quantity) == 0
        and sp.simplify(changed_coordinate * rho * unit - quantity) == 0,
    )

    ledger.check(
        "fresh source audit finds omitted reference in no-import predicate",
        "Lambda_gen = mu0 *" in source_text
        and "not Lambda_gen.has(a_len) and not Lambda_gen.has(G)"
        in source_text,
    )
    ledger.check(
        "fresh source audit finds unused G span result",
        "G_not_in_span =" in source_text
        and "ellP_carries_G and ellP.has(hbar) and ellP.has(c0)"
        in source_text,
    )
    ledger.check(
        "fresh source audit finds reciprocal hierarchy label",
        "hierarchy = sp.exp(-8 * sp.pi**2 / (b0 * beta2))"
        in source_text
        and "a/xi -- a pure number" in source_text,
    )
    ledger.check(
        "fresh source guard inspects only a and beta2 numerics",
        "for s in (a_len, beta2)" in source_text,
    )
    ledger.check(
        "fresh source uses exact algebra and no numpy integration",
        "import numpy" not in source_text
        and "np." + "trapz" not in source_text
        and "np." + "trapezoid" not in source_text,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
