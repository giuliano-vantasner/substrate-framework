---
description: Qualify GK3D6 through accepted affine scale, identifiability, trace-coordinate, and classical-radial ceilings
author: vantasner-review
created: '2026-08-05T21:08:00Z'
updated: '2026-08-05T21:08:00Z'
tags:
- substrate-framework
- source-review
- migration-GK3D6
- kinetic-matching
- scheme-ratios
category: decisions
confidence: established
status: archived
---
# GK3D6 Qualified Review

## Exact surviving content

For the accepted affine family
`Z_i=z_i+b_i*(L-log(c))/(8*pi^2)` with nonzero coordinates,
`g_i^2/g_j^2=Z_j/Z_i` and

`d(g_i^2/g_j^2)/dlog(c)=(b_i*z_j-b_j*z_i)/(8*pi^2*Z_i^2)`.

The common scheme factor therefore cancels exactly when the affine boundaries
are proportional to the weights. Zero matching is one separately imposed
corollary. Factorwise logs, conversions, orientations, or nonproportional
boundaries break the ratio.

## Accuracy and provenance correction

The source computes a relative normalization shift `-log(c)/L`, not the
relative inverse-coordinate shift `log(c)/(L-log(c))`. Smallness additionally
requires a bounded shift, large log, nonzero domain, and controlled omitted
orders. Its `b0=7`, `beta^2=0.245`, and `xi/a=1e20` are hardcoded. C-IDN-002
already proves AS7's alleged second route is inverse reconstruction by
construction rather than independent over-determination.

C-QBL-004 supplies a dimensionless classical radial branch but no particle
pole, determinant-field identity, physical mass conversion, or absolute
scale. C-REP-001 retains three-eighths only as a conditional trace coordinate
under a common inverse-trace law and Abelian normalization convention.

## Verification and compatibility

The native source reproduces ten checks. The mutation-sensitive primary and
fresh raw-SymPy routes pass 35 and 17 checks, and the seven-node source graph
passes 25 terminal checks with no reverse consumer and no duplicate native execution.
Two verifier-construction failures are preserved and repaired.

GK3D6 and mutable P203 have no NumPy quadrature surface. Immutable GK3D5's
current-first lazy fallback selects `numpy.trapezoid` under NumPy 2.5.1; its
legacy branch is compatibility evidence only and produces zero scientific
failures.

## Four-axis decision

- Verification: exact symbolic evidence for the conditional affine ratio,
  sensitivity, scale conversion, normalization shift, and trace ceilings.
- Review: audited predicate by predicate and qualified.
- Compatibility: accepted composition of C-RGE-003, C-IDN-002, C-VAC-003,
  C-VAC-004, C-REP-001, and C-QBL-004.
- Epistemic: qualified source evidence, not a new claim.
- Release: v0.150.0 unchanged.

## Closure

C-VAC-006 remains reserved and unpromoted. No canonical API, package test,
accepted registry entry, release claim set, physical particle map, universal
matching, absolute accuracy, coupling prediction, weak-angle observation, or
substrate mechanism is accepted. The governed delta is GK3D6's terminal
qualified disposition and synchronized queue and durable memory.
