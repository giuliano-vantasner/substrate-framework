---
description: Separate coherent occupation support from compact phase vertices and classical cosine vacua
author: vantasner
created: '2026-08-11T22:10:00Z'
updated: '2026-08-11T22:12:00Z'
tags:
- substrate-framework
- research-arc
- migration-MD3
- vertex-operator
- coherent-state
category: proposals
confidence: exploratory
status: active
---
# P198 MD3 Vertex Operator Audit

## Question and Positive Deliverable

P198 must deliver the strongest exact importable vertex-operator theorem that
survives with its Hilbert space, state, normalization, ordering, and parameters
declared. It must decide whether MD3 distinguishes a Weyl displacement, a
compact-phase multiplication vertex, and an ordered exponential, and must keep
unbounded Fock occupation support separate from classical phase amplitude and
the vacuum set of a cosine potential. A no-go for MD3's physical reading is
attempt evidence, not completion.

## Base Release and Provenance

The accepted base is v0.146.0 at framework commit `1fa3711`. The source
baseline is `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`;
MD3 is the pending candidate unit at
`merged-framework/bridges/phase-38/bridge_MD3_vertex_operator_removes_the_single_vacuum_bound.py`,
hash `2c50b4cacb8746a35f99c26d9f0edd0227314ab9410677aebc54c29812daf128`.
Its six declared predecessors are terminal, but only C-SG-019, C-SPN-002,
C-OSC-001, C-CMB-003, and C-OSC-002 have accepted authority; PN2 has no
accepted mapping.

The bundled memory searches returned no authoritative MD3 theorem. Unrelated
personal records are not imported. The accepted claim entries and canonical
`bosonic_fock`, `cosine_vertices`, and `symmetric_spin` modules were verified
at source before reuse.

## Invariants, Conventions, and Allowed Imports

C-SG-019 and C-OSC-002 remain classical cosine and amplitude-convention
claims. C-OSC-001 supplies a mathematical one-mode Fock ladder, while
C-CMB-003 supplies a normalized factorial-one mathematical mass; neither
prepares a coherent state or supplies a physical Poisson process. C-SPN-002 is
a distinct finite collective SU2 system. A Weyl displacement and a compact
phase multiplier live on separately declared Hilbert spaces. Occupation number,
Fourier label, classical excursion, and potential-vacuum count are not aliases.
Mutable numeric probes use `numpy.trapezoid` or the shared helper.

## Candidate Preregistration

Five candidates separate the operator families and the no-change alternatives
before renewed source execution.

| Candidate | Description | Assumptions | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- |
| A | Weyl displacement and coherent-state occupation theorem | one-mode Fock vacuum and complex alpha | compatible composition of C-OSC-001 and C-CMB-003 if distinct | BCH, normalization, eigenstate, and raw coefficient rederivations |
| B | Compact-phase multiplication vertex and Fourier translation | L2 circle, Haar measure, integer charge | native independent mathematical object | unitary action, periodicity, and pointwise density preservation |
| C | Ordered or pure-creation exponential | explicit ordering and normalization | compatible only when not conflated with A | compare coefficients, norms, and conjugation |
| D | No new claim beyond accepted Fock and factorial-one results | no added premise | selected if composition is only renaming | exact nonduplication audit |
| E | Foundational quantized-medium revision | independent accepted inconsistency and migration map | predicted unnecessary | foundation trigger and two-repair audit |

## Selection Criteria and Blinding

Selection prioritizes exact domain and normalization, natural framework fit,
operator-ordering honesty, independent derivation, mutation sensitivity,
distinction among occupation, Fourier, and configuration support, novelty, and
usefulness without physical overreach. Numerical proximity selects nothing.

MD3's 41-check result was already exposed in the P191 and P192 reverse-
consumer graphs. No fresh blinding is claimed. This contract freezes operator
families, imports, criteria, mutations, and ceilings before any renewed P198
execution, detailed predicate audit, comparison-value inspection, or
implementation.

## Proposed Claim Delta

P198 reserves provisional identifier C-VOP-001 for a distinct exact vertex-
operator result if Candidate A, B, or their carefully typed separation is not
already covered. Expected dependencies are C-OSC-001 and C-CMB-003 for a Weyl
composition. C-SG-019, C-OSC-002, and C-SPN-002 are comparison ceilings. MD4,
MD5, and MD6 remain individually pending.

## Implementation and Oracle Plan

Any reusable operator definitions and ledgers will live under
`src/substrate_framework/` with pure imports. SymPy and finite exact matrices
will check BCH consequences, coefficients, norms, eigenvalue recurrences,
Fourier translation, and mutations. An independent derivation will start from
raw series or finite coefficients rather than the canonical API. Domain and
truncation statements will remain explicit. Sampled integration, if genuinely
needed, uses `numpy.trapezoid`, declares its grid and error, and remains numeric
evidence only.

Compatibility preflight scans direct, imported, and dynamic legacy trapezoid
access including eager nested defaults. Mutable code uses the current API;
immutable source receives an alias-only replay if necessary, and a version
event never counts as scientific rejection. Source graph replay pins lexical
checks, runtime checks, dependencies, and reverse consumers separately.

## Attempts and Continuation

Attempts are append-only. Attempt 0001 preserves the initial contract-schema
failure: the proposal used an ungoverned status enum and two memory table
sections lacked prose lead-ins. Attempt 0002 repairs only that representation,
validates the durable contract, proposal, provenance, and formula freeze, and
does not select a scientific candidate. A failed scientific route must identify
whether the fault is implementation, representation, operator choice, target,
or foundation and then continue without lowering the bar.

## Debt Ledger

The ledger tracks every conflation that could turn an exact state identity
into an unsupported physical claim.

| Debt | Discharge | Status |
| --- | --- | --- |
| Prior MD3 execution prevents fresh blinding | Preserve P191/P192 exposure and freeze before renewed P198 work | discharged by validated attempt 0002 |
| Vertex terminology can conflate distinct operators | Type every Hilbert space, operator, domain, and state | open |
| Gaussian normalization and ordering are load bearing | Independently derive BCH coefficients and mutate the half factor | open |
| Factorial-one mass may be called a physical probability or rate | Require preparation and observable semantics; retain the mathematical ceiling | open |
| Occupation support may be confused with classical vacua | Give explicit countermodels and support taxonomy | open |
| Claim may duplicate C-OSC-001 or C-CMB-003 | Complete claim-level nonduplication review | open |
| Downstream consumers may inherit MD3 wholesale | Replay exact graph and preserve individual dispositions | open |

## Review and Promotion Plan

Any proposed claim and MD3 receive separate reviews. Promotion requires exact
primary and independent routes, load-bearing mutations, package tests, source
and consumer replay, a terminal MD3 disposition, one integrated gate at the
unchanged promotion boundary, synchronized generated records, and an empty
ledger. Campaign migration to `campaigns/` occurs only after adjudication.

## Done Gate

P198 closes only when a positive importable object exists, premises and
dependency closure are explicit, competing concepts are adjudicated, strong
oracles and mutations pass, every affected consumer replays, claim and source
reviews agree, generated records synchronize, and the debt ledger is empty.
