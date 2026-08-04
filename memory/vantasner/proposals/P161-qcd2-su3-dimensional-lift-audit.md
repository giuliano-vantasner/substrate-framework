---
description: Audit QCD2 and test whether any distinct SU3 dimensional-lift operator survives
author: vantasner
created: '2026-08-10T17:15:00Z'
updated: '2026-08-10T18:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-QCD2
- dimensional-lift
category: proposals
confidence: established
status: archived
---
# P161 QCD2 SU3 Dimensional-Lift Audit

## Question and Positive Deliverable

P161 must reproduce and independently adjudicate QCD2's claimed lift from the
accepted conditional two-dimensional SU3 scalar loop to a 3+1-dimensional
Yang--Mills sector. The positive deliverable is either a distinct importable
operator theorem that closes every dimensional and gauge premise, or a complete
exact accepted composition that types the surviving color and Riesz objects and
terminally qualifies QCD2. A failed lift or compatibility abort alone is not
completion.

## Base Release and Provenance

The accepted base is v0.124.0 at framework commit `1451670`. The predecessor
baseline is `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`.
QCD2 is pinned at
`merged-framework/bridges/phase-8/bridge_QCD2_su3_3plus1_lift.py`,
SHA-256 `64f8125a5c0ef194e23569711036ce6ec46f3ffef2b6eb94a7b5c97ed8bb566f`.
Its dossier is pinned at
`merged-framework/bridges/phase-8/dossiers/QCD2-dossier.md`, SHA-256
`6db12d5d203e04587ab7b241a838a9a471c7fdb69a143c3f0478637100d7b129`.

P159 and P160 already executed QCD2 as a semantic consumer, and source or
dossier excerpts were exposed during those audits. P161 therefore claims no
fresh source blinding. This freeze separates prior knowledge from renewed
targeted inspection and excludes all familiar constants, powers, tallies, and
physical labels from concept selection.

## Invariants, Conventions, and Allowed Imports

C-LIE-001 owns the standard fundamental SU3 trace metric and structure
constants without a physical color map. C-NVP-002 owns a conditional massive
complex-scalar finite-representation loop only in flat Euclidean two-space and
explicitly supplies no dimensional lift or unique total coupling. C-KRN-001
owns a scalar Riesz inverse only for supplied dimension, exponent, Fourier
convention, and nonzero coefficient. C-KRN-002 owns the source--probe force
dictionary and dimension--power nonidentifiability. P159 already proves that a
trace-weighted quadratic kernel inverts with the reciprocal color metric.

Allowed inputs are those claims and exact finite-dimensional matrix inversion,
tensor-product, Fourier, and dimensional algebra. C-NAG-001 may fix only the
connection and curvature convention. No QCD1 or QCD2 physical headline, quark
or gluon dictionary, spacetime lift, kinetic coefficient, gauge fixing, source,
boundary condition, force, observation, or substrate mechanism may enter as
authority.

## Candidate Preregistration

The candidate set separates literal replay, accepted composition, a reusable
color-kernel theorem, a real dimensional map, a genuine 4D loop, falsifiers,
and governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal QCD2 replay | Pinned source conventions | Source symbols | Retains exact algebra while likely overclaiming operator meaning | Ten-predicate AST and data-flow audit |
| B | Existing accepted composition | C-LIE-001, C-NVP-002, C-KRN-001, C-KRN-002 | Their declared inputs | May own all supportable content without a new claim | Typed nonduplication and closure audit |
| C | Color-metric quadratic-kernel inversion theorem | Positive invertible finite color metric and invertible scalar kernel | Metric and scalar coefficient | Natural if a reusable consumer is missing | Exact tensor-product inverse and representation mutations |
| D | Dimension-changing intertwiner | Explicit domains, actions, dimensions, signatures, fields, and boundary data | Full map data | Required for a literal 2D-to-4D lift | Action and operator intertwining identity |
| E | Genuine 4D background matter loop | Complete 4D matter/gauge action, statistics, regulator, subtraction, matching | Masses, representations, scale, bare terms | Distinct but high-cost conditional theorem | Diagrammatic or background-field 4D derivation |
| F | Counterfamilies | Accepted invariants only | Metric, exponent, dimension, longitudinal coefficient, bare and source data | Familiar static shapes fail to select the physical construction | Inverse-metric, same-power, gauge, and normalization mutations |
| G | Governance closure | Accepted authority order | None | Terminal claim or composition review | Dependency, consumer, impact, queue, docs, release, and memory replay |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, correct quadratic-kernel
inversion, explicit action and spacetime data, dimension and exponent
identifiability, normalization honesty, correct limits, mutation sensitivity,
API economy, and consumer compatibility. Numerical closeness, a familiar
inverse-square law, a trace-one-half value, or a green source tally cannot
select a candidate. Prior exposure is documented; no fresh blinding is claimed.

## Proposed Claim Delta

The source-aware claim delta remains empty. Candidate B is selected because
accepted claims already contain every exact SU3 trace, Riesz, endpoint, and
derivative surface. Candidate C duplicates the exact colored-kernel inversion
review in P159; Candidates D and E require actions and operators absent from
QCD2. No new identifier, API, or release is planned. The source's unsupported
lift prose does not justify framework expansion.

## Implementation and Oracle Plan

The primary oracle will use exact SymPy matrix and tensor-product algebra for
color metric inversion, Riesz powers, dimensional identities, projector
structure, and coefficient counterfamilies. A fresh route will independently
derive the inverse and distinguish static scalar Green functions from gauge
quadratic operators. Any QCD2 NumPy regression is evidence only because exact
algebra decides the headline.

Compatibility preflight will AST-audit direct, imported, dynamic, and eager
legacy integration access. Mutable code must use `np.trapezoid` or the audited
safe helper. Immutable QCD2 will run through an alias backed by
`np.trapezoid`; a native abort caused solely by removed `np.trapz` is not a
scientific failure. The verifier will mutate the trace metric, inversion
direction, dimension--exponent pair, longitudinal sector, bare coefficient,
source--probe dictionary, and claimed dimensional map.

## Attempts and Continuation

The append-only ledger preserves the prior-exposure-aware freeze, native NumPy
compatibility abort, successful alias-only replay, a failed lexical probe,
repaired scientific closure, and complete source-graph replay. Primary and
fresh independent routes pass 33 and 21 checks; 53 focused accepted-API tests
pass; and the graph route passes 25 checks over 135 source predicates.
Candidates A, B, F, and G close the source through exact accepted composition,
counterfamilies, and governance without a claim or release delta.

## Debt Ledger

The campaign ledger tracks the source and dossier, all ten predicates and one
assertion, color metric and inverse direction, scalar versus gauge operator,
spacetime action and dimension, kinetic normalization, gauge and boundary data,
source--probe dictionary, compatibility, novelty, consumers, governance, and
continuation.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| QCD2 predicate strength is unaudited | Reproduce and classify all ten checks and the assertion | discharged |
| Accepted composition versus Candidate C novelty is unknown | Audit canonical APIs, P159 evidence, and actual consumers | discharged |
| The claimed dimension-changing map is unspecified | Construct it with complete typed data or reject it predicate by predicate | discharged |
| Gauge, normalization, and source data are unresolved | Exercise longitudinal, bare, counterterm, metric, and source--probe counterfamilies | discharged |
| Compatibility status is known but not campaign-pinned | Record native and alias-only behavior without scientific demotion | discharged |
| Consumers and generated state are unresolved | Replay the semantic graph and complete terminal governance synchronization | discharged |

## Review and Promotion Plan

Every distinct claim receives its own review and importable tested API. If
accepted composition is complete, QCD2 is qualified through exact mapped claims
without creating a redundant claim or wrapper. Both routes require primary and
independent oracles, source-graph replay, compatibility and impact audits,
materialized evidence, an immutable adjudication, regenerated queue and memory,
and one terminal integrated gate only when a release or terminal disposition
boundary is reached.

## Done Gate

P161 closes only when a positive operator theorem or complete accepted
composition exists, every QCD2 predicate has an individual verdict, the
spacetime and physical premises are typed, mutations are load-bearing, all
consumers replay, governance agrees, and debt is empty. The accepted
composition, individual predicate review, compatibility replay, semantic
graph, disposition, generated queue, and durable decision now satisfy that
gate without changing v0.124.0. The integrated repository result is pinned in
attempt 0009.

## Cross-References

See QCD2, QCD2-dossier, QCD1, YM2, EM7, GK1, C-LIE-001, C-NVP-002,
C-KRN-001, C-KRN-002, C-NAG-001, P136, P159, P160, and the parent migration
effort.
