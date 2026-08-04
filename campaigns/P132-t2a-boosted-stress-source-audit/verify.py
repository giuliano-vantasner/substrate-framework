"""Primary exact and source-ceiling verifier for P132/T2A."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.sine_gordon import (
    breather_energy,
    breather_field,
    boosted_breather_energy_momentum,
    boosted_breather_phase_components,
    lorentz_factor,
    sine_gordon_stress_divergence,
    sine_gordon_stress_tensor_contravariant,
    sine_gordon_stress_tensor_covariant,
)
from substrate_framework.verification import CheckLedger


CAMPAIGN = Path("campaigns/P132-t2a-boosted-stress-source-audit")
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-2/"
    "bridge_T2A_moving_source.py"
)
SOURCE_SHA = "669803de1403c8ca66e399aa4b7c0e762447e40df7c241fe530a6b4e06dde70a"
FREEZE_SHA = "3e138cacdb5c7d67ce50b6dc5b4d94b20a5663827143bf2f163157413bf71007"
NOTE13 = Path(
    "/home/dan/substrate/soliton-shadow/cut-and-project-shadow/"
    "13-dynamic-analog-einstein-sourcing.md"
)
NOTE13_SHA = "10ae83e208af25dc95a148bbe954574632ea6db7d69099219d32b18ed11f7278"
DILATON = Path(
    "/home/dan/substrate/soliton-shadow/cut-and-project-shadow/sympy/"
    "dynamic_analog_C_dilaton.py"
)
DILATON_SHA = "fc89e917be8cd17b9fe5993a2b59c988c74090ddbda482e31f86295f8cc9ca63"


def source_check_calls(tree: ast.AST) -> list[ast.Call]:
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]


def imported_modules(tree: ast.AST) -> set[str]:
    modules = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    modules.update(
        node.module or ""
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    )
    return modules


def assigned_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        names.update(
            target.id
            for target in targets
            if isinstance(target, ast.Name)
        )
    return names


def charge_predicate(candidate: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]) -> bool:
    energy, momentum, rest_energy, velocity = candidate
    gamma = 1 / sp.sqrt(1 - velocity**2)
    return bool(
        sp.simplify(energy - gamma * rest_energy) == 0
        and sp.simplify(momentum - gamma * rest_energy * velocity) == 0
        and sp.simplify(energy**2 - momentum**2 - rest_energy**2) == 0
    )


def main() -> int:
    checks = CheckLedger("T2A-BOOSTED-STRESS-SOURCE-AUDIT")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    tree = ast.parse(source_text)
    note_bytes = NOTE13.read_bytes()
    note_text = note_bytes.decode("utf-8")
    dilaton_bytes = DILATON.read_bytes()

    checks.check(
        "T2A source bytes are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA,
    )
    normalized_contract = (CAMPAIGN / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n", b"status: draft\n"
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == FREEZE_SHA,
    )
    checks.check(
        "immutable preregistration remains byte identical",
        hashlib.sha256(
            (CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    checks.check(
        "twelve source predicates match the terminal tally",
        len(source_check_calls(tree)) == 12,
    )
    checks.check(
        "the executable import surface is SymPy and mpmath only",
        imported_modules(tree) == {"sympy", "mpmath"},
    )
    checks.check(
        "T2A has no NumPy trapezoid compatibility path",
        all(
            token not in source_text
            for token in (
                "np.trapz",
                "np.trapezoid",
                "trapezoid_integral",
                "numpy",
            )
        ),
    )
    checks.check(
        "the hidden local dilaton import is separately hash pinned",
        hashlib.sha256(note_bytes).hexdigest() == NOTE13_SHA
        and hashlib.sha256(dilaton_bytes).hexdigest() == DILATON_SHA,
    )

    t, x, velocity, gamma = sp.symbols("t x v gamma", real=True)
    tau = gamma * (t - velocity * x)
    xi = gamma * (x - velocity * t)
    time_jacobian = sp.Matrix([sp.diff(tau, t), sp.diff(xi, t)])
    space_jacobian = sp.Matrix([sp.diff(tau, x), sp.diff(xi, x)])
    principal_operator = sp.simplify(
        time_jacobian * time_jacobian.T
        - space_jacobian * space_jacobian.T
    )
    checks.check(
        "the scalar pullback has the exact Lorentz wave-operator factor",
        sp.simplify(
            principal_operator
            - gamma**2 * (1 - velocity**2) * sp.diag(1, -1)
        )
        == sp.zeros(2),
    )
    checks.check(
        "the source uses the frozen scalar boost convention",
        "xi_rest = g_sym * (xc - v_sym * tc)" in source_text
        and "tau_rest = g_sym * (tc - v_sym * xc)" in source_text,
    )
    checks.check(
        "the source imposes the physical Lorentz shell",
        "g_of_v = 1 / sp.sqrt(1 - v_sym**2)" in source_text,
    )

    omega = sp.Rational(3, 5)
    speed = sp.Rational(4, 5)
    gamma_value = lorentz_factor(speed)
    rest_energy = breather_energy(omega)
    phase = boosted_breather_phase_components(omega, speed)
    energy, momentum = boosted_breather_energy_momentum(omega, speed)
    checks.check(
        "accepted phase components reproduce the exact source boost",
        phase == (gamma_value * omega, gamma_value * omega * speed),
    )
    checks.check(
        "accepted charges reproduce gamma times the rest energy",
        energy == gamma_value * rest_energy
        and momentum == gamma_value * rest_energy * speed,
    )
    checks.check(
        "the accepted energy-momentum norm is exact",
        sp.simplify(energy**2 - momentum**2 - rest_energy**2) == 0,
    )
    checks.check(
        "the rest and velocity-reversal limits are regular",
        boosted_breather_energy_momentum(omega, 0) == (rest_energy, 0)
        and boosted_breather_energy_momentum(omega, -speed)
        == (energy, -momentum),
    )
    checks.mutation_sensitive(
        "boosted charge transformation",
        charge_predicate,
        (energy, momentum, rest_energy, speed),
        (
            (rest_energy, rest_energy * speed, rest_energy, speed),
            (energy, -momentum, rest_energy, speed),
            (energy, momentum, 2 * rest_energy, speed),
        ),
    )
    checks.check(
        "the source detail mislabels the momentum enhancement as gamma squared",
        "(factor gamma^2" in source_text
        and sp.simplify(
            (momentum / (rest_energy * speed)).subs(speed, sp.Rational(4, 5))
        )
        == sp.Rational(5, 3)
        and gamma_value**2 == sp.Rational(25, 9),
    )

    generic = sp.Function("phi")(x, t)
    field_t = sp.diff(generic, t)
    field_x = sp.diff(generic, x)
    covariant = sine_gordon_stress_tensor_covariant(generic, x, t)
    contravariant = sine_gordon_stress_tensor_contravariant(generic, x, t)
    checks.check(
        "the covariant mixed component has the positive derivative product",
        covariant[0, 1] == field_t * field_x,
    )
    checks.check(
        "raising both indices flips the mixed-component sign",
        contravariant[0, 1] == -field_t * field_x
        and contravariant[1, 0] == -field_t * field_x,
    )
    checks.check(
        "the exact off-shell divergence remains the accepted residual factorization",
        sp.simplify(
            sine_gordon_stress_divergence(generic, x, t)
            - sp.Matrix(
                [
                    field_t
                    * (
                        sp.diff(generic, t, 2)
                        - sp.diff(generic, x, 2)
                        + sp.sin(generic)
                    ),
                    -field_x
                    * (
                        sp.diff(generic, t, 2)
                        - sp.diff(generic, x, 2)
                        + sp.sin(generic)
                    ),
                ]
            )
        )
        == sp.zeros(2, 1),
    )

    rest_breather = breather_field(x, t, omega)
    rest_mixed = sine_gordon_stress_tensor_covariant(rest_breather, x, t)[0, 1]
    counterpoint = sp.N(rest_mixed.subs({x: 1, t: 5 * sp.pi / 18}), 40)
    checks.check(
        "a standing breather has nonzero pointwise covariant mixed stress",
        abs(complex(counterpoint)) > 1e-6,
    )
    checks.check(
        "standing integrated momentum can vanish without pointwise mixed stress",
        boosted_breather_energy_momentum(omega, 0)[1] == 0
        and abs(complex(counterpoint)) > 1e-6,
    )
    checks.check(
        "the imported static metric equation conflicts with the standing local stress",
        "M_tx:  0" in note_text
        and "= κ T_tx" in note_text
        and abs(complex(counterpoint)) > 1e-6,
    )
    checks.check(
        "the source mislabels contravariant momentum density as covariant T_tx",
        "def dens_T0x" in source_text
        and "return -ut * ux" in source_text
        and "Moving: T_tx_v = -u_t u_x" in source_text,
    )
    source_assignments = assigned_names(tree)
    checks.check(
        "the alleged dilaton equation has no executable target field or coupling",
        "M_tx" not in source_assignments
        and "kappa" not in source_assignments
        and "T0x_moving" in source_assignments,
    )
    checks.check(
        "T2A names rather than executes its dilaton action dependency",
        "the dilaton action / M_munu = kappa" in source_text
        and imported_modules(tree) == {"sympy", "mpmath"},
    )
    source_vi = source_check_calls(tree)[10]
    vi_names = {node.id for node in ast.walk(source_vi.args[1]) if isinstance(node, ast.Name)}
    checks.check(
        "the dilaton predicate tests only a pointwise stress magnitude",
        vi_names == {"T0x_moving", "abs", "mp"},
    )

    e0, v, period = sp.symbols("E0 v T", positive=True)
    g = 1 / sp.sqrt(1 - v**2)
    p = g * e0 * v
    source_average = g**2 * v**2 * e0
    spacetime_numerator = g**2 * v**2 * e0 * period
    lab_period = g * period
    correct_average = sp.simplify(spacetime_numerator / lab_period)
    checks.check(
        "the lab-period Jacobian gives mean integrated stress v times momentum",
        sp.simplify(correct_average - v * p) == 0
        and correct_average == g * v**2 * e0,
    )
    checks.check(
        "T2A's spatial-stress formula carries one spurious gamma",
        sp.simplify(source_average / correct_average - g) == 0
        and sp.simplify(source_average - correct_average) != 0,
    )
    checks.check(
        "the source never numerically integrates its load-bearing Txx verdict",
        "integrate_x(dens_Txx" not in source_text
        and "avg_Txx_moving = g_s**2 * v_s**2 * E0_s" in source_text,
    )
    checks.check(
        "the omitted factor is exposed at the source high-speed test velocity",
        sp.simplify((source_average / correct_average).subs(v, sp.Rational(4, 5)))
        == sp.Rational(5, 3),
    )
    checks.check(
        "the corrected stress has the rest and low-velocity limits",
        sp.limit(correct_average, v, 0, dir="+") == 0
        and sp.limit(correct_average / (e0 * v**2), v, 0, dir="+") == 1,
    )
    checks.check(
        "the singular light-speed boundary is not admitted as a finite sample",
        sp.limit(correct_average**2, v, 1, dir="-") == sp.oo
        and sp.limit(1 / correct_average, v, 1, dir="-") == 0,
    )

    checks.check(
        "uniform translation supplies no acceleration by itself",
        sp.diff(v * t, t, 2) == 0,
    )
    checks.check(
        "the source's post-hoc radiation annotation is not executable dependency closure",
        "SINCE CLOSED by Phase 12" in source_text
        and imported_modules(tree) == {"sympy", "mpmath"},
    )
    checks.check(
        "the exact surviving surface is already governed by accepted claims",
        energy == gamma_value * rest_energy
        and momentum == gamma_value * rest_energy * speed
        and covariant[0, 1] == -contravariant[0, 1],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
