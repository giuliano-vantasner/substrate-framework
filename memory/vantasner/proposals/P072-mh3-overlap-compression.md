---
description: Derive overlap-compression invariants and audit MH3
author: vantasner
created: '2026-08-03T07:40:00Z'
updated: '2026-08-03T08:20:00Z'
tags:
- substrate-framework
- campaign-proposal
- overlap-compression
- migration-MH3
category: proposals
confidence: exploratory
status: archived
---
# P072 MH3 Overlap Compression Audit

## Question and Positive Deliverable

P072 must deliver an importable basis-covariant multiplication-overlap
compression, exact parity blocks, the simultaneous-diagonalization criterion,
and a complete basis/physical-identifiability ledger. A nonzero entry in one
basis, automatic unitarity, or unsupported CKM language does not complete the
campaign.

## Base Release and Provenance

The accepted base is `v0.65.0` at scientific commit `4ca91af`; parent-effort
synchronization is commit `05f928c`. The predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. MH3 is
`/home/dan/substrate/merged-framework/bridges/phase-20/bridge_MH3_overlap_feeds_mixing.py`,
24259 bytes, with inventory and reproduced SHA-256
`f33ab10dadee8ae4f747328f1fc593733942d18ccdb280ca6f21c3961e03c425`.
The queue marks MH3 pending and names EM6, FG2, FG3, FG4, MH1, and MH2. Their
accepted mathematical content is bounded by C-QBL-001, C-QBL-003, C-MIX-001,
C-MIX-002, C-OVL-001, and C-OVL-002; none supplies physical flavor fields or a
charged current. The clean tree, history, seven-check preflight, registry,
release, accepted matrix/rephasing/overlap APIs, source synopsis, templates,
package search, and durable memory were inspected before this contract. Memory
contains no accepted weighted-compression or simultaneous-diagonalization
claim. At the contract freeze, MH3's executable body and detailed output
remained unopened; attempt 0001 subsequently reproduced and audited them.

## Invariants, Conventions, and Allowed Imports

C-OVL-001 fixes the actual centered even/odd cross overlap to zero. C-MIX-001
and C-MIX-002 supply matrix algebra with explicit basis, phase, ordering,
degeneracy, and physical ceilings. P072 may use finite Hermitian compression,
Rayleigh-Ritz bounds, parity, unitary similarity, spectral projectors, and the
commuting-Hermitian theorem. One common Hilbert space, measure, conjugation,
ordered orthonormal basis, multiplier, sector-identification map, and all
centers, widths, and amplitudes remain visible. No fermion, Yukawa, generation,
charged-current, or physical sector premise is available.

## Candidate Preregistration

The candidate set is frozen before MH3's executable is opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal MH3 | Its modes, profiles, sectors, bases, and diagonalizer conventions are complete | source inputs | Narrow matrix algebra may survive while physical mixing does not | Hash-pinned execution and data-flow audit |
| B | General multiplication compression | Finite orthonormal family and bounded real multiplier on one Hilbert space | modes and profile | Compression is Hermitian, bounded, and unitary-similarity covariant | Direct sesquilinear derivation and basis mutations |
| C | Parity blocks | Parity-definite modes and an even centered multiplier | parities and profile | Opposite-parity cross entries vanish for every even width | Reflection proof and odd/asymmetric counterexample |
| D | Commutator criterion | Two Hermitian matrices on one identified finite space | matrix entries | A common eigenbasis exists iff the commutator vanishes | Exact theorem, noncommuting example, equal-matrix limit |
| E | Basis/degeneracy ledger | Ordered spectral projectors and declared sector map | phases, permutations, degenerate blocks | Relative entries are noncanonical unless permitted freedoms are quotiented | Reordering, phase, degenerate-block, and missing-map probes |
| F | Asymmetric profile | A separately declared parity-breaking multiplier | shift or odd amplitude | A nonzero cross term is possible but requires a new premise | Exact first odd moment or displaced-profile calculation |

## Selection Criteria and Blinding

Selection is ordered by accepted closure; Hilbert-space and basis completeness;
Hermiticity, bounds, parity and commuting limits; invariant rather than entrywise
meaning; mutation sensitivity; and assumption economy. The synopsis's claimed
entry, widths, relative matrix, and Cabibbo labels cannot select a profile,
basis identification, or physical interpretation.

## Proposed Claim Delta

Provisional C-OVL-003 may state finite multiplication-compression
Hermiticity/bounds/covariance, exact parity blocks, simultaneous
diagonalization by the commutator criterion, and basis/degeneracy ceilings. It
may include a conditional asymmetric-profile cross term. It may not establish
a fermion mass matrix, Yukawa interaction, generation assignment, physical
up/down sectors, CKM matrix, Cabibbo angle, charged current, CP observable,
absolute mass, or substrate realization.

## Implementation and Oracle Plan

A pure module may expose exact finite overlap-matrix construction from symbolic
integrals, Hermiticity and bound ledgers, parity selection, basis covariance,
commutator/simultaneous-diagonalization diagnostics, spectral-projector
freedoms, and a parity-breaking counterexample. SymPy fits all promoted exact
obligations. NumPy eigendecomposition may regress generic matrices but cannot
prove the theorem or select a basis in degenerate blocks. An independent route
will derive the sesquilinear and commutator results without importing the new
API. Mutations will omit conjugation, reverse relative-basis orientation,
claim an even-profile parity violation, reorder or rephase one eigenbasis,
rotate a degenerate block, compare unidentified sector spaces, and use
unitarity as a nonidentity oracle.

## Attempts and Continuation

Attempt 0001 will preserve MH3's native process and trace every check. If its
cross term contradicts parity, its width change also changes the mode basis,
or its relative matrix is selected by arbitrary eigenvector conventions, those
failures are recorded and Candidates B-F continue. Rejection of physical CKM
semantics cannot close P072 by itself.

## Debt Ledger

The campaign tracks Hilbert-space, parity, basis, degeneracy, sector,
dependency, verification, interpretation, and synchronization debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| MH3's executable and output are unaudited | Hash-check, execute, preserve output, and trace all checks | discharged by attempt 0001 and the source evidence |
| The claimed cross term may violate exact parity | Reconstruct modes/profile and prove every entry with conjugation | discharged; only the separately odd profile component survives |
| Different widths may be confused with invariant misalignment | Freeze one common basis/space and apply the commutator criterion | discharged; every normalized entry is width independent |
| Eigenvector phase, ordering, and degeneracy may set the relative matrix | Expose spectral projectors and all permitted basis freedoms | discharged by exact phase, permutation, and degenerate-block probes |
| Physical sectors, Yukawa fields, or charged currents may be imported | Audit dependency closure and exclude every unaccepted premise | discharged; every physical flavor premise remains outside the claim |
| Verifier sensitivity, review, and synchronization are incomplete | Complete mutations, independent derivation, impact replay, claim review, disposition, release, docs, queue, and memory | discharged at the v0.66.0 promotion boundary |

## Review and Promotion Plan

Any proposed claim receives independent review of the compression convention,
Hermiticity, range bounds, parity blocks, commutator criterion, basis
covariance, phase/order/degeneracy freedoms, asymmetric counterexample, and
physical ceiling. MH3 receives a terminal disposition through the
authoritative queue. Accepted logic moves into the package with focused tests
and one full promotion-boundary workflow gate.

## Done Gate

P072 closes only when the positive importable overlap-compression ledger,
sensitive exact oracles, independent derivation, source adjudication,
claim-level decision, downstream replay, canonical synchronization, and empty
campaign debt all pass. A unitary or nonidentity matrix alone is not
completion.

## Cross-References

See C-QBL-003, C-MIX-001, C-MIX-002, C-OVL-001, C-OVL-002, MH3's generated
source record, release `v0.65.0`, and the parent migration effort.

## Outcome

Candidates B through E establish the exact compression, parity, covariance,
commutator, and basis-freedom ledger. Candidate F establishes the conditional
actual-mode matrix
`[[9*pi*A/32,sqrt(2)*A*b/5],[sqrt(2)*A*b/5,3*pi*A/16]]`; its new odd-profile
parameter is explicit and the common width cancels. Candidate A survives only
as source-proxy regression and an equal-input guard. Forty-two primary and
twenty-three independent checks pass, including conjugation, parity, width,
commutator, phase, ordering, and degeneracy mutations.

Attempt 0003 corrects the degenerate-block parameter count to `m^2-m`, the
dimension of `U(m)/U(1)^m`, after the final diff audit found that the initial
implementation's `m^2-1` formula did not match its documented quotient.

MH3 is qualified through C-MIX-001, C-MIX-002, C-OVL-001, and C-OVL-003. Its
width-driven texture, shared-parameter hierarchy, and physical mixing claims
are rejected. Release `v0.66.0`, the registry, generated docs and accepted
memory, and the migration queue are synchronized at the promotion boundary.
