---
description: Audit QCD3's exact SU(3) invariants and conditional one-loop coefficient
author: vantasner
created: '2026-08-01T14:49:01Z'
updated: '2026-08-01T15:07:43Z'
tags:
- substrate-framework
- campaign-proposal
- su3-group-factors
- migration-QCD3
category: proposals
confidence: exploratory
status: archived
---
# P024 SU(3) One-Loop Coefficient

## Question and Positive Deliverable
P024 must derive the exact invariants of the source's explicit fundamental
SU(3) representation and determine what beta-function conclusion follows only
after the one-loop coefficient formula is declared. The positive deliverable is
importable exact Lie-algebra data and, if dependency-honest, a conditional
coefficient/sign theorem. A copied perturbative formula or physical label alone
does not complete the campaign.

## Base Release and Provenance
The accepted base is `v0.20.0` at commit `12205e9`. `C-RGE-001` accepts a flow
only conditionally on positive `b0`; it does not derive that coefficient. The
hash-pinned candidate is QCD3 at
`merged-framework/bridges/phase-8/bridge_QCD3_asymptotic_freedom.py`, SHA-256
`7d7c9a9bc2f04c933fc62484fec3329c0eb7769bb54ba8cd67701da5110af0ca`.
Its EM5 and YM1 dependencies remain pending. Memory search supplies no group
factor or loop premise.

## Invariants, Conventions, and Allowed Imports
Generators use the explicit convention `T_a=lambda_a/2` and commutator
`[T_a,T_b]=i*f_abc*T_c`. Matrix traces may derive representation invariants.
The four-dimensional one-loop beta formula and its gauge/matter coefficients
are declared external premises unless independently derived; matrix algebra
cannot prove a loop calculation. Flavor count is an explicit nonnegative
integer. No physical substrate-to-QCD identification is accepted.

## Candidate Preregistration
The candidates are frozen before the full QCD3 body is read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Promote exact fundamental and adjoint SU(3) invariants plus a premise-explicit one-loop specialization | Explicit matrices; declared standard beta formula for the second claim | Integer `n_f` | Compatible extension of C-RGE-001 | Recompute traces, commutators, Casimirs, coefficient, threshold, and mutations |
| B | Promote only exact Lie-algebra invariants | Explicit matrices only | None | Preferred if loop coefficients are merely imported | Separate every matrix-derived equality from field-theory premises |
| C | Promote physical asymptotic freedom of the substrate sector | Accept YM1/EM5, matter representation/count, and loop formula as closed | Physical field content | Conflicts if any dependency remains pending | Dependency inventory and alternative matter-content counterexamples |

## Selection Criteria and Blinding
Selection is ordered by exact convention closure, derivation/import separation,
dependency economy, representation consistency, coefficient sensitivity,
integer-flavor threshold, and reusable reach. Candidate C cannot be selected by
agreement with known QCD values. Numerical running probes remain blinded until
symbolic matrices, formulas, and mutations freeze.

## Proposed Claim Delta
Provisional `C-LIE-001` records exact trace normalization, structure constants,
and fundamental/adjoint Casimirs for the declared generators. Provisional
`C-RGE-002` states only conditionally that substituting those invariants into
the declared one-loop formula gives `b0=11-(2/3)*n_f`, positive for integer
`0<=n_f<=16`; it does not derive the loop formula or physical field content.

## Implementation and Oracle Plan
A pure SU(3) module will expose exact generators, structure constants, and
Casimirs if they survive audit. SymPy matrices are the strongest oracle.
Mutations change generator normalization, commutator sign, trace factor, and
gauge/matter coefficients. An independent review will use completeness and
trace sums rather than implementation helpers. Focused tests will cover all
generator pairs and Casimir matrices.

## Attempts and Continuation
Attempt `0001` will reproduce QCD3 and inventory each check's actual premise.
Technical failures are append-only. If group identities pass but loop closure
does not, Candidate B remains a positive completed result and QCD3 is qualified.

## Debt Ledger
The campaign tracks convention and import debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Generator normalization may be assumed | Construct and test every matrix | discharged |
| Loop coefficients may be narrated as group algebra | Mark the beta formula as a premise | discharged |
| Flavor content may be hidden | Retain `n_f` and test the sign threshold | discharged |
| Pending YM1/EM5 may leak into physical closure | Exclude or terminally qualify that reading | discharged |

## Review and Promotion Plan
Independent review will reconstruct invariants and audit QCD3 check by check.
Promotion requires package APIs/tests, individual claim decisions, terminal
source disposition, registry/release/generated synchronization, targeted
replay, and one unchanged full release gate.

## Results and Promotion
QCD3 reproduces all nine source checks. The main audit passes 27 exact checks,
the independent completeness route passes five, and 19 focused tests pass.
`C-LIE-001` promotes the standard representation invariants. `C-RGE-002`
promotes only the weight-explicit conditional coefficient and exact sign window.
QCD3 is qualified because its loop weights and physical substrate field content
are not derived and its “why SU(3)” narrative is not a uniqueness theorem.

## Done Gate
P024 is complete. Both exact positive objects, premise boundary, mutations,
independent review, consumers, QCD3 disposition, and debt closure pass.
