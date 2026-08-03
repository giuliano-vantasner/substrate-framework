---
description: Derive the exact normalized symmetric-spin ladder and delimit its physical rate interpretation
author: vantasner
created: '2026-08-07T21:45:00Z'
updated: '2026-08-07T21:45:00Z'
tags:
- substrate-framework
- campaign-proposal
- symmetric-spin
- migration-PN3
category: proposals
confidence: exploratory
status: active
---
# P111 PN3 Symmetric Spin Ladder Audit

## Question and Positive Deliverable

P111 must deliver an exact importable classification of collective raising and
lowering on the normalized permutation-symmetric subspace of N declared
two-state factors. The object includes every excitation rung, ground and top
edges, representation and operator conventions, general N scaling, unequal
complex couplings, and a precise boundary between an algebraic squared matrix
element and a physical transition rate.

The abstract theorem cannot by itself identify nuclei, phonons, coherent
preparation, a material, an interaction, a continuum of final states, or a
rate. Rejecting those readings does not complete P111 unless the positive
normalized ladder object is implemented and verifier-backed.

## Base Release and Provenance

The accepted base is v0.92.0 at parent checkpoint
`640f02ab72fdd7a6333e1ddabdbe956e178ebe97`; the latest scientific transaction
is P110 at `263014ecf56830051f5db4c49965c44bcb38d20a`. The pinned source remains
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. The predecessor worktree's
unrelated Phase 47/48 work and the deliberate NumPy compatibility overlay are
excluded from authority.

PN3 is
`/home/dan/substrate/merged-framework/bridges/phase-30/bridge_PN3_dicke_collective_scaling.py`,
7,687 bytes, SHA-256
`da472079f418368926e27d22567cdf3ad8f32c836146ed8107ae2874f377b58b`,
and git blob `780233dbf80acaf9a23ec6a29c8923915db0974d`. It matches the pinned commit. The
queue marks PN3 pending with no candidate dependency, records nine static
checks, eight literal and one dynamic, and exposes the standard maximal-spin
ladder, its ground-rung square-root scaling, an N=1 limit, and a linear-rate
interpretation. Its predicate implementations and source body remain unopened
until this contract is committed.

Authority recall read v0.92.0 and all 127 accepted entries, then checked the
closest surfaces at their registry records. C-SPN-001 is a distinct pure
spin-one orbit theorem. C-TH-001 permits only a declared two-state partition
function and explicitly supplies no causal mechanism. C-REP-002 is already a
reserved rejected duplicate identifier, so P111 provisionally uses C-SPN-002.
Memory search found no accepted collective spin-half ladder result.

Ten direct pending queue consumers name PN3: PN4, CM2, CM4, GB1, GB3, GB4,
GB6, WN1, WN3, and MD3. Seventeen additional pending units are transitively
reachable through their declared dependency edges. These edges are provenance
and replay obligations, not accepted consumers or proof of a physical role.

## Invariants, Conventions, and Allowed Imports

Let N be a positive integer and let the computational tensor-product basis use
orthonormal local states zero and one. The normalized k-excitation Dicke vector
is the equal superposition over all subsets of size k. With dimensionless local
raising matrices and `J_plus=hbar*sum_i sigma_plus_i`, exact counting predicts
`J_plus|D_k>=hbar*sqrt((N-k)*(k+1))*|D_(k+1)>`; lowering is its adjoint. The
equivalent labels are `j=N/2` and `m=k-N/2`.

The ground-edge coefficient scales as square root N, while a central rung is
order N. These statements concern normalized state-vector coefficients. A
different operator scale, unnormalized state, nonsymmetric sector, or unequal
complex site couplings changes the result. Equal coupling to the symmetric
one-excitation state is a premise, not a consequence of the number of factors.

Allowed imports are finite exact linear algebra, tensor products, binomial
identities, the standard su(2) algebra independently rederived in the displayed
normalization, and SymPy. C-SPN-001 and C-TH-001 are used only for
nonduplication and interpretation ceilings. PN3 becomes noncanonical evidence
only after the freeze commit.

No sampled integration is planned. If immutable PN3 aborts only because
`np.trapz` is absent, an alias-only replay will be recorded before scientific
adjudication; mutable current-environment scripts use `np.trapezoid`, and any
future canonical sampled integral uses `trapezoid_integral`. Such a version
event is not candidate rejection.

## Candidate Preregistration

The candidates are frozen before PN3 execution or predicate inspection.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal PN3 reproduction | Source conventions only | Source N and hbar | Regression evidence | Predicate-level audit |
| B | Normalized symmetric bitstrings | Orthonormal tensor basis | N and k | Exact combinatorial coefficient | Exhaustive finite construction |
| C | Irreducible su(2) ladder | Maximal-spin representation | j and m | Same coefficient independently | Commutator and Casimir route |
| D | Unequal complex couplings | Declared site coefficients | g_i | Bright, dark, and symmetric amplitudes separate | Phase and magnitude mutations |
| E | Conditional rate completion | Declared interaction and spectral data | coupling and density | Squared coefficient is one factor only | Zero-density and off-resonance countermodels |
| F | Consumer closure | Hash-pinned queue graph | none | No inherited physical premise | Direct and transitive replay |
| G | Nonduplication and package extraction | Distinct theorem and consumer | none | C-SPN-002 and pure API survive | Registry and impact audit |

## Selection Criteria and Blinding

Selection prioritizes explicit Hilbert space, basis, normalization, symmetry
sector, and operator premises; agreement between combinatorial and
representation routes; correct all-rung and edge scaling; sensitivity to
normalization and unequal couplings; strict separation of algebra and physical
rate assumptions; assumption economy; API reuse; and consumer closure.

No source-conclusion blinding remains because the generated queue exposes the
formula, ground-rung result, N=1 limit, and advertised rate scaling. P111
freezes stronger all-rung, coupling, countermodel, mutation, and consumer gates
before opening the nine predicate implementations. Exposed expressions cannot
select the theorem or become a physical pass threshold.

## Proposed Claim Delta

P111 provisionally proposes C-SPN-002 for the exact normalized symmetric-spin
ladder, its ground and general-rung scaling, and unequal-coupling ceiling. It
would depend only on approved finite-dimensional mathematical imports and
would explicitly exclude every nuclear, phonon, material, state-preparation,
interaction, resonance, density-of-states, linewidth, decoherence, Golden-rule,
supertransfer, and observed-rate interpretation.

No accepted claim is challenged or superseded. The identifier is promoted only
if nonduplication, importable API, independent construction, mutation
sensitivity, and consumer usefulness all survive.

## Implementation and Oracle Plan

A pure `src/substrate_framework/symmetric_spin.py` module may expose validated
integer-domain coefficient, representation-coordinate, unequal-coupling, and
bright-state APIs. Imports must not execute enumeration or print. Focused tests
will cover all rungs, N=1, annihilated edges, exact radicals, adjoint symmetry,
operator-scale covariance, central versus edge asymptotics, invalid domains,
and complex-coupling cancellation.

The primary SymPy and combinatorial oracle will derive rather than hard-code
the coefficient and exhaust small tensor products. Mutations remove Dicke
normalization, replace the sum by an average, shift a rung factor, change local
operator normalization, and inject unequal phases. An independent route will
use the irreducible matrices, commutator, Casimir, and a separately written
bitmask countercheck without calling the canonical API.

Rate countermodels set the interaction to zero, the final spectral density to
zero, or the energy mismatch off resonance while leaving the collective
coefficient unchanged. The consumer audit will pin all ten direct and
seventeen indirect queue units and ensure no accepted consumer silently gains
the missing physical premises.

## Attempts and Continuation

Each failed source reproduction, convention, representation, combinatorial,
normalization, coupling, rate, consumer, or verifier route is recorded append-
only with its mechanism and next materially different attempt. A failed
physical interpretation triggers the next exact candidate and does not stop
the parent migration.

## Debt Ledger

P111 tracks source provenance and all nine predicates; local basis and tensor
ordering; state and operator normalization; N and k domains; maximal-spin and
permutation-symmetry premises; raising, lowering, commutator, Casimir, edge and
asymptotic statements; unequal coupling magnitudes and phases; bright and dark
states; physical state and interaction maps; energy, spectral, linewidth,
decoherence, Golden-rule, and material assumptions; all direct and transitive
consumers; nonduplication; claim and source disposition; generated state; and
parent continuation. Every item must be derived, declared, rejected, or
excluded before closure.

## Review and Promotion Plan

The claim receives an independent representation-and-counting review, exact
mutation replay, source and predicate adjudication, dependency and complete
consumer audits, package tests, GitNexus impact analysis, and downstream
repository replay. If accepted, C-SPN-002 is promoted individually with an
importable module, release, generated docs, and generated memory. PN3 receives
a terminal disposition that retains exact algebra and names every rejected
physical reading.

The integrated workflow runs once at the promotion boundary. A final attempt
is created in progress before that gate, finalized after it, and followed only
by record-sensitive checks.

## Done Gate

P111 closes only when the normalized all-rung ladder object exists, both
independent derivations and mutations validate it, every PN3 predicate and
consumer has an explicit verdict, physical-rate premises are separated, the
claim and source disposition are reviewed, all generated consumers agree, and
the campaign debt ledger is empty. A familiar formula or passing source tally
alone is insufficient.

## Cross-References

See PN3, C-SPN-001, C-TH-001, P067, P005, and the framework-migration effort.
