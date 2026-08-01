---
description: Derive a static breather-moment decomposition and audit FS4
author: vantasner
created: '2026-08-01T19:31:30Z'
updated: '2026-08-01T19:39:00Z'
tags:
- substrate-framework
- campaign-proposal
- static-moment
- migration-FS4
category: proposals
confidence: working
status: archived
---
# P043 FS4 Static-Moment Decomposition Audit

## Question and Positive Deliverable

P043 must derive any exact static-plus-dynamic decomposition of the accepted
breather energy moment, including a genuine zero-mean remainder and the exact
effect of constant offsets on accepted derivative, conditional waveform, and
power functionals. It must separately decide whether FS4 derives the static
quantity as a physical form factor, tidal coupling, or backreaction mechanism.
A generic statement that constants differentiate to zero is insufficient if
it adds no distinct framework object.

## Base Release and Provenance

The accepted base is `v0.38.0` at framework commit `aa1fd5d`, with fifty-two
claims. Relevant authority is `C-SG-009`, `C-MOM-002`, and `C-GW-004` plus the
canonical sine-Gordon and separable-moment modules. FS4 is pending candidate
evidence at `substrate@6d1f4e0`, SHA-256
`2f3c1b02bbad06bded6a38d0e1c203b2ba9c71c63adea34645d041b820feb129`.
Its cited T2C and G4 units are also pending. Memory search found no accepted
FS4 static form-factor or tidal theorem.

## Invariants, Conventions, and Allowed Imports

The centered scalar moment retains its 1+1 meaning and period `pi/omega`.
Time averaging, a fixed-profile spatial Fourier moment, transverse variance,
and an STF tensor offset remain distinct objects until an exact equality is
derived. Positive derivatives remove a truly constant offset, but not a
slowly varying or parameter-dependent function of time. No pending tidal,
backreaction, 3+1 source, or gravity result may be imported backward.

## Candidate Preregistration

The alternatives are frozen from the queue metadata and accepted dependencies
before the full FS4 executable body or any reported comparison values are read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact mean/remainder theorem with offset invariance | Accepted exact periodic moment | Frequency, time, arbitrary constant | Native or compatible exact extension | Exact period integral, zero mean, derivative and conditional-functional identities |
| B | Duplicate accepted derivative consequence | No new mean or consumer | Arbitrary constant | No release delta | Match every predicate to C-MOM-002/C-GW-004 |
| C | Physical form-factor/tidal/backreaction map | Object identity plus source and interaction dynamics | Added coupling data | Dependency conflict | Accepted T2C/G4, conserved source, and action-to-response closure |

## Selection Criteria and Blinding

Selection prioritizes exact mean derivation, object and dimension hygiene,
constant-versus-time-dependent sensitivity, dependency closure, parameter
economy, and a distinct importable consumer. Source decimal means or claimed
form-factor comparisons remain blinded until the decomposition and identity
criteria are frozen.

## Proposed Claim Delta

Provisional `C-SG-011` would state an exact special-frequency cycle mean,
zero-mean remainder, and its inherited derivative invariance only if this is
scientifically distinct from current claims. Otherwise FS4 will be terminally
classified as duplicate evidence mapped to `C-SG-009`, `C-MOM-002`, and
`C-GW-004`. No physical form-factor, tidal, or backreaction claim is proposed.

## Implementation and Oracle Plan

SymPy will differentiate the exact accepted formula and verify offset
cancellation. The cycle mean will be derived analytically from a transform,
Fourier identity, or parameter integral rather than inferred from a grid; a
high-precision independent quadrature will remain corroboration. Pure package
APIs will expose a decomposition only if it has a reusable consumer. Mutations
replace the constant by a time-dependent function, shift the wrong tensor
component, confuse a cycle mean with transverse variance, or apply a physical
label without dependency closure. FS4 will be hash-checked and reproduced
once, using its NumPy compatibility path as implementation evidence only.

## Attempts and Continuation

Attempt `0001` will reproduce FS4, inventory its mean, form-factor, derivative,
waveform, power, T2C, G4, and physical interpretations, and compare each
predicate with accepted claims. Failed exact-integration representations or a
duplicate verdict remain durable evidence with the next route recorded.

## Debt Ledger

This ledger tracks mean exactness, zero-mean normalization, object identity,
offset sensitivity, distinctness, and physical scope.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| A sampled average may be treated as an exact static moment | Derive the cycle mean analytically or label it numeric evidence | discharged: no mean value is promoted; C-SG-009's full exact moment is sufficient |
| Static mean and fixed-profile form factor may be conflated | Derive their equality with definitions or keep them distinct | discharged: the imported value and arbitrary decomposition remain explicitly unidentified |
| Constant cancellation may be insensitive to time dependence | Mutate the offset to a nonconstant function and require failure | discharged: quadratic and cubic offsets break waveform and power invariance |
| A duplicate calculus identity may receive a redundant claim | Identify a distinct consumer or terminally classify duplicate evidence | discharged: FS4 is terminal duplicate evidence with no registry delta |
| Normalized and triple tensor offsets may mix | Carry the scale while proving all positive derivatives agree | discharged: both conventions agree after differentiation and inverse coefficient rescaling |
| Static cancellation may be called tidal or radiation physics | Supply accepted dynamics or explicitly exclude the interpretation | discharged: duplicate review excludes form-factor, tidal, backreaction, and physical radiation readings |

## Review and Promotion Plan

Any provisional claim receives an independent period-mean derivation and
claim-level review. A duplicate outcome instead receives a terminal duplicate
review with exact accepted mappings. Closure requires immutable attempts,
source adjudication, terminal FS4 disposition, affected-consumer replay,
registry/release/docs/memory agreement if changed, and one full unchanged-
boundary repository gate.

## Done Gate

P043 closes only when mean, remainder, derivative, convention, identity,
distinctness, physical-scope, consumer, disposition, and debt obligations are
all resolved.

## Adjudication Result

Candidate B is selected. Twenty-six primary and eight independent checks prove
that FS4's valid constant-offset statements are exactly subsumed by
`C-SG-009`, `C-MOM-002`, and `C-GW-004`. Time-dependent mutations establish
the load-bearing premise, while arbitrary decompositions show that derivative
cancellation cannot identify the imported scalar as a form factor. FS4 is
terminally classified as duplicate evidence; its T2C/G4 ceiling-lift,
factor-nine power, strict positivity, tidal, backreaction, and physical
radiation readings are not accepted. No redundant claim or release is added.
