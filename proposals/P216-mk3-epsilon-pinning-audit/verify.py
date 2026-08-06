"""Primary exact verifier for the P216 MK3 epsilon-pinning audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import re
import subprocess

import sympy as sp
import yaml

from substrate_framework.bps_energy import (
    bogomolny_density_decomposition,
    bps_bound_per_absolute_degree,
)
from substrate_framework.skyrme_relations import matched_pion_coupling_ratio
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-43/"
    "bridge_MK3_epsilon_pinned.py"
)
SOURCE_SHA256 = "64254d0f6b9d6ff57f5a8b0a4b86a510e2bef230b4f3bec062533fac59516404"
FORMULA_FREEZE_SHA256 = "6f5af8f396925ea54177c318eb682c692f52c9e27eec1cb6719ffe866fded057"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _claim_map() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())
    return {claim["id"]: claim for claim in registry["claims"]}


def main() -> int:
    checks = CheckLedger("P216")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    checks.check(
        "MK3 source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "pre-source formula freeze is immutable",
        _sha256(CAMPAIGN / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )
    literal_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(source_tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source inventory separates six predicates from one assertion",
        len(literal_checks) == 6
        and len(assertions) == 1
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "MK3 has no NumPy integration compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    native = subprocess.run(
        [str(ROOT / ".venv/bin/python"), str(SOURCE)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    checks.check(
        "native source executes all six runtime predicates cleanly",
        native.returncode == 0
        and native.stdout.count("  PASS\n") == 6
        and native.stdout.rstrip().endswith("ALL 6 CHECKS PASS"),
    )

    f_pi, e_sk, lam, mu = sp.symbols("F_pi e lambda mu", positive=True)
    local = sp.simplify(1 / (e_sk * (lam * f_pi) * (mu / f_pi**2)))
    scale_over_product = sp.simplify((f_pi / e_sk) / (lam * mu))
    checks.check(
        "MK3.1 exact quotient identity survives as a supplied-input definition",
        sp.simplify(local - scale_over_product) == 0,
    )
    dimensions = {f_pi: 1, e_sk: 0, lam: -1, mu: 2}
    exponent = {f_pi: 1, e_sk: -1, lam: -1, mu: -1}
    checks.check(
        "the local quotient is dimensionless in KI2's declared convention",
        sum(exponent[symbol] * dimensions[symbol] for symbol in exponent) == 0,
    )
    normalization = sp.symbols("c_epsilon", positive=True)
    checks.check(
        "dimension algebra leaves an arbitrary local normalization",
        sp.simplify((2 * normalization * local) - (normalization * local)) != 0
        and normalization in (normalization * local).free_symbols
        and normalization not in local.free_symbols,
    )

    scale, product, target = sp.symbols("s p epsilon_target", positive=True)
    checks.check(
        "a supplied scale and product pin only their declared quotient",
        sp.simplify((scale / product).subs(product, scale / target) - target) == 0
        and sp.simplify((scale / target) - product) != 0,
    )
    splitter = sp.symbols("u", positive=True)
    same_product_one = {lam: splitter, mu: product / splitter}
    same_product_two = {lam: 2 * splitter, mu: product / (2 * splitter)}
    checks.check(
        "one pinned product does not derive lambda and mu individually",
        sp.simplify(local.subs(same_product_one) - local.subs(same_product_two)) == 0
        and same_product_one != same_product_two,
    )
    checks.check(
        "the accepted positive coupling family realizes every positive local target",
        sp.simplify(
            local.subs({lam: f_pi / (e_sk * mu * target)}) - target
        )
        == 0,
    )

    baryon, potential, t = sp.symbols("B0 V t", positive=True)
    base = bogomolny_density_decomposition(
        baryon,
        potential,
        lam,
        mu,
        orientation=1,
    )
    flowed = bogomolny_density_decomposition(
        baryon,
        potential,
        t * lam,
        t * mu,
        orientation=1,
    )
    checks.check(
        "KI2's simultaneous flow changes every load-bearing fixed-theory BPS object",
        sp.simplify(flowed.energy_density - t**2 * base.energy_density) == 0
        and sp.simplify(flowed.square_density - t**2 * base.square_density) == 0
        and sp.simplify(flowed.saturation_residual - t * base.saturation_residual)
        == 0
        and sp.simplify(
            bps_bound_per_absolute_degree(t * lam, t * mu, 1)
            - t**2 * bps_bound_per_absolute_degree(lam, mu, 1)
        )
        == 0,
    )
    checks.check(
        "a separately supplied fixed product would restrict the positive flow to identity",
        sp.solve(sp.Eq(t**2 * product, product), t) == [1],
    )

    color, pion_mass = sp.symbols("N_c m_pi", positive=True)
    lambda_a = color / (4 * f_pi)
    conditional_mu = pion_mass * f_pi / 2
    source_product = sp.simplify(lambda_a * conditional_mu)
    lambda_bps = sp.simplify(lambda_a / sp.pi**2)
    accepted_product = sp.simplify(lambda_bps * conditional_mu)
    checks.check(
        "MK3.2 source product is exact only as all-premise lambda_A algebra",
        source_product == color * pion_mass / 8,
    )
    checks.check(
        "accepted BPS convention changes the product by the load-bearing pi squared",
        accepted_product == color * pion_mass / (8 * sp.pi**2)
        and sp.simplify(source_product / accepted_product - sp.pi**2) == 0,
    )
    source_epsilon = sp.simplify((f_pi / e_sk) / source_product)
    accepted_epsilon = sp.simplify((f_pi / e_sk) / accepted_product)
    checks.check(
        "source and accepted-convention conditional epsilons differ by pi squared",
        source_epsilon == 8 * f_pi / (e_sk * color * pion_mass)
        and accepted_epsilon
        == 8 * sp.pi**2 * f_pi / (e_sk * color * pion_mass)
        and sp.simplify(accepted_epsilon / source_epsilon - sp.pi**2) == 0,
    )

    electron_energy = sp.symbols("E_e", positive=True)
    conditional_scale = matched_pion_coupling_ratio(electron_energy)
    source_final = sp.simplify(
        source_epsilon.subs(f_pi, conditional_scale * e_sk).subs(color, 3)
    )
    accepted_final = sp.simplify(
        accepted_epsilon.subs(f_pi, conditional_scale * e_sk).subs(color, 3)
    )
    checks.check(
        "C-SK-001 composition retains the empirical electron-energy input",
        conditional_scale == 16 * sp.pi * electron_energy
        and source_final == 128 * sp.pi * electron_energy / (3 * pion_mass)
        and sp.diff(source_final, electron_energy) != 0,
    )
    checks.check(
        "accepted-convention conditional composition carries pi cubed",
        accepted_final
        == 128 * sp.pi**3 * electron_energy / (3 * pion_mass)
        and sp.simplify(accepted_final / source_final - sp.pi**2) == 0,
    )

    electron_value = sp.Rational(511, 1000)
    pion_value = sp.Rational(13803, 100)
    source_numeric = source_final.subs(
        {electron_energy: electron_value, pion_mass: pion_value}
    )
    accepted_numeric = accepted_final.subs(
        {electron_energy: electron_value, pion_mass: pion_value}
    )
    checks.check(
        "MK3.5 less-than-one verdict reverses under the accepted convention",
        bool(sp.N(source_numeric) < 1)
        and bool(sp.N(accepted_numeric) > 1)
        and sp.simplify(accepted_numeric / source_numeric - sp.pi**2) == 0,
    )

    claims = _claim_map()
    near_bps_statement = str(claims["C-BPS-003"]["statement"])
    checks.check(
        "C-BPS-003 supplies no map or less-than-one self-consistency criterion",
        "epsilon a positive dimensionless parameter tending to zero" in near_bps_statement
        and not re.search(r"lambda|mu|F_pi", near_bps_statement)
        and "<1" not in near_bps_statement
        and "less than one" not in near_bps_statement,
    )

    dispositions = yaml.safe_load(
        (ROOT / "migration/dispositions.yaml").read_text()
    )["units"]
    checks.check(
        "governed MK1 and MK2 records withhold both claimed physical coupling closures",
        dispositions["MK1"]["disposition"] == "qualified"
        and "do not supply an accepted physical pion"
        in dispositions["MK1"]["qualification"]
        and dispositions["MK2"]["disposition"] == "qualified"
        and "lambda_A=pi^2*lambda_BPS" in dispositions["MK2"]["qualification"]
        and "Accepted claims derive no physical HLS sector"
        in dispositions["MK2"]["qualification"],
    )
    checks.check(
        "NY1 is duplicate conditional evidence rather than a zero-import scale derivation",
        dispositions["NY1"]["disposition"] == "duplicate_evidence"
        and "empirical electron rest energy" in dispositions["NY1"]["duplicate_reason"],
    )

    checks.check(
        "MK3 prose contains a factor-of-two contradiction excluded from its executable checks",
        "128 pi m_e / (3 m_pi)  =  (64 pi/3)" in source_text
        and "~  0.248" in source_text
        and "eps_expected = 128 * sp.pi * m_e / (3 * m_pi)" in source_text,
    )
    checks.check(
        "MK3.3 non-tautology guard never tests prior dependence on g or m_V",
        "for X in (F_pi, e_sk, lam, mu)" in source_text
        and "for X in (F_pi, e_sk, lam, mu, g, m_V)" in source_text,
    )
    checks.check(
        "MK3.4 removes t by substituting a t-free expression instead of validating closure",
        "sp.diff(eps_final_Nc3, t)" in source_text
        and "eps_final_Nc3" in source_text
        and t not in source_final.free_symbols,
    )
    checks.check(
        "MK3.6 executable guard reconstructs the comparator despite claiming none is read",
        "KAPPA_EMP_VALUE = 929 / 1000.0" in source_text
        and 'comparator_tokens = ("kappa" + "_emp"' in source_text
        and "KAPPA_EMP_VALUE" in source_text
        and "kappa_emp" not in {"KAPPA_EMP_VALUE"},
    )
    checks.check(
        "the epsilon calculation itself remains algebraically comparator-free",
        source_final.free_symbols == {electron_energy, pion_mass}
        and accepted_final.free_symbols == {electron_energy, pion_mass},
    )

    post_delta = yaml.safe_load(
        (CAMPAIGN / "evidence/post-source-claim-delta.yaml").read_text()
    )
    checks.check(
        "post-source nonduplication selects no new claim or package API",
        post_delta["claim_decision"]["promoted_new_claims"] == []
        and post_delta["claim_decision"]["new_package_apis"] == [],
    )
    checks.check(
        "source audit preserves conditional algebra and rejects physical pinning",
        "lambda_A_product" in (CAMPAIGN / "evidence/source-audit.yaml").read_text()
        and "MK3.5" in (CAMPAIGN / "evidence/check-adjudication.yaml").read_text()
        and "rejected" in (CAMPAIGN / "evidence/check-adjudication.yaml").read_text(),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
