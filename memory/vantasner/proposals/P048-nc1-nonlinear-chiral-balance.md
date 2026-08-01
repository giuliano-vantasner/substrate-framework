---
description: Derive exact nonlinear sine-Gordon chiral balance and audit NC1
author: vantasner
created: '2026-08-01T21:47:44Z'
updated: '2026-08-01T23:58:00Z'
tags:
- substrate-framework
- campaign-proposal
- sine-gordon
- migration-NC1
category: proposals
confidence: exploratory
status: archived
---
# P048 NC1 Nonlinear Chiral Balance Audit

## Question and Positive Deliverable

P048 must derive an importable exact account of what replaces the free-field
left/right split in the full normalized sine-Gordon equation. The positive
object is a convention-explicit theorem giving the sourced balance of both
naive derivative currents, a genuinely conserved local current with its
integrated charge hypotheses, and the exact spatial-parity action on that
charge. Rejecting a claimed physical V-A interpretation without supplying the
positive conservation object would not complete the campaign.

## Base Release and Provenance

The accepted base is `v0.42.0` at framework commit `bd60154`; its scientific
transaction is commit `288e646`. `C-SG-001` fixes the normalized real 1+1
sine-Gordon equation, while `C-TOP-001` supplies only an abstract integer
winding-sign character and no field-theory realization. NC1 is pending source
evidence at `substrate@6d1f4e0`, SHA-256
`b7206df001095b2706818ea5f3ffde13d24887816d867f7252da460588b010f5`.
Its declared dependencies W1, W3, and W7 are pending and are not permitted
imports. Memory search found the active migration frontier but no accepted NC1
result.

## Invariants, Conventions, and Allowed Imports

The equation is `phi_tt-phi_xx+sin(phi)=0` in dimensionless coordinates.
Define `J_plus=phi_t+phi_x`, `J_minus=phi_t-phi_x`, and
`partial_plus=(partial_t+partial_x)/2`,
`partial_minus=(partial_t-partial_x)/2`. A topological current, if selected,
must state its index components and normalization rather than borrow the
independent complex-field U1 current. Mixed partials may commute for a smooth
real field. An integrated charge requires convergent boundary limits; integer
winding additionally requires finite-energy vacuum limits `2*pi*n`. Spatial
parity invariance of the equation, exchange of topological sectors, selection
of one sector, and a physical parity-violating interaction are separate
claims. No bosonization dictionary or weak-sector ontology is allowed.

## Candidate Preregistration

The alternatives are frozen from the queue question and accepted framework
before reading the full NC1 executable.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact sourced naive-current balances plus identically conserved topological current and parity-sector map | Smooth real SG field; boundary limits only for charge | Explicit normalization `2*pi` | Native and minimal | Direct symbolic differentiation, EOM reduction, boundary theorem, parity and kink/antikink tests |
| B | Conserved stress-energy currents as the nonlinear chiral replacement | Accepted SG action and Noether stress tensor | Light-cone normalization | Exact but broader and likely belongs to NC2 | Compare assumptions and whether it answers NC1 without importing the next source unit |
| C | A selected topological sector is itself a derived physical V-A mechanism | Pending W1/W3/W7 and a physical current dictionary | Interaction and sector-selection inputs | Dependency conflict expected | Accepted-dependency audit and parity-invariance counterexample |

## Selection Criteria and Blinding

Selection is ordered by exact equation compatibility, accepted-dependency
closure, conservation strength, explicit boundary conditions, normalization
and light-cone factor closure, correct free-field/vacuum/kink/antikink/parity
limits, assumption economy, and reusable API scope. No empirical comparator is
needed for an exact identity campaign. The predecessor's detailed conclusions
remain unopened until current definitions, parity convention, proposed
oracles, and mutations are frozen in this contract.

## Proposed Claim Delta

Provisional `C-SG-011` will state, if verified, that both naive derivative
currents have the same potential source on shell, including the exact
light-cone half factors; that the explicitly normalized topological current is
identically conserved off shell for smooth fields; that finite-energy vacuum
boundaries give integer winding charge; and that spatial parity exchanges
opposite winding sectors while leaving the sine-Gordon equation invariant.
The claim will explicitly withhold independent chiral-current conservation,
intrinsic parity violation, V-A dynamics, weak charge, particle identity, and
bosonization conclusions.

## Implementation and Oracle Plan

The canonical sine-Gordon module will expose pure current, balance, divergence,
charge, and parity helpers. SymPy is the strongest oracle because all proposed
statements are exact differential identities. The primary verifier will derive
the naive defects from definitions before applying the EOM, verify both
light-cone factors, prove the topological divergence by commuting mixed
partials, and check the boundary charge. Mutations will flip a current sign,
drop the `2*pi` normalization, replace a half light-cone derivative by a full
one, and add a non-topological field component; each must fail a relevant
predicate. Independent rederivation will use differential-form or boundary
calculus without calling the new balance helpers. Free waves, constant vacua,
explicit kink/antikink profiles, and spatial parity provide exact limits and
counterexamples. Targeted replay includes sine-Gordon and topological-label
tests; the full repository gate runs once at the final promotion boundary.

## Attempts and Continuation

Two attempts are preserved. Attempt 0001 passed the 31-check primary verifier
but failed after four independent checks because SymPy retained the kink charge
as an unevaluated integral whose simplified value is one. Attempt 0002 changed
only that representation normalization and passed all 31 primary and seven
independent checks. Candidate A is selected. Candidate B remains reserved for
NC2's stress-tensor question, and Candidate C is rejected by exact parity
invariance and missing accepted weak-interaction dependencies.

## Debt Ledger

This ledger tracks current normalization, conservation type, boundary
hypotheses, parity semantics, source mapping, and affected consumers.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| NC1's exact executable claims have not been audited | Reproduce the hash-pinned source and review each conclusion | discharged by the source reproduction and sentence-level adjudication |
| No canonical nonlinear chiral-balance API exists | Implement pure definitions with exact package tests | discharged by the canonical sine-Gordon APIs and tests |
| Topological conservation may be conflated with physical V-A parity violation | Prove the parity map and preserve the interpretation ceiling | discharged by exact equation invariance, axial-current transformation, and source qualification |
| Direct and downstream consumers are not inventoried | Run impact analysis and targeted/global replay before promotion | discharged by graph analysis, targeted replay, and the full repository gate |

## Review and Promotion Plan

The exact claim received an individual review from raw verifier and independent
rederivation artifacts. Promotion adds the importable implementation, package
tests, append-only attempts, source reproduction, sentence-level adjudication,
consumer replay, qualified NC1 disposition, registry and v0.43 release,
rendered documentation, synchronized accepted memory, status-zero full
validation, and clean diff check.

## Done Gate

P048 closes with the exact positive conservation object, verifier sensitivity,
independent rederivation, accepted claim review, qualified source disposition,
consumer replay, synchronized canonical state, and an empty campaign debt
ledger. The parent corpus-migration effort continues to NC2.
