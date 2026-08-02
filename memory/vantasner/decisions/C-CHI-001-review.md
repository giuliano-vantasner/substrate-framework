---
description: Independent review of C-CHI-001 conditional O4 and SU2 specialization
author: vantasner-review
created: '2026-08-02T12:41:00Z'
updated: '2026-08-02T12:41:00Z'
tags:
- substrate-framework
- claim-review
- conditional-chiral-model
category: decisions
confidence: established
status: archived
---
# C-CHI-001 Claim Review

## Claim Under Review

C-CHI-001 specializes C-SYM-001 to two declared coordinate models. The O(4)
radial quartic at a nonzero axial vacuum has an exact one-radial/three-zero
Hessian and an actual broken-tangent rank of three. A linear tilt lifts the
transverse curvature on its shifted stationary branch. For declared SU(2)
exponential coordinates with Pauli generators, the exact leading trace fixes
two convention-explicit kinetic metrics. The claim excludes a framework
chiral sector, quantum Goldstone theorem, physical pion, GMOR, Skyrmion,
decay-constant, absolute-scale, or substrate identification.

## Sourced Inputs

The review reads C-SYM-001, base release `v0.53.0`, the P060 proposal, three
append-only attempts, the pinned PG1 source reproduction and audit, primary
model/theorem provenance, canonical and independent derivations, focused
tests, and the consumer analysis. The executed source's O(4) and tilted-model
algebra survives. Its final ANW normalization sentence, dimension-only count,
dispersion substitution, physical-pion identification, and links to pending
PG2, PG4, and S2 do not.

## Independence

The independent review constructs the O(4) matrices without canonical
helpers, finds their actual tangent column space and coefficient nullspace,
and differentiates the potential directly. It multiplies explicit Pauli
matrices, differentiates a second-order exponential path, and derives the
quadratic mode Euler-Lagrange equation. It does not import PG1's expected
matrix, count, kinetic coefficients, or physical labels as answers.

## Verification Status

The maximum verdict is `symbolic_verified`. Every promoted coefficient and
rank is established through exact SymPy algebra in canonical and independent
routes. The O(4) Hessian, tangent rank, stabilizer nullity, Pauli trace Gram,
both kinetic metrics, explicit-breaking curvature, and limiting branches are
actual computed objects. The source's clean tally is reproduction evidence,
not the acceptance oracle. No numerical mass, decay constant, or simulated
spectrum is claimed.

## Sensitivity and Counterexamples

The symmetric stationary point makes all generator tangents zero and defeats
a naive `dim G-dim H` count. An off-stationary point defeats the Hessian-kernel
conclusion without breaking radial invariance. An anisotropic mass term
breaks the relevant rotations and lifts one direction; a linear tilt lifts
all three transverse curvatures on the declared branch. Dependent generator
labels do not increase the rank. Changing the action prefactor from `F^2/4`
to `F^2/16` changes the kinetic metric from `I` to `I/4`; claiming both are
canonical in the same coordinates fails. Adding a potential mass term changes
the zero Hessian to `m^2 I`.

## Framework Compatibility

The specialization depends only on C-SYM-001 and approved exact Pauli matrix
algebra. Every model premise, coordinate normalization, positivity condition,
and branch remains visible. It does not import a physical `F_pi`, condensate,
quark mass, pion mass, or pending campaign. Its names are conditional
mathematics and cannot modify accepted framework ontology.

## Dependency and Consumer Replay

The sole dependency is C-SYM-001. GitNexus found no existing canonical
symmetry-Hessian consumer; the additive package export has no upstream caller.
The focused module tests, both P060 verifiers, governance and generated
consumers, migration queue, and full workflow are replayed before sealing. No
downstream claim is permitted to infer a physical pion from this coordinate
example and no debt remains.

## Competing Candidate Audit

Candidates A through D were registered before source inspection. Candidates C
and D are jointly selected because actual orbit rank and trace normalization
meet the predeclared structural criteria. Candidate A is rejected as the
positive physical route: names, cited forms, and arithmetic do not construct
the claimed framework objects. Candidate B supplies the separately governed
general theorem. No empirical comparator chooses the coefficient or model.

## Four-Axis Decision

The axes are assigned independently and introduce no challenge or
supersession relationship.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: new conditional specialization of C-SYM-001

## Promotion Transaction

Promotion adds C-CHI-001 to the registry with dependency C-SYM-001, includes
it in release `v0.54.0`, archives immutable P060 evidence and this review,
qualifies PG1, regenerates the migration queue, and synchronizes generated
docs and accepted memory. Both exact verifiers, focused tests, impact
analysis, one full workflow validation, and `git diff --check` must pass.

## Continuation if Not Accepted

This clause is inactive because the exact conditional specialization is
accepted. A physical pion or chiral-sector claim must independently construct
the action, transformation, vacuum, quantum spectrum, parameter map, and
substrate dependency closure; PG1's labels cannot supply them.

## Done Gate

The claim-level mathematical debt is empty after the exact promotion replay.
The parent corpus migration remains active because later queue units remain
pending.

## Cross-References

See P060, PG1, C-SYM-001, `symmetry_breaking.py`,
`test_symmetry_breaking.py`, the audited primary sources, and release v0.54.0.
