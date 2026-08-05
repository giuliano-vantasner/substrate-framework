---
description: Reaudit CF5's current-NumPy reproduction and information closure
author: vantasner
created: '2026-08-11T00:20:00Z'
updated: '2026-08-11T00:48:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-CF5
- numpy-compatibility
category: proposals
confidence: established
status: archived
---
# P170 CF5 Current-NumPy Information Closure Audit

## Question and Positive Deliverable

P170 must determine whether every CF5 predicate reproduces under current NumPy
and whether any output adds independent information beyond C-VTX-001,
C-VTX-002, and C-FLX-001. The positive deliverable is a compatibility-neutral,
claim-level duplicate audit that reproduces the source, types every predicate,
tests the effective-area inversion and comparison window, closes dependencies
and consumers, and retains a terminal duplicate disposition without confusing
an API name with physics.

## Base Release and Provenance

The accepted base is v0.127.0 at clean framework commit `af30141`, with 163
accepted claims. The source baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. CF5 is pinned at
`merged-framework/bridges/phase-10/bridge_CF5_flux_tube_tension_consistency.py`,
SHA-256
`0a449f8b95bc0a83fb0316992fb0d1776a6157e1445029623b4608246dc256f7`.
Its dossier is pinned at
`merged-framework/bridges/phase-10/dossiers/CF5-dossier.md`, SHA-256
`bd499ab50a04c45d3a80167a5a20b75067b8eecff5bfe11d992270e94ba95305`.
Both paths are clean at the pinned source commit; unrelated predecessor dirt is
excluded.

CF5 is already terminal duplicate evidence through P029. P029, the registry,
memory, generated queue, and P168 graph replay expose its six checks,
pre-check removed-`np.trapz` abort, BVP diagnostics, effective-area inversion,
broad ratio window, and physical exclusions. P170 claims no fresh source or
comparator blinding and audits the existing result rather than inheriting its
tally or its environment failure.

## Invariants, Conventions, and Allowed Imports

C-VTX-001 owns the conditional smooth-vortex equations, flux, and inverse
lengths; C-VTX-002 owns only the explicit resolution-bounded profile and
tension branch. C-FLX-001 owns the ideal fixed-area energy slope and explicitly
states that `A_eff=Phi^2/(2*sigma)` reconstructs a supplied tension rather than
predicting area. No accepted map identifies the smooth vortex with a uniform
fixed-area chromoelectric tube.

Compatibility is scientifically neutral. Mutable code uses
`trapezoid_integral` or `np.trapezoid`. Direct, imported, dynamic, and eager
legacy access is audited. The immutable source may run in an isolated process
with the missing legacy attribute bound only to `np.trapezoid`; the source is
not edited, and native name availability cannot reject or select a concept.

An information-bearing geometry comparison requires an independent profile
observable, support or moment convention, and discriminating preregistered
criterion. Numerical closeness to a broad interval and exact back-substitution
of an inverted input supply neither. No physical chromoelectric, QCD,
confinement, absolute-scale, or substrate premise is allowed.

## Candidate Preregistration

The candidates separate native and alias reproduction, accepted duplicate
composition, possible geometry novelty, a possible ratio theorem, bounded BVP
regression, physical overreach, evidence reuse, and governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Native abort plus alias-only replay | Hash-pinned source and current NumPy | Source demo inputs | Expected complete compatibility-neutral reproduction | AST audit and two-process execution |
| B | Accepted duplicate composition | C-VTX-001/002 and C-FLX-001 | Accepted symbolic and demo inputs | Expected terminal duplicate | Exact object, dependency, API, and consumer comparison |
| C | Independent effective geometry | A profile support, moment, or radius enters | New geometric convention | Expected absent | Source dataflow and profile-observable audit |
| D | Distinct ratio theorem | Independent area ratio and sharp criterion | `n,g,v,sigma` | Expected non-discriminating | Exact inversion and window mutation audit |
| E | Current BVP regression only | Source numeric branch remains valid | Declared mesh/domain/tolerance | Possible bounded evidence reuse | Status, diagnostic, and accepted-evidence hash audit |
| F | Physical model identity | Chromoelectric and QCD maps | Additional physical inputs | Expected conflict | Dependency and nonperturbative oracle audit |
| G | Full P026 rerun | Accepted evidence or canonical behavior drifted | Refinement matrix | Disfavored if hashes and current gates match | Hash, assumptions, and current canonical solver audit |
| H | Governance closure | Accepted authority order | None | Duplicate disposition remains synchronized | Source, claim, queue, memory, release, and consumer replay |

## Selection Criteria and Blinding

Selection is ordered by compatibility-neutral complete replay, independent
information and profile geometry, exact inversion sensitivity, discriminating
window and scale convention, dependency and API economy, consumers, and
governance. Numerical proximity cannot select a candidate. Prior formula,
verdict, and alias-execution exposure is recorded; no fresh blinding is claimed.

## Proposed Claim Delta

No claim is proposed at freeze. Candidate B is expected because P029 already
classified CF5 as duplicate evidence and the three accepted claims cover every
reported object. A delta requires an independently computed geometric
observable or other distinct exact object with complete dependency,
nonduplication, mutation, consumer, and review closure.

## Implementation and Oracle Plan

The primary route will inventory CF5's imports, six lexical and runtime checks,
assertions, solver status, formulas, inputs, terminology, and direct, imported,
dynamic, and eager legacy integration access. Native execution is preserved.
An isolated alias backed by `np.trapezoid` must recover the complete source
tally without editing bytes. Scientific diagnostics are compared using the
source's inequalities rather than exact printed decimals.

SymPy exact elimination, differentiation, dimensions, and interval maps fit
the information claim. Mutations vary the inversion coefficients, supplied
tension, flux, penetration-length convention, core-area factor, and comparison
window. A fresh exact review imports neither canonical model module nor numeric
solver. Hash-identical P026/P029 refinements are reused unless assumptions or
current canonical status gates differ; current source, one proportionate
canonical regression, graph, and focused consumers are replayed. Lexical
checks, runtime checks, and assertions remain separate inventories.

## Attempts and Continuation

Attempt 0001 freezes the contract before P170 opens CF5 or its dossier and
discloses P029/P168 exposure. Attempt 0002 preserves the native pre-predicate
version stop, and attempt 0003 passes all six predicates through the isolated
`np.trapezoid` alias. Attempts 0004 and 0005 pass 41 primary and 20 fresh exact
checks. Attempt 0006 preserves a graph-probe construction error that conflated
the executable and dossier edge surfaces; attempt 0007 repairs it and passes
24 graph checks plus 39 focused tests. Attempt 0008 preserves a multi-path
memory-CLI invocation error before separate record checks pass. The terminal
attempt passes the single repository workflow gate and the separately
prescribed full suite with v0.127.0 and all 163 claims unchanged.

## Debt Ledger

The P170 ledger tracks compatibility, all predicates and assertions, numeric
evidence provenance, inversion information, geometry, dependencies, consumers,
and the governed duplicate record.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Current native execution is known to stop at a removed API name | Preserve the abort and pass an alias-only replay backed by `np.trapezoid` | discharged by attempts 0002 and 0003 |
| Six predicates and assertions lack current individual review | Inventory lexical/runtime/assertion nodes and adjudicate each | discharged by source and check adjudication |
| Effective area may merely invert supplied tension | Eliminate the round trip and mutate inputs and coefficients | discharged by primary and fresh exact routes |
| Penetration-area ratio may be non-discriminating | Map its window, mutate tension, and expose free geometry conventions | discharged by the factor-1000 interval and geometry audit |
| Existing numeric evidence may be rerun ceremonially | Hash-audit P026/P029 and replay only current-sensitive gates | discharged by byte-identical reuse and one canonical solve |
| Physical cross-model identity may be borrowed | Close or reject every field, geometry, scale, QCD, and confinement dependency | discharged by dependency and source adjudication |
| Consumers and governed records may disagree | Replay affected paths and synchronize duplicate disposition, queue, memory, and effort | discharged by 39 focused tests and the duplicate transaction |

## Review and Promotion Plan

Every distinct CF5 predicate receives an individual verdict. Terminal duplicate
closure requires native and alias compatibility evidence, exact information
and scope mapping, mutations, fresh independent derivation, source/dependency/
nonduplication audits, consumers, graph, and materialized adjudication. A new
claim additionally requires importable implementation, tests, impact analysis,
release/registry change, generated documentation, and accepted-memory closure.
Otherwise P170 updates only CF5's duplicate evidence and leaves v0.127.0
unchanged.

Validation and commit are separate processes. Focused scientific gates run
during development, followed by one terminal repository validation, one
separately required full test command, and `git diff --check`. Later
record-only edits trigger record-sensitive validation rather than another full
suite.

## Done Gate

P170 closes as terminal duplicate evidence through unchanged C-VTX-001,
C-VTX-002, and C-FLX-001. The alias replay executes all six predicates; 41
primary and 20 fresh exact checks show that the area and ratio are reversible
transforms without profile geometry; 24 graph checks replay 35 predicates and
six assertions; and 39 focused tests pass. Compatibility aliases occur only
for immutable CF1 and CF5 and are backed by `np.trapezoid`. Physical overreach
is excluded, P026/P029 reuse is hash-justified, v0.127.0 remains unchanged, and
the campaign debt ledger is empty.

## Cross-References

See C-VTX-001, C-VTX-002, C-FLX-001, P026, P027, P029, P167-P169, CF1, CF2,
CF5, `abelian_higgs_vortex.py`, `flux_tube.py`, `numerics.py`, and the parent
migration and NumPy-compatibility efforts.
