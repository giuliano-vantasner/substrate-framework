---
description: Audit CF4 dimensional transmutation and confinement overreach
author: vantasner
created: '2026-08-01T15:14:48Z'
updated: '2026-08-01T15:19:49Z'
tags:
- substrate-framework
- campaign-proposal
- dimensional-transmutation
- migration-CF4
category: proposals
confidence: exploratory
status: archived
---
# P025 CF4 Dimensional Transmutation

## Question and Positive Deliverable
P025 must separate CF4's exact one-loop and dimensional statements from its
physical confinement narrative. The positive deliverable is a terminal,
claim-level migration decision: either an importable premise-explicit
string-tension scaling theorem that is genuinely distinct from accepted work,
or a demonstrated duplicate map with the physical overclaim excluded. A
one-loop coupling singularity by itself is not a confinement mechanism.

## Base Release and Provenance
The accepted base is `v0.21.0` at commit `2b863d4`. `C-RGE-001` already accepts
the exact one-loop solution, transmutation scale, total RG invariance, and
formal inverse-coupling zero while explicitly excluding confinement.
`C-RGE-002` conditionally specializes the coefficient to
`b0=11-(2/3)*n_f`. The hash-pinned candidate is CF4 at
`merged-framework/bridges/phase-10/bridge_CF4_dimensional_transmutation.py`,
SHA-256 `e8fa7072d78ba5462ef9410689090f4627528c3632d45afd528c0c118f863c6b`.
Memory search found historical transmutation discussion but no accepted
claim beyond the registry entries, so every reused fact will be sourced here.

## Invariants, Conventions, and Allowed Imports
The one-loop ODE and coefficient retain all premises and domains of
`C-RGE-001` and `C-RGE-002`. A formal zero of inverse coupling may sit outside
perturbative control and cannot be renamed confinement. Exact dimensional
algebra is allowed, but existence and positivity of a physical string tension,
the assertion that Lambda is the only scale, and any dimensionless coefficient
must remain explicit premises unless independently derived.

## Candidate Preregistration
The candidates are frozen from the migration metadata before reading the full
CF4 body.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Map the RGE derivation to `C-RGE-001` and promote only `sigma=k*Lambda^2` as a conditional scaling theorem | Lambda is the sole dimensionful mass scale; sigma exists with mass dimension two | Free dimensionless `k` | Compatible if it has reusable content not already accepted | Buckingham kernel, premise mutations, and exact duplicate map |
| B | Treat every valid exact CF4 subclaim as duplicate or elementary consequence | Accepted RGE claims only | None | Preferred if the scaling form adds no distinct explanatory or consumer value | Compare statement-by-statement with the accepted registry and APIs |
| C | Promote physical confinement from asymptotic freedom and the one-loop pole | Nonperturbative confinement follows from a perturbative flow | Hidden string-tension dynamics | Conflicts with `C-RGE-001` unless an independent nonperturbative mechanism is present | Inspect dependency closure for an area law, flux tube, or equivalent oracle |

## Selection Criteria and Blinding
Selection is ordered by nonperturbative implication closure, separation of
dimensional form from dynamical existence, assumption economy, novelty beyond
accepted claims, exact unit and limit closure, and sensitivity to sole-scale
and prefactor premises. Numerical or phenomenological values cannot select a
candidate. Full source outputs remain unread until this contract is stored.

## Proposed Claim Delta
Candidate A provisionally names `C-DIM-007`: conditional on a sole positive
mass scale Lambda and an independently existing tension sigma of mass dimension
two, dimensional homogeneity gives `sigma=k*Lambda^2` for an unconstrained
dimensionless `k`. Candidate B promotes no claim. Neither delta may assert
confinement or calculate a tension.

## Implementation and Oracle Plan
The source will first be reproduced and decomposed check by check. Exact SymPy
algebra is appropriate for the RGE duplicate map, dimensions, derivatives, and
limits. A verifier will mutate the beta sign, fixed-coupling versus total RG
derivative, tension dimension, extra independent scale, and free prefactor.
Independent review will reconstruct the dimension-matrix kernel without using
campaign helpers. Existing `renormalization.py` remains canonical unless CF4
contains a genuinely new API; duplicate code will not be added.

## Attempts and Continuation
Attempt `0001` will reproduce CF4 and audit every headline implication. A
technical failure will be repaired append-only. If Candidate C lacks a
nonperturbative bridge, it will be rejected while A and B are compared on
novelty and consumer value.

## Debt Ledger

This ledger tracks duplicate, implication, premise, and novelty debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| CF4 may duplicate `C-RGE-001` | Produce an exact subclaim-to-registry map | discharged |
| A one-loop pole may be narrated as confinement | Require an independent nonperturbative implication or reject it | discharged |
| `sigma=k*Lambda^2` may hide existence or a fitted coefficient | Keep existence, sole-scale closure, dimensions, and free `k` explicit | discharged |
| A trivial dimensional consequence may be over-promoted | Audit novelty and actual downstream consumers | discharged |

## Review and Promotion Plan
One review instance will be created for every proposed accepted claim. A
terminal no-new-claim outcome instead requires a durable source adjudication,
attempt record, independent duplicate/implication review, migration update,
parent-effort update, and one full unchanged gate. A mixed source maps to
`qualified`; a wholly redundant valid source maps to `duplicate_evidence`;
unsupported physical content must remain explicitly excluded.

## Results and Promotion
The source reproduces all six checks. Attempt `0001` exposed and preserved a
brittle symbolic inequality; attempt `0002` replaces it with an exact log-ratio
sign oracle and passes 26 checks. The independent route passes six checks and
22 focused tests pass. `C-DIM-007` promotes the unique one-scale exponent with a
free prefactor and extra-scale guard. CF4 is qualified: its RGE content is
duplicate, while its physical confinement implication fails a same-flow
zero-tension countermodel.

## Done Gate
P025 is complete. CF4 has a terminal qualified disposition, every exact
subclaim is mapped, the confinement implication is rejected by a countermodel,
the verifier is mutation-sensitive, consumers are recorded, and the debt
ledger is empty.
