---
description: Audit SM1 and test whether named factor algebras establish a physical Standard Model gauge group
author: vantasner
created: '2026-08-10T18:55:00Z'
updated: '2026-08-10T18:55:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-SM1
- product-gauge-algebra
category: proposals
confidence: exploratory
status: active
---
# P163 SM1 Combined Gauge-Group Audit

## Question and Positive Deliverable

P163 must reproduce and independently adjudicate SM1's claim that three named
factor constructions establish the combined Standard Model gauge group. The
positive deliverable is either a distinct importable theorem with complete
local, global, representation, coupling, and action data, or a complete
accepted composition that types the surviving direct-sum algebra and
terminally qualifies SM1. Showing only that physical identification is absent
does not complete the campaign.

## Base Release and Provenance

The accepted base is v0.124.0 at scientific commit `1451670`; the clean
framework checkpoint is `9e491a7`. The predecessor baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. SM1 is pinned at
`merged-framework/bridges/phase-9/bridge_SM1_combined_gauge_group.py`, SHA-256
`bb7b70bc2ac0dd703f95ccbbaf843d40e78279f357795b9be74d6eee484749f2`.
Its dossier is pinned at
`merged-framework/bridges/phase-9/dossiers/SM1-dossier.md`, SHA-256
`e605e5c0ecedd041c733ed08e60a2ad0461fbb72f00c989da4633e0b2fda8c3b`.

P141 through P145, P147, and P160 already executed SM1 as a semantic consumer
and exposed source predicates. P163 therefore claims no fresh source blinding;
the dossier has not been intentionally reopened in this campaign before the
freeze. The queue records six literal checks, no dynamic check site, one
assertion, a symbolic oracle hint, and candidate edges to qualified G1 through
G5, QCD1, W2, and YM1.

## Invariants, Conventions, and Allowed Imports

C-LIE-001 owns standard fundamental SU3 representation algebra and explicitly
denies physical color identification. C-NAG-001 owns a conditional finite
non-Abelian connection and curvature without physical matter, action
normalization, coupling match, or substrate map. C-GAU-001 owns conditional
local U1 covariance without a Maxwell action, photon, electric-charge map, or
substrate sector.

Allowed inputs are those accepted claims, C-LIE-003 only for exact SU3
convention checks, and exact finite-dimensional direct-sum, block-matrix,
dimension, center, commutant, and Lie-bracket algebra. A direct-sum Lie algebra
has componentwise brackets and zero cross brackets, but its dimension and
local algebra do not determine a global direct product versus quotient, a
faithful matter representation, hypercharge normalization, gauge action,
couplings, currents, or physical Standard Model identification. SM1 and its
dossier become hash-pinned candidate evidence only after the freeze.

## Candidate Preregistration

The candidate set separates literal replay, accepted composition, a possible
typed direct-sum ledger, the global Standard Model group, a physical
three-sector action, falsifiers, and governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal SM1 replay | Pinned source conventions | Source symbols | May retain finite algebra while overclaiming physical meaning | Six-predicate AST and data-flow audit |
| B | Existing accepted composition | Accepted factor algebras plus elementary direct sum | Supplied factors and embeddings | Likely owns the local algebra without a new API | Exact closure and nonduplication audit |
| C | Importable direct-sum ledger | Exact finite generator families and embeddings | Carriers, brackets, factor labels | Useful only if a real consumer needs typed cross-factor checks | Registry, API, and consumer search |
| D | Global Standard Model gauge group | Global topology, quotient kernel, faithful matter representation, hypercharge normalization | Group and representation data | Distinct if SM1 constructs more than the local algebra | Center-kernel and representation-faithfulness oracle |
| E | Physical simultaneous gauge action | Fields, three couplings, kinetic forms, matter, currents, dimensions, regulator or classical dynamics | Full action data | Required for a physical gauge-sector headline | Gauge covariance, action, source, and coupling audit |
| F | Counterfamilies | Accepted algebra only | Labels, isomorphic factors, quotients, couplings, embeddings | Same dimensions and zero cross brackets need not select the Standard Model | Label, quotient, carrier, and coupling mutations |
| G | Governance closure | Accepted authority order | None | Terminal claim or composition review | Dependency, consumer, impact, queue, memory, and release replay |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, exact bracket provenance,
separation of local Lie algebra from global group, explicit faithful matter
representations and quotient kernel, supplied action and couplings, assumption
economy, mutation sensitivity, API novelty, and downstream compatibility.
Dimension `8+3+1`, familiar group labels, or a green source tally cannot select
a concept. Prior source exposure is recorded and no fresh blinding is claimed.

## Proposed Claim Delta

The initial claim delta is empty because the accepted factor claims and
elementary direct-sum algebra may already own every supportable result.
Candidate C may receive a source-aware proposal only if the canonical
nonduplication and consumer audit finds a missing typed surface. Candidates D
and E require all global, representation, field, action, and coupling premises
to be present and independently verified; source labels cannot supply them.

## Implementation and Oracle Plan

The primary oracle will hash, parse, reproduce, and map every SM1 predicate and
its assertion. SymPy exact matrices, commutators, ranks, centers, kernels, and
block embeddings fit the load-bearing local and global algebra obligations. A
fresh independent route will build direct-sum brackets without importing P163
helpers and will contrast local-isomorphic groups with distinct global
quotients and representations. Any displayed dimension is regression evidence
only because dimension cannot decide group identity or physical realization.

Compatibility preflight will AST-audit direct, imported, dynamic, and eager
legacy integration access. Mutable code must use exact algebra,
`trapezoid_integral`, or `np.trapezoid`. Immutable legacy spelling receives an
isolated alias backed by `np.trapezoid`, never a scientific demotion. Mutations
will relabel equal-dimensional algebras, vary cross brackets, change block
embeddings and centers, compare direct products with discrete quotients, vary
couplings independently, remove matter representations, and test whether any
source object actually enters an action or covariant derivative. The graph
replay will pin dependencies and consumers without converting their tallies
into authority.

## Attempts and Continuation

Attempts are append-only and distinguish compatibility, verifier, local
algebra, global-group, representation, physical-action, candidate, target, and
foundation failures. A local direct-sum result returns first to accepted
composition or a genuinely typed global construction; it cannot rewrite the
factor claims to save a physical headline.

## Debt Ledger

The campaign ledger tracks all source predicates, factor provenance, local
brackets, embeddings, global quotient, centers, faithful representations,
hypercharge normalization, fields, couplings, action, compatibility, novelty,
consumers, governance, and continuation.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| SM1 predicate strength is unaudited | Reproduce and classify all six checks and the assertion | open |
| Factor independence and cross brackets are unproved | Recover the exact embedded generators and bracket table | open |
| Local algebra versus global group is unresolved | Audit centers, quotient kernels, and representation faithfulness | open |
| Candidate C novelty is unknown | Audit canonical APIs, accepted claims, prior campaigns, and consumers | open |
| Physical sector data are unspecified | Construct fields, couplings, action, currents, and matter representations or reject their source attribution | open |
| Consumers and generated state are unresolved | Replay the semantic graph and complete terminal governance synchronization | open |

## Review and Promotion Plan

Every distinct claim receives its own review and importable tested API. If
accepted composition is complete, SM1 is qualified through exact mapped claims
without creating a redundant theorem or wrapper. Both routes require primary
and independent oracles, source-graph replay, compatibility and impact audits,
materialized evidence, an immutable adjudication, regenerated queue and memory,
and one integrated terminal gate only at the terminal disposition boundary.

## Done Gate

P163 closes only when a positive exact theorem or complete accepted composition
exists, every SM1 predicate has an individual verdict, local and global group
data are separated, representations and physical inputs are typed, mutations
are load-bearing, all consumers replay, governance agrees, and debt is empty. A
dimension count, zero cross bracket, or rejected physical interpretation alone
cannot complete the campaign.

## Cross-References

See SM1, SM1-dossier, G1 through G5, QCD1, W2, YM1, C-LIE-001,
C-LIE-003, C-NAG-001, C-GAU-001, P141 through P145, P147, P158, P160, and the
parent migration effort.
