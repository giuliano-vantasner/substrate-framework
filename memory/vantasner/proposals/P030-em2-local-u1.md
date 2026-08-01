---
description: Derive EM2's exact local-U1 gauge algebra
author: vantasner
created: '2026-08-01T16:20:00Z'
updated: '2026-08-01T16:27:00Z'
tags:
- substrate-framework
- campaign-proposal
- local-u1
- gauge-covariance
- migration-EM2
category: proposals
confidence: exploratory
status: archived
---
# P030 EM2 Local U1 Algebra

## Question and Positive Deliverable

P030 must derive a convention-closed local-U1 covariant derivative and its
exact consequences while separating gauge redundancy from gauge dynamics. The
positive deliverable is an importable local-gauge algebra theorem, with a
conditional winding-flux clause only if its topology and finite-energy premises
close independently.

## Base Release and Provenance

The accepted base is `v0.25.0` at framework commit `3b55681`. `C-U1-001`
supplies an independently declared complex scalar and fixes the raised current
`j^mu=i(Psi_conj*d^mu Psi-Psi*d^mu Psi_conj)` in signature `(+,-)`.
`C-VTX-001` contains a model-specific radial gauge convention but does not
establish general local-U1 algebra. The hash-pinned candidate is EM2 at
`merged-framework/bridges/phase-3/bridge_EM2_gauge_u1_minimal_coupling.py`,
SHA-256 `9787ae25521e19d926de0f9addafd16353bebc149cea83f3d9dd4c491fef91d6`.
Memory search found no accepted local-gauge claim.

## Invariants, Conventions, and Allowed Imports

The campaign imports `C-U1-001`, exact complex differential algebra, and only
abstract integer-label context from `C-TOP-001`. It freezes
`D_mu=partial_mu-i*e*A_mu` with
`Psi'=exp(i*e*chi)Psi`, `A_mu'=A_mu+partial_mu chi`. The accepted current sign
must determine the cross term rather than source prose. No Maxwell kinetic
term, field equation, propagating photon, electric-charge identification, or
substrate emergence may be inferred from local covariance.

## Candidate Preregistration

The candidates are frozen from migration metadata before the full EM2 body is
read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact local covariance, matter invariance, curvature algebra, and conditional winding flux | C-U1-001 plus declared connection and topology | Coupling and winding | Native if all signs and premises close | Arbitrary-function expansion, commutator, and winding mutations |
| B | Covariance theorem only | Declared connection | Coupling | Preferred if coupling or flux prose mixes conventions | Coefficient-by-coefficient accepted-current audit |
| C | Physical electromagnetism and photon dynamics | Unprovided Maxwell action and sector map | Physical charge and gauge field | Conflicts with dependency closure | Action inventory and zero-curvature countermodel |

## Selection Criteria and Blinding

Selection is ordered by arbitrary-function covariance, accepted-current sign
consistency, curvature and wrong-sign sensitivity, explicit topology and
finite-energy premises, assumption economy, and reusable downstream reach. No
phenomenological charge, flux, or electromagnetic value may select a candidate.

## Proposed Claim Delta

Provisional `C-GAU-001` records exact local-U1 covariance and the invariant
complex-scalar kinetic construction, with curvature and commutator consequences
in the same convention. A flux clause is included only if its boundary and
winding premises are explicit. The claim cannot include a Maxwell equation,
physical electric charge, photon, or emergent-electromagnetism assertion.

## Implementation and Oracle Plan

Create a pure gauge-algebra module rather than extending profile-specific
charge helpers. SymPy is the exact oracle for arbitrary field, phase, gauge,
and gauge-function jets, kinetic expansion, curvature invariance, and
covariant-derivative commutators. Mutations reverse the connection shift,
derivative sign, coupling coefficient, current sign, and winding integer.
Independent review will derive the transformation and cross term from expanded
products without importing package helpers.

## Attempts and Continuation

Attempt `0001` reproduced all eleven EM2 checks and passed twenty-two stronger
exact checks. Candidate A was selected with the accepted-current coupling sign
corrected and integer winding separated from the source's inserted half flux.
An independent seven-check route confirms the result.

## Debt Ledger

This ledger tracks sign, dynamics, topology, and physical-interpretation debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The source coupling sign may conflict with C-U1-001 | Expand both conventions from first principles | discharged |
| Covariance may be mistaken for a dynamical gauge sector | Inventory the action and exclude absent kinetic equations | discharged |
| Flux quantization may hide finite-energy and topology premises | Derive the boundary condition with explicit winding | discharged |
| A pure-gauge connection may be renamed a photon | Add a nonzero-curvature countermodel boundary or exclude the map | discharged |

## Review and Promotion Plan

The provisional claim receives an independent sign and commutator review.
Promotion requires pure APIs/tests, immutable attempt and source evidence,
claim-level axes, terminal EM2 disposition, registry/release/generated and
parent synchronization, downstream EM6/EM3 consumer mapping, focused replay,
and one full unchanged promotion gate.

## Done Gate

P030 closes with exact local covariance, corrected current sign, curvature,
integer topology, explicit dynamics boundary, sensitive mutations, replayed
consumers, qualified source disposition, and an empty debt ledger.
