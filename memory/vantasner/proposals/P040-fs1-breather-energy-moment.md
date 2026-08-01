---
description: Derive the exact sine-Gordon breather energy-density second moment and audit FS1
author: vantasner
created: '2026-08-01T18:33:57Z'
updated: '2026-08-01T18:45:50Z'
tags:
- substrate-framework
- campaign-proposal
- breather-moment
- migration-FS1
category: proposals
confidence: working
status: archived
---
# P040 FS1 Breather Energy-Moment Audit

## Question and Positive Deliverable

P040 must derive and package the normalized 1+1 sine-Gordon breather's
instantaneous energy-density second moment, including its exact time structure
and useful closed form if one exists. It must separately decide whether FS1
supplies the missing premises required to call this scalar width functional a
physical 3+1 quadrupole or radiation source. A negative physical disposition
without the positive 1+1 object would not complete the campaign.

## Base Release and Provenance

The accepted base is `v0.35.0` at framework commit `4aff298`, with forty-eight
claims. The relevant authority is the exact breather field `C-SG-001` and its
normalized Hamiltonian density and energy `C-SG-002`. FS1 is a pending candidate
unit at `substrate@6d1f4e0`, SHA-256
`da6b3bb1a602e52abb6d6ec5c926285e99d5216d03a9d41abc00af06e50011c2`.
Memory search found no accepted internal energy-density second-moment theorem.

## Invariants, Conventions, and Allowed Imports

The field, coordinate, frequency domain, and Hamiltonian density remain exactly
those of the normalized real 1+1 sine-Gordon model. The candidate functional is
the full-line integral of `x^2` times energy density. A scalar moment of a 1+1
profile does not become a 3+1 STF tensor, isolated source, or radiation channel
by naming it a quadrupole. Pending FS2-FS4 and P3D3 remain nonauthority.

## Candidate Preregistration

The alternatives are frozen from queue metadata before the full FS1 executable
body or its reported numerical/Fourier values are inspected.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Closed analytic instantaneous second moment | Accepted exact field and density | Frequency and time | Native 1+1 extension | Direct spatial integration, differentiation, phases, period, and independent derivation |
| B | Integral API with exact symmetry and controlled quadrature | Accepted density plus numeric evaluation | Frequency, time, domain/tolerance | Compatible evidence-bounded extension | Tail/tolerance refinement, special phases, and independent integration |
| C | Physical internal 3+1 quadrupole and radiation | Embedding, transverse profile, conserved source, gravity | Additional source and coupling data | Dependency conflict | Accepted 3+1 tensor/source and field-law closure |

## Selection Criteria and Blinding

Selection is ordered by exact density normalization, full-line convergence,
analytic tractability, time/phase/period consistency, independent agreement,
mutation sensitivity, parameter economy, and accepted dependency closure. No
FS1 sample, Fourier peak, or later radiation coefficient may select a route.

## Proposed Claim Delta

Provisional `C-SG-009` would add the finite instantaneous second spatial moment
of the accepted breather energy density and its exact temporal structure. Its
dependencies would be only `C-SG-001` and `C-SG-002`. It will exclude a 3+1
embedding, STF quadrupole, physical mass density, gravity, or radiation unless
those premises independently close.

## Implementation and Oracle Plan

The canonical sine-Gordon module will expose a pure energy-moment API, preferring
an exact formula over runtime integration. SymPy is appropriate for field
derivatives, algebraic spatial integration, phase identities, periodicity, and
limits. If the general integral resists exact evaluation, a SciPy quadrature API
will state domain truncation, tolerances, tail error, and refinement explicitly.
An independent route will reconstruct the density and integrate without calling
the new helper. Mutations will alter the Hamiltonian half factors, remove the
potential term, change the spatial weight, or confuse field and density periods.

## Attempts and Continuation

Attempt `0001` will hash-check and reproduce FS1, inventory its density, moment,
quadrature, time grid, Fourier, form-factor, 3+1, and radiation premises, and
then test Candidate A before falling back to Candidate B. Failed symbolic forms
will be preserved with their representation or concept diagnosis.

## Debt Ledger

This ledger tracks density normalization, full-line tails, temporal symmetries,
harmonic interpretation, and the boundary between a 1+1 scalar width and 3+1
source physics.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The x-squared integral may be divergent or truncation-dependent | Prove convergence or publish refinement-bounded evidence | discharged: exact finite formula plus scaled-domain refinement |
| A sampled Fourier peak may be mistaken for exact harmonic structure | Derive symmetry/period before inspecting reported peaks | discharged: exact half-period and nonconstant formula precede FFT regression |
| Energy-density and field periods may be conflated | Derive phase invariances from the exact field and density | discharged: field sign reversal leaves density and moment invariant |
| A 1+1 scalar width may be called a 3+1 quadrupole | Supply an accepted embedding or explicitly exclude the interpretation | discharged: C-SG-009 and adjudication exclude 3+1 physics |
| Pending radiation consumers may be imported backward | Keep FS2-FS4/P3D3 outside dependencies and adjudicate narrative links | discharged: all remain nondependencies and pending |

## Review and Promotion Plan

The provisional claim receives a separate field-density and quadrature review.
Promotion requires importable APIs/tests, immutable attempt evidence, claim-
level review, terminal FS1 disposition, registry/release/docs/memory agreement,
targeted consumers, and one unchanged full repository gate.

## Done Gate

P040 closes only when the functional, convergence, normalization, temporal
structure, mutations, physical scope, source disposition, consumers, and every
campaign debt row are resolved under the repository success contract.

## Adjudication Result

Candidate A is accepted as `C-SG-009`. Thirty-one exact/audit checks and nine
independent quadrature checks establish the closed family formula, its extrema,
and its half-period. FS1 is qualified: its numerical values reproduce, but its
mean split is same-sample bookkeeping, its kink derivative is wrong by two, and
the scalar 1+1 moment does not establish a 3+1 quadrupole or radiation. Campaign
debt is empty.
