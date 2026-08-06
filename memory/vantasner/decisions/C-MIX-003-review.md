---
description: Independent review of C-MIX-003 globally phased real matrix theorem
author: vantasner
created: '2026-08-06T07:02:59Z'
updated: '2026-08-06T07:19:49Z'
tags:
- substrate-framework
- claim-review
- C-MIX-003
category: decisions
confidence: established
status: archived
---
# C-MIX-003 Claim Review

## Claim Under Review

C-MIX-003 states the exact left and right Gram cancellation for finite matrices
`Y_a=exp(i theta_a)R_a` with exactly real `R_a`, the existence of real left
Gram bases, null quartet imaginary parts in their relative basis, real
antisymmetric commutator odd-trace identities, and the enlarged degeneracy
basis caveat. It assigns no Yukawa, CKM, physical CP, condensate, generation,
observation, Standard-Model, or substrate meaning.

## Sourced Inputs

The review reads v0.151.0, C-MIX-001, C-MIX-002, the hash-pinned GC3 source,
P210's freeze and append-only attempts, both exact verifiers, source and
predicate adjudications, implementation tests, impact inventory, and GC4-GC6
consumer map. C-QBL-001, C-QBL-003, and C-OVL-001 are source-composition
ceilings but are not dependencies of the matrix theorem.

## Independence

The independent verifier imports no C-MIX-003 implementation. It directly
multiplies generic rectangular matrices, derives a positive quadratic form,
uses fresh exact rational orthogonal bases, and constructs fresh Fourier,
two-real-source, complex-coupling, and degenerate-basis countermodels.

## Verification Status

The claim earns symbolic verification because all load-bearing identities are
resolved exact SymPy equalities. Forty-two primary and twenty-seven independent
checks pass. Numeric API results are regression evidence only and use
scale-relative residuals for high matrix powers. The immutable source has zero
quadrature compatibility surface and no version event affects the verdict.

## Sensitivity and Counterexamples

Scalar phase mutations leave both Grams fixed. Entrywise or spatial phase,
independent complex coupling, and complex mode mutations break the real-matrix
premise and can make a Gram complex. Two real symmetric matrices at phases zero
and pi/2 exactly construct a nonzero Fourier quartet at N=3. A complex Fourier
basis of the identity Gram has a nonzero coordinate quartet while the Gram
commutator remains zero, proving the degeneracy caveat is load bearing.

## Framework Compatibility

The theorem is a compatible extension of C-MIX-001 and C-MIX-002. It changes no
accepted convention or existing API. Source count K and matrix dimension N
remain independent, and neither is selected. No fitted constant, measured
value, pending GC premise, or physical interaction enters the closure.

## Dependency and Consumer Replay

Direct API consumers are the P210 verifier and focused tests; the package
initializer re-exports the additive surface. GC4 through GC6 remain pending and
grant no backward authority. The thirteen-node graph contains ninety-seven
static predicates and eighteen assertions with zero quadrature compatibility
surface; its final replay is part of the promotion boundary.

## Competing Candidate Audit

Eight candidates and structural criteria were frozen before source access.
Exact common-phase algebra, basis-aware invariants, premise countermodels, and
independent K/N typing were selected. Universal condensate enforcement was
rejected, while the no-new-claim candidate was rejected only after a direct
registry and API nonduplication audit exposed the minimum novel surface.

## Four-Axis Decision

The integrated transaction establishes verification `symbolic_verified`,
review `accepted`, compatibility `compatible_extension`, and epistemic
`active`, with no challenge or supersession.

## Promotion Transaction

The transaction adds C-MIX-003, the canonical module and tests, v0.152.0,
generated docs and memory, the GC3 qualified disposition, the regenerated
queue, and campaign evidence. The single `scripts/validate.sh` boundary passed
all 1,837 tests and validated 851 memory files; record-only finalization
receives only the narrow repository, generation, memory, graph, and diff checks.

## Continuation if Not Accepted

If the integrated boundary finds a substantive dependency or implementation
failure, P210 remains in review and repairs the exact claim transaction rather
than lowering the theorem or accepting the source headline.

## Done Gate

The integrated boundary passes and the P210 debt ledger is empty. Source check
count and random agreement were not used as substitutes for this gate.

## Cross-References

The durable sources are the P210 campaign, C-MIX-001, C-MIX-002, v0.152.0,
`common_phase_matrices.py`, its focused tests, and the framework-migration
effort.
