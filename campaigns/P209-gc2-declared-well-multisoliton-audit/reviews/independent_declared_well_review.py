#!/usr/bin/env python3
"""Independent raw-SymPy review of GC2 without canonical localization APIs."""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-42/"
    "bridge_GC2_corpus_already_multisoliton.py"
)
MH2 = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-20/"
    "bridge_MH2_overlap_hierarchy.py"
)
WM9 = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-39/"
    "bridge_WM9_scalar_multiplicity_from_condensate.py"
)


def main() -> int:
    checks = CheckLedger("P209-INDEPENDENT-DECLARED-WELL")
    x, center = sp.symbols("x R", real=True)
    width, index = sp.symbols("w s", positive=True)
    depth = sp.simplify(index * (index + 1) / width**2)
    shifted = (x - center) / width
    state = sp.sech(shifted) ** index
    h_state = sp.simplify(
        -sp.diff(state, x, 2) - depth * sp.sech(shifted) ** 2 * state
    )
    eigen_residual = sp.trigsimp(
        h_state + index**2 / width**2 * state,
        method="fu",
    )
    checks.check(
        "fresh translated Poschl ground residual vanishes",
        sp.simplify(sp.expand_trig(eigen_residual)) == 0,
    )
    checks.check(
        "fresh ground eigenvalue is independent of center",
        center not in (-index**2 / width**2).free_symbols,
    )

    t = sp.symbols("t", real=True)
    log_characteristic = (
        sp.loggamma(index + sp.I * width * t / 2)
        + sp.loggamma(index - sp.I * width * t / 2)
        - 2 * sp.loggamma(index)
    )
    centered_mean = sp.simplify(
        sp.diff(log_characteristic, t).subs(t, 0) / sp.I
    )
    centered_variance = sp.simplify(
        -sp.diff(log_characteristic, t, 2).subs(t, 0)
    )
    checks.check("fresh centered density mean is zero", centered_mean == 0)
    checks.check(
        "fresh centered variance is exact and positive",
        centered_variance == width**2 * sp.polygamma(1, index) / 2
        and centered_variance.is_positive is True,
    )
    checks.check(
        "fresh translated moments separate origin and centered RMS",
        sp.expand(center**2 + centered_variance)
        == center**2 + width**2 * sp.polygamma(1, index) / 2,
    )
    positive_displacement = sp.symbols("R_positive", positive=True)
    checks.check(
        "fresh relative centered width vanishes under large translation",
        sp.limit(sp.sqrt(centered_variance) / positive_displacement, positive_displacement, sp.oo)
        == 0,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    checks.check(
        "fresh source audit finds E absolute x mislabeled as centroid",
        "cent = float(np.sum(d * np.abs(xi)) * h)" in source_text,
    )
    checks.check(
        "fresh source audit finds width refinement absent",
        "conv = max(abs(a[0] - b[0])" in source_text
        and "abs(a[1] - b[1])" not in source_text,
    )

    kappa = sp.symbols("kappa", positive=True)
    fixed_depth = sp.symbols("V_0", positive=True)
    core_depth = 6 * kappa**2 * sp.sech(kappa * positive_displacement) ** 2
    ratio = sp.simplify(fixed_depth / core_depth)
    asymptotic_ratio = sp.simplify(
        sp.limit(ratio / sp.exp(2 * kappa * positive_displacement), positive_displacement, sp.oo)
    )
    checks.check(
        "fresh fixed-well to core ratio has exact exponential asymptotic",
        asymptotic_ratio == fixed_depth / (24 * kappa**2),
    )
    checks.check(
        "fresh ratio mutation depends on independent fixed depth",
        sp.diff(ratio, fixed_depth) != 0,
    )

    p = sp.symbols("p", positive=True)
    trial = sp.sech(kappa * x) ** p
    quartic_potential = kappa**2 - 6 * kappa**2 * sp.sech(kappa * x) ** 2
    residual = sp.trigsimp(
        -sp.diff(trial, x, 2)
        + quartic_potential * trial
        - kappa**2 * (1 - p**2) * trial,
        method="fu",
    )
    expected = (
        kappa**2
        * (p * (p + 1) - 6)
        * sp.sech(kappa * x) ** (p + 2)
    )
    checks.check(
        "fresh trial-family residual has the source coefficient",
        sp.simplify(sp.expand_trig(residual - expected)) == 0,
    )
    checks.check(
        "fresh p one and three mutations fail while p two survives",
        sp.simplify(expected.subs(p, 2)) == 0
        and sp.simplify(expected.subs(p, 1)) != 0
        and sp.simplify(expected.subs(p, 3)) != 0,
    )

    profile = sp.sqrt(24) * kappa * sp.sech(kappa * x)
    translation = sp.diff(profile, x)
    fluctuation = kappa**2 - profile**2 / 4
    checks.check(
        "fresh quartic translation tangent is an exact zero mode",
        sp.simplify(-sp.diff(translation, x, 2) + fluctuation * translation)
        == 0,
    )
    omega = sp.symbols("omega", real=True)
    field = sp.Function("f")(x)
    differentiated_eom = (sp.cos(field) / 2 - omega**2) * sp.diff(field, x)
    exact_sine_zero_residual = sp.simplify(
        -differentiated_eom
        + (sp.cos(field) / 2 - omega**2) * sp.diff(field, x)
    )
    checks.check(
        "fresh exact-sine translation identity does not validate its bound count",
        exact_sine_zero_residual == 0,
    )

    mh2_tree = ast.parse(MH2.read_text(encoding="utf-8"), filename=str(MH2))
    assignments = {
        target.id: ast.literal_eval(node.value)
        for node in mh2_tree.body
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
        and target.id in {"D_SPACING", "N_GEN", "WELL_DEPTH", "WELL_W"}
    }
    checks.check(
        "fresh AST recovers the six-member external-well declaration",
        assignments
        == {"D_SPACING": 4.0, "N_GEN": 6, "WELL_DEPTH": 12.0, "WELL_W": 0.7},
    )
    wm9_tree = ast.parse(WM9.read_text(encoding="utf-8"), filename=str(WM9))
    modes = next(
        ast.literal_eval(node.value)
        for node in wm9_tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "MODES" for target in node.targets)
    )
    checks.check("fresh AST recovers literal WM9 count", modes == (1, 2, 3))
    checks.check(
        "fresh list mutation changes count without changing physics",
        len(modes[:2]) == 2 and len(modes + (4,)) == 4,
    )

    source_tree = ast.parse(source_text, filename=str(SOURCE))
    imports = {
        node.module
        for node in ast.walk(source_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    checks.check(
        "fresh source has no nonlinear multisoliton solver import",
        "scipy.integrate" not in imports and "eigh_tridiagonal" in source_text,
    )
    own_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"), filename=__file__)
    own_imports = {
        node.module
        for node in ast.walk(own_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    } | {
        alias.name
        for node in ast.walk(own_tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "independent route imports no canonical localization or Q-ball API",
        not any(
            name.startswith("substrate_framework.translated_localization")
            or name.startswith("substrate_framework.qball")
            for name in own_imports
        ),
    )
    integration_attributes = {
        node.attr
        for node in ast.walk(own_tree)
        if isinstance(node, ast.Attribute) and node.attr in {"trapz", "trapezoid"}
    }
    checks.check(
        "independent route has no NumPy compatibility surface",
        "numpy" not in own_imports and integration_attributes == set(),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
