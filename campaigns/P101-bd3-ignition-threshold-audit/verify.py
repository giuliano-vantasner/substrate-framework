"""Primary exact verifier for the P101 BD3 threshold-composition audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.coherence_gates import (
    continuous_population_threshold,
    population_activation_scale,
)
from substrate_framework.radial_energy import (
    capillary_barrier_height,
    quadratic_capillary_identifiability_ledger,
    quadratic_loading_area_drive,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-28/"
    "bridge_BD3_ignition_thresholds.py"
)
SOURCE_SHA256 = "8a8f2138c548d3ed90785fc3ea82302d39d71d4832cb3761f429938d9b94b950"
CONTRACT_SHA256 = "6d8674c52e6542f061628b6fcaf5dcf8c80cdcae3cc7e2403232c27223ab1227"
FREEZE_SHA256 = "55943985b5b4415eb18fd1a89fc3f16541c545f8d7a7fde67e809726ae72b023"


def _contract_path() -> Path:
    candidates = (
        Path("campaigns/P101-bd3-ignition-threshold-audit/proposal.yaml"),
        Path("proposals/P101-bd3-ignition-threshold-audit/proposal.yaml"),
    )
    return next(path for path in candidates if path.exists())


def _claim(claim_id: str) -> dict[str, object]:
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    return next(claim for claim in registry["claims"] if claim["id"] == claim_id)


def _log_elasticity(expression: sp.Expr, variable: sp.Symbol) -> sp.Expr:
    return sp.simplify(variable * sp.diff(expression, variable) / expression)


def main() -> int:
    checks = CheckLedger("P101")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash is pinned and BD3 remains outside the compatibility overlay",
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
        "pre-source commitment is immutable",
        hashlib.sha256(freeze_path.read_bytes()).hexdigest() == FREEZE_SHA256,
    )
    source_checks = sorted(
        (
            node
            for node in ast.walk(source_tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
        ),
        key=lambda node: node.lineno,
    )
    checks.check(
        "source has sixteen literal checks and a dynamic terminal tally",
        len(source_checks) == 16
        and 'print(f"\\nALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "exact source and campaign use no NumPy quadrature alias",
        all(
            alias not in source_text
            for alias in ("np." + "trapz", "np." + "trapezoid")
        ),
    )

    barrier, theta = sp.symbols("E theta", positive=True)
    visibility = sp.Symbol("V", positive=True)
    threshold = continuous_population_threshold(barrier, theta, visibility)
    expected_threshold = sp.simplify(
        (
            sp.sqrt((1 - visibility) ** 2 + 4 * visibility * barrier / theta)
            - (1 - visibility)
        )
        / (2 * visibility)
    )
    checks.check(
        "canonical general-coherence threshold is the positive quadratic root",
        threshold == expected_threshold
        and sp.simplify(
            theta
            * threshold
            * (1 + (threshold - 1) * visibility)
            - barrier
        )
        == 0,
    )
    incoherent = continuous_population_threshold(barrier, theta, 0)
    coherent = continuous_population_threshold(barrier, theta, 1)
    checks.check(
        "endpoint thresholds are the already accepted C-COH-001 formulas",
        incoherent == barrier / theta
        and coherent == sp.sqrt(barrier / theta),
    )
    checks.check(
        "accepted registry already owns the general and endpoint threshold surface",
        "unique positive continuous crossing" in _claim("C-COH-001")["statement"]
        and "integer population threshold requires" in _claim("C-COH-001")["assumptions"][3],
    )
    checks.mutation_sensitive(
        "linear and square-root endpoint branches are load bearing",
        lambda candidate: candidate == (coherent, incoherent),
        (sp.sqrt(barrier / theta), barrier / theta),
        (
            (barrier / theta, sp.sqrt(barrier / theta)),
            (sp.sqrt(barrier) / theta, barrier / theta),
            (sp.sqrt(barrier / theta), sp.sqrt(barrier / theta)),
        ),
    )

    ratio_coordinate = sp.Symbol("x", positive=True)
    coherent_x = sp.sqrt(ratio_coordinate)
    incoherent_x = ratio_coordinate
    checks.check(
        "endpoint ordering has greater-than equal and less-than one regimes",
        coherent_x.subs(ratio_coordinate, 4) < incoherent_x.subs(ratio_coordinate, 4)
        and coherent_x.subs(ratio_coordinate, 1) == incoherent_x.subs(ratio_coordinate, 1)
        and coherent_x.subs(ratio_coordinate, sp.Rational(1, 4))
        > incoherent_x.subs(ratio_coordinate, sp.Rational(1, 4)),
    )
    fourth_condition = ast.unparse(source_checks[3].args[1])
    checks.check(
        "source's less-than-one label is backed only by an identity check",
        "< 1" in ast.literal_eval(source_checks[3].args[0])
        and "theta1 < E_star" not in fourth_condition
        and "E_star > theta1" not in fourth_condition,
    )
    checks.mutation_sensitive(
        "the ratio-regime condition is load bearing",
        lambda candidate: bool(candidate.subs(ratio_coordinate, 4) < 1)
        and bool(candidate.subs(ratio_coordinate, sp.Rational(1, 4)) > 1),
        1 / sp.sqrt(ratio_coordinate),
        (sp.sqrt(ratio_coordinate), sp.Integer(1)),
    )

    tension, coupling, amplitude, wave, thickness = sp.symbols(
        "T g A k l_m", positive=True
    )
    drive = quadratic_loading_area_drive(coupling, amplitude, wave, thickness)
    composed_barrier = capillary_barrier_height(tension, drive)
    expected_barrier = 2 * sp.pi * tension**2 / (
        coupling * amplitude**2 * wave**2 * thickness
    )
    checks.check(
        "canonical C-RG-002 composition reproduces the source barrier exactly",
        sp.simplify(composed_barrier - expected_barrier) == 0,
    )
    checks.mutation_sensitive(
        "capillary factor two is load bearing",
        lambda candidate: sp.simplify(candidate - expected_barrier) == 0,
        composed_barrier,
        (composed_barrier / 2, 2 * composed_barrier, composed_barrier / sp.pi),
    )
    composed_coherent = sp.simplify(
        continuous_population_threshold(composed_barrier, theta, 1)
    )
    composed_incoherent = sp.simplify(
        continuous_population_threshold(composed_barrier, theta, 0)
    )
    checks.check(
        "source-style thresholds are canonical function composition with free theta",
        sp.simplify(composed_coherent**2 - composed_incoherent) == 0
        and theta in composed_coherent.free_symbols
        and theta in composed_incoherent.free_symbols,
    )
    variables = (tension, coupling, amplitude, wave, thickness, theta)
    coherent_elasticities = tuple(
        _log_elasticity(composed_coherent, variable) for variable in variables
    )
    incoherent_elasticities = tuple(
        _log_elasticity(composed_incoherent, variable) for variable in variables
    )
    checks.check(
        "exact endpoint chain-rule elasticities cover every displayed input",
        coherent_elasticities
        == (
            1,
            sp.Rational(-1, 2),
            -1,
            -1,
            sp.Rational(-1, 2),
            sp.Rational(-1, 2),
        )
        and incoherent_elasticities == (2, -1, -2, -2, -1, -1),
    )
    checks.check(
        "source samples only three signs at one substituted point",
        source_text.count("float(") == 5
        and "dNinc_dk" not in source_text
        and all(name not in source_text for name in ("dNcoh_dg", "dNcoh_dl", "dNcoh_dtheta")),
    )

    scale = sp.Symbol("lambda", positive=True)
    checks.check(
        "common energy-coordinate rescaling preserves every threshold",
        sp.simplify(
            continuous_population_threshold(scale * barrier, scale * theta, visibility)
            - threshold
        )
        == 0
        and sp.simplify(
            continuous_population_threshold(scale * barrier, scale * theta, 0)
            - incoherent
        )
        == 0,
    )
    checks.check(
        "rescaling theta alone changes both endpoint coordinates",
        sp.simplify(
            continuous_population_threshold(barrier, scale * theta, 1)
            / coherent
        )
        == 1 / sp.sqrt(scale)
        and sp.simplify(
            continuous_population_threshold(barrier, scale * theta, 0)
            / incoherent
        )
        == 1 / scale,
    )
    checks.mutation_sensitive(
        "paired normalization rescaling is load bearing",
        lambda pair: sp.simplify(pair[0] / pair[1] - barrier / theta) == 0,
        (scale * barrier, scale * theta),
        ((scale * barrier, theta), (barrier, scale * theta)),
    )
    log_matrix = sp.Matrix(
        [
            [1, sp.Rational(-1, 2), -1, -1, sp.Rational(-1, 2), sp.Rational(-1, 2)],
            [2, -1, -2, -2, -1, -1],
        ]
    )
    threshold_nullspace = log_matrix.nullspace()
    checks.check(
        "the two endpoint readings have rank one and identify no constituent",
        log_matrix.rank() == 1
        and len(threshold_nullspace) == 5
        and all(
            any(vector[index] != 0 for vector in threshold_nullspace)
            for index in range(log_matrix.cols)
        ),
    )
    barrier_ledger = quadratic_capillary_identifiability_ledger()
    checks.check(
        "composed thresholds cannot exceed the accepted barrier identifiability ceiling",
        barrier_ledger.barrier_only_rank == 1
        and barrier_ledger.barrier_only_coordinate_identifiable == (False,) * 5,
    )
    target = sp.Symbol("n_target", positive=True)
    checks.check(
        "the free per-source scale realizes arbitrary endpoint thresholds",
        sp.simplify(
            continuous_population_threshold(barrier, barrier / target, 0)
            - target
        )
        == 0
        and sp.simplify(
            continuous_population_threshold(barrier, barrier / target**2, 1)
            - target
        )
        == 0,
    )

    general_example = continuous_population_threshold(40, 1, sp.Rational(1, 2))
    checks.check(
        "integer thresholds require a separately declared ceiling operation",
        sp.ceiling(continuous_population_threshold(40, 1, 1)) == 7
        and sp.ceiling(continuous_population_threshold(40, 1, 0)) == 40
        and sp.ceiling(general_example) == 9,
    )
    general_count = sp.ceiling(general_example)
    checks.check(
        "the declared integer ceiling brackets the general-coherence crossing",
        population_activation_scale(general_count - 1, 1, sp.Rational(1, 2)) < 40
        and population_activation_scale(general_count, 1, sp.Rational(1, 2)) >= 40,
    )
    checks.check(
        "subunit continuous roots collapse to one positive integer source",
        continuous_population_threshold(1, 4, 0) == sp.Rational(1, 4)
        and continuous_population_threshold(1, 4, 1) == sp.Rational(1, 2)
        and sp.ceiling(continuous_population_threshold(1, 4, 0)) == 1
        and sp.ceiling(continuous_population_threshold(1, 4, 1)) == 1,
    )

    count = sp.Integer(10)
    critical_visibility = sp.simplify((sp.Integer(40) / count - 1) / (count - 1))
    checks.check(
        "the source discriminating example has an exact one-third coherence boundary",
        critical_visibility == sp.Rational(1, 3)
        and population_activation_scale(count, 1, critical_visibility) == 40
        and population_activation_scale(count, 1, 0) < 40
        and population_activation_scale(count, 1, 1) > 40,
    )
    checks.mutation_sensitive(
        "incoherent linear scaling is load bearing",
        lambda candidate: candidate == population_activation_scale(count, 1, 0),
        count,
        (count**2, 2 * count, count + 1),
    )
    checks.check(
        "source guard booleans establish algebraic comparisons rather than event dynamics",
        "def fabricated_incoherent_ignition" in source_text
        and "return THETA1*Nv**2 >= E_STAR" in source_text
        and not any(
            token in source_text
            for token in ("solve_ivp", "solve_bvp", "Langevin", "transition_rate", "cross_section")
        ),
    )

    theta_check = ast.unparse(source_checks[4].args[1])
    checks.check(
        "source hbar-frequency identification is a constructed tautology",
        "theta1_framework == hbar * omega_b" == theta_check
        and "theta1 = theta1_framework" not in source_text
        and "sp.Eq(theta1, theta1_framework)" not in source_text,
    )
    checks.check(
        "accepted claims contain no per-breather hbar-frequency population map",
        "hbar" not in _claim("C-SG-017")["statement"].lower()
        and "theta>0" in _claim("C-COH-001")["statement"]
        and "Calling Theta an energy or temperature"
        in _claim("C-COH-001")["assumptions"][4]
        and "k-omega dispersion" in _claim("C-RG-002")["statement"],
    )
    checks.check(
        "symbol presence cannot establish an isotope shift or k-omega law",
        "N_coh_fw.has(omega_b)" in source_text
        and "k~omega" in source_text
        and "omega_b" not in sp.srepr(composed_barrier)
        and "hbar" not in sp.srepr(composed_barrier),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
