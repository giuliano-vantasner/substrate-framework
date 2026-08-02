"""Primary exact verifier for P076 / provisional C-DIM-008."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.dimensional_analysis import monomial_exponents
from substrate_framework.scale_provenance import (
    one_loop_scale_provenance_ledger,
    reference_energy_for_target_inverse_length,
    reference_energy_for_target_transmuted_energy,
    speed_action_length_dimension_ledger,
    unit_coordinate_ledger,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-22/"
    "bridge_AS5_scale_generated_not_imported.py"
)
SOURCE_SHA256 = "7b2399f5fb61dad1ac692fb8a809e8a0429359b2264ee1b8a3899de504ab3bea"


def main() -> int:
    ledger = CheckLedger("P076")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    ledger.check(
        "source hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    ledger.check(
        "source has six literal checks and dynamic tally",
        source_text.count("check(") == 7
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    ledger.check(
        "source and canonical route avoid numpy quadrature aliases",
        all(
            alias not in source_text
            and alias
            not in Path("src/substrate_framework/scale_provenance.py").read_text(
                encoding="utf-8"
            )
            for alias in ("np." + "trapz", "np." + "trapezoid")
        ),
    )

    dimension = speed_action_length_dimension_ledger()
    ledger.check(
        "canonical MLT rows and c hbar columns are explicit",
        dimension.base_dimensions == ("M", "L", "T")
        and dimension.primitive_names == ("c", "hbar")
        and dimension.primitive_dimension_matrix
        == sp.Matrix([[0, 1], [1, 2], [-1, -1]]),
    )
    ledger.check(
        "c and hbar coefficient rank is two",
        dimension.without_length.coefficient_rank == 2,
    )
    ledger.check(
        "pure length target raises augmented rank",
        dimension.without_length.augmented_rank == 3
        and not dimension.without_length.consistent,
    )
    ledger.check(
        "adjoining the target length gives a unique solve",
        dimension.with_length.coefficient_rank == 3
        and dimension.with_length.augmented_rank == 3
        and dimension.with_length.unique,
    )
    ledger.check(
        "adjoined target solve only selects supplied a",
        dimension.with_length_exponents == sp.Matrix([0, 0, 1]),
    )
    ledger.check(
        "removing a breaks target membership",
        not dimension.without_length.consistent
        and dimension.with_length.consistent,
    )
    source_matrix = sp.Matrix([[0, 1, -1], [1, 2, -1], [0, 1, 0]])
    ledger.check(
        "source primitive-row convention is canonical transpose",
        source_matrix.T == dimension.with_length_dimension_matrix,
    )
    g_dimension = sp.Matrix([-1, 3, -2])
    g_exponents = monomial_exponents(
        dimension.with_length_dimension_matrix,
        g_dimension,
    )
    ledger.check(
        "G dimension is in full MLT span with retained coefficient",
        g_exponents == sp.Matrix([3, -1, 2]),
    )
    ledger.check(
        "source G span variables do not enter its check predicate",
        "G_not_in_span = (rank_prim == 3 and rank_prim_plus_G == 3)"
        in source_text
        and "ellP_carries_G and ellP.has(hbar) and ellP.has(c0)"
        in source_text,
    )

    mu0, g2, b0, conversion, rho = sp.symbols(
        "mu0 g2 b0 K rho", positive=True
    )
    exact = one_loop_scale_provenance_ledger(
        mu0,
        g2,
        b0,
        conversion=conversion,
        reference_rescaling=rho,
    )
    exponent = 8 * sp.pi**2 / (b0 * g2)
    ledger.check(
        "formal transmuted energy retains reference",
        exact.transmuted_energy == mu0 * sp.exp(-exponent)
        and exact.transmuted_energy.has(mu0),
    )
    ledger.check(
        "inverse-energy length retains reference and conversion",
        exact.inverse_energy_length == conversion * sp.exp(exponent) / mu0
        and exact.inverse_energy_length.has(mu0, conversion),
    )
    ledger.check(
        "only formal energy ratio cancels reference",
        exact.transmuted_to_reference_energy_ratio == sp.exp(-exponent)
        and not exact.transmuted_to_reference_energy_ratio.has(mu0),
    )
    ledger.check(
        "finite reference rescaling is exact",
        exact.rescaled_reference_energy == rho * mu0
        and exact.transmuted_energy_rescaling_ratio == rho
        and exact.inverse_length_rescaling_ratio == 1 / rho,
    )
    ledger.check(
        "reference mutation changes both absolute outputs",
        exact.rescaled_transmuted_energy != exact.transmuted_energy
        and exact.rescaled_inverse_energy_length != exact.inverse_energy_length,
    )
    ledger.check(
        "dimensionless flow inputs remain load bearing",
        sp.diff(exact.transmuted_energy, g2) != 0
        and sp.diff(exact.transmuted_energy, b0) != 0,
    )
    ledger.check(
        "reference and conversion inputs remain load bearing",
        sp.diff(exact.transmuted_energy, mu0) != 0
        and sp.diff(exact.inverse_energy_length, conversion) != 0,
    )

    energy_target = sp.symbols("Lambda_target", positive=True)
    target_reference = reference_energy_for_target_transmuted_energy(
        energy_target,
        g2,
        b0,
    )
    energy_roundtrip = one_loop_scale_provenance_ledger(
        target_reference,
        g2,
        b0,
        conversion=conversion,
        reference_rescaling=rho,
    )
    ledger.check(
        "arbitrary positive energy target can be reconstructed",
        sp.simplify(energy_roundtrip.transmuted_energy - energy_target) == 0,
    )
    ledger.check(
        "energy target is a load-bearing inverse input",
        target_reference.has(energy_target)
        and sp.diff(target_reference, energy_target) != 0,
    )

    length_target = sp.symbols("a_target", positive=True)
    length_reference = reference_energy_for_target_inverse_length(
        length_target,
        g2,
        b0,
        conversion=conversion,
    )
    length_roundtrip = one_loop_scale_provenance_ledger(
        length_reference,
        g2,
        b0,
        conversion=conversion,
        reference_rescaling=rho,
    )
    ledger.check(
        "arbitrary positive length target can be reconstructed",
        sp.simplify(length_roundtrip.inverse_energy_length - length_target)
        == 0,
    )
    ledger.check(
        "length target is a load-bearing inverse input",
        length_reference.has(length_target)
        and sp.diff(length_reference, length_target) != 0,
    )

    quantity, unit = sp.symbols("Q u", positive=True)
    coordinate = unit_coordinate_ledger(quantity, unit, rho)
    ledger.check(
        "unit coordinate rescales inversely",
        coordinate.coordinate == quantity / unit
        and coordinate.rescaled_coordinate == quantity / (rho * unit)
        and coordinate.coordinate_rescaling_ratio == 1 / rho,
    )
    ledger.check(
        "both coordinates reconstruct one fixed quantity",
        sp.simplify(coordinate.coordinate * coordinate.unit_standard - quantity)
        == 0
        and sp.simplify(
            coordinate.rescaled_coordinate
            * coordinate.rescaled_unit_standard
            - quantity
        )
        == 0,
    )
    ledger.check(
        "unit choice does not remove physical quantity input",
        coordinate.coordinate.has(quantity)
        and coordinate.rescaled_coordinate.has(quantity),
    )

    beta2, a_symbol, g_symbol = sp.symbols(
        "beta2 a G", positive=True
    )
    source_generation_predicate = lambda expression: (
        expression.has(beta2)
        and expression.has(b0)
        and not expression.has(a_symbol)
        and not expression.has(g_symbol)
    )
    wrong_scale = mu0 * b0 * beta2
    ledger.check(
        "source generation predicate accepts a nontransmutation mutant",
        source_generation_predicate(wrong_scale),
    )
    ledger.check(
        "source generation predicate never excludes mu0",
        "not Lambda_gen.has(a_len) and not Lambda_gen.has(G)" in source_text
        and "not Lambda_gen.has(mu0)" not in source_text,
    )

    source_hierarchy_predicate = lambda expression: (
        expression.has(beta2)
        and not expression.has(a_symbol)
        and not expression.has(sp.Symbol("hbar"))
        and not expression.has(sp.Symbol("c0"))
        and not expression.has(g_symbol)
    )
    ledger.check(
        "source hierarchy predicate accepts either reciprocal orientation",
        source_hierarchy_predicate(sp.exp(exponent.subs(g2, beta2)))
        and source_hierarchy_predicate(sp.exp(-exponent.subs(g2, beta2))),
    )
    ledger.check(
        "source labels inverse-energy hierarchy with wrong sign",
        "hierarchy = sp.exp(-8 * sp.pi**2 / (b0 * beta2))"
        in source_text
        and "a/xi -- a pure number" in source_text,
    )
    ledger.check(
        "canonical inverse-energy orientation is opposite source label",
        exact.inverse_energy_length
        == conversion / exact.transmuted_energy
        and exact.inverse_energy_length
        != conversion
        * exact.transmuted_to_reference_energy_ratio
        / mu0,
    )
    ledger.check(
        "free-symbol guard is not a no-fit provenance proof",
        "isinstance(s, sp.Symbol)" in source_text
        and "for s in (a_len, beta2)" in source_text
        and "mu0" not in source_text.split("for s in (a_len, beta2)")[0].split(
            "no_numeric ="
        )[-1],
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
