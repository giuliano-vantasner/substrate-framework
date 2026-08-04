---
description: Derive and audit NA1's exact finite non-Abelian holonomy content
author: vantasner
created: '2026-08-10T08:45:00Z'
updated: '2026-08-10T08:45:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-NA1
- nonabelian-holonomy
category: proposals
confidence: exploratory
status: active
---
# P156 NA1 Non-Abelian Holonomy Audit

## Question and Positive Deliverable

P156 must deliver an exact importable classification of finite parallel
transport in C-NAG-001's convention. It must distinguish an open transporter
from closed-loop conjugacy data, freeze the product order, prove the commuting
collapse and reversed-path inverse, demonstrate genuine order sensitivity with
noncommuting segments, and separate raw trace, normalized trace, spectrum,
basepoint, and representation behavior. It must keep Aharonov--Bohm, weak-
sector, particle, detector, and substrate interpretations behind their missing
base-space, action, carrier, source, and observable premises.

## Base Release and Provenance

The accepted base is v0.121.0 at framework and scientific commit `b4f2e61`.
The source baseline is `/home/dan/substrate` commit
`6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; its later dirty engineering,
framework-prose, and memory files remain excluded. NA1 is pinned at
`merged-framework/bridges/phase-7/bridge_NA1_su2L_wilson_loop.py`, SHA-256
`c36b2eeace179a95b44400ea42b74f6263671fd4b4a8441fc682c480bc9372c8`.
Its dossier is `merged-framework/bridges/phase-7/dossiers/NA1-dossier.md`,
SHA-256
`d0f7c241d0a06ce85acd3e98c9911023141104778543252d436a2704e229b262`.

The queue exposes five literal checks, one assertion, a symbolic oracle, five
candidate labels, and the fundamental `2*pi` minus-identity and `4*pi`
identity values. Those unavoidable values are recorded and cannot select a
concept. The source and dossier bodies, exact AST flow, guards, further
constants, and narrative consumers remain unopened.

## Invariants, Conventions, and Allowed Imports

C-NAG-001 fixes `D=partial-i*g*W` and therefore the path equation
`dV/ds=i*g*dot(x)^mu*W_mu*V`. Its finite connection law requires open
transport to transform by endpoint factors and closed transport by basepoint
conjugation. C-REP-002 supplies the Pauli-half fundamental carrier but no
physical weak doublet. C-BER-001 is a scalar rank-one Berry invariant with an
endpoint transition, while C-WIL-001 concerns declared area and perimeter
expectation laws; neither is a matrix parallel transporter. C-KIN-001 supplies
no holonomy authority, and pending O1 supplies none at all.

For ordered integrated Hermitian segments `B1,...,Bn`, chronological transport
is frozen as `exp(i*Bn)*...*exp(i*B1)`. Pairwise commuting segments collapse
to `exp(i*sum B)`, path reversal gives the inverse, and noncommuting Pauli-axis
segments must change the matrix under order exchange. A constant T3 loop is a
one-generator commuting control even when its fundamental value is central.
Closed-loop matrices are covariant; their conjugacy class, spectrum,
determinant, and trace are invariant finite-carrier data. Raw and normalized
traces and different representations must not be mixed.

## Candidate Preregistration

The candidates are frozen before source or dossier inspection and execution.

| Candidate | Description | Assumptions | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- |
| A | Literal NA1 audit | Hash-pinned source and dossier | Retains only convention-consistent exact consequences | AST, data-flow, process, guard, and mutation audit |
| B | General path transport | C-NAG-001 convention and an oriented path | Endpoint covariance and closed-loop conjugation | Direct ODE/product-rule derivation |
| C | Segmented ordered transport | Exact Hermitian integrated segments | Commuting collapse plus genuine order sensitivity | Exact exponentials, swapped order, reverse path |
| D | Conjugacy and representation audit | Declared finite carrier | Trace and spectrum are covariant but representation dependent | Fundamental, adjoint, and basis-change controls |
| E | Berry and AB comparison | Separately typed connections and base spaces | Equal phases do not identify physical objects | Premise, endpoint, curvature, and observable map |
| F | Accepted composition only | Existing accepted claims | No new claim if the theorem is duplicate | Registry, source, API, and semantic nonduplication |
| G | Physical countermodels | Same center value under distinct models | Center equality leaves physical dictionaries free | Alternative connections, paths, and carriers |
| H | Governance closure | Frozen graph and registry | Pending or green sources grant no authority | Dependency, consumer, queue, release, docs, and memory replay |

## Selection Criteria and Blinding

Selection is ordered by convention agreement; explicit path orientation,
segment order, endpoints, basepoint, carrier, coupling, and trace
normalization; genuine noncommutativity; composition, unitarity, determinant,
reverse-path, commuting, and constant limits; gauge and basis covariance;
representation sensitivity; separation from Berry, topology, curvature, flux,
and observables; mutation sensitivity; assumption economy; reusable API fit;
and complete semantic-consumer closure. Queue-exposed minus-identity,
plus-identity, and trace values do not select a theorem.

## Proposed Claim Delta

No claim identifier is reserved before source-aware nonduplication. A distinct
claim may be proposed only if the general endpoint-covariant transport and
ordered-segment theorem is absent from C-NAG-001, C-BER-001, C-WIL-001, the
registry, package APIs, campaigns, and durable memory. Otherwise NA1 will be
terminally mapped to accepted claims without a release change.

## Implementation and Oracle Plan

SymPy exact matrix exponentials and independent linear-ODE or Pauli-product
algebra are the primary oracles. The canonical route must derive product
ordering, endpoint covariance, closed-loop conjugation, reverse-path inverse,
commuting collapse, and representation data. A fresh route must avoid any new
helper module. Mutations reverse the `i*g` sign, swap noncommuting segments,
replace one axis by a commuting one, drop an endpoint factor, reverse the path,
change carrier representation, and confuse raw with normalized trace.

Compatibility preflight is explicit: canonical integration uses
`trapezoid_integral`, mutable current-environment scripts use
`np.trapezoid`, and executable direct, imported, or dynamic `np.trapz` access
is forbidden. If immutable NA1 aborts only from legacy NumPy spelling, an
alias backed by `np.trapezoid` may reproduce it and the event is version-only
rather than scientific rejection. The exact campaign should need no numeric
quadrature.

## Attempts and Continuation

Every sign, product-order, endpoint, gauge, basis, trace, representation,
topology, physical-dictionary, compatibility, dependency, consumer, or
verifier failure is preserved append-only with a materially different next
attempt. Technical invocation failures are repaired without changing the
science; overclaims yield to another registered candidate.

## Debt Ledger

The ledger tracks source, dossier, contract, and preexposure hashes; all five
predicates and one assertion; derivative and transporter conventions; path and
segment order; endpoint and basepoint behavior; commuting and noncommuting
controls; inverse, unitarity, determinant, trace, and spectrum; fundamental
and adjoint center images; Berry, topology, curvature, flux, AB, and physical
ceilings; five candidate dependencies; semantic and lexical consumers;
compatibility; nonduplication; disposition; generated state; and parent
continuation. Every item must be derived, declared, rejected, or excluded.

## Review and Promotion Plan

Every affected claim receives individual review. NA1 receives a terminal
disposition naming exactly which matrix identities survive and which weak or
AB readings do not. Any distinct theorem is extracted into pure APIs and
focused tests only after a frozen source-aware revision. Primary, independent,
graph, compatibility, dependency, consumer, nonduplication, release, queue,
documentation, and memory paths are replayed. One integrated gate runs at the
final promotion boundary; afterward only record-sensitive checks repeat.

## Done Gate

P156 closes only when the transporter convention, ordering, endpoint gauge
law, closed-loop conjugacy, commuting and noncommuting controls, orientation
reversal, representation dependence, all five source predicates, physical
content, compatibility, semantic consumers, generated state, and debt ledger
close through accepted APIs or a reviewed no-release disposition. A physical
weak Aharonov--Bohm sector additionally requires a governed base-space loop,
connection and action, matter carrier and coupling, flux or excluded-region
geometry, dynamics, and an observable interference dictionary; a central
matrix value cannot replace them.

## Cross-References

See NA1, NA1-dossier, B1, O1, W2, W4, W7, C-NAG-001, C-REP-002,
C-BER-001, C-WIL-001, C-KIN-001, `nonabelian_gauge.py`,
`berry_holonomy.py`, `wilson_loops.py`, and the parent migration effort.
