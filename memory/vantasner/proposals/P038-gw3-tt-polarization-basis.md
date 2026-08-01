---
description: Audit GW3's TT polarization basis and physical interpretation
author: vantasner
created: '2026-08-01T18:05:59Z'
updated: '2026-08-01T18:12:13Z'
tags:
- substrate-framework
- campaign-proposal
- tt-projector
- polarization-basis
- migration-GW3
category: proposals
confidence: exploratory
status: archived
---
# P038 GW3 TT Polarization-Basis Audit

## Question and Positive Deliverable

P038 must derive the exact dimension and normalized basis of the image of the
accepted three-dimensional TT projector for a fixed propagation direction.
The positive deliverable is a reusable basis, completeness, and transverse-
frame rotation theorem distinct from C-GW-001's projector and sphere integral;
merely repeating the projector or rejecting physical terminology would not
complete the campaign.

## Base Release and Provenance

The accepted base is `v0.33.0` at framework commit `cc9574a`. Its forty-six
claims include `C-GW-001`, which establishes exact TT projection and angular
reduction but explicitly excludes physical gravitational degrees of freedom.
The pending hash-pinned candidate is GW3 at
`merged-framework/bridges/phase-12/bridge_GW3_TT_projector_two_polarizations.py`,
SHA-256 `3b941debf6933729b693b928579d4a7f1d73d906911c2fcedb9316ad08038326`.
Bundled-memory search found no accepted TT polarization-basis theorem.

## Invariants, Conventions, and Allowed Imports

P038 may import the exact Euclidean TT operator of `C-GW-001`, rank-nullity,
orthonormal-frame algebra, and complexification. For an oriented transverse
pair `(u,v)`, normalized real polarization tensors will be tested with their
Frobenius convention explicit. Their span and completeness must be independent
of rotating `(u,v)`, while individual plus/cross labels remain conventional.
No gravitational field equation, gauge dynamics, or quantum state may be
inferred from this spatial linear algebra.

## Candidate Preregistration

The alternatives are frozen from queue metadata before the full GW3 executable
body or any source comparator is inspected.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact rank-two image, normalized plus/cross basis, completeness, double-angle rotations, and circular phases | Fixed nonzero direction and oriented orthonormal transverse frame | Frame angle and normalization convention | Compatible extension | Six-dimensional matrix rank, exact basis contraction, projector equality, and rotation law |
| B | Dimension-two solution space only | Symmetric, transverse, traceless constraints | Direction | Selected if basis normalization or frame coverage fails | Independent linear constraint solve and axis cases |
| C | Two propagating physical helicity-two modes | Linearized gravitational action, constraints, gauge quotient, equations of motion | Field and momentum data | Dependency conflict | Accepted-claim closure beyond spatial projector algebra |

## Selection Criteria and Blinding

Selection is ordered by rank/nullity closure, normalized basis construction,
completeness with the accepted projector, orientation/sign transparency,
axis-safe frame coverage, exact double-angle behavior, mutation sensitivity,
and accepted dependencies for physical language. No outside polarization count
or gravitational observation may select a candidate.

## Proposed Claim Delta

Provisional `C-GW-002` would state that the TT image inside real symmetric
three-by-three tensors has dimension two and give a normalized plus/cross
basis whose dyadic completeness equals the TT projector. It would include the
double-angle frame-rotation law and, if exact, circular-basis phase weights,
while excluding propagating graviton counts, physical helicity, gauge
reduction, observables, and substrate realization.

## Implementation and Oracle Plan

Pure APIs will construct an axis-safe oriented transverse frame and normalized
real/circular polarization tensors. SymPy will verify transversality,
tracelessness, orthonormality, rank two, completeness, and frame rotations.
Mutations will change the square-root normalization, projector trace factor,
cross sign, and rotation angle. An independent route will solve the linear
constraints for an arbitrary direction rotated to an axis and compare the
resulting two free coordinates.

## Attempts and Continuation

Attempt `0001` will reproduce GW3 and inventory its projector, basis,
normalization, rank, frame, circular-polarization, and physical-input claims.
If the explicit basis fails but the constraint dimension closes, Candidate B
remains the positive object; physical overreach is qualified rather than used
to lower the algebraic bar.

## Debt Ledger

This ledger tracks novelty over C-GW-001, image dimension, basis normalization,
frame coverage, rotation law, and physical scope.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| GW3 may only duplicate the accepted projector | Establish a distinct rank/basis/completeness theorem or classify as duplicate | discharged: C-GW-002 adds the exact image, normalized basis, completeness, and rotation theorem |
| Two displayed tensors may not prove the full image dimension | Compute rank or solve all symmetric TT constraints | discharged: the operator has rank two and the independent constraint matrix has nullity two |
| Polarization normalization and signs are conventional | Encode one convention and test conversion/rotation explicitly | discharged: normalized tensors, half-weight source coefficients, double-angle rotation, and sign invariance are explicit |
| A coordinate-axis frame may fail at parallel directions | Supply and test an axis-safe deterministic construction | discharged: the piecewise constructor covers all three coordinate axes and rejects a parallel explicit reference |
| Two algebraic tensors may be called propagating helicities | Audit the missing action, constraints, gauge quotient, and dynamics | discharged: every physical mode and helicity reading is excluded from C-GW-002 |

## Review and Promotion Plan

The provisional claim receives an independent constraint and frame-rotation
review. Promotion requires pure APIs/tests, immutable attempt evidence,
claim-level adjudication, terminal GW3 disposition, release/docs/memory
synchronization, targeted replay, and one unchanged full repository gate.

## Done Gate

P038 closes only when novelty, rank, basis, normalization, completeness, frame
coverage, rotations, mutations, physical scope, consumers, and all campaign
debt satisfy the framework contract.

## Adjudication Result

Candidate A is accepted as `C-GW-002`. Thirty-three main checks establish the
rank-two image, normalized complete basis, piecewise axis coverage, double-angle
rotation, circular phases, and sensitive normalization/rotation mutations;
eight independent checks solve the complete constraint space and rederive the
basis law. GW3 is qualified because its displayed tensors are not orthonormal,
its provenance misstates the wrong-projector trace as four instead of three,
and the propagating-graviton map is imported. All campaign debt is discharged.
