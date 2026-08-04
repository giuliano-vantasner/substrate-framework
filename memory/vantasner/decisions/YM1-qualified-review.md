---
description: Qualified review of YM1 Yang-Mills induction bridge
author: vantasner-review
created: '2026-08-10T14:20:00Z'
updated: '2026-08-10T14:25:00Z'
tags: [substrate-framework, source-review, migration-YM1, nonabelian-vacuum-polarization]
category: decisions
confidence: established
status: archived
---
# YM1 Qualified Review

## Decision

YM1 is qualified through C-NVP-001, C-NAG-001, and C-VAC-001. Its exact
Pauli-half trace and projector controls survive, while its claimed physical
Yang--Mills induction does not.

## Corrected Positive Object

For separately declared massive complex-scalar SU2 multiplets, the exact
color kernel is T(R) times the accepted Abelian scalar kernel. The bubble and
seagull cancel before transverse decomposition. The leading local coefficient
is `N_s*g^2*T(R)/(48*pi*m^2)` for the component density, equivalently
`N_s*g^2/(48*pi*m^2)` for `tr_R(F^2)`. An independent proper-time derivation
completes the leading term with the full non-Abelian curvature.

## Retained and Rejected Content

YM1 defines factorization and imposes transversality rather than deriving a
loop. It supplies no action, determinant, regulator, bubble, seagull, or
counterterm. Its numerator is not complex-scalar QED2, its finite massless
pole is false in that model, its action step drops a momentum factor, and its
Abelian guard changes normalization. Bare and counterterm coefficients remain
independent. No physical W, weak matter, dimensional lift, or substrate
mechanism follows.

## Compatibility and Closure

Native YM1 passes all nine predicates and has no NumPy surface. Primary,
independent, focused-plus-adjacent, and graph routes pass 32, 20, 38, and 21
checks or tests, with the graph replaying 132 immutable predicates. Mutable
P158 has no legacy integration access; immutable YM2's spelling-only legacy
surface is isolated behind `np.trapezoid`. YM1 is terminally qualified in
v0.123.0 rather than accepted as a physical weak gauge construction.

## Cross-References

See P158, C-NVP-001, C-NAG-001, C-VAC-001, the source and predicate audits,
independent derivation, semantic graph, primary literature, impact analysis,
and compatibility evidence.
