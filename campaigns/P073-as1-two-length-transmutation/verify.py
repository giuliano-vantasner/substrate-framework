"""Primary exact and regression verifier for P073 / C-RGE-003."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.scale_transmutation import (
    common_length_rescaling,
    coupling_squared_from_length_ratio,
    one_loop_inverse_energy_length_ledger,
    two_length_log_constraint,
    two_length_speed_dimension_ledger,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-21/"
    "bridge_AS1_two_length_transmutation.py"
)
SOURCE_SHA256 = "baca25e9b2b999088c1dc2969f9979cd341c582b3bdcfd009432db0eae9ea6cf"


def main() -> int:
    ledger = CheckLedger("P073")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    ledger.check(
        "source hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    ledger.check(
        "source has ten literal checks",
        source_text.count("check(") == 11
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    ledger.check(
        "source avoids numpy quadrature compatibility issue",
        "np.trapz" not in source_text and "np.trapezoid" not in source_text,
    )
    ledger.check(
        "source exposes later unaccepted annotations",
        "AS6" in source_text and "AS7" in source_text and "s_G" in source_text,
    )

    dimension = two_length_speed_dimension_ledger()
    ledger.check(
        "canonical dimension rows and primitive columns declared",
        dimension.dimension_matrix == sp.Matrix([[1, 1, 1], [0, 0, -1]]),
    )
    ledger.check(
        "two lengths and speed have rank two and one group",
        dimension.rank == 2 and dimension.dimensionless_group_count == 1,
    )
    kernel = dimension.monomial_kernel[0]
    ledger.check(
        "dimension kernel derives the length ratio",
        kernel == sp.Matrix([-1, 1, 0])
        and dimension.dimension_matrix * kernel == sp.zeros(2, 1),
    )
    ledger.check(
        "reciprocal kernel is equally dimensionless",
        dimension.dimension_matrix * (-kernel) == sp.zeros(2, 1),
    )
    source_dimension_matrix = sp.Matrix([[1, 0], [1, 0], [1, -1]])
    ledger.check(
        "source transposed matrix preserves rank but not canonical kernel orientation",
        source_dimension_matrix.rank() == dimension.rank
        and source_dimension_matrix.T == dimension.dimension_matrix,
    )
    ledger.check(
        "source ratio check does not derive its claimed kernel",
        "ratio_is_dimensionless = (dim(u.meter / u.meter) == {})" in source_text
        and "dim_matrix.nullspace" not in source_text,
    )

    mu0, g2, b0, conversion = sp.symbols("mu0 g2 b0 K", positive=True)
    exact = one_loop_inverse_energy_length_ledger(
        mu0,
        g2,
        b0,
        reference_conversion=conversion,
        transmuted_conversion=conversion,
    )
    exponent = 8 * sp.pi**2 / (b0 * g2)
    ledger.check("one-loop exponent is positive on declared domain", exact.exponent == exponent and exponent.is_positive)
    ledger.check(
        "formal transmutation energy ratio derived",
        exact.transmuted_to_reference_energy_ratio == sp.exp(-exponent),
    )
    ledger.check(
        "common inverse-energy length ratio derived",
        exact.transmuted_to_reference_length_ratio == sp.exp(exponent),
    )
    ledger.check(
        "energy and length ratios are exact reciprocals",
        sp.simplify(
            exact.transmuted_to_reference_energy_ratio
            * exact.transmuted_to_reference_length_ratio
            - 1
        )
        == 0,
    )
    ledger.check(
        "reference energy cancels only from the ratio",
        not exact.transmuted_to_reference_length_ratio.has(mu0)
        and exact.reference_length.has(mu0)
        and exact.transmuted_length.has(mu0),
    )

    ledger.check(
        "source executable swaps its opening UV and IR length names",
        "UV lattice length a" in source_text
        and "IR soliton length xi" in source_text
        and "xi_from_mu0 = hbar * c0 / mu0" in source_text
        and "a_from_Lam = hbar * c0 / Lambda_CF4" in source_text,
    )
    ledger.check(
        "source calls reciprocal representatives exactly equal",
        "it is exactly the Buckingham group xi/a of AS1.1" in source_text
        and "a_over_xi = sp.simplify(a_from_Lam / xi_from_mu0)" in source_text,
    )
    ledger.check(
        "source reciprocal oracle checks only symbol absence",
        "not a_over_xi.has(a_len) and not a_over_xi.has(xi)" in source_text,
    )

    k0, k1 = sp.symbols("K0 K1", positive=True)
    unequal = one_loop_inverse_energy_length_ledger(
        mu0,
        g2,
        b0,
        reference_conversion=k0,
        transmuted_conversion=k1,
    )
    ledger.check(
        "unequal conversion prefactor remains in length ratio",
        unequal.transmuted_to_reference_length_ratio
        == k1 * sp.exp(exponent) / k0,
    )
    ledger.check(
        "common-conversion mutation is load bearing",
        sp.simplify(
            unequal.transmuted_to_reference_energy_ratio
            * unequal.transmuted_to_reference_length_ratio
            - k1 / k0
        )
        == 0,
    )
    ledger.check(
        "beta coefficient remains a free ratio input",
        exact.transmuted_to_reference_length_ratio.has(b0)
        and sp.diff(exact.transmuted_to_reference_length_ratio, b0) != 0,
    )
    ledger.check(
        "coupling squared remains a free ratio input",
        exact.transmuted_to_reference_length_ratio.has(g2)
        and sp.diff(exact.transmuted_to_reference_length_ratio, g2) != 0,
    )
    ledger.check(
        "source claimed reduced expression still contains b0",
        "xi_reduced.free_symbols == {a_len, beta2, b0}" in source_text
        and "{a, beta^2}" in source_text,
    )

    ratio_symbol = sp.symbols("R", positive=True)
    constraint = two_length_log_constraint(
        ratio_symbol,
        provenance="conditional one-loop length ratio",
    )
    ledger.check(
        "one supplied ratio is one exact log row",
        constraint.design == sp.Matrix([[-1, 1]])
        and constraint.rhs == sp.Matrix([sp.log(ratio_symbol)]),
    )
    ledger.check(
        "ratio row leaves one common-scale null direction",
        constraint.linear.coefficient_rank == 1
        and constraint.linear.solution_dimension == 1
        and constraint.nullspace == (sp.ImmutableMatrix([1, 1]),),
    )
    ledger.check(
        "neither absolute length coordinate is identifiable",
        constraint.coordinate_identifiable == (False, False),
    )
    ell0, ell1, rho = sp.symbols("ell0 ell1 rho", positive=True)
    changed0, changed1, unchanged_ratio = common_length_rescaling(ell0, ell1, rho)
    ledger.check(
        "common length rescaling preserves the relative coordinate",
        unchanged_ratio == ell1 / ell0
        and sp.simplify(changed1 / changed0 - unchanged_ratio) == 0,
    )
    ledger.check(
        "absolute-scale prediction mutation rejected",
        changed0 != ell0 and changed1 != ell1 and unchanged_ratio == ell1 / ell0,
    )

    inferred = coupling_squared_from_length_ratio(ratio_symbol, b0)
    ledger.check(
        "coupling inverse is conditional on supplied ratio",
        inferred == 8 * sp.pi**2 / (b0 * sp.log(ratio_symbol))
        and inferred.has(ratio_symbol, b0),
    )
    ledger.check(
        "valid inverse round trip",
        sp.simplify(
            coupling_squared_from_length_ratio(sp.exp(exponent), b0) - g2
        )
        == 0,
    )
    for invalid_ratio in (sp.Rational(1, 2), sp.Integer(1)):
        try:
            coupling_squared_from_length_ratio(invalid_ratio, 7)
        except ValueError:
            rejected = True
        else:
            rejected = False
        ledger.check(f"inverse rejects nonpositive-log ratio {invalid_ratio}", rejected)
    ledger.check(
        "source inverse omits the R greater than one domain",
        "ratio_sym = sp.Symbol(\"R\", positive=True)" in source_text
        and "R > 1" not in source_text,
    )

    ledger.check(
        "weak-coupling formal length ratio diverges",
        sp.limit(exact.transmuted_to_reference_length_ratio, g2, 0, dir="+")
        == sp.oo,
    )
    ledger.check(
        "large-coupling formal length ratio tends to conversion ratio",
        sp.limit(unequal.transmuted_to_reference_length_ratio, g2, sp.oo)
        == k1 / k0,
    )
    ledger.check(
        "equal scale is a limit rather than finite positive input",
        sp.solve(sp.Eq(sp.exp(exponent), 1), g2) == [],
    )
    ledger.check(
        "source universal positivity guard samples one point",
        "exponent.subs({b0: 7, beta2: 1})" in source_text,
    )
    ledger.check(
        "source fixed-ratio guard proves dependence only",
        "real_ratio_depends_on_beta = (sp.diff(real_ratio, beta2) != 0)"
        in source_text,
    )
    ledger.check(
        "source physical closure has no accepted constructing equation",
        "closes S5 debt" in source_text
        and "lattice" in source_text
        and "soliton" in source_text
        and "Lambda_CF4" in source_text,
    )
    ledger.check(
        "canonical exact module avoids numpy quadrature aliases",
        "np.trapz"
        not in Path("src/substrate_framework/scale_transmutation.py").read_text(
            encoding="utf-8"
        )
        and "np.trapezoid"
        not in Path("src/substrate_framework/scale_transmutation.py").read_text(
            encoding="utf-8"
        ),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
