---
description: Audit FG3's complex mass-matrix and flavor-mixing construction
author: vantasner
created: '2026-08-01T17:08:59Z'
updated: '2026-08-01T17:17:53Z'
tags:
- substrate-framework
- campaign-proposal
- singular-value-decomposition
- flavor-mixing
- migration-FG3
category: proposals
confidence: exploratory
status: archived
---
# P034 FG3 Flavor-Mixing Matrix Audit

## Question and Positive Deliverable

P034 must derive the convention-complete finite-dimensional relationship
between a complex mass matrix, its singular values, and its left and right
bases, then determine whether accepted framework structure identifies the
relative left-basis matrix with physical CKM mixing. The positive deliverable
is a reusable matrix theorem with its exact freedoms and physical boundary;
merely exposing an unsupported CKM narrative would not complete the campaign.

## Base Release and Provenance

The accepted base is `v0.29.0` at framework commit `b7d8fbc`, whose forty-two
claims contain no accepted fermion-family, Yukawa-texture, charged-current, or
CKM construction. The hash-pinned candidate is pending unit FG3 at
`merged-framework/bridges/phase-11/bridge_FG3_flavor_mixing_matrix.py`,
SHA-256 `5030cf63716914a0effe2d89de2510c14a1c081784ffa2abfd73d24d982ea7cb`.
A bundled-memory search returned no framework result matching FG3, SVD,
biunitary diagonalization, or CKM; any reused mathematical fact will therefore
be rederived from its finite-dimensional source theorem rather than memory.

## Invariants, Conventions, and Allowed Imports

The campaign preserves the distinction between a declared matrix and a
derived physical interaction. It may import the finite-dimensional complex
spectral theorem and singular-value decomposition, exact matrix algebra, and
numerical calculations only as regression evidence. Matrix shapes,
conjugate-transpose placement, vector orientation, ordering, phase freedom,
zero singular values, and degenerate subspaces must be explicit. A relative
unitary basis is not a CKM prediction without accepted fermion representations,
Yukawa couplings, and a charged-current interaction using that basis.

## Candidate Preregistration

The alternatives are frozen from migration metadata before the full FG3
executable body or any comparison values are inspected.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | General convention-safe complex SVD, relative left-basis unitarity, degeneracy freedoms, and real symmetric two-family limit | Finite complex matrix and declared bases | Matrix entries only | Native mathematical extension with explicit physical exclusion | Exact reconstruction, spectra, basis transformations, degeneracy and zero-mode probes |
| B | Unitary-product identity and real symmetric two-by-two rotation only | Two unitary matrices or one real symmetric matrix | Matrix entries and rotation angle | Selected if FG3's reconstruction convention or claimed generality fails | Wrong-orientation counterexample and exact diagonalization residual |
| C | Substrate-derived physical CKM mechanism and Cabibbo prediction | Unaccepted fermion, Yukawa, current, and texture maps | Arbitrary textures plus physical labels | Dependency conflict | Accepted-claim closure and texture-variation tests |

## Selection Criteria and Blinding

Selection is ordered by reconstruction correctness, exact spectral
relationships, zero/repeated-singular-value treatment, basis and phase
covariance, unitary-product closure, the real symmetric limit, assumption
economy, and accepted-dependency closure. Texture values, named mixing angles,
or empirical comparators remain blinded until these algebraic conventions and
the physical-identification boundary are frozen; numerical closeness cannot
select a candidate.

## Proposed Claim Delta

Provisional `C-MIX-001` would state a finite-dimensional complex SVD in one
explicit convention, identify the nonnegative singular spectrum through both
Gram matrices, characterize basis freedom in zero and repeated subspaces, and
prove that the relative matrix between two left unitary bases is unitary. It
may include the conditional real symmetric two-by-two rotation formula. It
will explicitly exclude a derived Yukawa texture, CKM identification,
Cabibbo-angle prediction, fermion generations, CP phases, masses, or substrate
realization unless separate accepted dependencies close those statements.

## Implementation and Oracle Plan

Reusable pure APIs will live under `src/substrate_framework/` and will expose
one documented SVD convention, reconstruction, Gram residuals, relative
left-basis construction, and the real symmetric rotation. SymPy will check the
tractable symbolic identities and counterexamples; NumPy will exercise general
complex rectangular, rank-deficient, and repeated-spectrum cases as regression
coverage. Mutations will swap a conjugate transpose, use the wrong Gram
matrix, perturb an eigenvector pairing, and vary arbitrary textures. An
independent polar/spectral or direct matrix-unitarity route will rederive the
load-bearing statements without importing the campaign verifier.

## Attempts and Continuation

Attempt `0001` will reproduce FG3, inventory each executable subclaim, and
test its matrix orientation, singular-vector reconstruction, unitarity,
two-family angle convention, parameter count, and physical dependencies. A
bad reconstruction selects Candidate B only if the general theorem cannot be
repaired cleanly in an importable API. Missing physics dependencies reject
Candidate C and do not weaken the positive algebraic deliverable.

## Debt Ledger

This ledger tracks convention closure, exceptional spectra, independence, and
physical dependency boundaries.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| FG3's left/right convention may not reconstruct its declared matrix | Derive and test one shape-safe convention and audit the source convention exactly | discharged: the column-basis theorem reconstructs, and a rational row-transform counterexample exposes FG3's mismatch |
| Positive or repeated spectra may hide zero-mode and basis freedoms | Test full-rank, rank-deficient, repeated, square, and rectangular cases | discharged: exact and API checks cover every listed case and state nonuniqueness |
| Unitarity may be a copied identity rather than a sensitive claim | Mutate a load-bearing basis and require the residual verdict to fail | discharged: value, pairing, scale, and orientation mutations fail their relevant predicates |
| A real two-family formula may be overgeneralized to complex matrices | State and verify its symmetry/reality assumptions and give a counterexample outside them | discharged: the exact real result passes and the API rejects a complex Hermitian input |
| Matrix algebra may be relabeled a physical CKM prediction | Inventory every fermion, current, Yukawa, and texture dependency against `v0.29.0` | discharged: all named physics units are unaccepted and the promoted claim excludes their interpretations |

## Review and Promotion Plan

The provisional claim receives an independent decomposition and basis-freedom
review. Promotion requires pure APIs with tests, immutable attempt evidence,
claim-level adjudication, a terminal FG3 disposition, release/docs/memory
synchronization, targeted consumer replay, and one unchanged full repository
gate. A mixed algebraic/physical source will be `qualified` only with accepted
claim mappings and durable evidence naming every excluded subclaim.

## Done Gate

P034 closes only when the exact convention, reconstruction, spectrum,
exceptional cases, unitary misalignment, real-symmetric limit, mutation
sensitivity, dependency boundary, source disposition, and campaign debt all
satisfy the framework success contract.

## Adjudication Result

Candidate A is accepted as `C-MIX-001`. Thirty-five main and nine independent
checks close the exact decomposition, exceptional subspaces, relative-basis
unitarity, row-transform conversion, and real-symmetric limit. FG3 is qualified
because its own returned row convention conflicts with its mixing formula,
while arbitrary inserted textures and unaccepted M1/SM2/SM3/W3/W7 imports
cannot establish CKM, Cabibbo, current, GIM, or anomaly physics. All campaign
debt is discharged.
