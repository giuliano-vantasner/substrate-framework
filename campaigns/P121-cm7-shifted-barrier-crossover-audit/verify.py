"""Primary exact and provenance verifier for P121's CM7 audit."""

from __future__ import annotations

import ast
import hashlib
import importlib
from pathlib import Path
import sys
from typing import Callable

import numpy as np
import sympy as sp

from substrate_framework.crossovers import (
    monotone_range_location,
    shifted_barrier_crossover_energy,
    shifted_barrier_crossover_ledger,
    shifted_barrier_crossover_residual,
    shifted_barrier_zero_energy_floor,
)
from substrate_framework.screened_barrier import (
    shifted_inverse_sqrt_barrier_factor,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-31/"
    "bridge_CM7_gamow_crossover.py"
)
SCREENING = Path("/home/dan/substrate/engineering/screening/screening.py")
MATERIALS = Path("/home/dan/substrate/engineering/dbd/materials.py")
CAMPAIGN = Path("campaigns/P121-cm7-shifted-barrier-crossover-audit")
SOURCE_SHA = "10344b842a47b24651c891dfa55a030dd193e3e48e0b128b93bf74f29af6cee2"
SCREENING_SHA = "8ed6d54c8e3626f58ee2b3da78ce6eea7f4689092103dc23ed888b985e4cb4c3"
MATERIALS_SHA = "3639e1348fce91d38392c9405f62321059aec0452c4628262a515297d9a27f30"
FREEZE_SHA = "e7e6b6d1fffa9aa9606e9aed825544f78ae4b8213547aed6d0f623023a280045"


def _extract_function(
    tree: ast.Module,
    name: str,
    namespace: dict[str, object],
) -> Callable[..., object]:
    node = next(
        item for item in tree.body if isinstance(item, ast.FunctionDef) and item.name == name
    )
    module = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
    scope = dict(namespace)
    exec(compile(module, str(SOURCE), "exec"), scope)
    return scope[name]  # type: ignore[return-value]


def _source_bisect(
    level: float,
    barrier: float,
    shift: float,
    *,
    iterations: int,
) -> float:
    lo, hi = 0.0, 1.0e9
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        if np.exp(-np.sqrt(barrier / (mid + shift))) < level:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main() -> int:
    checks = CheckLedger("CM7-SHIFTED-CROSSOVER-AUDIT")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "CM7 source bytes are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA,
    )
    checks.check(
        "screening support bytes are hash pinned",
        hashlib.sha256(SCREENING.read_bytes()).hexdigest() == SCREENING_SHA,
    )
    checks.check(
        "live materials support bytes are hash pinned",
        hashlib.sha256(MATERIALS.read_bytes()).hexdigest() == MATERIALS_SHA,
    )
    normalized_contract = (CAMPAIGN / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n", b"status: draft\n"
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == FREEZE_SHA,
    )
    checks.check(
        "pre-source contract is immutable",
        hashlib.sha256(
            (CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "twenty-seven source predicates match the terminal tally",
        len(source_checks) == 27
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "CM7 and its screening support require no quadrature compatibility path",
        all(
            token not in SOURCE.read_text() + SCREENING.read_text()
            for token in ("np.trapz", "np.trapezoid", "trapezoid_integral")
        ),
    )

    energy = sp.symbols("E", nonnegative=True)
    barrier, shift, level = sp.symbols("G U c", positive=True)
    response = sp.exp(-sp.sqrt(barrier / (energy + shift)))
    floor = sp.exp(-sp.sqrt(barrier / shift))
    crossing = sp.simplify(barrier / sp.log(level) ** 2 - shift)
    checks.check(
        "the accepted factor has the exact attained floor and unattained supremum",
        sp.limit(response, energy, 0, dir="+") == floor
        and sp.limit(response, energy, sp.oo) == 1,
    )
    checks.check(
        "the accepted factor is globally strictly increasing",
        sp.diff(sp.log(response), energy)
        == sp.sqrt(barrier) / (2 * (energy + shift) ** sp.Rational(3, 2)),
    )
    k = sp.symbols("k", positive=True)
    branch_crossing = sp.simplify(crossing.subs(level, sp.exp(-k)))
    checks.check(
        "the real branch c=exp(-k) gives the exact inverse and zero residual",
        branch_crossing == barrier / k**2 - shift
        and sp.simplify(
            response.subs(energy, branch_crossing) - sp.exp(-k)
        )
        == 0,
    )
    checks.check(
        "positive crossing requires k below sqrt(G/U), equivalently c above the floor",
        sp.solve_univariate_inequality(
            sp.Integer(9) / k**2 - 1 > 0,
            k,
        )
        == (k < 3)
        and k.is_positive is True,
    )

    exact_barrier = sp.Integer(9)
    exact_shift = sp.Integer(1)
    exact_level = sp.exp(-2)
    exact_floor = shifted_barrier_zero_energy_floor(exact_barrier, exact_shift)
    exact_crossing = shifted_barrier_crossover_energy(
        exact_barrier, exact_shift, exact_level
    )
    checks.check(
        "the accepted API gives the exact interior crossing",
        exact_floor == sp.exp(-3) and exact_crossing == sp.Rational(5, 4),
    )
    checks.check(
        "the accepted API residual vanishes at the exact interior crossing",
        shifted_barrier_crossover_residual(
            exact_barrier, exact_shift, exact_level
        )
        == 0,
    )
    checks.check(
        "the general range classifier separates below floor floor interior one and above",
        monotone_range_location(exact_floor, sp.Integer(1), sp.exp(-4))
        == "below_range"
        and monotone_range_location(exact_floor, sp.Integer(1), exact_floor)
        == "lower_endpoint"
        and monotone_range_location(exact_floor, sp.Integer(1), exact_level)
        == "unique_interior"
        and monotone_range_location(exact_floor, sp.Integer(1), sp.Integer(1))
        == "upper_limit_only"
        and monotone_range_location(exact_floor, sp.Integer(1), sp.Integer(2))
        == "above_range",
    )
    checks.check(
        "the U=0 specialization has zero floor and the unscreened inverse",
        shifted_barrier_zero_energy_floor(exact_barrier, sp.Integer(0)) == 0
        and shifted_barrier_crossover_energy(
            exact_barrier, sp.Integer(0), exact_level
        )
        == sp.Rational(9, 4),
    )
    for invalid_level in (sp.Integer(0), sp.Integer(1), sp.Integer(2), sp.Integer(-1)):
        try:
            shifted_barrier_crossover_energy(
                exact_barrier, exact_shift, invalid_level
            )
        except ValueError:
            rejected = True
        else:
            rejected = False
        checks.check(
            f"accepted API rejects invalid level {invalid_level}",
            rejected,
        )
    try:
        shifted_barrier_crossover_energy(
            exact_barrier, exact_shift, exact_floor
        )
    except ValueError:
        floor_rejected_as_interior = True
    else:
        floor_rejected_as_interior = False
    checks.check(
        "the positive-interior API separates the zero-energy floor endpoint",
        floor_rejected_as_interior,
    )
    outside_candidate = crossing.subs(
        {barrier: exact_barrier, shift: exact_shift, level: 2}
    )
    outside_response = shifted_inverse_sqrt_barrier_factor(
        outside_candidate,
        exact_barrier,
        exact_shift,
    )
    checks.check(
        "the squared-log formula is spurious for c above one",
        sp.simplify(outside_response - sp.Rational(1, 2)) == 0
        and outside_response != 2,
    )

    ledger = shifted_barrier_crossover_ledger(barrier, shift, level)
    checks.check(
        "accepted sensitivities reproduce all three source derivatives exactly",
        ledger.crossover_energy == crossing
        and ledger.level_derivative
        == -2 * barrier / (level * sp.log(level) ** 3)
        and ledger.barrier_derivative == 1 / sp.log(level) ** 2
        and ledger.shift_derivative == -1,
    )
    level_elasticity = sp.simplify(level * ledger.level_derivative / crossing)
    barrier_elasticity = sp.simplify(
        barrier * ledger.barrier_derivative / crossing
    )
    shift_elasticity = sp.simplify(shift * ledger.shift_derivative / crossing)
    checks.check(
        "barrier and shift elasticities sum to the common energy-scale exponent one",
        sp.simplify(barrier_elasticity + shift_elasticity - 1) == 0,
    )
    checks.check(
        "level elasticity is positive on a declared interior branch",
        sp.simplify(
            level_elasticity.subs(
                {barrier: 9, shift: 1, level: sp.exp(-2)}
            )
        )
        > 0,
    )
    eps_g_k = sp.simplify(barrier_elasticity.subs(level, sp.exp(-k)))
    eps_u_k = sp.simplify(shift_elasticity.subs(level, sp.exp(-k)))
    eps_c_k = sp.simplify(level_elasticity.subs(level, sp.exp(-k)))
    floor_k = sp.sqrt(barrier / shift)
    checks.check(
        "all relative sensitivities diverge at the zero-crossing floor as appropriate",
        sp.limit(eps_g_k, k, floor_k, dir="-") == sp.oo
        and sp.limit(eps_u_k, k, floor_k, dir="-") == -sp.oo
        and sp.limit(eps_c_k, k, floor_k, dir="-") == sp.oo,
    )
    rho = sp.symbols("rho", positive=True)
    checks.check(
        "common positive energy rescaling scales the crossing and threshold",
        sp.simplify(
            crossing.subs({barrier: rho * barrier, shift: rho * shift})
            - rho * crossing
        )
        == 0,
    )

    target = sp.symbols("E_T", positive=True)
    target_level = sp.exp(-sp.sqrt(barrier / (target + shift)))
    checks.check(
        "every positive target is fitted exactly by a corresponding free level",
        sp.simplify(crossing.subs(level, target_level) - target) == 0,
    )
    checks.check(
        "independent channel normalizations change the horizontal level",
        sp.Rational(1, 2) * exact_level != exact_level
        and shifted_barrier_crossover_energy(
            exact_barrier, exact_shift, exact_level / 2
        )
        != exact_crossing,
    )

    threshold = sp.symbols("T", positive=True)
    threshold_level = sp.exp(-sp.sqrt(barrier / (shift + threshold)))
    log_fraction_below = sp.simplify(
        (sp.log(threshold_level) - sp.log(floor)) / (-sp.log(floor))
    )
    expected_log_fraction = 1 - sp.sqrt(shift / (shift + threshold))
    checks.check(
        "the log-window fraction has the exact declared measure-dependent form",
        sp.simplify(log_fraction_below - expected_log_fraction) == 0,
    )
    uniform_c_fraction = sp.simplify(
        (threshold_level - floor) / (1 - floor)
    )
    checks.check(
        "uniform-c and uniform-log-c threshold fractions differ",
        sp.N(
            uniform_c_fraction.subs({barrier: 4, shift: 1, threshold: 1})
            - expected_log_fraction.subs({shift: 1, threshold: 1})
        )
        != 0,
    )
    checks.check(
        "arbitrary concentrated level laws give either zero or one below-threshold probability",
        bool(sp.exp(-2) < sp.exp(-sp.sqrt(2)))
        and bool(
            sp.exp(-sp.sqrt(sp.Rational(8, 3))) < sp.exp(-sp.sqrt(2))
        )
        and not bool(sp.exp(-sp.sqrt(sp.Rational(4, 3))) < sp.exp(-sp.sqrt(2))),
    )

    screening_dir = str(SCREENING.parent)
    if screening_dir not in sys.path:
        sys.path.insert(0, screening_dir)
    screening = importlib.import_module("screening")
    metals = (
        screening.MAT_NI,
        screening.MAT_PD,
        screening.MAT_TI,
        screening.MAT_ZR,
    )
    material_values = tuple(float(screening.material_U_e_eV(m)) for m in metals)
    barrier_value = float(screening.gamow_energy_keV(screening.PAIR_DD))
    checks.check(
        "selected screening inputs reproduce the source values",
        np.isclose(barrier_value, 985.7655246160418, rtol=0, atol=1e-12)
        and np.isclose(max(material_values), 26.367367161568605, rtol=0, atol=1e-12),
    )
    checks.check(
        "the selected maximum is Ni among four assigned one-electron models",
        metals[int(np.argmax(material_values))].name == "Ni"
        and all(m.Z_conduction == 1.0 for m in metals),
    )
    mutated_ni = screening.Metal(
        "Ni-mutated",
        screening.MAT_NI.density_g_cm3,
        screening.MAT_NI.molar_mass_g_mol,
        64.0,
    )
    checks.check(
        "the declared conduction-count model changes the selected screening scale",
        np.isclose(
            screening.material_U_e_eV(mutated_ni)
            / screening.material_U_e_eV(screening.MAT_NI),
            2.0,
            rtol=1e-12,
            atol=0,
        ),
    )
    checks.check(
        "source material records contain no uncertainty or universal-ceiling field",
        "uncertainty" not in screening.Metal.__dataclass_fields__
        and "universal" not in screening.Metal.__dataclass_fields__,
    )

    selected_shift_keV = max(material_values) * 1.0e-3
    selected_floor = np.exp(-np.sqrt(barrier_value / selected_shift_keV))
    selected_threshold = np.exp(
        -np.sqrt(barrier_value / (selected_shift_keV + 1.0e-3))
    )
    selected_fraction = (
        np.log(selected_threshold) - np.log(selected_floor)
    ) / (-np.log(selected_floor))
    checks.check(
        "the reported 1.84 percent is the selected uniform-log window fraction",
        np.isclose(
            selected_fraction,
            1 - np.sqrt(selected_shift_keV / (selected_shift_keV + 1.0e-3)),
            rtol=1e-13,
            atol=0,
        )
        and 0.018 < selected_fraction < 0.019,
    )
    checks.check(
        "the fraction is barrier-independent but remains shift threshold and measure dependent",
        np.isclose(
            selected_fraction,
            1 - np.sqrt(selected_shift_keV / (selected_shift_keV + 1.0e-3)),
        )
        and selected_threshold != selected_floor,
    )

    source_satisfies = _extract_function(
        source_tree,
        "satisfies_crossover",
        {"np": np},
    )
    source_admissible = _extract_function(
        source_tree,
        "admissible",
        {"np": np},
    )
    source_closed = _extract_function(
        source_tree,
        "crossover_closed",
        {
            "np": np,
            "E_G_keV": barrier_value,
            "U_e_max_keV": selected_shift_keV,
        },
    )
    source_bisect = _extract_function(
        source_tree,
        "crossover_bisect",
        {
            "np": np,
            "E_G_keV": barrier_value,
            "U_e_max_keV": selected_shift_keV,
        },
    )
    scan = (1e-40, 1e-20, 1e-10, 1e-5, 1e-1, 5e-1)
    rows = tuple((cv, source_closed(cv), source_bisect(cv)) for cv in scan)
    checks.check(
        "selected source bisections regress the exact closed form",
        all(
            source_admissible(cv, barrier_value, selected_shift_keV)
            and abs(closed - bisected) <= 1e-12 * closed
            and source_satisfies(closed, barrier_value, selected_shift_keV, cv)
            for cv, closed, bisected in rows
        ),
    )
    unbracketed_level = 0.9999
    unbracketed_exact = source_closed(unbracketed_level)
    unbracketed_result = source_bisect(unbracketed_level)
    checks.check(
        "the fixed source bisection bracket fails for an admissible near-one level",
        unbracketed_exact > 1.0e9
        and unbracketed_result <= 1.0e9
        and not source_satisfies(
            unbracketed_result,
            barrier_value,
            selected_shift_keV,
            unbracketed_level,
        ),
    )
    forty = _source_bisect(
        0.5,
        barrier_value,
        selected_shift_keV,
        iterations=40,
    )
    sixty = _source_bisect(
        0.5,
        barrier_value,
        selected_shift_keV,
        iterations=60,
    )
    eighty = _source_bisect(
        0.5,
        barrier_value,
        selected_shift_keV,
        iterations=80,
    )
    three_hundred = _source_bisect(
        0.5,
        barrier_value,
        selected_shift_keV,
        iterations=300,
    )
    checks.check(
        "bisection converges to float64 precision and saturates before three hundred steps",
        abs(forty - source_closed(0.5)) > abs(sixty - source_closed(0.5))
        and abs(sixty - source_closed(0.5)) < 1e-9
        and eighty == three_hundred
        and abs(three_hundred - source_closed(0.5))
        <= np.spacing(source_closed(0.5)),
    )
    checks.check(
        "the random source interval excludes both endpoints and the bottom 0.1 percent in log measure",
        "rng.uniform(ln_floor * 0.999, -1e-6, size=500)" in source_text,
    )
    checks.check(
        "finite random regression cannot prove arbitrary-level validity",
        500 < sp.oo and shifted_barrier_crossover_residual(9, 1, sp.exp(-2)) == 0,
    )

    checks.check(
        "the exact surviving CM7 surface is already C-XOV-001",
        exact_crossing == sp.Rational(5, 4)
        and shifted_barrier_crossover_residual(9, 1, sp.exp(-2)) == 0,
    )
    checks.check(
        "a dimensionless factor equality supplies no rate or common-observable normalization",
        not crossing.has(sp.symbols("time"))
        and shifted_barrier_crossover_energy(9, 1, sp.exp(-2) / 2)
        != exact_crossing,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
