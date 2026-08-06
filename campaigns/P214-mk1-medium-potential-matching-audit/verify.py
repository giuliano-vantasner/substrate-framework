"""Primary exact verifier for the P214 MK1 potential-matching audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess

import sympy as sp
import yaml

from substrate_framework.bps_energy import (
    normalized_sqrt_potential_average,
    target_three_sphere_volume,
)
from substrate_framework.dimensional_sine_gordon import (
    dimensional_sine_gordon_coefficients,
    dimensional_sine_gordon_scales,
    rescale_dimensional_sine_gordon_coefficients,
)
from substrate_framework.explicit_breaking import (
    matched_local_curvature_potentials,
    periodic_potential_evidence,
    su2_trace_breaking_evidence,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-43/"
    "bridge_MK1_mu_from_medium_cosine.py"
)
SOURCE_SHA256 = "98ff5459ae3c6cb64a9a7632fbaa8613f1f5b1adb68419de25ffa06b1c3a3222"
FORMULA_FREEZE_SHA256 = "497b0d9f333c8e55e8a44dc34f9b9873ecc49d03d6c77b7531da9375e10ad8c6"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _claim_map() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())
    return {claim["id"]: claim for claim in registry["claims"]}


def main() -> int:
    checks = CheckLedger("P214")

    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    checks.check(
        "MK1 source hash is pinned",
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
        "source inventory separates seven predicates from one assertion",
        len(literal_checks) == 7
        and len(assertions) == 1
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )

    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "MK1 has no NumPy integration compatibility surface",
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
        "native source executes all seven runtime predicates cleanly",
        native.returncode == 0
        and native.stdout.count("  PASS\n") == 7
        and native.stdout.rstrip().endswith("ALL 7 CHECKS PASS"),
    )

    pion = sp.Symbol("pi", real=True)
    amplitude, scale, kinetic, multiplier, mass = sp.symbols(
        "A F K q m",
        positive=True,
    )
    periodic = periodic_potential_evidence(
        pion,
        amplitude,
        scale,
        kinetic,
        angle_multiplier=multiplier,
    )
    checks.check(
        "canonical periodic API derives the generalized mass operator",
        periodic.curvature_at_origin == amplitude * multiplier**2 / scale**2
        and periodic.generalized_mass_squared
        == amplitude * multiplier**2 / (kinetic * scale**2),
    )
    mu_bps = sp.Symbol("mu_BPS", positive=True)
    positive_solutions = sp.solve(
        sp.Eq(
            periodic.generalized_mass_squared.subs(amplitude, mu_bps**2),
            mass**2,
        ),
        mu_bps,
    )
    general_match = mass * scale * sp.sqrt(kinetic) / multiplier
    checks.check(
        "positive coefficient matching has one convention-covariant solution",
        len(positive_solutions) == 1
        and sp.simplify(positive_solutions[0] - general_match) == 0,
    )
    checks.check(
        "the MK1 q=2 K=1 specialization gives the advertised factor",
        sp.simplify(general_match.subs({multiplier: 2, kinetic: 1}) - mass * scale / 2)
        == 0,
    )
    checks.check(
        "angle and kinetic mutations change the solution when varied separately",
        sp.simplify(
            general_match.subs({multiplier: 1, kinetic: 1})
            - 2 * general_match.subs({multiplier: 2, kinetic: 1})
        )
        == 0
        and sp.simplify(
            general_match.subs({multiplier: 2, kinetic: 4})
            - 2 * general_match.subs({multiplier: 2, kinetic: 1})
        )
        == 0,
    )

    trace_q1 = su2_trace_breaking_evidence(
        pion,
        scale,
        1,
        scale**2 / 16,
        mass**2 * scale**2 / 8,
    )
    trace_q2 = su2_trace_breaking_evidence(
        pion,
        scale,
        2,
        scale**2 / 16,
        mass**2 * scale**2 / 8,
    )
    checks.check(
        "ANW trace pair exposes both coordinate kinetic coefficients",
        trace_q1.kinetic_coefficient == sp.Rational(1, 4)
        and trace_q2.kinetic_coefficient == 1,
    )
    checks.check(
        "matched q=1 and q=2 coordinates have the same generalized mass",
        trace_q1.generalized_mass_squared == mass**2
        and trace_q2.generalized_mass_squared == mass**2
        and trace_q1.generalized_mass_coordinate_residual == 0
        and trace_q2.generalized_mass_coordinate_residual == 0,
    )
    checks.check(
        "the trace convention fixes potential amplitude mu squared to m squared F squared over four",
        sp.simplify(trace_q2.potential - mass**2 * scale**2 * (1 - sp.cos(2 * pion / scale)) / 4)
        == 0
        and sp.simplify(mu_bps - mass * scale / 2).subs(mu_bps, mass * scale / 2)
        == 0,
    )
    mixed_pg2 = periodic_potential_evidence(
        pion,
        mass**2 * scale**2,
        scale,
        sp.Rational(1, 4),
        angle_multiplier=1,
    )
    checks.check(
        "the PG2 mixed amplitude and q=1 kinetic convention gives four times the target mass squared",
        mixed_pg2.generalized_mass_squared == 4 * mass**2,
    )

    curvature = sp.Symbol("h", positive=True)
    local_pair = matched_local_curvature_potentials(pion, curvature, scale)
    checks.check(
        "equal local curvature does not establish global potential equality",
        local_pair.hessian_difference_at_origin == 0
        and local_pair.periodic_shift_residual == 0
        and local_pair.quadratic_shift_residual != 0
        and local_pair.fourth_derivative_difference_at_origin != 0,
    )

    angle = sp.Symbol("chi", real=True)
    round_measure = 4 * sp.pi * sp.sin(angle) ** 2
    volume = sp.integrate(round_measure, (angle, 0, sp.pi))
    square_root = sp.sqrt(2) * sp.sin(angle / 2)
    weighted_integral = sp.integrate(
        round_measure * square_root,
        (angle, 0, sp.pi),
    )
    expected_average = 32 * sp.sqrt(2) / (15 * sp.pi)
    checks.check(
        "round S3 measure has the accepted exact volume",
        sp.simplify(volume - target_three_sphere_volume()) == 0,
    )
    checks.check(
        "supplied one-cosine potential has the exact P107 target average",
        sp.simplify(
            normalized_sqrt_potential_average(weighted_integral) - expected_average
        )
        == 0,
    )
    mutated_average = normalized_sqrt_potential_average(
        sp.integrate(
            round_measure * sp.sqrt(2) * sp.sin(angle),
            (angle, 0, sp.pi),
        )
    )
    checks.check(
        "a different supplied potential shape changes the target average",
        sp.simplify(mutated_average - expected_average) != 0,
    )

    e_sk = sp.Symbol("e", positive=True)
    length_unit = 2 / (e_sk * scale)
    reduced_coefficient = 4 * e_sk * mu_bps**2 * length_unit**3 / scale
    tail_mass = sp.simplify(sp.sqrt(reduced_coefficient / 2) / length_unit)
    checks.check(
        "the source radial tail expression reduces before any coefficient substitution",
        sp.simplify(tail_mass - 2 * mu_bps / scale) == 0,
    )
    tail_solutions = sp.solve(sp.Eq(tail_mass, mass), mu_bps)
    specialized_mass_solutions = [
        solution.subs({multiplier: 2, kinetic: 1})
        for solution in positive_solutions
    ]
    checks.check(
        "tail matching solves exactly the same coefficient equation as local mass matching",
        tail_solutions == specialized_mass_solutions
        and sp.simplify(tail_solutions[0] - mass * scale / 2) == 0,
    )
    checks.check(
        "the source wrong-factor tail guard is only a mutation of that same equation",
        sp.simplify(tail_mass.subs(mu_bps, mass * scale) - 2 * mass) == 0,
    )

    medium = dimensional_sine_gordon_coefficients(2, 8, 18)
    medium_scales = dimensional_sine_gordon_scales(medium)
    rescaled_medium = rescale_dimensional_sine_gordon_coefficients(medium, 5)
    rescaled_scales = dimensional_sine_gordon_scales(rescaled_medium)
    checks.check(
        "accepted medium gap is a coefficient ratio rather than its onsite coefficient",
        medium_scales.gap_frequency == 3
        and medium.onsite == 18
        and rescaled_medium.onsite == 90,
    )
    checks.check(
        "common medium rescaling preserves the gap while changing action normalization",
        rescaled_scales.gap_frequency == medium_scales.gap_frequency
        and rescaled_scales.signal_speed == medium_scales.signal_speed
        and rescaled_scales.energy == 5 * medium_scales.energy
        and rescaled_scales.action == 5 * medium_scales.action,
    )
    scale_a, scale_b = sp.symbols("F_a F_b", positive=True)
    coupling_a = medium_scales.gap_frequency * scale_a / 2
    coupling_b = medium_scales.gap_frequency * scale_b / 2
    checks.check(
        "one accepted medium admits distinct BPS couplings when the absent decay scale varies",
        sp.simplify(coupling_b.subs(scale_b, 2 * scale_a) - 2 * coupling_a) == 0,
    )

    claims = _claim_map()
    checks.check(
        "accepted periodic claim explicitly withholds physical and substrate maps",
        "derive no field ontology" in claims["C-BRK-001"]["statement"]
        and "substrate map" in claims["C-BRK-001"]["statement"],
    )
    checks.check(
        "accepted trace claim explicitly withholds coefficient and substrate realization",
        "derived coefficient" in claims["C-CHI-002"]["statement"]
        and "substrate realization" in claims["C-CHI-002"]["statement"],
    )
    checks.check(
        "accepted BPS claim supplies rather than selects potential and coupling",
        "select a potential or coupling" in claims["C-BPS-001"]["statement"],
    )
    checks.check(
        "accepted medium claim retains the common action scale and no material map",
        "common energy/action scale" in claims["C-MED-003"]["statement"]
        and "derive a material" in claims["C-MED-003"]["statement"],
    )

    post_delta = yaml.safe_load(
        (CAMPAIGN / "evidence/post-source-claim-delta.yaml").read_text()
    )
    checks.check(
        "nonduplication adjudication promotes no wrapper claim",
        post_delta["claim_decision"]["promoted_new_claims"] == []
        and post_delta["claim_decision"]["reserved_unpromoted_claims"]
        == ["C-BPS-004"],
    )
    checks.check(
        "source decomposition preserves the conditional exact ceiling and rejects physical overreach",
        "mu_BPS=m_pi*F_pi/2" in (
            CAMPAIGN / "evidence/source-audit.yaml"
        ).read_text()
        and "tail_route_is_independent" in (
            CAMPAIGN / "attempts/0002/result.yaml"
        ).read_text(),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
