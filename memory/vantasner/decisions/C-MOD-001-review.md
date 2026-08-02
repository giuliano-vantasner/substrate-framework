---
description: Independent review of C-MOD-001 radial second-variation theorem
author: vantasner-review
created: '2026-08-02T20:50:00Z'
updated: '2026-08-02T20:50:00Z'
tags:
- substrate-framework
- claim-review
- radial-hessian
category: decisions
confidence: established
status: archived
---
# C-MOD-001 Claim Review

## Claim Under Review

C-MOD-001 states the exact Euler--Lagrange equation, mixed-term-complete
self-adjoint second variation, Green boundary form, Derrick scale tangent and
curvature, and massless continuum threshold of one explicitly declared radial
Option-C energy. It distinguishes a positive finite-box level from a bound
half-line mode and excludes every physical Skyrme, nucleon, Roper, quantum,
absolute-scale, and substrate identification.

## Sourced Inputs

The review reads base release `v0.55.0`, C-SYM-001, C-QBL-003, C-DIM-001,
C-DIM-003, C-SK-001, the P062 contract, PG3 at hash
`4e3b56ab...`, the S2 evidence it cites, attempts 0001 through 0005, the raw
source reproduction and adjudication, `radial_modes.py`, focused tests, both
verifiers, and the pre-change impact report. PG3's Roper, bound-state,
translation, quantum-label, and gap-ratio readings remain outside the claim.

## Independence

The independent route re-expands the perturbed energy through second order,
derives the mixed coefficient and its integration-by-parts correction, and
assembles the Green-compatible operator without importing the canonical radial
module. It intentionally shares only SymPy and the declared energy density;
no PG3 eigenvalue or expected Roper statement enters the exact oracle.

## Verification Status

The maximum verdict is `symbolic_verified`. All promoted identities simplify
to evaluated exact expressions. The primary verifier passes 30 checks across
the P062 claims and the independent route passes 16. The source's omitted
mixed correction is exposed by the complete epsilon expansion, not inferred
from numerical disagreement. The zero continuum threshold follows from the
exact massless far-field coefficients.

## Sensitivity and Counterexamples

Deleting the mixed correction changes the load-bearing finite-box level and,
with PG3's removed-origin window, recreates its reported scale. Doubling the
kinetic weight halves every generalized eigenvalue. Subtracting the weight
from the potential shifts the spectrum through zero. Endpoint-fixed Green
data cancel the exact boundary form, whereas undeclared boundary data do not.
The Derrick counterexample has zero first scale derivative at E2=E4 but
strictly positive curvature E2+E4, so stationarity does not make dilation a
zero mode.

## Framework Compatibility

The claim is a new conditional reduced-model theorem and changes no accepted
symbol. It preserves C-SYM-001's requirement of actual stationarity and
C-QBL-003's separation of a classical Hessian from particle masses. The
energy, radial coordinate, kinetic mirror, endpoint conditions, and massless
tail remain explicit premises. No pending PG3 dependency enters.

## Dependency and Consumer Replay

The claim is dependency-free. Its consumers are the new module, focused tests,
P062 verifiers, governance, generated documentation, and later radial-mode
audits. GitNexus finds the implementation additive; the critical shared
trapezoid helper and all existing consumers are unchanged. Focused and full
workflow replay remain promotion gates, with no claim-local debt accepted.

## Competing Candidate Audit

Candidates A through E were registered before PG3's executable was opened.
Candidate B supplies the exact theorem and Candidate C supplies the scale-
tangent guard. Candidate A is rejected because its local half-Hessian is not
the integrated quadratic operator. Selection follows action closure,
self-adjointness, and limits rather than proximity to 0.097.

## Four-Axis Decision

The axes support a new exact conditional theorem with no challenge or
supersession relationship.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: new dependency-free declared radial-model theorem

## Promotion Transaction

Promotion adds C-MOD-001 to release `v0.56.0`, archives P062 evidence and this
review, exports and tests the canonical API, qualifies PG3, regenerates the
queue, and synchronizes docs and accepted memory. Primary, independent,
focused, registry, downstream, one full workflow, graph-change, and diff gates
must pass.

## Continuation if Not Accepted

This clause is inactive because the exact theorem is accepted. A future
physical radial excitation must separately establish a complete action,
half-line spectral pole or resonance criterion, quantization, state map, and
scale; it cannot infer them from this conditional Hessian.

## Done Gate

The claim-level debt is empty once the promotion transaction replays and
canonical state agrees. The parent corpus effort remains active because later
queue units are pending.

## Cross-References

See P062, PG3, `radial_modes.py`, `test_radial_modes.py`, C-MOD-002,
C-SCL-001, release `v0.56.0`, and the parent migration effort.
