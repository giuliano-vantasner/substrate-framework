---
description: Derive a conditional breather breathing-wave theorem and audit FS3
author: vantasner
created: '2026-08-01T19:10:33Z'
updated: '2026-08-01T19:30:00Z'
tags:
- substrate-framework
- campaign-proposal
- breathing-mode
- migration-FS3
category: proposals
confidence: working
status: archived
---
# P042 FS3 Conditional Breathing-Wave Audit

## Question and Positive Deliverable

P042 must derive a reusable, premise-explicit consequence of the accepted
breather energy moment and separable STF tensor: its exact third time
derivative, contraction, conditional power, cycle average, and viewing
polarization wherever those objects close. It must separately decide whether
FS3 supplies a conserved isolated 3+1 source and gravitational dynamics. A
positive sampled number or a negative ontology audit alone would not complete
the campaign.

## Base Release and Provenance

The accepted base is `v0.37.0` at framework commit `d6a90e3`, with fifty
claims. Relevant authority is `C-SG-009`, `C-MOM-002`, `C-GW-001`, and
`C-GW-002`, plus their canonical sine-Gordon, separable-moment, and TT modules.
FS3 is pending candidate evidence at `substrate@6d1f4e0`, SHA-256
`572e4e156897bf335784cc606123e9a482fdf13a16434a239e15583050a0ac90`.
Memory search found no accepted FS3 derivative, power, or waveform theorem.

## Invariants, Conventions, and Allowed Imports

The longitudinal moment retains its exact 1+1 meaning and fundamental period
`pi/omega`. The normalized tensor `I_STF` and triple tensor `Q=3*I_STF` must
carry inverse waveform coefficients and factor-nine contraction changes
consistently. TT projection is algebraic. No pending FS4 form factor, P3D3
embedding, source conservation, gravitational action, retarded field law, or
physical flux may be inferred.

## Candidate Preregistration

The candidates are frozen from the queue headline and accepted dependencies
before the full FS3 executable body or any of its reported numbers is read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact conditional derivative, average, and viewing theorem | Accepted scalar moment, declared separable tensor, conditional wave/flux law | Breather frequency and declared prefactors | Compatible conditional extension | Exact differentiation, contraction, period integral, and TT projection |
| B | Pointwise contraction and viewing only | Same accepted algebra without a closed average | Same inputs | Minimal compatible extension | Exact derivatives and projections; reject unsupported spectral closure |
| C | Physical breather radiation | Conserved 3+1 source plus gravity | Added source and coupling data | Dependency conflict | Accepted local conservation, field equations, and source-to-wave closure |

## Selection Criteria and Blinding

Selection prioritizes accepted dependency closure, exact tensor convention,
temporal symmetry and period, analytic or independently controlled averaging,
mutation sensitivity, viewing geometry, parameter economy, and explicit
physical scope. FS3 numerical power values and harmonic comparisons remain
blinded until these equations and criteria are frozen.

## Proposed Claim Delta

Provisional `C-GW-004` would state the exact conditional time-domain tensor,
power-functional, and viewing consequences that follow from `C-SG-009`,
`C-MOM-002`, `C-GW-001`, and `C-GW-002`. A separate provisional `C-SG-010`
would carry only the resolution-bounded special-frequency cycle average and
Fourier power fraction, so its numeric evidence cannot upgrade the exact
claim's verification axis or vice versa. Both claims will exclude a physical
3+1 breather, gravitational theory, radiation channel, and detector
prediction. If the average does not converge independently, Candidate B
narrows the delta without weakening its exact predicates.

## Implementation and Oracle Plan

Pure package APIs will expose exact positive-order derivatives and, if useful,
conditional power evaluation without embedding a simulation or source file.
SymPy is primary for analytic differentiation, tensor contractions, symmetry,
period, and axial/perpendicular TT geometry. Exact integration is attempted
without treating failure to find an elementary form as a no-go. If needed,
high-precision quadrature over the exact expression supplies numeric evidence
with precision and subdivision refinement, while an independently derived
Fourier or change-of-variable route checks the average. Mutations change the
STF factor, waveform coefficient, derivative order, base period, or line of
sight. The FS3 source is hash-checked and reproduced once; any dense unchanged
replay may use a hash-bound durable reproduction record.

## Attempts and Continuation

Attempt `0001` will reproduce FS3, inventory its derivative, FFT, average,
normalization, waveform, FS4, and physical-source premises, and compare every
formula against accepted conventions. Symbolic representation failures,
quadrature limitations, and rejected physical interpretations remain
append-only evidence with an explicit next route.

## Debt Ledger

This ledger tracks derivative exactness, averaging, convention scaling,
period/harmonics, viewing geometry, and physical-source scope.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Sampled finite differences may stand in for an available exact derivative | Differentiate C-SG-009 directly and test finite differences only as regression | discharged: the canonical API differentiates C-SG-009 exactly |
| A same-data FFT may be labeled an analytic harmonic oracle | Supply an independent exact or controlled average route | discharged: refined direct quadrature and a sixty-digit manual Fourier route agree |
| Triple and normalized STF power coefficients may be mixed | Carry both tensor and waveform rescalings together | discharged: inverse rescaling restores equality and exposes FS3's factors three and nine |
| The scalar-moment period may be confused with the field period | Derive symmetry, fundamental period, and harmonic support exactly | discharged: the moment and all derivatives have period pi/omega and only even field harmonics |
| Viewing read-offs may mix normalized basis and matrix conventions | Declare basis, direction, and coefficient normalization | discharged: arbitrary-inclination normalized coordinates and conventional readouts are both exact |
| Conditional positive power may be called physical radiation | Supply conserved source and gravity closure or explicitly exclude it | discharged: C-GW-004 is explicitly conditional and excludes all physical radiation conclusions |

## Review and Promotion Plan

The provisional claim receives an independent time-average and projection
review that does not call the new helper. Promotion requires pure APIs/tests,
immutable attempt evidence, source adjudication, claim-level review, terminal
FS3 disposition, registry/release/docs/memory agreement, affected-consumer
replay, and one full repository gate at the unchanged promotion boundary.

## Done Gate

P042 closes only when derivative, contraction, averaging, period/harmonic,
normalization, viewing, source-scope, consumer, disposition, and debt
obligations are all resolved.

## Adjudication Result

Candidate A is accepted in two claim-sized pieces. `C-GW-004` carries the
symbolically verified exact derivative, convention-invariant conditional
power, and arbitrary-inclination TT geometry. `C-SG-010` separately carries
numeric evidence for the special-frequency cycle mean and two-omega Fourier
fraction. Thirty-seven primary and eleven independent checks pass after two
preserved verifier-representation failures. FS3 is qualified for its
factor-nine power, factor-three waveform, grid-induced strict positivity,
same-data FFT, kink derivative, and absent physical source/gravity closure.
