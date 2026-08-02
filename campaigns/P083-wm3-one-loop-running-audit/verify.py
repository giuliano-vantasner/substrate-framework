"""Primary exact verifier for the P083 WM3 one-loop running audit."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.linear_systems import diagnose_linear_system
from substrate_framework.renormalization import (
    affine_unification_scale,
    diagnose_affine_unification,
    reconstruct_electroweak_unification,
    rescale_abelian_inverse_coordinate,
    shift_affine_reference,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-23/"
    "bridge_WM3_sin2thetaw_rg_running.py"
)
SOURCE_SHA256 = "2328ae4d6e66e1caa14a39042c362e57258406383f14ecaa5f5f6c468105e298"
CONTRACT_SHA256 = "c7dc37c656184a1173089d2a09d6506debd71340fd660af3f946ec92046a4990"
FREEZE_SHA256 = "dd307c369514ab13c762d563567e2a09e6392ae85c9a7dec1a05a3ecbca689df"


def _contract_path() -> Path:
    candidates = (
        Path("campaigns/P083-wm3-one-loop-running-audit/proposal.yaml"),
        Path("proposals/P083-wm3-one-loop-running-audit/proposal.yaml"),
    )
    return next(path for path in candidates if path.exists())


def _queue_unit(source_unit: str) -> dict[str, object]:
    queue = yaml.safe_load(Path("migration/source-claims.yaml").read_text())
    return next(unit for unit in queue["units"] if unit["source_unit"] == source_unit)


def _reconstruction(values: object) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    electromagnetic, strong, beta_1, beta_2, beta_3, weight = values
    result = reconstruct_electroweak_unification(
        electromagnetic, strong, beta_1, beta_2, beta_3, weight
    )
    return (
        result.common_inverse_coupling,
        result.running_coordinate,
        result.weak_angle_coordinate,
    )


def main() -> int:
    checks = CheckLedger("P083")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
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
    checks.check(
        "source has ten literal checks and a dynamic terminal tally",
        source_text.count("check(") == 11
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source and exact audit use no NumPy quadrature alias",
        all(alias not in source_text for alias in ("np." + "trapz", "np." + "trapezoid")),
    )
    checks.check(
        "source re-hardcodes every claimed inherited load-bearing number",
        all(
            token in source_text
            for token in (
                "b1, b2, b3 = sp.Rational(41, 10), sp.Rational(-19, 6), sp.Integer(-7)",
                "gp2_over_g2 = sp.Rational(3, 5)",
                "ALPHA_EM_INV = 127.9",
                "ALPHA_S = 0.118",
                "SIN2_MEASURED = 0.23122",
            )
        ),
    )
    checks.check(
        "source headline oracle is approximate regression against literals",
        all(
            token in source_text
            for token in (
                "np.linalg.solve",
                "math.isclose(A, 41.5",
                "math.isclose(sin2_pred, 0.208",
                "math.isclose(log10_Lambda, 14.83",
            )
        ),
    )

    electromagnetic = sp.Rational(1279, 10)
    strong = sp.Rational(500, 59)
    weight = sp.Rational(5, 3)
    beta = (sp.Rational(41, 10), -sp.Rational(19, 6), sp.Integer(-7))
    reconstruction = reconstruct_electroweak_unification(
        electromagnetic, strong, *beta, weight
    )
    checks.check(
        "exact inverse solve recovers the source coordinates without a numeric solver",
        reconstruction.denominator == sp.Rational(67, 3)
        and reconstruction.common_inverse_coupling == sp.Rational(1639681, 39530)
        and reconstruction.running_coordinate == sp.Rational(186383, 39530)
        and reconstruction.weak_angle_coordinate
        == sp.Rational(6296809, 30335322),
    )
    a1, a2, a3 = reconstruction.inverse_couplings
    checks.check(
        "exact reconstruction closes both supplied observation equations",
        a3 == strong
        and sp.simplify(a2 + weight * a1 - electromagnetic) == 0,
    )
    checks.check(
        "three reconstructed low-energy lines have one exact common intersection",
        (
            diagnosis := diagnose_affine_unification(
                reconstruction.inverse_couplings,
                beta,
                provenance=("U1", "SU2", "SU3"),
            )
        ).linear.unique
        and diagnosis.common_inverse_coupling
        == reconstruction.common_inverse_coupling
        and diagnosis.running_coordinate == reconstruction.running_coordinate
        and diagnosis.compatibility_residuals == (0,),
    )
    checks.check(
        "all reconstructed pairwise crossings agree because the weak coordinate was solved",
        len(diagnosis.pairwise_crossings) == 3
        and all(crossing.status == "unique" for crossing in diagnosis.pairwise_crossings)
        and {crossing.coordinate for crossing in diagnosis.pairwise_crossings}
        == {reconstruction.running_coordinate},
    )

    weak = sp.Symbol("w", real=True)
    full_design = sp.Matrix(
        [
            [1, beta[0], electromagnetic / weight],
            [1, beta[1], -electromagnetic],
            [1, beta[2], 0],
        ]
    )
    full_rhs = sp.Matrix([electromagnetic / weight, 0, strong])
    full = diagnose_linear_system(full_design, full_rhs)
    full_solution = next(iter(sp.linsolve((full_design, full_rhs))))
    checks.check(
        "equivalent three-coordinate system is uniquely identified by three equations",
        full.unique
        and full_solution
        == (
            reconstruction.common_inverse_coupling,
            reconstruction.running_coordinate,
            reconstruction.weak_angle_coordinate,
        ),
    )
    reduced_design = full_design[:2, :]
    reduced_rhs = full_rhs[:2, :]
    reduced = diagnose_linear_system(reduced_design, reduced_rhs)
    reduced_nullspace = reduced_design.nullspace()
    checks.check(
        "removing the strong observation reopens a weak-angle fit direction",
        reduced.consistent
        and reduced.solution_dimension == 1
        and len(reduced_nullspace) == 1
        and sp.simplify(reduced_nullspace[0][2]) != 0,
    )
    checks.check(
        "the three-coordinate form makes the alleged prediction an inverse reconstruction",
        full.equations == full.unknowns == full.coefficient_rank == 3
        and full_rhs[0] == electromagnetic / weight
        and full_rhs[2] == strong
        and full_design[1, 2] == -electromagnetic
        and weak not in full_rhs.free_symbols,
    )

    checks.mutation_sensitive(
        "every observation coefficient and normalization input is load bearing",
        lambda values: _reconstruction(values)
        == (
            reconstruction.common_inverse_coupling,
            reconstruction.running_coordinate,
            reconstruction.weak_angle_coordinate,
        ),
        (electromagnetic, strong, *beta, weight),
        (
            (electromagnetic + 1, strong, *beta, weight),
            (electromagnetic, strong + 1, *beta, weight),
            (electromagnetic, strong, beta[0] + 1, beta[1], beta[2], weight),
            (electromagnetic, strong, beta[0], beta[1] + 1, beta[2], weight),
            (electromagnetic, strong, beta[0], beta[1], beta[2] + 1, weight),
            (electromagnetic, strong, *beta, weight + 1),
        ),
    )
    checks.check(
        "the three-equal-coefficient branch is singular rather than predictive",
        sp.simplify(
            beta[1] + weight * beta[0] - (1 + weight) * beta[2]
        )
        != 0,
    )
    try:
        reconstruct_electroweak_unification(
            electromagnetic, strong, 2, 2, 2, weight
        )
    except ValueError as error:
        singular_rejected = "denominator" in str(error)
    else:
        singular_rejected = False
    checks.check("degenerate equal slopes are rejected explicitly", singular_rejected)

    boundary_weight = sp.Symbol("n", positive=True)
    checks.check(
        "common-coupling boundary remains a supplied normalization coordinate",
        sp.diff(1 / (1 + boundary_weight), boundary_weight) != 0
        and reconstruction.boundary_weak_angle_coordinate == sp.Rational(3, 8),
    )
    rescaled_a1, rescaled_b1, rescaled_weight = rescale_abelian_inverse_coordinate(
        a1, beta[0], weight, 2
    )
    checks.check(
        "paired Abelian rescaling preserves the electromagnetic contribution and running",
        rescaled_weight * rescaled_a1 == weight * a1
        and rescaled_weight * rescaled_b1 == weight * beta[0],
    )
    checks.check(
        "coordinate rescaling does not preserve an unqualified equality to SU2",
        reconstruction.common_inverse_coupling / 2
        != reconstruction.common_inverse_coupling
        and rescaled_a1 != a1,
    )

    measured = sp.Rational(11561, 50000)
    measured_inverse = (
        sp.simplify((1 - measured) * electromagnetic / weight),
        sp.simplify(measured * electromagnetic),
        strong,
    )
    measured_diagnosis = diagnose_affine_unification(
        measured_inverse, beta, provenance=("U1", "SU2", "SU3")
    )
    measured_crossings = tuple(
        crossing.coordinate for crossing in measured_diagnosis.pairwise_crossings
    )
    checks.check(
        "fixed measured weak coordinate fails the exact three-way intersection test",
        not measured_diagnosis.linear.consistent
        and measured_diagnosis.compatibility_residuals != (0,)
        and all(coordinate is not None for coordinate in measured_crossings),
    )
    checks.check(
        "the three fixed-data pairwise crossings are exactly unequal and ordered",
        len(set(measured_crossings)) == 3
        and measured_crossings[0] < measured_crossings[1] < measured_crossings[2]
        and measured_crossings
        == (
            sp.Rational(27584193, 6812500),
            sp.Rational(7451936137, 1637250000),
            sp.Rational(1867213863, 339250000),
        ),
    )
    checks.check(
        "the fixed-data crossing spread reproduces the pending SM4 near-miss structurally",
        measured_crossings[2] - measured_crossings[0] > sp.Rational(7, 5),
    )

    shift = sp.Rational(7, 11)
    shifted_inverse = shift_affine_reference(
        reconstruction.inverse_couplings, beta, shift
    )
    shifted = diagnose_affine_unification(
        shifted_inverse, beta, provenance=("U1", "SU2", "SU3")
    )
    checks.check(
        "reference shift preserves the common inverse and translates the scale coordinate",
        shifted.linear.unique
        and shifted.common_inverse_coupling
        == reconstruction.common_inverse_coupling
        and shifted.running_coordinate == reconstruction.running_coordinate - shift,
    )
    reference = sp.Symbol("mu0", positive=True)
    checks.check(
        "declared source scale map retains its positive reference input",
        affine_unification_scale(reference, reconstruction.running_coordinate)
        == reference * sp.exp(2 * sp.pi * reconstruction.running_coordinate)
        and reconstruction.running_coordinate > 0,
    )

    target = sp.Symbol("target", positive=True)
    target_inverse = (
        (1 - target) * electromagnetic / weight,
        target * electromagnetic,
        strong,
    )
    threshold_offsets = (
        sp.simplify(target_inverse[0] - strong),
        sp.simplify(target_inverse[1] - strong),
        sp.Integer(0),
    )
    checks.check(
        "two sector matching offsets realize every supplied weak-angle target",
        all(
            sp.simplify(
                target_inverse[index]
                - threshold_offsets[index]
                - strong
            )
            == 0
            for index in range(3)
        )
        and target in threshold_offsets[0].free_symbols
        and target in threshold_offsets[1].free_symbols,
    )
    comparator_residual = sp.simplify(
        abs(reconstruction.weak_angle_coordinate - measured) / measured
    )
    checks.check(
        "opened comparator gives an exact nonzero residual rather than a selection rule",
        comparator_residual == sp.Rational(17933103821, 175353328821)
        and sp.Rational(1, 10) < comparator_residual < sp.Rational(11, 100),
    )
    checks.check(
        "source leaves the weak-angle scheme unspecified",
        "SIN2_MEASURED = 0.23122" in source_text
        and "weak mixing angle scheme" not in source_text.lower()
        and "msbar" not in source_text.lower(),
    )

    qcd3 = _queue_unit("QCD3")
    sm4 = _queue_unit("SM4")
    wm1 = _queue_unit("WM1")
    wm2 = _queue_unit("WM2")
    checks.check(
        "only the conditional SU3 coefficient route has accepted closure",
        qcd3["disposition"] == "qualified"
        and set(qcd3["accepted_claims"])
        == {"C-LIE-001", "C-RGE-001", "C-RGE-002"}
        and sm4["disposition"] == "pending_adjudication"
        and sm4["accepted_claims"] == [],
    )
    checks.check(
        "WM1 and WM2 supply no accepted physical boundary mechanism",
        wm1["disposition"] == "qualified"
        and wm2["disposition"] == "duplicate_evidence"
        and "unification scale, or running" in wm1["qualification"]
        and "boundary scale" in wm2["duplicate_reason"],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
