---
description: Qualified review of G1's radiating-dilaton source claim
author: vantasner-review
created: '2026-08-09T14:10:00Z'
updated: '2026-08-09T14:10:00Z'
tags: [substrate-framework, source-review, migration-G1, retarded-wave]
category: decisions
confidence: established
status: archived
---
# G1 Qualified Review

## Decision

G1 is qualified through C-RAD-001, C-SG-001, C-SG-002, C-SG-008, and
C-SG-012. C-RAD-001 is promoted for a distinct exact scalar-action surface.
No physical dilaton, accelerated-breather radiation, coupling, multipole,
self-force, gravity, or substrate claim is promoted.

## Corrected Positive Object

A separately declared canonical scalar action yields a retarded point-source
solution whose distributional jump closes. Each outgoing side carries
`B^2*q^2/(4*A*c)` and total power `B^2*q^2/(2*A*c)` equals local source work.
A static solution has the same local equation and jump but zero flux, proving
the boundary and history premise. Field rescaling preserves the power.

## Retained and Rejected Content

G1's conditional metric algebra, trace simplification, normalized rest
breather regression, gamma derivative, and free-wave identity survive narrowly.
Its trace integral uses the wrong gamma transformation, its retarded response
differentiates the source once too many, and its two-sided flux is low by four.
The numerical leg integrates its target right-hand side and selects the weak
coupling backward. The displayed dilaton action contains no canonical h kinetic
term, and replacing v by v(t) does not construct an on-shell accelerated
breather.

## Compatibility and Closure

Native G1 stops only because NumPy 2.5.1 removed `np.trapz`; isolated alias-only
replay backed by `np.trapezoid` passes all ten source checks. The scientific
verdict is independent of compatibility. Primary, independent, graph, and
focused routes pass 37, 29, 73, and 75 checks. The 31-node graph pins 339
predicates. Mutable code has no executable legacy integration access, and
GitNexus risk is LOW.

## Cross-References

See P141, C-RAD-001, its predicate adjudication, source and literature audits,
impact analysis, independent derivation, and frozen dependency/consumer graph.
