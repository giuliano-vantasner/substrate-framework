---
description: Derive a lossless dimensionless coordinate for imported mass relative to the accepted primitive basis
author: vantasner
created: '2026-08-01T13:50:33Z'
updated: '2026-08-01T13:54:42Z'
tags:
- substrate-framework
- campaign-proposal
- dimensional-analysis
- migration-EL1
category: proposals
confidence: exploratory
status: archived
---
# P018 Imported Mass Coordinate

## Question and Positive Deliverable
P018 must construct and audit the exact map between an independently supplied
mass `m` and its dimensionless coordinate relative to the accepted
speed-action-length basis. The positive object is a reusable, invertible API
for `N_m=m*c0*a/S` and `m=N_m*S/(c0*a)`, plus a terminal adjudication of EL1's
claims about what this reparameterization does and does not eliminate. Merely
renaming an imported mass or reproducing EL1's tally is not completion.

## Base Release and Provenance
The accepted base is `v0.15.0` at commit `791ae87`. Direct authority is
`C-DIM-002` and its dimensional-analysis API. `C-SK-001` is available only for
auditing a conditional consumer, and P017 establishes that MR1 adds no stronger
mass premise. The hash-pinned candidate is EL1 at
`merged-framework/bridges/phase-46/bridge_EL1_import_is_one_pure_number.py`,
SHA-256 `d39debe384fed8383fdf65161e29b0a8de7e574dcc4f394d9011760814e4dae4`.
Its AS2 and MR1 prerequisites are now terminally adjudicated; S5 remains
qualified and supplies no unconditional mass formula. Memory search surfaced a
historical one-length discussion, but it is neither project authority nor an
allowed premise.

## Invariants, Conventions, and Allowed Imports
Dimension rows are `(M,L,T)` and primitive columns are speed `c0`, action `S`,
and length `a`. The basis is set-local. A dimensionless coordinate is lossless
only when all scale inputs are positive and retained; it does not predict the
coordinate, remove empirical information, or select physical primitive values.
No electron value, SI conversion, observed ratio, pending source unit, or
claimed one-length ontology may select the theorem.

## Candidate Preregistration
The routes are frozen before reading EL1's full check body.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Promote a lossless mass-coordinate bijection relative to `{c0,S,a}` | Positive mass and primitive values; C-DIM-002 | One free dimensionless coordinate per imported mass | Distinct reusable composition of the basis theorem | Prove dimensions and both inverse identities; mutate each factor |
| B | Classify EL1 wholly as duplicate evidence for C-DIM-002 | Accepted unique mass monomial only | none | Preferred if EL1 adds no import/reconstruction semantics or consumer | Compare exact claim scope and package consumer need |
| C | Treat reparameterization as eliminating the mass import or closing absolute scale | Dimensionless coordinate assumed fixed or predicted | Hidden numerical coordinate | Conflicts with set-local and coefficient-free invariants | Vary `N_m` while keeping all dimensions valid and reconstruct different masses |

## Selection Criteria and Blinding
Selection is ordered by exact invertibility, dimension closure, retained
information, dependency economy, distinct consumer reach, and mutation
sensitivity. Candidate A survives only if the forward/inverse map adds a useful
import boundary beyond `C-DIM-002`; otherwise B is selected. Candidate C must
fail whenever arbitrary dimensionless coordinates remain admissible. EL1's
physical constants and numerical outputs remain blinded until the symbolic API,
criteria, and mutations are frozen.

## Proposed Claim Delta
The provisional `C-DIM-003` states that, relative to `C-DIM-002`'s declared
positive primitives, specifying a mass `m` is bijectively equivalent to
specifying the dimensionless coordinate `N_m=m*c0*a/S`, with inverse
`m=N_m*S/(c0*a)`. The map changes representation but neither predicts `N_m`
nor removes one independent dimensionless input. Direct consumers are the
canonical dimensional-analysis API, EL1's source disposition, and later import
audits. No physical mass relation is proposed.

## Implementation and Oracle Plan
The dimensional-analysis module will gain pure forward and inverse mass-
coordinate functions with numeric positivity guards. SymPy exact algebra fits
the dimension and bijection obligations. The verifier will derive the mass
monomial from the accepted matrix, prove both compositions are identities,
show the coordinate is dimensionless, and reject swapped factors, wrong powers,
zero inputs, and a fixed-coordinate closure. An independent review will solve
the exponent equations and reconstruct the map without importing the new APIs.
Campaign verifiers run with `PYTHONPATH=src`. Numerical EL1 examples cannot add
independent evidence to an exact bijection.

## Attempts and Continuation
Attempt `0001` will reproduce hash-pinned EL1 and execute the exact map and
scope audit. Technical failures will be repaired without changing the claim.
If the map is an unused restatement, `C-DIM-003` will be withdrawn and EL1
preserved as duplicate evidence. If EL1 assumes a coordinate value, that
physical route will be rejected while the exact map remains under review.

## Debt Ledger
The campaign starts with four explicit debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The coordinate may be mistaken for a prediction | Claim and API retain arbitrary `N_m` | discharged |
| Positive/nonzero domains may be implicit | APIs and mutations enforce them | discharged |
| EL1 may import qualified S5 physics | Source audit maps every consumer without promoting its premise | discharged |
| The map may duplicate C-DIM-002 without useful semantics | Claim-level consumer review selects promotion or duplicate | discharged |

## Review and Promotion Plan
An independent reviewer will rederive the exponent solution, information count,
and inverse map, then audit every EL1 check as exact composition, regression,
declared input, or unsupported scale closure. Promotion requires package APIs
and tests, individual claim review, a qualified or migrated EL1 disposition,
registry/release synchronization, generated docs/memory, targeted replay, and
one full repository gate at the unchanged promotion boundary.

## Results and Promotion
EL1's nine source checks reproduce at the pinned hash. Attempt `0001` passes 18
exact checks; independent exponent elimination passes six checks; and 20 focused
consumer tests pass. `C-DIM-003` is accepted because its forward/inverse APIs
form a distinct information-preserving import boundary. EL1 is qualified: the
coordinate remains free, its mass ratio is not thereby derived, and its regex
census cannot establish one semantic role for every consumer.

## Done Gate
P018 is complete. The positive mass-coordinate object is importable and
invertible, all scale information and assumptions are explicit, mutations are
load-bearing, EL1 is terminally qualified, every affected consumer agrees, and
the debt ledger is empty.
