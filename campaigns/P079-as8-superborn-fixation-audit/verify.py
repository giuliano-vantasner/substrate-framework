"""Primary exact verifier for P079 / provisional C-PRB-001."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.fixation_probability import (
    continuous_exponential_fixation_probability,
    exponential_fixation_ledger,
    two_intensity_selection_ledger,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-22/"
    "bridge_AS8_superborn_quantum_face_of_granularity.py"
)
SOURCE_SHA256 = "47fda3732d8901b6949b2859952123be675eef2bb28bad0ac0d241948fe3ea73"
CONTRACT_SHA256 = "0256eadcd40e26333fd19ad7815a4d9f5c25706fd8c6bb7c2c6bd801f0a6c4d5"
FREEZE_SHA256 = "34e445444ac67e1706f35f5255f9ea85a485f047fac33b2839a879e26060e9dc"


def _contract_path() -> Path:
    candidates = (
        Path("campaigns/P079-as8-superborn-fixation-audit/proposal.yaml"),
        Path("proposals/P079-as8-superborn-fixation-audit/proposal.yaml"),
    )
    return next(path for path in candidates if path.exists())


def main() -> int:
    checks = CheckLedger("P079")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "candidate contract hash remains frozen apart from terminal status",
        hashlib.sha256(
            _contract_path()
            .read_bytes()
            .replace(b"status: accepted\n", b"status: draft\n")
        ).hexdigest()
        == CONTRACT_SHA256,
    )
    freeze_path = _contract_path().parent / "evidence/frozen-proposal.yaml"
    checks.check(
        "pre-source contract commitment is immutable",
        hashlib.sha256(freeze_path.read_bytes()).hexdigest() == FREEZE_SHA256,
    )
    checks.check(
        "source has five literal checks and a dynamic terminal tally",
        source_text.count("check(") == 6
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    canonical_text = Path(
        "src/substrate_framework/fixation_probability.py"
    ).read_text(encoding="utf-8")
    checks.check(
        "source and canonical exact routes use no NumPy quadrature alias",
        all(
            alias not in source_text and alias not in canonical_text
            for alias in ("np." + "trapz", "np." + "trapezoid")
        ),
    )

    x = sp.symbols("x", real=True)
    selection = sp.symbols("S", real=True, nonzero=True)
    checks.check(
        "continuous family defines neutral point exactly",
        continuous_exponential_fixation_probability(x, 0) == x,
    )
    symbolic_selection = sp.symbols("S_symbolic", real=True)
    continuous = continuous_exponential_fixation_probability(
        x, symbolic_selection
    )
    checks.check(
        "undecided symbolic selection retains removable branch",
        isinstance(continuous, sp.Piecewise)
        and continuous.subs(symbolic_selection, 0) == x,
    )

    ledger = exponential_fixation_ledger(x, selection)
    expected = (1 - sp.exp(-selection * x)) / (1 - sp.exp(-selection))
    checks.check(
        "nonzero exponential branch is exact",
        sp.simplify(ledger.probability - expected) == 0,
    )
    checks.check(
        "neutral limit is exact",
        ledger.neutral_limit == x,
    )
    checks.check(
        "absorbing endpoint values are exact",
        ledger.boundary_at_zero == 0 and ledger.boundary_at_one == 1,
    )
    checks.check(
        "boundary matrix is nonsingular for declared nonzero selection",
        ledger.bvp_boundary_matrix
        == sp.ImmutableMatrix([[1, 1], [1, sp.exp(-selection)]])
        and ledger.bvp_boundary_determinant == sp.exp(-selection) - 1
        and ledger.bvp_boundary_determinant != 0,
    )
    reconstructed = sp.simplify(
        ledger.bvp_constant_offset
        + ledger.bvp_exponential_coefficient * sp.exp(-selection * x)
    )
    checks.check(
        "boundary solve reconstructs supplied branch",
        sp.simplify(reconstructed - ledger.probability) == 0,
    )
    checks.check(
        "declared backward equation residual vanishes",
        ledger.bvp_residual == 0,
    )
    wrong_generator = sp.simplify(
        sp.diff(ledger.probability, x, 2)
        + 2 * selection * sp.diff(ledger.probability, x)
    )
    checks.check(
        "generator coefficient mutation breaks the residual",
        wrong_generator != 0,
    )
    checks.check(
        "complement and sign-reversal symmetry is exact",
        ledger.complement_symmetry_residual == 0,
    )
    checks.check(
        "frequency derivative has a positive-factor representation",
        sp.simplify(
            ledger.frequency_derivative
            - selection
            * sp.exp(-selection * x)
            / (1 - sp.exp(-selection))
        )
        == 0,
    )
    checks.check(
        "selection derivative factorization is exact",
        ledger.selection_derivative_factorization_residual == 0,
    )
    midpoint_gap = sp.factor(
        ledger.selection_derivative_convexity_gap.subs(x, sp.Rational(1, 2))
    )
    checks.check(
        "midpoint convexity gap is a nonzero square",
        sp.simplify(
            midpoint_gap
            - (sp.exp(selection / 2) - 1) ** 2 / 2
        )
        == 0,
    )
    expected_series = sp.simplify(
        x
        + selection * x * (1 - x) / 2
        + selection**2 * x * (1 - x) * (1 - 2 * x) / 12
        - selection**3 * x**2 * (1 - x) ** 2 / 24
    )
    checks.check(
        "small-selection series exposes signed leading bias",
        sp.simplify(
            ledger.small_selection_series_through_cubic - expected_series
        )
        == 0,
    )

    interior = sp.Rational(2, 5)
    positive = continuous_exponential_fixation_probability(interior, 3)
    negative = continuous_exponential_fixation_probability(interior, -3)
    checks.check(
        "positive and negative selection move probability in opposite directions",
        0 < negative < interior < positive < 1,
    )
    branch = (
        1 - sp.exp(-symbolic_selection * interior)
    ) / (1 - sp.exp(-symbolic_selection))
    checks.check(
        "interior family spans the open probability interval",
        sp.limit(branch, symbolic_selection, -sp.oo) == 0
        and sp.limit(branch, symbolic_selection, sp.oo) == 1,
    )
    checks.check(
        "supplied target would remain load bearing in inverse selection",
        ledger.selection_derivative != 0
        and sp.diff(ledger.probability, selection) != 0,
    )

    intensity1, intensity2, coefficient, scale = sp.symbols(
        "I1 I2 kappa lambda", positive=True
    )
    intensity = two_intensity_selection_ledger(
        intensity1, intensity2, coefficient, scale
    )
    checks.check(
        "two intensities split into total and normalized frequency",
        intensity.total_intensity == intensity1 + intensity2
        and intensity.initial_frequency == intensity1 / (intensity1 + intensity2),
    )
    checks.check(
        "raw contrast retains total normalization",
        sp.simplify(
            intensity.raw_contrast
            - intensity.total_intensity * intensity.normalized_contrast
        )
        == 0
        and sp.simplify(
            intensity.normalized_contrast
            - (2 * intensity.initial_frequency - 1)
        )
        == 0,
    )
    checks.check(
        "common amplitude scaling preserves frequency but changes fixed-k S",
        intensity.scaled_initial_frequency == intensity.initial_frequency
        and intensity.fixed_coefficient_scaled_selection
        == scale**2 * intensity.selection_ratio,
    )
    checks.check(
        "compensating coefficient transformation preserves S",
        intensity.covariant_scaled_coefficient == coefficient / scale**2
        and intensity.covariant_scaled_selection == intensity.selection_ratio,
    )
    checks.check(
        "unit normalization preserves S only with transformed coefficient",
        sp.simplify(
            intensity.unit_normalized_first_intensity
            + intensity.unit_normalized_second_intensity
            - 1
        )
        == 0
        and intensity.unit_normalized_selection == intensity.selection_ratio,
    )

    source_first = two_intensity_selection_ledger(4, 1, 1, 5)
    source_second = two_intensity_selection_ledger(100, 25, 1, 1)
    checks.check(
        "source examples share frequency but have different raw norms",
        source_first.initial_frequency
        == source_second.initial_frequency
        == sp.Rational(4, 5)
        and source_first.total_intensity == 5
        and source_second.total_intensity == 125,
    )
    checks.check(
        "source examples become identical after unit normalization",
        source_first.unit_normalized_first_intensity
        == source_second.unit_normalized_first_intensity
        and source_first.unit_normalized_second_intensity
        == source_second.unit_normalized_second_intensity
        and source_first.unit_normalized_contrast
        == source_second.unit_normalized_contrast,
    )
    selection_expression_load_lines = tuple(
        sorted(
            node.lineno
            for node in ast.walk(source_tree)
            if isinstance(node, ast.Name)
            and node.id == "S_expr"
            and isinstance(node.ctx, ast.Load)
        )
    )
    checks.check(
        "source numerical S values hold unsourced coefficient fixed",
        source_second.selection_ratio == 25 * source_first.selection_ratio
        and selection_expression_load_lines == (111, 112)
        and "u_S3" in source_text
        and "u_S75" in source_text,
    )

    theta_loads = sum(
        isinstance(node, ast.Name)
        and node.id == "Theta_eff"
        and isinstance(node.ctx, ast.Load)
        for node in ast.walk(source_tree)
    )
    cutoff_loads = sum(
        isinstance(node, ast.Name)
        and node.id == "a"
        and isinstance(node.ctx, ast.Load)
        for node in ast.walk(source_tree)
    )
    checks.check(
        "source unification never evaluates Theta_eff or cutoff a",
        theta_loads == 0 and cutoff_loads == 0,
    )
    checks.check(
        "source unification check is direct symbol substitution",
        "Theta_form = hbar_med * omega" in source_text
        and "Theta_form.subs(hbar_med, hbar) == hbar * omega" in source_text,
    )
    checks.check(
        "source supplies no backward equation or absorbing-boundary derivation",
        "u_xx" not in source_text
        and "absorbing" not in source_text.lower()
        and "boundary" not in source_text.lower(),
    )
    checks.check(
        "source restricts symbolic S to positive values",
        'sp.symbols("A1 A2 lambda S x0", positive=True)' in source_text,
    )
    checks.check(
        "source imports no accepted quantum or stochastic implementation",
        source_text.count("import ") == 1
        and "import sympy as sp" in source_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
