---
description: Adjudicate MR1's shared-shape mass-unit identity against the accepted conditional theorem
author: vantasner
created: '2026-08-01T13:40:42Z'
updated: '2026-08-01T13:45:25Z'
tags:
- substrate-framework
- campaign-proposal
- mass-unit-identity
- migration-MR1
category: proposals
confidence: exploratory
status: archived
---
# P017 Mass Unit Identity

## Question and Positive Deliverable
P017 must produce a hash-pinned, exact adjudication of MR1's claim that two
mass expressions share a dimensionless shape factor and differ only in their
declared energy units. The positive object is an executable factorization and
logical-type audit that determines whether MR1 adds a new accepted theorem,
duplicates `C-SK-001`, or overreaches into physical calibration and
double-counting conclusions. A merely reproduced terminal tally does not
complete the campaign.

## Base Release and Provenance
The accepted base is `v0.15.0` at commit `c84f23d`. The accepted source is
`C-SK-001` and its canonical implementation in `skyrme_relations.py`. The
hash-pinned candidate is MR1 at
`merged-framework/bridges/phase-44/bridge_MR1_mass_unit_identity.py`, SHA-256
`d065f592390fe9322d27fbd2cf55262d8ccb8d45e6510cf8628058f716b6c875`.
Its listed predecessor units remain pending and are evidence, not imports.
Durable-memory search returned no authoritative MR1 result; every reused fact
will be checked against the registry, package, or pinned source.

## Invariants, Conventions, and Allowed Imports
Both mass formulas remain conditional premises. Positive symbols permit exact
cancellation, but cancellation cannot establish either premise, identify an
observed particle, or decide sector double counting. A common nonzero
dimensionless shape factor may be divided out. Declared energy units must be
distinguished from physical mass predictions. No pending source dependency,
numerical comparator, fitted coefficient, or literature normalization is an
allowed scientific import.

## Candidate Preregistration
The candidates are frozen before MR1's full verifier body is read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Promote a general shared-shape unit-equivalence theorem | Common nonzero shape factor and two declared units | none beyond the units | Useful only if materially broader than C-SK-001 and consumed independently | Factor arbitrary `K*U1` and `K*U2`; compare exact scope and consumers |
| B | Classify MR1 as duplicate evidence for `C-SK-001` | The two accepted conditional mass premises | none | Most economical if MR1's unit equality is exactly the existing iff in refactored notation | Normalize both formula pairs and prove bidirectional equivalence |
| C | Promote a physical calibration or double-counting verdict | Conditional formulas treated as established sector physics | Hidden model identification | Conflicts with accepted premise status | Exhibit two models satisfying the algebra with different physical interpretations |

## Selection Criteria and Blinding
Selection is ordered by exact logical equivalence, dependency closure,
assumption economy, reusable consumer need, preservation of premise status, and
mutation sensitivity. A new claim is justified only by distinct scope with a
real consumer; restating `C-SK-001` through a common factor selects duplicate
evidence. MR1's numerical values are not selection inputs and will be inspected
only after the structural candidates and tests are frozen.

## Proposed Claim Delta
The provisional delta is `C-SK-002`, a generic conditional theorem that
`K*U1=K*U2` iff `U1=U2` for nonzero `K`, composed with MR1's declared units.
It depends on no physical claim. It will be withdrawn if it has no distinct
framework consumer beyond rephrasing `C-SK-001`; in that case MR1 receives a
terminal `duplicate_evidence` disposition and the accepted release is
unchanged. No existing claim is challenged or superseded.

## Implementation and Oracle Plan
SymPy exact algebra is the appropriate oracle. The verifier will derive both
mass factorizations, cancel only a declared nonzero common factor, prove both
directions of unit equality and `C-SK-001` equivalence, and mutate a coefficient,
factor power, and unit assignment so the relevant verdict fails. It will also
show that equal units do not encode a sector ontology. An independent route
will compare coefficient ratios without importing a new helper. Existing
package APIs will be reused unless the generic theorem survives the consumer
test; campaign verifiers run with `PYTHONPATH=src`. No numerical rerun can add
independent evidence to this exact identity.

## Attempts and Continuation
Attempt `0001` failed after three exact checks because the reverse-implication
test substituted a composite unit expression rather than its primitive
parameter relation. This is a representation failure; it changes no candidate,
coefficient, premise, or tolerance. Attempt `0002` will substitute
`F_pi=16*pi*E_e*e` explicitly and continue the same audit. If the generic
theorem is exact but adds no distinct consumer, it will remain campaign evidence
rather than an accepted claim. Physical calibration requires separately
accepted premises and cannot be rescued by a close comparator.

## Debt Ledger
The campaign starts with four explicit debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| MR1 may merely rename `C-SK-001` | Exact normalized equivalence comparison | discharged |
| Pending predecessors may be used as hidden authority | Import inventory contains no pending scientific claim | discharged |
| Unit equality may be presented as physical calibration | Source audit separates algebra from interpretation | discharged |
| Generic cancellation may be promoted without a consumer | Consumer audit selects promotion or duplicate disposition | discharged |

## Review and Promotion Plan
Review will independently rederive the coefficient cancellation and compare
the proposed logical type claim by claim with `C-SK-001`. The source audit will
map each MR1 check to exact algebra, duplicate evidence, declared premise, or
unsupported physical narrative. If no claim survives, no release or generated
accepted-state record changes; MR1 still receives a durable terminal
`duplicate_evidence` disposition. Promotion, if warranted, requires package
extraction, tests, registry/release synchronization, generated consumers,
targeted verification, and one full replay at an unchanged boundary.

## Results and Adjudication
MR1's own seven checks reproduce at the pinned hash. After preserved
representation failure `0001`, attempt `0002` passes 17 exact checks and the
independent coefficient-ratio route passes five. The unit factorization and
ratio are exactly `C-SK-001`; coefficient, power, and zero-factor mutations
show the premise boundary. The sector-allocation symbol remains unconstrained,
and MR1's two numerical shape substitutions are regression instances of the
exact cancellation. `C-SK-002` is individually reviewed and rejected as a
separate claim because no distinct consumer exists. MR1 is terminally
`duplicate_evidence` for `C-SK-001`; `v0.15.0` remains current.

## Done Gate
P017 is complete. The exact shared-factor object exists, mutations prove the
oracle is load-bearing, every pending input remains quarantined, MR1 has a
terminal evidence-backed disposition, the withdrawn claim has individual
review, accepted-state duplication is avoided, and the debt ledger is empty.
