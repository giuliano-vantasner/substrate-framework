---
description: Audit EL4's one-loop frontier form while retaining its free scale and coupling
author: vantasner
created: '2026-08-01T14:18:26Z'
updated: '2026-08-01T14:24:53Z'
tags:
- substrate-framework
- campaign-proposal
- conditional-rg-invariant
- migration-EL4
category: proposals
confidence: exploratory
status: archived
---
# P021 Frontier RG Coordinate

## Question and Positive Deliverable
P021 must determine whether EL4 contains a new exact object beyond the accepted
mass-coordinate reparameterization. The positive target is a premise-explicit,
importable one-loop running-coupling invariant and, only if distinct and closed,
its conditional composition with the mass coordinate. An electron label or a
numerically close mass does not complete the campaign.

## Base Release and Provenance
The accepted base is `v0.18.0` at commit `e268261`. Direct authority is
`C-DIM-002`, `C-DIM-003`, and `C-DIM-004`; none fixes a length, a coupling, a
beta-function coefficient, or a particle identity. The hash-pinned candidate
is EL4 at
`merged-framework/bridges/phase-46/bridge_EL4_me_in_the_frontier_form.py`,
SHA-256 `4ae8185505b11d3cf2beffcbb6ec786e4bfbdd57e00cd42b8fc223a28a17cf2f`.
Its listed AS, CF, QCD, B, OD, and later EL dependencies remain noncanonical
unless separately mapped to an accepted claim. Memory search found the parent
migration direction and prior coordinate audits only; it supplies no premise.

## Invariants, Conventions, and Allowed Imports
The positive speed, action, length, mass, coupling, and beta-function
coefficient remain explicit. `C-DIM-003` is a lossless coordinate map and
`C-DIM-004` is conditional on both of its unit equations. A running-coupling
invariant must use the total derivative along the declared flow, not a partial
derivative at fixed coupling. The UV reference scale and any proportionality
between an RG scale and a mass-energy are independent premises. No pending
QCD coefficient, hedgehog number, observed hierarchy, or electron value is an
allowed derivation input.

## Candidate Preregistration
The candidates are frozen before EL4's full body or comparator values are read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Promote the exact invariant of a declared one-loop asymptotically-free flow, plus any closed conditional coordinate composition | Positive solution of the declared beta ODE; explicit scale identification and mass coefficient for the composition | `b0`, boundary coupling, reference scale, optional mass coefficient | Compatible extension retaining all inputs | Differentiate along the ODE, solve independently, test boundary data, and mutate sign/coefficient |
| B | Classify EL4's mass form as a duplicate reparameterization of C-DIM-003/C-DIM-004 | Existing accepted coordinate maps only | Free mass coordinate | Preferred if the exponential merely renames the free coordinate | Normalize the formula and vary its coupling or prefactor without violating dimensions |
| C | Promote EL4's electron mass as derived from one length and one coupling | Treat source scale, coupling, beta coefficient, and object map as established | Hidden physical inputs | Conflicts with the accepted information boundary | Inventory dependencies and construct two admissible premise sets giving different masses |

## Selection Criteria and Blinding
Selection is ordered by exact ODE closure, correct total-derivative semantics,
retention of independent inputs, dimensional consistency, limiting behavior,
dependency economy, and distinct reusable reach. Candidate A survives only as
a conditional theorem. Candidate C fails if any physical coefficient, scale,
coupling value, or object identification is imported. All observed masses,
hierarchy estimates, and fitted operating-point values remain blinded until the
symbolic equations, conventions, mutations, and selection verdict are frozen.

## Proposed Claim Delta
Provisional `C-RGE-001` states that a positive coupling satisfying
`mu*dg/dmu=-(b0/(16*pi^2))*g^3`, with `b0>0`, has the exact trajectory invariant
`Lambda=mu*exp(-8*pi^2/(b0*g^2))`. If `mu0=S*c0/a`, then the corresponding
length `S*c0/Lambda` is conditionally
`a*exp(8*pi^2/(b0*g(mu0)^2))`. Provisional `C-DIM-005` adds the distinct
composition: if `g(mu0)^2=beta^2` and `m*c0^2=q*Lambda`, then
`N_m=q*exp(-8*pi^2/(b0*beta^2))`. Nothing in this delta selects `a`, `b0`, the
boundary coupling, `q`, a mass, or a particle.

## Implementation and Oracle Plan
If it survives audit, a pure RG module will expose the invariant and exact
one-loop trajectory without executing simulations. SymPy is appropriate for
separation, substitution, total differentiation, limits, and exact coefficient
mutations. An independent review will integrate the reciprocal squared
coupling rather than importing the implementation. Counterexamples will hold
the coupling fixed when differentiating, reverse the beta-function sign, and
alter the factor `16*pi^2`; each must change the relevant verdict. Package
tests will enforce positivity and boundary recovery. Numerical values, if
present in EL4, are regression evidence only and cannot verify the exact claim.

## Attempts and Continuation
Attempt `0001` will reproduce the pinned source, inventory every premise, and
separate its exact ODE algebra from physical mappings and comparator use. A
technical failure will be repaired append-only. If the invariant is already
accepted under another exact claim, Candidate B replaces it. If only the
physical electron reading fails, the exact conditional object remains live and
EL4 receives a mixed terminal disposition.

## Debt Ledger

The campaign tracks four premise-closure and selection debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The source may confuse a partial with a total scale derivative | Derive both and state the precise invariant semantics | discharged |
| The beta coefficient and boundary coupling may be called derived | Claim and import inventory retain them as premises | discharged |
| A mass prefactor may import pending soliton claims | Exclude it or expose every dependency in a conditional API | discharged |
| Comparator values may select the formula | Freeze symbolic selection before inspecting them | discharged |

## Review and Promotion Plan
Review will independently integrate the ODE, audit EL4 check by check, and map
every direct and indirect consumer. Promotion requires package APIs/tests,
claim-level review, a terminal EL4 disposition with durable evidence, registry
and release synchronization, generated records, targeted replay, and one full
repository gate at the unchanged promotion boundary.

## Results and Promotion
EL4 reproduces all ten source checks. The main audit passes 22 exact checks, the
independent reciprocal-coupling derivation passes five, and 33 focused tests
pass. `C-RGE-001` retains the ODE and all boundary data as premises;
`C-DIM-005` retains `q`, `b0`, and `beta^2`. EL4 is qualified because its
unpinned prefactor can reproduce any mass coordinate, its free-length guard
remains full-column-rank, and its hedgehog solve lacks the numerical evidence
needed for promotion.

## Done Gate
P021 is complete. Both positive exact objects exist with complete premise
closure, mutation-sensitive and independent verification, EL4 is terminally
qualified, all affected consumers pass, and campaign debt is empty.
