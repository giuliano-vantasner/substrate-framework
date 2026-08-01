---
description: Independent review of C-U1-001
author: vantasner-review
created: '2026-08-01T13:07:00Z'
updated: '2026-08-01T13:07:00Z'
tags:
- substrate-framework
- claim-review
- u1-current
category: decisions
confidence: working
status: archived
---
# Review of C-U1-001

## Claim Under Review
For an independently declared complex scalar `Psi` on 1+1 Minkowski spacetime
with signature `(+,-)`, define
`j^mu=i*(Psi_conj*d^mu(Psi)-Psi*d^mu(Psi_conj))`. Its divergence is exactly
`i*(Psi_conj*Box(Psi)-Psi*Box(Psi_conj))`. If the field and conjugate equations
use `Box(Psi)=F(|Psi|^2)*Psi` and its conjugate with real `F`, the current is
conserved on shell. A real field has zero current; a declared stationary phase
has density `2*omega*f^2`; a phase-breaking `lambda*Psi_conj` term leaks charge.

## Sourced Inputs
The review read `v0.13.0`, P014 and both attempts, the new U(1) module/tests,
the exact and independent verifiers, and hash-pinned EM1. EM1's complex
ontology, named potential, profile dynamics, electric-charge map, and 3+1
claims remain outside the delta.

## Independence
The main route expands arbitrary Cartesian real and imaginary field components.
The review independently writes `Psi=R*exp(-i*theta)` and derives the density and
spatial current directly. It does not import the proposed U(1) APIs.

## Verification Status
Exact symbolic differentiation proves the off-shell identity for arbitrary
functions, and exact EOM substitution proves the conditional on-shell result.
The oracle tests the actual conservation identity rather than only a stationary
ansatz. The maximum verdict is `symbolic_verified`.

## Sensitivity and Counterexamples
Wrong time sign, time coefficient, raised spatial sign, or simultaneous current
sign fails the coupled off-shell-and-stationary predicate. A genuinely real
field gives zero current. A complex restoring coefficient and a phase-breaking
conjugate-field term give nonzero divergence, while setting the breaking
coupling to zero restores conservation.

## Framework Compatibility
The claim is a compatible extension because it declares a separate complex
scalar theory and does not rewrite the accepted real sine-Gordon field. The
metric and current signs are encoded once. No potential, soliton profile,
electric charge, gauge field, or higher-dimensional stability premise is hidden.

## Dependency and Consumer Replay
The claim has no accepted scientific dependency. Its direct consumers are the
declared-profile specialization, the U(1) APIs/tests, EM1's disposition, and
future gauge-sector audits. No existing canonical symbol changes.

## Competing Candidate Audit
The proposal registered the full conditional theorem, stationary continuity
alone, and a physical charged-breather identification. The arbitrary-field
identity and symmetry guard select the first structurally. The second is too
weak, and the third conflicts with the real-field zero-current guard and lacks
ontology.

## Four-Axis Decision

The exact conditional theorem supports acceptance without accepting the
underlying complex model as realized physics.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive conditional field-theory claim

## Promotion Transaction
Promotion adds `u1_charge.py`, focused tests, exact and independent evidence,
`C-U1-001`, the frozen P014 campaign, a `v0.14.0` release, terminal source
qualification, and regenerated records.

## Continuation if Not Accepted
A sign or arbitrary-field failure would return to the raised-index convention.
Stationary ansatz checks could not substitute for the missing theorem.

## Done Gate
The positive local-current theorem, independent polar route, symmetry
counterexamples, mutation sensitivity, explicit scope, and consumers are
complete with no claim debt.

## Cross-References
See P014, EM1, `C-U1-002`, the U(1) module/tests, and the parent migration
effort.
