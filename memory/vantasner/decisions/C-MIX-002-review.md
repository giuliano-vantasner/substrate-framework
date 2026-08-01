---
description: Independent review of C-MIX-002
author: vantasner-review
created: '2026-08-01T17:32:26Z'
updated: '2026-08-01T17:32:26Z'
tags:
- substrate-framework
- claim-review
- unitary-rephasing
- invariant-quartet
category: decisions
confidence: working
status: archived
---
# Review of C-MIX-002

## Claim Under Review

Conditional on the abstract unitary bases of `C-MIX-001`, the claim gives the
diagonal-rephasing action, support-dependent stabilizer and orbit dimensions,
generic quotient and angle/phase count, the `N=2` real representative, and
rephasing/conjugation properties of invariant quartets without a physical CP
assignment.

## Sourced Inputs

The review read `v0.30.0`, `C-MIX-001`, P035, both exact routes, package
APIs/tests, hash-pinned FG4 and its successful reproduction, and the
subclaim-level source adjudication. FG3, M1, S2, SM2, SM3, W2, W3, and W7 were
inventoried as source relationships rather than accepted dependencies.

## Independence

The main route combines exact complete-support and exceptional-support
incidence ranks with the source parameterization. The independent route uses
`K4,4`, a four-edge permutation support, a separately parameterized `U(2)`, a
normalized Fourier `U(3)` matrix, and a degenerate-spectrum basis change. It
does not import the new rephasing module or source constants.

## Verification Status

Exact Lie-algebra dimensions, incidence ranks, symbolic phase cancellation,
unitarity, and quartet identities support `symbolic_verified`. Numeric APIs
are regression consumers. The claim deliberately assigns no empirical,
simulation, or physical CP verdict.

## Sensitivity and Counterexamples

Forgetting the common phase, substituting the angle count, or assigning one
irreducible phase at `N=2` breaks the exact budget. Removing a quartet
conjugation or changing a balancing index breaks rephasing invariance.
Permutation and block supports expose enlarged stabilizers. Degenerate scalar
spectra permit arbitrary unitary bases, so a quartet that is invariant under
diagonal phases need not define physics under all allowed basis changes.

## Framework Compatibility

The claim is a compatible extension of `C-MIX-001`. It preserves that claim's
phase, ordering, and degenerate-subspace freedoms, adds a tolerance-declared
support oracle, and labels `2N-1` as generic connected-support orbit dimension.
It imports no fields, currents, masses, representations, or CP operation.

## Dependency and Consumer Replay

The sole accepted dependency is `C-MIX-001`. Direct consumers are
`unitary_rephasing.py`, its exports/tests, P035, FG4's disposition, and future
abstract unitary-matrix audits. Physical FG4 consumers remain outside the
accepted graph. Focused replay passes with no debt.

## Competing Candidate Audit

Candidate A was selected because the support graph repairs the universal count
and exact low-dimensional results close, making Candidate B too narrow.
Candidate C fails accepted-dependency closure and the degenerate-basis audit;
no comparator or physical label selected the mathematical candidate.

## Four-Axis Decision

The axes apply only to the generic rephasing quotient and invariant algebra.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: rephasing-quotient extension of C-MIX-001

## Promotion Transaction

Promotion adds pure count, support, rephasing, quartet, and declared-chart
APIs; guarded tests; immutable P035; qualified FG4 disposition; `v0.31.0`;
generated records; and parent-effort synchronization.

## Continuation if Not Accepted

If the stabilizer repair had failed, Candidate B would retain only the budget
identity and quartet cancellation. Physical CP work must first establish
fields, interactions, mass nondegeneracy or a stronger invariant, a physical
conjugation map, and an accepted family sector.

## Done Gate

The action, kernel, strata, dimensions, low-`N` results, invariant,
conjugation, mutations, dependency boundary, consumers, disposition, and debt
closure are complete.

## Cross-References

See P035, FG4, `C-MIX-001`, `unitary_rephasing.py`, and the parent migration
effort.
