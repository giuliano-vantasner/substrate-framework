---
description: Derive and audit the exact representation content of W2's proposed chiral SU2 doublet
author: vantasner
created: '2026-08-09T21:40:00Z'
updated: '2026-08-09T21:40:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-W2
- representation
category: proposals
confidence: exploratory
status: active
---
# P147 W2 SU2 Doublet Audit

## Question and Positive Deliverable

P147 must deliver an exact importable classification of W2's two-state carrier,
generator, ladder, charge, and projector statements. The positive object must
separate abstract SU(2) representation identities from supplied kink/antikink
labels, compatible Abelian charge assignments, an independent chirality factor,
and the additional action and connection data required by a physical gauged
doublet. A source failure or no-go alone does not complete the campaign.

## Base Release and Provenance

The accepted base is v0.113.0 at framework checkpoint `f30d7c9`, with scientific
promotion `5b9fa7c`. The source baseline is `/home/dan/substrate` commit
`6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; later dirty Phase 47/48 and
engineering files remain excluded. W2 is pinned at
`merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py`, SHA-256
`0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16`.
Its dossier is pinned at `merged-framework/bridges/phase-6/dossiers/W2_dossier.md`,
SHA-256 `bd870f2e85b9d7f4d546c8fdd304fd94fc4b9e196c64cb8b7b16c798559064b4`.
The queue exposes thirteen dependency names, nine literal checks, one assertion,
symbolic machinery, and partial result prose. Neither source body has been
opened or executed before this freeze.

## Invariants, Conventions, and Allowed Imports

P147 preserves C-SPN-002's exact normalized abstract ladder and explicit
physical ceilings, C-SG-011's winding and parity exchange without particle or
weak identity, C-BND-001's rejection of W1 charge selection, and C-REP-001's
supplied-table and normalization semantics. C-U1-001 and C-GAU-001 may be used
only as independent examples of the current, connection, covariance, and
dynamical premises missing from bare representation algebra. Pending source
units and rejected readings grant no authority.

The default carrier convention is complex dimension two with orthonormal basis
and Hermitian generators `T_a=sigma_a/2`. A common Abelian generator must commute
with the irreducible SU(2) action. Chirality is a separate Lorentz-spinor factor,
not a rank-one name on the isospin carrier. All matrices and labels are exact;
source witnesses and any external comparators remain outside selection.

## Candidate Preregistration

The candidates are frozen before W2 body inspection or execution.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal W2 predicate audit | Hash-pinned source | Source matrices and labels | Retains only what each predicate evaluates | AST, process, data-flow, and mutation audit |
| B | Existing abstract spin-half specialization | Declared C2 carrier and C-SPN-002 | Operator scale | Pauli, ladder, commutator, and Casimir are duplicate exact evidence | Match every matrix identity to N=1 without physical labels |
| C | Carrier commutant and charge theorem | Irreducible SU(2) carrier and commuting Abelian operator | Common Abelian eigenvalue and coefficient | Basis relabels preserve algebra; compatible charge splitting is fixed by T3 normalization | Solve the full commutant and charge eigenvalue equations |
| D | Independent chirality-factor theorem | Isospin tensor chirality carrier and idempotent projector | Projector rank and factor placement | Tensor-product left action closes; same-carrier nontrivial projector conflicts with irreducibility | Compare commutators, adjoints, and projector mutations |
| E | Dynamical gauge completion | Spacetime field, connection, action, current, and transformation law | Couplings and kinetic normalizations | Representation algebra alone leaves all interaction data free | Inventory loaded symbols and construct inequivalent dynamics on one carrier |
| F | Governance and graph closure | Frozen dependencies and consumers | None | No circular or pending source authority enters acceptance | Hash, disposition, compatibility, and downstream replay |

## Selection Criteria and Blinding

Selection is ordered by exact carrier and basis correctness, separation of
algebra from physical identification, accepted charge and parity compatibility,
common-Abelian normalization, independent chirality semantics, correct limits,
mutation sensitivity, assumption economy, reusability, nonduplication, and
consumer closure. Queue-visible summary prose does not select a candidate.
Exact predicates, matrices, output, thresholds, and any further comparator
material remain blinded until this contract and its matching manifest are
committed.

## Proposed Claim Delta

No claim identifier is assigned at freeze. Candidate B may show that all valid
algebra is already C-SPN-002. Candidates C and D may justify a distinct additive
representation claim only after source-aware nonduplication proves that the
commutant, charge-separation, and factor-placement theorem is not already
accepted. A later proposal revision must freeze the exact statement and
dependencies before implementation. W2 is the source unit; all rejected and
qualified subclaims remain durable evidence rather than accepted authority.

## Implementation and Oracle Plan

SymPy exact matrices are the primary oracle because every load-bearing claim is
finite-dimensional algebra. The primary route will derive Hermiticity, trace,
commutators, ladder edges, Casimir, unitary basis covariance, the full
commutant, compatible charge eigenvalues, tensor-factor projector closure, and
same-carrier counterexamples. A fresh independent route will solve the linear
intertwiner and charge equations without importing any new canonical helper.

Mutations change a generator scale or sign, replace an idempotent projector,
move the projector onto the isospin carrier, alter one charge label, and break
the common Abelian eigenvalue. The source audit will derive rather than copy
every expected matrix and will distinguish a printed physical name from an
evaluated operator. No numerical rerun can strengthen an exact matrix identity.

The compatibility preflight uses the shared AST auditor. Mutable code must use
exact algebra, `trapezoid_integral`, or `np.trapezoid` and have no executable
legacy access. If immutable W2 contains `np.trapz`, native failure is recorded
as version-only and an isolated alias-only replay precedes scientific
adjudication. The frozen dependency and reverse-consumer graph will pin every
source hash and predicate inventory without importing pending authority.

## Attempts and Continuation

Every failed reproduction, representation, charge, projector, compatibility,
or graph route is appended with its diagnosis. Technical failures are repaired;
an ill-fitting concept yields to the next preregistered candidate. Neither a
source tally nor an honest no-go stops the parent migration.

## Debt Ledger

The ledger tracks carrier and basis assumptions, generator normalization,
state-label provenance, topological versus electric charge, Abelian
normalization, chirality factor placement, gauge and interaction data,
dependency cycles, compatibility shapes, broken consumers, and generated
state. The campaign remains active until every item is resolved or explicitly
excluded from the promoted claim and W2 disposition.

## Review and Promotion Plan

The exact result receives an independent linear-algebra review and individual
claim review. W2 receives a terminal disposition retaining every exact
representation identity while naming every supplied or unsupported physical
reading. Promotion, if distinct, extracts pure APIs and focused tests, validates
dependency and consumer closure, updates the registry and release, regenerates
the queue, docs, and accepted memory, and runs one integrated repository gate.
A final in-progress attempt is finalized after that gate, followed only by
record-sensitive validation.

## Done Gate

P147 closes only when the positive representation-classification object exists,
exact and independent sensitive oracles pass, every W2 predicate is
adjudicated, dependencies and reverse consumers replay, compatibility and
nonduplication are explicit, W2 has a durable terminal disposition, generated
state agrees, and the campaign debt ledger is empty. A physical SU(2)_L or weak
claim additionally requires the missing dynamical object; assigned labels and
matrix closure cannot substitute for it.
