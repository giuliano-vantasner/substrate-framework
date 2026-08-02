---
description: Independent review of C-DIM-008 scale provenance and unit-coordinate covariance
author: vantasner-review
created: '2026-08-03T11:20:00Z'
updated: '2026-08-03T11:20:00Z'
tags:
- substrate-framework
- claim-review
- scale-provenance
category: decisions
confidence: established
status: archived
---
# C-DIM-008 Claim Review

## Claim Under Review

C-DIM-008 states an exact M,L,T target-span result for speed and action, the
effect of adjoining the target length as a primitive, finite reference-scale
covariance for a conditional one-loop scale and inverse-energy length,
arbitrary-target inverse families, and unit-coordinate covariance. Its
positive framework role is to make dimensionful provenance explicit without
claiming a physical absolute scale.

## Sourced Inputs

The review reads release `v0.68.0`, C-DIM-001, C-DIM-002, C-LIN-001,
C-RGE-001, C-RGE-003, C-IDN-001, their canonical modules and tests, P076's
frozen contract, attempts 0001 through 0003, the hash-pinned AS5 reproduction and source
audit, candidate comparison, impact map, new canonical module, focused tests,
and both verifier routes. AS4 supplies no physical row, while AS6 and every
later operating-point narrative remain pending and supply no premise.

## Independence

The independent route imports no `scale_provenance`, `scale_transmutation`,
`dimensional_analysis`, `linear_systems`, or `renormalization` API. It rebuilds
the M,L,T matrices, target solve, formal exponential, inverse-energy map,
finite reference family, arbitrary-target inverses, and unit-coordinate
transformation from fresh SymPy expressions and separately audits source text.

## Verification Status

The maximum verdict is `symbolic_verified`. The primary route passes 32 exact
checks, the independent route passes 21 exact checks, and 62 affected
canonical tests pass. Every promoted quantity is an evaluated exact matrix or
SymPy expression. No simulation, floating-point fit, unresolved integral,
numerical quadrature, deprecated `np.trapz`, or replacement NumPy alias is
used.

## Sensitivity and Counterexamples

Removing the supplied length changes a unique target solve into augmented-rank
inconsistency. Rescaling `mu0` changes both absolute outputs while preserving
the dimensionless energy ratio. Reversing the inverse-energy orientation fails
the canonical relation but passes AS5's symbol-absence predicate. A
nontransmutation mutant passes AS5.1's predicate. Arbitrary energy and length
targets round-trip only because the chosen reference contains those targets,
and a rescaled unit changes the coordinate while reconstructing the same fixed
quantity.

## Framework Compatibility

The claim is a compatible composition of accepted dimensional,
renormalization, ratio, and identifiability machinery. It retains the positive
reference energy, coupling squared, beta coefficient, conversion, target, and
unit standard wherever they are load bearing. It establishes no physical beta
function, QCD, confinement, lattice, soliton, chemistry, gravity, empirical
scale, preferred unit system, or absolute prediction.

## Dependency and Consumer Replay

Direct dependencies are C-DIM-002, C-RGE-001, C-RGE-003, and C-IDN-001. The
new consumers are the canonical module and exports, focused tests, P076
verifier, governance records, generated claim and release memory, and the AS5
disposition. GitNexus reports LOW impact for every reused existing API and no
affected execution flow; direct search covers the new unindexed file. The
final replay includes all affected scientific and governance paths.

## Competing Candidate Audit

Candidates B-F are selected on dependency closure, target membership,
reference covariance, inverse reconstruction, and unit semantics. Candidate A
is retained only as source regression because its passing predicates are
insensitive to its own headline. The exposed Angstrom and Planck labels were
never opened as numerical comparators and did not select the result.

## Four-Axis Decision

The exact evidence supports acceptance.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: depends on C-DIM-002, C-RGE-001, C-RGE-003, and C-IDN-001; challenges no accepted claim

## Promotion Transaction

Promotion adds C-DIM-008 to `v0.69.0`, qualifies AS5 through the editable
disposition source, regenerates the queue, and synchronizes package code,
tests, immutable campaign evidence, registry, release manifests, generated
docs, and accepted memory. One integrated workflow gate includes the complete
pytest suite; record-only synchronization receives targeted validation rather
than duplicate full-suite ceremony.

## Done Gate

Claim-level debt closes only after registry, release, queue, docs, memory,
campaign, affected consumers, and integrated validation agree. The parent
migration remains active because later source units remain pending.

## Cross-References

See P076, AS5, C-DIM-002, C-RGE-001, C-RGE-003, C-IDN-001,
`scale_provenance.py`, `test_scale_provenance.py`, base release `v0.68.0`,
accepted release `v0.69.0`, and the parent migration effort.
