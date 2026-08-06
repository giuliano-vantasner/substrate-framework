"""Primary exact verifier for P219 MK6 and C-VAR-002."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.bps_energy import (
    bps_bound_per_absolute_degree,
    near_bps_mass_difference,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.variational import finite_functional_infimum_ledger
from substrate_framework.verification import CheckLedger


CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-43/"
    "bridge_MK6_confrontation_and_tension.py"
)
SOURCE_SHA = "ef900954d9782bbf2589ff3e33045577ebdce3860d1a3ed7a6a6827e0ae81788"
FREEZE_SHA = "35bfb22f64039a8d756f601cea73ee03fb630c7c2b451585bbbf7483e349fd84"


def main() -> int:
    checks = CheckLedger("P219")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source and preregistered formula surface are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA
        and hashlib.sha256(
            (CAMPAIGN / "evidence/formula-freeze.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(source_tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source inventory separates six predicates and one assertion",
        len(calls) == 6 and len(assertions) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "MK6 has no sampled integration or legacy NumPy compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0
        and "numpy" not in source_text
        and "scipy" not in source_text,
    )
    reproduction = yaml.safe_load(
        (CAMPAIGN / "evidence/source-reproduction.yaml").read_text()
    )
    checks.check(
        "one P219 native reproduction reached the six-check terminal tally",
        reproduction["native_run"]["exit_status"] == 0
        and reproduction["inventory"]["runtime_check_executions"] == 6
        and reproduction["native_run"]["terminal_tally"] == "ALL_6_CHECKS_PASS",
    )

    nc, pion_mass, scale, degree = sp.symbols("N_c m_pi F B", positive=True)
    lambda_a = nc / (4 * scale)
    lambda_bps = lambda_a / sp.pi**2
    mu = pion_mass * scale / 2
    target_average = 32 * sp.sqrt(2) / (15 * sp.pi)
    bps_route = sp.simplify(
        bps_bound_per_absolute_degree(lambda_bps, mu, target_average) * degree
    )
    lambda_a_route = sp.simplify(2 * lambda_a * mu * target_average * degree)
    corrected = 8 * sp.sqrt(2) * nc * pion_mass * degree / (15 * sp.pi)
    checks.check(
        "lambda_BPS and lambda_A routes eliminate to the same corrected bound",
        sp.simplify(bps_route - corrected) == 0
        and sp.simplify(lambda_a_route - corrected) == 0,
    )
    source_formula = 8 * sp.sqrt(2) * sp.pi * nc * pion_mass * degree / 15
    checks.check(
        "the MK6 headline formula is exactly pi squared too large",
        sp.simplify(source_formula / corrected - sp.pi**2) == 0,
    )
    corrected_numeric = corrected.subs(
        {nc: 3, pion_mass: sp.Rational(13803, 100), degree: 1}
    )
    nucleon = sp.Rational(93892, 100)
    checks.check(
        "the corrected supplied-input value defeats the source five-percent premise",
        abs(float(corrected_numeric) - 99.4165288953323) < 1.0e-12
        and corrected_numeric / nucleon < sp.Rational(11, 100)
        and abs(corrected_numeric - nucleon) / nucleon > sp.Rational(4, 5),
    )
    checks.check(
        "the corrected formula retains supplied pion mass color count and degree",
        corrected.free_symbols == {nc, pion_mass, degree},
    )

    coefficient, epsilon = sp.symbols("K epsilon", positive=True)
    base_correction, final_correction = sp.symbols("D_A D_nA", real=True)
    difference = near_bps_mass_difference(
        1,
        2,
        multiplicity=2,
        bps_energy_per_degree=coefficient,
        epsilon=epsilon,
        base_correction=base_correction,
        composite_correction=final_correction,
    )
    checks.check(
        "linearity cancels only the attained leading term not arbitrary corrections",
        difference.bps_term == 0
        and sp.simplify(
            difference.expression
            - epsilon * (2 * base_correction - final_correction)
        )
        == 0
        and difference.expression.subs({base_correction: 0, final_correction: 1})
        == -epsilon,
    )

    m1, m2 = sp.symbols("m1 m2", real=True)
    d1, d2 = sp.symbols("d1 d2", nonnegative=True)
    ledger = finite_functional_infimum_ledger(
        (m1 + d1, m2 + d2),
        (m1, m2),
    )
    checks.check(
        "common-configuration excess is the sum of nonnegative component excesses",
        ledger.component_excesses == (d1, d2)
        and ledger.total_excess == d1 + d2
        and ledger.identity_residual == 0,
    )
    checks.check(
        "zero joint excess is equivalent to simultaneous component attainment",
        sp.solve(
            [ledger.total_excess, d1, d2],
            [d1, d2],
            dict=True,
        )
        == [{d1: 0, d2: 0}],
    )
    coordinate = sp.symbols("x", real=True)
    common = finite_functional_infimum_ledger(
        (coordinate**2, 3 * coordinate**2),
        (0, 0),
    )
    incompatible = finite_functional_infimum_ledger(
        ((coordinate - 1) ** 2, (coordinate + 1) ** 2),
        (0, 0),
    )
    checks.check(
        "a common minimizer saturates while incompatible minimizers leave a strict gap",
        sp.minimum(common.summed_value, coordinate) == 0
        and sp.minimum(incompatible.summed_value, coordinate) == 2,
    )
    checks.mutation_sensitive(
        "shared minimizer is load bearing",
        lambda shift: sp.minimum(
            (coordinate - 1) ** 2 + (coordinate - shift) ** 2,
            coordinate,
        )
        == 0,
        1,
        (-1, 0, 2),
    )

    radius = (lambda_bps * degree / mu) ** sp.Rational(1, 3)
    scale_ratio = sp.factor(
        scale**2 * radius / (lambda_bps * mu * degree)
    )
    scale_factor = sp.simplify(
        scale_ratio / (scale / pion_mass) ** sp.Rational(4, 3)
    )
    checks.check(
        "accepted-convention scale estimate retains degree color and pi factors",
        scale_factor
        == 4
        * 2 ** sp.Rational(2, 3)
        * sp.pi ** sp.Rational(4, 3)
        / (degree ** sp.Rational(2, 3) * nc ** sp.Rational(2, 3)),
    )
    skyrme_coupling = sp.symbols("e", positive=True)
    local_epsilon = 8 * sp.pi**2 * (scale / skyrme_coupling) / (
        nc * pion_mass
    )
    checks.check(
        "the scale estimate and local epsilon are distinct conditional objects",
        sp.diff(scale_ratio, skyrme_coupling) == 0
        and sp.diff(local_epsilon, skyrme_coupling) != 0,
    )
    checks.check(
        "power counting supplies no controlled expansion or physical regime",
        "remainder" not in source_text
        and "tolerance" not in source_text
        and "error" not in source_text.lower(),
    )
    checks.check(
        "MK6 never forms its alleged separately additive sector sum",
        "M_classical_sector + E_BPS_1" not in source_text
        and "E_BPS_1 + M_classical_sector" not in source_text,
    )
    checks.check(
        "the source guard is a narrow lexical filter rather than provenance proof",
        "M_NUCLEON = 938.92" in source_text
        and "MP_ME = 1836.15" in source_text
        and "FORBIDDEN = [929 / 1000.0" in source_text,
    )
    checks.check(
        "source prose values are not the executable classical comparison values",
        "1833.6" in source_text
        and abs(float(48 * sp.pi**3) * 1.2314 - 1832.7) < 0.1,
    )
    checks.check(
        "C-VAR-002 adds no physical fields parameters or empirical inputs",
        ledger.summed_value.free_symbols == {m1, m2, d1, d2}
        and corrected.free_symbols.isdisjoint(ledger.summed_value.free_symbols),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
