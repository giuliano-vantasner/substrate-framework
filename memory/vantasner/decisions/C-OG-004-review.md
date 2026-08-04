---
description: Independent review of C-OG-004
author: vantasner-review
created: '2026-08-09T01:20:00Z'
updated: '2026-08-09T01:20:00Z'
tags: [substrate-framework, claim-review, optical-geometry, finite-width]
category: decisions
confidence: established
status: archived
---
# Review of C-OG-004

## Claim Under Review

The claim gives the exact second scale derivative and leading variance term for
a declared normalized centered profile average of the C-CC-001 slow optical
acceleration. It includes the explicit nonlinear index jet, third-derivative
weak-profile limit, dimensions, and reflection-center null while excluding an
MPD or field-derived reading.

## Sourced Inputs

The review read v0.100.0, C-OG-001 through C-OG-003, C-CC-001, C-SG-009,
P133's frozen contracts and attempts, the canonical optical and collective APIs,
hash-pinned T2C, phase three, FS1/FS2/FS4/P3D3/T1B adjudications, and G2/G4
reverse consumers. The profile-average prescription is explicit new conditional
input rather than a hidden physical law.

## Independence

The primary route differentiates the canonical C-CC-001 acceleration and calls
the new pure API. The independent route reconstructs the metric and point
acceleration without importing that API, derives the Gaussian Fourier moment,
checks cubic wave-number parity, and uses a reflection-symmetric index
countermodel.

## Verification Status

Exact SymPy identities prove the scale jet, nonlinear coefficient, weak limit,
and symmetry null. The independent Gaussian and direct connection derivations
agree. The claim therefore earns `symbolic_verified`; no numeric tolerance,
empirical comparator, or MPD premise enters the accepted statement.

## Sensitivity and Counterexamples

Riemann sign and coefficient mutations, Fourier sign and derivative-order
mutations, and first-, second-, or zeroth-background-derivative substitutions
fail. The even profile `n=1+beta*x^2/2` forces an exact centered null and rejects
T2C's curvature-width term. A linear index separates the accepted cubic order
from T2C's quadratic order and opposite sign.

## Framework Compatibility

The result composes naturally with C-CC-001 and retains the positive-index,
coordinate-time, and signal-speed conventions. The new input is only a
normalized centered effective profile average. It changes no accepted metric,
point trajectory, sine-Gordon moment, gravity equation, or physical ontology.

## Dependency and Consumer Replay

The direct dependency is C-CC-001, with C-OG-001 transitive. Direct consumers
are the pure collective-dynamics API, package export, tests, P133 verifiers, and
T2C's corrected disposition. Pending G2 and G4 replay but gain no authority and
do not execute the rejected T2C formula.

## Competing Candidate Audit

Candidates A through H froze before source-body inspection. Exact geometry and
the kernel identity survive, but the MPD candidate fails rank, derivative,
index, unit, symmetry, and dependency closure. The profile-average candidate is
selected by the predeclared structural criteria and independent countermodels,
not by T2C's reported decimal or thirteen-check tally.

## Four-Axis Decision

The exact conditional theorem supports a narrow compatible extension.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive consequence of C-CC-001 under an explicit profile-average premise

## Promotion Transaction

Promotion adds C-OG-004, its pure API and tests, P133 evidence and reviews,
qualifies T2C, creates v0.101.0, and regenerates canonical docs, memory, and the
migration queue. It promotes no MPD equation, raw SG quadrupole, or physical
gravity mechanism.

## Continuation if Not Accepted

Any derivative, dimension, or symmetry failure would withdraw the claim and
leave only the already accepted point acceleration. A physical finite-body law
would still require a separately varied field action or a fully typed covariant
multipole system.

## Done Gate

The exact positive object exists in importable code, its conditional premise and
units are explicit, independent derivations and mutations are sensitive, source
countermodels discriminate it from T2C, consumers pass, and claim debt is empty.

## Cross-References

See C-OG-001, C-CC-001, C-SG-009, P007, P040, P133, T2C, v0.101.0,
`collective_dynamics.py`, and the parent framework-migration effort.
