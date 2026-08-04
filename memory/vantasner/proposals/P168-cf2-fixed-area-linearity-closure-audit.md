---
description: Reaudit CF2's fixed-area field-energy and endpoint-work closure
author: vantasner
created: '2026-08-10T22:50:00Z'
updated: '2026-08-10T23:20:00Z'
tags:
- substrate-framework
- campaign-proposal
- migration-CF2
- fixed-flux-tube
category: proposals
confidence: established
status: archived
---
# P168 CF2 Fixed-Area Linearity Closure Audit

## Question and Positive Deliverable

P168 must determine whether every scientifically valid CF2 predicate closes
through C-FLX-001 with stored field energy and endpoint work kept distinct.
The positive deliverable is a current claim-level source audit that derives
both slopes, their equality condition, fixed-area sensitivity, geometry
counterexamples, dependencies, consumers, and terminal qualification without
turning generic linearity into physical confinement.

## Base Release and Provenance

The accepted base is v0.127.0 at clean framework commit `61a85bd`, with 163
accepted claims. The source baseline is
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. CF2 is pinned at
`merged-framework/bridges/phase-10/bridge_CF2_linear_potential.py`, SHA-256
`e9651b9d4db9f23bb54d013a419c2f050725063347e63f253a968781598bfe6a`.
Its dossier is pinned at
`merged-framework/bridges/phase-10/dossiers/CF2-dossier.md`, SHA-256
`b88a66e7b4bba4a886ea87d5a88ff6dcaac20ec99b1e9c556198b4c7dc2e79e1`.
Both paths are clean at the pinned source commit; unrelated predecessor dirt is
excluded.

CF2 is already qualified through P027 and accepted C-FLX-001. P027, the
registry, memory, generated queue, and P167 graph replay expose or execute its
fifteen checks, constant-field line, energy/work coefficient mismatch, and
physical exclusions. P168 therefore claims no fresh source or comparator
blinding and audits the existing result rather than trusting its tally.

## Invariants, Conventions, and Allowed Imports

Positive flux `Phi`, cross-section `A`, endpoint charge `q`, and length `L` are
independent inputs. Uniform cap flux gives `E=Phi/A`. Declared energy density
`E^2/2` gives stored-energy slope `Phi^2/(2A)`; declared endpoint force `qE`
gives work slope `qPhi/A`. They agree only when `q=Phi/2`. Fixed area and
uniformity are premises, and variable-area or spherical spreading must remain
counterexamples.

C-VTX-001/002 are separate vortex results and provide no ideal area or charge
map. C-MAX-001 supplies only a separately normalized radial-spreading
comparison. C-WIL-001 derives a line only after an area-law expectation is
declared; it does not derive that law. P027's immutable evidence and the pure
`flux_tube.py` API are allowed. No quark, QCD, Riesz, confinement, empirical
tension, or substrate premise is allowed.

Compatibility is scientifically neutral. CF2 and the canonical module have
no executable NumPy integration surface and P167 already replayed CF2 natively.
Mutable P168 code uses current or exact APIs; any unexpected environment abort
is preserved and repaired before scientific adjudication rather than counted
against a candidate.

## Candidate Preregistration

The candidates separate literal replay, accepted closure, reduced exact scope,
possible geometry novelty, cross-model identification, physical overreach,
Riesz narrative, and governance completion.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal CF2 replay | Hash-pinned source conventions | Source-declared symbols | Should pass natively but may conflate meanings | Fifteen-predicate and assertion audit |
| B | Accepted C-FLX-001 closure | Explicit uniform fixed-area energy and force laws | `Phi,A,q,L` | Expected exact nonduplicative closure | Exact source/API comparison and iff audit |
| C | Energy-only closure | Endpoint work fails provenance or coefficient checks | `Phi,A,L` | Retains a narrower positive theorem | Separate volume-energy and work derivations |
| D | New geometry-family theorem | A reusable exact gap survives | Variable area function | Disfavored if accepted statement already contains decisive counterfamilies | Registry/API/consumer gap audit |
| E | CF1 composition | Derived map from vortex profile/flux/tension to ideal `A,q,Phi` | Additional mapping data | Expected absent | Dependency and normalization audit |
| F | Physical QCD confinement | Quark charge, chromoelectric tube, area law, sector map | Physical data | Expected conflict | Nonperturbative dependency and oracle audit |
| G | Riesz explanation | Derived operator and dimension map | Fractional operator inputs | Expected narrative-only | Executable dependency and exponent audit |
| H | Governance closure | Accepted authority order | None | Qualified disposition remains synchronized | Source, claim, queue, memory, release, and consumer replay |

## Selection Criteria and Blinding

Selection is ordered by energy/work definition separation, sensitivity to the
one-half, charge, flux, and area powers, fixed-area visibility and geometry
limits, dependency and physical-interpretation closure, assumption and API
economy, consumers, compatibility, and governance. Numerical or empirical
proximity cannot select a candidate. Prior formula and execution exposure is
recorded; no fresh blinding is claimed.

## Proposed Claim Delta

No claim is proposed at freeze. Candidate B is expected because C-FLX-001 was
accepted from CF2 and already states both slopes, their exact iff, variable-area
and spherical counterexamples, effective-area reconstruction ceiling, and
physical exclusions. A delta requires a distinct exact object and complete
dependency, nonduplication, mutation, consumer, and review closure.

## Implementation and Oracle Plan

The primary route will inventory CF2's imports, fifteen lexical and runtime
checks, assertion, formulas, inputs, terminology, and compatibility surface.
SymPy exact integration, differentiation, solving, dimensions, and limits fit
all scientific obligations. It will mutate the energy one-half, charge, flux,
area power, fixed-area premise, and any equality shortcut. Variable area and
spherical spreading supply countermodels.

A fresh exact review will derive stored energy by volume integration and
endpoint work by distance integration without importing `flux_tube.py`.
P027's byte-identical verifier and independent review will be reused when
their hashes and assumptions match; current source, canonical API, source
graph, and focused consumers are replayed proportionately. Exact printed
formatting is never an oracle. Source-graph inventories keep lexical checks,
runtime checks, and assertions separate and classify narrative edges without
granting them authority.

## Attempts and Continuation

Attempt 0001 freezes the contract before P168 opens CF2 or its dossier and
discloses P027/P167 exposure. It records base release and commit, source and
dossier hashes, eight candidates, structural criteria, accepted-composition
route, and native compatibility preflight. Every later implementation,
representation, source, schema, or scientific failure is preserved
append-only before repair. Attempt 0002 validates repository schema, proposal
memory, campaign YAML, and diff shape and pins the freeze manifest hash before
renewed source-body access. Attempt 0003 preserves a workflow-ordering mistake
in the freeze commit invocation; attempt 0004 independently verifies the
committed tree before source access. Attempt 0005 reproduces all fifteen source
predicates natively. Attempts 0006 and 0007 pass 39 primary and 19 fresh exact
checks. Attempt 0008 passes 31 graph checks and 43 focused tests over the
accepted and adjacent consumer surface. Attempt 0009 preserves a record
preflight whose multi-path memory invocation failed and whose shell status was
masked by later commands; the repaired route validates each path separately
under fail-fast execution. Attempt 0010 passes that repair. Attempt 0011 passes
the terminal repository gate and both prescribed 1,478-test executions with
v0.127.0 and all 163 accepted claims unchanged.

## Debt Ledger

The P168 ledger tracks every source predicate, slope definition, coefficient,
geometry premise, dependency, compatibility event, consumer, and governed
record.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Fifteen predicates and one assertion lack current individual review | Reproduce, inventory, and adjudicate every node | discharged by source reproduction and check adjudication |
| Energy and endpoint work may share an unjustified sigma | Derive both slopes and exact equality condition independently | discharged by 39 primary and 19 independent checks |
| Fixed area may be hidden | Mutate it and retain variable-area and spherical counterexamples | discharged by coefficient, geometry, logarithmic, and spherical guards |
| Existing evidence may be rerun ceremonially | Hash-audit P027 and replay only changed or current-sensitive gates | discharged by byte-identical accepted-evidence reuse |
| CF1, Riesz, Wilson, QCD, and confinement identities may be borrowed | Close or reject every narrative dependency explicitly | discharged by dependency, source, graph, and source adjudication |
| Consumers and governed records may disagree | Replay affected paths and synchronize disposition, queue, memory, and effort | discharged by 43 focused tests and qualification transaction |

## Review and Promotion Plan

Every distinct CF2 predicate receives an individual verdict. Accepted
composition requires native reproduction, exact scope mapping, mutations,
fresh independent derivation, source/dependency/nonduplication audits,
consumers, graph, and materialized adjudication. A new claim additionally
requires an importable API, tests, impact analysis, release/registry update,
generated documentation, and accepted-memory synchronization. Otherwise P168
updates only CF2's qualification evidence and leaves v0.127.0 unchanged.

Validation and commit are separate processes. Focused scientific gates run
during development, followed by one terminal repository validation, one
separately required full test command, and `git diff --check`. Later record-only
edits trigger record-sensitive validation rather than another full suite.

## Done Gate

P168 closes through unchanged C-FLX-001 composition. Both positive conditional
linear constructions and their exact distinction pass 39 primary and 19 fresh
exact checks. All fifteen source predicates and the assertion have individual
verdicts; 31 graph checks replay 66 lexical and runtime predicates plus eight
assertions; and 43 focused tests pass. Compatibility aliases occur only for
immutable CF1 and CF5 and are backed by `np.trapezoid`. Physical overreach is
excluded, P027 reuse is hash-justified, v0.127.0 remains unchanged, and the
campaign debt ledger is empty.

## Cross-References

See C-FLX-001, C-VTX-001, C-VTX-002, C-MAX-001, C-WIL-001, P027, P167, CF1,
CF2, CF5, EM3, EM7, QCD3, `flux_tube.py`, and the parent migration effort.
