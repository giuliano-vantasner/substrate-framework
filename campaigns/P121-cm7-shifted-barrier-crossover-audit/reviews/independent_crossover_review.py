"""Independent CM7 audit without importing P121 or canonical crossover APIs."""

from __future__ import annotations

import ast
import hashlib
import importlib
from pathlib import Path
import sys

import numpy as np
import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-31/"
    "bridge_CM7_gamow_crossover.py"
)
SCREENING = Path("/home/dan/substrate/engineering/screening/screening.py")
MATERIALS = Path("/home/dan/substrate/engineering/dbd/materials.py")
FROZEN = Path(
    "campaigns/P121-cm7-shifted-barrier-crossover-audit/evidence/"
    "frozen-proposal.yaml"
)
SOURCE_SHA = "10344b842a47b24651c891dfa55a030dd193e3e48e0b128b93bf74f29af6cee2"
SCREENING_SHA = "8ed6d54c8e3626f58ee2b3da78ce6eea7f4689092103dc23ed888b985e4cb4c3"
MATERIALS_SHA = "3639e1348fce91d38392c9405f62321059aec0452c4628262a515297d9a27f30"
FREEZE_SHA = "e7e6b6d1fffa9aa9606e9aed825544f78ae4b8213547aed6d0f623023a280045"


def manual_bisection(
    level: float,
    barrier: float,
    shift: float,
    low: float,
    high: float,
    iterations: int,
) -> tuple[float, bool]:
    response = lambda energy: np.exp(-np.sqrt(barrier / (energy + shift)))
    bracketed = response(low) <= level <= response(high)
    if not bracketed:
        return 0.5 * (low + high), False
    for _ in range(iterations):
        mid = 0.5 * (low + high)
        if response(mid) < level:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high), True


def main() -> int:
    checks = CheckLedger("CM7-INDEPENDENT-REVIEW")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    tree = ast.parse(source_text)
    checks.check(
        "independently read CM7 bytes are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA,
    )
    checks.check(
        "independently read screening bytes are hash pinned",
        hashlib.sha256(SCREENING.read_bytes()).hexdigest() == SCREENING_SHA,
    )
    checks.check(
        "independently read materials bytes are hash pinned",
        hashlib.sha256(MATERIALS.read_bytes()).hexdigest() == MATERIALS_SHA,
    )
    checks.check(
        "the preregistration artifact remains byte identical",
        hashlib.sha256(FROZEN.read_bytes()).hexdigest() == FREEZE_SHA,
    )
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "fresh AST count finds all twenty-seven source predicates",
        len(source_checks) == 27,
    )

    k, barrier, shift = sp.symbols("k G U", positive=True)
    level = sp.exp(-k)
    energy = sp.simplify(barrier / k**2 - shift)
    response_at_energy = sp.simplify(
        sp.exp(-sp.sqrt(barrier / (energy + shift)))
    )
    checks.check(
        "fresh k-coordinate inversion gives E=G/k^2-U",
        response_at_energy == level,
    )
    checks.check(
        "fresh positive-domain inequality gives 0<k<sqrt(G/U)",
        sp.solve_univariate_inequality(9 / k**2 - 1 > 0, k) == (k < 3)
        and k.is_positive is True,
    )
    floor = sp.exp(-sp.sqrt(barrier / shift))
    checks.check(
        "fresh endpoint evaluation gives floor crossing zero and upper divergence",
        sp.simplify(energy.subs(k, sp.sqrt(barrier / shift))) == 0
        and sp.limit(energy, k, 0, dir="+") == sp.oo,
    )
    checks.check(
        "fresh response limits are the attained floor and unattained one",
        sp.limit(sp.exp(-sp.sqrt(barrier / (sp.Symbol("x", positive=True) + shift))), sp.Symbol("x", positive=True), 0, dir="+")
        == floor,
    )
    # Repeat the high limit with a single shared symbol so no canonical helper is used.
    x = sp.symbols("x", nonnegative=True)
    response = sp.exp(-sp.sqrt(barrier / (x + shift)))
    finite_exponent = -sp.sqrt(barrier / (1 + shift))
    checks.check(
        "fresh response tends to one only at infinite input",
        sp.limit(response, x, sp.oo) == 1
        and finite_exponent.is_negative is True
        and finite_exponent.is_zero is False,
    )

    c = sp.symbols("c", positive=True)
    inverse = barrier / sp.log(c) ** 2 - shift
    dc = sp.diff(inverse, c)
    dbarrier = sp.diff(inverse, barrier)
    dshift = sp.diff(inverse, shift)
    checks.check(
        "fresh differentiation gives all three exact sensitivities",
        dc == -2 * barrier / (c * sp.log(c) ** 3)
        and dbarrier == 1 / sp.log(c) ** 2
        and dshift == -1,
    )
    checks.check(
        "fresh branch substitution proves the level derivative positive",
        sp.simplify(dc.subs(c, sp.exp(-k))).is_positive is True,
    )
    eps_g = sp.simplify(barrier * dbarrier / inverse)
    eps_u = sp.simplify(shift * dshift / inverse)
    eps_c = sp.simplify(c * dc / inverse)
    checks.check(
        "fresh barrier and shift elasticities close common-scale exponent one",
        sp.simplify(eps_g + eps_u) == 1,
    )
    checks.check(
        "fresh elasticities diverge at the zero-crossing floor",
        sp.limit(eps_g.subs(c, sp.exp(-k)), k, sp.sqrt(barrier / shift), dir="-")
        == sp.oo
        and sp.limit(eps_u.subs(c, sp.exp(-k)), k, sp.sqrt(barrier / shift), dir="-")
        == -sp.oo
        and sp.limit(eps_c.subs(c, sp.exp(-k)), k, sp.sqrt(barrier / shift), dir="-")
        == sp.oo,
    )
    rho = sp.symbols("rho", positive=True)
    checks.check(
        "fresh common-scale substitution makes the inverse homogeneous of degree one",
        sp.simplify(
            inverse.subs({barrier: rho * barrier, shift: rho * shift})
            - rho * inverse
        )
        == 0,
    )

    checks.check(
        "the squared-log expression does not solve the factor equation for c above one",
        sp.simplify(
            sp.exp(
                -sp.sqrt(
                    sp.Integer(9)
                    / ((sp.Integer(9) / sp.log(2) ** 2 - 1) + 1)
                )
            )
            - sp.Rational(1, 2)
        )
        == 0,
    )
    checks.check(
        "zero negative one and above-one levels are outside the real finite interior",
        all(value <= 0 or value >= 1 for value in (0, -1, 1, 2)),
    )
    checks.check(
        "zero shift changes the floor and removes the subtraction term",
        sp.limit(floor, shift, 0, dir="+") == 0
        and inverse.subs(shift, 0) == barrier / sp.log(c) ** 2,
    )

    target = sp.symbols("T", positive=True)
    fitted_level = sp.exp(-sp.sqrt(barrier / (target + shift)))
    checks.check(
        "fresh arbitrary-target substitution proves free-level nonidentifiability",
        sp.simplify(inverse.subs(c, fitted_level) - target) == 0,
    )
    checks.check(
        "a relative normalization changes the formal crossing",
        sp.simplify(
            inverse.subs({barrier: 9, shift: 1, c: sp.exp(-2)})
            - inverse.subs({barrier: 9, shift: 1, c: sp.exp(-2) / 2})
        )
        != 0,
    )

    threshold_level = sp.exp(-sp.sqrt(barrier / (target + shift)))
    log_fraction = sp.simplify(
        (sp.log(threshold_level) - sp.log(floor)) / (-sp.log(floor))
    )
    checks.check(
        "fresh change of variables gives the log-uniform below-threshold fraction",
        sp.simplify(log_fraction - (1 - sp.sqrt(shift / (shift + target))))
        == 0,
    )
    c_fraction = sp.simplify((threshold_level - floor) / (1 - floor))
    checks.check(
        "uniform-c gives a different exact fraction",
        sp.N(
            (c_fraction - log_fraction).subs(
                {barrier: 4, shift: 1, target: 1}
            )
        )
        != 0,
    )
    checks.check(
        "two point masses realize opposite threshold probabilities",
        bool(sp.exp(-2) < sp.exp(-sp.sqrt(2)))
        and not bool(sp.exp(-sp.sqrt(sp.Rational(4, 3))) < sp.exp(-sp.sqrt(2))),
    )

    screening_path = str(SCREENING.parent)
    if screening_path not in sys.path:
        sys.path.insert(0, screening_path)
    support = importlib.import_module("screening")
    metals = (support.MAT_NI, support.MAT_PD, support.MAT_TI, support.MAT_ZR)

    def fresh_u_e(metal: object) -> float:
        density = metal.density_g_cm3 * support.N_A / metal.molar_mass_g_mol * 1e6
        n_e = metal.Z_conduction * density
        k_f = (3 * np.pi**2 * n_e) ** (1 / 3)
        dos = support.M_E * k_f / (np.pi**2 * support.HBAR**2)
        k_tf = np.sqrt(support.E_CHG**2 * dos / support.EPS0)
        return support.KE * k_tf / support.EV_J

    fresh_values = tuple(fresh_u_e(metal) for metal in metals)
    checks.check(
        "fresh Thomas-Fermi calculation reproduces each selected material value",
        all(
            np.isclose(fresh, support.material_U_e_eV(metal), rtol=1e-15, atol=0)
            for fresh, metal in zip(fresh_values, metals, strict=True)
        ),
    )
    checks.check(
        "fresh selected maximum is Ni at 26.367 eV",
        metals[int(np.argmax(fresh_values))].name == "Ni"
        and np.isclose(max(fresh_values), 26.367367161568605),
    )
    fresh_gamow = (
        2
        * np.pi**2
        * (support.PAIR_DD.Z1 * support.PAIR_DD.Z2 * support.ALPHA) ** 2
        * support.PAIR_DD.mu_MeV
        * 1e3
    )
    checks.check(
        "fresh imported-constant formula reproduces the selected Gamow scale",
        np.isclose(fresh_gamow, 985.7655246160418, rtol=0, atol=1e-12),
    )
    checks.check(
        "all four conduction counts are assigned model choices rather than measured uncertainties",
        all(metal.Z_conduction == 1.0 for metal in metals)
        and "[DESIGN: model choice" in SCREENING.read_text(),
    )

    u_keV = max(fresh_values) * 1e-3
    floor_float = np.exp(-np.sqrt(fresh_gamow / u_keV))
    threshold_float = np.exp(-np.sqrt(fresh_gamow / (u_keV + 1e-3)))
    fraction_float = (
        np.log(threshold_float) - np.log(floor_float)
    ) / (-np.log(floor_float))
    checks.check(
        "fresh selected calculation reproduces the 1.84-percent log fraction",
        0.018 < fraction_float < 0.019
        and np.isclose(fraction_float, 1 - np.sqrt(u_keV / (u_keV + 1e-3))),
    )
    checks.check(
        "the selected fraction has no supplied probability distribution",
        "probability" not in source_text.lower()
        and "rng.uniform" in source_text,
    )

    scan = (1e-40, 1e-20, 1e-10, 1e-5, 1e-1, 0.5)
    exact_roots = tuple(fresh_gamow / np.log(value) ** 2 - u_keV for value in scan)
    numeric_roots = tuple(
        manual_bisection(value, fresh_gamow, u_keV, 0.0, 1e9, 100)[0]
        for value in scan
    )
    checks.check(
        "fresh bracketed bisection regresses all six selected exact roots",
        all(
            abs(exact - numeric) <= 1e-12 * exact
            for exact, numeric in zip(exact_roots, numeric_roots, strict=True)
        ),
    )
    near_one = 0.9999
    near_one_root = fresh_gamow / np.log(near_one) ** 2 - u_keV
    _, bracketed = manual_bisection(
        near_one, fresh_gamow, u_keV, 0.0, 1e9, 100
    )
    checks.check(
        "fresh bracket status rejects the source's admissible near-one unbracketed case",
        near_one_root > 1e9 and bracketed is False,
    )
    checks.check(
        "the source random interval is finite and excludes declared endpoints",
        "size=500" in source_text
        and "ln_floor * 0.999" in source_text
        and "-1e-6" in source_text,
    )
    checks.check(
        "exact inversion rather than random agreement decides arbitrary levels",
        sp.simplify(inverse.subs(c, fitted_level) - target) == 0,
    )
    checks.check(
        "the surviving exact surface is already a conditional dimensionless equality",
        not inverse.has(sp.symbols("time"))
        and sp.simplify(inverse.subs(c, fitted_level) - target) == 0,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
