---
description: Independent review of C-GW-003
author: vantasner-review
created: '2026-08-01T18:27:49Z'
updated: '2026-08-01T18:27:49Z'
tags:
- substrate-framework
- claim-review
- circular-pair
- conditional-waveform
category: decisions
confidence: working
status: archived
---
# Review of C-GW-003

## Claim Under Review

The claim states exact moment derivatives and a convention-complete conditional
TT waveform for two equal point masses on declared opposite circular paths. It
excludes binding, breather identity, physical gravity, and detector claims.

## Sourced Inputs

The review read `v0.34.0`, `C-MOM-001`, `C-GW-001`, `C-GW-002`, the P039
proposal and APIs, and hash-pinned GW4. The special breather energy reproduces
`C-SG-002`, but that value is not needed by the general theorem and creates no
3+1 source embedding. Pending FS2/P3D3 are inventoried, not imported.

## Independence

The main route calls shared discrete-moment and TT APIs. The independent route
builds both particle dyads directly, differentiates them without the new helper,
constructs its viewing frame and basis tensors, and performs a separate finite-
difference refinement. It agrees on all load-bearing coefficients.

## Verification Status

Exact symbolic identities support `symbolic_verified`. The numerical refinement
is a sensitivity cross-check rather than the claim's authority. The conditional
power inherits declared waveform and flux premises and is not exact evidence
for a physical gravitational theory.

## Sensitivity and Counterexamples

Changing derivative order fails the norm predicate. Scaling the moment by
three without inversely scaling the waveform coefficient produces a factor-
three field and factor-nine power error. Static and uniformly translating pairs
have zero third derivative, while the circular path accelerates and exposes its
missing force/stress premise. Constant origin translation leaves the radiating
third derivative unchanged.

## Framework Compatibility

The new claim is a compatible specialization of `C-MOM-001`, `C-GW-001`, and
`C-GW-002`. It uses each mass's orbital radius `a`; pair separation is `2a`.
Normalized basis coordinates and conventional matrix read-offs remain distinct.
No coefficient from the noncanonical source is used to select the claim.

## Source and Compatibility Defects

GW4 stops at removed `numpy.trapz` under NumPy 2.5.1; the current API is
`numpy.trapezoid`. More substantially, GW4 combines `Q=3 I_STF` with the
coefficient for `I_STF`, while its headline factor 32 also conflicts with its
executable factor 1152. P039 corrects these convention errors rather than
patching an immutable source artifact.

## Dependency and Consumer Replay

Accepted dependencies are `C-MOM-001`, `C-GW-001`, and `C-GW-002`. Direct
consumers are `circular_pair.py`, exports, exact tests, P039, and GW4's terminal
disposition. Their focused closure passes with the pre-existing TT tests.

## Competing Candidate Audit

Candidate A is selected because the arbitrary-inclination conditional waveform
closes exactly. Candidate B is unnecessarily weak. Candidate C fails because a
declared accelerated point path and a borrowed 1+1 rest energy supply neither a
conserved isolated 3+1 source nor binding, orbital dynamics, or gravity.

## Four-Axis Decision

The four axes apply only to the exact kinematic and conditional theorem.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: depends on C-MOM-001, C-GW-001, and C-GW-002

## Promotion Transaction

Promotion adds a pure circular-pair API and tests, freezes P039, qualifies GW4,
adds `v0.35.0`, and synchronizes generated records and parent effort. It does
not promote a breather binary, gravitational radiation, or observed waveform.

## Done Gate

Radius convention, harmonics, observer geometry, basis normalization, power
convention, source API failure, mutations, physical boundary, consumers, and
campaign debt are closed.

## Cross-References

See P039, GW4, `C-MOM-001`, `C-GW-001`, `C-GW-002`, `circular_pair.py`, and the
parent migration effort.
