---
description: Independent review of the three corrected conditional rational-map stationary branches
author: vantasner-review
created: '2026-08-07T15:25:00Z'
updated: '2026-08-07T15:25:00Z'
tags:
- substrate-framework
- claim-review
- rational-map
- numerical-evidence
category: decisions
confidence: established
status: archived
---
# Review of C-RPROF-002

## Claim Under Review

C-RPROF-002 supplies resolution-bounded evidence for stationary branches of
C-RPROF-001 at `(B,I)=(1,1),(2,pi+8/3),(4,20.6496264884189)`. It reports the
conditional energy coefficients and their selected per-degree ordering. The
claim is not a half-line existence or uniqueness theorem, a minimum, a full
three-dimensional solution, or a physical state or binding claim.

## Numerical Independence

The canonical route uses DOP853 amplitude shooting in `g=pi-f`, which preserves
the tiny degree-four origin perturbation, regular-origin and massless-tail
Robin residuals, the shared trapezoid compatibility helper, and explicit
leading endpoint energy estimates. It isolates sampled quadrature, origin
cutoff, outer domain, IVP tolerance, and maximum step. A fresh `solve_bvp`
collocation route uses an independently constructed two-power guess, adaptive
mesh residuals, and SciPy Simpson integration without importing the canonical
radial module.

The canonical 2401-sample energy coefficients are `1.2314456867`,
`2.4162704269`, and `4.5460579996`, with per-degree values `1.2314456867`, `1.2081352135`, and
`1.1365144999`. Independent collocation gives `1.2314503696`, `2.4162703856`,
and `4.5460579996`. Both routes satisfy their stated residual and virial gates.

## Failed Routes and Sensitivity

Attempt 0002 exposes the ill-conditioned degree-four outer residual when `f`
is integrated directly near `pi`; attempt 0003 shows scalar-root tightening
does not repair that representation loss. The vacuum-complement variable does.
Attempt 0004 rejects a comparison between endpoint-corrected and finite-domain
uncorrected energies and replaces it with a like-for-like regression.
Attempt 0006 preserves and corrects the sample-count provenance error in the
0005 result block; the change is below `3e-8` relative and changes no verdict.

Correct accepted angular inputs, source-biased inputs, `I=B`, and `I=B^2` are
all distinct solved cases. The mutations materially change energy. Both simple
mutations nevertheless preserve the selected ordering, so the source guard is
not an ordering oracle and cannot validate a binding or yield story.

## Dependency and Consumer Replay

The numeric claim depends on C-RPROF-001 and accepted C-RMAP-001/002 angular
inputs; C-MOD-002 is a B=1 comparator only. E3, E4, E5, KI5, TX1–TX5, MK5,
MR5, and narrative consumers remain pending. They may not turn conditional
stationary-branch numbers into an action, global energy bound, baryon, nucleus,
fission threshold, reaction, or observation without their own accepted closure.

## Four-Axis Decision

The numeric branch evidence is accepted with the following independent status axes.

- Verification: `numeric_evidence`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `qualified`
- Relationship: depends on C-RPROF-001 and C-RMAP-001/002; challenges and supersedes none

## Done Gate

Acceptance requires two independent successful solvers, explicit boundary and
equation residuals, isolated refinements, endpoint estimates, mutation
sensitivity, conditional interpretation, importable implementation and tests,
complete source/consumer classification, and synchronized release and memory.
No lower evidentiary surface is promoted merely because a tally passes.

## Cross-References

See P105, E2, C-RPROF-001, C-RMAP-001/002, C-MOD-001/002,
`rational_map_radial.py`, release v0.89.0, and the framework-migration effort.
