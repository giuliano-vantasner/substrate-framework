#!/usr/bin/env python3
"""Independent raw-SymPy rederivation for C-VAC-004.

This review deliberately does not import the canonical scale-matching,
scale-transmutation, or vacuum-polarization modules.
"""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P187-INDEPENDENT-C-VAC-004")
    this_file = Path(__file__)
    tree = ast.parse(this_file.read_text(encoding="utf-8"), filename=str(this_file))
    imported_modules = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    forbidden = {
        "substrate_framework.kinetic_scale_matching",
        "substrate_framework.scale_transmutation",
        "substrate_framework.vacuum_polarization",
    }
    checks.check(
        "review is independent of canonical and parent claim APIs",
        imported_modules.isdisjoint(forbidden),
    )

    ell0, ell1, k0, k1 = sp.symbols("ell0 ell1 K0 K1", positive=True)
    energy0 = sp.factor(k0 / ell0)
    energy1 = sp.factor(k1 / ell1)
    length_ratio = sp.factor(ell1 / ell0)
    conversion_ratio = sp.factor(k1 / k0)
    energy_ratio = sp.factor(energy0 / energy1)
    checks.check(
        "raw inverse-length energy ratio retains conversions",
        sp.cancel(energy_ratio - length_ratio / conversion_ratio) == 0
        and energy_ratio.has(k0, k1, ell0, ell1),
    )

    scale_log = sp.log(energy_ratio)
    local, finite = sp.symbols("Z_local c_fin", real=True)
    scalar, dirac = sp.symbols("W_s W_f", nonnegative=True)
    coefficient = sp.factor(scalar / 3 + 4 * dirac / 3)
    affine = sp.factor(
        local + finite + coefficient * scale_log / (8 * sp.pi**2)
    )
    checks.check(
        "raw affine family retains both boundary coordinates",
        affine.has(local, finite, scalar, dirac, ell0, ell1, k0, k1)
        and sp.diff(affine, local) == 1
        and sp.diff(affine, finite) == 1,
    )
    formal_energy1 = sp.Symbol("E1_formal", positive=True)
    formal_affine = (
        local
        + finite
        + coefficient * sp.log(energy0 / formal_energy1) / (8 * sp.pi**2)
    )
    checks.check(
        "raw affine scale derivative has the declared slope",
        sp.simplify(
            formal_energy1 * sp.diff(formal_affine, formal_energy1)
            + coefficient / (8 * sp.pi**2)
        )
        == 0,
    )

    changed_k0 = sp.simplify(
        sp.log((2 * k0) * ell1 / (k1 * ell0)) - scale_log
    )
    changed_k1 = sp.simplify(
        sp.log(k0 * ell1 / ((3 * k1) * ell0)) - scale_log
    )
    checks.check(
        "fixed-length conversion mutations are load-bearing",
        changed_k0 == sp.log(2) and changed_k1 == -sp.log(3),
    )
    delta = sp.Symbol("delta_Z", nonzero=True, real=True)
    checks.check(
        "same scale data admit unequal affine boundaries",
        sp.simplify((affine + delta) - affine - delta) == 0
        and sp.simplify(
            sp.diff(affine + delta, ell1) - sp.diff(affine, ell1)
        )
        == 0,
    )

    rho = sp.Symbol("rho", positive=True)
    rescaled_energy0 = sp.factor(k0 / (rho * ell0))
    rescaled_energy1 = sp.factor(k1 / (rho * ell1))
    checks.check(
        "common length rescaling preserves ratio but shifts energies",
        sp.cancel(rescaled_energy0 / rescaled_energy1 - energy_ratio) == 0
        and rescaled_energy0 == energy0 / rho
        and rescaled_energy1 == energy1 / rho,
    )

    mu0, g2, b0 = sp.symbols("mu0 g2 b0", positive=True)
    exponent = sp.factor(8 * sp.pi**2 / (b0 * g2))
    transmuted = sp.factor(mu0 * sp.exp(-exponent))
    paired_ell0 = sp.factor(k0 / mu0)
    paired_ell1 = sp.factor(k1 / transmuted)
    paired_length_ratio = sp.factor(paired_ell1 / paired_ell0)
    checks.check(
        "raw one-loop paired length ratio is exact",
        sp.cancel(
            paired_length_ratio - (k1 / k0) * sp.exp(exponent)
        )
        == 0,
    )
    paired_energy_ratio = sp.cancel(
        (k0 / paired_ell0) / (k1 / paired_ell1)
    )
    paired_log = sp.simplify(sp.log(paired_energy_ratio))
    checks.check(
        "unequal paired conversions cancel without equality premise",
        paired_energy_ratio == sp.exp(exponent)
        and paired_log == exponent
        and k0 != k1,
    )

    positive_scalar, positive_dirac = sp.symbols("Wsp Wfp", positive=True)
    positive_coefficient = sp.factor(positive_scalar / 3 + 4 * positive_dirac / 3)
    composed = sp.factor(
        local
        + finite
        + positive_coefficient * paired_log / (8 * sp.pi**2)
    )
    expected_general = sp.factor(
        local + finite + positive_coefficient / (b0 * g2)
    )
    checks.check(
        "raw general one-loop composition retains Z_ref",
        sp.cancel(composed - expected_general) == 0
        and composed.has(local, finite),
    )
    zero_branch = sp.factor(composed.subs({local: 0, finite: 0}))
    inverse_branch = sp.factor(1 / zero_branch)
    checks.check(
        "raw zero branch and inverse coordinate are exact",
        sp.cancel(zero_branch - positive_coefficient / (b0 * g2)) == 0
        and sp.cancel(inverse_branch - b0 * g2 / positive_coefficient) == 0
        and inverse_branch.is_positive is True,
    )
    checks.check(
        "zero branch does not represent the general family",
        sp.cancel(composed - zero_branch - local - finite) == 0
        and composed != zero_branch,
    )

    paired_mutated_ell0 = sp.factor((5 * k0) / mu0)
    paired_mutated_ell1 = sp.factor((7 * k1) / transmuted)
    paired_mutated_ratio = sp.cancel(
        ((5 * k0) / paired_mutated_ell0)
        / ((7 * k1) / paired_mutated_ell1)
    )
    checks.check(
        "paired conversion reparameterization preserves the energy ratio",
        paired_mutated_ratio == paired_energy_ratio
        and paired_mutated_ell0 != paired_ell0
        and paired_mutated_ell1 != paired_ell1,
    )

    soliton_factor = sp.Symbol("c_soliton", positive=True)
    unpaired_mass = sp.factor(soliton_factor * k1 / ell1)
    unpaired_log = sp.simplify(sp.log(energy0 / unpaired_mass))
    checks.check(
        "unpaired soliton coefficient remains in the scale logarithm",
        sp.simplify(unpaired_log - scale_log) == -sp.log(soliton_factor)
        and unpaired_log.has(soliton_factor),
    )
    reversed_log = sp.log(sp.cancel((k0 / ell1) / (k1 / ell0)))
    checks.check(
        "unpaired length orientation mutation changes the logarithm",
        sp.simplify(reversed_log - scale_log) != 0,
    )

    design = sp.Matrix([[-1, 1]])
    checks.check(
        "raw log-row rank leaves the common absolute scale free",
        design.rank() == 1
        and design.nullspace() == [sp.Matrix([1, 1])]
        and len(design.nullspace()) == 1,
    )

    zero_coefficient = sp.Integer(0)
    zero_matter_general = sp.simplify(local + finite + zero_coefficient * paired_log)
    checks.check(
        "zero matter retains only the affine boundary",
        zero_matter_general == local + finite
        and zero_matter_general.subs({local: 0, finite: 0}) == 0,
    )

    x = sp.Symbol("X", positive=True)
    y = sp.exp(x)
    checks.check(
        "dimensional power zero is constant not logarithmic",
        y**0 == 1 and sp.simplify(y**0 - sp.log(y)) == 1 - x,
    )
    checks.check(
        "raw counterfamilies refute logarithm uniqueness",
        sp.simplify(sp.log(y)) == x
        and sp.simplify(sp.log(y) ** 2) == x**2
        and sp.simplify(1 / sp.log(y)) == 1 / x
        and sp.simplify((1 + sp.log(y)) / (2 + sp.log(y)))
        == (x + 1) / (x + 2),
    )

    compatibility = audit_numpy_trapezoid_compatibility(
        this_file.read_text(encoding="utf-8"),
        filename=str(this_file),
    )
    checks.check(
        "independent review has no NumPy compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
