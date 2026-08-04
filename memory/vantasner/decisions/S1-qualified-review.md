---
description: Qualified review of S1's two-Skyrmion nucleon-force source claim
author: vantasner-review
created: '2026-08-09T07:00:00Z'
updated: '2026-08-09T07:00:00Z'
tags: [substrate-framework, source-review, migration-S1, skyrmion]
category: decisions
confidence: established
status: archived
---
# S1 Qualified Review

## Decision

S1 is qualified through C-CC-001, C-VIR-001, C-RPROF-001, and C-SKY-001. Its
successful eleven-check tally is not a wholesale acceptance of the claimed
two-Skyrmion or nucleon force.

## Surviving Content

The declared one-coordinate optical variation, the sign and exponential decay
of a separately supplied Yukawa index profile, the first-order profile
potential, conditional virial algebra, and massless B=1 radial tail survive
under their exact accepted ceilings. C-SKY-001 separately supplies a coherent
declared-field long-range triplet-dipole interaction with global orientation
extrema.

## Rejected or Corrected Content

S1's numeric ODE omits one `1/R`, does not check solver success and has no
refinement. Its orientation test assigns scalar values and samples two
directions rather than deriving a cross energy over SO(3). ANW 1983 is
misattributed as a two-Skyrmion interaction source. The optical-profile and
triplet-dipole routes have no derived bridge between them. No physical
Skyrmion, baryon, nucleon, core, binding, scale, material, observation, or
substrate mechanism follows.

## Compatibility

S1 itself has no executable quadrature compatibility event on NumPy 2.5.1.
Immutable G1 and B1 consumer/dependency replay uses isolated aliases backed by
`np.trapezoid`; this is version compatibility, not scientific evidence.

## Cross-References

See P137, C-SKY-001, the predicate adjudication, source audit, primary review,
and eleven-node source graph.
