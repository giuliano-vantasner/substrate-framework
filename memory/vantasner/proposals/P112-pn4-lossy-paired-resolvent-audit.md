---
description: Derive the exact paired complex-resolvent identity and delimit PN4's lossy-channel interpretation
author: vantasner
created: '2026-08-07T23:15:00Z'
updated: '2026-08-07T23:15:00Z'
tags:
- substrate-framework
- campaign-proposal
- finite-resolvent
- migration-PN4
category: proposals
confidence: exploratory
status: active
---
# P112 PN4 Lossy Paired Resolvent Audit

## Question and Positive Deliverable

P112 must deliver an exact importable theorem for a finite endpoint-to-
intermediate resolvent with symmetric detuning pairs and a declared common
complex shift. It must fix block, projection, energy, sign, factor, coupling,
dimension, limit, extremum, asymmetry, and system-size conventions and then
adjudicate every PN4 predicate and physical interpretation.

A nonzero conditional effective element is not itself an open physical
channel, probability, or rate. Rejecting those readings does not complete the
campaign unless the positive finite-resolvent object and its independent
matrix reconstruction exist.

## Base Release and Provenance

The accepted base is v0.93.0 at parent checkpoint
`762ead2ec767bf237df65ff2329d0e9a5021af02`; the latest scientific transaction
is P111 at `df3df9facbe1a5a01230b2516b1c3c5ebfbe111c`. Source evidence remains
pinned to `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; unrelated
Phase 47/48 work and the compatibility overlay remain outside authority.

PN4 is
`/home/dan/substrate/merged-framework/bridges/phase-30/bridge_PN4_lossy_exchange_and_guard.py`,
18,887 bytes, SHA-256
`45ac6c039805964efa41ae8167f6257af18c5ef2b066d376efa19ec79dfd0c67`,
and git blob `f123c7cf92fb041b0d8b7ff44a6c039342e8299e`. It matches the pinned
commit. The queue marks PN4 pending, records twenty-two static check sites,
twenty literal and two dynamic, and names FS1, LB1, LB2, PN1, PN2, PN3, and
forward PN5 as candidate dependencies. The body and predicate implementations
remain unopened until this contract is committed.

Authority recall read v0.93.0 and the relevant accepted records. C-EFT-001 is
a real finite stationary-elimination theorem with no complex open-system
meaning. C-DYN-001 distinguishes abstract damping from decoherence and
material loss. C-SG-019 and C-SPN-002 supply only the algebraic ceilings of
PN1 and PN3; PN2 has no accepted claim. C-EFT-002 is already reserved by P063,
so P112 provisionally uses C-RES-001. Memory search found no accepted paired
complex-resolvent theorem.

Eight direct pending consumers name PN4: PN5, PN6, CM2, CM5, CM6, CM7, GB6,
and WN7. Sixteen additional pending units are reachable transitively after
excluding PN4 itself. PN4 depends forward on PN5 and PN5 depends back on PN4;
this candidate-level cycle is debt and grants neither unit authority.

## Invariants, Conventions, and Allowed Imports

For one declared pair at detunings plus and minus Delta, common shifted
intermediate energies `E_k=sigma*Delta-i*Gamma/2`, equal real coupling product
c, and spectral argument E=0, exact rational summation predicts
`-i*c*Gamma/(Delta^2+Gamma^2/4)`. The zero-loss cancellation needs both
detuning symmetry and matched complex coupling products.

The magnitude is linear at small positive loss, falls as one over loss at
large loss, and peaks at `Gamma=2*abs(Delta)` for one pair. A sum over unequal
detunings has its own stationary equation. Adding more pairs at fixed
per-pair coupling changes the model; fixed total coupling norm instead
rescales each contribution and can remove apparent growth.

Allowed imports are exact complex finite linear algebra, block inversion,
resolvents, Schur complements, rational calculus, C-EFT-001 and C-DYN-001 only
at their ceilings, and exact SymPy. NumPy may reproduce finite source matrices
but cannot upgrade an exact identity. PN4 and named literature become evidence
only after freeze; PN5 remains forbidden as a forward circular premise.

Canonical sampled integration would use `trapezoid_integral`, mutable scripts
use `np.trapezoid`, and immutable `np.trapz` failure receives an alias-only
replay. A compatibility event is not scientific candidate failure.

## Candidate Preregistration

The candidate set is frozen before PN4 execution or predicate inspection.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal reproduction | Source conventions | source inputs | Regression evidence | Predicate audit |
| B | Exact paired resolvent | Declared complex shift | Delta, Gamma, c | Conditional rational identity | Exact simplification and mutations |
| C | Full matrix inversion | Fixed endpoint/intermediate blocks | spectral E | Same projected element | Direct inverse and Schur complement |
| D | Loss-regime classification | Positive scales | detunings and couplings | Explicit limits and extrema | Series, limits, derivatives |
| E | Asymmetric pairs | General complex products | pair data | Exact cancellation locus | Counterfamilies and phase mutations |
| F | Size normalization | Declared coupling ensemble | pair count | Extensive and normalized laws differ | L versus 2L under fixed norms |
| G | Open-system ceiling | Separately declared dynamics | loss model | Algebra survives without rate | no-jump and zero-transition countermodels |
| H | Dependency and consumer closure | Hash-pinned graph | none | Cycle and physical gaps exposed | Full graph replay |
| I | Nonduplication and extraction | Distinct theorem and consumer | none | C-RES-001 survives | Registry and impact audit |

## Selection Criteria and Blinding

Selection prioritizes explicit spaces, blocks, projection, spectral argument,
signs, factors, dimensions, couplings, and complex-shift conventions; exact
agreement between rational and matrix routes; correct limits and extrema;
asymmetry and phase sensitivity; honest size normalization; separation from
open-system and rate claims; assumption economy; nonduplication; literature
honesty; and complete consumer closure.

The queue exposes the headline formula and physical conclusion, so no source-
conclusion blinding remains. P112 freezes stronger structural gates before
opening its twenty-two predicate sites. Exposed values cannot select a model
or pass threshold.

## Proposed Claim Delta

P112 provisionally proposes C-RES-001 for the exact conditional paired finite-
resolvent theorem, its limits and one-pair extremum, general cancellation
locus, and size-normalization ceiling. It has mathematical imports only and
explicitly excludes a Lindblad derivation, physical loss channel, probability,
rate, nuclear or phonon process, material, magnitude, and observation.

No accepted claim is challenged or superseded. Promotion requires a distinct
pure API, independent matrix route, sensitive mutations, and governed
consumer utility.

## Implementation and Oracle Plan

A pure `src/substrate_framework/paired_resolvent.py` module may expose a pair
contribution, general endpoint resolvent sum, cancellation ledger, loss-regime
data, and size-normalization transformations. It must execute no simulation
or logging on import. Focused tests cover exact signs, factor two, units,
zero/small/large loss, extrema, unequal pairs, phases, and normalization.

The primary oracle uses SymPy rational identities, series, limits,
derivatives, and exact block inversion. Mutations change the resolvent sign,
imaginary-shift sign, half width, pair sign, coupling conjugation, energy
argument, loss power, and pair-count normalization. The independent route
constructs the complete matrix afresh and uses a separately written direct
solve without importing the canonical API.

Countermodels retain the same effective element but assign zero observation
jump operator, no normalized final state, or incompatible energy measurement.
The dependency audit forbids PN5 and records the cycle. Literature is checked
only at primary provenance. Eight direct and sixteen indirect consumers are
hash pinned and individually retain their missing premises.

## Attempts and Continuation

Every source, sign, factor, matrix, limit, extremum, asymmetry, normalization,
open-system, literature, dependency, consumer, or verifier failure is
preserved append-only with a next materially different route. A rejected
physical channel does not stop the exact theorem or parent migration.

## Debt Ledger

P112 tracks the source and every static and dynamic predicate; endpoint and
intermediate spaces; block, projection, spectral, sign, half-width, coupling,
and dimensional conventions; zero and positive loss; small and large limits;
single and multiple extrema; unequal detunings and phases; size normalization;
non-Hermitian and complete open-system meanings; matrix element, probability,
and rate; PN1-PN3 ceilings; the PN4-PN5 cycle; literature; all consumers;
nonduplication; claim and source disposition; generated state; and parent
continuation. Every debt must be derived, declared, rejected, or excluded.

## Review and Promotion Plan

C-RES-001 receives independent matrix review, source and predicate audit,
mutation and countermodel replay, dependency-cycle and consumer review,
package tests, GitNexus impact analysis, and complete repository replay. If
accepted, it is promoted individually with an importable module, release,
generated docs, and accepted memory. PN4 receives a terminal disposition that
names every retained algebraic and rejected physical subclaim.

The integrated workflow runs once at the complete promotion boundary. Its
attempt is created in progress before the run, finalized after it, and
followed only by record-sensitive checks.

## Done Gate

P112 closes only when the exact finite-resolvent object, independent full-
matrix route, limits, extrema, asymmetry, normalization, every source
predicate, cycle, literature statement, dependency, consumer, claim record,
source disposition, generated consumer, and empty debt ledger agree. A
nonzero number or source tally alone is insufficient.

## Cross-References

See PN4, PN5, C-EFT-001, C-DYN-001, C-SG-019, C-SPN-002, and the framework-
migration effort.
