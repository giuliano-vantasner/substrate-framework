---
description: Independent review of C-GW-004
author: vantasner-review
created: '2026-08-01T19:30:00Z'
updated: '2026-08-01T19:30:00Z'
tags:
- substrate-framework
- claim-review
- conditional-power
- breathing-wave
category: decisions
confidence: working
status: archived
---
# Review of C-GW-004

## Claim Under Review

The claim states exact derivative, conditional power, convention-rescaling,
and arbitrary-inclination TT geometry for the declared axisymmetric separable
breather moment. It explicitly excludes a physical source or radiation claim.

## Sourced Inputs

The review read `v0.37.0`, `C-SG-009`, `C-MOM-002`, `C-GW-001`, `C-GW-002`,
their canonical modules, P042, and hash-pinned FS3. Pending FS4 and P3D3 are
consumers or candidate evidence, not dependencies.

## Exact Derivation

Direct differentiation of the accepted scalar moment gives `d=mu'''`. Trace
subtraction gives norm squared `2d^2/3` for normalized `I_STF'''`; multiplication
by three gives `6d^2` for triple `Q'''`. Inserting the inverse-rescaled waveform
coefficients into `C-GW-001` gives the same conditional power `2Gd^2/15` in
both conventions.

## Independent Route

The independent reviewer derives the special third derivative by a manual
chain rule, reconstructs trace removal directly, and contracts the tensor with
an explicit oriented transverse frame without calling the new package helper.
All exact factors agree.

## Verification Status

Finite differentiation, contractions, coefficient cancellation, symmetries,
and projection geometry support `symbolic_verified`. P042's quadratures are
not used to upgrade this exact claim and belong to separate `C-SG-010`.

## Sensitivity and Counterexamples

Power coefficients `6/5`, `2/5`, and `1/15` fail against the exact normalized
`2/15`. Triple waveform coefficients `2`, `1`, and `1/3` fail against `2/3`.
Exact symmetry phases give zero instantaneous power, refuting FS3's strict
pointwise positivity while a quarter-half-period phase is nonzero.

## Framework Compatibility

The result is a compatible conditional extension. It preserves both accepted
STF conventions and the premise-explicit waveform/flux boundary of
`C-GW-001`. Its normalized plus coordinate and conventional matrix readout are
kept distinct by the required square-root-of-two factor.

## Source Defects and Scope

FS3 uses triple `Q` with normalized coefficients, overstating field and power
by three and nine. Its FFT reuses its own sampled moment, and it imports the
retarded waveform while declaring the transverse embedding and coupling. It
supplies no complete source conservation or gravitational dynamics.

## Dependency and Consumer Replay

Accepted dependencies are `C-SG-009`, `C-MOM-002`, `C-GW-001`, and
`C-GW-002`. Direct consumers are the sine-Gordon and separable-moment APIs,
breathing-mode tests, P042, and FS3's disposition. FS4 and P3D3 remain pending.

## Competing Candidate Audit

Candidate A is selected because the exact pointwise power and full viewing
geometry close without spectral or physical-source assumptions. Candidate B
is too narrow. Candidate C fails dependency closure and is excluded rather
than used to revise accepted invariants.

## Four-Axis Decision

The decision applies only to conditional tensor and wave-functional algebra.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: depends on C-SG-009, C-MOM-002, C-GW-001, and C-GW-002

## Promotion Transaction

Promotion extends pure derivative and TT readout APIs, freezes P042, qualifies
FS3, adds the next pinned release, and synchronizes generated state. It does
not promote source dynamics, gravity, physical radiation, or a detector signal.

## Done Gate

Derivative exactness, tensor conventions, conditional coefficients, viewing
geometry, mutations, source boundary, consumers, and claim-specific debt are
closed.

## Cross-References

See P042, FS3, `C-SG-009`, `C-MOM-002`, `C-GW-001`, `C-GW-002`, and the parent
migration effort.
