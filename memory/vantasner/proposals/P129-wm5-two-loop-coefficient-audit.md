---
description: Audit whether WM5 conditionally derives a two-loop gauge matrix from a complete supplied representation table
author: vantasner
created: '2026-08-08T19:30:00Z'
updated: '2026-08-08T19:30:00Z'
tags: [substrate-framework, campaign-proposal, renormalization, migration-WM5]
category: proposals
confidence: exploratory
status: active
---
# P129 WM5 Two-Loop Coefficient Audit

## Question and Positive Deliverable

P129 must deliver an exact, import-explicit classification of WM5's one-loop
coefficient vector and two-loop gauge-gauge matrix. The positive candidate is a
reusable product-group representation-sum ledger with declared field counting,
normalization, matrix orientation, and imported perturbative weights—not table
agreement or a claim that charge labels derive a physical Standard Model.

## Base Release and Provenance

The accepted base is v0.98.0 at parent checkpoint `ae73006`; the latest
scientific transaction is P128 at `a83cc63`. Source evidence remains pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`.

WM5 is `merged-framework/bridges/phase-33/bridge_WM5_two_loop_coefficients.py`,
27,585 bytes, SHA-256
`8c3fbfeecb6f98d7d80c47e8f267fe1216dde724b81cc3f73f2a3bb17caf1bbc`,
and blob `d081b27dd4604137b4edaee2166baf912532c684`. Queue metadata records eleven
static sites, eight literal and three dynamic, one assertion, a symbolic oracle,
and dependencies QCD1, QCD3, SM2, SM3, SM4, WM1, WM2, and WM6. Direct pending
consumers are WM6, WM7, and WM10. Dirty Phase47/48 work and the source
compatibility overlay remain excluded.

Authority recall read v0.98.0, C-LIE-001, C-REP-001, C-RGE-001, C-RGE-002,
C-RGE-004, the canonical SU3 and charge-trace modules, P024/QCD3, P081/WM1,
all dependency dispositions, queue metadata, parent memory, and durable memory
search results. WM5's body, formulas, coefficient entries, standard table,
output, and predicate details remain unopened through freeze.

## Invariants, Conventions, and Allowed Imports

A finite charge table does not uniquely determine a product-group multiplet
table. The latter must separately state each representation, dimension, Dynkin
index, Casimir, multiplicity, chirality convention, scalar convention, and
Abelian normalization. C-LIE-001 fixes only one SU3 convention; C-REP-001
explicitly withholds physical meaning from WM1's labels.

The beta convention must state signs, loop powers, Weyl versus Dirac and real
versus complex weights, and B-matrix orientation. A positive Abelian generator
rescaling paired with inverse coupling rescaling changes raw coefficient
coordinates predictably and cannot select GUT normalization. Gauge-gauge terms
alone omit Yukawa contributions to the full two-loop gauge beta. Threshold,
scheme, matching, boundary, and validity assumptions stay explicit.

An audited primary-source general loop formula may enter only as a declared
external premise after freeze. Exact representation arithmetic, accepted SU3
invariants, accepted trace covariance, and hash-pinned WM5 evidence are allowed.
No numerical integration is expected; a compatibility alias cannot affect the
scientific verdict.

## Candidate Preregistration

The candidates are frozen before WM5 source access.

| Candidate | Construction | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- |
| A | Literal source reproduction | Evidence only | Any predicate or provenance sentence exceeds its oracle |
| B | Generic multiplet-sum ledger | Possible distinct API | Inputs or imported weights remain hidden |
| C | Fresh SM-like multiplet enumeration | Independent exact route | Entries disagree before comparator opening |
| D | Source-data provenance audit | Labels are insufficient | Executable dependencies supply every invariant directly |
| E | Abelian rescaling | Coordinate covariance required | Raw U1 entries remain invariant under generator rescaling |
| F | Convention map | Exact sign and orientation map required | A transpose or counting mutation survives |
| G | Full-beta ceiling | Gauge matrix is incomplete | Yukawa, threshold, or matching terms are actually included |
| H | Field mutations | Every load-bearing field must matter | Multiplicity, charge, or scalar mutations pass unchanged |
| I | Blinded table and graph audit | Comparison and consumers are downstream | Comparator entries select construction or duplicate an accepted API |

## Selection Criteria and Blinding

Selection prioritizes exact representation provenance, multiplicity and
invariant closure; explicit loop weights and conventions; Abelian covariance;
mutation sensitivity; accepted dependency fit; parameter economy;
nonduplication; and consumer closure. Standard matrix values remain blinded
until derivation routes and conventions are frozen. Agreement cannot select a
formula or confer physical authority.

## Proposed Claim Delta

C-RGE-005 is tentatively reserved for a generic, premise-explicit product-group
coefficient ledger if a distinct reusable theorem, canonical API, sensitive
tests, and consumer survive. It will not state that the supplied table is the
physical Standard Model or that the general loop formula was derived here.

## Implementation and Oracle Plan

The primary route will pin WM5 and every executed dependency, recover field and
formula provenance with AST and exact data ledgers, map source conventions, and
mutate signs, transpose, multiplicities, charges, representations, scalar
content, generation count, and U1 normalization. A canonical API is extracted
only if it adds a distinct general theorem.

The independent route will enumerate separately declared SM-like multiplets
and compute exact sums without importing WM5 or the primary verifier. A
primary-literature audit will pin the external loop formula and distinguish its
gauge-gauge matrix from the full beta. SymPy exact arithmetic is the strongest
oracle; standard-table comparison opens only after structural checks freeze.

## Attempts and Continuation

Every provenance, source, representation, normalization, field-counting,
formula, sign, orientation, comparator, dependency, consumer, verifier, or
workflow failure is preserved append-only before repair.

## Debt Ledger

P129 tracks source and freeze hashes, imported scripts and primary literature,
every field record, representation and multiplicity, Weyl/Dirac and
real/complex conventions, Dynkin and Casimir normalizations, Abelian coordinate,
generation and scalar counts, loop weights, sign, powers, matrix orientation,
Yukawa and threshold omissions, every predicate, mutations, dependencies,
consumers, nonduplication, claim disposition, generated state, and parent
continuation. Every item must close.

## Review and Promotion Plan

Both exact routes, source predicate audit, literature and convention ledgers,
mutations, dependency and consumer replay, nonduplication, and impact analysis
must agree. A surviving generic theorem is promoted claim by claim; otherwise
WM5 receives terminal qualification with no release change. One integrated
workflow closes each actual commit or promotion boundary.

## Done Gate

P129 closes only when every coefficient has a traceable representation sum and
imported formula, all conventions and omissions are explicit, the comparator
is downstream of selection, every predicate and mutation is adjudicated, the
graph and generated state agree, and debt is empty. A green standard-table
comparison alone is not completion.

## Cross-References

See C-LIE-001, C-REP-001, C-RGE-001, C-RGE-002, C-RGE-004, P024, P081,
QCD1, QCD3, SM2-SM4, WM1, WM2, WM5, WM6-WM7, WM10, v0.98.0, and the parent
migration effort.
