---
description: Qualified review of W2 chiral SU2 doublet bridge
author: vantasner-review
created: '2026-08-09T22:50:00Z'
updated: '2026-08-09T22:50:00Z'
tags: [substrate-framework, source-review, migration-W2, representation]
category: decisions
confidence: established
status: archived
---
# W2 Qualified Review

## Decision

W2 is qualified through C-REP-002, C-SPN-002, C-REP-001, C-SG-011, and
C-BND-001. Its standard fundamental SU2 algebra, ladder, supplied charge
rescaling, exact projector arithmetic, and negative gauge inventory survive
under those ceilings. No physical kink or antikink doublet, fermion parity,
charge-changing event, common hypercharge, Lorentz chirality, parity violation,
rectification, gauge interaction, anomaly statement, or weak sector is
promoted.

## Corrected Positive Object

An independent chirality carrier gives Hermitian closing actions
`T_a⊗P_L` and `T_a⊗P_R`. A declared factor exchange swaps them, makes their sum
even and difference odd, and does not make one left operator an odd
eigenoperator. On the irreducible isospin C2, the commutant is scalar, so no
nontrivial rank-one projector can silently serve as independent chirality. A
common Abelian shift leaves the charge gap equal to one.

## Retained and Rejected Content

W2.1 and W2.2 are duplicate accepted algebra. W2.3 conflates the actual label
change two with an inserted unit event. W2.4 is a supplied coordinate
calibration. W2.5 correctly contradicts the dossier but gives opposite rather
than common Abelian charges. W2.6 has valid projector arithmetic on the wrong
carrier. W2.7 fails Hermiticity and closure. W2.8 preloads its parity image and
guard and computes no rectification. W2.9 accurately declares absent gauge
dynamics but does not build a coupling.

## Compatibility and Closure

Native W2 passes all nine predicates without a NumPy compatibility event.
Primary, independent, graph, and focused routes pass 49, 25, 83, and fourteen
checks. The 24-node graph inventories 234 predicates and 26 assertions.
Immutable W1 and W3 retain alias-only legacy integration shapes; pending YM2's
eager fallback remains isolated source evidence. Mutable P147 and canonical
code have no executable legacy integration access. GitNexus rates the additive
change LOW risk with no affected execution process.

## Cross-References

See P147, C-REP-002, C-SPN-002, C-REP-001, C-SG-011, C-BND-001, the source,
predicate, dependency, consumer, and nonduplication audits, independent
derivation, impact analysis, and frozen source graph.
