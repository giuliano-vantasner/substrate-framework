---
description: Audit QCD1 and test a generic finite-representation scalar-loop theorem
author: vantasner
created: '2026-08-10T16:00:00Z'
updated: '2026-08-10T16:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-QCD1
- nonabelian-vacuum-polarization
category: proposals
confidence: exploratory
status: active
---
# P160 QCD1 SU3 Kinetic Induction Audit

## Question and Positive Deliverable

P160 must reproduce and independently adjudicate QCD1's claimed SU3 kinetic
induction. The positive deliverable is either a distinct importable generic
finite-Lie-representation complex-scalar loop theorem with SU2 and SU3
specializations, or a complete exact accepted composition showing why no new
claim or API is needed, together with a terminal predicate-level QCD1
disposition. Rejecting a physical QCD headline alone is not completion.

## Base Release and Provenance

The accepted base is v0.123.0 at framework commit `d5b76e8`. The predecessor
baseline is `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`.
QCD1 is pinned at
`merged-framework/bridges/phase-8/bridge_QCD1_su3_kinetic_induction.py`,
SHA-256 `b70065548c121661c9a6801255aa844a40165e947c054a48617d926955a704ed`.
Its dossier is pinned at
`merged-framework/bridges/phase-8/dossiers/QCD1-dossier.md`, SHA-256
`83270b8c52d51b439c05ae3c80a8a1679b537d265bf97854bae1312a3a32bd14`.

The generated queue exposes eleven static predicates, one assertion, symbolic
oracles, twelve candidate dependencies, a Gell-Mann representation, a copied
induction scaffold, and a physical SU3 headline. Its headline and result
excerpts were already exposed while selecting the next unit, so P160 makes no
fresh prose-blinding claim. The source body, dossier body, and detailed check
expressions remain unopened at this freeze. The predecessor's later dirty
Phase 47/48 material remains excluded.

## Invariants, Conventions, and Allowed Imports

C-LIE-001 owns the exact standard fundamental SU3 generators, trace metric,
structure constants, and Casimirs without a physical gauge-sector map.
C-VAC-001 owns the complete massive complex-scalar Euclidean two-dimensional
Abelian loop and its bubble--seagull Ward cancellation. C-NVP-001 owns the SU2
representation-indexed version and full leading background-curvature
completion, while denying a unique coupling, dimensional lift, and physical
weak sector. C-NAG-001 fixes the accepted connection and curvature signs only.
C-RGE-002 supplies a boundary showing that loop weights and physical matter
content remain separately imported.

Allowed inputs are those claims and their canonical modules, exact finite
Hermitian matrix and Lie-algebra identities, exact tensor and projector
algebra, parameter integrals, proper-time identities already accepted in P158,
and explicit counterfamilies. No quark, color-triplet substrate excitation,
statistics, determinant, regulator, gauge action, bare term, counterterm,
dimension, analytic continuation, state, or observation may enter undeclared.

## Candidate Preregistration

The candidate set distinguishes literal source replay, accepted composition,
generic and group-specific APIs, a physical QCD construction, falsifiers, and
governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal QCD1 replay | Source conventions only | Source symbols | May retain exact SU3 algebra while overclaiming the loop | Eleven-predicate AST and data-flow audit |
| B | Existing accepted composition | C-LIE-001 plus C-VAC-001 and their ceilings | Declared loop inputs | May close the two-point color factor but not a full generic non-Abelian theorem | Typed composition and novelty audit |
| C | Generic finite-representation scalar loop | Declared compact finite Hermitian representation, scalar determinant, regulator, Euclidean two-space | generators, structure constants, Q, m, g, multiplicity | Natural reusable generalization if exact validation and background completion are group-independent | SU2/SU3/direct-sum tests, Ward derivation, proper-time completion, normalization mutations |
| D | SU3-specific scalar-loop wrapper | Candidate C premises specialized to the fundamental | Same plus fixed SU3 generators | Likely duplicate if C is sound | API and claim nonduplication comparison |
| E | Physical four-dimensional QCD sector | Complete quantum gauge and quark action, gauge fixing, renormalization, matching, state | full physical inputs | High assumption cost and absent unless source constructs every premise | Action, statistics, dimension, pole, spectrum, and observable audit |
| F | Counterfamilies | Accepted invariants only | statistics, representation, normalization, bare term, counterterm, field coordinate | Narrow matrix checks survive while induction and physical readings vary | Load-bearing mutations and same-trace nonidentity examples |
| G | Governance closure | Accepted authority order | None | Terminal claim-level promotion or exact qualification | Dependency, consumer, impact, queue, release, docs, and memory replay |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, exact representation and
structure validation, explicit quantum action and statistics, bubble--seagull
Ward derivation before transverse decomposition, full background-curvature
completion, normalization and coefficient honesty, correct limits, mutation
sensitivity, independent rederivation, API economy, consumer compatibility,
and physical-scope honesty.

Queue headline and result prose already disclosed the fundamental trace value
and claimed transfer. Those known literals are excluded from selection. This
contract freezes concepts and criteria before renewed body or dossier
inspection; subsequent source values and tallies cannot select a candidate.

## Proposed Claim Delta

The provisional delta remains unselected until the source-aware comparison.
`C-NVP-002` is reserved for Candidate C: a generic finite exact
Hermitian Lie-representation massive-complex-scalar theorem in Euclidean
two-space, depending on C-VAC-001 and the accepted connection-curvature
convention. Its delta is not selected. Candidate B may instead establish that
QCD1 adds only accepted composition, while Candidate D is rejected if it is a
group-specific duplicate. No accepted claim is challenged or superseded.

## Implementation and Oracle Plan

Before any package edit, the campaign will hash, parse, reproduce, and map all
QCD1 predicates and its assertion, audit direct and semantic consumers, and
run nonduplication and impact analysis. If Candidate C survives, a pure generic
canonical API will validate same-size exact Hermitian generators, closure
against supplied exact real structure constants, a positive invariant trace
metric, and the complete scalar-loop premises. The current SU2 wrapper remains
backward compatible and becomes a specialization only if impact replay makes
that refactor safe.

SymPy fits the finite matrix, closure, trace, parameter-integral, series,
limit, Ward, and proper-time obligations. A fresh reviewer will not import the
new helper and will reconstruct SU2 and SU3 metrics, a non-orthonormal basis
coordinate mutation, direct sums, scalar bubble--seagull cancellation, and a
noncommuting background. Source numeric output, if any, is regression evidence
only. Load-bearing mutations change statistics numerator, seagull sign,
generator basis without its metric, coupling normalization, representation,
multiplicity, determinant factor, bare and counterterm coefficients, field
coordinate, dimension, and physical dictionary.

Compatibility preflight audits direct, imported, dynamic, and eager legacy
NumPy integration access. Mutable code uses exact algebra,
`trapezoid_integral`, or `np.trapezoid`, never executable `np.trapz`. Immutable
spelling-only failures receive an isolated alias backed by `np.trapezoid` and
do not reject a scientific candidate. The final transaction runs the targeted
oracles and affected tests before one integrated repository gate.

## Attempts and Continuation

The append-only ledger begins with this prior-exposure-aware freeze. Every
representation, statistics, Ward, background, normalization, compatibility,
source, consumer, or verifier failure will identify its layer and a materially
different next attempt. A failed physical interpretation returns to the
generic or accepted-composition candidates rather than ending the campaign.

## Debt Ledger

The campaign ledger tracks the pinned source and dossier, all eleven predicates
and one assertion, representation and structure conventions, quantum action,
statistics, determinant, regulator, Ward identity, exact kernel, local and
background completion, dimension, normalization, coefficient freedom,
limits, novelty, consumers, compatibility, governance, and continuation.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| QCD1 predicate strength is unaudited | Reproduce and classify all eleven checks and the assertion | open |
| Generic versus SU3-specific novelty is unknown | Compare C-LIE-001, C-VAC-001, C-NVP-001, and canonical APIs | open |
| Action, statistics, and Ward provenance are unknown | Inventory or explicitly declare the determinant, regulator, bubble, and seagull | open |
| Full non-Abelian completion is unknown | Independently derive or reject the background-curvature term | open |
| Normalization and coefficient freedom are unresolved | Mutate basis, representation, coupling, bare term, counterterm, and field coordinate | open |
| Consumers and compatibility are unknown | Replay the frozen semantic graph and executable integration shapes | open |
| Registry, release, queue, docs, and memory are unresolved | Complete claim-level adjudication and one terminal transaction | open |

## Review and Promotion Plan

A surviving C-NVP-002 receives individual review, a pure reusable API, focused
tests, exact and fresh oracles, primary-evidence provenance inherited only
through its audited use, impact analysis, registry and release updates,
generated documentation, and accepted memory. Otherwise QCD1 closes through a
disposition-specific accepted composition with no duplicate API. Both routes
require source predicates, dependencies, consumers, compatibility,
nonduplication, queue, generated state, memory, and an empty ledger.

## Done Gate

P160 closes only when the positive generic theorem or complete accepted
composition exists, every QCD1 predicate has an individual verdict, the
quantum and physical premises are typed, load-bearing mutations work, all
consumers replay, governance agrees, and debt is empty. A green source tally,
equal trace index, copied loop expression, or rejected QCD interpretation alone
cannot complete it.

## Cross-References

See QCD1, QCD1-dossier, QCD3, YM1, YM2, EM5, C-LIE-001, C-RGE-002,
C-VAC-001, C-NVP-001, C-NAG-001, P024, P135, P158, P159, and the parent
migration effort.
