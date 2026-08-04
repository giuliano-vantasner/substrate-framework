---
description: Qualified review of S4's vector-meson c4 closure claim
author: vantasner-review
created: '2026-08-09T12:30:00Z'
updated: '2026-08-09T12:30:00Z'
tags: [substrate-framework, source-review, migration-S4, hls, skyrme]
category: decisions
confidence: established
status: archived
---
# S4 Qualified Review

## Decision

S4 is qualified through C-VEC-001, C-EFT-001, and C-CHI-001. C-VEC-001 is
promoted for the distinct exact current and leading-connection surface. No
physical rho, KSRF, c4, B1, medium, or substrate claim is promoted.

## Corrected Positive Object

Exact ordered SU(2) currents obey the Gram-wedge and Pauli commutator-square
identities. A declared positive mass penalty selects the half current, whose
Maurer--Cartan curvature gives the equally normalized leading Skyrme density
with `e=g`. This is order `p^4`; the full-vector backreaction first changes the
action at order `p^6/M^2`. A separately supplied
`m_V^2=a*g^2*F^2` condition gives a dimensionless mass ratio but is not derived.

## Retained and Rejected Content

S4's scalar series, one Pauli special case, polynomial specialization, and
pole-versus-polynomial distinction survive narrowly. The source assigns the
effective operator and desired tensor, inserts the coefficient ratio, imports
the B1 target, solves J1 backward, and never eliminates a vector field. Its
`e=F_pi/2` has the wrong dimensions. No physical HLS action, rho, pion,
Skyrmion, KSRF theorem, medium response, or absolute coefficient closes.

## Compatibility and Closure

S4 has no NumPy compatibility event. Primary, independent, graph, and focused
routes pass 36, 25, 31, and 44 checks. The thirteen-node graph pins 123
predicates. Pending B1 retains an immutable alias-only path backed by
`np.trapezoid`; no mutable legacy integration access is introduced. GitNexus
risk is LOW.

## Cross-References

See P140, C-VEC-001, its predicate adjudication, source and literature audits,
impact analysis, independent derivation, and frozen dependency/consumer graph.
