---
description: Audit QCD5 and test whether three sector labels independently overdetermine dimension
author: vantasner
created: '2026-08-10T18:20:00Z'
updated: '2026-08-10T18:45:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-QCD5
- dimensional-identifiability
category: proposals
confidence: established
status: archived
---
# P162 QCD5 Dimensional Overdetermination Audit

## Question and Positive Deliverable

P162 must reproduce and independently adjudicate QCD5's claim that U1, SU2,
and SU3 copies of one Riesz force exponent overdetermine the spatial dimension
to three. The positive deliverable is either a distinct exact theorem built
from genuinely independent sector constraints, or a complete accepted
composition that types the surviving shared-exponent result, establishes its
actual constraint rank, and terminally qualifies QCD5. Showing only that the
headline is circular or rank deficient is not completion.

## Base Release and Provenance

The accepted base is v0.124.0 at scientific commit `1451670`; the clean
framework checkpoint is `68ef8fd`. The predecessor baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. QCD5 is pinned at
`merged-framework/bridges/phase-8/bridge_QCD5_d3_overdetermination.py`, SHA-256
`60a2f5b8dbd76f3b4d6b0a48e4fcd5ed9edbc6a4e1d3869cb4a40bf30c87084c`.
Its dossier is pinned at
`merged-framework/bridges/phase-8/dossiers/QCD5-dossier.md`, SHA-256
`e5169d4eae1706e9d000cf1c313e22bbcefcf9840ead86642224ab8bc0a8975d`.

P159 and P161 already executed QCD5 as a semantic consumer and exposed selected
source predicates. P162 therefore claims no fresh source blinding. The dossier
has not been intentionally reopened in this campaign before the freeze. Known
`d=3`, `s=1`, three-sector, tally, and counterexample values are barred from
candidate selection.

## Invariants, Conventions, and Allowed Imports

C-KRN-001 owns only a fixed-input scalar Riesz inverse. C-KRN-002 proves that
inverse-square behavior selects the one-parameter family `d=2s+1`, not either
parameter separately. C-LIN-001 distinguishes equation count from exact row
rank, so proportional or identical rows add no independent constraint. EM7,
YM2, QCD1, and QCD2 are qualified and grant no dimensional-lift or endpoint
selection authority.

Allowed inputs are those accepted claims, C-LIE-003 and C-NVP-002 only for exact
SU3 trace data and their ceilings, and exact rank, nullspace, exponent, and
finite-dimensional algebra. No physical Coulomb comparator, observed
dimension, gauge-sector independence, geometry, action, dimensional map, or
substrate mechanism may enter as authority. QCD5 and its dossier become
hash-pinned candidate evidence only after the freeze.

## Candidate Preregistration

The candidate set separates literal replay, accepted composition, a possible
rank-ledger theorem, genuine independent sector derivations, a geometric
selection mechanism, falsifiers, and governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal QCD5 replay | Pinned source conventions | Source symbols | Retains exact substitutions but may overcount repeated rows | Seven-predicate AST and data-flow audit |
| B | Existing accepted composition | C-KRN-002 and C-LIN-001 | Supplied `s`, force power, row provenance | One shared equation and rank one | Exact rank and dependency closure |
| C | Provenance-aware constraint-rank theorem | Finite exact rows with independent provenance | Constraint matrix and right side | Useful only if C-LIN-001 lacks the surface | Registry, API, and consumer nonduplication audit |
| D | Independent sector mechanisms | Separately derived U1, SU2, and SU3 operators | Sector-specific powers and inputs | Can overdetermine only if rows are genuinely distinct | Independent derivations and rank increase |
| E | Geometric dimension selector | Explicit metric, measure, operator, and map | Geometric data | Could fix `d` without a force comparator | Construction and limiting-case oracle |
| F | Counterfamilies | Accepted invariants only | `s`, sector amplitudes, labels, row multiplicity | Repeated labels preserve rank one | Nonunit-`s`, label permutation, amplitude, and row-duplication mutations |
| G | Governance closure | Accepted authority order | None | Terminal claim or composition review | Dependency, consumer, impact, queue, memory, and release replay |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, exact algebraic rank,
independently sourced rows, dimension and exponent identifiability, explicit
operator and geometry data, assumption economy, mutation sensitivity, API
novelty, consumer compatibility, and physical-scope honesty. Counting three
sector labels, reproducing a familiar inverse-square exponent, or printing
three copies of `d=3` cannot select a concept. Prior source exposure is recorded
and all familiar values are excluded from thresholds.

## Proposed Claim Delta

The source-aware claim delta remains empty. Candidate B is selected because
C-KRN-002 already owns `d=2s+1` and C-LIN-001 already governs exact rank,
consistency, nullity, equation count, and duplicate rows. Candidate C would
duplicate `diagnose_linear_system`. Candidates D and E require sector-specific
operators or geometry absent from QCD5. No new identifier, API, or release is
planned.

## Implementation and Oracle Plan

The primary oracle will hash, parse, reproduce, and map every QCD5 predicate
and its assertion. SymPy exact solves, matrix ranks, nullspaces, substitutions,
and symbolic mutations fit the load-bearing obligations. A fresh independent
route will derive the constraint matrix without importing P162 helpers. Numeric
source output is regression evidence only because exact algebra decides the
rank and family.

Compatibility preflight will AST-audit direct, imported, dynamic, and eager
legacy integration access. Mutable code must use exact algebra,
`trapezoid_integral`, or `np.trapezoid`. Immutable sources with only legacy
spelling receive an isolated alias backed by `np.trapezoid`, never a scientific
demotion. Mutations will vary `s`, duplicate or remove sector rows, permute
labels, change color amplitudes, give sectors distinct exponent functions, and
test inconsistent rows. The graph replay will pin dependencies and consumers
without converting their green tallies into authority.

## Attempts and Continuation

The append-only ledger preserves the prior-exposure-aware freeze, successful
native replay, one verifier API-field failure, two graph-inventory failures,
repaired exact closure, and complete source-graph replay. The inventory repairs
distinguish lexical check sites, runtime executions, and actual assertion
nodes. Primary and fresh independent routes pass 32 and 14 checks, 46 focused
accepted-API tests pass, and the graph route passes 20 checks over 91 lexical
and 99 runtime predicates. Candidates A, B, F, and G close the source through
exact accepted composition, counterfamilies, and governance.

## Debt Ledger

The campaign ledger tracks all source predicates, row provenance and rank,
dimension and exponent inputs, sector amplitudes, comparator circularity,
geometry and operator data, compatibility, novelty, consumers, governance, and
continuation.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| QCD5 predicate strength is unaudited | Reproduce and classify all seven checks and the assertion | discharged |
| Three-sector independence is unproved | Recover the exact constraint rows and their provenance and rank | discharged |
| Dimension and exponent selection are unresolved | Mutate `s` and distinguish a conditional specialization from identification | discharged |
| Candidate C novelty is unknown | Audit C-LIN-001, canonical APIs, prior campaigns, and consumers | discharged |
| Geometry and sector-specific operators are unspecified | Construct them with complete data or reject their source attribution | discharged |
| Consumers and generated state are unresolved | Replay the semantic graph and complete terminal governance synchronization | discharged |

## Review and Promotion Plan

Every distinct claim receives its own review and importable tested API. If
accepted composition is complete, QCD5 is qualified through exact mapped claims
without creating a redundant theorem or wrapper. Both routes require primary
and independent oracles, source-graph replay, compatibility and impact audits,
materialized evidence, an immutable adjudication, regenerated queue and memory,
and one integrated terminal gate only at the terminal disposition boundary.

## Done Gate

P162 closes only when a positive exact theorem or complete accepted composition
exists, every QCD5 predicate has an individual verdict, row rank and provenance
are explicit, dimension and exponent inputs are typed, mutations are
load-bearing, all consumers replay, governance agrees, and debt is empty. The
accepted composition, individual predicate review, rank and mutation oracles,
semantic graph, disposition, generated queue, and durable decision satisfy
that gate without changing v0.124.0. The integrated result is pinned in attempt
0008.

## Cross-References

See QCD5, QCD5-dossier, EM7, D3S, YM2, QCD2, GK1, C-KRN-001, C-KRN-002,
C-LIN-001, P064, P136, P159, P161, and the parent migration effort.
