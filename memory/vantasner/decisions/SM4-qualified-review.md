---
description: Terminal review of SM4's exact fixed-data one-loop nonintersection and overbroad provenance
author: vantasner-review
created: '2026-08-10T21:57:00Z'
updated: '2026-08-10T21:57:00Z'
tags:
- substrate-framework
- source-review
- migration-SM4
- gauge-running
category: decisions
confidence: established
status: archived
---
# Review of SM4 Terminal Qualification

## Claim Under Review

SM4 asserts that three supplied GUT-coordinate inverse couplings run affinely
with coefficients `(41/10,-19/6,-7)`, cross pairwise across an approximately
four-decade high-scale window, and do not meet at one point. It also attributes
coefficient provenance, asymptotic-freedom signs, input provenance, and guard
semantics to that result.

## Verification and Independence

The primary route passes 37 exact and source-semantic checks. A fresh route
that imports neither `renormalization.py` nor the primary verifier passes 24
checks by reconstructing the exact design matrix, augmented rank, left-null
residual, pairwise crossings, scale spread, degeneracies, offsets, reference
behavior, and normalization map.

The supplied decimals exactize to coefficient rank two and augmented rank
three. The three exact crossing coordinates evaluate to 13.013127, 14.387275,
and 16.992183 in `log10(GeV)`, with a 3.979055-decade spread. Thus the supplied
lines are exactly inconsistent with one common point. This is accepted
composition through C-RGE-002, C-RGE-004, and C-RGE-005, not a new claim.

## Source Predicate Review

All eight source checks run natively. SM4 locally repeats QCD3's coefficient
formula and inputs rather than importing it. It hard-codes `b1`, `b2`, all
low-scale values, and the U1 coordinate normalization. The monotonic sweep and
rounded crossing targets are regressions of exact affine algebra.

The near-miss threshold is declared, and its check bundles an unrelated MSSM-
window boolean. The wrong-sign sample drives the inverse strong coupling
negative, so only the exact derivative-sign sensitivity survives generally.
The equal-slope guard proves parallel-disjoint behavior for unequal inputs but
omits the coincident equal-intercept branch. One comment-sensitive verifier
probe failed before an AST-backed repair and is preserved as attempt 0003.

## Framework Fit and Counterfamilies

C-RGE-004 was explicitly accepted for the SM4 consumer and already provides
the required rank, crossing, degeneracy, reference, and normalization API.
C-RGE-005 supplies the vector under a declared normalized table and selects no
physical embedding. Independent offsets can realize any common affine point;
reference scaling moves absolute scales; paired Abelian rescaling preserves
the electromagnetic row but not unqualified cross-factor equality.

No threshold spectrum, matching theorem, scheme and uncertainty record,
simple-group embedding, preferred U1 normalization, perturbative-domain proof,
observed-running likelihood, Standard Model construction, or substrate
mechanism is accepted.

## Dependency and Consumer Replay

The direct source graph includes SM4, qualified WM3, WM4, and WM5, and pending
WM7. Thirty-three graph checks cover 50 lexical predicates, 50 runtime
predicates, and five assertions. All five nodes are native and have no legacy
NumPy integration reference. Sixty accepted renormalization, beta-ledger, and
running tests pass. Pending WM7 gains only the accepted claim mapping and must
still be adjudicated independently.

## Four-Axis Decision

No claim changes axis. SM4 is terminally qualified through unchanged accepted
claims C-RGE-002, C-RGE-004, and C-RGE-005. Its exact supplied-data crossing
and nonintersection content survives; its stronger provenance, classifier,
physical, and substrate readings do not. There is no challenge, supersession,
canonical code change, or release change.

## Done Gate

Closure requires all eight predicate verdicts, primary and independent exact
oracles, source and consumer replay, input and literature provenance,
nonduplication, queue and memory synchronization, the integrated repository
gate, and empty P166 debt. The parent migration remains active after SM4.

## Cross-References

See C-RGE-002, C-RGE-004, C-RGE-005, C-RGE-006, P083, P128-P130, P166, SM4,
WM3-WM7, v0.127.0, and the parent framework-migration effort.
