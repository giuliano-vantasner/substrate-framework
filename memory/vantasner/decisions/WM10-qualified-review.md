---
description: Qualify WM10 as a conditional arbitrary-boundary gauge-only two-loop specialization
author: vantasner-review
created: '2026-08-05T23:28:00Z'
updated: '2026-08-05T23:28:00Z'
tags:
- substrate-framework
- source-review
- migration-WM10
- gauge-running
- two-loop
category: decisions
confidence: established
status: archived
---
# WM10 Qualified Review

## Exact and numeric surviving content

WM10 specializes C-RGE-006 at the supplied boundary
`(41/10,25/6,4)`. The status-gated solver gives readout
`0.2192066478076030` and high scale `1.618331584571e14` in the supplied unit.
The zero-matrix axis reproduces WM8 exactly; the equal-boundary full-matrix
axis reproduces C-RGE-006/WM6. The four-corner cross term is
`-0.0000827877685999`, so the readout effects are nonadditive.

## Interpretation correction

C-RGE-006 already owns arbitrary positive boundary ratios. The field table,
one-scalar count, boundary, two low coordinates, reference scale,
normalization, and zero matching offsets are supplied. WM9 derives no scalar
or generation count. The result is conditional inverse inference, not a new
theorem or ab-initio weak-angle prediction.

The source uses default RK45 only, does not check residual magnitude, ignores
grid success flags, and repeats identical arguments for its comparator guard.
Finite grids supply numeric samples, not a continuum monotonicity theorem. Its
residual-attribution result is prose-only; named uncomputed omissions do not
quantify or exhaust the discrepancy.

## Verification

Canonical DOP853 refinement and Radau agree, as does an independent direct-
coupling Radau/DOP853 route. Residuals, positivity, sign, target, matching, and
comparator mutations pass. Primary and independent routes close 38 and 15
checks. The 14-node graph closes 39 checks over 125 predicates and 16
assertions, and twelve focused gauge-running tests pass. There is no NumPy
quadrature compatibility surface.

## Four-axis decision

- Verification: numeric evidence with exact zero-matrix containment.
- Review: audited predicate by predicate and qualified.
- Compatibility: accepted composition of C-MIX-002, C-REP-001, C-REP-003,
  C-RGE-004, C-RGE-005, C-RGE-006, and C-VAC-003.
- Epistemic: qualified source evidence, not a new claim.
- Release: v0.150.0 unchanged.

## Closure

C-RGE-008 remains reserved and unpromoted. No package or release surface
changes. WM10's terminal disposition, queue, campaign, and durable memory are
the complete governed delta.
