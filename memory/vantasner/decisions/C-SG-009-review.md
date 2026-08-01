---
description: Independent review of C-SG-009
author: vantasner-review
created: '2026-08-01T18:45:50Z'
updated: '2026-08-01T18:45:50Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- energy-moment
category: decisions
confidence: working
status: archived
---
# Review of C-SG-009

## Claim Under Review

The claim gives the exact centered second spatial moment of the accepted
breather's normalized 1+1 Hamiltonian density, its extrema, and its temporal
symmetry. It expressly denies that this scalar alone is a 3+1 quadrupole or
radiation source.

## Sourced Inputs

The review read `v0.35.0`, `C-SG-001`, `C-SG-002`, the canonical sine-Gordon
module, P040, and hash-pinned FS1. Pending FS2-FS4 and P3D3 were inventoried as
source narrative consumers rather than dependencies.

## Exact Derivation

After scaling `y=eta*x` and writing
`b=(eta/omega)*sin(omega*t)`, the Hamiltonian density reduces to a linear
combination of `1/(cosh(y)^2+b^2)` and its parameter derivative. The contour-
integral Fourier transform is differentiated twice at zero spatial frequency.
The two resulting terms collapse to the registered closed formula before any
FS1 value or form-factor comparator is inspected.

## Independence

The independent route rebuilds `u`, `u_x`, `u_t`, and the Hamiltonian density
from elementary floating-point functions. Adaptive quadrature on scaled finite
domains 12, 18, and 24 with absolute and relative tolerances `1e-11` agrees
across four family points and shows improving tail convergence. It does not call
the new moment API.

## Verification Status

The transform derivation, exact extrema, evenness, period, and mutations support
`symbolic_verified`. The independent quadrature and FFT are corroborating
numeric evidence. No exact claim is inferred from FS1's decimal comparator.

## Sensitivity and Counterexamples

Halving either transform coefficient fails. Quarter-, third-, and eighth-cycle
shifts fail the half-period predicate. Doubling the time-kinetic half factor or
removing the potential term breaks direct quadrature agreement. A correctly
normalized static kink remains a constant-moment counterexample.

## Framework Compatibility

The result is native to `C-SG-001` and `C-SG-002`. The breather is centered at
the coordinate origin; translating the origin would change a raw second moment.
The formula is dimensionless in the accepted normalized 1+1 conventions. No
3+1 embedding or physical mass interpretation is introduced.

## Source Defects and Scope

FS1's four broad checks reproduce, and its current NumPy compatibility alias is
correct. Its mean split uses the same samples and is linear bookkeeping. Its
kink derivative is too large by two. Its `2*omega` statement must mean base and
dominant special-case frequency, not a pure sinusoid, and none of this supplies
a gravitational source or radiation law.

## Dependency and Consumer Replay

Accepted dependencies are `C-SG-001` and `C-SG-002`. Direct consumers are the
sine-Gordon module and tests, P040, and FS1's terminal disposition. P001-P003
breather tests replay unchanged. Later FS units remain pending consumers.

## Competing Candidate Audit

Candidate A is selected because the exact spatial transform closes. Candidate
B would preserve unnecessary numerical error. Candidate C fails its dependency
closure because a scalar 1+1 moment is not a conserved 3+1 STF source and no
accepted physical field law connects it to radiation.

## Four-Axis Decision

The axes apply only to the centered normalized 1+1 energy-moment theorem.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: depends on C-SG-001 and C-SG-002

## Promotion Transaction

Promotion extends the pure sine-Gordon API and exact tests, freezes P040,
qualifies FS1, adds `v0.36.0`, and synchronizes generated and durable records.
It does not promote a 3+1 quadrupole, gravitational radiation, or substrate
finite-size mechanism.

## Done Gate

Convergence, formula, extrema, period, harmonic meaning, mutations, source
defects, physical boundary, consumers, and campaign debt are closed.

## Cross-References

See P040, FS1, `C-SG-001`, `C-SG-002`, `sine_gordon.py`, and the parent migration
effort.
