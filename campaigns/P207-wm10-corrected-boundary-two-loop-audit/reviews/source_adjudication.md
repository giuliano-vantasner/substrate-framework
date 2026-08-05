# WM10 Source Adjudication

WM10's combined gauge-only value is reproducible: the accepted solver gives
`0.2192066478076030` and a supplied-unit high scale
`1.618331584571e14`. The exact zero-matrix boundary axis reproduces WM8, the
equal-boundary matrix axis reproduces C-RGE-006/WM6, and the four-corner cross
term is `-0.0000827877685999`.

This is not a new theorem. C-RGE-006 already quantifies over arbitrary positive
boundary ratios and calls the result conditional inverse inference. WM7's
field table, the one-scalar beta ledger, two low coordinates, reference scale,
normalization, and zero matching remain supplied. WM9 does not derive the
scalar or generation counts.

The source's evidence is weaker than its wording. It uses default RK45 only,
does not test residual magnitude, ignores success flags for its nine grid
solves, repeats identical arguments instead of perturbing the comparator, and
cannot infer continuum monotonicity from nine points. Its exhaustive residual
attribution is prose-only; named uncomputed omissions do not quantify or
exhaust the discrepancy.

Canonical DOP853 refinement, Radau, an independent direct-coupling route,
residual and positivity gates, 25-point sampled monotonic evidence, target and
sign mutations, matching offsets, and comparator dataflow checks support the
narrow conditional result. WM10 is qualified under existing claims, with no
new API, claim, or release.
