---
description: Reproduce CF1 under current NumPy and audit its accepted vortex closure
author: vantasner
created: '2026-08-10T22:12:00Z'
updated: '2026-08-10T22:16:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-CF1
- abelian-higgs-vortex
- numpy-compatibility
category: proposals
confidence: exploratory
status: active
---
# P167 CF1 Current-NumPy Closure Audit

## Question and Positive Deliverable

P167 must reproduce hash-pinned CF1 under the installed NumPy and determine
whether every scientifically valid source predicate is exactly closed by
C-VTX-001 and C-VTX-002. The positive deliverable is a current-environment,
claim-level audit with compatibility separated from physics, all source checks
individually classified, accepted APIs and consumers replayed proportionately,
and CF1's qualified disposition synchronized without duplicate claims or
physical overreach.

## Base Release and Provenance

The accepted base is v0.127.0 at clean framework commit `fcaa685`, with 163
accepted claims. The source baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. CF1 is pinned at
`merged-framework/bridges/phase-10/bridge_CF1_dual_superconductor_flux_tube.py`,
SHA-256 `a4ec97923804f1b7c624b7619bc6b6a1cbb62f42d659897799545b257ca33f5d`.
Its dossier is pinned at
`merged-framework/bridges/phase-10/dossiers/CF1-dossier.md`, SHA-256
`b0f1d6abc6d37410a6258a1411061c3fe9889c68b2f0314dc3fdd38c19ebadcc`.
Those two paths are clean at the pinned source commit; unrelated predecessor
worktree changes are excluded from P167.

CF1 is already qualified in the generated queue through P026 and accepted
C-VTX-001/C-VTX-002. P026, P027, the registry, durable memory, and the queue
already expose the equations, numerical tension, eight-check headline,
physical exclusions, and native `np.trapz` abort. P167 therefore claims no
fresh source or comparator blinding. It audits and reproduces the existing
result rather than treating chronology or a prior pass tally as authority.

## Invariants, Conventions, and Allowed Imports

C-VTX-001 owns the declared convention
`phi=f(r) exp(i*n*theta)`, `A_theta=a(r)/(g*r)`, its radial functional,
Euler-Lagrange equations, finite-energy condition, flux, and inverse lengths.
C-VTX-002 owns only resolution-bounded evidence for the explicitly stated
parameter, domain, boundary, solver, residual, quadrature, and refinement
family. Neither claim supplies a substrate, dual, chromoelectric, QCD,
confinement, continuum-existence, uniqueness, or absolute-scale identity.

C-DIM-007 is allowed only as a dimensional ceiling. C-FLX-001 remains a
separate fixed-area uniform-field theorem; P167 cannot equate its field-energy
or endpoint-work slopes to CF1 vortex tension without an explicit accepted
map. The accepted vortex and numerical modules, shared verification and
numerics APIs, immutable P026/P027 evidence, and exact symbolic or status-gated
numeric methods are allowed. No empirical comparator or fitted constant is an
input.

Compatibility is frozen as scientifically neutral. Mutable P167 code will use
`np.trapezoid` or canonical `trapezoid_integral`, never `np.trapz`. Immutable
CF1 may receive only a process-local `np.trapz = np.trapezoid` alias when the
old name is absent. The unmodified native abort and the repaired replay are
both recorded; the abort cannot reject or select a scientific candidate.

## Candidate Preregistration

The candidates distinguish literal reproduction, accepted closure, numerical
fallback, genuine novelty, overbroad interpretation, cross-model composition,
and governance completion.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal alias-only CF1 replay | Hash-pinned source and isolated compatibility alias | Source-declared inputs | Should recover the source tally without changing scientific semantics | Native-versus-alias process replay plus check/assertion audit |
| B | Accepted C-VTX-001/C-VTX-002 composition | Exact claim scopes and immutable reviewed evidence | Already declared model and numerical data | Expected natural closure with no new API | Source-to-claim coverage and nonduplication audit |
| C | Exact-only closure | Numerical predicates fail scientifically after compatibility repair | Symbolic model parameters | Retains C-VTX-001 while reopening numeric debt | Solver-status, residual, boundary, and regression gates |
| D | New vortex claim or API | A distinct reusable invariant survives outside accepted scope | Any newly exposed input | Disfavored if accepted modules already own the object | Registry, module, and consumer gap audit |
| E | Physical dual-superconductor or confinement reading | An accepted substrate/QCD map and nonperturbative oracle | Physical sector data | Expected conflict with accepted interpretation boundaries | Dependency closure and physical oracle audit |
| F | Composition with C-FLX-001 | Explicit charge, flux, area, and work-energy map | Additional independent quantities | Remains separate unless the map is derived | Dimensional, normalization, and dependency audit |
| G | Governance closure | Accepted authority order and hash-pinned evidence | None | Qualified disposition and current records agree | Source, claim, queue, release, docs, memory, and consumer replay |

## Selection Criteria and Blinding

Selection is ordered by exact functional/ansatz/coupling convention closure,
compatibility-neutral predicate replay, solver-status and residual evidence,
independent-evidence provenance, mutation sensitivity and known limits,
interpretation boundaries, assumption and parameter economy, API
nonduplication, downstream separation, and governance closure. The already
exposed tension or terminal tally cannot select a candidate. The contract is
committed before renewed CF1 or dossier body inspection and current execution,
but no fresh source or value blinding is claimed.

## Proposed Claim Delta

No claim is proposed at freeze. Candidate B is the expected closure because
C-VTX-001 and C-VTX-002 were accepted specifically from CF1 and their APIs
remain importable. P167 may propose a delta only if a distinct source object
survives exact scope, dependency, nonduplication, mutation, consumer, and
independent-review gates. It does not challenge or supersede an accepted claim.

## Implementation and Oracle Plan

The primary route will inventory CF1's lexical checks, runtime executions,
assertions, imports, equations, inputs, solver setup, quadrature, and headline
predicates. It will preserve the native compatibility abort, then run the same
immutable source in an isolated process with the missing legacy name aliased
only to `np.trapezoid`. AST and runtime probes will show that mutable P167 and
canonical scientific modules contain no executable legacy access and that the
alias changes only name availability.

SymPy fits exact variation, finite-energy, flux, inverse-length, convention,
and limiting-case obligations. NumPy/SciPy evidence is status-gated and never
upgraded beyond C-VTX-002. Because P026 already supplies expensive refinement
and an independent finite-difference route, P167 will hash-audit and reuse that
immutable evidence when assumptions and code match, run current source and
focused accepted consumers once, and avoid repeating the unchanged full
refinement matrix as validation theater. A scientific mismatch, changed hash,
or failed current solver gate reopens the appropriate exact or numeric attempt.

The source graph will count lexical check sites, runtime check executions, and
assertions separately. Mutations cover missing compatibility alias, equation
sign/coupling convention, asymptotic gauge boundary, zero vacuum limit,
quadrature result sensitivity, and physical-label overreach. Release, claim,
generated-doc, memory, and queue changes remain conditional on the actual
claim delta; an unchanged accepted composition does not manufacture a release.

## Attempts and Continuation

Attempt 0001 freezes P167 with the source body unopened by this campaign and
with extensive prior exposure disclosed. It records exact framework, source,
dossier, module, and adjudication provenance, seven candidates, structural
criteria, the compatibility-neutral replay policy, and the validation debt.
Every later compatibility, implementation, numerical, schema, or scientific
failure is preserved append-only before repair with the next viable candidate
named. Attempt 0002 validates the repository, proposal memory, campaign YAML,
and diff shape and pins the frozen manifest hash before source-body access.

## Debt Ledger

The P167 ledger tracks compatibility, all CF1 predicate semantics, accepted
claim coverage, numerical-evidence provenance, conventions, physical scope,
dependencies, consumers, generated state, and terminal disposition.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Current CF1 execution stops at a removed API name | Preserve native abort and pass alias-only replay backed by `np.trapezoid` | open |
| Eight source checks and two assertions lack a fresh individual audit | Inventory lexical/runtime/assertion nodes and adjudicate each | open |
| Existing accepted composition may hide convention or numerical mismatch | Match source inputs and predicates to C-VTX-001/C-VTX-002 and P026 evidence | open |
| Revalidation may duplicate expensive settled evidence | Hash-audit immutable evidence and rerun only changed or current-environment-sensitive gates | open |
| Physical dual/QCD/confinement language may exceed dependency closure | Exclude it or provide separately accepted map and oracle | open |
| Consumers and governed records may disagree | Replay affected APIs and synchronize disposition, queue, memory, and proposal | open |

## Review and Promotion Plan

Every distinct CF1 predicate receives an individual verdict. Accepted
composition requires native/alias compatibility evidence, current source
reproduction, exact claim-scope mapping, numerical status discipline,
immutable independent-evidence audit, nonduplication, consumers, source graph,
and materialized source adjudication. A new claim additionally requires an
importable implementation, tests, impact analysis, independent review, release
and registry changes, generated documentation, and accepted-memory closure.
Otherwise P167 updates only CF1's durable qualification evidence and leaves
v0.127.0 unchanged.

Validation and commit are separate process invocations. P167 runs focused
scientific verifiers and affected tests during development, then one terminal
`scripts/validate.sh`, one separately required full `pytest`, and
`git diff --check`. Final record edits trigger only record-sensitive validation
unless they alter code or claims.

## Done Gate

P167 closes only when current NumPy reproduces the positive conditional vortex
object, every CF1 predicate has an individual claim-level verdict, the accepted
composition or justified delta passes its strongest appropriate oracle,
version compatibility cannot masquerade as science, all consumers and records
agree, and the debt ledger is empty. A compatibility repair, native pass tally,
failed physical interpretation, or preserved no-go alone is not completion.

## Cross-References

See C-DIM-007, C-VTX-001, C-VTX-002, C-FLX-001, P026, P027, CF1, CF2-CF4,
M1, M2, `abelian_higgs_vortex.py`, `numerics.py`, and the parent
framework-migration and NumPy-compatibility efforts.
