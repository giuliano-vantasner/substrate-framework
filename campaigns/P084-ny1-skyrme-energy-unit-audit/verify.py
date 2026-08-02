"""Primary exact verifier for the P084 NY1 Skyrme energy-unit audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.skyrme_relations import (
    conditional_anw_mass,
    conditional_topological_mass,
    matched_pion_coupling_ratio,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-24/"
    "bridge_NY1_skyrme_energy_unit.py"
)
SOURCE_SHA256 = "b3531d7f906fe396a1326d44d68f34d09ae34988e86a8f721c360040c4aa0921"
CONTRACT_SHA256 = "ff8c53c7529198d7c09a8958956c9cc9d81219c61d920072f99e35c3743d79df"
FREEZE_SHA256 = "9cd2980846e5d0b2cd27998927f58ae19a40aecc3221817034c030383bad5e8c"


def _contract_path() -> Path:
    candidates = (
        Path("campaigns/P084-ny1-skyrme-energy-unit-audit/proposal.yaml"),
        Path("proposals/P084-ny1-skyrme-energy-unit-audit/proposal.yaml"),
    )
    return next(path for path in candidates if path.exists())


def _queue_unit(source_unit: str) -> dict[str, object]:
    queue = yaml.safe_load(Path("migration/source-claims.yaml").read_text())
    return next(unit for unit in queue["units"] if unit["source_unit"] == source_unit)


def _queue_index(source_unit: str) -> int:
    queue = yaml.safe_load(Path("migration/source-claims.yaml").read_text())
    return next(
        index
        for index, unit in enumerate(queue["units"])
        if unit["source_unit"] == source_unit
    )


def _claim(claim_id: str) -> dict[str, object]:
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    return next(claim for claim in registry["claims"] if claim["id"] == claim_id)


def _literal_match(candidate: object) -> bool:
    top_prefactor, anw_prefactor, top_power, anw_power = candidate
    coefficient, rest_energy, ratio = sp.symbols("B E R", positive=True)
    solved = sp.solve(
        sp.Eq(
            anw_prefactor * sp.pi**2 * coefficient**anw_power * ratio,
            top_prefactor * sp.pi**3 * coefficient**top_power * rest_energy,
        ),
        ratio,
    )[0]
    return bool(
        sp.simplify(solved - 16 * sp.pi * rest_energy) == 0
        and coefficient not in solved.free_symbols
    )


def main() -> int:
    checks = CheckLedger("P084")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    normalized_contract = (
        _contract_path()
        .read_bytes()
        .replace(b"status: accepted\n", b"status: draft\n")
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    freeze_path = _contract_path().parent / "evidence/frozen-proposal.yaml"
    checks.check(
        "pre-source contract commitment is immutable",
        hashlib.sha256(freeze_path.read_bytes()).hexdigest() == FREEZE_SHA256,
    )
    literal_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source has nine literal checks and a dynamic terminal tally",
        len(literal_checks) == 9
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "exact source and audit use no NumPy quadrature alias",
        all(alias not in source_text for alias in ("np." + "trapz", "np." + "trapezoid")),
    )

    coefficient, rest_energy, pion_scale, coupling = sp.symbols(
        "B1 E_e F_pi e", positive=True
    )
    ratio = sp.Symbol("X", positive=True)
    source_top = 48 * sp.pi**3 * coefficient * rest_energy
    source_anw = 3 * sp.pi**2 * coefficient * ratio
    solved_ratio = sp.solve(sp.Eq(source_anw, source_top), ratio)[0]
    checks.check(
        "canonical APIs reproduce both supplied source premises exactly",
        conditional_topological_mass(coefficient, rest_energy) == source_top
        and conditional_anw_mass(coefficient, pion_scale, coupling)
        == 3 * sp.pi**2 * coefficient * pion_scale / coupling,
    )
    checks.check(
        "NY1's exact solution is the already accepted C-SK-001 ratio",
        solved_ratio == matched_pion_coupling_ratio(rest_energy)
        == 16 * sp.pi * rest_energy,
    )
    checks.check(
        "the reverse implication closes only the two supplied premises",
        sp.simplify(
            source_top
            - source_anw.subs(ratio, matched_pion_coupling_ratio(rest_energy))
        )
        == 0,
    )
    skyrme_claim = _claim("C-SK-001")
    checks.check(
        "accepted C-SK-001 already owns the exact iff and its premise ceiling",
        skyrme_claim["review"] == "accepted"
        and skyrme_claim["verification"] == "symbolic_verified"
        and "if and only if" in skyrme_claim["statement"]
        and "Both mass formulas are approved conditional premises"
        in skyrme_claim["assumptions"][0]
        and "No numerical comparator" in skyrme_claim["assumptions"][2],
    )

    top_prefactor, anw_prefactor = sp.symbols("a c", positive=True)
    top_power, anw_power = sp.symbols("p q", integer=True)
    generic_ratio = sp.simplify(
        top_prefactor
        * sp.pi**3
        * coefficient**top_power
        * rest_energy
        / (anw_prefactor * sp.pi**2 * coefficient**anw_power)
    )
    checks.check(
        "generic monomial matching retains prefactor and power differences",
        generic_ratio
        == sp.pi
        * top_prefactor
        * coefficient ** (top_power - anw_power)
        * rest_energy
        / anw_prefactor,
    )
    checks.check(
        "the coefficient cancels exactly for equal powers and survives a power mismatch",
        sp.simplify(generic_ratio.subs(top_power, anw_power) - sp.pi * top_prefactor * rest_energy / anw_prefactor)
        == 0
        and coefficient
        in generic_ratio.subs({top_power: anw_power + 1}).free_symbols,
    )
    checks.mutation_sensitive(
        "both literal prefactors and shared coefficient powers are load bearing",
        _literal_match,
        (48, 3, 1, 1),
        (
            (24, 3, 1, 1),
            (48, 6, 1, 1),
            (48, 3, 2, 1),
            (48, 3, 1, 2),
        ),
    )

    checks.check(
        "B1 cancellation does not remove the empirical electron-energy coordinate",
        coefficient not in solved_ratio.free_symbols
        and solved_ratio.free_symbols == {rest_energy}
        and sp.diff(solved_ratio, rest_energy) == 16 * sp.pi
        and sp.limit(solved_ratio, rest_energy, 0, dir="+") == 0,
    )
    dimensionless_coordinate = sp.Symbol("N_e", positive=True)
    action, speed, length = sp.symbols("S c_0 a", positive=True)
    reparameterized = sp.simplify(
        solved_ratio.subs(rest_energy, dimensionless_coordinate * action * speed / length)
    )
    checks.check(
        "lossless reparameterization leaves one free dimensionless mass input",
        dimensionless_coordinate in reparameterized.free_symbols
        and sp.solve(
            sp.Eq(sp.Symbol("Y", positive=True), reparameterized),
            dimensionless_coordinate,
        )
        == [sp.Symbol("Y", positive=True) * length / (16 * sp.pi * action * speed)],
    )

    electron_mev = sp.Rational(10219979, 20000000)
    numerical_scale = sp.simplify(solved_ratio.subs(rest_energy, electron_mev))
    checks.check(
        "the reported 25.69 MeV is an evaluation of an inserted measured value",
        "M_E_MEV = 0.51099895" in source_text
        and numerical_scale == sp.Rational(10219979, 1250000) * sp.pi
        and 25.6 < float(numerical_scale) < 25.8,
    )
    arbitrary_coefficient = sp.Symbol("B", positive=True)
    closed_mass = sp.simplify(3 * sp.pi**2 * arbitrary_coefficient * solved_ratio)
    checks.check(
        "the proton closure is an identity by construction for every positive input",
        sp.simplify(
            closed_mass - 48 * sp.pi**3 * arbitrary_coefficient * rest_energy
        )
        == 0
        and {arbitrary_coefficient, rest_energy} <= closed_mass.free_symbols
        and "900 < m_p_closed < 970" in source_text,
    )

    correction, target = sp.symbols("kappa T", positive=True)
    corrected_scale = correction * solved_ratio
    target_correction = sp.solve(sp.Eq(corrected_scale, target), correction)[0]
    checks.check(
        "an unconstrained dimensionless correction realizes every positive target",
        target_correction == target / (16 * sp.pi * rest_energy)
        and sp.simplify(corrected_scale.subs(correction, target_correction) - target)
        == 0,
    )
    physical_fit = sp.Rational(341, 10)
    fit_correction = sp.simplify(physical_fit / numerical_scale)
    engine_target = sp.Integer(24)
    engine_coefficient = sp.simplify(engine_target / numerical_scale)
    checks.check(
        "opened fit and engine values determine different comparator-derived coefficients",
        "F_pi_over_e_PHYS = 34.1" in source_text
        and fit_correction != 1
        and engine_coefficient != 1
        and fit_correction != engine_coefficient
        and sp.simplify(fit_correction * numerical_scale - physical_fit) == 0
        and sp.simplify(engine_coefficient * numerical_scale - engine_target) == 0,
    )
    checks.check(
        "source computes no quantum correction or multi-soliton binding coefficient",
        "this bridge does not compute the correction" in source_text
        and "M(B=2)" not in source_text
        and "M(B=4)" not in source_text
        and "Y_NUC =" not in source_text,
    )

    b1 = _queue_unit("B1")
    s2 = _queue_unit("S2")
    ny2 = _queue_unit("NY2")
    checks.check(
        "all named corpus dependencies remain pending with empty accepted mappings",
        all(
            unit["disposition"] == "pending_adjudication"
            and unit["accepted_claims"] == []
            for unit in (b1, s2, ny2)
        ),
    )
    checks.check(
        "NY2 is a later consumer rather than a derivation dependency",
        ny2["phase"] == "phase-24"
        and "NY1" in ny2["candidate_dependencies"]
        and _queue_index("NY2") > _queue_index("NY1"),
    )
    checks.check(
        "source labels cannot convert its visible imports into zero-input physics",
        "no fit, no import" in source_text
        and "M_E_MEV = 0.51099895" in source_text
        and "B1_NUM = 1.232" in source_text
        and "F_pi_over_e_PHYS = 34.1" in source_text,
    )
    checks.check(
        "NY1 adds no distinct canonical theorem API or accepted consumer",
        Path("src/substrate_framework/skyrme_relations.py").exists()
        and Path("tests/test_skyrme_relations.py").exists()
        and set(skyrme_claim["evidence"])
        >= {
            "campaigns/P008-constitutive-qualification/verify.py",
            "campaigns/P008-constitutive-qualification/reviews/independent_algebra_review.py",
            "tests/test_skyrme_relations.py",
        },
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
