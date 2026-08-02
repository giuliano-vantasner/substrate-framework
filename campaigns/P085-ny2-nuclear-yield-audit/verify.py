"""Primary exact verifier for the P085 NY2 nuclear-yield audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.skyrme_relations import matched_pion_coupling_ratio
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-24/"
    "bridge_NY2_nuclear_yield_one_skyrme_unit.py"
)
ENGINE = Path(
    "/home/dan/substrate/pulson-backreaction-bridge/campaigns/"
    "c035-calculator/engine.js"
)
CROSS_CHECK = ENGINE.with_name("cross_check.js")
ENGINEERING_MATERIALS = Path(
    "/home/dan/substrate/engineering/spark_discharge/materials.py"
)
SOURCE_SHA256 = "a0ab1c713ff4224a3f4e39e6770c1a1c8c5bdc4c2f7ef2bd8b18ab8fc87c18a3"
ENGINE_SHA256 = "653484e15173a6d3ef5dc5cdc9a993872d02d3d6f390b885aba23a7b367e6bca"
CROSS_CHECK_SHA256 = "d73d658d921b91f593b40d8e0c776528ce0c936201141718716402396308dffa"
ENGINEERING_SHA256 = "971a101fcee44fb61e28e779da66f5ef24a0976d46c2c02566b249026b73815f"
CONTRACT_SHA256 = "97eff9083e36b2c7c9422db01c013519d5a44bb5d5acb0554551d9607d0c9507"
FREEZE_SHA256 = "575891ee68873db74edc52114a029d1e3daa51b8f50ffe7ae6b1fc56c316cd9e"


def _contract_path() -> Path:
    candidates = (
        Path("campaigns/P085-ny2-nuclear-yield-audit/proposal.yaml"),
        Path("proposals/P085-ny2-nuclear-yield-audit/proposal.yaml"),
    )
    return next(path for path in candidates if path.exists())


def _queue_unit(source_unit: str) -> dict[str, object]:
    queue = yaml.safe_load(Path("migration/source-claims.yaml").read_text())
    return next(unit for unit in queue["units"] if unit["source_unit"] == source_unit)


def _claim(claim_id: str) -> dict[str, object]:
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    return next(claim for claim in registry["claims"] if claim["id"] == claim_id)


def main() -> int:
    checks = CheckLedger("P085")
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
        "source has ten literal checks and a dynamic terminal tally",
        len(literal_checks) == 10
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "exact source and audit use no NumPy quadrature alias",
        all(alias not in source_text for alias in ("np." + "trapz", "np." + "trapezoid")),
    )

    rest_energy, scale, coefficient, target = sp.symbols(
        "E_e U kappa Q", positive=True
    )
    conditional_scale = matched_pion_coupling_ratio(rest_energy)
    yield_family = coefficient * scale
    checks.check(
        "same-dimension yield composition retains a dimensionless coefficient",
        sp.solve(sp.Eq(target, yield_family), coefficient) == [target / scale]
        and sp.simplify(yield_family.subs(coefficient, target / scale) - target)
        == 0,
    )
    checks.check(
        "coefficient one is a separately imposed coordinate rather than dimensional output",
        yield_family.subs(coefficient, 1) == scale
        and sp.diff(yield_family, coefficient) == scale
        and coefficient in yield_family.free_symbols,
    )
    checks.mutation_sensitive(
        "the source's coefficient-one yield is load bearing",
        lambda candidate: sp.simplify(candidate * scale - scale) == 0,
        sp.Integer(1),
        (sp.Rational(9, 10), sp.Rational(11, 10), sp.Rational(93, 100)),
    )
    checks.check(
        "C-DIM-002 already states that dimensions leave coefficients unconstrained",
        "Dimensionless multiplicative coefficients" in _claim("C-DIM-002")["assumptions"][2]
        and _claim("C-DIM-002")["review"] == "accepted",
    )
    checks.check(
        "C-SK-001 supplies no physical numerical or nuclear-yield prediction",
        "No numerical comparator" in _claim("C-SK-001")["assumptions"][2]
        and "physical mass prediction" in _claim("C-SK-001")["assumptions"][2],
    )

    electron_mev = sp.Rational(10219979, 20000000)
    unit_mev = sp.simplify(conditional_scale.subs(rest_energy, electron_mev))
    empirical_mev = sp.Rational(1193, 50)
    engine_mev = sp.Integer(24)
    empirical_coefficient = sp.simplify(empirical_mev / unit_mev)
    engine_coefficient = sp.simplify(engine_mev / unit_mev)
    checks.check(
        "opened reaction and engine comparators infer distinct nonunit coefficients",
        empirical_coefficient == sp.Rational(29825000, 10219979) / sp.pi
        and engine_coefficient == sp.Rational(30000000, 10219979) / sp.pi
        and empirical_coefficient != 1
        and engine_coefficient != 1
        and empirical_coefficient != engine_coefficient,
    )
    checks.check(
        "the source selects coefficient one before computing comparator residuals",
        source_text.index("Y_NUC_DERIVED_MEV = F_pi_over_e_MeV")
        < source_text.index("Q_EMPIRICAL = B_HE4 - 2 * B_D")
        and "leading O(1) coefficient = 1" in source_text,
    )
    checks.check(
        "the fixed O(1) band admits multiple incompatible coefficient choices",
        all(sp.Rational(85, 100) <= value <= sp.Rational(115, 100) for value in (
            sp.Rational(9, 10), sp.Integer(1), sp.Rational(11, 10)
        ))
        and sp.Rational(9, 10) * unit_mev != unit_mev
        and sp.Rational(11, 10) * unit_mev != unit_mev
        and "band_lo = 0.85 * F_pi_over_e_MeV" in source_text
        and "band_hi = 1.15 * F_pi_over_e_MeV" in source_text,
    )
    source_residual = sp.simplify(abs(unit_mev - empirical_mev) / empirical_mev)
    engine_residual = sp.simplify(abs(unit_mev - engine_mev) / engine_mev)
    checks.check(
        "source comparison percentages are nonzero post-freeze residuals only",
        sp.Rational(7, 100) < source_residual < sp.Rational(8, 100)
        and sp.Rational(7, 100) < engine_residual < sp.Rational(8, 100),
    )
    checks.check(
        "symbolic independence from comparators does not remove the empirical mass input",
        conditional_scale.free_symbols == {rest_energy}
        and sp.diff(conditional_scale, rest_energy) == 16 * sp.pi
        and "M_E_MEV = 0.51099895" in source_text,
    )

    mass_two, mass_four = sp.symbols("a_2 a_4", real=True)
    binding = sp.expand(2 * mass_two * scale - mass_four * scale)
    binding_coefficient = sp.factor(binding / scale)
    checks.check(
        "generic multi-soliton subtraction leaves both mass coefficients free",
        binding_coefficient == 2 * mass_two - mass_four
        and {mass_two, mass_four} == binding_coefficient.free_symbols,
    )
    checks.check(
        "unconstrained mass coefficients permit positive zero and negative binding",
        binding_coefficient.subs({mass_two: 2, mass_four: 3}) == 1
        and binding_coefficient.subs({mass_two: 2, mass_four: 4}) == 0
        and binding_coefficient.subs({mass_two: 2, mass_four: 5}) == -1,
    )
    positive_binding = sp.Symbol("k", positive=True)
    checks.check(
        "even an exothermic restriction leaves every positive coefficient reachable",
        sp.simplify(
            binding_coefficient.subs(
                {mass_two: (positive_binding + 1) / 2, mass_four: 1}
            )
            - positive_binding
        )
        == 0,
    )
    checks.check(
        "source admits it has no multi-soliton solution or computed coefficient",
        "exact O(1) coefficient" in source_text
        and "is NOT computed" in source_text
        and "no multi-Skyrmion solution exists" in source_text,
    )

    total_energy, release = sp.symbols("W Delta", positive=True)
    product_mass = total_energy - release
    photon_energy = sp.factor(
        (total_energy**2 - product_mass**2) / (2 * total_energy)
    )
    checks.check(
        "a one-body final state cannot carry a positive CM release by itself",
        sp.simplify(total_energy - product_mass) == release
        and total_energy != product_mass,
    )
    checks.check(
        "a radiative two-body final state partitions release into photon and recoil",
        sp.simplify(photon_energy - (release - release**2 / (2 * total_energy)))
        == 0
        and sp.simplify(release - photon_energy) == release**2 / (2 * total_energy),
    )
    checks.check(
        "source supplies no radiation branch rate or medium energy-deposition map",
        "gamma" not in source_text.lower()
        and "branching" not in source_text.lower()
        and "cross section" not in source_text.lower(),
    )

    engine_bytes = ENGINE.read_bytes()
    cross_bytes = CROSS_CHECK.read_bytes()
    engineering_bytes = ENGINEERING_MATERIALS.read_bytes()
    checks.check(
        "declared C035 engine and parity consumer are hash pinned",
        hashlib.sha256(engine_bytes).hexdigest() == ENGINE_SHA256
        and hashlib.sha256(cross_bytes).hexdigest() == CROSS_CHECK_SHA256,
    )
    engine_text = engine_bytes.decode("utf-8")
    cross_text = cross_bytes.decode("utf-8")
    checks.check(
        "C035 runtime and parity oracle still require the imported 24 MeV literal",
        "const Y_NUC_EV = 24.0e6" in engine_text
        and "E.Y_NUC_EV !== 24.0e6" in cross_text
        and "IMPORTED nuclear magnitude" in engine_text,
    )
    checks.check(
        "a D+D comparator cannot justify one common H2 and D2 event payload",
        "const NUCLEAR_CHANNEL = { H: true, D: true" in engine_text
        and "return nuclearChannel(g) ? Y_NUC_EV : 0.0" in engine_text
        and "D+D->4He" in source_text,
    )
    engineering_text = engineering_bytes.decode("utf-8")
    checks.check(
        "separate predecessor engineering code embeds the disputed conditional scale",
        hashlib.sha256(engineering_bytes).hexdigest() == ENGINEERING_SHA256
        and "NUCLEAR_YIELD_MEV = float(16 * np.pi * M_E_MEV)" in engineering_text
        and "DERIVED as the Skyrme energy unit" in engineering_text,
    )
    checks.check(
        "predecessor consumers are inconsistent rather than one completed migration",
        "24.0e6" in engine_text
        and "16 * np.pi * M_E_MEV" in engineering_text
        and "engine substitution outstanding" in source_text,
    )

    ny1 = _queue_unit("NY1")
    he4 = _queue_unit("HE4")
    checks.check(
        "NY1 is terminal duplicate evidence with no accepted physical yield mapping",
        ny1["disposition"] == "duplicate_evidence"
        and ny1["accepted_claims"] == ["C-SK-001"]
        and "multi-soliton binding" in ny1["duplicate_reason"],
    )
    checks.check(
        "HE4's accepted mappings are unrelated sine-Gordon action claims",
        he4["disposition"] == "qualified"
        and set(he4["accepted_claims"])
        == {"C-SG-001", "C-SG-003", "C-SG-004", "C-SG-006", "C-SG-007"}
        and "physical quantization" in he4["qualification"],
    )
    checks.check(
        "NY2 adds no dependency-closed canonical theorem API or accepted consumer",
        not any(
            token in source_text
            for token in (
                "solve_b2_profile",
                "solve_b4_profile",
                "binding_coefficient =",
                "branching_ratio =",
            )
        )
        and not Path("src/substrate_framework/nuclear_yield.py").exists(),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
