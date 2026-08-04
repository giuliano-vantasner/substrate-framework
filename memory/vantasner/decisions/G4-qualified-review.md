---
description: Qualified review of G4 radiation reaction and internal backreaction
author: vantasner-review
created: '2026-08-09T17:50:00Z'
updated: '2026-08-09T17:50:00Z'
tags: [substrate-framework, source-review, migration-G4, radiation-reaction]
category: decisions
confidence: established
status: archived
---
# G4 Qualified Review

## Decision

G4 is qualified through C-RR-001 and the narrow accepted ceilings of G1, T2A,
and T2C. Its scalar work quotient and nonpositive-work identity survive only
conditionally. No physical power, independently derived self-force, internal
backreaction, causal equation, gravity, material, observation, or substrate
claim is promoted.

## Corrected Positive Object

One supplied scalar power fixes only force contracted with generalized rate.
For a nonzero rate vector, a declared positive-definite coordinate metric gives
a minimum-norm particular force, while every work-free covector generates an
alternate balanced force. A single rate is unique only away from zero. A
separately declared positive-semidefinite Rayleigh matrix gives an exact
effective force, dissipation, and external-work ledger.

## Retained and Rejected Content

G4's `F*v=-P`, `F=-P/v` for nonzero one-dimensional rate, and sign of minus a
declared square are retained conditionally. Its G1 power has rejected
normalization and no accepted breather source. The second expression is not an
independent ALD route. The prescribed accelerating path increases gamma E0 and
does not evolve damping. The time-averaged kernel cannot provide the omitted
temporal source harmonic, and the assigned internal power has no internal
amplitude or evolution. Runaway and preacceleration claims are unsupported.

## Compatibility and Closure

Native G4 stops only at removed `np.trapz`; an isolated alias backed by
`np.trapezoid` passes all ten predicates. The scientific verdict is independent
of that version event. Primary, independent, graph, and focused routes pass 29,
16, 27, and 17 checks. The ten-node graph pins 99 predicates. Mutable code has
no executable legacy integration access, and GitNexus risk is LOW.

## Cross-References

See P144, C-RR-001, C-RAD-001, its predicate adjudication, source and literature
audits, impact analysis, independent derivation, and frozen graph.
